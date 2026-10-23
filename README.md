# Deku Linux

Deku Linux is an independent, free and open-source Linux distribution in its foundation and prototype stage. The project prioritizes maintainability, a coherent desktop experience, transparent engineering decisions and explicit software-supply-chain trust boundaries.

> **Status:** no public ISO, supported release, production package repository, production installer, or reproducible system-image pipeline is available. Component repositories contain prototypes and proposals; they do not yet constitute an installable distribution.

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
- [deku-build](https://github.com/Deku-Foundation/deku-build) — bounded build-plan validation; no isolated build worker.
- [deku-system](https://github.com/Deku-Foundation/deku-system) — system manifest validation; no root filesystem or image assembly.
- [deku-installer](https://github.com/Deku-Foundation/deku-installer) — non-destructive installation-plan validation; no disk-writing operations.
- [deku-infra](https://github.com/Deku-Foundation/deku-infra) — infrastructure and publication guidance; no production release service.
- [Deku-Foundation.github.io](https://github.com/Deku-Foundation/Deku-Foundation.github.io) — static English, French and Arabic website.
- deku-linux — project direction, architecture decisions, roadmap, contribution and security policy.

## Architecture decisions

The current proposal is [ADR-0001: First ISO and Rust-first architecture](docs/adr/0001-first-iso-and-rust-first-architecture.md). It separates a real upstream-based technology-preview ISO from the later goal of an independent Deku distribution, and defines what must be proven before any release claim.

## Current milestone

See [ISO roadmap and repository gaps](docs/strategy/iso-build-gap-analysis.md) for the upstream tooling comparison, justified future repository names, architecture decisions and measurable gates toward a first bootable x86_64 prototype. The immediate goal is integration and a VM-verified image, not adding empty repositories.

Make architecture decisions reviewable and strengthen the package/build prototypes before attempting a bootable image. Repository signing, isolated builds, file ownership, transactions, interrupted-update recovery and image creation remain future milestones.

## Language

English is canonical for technical source files and decisions. French and Arabic are supported on the public website. Translations of technical documentation should be reviewed for meaning and terminology; keep identifiers, commands and file paths unchanged.

## License

The repository license applies to files as stated in LICENSE. License choices for future code, package metadata, artwork and trademarks may differ and must be explicit.
