import asyncio
import time

from google import genai
from google.genai import errors

from app.core.config import settings
from app.providers.base import LLMProvider, LLMResponse


class GeminiProvider(LLMProvider):

    DEFAULT_MODEL = "gemini-3.6-flash"

    MAX_RETRIES = 3
    RETRY_DELAYS = (1, 2, 4)

    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    async def generate(
        self,
        prompt: str,
        model: str | None = None,
    ) -> LLMResponse:

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        selected_model = model or self.DEFAULT_MODEL

        start_time = time.perf_counter()

        response = await self._generate_with_retry(
            prompt=prompt,
            model=selected_model,
        )

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        usage = response.usage_metadata

        input_tokens = (
            usage.prompt_token_count
            if usage
            else 0
        )

        output_tokens = (
            usage.candidates_token_count
            if usage
            else 0
        )

        return LLMResponse(
            output=response.text or "",
            model=selected_model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            cost=0.0,
        )

    async def _generate_with_retry(
        self,
        prompt: str,
        model: str,
    ):
        last_error = None

        for attempt in range(self.MAX_RETRIES + 1):

            try:
                return await self.client.aio.models.generate_content(
                    model=model,
                    contents=prompt,
                )

            except errors.ServerError as exc:
                last_error = exc

                if attempt >= self.MAX_RETRIES:
                    break

                delay = self.RETRY_DELAYS[attempt]

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {delay}s..."
                )

                await asyncio.sleep(delay)

            except errors.ClientError as exc:
                status_code = getattr(
                    exc,
                    "status_code",
                    None,
                )

                if status_code == 429:
                    raise RuntimeError(
                        "Gemini rate limit or quota exceeded."
                    ) from exc

                if status_code == 404:
                    raise RuntimeError(
                        f"Gemini model '{model}' "
                        "was not found or is unavailable."
                    ) from exc

                raise RuntimeError(
                    f"Gemini request was rejected "
                    f"(status {status_code})."
                ) from exc

            except Exception as exc:
                raise RuntimeError(
                    "Unexpected error while calling Gemini."
                ) from exc

        raise RuntimeError(
            "Gemini service remained unavailable "
            f"after {self.MAX_RETRIES} retries."
        ) from last_error