from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import (
    GenerateRequest,
    GenerateResponse,
)
from app.core.database import get_db
from app.services.llm_service import LLMGenerationService


router = APIRouter(
    prefix="/api",
    tags=["generation"],
)


@router.post(
    "/generate",
    response_model=GenerateResponse,
)
async def generate(
    request: GenerateRequest,
    db: Session = Depends(get_db),
):

    try:

        service = LLMGenerationService(db)

        result = await service.generate(
            request.prompt
        )

        return GenerateResponse(
            output=result.output,

            model=result.model,
            provider=result.provider,

            complexity=result.complexity,
            complexity_score=result.complexity_score,

            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,

            latency_ms=result.latency_ms,
            cost=result.cost,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc