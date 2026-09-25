from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.providers.manager import ProviderManager
from app.router.router import LLMRouter
from app.services.cost_engine import CostEngine
from app.services.request_logger import (
    LLMRequest,
    hash_prompt,
)


@dataclass(frozen=True)
class GenerationResult:

    request_id: int

    output: str

    model: str
    provider: str

    complexity: str
    complexity_score: int

    input_tokens: int
    output_tokens: int

    latency_ms: float
    cost: float

    quality_score: float | None
    quality_passed: bool
    quality_reason: str


class LLMGenerationService:

    def __init__(self, db: Session, user_id: int):

        self.db = db
        self.user_id = user_id

        self.router = LLMRouter()

        self.provider_manager = ProviderManager()

    async def generate(
        self,
        prompt: str,
    ) -> GenerationResult:

        # --------------------------------
        # 1. Route the request
        # --------------------------------

        decision = self.router.route(prompt)

        model = decision.model

        # --------------------------------
        # 2. Get provider
        # --------------------------------

        provider = self.provider_manager.get_provider(
            model.provider
        )

        try:

            # --------------------------------
            # 3. Generate LLM response
            # --------------------------------

            response = await provider.generate(
                prompt=prompt,
                model=model.name,
            )

            # --------------------------------
            # 4. Calculate cost
            # --------------------------------

            cost_breakdown = CostEngine.calculate(
                model_name=response.model,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
            )

            # --------------------------------
            # 5. Save successful request
            # --------------------------------

            record = LLMRequest(
                user_id=self.user_id,
                prompt_hash=hash_prompt(prompt),

                complexity_level=decision.complexity,

                complexity_score=decision.score,

                complexity_features=decision.features,

                selected_model=response.model,

                selected_provider=model.provider,

                routing_reason=decision.reason,

                fallback_used=False,

                input_tokens=response.input_tokens,

                output_tokens=response.output_tokens,

                latency_ms=response.latency_ms,

                cost=cost_breakdown.total_cost,

                quality_score=None,

                verification_status="pending",

                verification_model=None,

                verification_reason=None,

                escalated=False,

                error_type=None,

                error_message=None,
            )

            self.db.add(record)

            self.db.commit()

            # --------------------------------
            # 6. Return generation result
            # --------------------------------

            return GenerationResult(

                request_id=record.id,

                output=response.output,

                model=response.model,

                provider=model.provider,

                complexity=decision.complexity,

                complexity_score=decision.score,

                input_tokens=response.input_tokens,

                output_tokens=response.output_tokens,

                latency_ms=response.latency_ms,

                cost=cost_breakdown.total_cost,

                quality_score=None,

                quality_passed=False,

                quality_reason="Verification pending.",
            )

        except Exception as exc:

            # --------------------------------
            # 7. Save failed request
            # --------------------------------

            self.db.rollback()

            error_record = LLMRequest(
                user_id=self.user_id,
                prompt_hash=hash_prompt(prompt),

                complexity_level=decision.complexity,

                complexity_score=decision.score,

                complexity_features=decision.features,

                selected_model=model.name,

                selected_provider=model.provider,

                routing_reason=decision.reason,

                fallback_used=False,

                input_tokens=0,

                output_tokens=0,

                latency_ms=0.0,

                cost=0.0,

                quality_score=None,

                verification_status="error",

                verification_model=None,

                verification_reason=None,

                escalated=False,

                error_type=type(exc).__name__,

                error_message=str(exc),
            )

            self.db.add(error_record)

            self.db.commit()

            raise