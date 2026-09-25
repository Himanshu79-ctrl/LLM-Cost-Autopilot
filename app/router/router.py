from dataclasses import dataclass

from app.router.complexity_analyzer import (
    ComplexityAnalyzer,
    ComplexityLevel,
)
from app.router.model_registry import (
    ModelInfo,
    get_models_by_tier,
)


COMPLEXITY_TO_TIER = {
    "low": "cheap",
    "medium": "medium",
    "high": "powerful",
}

TIER_ESCALATION = {
    "cheap": "medium",
    "medium": "powerful",
}


@dataclass(frozen=True)
class RoutingDecision:
    model: ModelInfo
    complexity: ComplexityLevel
    score: int
    features: dict
    reason: str


class LLMRouter:

    def __init__(self):
        self.analyzer = ComplexityAnalyzer()

    def route(
        self,
        prompt: str,
    ) -> RoutingDecision:

        complexity = self.analyzer.analyze(prompt)

        required_tier = COMPLEXITY_TO_TIER[
            complexity.level
        ]

        candidates = get_models_by_tier(
            required_tier
        )

        if not candidates:
            raise RuntimeError(
                f"No models available for "
                f"tier: {required_tier}"
            )

        selected_model = min(
            candidates,
            key=lambda model: (
                model.input_cost_per_million
                + model.output_cost_per_million
            ),
        )

        return RoutingDecision(
            model=selected_model,
            complexity=complexity.level,
            score=complexity.score,
            features=complexity.features,
            reason=(
                f"Prompt classified as "
                f"{complexity.level} complexity. "
                f"Selected {required_tier} tier model."
            ),
        )

    def escalate(self, current_model: ModelInfo,) -> ModelInfo | None:

        current_tier = current_model.tier

        next_tier = TIER_ESCALATION.get(
            current_tier
        )

        if next_tier is None:
            return None

        candidates = get_models_by_tier(
            next_tier
        )

        if not candidates:
            return None

        selected_model = min(
            candidates,
            key=lambda model: (
                model.input_cost_per_million
                + model.output_cost_per_million
            ),
        )

        return selected_model