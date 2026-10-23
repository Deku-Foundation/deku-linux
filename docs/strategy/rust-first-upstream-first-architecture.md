# Deku OS Architecture Strategy: Upstream First, Rust-Controlled

- Status: proposed architecture for review, not an implemented system.
- Date: 2026-10-23
- Scope: first x86_64 UEFI bootable prototype and a path to an independent distribution.

## Executive summary

Deku should not rewrite the Linux kernel, libc, desktop environment, service manager, compiler toolchain or installer merely to claim that the distribution is Rust-based. The credible goal is a **Rust-first distribution control plane**: package metadata and tooling, dependency planning, build orchestration, profile validation, image manifests, update policy, verification and release tooling are developed in Rust where the language materially improves safety and maintainability. Mature upstream system components remain upstream, with explicit version pins, configuration, tests and documented patches.

The strategy combines proven ideas rather than copying three distributions wholesale:

- **Void Linux:** simple source recipes, XBPS's clear package/repository boundaries, unprivileged package builds, explicit glibc/musl trade-offs.
- **Nix/NixOS:** declarative system profiles, immutable input references, isolated derivations, content-addressed thinking, generations/rollback and reproducibility checks.
- **Fedora:** strong integration testing, kernel/firmware coverage, SELinux-aware security posture, documented release engineering, and mature installer/image practices.
- **systemd/mkosi and upstream image tools:** reuse an existing image builder for the first technical proof where compatible; do not invent ISO authoring before a tested requirement exists.
- **Rust ecosystem:** workspace-based tooling, typed schemas, explicit error handling, fuzz/property tests and a conservative dependency policy.

## Architectural principles

1. **Upstream first, own only the differentiating layer.** Track upstream source and licenses; patch narrowly and submit fixes upstream where possible.
2. **Rust for new privileged or security-sensitive control-plane code.** Keep privileged operations small, auditable and isolated. A Rust implementation is not automatically secure; tests, threat modelling and operational boundaries remain mandatory.
3. **Declarative inputs, explicit outputs.** A profile and lock/manifest identify every package, source revision, patch, toolchain, configuration, builder and output digest.
4. **No untrusted build as root.** Package compilation must run in disposable, unprivileged, resource-limited workers. Network access should be denied during the build phase unless a documented exception is required.
5. **Reproducibility is measured, not claimed.** Compare independent rebuilds and investigate nondeterminism. A digest identifies bytes but does not authenticate a publisher.
6. **Repository, build, signing and publishing are separate trust domains.** Never expose release signing credentials to pull-request or package build jobs.
7. **Safe rollback and recovery before convenience.** Package transactions and OS updates must have explicit state machines, interruption handling and recovery tests.
8. **Compatibility is a release feature.** Define ABI, package format, upgrade policy, supported architectures and deprecation windows before stable releases.
9. **Small milestones and real evidence.** A metadata validator is not a package builder; a successful image build is not proof of boot; a VM boot is not proof of hardware compatibility.
10. **Open governance.** Architecture decisions, threat models, test results, known limitations and upstream attributions remain public.

## Recommended system shape

### Stage A — Bootable proof, not yet an independent release

Use a pinned, mature upstream base and a supported image builder to demonstrate UEFI x86_64 boot, root filesystem composition, initramfs, console login and automated QEMU tests. The initial proof can use an upstream package manager because Deku's native package manager and recipes are not production-ready. Label the result explicitly as a technology preview, not as an independent production distribution.

Evaluate `systemd/mkosi` first because it can build customized images from several existing package ecosystems and can boot images in QEMU. Confirm host requirements, license, package source availability and whether the desired base is supported before adopting it. If the chosen base is Void, use Void's own supported `void-mklive`/XBPS path rather than forcing it into an incompatible image tool.

### Stage B — Native Rust package and build path

Integrate the existing repositories into one end-to-end path:
- `deku-recipes`: reviewed recipe schema, source URL + immutable revision + digest, license expression, patches, dependencies and build environment.
- `deku-build`: Rust CLI/orchestrator, canonical build plan, worker protocol, sandbox adapter, bounded logs, resource limits, artifact manifest and provenance.
- `deku-pkg`: Rust package format/client core, dependency solver, repository metadata verification, download integrity, staged installation and recoverable transactions.
- `deku-system`: profile resolver, rootfs composition, initramfs/boot configuration integration, image manifest and image-builder adapter.
- `deku-profiles`: maintained system/desktop profiles and package selections, created as a separate repo because it now exists; keep the first profile minimal and versioned.
- `deku-tests`: cross-repository integration contracts, disposable-VM boot tests, update/rollback and installer tests. Keep component unit tests beside each implementation.
- `deku-infra`: CI trust boundaries, cache/artifact retention, least-privilege publishing and operational docs.
- `deku-signing`: key policy, signed repository metadata and release attestation design; signing keys remain external to Git and build runners.
- `deku-release`: release manifests, checksums, SBOM/provenance validation and publication workflow.
- `deku-updater`: later client-side update orchestration after repository trust and package transactions are proven.
- `deku-kernel`: track upstream kernel source/configuration/patches only when there is a real maintained patch queue; do not fork or rewrite Linux just to use Rust.
- `deku-desktop` / `deku-themes`: integration and branding configuration around upstream KDE components; not a reason to fork Plasma.
- `deku-mirrors`: mirror policy/health metadata after a real package repository exists.
- `deku-rukn`: independent Arabic-first Rust language project; not a prerequisite for the OS image.

### Stage C — Independent, signed distribution

Promote from the upstream-base proof only when Deku can build and verify a minimal package set, generate a trusted repository index, install packages with safe transactions, compose the root filesystem, boot it in CI, and rebuild the critical artifacts independently. Then choose a long-term base/libc/init/kernel/update model by ADR and migrate package-by-package. A self-hosting compiler/language is a separate long-term research goal, not a condition for the first ISO.

## Decisions that must be recorded before the prototype becomes a release

- Base strategy: upstream-base technology preview versus independent bootstrap. Recommended: upstream-base proof first, independent distribution as a later gate.
- Initial target: x86_64 UEFI only.
- libc: choose one initial ABI (glibc is the pragmatic compatibility default; musl can be a separately tested future target). Void shows that dual libc support is possible but requires real build/test coverage and has proprietary-driver compatibility consequences.
- Init/service manager and initramfs: evaluate maintained upstream components; decide together with the base and image builder.
- Package/update model: initially use the upstream manager for the proof image; do not pretend `deku-pkg` can install systems yet. Design Deku's native manager around signed repository metadata, content integrity, transactional staging and rollback.
- Image tool: proof-of-concept with mkosi if compatible; compare against the chosen base's native live-image tooling.
- Desktop: KDE Plasma x86_64 profile, initially only if image size, graphics and VM test capacity are practical.
- Security: Secure Boot scope, signing identity, key rotation/revocation, SBOM/provenance, vulnerability response and supported update lifetime.
- License and trademark review for every reused upstream component and artwork.

## Rust implementation standards

- Use a Cargo workspace only where crates share release/test ownership; avoid splitting every module into its own repository.
- Pin the Rust toolchain and dependency graph; commit `Cargo.lock` for applications and build tools.
- Enable formatting, clippy and tests in CI; use `cargo-deny` or an equivalent review process for licenses, advisories and duplicate dependencies.
- Use fuzzing/property tests for parsers, package archives, manifests and transaction state machines.
- Bound all untrusted input sizes, nesting, path lengths, archive entries and decompression ratios.
- Use safe Rust by default; any `unsafe` requires a documented safety argument and targeted tests.
- Avoid custom cryptography. Use reviewed libraries and standard signature formats/protocols.
- Use capability-limited workers and explicit filesystem/network boundaries; do not assume a Rust process alone is a sandbox.

## First milestone acceptance criteria

A first prototype is complete only when CI:
1. Resolves a pinned profile and creates a complete manifest.
2. Builds or retrieves only pinned inputs and records their hashes.
3. Produces an ISO and checksum from a documented command in a clean environment.
4. Boots the ISO under QEMU with UEFI and reaches a declared userspace target.
5. Runs smoke checks for root mount, init/service status, console login and expected profile marker.
6. Stores logs, builder versions, commit IDs, manifest and artifact digests.
7. Fails on missing inputs, changed digests, unpinned versions or boot-test failure.

The first milestone does not claim: production hardware support, stable updates, secure boot, a production installer, a signed package repository, complete reproducibility or an independently bootstrapped system.

## Branch and promotion policy

Keep `main` and `dev` as the only persistent branches. Commit changes on `dev`; promote to `main` after tests and review. Do not use force pushes or delete either persistent branch. Use temporary pull-request branches only where review/CI requires them and clean them up after merge.
