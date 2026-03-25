---
apply: by file patterns
patterns: src/backend/api/**/*, src/backend/core/**/*, src/backend/runtime/**/*, src/backend/main.py, src/backend/pyproject.toml, src/backend/tests/architecture/**/*, src/backend/tests/core/**/*, src/backend/tests/runtime/**/*, src/backend/tests/factories/**/*, src/backend/tests/fixtures/**/*, src/backend/tests/conftest.py, migrations/**/*, alembic.ini, docker/Dockerfile, docker/entrypoints/backend.sh, docker/runs/backend.sh, scripts/check_backend_architecture.py, scripts/check_backend_observability.py, scripts/run_backend_bandit.py, scripts/run_backend_deptry.py, scripts/run_backend_eradicate.py, scripts/run_backend_import_boundaries.py, scripts/run_backend_lint.py, scripts/run_backend_lint_fix.py, scripts/run_backend_pip_audit.sh, scripts/run_backend_pyupgrade.py, scripts/run_backend_sync.py, scripts/run_backend_tests.py, scripts/run_backend_tryceratops.py, scripts/run_backend_types.py, scripts/run_backend_xenon.py
---

# Backend Platform

Path scope:

- `src/backend/api/**`
- `src/backend/core/**`
- `src/backend/runtime/**`
- `src/backend/main.py`
- `src/backend/pyproject.toml`
- `src/backend/tests/architecture/**`
- `src/backend/tests/core/**`
- `src/backend/tests/runtime/**`
- `src/backend/tests/factories/**`
- `src/backend/tests/fixtures/**`
- `src/backend/tests/conftest.py`
- `migrations/**`
- `alembic.ini`
- `docker/Dockerfile`
- `docker/entrypoints/backend.sh`
- `docker/runs/backend.sh`
- `scripts/check_backend_architecture.py`
- `scripts/check_backend_observability.py`
- `scripts/run_backend_bandit.py`
- `scripts/run_backend_deptry.py`
- `scripts/run_backend_eradicate.py`
- `scripts/run_backend_import_boundaries.py`
- `scripts/run_backend_lint.py`
- `scripts/run_backend_lint_fix.py`
- `scripts/run_backend_pip_audit.sh`
- `scripts/run_backend_pyupgrade.py`
- `scripts/run_backend_sync.py`
- `scripts/run_backend_tests.py`
- `scripts/run_backend_tryceratops.py`
- `scripts/run_backend_types.py`
- `scripts/run_backend_xenon.py`

Применяй это правило при изменении backend platform, runtime, migrations и backend container wiring.

Обязательные ADR:

- [ADR-0005](../../docs/adr/architecture/0005-background-jobs-and-workflow-orchestration.md)
- [ADR-0008](../../docs/adr/architecture/0008-layered-testing-strategy.md)
- [ADR-0009](../../docs/adr/architecture/0009-deployment-topology-and-runtime-model.md)
- [ADR-0010](../../docs/adr/architecture/0010-use-taskiq-redis-streams-and-postgresql.md)
- [ADR-0011](../../docs/adr/architecture/0011-manage-postgresql-schema-with-alembic.md)
- [ADR-0012](../../docs/adr/architecture/0012-define-repository-layout-and-file-placement-rules.md)
- [ADR-0013](../../docs/adr/architecture/0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](../../docs/adr/architecture/0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0017](../../docs/adr/architecture/0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [ADR-0018](../../docs/adr/architecture/0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)
- [ADR-0019](../../docs/adr/architecture/0019-centralize-persistence-behind-repositories-query-services-and-exhaustive-layer-contracts.md)
- [ADR-0020](../../docs/adr/architecture/0020-centralize-platform-error-registry-and-http-error-projection.md)
- [ADR-0021](../../docs/adr/architecture/0021-centralize-backend-observability-bootstrap-and-structured-telemetry.md)
- [ADR-0022](../../docs/adr/architecture/0022-group-backend-settings-into-nested-platform-models.md)

Правила:

- backend service root остаётся плоским: `src/backend/{api,apps,core,runtime,main.py,tests}`;
- `core` не зависит от `api`, `runtime` и внутренних bounded contexts кроме bootstrap wiring;
- runtime и workers не обходят application/contracts слои без явной причины;
- миграции хранятся в `migrations/` и управляются только через `Alembic`;
- миграции не должны запускаться как side effect import-time bootstrap;
- для фоновых задач сохраняется стек `Taskiq + Redis Streams + PostgreSQL`.
- persistence и транзакции принадлежат `repository` и `Unit of Work`, а не endpoint или service helper-модулям;
- top-level dependency contract между `api`, `runtime`, `apps` и `core` должен оставаться exhaustive, а исключения фиксируются явно;
- endpoints остаются `async` function handlers, остальные активные backend components проектируются `class-first`;
- endpoint handler получает уже собранный service/gateway через `api/deps.py` и не собирает `UoW`, repositories или DB clients внутри себя;
- canonical error codes, message keys и HTTP error payloads живут централизованно в `core/errors` и `core/http/errors`;
- ad-hoc `HTTPException(detail={...})` без `ApiErrorFactory` считается нарушением platform baseline;
- observability bootstrap централизован в `core/observability` и вызывается из composition root, а не из случайных runtime-модулей;
- backend runtime не использует `print`, `pprint`, direct `logging.getLogger` или direct `structlog` setup вне `core/observability`;
- tracing instrumentors, metrics exposure и `sentry_sdk.init` не размазываются по сервисам и endpoints, а остаются в platform-owned observability modules;
- request context обязан нести и `request_id`, и `correlation_id`; если клиент не прислал `correlation_id`, platform middleware выводит его из `request_id`, а оба значения попадают в headers, logs и error payloads;
- platform settings группируются в `settings.app`, `settings.api`, `settings.db`, `settings.broker` и `settings.observability`, а новые platform fields не добавляются обратно в flat root;
- env-backed config для backend использует nested keys с `REGISTRIES_*__*`, а не бесконтрольное разрастание flat variable names;
- слои не должны общаться сырыми `dict`, кроме низкоуровневой boundary-serialization логики.
