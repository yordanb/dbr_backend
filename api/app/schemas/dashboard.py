from pydantic import BaseModel


class BreakdownTrendResponse(BaseModel):
    date: str
    total_breakdowns: int


class TopCNResponse(BaseModel):
    cn: str
    total_breakdowns: int


class TopBreakdownCodeResponse(BaseModel):
    breakdown_code: str
    total: int


class MonthlySummaryResponse(BaseModel):
    month: str
    total_breakdowns: int
