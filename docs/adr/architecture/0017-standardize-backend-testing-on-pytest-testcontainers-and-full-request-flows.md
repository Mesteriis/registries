# ADR-0017: Standardize backend testing on pytest, Testcontainers and full request flows

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0010](./0010-use-taskiq-redis-streams-and-postgresql.md)
- [ADR-0011](./0011-manage-postgresql-schema-with-alembic.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)

## Context

Общая layered testing strategy уже зафиксирована, но для backend по-прежнему не определены жёсткие правила test harness, допустимые doubles и форма тестовых данных. Без этого команда быстро скатывается в несколько нежелательных паттернов:

- SQLite используется как дешёвая замена PostgreSQL и скрывает реальные ограничения production storage;
- Redis либо не тестируется вовсе, либо заменяется in-memory подделками;
- internal services и repositories мокируются до такой степени, что тест перестаёт проверять реальный execution path;
- тестовые payloads собираются сырыми `dict`, что размывает contract boundaries;
- фикстуры и helpers размазываются по случайным файлам, а структура тестов перестаёт повторять структуру проекта.

Для максимально opinionated template нужна единая backend testing policy, которая проверяет реальные runtime boundaries, а не только отдельные куски логики.

## Decision

Backend tests стандартизируются следующим образом.

Тестовый runtime:

- backend использует `pytest` как единственный test runner;
- для integration и persistence tests поднимаются только реальные `PostgreSQL` и `Redis` через `Testcontainers`;
- `SQLite` запрещён как test database и не считается допустимой заменой `PostgreSQL`;
- миграции и persistence behavior проверяются против той же реляционной модели, что и production path.

Допустимый execution path:

- backend integration/API tests по умолчанию проверяют полный путь `request -> endpoint -> service -> repo -> db -> repo -> service -> endpoint -> response`;
- internal services, repositories, UoW и persistence adapters не мокируются в обычных backend tests;
- если тестируется клиент внешнего API, подмена делается не через мок методов, а через поднятие fake external service с предсказуемыми ответами;
- мокать допустимо только внешние API boundaries и внешние side effects, которые не принадлежат самому сервису.

Тестовые данные и factories:

- тестовые данные создаются через `faker` и `polyfactory`;
- сырые `dict` как основной способ построения test input/output запрещены;
- test payloads и expected values должны собираться через typed models, factories, dataclasses или Pydantic structures;
- fixtures и factories должны давать repeatable, typed test arrangements.

Организация тестов:

- структура тестов повторяет структуру проекта;
- backend tests размещаются под `src/backend/tests/` и отражают `apps/`, `core/` и `runtime/`;
- fixtures объявляются только в `conftest.py` на соответствующем уровне;
- тесты пишутся только как function-based pytest tests;
- class-based test containers, `unittest.TestCase` и grouping через тестовые классы запрещены.

## Consequences

### Positive

- integration tests начинают проверять реальный backend flow, а не заранее замоканную схему вызовов;
- persistence и transaction behavior валидируются на production-like `PostgreSQL` и `Redis`;
- тестовые данные получают typed boundaries и лучше переживают refactor;
- структура тестов остаётся предсказуемой и совпадает со структурой сервиса.

### Negative

- integration tests становятся тяжелее и медленнее, чем при SQLite или in-memory doubles;
- fake external services требуют больше обвязки, чем прямой monkeypatch.

### Neutral

- unit tests для pure domain logic остаются допустимыми, но даже они должны придерживаться typed factories и function-based pytest style.

## Alternatives considered

- использовать `SQLite` для дешёвых repository tests;
- мокировать services и repositories в большинстве endpoint tests;
- использовать raw `dict` и ad-hoc payload builders как основную форму test data;
- разрешить test classes и произвольное размещение fixtures рядом с отдельными test files.

## Follow-up work

- [ ] добавить backend test tooling для `Testcontainers` с `PostgreSQL` и `Redis`
- [ ] ввести static checks против `SQLite` и class-based pytest tests
- [ ] добавить factories на `faker` и `polyfactory` в template baseline
