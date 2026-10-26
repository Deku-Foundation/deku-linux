# Contributing to Deku Linux

## Before starting

1. Read the project charter and roadmap.
2. Search existing issues and pull requests.
3. Propose an issue or ADR before broad architectural changes.
4. Never submit credentials, private keys, access tokens, personal data, or proprietary material.

## Branch workflow

- Use `dev` for integration and validation; `main` is the reviewed baseline.
- Maintainers make routine changes directly on `dev`, run the applicable checks, and inspect the diff. When all required checks pass, fast-forward `main` to the exact `dev` commit; do not open a PR to promote `dev` to `main`.
- Keep `main` and `dev` as the only persistent repository branches. Do not create in-repository feature branches for routine work. External contributors can use a fork and submit changes for review into `dev`.
- After promotion, confirm that `main` and the verified `dev` commit match, then check deployment or post-promotion workflows.

See the [foundation-wide engineering workflow](https://github.com/Deku-Foundation/Deku-Foundation.github.io/blob/main/ENGINEERING_WORKFLOW.md) and [governance policy](https://github.com/Deku-Foundation/Deku-Foundation.github.io/blob/main/GOVERNANCE.md).

## Changes

- Keep pull requests focused and explain the problem, approach, risks, and validation.
- Update documentation when architecture, behavior, support, or operations change.
- Prefer upstream fixes over long-lived local patches.
- Do not claim tests, reviews, compatibility, or reproducible builds that were not actually verified.
- Clearly identify assumptions and known limitations.

## Commit messages

Use concise imperative messages. Conventional Commits style is encouraged, for example `docs: document package trust model`.

## Review and merge

- Use pull requests to review external contributions from forks. Maintainer changes are validated on `dev` and promoted to `main` with a direct fast-forward after required checks pass.
- Have another maintainer review changes when project size permits.
- Require applicable CI checks to pass once configured.
- Give security-sensitive changes additional scrutiny.
- Do not bypass required checks or overwrite another contributor's work.

## Licensing

Contributors must have the right to submit their work. Check the repository license and any file-specific license before contributing. Third-party code must retain required notices and license information.

## Conduct concerns

Report sensitive concerns privately through a verified maintainer contact. Do not publish personal information in issues.

## Documentation style

Write for the reader's task. State what is implemented, what has been tested and what remains planned; keep important limitations and translations aligned. Follow the [Deku Foundation technical writing standard](https://github.com/Deku-Foundation/.github/blob/main/EDITORIAL_STYLE.md).
