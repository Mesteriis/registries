# Product ADR

This section contains reference decisions that describe the domain model and
product semantics for derived projects.

It does not mean the current repository already implements the full product
scope. These ADRs exist as examples of how the template records domain
decisions once a real project starts growing on top of the baseline.

Mandatory entrypoint before reading individual ADRs:
[ADR Reading Map](/adr/INDEX).

Use this section for decisions about:

- domain entity lifecycle;
- trust model and verification rules;
- domain-specific storage model;
- quarantine, override, promotion, and other business-significant states;
- external ecosystems, adapters, and the canonical identity model.

Current accepted ADRs:

- [1000-artifact-immutability-and-promotion-model.md](./1000-artifact-immutability-and-promotion-model.md)
- [1001-trust-and-verification-policy.md](./1001-trust-and-verification-policy.md)
- [1002-sbom-provenance-and-signatures.md](./1002-sbom-provenance-and-signatures.md)
- [1003-quarantine-and-security-gates.md](./1003-quarantine-and-security-gates.md)
- [1004-storage-strategy-for-artifacts-metadata-and-decisions.md](./1004-storage-strategy-for-artifacts-metadata-and-decisions.md)
