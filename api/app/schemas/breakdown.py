from datetime import date, datetime, time
from decimal import Decimal
from pydantic import BaseModel


class BreakdownResponse(BaseModel):
    id: int
    report_date_raw: str | None = None
    report_date: date | None = None
    breakdown_start_date: date | None = None
    row_no: int | None = None
    cn: str | None = None
    crew_type: str | None = None
    section: str | None = None
    trouble_description: str | None = None
    breakdown_code: str | None = None
    hm_start: str | None = None
    hour_meter: Decimal | None = None
    location: str | None = None
    start_breakdown: str | None = None
    start_bd_hour: time | None = None
    rfu_bour: time | None = None
    start_time: str | None = None
    finish_time: str | None = None
    total: str | None = None
    total_hours: Decimal | None = None
    wo_number: str | None = None
    notification_number: str | None = None
    mo_number: str | None = None
    action_taken: str | None = None
    mechanic: str | None = None
    gl: str | None = None
    source_file: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True
