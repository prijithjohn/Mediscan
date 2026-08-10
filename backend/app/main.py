from fastapi import FastAPI

from backend.app.api.routes.auth import router as auth_router
from backend.app.api.routes.pipeline import router as pipeline_router
from backend.app.api.routes.prescriptions import router as prescriptions_router
from backend.app.api.routes.usage import router as usage_router
from backend.app.api.routes.alerts import router as alerts_router
from backend.app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(auth_router)
app.include_router(prescriptions_router)
app.include_router(pipeline_router)
app.include_router(usage_router)
app.include_router(alerts_router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "MediScan API is starting"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
