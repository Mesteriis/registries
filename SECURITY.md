# Security Policy

## Reporting

Do not open a public issue for suspected credential leaks, supply-chain incidents or exploitable vulnerabilities.

Report privately to the repository owners first.

## Baseline

- dependencies are audited in CI
- Dockerfiles and shell entrypoints are linted in CI
- filesystem scans run through `trivy`
- migrations are reviewable and version-controlled
- production containers should run with least privilege
