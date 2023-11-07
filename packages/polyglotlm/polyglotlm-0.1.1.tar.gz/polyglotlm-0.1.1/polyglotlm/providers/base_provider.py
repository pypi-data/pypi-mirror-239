import abc
import typing as t
import json
import time
import statistics
from pydantic import BaseModel, Extra
from enum import Enum

from polyglotlm import logger

class ChatRole(str, Enum):
  SYSTEM = "system"
  USER = "user"
  ASSISTANT = "assistant"

class ProviderName(str, Enum):
  OPENAI = "openai",
  VERTEX_AI_TEXT = "vertex_ai_text"
  AWS_BEDROCK = "aws_bedrock"

  @classmethod
  def from_str(cls, value):
    for item in cls:
      if item.value == value:
        return item
    raise ValueError(f"{value} is not a valid Provider")

dct_role_for_prompt = {
  ChatRole.SYSTEM: "System",
  ChatRole.USER: "Human",
  ChatRole.ASSISTANT: "Assistant"
}

class LLM(str, Enum):
  GPT_3_5_TURBO = "gpt-3.5-turbo"
  GPT_3_5_TURBO_0613 = "gpt-3.5-turbo-0613"
  GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"
  GPT_3_5_TURBO_1106 = "gpt-3.5-turbo-1106" # default 16K
  GPT_4 = "gpt-4"
  GPT_4_0613 = "gpt-4-0613"
  GPT_4_1106_PREVIEW = "gpt-4-1106-preview" # 128K
  ANTROPHIC_CLAUDE_INSTANT_V1 = "anthropic.claude-instant-v1"
  ANTROPHIC_CLAUDE_V2 = "anthropic.claude-v2"
  PALM_TEXT_BISON_32K = "text-bison-32k"

  @classmethod
  def from_str(cls, value):
    for item in cls:
      if item.value == value:
        return item
    raise ValueError(f"{value} is not a valid LLM")

dct_provider_to_llms = {
  ProviderName.OPENAI: [
    LLM.GPT_3_5_TURBO,
    LLM.GPT_3_5_TURBO_0613,
    LLM.GPT_3_5_TURBO_16K,
    LLM.GPT_3_5_TURBO_1106,
    LLM.GPT_4,
    LLM.GPT_4_0613,
    LLM.GPT_4_1106_PREVIEW,
  ],
  ProviderName.AWS_BEDROCK: [
    LLM.ANTROPHIC_CLAUDE_INSTANT_V1,
    LLM.ANTROPHIC_CLAUDE_V2,
  ],
  ProviderName.VERTEX_AI_TEXT: [
    LLM.PALM_TEXT_BISON_32K,
  ]
}

dct_llm_to_provider = {llm: p for p, llms in dct_provider_to_llms.items() for llm in llms}

dct_context_size = {
  LLM.GPT_3_5_TURBO: 4_096,
  LLM.GPT_3_5_TURBO_0613: 4_096,
  LLM.GPT_3_5_TURBO_16K: 16_032,
  LLM.GPT_3_5_TURBO_1106: 16 * 1024,
  LLM.GPT_4: 8_092,
  LLM.GPT_4_0613: 8_092,
  LLM.GPT_4_1106_PREVIEW: 128 * 1024,
  LLM.ANTROPHIC_CLAUDE_INSTANT_V1: 100_000,
  LLM.ANTROPHIC_CLAUDE_V2: 100_000,
  LLM.PALM_TEXT_BISON_32K: 32_768,
}

def process_llm(llm: t.Union[str, LLM]) -> t.Tuple[ProviderName, LLM]:
  provider_name = None
  if isinstance(llm, str):
    str_llm = llm
    if "/" in str_llm:
      str_provider_name, str_llm = str_llm.split("/")
      provider_name = ProviderName.from_str(str_provider_name)

    llm = LLM.from_str(str_llm)
  #endif

  infered_provider_name = dct_llm_to_provider[llm]
  if provider_name is not None and infered_provider_name != provider_name:
    print("Warning!")

  return infered_provider_name, llm


def get_provider_llms(provider_name: t.Union[str, ProviderName]):
  if isinstance(provider_name, str):
    provider_name = ProviderName.from_str(provider_name)

  if provider_name not in dct_provider_to_llms:
    raise ValueError(f"Unknown provider {provider_name}")

  return dct_provider_to_llms[provider_name]

def get_llm_context_size(llm: t.Union[str, LLM]):
  _, llm = process_llm(llm)
  if llm not in dct_context_size:
    raise ValueError(f"Unknown LLM {llm}")

  return dct_context_size[llm]

class ChatMessage(BaseModel):
  role: ChatRole
  content: str

class Function(BaseModel):
  name: str
  parameters: t.Optional[t.Dict] = None
  description: t.Optional[str] = None

class FunctionCall(BaseModel):
  name: t.Optional[str] = None
  arguments: t.Optional[str] = None

class Usage(BaseModel):
  prompt_tokens: t.Optional[int] = None
  completion_tokens: t.Optional[int] = None
  total_tokens: t.Optional[int] = None

class GenerationOutput(BaseModel):
  finish_reason: t.Optional[str] = None
  content: t.Optional[str] = None
  function_call: t.Optional[FunctionCall] = None
  usage: t.Optional[Usage] = None

Messages = t.List[ChatMessage]
Functions = t.List[Function]

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

  request_timeout: t.Optional[float] = None

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
    if self.max_tokens is None:
      self.max_tokens = dct_context_size[self.model]
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
      prefix = dct_role_for_prompt[m.role]
      prompt += f"{prefix}: {m.content}\n\n"

    prompt += f"{dct_role_for_prompt[ChatRole.ASSISTANT]}:\n"
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
