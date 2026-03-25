# ADR-0003: Use event-driven integration for internal workflows

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Context

Внутренние процессы платформы неоднородны по latency и часто естественно асинхронны. Синхронная оркестрация всех шагов через один request lifecycle усиливает связанность и делает систему менее отказоустойчивой.

## Decision

Для внутренних workflow используется event-driven модель.

Компоненты:

- публикуют доменные события;
- подписываются на релевантные события;
- обрабатывают их асинхронно и идемпотентно;
- сохраняют correlation и causation identifiers.

Синхронные команды допустимы только для коротких операций, где нужна немедленная обратная связь.

## Consequences

### Positive

- тяжёлые процессы лучше масштабируются;
- проще расширять pipeline новыми стадиями;
- снижается связанность между компонентами.

### Negative

- отладка end-to-end становится сложнее;
- нужны idempotency, replay, tracing и schema governance;
- появляется eventual consistency.

### Neutral

- event-driven модель не запрещает точечные synchronous interactions.

## Alternatives considered

- полностью синхронный orchestration layer;
- cron-driven batch processing;
- tight coupling через direct service calls.

## Follow-up work

- [ ] выбрать event bus
- [ ] определить стандартный event envelope
- [ ] зафиксировать correlation_id и causation_id
