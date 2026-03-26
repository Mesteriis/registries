# ADR-0010: Use Taskiq with Redis Streams for background jobs and PostgreSQL for primary relational state

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0005](./0005-background-jobs-and-workflow-orchestration.md)
- [ADR-0009](./0009-deployment-topology-and-runtime-model.md)
- [ADR-0011](./0011-manage-postgresql-schema-with-alembic.md)
- [ADR-1004](../product/1004-storage-strategy-for-artifacts-metadata-and-decisions.md)

## Context

The platform needs:

- deferred tasks and background workers for heavy processing;
- reliable transactional storage for metadata, policy decisions, audit, and pipeline state.

High-level ADRs already require background jobs and separate storage concerns,
but without a concrete infrastructure choice the decision stays vague.

## Decision

The baseline stack is:

- `Taskiq` as the runtime and programming model for background jobs;
- `Redis Streams` as the broker between producers and workers;
- `PostgreSQL` as the primary relational database for metadata, state, policy decisions, audit, and other durable transactional data.

Responsibility boundaries:

- the broker is responsible for task delivery and execution coordination;
- `PostgreSQL` is the source of truth for domain state;
- `Redis Streams` is not treated as long-term business-state storage;
- schema evolution for `PostgreSQL` is managed through versioned migrations and detailed in the dedicated Alembic ADR.

## Consequences

### Positive

- the async-processing stack becomes explicit and understandable;
- worker and workflow development becomes easier;
- transactional state and audit stay in mature SQL storage.

### Negative

- the system depends on two infrastructure components;
- idempotency and retry behavior must be designed carefully;
- operational expertise is needed for both Redis Streams and PostgreSQL.

### Neutral

- concrete broker or database implementations may change later through a new ADR without changing the underlying architectural model.

## Alternatives considered

- handling background jobs only through cron or batch processing;
- using only PostgreSQL with no dedicated job broker;
- using Redis both as broker and as primary state storage;
- leaving the technology choice open until later.

## Follow-up work

- [ ] define naming conventions for queues and job types
- [ ] document retry, timeout, and dead-letter policy for `Taskiq`
- [ ] define how job outcome and execution history are stored in `PostgreSQL`
