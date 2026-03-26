# ADR-1003: Introduce explicit quarantine and security gates

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0004](../architecture/0004-observability-and-audit-trail.md)
- [ADR-1000](./1000-artifact-immutability-and-promotion-model.md)
- [ADR-1001](./1001-trust-and-verification-policy.md)
- [ADR-1002](./1002-sbom-provenance-and-signatures.md)

## Context

Some artifacts cannot simply remain “not promoted.” They must be held back from
consumption, escalated for manual review, marked as suspicious, and preserved
with a forensic trail.

## Decision

Quarantine is introduced as an explicit state with its own operational model.

An artifact is moved into quarantine when:

- a high-risk verdict is produced;
- trust policy is violated;
- the source is considered compromised;
- there are signs of tampering;
- a security operator performs a manual isolation step.

Security gates and the quarantine model are applied explicitly rather than
through informal operator conventions.

## Consequences

### Positive

- suspicious artifacts get a clear operational model;
- “not yet verified” and “dangerous” become distinct states;
- incident response becomes stronger.

### Negative

- UI or API support is needed for investigation and override flows;
- rules are needed for leaving quarantine.

### Neutral

- quarantine may be triggered automatically or manually.

## Alternatives considered

- soft-fail only with no quarantine;
- simple deny with no separate state;
- deleting suspicious artifacts from the system.

## Follow-up work

- [ ] define a taxonomy of quarantine reasons
- [ ] describe the release and unquarantine flow
- [ ] define the incident annotation model
