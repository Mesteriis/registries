# ADR-0003: Use event-driven integration for internal workflows

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0004](./0004-observability-and-audit-trail.md)
- [ADR-0005](./0005-background-jobs-and-workflow-orchestration.md)
- [ADR-0009](./0009-deployment-topology-and-runtime-model.md)
- [ADR-0010](./0010-use-taskiq-redis-streams-and-postgresql.md)

## Context

Internal platform processes vary in latency and are often naturally
asynchronous. Orchestrating every step synchronously inside a request lifecycle
increases coupling and makes the system less resilient.

## Decision

Internal workflows use an event-driven model.

Components:

- publish domain events;
- subscribe to relevant events;
- process them asynchronously and idempotently;
- preserve correlation and causation identifiers.

Synchronous commands remain acceptable only for short operations that require
immediate feedback.

## Consequences

### Positive

- heavy processes scale more cleanly;
- pipelines are easier to extend with new stages;
- coupling between components is reduced.

### Negative

- end-to-end debugging becomes harder;
- idempotency, replay, tracing, and schema governance are required;
- eventual consistency appears.

### Neutral

- the event-driven model does not forbid small synchronous interactions.

## Alternatives considered

- a fully synchronous orchestration layer;
- cron-driven batch processing;
- tight coupling through direct service calls.

## Follow-up work

- [ ] choose an event bus
- [ ] define the standard event envelope
- [ ] lock down `correlation_id` and `causation_id`
