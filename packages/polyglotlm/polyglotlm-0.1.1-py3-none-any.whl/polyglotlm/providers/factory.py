import typing as t
from polyglotlm.providers.base_provider import BaseProvider, ProviderName
from polyglotlm.providers.openai_provider import OpenAIProvider
from polyglotlm.providers.aws_bedrock_provider import AWSBedrockProvider
from polyglotlm.providers.vertex_ai_text_provider import VertexAITextProvider

def provider_factory(provider_name, **llm_params) -> t.Optional[BaseProvider]:
  if isinstance(provider_name, str):
    provider_name = ProviderName.from_str(provider_name)

  if provider_name == ProviderName.OPENAI:
    return OpenAIProvider(stream=True, **llm_params)

  if provider_name == ProviderName.AWS_BEDROCK:
    return AWSBedrockProvider(stream=True, **llm_params)

  if provider_name == ProviderName.VERTEX_AI_TEXT:
    return VertexAITextProvider(stream=True, **llm_params)

  return
