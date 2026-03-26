# ADR-0000: Record architecture decisions

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-0016](./0016-support-github-and-gitea-ci-for-template-repositories.md)

## Context

Important architecture decisions are quickly lost in chats, pull requests, and
verbal agreements. Without a persistent decision log, it becomes hard to
understand why the system looks the way it does and which constraints were
chosen deliberately.

## Decision

Architecture-significant decisions are recorded as ADRs in `docs/adr`.

Each ADR:

- documents one decision;
- is reviewed through a pull request;
- has a unique number;
- remains part of repository history;
- is updated by a new ADR rather than by rewriting the old one.

## Consequences

### Positive

- the repository gains a single log of architecture decisions;
- onboarding becomes easier for new contributors;
- already-made decisions are discussed repeatedly less often.

### Negative

- the team must keep ADRs up to date with discipline;
- stale statuses can become misleading if they are not maintained.

### Neutral

- ADRs do not replace RFCs, design docs, or issues; they record the accepted decision itself.

## Alternatives considered

- not documenting decisions formally;
- documenting decisions only in issues and pull requests;
- keeping a separate wiki outside the repository.

## Follow-up work

- [ ] add an ADR checklist to the PR template
- [ ] create a reusable ADR template
- [ ] treat architecture changes without an ADR as incomplete
