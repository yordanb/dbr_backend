from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.breakdown_repository import (
    get_breakdowns,
    get_master_cn
)
from app.schemas.breakdown import BreakdownResponse


router = APIRouter()


@router.get("/breakdowns")
def list_breakdowns(
    cn: str | None = None,
    breakdown_code: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,

    page: int = Query(
        default=1,
        ge=1
    ),

    size: int = Query(
        default=100,
        ge=1,
        le=1000
    ),

    db: Session = Depends(get_db)
):

    return get_breakdowns(
        db=db,
        cn=cn,
        breakdown_code=breakdown_code,
        start_date=start_date,
        end_date=end_date,
        page=page,
        size=size
    )


@router.get("/master/cn")
def master_cn(
    db: Session = Depends(get_db)
):

    data = get_master_cn(db)

    return [row[0] for row in data]
