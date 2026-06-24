from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.breakdown_repository import (
    get_breakdowns,
    get_master_cn
)
from app.models.breakdown import BreakdownHistory
from app.models.import_log import ImportLog
from app.schemas.breakdown import BreakdownResponse

router = APIRouter()


@router.get("/breakdowns")
def list_breakdowns(
    cn: str | None = None,
    breakdown_code: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    sort: str | None = None,

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


@router.delete("/breakdowns/truncate")
def truncate_breakdowns(db: Session = Depends(get_db)):
    """Truncate all breakdown data. Admin only."""
    try:
        count = db.query(BreakdownHistory).count()
        db.query(ImportLog).delete()
        db.query(BreakdownHistory).delete()
        db.commit()
        return {"status": "ok", "deleted": count}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/master/cn")
def master_cn(
    db: Session = Depends(get_db)
):

    data = get_master_cn(db)

    return [row[0] for row in data]
