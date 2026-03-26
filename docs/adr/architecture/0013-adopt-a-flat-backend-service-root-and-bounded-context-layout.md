# ADR-0013: Adopt a flat backend service root and bounded-context layout

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0009](./0009-deployment-topology-and-runtime-model.md)
- [ADR-0012](./0012-define-repository-layout-and-file-placement-rules.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0017](./0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)

## Context

Repository layout alone does not answer how the backend service should be
organized internally. Without a separate decision, code quickly degrades into a
mix of root directories like `api/`, `domain/`, and `infrastructure/` with no
clear top-level model, and imports start relying on a namespace layer that adds
no architectural value.

This creates several problems:

- `src/backend` gains an unnecessary wrapper namespace with no real boundary value;
- top-level layers mix with bounded contexts;
- new modules copy the layout inconsistently;
- the backend loses the distinction between transport, application, platform kernel, and runtime workers.

## Decision

Each backend service uses a flat service root directly inside `src/backend/`.

Repository layout:

```text
src/backend/
  api/
  apps/
  core/
  runtime/
  main.py
  tests/
  pyproject.toml
```

Package-layout rules:

- `src/backend` is both the service root for backend code and the repository-local root for manifests, tests, and tooling;
- runtime imports start with `api.*`, `apps.*`, `core.*`, and `runtime.*`;
- the top-level backend service root is split into `api`, `apps`, `core`, and `runtime`;
- `apps/` contains bounded contexts;
- `core/` contains the minimal shared platform kernel;
- `runtime/` contains workers, stream consumers, schedulers, and orchestration primitives;
- `tests/` mirrors the backend service topology rather than a legacy flat root layout.

Each bounded context under `apps/<context>/` uses the same internal template:

```text
apps/<context>/
  api/
  application/
  contracts/
  domain/
  infrastructure/
```

Top-level package ownership:

- `api` owns HTTP versioning, root router composition, and transport wiring, but it is not a warehouse for app-level contracts;
- `apps` owns domain-focused bounded contexts;
- `core` owns shared settings, bootstrap, DB primitives, and other stable platform modules;
- `runtime` owns async workers, background orchestration, and messaging runtime.

Context-layer ownership:

- `api` for transport adapters, dependency wiring, and response mapping;
- `application` for use cases and orchestration;
- `contracts` for typed boundary models owned by the bounded context;
- `domain` for business rules, entities, and policies;
- `infrastructure` for persistence and technical adapters.

Contract ownership rule:

- app-level contracts live in `apps/<context>/contracts`;
- top-level `api/` must not accumulate per-context request and response schemas;
- truly global transport envelopes are allowed only as rare exceptions and must not replace bounded-context ownership.

## Consequences

### Positive

- the backend gets a shorter, clearer import graph with no artificial namespace wrapper;
- bounded contexts become the first architectural layer rather than a side effect of file placement;
- static checks for import boundaries and package ownership become easier to add;
- bootstrap, runtime, and transport responsibilities stop mixing at the root.

### Negative

- the initial structure is heavier than a flat scaffold;
- even small temporary modules must be placed in the correct bounded context and layer.

### Neutral

- the specific top-level package names are fixed by this ADR and do not require another service package wrapper.

## Alternatives considered

- keeping `api`, `domain`, `infrastructure`, and `settings` directly at `src/backend` root with no bounded contexts;
- using `src.backend.*` as the runtime import namespace;
- wrapping the backend in another service package under `src/backend`;
- organizing the backend only by technical layers and not by bounded contexts.

## Follow-up work

- [x] create the initial backend service root and `system` context scaffold
- [x] move the initial FastAPI entrypoint to the flat service root
- [ ] add static checks for import boundaries between top-level packages and context layers
