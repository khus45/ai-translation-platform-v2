from fastapi import FastAPI

from app.api.health import router as health_router
from app.config.constants import PROJECT_NAME
from app.config.logging import logger
from app.config.settings import settings

app = FastAPI(
    title=PROJECT_NAME,
    version="1.0.0",
)
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

logger.info("Application Started")


@app.get("/")
def root():
    return {
        "message": f"{settings.PROJECT_NAME} Running Successfully 🚀",
        "environment": settings.PROJECT_NAME,
    }
