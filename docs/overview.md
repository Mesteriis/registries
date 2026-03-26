# Template Overview

`Fullstack Template` is a reusable engineering template for teams that want a
strict fullstack baseline rather than an empty starter.

This page is the site-local equivalent of the root repository README. Use it
when you want the public documentation portal version of the same orientation.

## What The Template Already Includes

- A FastAPI backend under `src/backend/` with bounded contexts, typed settings,
  explicit Unit of Work semantics, structured error handling, observability
  bootstrap, Alembic migrations, and pytest/Testcontainers validation.
- A Vue 3 frontend under `src/frontend/` with layered
  `app/pages/features/entities/shared` architecture, router shell, adapter-style
  UI boundary, typed runtime config, OpenAPI-derived generated client bindings,
  and frontend observability baseline.
- Contract-first artifacts under `specs/`, including canonical OpenAPI and
  machine-enforced parity checks across spec, backend runtime, and frontend
  bindings.
- ADR-driven governance in `docs/adr/`, with architecture, engineering, and
  reference product decisions kept version-controlled.
- Local and CI automation through `Makefile`, `pre-commit`, `pre-push`, GitHub
  Actions, Gitea Actions, Dockerfiles, and compose files.

## Current Status

This repository is a template baseline, not a finished product.

Production-oriented baseline already exists for:

- architecture boundaries;
- observability bootstrap;
- testing, type-checking, linting, security, and Docker build paths;
- one reference slice covering system health end to end.

Intentional baseline-only areas:

- the business/domain surface remains thin on purpose;
- local UI primitives are compatibility adapters, not a branded design system;
- the homepage explains the template rather than pretending to be a finished product dashboard;
- product ADRs are examples for derived projects, not evidence that this repo already implements the full product domain.

## Source Of Truth

- Public HTTP contract: [`specs/openapi/platform.openapi.yaml`](https://github.com/Mesteriis/fullstack-template/blob/main/specs/openapi/platform.openapi.yaml)
- Contract governance: [`specs/README.md`](https://github.com/Mesteriis/fullstack-template/blob/main/specs/README.md)
- HTTP parity enforcement: [`scripts/check_http_contract_parity.py`](https://github.com/Mesteriis/fullstack-template/blob/main/scripts/check_http_contract_parity.py)
- Generated frontend API: [`src/frontend/shared/api/generated/platform-api.ts`](https://github.com/Mesteriis/fullstack-template/blob/main/src/frontend/shared/api/generated/platform-api.ts)
- Architecture reading map: [`docs/adr/INDEX.md`](./adr/INDEX)
- Template philosophy: [`docs/template/PHILOSOPHY.md`](./template/PHILOSOPHY)

If implementation and documentation disagree, the disagreement is a defect and
must be fixed. The template is not designed to rely on tribal knowledge.

## Canonical Reference Slice

The current reference slice is `system health`.

It includes:

- backend endpoints under `/api/v1/system/health`, `/readyz`, and `/livez`;
- typed backend contracts for readiness and dependency checks;
- concurrent dependency probing with settings-driven timeout bounds;
- safe externally-visible details backed by structured backend logging for operators;
- frontend entity and feature wiring through the shared API boundary;
- homepage composition that demonstrates the layered frontend shell;
- backend API tests, frontend rendering tests, contract tests, and smoke tests.

Treat it as the sample for building the next bounded context, not as the first
screen of a product dashboard.

## What Derived Projects Must Customize

- application name, environment values, and deployment metadata;
- domain-specific OpenAPI, AsyncAPI, and JSON Schema contracts under `specs/`;
- bounded contexts under `src/backend/apps/`;
- frontend pages, entities, and features built on top of the shared UI/API boundaries;
- observability endpoints, DSNs, and environment-specific telemetry settings;
- product and domain ADRs to match the real project;
- CI secrets, registry destinations, and deployment topology.

## Suggested Reading Order

1. [Getting Started](./getting-started)
2. [Template Philosophy](./template/PHILOSOPHY)
3. [ADR Reading Map](./adr/INDEX)
4. [Frontend UI Layer](./frontend/ui-layer)
