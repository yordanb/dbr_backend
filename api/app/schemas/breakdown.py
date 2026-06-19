from datetime import date, datetime
from pydantic import BaseModel


class BreakdownResponse(BaseModel):
    id: int

    report_date_raw: str | None
    report_date: date | None
    breakdown_start_date: date | None

    cn: str | None
    section: str | None
    trouble_description: str | None
    breakdown_code: str | None

    hm_start: str | None
    location: str | None

    start_breakdown: str | None
    start_time: str | None
    finish_time: str | None
    total: str | None

    wo_number: str | None
    notification_number: str | None

    action_taken: str | None
    mechanic: str | None
    gl: str | None

    created_at: datetime

    class Config:
        from_attributes = True
