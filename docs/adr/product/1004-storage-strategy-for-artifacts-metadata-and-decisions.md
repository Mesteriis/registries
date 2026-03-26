# ADR-1004: Separate artifact blob storage from metadata and decision storage

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0010](../architecture/0010-use-taskiq-redis-streams-and-postgresql.md)
- [ADR-0011](../architecture/0011-manage-postgresql-schema-with-alembic.md)
- [ADR-1000](./1000-artifact-immutability-and-promotion-model.md)
- [ADR-1001](./1001-trust-and-verification-policy.md)
- [ADR-1003](./1003-quarantine-and-security-gates.md)

## Context

The platform deals with at least three different classes of data:

1. binary artifacts;
2. metadata and indexes;
3. verdicts, audit records, and pipeline state.

These classes differ in size, access patterns, retention needs, and update
behavior.

## Decision

Data is separated logically by storage role:

- blob or object storage for binary artifacts;
- `PostgreSQL` as the primary relational and transactional storage for metadata, state, policy decisions, and audit;
- a dedicated index or search layer when needed.

Storage design must not try to serve all three data classes through one default
storage engine. Relational schema evolution is managed through versioned
`PostgreSQL` migrations rather than ad-hoc SQL changes in environments.

## Consequences

### Positive

- each data class can live in a storage layer that fits it well;
- system hotspots become easier to scale and optimize;
- transactional storage is less likely to be overloaded with the wrong workload.

### Negative

- the data consistency model becomes more complex;
- references, retention, and cleanup flows must be designed carefully.

### Neutral

- physical storage implementations may differ between dev and production.

## Alternatives considered

- store everything in one SQL database;
- store everything in blob storage;
- choose storage ad hoc as the system grows.

## Follow-up work

- [ ] describe the data model between storage layers
- [ ] define retention and cleanup strategy
- [ ] define the artifact reference model
