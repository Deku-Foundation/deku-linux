# ADR-0003: Deku Native Package System

- **Status:** Proposed — prototype and review required
- **Date:** 2026-10-23
- **Scope:** Native packages, repository metadata, dependency solving, transactions, and application delivery

## Problem

Deku needs a broad, current software catalog without inheriting another distribution's package policy or writing a fragile package manager in one step. The package manager is a core product component, but a package manager alone does not create a large catalog: recipes, build capacity, update triage, and maintainers do.

## Proposed direction

Build a Deku-owned package manager and repository format in stages. Own the user-facing workflow, metadata contract, trust model, transaction coordinator, repository service, and integration tests. Reuse narrowly scoped, maintained libraries where they materially improve correctness; do not bind the project to an upstream distribution's complete packaging model before evidence supports it.

The working name is **Deku Package System**. The executable and public package format names remain open until a prototype and naming review. This ADR does not claim that a package manager already exists.

## Design requirements

### Package and repository model

- Declarative, versioned package manifests with a machine-readable schema and strict validation.
- Separate source recipes from built binary packages.
- Record source URLs, immutable revisions, cryptographic digests, license identifiers, patches, build inputs, outputs, and maintainer ownership.
- Support package splits, architecture and ABI constraints, optional features, conflicts, replacements, virtual capabilities, and explicit dependency types.
- Keep repository indexes signed and versioned; verify metadata before trusting package hashes or dependency data.
- Support mirrors and resumable downloads without weakening signature checks.
- Make package provenance and installed-file ownership queryable.

### Dependency resolution

- Model dependency solving as a separately testable component.
- Define deterministic selection rules for versions, repositories, architecture, conflicts, and explicit user intent.
- Evaluate a mature solver library against a small independent prototype before selecting the implementation. Compare correctness, licensing, language bindings, maintenance activity, performance, and the cost of maintaining the integration.
- Do not implement a custom SAT solver merely for ideological purity.

### Transactions and recovery

- Compute and display a complete transaction plan before changing the system.
- Validate disk space, package signatures, dependency closure, file conflicts, and required service actions before commit.
- Stage downloads and package extraction before activating changes.
- Maintain a durable transaction journal and recover safely from power loss or process termination.
- Design a snapshot-provider interface. Test Btrfs snapshots first; support other recovery strategies only with explicit guarantees. Do not describe every install as atomic or rollback-capable until the selected filesystem path has been tested.
- Preserve user configuration and distinguish package-owned files from administrator-modified files.
- Provide a clear rollback and repair workflow with logs that do not expose secrets.

### Security boundaries

- Never execute package build scripts as root.
- Separate untrusted source builds from trusted repository signing and publication.
- Verify repository signatures and package digests; use distinct keys and documented rotation/revocation procedures.
- Treat package hooks as privileged code. Minimize them, declare their effects, constrain execution, and record failures.
- Reject path traversal, unsafe archive entries, unexpected ownership/modes, and conflicting package file claims.
- Do not allow package metadata from an untrusted mirror to authorize a new signing key.
- Publish a threat model and security response process before production repositories exist.

### Software availability

- Build a maintained native catalog for the base OS, libraries, drivers, system services, development tools, and core desktop applications.
- Evaluate integration with an established sandboxed desktop application format for applications that are costly to maintain natively. Keep this an explicit integration boundary, not a claim that Deku's native repository contains every application.
- Prioritize catalog breadth through recipe automation, shared build infrastructure, CI, clear ownership, and upstream update monitoring.
- Avoid copying entire external package collections without license review, provenance, build-policy review, and a plan to keep them updated.

## Implementation language and module boundaries

Rust is the leading candidate for the privileged client and transaction core because memory safety matters at this boundary. This is a proposal, not a requirement for every Deku component. Compare implementation effort, available libraries, testability, and maintainability before committing.

Initial logical modules:

1. `manifest` — schema, validation, canonical serialization.
2. `repository` — signed metadata, mirrors, freshness and rollback protection.
3. `solver` — deterministic dependency resolution.
4. `store` — verified downloads, cache and immutable artifact identity.
5. `transaction` — plan, stage, commit, journal, recovery.
6. `database` — installed package state and file ownership.
7. `build` — unprivileged recipe execution and provenance, kept separate from the privileged installer.
8. `cli` — inspectable commands and machine-readable output.

Keep these as modules in one tested codebase initially. Split them into separate services or repositories only when independent ownership or security boundaries justify it.

## Prototype sequence

1. Specify the manifest and repository metadata schemas.
2. Implement schema validation and fixtures for valid, invalid, and adversarial inputs.
3. Build and install a harmless package in a disposable virtual machine.
4. Implement signed repository metadata and signature/key-rotation tests.
5. Implement dependency planning and conflict detection without modifying the host.
6. Add staged installation, durable journal, file ownership database, interruption tests, and recovery.
7. Test upgrades and rollback on supported filesystem configurations.
8. Add build isolation, provenance, and a separate publish/sign workflow.
9. Benchmark a representative dependency graph and package set before optimizing.
10. Publish a small test repository; do not promote it to a user-facing release until upgrade, recovery, and security tests pass.

## Alternatives considered

- **Adopt an existing package manager unchanged:** faster initial result, but it may constrain Deku's desired package semantics and user experience. Keep it as a benchmark and fallback while requirements are tested.
- **Write every component from scratch:** maximum control, but unnecessarily increases the risk of dependency-solving, archive-handling, and transaction bugs.
- **Use only immutable whole-system images:** offers strong deployment semantics, but does not alone satisfy the desired interactive native package workflow.
- **Use a hybrid design:** Deku owns the package workflow and repository contract, with tested libraries and optional snapshot support. This is the proposed direction.

## Acceptance criteria

This ADR can be accepted only after a reviewed prototype demonstrates: manifest validation; deterministic solving on a fixture graph; signature verification; rejection of malformed archives; interruption-safe transaction recovery; clear file ownership; documented license obligations; and measured build and maintenance cost.

Until then, all package-system features remain proposals. No production package repository, universal rollback guarantee, or complete application catalog is claimed.
