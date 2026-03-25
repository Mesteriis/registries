from typing import Any

import sentry_sdk
from fastapi import Request
from opentelemetry import trace
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.types import Event, Hint

from core.observability.context import get_correlation_id, get_request_id
from core.settings import Settings

_SENTRY_CONFIGURED = False


def _trace_context() -> tuple[str | None, str | None]:
    span = trace.get_current_span()
    span_context = span.get_span_context()
    if not span_context.is_valid:
        return None, None
    return f"{span_context.trace_id:032x}", f"{span_context.span_id:016x}"


def _scrub_event_payload(event: Event) -> Event:
    request = event.get("request")
    if isinstance(request, dict):
        headers = request.get("headers")
        if isinstance(headers, dict):
            for key in ("Authorization", "Cookie", "Set-Cookie"):
                if key in headers:
                    headers[key] = "[REDACTED]"
        if "data" in request:
            request["data"] = "[FILTERED]"
    return event


def _before_send(event: Event, hint: Hint) -> Event | None:
    del hint
    event = _scrub_event_payload(event)
    request_id = get_request_id()
    correlation_id = get_correlation_id()
    trace_id, span_id = _trace_context()

    tags = event.setdefault("tags", {})
    if isinstance(tags, dict):
        if request_id is not None:
            tags["request_id"] = request_id
        if correlation_id is not None:
            tags["correlation_id"] = correlation_id
        if trace_id is not None:
            tags["trace_id"] = trace_id
        if span_id is not None:
            tags["span_id"] = span_id

    extra = event.setdefault("extra", {})
    if isinstance(extra, dict):
        if request_id is not None:
            extra["request_id"] = request_id
        if correlation_id is not None:
            extra["correlation_id"] = correlation_id
        if trace_id is not None:
            extra["trace_id"] = trace_id
        if span_id is not None:
            extra["span_id"] = span_id

    return event


def setup_error_tracking(settings: Settings) -> None:
    """Configure sentry-sdk for GlitchTip-compatible error tracking."""
    global _SENTRY_CONFIGURED

    if not settings.observability.enabled or not settings.observability.sentry_enabled:
        return
    if not settings.observability.glitchtip_dsn:
        return
    if _SENTRY_CONFIGURED:
        return

    sentry_sdk.init(
        dsn=settings.observability.glitchtip_dsn,
        environment=settings.observability_environment,
        release=settings.observability_service_version,
        integrations=[FastApiIntegration(transaction_style="endpoint")],
        send_default_pii=False,
        traces_sample_rate=0.0,
        profiles_sample_rate=settings.observability.profile_sample_rate,
        before_send=_before_send,
    )
    _SENTRY_CONFIGURED = True


def capture_handled_exception(request: Request, exc: Exception) -> None:
    """Send handled unexpected exceptions to GlitchTip when enabled."""
    if not _SENTRY_CONFIGURED:
        return

    trace_id, span_id = _trace_context()
    request_id = get_request_id()
    correlation_id = get_correlation_id()

    with sentry_sdk.push_scope() as scope:
        scope.set_tag("http.path", request.url.path)
        scope.set_tag("http.method", request.method)
        if request_id is not None:
            scope.set_tag("request_id", request_id)
        if correlation_id is not None:
            scope.set_tag("correlation_id", correlation_id)
        if trace_id is not None:
            scope.set_tag("trace_id", trace_id)
        if span_id is not None:
            scope.set_tag("span_id", span_id)
        sentry_sdk.capture_exception(exc)


def flush_error_tracking() -> None:
    """Flush buffered sentry events during graceful shutdown."""
    if _SENTRY_CONFIGURED:
        sentry_sdk.flush(timeout=2.0)
