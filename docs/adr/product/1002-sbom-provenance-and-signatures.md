# ADR-1002: Use SBOM, provenance and signatures as first-class verification inputs

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

A mature trust model cannot rely only on vulnerability scanning or only on the
upload source. It needs independent signals about composition, provenance, and
authenticity.

## Decision

SBOMs, provenance, and signatures are treated as first-class inputs for trust
evaluation.

When one of these signals is missing, the policy may:

- block promotion;
- reduce the trust level;
- require a manual override.

The exact outcome depends on the policy tier and the ecosystem context.

## Consequences

### Positive

- trust decisions become deeper and higher quality;
- the platform gains a stronger foundation for compliance and explainability;
- policy tiers can be introduced based on verification maturity.

### Negative

- the ingestion pipeline becomes more complex;
- metadata storage requirements increase;
- verification-signal maturity depends on the surrounding ecosystem.

### Neutral

- different ecosystems may require different baseline verification inputs.

## Alternatives considered

- rely only on vulnerability scanning;
- treat SBOM and provenance as optional extras;
- verify signatures only selectively with no shared model.

## Follow-up work

- [ ] define verification baselines per ecosystem
- [ ] approve the canonical metadata model
- [ ] define policy tiers
