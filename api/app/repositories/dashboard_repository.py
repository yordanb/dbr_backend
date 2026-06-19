from sqlalchemy import func
from sqlalchemy.orm import Session

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

    return {
        "total_records": total_records,
        "total_cn": total_cn,
        "total_breakdowns": total_breakdowns
    }
