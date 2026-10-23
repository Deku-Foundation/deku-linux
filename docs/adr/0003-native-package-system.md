# ADR-0003: Deku Native Package System

- **Status:** Proposed — prototype exists; production acceptance criteria remain open
- **Date:** 2026-10-23
- **Scope:** Native packages, repository metadata, dependency solving, transactions and application delivery

## Problem

Deku needs a broad, current software catalog without inheriting another distribution's package policy or writing a fragile package manager in one step. A package manager alone does not create a large catalog: recipes, build capacity, update triage and maintainers do.

## Current implementation status

The [deku-pkg](https://github.com/Deku-Foundation/deku-pkg) repository contains a Python planning prototype and a Rust core that validates bounded package-catalog JSON, checks package metadata and dependency graphs, computes deterministic dependency order, and verifies artifact bytes against a supplied SHA-256 digest using bounded streaming reads.

This is **not** a production package manager. It does not authenticate repository publishers, download artifacts, validate archives, install files, track file ownership, execute hooks, update the host or recover transactions. A SHA-256 digest establishes consistency with supplied metadata; it does not establish who published that metadata.

The [deku-recipes](https://github.com/Deku-Foundation/deku-recipes) repository validates recipe metadata but does not execute recipes. The [deku-build](https://github.com/Deku-Foundation/deku-build) repository validates build plans but does not execute isolated builds.

## Proposed direction

Build a Deku-owned package manager and repository format in stages. Own the user-facing workflow, metadata contract, trust model, transaction coordinator, repository policy and integration tests. Reuse narrowly scoped, maintained libraries where they materially improve correctness; do not bind the project to an upstream distribution's complete packaging model before evidence supports it.

The working name is **Deku Package System**. The executable name and public package-format name remain open until a prototype and naming review.

## Design requirements

### Package and repository model

- Declarative, versioned package manifests with a machine-readable schema and strict validation.
- Separate source recipes from built binary packages.
- Record source URLs, immutable revisions, cryptographic digests, license identifiers, patches, build inputs, outputs and maintainer ownership.
- Support package splits, architecture and ABI constraints, optional features, conflicts, replacements, virtual capabilities and explicit dependency types.
- Keep repository indexes signed and versioned; verify metadata before trusting package hashes or dependency data.
- Support mirrors and resumable downloads without weakening signature checks.
- Make package provenance and installed-file ownership queryable.

### Dependency resolution

- Model dependency solving as a separately testable component.
- Define deterministic selection rules for versions, repositories, architecture, conflicts and explicit user intent.
- Evaluate a mature solver library against a small independent prototype before selecting the implementation. Compare correctness, licensing, language bindings, maintenance activity, performance and integration cost.
- Do not implement a custom SAT solver merely for ideological purity.

### Transactions and recovery

- Compute and display a complete transaction plan before changing the system.
- Validate disk space, package signatures, dependency closure, file conflicts and required service actions before commit.
- Stage downloads and package extraction before activating changes.
- Maintain a durable transaction journal and recover safely from power loss or process termination.
- Design a snapshot-provider interface. Test Btrfs snapshots first; support other recovery strategies only with explicit guarantees. Do not describe every install as atomic or rollback-capable until the selected filesystem path has been tested.
- Preserve user configuration and distinguish package-owned files from administrator-modified files.
- Provide a clear rollback and repair workflow with logs that do not expose secrets.

### Security boundaries

- Never execute package build scripts as root.
- Separate untrusted source builds from trusted repository signing and publication.
- Verify repository signatures and package digests; use distinct keys and documented rotation/revocation procedures.
- Treat package hooks as privileged code. Minimize them, declare their effects, constrain execution and record failures.
- Reject path traversal, unsafe archive entries, unexpected ownership/modes and conflicting package file claims.
- Do not allow package metadata from an untrusted mirror to authorize a new signing key.
- Publish a threat model and security response process before production repositories exist.

### Software availability

- Build a maintained native catalog for the base OS, libraries, drivers, system services, development tools and core desktop applications.
- Evaluate integration with an established sandboxed desktop application format for applications that are costly to maintain natively. Keep this an explicit integration boundary, not a claim that Deku's native repository contains every application.
- Prioritize catalog breadth through recipe automation, shared build infrastructure, CI, clear ownership and upstream update monitoring.
- Avoid copying entire external package collections without license review, provenance, build-policy review and a plan to keep them updated.

## Implementation language and module boundaries

Rust is the current language for the package-core prototype because memory safety matters at this boundary. This does not require every Deku component to be written in Rust. Evaluate available libraries, correctness, testability and maintainability before committing the full architecture.

Initial logical modules:

1. manifest — schema, validation and canonical serialization.
2. repository — signed metadata, mirrors, freshness and rollback protection.
3. solver — deterministic dependency resolution.
4. store — verified downloads, cache and immutable artifact identity.
5. transaction — plan, stage, commit, journal and recovery.
6. database — installed package state and file ownership.
7. build — unprivileged recipe execution and provenance, kept separate from the privileged installer.
8. cli — inspectable commands and machine-readable output.

Keep these as modules in one tested codebase initially. Split them into separate services or repositories only when independent ownership or security boundaries justify it.

## Prototype sequence

1. Specify the manifest and repository metadata schemas; the first catalog/recipe validation schemas exist, while the signed repository contract remains open.
2. Implement schema validation and fixtures for valid, invalid and adversarial inputs; bounded metadata validators and dependency-graph tests exist.
3. Build and install a harmless package in a disposable virtual machine; not implemented.
4. Implement signed repository metadata and signature/key-rotation tests; not implemented.
5. Implement dependency planning and conflict detection without modifying the host; deterministic dependency ordering exists, but version solving and file-conflict planning remain incomplete.
6. Add staged installation, durable journal, file-ownership database, interruption tests and recovery; not implemented.
7. Test upgrades and rollback on supported filesystem configurations; not implemented.
8. Add build isolation, provenance and a separate publish/sign workflow; not implemented.
9. Benchmark a representative dependency graph and package set before optimizing.
10. Publish a small test repository; do not promote it to a user-facing release until upgrade, recovery and security tests pass.

## Alternatives considered

- **Adopt an existing package manager unchanged:** faster initial result, but it may constrain Deku's desired package semantics and user experience. Keep it as a benchmark and fallback while requirements are tested.
- **Write every component from scratch:** maximum control, but unnecessarily increases the risk of dependency-solving, archive-handling and transaction bugs.
- **Use only immutable whole-system images:** offers strong deployment semantics, but does not alone satisfy the desired interactive native package workflow.
- **Use a hybrid design:** Deku owns the package workflow and repository contract, with tested libraries and optional snapshot support. This is the proposed direction.

## Acceptance criteria

This ADR can be accepted only after a reviewed prototype demonstrates manifest validation; deterministic solving on a fixture graph; signature verification; rejection of malformed archives; interruption-safe transaction recovery; clear file ownership; documented license obligations; and measured build and maintenance cost.

Until then, all package-system features remain proposals or experimental prototypes. No production package repository, universal rollback guarantee or complete application catalog is claimed.
