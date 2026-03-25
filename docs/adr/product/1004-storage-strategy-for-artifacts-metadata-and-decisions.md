# ADR-1004: Separate artifact blob storage from metadata and decision storage

- Status: Accepted
- Date: 2026-03-25
- Deciders: core engineering team
- Supersedes:
- Superseded by:

## Context

Платформа работает как минимум с тремя разными классами данных:

1. бинарные артефакты;
2. metadata и индексы;
3. verdicts, audit records и pipeline state.

Эти данные отличаются по объёму, access patterns, retention и характеру обновления.

## Decision

Данные разделяются логически по классам хранения:

- blob or object storage для бинарных артефактов;
- `PostgreSQL` как primary relational and transactional storage для metadata, state, policy decisions и audit;
- отдельный index or search layer при необходимости.

Storage design не должен пытаться обслужить все три класса данных через одно универсальное хранилище по умолчанию.

## Consequences

### Positive

- каждый класс данных хранится в подходящем storage;
- проще масштабировать и оптимизировать system hotspots;
- ниже риск перегрузить transactional storage несвойственной нагрузкой.

### Negative

- усложняется data consistency model;
- нужно проектировать references, retention и cleanup flows.

### Neutral

- физическая реализация может отличаться между dev и production.

## Alternatives considered

- хранить всё в одной SQL database;
- хранить всё в blob store;
- строить storage strategy ad hoc по мере роста.

## Follow-up work

- [ ] описать data model между storage слоями
- [ ] определить retention и cleanup strategy
- [ ] определить artifact reference model
