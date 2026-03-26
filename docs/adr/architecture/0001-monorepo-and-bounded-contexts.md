# ADR-0001: Use a monorepo with explicit bounded contexts

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0002](./0002-api-first-and-contract-versioning.md)
- [ADR-0012](./0012-define-repository-layout-and-file-placement-rules.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)

## Context

The system combines multiple applications, contracts, and operational assets.
Without explicit boundaries, the repository quickly turns into a flat directory
set with high coupling and unclear ownership.

## Decision

The repository uses a monorepo, but with explicit bounded contexts and a
neutral source root.

Baseline structure:

- `src/` for applications;
- `specs/` for contracts;
- `tests/` for cross-app scenarios;
- `docs/` for decisions and documentation;
- `docker/` and `scripts/` for runtime and automation.

Boundary principles:

- each application owns its local code, manifest files, and tests;
- if repo-wide shared or generated code appears later, the reserved root is `packages/`, not ad-hoc names such as `shared/` or `libs/`;
- if repo-wide IaC or deployment configuration appears later, the reserved root is `infra/`, not arbitrary alternatives;
- the repository root stays polyglot and does not look like the root of a single language or runtime;
- cross-context dependencies go through explicit contracts rather than arbitrary imports.

## Consequences

### Positive

- repository navigation becomes easier;
- responsibility boundaries are easier to enforce;
- the system is easier to scale to new applications and stacks.

### Negative

- placement discipline must be maintained;
- early decomposition can feel stricter than an ad-hoc approach.

### Neutral

- a monorepo does not imply a monolithic architecture inside the code.

## Alternatives considered

- a flat structure with no bounded contexts;
- multiple separate repositories;
- a layout organized only by technical layers and not by domain boundaries.

## Follow-up work

- [ ] define cross-context dependency rules
- [ ] document ownership for the main repository areas
- [ ] define the minimal shared kernel
