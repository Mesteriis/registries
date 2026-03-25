# Architecture ADR

Этот раздел содержит архитектурные решения, которые задают форму системы, но не зависят от названия продукта.

Используем этот раздел для решений про:

- структуру репозитория и bounded contexts;
- контракты и интеграции;
- runtime topology;
- тестовую стратегию;
- безопасность, identity, policy и observability как платформенные практики.

Текущий набор accepted ADR:

- [0000-record-architecture-decisions.md](./0000-record-architecture-decisions.md)
- [0001-monorepo-and-bounded-contexts.md](./0001-monorepo-and-bounded-contexts.md)
- [0002-api-first-and-contract-versioning.md](./0002-api-first-and-contract-versioning.md)
- [0003-event-driven-internal-integration.md](./0003-event-driven-internal-integration.md)
- [0004-observability-and-audit-trail.md](./0004-observability-and-audit-trail.md)
- [0005-background-jobs-and-workflow-orchestration.md](./0005-background-jobs-and-workflow-orchestration.md)
- [0006-authn-authz-and-machine-identities.md](./0006-authn-authz-and-machine-identities.md)
- [0007-configuration-and-policy-as-code.md](./0007-configuration-and-policy-as-code.md)
- [0008-layered-testing-strategy.md](./0008-layered-testing-strategy.md)
- [0009-deployment-topology-and-runtime-model.md](./0009-deployment-topology-and-runtime-model.md)
- [0010-use-taskiq-redis-streams-and-postgresql.md](./0010-use-taskiq-redis-streams-and-postgresql.md)
