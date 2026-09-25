import pytest
from app.services.request_logger import LLMRequest
from app.core.database import SessionLocal
from app.services.quality_evaluator import QualityResult
from app.services.verification_service import VerificationService


@pytest.mark.asyncio
async def test_failed_verification_triggers_escalation(
    monkeypatch,
):
    db = SessionLocal()

    try:
        service = VerificationService(db)

        record = LLMRequest(
            prompt_hash="test-hash",
            complexity_level="medium",
            complexity_score=5,
            complexity_features={},
            selected_model="openai/gpt-oss-20b",
            selected_provider="groq",
            routing_reason="Test routing decision",
            fallback_used=False,
            input_tokens=100,
            output_tokens=200,
            latency_ms=1000.0,
            cost=0.0001,
            quality_score=None,
            verification_status="pending",
            verification_model=None,
            verification_reason=None,
            escalated=False,
            escalated_model=None,
            escalation_cost_delta=None,
            quality_gap=None,
            error_type=None,
            error_message=None,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        results = [
            QualityResult(
                score=5.0,
                passed=False,
                relevance=5.0,
                correctness=5.0,
                completeness=5.0,
                instruction_following=5.0,
                clarity=5.0,
                reason="Original response failed.",
            ),
            QualityResult(
                score=9.0,
                passed=True,
                relevance=9.0,
                correctness=9.0,
                completeness=9.0,
                instruction_following=9.0,
                clarity=9.0,
                reason="Escalated response passed.",
            ),
        ]

        async def fake_evaluate(
            prompt,
            response,
        ):
            return results.pop(0)

        monkeypatch.setattr(
            service.quality_evaluator,
            "evaluate",
            fake_evaluate,
        )

        class FakeResponse:
            output = "Improved escalated response."
            model = "gemini-3.6-flash"
            input_tokens = 120
            output_tokens = 250
            latency_ms = 1200.0

        async def fake_generate(
            prompt,
            model,
        ):
            return FakeResponse()

        provider = service.provider_manager.get_provider(
            "gemini"
        )

        monkeypatch.setattr(
            provider,
            "generate",
            fake_generate,
        )

        await service.verify(
            request_id=record.id,
            prompt="Test prompt",
            response="Original weak response.",
        )

        db.refresh(record)

        assert record.verification_status == "passed"

        assert record.escalated is True

        assert (
            record.escalated_model
            == "gemini-3.6-flash"
        )

        assert record.quality_score == 9.0

        assert record.quality_gap == 4.0

        assert record.escalation_cost_delta is not None
        assert record.escalation_cost_delta > 0

    finally:
        db.close()