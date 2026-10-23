# Repository naming and ownership

- **Status:** Current inventory and responsibility map
- **Last reviewed:** 2026-10-23

The organization has standardized the primary component repositories around Deku-owned names. This document records the repositories that exist today and distinguishes a repository's current prototype from its intended long-term responsibility.

## Current repository map

| Responsibility | Repository | Current status |
|---|---|---|
| Project direction, architecture decisions, roadmap and contribution/security policy | [deku-linux](https://github.com/Deku-Foundation/deku-linux) | Planning and engineering proposals; no release image |
| Native package metadata, dependency planning and artifact verification | [deku-pkg](https://github.com/Deku-Foundation/deku-pkg) | Python and Rust prototypes; no production installation or repository client |
| Package recipes and source metadata | [deku-recipes](https://github.com/Deku-Foundation/deku-recipes) | Metadata schema and validation; no source build execution |
| Build-plan validation and future isolated build workers | [deku-build](https://github.com/Deku-Foundation/deku-build) | Python reference plus Rust validation CLI; no build sandbox or artifact pipeline |
| System composition and image assembly | [deku-system](https://github.com/Deku-Foundation/deku-system) | Fedora 44/Lorax technology-preview ISO successfully built and passed one UEFI/QEMU serial-marker test; latest profile/toolchain revision is being retested |
| Installation plan validation and future installer | [deku-installer](https://github.com/Deku-Foundation/deku-installer) | Non-destructive plan prototype; no disk writes or installation execution |
| Public infrastructure and operational security documentation | [deku-infra](https://github.com/Deku-Foundation/deku-infra) | Bootstrap documentation; no production release infrastructure |
| Public website and GitHub Pages workflow | [Deku-Foundation.github.io](https://github.com/Deku-Foundation/Deku-Foundation.github.io) | Static multilingual site; no supported ISO or release download |
| Declarative system and desktop profiles | [deku-profiles](https://github.com/Deku-Foundation/deku-profiles) | Fedora 44 canonical profile restored after Fedora 45 media returned HTTP 404; latest profile contract checks pass |
| Cross-project integration and VM acceptance tests | [deku-tests](https://github.com/Deku-Foundation/deku-tests) | QEMU/UEFI serial-marker harness passed against one Fedora 44 technology-preview ISO; wider runtime and hardware testing remain open |
| Release manifests and artifact promotion | [deku-release](https://github.com/Deku-Foundation/deku-release) | Manifest and promotion contract only; no release pipeline |
| Repository/release trust policy and verification | [deku-signing](https://github.com/Deku-Foundation/deku-signing) | Trust-model proposal; no production keys or signing service |
| System update client | [deku-updater](https://github.com/Deku-Foundation/deku-updater) | Future component; no updater implementation |
| Kernel configuration and narrow patch queue | [deku-kernel](https://github.com/Deku-Foundation/deku-kernel) | Upstream tracking scope only; not a kernel fork/build service |
| KDE Plasma integration and defaults | [deku-desktop](https://github.com/Deku-Foundation/deku-desktop) | Bootstrap stage; no supported desktop image |
| Theme and visual assets | [deku-themes](https://github.com/Deku-Foundation/deku-themes) | Bootstrap stage; licenses and attribution required for every asset |
| Mirror policy and future synchronization | [deku-mirrors](https://github.com/Deku-Foundation/deku-mirrors) | Planning only; no production mirror service |
| Arabic-first Rust language/toolchain | [deku-rukn](https://github.com/Deku-Foundation/deku-rukn) | Separate experimental language project; not an ISO dependency |
| Organization profile and shared guidance | [.github](https://github.com/Deku-Foundation/.github) | Organization metadata, not an OS component |

## ISO roadmap and repository gaps

See [ISO build gap analysis](iso-build-gap-analysis.md) for the upstream tooling comparison, architecture decisions, the first successful boot evidence and the remaining acceptance gates. The organization already has the required repository boundaries; do not add more. Build and test the actual integration before describing a subsystem as implemented.

## Ownership boundaries

- Keep recipes separate from the package-manager implementation so source review and client releases can follow different lifecycles.
- Keep build execution separate from package installation and repository signing. Build workers must not hold release-signing credentials.
- Keep system composition separate from installer interaction; an image manifest must not become an implicit shell script.
- Keep the website static until a generator or documentation framework demonstrates a measurable maintenance benefit.
- Do not create empty repositories merely to reserve names. Split components only when separate ownership, release cadence or security boundaries justify the cost.

## Naming and change control

- Use lowercase kebab-case for component repositories; retain the organization Pages repository name required by GitHub Pages.
- A repository rename or transfer is an organization-level GitHub operation, not a documentation edit. After any future rename, verify redirects, Actions, Pages, branch protection, webhook configuration and workflow permissions.
- Keep generated binaries and ISO images out of ordinary Git history.
- Do not fork the Linux kernel or an upstream package ecosystem solely to hold local configuration. Store Deku's configuration, recipes, patches and test evidence in the appropriate repository unless a separately maintained patch queue justifies a split.

## Branch hygiene

- Keep `main` and `dev` as the only persistent development branches in each active repository.
- Develop on `dev`; promote changes to `main` only after required CI checks, review, and relevant integration/VM tests pass.
- Avoid persistent feature branches. Use a short-lived PR branch only when a review or CI workflow genuinely requires it, then remove it after merge.
- Protect `main` from direct pushes where GitHub settings permit. Keep `dev` testable and periodically synchronize it with `main` after promotions.
- Never delete or force-update `main` or `dev`. Remove obsolete topic branches only after confirming they contain no unique unmerged work and are not used by an open PR or deployment.

## What this inventory does not claim

The existence of a repository does not mean its intended production service is implemented. The package manager, build workers, repository signing service, installer, system image builder and release infrastructure remain prototypes or planned work until their own acceptance gates pass.
