# ADR-0027: Enforce machine-validated HTTP contract parity across spec, backend and frontend

- Status: Accepted
- Date: 2026-03-26
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0002](./0002-api-first-and-contract-versioning.md)
- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)
- [ADR-0023](./0023-layer-the-frontend-into-app-pages-features-entities-and-shared.md)

## Context

API-first сам по себе недостаточен, если backend implementation, frontend client
и typed frontend models могут молча drift-ить от `specs/`.

Для strict template это особенно опасно:

- frontend начинает опираться на путь или shape, которого уже нет на backend;
- backend response model меняется, а frontend client/types остаются старыми;
- OpenAPI остаётся декларацией намерения, но не проверяемым source of truth;
- drift обнаруживается слишком поздно, уже в runtime или через ручную проверку.

Требование “100% соответствия” нельзя честно обеспечить generic lint для любого
произвольного ручного кода. Но template может и должен enforce-ить максимально
жёсткую parity policy для своих template-owned HTTP surfaces, если expected
surface автоматически выводится из canonical OpenAPI spec.

## Decision

Принимается machine-validated HTTP contract parity policy:

- `specs/` остаётся source of truth для публичного HTTP contract;
- expected parity map выводится автоматически из `specs/openapi/platform.openapi.yaml`,
  а не хранится как отдельный ручной manifest;
- template-owned backend routes и response contracts должны быть явно привязаны к
  canonical spec path и shape;
- template-owned frontend client paths и typed models должны быть явно привязаны
  к тому же canonical contract;
- для template-owned frontend HTTP slices preferred baseline — generated client/types
  from OpenAPI plus thin entity-layer wrappers;
- parity должна проверяться автоматикой на уровне repository checks и local hooks,
  а не только unit/integration tests;
- для каждого template-owned HTTP reference slice должен существовать explicit
  parity check, который валит репозиторий при drift.

В текущем baseline это применяется к canonical `system health` slice:

- OpenAPI contract в `specs/openapi/platform.openapi.yaml`;
- backend runtime OpenAPI from `FastAPI.app.openapi()` and contracts under `src/backend/apps/system/`;
- generated frontend API under `src/frontend/shared/api/generated/`;
- thin entity-layer wrappers under `src/frontend/entities/system/`;
- root-level contract tests in `tests/contract/`.

## Consequences

### Positive

- drift между spec, backend и frontend ловится до runtime;
- `specs/` перестаёт быть purely aspirational document;
- parity policy не требует отдельного ручного списка expected paths и schema names;
- manual clients остаются допустимыми только при machine-enforced parity;
- template становится safer baseline для derived projects.

### Negative

- generic “prove 100% semantic equivalence for all code” по-прежнему невозможен;
- новые HTTP slices должны получать такую же parity automation, иначе policy будет неполной.

### Neutral

- generated clients считаются preferred baseline, но не отменяют requirement на
  source-of-truth spec, thin wrappers и parity validation;
- contract tests и lint-like parity checks дополняют друг друга, а не заменяют.

## Alternatives considered

- полагаться только на unit/integration/e2e tests;
- доверять code review и manual discipline без machine enforcement;
- делать generic AST-level prover для любого backend/frontend contract surface.

## Follow-up work

- [ ] расширять spec-derived parity coverage при появлении новых template-owned HTTP slices
- [ ] определить, какие derived projects остаются на thin wrappers over generated clients, а где нужен полноценный generated SDK layer
