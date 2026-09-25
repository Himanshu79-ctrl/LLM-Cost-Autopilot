from datetime import datetime
import hashlib
from sqlalchemy import DateTime, Float,ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LLMRequest(Base):

    __tablename__ = "llm_requests"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    prompt_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    complexity_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    complexity_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    complexity_features: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    selected_model: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    selected_provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    routing_reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    fallback_used: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    input_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    output_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    latency_ms: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    quality_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    verification_status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False,
    )

    verification_model: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    verification_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    escalated: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    escalated_model: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    
    escalation_cost_delta: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    
    quality_gap: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    error_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )



def hash_prompt(prompt: str) -> str:
    return hashlib.sha256(
        prompt.encode("utf-8")
    ).hexdigest()