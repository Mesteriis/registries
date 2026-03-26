# ADR-0016: Support GitHub and Gitea CI for template repositories

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0009](./0009-deployment-topology-and-runtime-model.md)
- [ADR-0012](./0012-define-repository-layout-and-file-placement-rules.md)
- [ADR-0015](./0015-enforce-template-quality-gates-and-governance-baseline.md)
- [ADR-2000](../engineering/2000-centralize-template-metadata-and-self-consistency-checks.md)

## Context

The template repository must work both for hosted GitHub and for self-hosted
Gitea installations. If the quality baseline exists only for one forge or one
CI environment, the template stops being portable and requires manual
adaptation immediately after project creation.

The repository also assumes `Dokploy Method 2`, where the platform tracks the
git repository itself, and the CI pipeline focuses on quality gates, image
build validation, and security checks rather than imperative deployment.

## Decision

The template ships with two compatible CI definitions:

- `.github/workflows/ci.yml` for GitHub Actions;
- `.gitea/workflows/ci.yml` for self-hosted Gitea Actions.

Shared rules:

- quality gates in both CI systems must be equivalent in meaning;
- the pipeline is limited to at most two parallel test jobs before a shared security or image job;
- backend and frontend are checked separately;
- the security or image job runs container linting, shell linting, filesystem scanning, and smoke Docker builds;
- Docker images are always tagged with `latest`, branch name, and commit SHA;
- under `Dokploy Method 2`, a deployment step from CI is optional and not part of the baseline pipeline.

Gitea-specific baseline:

- the workflow uses runner labels `python`, `node`, and `main`;
- the `main` runner performs Docker and security steps, while `python` and `node` handle language-specific checks.

GitHub-specific baseline:

- the workflow uses hosted runners and explicit setup for Python, `uv`, Node/pnpm, and security tooling;
- the quality-gate logic stays equivalent to the Gitea pipeline.

## Consequences

### Positive

- the template remains portable across GitHub and self-hosted Gitea;
- quality gates work consistently before a team chooses one forge platform;
- Dockerfile and shell-entrypoint hygiene are enforced in the baseline pipeline.

### Negative

- two workflow definitions must be maintained;
- drift between CI configurations becomes a separate review risk.

### Neutral

- concrete deployment automation can be added later in a separate ADR without changing the baseline CI contract.

## Alternatives considered

- supporting only GitHub Actions;
- supporting only Gitea Actions;
- leaving CI adaptation to every generated project.

## Follow-up work

- [x] add the GitHub workflow
- [x] add the Gitea workflow
- [x] fix `Dokploy Method 2` as the baseline with no CI-driven deploy
- [ ] add separate deployment workflows for environment-specific targets if needed
