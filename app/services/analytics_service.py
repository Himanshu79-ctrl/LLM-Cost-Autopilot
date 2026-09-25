from sqlalchemy import func
from sqlalchemy.orm import Session

from app.services.request_logger import LLMRequest


class AnalyticsService:

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def get_summary(self) -> dict:

        total_requests = (
            self.db.query(
                func.count(LLMRequest.id)
            )
            .filter(
                LLMRequest.user_id == self.user_id
            )
            .scalar()
            or 0
        )

        total_input_tokens = (
            self.db.query(
                func.coalesce(
                    func.sum(
                        LLMRequest.input_tokens
                    ),
                    0,
                )
            )
            .filter(
                LLMRequest.user_id == self.user_id
            )
            .scalar()
            or 0
        )

        total_output_tokens = (
            self.db.query(
                func.coalesce(
                    func.sum(
                        LLMRequest.output_tokens
                    ),
                    0,
                )
            )
            .filter(
                LLMRequest.user_id == self.user_id
            )
            .scalar()
            or 0
        )

        total_cost = (
            self.db.query(
                func.coalesce(
                    func.sum(LLMRequest.cost),
                    0.0,
                )
            )
            .filter(
                LLMRequest.user_id == self.user_id
            )
            .scalar()
            or 0.0
        )

        average_latency = (
            self.db.query(
                func.avg(
                    LLMRequest.latency_ms
                )
            )
            .filter(
                LLMRequest.user_id == self.user_id
            )
            .scalar()
            or 0.0
        )

        return {
            "total_requests": total_requests,
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": (
                total_input_tokens
                + total_output_tokens
            ),
            "total_cost": float(total_cost),
            "average_latency_ms": float(
                average_latency
            ),
        }

    def get_provider_usage(self) -> list[dict]:

        rows = (
            self.db.query(
                LLMRequest.selected_provider,
                func.count(LLMRequest.id),
                func.sum(LLMRequest.cost),
                func.sum(
                    LLMRequest.input_tokens
                ),
                func.sum(
                    LLMRequest.output_tokens
                ),
            )
            .filter(
                LLMRequest.user_id == self.user_id
            )
            .group_by(
                LLMRequest.selected_provider
            )
            .all()
        )

        return [
            {
                "provider": provider,
                "requests": requests,
                "cost": float(cost or 0),
                "input_tokens": int(
                    input_tokens or 0
                ),
                "output_tokens": int(
                    output_tokens or 0
                ),
            }
            for (
                provider,
                requests,
                cost,
                input_tokens,
                output_tokens,
            ) in rows
        ]

    def get_model_usage(self) -> list[dict]:

        rows = (
            self.db.query(
                LLMRequest.selected_model,
                func.count(LLMRequest.id),
                func.sum(LLMRequest.cost),
            )
            .filter(
                LLMRequest.user_id == self.user_id
            )
            .group_by(
                LLMRequest.selected_model
            )
            .all()
        )

        return [
            {
                "model": model,
                "requests": requests,
                "cost": float(cost or 0),
            }
            for (
                model,
                requests,
                cost,
            ) in rows
        ]

    def get_complexity_usage(self) -> list[dict]:

        rows = (
            self.db.query(
                LLMRequest.complexity_level,
                func.count(LLMRequest.id),
            )
            .filter(
                LLMRequest.user_id == self.user_id
            )
            .group_by(
                LLMRequest.complexity_level
            )
            .all()
        )

        return [
            {
                "complexity": complexity,
                "requests": requests,
            }
            for (
                complexity,
                requests,
            ) in rows
        ]

    def get_request_history(
        self,
        limit: int = 50,
    ) -> list[LLMRequest]:

        return (
            self.db.query(LLMRequest)
            .filter(
                LLMRequest.user_id == self.user_id
            )
            .order_by(
                LLMRequest.created_at.desc()
            )
            .limit(limit)
            .all()
        )