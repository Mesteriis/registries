# Contributing

Start here before changing runtime or architecture:

1. [README.md](./README.md)
2. [docs/getting-started.md](./docs/getting-started.md)
3. [docs/adr/INDEX.md](./docs/adr/INDEX.md)

## Workflow

1. Update specs first when changing public contracts.
2. Keep ADRs in sync with architecture-level decisions.
3. Run `make doctor` before opening a PR.
4. Run `make ci` before opening a PR that changes runtime, CI, tooling or contracts.
5. Include migrations in the same PR as relational schema changes.

## Placement Rules

- App code lives under `src/`
- Cross-app tests live only in `tests/`
- Migrations live in `migrations/`
- Contract sources live in `specs/`

`specs/` remains the source of truth for public API contracts.

## Pull Requests

- explain the intent
- describe contract, schema or runtime impact
- list manual verification if automation is not enough
