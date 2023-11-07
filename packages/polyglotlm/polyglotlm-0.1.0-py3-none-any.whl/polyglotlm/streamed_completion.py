import os
import logging
import typing as t
import uuid
import time
import threading
from pydantic import Extra
from tenacity import (
  after_log,
  retry,
  stop_after_attempt,
  wait_exponential,
)
from polyglotlm.providers.base_provider import (
  Schema, BaseProvider, GenerationOutput, FunctionCall,
  process_llm,
)
from polyglotlm.providers.factory import provider_factory
from polyglotlm import logger

class StreamedCompletionInterface(object):
  def __init__(
      self,
      completion_timeout: t.Optional[int] = None,
      request_timeout_start: t.Optional[float] = None,
      request_timeout_max: t.Optional[float] = None,
      request_timeout_increment: t.Optional[float] = None,
      on_first_chunk_callback: t.Optional[t.Callable] = None,
      on_new_chunk_callback: t.Optional[t.Callable] = None,
      on_stop_generation_callback: t.Optional[t.Callable] = None,
      callback_msg_full: t.Optional[bool] = True,
      **llm_params
  ):
    model = llm_params.get('model')
    if model is None:
      raise ValueError("model cannot be None")

    provider_mame, llm = process_llm(model)
    print(f"Using LLM {llm} from provider {provider_mame}")
    llm_params['model'] = llm

    self.completion_timeout = completion_timeout
    self.request_timeout_start = request_timeout_start
    self.request_timeout_max = request_timeout_max
    self.request_timeout_increment = request_timeout_increment
    self.on_first_chunk_callback = on_first_chunk_callback
    self.on_new_chunk_callback = on_new_chunk_callback
    self.on_stop_generation_callback = on_stop_generation_callback
    self.callback_msg_full = callback_msg_full

    self._attrs: t.Dict = {}
    self._attrs['call_id'] = str(uuid.uuid4())
    self._attrs['start_time'] = time.time()
    self._attrs['llm_params'] = llm_params
    self._attrs['provider'] = provider_factory(provider_name=provider_mame, **self.llm_params)
    return

  @property
  def llm_params(self):
    return self._attrs.get('llm_params')

  @property
  def call_id(self):
    return self._attrs.get('call_id')

  @property
  def start_time(self):
    return self._attrs.get('start_time')

  @property
  def provider(self) -> t.Optional[BaseProvider]:
    return self._attrs.get('provider')

  @classmethod
  def create(
      cls,
      completion_timeout: t.Optional[int] = None,
      request_timeout_start: t.Optional[float] = None,
      request_timeout_max: t.Optional[float] = None,
      request_timeout_increment: t.Optional[float] = None,
      on_first_chunk_callback: t.Optional[t.Callable] = None,
      on_new_chunk_callback: t.Optional[t.Callable] = None,
      on_stop_generation_callback: t.Optional[t.Callable] = None,
      callback_msg_full: t.Optional[bool] = True,
      return_instance: t.Optional[bool] = False,
      print_timings: t.Optional[bool] = False,
      **llm_params
  ):
    completion = cls(
      completion_timeout=completion_timeout,
      request_timeout_start=request_timeout_start,
      request_timeout_max=request_timeout_max,
      request_timeout_increment=request_timeout_increment,
      on_first_chunk_callback=on_first_chunk_callback,
      on_new_chunk_callback=on_new_chunk_callback,
      on_stop_generation_callback=on_stop_generation_callback,
      callback_msg_full=callback_msg_full,
      **llm_params,
    )

    output = completion.run()
    if print_timings:
      completion.provider.print_timings()

    if return_instance:
      result = completion, output
    else:
      result = output

    return result

  def _should_stop_prematurely(self) -> bool:
    if self.completion_timeout is None:
      return False

    elapsed = time.time() - self.start_time
    stop = elapsed >= self.completion_timeout
    if stop:
      logger.info(f"Call id {self.call_id} should stop prematurely. Elapsed {elapsed:.1f}s")
    return stop

  @staticmethod
  def compute_request_timeout(
      start,
      maximum,
      attempt_number,
      increment: t.Optional[float] = 1,
  ):

    if any([x is None for x in [start, maximum, attempt_number, increment]]):
      return

    result = start + (increment * (attempt_number - 1))
    return max(0, min(result, maximum))

  @retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=5),
    after=after_log(logger, logging.INFO),
    retry_error_callback=lambda retry_state: None,
  )
  def _streamed_request_with_retry(self) -> t.Optional[GenerationOutput]:
    if self._should_stop_prematurely():
      return

    request_timeout_params = self.provider.get_timeout_params() or {}
    request_timeout = self.compute_request_timeout(
      attempt_number=self._streamed_request_with_retry.retry.statistics['attempt_number'],
      start=self.request_timeout_start or request_timeout_params.get('start'),
      maximum=self.request_timeout_max or request_timeout_params.get('maximum'),
      increment=self.request_timeout_increment or request_timeout_params.get('increment'),
    )

    self.provider.request_timeout = request_timeout
    self.provider.clean_parameters()
    self.provider.refresh_timings()

    try:
      gen_events = self.provider.get_stream()
    except Exception as e:
      self.provider.last_exception = e
      logger.error(f"Exception for `get_stream` {e}")
      raise e

    generation_output = GenerationOutput()

    try:
      for i, event in gen_events:
        current_out = self.provider.get_generation_output(event)
        finished = current_out.finish_reason is not None
        crt_content = current_out.content
        crt_function_call = current_out.function_call

        generation_output.finish_reason = current_out.finish_reason

        if crt_content is not None:
          if i == 0:
            generation_output.content = ""
          generation_output.content += crt_content
          if i == 0 and self.on_first_chunk_callback is not None:
            self.on_first_chunk_callback(generation_output.content if self.callback_msg_full else crt_content)

          if i > 0 and self.on_new_chunk_callback is not None:
            res = self.on_new_chunk_callback(generation_output.content if self.callback_msg_full else crt_content)
            if res:
              break

        elif crt_function_call is not None:
          if i == 0:
            generation_output.function_call = FunctionCall(name=crt_function_call.name, arguments='')
          generation_output.function_call.arguments += (crt_function_call.arguments or '')
        #endif

        if self._should_stop_prematurely() and not finished:
          # do not stop prematurely if it's exactly the last chunk
          return
      #endfor
    except Exception as e:
      self.provider.last_exception = e
      logger.error(f"Exception {e}")
      raise e

    if generation_output.content is not None:
      crt_message = generation_output.content.strip('\n')

      if self.on_stop_generation_callback is not None:
        self.on_stop_generation_callback(crt_message)

    return generation_output

  def run(self):
    logger.info(f"Start call id {self.call_id}")
    output = self._streamed_request_with_retry()

    if output is None:
      logger.info(f"End call id {self.call_id}")
      return

    # output['usage'] = {'prompt_tokens': -1, 'completion_tokens': -1, 'total_tokens': -1}
    # if compute_usage:
    #   # in stream mode the usage is no more provided and it should be computed using tiktoken
    #   # TODO this computation does not take into account the functions!
    #   try:
    #     output['usage']['prompt_tokens'] = num_tokens_from_messages(
    #       messages=messages, model=self._model.value, encoding=tokenizer
    #     )
    #     output['usage']['completion_tokens'] = num_tokens_from_messages(
    #       messages=[{'role': 'assistant', 'content': output['content']}],
    #       model=self._model.value,
    #       encoding=tokenizer
    #     )
    #     output['usage']['total'] = output['usage']['prompt_tokens'] + output['usage']['completion_tokens']
    #   except Exception as e:
    #     logger.error("Could not compute tokens", exc_info=True)
    # # endif

    logger.info(f"End call id {self.call_id}")
    return output
