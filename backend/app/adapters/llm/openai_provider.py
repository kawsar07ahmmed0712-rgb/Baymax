from app.adapters.llm.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """
    Placeholder for future paid deployment.

    Later:
    - install langchain-openai
    - add OPENAI_API_KEY
    - replace this placeholder with real OpenAI integration
    """

    def health_check(self) -> dict:
        return {
            "ok": False,
            "provider": "openai",
            "reason": "OpenAI provider is not configured yet.",
        }

    def generate(self, prompt: str, system_prompt: str | None = None) -> dict:
        return {
            "ok": False,
            "provider": "openai",
            "text": None,
            "error": "OpenAI provider is not implemented yet.",
        }