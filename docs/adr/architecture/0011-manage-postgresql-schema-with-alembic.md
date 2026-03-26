# ADR-0011: Manage PostgreSQL schema evolution with Alembic migrations

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0009](./0009-deployment-topology-and-runtime-model.md)
- [ADR-0010](./0010-use-taskiq-redis-streams-and-postgresql.md)
- [ADR-0012](./0012-define-repository-layout-and-file-placement-rules.md)
- [ADR-1004](../product/1004-storage-strategy-for-artifacts-metadata-and-decisions.md)

## Context

`PostgreSQL` is already chosen as the primary relational storage for metadata,
state, policy decisions, and audit. Without one schema-evolution mechanism, the
team quickly ends up with environment drift, manual SQL changes, and hidden
dependencies between code and database shape.

This ADR specifies how relational schema evolves for the storage chosen in
ADR-0010 and how that process fits the runtime and deployment model from
ADR-0009.

## Decision

Schema evolution for `PostgreSQL` is managed only through `Alembic`.

Rules:

- migrations are stored in the repository and version-controlled;
- every relational schema change is delivered in the same pull request as the application code that depends on it;
- Alembic autogeneration is allowed only as a starting point, and the final migration script must still be read and reviewed manually;
- destructive changes must not be mixed with the expand phase when rollout compatibility between app versions is needed;
- manual ad-hoc SQL changes in environments are not an accepted schema-management mechanism.

Runtime and deployment rules:

- migrations do not run as a side effect of FastAPI app bootstrap, import-time initialization, or request handling;
- migrations run either as a separate administrative, CI/CD, or deployment step, or as an explicit pre-start step in the backend container entrypoint before the API starts;
- successful migration execution is an explicit rollout step for changes that affect the relational model;
- rollback strategy must be considered when a migration is created, not after the fact.

Repository layout rule:

- the Alembic configuration and `migrations/` directory live at repository root as a shared infrastructure artifact for the primary relational database.

## Consequences

### Positive

- `PostgreSQL` schema evolution becomes predictable and reproducible;
- drift between local, staging, and production environments is reduced;
- the delivery pipeline gets an explicit schema-change step;
- the link between data model and code becomes reviewable.

### Negative

- migration discipline must be maintained;
- poorly designed migrations can make rollout and rollback harder;
- one more operational step appears in the delivery pipeline.

### Neutral

- `Alembic` does not define the domain storage model itself; it defines how that model evolves.

## Alternatives considered

- manual SQL scripts with no shared migration framework;
- automatic schema changes on application startup;
- using ORM auto-create or auto-update instead of versioned migrations;
- postponing schema governance until the database becomes more complex.

## Follow-up work

- [x] add `alembic.ini` and `migrations/` at repository root
- [ ] define naming conventions for revision and branch labels
- [ ] document an expand-contract guideline for breaking schema changes
