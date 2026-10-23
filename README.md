# Deku Linux

Deku Linux is a proposed independent, free and open-source Linux distribution focused on security, maintainability, coherent integration, and a polished user experience.

> **Status: early planning.** Deku Linux is not yet a usable distribution. No release, package repository, installer, security certification, or reproducible build is claimed.

## Goals

- Maintainable engineering and transparent decisions.
- Security and software supply-chain integrity by design.
- A coherent desktop experience that does not hide system behavior.
- Upstream collaboration, documented changes, automated checks, and repeatable builds.
- An accessible project for contributors and users.

## Initial scope

The initial target is x86_64. Decisions about libc, init system, kernel policy, package manager, release model, desktop environment, and build infrastructure must be documented in Architecture Decision Records (ADRs) before becoming commitments.

## Principles

1. Security by design: least privilege, signed artifacts, responsible vulnerability handling, and timely updates.
2. Transparency: traceable changes, documented limitations, and evidence-based claims.
3. Upstream first: reuse maintained components where practical and avoid unnecessary forks.
4. Reproducibility: work toward verifiable, repeatable package and image builds.
5. Quality gates: review and test changes proportionally to risk.
6. Sustainable scope: deliver a small, testable foundation before expanding features.

## Repository map

- `docs/architecture/` — architecture principles and constraints.
- `docs/adr/` — Architecture Decision Records.
- `docs/roadmap.md` — staged milestones and exit criteria.
- `CONTRIBUTING.md` — contribution workflow.
- `SECURITY.md` — vulnerability reporting policy.
- `.github/` — issue and pull-request templates.

## Repository map

The organization is moving toward purpose-specific Deku-named repositories. The current intended ownership map is documented in [`docs/strategy/repository-layout-and-migration.md`](docs/strategy/repository-layout-and-migration.md). Existing repository names and links should be updated in focused pull requests; repository renames, forks, and transfers must be performed by an organization owner through GitHub settings when the available tooling cannot perform them safely.

## Current milestone

Establish governance and make critical architecture decisions before attempting a bootable image. Package provenance, build isolation, signing, updates, and recovery must be designed and reviewed early.

## Language

English is canonical for technical source files and project decisions. Arabic translations may be added alongside canonical documents. Keep identifiers, commands, and file paths unchanged in translations.

## License

The repository's current license applies to its files as stated in `LICENSE`. License choices for future code, packaging metadata, artwork, and trademarks may differ and must be explicit.
