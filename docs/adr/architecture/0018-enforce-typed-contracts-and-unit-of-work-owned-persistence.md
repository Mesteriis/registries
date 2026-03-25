# ADR-0018: Enforce typed contracts and Unit of Work owned persistence

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0002](./0002-api-first-and-contract-versioning.md)
- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0010](./0010-use-taskiq-redis-streams-and-postgresql.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0017](./0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [ADR-0019](./0019-centralize-persistence-behind-repositories-query-services-and-exhaustive-layer-contracts.md)

## Context

Даже при хорошем package layout backend быстро деградирует, если слои начинают общаться сырыми `dict`, endpoints владеют транзакциями, а business flow обходит repositories или работает напрямую с `AsyncSession`. Это порождает несколько системных проблем:

- границы между transport, application и persistence становятся неявными;
- typed contracts заменяются ad-hoc словарями, которые трудно валидировать и безопасно менять;
- services и workers начинают владеть low-level transaction lifecycle без общей policy;
- логика чтения и записи к базе расползается по endpoints, tasks и helper-модулям;
- асинхронные runtime paths начинают смешиваться с sync-style procedural code.

Для backend template нужен единый execution model, в котором ownership typed contracts, repositories и transactions задан явно.

## Decision

Backend использует typed, repository-driven и Unit-of-Work-owned execution model.

Правила boundary contracts:

- слои не общаются через сырые `dict`;
- между слоями допустимы только `dataclass` или Pydantic-based structures;
- transport payloads, application commands/results, repository inputs/outputs и query/read models должны быть typed;
- raw `dict` допустимы только на внешней границе парсинга/сериализации или внутри низкоуровневой инфраструктуры, но не как межслойовой contract.

Правила runtime shape:

- endpoints остаются `async-first` function handlers;
- application services, repositories, query services, clients и другие non-endpoint components проектируются `class-first`;
- endpoint отвечает за transport wiring и вызов service boundary, но не владеет transaction orchestration;
- endpoint получает уже собранный service/gateway через dependency provider и не конструирует repositories, UoW или low-level clients внутри handler;
- active backend path должен оставаться предсказуемым и typed на всём протяжении запроса.

Правила persistence:

- общение с базой идёт только через repositories или query services;
- read path по умолчанию идёт через query services и typed immutable read models;
- endpoints, services и workers не обращаются к `AsyncSession` или SQL напрямую в обход repository boundary;
- транзакциями управляет `Unit of Work`;
- `Unit of Work` является единственной точкой владения commit/rollback policy;
- side effects, зависящие от успешного commit, должны подчиняться transaction boundary и по возможности выполняться post-commit.

Роли слоёв:

- endpoint: принимает request, валидирует transport boundary, вызывает service, возвращает typed response;
- service: оркестрирует use case, использует repositories и domain policies, но не знает о transport details;
- repository: единственная write/read boundary к БД на write path;
- query service: typed read boundary для read-heavy flows, если repository abstraction становится избыточной;
- Unit of Work: владеет session lifecycle и transaction boundary.

## Consequences

### Positive

- межслойовые контракты становятся проверяемыми и безопаснее переживают refactor;
- transaction ownership централизуется и перестаёт быть случайным побочным эффектом endpoint или worker code;
- persistence code концентрируется в repositories и query services вместо расползания по runtime paths;
- async API layer и class-based services получают чёткое разделение ролей.

### Negative

- для простых сценариев приходится создавать typed structures и repository/UoW wiring сразу, без shortcuts;
- write path становится строже и не допускает быстрых direct-session hacks.

### Neutral

- конкретная реализация UoW и repository internals может меняться, если сохраняются typed boundaries и ownership rules.

## Alternatives considered

- разрешить слоям обмениваться сырыми `dict[str, object]`;
- допустить прямой доступ к `AsyncSession` из endpoints и services;
- строить backend в procedural style без class-based services и repositories;
- считать repository pattern optional и использовать его только выборочно.

## Follow-up work

- [ ] добавить static checks против raw dict layer contracts на backend path
- [ ] добавить template scaffold для `Unit of Work`, repositories и typed command/result contracts
- [ ] усилить backend architecture validation правилами против direct session access вне repository/UoW layers
