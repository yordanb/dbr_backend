from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.repositories.dashboard_repository import (
    get_summary
)

router = APIRouter()


@router.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):
    return get_summary(db)
