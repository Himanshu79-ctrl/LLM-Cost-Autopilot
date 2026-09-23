from app.providers.base import LLMProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.groq_provider import GroqProvider
from app.providers.openai_provider import OpenAIProvider


class ProviderManager:

    def __init__(self):
        self._providers: dict[str, LLMProvider] = {}

    def get_provider(
        self,
        provider_name: str,
    ) -> LLMProvider:

        if provider_name in self._providers:
            return self._providers[provider_name]

        provider = self._create_provider(provider_name)

        self._providers[provider_name] = provider

        return provider

    def _create_provider(
        self,
        provider_name: str,
    ) -> LLMProvider:

        if provider_name == "gemini":
            return GeminiProvider()

        if provider_name == "groq":
            return GroqProvider()

        if provider_name == "openai":
            return OpenAIProvider()

        raise ValueError(
            f"Unsupported provider: {provider_name}"
        )