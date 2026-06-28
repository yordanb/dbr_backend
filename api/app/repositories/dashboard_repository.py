from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.breakdown import BreakdownHistory


def get_summary(db: Session):

    total_records = (
        db.query(func.count(BreakdownHistory.id))
        .scalar()
    )

    total_cn = (
        db.query(
            func.count(
                func.distinct(
                    BreakdownHistory.cn
                )
            )
        )
        .scalar()
    )

    total_breakdowns = (
        db.query(
            func.count(
                BreakdownHistory.id
            )
        )
        .filter(
            BreakdownHistory.breakdown_start_date.isnot(None)
        )
        .scalar()
    )

    # Date range
    min_date = db.query(func.min(BreakdownHistory.report_date)).scalar()
    max_date = db.query(func.max(BreakdownHistory.report_date)).scalar()

    return {
        "total_records": total_records,
        "total_cn": total_cn,
        "total_breakdowns": total_breakdowns,
        "data_old": str(min_date) if min_date else None,
        "data_new": str(max_date) if max_date else None
    }
