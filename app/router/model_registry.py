from dataclasses import dataclass
from typing import Literal


ProviderName = Literal[
    "gemini",
    "groq",
    "openai",
]

ModelTier = Literal[
    "cheap",
    "medium",
    "powerful",
]


@dataclass(frozen=True)
class ModelInfo:
    name: str
    provider: ProviderName
    tier: ModelTier

    input_cost_per_million: float
    output_cost_per_million: float

    supports_reasoning: bool
    supports_vision: bool

    context_window: int


MODEL_REGISTRY: dict[str, ModelInfo] = {

    # -------------------------------------------------
    # Gemini
    # -------------------------------------------------
    "gemini-3.1-flash-lite": ModelInfo(
        name="gemini-3.1-flash-lite",
        provider="gemini",
        tier="cheap",
        input_cost_per_million=0.25,
        output_cost_per_million=1.50,
        supports_reasoning=True,
        supports_vision=True,
        context_window=1_048_576,
    ),


    "gemini-3.6-flash": ModelInfo(
        name="gemini-3.6-flash",
        provider="gemini",
        tier="powerful",
        input_cost_per_million=0.75,
        output_cost_per_million=3.75,
        supports_reasoning=True,
        supports_vision=True,
        context_window=1_000_000,
    ),

    # -------------------------------------------------
    # Groq
    # -------------------------------------------------

    "openai/gpt-oss-20b": ModelInfo(
        name="openai/gpt-oss-20b",
        provider="groq",
        tier="medium",
        input_cost_per_million=0.075,
        output_cost_per_million=0.30,
        supports_reasoning=True,
        supports_vision=False,
        context_window=131_072,
    ),

    # -------------------------------------------------
    # Future OpenAI models
    # -------------------------------------------------
    # Add official models here later.
}


def get_model(model_name: str) -> ModelInfo:
    try:
        return MODEL_REGISTRY[model_name]
    except KeyError as exc:
        raise ValueError(
            f"Unknown model: {model_name}"
        ) from exc


def list_models() -> list[ModelInfo]:
    return list(MODEL_REGISTRY.values())


def get_models_by_tier(
    tier: ModelTier,
) -> list[ModelInfo]:

    return [
        model
        for model in MODEL_REGISTRY.values()
        if model.tier == tier
    ]