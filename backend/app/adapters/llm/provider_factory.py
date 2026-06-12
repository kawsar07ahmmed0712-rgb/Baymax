from app.adapters.llm.base import BaseLLMProvider
from app.adapters.llm.ollama_provider import OllamaProvider
from app.adapters.llm.openai_provider import OpenAIProvider
from app.core.config import settings


def get_llm_provider() -> BaseLLMProvider:
    """
    Select LLM provider based on .env.

    Current:
    LLM_PROVIDER=ollama

    Future:
    LLM_PROVIDER=openai
    """

    provider = settings.llm_provider.lower().strip()

    if provider == "ollama":
        return OllamaProvider()

    if provider == "openai":
        return OpenAIProvider()

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")