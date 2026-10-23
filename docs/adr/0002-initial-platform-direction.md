# ADR-0002: Initial Platform Direction

- **Status:** Proposed — not yet accepted
- **Date:** 2026-10-23
- **Decision owners:** Project maintainers
- **Related documents:** `docs/strategy/growth-and-reliability.md`, `docs/roadmap.md`

## Context

Deku Linux needs a narrow technical target to make the first package and image prototype achievable. The wrong early choice can multiply maintenance cost, break binary compatibility, or create avoidable security and recovery risks.

## Decision drivers

- sustainable maintenance by a small early team;
- broad application and hardware compatibility;
- mature upstream documentation and tooling;
- traceable package sources and build inputs;
- secure updates and recoverability;
- a clear route to independent distribution infrastructure over time.

## Proposed direction for a prototype

These are defaults to validate with small experiments, not final commitments:

1. **Architecture:** target x86_64 first.
2. **C library:** evaluate glibc first for broad desktop application compatibility; revisit musl only with a concrete target and compatibility plan.
3. **Init/service management:** compare systemd and runit using actual service requirements, desktop integration, diagnostics, and maintainer capacity. Do not choose solely on minimalism or ideology.
4. **Package/build foundation:** prototype a mature existing package/build system before writing a new package manager. Evaluate license compatibility, maintenance activity, metadata capabilities, dependency handling, signing, rollback behavior, and the cost of maintaining divergence.
5. **Desktop:** start with one supported desktop profile; select it after testing hardware, accessibility, localization, session management, and update behavior.
6. **Release model:** do not commit to rolling release until automated upgrade testing, security update capacity, and repository promotion controls exist.
7. **Build security:** separate untrusted pull-request builds from trusted release signing and publication. Build workers must not have access to long-lived signing keys.
8. **Reproducibility:** record immutable source references and checksums from the first prototype; measure reproducibility instead of claiming it.

## Options considered

### Build all core tools from scratch immediately

Benefits: maximal design control.

Costs: substantially larger scope, more security-sensitive code, slower initial delivery, and greater long-term maintenance risk.

### Reuse mature upstream tools and replace components only when justified

Benefits: faster validation, existing tests and documentation, reduced bespoke code.

Costs: upstream constraints, integration work, possible differences between upstream assumptions and Deku's goals.

### Ship a derivative of an existing distribution first

Benefits: quickest route to a working desktop prototype.

Costs: lower control over the base system and risk of confusing product goals with a theme or configuration layer.

## Proposed decision

Choose the second option for the initial engineering phase: reuse mature components where practical, while retaining ownership of Deku's integration, policies, release engineering, documentation, and user experience. Reconsider only when prototypes show a specific unmet requirement.

## Validation required before acceptance

- compare at least two realistic package/build approaches against a documented checklist;
- build a harmless test package in a disposable environment;
- document source verification, dependency metadata, build logs, and artifact hashes;
- test how the approach handles failed builds and dependency changes;
- estimate maintenance cost and license obligations;
- review the threat model and signing/publication separation.

## Consequences

The project will not initially have a bespoke package manager or a fully independent toolchain. This is intentional: engineering effort should first establish a trustworthy build and update path. Any later decision to replace an upstream component must include a maintenance owner, compatibility plan, migration path, and test evidence.
