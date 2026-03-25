# ADR-0002: Adopt API-first design and explicit contract versioning

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Context

Система имеет внешние и внутренние интерфейсы: HTTP API, события, схемы данных и generated clients. Если контракты появляются постфактум, начинается drift между реализацией, клиентами и тестами.

## Decision

Принимается API-first подход:

- сначала меняется контракт;
- затем обновляются примеры и версии;
- затем генерируются артефакты;
- затем реализуется код;
- затем обновляются contract tests.

Breaking changes допускаются только через новую версию контракта. Контракты хранятся в `specs/` и считаются source of truth для публичных surface area.

## Consequences

### Positive

- уменьшается contract drift;
- упрощается синхронизация backend и frontend;
- контракт становится reviewable artifact, а не побочным продуктом реализации.

### Negative

- любое API-изменение требует дополнительного шага;
- нужна дисциплина по versioning и примерам.

### Neutral

- не все внутренние вызовы обязаны быть HTTP, но контрактность сохраняется.

## Alternatives considered

- code-first без явного contract governance;
- неверсионированные API;
- версионирование только при больших релизах.

## Follow-up work

- [ ] определить naming conventions для endpoint и event types
- [ ] зафиксировать error envelope
- [ ] описать правила pagination, filtering и sorting
