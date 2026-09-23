from dataclasses import dataclass

from app.router.model_registry import get_model


@dataclass(frozen=True)
class CostBreakdown:
    model: str
    input_tokens: int
    output_tokens: int

    input_cost: float
    output_cost: float
    total_cost: float


class CostEngine:

    @staticmethod
    def calculate(
        model_name: str,
        input_tokens: int,
        output_tokens: int,
    ) -> CostBreakdown:
        """
        Calculate the estimated cost of an LLM request.
        """

        if input_tokens < 0:
            raise ValueError(
                "Input tokens cannot be negative."
            )

        if output_tokens < 0:
            raise ValueError(
                "Output tokens cannot be negative."
            )

        model = get_model(model_name)

        input_cost = (
            input_tokens
            / 1_000_000
            * model.input_cost_per_million
        )

        output_cost = (
            output_tokens
            / 1_000_000
            * model.output_cost_per_million
        )

        total_cost = input_cost + output_cost

        return CostBreakdown(
            model=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost,
        )