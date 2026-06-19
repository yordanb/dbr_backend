from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.breakdown import BreakdownHistory

router = APIRouter(
    prefix="/api/v1/breakdowns",
    tags=["Breakdowns"]
)


@router.get("")
def get_breakdowns(
    cn: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(BreakdownHistory)

    if cn:
        query = query.filter(
            BreakdownHistory.cn == cn
        )

    if start_date:
        query = query.filter(
            BreakdownHistory.start_breakdown >= start_date
        )

    if end_date:
        query = query.filter(
            BreakdownHistory.start_breakdown <= end_date
        )

    data = query.order_by(
        BreakdownHistory.start_breakdown.desc()
    ).all()

    return data
