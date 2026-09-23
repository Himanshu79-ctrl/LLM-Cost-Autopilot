import time
from openai import AsyncOpenAI
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

from app.core.config import settings
from app.providers.base import LLMProvider, LLMResponse


class OpenAIProvider(LLMProvider):

    DEFAULT_MODEL = "gpt-5.6-luna"

    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured.")

        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=30.0,
            max_retries=2,
        )

    async def generate(self, prompt: str, model: str | None = None,) -> LLMResponse:

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        selected_model = model or self.DEFAULT_MODEL

        start_time = time.perf_counter()

        try:
            response = await self.client.responses.create(
                model=selected_model,
                input=prompt,
            )

        except AuthenticationError as exc:
            raise RuntimeError(
                "OpenAI authentication failed. "
                "Check your OPENAI_API_KEY."
            ) from exc

        except RateLimitError as exc:
            raise RuntimeError(
                "OpenAI rate limit exceeded. Please try again later."
            ) from exc

        except APITimeoutError as exc:
            raise RuntimeError(
                "OpenAI request timed out."
            ) from exc

        except APIConnectionError as exc:
            raise RuntimeError(
                "Could not connect to OpenAI."
            ) from exc

        except APIStatusError as exc:
            raise RuntimeError(
                f"OpenAI API returned an error: {exc.status_code}"
            ) from exc

        except Exception as exc:
            raise RuntimeError(
                "Unexpected error while calling OpenAI."
            ) from exc

        latency_ms = (time.perf_counter() - start_time) * 1000

        usage = response.usage

        input_tokens = usage.input_tokens if usage else 0
        output_tokens = usage.output_tokens if usage else 0

        return LLMResponse(
            output=response.output_text,
            model=selected_model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            cost=0.0,
        )