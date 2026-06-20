from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.import_excel import router as import_router
from app.api.v1.router import api_router
from app.api.dashboard import router as dashboard_router
from app.core.config import settings

app = FastAPI(
    title="DBR API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix="/api/v1"
)

app.include_router(import_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "application": "DBR API",
        "status": "running"
    }


@app.get("/health")
def health():
    from app.core.database import engine
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
