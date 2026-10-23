# ADR-0002: System Updates, Root Ownership and Rollback Model

- Status: Proposed evaluation plan; no production update architecture has been selected.
- Date: 2026-10-23
- Scope: future installed Deku systems, not the existing Fedora-based live preview.

## Context

Deku needs a coherent security/update story across packages, kernel, boot artifacts and user configuration. The projects we study solve different problems: Nix generations are tied to NixOS configuration and store semantics; OSTree deploys immutable filesystem trees and can complement a package manager; bootc uses OCI-style container images to manage an OS deployment; systemd-sysupdate provides A/B transfer/update mechanics but is currently marked experimental upstream. These are not interchangeable libraries that should be stacked indiscriminately.

## Problem statement

A single operation must own activation and recovery for system-critical paths such as the root tree, /usr, kernel/initramfs and bootloader entries. Overlapping mutators can leave the system in states that are difficult to recover and test. Deku must not introduce a native updater until it can prove transaction recovery, publisher authentication and compatibility policy.

## Options to prototype

### A. Generation-based system (Nix-style semantics)

Represent a complete system as an immutable generation, keep previous bootable generations, and change the active generation as a small activation step. Measure the costs of generation garbage collection, /etc configuration merging, space use, bootloader integration, package ABI policy and recovery.

This is a reference pattern, not a proposal to import NixOS internals into a Fedora root filesystem. Using a Nix-managed root would be a major architecture choice and would need a separate ADR.

### B. Immutable filesystem-tree deployments (OSTree; evaluate bootc separately)

OSTree manages content-addressed filesystem trees and atomic deployments. Upstream explicitly describes it as an operating-system upgrade system, not a package manager; it can be combined with a package manager when composition and mutation boundaries are clear. bootc is a different, OCI/image-oriented operating-system workflow, and its fit depends on the distribution package/build model and registry trust requirements.

Evaluate whether an OSTree-derived deploy model or a bootc/RPM image model meets Deku's long-term rootfs, package customization, storage and hardware goals. Do not treat a successful Fedora boot ISO as evidence that bootc is already integrated.

### C. A/B resource updates (systemd-sysupdate)

Prototype only in disposable VMs for kernel/initramfs or complete image partitions. The current upstream manual marks systemd-sysupdate experimental; it must not be the default production updater solely because it is available with systemd. Evaluate partial downloads, activation ordering, rollback, disk exhaustion, version pinning and signature checks.

### D. Transactional native package manager

Deku's native package manager could own package installation and upgrades after it has authenticated metadata, verifies all package bytes, stages changes out of the live system, handles dependency conflicts and interruption, and can restore the prior state. That alone does not solve bootable root-tree updates, kernel slots or recovery; those interfaces must be explicitly assigned.

## Evaluation matrix

Before selecting an option, build the same tiny proof system in disposable QEMU with the same kernel, base package set and console marker, then inject failures at controlled checkpoints.

| Requirement | Required test evidence |
|---|---|
| Power loss / process kill | Interrupt download, unpack, deployment and activation; the system returns to old or new valid state, never a mixed state |
| Rollback | Boot previous generation/image, verify its package manifest and prove user data policy |
| Bootloader integration | Kernel, initramfs and root image references stay consistent across update and rollback |
| Repository trust | Reject unsigned, expired, wrong-role, rollback and digest-mismatched metadata using an established trust framework |
| /etc and mutable data | Document merge/conflict policy; do not overwrite user data silently |
| Storage pressure | Fail safely when there is not enough room to stage the next version or preserve rollback |
| ABI / package compatibility | Define what can be layered onto the base and what requires a complete image update |
| Reproducibility / provenance | Record exact inputs and builder identity; compare independent builds before making reproducibility claims |
| Maintainability | Count custom privileged code, upstream delta, operating modes, recovery paths and required specialist knowledge |

## Provisional guidance

1. Keep the current Fedora 44/Lorax path as an experimental ISO demonstration; do not mix Nix, Void/XBPS and Fedora package databases in a single root.
2. Keep deku-pkg focused on package metadata and safe transaction primitives; it is not yet a system image updater.
3. Prototype OSTree/bootc and Nix-style generations as alternative system-deployment tracks only after the minimal UEFI image and package inventory tests are stable. Treat systemd-sysupdate as an experimental comparison.
4. Select exactly one owner for activation/rollback of the system root. A package manager may cooperate with that owner, but must not independently mutate files it does not own.
5. Use Update Framework (TUF) concepts for repository metadata trust, including separated Root/Targets/Snapshot/Timestamp roles, threshold signing, expiry and key rotation. Use a reviewed implementation rather than creating a new cryptographic protocol.
6. Do not publish a stable update design until interrupted updates, rollback and key-revocation tests pass in disposable VMs and the release artifact has verifiable provenance.

## Upstream references

- OSTree overview and its relationship to package managers: https://ostreedev.github.io/ostree/introduction/
- bootc: https://bootc-dev.github.io/bootc/
- systemd-sysupdate manual (explicitly experimental): https://freedesktop.org/software/systemd/man/latest/systemd-sysupdate.html
- NixOS manual and generation model: https://nixos.org/manual/nixos/stable/
- TUF metadata roles and signature thresholds: https://theupdateframework.io/docs/metadata/
- SLSA provenance and isolation requirements: https://slsa.dev/spec/v1.0/requirements
