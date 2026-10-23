# Native Deku Distribution Architecture

- **Status:** Proposed architecture for review; not an accepted release contract yet.
- **Date:** 2026-10-23
- **Scope:** First independent x86_64 UEFI system and the Rust-owned control plane.
- **Non-goal:** Rebranding or shipping another distribution's root filesystem.

## Decision statement

Deku's target is an independently composed Linux distribution. Fedora, Void and Nix are engineering references and possible sources of reusable upstream components; none is the runtime base distribution. The existing Fedora 44/Lorax image is retained only as a labelled boot-harness fixture. It must not be promoted into a Deku release or used as evidence that the native package stack works.

Independence means Deku owns its package metadata and recipes, build policy, package/repository trust, system profile, root filesystem composition, release process and integration tests. It does not mean rewriting the Linux kernel, libc, compiler, init system or desktop stack in Rust. Upstream components may be used as unmodified dependencies when their licences, maintenance and compatibility are acceptable.

## Proposed first platform

These are proposals for the first engineering target, not final compatibility promises:

- Architecture: x86_64.
- Firmware: UEFI first; BIOS and Secure Boot are separate acceptance targets.
- Kernel: upstream Linux, pinned source and configuration; keep local patches minimal and reviewable.
- Userspace ABI: glibc as the initial compatibility default, subject to a documented ADR; keep musl as a future profile rather than mixing ABIs in one root.
- Init/service management: systemd as the initial integration target, subject to explicit review. Rust does not require replacing mature service-management components.
- Package and build control plane: Rust.
- Desktop: deferred until a native console system boots and survives update/recovery tests.
- Initial image: minimal console image assembled from Deku's own package manifest and rootfs, not copied from a Fedora/Void/NixOS installation.
- Updates: choose one transaction owner only after comparing generation-based rootfs and image-based OSTree/bootc approaches. Do not layer two competing managers over the same system root.

## What to reuse from upstream

| Reference | Reuse or learn from | Do not inherit by accident |
|---|---|---|
| Void void-packages / xbps-src | Recipe phases, build options, clean build roots, cross-build boundaries, local repository workflow and signature/integrity concepts | XBPS package semantics or Void's service/libc defaults without an explicit compatibility decision |
| Nix / Nixpkgs | Declarative inputs, pinned dependency graphs, isolated build concepts, cache addressing and independent rebuild comparison | NixOS module/rootfs assumptions as an undeclared runtime base |
| Fedora RPM / Lorax / Anaconda | RPM metadata and image-builder implementation details, installer test patterns, kernel/initramfs integration lessons | Fedora release repositories or Fedora's resolved package set as Deku's runtime payload |
| systemd mkosi | Image assembly, image layouts, tools trees and image-safety checks; investigate its custom/prebuilt-rootfs boundary | Treating mkosi as a package manager or proof of a native Deku rootfs |
| TUF (tough Rust implementation) | Standardized signed metadata, expiry/version checks and target verification | A home-grown signature protocol or trust-on-first-use from the same untrusted repository |
| SLSA / in-toto / SPDX or CycloneDX | Provenance, attestation and machine-readable component inventories | Claims of supply-chain security based only on a checksum |

Upstream projects are not interchangeable layers. Do not combine Fedora RPM, Void XBPS and Nix store semantics in one root filesystem. Select one native package contract and make compatibility importers explicit, optional and out of the critical path.

## Native package contract — minimum viable scope

1. Recipe source: reviewed metadata with immutable source revision, cryptographic source digest, licence expression, patch set, architecture and explicit build/runtime dependencies.
2. Fetch phase: verify source content before extraction; restrict redirects and network destinations; defend against path traversal, archive symlinks/hardlinks, decompression bombs and DNS/IP rebinding.
3. Build phase: disposable unprivileged worker, resource/time/disk limits, no secrets, no network during compilation by default, pinned toolchain and declared environment. A plan validator is not a sandbox.
4. Package artifact: deterministic metadata, payload file manifest, ownership/mode policy, symlink validation, dependency ABI requirements, digest and provenance reference.
5. Repository: TUF-style authenticated metadata with trusted root distributed out-of-band, expiry/freshness, rollback protection, root rotation/revocation and bounded metadata. SHA-256 alone is not publisher authentication.
6. Client: unprivileged query/plan operations; no package scripts as root; validate paths and conflicts; stage changes; journal transactions; recover safely after power loss before any production installation.
7. System composition: exact package closure and hashes, kernel/initramfs/firmware/bootloader manifest, deterministic rootfs assembly, first-boot identity reset and no accidental builder secrets.
8. Release: SPDX or CycloneDX SBOM, build provenance, checksums, signatures, boot/install/recovery evidence and explicit known limitations.

## Architecture boundaries and ownership

- deku-recipes: recipe schema, review policy, source pins and patch references.
- deku-build: Rust validation/orchestration and, later, the actual isolated worker; no signing credentials.
- deku-pkg: native package format, dependency solving, TUF client integration and eventually transactional installation.
- deku-system: profile, locked package closure, rootfs assembly, kernel/initramfs/boot integration and image-builder adapter.
- deku-installer: only after the rootfs and package transaction contract stabilise; VM-only destructive-operation tests first.
- deku-signing: trust policy and signing workflow design; private keys stay outside source and build workers.
- deku-release: release manifest schema and promotion checks.
- deku-tests: shared contract tests, VM boot/health, install, upgrade, rollback and recovery.
- deku-infra: CI, artifact retention, publication, backups and incident response.

No new repository is needed for this architecture.

## Milestones and exit gates

### M0 — Freeze the contract

Publish and review the platform ADRs: ABI/libc, init/service manager, package format, repository trust, root ownership/update model, boot mode, licence policy and supported architecture. Record dissent and rejected alternatives.

### M1 — Build one native package safely

Create a harmless, tiny package from a pinned source using a real disposable unprivileged worker. Verify the produced payload, metadata, licence, hashes and provenance. Test malicious archives, path traversal, network denial, timeout, disk exhaustion and worker cleanup.

Exit: repeated clean builds produce matching package payloads or documented differences; the worker cannot modify host paths or access secrets.

### M2 — Authenticate a local package repository

Build a disposable local TUF test repository, bootstrap trust out-of-band, install metadata into persistent protected state, and test expiry, rollback, wrong keys, key rotation, revocation and tampered targets. Test network failure and stale metadata.

Exit: every negative trust test fails closed; no package is installed based on a bare digest or unauthenticated metadata.

### M3 — Assemble a native minimal rootfs

Resolve a locked closure from Deku packages, plus only explicitly declared upstream binary/source components. Build a rootfs without invoking a foreign distribution installer or inheriting its package database. Generate /etc/deku-release, package inventory, licence inventory, SBOM and provenance. Include a pinned upstream Linux kernel, initramfs and boot chain.

Exit: the manifest explains every installed file and package; no unreviewed foreign distro package manager/repository is required at runtime.

### M4 — Build and boot a native ISO

Use an image assembler only at the media/layout boundary. Evaluate mkosi with a prebuilt/custom rootfs, or a small dedicated ISO-layout adapter if it cannot satisfy requirements. Run two clean builds and test UEFI/QEMU boot, root mount, systemd health, console/login, networking, shutdown and failure diagnostics.

Exit: a native Deku rootfs boots and all required VM acceptance tests pass. A serial marker alone is insufficient.

### M5 — Installation, update and recovery

Install only to disposable VM disks; test partition planning, interruption, upgrade, rollback and recovery. Hardware and Secure Boot support are separate declared targets.

### M6 — Release candidate

Publish only after independent review of SBOM, provenance, signatures, reproducibility evidence, vulnerability triage, licensing, install/recovery tests and release manifest.

## Explicitly rejected shortcuts

- Do not promote the existing Fedora-based ISO as an independent Deku release.
- Do not combine three package managers in one root filesystem.
- Do not write a custom cryptographic format when a maintained standard implementation fits.
- Do not execute recipe-supplied shell commands in the validator or with host privileges.
- Do not call a build reproducible until independent builds have been compared.
- Do not add a desktop, installer, updater or custom kernel before the minimal native console system is proven.
- Do not interpret passing CI or the existence of a repository as production implementation.
