from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


@router.get("/breakdown-trend")
def breakdown_trend(
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db)
):
    return DashboardService.breakdown_trend(
        db,
        start_date,
        end_date
    )


@router.get("/top-cn")
def top_cn(
    limit: int = 10,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db)
):
    return DashboardService.top_cn(
        db,
        limit,
        start_date,
        end_date
    )


@router.get("/top-breakdown-code")
def top_breakdown_code(
    limit: int = 10,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db)
):
    return DashboardService.top_breakdown_code(
        db,
        limit,
        start_date,
        end_date
    )


@router.get("/monthly-summary")
def monthly_summary(
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db)
):
    return DashboardService.monthly_summary(
        db,
        start_date,
        end_date
    )
