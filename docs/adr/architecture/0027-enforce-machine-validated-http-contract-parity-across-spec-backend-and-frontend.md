# ADR-0027: Enforce machine-validated HTTP contract parity across spec, backend and frontend

- Status: Accepted
- Date: 2026-03-26
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0002](./0002-api-first-and-contract-versioning.md)
- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)
- [ADR-0023](./0023-layer-the-frontend-into-app-pages-features-entities-and-shared.md)

## Context

API-first is not enough if backend implementation, frontend clients, and typed
frontend models can silently drift away from `specs/`.

For a strict template this is especially dangerous:

- the frontend starts depending on a path or shape that no longer exists on the backend;
- a backend response model changes while frontend clients or types stay stale;
- OpenAPI remains a statement of intent rather than a validated source of truth;
- drift is discovered too late, at runtime or through manual inspection.

A claim of “100% parity” cannot honestly be proven for arbitrary handwritten
code through generic linting. But the template can and must enforce the
strongest possible parity policy for template-owned HTTP surfaces when the
expected surface is derived automatically from the canonical OpenAPI spec.

## Decision

The repository adopts a machine-validated HTTP contract parity policy:

- `specs/` remains the source of truth for the public HTTP contract;
- the expected parity map is derived automatically from `specs/openapi/platform.openapi.yaml`, not stored as a separate manual manifest;
- template-owned backend routes and response contracts must stay explicitly aligned with canonical spec paths and shapes;
- template-owned frontend client paths and typed models must stay explicitly aligned with the same contract;
- for template-owned frontend HTTP slices, the preferred baseline is generated client and type code from OpenAPI plus thin entity-layer wrappers;
- parity must be checked automatically through repository checks and local hooks, not only through unit or integration tests;
- each template-owned HTTP reference slice must have an explicit parity check that fails the repository on drift.

In the current baseline this applies to the canonical `system health` slice:

- OpenAPI contract in `specs/openapi/platform.openapi.yaml`;
- backend runtime OpenAPI from `FastAPI.app.openapi()` and contracts under `src/backend/apps/system/`;
- generated frontend API under `src/frontend/shared/api/generated/`;
- thin entity-layer wrappers under `src/frontend/entities/system/`;
- root-level contract tests under `tests/contract/`.

## Consequences

### Positive

- drift between spec, backend, and frontend is caught before runtime;
- `specs/` stops being a purely aspirational document;
- the parity policy no longer needs a separate manual list of expected paths and schema names;
- handwritten clients remain acceptable only when parity is still machine-enforced;
- the template becomes a safer baseline for derived projects.

### Negative

- generic proof of semantic equivalence for all code remains impossible;
- every new HTTP slice must get the same parity automation or the policy becomes incomplete.

### Neutral

- generated clients are the preferred baseline, but they do not replace the requirement for a source-of-truth spec, thin wrappers, and parity validation;
- contract tests and lint-like parity checks complement each other rather than replacing each other.

## Alternatives considered

- relying only on unit, integration, or e2e tests;
- relying on code review and manual discipline with no machine enforcement;
- trying to build a generic AST-level prover for any backend/frontend contract surface.

## Follow-up work

- [ ] expand spec-derived parity coverage as new template-owned HTTP slices appear
- [ ] define where derived projects stay on thin wrappers over generated clients and where a fuller generated SDK layer is needed
