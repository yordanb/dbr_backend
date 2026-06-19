from sqlalchemy.orm import Session
from sqlalchemy import distinct
from app.models.breakdown import BreakdownHistory


def get_breakdowns(
    db: Session,
    cn: str | None = None,
    start_date=None,
    end_date=None,
    page: int = 1,
    size: int = 100,
):
    query = db.query(BreakdownHistory)
    if cn:
        query = query.filter(BreakdownHistory.cn == cn)
    if start_date:
        query = query.filter(
            BreakdownHistory.report_date >= start_date
        )
    if end_date:
        query = query.filter(
            BreakdownHistory.report_date <= end_date
        )
    total = query.count()

    offset = (page - 1) * size

    data = (
        query
        .order_by(
            BreakdownHistory.report_date.desc(),
            BreakdownHistory.id.desc()
        )
        .offset(offset)
        .limit(size)
        .all()
    )

    return {
        "page": page,
        "size": size,
        "total": total,
        "pages": (total + size - 1) // size,
        "items": data
    }


def get_master_cn(db: Session):
    return (
        db.query(
            distinct(BreakdownHistory.cn)
        )
        .filter(
            BreakdownHistory.cn.isnot(None)
        )
        .order_by(BreakdownHistory.cn)
        .all()
    )

