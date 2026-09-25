from sqlalchemy.orm import Session

from app.router.router import LLMRouter
from app.services.cost_engine import CostEngine
from app.services.quality_evaluator import QualityEvaluator
from app.services.request_logger import LLMRequest
from app.providers.manager import ProviderManager


class VerificationService:

    def __init__(self, db: Session):

        self.db = db

        self.quality_evaluator = QualityEvaluator()

        self.router = LLMRouter()

        self.provider_manager = ProviderManager()

    async def verify(
        self,
        request_id: int,
        prompt: str,
        response: str,
    ) -> None:

        record = self.db.get(
            LLMRequest,
            request_id,
        )

        if record is None:
            raise ValueError(
                f"LLM request {request_id} not found."
            )

        try:

            # --------------------------------
            # 1. Verify original response
            # --------------------------------

            quality = await self.quality_evaluator.evaluate(
                prompt=prompt,
                response=response,
            )

            record.verification_model = (
                QualityEvaluator.JUDGE_MODEL
            )

            record.quality_score = quality.score

            record.verification_reason = (
                quality.reason
            )

            # --------------------------------
            # 2. Response passed
            # --------------------------------

            if quality.passed:

                record.verification_status = "passed"

                self.db.commit()

                return

            # --------------------------------
            # 3. Response failed
            # --------------------------------

            record.verification_status = "failed"

            current_model = (
                self._get_current_model(
                    record.selected_model
                )
            )

            escalated_model = self.router.escalate(
                current_model
            )

            # No stronger model available

            if escalated_model is None:

                self.db.commit()

                return

            # --------------------------------
            # 4. Generate with stronger model
            # --------------------------------

            provider = (
                self.provider_manager.get_provider(
                    escalated_model.provider
                )
            )

            escalated_response = (
                await provider.generate(
                    prompt=prompt,
                    model=escalated_model.name,
                )
            )

            # --------------------------------
            # 5. Calculate escalation cost
            # --------------------------------

            original_cost = CostEngine.calculate(
                model_name=record.selected_model,
                input_tokens=record.input_tokens,
                output_tokens=record.output_tokens,
            )

            escalated_cost = CostEngine.calculate(
                model_name=escalated_response.model,
                input_tokens=(
                    escalated_response.input_tokens
                ),
                output_tokens=(
                    escalated_response.output_tokens
                ),
            )

            cost_delta = (
                escalated_cost.total_cost
                - original_cost.total_cost
            )

            # --------------------------------
            # 6. Verify escalated response
            # --------------------------------

            escalated_quality = (
                await self.quality_evaluator.evaluate(
                    prompt=prompt,
                    response=escalated_response.output,
                )
            )

            # --------------------------------
            # 7. Save escalation information
            # --------------------------------

            record.escalated = True

            record.escalated_model = (
                escalated_response.model
            )

            record.escalation_cost_delta = (
                cost_delta
            )

            record.quality_gap = (
                escalated_quality.score
                - quality.score
            )
            record.quality_score = (
                escalated_quality.score
            )

            record.verification_status = (
                "passed"
                if escalated_quality.passed
                else "failed"
            )

            record.verification_model = (
                QualityEvaluator.JUDGE_MODEL
            )

            record.verification_reason = (
                f"Original model failed verification. "
                f"Escalated to "
                f"{escalated_response.model}. "
                f"Original score: "
                f"{quality.score:.2f}. "
                f"Escalated score: "
                f"{escalated_quality.score:.2f}. "
                f"{escalated_quality.reason}"
            )

            self.db.commit()

        except Exception as exc:

            self.db.rollback()

            record = self.db.get(
                LLMRequest,
                request_id,
            )

            if record is not None:

                record.verification_status = "error"

                record.verification_model = (
                    QualityEvaluator.JUDGE_MODEL
                )

                record.verification_reason = str(
                    exc
                )

                self.db.commit()

    def _get_current_model(
        self,
        model_name: str,
    ):

        from app.router.model_registry import get_model

        return get_model(model_name)