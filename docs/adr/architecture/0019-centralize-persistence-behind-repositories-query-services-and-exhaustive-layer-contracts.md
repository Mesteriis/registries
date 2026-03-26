# ADR-0019: Centralize persistence behind repositories, query services and exhaustive layer contracts

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0017](./0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)

## Context

Experience from earlier systems showed that the basic
`api/application/domain/infrastructure` layer scheme is not enough on its own.
Without explicit read and write boundaries and explicit enforcement, the system
quickly drifts into anti-patterns:

- routes, workers, and services accept `AsyncSession` directly;
- reads happen through raw ORM or session helpers instead of a dedicated read boundary;
- writes happen from service helpers, tasks, and endpoint handlers outside repositories;
- repositories start owning `commit()` and `rollback()` instead of acting as persistence adapters;
- the read path returns ORM entities or ad-hoc `dict` values instead of typed immutable read models;
- import boundaries between `api`, `runtime`, `apps`, and `core` remain a declaration with no exhaustive static enforcement.

## Decision

The backend adopts a repository/query/UoW model as the mandatory execution
baseline.

Read/write boundaries:

- all write operations go only through repositories;
- all read operations go only through query services;
- query services are the default read boundary for list, detail, dashboard, and query flows;
- query services return typed immutable read models or other typed read contracts;
- repositories are the only write boundary to `PostgreSQL` on the active backend path.

Transaction ownership:

- the `Unit of Work` is the single authority for commit, rollback, transaction boundaries, and after-commit hooks;
- repositories must not call `commit()` or `rollback()`;
- query services never call `commit()`;
- routes, workers, tasks, and application services may initiate `uow.commit()` only as the use-case boundary and must not bypass the repository/query split;
- side effects that depend on a successful transaction must be placed on a post-commit path owned by the Unit of Work.

Session ownership:

- routes, workers, and public service boundaries must not accept raw `AsyncSession` as a primary dependency;
- routes and public endpoints receive assembled service or query-gateway dependencies instead of building the persistence graph inside handlers;
- direct session handling on the active runtime path is forbidden outside UoW, repositories, query services, and low-level persistence primitives;
- direct SQL or raw ORM access outside the repository/query boundary is an architectural violation by default.

Bounded-context ownership:

- each bounded context owns its own routers, contracts, services, repositories, query services, and read models;
- modules must not leak persistence models or raw session objects across boundaries;
- read models are the default result type for the read path;
- presenters and response mappers build transport schemas from typed read models or service results, not from ORM entities or ad-hoc dict payloads.

Dependency enforcement:

- the top-level contract between `api`, `runtime`, `apps`, and `core` should be exhaustive;
- every allowed exception must be captured in an explicit allowlist in static checks or import-linter configuration;
- temporary implicit exceptions with no allowlist and no architecture decision are forbidden.

## Consequences

### Positive

- read and write paths become predictable and consistent across API, workers, and tasks;
- transaction ownership stops leaking into repositories or route handlers;
- query services and immutable read models make read contracts easier to stabilize;
- import-boundary drift becomes visible and testable through exhaustive static rules;
- bounded contexts keep full ownership of their persistence contracts.

### Negative

- the codebase needs more formal abstractions even for simple flows;
- new flows require choosing repository, query-service, and UoW boundaries early instead of using direct session shortcuts.

### Neutral

- specific filenames such as `query_services.py`, `repositories.py`, or `read_models.py` may vary as long as the roles and ownership rules remain intact.

## Alternatives considered

- allowing direct `AsyncSession` injection into routes and services;
- treating the repository pattern as optional and using it only for some write flows;
- reading directly through ORM or session helpers with no query services;
- keeping import-boundary exceptions implicit and unvalidated.

## Follow-up work

- [ ] strengthen backend static checks against direct session access outside repository, query, and UoW layers
- [ ] extend import-boundary enforcement toward an exhaustive allowlist model
- [ ] add a template scaffold for query services and immutable read models inside bounded contexts
