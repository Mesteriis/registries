# ADR-1000: Treat stored artifacts as immutable and promote by stage

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-1001](./1001-trust-and-verification-policy.md)
- [ADR-1003](./1003-quarantine-and-security-gates.md)
- [ADR-1004](./1004-storage-strategy-for-artifacts-metadata-and-decisions.md)

## Context

The platform manages the lifecycle of uploaded artifacts and must support
reproducibility, auditability, and controlled movement across trust stages. If
artifacts can be changed in place, causal history is lost and investigations
become harder.

## Decision

All stored artifacts are treated as immutable.

Promotion happens only as a stage or status transition, never as an overwrite
of an existing object.

Baseline stage model:

- `incoming` for artifacts that were received but are not yet trusted;
- `trusted` for artifacts that passed the required checks and policy;
- `quarantine` for artifacts that are isolated and unavailable for normal consumption.

## Consequences

### Positive

- reproducibility and auditability improve;
- deterministic promotion pipelines become easier to build;
- forensic analysis becomes simpler.

### Negative

- storage usage may grow;
- retention and garbage-collection rules are required.

### Neutral

- promotion may be implemented either as a physical copy or as a logical state transition.

## Alternatives considered

- mutable overwrite by version or tag;
- `latest wins` with no stage model;
- manual promotion without explicit stages.

## Follow-up work

- [ ] define lifecycle states and transitions
- [ ] define retention policy
- [ ] define rollback semantics
