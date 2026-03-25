# ADR-0022: Group backend settings into nested platform models

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0007](./0007-configuration-and-policy-as-code.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-0021](./0021-centralize-backend-observability-bootstrap-and-structured-telemetry.md)

## Context

Flat settings fields work for a tiny scaffold, but they do not scale well once the template owns API runtime, data stores, workers, observability and deployment-facing behavior at the same time. Over time a flat `Settings` model degrades into:

- dozens of top-level fields without clear ownership;
- duplicated prefixes like `app_*`, `api_*`, `observability_*` scattered through code;
- poor discoverability for new platform modules;
- environment examples that do not communicate grouping or intent;
- higher chance of mixing unrelated concerns in bootstrap code.

The maximum template needs a stricter configuration shape that mirrors platform ownership boundaries directly.

## Decision

Backend settings are grouped into nested platform models under a single `Settings(BaseSettings)` root.

Canonical groups:

- `settings.app` for service identity and environment metadata;
- `settings.api` for HTTP runtime configuration;
- `settings.db` for PostgreSQL and Redis connection settings;
- `settings.broker` for Taskiq/stream worker runtime naming;
- `settings.observability` for logging, tracing, metrics and GlitchTip controls.

Rules:

- backend code reads configuration through grouped settings paths such as `settings.api.prefix` or `settings.observability.metrics_path`;
- `.env` and `.env.example` use nested environment keys with `__` separators under the existing repository env prefix;
- computed fallbacks such as observability service identity may derive from `settings.app`, but the owning configuration still lives in grouped models;
- new platform-level configuration must be added to an existing group or to a new explicit nested model, not as another flat top-level field.

## Consequences

### Positive

- settings ownership becomes obvious from the path itself;
- app/bootstrap/runtime code reads cleaner and drifts less;
- `.env.example` documents the platform model instead of just listing unrelated flat variables;
- future extensions like workers, auth or integrations have a clear place in the configuration tree.

### Negative

- existing local environment files must migrate from flat variables to nested keys;
- code changes that touch settings now require coordinated updates across references, examples and tests.

### Neutral

- the root `Settings` object remains the single entrypoint, but its internal shape becomes intentionally hierarchical.

## Alternatives considered

- keep a flat `Settings` model and accept growth in top-level fields;
- split configuration into multiple independent `BaseSettings` roots without a single composition object;
- hardcode runtime-specific configuration near each subsystem instead of modeling ownership in settings.

## Follow-up work

- [ ] add new grouped settings models only when a new platform area appears, not pre-emptively
- [ ] keep `.env.example` aligned with grouped settings names on every config change
- [ ] add integration docs for deployment systems that need nested env variable templates
