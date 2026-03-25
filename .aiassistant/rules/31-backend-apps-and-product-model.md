---
apply: by file patterns
patterns: src/backend/apps/**/*, src/backend/tests/apps/**/*, tests/contract/**/*
---

# Backend Apps And Product Model

Path scope:

- `src/backend/apps/**`
- `src/backend/tests/apps/**`
- `tests/contract/**`

Применяй это правило при изменении bounded contexts, application/domain/contracts/infrastructure слоёв и app-level тестов backend.

Сначала прочитай:

- [ADR-0002](../../docs/adr/architecture/0002-api-first-and-contract-versioning.md)
- [ADR-0008](../../docs/adr/architecture/0008-layered-testing-strategy.md)
- [ADR-0013](../../docs/adr/architecture/0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](../../docs/adr/architecture/0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0017](../../docs/adr/architecture/0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [ADR-0018](../../docs/adr/architecture/0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)
- [ADR-0019](../../docs/adr/architecture/0019-centralize-persistence-behind-repositories-query-services-and-exhaustive-layer-contracts.md)
- [ADR-0020](../../docs/adr/architecture/0020-centralize-platform-error-registry-and-http-error-projection.md)
- [ADR-0021](../../docs/adr/architecture/0021-centralize-backend-observability-bootstrap-and-structured-telemetry.md)

Если изменение затрагивает trust, verification, quarantine, promotion, metadata, audit или storage semantics, дополнительно прочитай:

- [ADR-1000](../../docs/adr/product/1000-artifact-immutability-and-promotion-model.md)
- [ADR-1001](../../docs/adr/product/1001-trust-and-verification-policy.md)
- [ADR-1002](../../docs/adr/product/1002-sbom-provenance-and-signatures.md)
- [ADR-1003](../../docs/adr/product/1003-quarantine-and-security-gates.md)
- [ADR-1004](../../docs/adr/product/1004-storage-strategy-for-artifacts-metadata-and-decisions.md)

Правила:

- внутри bounded context соблюдай слои `api/application/contracts/domain/infrastructure`;
- cross-context imports идут только через `contracts`, public facades или события;
- app-owned contracts хранятся в `apps/<context>/contracts`, а не накапливаются в top-level `api/`;
- каждый bounded context владеет своими `repositories`, `query services` и `read models`;
- app-level `api/errors.py` использует centralized platform errors и `ApiErrorFactory`, а не invent-your-own error payloads;
- app-level code uses `core.observability.get_logger` when structured logs are needed and never falls back to `print` or direct stdlib loggers;
- все reads идут через query services, все writes идут через repositories;
- routes, workers и public service boundaries не должны принимать raw `AsyncSession` как primary dependency;
- API handlers должны зависеть от уже собранных service/query gateway dependencies, а не конструировать persistence graph прямо в endpoint;
- services, repositories и query adapters должны общаться typed structures, а не raw `dict`;
- доступ к БД идёт только через repositories/query services под управлением `Unit of Work`;
- backend tests должны повторять структуру проекта, использовать pytest functions и держать fixtures только в `conftest.py`;
- integration tests проверяют полный flow и не мокируют internal service/repository path;
- продуктовые правила не должны silently расходиться с product ADR;
- если меняется business semantics, сначала обнови контракт или ADR, затем реализацию и тесты.
