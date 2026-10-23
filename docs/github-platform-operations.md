# Operating Deku's GitHub workspace

**Status:** Maintainer runbook. This document describes settings to configure and verify; it does not claim that organization-level features have already been enabled.

Deku has separate repositories for the website, project architecture, recipes, package planning, build-plan validation, installer planning, system composition and infrastructure. A useful GitHub workspace should make ownership and review status visible without turning the website into a second, manually maintained issue tracker.

## 1. Use each GitHub surface for a specific job

| Surface | Use it for | Do not use it for |
|---|---|---|
| Repository README | Component scope, current status, development entry point and local checks | Duplicating the full project roadmap in every repository |
| Issues | Reproducible bugs, scoped work, supportable feature requests and follow-up tasks | Public disclosure of an exploitable vulnerability |
| Pull requests | A reviewable diff, evidence, CI results, risk analysis and known limitations | Announcements with no code or documentation change |
| Actions | Authoritative results for the exact commit or PR revision | Static badges or manually edited claims that checks passed |
| Organization Project | Cross-repository execution plan, blockers, milestone visibility and release gates | A substitute for owning issues in the source repository |
| Discussions | Open questions, community Q&A, announcements and early design conversations | Work tracking after a proposal becomes a scoped, actionable change |
| Releases | Versioned source/artifacts, notes, checksums, signatures and provenance when available | A substitute for signed, freshness-protected Linux repository metadata |
| GitHub Pages | Public documentation, contribution routing and verified project status | A manual mirror of live issue counts or workflow state |

Issues remain attached to their owning repository. The organization Project can aggregate them without copying issue descriptions between repositories. If Discussions are disabled, the issue form and contribution guide must explain where to ask a question instead.

## 2. Organization Project board

Create the Project from the organization's **Projects** area using an owner account. Link the eight canonical repositories listed in the [engineering hub](https://deku-foundation.github.io/development/). Start with a small set of fields rather than a complex workflow.

Recommended fields:

- **Status:** Backlog, Ready, In progress, In review, Blocked, Done.
- **Workstream:** Architecture, Recipes, Package manager, Build, Installer, System image, Kernel/Desktop, Security, Website/Docs.
- **Priority:** P0 release blocker, P1 high, P2 normal, P3 low.
- **Milestone:** Research, prototype, integration, release candidate, post-release.
- **Evidence/exit criterion:** a link to a CI run, test result, ADR, or other concrete proof required to close a release-gate item.

Recommended views:

1. **Roadmap:** group by milestone and sort by priority.
2. **Working board:** board view grouped by status, filtered to open work.
3. **Blocked work:** issues with status Blocked and a named dependency.
4. **Release gates:** only items whose exit criterion must pass before an installer image or ISO can be announced.
5. **Website and documentation:** localization, accessibility, stale-link and publication tasks.

After creating the fields, add GitHub's built-in Project workflows where appropriate (for example, adding newly opened issues and moving closed issues to Done). Verify the automation with a test issue before relying on it. Project settings, field configuration and workflow automation are not committed as repository files, so record the owner and configuration location.

## 3. Discussions and community routing

A settings check on 23 October 2026 found GitHub Discussions disabled on the core repositories. An administrator with suitable repository or organization permissions should decide whether to enable one central discussion space or separate discussions for individual components.

If enabled, use a few clear categories:

- **Announcements** — maintainer-created updates; avoid using this for unreleased features.
- **Q&A** — general questions, with answers linked into documentation when useful.
- **Design proposals** — early options analysis before the question is narrow enough for an issue or ADR.
- **Show and tell** — community experiments and contributions, clearly distinguished from supported project functionality.

Create a written moderation and response policy before inviting broad participation. Move agreed, actionable work into repository issues and link back to the discussion. Do not publish security-sensitive reproduction details in a public discussion; follow the SECURITY.md policy.

Until Discussions are enabled and tested, link contributors to the existing contribution guide and use one focused issue when a question requires a tracked technical answer. Do not publish an unverified discussions URL.

## 4. Protect the main branch and CI

A maintainer should review GitHub repository settings directly and record the resulting configuration. The code cannot prove a setting has been enabled.

- Protect main with a repository ruleset or branch protection rule.
- Require pull requests for changes to main; require at least one maintainer review where staffing permits.
- Require applicable CI checks for the repository, and dismiss stale approvals when new commits materially change a reviewed patch.
- Restrict force pushes and branch deletion on main; define a documented exception process for incidents.
- Set GITHUB_TOKEN permissions to read-only unless a specific job needs more.
- Keep deploy, signing and publication credentials out of build/test jobs and untrusted pull-request workflows.
- Pin GitHub Actions to full commit SHAs and audit changes to workflow files.
- Enable Dependabot version and security update alerts where supported, then triage them according to risk and actual package ownership.

A green CI run only proves that the configured tests passed for the checked revision. It does not prove the full distribution is safe, that an artifact is reproducible, or that Pages/registry deployment completed. Link evidence to the exact commit and keep limitations explicit.

## 5. Security and supply-chain readiness

Before announcing a first installable image, verify that the project has:

- A monitored private vulnerability reporting route and a published disclosure policy.
- Maintainers who can rotate credentials and recover a compromised account or release key.
- A documented signer/verification model for releases and repository metadata.
- An inventory of workflow permissions and pinned external actions.
- Reproducible build inputs, checksums, provenance/SBOM where appropriate, and a way to revoke a bad release.
- A tested process for restoring or rolling back a broken update.
- A known-issues page and an owner for incoming security reports.

Use OpenSSF Scorecard as one source of supply-chain signals, not as a security certification or a replacement for threat modelling, code review and tests.

## 6. Releases and package hosting

When a release artifact is available, create a Git tag and a GitHub Release with notes, checksums, signatures, source references, build provenance and known limitations. For a future Deku package repository, publish immutable package artifacts and signed repository metadata with expiration/freshness and rollback protection. Do not upload placeholder ISOs or describe a GitHub Release as a package repository.

The current package manager, build tool and installer are prototypes. This runbook does not change that status.

## 7. Maintainer verification checklist

- [ ] A Project owner is named; the shared board and its fields/views are created.
- [ ] Project automation is tested with a real issue and a closed PR.
- [ ] Discussions decision is recorded; if enabled, categories and moderation guidance are in place.
- [ ] Main-branch rules require the intended reviews and checks.
- [ ] Workflow permissions and full-SHA Action pins are checked across all repositories.
- [ ] Private security reporting is configured and an owner is monitoring it.
- [ ] Release-key custody, revocation and recovery are documented before signing production artifacts.
- [ ] The public website's project/CI status links resolve to the canonical repositories.
- [ ] A successful default-branch Pages deployment is checked after website changes.

**Completion evidence:** add the settings links, board URL, names of responsible maintainers, and date of the last verification here once those actions are completed. Do not mark checklist items complete from a pull-request merge alone.
