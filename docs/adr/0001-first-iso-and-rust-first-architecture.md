# ADR-0001: First ISO Strategy and Rust-First Distribution Architecture

- Status: Proposed for implementation as a technology preview
- Date: 2026-10-23
- Decision owners: Deku maintainers
- Scope: first x86_64 UEFI ISO only; not the final distribution base decision

## Context

Deku's current package manager, recipes, build coordinator, system composition and installer are prototypes. None can yet produce and install a complete native system. Rewriting all of them before the first bootable artifact would delay learning and repeat work already solved upstream.

## Decision

1. Build a clearly labelled **technology-preview ISO using a pinned, mature upstream package ecosystem** as the first boot milestone. This is not an independent Deku release.
2. Evaluate Fedora's maintained live-image tooling (Lorax / livemedia-creator) as the first ISO path. Fedora's release tooling and broad hardware/kernel coverage provide a practical reference. Test the exact host requirements and CI feasibility before treating this as selected production infrastructure.
3. Evaluate systemd/mkosi alongside it for disk-image and system-tree integration tests. mkosi creates disk/system images in supported formats; it should not be described as an ISO generator without a verified pipeline that produces the actual ISO.
4. Use Fedora 44 for the current traceable technology-preview experiment. As of 2026-10-23, Fedora 45 had not reached Final; the 2026-10-22 Go/No-Go resulted in another NO-GO and the schedule lists 2026-11-03 as the next target, subject to blockers. See the [Fedora release schedule](https://fedorapeople.org/groups/schedule/f-45/f-45-key-tasks.html) and [Final Go/No-Go meeting](https://calendar.fedoraproject.org/meeting/11450/). Do not switch to Fedora 45 beta or Rawhide just to use a higher version number. Fedora 44 package repositories still move, so this first build is traceable but not yet fully reproducible.
5. First boot target is x86_64 UEFI to a console. KDE Plasma follows after the base image passes repeatable boot tests.
6. Develop Deku's native tooling in Rust: package metadata/client core, dependency planning, build-plan validation/orchestration, profile and manifest validation, image/release metadata verification. Keep Linux kernel, systemd, libc, compilers, desktop components and bootloader upstream unless a measured need justifies a narrow patch.
7. Adopt the useful design patterns, not entire codebases: Void's explicit recipe/build/package boundaries; Nix's declarative inputs, isolation and rebuild comparisons; Fedora's release QA, signing and hardware integration; upstream Rust's safe control-plane tooling.
8. Treat glibc as the initial compatibility baseline for the technology preview. Make musl a separately tested target, not a second ABI promised without package/build coverage.
9. Keep the upstream package manager for the proof ISO. Do not claim the native Deku package manager is production-ready until it can authenticate repository metadata, install packages transactionally, recover from interruption and pass integration tests.
10. Do not ship a physical-disk installer, automatic updater, Secure Boot claim or stable release as part of the first milestone.

## Why not write every component in Rust?

The Linux kernel is primarily C, systemd and major desktop components are established upstream projects, and replacing them would multiply risk without advancing the first ISO. Rust should be used where Deku owns new control-plane logic and memory-safety benefits matter. The distribution can be Rust-first without falsely claiming that every component is Rust.

## Consequences

- The first ISO demonstrates a real boot path but does not prove full independence from Fedora.
- The base and image builder must be replaceable behind a declarative profile and manifest interface.
- The image pipeline records upstream snapshot, toolchain, configuration, package manifest, checksums and test logs.
- The native package path can mature independently and later replace the bootstrap package manager after a migration ADR.
- The image is not published as a release until a disposable UEFI VM reaches the declared target and evidence is retained.

## Acceptance gate

Before implementation is treated as accepted, add a working CI proof that produces a real ISO from pinned inputs, calculates its digest, boots it in disposable x86_64 UEFI QEMU, captures serial logs and fails on missing userspace. If hosted CI cannot provide required virtualization or builder privileges, document and choose a suitable isolated runner rather than weakening the test.
