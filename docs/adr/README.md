# ADR

The ADR catalog is split into three independent categories:

- [architecture/](./architecture/README.md) for architecture decisions and engineering principles that must not depend on the current product name.
- [product/](./product/README.md) for reference domain and product decisions that show how the template captures domain rules through ADRs. They do not mean the repository is already a finished product.
- [engineering/](./engineering/README.md) for template-level and repository-governance decisions that describe self-validation, metadata, CI symmetry, and the engineering baseline.

Before changing code, CI, contracts, runtime topology, or the ADR set itself,
read [INDEX.md](/adr/INDEX) first. It is the mandatory reading map for humans
and AI agents.

## Formatting Principles

- one ADR = one decision;
- an ADR records the decision, not the background discussion;
- if a decision changes, create a new ADR and link the old one through `Supersedes` or `Superseded by`;
- language-specific coding conventions should not automatically become ADRs unless they are truly architectural.

## Numbering

- `0000-0999` for architecture ADRs;
- `1000-1999` for product ADRs;
- `2000-2999` for engineering ADRs.

## Statuses

- `Proposed`
- `Accepted`
- `Rejected`
- `Deprecated`
- `Superseded`

## Template

Each ADR uses the same structure:

- `Status`
- `Date`
- `Deciders`
- `Supersedes`
- `Superseded by`
- `Context`
- `Decision`
- `Consequences`
- `Alternatives considered`
- `Follow-up work`

## Neutrality Rule

Architecture ADRs must be written without binding them to a brand, a product
name, or current marketing language. The wording must describe architectural
principles, constraints, component roles, and operational requirements.
