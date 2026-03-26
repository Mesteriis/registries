# Architecture ADR

This section contains architecture decisions that define the shape of the
system without depending on a specific product name.

Mandatory entrypoint before reading individual ADRs:
[ADR Reading Map](/adr/INDEX).

Use this section for decisions about:

- repository structure and bounded contexts;
- contracts and integrations;
- runtime topology;
- testing strategy;
- security, identity, policy, and observability as platform practices.

Current accepted ADRs:

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
- [0011-manage-postgresql-schema-with-alembic.md](./0011-manage-postgresql-schema-with-alembic.md)
- [0012-define-repository-layout-and-file-placement-rules.md](./0012-define-repository-layout-and-file-placement-rules.md)
- [0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md](./0013-adopt-a-flat-backend-service-root-and-bounded-context-layout.md)
- [0014-enforce-backend-dependency-direction-and-import-boundaries.md](./0014-enforce-backend-dependency-direction-and-import-boundaries.md)
- [0015-enforce-template-quality-gates-and-governance-baseline.md](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [0016-support-github-and-gitea-ci-for-template-repositories.md](./0016-support-github-and-gitea-ci-for-template-repositories.md)
- [0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md](./0017-standardize-backend-testing-on-pytest-testcontainers-and-full-request-flows.md)
- [0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md](./0018-enforce-typed-contracts-and-unit-of-work-owned-persistence.md)
- [0019-centralize-persistence-behind-repositories-query-services-and-exhaustive-layer-contracts.md](./0019-centralize-persistence-behind-repositories-query-services-and-exhaustive-layer-contracts.md)
- [0020-centralize-platform-error-registry-and-http-error-projection.md](./0020-centralize-platform-error-registry-and-http-error-projection.md)
- [0021-centralize-backend-observability-bootstrap-and-structured-telemetry.md](./0021-centralize-backend-observability-bootstrap-and-structured-telemetry.md)
- [0022-group-backend-settings-into-nested-platform-models.md](./0022-group-backend-settings-into-nested-platform-models.md)
- [0023-layer-the-frontend-into-app-pages-features-entities-and-shared.md](./0023-layer-the-frontend-into-app-pages-features-entities-and-shared.md)
- [0024-introduce-a-ui-adapter-layer-ready-for-external-kits.md](./0024-introduce-a-ui-adapter-layer-ready-for-external-kits.md)
- [0025-enforce-frontend-import-boundaries-and-architecture-validation.md](./0025-enforce-frontend-import-boundaries-and-architecture-validation.md)
- [0026-adopt-a-lightweight-semantic-design-foundation-for-frontend-primitives.md](./0026-adopt-a-lightweight-semantic-design-foundation-for-frontend-primitives.md)
- [0027-enforce-machine-validated-http-contract-parity-across-spec-backend-and-frontend.md](./0027-enforce-machine-validated-http-contract-parity-across-spec-backend-and-frontend.md)
- [0028-codify-backend-runtime-lifecycle-resource-ownership-and-health-slice-contract.md](./0028-codify-backend-runtime-lifecycle-resource-ownership-and-health-slice-contract.md)
