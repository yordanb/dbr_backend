from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Date,
    DateTime
)

from sqlalchemy.sql import func

from app.core.database import Base


class BreakdownHistory(Base):

    __tablename__ = "breakdown_history"
    __table_args__ = {"schema": "dbr"}

    id = Column(BigInteger, primary_key=True)

    report_date_raw = Column(Text)
    report_date = Column(Date)
    breakdown_start_date = Column(Date)

    cn = Column(String(50))

    section = Column(String(100))

    trouble_description = Column(Text)

    breakdown_code = Column(String(50))

    hm_start = Column(String(100))

    location = Column(String(100))

    start_breakdown = Column(String(100))

    start_time = Column(String(100))

    finish_time = Column(String(100))

    total = Column(String(100))

    wo_number = Column(String(100))

    notification_number = Column(String(100))

    action_taken = Column(Text)

    mechanic = Column(String(255))

    gl = Column(String(255))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )
