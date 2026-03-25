from fastapi import FastAPI

from core.observability.error_tracking import flush_error_tracking, setup_error_tracking
from core.observability.logging import setup_logging
from core.observability.metrics import setup_metrics
from core.observability.middleware import setup_request_context
from core.observability.tracing import setup_tracing
from core.settings import Settings


def setup_observability(app: FastAPI, settings: Settings) -> None:
    """Apply the project-standard observability stack to the FastAPI app."""
    if getattr(app.state, "observability_configured", False):
        return

    setup_logging(settings)
    setup_error_tracking(settings)
    setup_request_context(
        app,
        request_id_header_name=settings.observability.request_id_header,
        correlation_id_header_name=settings.observability.correlation_id_header,
    )
    setup_metrics(app, settings)
    setup_tracing(app, settings)

    if not getattr(app.state, "error_tracking_flush_registered", False):
        app.add_event_handler("shutdown", flush_error_tracking)
        app.state.error_tracking_flush_registered = True

    app.state.observability_configured = True
