# ADR-0002: Adopt API-first design and explicit contract versioning

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0001](./0001-monorepo-and-bounded-contexts.md)
- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0012](./0012-define-repository-layout-and-file-placement-rules.md)
- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)

## Context

The system exposes external and internal interfaces: HTTP APIs, events, data
schemas, and generated clients. If contracts are written after implementation,
drift begins between runtime code, clients, and tests.

## Decision

The repository follows an API-first process:

- change the contract first;
- update examples and versions next;
- regenerate artifacts;
- implement the code;
- update contract tests last.

Breaking changes are allowed only through a new contract version. Contracts live
in `specs/` and remain the source of truth for public surfaces.

## Consequences

### Positive

- contract drift is reduced;
- backend and frontend synchronization becomes easier;
- the contract becomes a reviewable artifact instead of a side effect of the implementation.

### Negative

- every API change adds an explicit extra step;
- versioning and example maintenance require discipline.

### Neutral

- not every internal call needs to be HTTP, but contract ownership still applies.

## Alternatives considered

- code-first development with no explicit contract governance;
- unversioned APIs;
- versioning only during major releases.

## Follow-up work

- [ ] define naming conventions for endpoints and event types
- [ ] lock down the error envelope
- [ ] document pagination, filtering, and sorting rules
