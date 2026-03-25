import uvicorn
from core.bootstrap import create_app
from core.settings import get_settings

settings = get_settings()
app = create_app()


def run() -> None:
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )


if __name__ == "__main__":
    run()
