from pydantic import BaseModel
from typing import Any


class PaginatedResponse(BaseModel):
    page: int
    size: int
    total: int
    pages: int
    items: list[Any]
