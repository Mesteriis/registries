# ADR-0020: Centralize platform error registry and HTTP error projection

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0002](./0002-api-first-and-contract-versioning.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0014](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)
- [ADR-0019](./0019-centralize-persistence-behind-repositories-query-services-and-exhaustive-layer-contracts.md)
- [ADR-0021](./0021-centralize-backend-observability-bootstrap-and-structured-telemetry.md)

## Context

Без централизованного error model backend обычно быстро деградирует в смесь ad-hoc `HTTPException(detail={...})`, локальных string-кодов и разрозненных error-payload схем по разным endpoints. Это создаёт несколько системных проблем:

- error codes и message keys начинают дублироваться и расходиться между bounded contexts;
- transport error payload становится нестабильным и непредсказуемым;
- API documentation теряет единый typed error contract;
- domain/application исключения протекают в transport layer без единой policy;
- новые contexts начинают invent-your-own error format вместо reuse общей платформенной модели.

Для maximum template нужен единый platform-level error registry, который задаёт taxonomy, canonical codes и стандартную HTTP projection model.

## Decision

Backend принимает centralized error model как обязательный platform baseline.

Правила platform registry:

- canonical error codes, message keys, categories, severities и HTTP statuses живут централизованно в `core/errors`;
- дублирующиеся error codes и message keys запрещены registry-level validation;
- application и domain layers выбрасывают typed platform errors, а не ad-hoc `HTTPException` и не free-form string errors;
- generic backend failures мапятся в canonical `internal_error`, а не в произвольные 500 payloads.

Правила HTTP projection:

- canonical HTTP error payload задаётся централизованно в `core/http/errors.py`;
- app-level `api/errors.py` modules используют `ApiErrorFactory` и registry-backed errors, а не собирают response payload вручную;
- `HTTPException(detail={...})` с ad-hoc словарём считается нарушением baseline, если payload не создан через централизованный error factory;
- request validation errors и unhandled exceptions проецируются в typed `ApiError` через единые exception handlers.

Правила context ownership:

- каждый bounded context может иметь собственный `api/errors.py` для response docs и переводов domain/platform errors в transport boundary;
- но source of truth для кодов, категорий и message keys остаётся в `core/errors`;
- per-context API errors не создают собственные параллельные registry и не дублируют platform error catalog.

## Consequences

### Positive

- backend получает единый typed error payload для OpenAPI, runtime responses и exception handling;
- коды и категории ошибок становятся централизованными и проверяемыми;
- bounded contexts могут добавлять transport-level helpers, не теряя platform consistency;
- generic и validation failures перестают возвращать произвольные error payloads.

### Negative

- даже для простых endpoints приходится использовать platform error classes и shared factory вместо прямого `HTTPException`;
- добавление нового canonical error требует обновления registry, а не только одного route handler.

### Neutral

- конкретный набор canonical errors может расширяться, если сохраняются centralized registry и единая HTTP projection model.

## Alternatives considered

- разрешить каждому context собирать собственный `HTTPException(detail={...})`;
- держать error payload как свободный dict без typed transport contract;
- хранить error definitions прямо в `api/errors.py` каждого bounded context;
- мапить generic exceptions напрямую в plain text или framework-default payload.

## Follow-up work

- [ ] добавить static check против ad-hoc `HTTPException(detail={...})` вне централизованного error factory
- [ ] добавить more domain-specific registry entries по мере появления bounded contexts
- [ ] расширить app-level `api/errors.py` helpers в новых contexts по тому же шаблону
