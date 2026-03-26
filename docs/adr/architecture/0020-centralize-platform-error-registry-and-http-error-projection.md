# ADR-0020: Centralize platform error registry and HTTP error projection

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0002](./0002-api-first-and-contract-versioning.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)
- [ADR-0019](./0019-centralize-persistence-behind-repositories-query-services-and-exhaustive-layer-contracts.md)
- [ADR-0021](./0021-centralize-backend-observability-bootstrap-and-structured-telemetry.md)

## Context

Without a centralized error model, a backend usually degrades into a mix of
ad-hoc `HTTPException(detail={...})`, local string codes, and inconsistent
error payloads across endpoints. That creates systemic problems:

- error codes and message keys get duplicated across bounded contexts;
- the transport error payload becomes unstable and unpredictable;
- API documentation loses a single typed error contract;
- domain and application exceptions leak into the transport layer with no shared policy;
- new contexts start inventing their own error format instead of reusing the platform model.

## Decision

The backend adopts a centralized error model as a mandatory platform baseline.

Platform-registry rules:

- canonical error codes, message keys, categories, severities, and HTTP statuses live centrally in `core/errors`;
- duplicate error codes and message keys are forbidden by registry-level validation;
- application and domain layers raise typed platform errors instead of ad-hoc `HTTPException` values or free-form string errors;
- generic backend failures map to canonical `internal_error` instead of arbitrary 500 payloads.

HTTP-projection rules:

- the canonical HTTP error payload is defined centrally in `core/http/errors.py`;
- app-level `api/errors.py` modules use `ApiErrorFactory` and registry-backed errors instead of assembling response payloads manually;
- `HTTPException(detail={...})` with an ad-hoc dictionary is a baseline violation unless the payload comes from the centralized error factory;
- request validation errors and unhandled exceptions are projected into typed `ApiError` values through shared exception handlers.

Context-ownership rules:

- each bounded context may define its own `api/errors.py` helpers for response docs and translation of domain or platform errors into the transport boundary;
- the source of truth for codes, categories, and message keys remains in `core/errors`;
- per-context API helpers must not create parallel registries or duplicate the platform error catalog.

## Consequences

### Positive

- the backend gets one typed error payload shared by OpenAPI, runtime responses, and exception handling;
- error codes and categories become centralized and validated;
- bounded contexts can add transport-level helpers without losing platform consistency;
- generic and validation failures stop returning arbitrary error payloads.

### Negative

- even simple endpoints must use platform error classes and the shared factory instead of direct `HTTPException`;
- adding a new canonical error requires updating the central registry, not just one route handler.

### Neutral

- the canonical error catalog may grow over time as long as the centralized registry and shared HTTP projection model remain.

## Alternatives considered

- letting each context build its own `HTTPException(detail={...})`;
- keeping the error payload as a free-form dict with no typed transport contract;
- storing error definitions directly in each bounded context's `api/errors.py`;
- mapping generic exceptions directly to plain text or framework-default payloads.

## Follow-up work

- [ ] add a static check against ad-hoc `HTTPException(detail={...})` outside the centralized error factory
- [ ] add more domain-specific registry entries as new bounded contexts appear
- [ ] extend app-level `api/errors.py` helpers in new contexts using the same template
