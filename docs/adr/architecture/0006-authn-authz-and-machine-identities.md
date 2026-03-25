# ADR-0006: Use explicit machine identities and policy-based authorization

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Context

Система взаимодействует не только с людьми, но и с automation, внутренними сервисами и внешними агентами. Без явной модели identity и authorization критичные операции быстро начинают защищаться несогласованно.

## Decision

Система различает:

- human identities;
- machine identities;
- internal service identities.

Авторизация строится на policy-based модели, а не на хаотичном наборе role checks. Чувствительные операции должны явно проверять actor type, scope, policy context и auditability.

## Consequences

### Positive

- повышается безопасность и прозрачность операций;
- проще автоматизировать CI/CD и service-to-service flows;
- опасные действия легче ограничивать и аудитить.

### Negative

- возрастает стартовая сложность;
- нужен lifecycle management для credential и token.

### Neutral

- конкретный identity provider может быть выбран позже отдельным ADR.

## Alternatives considered

- shared admin tokens;
- role checks без policy model;
- отсутствие разделения между human и machine actors.

## Follow-up work

- [ ] описать actor model
- [ ] определить matrix чувствительных операций
- [ ] зафиксировать credential lifecycle
