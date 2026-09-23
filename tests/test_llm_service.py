import pytest

from app.core.database import SessionLocal
from app.services.llm_service import LLMGenerationService


@pytest.mark.asyncio
async def test_generate():

    db = SessionLocal()

    try:
        service = LLMGenerationService(db)

        result = await service.generate(
            "Explain what an API is in simple terms."
        )

        assert result.output
        assert result.model
        assert result.provider

        assert result.input_tokens >= 0
        assert result.output_tokens >= 0

        assert result.latency_ms > 0
        assert result.cost >= 0

    finally:
        db.close()