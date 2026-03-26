# ADR-0015: Enforce template quality gates and governance baseline

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0002](./0002-api-first-and-contract-versioning.md)
- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0012](./0012-define-repository-layout-and-file-placement-rules.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0016](./0016-support-github-and-gitea-ci-for-template-repositories.md)
- [ADR-0021](./0021-centralize-backend-observability-bootstrap-and-structured-telemetry.md)
- [ADR-2000](../engineering/2000-centralize-template-metadata-and-self-consistency-checks.md)

## Context

A template repository is valuable only if it transfers a working engineering
baseline, not just a set of files. Without that, derived projects drift
quickly:

- architecture constraints remain only in ADRs and are not checked automatically;
- spec-first becomes a declaration with no naming or placement enforcement;
- local developer workflow and CI return different results;
- governance artifacts such as `CODEOWNERS`, the contribution guide, and security policy appear inconsistently;
- baseline security checks arrive too late, after services already exist.

## Decision

The template repository must include one shared quality and governance baseline:

- machine-enforced checks for ADRs, repository structure, backend architecture, and spec placement;
- a local automation layer through `Makefile` and `pre-commit`;
- governance artifacts such as `CODEOWNERS`, `CONTRIBUTING.md`, `SECURITY.md`, and issue or PR templates;
- baseline security checks such as dependency audit, `bandit`, `trivy`, `hadolint`, and `shellcheck`;
- a frontend baseline with lint, type-check, unit tests, and production build;
- a backend baseline with lint, format, type-check, import boundaries, architecture checks, and tests.

Spec-first baseline:

- `specs/` remains the source of truth for contracts;
- naming rules for OpenAPI, AsyncAPI, and JSON Schema are validated automatically;
- generated artifacts remain derived artifacts and never replace the source contracts.

DX baseline:

- the repository must expose a short set of canonical commands for sync, check, lint, test, and build;
- local hooks must stay compatible with the CI pipeline rather than creating a separate alternative process.

## Consequences

### Positive

- new projects get a working engineering discipline instead of only a scaffold;
- architectural drift is caught earlier and more cheaply;
- onboarding becomes shorter and more predictable;
- security and governance stop being optional follow-up work.

### Negative

- the initial template becomes heavier in checks and support files;
- maintaining the baseline requires regular tooling and workflow updates.

### Neutral

- concrete tools inside the baseline may evolve as long as the principle of machine-enforced quality gates remains.

## Alternatives considered

- relying only on README and ADRs without automated checks;
- leaving governance and security baseline decisions to every new project;
- including only language-specific lint and tests with no repo-wide rules.

## Follow-up work

- [x] add repo-wide validators for architecture and specs
- [x] add governance baseline files
- [x] add DX entrypoints for local quality gates
- [ ] add a template bootstrap/init flow for renaming project-specific identifiers
