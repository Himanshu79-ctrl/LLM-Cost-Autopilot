from fastapi import APIRouter, Depends, HTTPException,BackgroundTasks
from app.services.verification_service import VerificationService
from sqlalchemy.orm import Session
from app.api.schemas import (
    GenerateRequest,
    GenerateResponse,
)
from app.core.database import get_db, SessionLocal
from app.services.llm_service import LLMGenerationService
from app.core.dependencies import get_current_user
from app.models.user import User


async def run_background_verification(
    request_id: int,
    prompt: str,
    response: str,
) -> None:

    db = SessionLocal()

    try:
        service = VerificationService(db)

        await service.verify(
            request_id=request_id,
            prompt=prompt,
            response=response,
        )

    finally:
        db.close()




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
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:

        service = LLMGenerationService(
            db=db,
            user_id=current_user.id,    
        )

        result = await service.generate(
            request.prompt
        )
        
        background_tasks.add_task(
            run_background_verification,
            result.request_id,
            request.prompt,
            result.output,
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

            quality_score=result.quality_score,
            quality_passed=result.quality_passed,
            quality_reason=result.quality_reason,   
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