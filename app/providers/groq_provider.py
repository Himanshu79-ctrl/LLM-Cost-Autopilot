import asyncio
import time

from groq import AsyncGroq
from groq import APIConnectionError
from groq import APITimeoutError
from groq import APIStatusError
from groq import RateLimitError

from app.core.config import settings
from app.providers.base import LLMProvider, LLMResponse


class GroqProvider(LLMProvider):

    DEFAULT_MODEL = "openai/gpt-oss-20b"

    MAX_RETRIES = 3
    RETRY_DELAYS = (1, 2, 4)

    def __init__(self):
        if not settings.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = AsyncGroq(
            api_key=settings.groq_api_key,
        )

    async def generate(
        self,
        prompt: str,
        model: str | None = None,
    ) -> LLMResponse:

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        selected_model = (
            model or self.DEFAULT_MODEL
        )

        start_time = time.perf_counter()

        response = await self._generate_with_retry(
            prompt=prompt,
            model=selected_model,
        )

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        usage = response.usage

        input_tokens = (
            usage.prompt_tokens
            if usage
            else 0
        )

        output_tokens = (
            usage.completion_tokens
            if usage
            else 0
        )

        output = ""

        if response.choices:
            output = (
                response.choices[0]
                .message
                .content
                or ""
            )

        return LLMResponse(
            output=output,
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

        for attempt in range(
            self.MAX_RETRIES + 1
        ):

            try:

                return await (
                    self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                    )
                )

            except RateLimitError as exc:

                raise RuntimeError(
                    "Groq rate limit or quota "
                    "exceeded."
                ) from exc

            except APITimeoutError as exc:

                last_error = exc

            except APIConnectionError as exc:

                last_error = exc

            except APIStatusError as exc:

                if exc.status_code == 404:
                    raise RuntimeError(
                        f"Groq model '{model}' "
                        "was not found or is "
                        "unavailable."
                    ) from exc

                if exc.status_code == 429:
                    raise RuntimeError(
                        "Groq rate limit or quota "
                        "exceeded."
                    ) from exc

                raise RuntimeError(
                    "Groq API request failed "
                    f"(status {exc.status_code})."
                ) from exc

            except Exception as exc:

                raise RuntimeError(
                    "Unexpected error while "
                    "calling Groq."
                ) from exc

            if attempt >= self.MAX_RETRIES:
                break

            delay = self.RETRY_DELAYS[attempt]

            print(
                f"Groq temporarily unavailable. "
                f"Retrying in {delay}s..."
            )

            await asyncio.sleep(delay)

        raise RuntimeError(
            "Groq service remained unavailable "
            f"after {self.MAX_RETRIES} retries."
        ) from last_error