# Foundation scope and Arabic-first language strategy

**Status:** proposal for review
**Scope:** organization identity, multi-project portfolio, and a possible Arabic-first programming language
**Non-goal:** this document does not claim that a new language, compiler, standard library, or self-hosting toolchain exists.

## 1. Foundation, not a single-product company

Deku Foundation should be described as an open-source engineering organization building independent software projects. Deku Linux is its first visible platform project, not the definition of the entire organization.

A concise public description:

> Deku Foundation is an open-source engineering organization building secure, accessible and dependable software—from Linux infrastructure to developer tools and Arabic-first programming technology.

Short organization tagline:

> Independent open-source engineering.

The foundation should publish a portfolio map and make each project’s status explicit: idea, specification, prototype, alpha, stable, or archived. A repository existing does not imply that its software is usable or production-ready.

## 2. Proposed project portfolio

| Area | Purpose | Boundary |
| --- | --- | --- |
| Deku Linux | A Linux distribution and coherent desktop platform | Distribution work must not dictate every future foundation project |
| Native package tooling | Package metadata, dependency planning, repository trust and transactions | Separate the unprivileged client, repository publication and privileged system integration |
| Build and recipe tooling | Reviewed recipes and constrained builds | A recipe parser is not a secure build service |
| Arabic-first language (working name TBD) | Programming language, compiler, tools and libraries | Start as a small, testable language hosted by Rust; self-hosting is a later milestone |
| Shared engineering | CI templates, contribution policies, security reporting and release practices | Reuse policies without forcing every project into one stack |

Do not create empty repositories just to make the portfolio look larger. Create each project when it has an owner, a short charter, an initial milestone and a CI-tested vertical slice.

## 3. Arabic-first programming language: design direction

The goal should be a real programming language whose syntax and diagnostics are designed for Arabic readers, not merely English keywords translated into Arabic. The implementation can initially be written in Rust and gradually become self-hosting if that proves useful.

### First release scope

1. A written language specification with examples, grammar, precedence, types and error semantics.
2. A Unicode-aware lexer and parser that handle Arabic identifiers and keywords deterministically.
3. A minimal type system and a small standard library.
4. An interpreter or a deliberately small compiler target for the first vertical slice.
5. Clear diagnostics in Arabic and English, including source spans and actionable error messages.
6. Formatter, test runner, language-server protocol support and editor examples only as each becomes testable.
7. A documented interoperability boundary for calling Rust/C libraries rather than promising universal foreign-function compatibility.

### Unicode and text are core design constraints

- Normalize identifiers consistently (for example, NFC) and specify exactly which code points are legal.
- Define whether Arabic diacritics, tatweel, Arabic-Indic digits and Persian/Urdu letter variants are accepted in identifiers; do not silently equate visually similar characters.
- Specify bidirectional text behavior for source code, diagnostics, comments, strings, terminals and editor selections. Test mixed Arabic/Latin text and punctuation.
- Prevent confusing identifiers with invisible or control characters; show escaped forms in diagnostics and provide lint rules for confusables.
- Keep keywords and identifiers separate. Do not make the parser depend on visual shaping or presentation-form code points.
- Decide explicitly whether the canonical source representation is UTF-8 and document newline and encoding rules.

### Compiler roadmap

**Stage 0 — RFC and examples:** define goals, non-goals, grammar, Unicode policy, type semantics and an error catalogue. Collect small programs before building features.

**Stage 1 — hosted prototype:** implement lexer, parser, AST, interpreter and golden tests in Rust. Add property/fuzz tests for malformed UTF-8 boundaries, deeply nested expressions and arbitrary Unicode input.

**Stage 2 — usable developer loop:** add formatter, package/module model, test runner, editor integration and stable diagnostics. Publish examples and migration/versioning rules.

**Stage 3 — native compilation and interoperability:** select a backend based on measured needs (for example LLVM or Cranelift), define ABI and linking behavior, and keep generated code reproducible where possible.

**Stage 4 — self-hosting experiment:** write a subset of the compiler in the language, compare outputs against the Rust-hosted compiler, and retain a bootstrap compiler with a documented trust and reproducibility process. Self-hosting is a milestone, not a prerequisite for usefulness.

## 4. Naming: preliminary screening, not legal clearance

**Do not assume Qaf / قاف is available.** A public search finds an earlier project described as “Qaf - Arabic-Based Programming Language”, as well as other unrelated products using Qaf. This does not prove a legal conflict, but it makes an unqualified name harder to discover and distinguish.

Candidate directions for research:

- **Nasaq (نسق):** suggests structure, order and syntax; relatively suitable for a compiler/toolchain identity.
- **Mantiq (منطق):** conveys logic, but is a common technical/philosophical word and may be crowded.
- **Qaf / قاف:** memorable and culturally grounded, but already used by an Arabic-based language project and multiple unrelated products.

These are brainstorming candidates, not availability findings. Before selecting a name, check GitHub organization/repository names, crates.io, package registries, domains, search results in Arabic and Latin spellings, and relevant trademark databases in target markets. A legal trademark search cannot be replaced by a web search.

If Qaf remains a strong preference, use a distinct compound identity only after checking it (for example, a qualified project name rather than Qaf alone). Do not claim exclusivity until checks are complete.

## 5. Governance and GitHub as the engineering platform

Use GitHub as the source of truth for project work, not as a substitute for project design.

- Organization profile: clear mission, project map, contribution entry point, security reporting route and current status.
- Pin a small set of repositories that represent active work; do not pin every repository.
- Use issue forms for bugs and feature requests, pull-request templates, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, SUPPORT.md, and a FUNDING.yml only if there is a real funding destination.
- Use GitHub Discussions for design questions and community support where maintainers can respond; keep accepted technical decisions in versioned RFCs/ADRs.
- Use Projects for milestone tracking, Releases for actual versioned artifacts, and Actions for repeatable tests. Publish only artifacts that were built and tested.
- Apply least-privilege GITHUB_TOKEN permissions, pin third-party Actions to reviewed immutable SHAs, protect the default branch, require review for high-risk code, and use CODEOWNERS when real maintainers exist.
- Use Dependabot/Renovate and CodeQL where they fit the language and repository. Add secret scanning and signed releases when the organization’s available plan and project risk justify them.
- Prefer reusable workflows only after the common policy is stable; keep project-specific tests explicit.
- Keep website status synchronized with releases and repository evidence. Never display fabricated CI badges, downloads, release dates or contributor counts.

## 6. Identity and design-system direction

The current site mark is a small green abstract leaf combined with circuit-like strokes. It is clean and legible at larger sizes, but its plant motif strongly suggests sustainability or “green technology”, while the circuit paths are generic technology imagery. It does not yet express an independent, multi-project engineering foundation, and its small internal strokes may lose definition at avatar sizes.

The generated leaf/circuit concept has the same limitation. Treat it as a direction study, not as a finalized identity.

A more durable identity should be built around a simple geometric symbol that works at 16–32 px, has a strong silhouette in monochrome, does not depend on fine lines or gradients, and can be used consistently across Linux, compilers, libraries and developer tooling. Keep the wordmark separate from the avatar symbol. Use a restrained forest-green palette with neutral backgrounds, and verify text contrast against WCAG 2.2 AA. Do not copy GitHub’s Octocat or imply official affiliation with GitHub.

## 7. Acceptance criteria

This strategy is ready to become an accepted decision only after maintainers review:

- the foundation mission and first project portfolio;
- the language’s audience, syntax goals and Unicode policy;
- the naming search and repository/domain namespace;
- the initial language vertical slice and test strategy;
- contribution, security-disclosure and release governance;
- the final identity’s monochrome, small-size, contrast and RTL tests.

Until then, use the public description as an organizational statement, not as a claim of legal status, release maturity or an existing self-hosted language.
