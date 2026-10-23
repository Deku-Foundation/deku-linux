# Deku Linux: Growth and Reliability Strategy

- **Status:** Strategic proposal
- **Date:** 2026-10-23
- **Review cadence:** Every 6 months, and after a major incident or scope change

## Executive direction

Build Deku as an independent distribution gradually, while reusing mature upstream components and tools wherever this reduces risk without undermining the project's goals. The differentiator should be a coherent, well-integrated system with trustworthy updates, clear support boundaries, good documentation, and a disciplined release process—not the number of components rewritten from scratch.

No forecast guarantees adoption, funding, security, or long-term maintenance. Growth depends on consistent delivery, trust, contributor capacity, hardware coverage, and the ability to respond to problems.

## What the project should optimize for

1. **Recoverability:** failed upgrades and configuration errors must have documented diagnosis and recovery paths.
2. **Supply-chain integrity:** source inputs, build environments, artifacts, and publication must be traceable.
3. **Maintainability:** minimize bespoke infrastructure and patches that only project insiders understand.
4. **Compatibility:** define a supported hardware and software baseline and test it continuously.
5. **Predictability:** publish update channels, support windows, and release criteria.
6. **Contributor sustainability:** keep ownership clear, automate routine work, and avoid dependence on a single person.
7. **User trust:** make limitations, known issues, support status, and security advisories visible.

## Scenario-based outlook

These are planning scenarios, not statistical predictions. The dates are illustrative gates and must be revised based on actual capacity.

### 0–6 months: establish engineering credibility

Expected focus:
- governance, licenses, maintainers, architecture decision records, and contribution workflow;
- CI for documentation and repository hygiene;
- a threat model and explicit package trust model;
- small experiments for packaging and isolated builds.

Success evidence:
- important design decisions have reviewed ADRs;
- CI is repeatable and has least-privilege permissions;
- a new contributor can reproduce the documented development setup;
- no public release is claimed before release criteria exist.

### 6–18 months: prove the core technically

Expected focus:
- a minimal package recipe and build prototype;
- a small set of core packages with source checksums, license metadata, tests, and build logs;
- package signing and repository metadata verification;
- virtual-machine image and update/recovery tests.

Success evidence:
- another maintainer can independently build and verify the prototype;
- package installation, upgrade, interruption, and rollback/recovery behavior are tested;
- release artifacts have checksums, signatures, and build provenance;
- known limitations are published.

### 18–36 months: evaluate a limited public preview

This stage is conditional, not a promise. It should begin only if the project has enough maintainers and test capacity.

Expected focus:
- a narrowly supported hardware matrix;
- an installer prototype, release notes, and update channel;
- security response process and regression testing;
- external testing and review.

Success evidence:
- no release-blocking defects remain under published criteria;
- installation, upgrade, recovery, and security-update paths have evidence;
- maintainers can respond to issues without relying on one person;
- a support and end-of-life policy is published.

### Beyond 36 months: grow only where capacity supports it

Possible growth includes more hardware, additional desktop environments, a server profile, or a stable channel. Each expansion increases test and maintenance cost. Add one only when existing support is healthy and measurable.

## Principal risks and responses

| Risk | Likely consequence | Response |
|---|---|---|
| Scope grows too early | Many incomplete subsystems | Freeze scope around one target and one desktop profile |
| Maintainer bottleneck | Delayed fixes and stalled releases | Document ownership, automate checks, recruit reviewers |
| Supply-chain compromise | Malicious or untrusted artifacts | Isolate builds, separate signing from building, publish provenance |
| Update regression | Systems become unusable | Staged updates, test suites, recovery procedures, clear advisories |
| Hardware variability | Failures on user machines | Publish supported matrix, test representative devices, collect diagnostics safely |
| Upstream changes | Patch burden and compatibility breaks | Track upstream, keep patches small, test upgrades |
| Unclear licensing or naming | Legal or community friction | Audit licenses and trademarks before wider publication |
| Unrealistic promises | Loss of user trust | Publish evidence and limitations; avoid unsupported guarantees |

## Reliability model

Reliability is a system of controls rather than one feature.

### Before a change ships
- review source changes and dependency changes;
- validate package metadata, checksums, and licenses;
- build in isolated environments with minimal privileges;
- run unit, integration, install, upgrade, and boot tests appropriate to the change;
- keep signing keys out of ordinary build jobs.

### Before a release ships
- freeze the candidate and publish release criteria;
- test installation, upgrade, interruption, recovery, and security updates in disposable virtual machines;
- provide checksums, signatures, release notes, and provenance;
- document known issues and supported hardware;
- ensure a maintainer is responsible for the release and incident response.

### After a release ships
- monitor reports and upstream advisories;
- triage vulnerabilities separately from ordinary bugs;
- provide a clear update path and recovery instructions;
- publish incident notes and corrective actions where appropriate;
- retire unsupported releases according to the published policy.

## Suggested metrics

Track trends rather than optimizing a single score.

- Percentage of changes passing required CI checks.
- Number and age of release-blocking defects.
- Time from confirmed critical vulnerability to available fix, once releases exist.
- Percentage of packages with complete source, license, checksum, and build metadata.
- Percentage of release artifacts with verifiable signatures and provenance.
- Success rate for clean installation and upgrade tests across the supported matrix.
- Number of active maintainers able to perform a release independently.
- Time to reproduce a reported defect from its documented evidence.

Do not publish numerical targets until the baseline is measured and maintainers agree that the targets are realistic.

## Decisions to make before implementation expands

1. Target users and initial product profile.
2. Base ABI and C library.
3. Init and service management.
4. Package format, dependency semantics, signing, and repository metadata.
5. Build isolation and provenance strategy.
6. Update channels, rollback/recovery, and support lifecycle.
7. Desktop and installer scope.
8. Governance, licensing, trademark ownership, and maintainer succession.

## Review rule

If project capacity falls below what is needed to maintain the supported package set and respond to security issues, reduce scope or pause releases rather than silently lowering quality gates.
