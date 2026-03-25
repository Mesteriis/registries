from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from core.settings import Settings


def setup_metrics(app: FastAPI, settings: Settings) -> None:
    """Expose Prometheus metrics for HTTP request count, latency and status codes."""
    if not settings.observability.enabled or not settings.observability.metrics_enabled:
        return
    if getattr(app.state, "metrics_configured", False):
        return

    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=False,
        excluded_handlers=[settings.observability.metrics_path],
    )
    instrumentator.instrument(app).expose(
        app,
        endpoint=settings.observability.metrics_path,
        include_in_schema=False,
    )
    app.state.metrics_configured = True
