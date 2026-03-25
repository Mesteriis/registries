# ADR-0021: Centralize backend observability bootstrap and structured telemetry

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0004](./0004-observability-and-audit-trail.md)
- [ADR-0007](./0007-configuration-and-policy-as-code.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-0022](./0022-group-backend-settings-into-nested-platform-models.md)
- [ADR-0020](./0020-centralize-platform-error-registry-and-http-error-projection.md)

## Context

High-level ADR-0004 already fixes observability as a first-class platform concern, but the template still needs a concrete backend baseline that is hard to misuse. Without a centralized runtime pattern, projects degrade quickly:

- tracing, metrics, logging and error tracking get initialized in random places such as `main.py`, endpoints or workers;
- request correlation becomes inconsistent between logs, traces and error events;
- service metadata, OTLP endpoints and DSN values get duplicated or hardcoded outside the settings layer;
- teams fall back to `print`, stdlib loggers and ad-hoc middleware because there is no single platform path;
- custom exception handlers and framework integrations start fighting each other instead of composing cleanly.

The maximum template therefore needs one canonical observability bootstrap that stays settings-driven, platform-owned and machine-enforced.

## Decision

Backend adopts a centralized observability baseline under `src/backend/core/observability`.

Platform bootstrap rules:

- `setup_observability(app, settings)` is the single orchestration entrypoint for runtime observability;
- logging, tracing, metrics, request context and error tracking are implemented as separate modules with narrow public `setup_*` functions;
- application bootstrap calls the orchestration entrypoint once and does not inline instrumentation logic in routes, repositories or `main.py`;
- service name, service version, deployment environment, OTLP endpoint, metrics path and GlitchTip DSN come strictly from the settings layer.
- incoming HTTP context carries both `request_id` and `correlation_id`; when the client omits `correlation_id`, the platform derives it from `request_id` for a deterministic default.

Logging rules:

- structured JSON logging via `structlog` is the canonical logging baseline for backend runtime code;
- backend modules must obtain loggers through the platform wrapper, not through direct `logging.getLogger` or raw `structlog` setup;
- `print`/`pprint` are forbidden in backend runtime code;
- logs must include timestamp, log level, message, service, environment, request id, correlation id and active trace/span identifiers when available;
- observability processors must redact obvious sensitive fields such as authorization and cookie headers when they appear in log payloads.

Tracing and metrics rules:

- OpenTelemetry uses a `TracerProvider` with `Resource` attributes for `service.name`, `service.version` and `deployment.environment`;
- trace export uses OTLP with `BatchSpanProcessor` and a settings-driven endpoint;
- FastAPI, SQLAlchemy and Redis instrumentation are enabled only through the centralized tracing module and must avoid double instrumentation;
- Prometheus metrics are exposed through a settings-driven endpoint and coexist with existing health endpoints without replacing them.

Error tracking rules:

- GlitchTip-compatible error tracking uses `sentry-sdk` and remains optional by configuration;
- custom exception handlers keep the typed HTTP error contract from ADR-0020 and enrich captured events with request id, correlation id and trace correlation data;
- error tracking must not hardcode DSN, environment or release values and must stay safe when disabled.

## Consequences

### Positive

- tracing, logs, metrics and handled error events now share the same request-level correlation path;
- application and platform code get one obvious observability integration path instead of multiple competing patterns;
- settings remain the single source of truth for external endpoints and release metadata;
- local hooks and CI can statically forbid regressions back to `print` and ad-hoc loggers.

### Negative

- backend runtime gains a non-trivial platform module that must be maintained together with dependency versions;
- more instrumentation means more care is required around sampling, redaction and noise budgets.

### Neutral

- individual exporters and processors can evolve over time, provided the centralized bootstrap and settings-driven ownership model remain intact.

## Alternatives considered

- initialize logging, tracing, metrics and sentry directly inside `main.py`;
- let each bounded context own its own middleware and logger bootstrap;
- use plain stdlib logging without JSON structure or trace correlation;
- keep error tracking fully implicit and rely only on framework defaults despite custom exception handlers.

## Follow-up work

- [ ] add worker/task context propagation rules so background jobs can carry request and trace correlation explicitly
- [ ] extend platform docs with log field schema and redaction expectations
- [ ] add contract-level tests for exported telemetry shape once external collectors are wired in integration environments
