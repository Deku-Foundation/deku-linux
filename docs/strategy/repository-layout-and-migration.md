# Repository Layout and Migration Plan

**Status:** proposed operational map. This document does not itself rename, fork, transfer, or archive repositories.

## Ownership map

| Repository | Responsibility | Current action |
|---|---|---|
| `deku-linux` | Governance, roadmap, ADRs, shared policies | Canonical project coordination |
| `deku-pkg` | Native package-manager design and implementation | Keep manager code separate from recipes |
| `deku-recipes` | Package recipes, patches, source pins, license/provenance metadata | Bootstrap recipe conventions before adding real packages |
| `deku-build` | Build orchestration, isolation, provenance, artifact validation | Bootstrap pipeline and trust boundaries |
| `deku-system` | Base-system integration, defaults, first boot, service configuration | Do not assume the final init/libc/kernel decisions are accepted |
| `deku-installer` | Installer planning, UI, storage/deployment integration | Prototype remains plan-only until reviewed and tested |
| `deku-infra` | CI operations, Pages, release infrastructure, least-privilege deployment | No production secrets or release signing keys in source |
| `Deku-Foundation.github.io` | Public website and documentation entry points | Keep stable Pages URL during repository organization |

## Migration rules

1. Do not create duplicate repositories to reserve names.
2. Do not fork an upstream project solely to make its name appear in the organization. Fork only after an ADR identifies the required ownership boundary, maintenance plan, patch policy, and license obligations.
3. Before moving code, identify its current source of truth and open PRs. Do not silently discard open review history or user changes.
4. When a repository rename is needed, use GitHub repository settings and preserve redirects. Update canonical links, badges, workflow permissions, Pages configuration, issue templates, branch protection, and external references afterward.
5. When transferring or forking upstream code, preserve copyright notices, license files, required attribution, and a machine-readable provenance register. Product identity can be independent; legal notices must remain accurate.
6. Keep project-owned package-manager code, package recipes, build orchestration, base-system configuration, installer, and deployment infrastructure separated by clear responsibility.
7. Never import a large upstream tree until its license, security support, integration cost, update path, and long-term maintainer capacity have been reviewed.

## Upstream evaluation and forks

A fork is not the default implementation strategy. Evaluate in this order:

1. Configure a maintained component without patches.
2. Package it and maintain Deku-specific configuration.
3. Carry a small, documented patch series.
4. Maintain a fork only if patches cannot be managed responsibly elsewhere or an explicit long-term ownership need exists.
5. Rewrite a component only when measurable requirements justify the engineering and security cost.

For every candidate, record upstream URL, immutable revision, license, security policy, maintenance status, local patch list, integration surface, and how updates will be merged. Do not conflate a technical evaluation with an accepted platform decision.

## Work sequence

- [ ] Review open PRs before changing repository names or default branches.
- [ ] Bootstrap `deku-build` and `deku-recipes` with scoped READMEs and CI checks.
- [ ] Keep the package manager prototype in `deku-pkg`; move experimental files only through a reviewed PR.
- [ ] Define the first base-system integration boundary in `deku-system`.
- [ ] Review the installer prototype and decide whether Anaconda is adaptable before copying any source.
- [ ] After implementation boundaries stabilize, update cross-repository links and organization metadata.
- [ ] Only then decide whether any old repository should be renamed, archived, or retained as a compatibility/history repository.

## Tooling limitation

If repository creation, rename, fork, or transfer operations are not exposed by the connected GitHub tooling, perform those administrative steps manually in the GitHub organization UI. Code and documentation can still be prepared in PRs, but administrative actions must not be claimed complete until GitHub confirms them.
