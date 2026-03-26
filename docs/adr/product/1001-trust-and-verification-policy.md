# ADR-1001: Separate artifact storage from trust decision

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0006](../architecture/0006-authn-authz-and-machine-identities.md)
- [ADR-0007](../architecture/0007-configuration-and-policy-as-code.md)
- [ADR-1000](./1000-artifact-immutability-and-promotion-model.md)
- [ADR-1002](./1002-sbom-provenance-and-signatures.md)
- [ADR-1003](./1003-quarantine-and-security-gates.md)
- [ADR-1004](./1004-storage-strategy-for-artifacts-metadata-and-decisions.md)

## Context

The fact that an artifact is physically stored does not mean it should be
trusted. A controlled supply-chain model needs a separate trust decision driven
by verification signals and policy.

## Decision

Two independent planes are separated:

1. the fact that the artifact is stored;
2. the trust decision attached to that artifact.

An artifact may exist in the system and still carry one of these trust
outcomes:

- `not_yet_trusted`;
- `trusted`;
- `denied`;
- `quarantined`;
- `expired`.

The trust decision is produced by a policy engine using verification signals
and policy context.

## Consequences

### Positive

- the trust model becomes more flexible and explainable;
- policy can evolve without changing the storage model;
- allow and deny outcomes become easier to justify.

### Negative

- cognitive and technical complexity increase;
- consistent status and verdict-reason models are required.

### Neutral

- the same artifact may receive different trust outcomes in different policy contexts.

## Alternatives considered

- treat `stored = trusted`;
- make the trust decision only at consumption time;
- rely only on vulnerability scanning.

## Follow-up work

- [ ] define trust signals
- [ ] define the verdict model
- [ ] define the explainability format
