from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import (
    UsageSummaryResponse,
    ProviderUsageResponse,
    ModelUsageResponse,
    ComplexityUsageResponse,
    RequestHistoryResponse,
)

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.analytics_service import AnalyticsService


router = APIRouter(
    prefix="/api/usage",
    tags=["usage"],
)


@router.get(
    "/summary",
    response_model=UsageSummaryResponse,
)
async def usage_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AnalyticsService(
        db,
        current_user.id,
    )

    return service.get_summary()


@router.get(
    "/providers",
    response_model=list[ProviderUsageResponse],
)
async def provider_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AnalyticsService(
        db,
        current_user.id,
    )

    return service.get_provider_usage()


@router.get(
    "/models",
    response_model=list[ModelUsageResponse],
)
async def model_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AnalyticsService(
        db,
        current_user.id,
    )

    return service.get_model_usage()


@router.get(
    "/complexity",
    response_model=list[ComplexityUsageResponse],
)
async def complexity_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AnalyticsService(
        db,
        current_user.id,
    )

    return service.get_complexity_usage()


@router.get(
    "/requests",
    response_model=list[RequestHistoryResponse],
)
async def request_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AnalyticsService(
        db,
        current_user.id,
    )

    return service.get_request_history()