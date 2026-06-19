from fastapi import FastAPI
from app.routers.breakdown import router as breakdown_router
from app.routers.import_excel import router as import_router
from app.api.v1.router import api_router
from app.api.dashboard import router as dashboard_router

app = FastAPI(
    title="DBR API",
    version="1.0.0"
)

app.include_router(
    api_router,
    prefix="/api/v1"
)

app.include_router(
    breakdown_router
)

app.include_router(
    import_router
)

app.include_router(
    dashboard_router
)



@app.get("/")
def root():
    return {
        "application": "DBR API",
        "status": "running"
    }
