# ADR-0014: Enforce backend dependency direction and import boundaries

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0008](./0008-layered-testing-strategy.md)
- [ADR-0013](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-0017](./0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [ADR-0018](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)
- [ADR-0019](./0019-centralize-persistence-behind-repositories-query-services-and-exhaustive-layer-contracts.md)

## Context

Even with a good package layout, architecture blurs quickly when dependency
direction is not enforced. Then:

- `api` starts owning orchestration and direct persistence access;
- `domain` starts importing framework- or ORM-specific dependencies;
- one bounded context imports the internals of another;
- `core` turns into an uncontrolled shared bucket;
- runtime workers bypass the application layer and duplicate business logic.

## Decision

The backend follows a unidirectional dependency model.

At top-level package scope:

- `src/backend` is the service root, not an import namespace;
- `api` may depend on `apps` and `core`;
- `runtime` may depend on `apps` and `core`;
- `apps` may depend on `core`;
- `core` must not depend on `api`, `runtime`, or concrete bounded contexts except in limited bootstrap-level wiring that assembles the application.

Inside a bounded context, the allowed direction is:

```text
api -> application -> domain
infrastructure -> domain
application -> contracts
api -> contracts
infrastructure -> contracts
```

Layer restrictions:

- `domain` does not import `api`, `application`, `infrastructure`, ORM models, transport objects, or external SDKs;
- `application` does not import transport-specific types and does not know framework lifecycle;
- `api` does not hold business rules and does not work directly with persistence models;
- `contracts` stay lightweight typed boundary objects and do not depend on transport or persistence implementation;
- `infrastructure` implements adapters and persistence but does not own domain rules.

Cross-context rules:

- one bounded context must not import another context's internals;
- cross-context integration goes through `contracts`, explicit public facades, or events;
- direct imports of another context's `api`, `application.services`, or `infrastructure` are forbidden by default.

Enforcement model:

- bootstrap modules may have narrow composition-root exceptions;
- import-boundary rules should be strengthened gradually through linter and CI checks;
- the top-level boundary contract should move toward exhaustive enforcement with explicit allowlisted exceptions;
- new exceptions are allowed only as explicit architectural compromises, not as silent practice.

## Consequences

### Positive

- architecture boundaries become enforceable instead of declarative;
- bounded contexts keep ownership of their logic;
- framework leakage into the domain layer becomes less likely;
- runtime workers and APIs use the same application contracts.

### Negative

- quick short-term implementation shortcuts become harder;
- some code must move into contracts or public facades instead of direct imports.

### Neutral

- the concrete enforcement tool may change as long as the dependency model remains directional.

## Alternatives considered

- not enforcing import boundaries and relying only on code review;
- letting bounded contexts import each other's internals freely;
- relying only on naming conventions with no explicit dependency model.

## Follow-up work

- [x] add baseline import-linter configuration to backend tooling
- [ ] expand CI checks to automatically enforce top-level and cross-context boundaries
- [ ] add rules for domain-safe modules inside `core`
