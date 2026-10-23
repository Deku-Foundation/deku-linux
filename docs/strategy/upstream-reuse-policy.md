# Deku Linux upstream reuse and fork policy

**Status:** Proposed policy — requires maintainer approval.

## 1. Objective

Deku Linux should reuse mature upstream software where it improves compatibility, security, maintainability, and delivery speed. Independence means controlling our release engineering, integration, defaults, documentation, and long-term direction; it does not require rewriting every component.

## 2. Reuse hierarchy

Evaluate options in this order:

1. Configure an upstream component without maintaining a fork.
2. Package an upstream release with a small, reviewable Deku-specific patch set.
3. Maintain a fork only when a concrete requirement cannot be met upstream or through packaging.
4. Develop a replacement only when documented requirements, security review, maintenance capacity, and comparative tests justify it.

Every maintained fork must have an owner, upstream tracking strategy, patch inventory, update cadence, and exit or upstreaming plan.

## 3. Candidate upstreams

- **Void Linux / XBPS / void-packages:** evaluate the package format, build templates, build isolation, repository metadata and signing. These are separate projects with separate licenses and maintenance histories; review each repository and component before copying or redistributing.
- **systemd:** evaluate as the initial default service manager for compatibility. Keep init integration modular where practical; document why any alternative is supported.
- **glibc:** evaluate as the initial default C library for application compatibility. Pin and test versions, track security advisories, and document ABI/update policy.
- **Nix / NixOS ideas:** evaluate reproducible-build workflows, declarative configuration, isolated builds, generations and rollback. Adopt the smallest useful mechanisms first rather than importing the whole NixOS architecture without a clear requirement.

These are evaluation directions, not accepted architecture decisions.

## 4. Mandatory checks before copying or forking

For every upstream repository or imported component, record:

- Canonical upstream URL and exact commit or release tag.
- License and notices for the repository and any bundled subcomponents.
- Whether redistribution, modification, and relicensing are permitted; preserve required copyright and license notices.
- Local patches and their rationale.
- Known vulnerabilities, support status, release cadence, and compatibility impact.
- Build and test instructions, and whether the build can run in an isolated, unprivileged environment.
- An owner and a plan for importing upstream updates.

Do not assume that a public Git repository is public domain or that every file shares the repository's top-level license. Do not copy trademarks, branding, signing keys, release credentials, or upstream infrastructure secrets.

## 5. Supply-chain and release rules

- Never execute unreviewed code from an upstream repository on a privileged runner.
- Pin CI actions and external build inputs to reviewed immutable versions where feasible.
- Verify source hashes; use signatures and trusted provenance where supported. A hash alone is not authentication.
- Keep build jobs separate from release signing and publication.
- Store signing keys outside source control and do not expose them to untrusted pull-request workflows.
- Prefer reproducibility checks and independent rebuilds; do not claim a build is reproducible until measured.
- Require review and automated tests before changes reach release branches.

## 6. Repository organization

Proposed repositories, created only when there is an immediate purpose:

- `project`: governance, architecture decisions, roadmap and security policy.
- `packages`: Deku-owned package templates and patches; upstream imports must be clearly tracked.
- `build-system`: image and package build orchestration, initially without release-signing secrets.
- `infrastructure`: public infrastructure configuration and deployment automation; secrets never belong here.
- `website`: project website and documentation site, when needed.

Avoid creating empty repositories just to reserve names. Each repository should have an owner, README, license, security reporting instructions, CI, and branch protections appropriate to its risk.

## 7. Acceptance criteria

Before this policy is accepted, maintainers should agree on the first platform target, the package/build system to prototype, the initial init system and C library, and what level of upstream divergence is acceptable. Record final decisions in numbered ADRs; keep proposals marked as proposed until tested and approved.
