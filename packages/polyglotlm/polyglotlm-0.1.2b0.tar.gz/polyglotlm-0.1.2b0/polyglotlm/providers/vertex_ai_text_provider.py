import os
from time import time

from polyglotlm.providers.base_provider import BaseProvider, GenerationOutput, LLM
from decouple import config
import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.preview.language_models import TextGenerationModel as PreviewTextGenerationModel

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config("GOOGLE_APPLICATION_CREDENTIALS")
vertexai.init()

class VertexAITextProvider(BaseProvider):

  def __init__(self, **kwargs):
    super(VertexAITextProvider, self).__init__(**kwargs)
    if self.model == LLM.PALM_TEXT_BISON_32K:
      vertex_class = PreviewTextGenerationModel
    else:
      vertex_class = TextGenerationModel

    self._attrs['text_generation_model'] = vertex_class.from_pretrained(self.model.value)
    return

  @property
  def request_params(self):
    params = {"prompt": self.messages_to_prompt}

    if self.max_tokens is not None:
      params['max_output_tokens'] = self.max_tokens

    if self.temperature is not None:
      params['temperature'] = self.temperature

    return params

  def get_response(self):
    response = self._attrs['text_generation_model'].predict_streaming(**self.request_params)
    return response

  def get_generation_output(self, event) -> GenerationOutput:
    kwargs = {
      'content': event.text,
    }

    return GenerationOutput(**kwargs)

  def get_timeout_params(self):
    return {
      'start': 5.0,
      'maximum': 20.0,
      'increment': 5.0,
    }
