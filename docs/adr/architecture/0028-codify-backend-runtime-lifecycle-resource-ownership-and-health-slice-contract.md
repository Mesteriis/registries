# ADR-0028: Codify backend runtime lifecycle, shared resource ownership, and health slice operational contract

- Status: Accepted
- Date: 2026-03-26
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0009](./0009-deployment-topology-and-runtime-model.md)
- [ADR-0010](./0010-use-taskiq-redis-streams-and-postgresql.md)
- [ADR-0017](./0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [ADR-0021](./0021-centralize-backend-observability-bootstrap-and-structured-telemetry.md)
- [ADR-0022](./0022-group-backend-settings-into-nested-platform-models.md)
- [ADR-0027](./0027-enforce-machine-validated-http-contract-parity-across-spec-backend-and-frontend.md)

## Context

The template already moved away from eager infrastructure bootstrap and ad-hoc
health checks, but the remaining runtime contract still needed to be made
explicit.

Without a clear policy, reusable templates degrade quickly:

- importing the ASGI entrypoint starts opening infrastructure clients unexpectedly;
- runtime code recreates Redis or database clients in request paths;
- shutdown ownership becomes ambiguous and lazy resources leak across tests or process shutdown;
- health endpoints either block too long, expose unsafe internals, or become too shallow to diagnose failures;
- future bounded contexts copy whatever behavior they happen to see first instead of following a platform rule.

The template needs one explicit contract for backend app composition, shared
resource ownership, and the operational expectations of the reference `system
health` slice.

## Decision

Backend runtime lifecycle is standardized as follows.

Bootstrap contract:

- `src/backend/main.py` may expose a top-level `app` for ASGI servers;
- importing `main.py` is allowed to compose settings, logging, middleware, routes, and observability wiring;
- import-time bootstrap must not eagerly establish persistent PostgreSQL or Redis client connections for normal API startup.

Shared resource ownership:

- the async SQLAlchemy engine is process-local and initialized lazily through `core.db.get_async_engine()`;
- the async session factory is derived from that engine and reset together with it;
- the async SQLAlchemy engine is disposed on FastAPI app shutdown;
- Redis clients used by the `system` bounded context are obtained through an explicit cache/factory keyed by Redis URL, not recreated per health probe;
- cached Redis clients are closed on FastAPI app shutdown;
- SQLAlchemy tracing instrumentation may be registered during app composition, but engine-backed instrumentation runs on app startup rather than forcing engine creation during app assembly.

Health slice operational contract:

- readiness and health dependency probes run concurrently;
- each dependency probe is bounded by `settings.system.health_timeout_seconds`;
- timeout is reported externally as `detail="timeout"` while preserving the existing response schema;
- external health/readiness payloads expose only safe details such as `database unavailable`, `redis unavailable`, or `timeout`;
- structured backend logs must capture the failing dependency and underlying exception context for operators;
- the `system health` slice is the canonical reference slice for how future bounded contexts should expose safe operational status without leaking internal error data.

## Consequences

### Positive

- backend startup becomes easier to reason about because app assembly and infrastructure connection ownership are no longer conflated;
- shared runtime resources are reused deliberately and closed deliberately;
- health endpoints remain externally safe while still giving operators useful logs;
- future bounded contexts have a concrete reference slice for operational status behavior.

### Negative

- lifecycle rules now span bootstrap, observability, and infrastructure modules and must stay aligned;
- tests must cover both lazy initialization and shutdown cleanup so regressions are caught early.

### Neutral

- the template still keeps a top-level ASGI `app`; the decision is not to remove that convention, but to narrow what it is allowed to do.

## Alternatives considered

- eagerly creating the SQLAlchemy engine or Redis clients during module import;
- constructing a brand new Redis client for every health ping;
- probing dependencies sequentially and accepting additive timeout latency;
- returning raw exception text or stack traces in health/readiness responses.

## Follow-up work

- [ ] keep lifecycle tests aligned whenever new shared runtime resources gain process-level ownership
- [ ] extend the same safe operational status pattern when new bounded contexts expose public readiness-style endpoints
