from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMResponse:
    output: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost: float


class LLMProvider(ABC):

    @abstractmethod
    async def generate(self, prompt: str, model: Optional[str] = None,) -> LLMResponse:
        """Generate a response from the LLM provider."""
        pass