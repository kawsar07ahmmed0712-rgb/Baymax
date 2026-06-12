from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from app.adapters.llm.base import BaseLLMProvider
from app.core.config import settings


class OllamaProvider(BaseLLMProvider):
    """
    Local Ollama LLM provider.

    This keeps Baymax fully free/local.
    Example models:
    - llama3:latest
    - gemma3:4b
    - gemma3:1b
    """

    def __init__(self):
        self.model_name = settings.ollama_model
        self.base_url = settings.ollama_base_url

        self.model = ChatOllama(
            model=self.model_name,
            base_url=self.base_url,
            temperature=0.2,
        )

    def health_check(self) -> dict:
        try:
            response = self.model.invoke(
                [
                    SystemMessage(content="You are a health check assistant."),
                    HumanMessage(content="Reply with only: ok"),
                ]
            )

            return {
                "ok": True,
                "provider": "ollama",
                "model": self.model_name,
                "base_url": self.base_url,
                "response": response.content.strip(),
            }

        except Exception as exc:
            return {
                "ok": False,
                "provider": "ollama",
                "model": self.model_name,
                "base_url": self.base_url,
                "error": str(exc),
            }

    def generate(self, prompt: str, system_prompt: str | None = None) -> dict:
        try:
            messages = []

            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))

            messages.append(HumanMessage(content=prompt))

            response = self.model.invoke(messages)

            return {
                "ok": True,
                "provider": "ollama",
                "model": self.model_name,
                "text": response.content.strip(),
            }

        except Exception as exc:
            return {
                "ok": False,
                "provider": "ollama",
                "model": self.model_name,
                "text": None,
                "error": str(exc),
            }