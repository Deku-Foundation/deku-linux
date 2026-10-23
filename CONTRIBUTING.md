# Contributing to Deku Linux

## Before starting

1. Read the project charter and roadmap.
2. Search existing issues and pull requests.
3. Propose an issue or ADR before broad architectural changes.
4. Never submit credentials, private keys, access tokens, personal data, or proprietary material.

## Branch workflow

- Use `dev` for integration and validation; `main` is the reviewed baseline.
- Test changes on `dev`, inspect the diff, and open a pull request from `dev` to `main` only after the applicable checks pass.
- Keep long-lived branches to `main` and `dev`. Temporary branches are exceptions for active pull requests; forks are preferred for independent contributor work.
- After promotion, verify the post-merge checks and confirm `dev` is synchronized before starting the next task.

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

- Prefer pull requests over direct commits to the default branch.
- Have another maintainer review changes when project size permits.
- Require applicable CI checks to pass once configured.
- Give security-sensitive changes additional scrutiny.
- Do not bypass required checks or overwrite another contributor's work.

## Licensing

Contributors must have the right to submit their work. Check the repository license and any file-specific license before contributing. Third-party code must retain required notices and license information.

## Conduct concerns

Report sensitive concerns privately through a verified maintainer contact. Do not publish personal information in issues.
