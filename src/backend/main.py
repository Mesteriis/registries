import uvicorn
from core.bootstrap import create_app
from core.observability import setup_logging
from core.settings import Settings, get_settings
from fastapi import FastAPI


def bootstrap_runtime() -> tuple[Settings, FastAPI]:
    """Create the runtime settings/app pair used by the ASGI entrypoint."""

    runtime_settings = get_settings()
    setup_logging(runtime_settings)
    runtime_app = create_app()
    return runtime_settings, runtime_app


settings, app = bootstrap_runtime()


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
