# Upstream reuse and repository creation plan

- **Status:** proposed; no package manager or upstream fork is selected by this document.
- **Last reviewed:** 2026-10-23
- **Goal:** keep the project maintainable, traceable, and genuinely independent without creating unnecessary long-lived forks.

## Existing Deku repositories

| Repository | Responsibility | Next boundary |
|---|---|---|
| `Deku-Foundation/project` | Governance, roadmap, ADRs, architecture, threat model | No package payloads or generated images |
| `Deku-Foundation/packages` | Deku-owned package metadata, patches, and recipes once the format is accepted | Do not mirror every upstream package by default |
| `Deku-Foundation/build-system` | Isolated builds, provenance, image assembly, test harnesses | No signing keys in untrusted build jobs |
| `Deku-Foundation/infrastructure` | Release infrastructure, mirror and deployment policies | Separate public metadata from secrets |
| `Deku-Foundation/Deku-Foundation.github.io` | Public website | No fake release downloads or unsupported product claims |

## Upstream candidates and exact repository names

### Package build and package collection

- Upstream candidate: `void-linux/void-packages`.
- Possible Deku fork name if XBPS is accepted after evaluation: `Deku-Foundation/void-packages`.
- Upstream candidate: `void-linux/xbps`.
- Possible Deku fork name only if Deku needs maintained code changes: `Deku-Foundation/xbps`.
- Until the ADR is accepted, keep evaluating XBPS/xbps-src and alternatives; do not import or mirror the full package collection. A fork creates ongoing merge, security, license, and package-review obligations.

### Linux kernel

- Upstream source: `torvalds/linux`, official release metadata at https://www.kernel.org/.
- **Do not fork the entire kernel repository as the first step.** Track official stable/LTS source archives, verify upstream signatures, and maintain a small, reviewed configuration/packaging layer.
- Proposed future repository name if kernel-specific configuration, patches, and test results become substantial: `Deku-Foundation/kernel`.
- Keep Deku-owned kernel packaging in `Deku-Foundation/packages` unless it grows into a separate release boundary. If a long-lived kernel patch set is eventually required, reconsider a fork named `Deku-Foundation/linux`; do not create it before there is a maintained patch queue and clear rebase owner.

## Repositories to defer

- `Deku-Foundation/installer`: create only after the first bootable image and installation requirements are testable.
- `Deku-Foundation/system-tools`: create when there are multiple Deku-maintained tools with a shared release/test lifecycle.
- `Deku-Foundation/kernel`: create only when kernel configuration, patches, CI, and support policy justify independent ownership; it is not a copy of the Linux source tree.
- `Deku-Foundation/mirror` or `Deku-Foundation/release-artifacts`: do not use a Git repository for large binary package/ISO distribution. Choose object storage or a package repository service after signing, retention, and access controls are designed.

## Required gates before a fork

1. Confirm upstream license and notices for the exact code to be reused.
2. Record the upstream canonical URL, default branch, release cadence, maintainer health, and security response path.
3. State the unmet requirement that configuration or packaging cannot solve.
4. Identify an owner for upstream syncs, patch rebases, CVE triage, and release compatibility.
5. Add CI and a documented process for regularly comparing against upstream.
6. Keep the fork public only if intended and all imported content permits it; never rewrite history or remove upstream notices.
7. If a repository cannot be created through the available GitHub integration, create it in the GitHub organization UI with the exact proposed name, then record its canonical URL here. Do not pretend that a name proposal is a created repository.

## Current execution order

1. Review and merge the package review policy only after review.
2. Evaluate XBPS/xbps-src versus at least one alternative with a disposable, non-privileged test package.
3. Track the current stable kernel candidate and LTS alternative in `Deku-Foundation/packages`; refresh versions from kernel.org before use.
4. Record build and boot evidence before publishing a kernel package.
5. Create a dedicated repository only when the ownership boundary and maintenance plan are concrete.
