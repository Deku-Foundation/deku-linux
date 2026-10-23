# Deku Linux Roadmap

This roadmap defines decision gates, not promised release dates. A stage is complete only when its exit criteria are evidenced.

## Stage 0 — Governance and scope

- [x] Establish project charter and initial contribution/security guidance.
- [ ] Confirm licenses for source, documentation, artwork, and packaging metadata.
- [ ] Publish maintainer responsibilities and decision process.
- [ ] Enable private vulnerability reporting and verify the contact route.
- [ ] Add baseline documentation checks.

**Exit criteria:** contributors can identify the project's scope, license terms, decision process, and reporting channels.

## Stage 1 — Architecture decisions

- [ ] Decide initial libc and target ABI.
- [ ] Decide init/service manager and boot approach.
- [ ] Define kernel selection, configuration, and security update policy.
- [ ] Define package identity, dependency, conflict, and versioning semantics.
- [ ] Define package-source trust, metadata, and signing-key model.
- [ ] Choose release cadence and support policy.
- [ ] Document the threat model and security boundaries.

**Exit criteria:** critical decisions have accepted ADRs covering alternatives, consequences, and migration costs.

## Stage 2 — Package/build prototype

- [ ] Define a minimal package recipe schema.
- [ ] Build a test package in an isolated environment.
- [ ] Record source checksums, build inputs, logs, and artifact hashes.
- [ ] Test dependency resolution and failure behavior.
- [ ] Design signing and key custody before publishing packages.
- [ ] Compare clean builds and document sources of variation.

**Exit criteria:** another contributor can build, inspect, verify, and rebuild the prototype from documented steps.

## Stage 3 — Minimal bootable image

- [ ] Compose an image from traceable packages.
- [ ] Boot it in an emulator using documented automated tests.
- [ ] Test boot failure diagnostics and recovery.
- [ ] Verify signature enforcement and update failure behavior.
- [ ] Test installation and upgrades in disposable virtual machines.

**Exit criteria:** repeatable image creation and boot smoke tests, with limitations documented.

## Stage 4 — Developer preview

- [ ] Add an installer prototype and hardware compatibility matrix.
- [ ] Add a supported package set and update workflow.
- [ ] Publish release notes, checksums, signatures, and build provenance.
- [ ] Conduct threat-model review and external testing.
- [ ] Establish security advisory and end-of-life processes.

## Stage 5 — Public beta and stable release

- [ ] Define release-blocking criteria and regression tests.
- [ ] Test representative physical hardware and virtual machines.
- [ ] Review accessibility, localization, performance, and documentation.
- [ ] Publish support commitments and incident response procedures.
- [ ] Conduct independent security and supply-chain reviews.

A release must meet published criteria; a booting image alone is not sufficient evidence for a stable release.

## Scope discipline

Do not build a package manager, installer, desktop shell, and complete repository infrastructure simultaneously. Prefer small prototypes, explicit decision records, upstream components, and measurable exit criteria.
