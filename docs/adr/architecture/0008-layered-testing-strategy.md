# ADR-0008: Define a layered testing strategy for critical flows

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0002](./0002-api-first-and-contract-versioning.md)
- [ADR-0003](./0003-event-driven-internal-integration.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-0017](./0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)

## Context

Integration, orchestration, and policy failures are expensive. Unit tests alone
are not enough, while relying only on e2e tests makes feedback slow and
expensive.

## Decision

The repository uses a layered testing strategy:

- unit tests for domain logic and pure functions;
- integration tests for storage, message bus, and external adapters;
- contract tests for APIs and events;
- workflow tests for state transitions and orchestration;
- smoke or e2e tests for critical end-to-end scenarios;
- security regression tests for sensitive flows.

Tests live as close as possible to the owning code, while cross-app scenarios
live in root-level `tests/`.

## Consequences

### Positive

- confidence in platform-critical flows increases;
- regressions are caught at the right level faster;
- the test strategy stays balanced in cost and signal quality.

### Negative

- test infrastructure becomes more expensive;
- workflow and e2e tests can be slow and fragile.

### Neutral

- high coverage alone does not guarantee correct architecture or policy behavior.

## Alternatives considered

- relying only on unit tests;
- testing critical flows mostly by hand;
- relying only on e2e tests and skipping lower layers.

## Follow-up work

- [ ] define the test pyramid
- [ ] define the golden scenarios
- [ ] document shared test fixtures
