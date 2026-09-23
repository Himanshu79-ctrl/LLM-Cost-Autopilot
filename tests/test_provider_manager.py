import pytest

from app.providers.manager import ProviderManager
from app.providers.gemini_provider import GeminiProvider
from app.providers.groq_provider import GroqProvider


def test_groq_provider():

    manager = ProviderManager()

    provider = manager.get_provider("groq")

    assert isinstance(provider, GroqProvider)


def test_gemini_provider():

    manager = ProviderManager()

    provider = manager.get_provider("gemini")

    assert isinstance(provider, GeminiProvider)


def test_same_provider_is_reused():

    manager = ProviderManager()

    provider1 = manager.get_provider("groq")
    provider2 = manager.get_provider("groq")

    assert provider1 is provider2


def test_unknown_provider():

    manager = ProviderManager()

    with pytest.raises(ValueError):
        manager.get_provider("unknown")