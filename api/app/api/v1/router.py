from fastapi import APIRouter

from app.api.v1.endpoints import breakdowns
from app.api.v1.endpoints import dashboard
from app.api.v1.endpoints import equipment


api_router = APIRouter()

api_router.include_router(
    breakdowns.router,
    tags=["Breakdowns"]
)

api_router.include_router(
    dashboard.router,
    tags=["Dashboard"]
)

api_router.include_router(
    equipment.router,
    tags=["Equipment"]
)
