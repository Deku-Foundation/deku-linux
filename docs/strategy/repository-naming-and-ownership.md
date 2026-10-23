# Repository naming and ownership

- **Status:** Proposed
- **Date:** 2026-10-23

Repository names should identify Deku components and their responsibilities. They should not expose temporary research directions or imply that Deku is a fork of another distribution.

## Proposed canonical names

| Purpose | Proposed repository | Notes |
|---|---|---|
| Project decisions, roadmap, architecture and governance | `deku-linux` | Current repository is `project`; rename requires an organization-level GitHub operation |
| Native package manager and repository client | `deku-pkg` | Create when the first code prototype exists |
| Package recipes and maintained patches | `deku-recipes` | Separate from the package-manager implementation |
| Isolated package and image builds | `deku-build` | Current repository is `build-system`; rename requires an organization-level GitHub operation |
| System configuration and first-boot integration | `deku-system` | Create when code exists to maintain |
| Installer and live environment | `deku-installer` | Defer until a bootable image exists |
| Release signing, mirrors and operational tooling | `deku-infra` | Current repository is `infrastructure`; rename requires an organization-level GitHub operation |
| Public website | `deku-linux.github.io` or current organization Pages repository | Keep the public domain stable; changing the repo name may affect Pages configuration |

## Naming rules

- Use lowercase kebab-case.
- One repository should have one clear owner and purpose.
- Do not create empty repositories to reserve names.
- Do not put the package manager and all package recipes in one repository once their review and release cycles differ.
- Keep generated binaries and ISO images out of ordinary Git history.
- Do not create a kernel-source fork just to hold a configuration. Store Deku's kernel configuration, package recipe, patches, and test results in the appropriate Deku repository until a separately maintained patch queue justifies a split.
- Repository renames and transfers must be performed through GitHub, then verified for redirects, Actions, Pages, branch protections, and workflow permissions. Do not assume an API-connected documentation change renamed the actual repository.

## Current repository status

The organization currently has `project`, `packages`, `build-system`, `infrastructure`, and `Deku-Foundation.github.io`. This document proposes future names; it does not claim that these repositories have been renamed or that proposed repositories already exist.
