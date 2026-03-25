from api import api_router
from fastapi import FastAPI

from core.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/", tags=["meta"])
    async def read_root() -> dict[str, str]:
        return {
            "service": settings.app_name,
            "docs": "/docs",
            "health": f"{settings.api_prefix}/system/health",
        }

    return app
