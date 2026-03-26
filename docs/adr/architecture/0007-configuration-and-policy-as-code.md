# ADR-0007: Keep configuration and operational policy under version control

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0006](./0006-authn-authz-and-machine-identities.md)
- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-0022](./0022-group-backend-settings-into-nested-platform-models.md)
- [ADR-1001](../product/1001-trust-and-verification-policy.md)
- [ADR-1003](../product/1003-quarantine-and-security-gates.md)

## Context

Operational rules, trust policy, routing rules, thresholds, and toggles should
not live only in a UI, a database, or in the heads of individual operators.
These decisions need review, diffs, and rollback.

## Decision

Configuration and policy that influence platform behavior are kept as code or
config under version control.

This includes:

- operational policy;
- trust and verification rules;
- environment-specific configuration;
- allow and deny lists;
- thresholds and gates;
- override rules.

Changes to these rules go through review and validation before they are
applied.

## Consequences

### Positive

- rule changes get a reviewable history;
- rollback and diff analysis become easier;
- reproducibility across environments improves.

### Negative

- operators get less instant flexibility;
- safe mechanisms for policy loading and validation are required.

### Neutral

- a UI on top of policy-as-code is acceptable if it still generates a versioned source of truth.

## Alternatives considered

- keeping policy only in a database;
- keeping policy only in a UI;
- manual overrides with no versioned source of truth.

## Follow-up work

- [ ] choose the policy format
- [ ] describe the validation pipeline
- [ ] define the override process
