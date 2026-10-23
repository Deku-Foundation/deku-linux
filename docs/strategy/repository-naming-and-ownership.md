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
| Build-plan validation and future isolated build workers | [deku-build](https://github.com/Deku-Foundation/deku-build) | Validation-only prototype; no build sandbox or artifact pipeline |
| System composition manifests and future image assembly | [deku-system](https://github.com/Deku-Foundation/deku-system) | Manifest validation only; no root filesystem or image assembly |
| Installation plan validation and future installer | [deku-installer](https://github.com/Deku-Foundation/deku-installer) | Non-destructive plan prototype; no disk writes or installation execution |
| Public infrastructure and operational security documentation | [deku-infra](https://github.com/Deku-Foundation/deku-infra) | Bootstrap documentation; no production release infrastructure |
| Public website and GitHub Pages workflow | [Deku-Foundation.github.io](https://github.com/Deku-Foundation/Deku-Foundation.github.io) | Static multilingual site; release status remains explicitly pre-release |

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

## What this inventory does not claim

The existence of a repository does not mean its intended production service is implemented. The package manager, build workers, repository signing service, installer, system image builder and release infrastructure remain prototypes or planned work until their own acceptance gates pass.
