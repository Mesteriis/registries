# ADR-2000: Centralize template metadata and self-consistency checks

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0000](../architecture/0000-record-architecture-decisions.md)
- [ADR-0015](../architecture/0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-0016](../architecture/0016-support-github-and-gitea-ci-for-template-repositories.md)

## Context

A highly opinionated template quickly degrades if separate hardcoded assumptions
about owner, decider, golden-path commands, and pipeline semantics start to
appear across the repository. When that happens:

- scripts drift in ownership and decider constants;
- the Makefile, pre-commit hooks, and CI stop describing the same engineering baseline;
- dual-CI becomes nominally enabled but effectively asymmetric;
- `specs/` can degrade into placeholder directories with no canonical contract examples.

A golden-master template needs checks not only for code and structure, but also
for the internal consistency of the template itself.

## Decision

The template uses two mandatory mechanisms:

- `template.meta.toml` as the single source of script-level metadata for the owner, ADR decider, and template type;
- self-consistency checks that validate alignment across the Makefile, hooks, CI, Docker targets, and contract scaffold.

Rules:

- ownership and ADR decider must not be hardcoded inside validation scripts;
- the `Makefile`, pre-commit, GitHub CI, and Gitea CI must remain semantically aligned;
- dual-CI is validated by a dedicated symmetry check, not by manual inspection;
- placeholder-only contract directories are not an acceptable state for the maximum template;
- the engineering baseline of the template itself is treated as an ADR-worthy decision, not as an accidental pile of scripts.

## Consequences

### Positive

- ownership assumptions become centralized instead of scattered through scripts;
- the template becomes self-validating not only for code, but also for its own engineering shape;
- dual-CI and the golden-master workflow are easier to maintain without hidden drift;
- derived templates get a more stable starting baseline.

### Negative

- the number of meta-validation checks increases;
- changing template governance requires updates across several related artifacts.

### Neutral

- `template.meta.toml` is not runtime configuration or a feature-flag system; it is repository metadata for the template engineering tooling.

## Alternatives considered

- keep owner and ADR decider as hardcoded constants in scripts;
- treat the Makefile, hooks, and CI as independent layers with no symmetry validation;
- allow placeholder-only `specs/` scaffolding with no canonical contract examples.

## Follow-up work

- [x] introduce `template.meta.toml`
- [x] add a template consistency check
- [x] add a CI symmetry check
- [ ] continue recording new engineering-level governance decisions under `docs/adr/engineering/`
