# ADR-0018: Enforce typed contracts and Unit of Work owned persistence

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0002](./0002-api-first-and-contract-versioning.md)
- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0010](./0010-use-taskiq-redis-streams-and-postgresql.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0017](./0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [ADR-0019](./0019-centralize-persistence-behind-repositories-query-services-and-exhaustive-layer-contracts.md)

## Context

Even with a good package layout, the backend quickly degrades if layers start
talking through raw `dict` values, endpoints own transactions, and business
flows bypass repositories or work directly with `AsyncSession`. That creates
several systemic problems:

- boundaries between transport, application, and persistence become implicit;
- typed contracts are replaced with ad-hoc dictionaries that are harder to validate and evolve safely;
- services and workers start owning low-level transaction lifecycle without one shared policy;
- database reads and writes spread across endpoints, tasks, and helper modules;
- async runtime paths start mixing with sync-style procedural code.

## Decision

The backend uses a typed, repository-driven, Unit-of-Work-owned execution
model.

Boundary-contract rules:

- layers do not communicate through raw `dict` values;
- only `dataclass` or Pydantic-based structures are allowed across layers;
- transport payloads, application commands and results, repository inputs and outputs, and query/read models must be typed;
- raw `dict` values are acceptable only at parsing or serialization edges or inside low-level infrastructure, not as cross-layer contracts.

Runtime-shape rules:

- endpoints stay `async-first` function handlers;
- application services, repositories, query services, clients, and other non-endpoint components are designed `class-first`;
- endpoints own transport wiring and service invocation, but not transaction orchestration;
- endpoints receive already-assembled service or gateway dependencies through providers and do not build repositories, UoW objects, or low-level clients inside handlers;
- active backend paths must stay predictable and typed across the whole request.

Persistence rules:

- database access goes only through repositories or query services;
- the read path uses query services and typed immutable read models by default;
- endpoints, services, and workers do not talk to `AsyncSession` or SQL directly outside the repository boundary;
- transactions are owned by the `Unit of Work`;
- the `Unit of Work` is the single owner of commit, rollback, and transaction policy;
- side effects that depend on a successful commit should respect the transaction boundary and ideally run post-commit.

Layer roles:

- endpoint: accept the request, validate the transport boundary, call the service, return a typed response;
- service: orchestrate the use case, use repositories and domain policies, and stay unaware of transport details;
- repository: the write boundary to the database on the write path;
- query service: a typed read boundary for read-heavy flows when repository abstraction is not enough;
- Unit of Work: own session lifecycle and transaction boundary.

## Consequences

### Positive

- cross-layer contracts become testable and safer to refactor;
- transaction ownership becomes centralized instead of leaking into endpoints or workers;
- persistence code stays concentrated in repositories and query services rather than spreading across runtime paths;
- the async API layer and class-based services get a clear role split.

### Negative

- even simple scenarios require typed structures and repository or UoW wiring instead of shortcuts;
- the write path becomes stricter and does not allow fast direct-session hacks.

### Neutral

- the specific UoW and repository internals may change as long as typed boundaries and ownership rules remain intact.

## Alternatives considered

- allowing layers to exchange raw `dict[str, object]`;
- allowing direct `AsyncSession` access from endpoints and services;
- building the backend in a procedural style with no class-based services or repositories;
- treating the repository pattern as optional and using it only selectively.

## Follow-up work

- [ ] add static checks against raw `dict` layer contracts on the backend path
- [ ] add a template scaffold for Unit of Work, repositories, and typed command or result contracts
- [ ] strengthen backend architecture validation against direct session access outside repository and UoW layers
