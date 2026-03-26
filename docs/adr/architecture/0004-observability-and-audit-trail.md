# ADR-0004: Make observability and audit trail first-class concerns

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0003](./0003-event-driven-internal-integration.md)
- [ADR-0006](./0006-authn-authz-and-machine-identities.md)
- [ADR-0021](./0021-centralize-backend-observability-bootstrap-and-structured-telemetry.md)
- [ADR-1004](../product/1004-storage-strategy-for-artifacts-metadata-and-decisions.md)

## Context

Without strong observability, the platform quickly turns into a black box. For
operations, security, and explainability, the system needs not only technical
logs but also a full audit trail for sensitive actions.

## Decision

Observability and audit are treated as baseline system properties.

Mandatory elements:

- structured logs;
- trace and correlation identifiers;
- metrics for APIs, job execution, and integration points;
- audit records for sensitive actions;
- domain events and pipeline state changes.

Audit and observability are related, but they are not the same concern.

## Consequences

### Positive

- incidents and regressions are easier to investigate;
- system decisions become easier to explain;
- platform-critical flows become easier to operate.

### Negative

- storage and retention requirements increase;
- a redaction and sensitive-data control policy is required.

### Neutral

- local development may use a simplified observability stack, but not a different event model.

## Alternatives considered

- technical logs only;
- audit as a later follow-up concern;
- minimal logs with no correlation.

## Follow-up work

- [ ] define the audit-event taxonomy
- [ ] lock down the log schema
- [ ] document the redaction policy
