from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.breakdown import BreakdownHistory
from app.models.import_log import ImportLog

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


@router.delete("/truncate")
def truncate_breakdowns(db: Session = Depends(get_db)):
    """Truncate all breakdown data. Requires admin authorization."""
    try:
        count = db.query(BreakdownHistory).count()
        db.query(ImportLog).delete()
        db.query(BreakdownHistory).delete()
        db.commit()
        return {"status": "ok", "deleted": count}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
