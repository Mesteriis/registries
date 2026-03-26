# ADR-0012: Define repository layout and file placement rules

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0001](./0001-monorepo-and-bounded-contexts.md)
- [ADR-0002](./0002-api-first-and-contract-versioning.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-0016](./0016-support-github-and-gitea-ci-for-template-repositories.md)

## Context

The high-level monorepo decision already exists, but without exact placement
rules the repository quickly degrades: language-specific manifest files drift
back to the root, tests end up far from the owning code, and infrastructure
directories appear ad hoc. Repo-wide layout and internal app architecture must
also stay separate decisions.

## Decision

The repository layout baseline is:

- `src/backend/` for backend service roots, backend manifests, and backend tests;
- `src/frontend/` for frontend application code, frontend manifests, and frontend tests;
- `specs/` for OpenAPI, AsyncAPI, and JSON Schema contracts;
- `migrations/` for versioned primary relational database migrations;
- `tests/contract` and `tests/e2e` only for cross-app scenarios;
- `docker/` and `scripts/` for runtime, deployment, and automation.

Placement rules:

- application-local manifests stay next to the owning app, not at repository root;
- backend test suites live under `src/backend/tests/` and mirror backend service topology;
- frontend component-level tests stay under the frontend app root;
- root `tests/` is not used for app-local test suites;
- empty but mandatory directories may be preserved with `.gitkeep`;
- a new root directory is allowed only for repo-wide concerns, not for one app;
- `packages/` is reserved for future shared or generated repo-wide code under that exact name;
- `infra/` is reserved for future IaC and deployment-level configuration under that exact name;
- the internal structure of a backend service root is not defined by this ADR and belongs to a separate architecture decision.

## Consequences

### Positive

- repository layout becomes predictable;
- structure can be validated automatically;
- empty directories without a clear owner or use case are avoided;
- the repo is less likely to drift back to a Python-first or framework-first root.

### Negative

- keeping the structure clean requires discipline;
- temporary experiment files still need to be placed correctly rather than dropped into the root.

### Neutral

- layout rules do not define module architecture inside each application; they define placement rules at repository level.

## Alternatives considered

- relying only on the high-level monorepo ADR;
- not fixing a concrete layout model and deciding placement case by case;
- storing app-local tests and manifests at repository root.

## Follow-up work

- [x] enforce the layout through automated `pre-commit` checks
- [x] keep repo-wide layout rules separate from backend service architecture
- [x] remove optional `packages/` and `infra/` from the current scaffold while keeping them as reserved roots
- [ ] document new repo-wide directories through separate ADRs when needed
- [ ] keep the contribution guide aligned with the layout rules
