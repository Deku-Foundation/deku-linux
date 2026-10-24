# Infrastructure-First Architecture and Roadmap

**Status:** active engineering strategy, 2026-10-24. **ISO work is paused.** The target is an independent distribution built from reviewed open-source components—not a Fedora re-spin.

## 1. Mission and design rule

Deku should own the integration, package contracts, Rust control plane, security policy, repository trust, profile system, update semantics and user experience that differentiate it. Reuse mature Linux upstream projects for low-level capabilities where rewriting them would add risk rather than value.

“Rust-first” means new Deku-owned control-plane code is primarily Rust where that improves memory safety, type guarantees and testing. It does not mean rewriting the Linux kernel, libc, firmware, compiler toolchain, desktop frameworks or cryptography.

The platform is not practical until one small source package can pass through the full chain: reviewed recipe → isolated build → package artifact → authenticated repository metadata → verified install plan → recoverable transaction → auditable installed state.

## 2. What to learn from existing systems

| Upstream | Reusable engineering lesson | What Deku should not assume |
| --- | --- | --- |
| [Void XBPS](https://github.com/void-linux/xbps) | Clear separation of source templates, package generation, binary repository/index, file state, dependency ordering and package repair; BSD-2-Clause source can support selected reuse subject to notices. | Its C implementation, package format and service model do not automatically fit Deku. Adaptations must preserve behavior and test vectors. |
| [Void void-packages](https://github.com/void-linux/void-packages) | Maintained recipes, explicit phases, patches and a build master directory. | Recipe shell is executable code. It must never run with host secrets or trusted publishing credentials. |
| [Nix/Nixpkgs](https://github.com/NixOS/nixpkgs) | Declarative derivations, explicit dependency graphs, immutable references, isolated builds, content-addressed ideas and generations. | Nixpkgs' MIT license covers its repository expression code, not automatically the upstream packages or all included patches. Nix's store does not alone solve repository trust or hardware integration. |
| [Fedora Anaconda](https://github.com/rhinstaller/anaconda) | Mature installation flow, storage planning, automated Kickstart workflows and separation of UI/installation logic. | Anaconda is GPL-2.0 and depends on other installer services. Reusing it does not mean inheriting Fedora's package-management assumptions or branding. |
| [Debian reproducible builds](https://wiki.debian.org/ReproducibleBuilds) | Record build environments and compare independent rebuilds; normalize timestamps, paths, locales, ordering and other sources of nondeterminism. | A matching source commit does not guarantee a reproducible binary. Measure equality rather than claiming it. |
| [TUF](https://theupdateframework.io/spec/) | Separate trust roles, metadata freshness/expiry, rollback resistance, key rotation and controlled delegation. | A SHA-256 digest or HTTPS URL does not authenticate a publisher. Do not invent a cryptographic protocol. |
| [SPDX](https://spdx.dev/use/specifications/) and [SLSA](https://slsa.dev/spec/v1.2/) | Standard SBOM and build-provenance formats let external parties inspect inputs and builder claims. | Unsigned JSON is not authenticated provenance; a file listing is not a complete SBOM. |
| [bootc](https://github.com/bootc-dev/bootc), [OSTree](https://github.com/ostreedev/ostree) | Image-based systems can provide coherent OS updates and rollback boundaries. | Image-based and mutable package-root models have different semantics. Deku must choose one transaction owner instead of stacking competing rootfs mechanisms. |

## 3. Code-reuse policy: mandatory before importing source

Every imported implementation needs a record with canonical upstream URL, exact commit/tag, license expression, copyright/NOTICE files, copied/modified file list, patch rationale, upstream contribution status, security-update owner and rebase procedure.

- Do not paste GPL code into an MIT-only component while claiming the combined derivative is MIT. Anaconda is GPL-2.0; a substantial derivative must use compatible distribution terms and retain notices.
- Reuse only the files and dependencies needed for a clear capability. Do not wholesale-copy a distribution's package manager, repositories, brand, release keys, defaults or service layout by accident.
- Generate a license inventory from SPDX identifiers. SPDX 3.0 is the current schema family to evaluate; 2.3 may remain the practical exchange format for some tools.
- Preserve copyright, license, attribution and modification notices. Track patches and upstream security fixes.
- Prefer upstream contributions to long-lived divergences. Pin exact consumed revisions and run regression tests before updating them.
- Code licensing does not license logos or bundled third-party assets automatically; review these separately.

## 4. Target architecture and trust boundaries

### Source and recipe registry — deku-recipes
Recipes are reviewed source declarations, not arbitrary application JSON. A production recipe must describe package name/version, immutable source and SHA-256, patches with their own hashes, SPDX license expression, architectures/ABI, hard and optional dependencies, build steps, output names, test commands and build-environment digest. Validators fail closed on unknown schema versions and duplicate keys, bound inputs, reject unsafe URLs/paths and distinguish package intent from an approved build. Recipe code remains untrusted even after review.

### Acquisition and build orchestration — deku-build
Use a two-domain pipeline. A small fetch service accesses the network, restricts schemes/redirects/addresses, applies download caps and verifies pinned digests. A build worker receives verified inputs, runs in a disposable VM or a separately reviewed isolation boundary, has no signing secrets and no network by default during compilation, has resource limits, and emits an artifact plus a typed result/provenance record. A verifier checks archive paths, ownership metadata, expansion limits, package tests and provenance. Release approval/signing is separate from source builds and untrusted PR jobs.

Containers share the host kernel and are not assumed to resist a malicious compiler. Package builds may require root-like ownership semantics inside the guest; this must never confer host-root authority.

### Binary package and transaction engine — deku-pkg
The Rust library is the package-policy core. Keep pure operations (parse, validate, solve, calculate effects) separate from I/O and privileged execution. The client creates an immutable transaction plan, verifies signatures and hashes, checks disk space and file conflicts, stages files, writes a durable journal, commits atomically where possible, and recovers to a defined state after interruption. Do not permit a recipe to inject arbitrary commands into the package manager. Service triggers and configuration merges need explicit, sandboxed policy.

### Repository and trust services — deku-signing, deku-infra, deku-mirrors
Use TUF-inspired roles for root/targets/snapshot/timestamp metadata, with protected root keys, expiry, rotation/revocation and rollback/freeze protections. Mirrors serve bytes but clients verify freshness metadata regardless of mirror trust. Keep private keys out of Git, image builders and PR jobs. Use reviewed signing software, not custom crypto.

### System composition and profiles — deku-system, deku-profiles
Declarative profile manifests resolve exact package identities, recipe revisions, ABI, architecture and boot policy. They do not embed shell. The composer validates manifests and produces inventory. Image assembly is a downstream consumer and is paused until the package path works end to end.

### Installation and recovery — deku-installer
Evaluate Anaconda as upstream source code, not as a Fedora base. Decide between a GPL-compatible Anaconda-derived installer and a new Deku UX around selected backend APIs. Keep storage, package deployment, boot configuration and recovery behind explicit interfaces so the UI and package format can change independently. No physical disk writes until there is dry-run preview, second confirmation and disposable virtual-disk integration testing.

### Release and updates — deku-release, deku-updater
A release manifest binds source commits, recipe/profile revisions, builder/toolchain identities, package digests, SBOM, provenance, tests, limitations and signed metadata. Updates authenticate repository metadata and protect against rollback; the updater activates only recoverable package transactions or the selected image/generation mechanism.

## 5. Strategic decisions

- Distribution goal: independent long-term; no Fedora-derived distribution as the product strategy. Selective source reuse is allowed under its license.
- ABI: choose one after building representative packages. Do not promise glibc and musl until both have real build/test coverage; ABI belongs in package identity.
- System root: compare generation-based profiles and image-based OSTree/bootc in a short ADR. Select one owner for activation and rollback.
- Boot stack: use maintained upstream Linux, service manager, initramfs and bootloader components until a measured requirement justifies a patch. Do not fork them in advance.
- Installer: substantial Anaconda reuse requires GPL-compatible terms and dependency audit.
- No ISO priority: keep ISO orchestration disabled; focus on package tooling, build workers, repository trust, profiles and installer engine.

## 6. Ordered milestones and exit gates

### M0 — governance and source reuse
Keep main/dev as the only persistent branches. Pin external Actions by full commit SHA. Record upstream source/license inventory and an owner for each critical component.
**Exit:** component roles, licenses and maintainers are clear; no active workflow contradicts the infrastructure-first direction.

### M1 — first end-to-end package (no image)
Complete one small package from immutable source. Build it in a disposable worker without secrets/network during compilation. Produce package manifest, artifact digest, logs and provenance. Rebuild independently and compare output or document nondeterminism.
**Exit:** outputs reproduce from pinned inputs or the variance is explained and policy-approved.

### M2 — repository trust
Generate canonical target metadata, sign with a test key separated from production credentials, and verify with a clean client. Test expiry, wrong key, tampered digest, rollback, missing target and key rotation.
**Exit:** all negative tests fail closed; no checksum-only trust claim.

### M3 — safe install transactions
Install to a temporary root first, never host /. Implement file ownership DB, collision detection, symlink/path safety, durable journal, interrupted recovery and uninstall ownership checks. Inject disk-full, corrupt archive, permission and shared-file failures.
**Exit:** fault-injection tests pass without modifying the host.

### M4 — native system root and installer
Select package-vs-image root semantics using an ADR. Integrate storage planning, boot configuration and package deployment. Run end-to-end installs only in disposable UEFI VMs and virtual disks.
**Exit:** install, reboot, update, rollback and recovery are tested. Only then revisit ISO production.

### M5 — release operations
Generate standards-based SBOM/provenance and signed release manifest; publish sources/patches/attribution and known limitations. Document key rotation, recovery, security response, backups and mirror freshness.
**Exit:** an independent maintainer can verify and reproduce release evidence without trusting the builder.

## 7. Immediate implementation tasks

1. Keep the Fedora ISO workflow disabled and correct all documents that described its failed boot test as success.
2. Replace installer documentation that treats Anaconda as an unexamined candidate with a concrete source/license and backend/UI decision.
3. Add a Rust transaction state machine to deku-pkg-core before privileged file installation.
4. Strengthen recipes to declare patches, dependency classes, outputs and build settings.
5. Make deku-build emit a typed result/provenance document before running arbitrary build commands.
6. Add negative tests for signatures, hostile archive paths, interrupted installs and network isolation.
