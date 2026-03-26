# ADR-0009: Separate control plane from heavy execution workers

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0005](./0005-background-jobs-and-workflow-orchestration.md)
- [ADR-0010](./0010-use-taskiq-redis-streams-and-postgresql.md)
- [ADR-0011](./0011-manage-postgresql-schema-with-alembic.md)
- [ADR-0016](./0016-support-github-and-gitea-ci-for-template-repositories.md)

## Context

The system serves different kinds of load: API requests, orchestration,
background computation, periodic reconciliation jobs, and integration
workloads. If everything runs in one runtime process, heavy work starts to harm
control-plane latency and stability.

## Decision

The runtime is split into at least:

- the control plane or API;
- background workers;
- optional scheduled or reconciliation workers.

The control plane must not depend on heavy background tasks for latency or
resources. Local development may use a collapsed topology, but the production
model remains separated.

Schema migrations for the primary relational database are not executed as part
of FastAPI app bootstrap, import-time initialization, or request handling. They
run either as a separate administrative or deployment step, or as an explicit
pre-start step in the backend container entrypoint before the API process
starts.

## Consequences

### Positive

- API stability improves;
- heavy handlers can be scaled independently;
- resource contention between load types is reduced.

### Negative

- operational complexity increases;
- health, coordination, and deployment conventions are required.

### Neutral

- physical implementation may differ between environments while keeping the same logical model.

## Alternatives considered

- one process for everything;
- cron-only or batch-only workers;
- delaying topology separation until problems appear.

## Follow-up work

- [ ] describe runtime roles and responsibilities
- [ ] define health, readiness, and scaling semantics
- [ ] document deployment conventions for environments
