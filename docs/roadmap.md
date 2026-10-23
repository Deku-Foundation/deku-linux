# Deku Linux Roadmap

This roadmap defines decision gates, not promised release dates. A stage is complete only when its exit criteria are supported by reviewable evidence. A validator passing tests is evidence for that validator—not evidence that an operating system can install or boot.

## Stage 0 — Governance and scope

- [x] Establish the project charter and initial contribution/security guidance.
- [ ] Confirm licenses for source, documentation, artwork and packaging metadata.
- [ ] Publish maintainer responsibilities and a decision process.
- [ ] Enable private vulnerability reporting and verify the contact route.
- [x] Add baseline documentation, website-link and language-metadata checks.

**Exit criteria:** contributors can identify project scope, license terms, decision process and reporting channels. This stage remains open until the unchecked governance and licensing items are resolved.

## Stage 1 — Architecture decisions

- [ ] Decide initial libc and target ABI.
- [ ] Decide init/service manager and boot approach.
- [ ] Define kernel selection, configuration and security-update policy.
- [ ] Define package identity, dependency, conflict and versioning semantics.
- [ ] Define repository trust, signed metadata, freshness and signing-key lifecycle.
- [ ] Choose release cadence and support policy.
- [ ] Review the threat model and security boundaries.

**Exit criteria:** critical decisions have accepted ADRs covering alternatives, consequences, operational costs and migration paths. Proposals are not accepted decisions.

## Stage 2 — Package and build prototypes

- [x] Define a minimal recipe metadata schema and strict input validation in [deku-recipes](https://github.com/Deku-Foundation/deku-recipes).
- [x] Test deterministic dependency planning and malformed dependency-graph failures in [deku-pkg](https://github.com/Deku-Foundation/deku-pkg).
- [x] Bound untrusted recipe, build-plan, installer-plan and package-catalog inputs before parsing.
- [x] Verify artifact bytes against supplied SHA-256 metadata using bounded streaming reads.
- [ ] Build a test package in a disposable, unprivileged environment.
- [ ] Record real source/build inputs, logs, artifact manifests and provenance from an executed build.
- [ ] Design and test signed repository metadata, key custody, rotation/revocation and rollback protection.
- [ ] Rebuild selected inputs in independent environments and investigate output differences.

**Exit criteria:** another contributor can build, inspect, verify and rebuild a harmless prototype using documented steps. Current validation prototypes do not satisfy this exit gate.

## Stage 3 — Minimal bootable image

- [ ] Compose a root filesystem from traceable, verified packages.
- [ ] Boot it in an emulator using documented automated tests.
- [ ] Test boot-failure diagnostics and recovery.
- [ ] Verify signature enforcement and update-failure behaviour.
- [ ] Test installation and upgrades in disposable virtual machines.

**Exit criteria:** repeatable image creation and boot smoke tests, with known limitations documented.

## Stage 4 — Developer preview

- [ ] Add an installer that operates only after explicit device selection and confirmation.
- [ ] Publish a hardware compatibility matrix and supported package set.
- [ ] Publish release notes, checksums, signatures and build provenance.
- [ ] Conduct threat-model review and external testing.
- [ ] Establish security advisory and end-of-life processes.

## Stage 5 — Public beta and stable release

- [ ] Define release-blocking criteria and regression tests.
- [ ] Test representative physical hardware and virtual machines.
- [ ] Review accessibility, localization, performance and documentation.
- [ ] Publish support commitments and incident-response procedures.
- [ ] Conduct independent security and supply-chain reviews.

A release must meet published criteria; a booting image alone is not sufficient evidence for a stable release.

## Scope discipline

Do not build a package manager, installer, desktop shell and complete repository infrastructure simultaneously. Prefer small prototypes, accepted decision records, upstream components and measurable exit criteria.
