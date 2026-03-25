from collections.abc import MutableMapping
from typing import cast

from fastapi import FastAPI
from opentelemetry import trace
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from core.observability.context import (
    generate_request_id,
    reset_correlation_id,
    reset_request_id,
    set_correlation_id,
    set_request_id,
)


class RequestContextMiddleware:
    """Attach stable request and correlation identifiers to each incoming HTTP request."""

    def __init__(self, app: ASGIApp, *, request_id_header_name: str, correlation_id_header_name: str) -> None:
        self.app = app
        self.request_id_header_name = request_id_header_name
        self.correlation_id_header_name = correlation_id_header_name
        self._request_id_header_bytes = request_id_header_name.lower().encode("latin-1")
        self._correlation_id_header_bytes = correlation_id_header_name.lower().encode("latin-1")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = self._resolve_request_id(scope)
        correlation_id = self._resolve_correlation_id(scope, request_id=request_id)
        token = set_request_id(request_id)
        correlation_token = set_correlation_id(correlation_id)
        state = scope.setdefault("state", {})
        if isinstance(state, MutableMapping):
            state["request_id"] = request_id
            state["correlation_id"] = correlation_id

        self._bind_context_to_active_span(request_id=request_id, correlation_id=correlation_id)

        async def send_with_request_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers = self._ensure_response_header(
                    headers,
                    header_name=self._request_id_header_bytes,
                    header_value=request_id,
                )
                headers = self._ensure_response_header(
                    headers,
                    header_name=self._correlation_id_header_bytes,
                    header_value=correlation_id,
                )
                message = {**message, "headers": headers}
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        finally:
            reset_correlation_id(correlation_token)
            reset_request_id(token)

    def _resolve_request_id(self, scope: Scope) -> str:
        for header_name, header_value in scope.get("headers", []):
            if header_name.lower() != self._request_id_header_bytes:
                continue
            raw_request_id = cast(str, header_value.decode("latin-1")).strip()
            if raw_request_id:
                return raw_request_id
        return generate_request_id()

    def _resolve_correlation_id(self, scope: Scope, *, request_id: str) -> str:
        for header_name, header_value in scope.get("headers", []):
            if header_name.lower() != self._correlation_id_header_bytes:
                continue
            raw_correlation_id = cast(str, header_value.decode("latin-1")).strip()
            if raw_correlation_id:
                return raw_correlation_id
        return request_id

    def _ensure_response_header(
        self,
        headers: list[tuple[bytes, bytes]],
        *,
        header_name: bytes,
        header_value: str,
    ) -> list[tuple[bytes, bytes]]:
        if any(existing_name.lower() == header_name for existing_name, _ in headers):
            return headers
        headers.append((header_name, header_value.encode("latin-1")))
        return headers

    def _bind_context_to_active_span(self, *, request_id: str, correlation_id: str) -> None:
        span = trace.get_current_span()
        span_context = span.get_span_context()
        if span_context.is_valid:
            span.set_attribute("request.id", request_id)
            span.set_attribute("correlation.id", correlation_id)


def setup_request_context(
    app: FastAPI,
    *,
    request_id_header_name: str,
    correlation_id_header_name: str,
) -> None:
    """Register the request/correlation middleware exactly once for the ASGI app."""
    if getattr(app.state, "request_context_configured", False):
        return
    app.state.request_id_header = request_id_header_name
    app.state.correlation_id_header = correlation_id_header_name
    app.add_middleware(
        RequestContextMiddleware,
        request_id_header_name=request_id_header_name,
        correlation_id_header_name=correlation_id_header_name,
    )
    app.state.request_context_configured = True
