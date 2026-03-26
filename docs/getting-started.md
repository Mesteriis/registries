# Getting Started

This document is the fast path for new developers. Read this before going deep
into ADRs.

## Prerequisites

Required local tools:

- `git`
- `make`
- `uv`
- `pnpm`
- `pre-commit`
- `docker`

If you want the full local quality pipeline, you also need:

- `shellcheck`
- `hadolint`
- `trivy`

You can verify the expected toolchain with:

```bash
make doctor
```

## Environment Setup

Copy the template env file at the repository root:

```bash
cp .env.example .env
```

The backend reads `.env` with the `FULLSTACK_TEMPLATE_` prefix. The defaults are
already wired for local development:

- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`
- backend API on `http://localhost:8000`

The frontend works without an extra env file for local development. By default it
uses the current browser origin and Vite proxies `/api` to the backend.

If you need to override frontend settings, create `src/frontend/.env.local`, for
example:

```env
VITE_APP_NAME=Fullstack Template
VITE_DEV_PROXY_TARGET=http://127.0.0.1:8000
```

## Install Dependencies

Bootstrap both apps and install local git hooks:

```bash
make bootstrap
```

## Start Local Services

Use your own PostgreSQL and Redis, or start quick containers:

```bash
docker run -d --name fullstack-template-postgres \
  -e POSTGRES_USER=fullstack_template \
  -e POSTGRES_PASSWORD=fullstack_template \
  -e POSTGRES_DB=fullstack_template \
  -p 5432:5432 postgres:17

docker run -d --name fullstack-template-redis \
  -p 6379:6379 redis:7-alpine
```

## Run The Backend

Apply migrations first:

```bash
cd src/backend && uv run alembic -c ../../alembic.ini upgrade head
```

Start the API:

```bash
cd src/backend && uv run uvicorn main:app --reload
```

Useful backend URLs:

- root metadata: `http://localhost:8000/`
- docs: `http://localhost:8000/docs`
- health: `http://localhost:8000/api/v1/system/health`

## Run The Frontend

In another terminal:

```bash
pnpm -C src/frontend dev
```

Frontend URL:

- app shell: `http://localhost:5173/`

## Quality Checks

Common commands:

- `make check`
- `make contract-parity`
- `make lint`
- `make test`
- `make contract-test`
- `make e2e-test`
- `make build`
- `make ci`

App-specific commands:

- frontend API generation: `make frontend-api-generate`
- backend tests: `python3 scripts/run_backend_tests.py`
- frontend tests: `python3 scripts/run_frontend_tests.py`
- frontend build: `python3 scripts/run_frontend_build.py`

## Typical Developer Workflow

1. Read `README.md` and this document.
2. Check `specs/` before changing public contracts.
3. Read `docs/adr/INDEX.md` before changing architecture, runtime or governance.
4. Make the change in the owning layer only.
5. Run the smallest relevant checks locally.
6. Run `make doctor` and `make ci` before a large PR or infrastructure change.

## First-Run Problems

`uv` or `pnpm` is missing:
- install the missing tool, then rerun `make doctor`.

Backend cannot connect to PostgreSQL or Redis:
- verify local services are running;
- verify `.env` matches your local ports and credentials.

`alembic upgrade head` fails:
- confirm PostgreSQL is reachable and the database exists;
- confirm `FULLSTACK_TEMPLATE_DB__POSTGRES_DSN` in `.env`.

Frontend shows health errors on the homepage:
- check that the backend is running on `localhost:8000`;
- if you changed backend host/port, update `VITE_DEV_PROXY_TARGET` or `VITE_API_BASE_URL`.

Pre-commit hooks fail on unrelated paths:
- hooks are path-scoped now, so check whether you also changed root/shared files
  such as `Makefile`, `scripts/`, `docs/`, or `specs/`.

You are unsure which document is normative:
- `specs/` is the source of truth for public contracts;
- ADRs are the source of truth for architecture-level decisions;
- code and checks must stay aligned with both.
