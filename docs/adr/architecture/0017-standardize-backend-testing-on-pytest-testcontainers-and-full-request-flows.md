# ADR-0017: Standardize backend testing on pytest, Testcontainers and full request flows

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0010](./0010-use-taskiq-redis-streams-and-postgresql.md)
- [ADR-0011](./0011-manage-postgresql-schema-with-alembic.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)

## Context

The layered testing strategy already exists, but backend-specific rules for the
test harness, doubles, and test data were still easy to dilute. Without a hard
policy, teams quickly fall into several bad patterns:

- using SQLite as a cheap substitute for PostgreSQL and hiding real storage constraints;
- skipping Redis tests or replacing them with in-memory fakes;
- mocking internal services and repositories so heavily that tests stop validating the real execution path;
- building test payloads from raw `dict` objects and weakening contract boundaries;
- scattering fixtures and helpers through random files instead of mirroring the project structure.

## Decision

Backend testing is standardized as follows.

Test runtime:

- `pytest` is the only backend test runner;
- integration and persistence tests use real `PostgreSQL` and `Redis` through `Testcontainers`;
- SQLite is forbidden as the backend test database and is not an accepted substitute for `PostgreSQL`;
- migrations and persistence behavior are validated against the same relational model used by the production path.

Allowed execution path:

- backend integration and API tests validate the full path `request -> endpoint -> service -> repo -> db -> repo -> service -> endpoint -> response`;
- internal services, repositories, Unit of Work objects, and persistence adapters are not mocked in normal backend tests;
- when testing an external API client, substitution happens through a fake external service with predictable responses rather than by mocking internal methods;
- only external API boundaries and external side effects outside the service's ownership may be mocked.

Test data and factories:

- test data is created through `faker` and `polyfactory`;
- raw `dict` objects are not the main way to build test input and output;
- payloads and expected values should be assembled through typed models, factories, dataclasses, or Pydantic structures;
- fixtures and factories must provide repeatable, typed arrangements.

Test organization:

- the test tree mirrors the project structure;
- backend tests live under `src/backend/tests/` and reflect `apps/`, `core/`, and `runtime/`;
- fixtures are declared only in `conftest.py` files at the appropriate scope;
- tests are written as function-based pytest tests only;
- class-based test containers, `unittest.TestCase`, and grouping through test classes are forbidden.

## Consequences

### Positive

- integration tests validate the real backend flow instead of a pre-mocked call chain;
- persistence and transaction behavior are exercised against production-like `PostgreSQL` and `Redis`;
- test data keeps typed boundaries and survives refactors better;
- test structure stays predictable and mirrors the service structure.

### Negative

- integration tests are heavier and slower than SQLite or in-memory doubles;
- fake external services require more setup than direct monkeypatching.

### Neutral

- unit tests for pure domain logic remain valid, but they still should use typed factories and function-based pytest style.

## Alternatives considered

- using SQLite for cheap repository tests;
- mocking services and repositories in most endpoint tests;
- using raw `dict` payload builders as the main form of test data;
- allowing test classes and arbitrary fixture placement next to individual test files.

## Follow-up work

- [ ] add backend test tooling for `Testcontainers` with `PostgreSQL` and `Redis`
- [ ] add static checks against SQLite and class-based pytest tests
- [ ] add `faker` and `polyfactory` factories to the template baseline
