from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """
    Base interface for LLM providers.

    Current free/local:
    - Ollama local models: llama3, gemma3

    Future deploy:
    - OpenAI
    - Claude
    - Gemini
    - Ollama cloud models if needed
    """

    @abstractmethod
    def health_check(self) -> dict:
        pass

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str | None = None) -> dict:
        pass