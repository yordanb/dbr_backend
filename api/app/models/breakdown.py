from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Time,
    Interval,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from app.core.database import Base


class BreakdownHistory(Base):
    __tablename__ = "breakdown_history"
    __table_args__ = (
        UniqueConstraint(
            "report_date", "cn", "trouble_description", "row_no",
            name="uq_breakdown_entry",
        ),
        {"schema": "dbr"},
    )

    id = Column(BigInteger, primary_key=True)

    report_date_raw = Column(Text)
    report_date = Column(Date)
    breakdown_start_date = Column(Date)

    row_no = Column(Integer, nullable=False, default=0)

    cn = Column(String(50))

    crew_type = Column(String(10))

    section = Column(String(100))

    trouble_description = Column(Text)

    breakdown_code = Column(String(50))

    hm_start = Column(String(100))
    hour_meter = Column(Numeric(10, 1))

    location = Column(String(100))

    start_breakdown = Column(String(100))
    start_bd_hour = Column(Time)
    rfu_bour = Column(Time)

    start_time = Column(String(100))
    finish_time = Column(String(100))

    total = Column(String(100))
    total_hours = Column(Numeric(8, 2))
    hours_breakdown = Column(Interval)

    wo_number = Column(String(100))
    notification_number = Column(String(100))
    mo_number = Column(String(30))

    action_taken = Column(Text)

    mechanic = Column(String(255))

    gl = Column(String(255))

    source_file = Column(String(100))

    created_at = Column(DateTime, server_default=func.now())
