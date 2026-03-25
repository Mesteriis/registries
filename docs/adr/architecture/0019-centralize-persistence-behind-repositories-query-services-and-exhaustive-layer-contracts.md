# ADR-0019: Centralize persistence behind repositories, query services and exhaustive layer contracts

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0017](./0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)

## Context

Опыт `iris` показал, что одна только схема слоёв `api/application/domain/infrastructure` недостаточна. Если не определить явные read/write boundaries и способ enforcement, система быстро деградирует в следующие anti-patterns:

- routes, workers и services принимают `AsyncSession` напрямую;
- reads идут через raw ORM/session helpers вместо отдельной read boundary;
- writes выполняются из service helpers, tasks и endpoint handlers в обход repositories;
- repositories начинают владеть `commit()` и `rollback()` вместо того, чтобы быть persistence adapters;
- read path возвращает ORM entities или ad-hoc `dict`, а не typed immutable read models;
- import boundaries между `api`, `runtime`, `apps` и `core` остаются декларацией без exhaustive static enforcement.

Для maximum baseline template нужно зафиксировать такую же persistence governance model, как в `iris`: явный repository/query split, единый UoW authority и исчерпывающий dependency contract с явными исключениями.

## Decision

Backend принимает repository/query/UoW model как обязательный execution baseline.

Read/write boundaries:

- все write operations идут только через repositories;
- все read operations идут только через query services;
- query services являются default read boundary для list/detail/dashboard/query flows;
- query services возвращают typed immutable read models или другие typed read contracts;
- repositories являются единственной write boundary к `PostgreSQL` на active backend path.

Transaction ownership:

- `Unit of Work` является единственной authority для `commit`, `rollback`, transaction boundary и after-commit hooks;
- repositories не должны вызывать `commit()` или `rollback()`;
- query services никогда не вызывают `commit()`;
- routes, workers, tasks и application services могут инициировать `uow.commit()` только как owner use-case boundary, но не должны обходить repository/query split;
- side effects, зависящие от успешной транзакции, должны ставиться на post-commit path через UoW-owned mechanism.

Session ownership:

- routes, workers и public service boundaries не должны принимать raw `AsyncSession` как primary dependency;
- routes и public endpoints получают уже собранные service/query gateway dependencies, а не собирают persistence graph внутри handler;
- direct session handling в active runtime path запрещён вне UoW, repositories, query services и низкоуровневых persistence primitives;
- прямой SQL или raw ORM access вне repository/query boundary считается архитектурным нарушением по умолчанию.

Bounded context ownership:

- каждый bounded context владеет своими router/contracts/services/repositories/query services/read models;
- modules не должны протаскивать persistence models или raw session objects через boundary;
- read models считаются default result type для read path;
- presenters/response mappers преобразуют typed read models или service results в transport schemas, а не строят response из ORM entities или ad-hoc dict payloads.

Dependency enforcement:

- top-level contract между `api`, `runtime`, `apps` и `core` должен быть exhaustive;
- любые допустимые исключения фиксируются явным allowlist в static checks или import-linter configuration;
- неявные “временные” исключения без whitelist и архитектурного решения запрещены.

## Consequences

### Positive

- read и write paths становятся предсказуемыми и одинаковыми между API, workers и tasks;
- transaction ownership централизуется и перестаёт протекать в repositories или route handlers;
- query services и immutable read models упрощают стабилизацию read contracts;
- import boundary drift становится заметным и проверяемым через exhaustive static rules;
- bounded contexts получают полное ownership над своими persistence contracts.

### Negative

- кодовая база требует больше формальных abstractions даже для простых сценариев;
- для новых flow приходится сразу выбирать repository, query service и UoW boundary вместо прямого session shortcut.

### Neutral

- конкретные имена файлов (`query_services.py`, `repositories.py`, `read_models.py`) могут отличаться, если сохраняются сами роли и ownership rules.

## Alternatives considered

- разрешить direct `AsyncSession` injection в routes и services;
- считать repository pattern optional и использовать его только для части write flows;
- читать данные напрямую через ORM/session helpers без query services;
- держать import boundary exceptions неявными и непроверяемыми.

## Follow-up work

- [ ] усилить backend static checks против direct session access вне repository/query/UoW layers
- [ ] расширить import boundary enforcement до exhaustive allowlist model
- [ ] добавить template scaffold для query services и immutable read models внутри bounded contexts
