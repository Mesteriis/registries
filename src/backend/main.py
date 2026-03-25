import uvicorn
from core.bootstrap import create_app
from core.observability import setup_logging
from core.settings import get_settings

settings = get_settings()
setup_logging(settings)
app = create_app()


def run() -> None:
    uvicorn.run(
        "main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.api.reload,
        log_config=None,
    )


if __name__ == "__main__":
    run()
