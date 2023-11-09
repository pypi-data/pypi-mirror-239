import abc
import typing as t
import json
import time
import statistics
from pydantic import BaseModel, Extra
from polyglotlm.models import (
  LLM, Messages, Functions, map_context_size, map_role_for_prompt,
  ChatRole, GenerationOutput,
)

class Schema(BaseModel):
  model: LLM
  messages: Messages
  max_tokens: t.Optional[int] = None
  temperature: t.Optional[float] = None
  functions: t.Optional[Functions] = None
  n: t.Optional[int] = None
  top_p: t.Optional[float] = None
  frequence_penalty: t.Optional[float] = None
  presence_penalty: t.Optional[float] = None
  stop: t.Optional[t.Union[str, t.List[str]]] = None
  user: t.Optional[str] = None

  timeout: t.Optional[float] = None

def basic_statistics(lst):
  max_value = max(lst)
  min_value = min(lst)
  avg_value = statistics.mean(lst)
  median_value = statistics.median(lst)
  return {
    'min': min_value, 'max': max_value,
    'avg': avg_value, 'median': median_value,
  }

class BaseProvider(Schema, extra=Extra.allow, arbitrary_types_allowed=True):
  _attrs = {
    'parameters': {},
    'timings': {'response_time': None, 'first_event_time': None, 'next_events_times': []},
    'last_exception': None,
  }

  def __init__(self, **kwargs):
    super(BaseProvider, self).__init__(**kwargs)
    self.clean_parameters()
    return

  @property
  def last_exception(self):
    return self._attrs['last_exception']

  @last_exception.setter
  def last_exception(self, exc):
    self._attrs['last_exception'] = exc

  def clean_parameters(self):
    self._attrs['parameters'] = json.loads(self.json(exclude={'_attrs', 'retry'}))
    keys = list(self._attrs['parameters'].keys())
    for k in keys:
      if self._attrs['parameters'][k] is None:
        self._attrs['parameters'].pop(k)
    return

  def refresh_timings(self):
    self._attrs['timings'] = {'response_time': None, 'first_event_time': None, 'next_events_times': []}
    return

  def set_response_time(self, nr_seconds):
    self._attrs['timings']['response_time'] = nr_seconds
    return

  def set_first_event_time(self, nr_seconds):
    self._attrs['timings']['first_event_time'] = nr_seconds
    return

  def append_next_event_time(self, nr_seconds):
    self._attrs['timings']['next_events_times'].append(nr_seconds)
    return

  def print_timings(self):
    response_time = self._attrs['timings']['response_time']
    first_event_time = self._attrs['timings']['first_event_time']
    next_events_times = self._attrs['timings']['next_events_times']
    stats1 = basic_statistics(next_events_times)
    print(f"Response time: {response_time:.3f}s")
    print(f"First event time: {first_event_time:.3f}s")
    print((
        f"Next event time: "
        f"min={stats1['min']:.3f}s | "
        f"avg={stats1['avg']:.3f}s | "
        f"median={stats1['median']:.3f}s | "
        f"max={stats1['max']:.3f}s"
    ))
    return

  @property
  def cleaned_parameters(self):
    return self._attrs['parameters']

  @property
  def messages_to_prompt(self):
    prompt = ""
    for m in self.messages:
      prefix = map_role_for_prompt[m.role]
      prompt += f"{prefix}: {m.content}\n\n"

    prompt += f"{map_role_for_prompt[ChatRole.ASSISTANT]}:\n"
    return prompt

  @property
  def prompt_nr_characters(self):
    return len(self.messages_to_prompt)

  def get_stream(self):
    start = time.time()
    # TODO response could be none??
    response = self.get_response()
    end = time.time()

    self.set_response_time(end-start)

    i = -1
    start = time.time()
    for event in response:
      # TODO event can be None??
      i+=1
      end = time.time()
      if i == 0:
        self.set_first_event_time(end-start)
      else:
        self.append_next_event_time(end-start)
      start = time.time()
      yield i,event

  @abc.abstractmethod
  def get_response(self) -> t.Any:
    pass

  @abc.abstractmethod
  def get_generation_output(self, event) -> GenerationOutput:
    pass

  def get_timeout_params(self):
    return
