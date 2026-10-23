# Deku Linux

Deku Linux is an independent, free and open-source Linux distribution in its foundation and prototype stage. The project prioritizes maintainability, a coherent desktop experience, transparent engineering decisions and explicit software-supply-chain trust boundaries.

> **Status:** No official supported ISO, production package repository or installer is available. An experimental Fedora 44/Lorax ISO has been built and passed one UEFI/QEMU console-marker smoke test ([run 40003527897](https://github.com/Deku-Foundation/deku-system/actions/runs/40003527897), ISO SHA-256: `a5d604ea3964a8a05c7a42b0c515586204e0f5c23a1a5e412fa585649eca5a58`). This is an upstream-based technology preview, not an independent Deku system or production-readiness claim; its Actions artifact is short-lived.


## Goals

- Maintainable engineering and transparent decisions.
- Software-supply-chain integrity designed into source review, builds, repositories and releases.
- A coherent desktop experience that does not hide system behaviour.
- Upstream collaboration, documented changes, automated checks and repeatable builds.
- An accessible project for users and contributors.

## Initial desktop and platform direction

KDE Plasma is the initial desktop direction; GNOME remains a possible later profile, not a current supported edition. The first architecture target is x86_64. The libc, init/service manager, ABI, boot approach and release model require accepted Architecture Decision Records before becoming production commitments.

Kernel 7.3 may be evaluated as an experimental mainline target. The release kernel must be selected from versions that have been tested for boot, hardware support, security updates and recovery. A newer mainline number alone is not a release criterion.

## Principles

1. **Security by design:** least privilege, signed artifacts, responsible vulnerability handling and timely updates.
2. **Transparency:** traceable changes, documented limitations and evidence-based claims.
3. **Upstream first:** reuse maintained components where practical; avoid unnecessary forks.
4. **Reproducibility:** work toward verifiable, repeatable package and image builds.
5. **Quality gates:** review and test changes in proportion to risk.
6. **Sustainable scope:** deliver a small, testable foundation before expanding features.

## Repository map

The active repositories and their actual prototype status are recorded in [repository naming and ownership](docs/strategy/repository-naming-and-ownership.md):

- [deku-pkg](https://github.com/Deku-Foundation/deku-pkg) — Rust package metadata validation, deterministic dependency planning and streamed SHA-256 artifact verification; no production installation, signature trust or transaction engine.
- [deku-recipes](https://github.com/Deku-Foundation/deku-recipes) — strict recipe metadata validation; no recipe execution.
- [deku-build](https://github.com/Deku-Foundation/deku-build) — Python reference and Rust build-plan validation CLI; no isolated package-build worker yet.
- [deku-system](https://github.com/Deku-Foundation/deku-system) — system manifest validation plus an experimental Fedora 44/Lorax ISO pipeline currently being debugged; no accepted bootable Deku ISO yet.
- [deku-installer](https://github.com/Deku-Foundation/deku-installer) — non-destructive installation-plan validation; no disk-writing operations.
- [deku-infra](https://github.com/Deku-Foundation/deku-infra) — infrastructure and publication guidance; no production release service.
- [deku-profiles](https://github.com/Deku-Foundation/deku-profiles) — experimental system-profile specifications; not a verified build input yet.
- [deku-tests](https://github.com/Deku-Foundation/deku-tests) — integration contracts and a disposable QEMU/UEFI boot-smoke harness; no Deku ISO has passed it yet.
- [deku-release](https://github.com/Deku-Foundation/deku-release) — release-manifest and promotion-gate proposal; no release pipeline.
- [deku-signing](https://github.com/Deku-Foundation/deku-signing) — package/release trust model; no production keys or signing service.
- [deku-updater](https://github.com/Deku-Foundation/deku-updater) — future update orchestration; depends on trusted repositories and recoverable package transactions.
- [deku-kernel](https://github.com/Deku-Foundation/deku-kernel) — upstream kernel configuration/patch tracking; not a kernel fork.
- [deku-desktop](https://github.com/Deku-Foundation/deku-desktop) — KDE Plasma integration planning; no supported desktop image.
- [deku-themes](https://github.com/Deku-Foundation/deku-themes) — theme and visual assets with explicit licensing.
- [deku-mirrors](https://github.com/Deku-Foundation/deku-mirrors) — future mirror policy; no production mirror service.
- [deku-rukn](https://github.com/Deku-Foundation/deku-rukn) — separate Arabic-first Rust language/toolchain project, not an ISO prerequisite.
- [Deku-Foundation.github.io](https://github.com/Deku-Foundation/Deku-Foundation.github.io) — static English, French and Arabic website.
- deku-linux — project direction, architecture decisions, roadmap, contribution and security policy.

## Architecture decisions

The current proposal is [ADR-0001: First ISO and Rust-first architecture](docs/adr/0001-first-iso-and-rust-first-architecture.md). It separates a real upstream-based technology-preview ISO from the later goal of an independent Deku distribution, and defines what must be proven before any release claim.

## Current milestone

See [ISO roadmap and repository gaps](docs/strategy/iso-build-gap-analysis.md) for the upstream tooling comparison, the roles of the repositories that now exist, architecture decisions and measurable gates toward a first bootable x86_64 prototype. The immediate goal is to fix the GRUB image-assembly failure, then pass the disposable UEFI boot test—not create more repositories.

Make architecture decisions reviewable and strengthen the package/build prototypes before attempting a bootable image. Repository signing, isolated builds, file ownership, transactions, interrupted-update recovery and image creation remain future milestones.

## Language

English is canonical for technical source files and decisions. French and Arabic are supported on the public website. Translations of technical documentation should be reviewed for meaning and terminology; keep identifiers, commands and file paths unchanged.

## License

The repository license applies to files as stated in LICENSE. License choices for future code, package metadata, artwork and trademarks may differ and must be explicit.
