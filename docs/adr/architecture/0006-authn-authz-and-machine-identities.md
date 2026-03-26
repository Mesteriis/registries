# ADR-0006: Use explicit machine identities and policy-based authorization

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0004](./0004-observability-and-audit-trail.md)
- [ADR-0007](./0007-configuration-and-policy-as-code.md)
- [ADR-1001](../product/1001-trust-and-verification-policy.md)
- [ADR-1003](../product/1003-quarantine-and-security-gates.md)

## Context

The system interacts not only with humans but also with automation, internal
services, and external agents. Without an explicit identity and authorization
model, critical operations quickly end up protected inconsistently.

## Decision

The system distinguishes between:

- human identities;
- machine identities;
- internal service identities.

Authorization follows a policy-based model instead of an ad-hoc collection of
role checks. Sensitive operations must explicitly evaluate actor type, scope,
policy context, and auditability.

## Consequences

### Positive

- security and operational transparency improve;
- CI/CD and service-to-service flows become easier to automate;
- dangerous actions become easier to constrain and audit.

### Negative

- initial complexity increases;
- credential and token lifecycle management becomes necessary.

### Neutral

- a specific identity provider may be chosen later in a separate ADR.

## Alternatives considered

- shared admin tokens;
- role checks with no policy model;
- no separation between human and machine actors.

## Follow-up work

- [ ] describe the actor model
- [ ] define a matrix of sensitive operations
- [ ] lock down the credential lifecycle
