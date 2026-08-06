from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.translation import router as translation_router
from app.api.users import router as users_router
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
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(translation_router, prefix="/api/v1")

logger.info("Application Started")


@app.get("/")
def root():
    return {
        "message": f"{settings.PROJECT_NAME} Running Successfully 🚀",
        "environment": settings.PROJECT_NAME,
    }
