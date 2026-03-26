# Fullstack Template

`Fullstack Template` is a reusable engineering template for teams that want a
strict fullstack baseline instead of an empty starter.

It is designed to make the first 5 to 10 minutes in the repository predictable:

- what the template is;
- what is already implemented;
- how to run it locally;
- which rules are mandatory;
- which files are the source of truth;
- which parts are only baseline/reference slices, not finished product features.

## What Is Included

- `src/backend/`: FastAPI backend with bounded-context layout, typed settings,
  explicit Unit of Work, structured error model, observability bootstrap,
  pytest/Testcontainers baseline, and import-boundary enforcement.
- `src/frontend/`: Vue 3 frontend with layered `app/pages/features/entities/shared`
  structure, router + shell, local UI adapter boundary, typed config, shared API
  client, OpenAPI-derived generated API bindings, frontend observability baseline,
  and unit/component tests.
- `specs/`: contract-first source artifacts. OpenAPI lives here and remains the
  canonical HTTP API contract.
- `docs/adr/`: architecture decisions, engineering governance, and sample
  domain/product ADRs used as reference material for derived projects.
- `scripts/`, `Makefile`, `.pre-commit-config.yaml`: local and CI quality gates
  that enforce the template instead of leaving rules as documentation only.
- `docker/`, `migrations/`, `.github/`, `.gitea/`: baseline delivery and CI/CD
  assets for reuse.

## Current Status

This repository is a template baseline, not a finished product.

What is production-oriented already:

- repository governance and self-checks;
- backend and frontend architecture boundaries;
- observability baseline on both sides;
- testing, linting, type checking, security and Docker build paths;
- one end-to-end reference slice built around system health.

What is intentionally still baseline/reference:

- the business/domain surface is intentionally thin;
- frontend homepage explains the template instead of acting like a real dashboard;
- local `shared/ui` primitives are adapters, not a branded design system;
- product ADRs describe reference domain decisions, not a claim that the full
  product is already implemented here.

## Quick Start

1. Copy the backend env file:

   ```bash
   cp .env.example .env
   ```

2. Install dependencies and hooks:

   ```bash
   make bootstrap
   ```

3. Start PostgreSQL and Redis.

   Use your own local services, or start quick containers:

   ```bash
   docker run -d --name fullstack-template-postgres \
     -e POSTGRES_USER=fullstack_template \
     -e POSTGRES_PASSWORD=fullstack_template \
     -e POSTGRES_DB=fullstack_template \
     -p 5432:5432 postgres:17

   docker run -d --name fullstack-template-redis \
     -p 6379:6379 redis:7-alpine
   ```

4. Apply migrations:

   ```bash
   cd src/backend && uv run alembic -c ../../alembic.ini upgrade head
   ```

5. Run the backend:

   ```bash
   cd src/backend && uv run uvicorn main:app --reload
   ```

6. Run the frontend in another terminal:

   ```bash
   pnpm -C src/frontend dev
   ```

## Local URLs

- Frontend shell: `http://localhost:5173/`
- Backend root metadata: `http://localhost:8000/`
- Backend API docs: `http://localhost:8000/docs`
- Health endpoint: `http://localhost:8000/api/v1/system/health`
- Readiness endpoint: `http://localhost:8000/api/v1/system/readyz`
- Liveness endpoint: `http://localhost:8000/api/v1/system/livez`

## Daily Commands

- `make doctor`: validate required tooling and repository invariants
- `make check`: run repository invariants
- `make lint`: run backend, frontend and repo linting
- `make test`: run backend and frontend tests
- `make frontend-api-generate`: regenerate frontend API bindings from OpenAPI
- `make contract-test`: run cross-app contract checks from `tests/contract/`
- `make e2e-test`: run root-level smoke scenarios from `tests/e2e/`
- `make build`: run type checks and frontend build
- `make ci`: run the full golden-master local pipeline

## Repository Structure

```text
.
├── src/
│   ├── backend/        # FastAPI service, runtime, tests, migrations ownership
│   └── frontend/       # Vue 3 app, layered UI boundary, frontend tests
├── docs/
│   ├── getting-started.md
│   ├── template/
│   ├── frontend/
│   └── adr/
├── specs/              # canonical OpenAPI / AsyncAPI / JSON Schema contracts
├── scripts/            # repository checks and local automation entrypoints
├── docker/             # reusable container/runtime assets
├── migrations/         # Alembic migrations
├── Makefile
└── .pre-commit-config.yaml
```

## Source Of Truth

- HTTP API contract: [specs/openapi/platform.openapi.yaml](./specs/openapi/platform.openapi.yaml)
- Contract-first rules: [specs/README.md](./specs/README.md)
- Parity enforcement: [scripts/check_http_contract_parity.py](./scripts/check_http_contract_parity.py)
  This check derives the expected HTTP surface from OpenAPI and compares it with backend runtime OpenAPI and frontend bindings.
- Frontend generated API: [src/frontend/shared/api/generated/platform-api.ts](./src/frontend/shared/api/generated/platform-api.ts)
- Template philosophy: [docs/template/PHILOSOPHY.md](./docs/template/PHILOSOPHY.md)
- Architecture reading map: [docs/adr/INDEX.md](./docs/adr/INDEX.md)
- Contribution workflow: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Local/CI control plane: [Makefile](./Makefile), [scripts/](./scripts/), [.pre-commit-config.yaml](./.pre-commit-config.yaml)

If implementation and documentation disagree, fix the disagreement. The repo is
not supposed to rely on tribal knowledge.

## Reference Slice Already Implemented

The current canonical reference slice is `system health`.

It includes:

- backend endpoints under `/api/v1/system/health`, `/readyz`, `/livez`;
- typed backend contracts for readiness and dependency checks;
- a frontend feature that reads the health contract through the shared API client;
- homepage composition that demonstrates the layered frontend shell;
- tests on backend API behavior and frontend rendering.

Treat this slice as a sample of how to build the next bounded context or feature,
not as the beginning of a product dashboard.

## What To Read First

1. This `README.md`
2. [docs/getting-started.md](./docs/getting-started.md)
3. [CONTRIBUTING.md](./CONTRIBUTING.md)
4. [docs/adr/INDEX.md](./docs/adr/INDEX.md)

## What To Customize For A Real Project

- application name, env values and deployment metadata;
- domain-specific OpenAPI/AsyncAPI/JSON Schema contracts in `specs/`;
- bounded contexts under `src/backend/apps/`;
- frontend pages/features/entities built on top of the shared UI/API boundaries;
- external observability endpoints and GlitchTip/OTLP settings;
- product/domain ADRs to match the real problem space;
- CI secrets, container registry settings and deployment topology.

## Notes For Derived Projects

- Keep the strictness if you keep the scope.
- Remove unused template parts deliberately instead of weakening checks in place.
- Do not treat the reference slice or sample ADRs as mandatory product shape.
