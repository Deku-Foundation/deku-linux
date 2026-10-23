# ADR-0002: Deku package, build, and application architecture

- **Status:** Proposed; implementation must follow staged acceptance criteria.
- **Date:** 2026-10-23
- **Scope:** Architecture direction, not a claim of production readiness.

## Context

Deku needs an independent Rust-native package manager and build system, official repositories with a clear trust boundary, optional compatibility with external package ecosystems, KDE as the initial desktop, and a path to GNOME later. Fedora, Void, Nix, Flatpak, bootc, Tvix, and Linux kernel sandbox interfaces provide useful ideas, but their components must not be combined without explicit ownership and threat-model decisions.

## Decisions proposed

### 1. Keep five separate layers

1. **Recipe/source layer (deku-recipes):** reviewed package recipes, source URL, immutable revision, source digest, license/provenance, patches, dependencies, build environment, and test policy.
2. **Build layer (deku-build):** isolated source builds, dependency closure, cache, logs, reproducibility checks, attestations, and signed outputs. Recipes are data; no untrusted recipe runs on the host.
3. **Repository layer (deku-infra):** immutable artifacts, versioned metadata, signed snapshots, key rotation, revocation, freshness and rollback protection.
4. **Native package manager (deku-pkg):** metadata validation, dependency solver, download verification, transaction planning, staging, activation, rollback, and garbage collection.
5. **Application delivery:** Flatpak integration for desktop apps; native packages for the base OS, libraries, drivers, command-line/system tools, and tightly integrated components.

### 2. Prefer native source recipes over blind RPM/DEB conversion

The official Deku repository is the default and only trusted native source out of the box. Upstream projects become Deku recipes pinned to reviewed revisions, with licenses, patches, dependencies, and test results recorded. RPM/DEB import is an optional compatibility feature, not an alternate source of trust.

RPM and DEB are not merely archive formats. They have different dependency semantics, file ownership rules, triggers, and maintainer-script behavior. A conversion cannot safely assume that translating metadata or extracting files preserves behavior. In advanced mode, importers must parse formats without executing scripts, inspect file lists and metadata, reject unsupported features, and build a Deku-native artifact in a sandbox where possible. Packages requiring arbitrary privileged scripts or unsupported dependency semantics must be rejected or run only in a separately designed compatibility environment. Never run imported maintainer scripts as root by default.

### 3. Store immutable package payloads separately from mutable system state

Do not put every program into one shared /opt/programs directory and do not overwrite files in /usr directly from arbitrary upstream packages.

Proposed model:
- /deku/store/<content-id>/ contains immutable package payloads keyed by verified content/build identity.
- /deku/profiles/system/<generation>/ represents a coherent set of package versions.
- /deku/var/ contains mutable package-manager state, caches, and transaction journals.
- /usr remains the conventional host filesystem interface. During the first implementation, activate the selected generation via a tested profile/link strategy or a generated filesystem image; do not require every application to understand /deku/store.
- /etc remains administrator-owned configuration. Package defaults are delivered as vendor defaults and cannot silently overwrite user changes.
- /var holds mutable system data; user settings remain in XDG locations such as ~/.config and ~/.local/share.
- /opt remains available for third-party/vendor software where appropriate, not as the universal package database.

The Nix-style immutable store and profile idea is useful for coexistence of versions and rollback. It does not automatically solve integration: absolute paths, ELF interpreter paths, RPATH/RUNPATH, plugins, icons, desktop files, D-Bus activation, system services, udev rules, kernel modules, and services need explicit integration rules. Start with a small tested set of supported integration types.

### 4. Transactions must be atomic or recoverable

Before applying a transaction, resolve the full dependency graph and conflicts, verify signatures and digests, check available space, and produce a human-readable plan. Stage changes away from the live system, validate ownership and paths, and commit a journaled generation switch. On failure, restore the previous generation. Never claim atomicity until crash/power-loss tests demonstrate it.

Configuration migrations and service actions must be explicit, bounded, logged, and recoverable. Package removal must not remove files owned by another package or user data. Kernel upgrades must preserve a bootable previous kernel and boot entry.

### 5. Trust and build security

- Official repository keys and build-signing keys are separate; signing keys never live in source control.
- Sign repository metadata and artifacts; hash checking alone does not authenticate publishers.
- Use immutable source revisions and verified source digests.
- Build unprivileged with network disabled after source acquisition, restricted filesystem views, resource limits, and disposable workers.
- Use namespaces and seccomp where available, plus Landlock for filesystem restrictions when supported. Fail closed or downgrade only through an explicit, visible policy when a required sandbox feature is unavailable.
- Keep build provenance and test attestations. Reproducibility checks should compare independent builds for selected packages.
- Protect against stale metadata, key revocation failures, freeze/rollback attacks, and compromised mirrors. Evaluate TUF-style metadata roles/expiry and in-toto-style provenance before specifying a custom protocol.
- No third-party repository is trusted by default. Adding a repository requires an explicit trust decision and scoped key identity.

### 6. External formats and Flatpak

- **RPM/DEB:** advanced mode is off by default. First implement safe inspection and metadata reporting; later support controlled import/rebuild. Do not promise every package will work.
- **AppImage:** optional application compatibility, separately reviewed; not a native system package.
- **Flatpak:** integrate upstream Flatpak tooling and Discover-facing metadata rather than reimplementing Flatpak. Enable Flathub only with a clear user-visible first-run choice or documented default policy, and distinguish Flathub trust from the official Deku repository.
- Flatpak applications do not replace kernel modules, boot-critical packages, host services, or drivers.

### 7. KDE first, GNOME later

The first desktop target is KDE Plasma, with a pinned, tested version set and a reproducible image manifest. Keep desktop-independent system services, portals, audio, graphics, login/session integration, and application metadata separated from Plasma-specific packages. Add GNOME as a second desktop profile only after the common base and display/session stack are stable. Avoid installing both full desktops by default.

### 8. Kernel policy

Linux 7.3 was published as mainline on 2026-10-18, but the latest stable series listed by kernel.org on 2026-10-23 is 7.2.12. Therefore, 7.3 may be tested in a development/experimental image, but the first stable image should default to the latest tested stable release unless the project explicitly accepts mainline risk. Keep a previous known-good kernel and recovery boot entry. Pin the exact source tag and signature, config, compiler/toolchain, and patch set.

## Architecture sketch

    Official reviewed recipes
             | immutable sources + license/provenance
             v
    Isolated build workers -----> logs / provenance / tests
             | signed Deku-native artifacts
             v
    Signed repository snapshots (freshness + rollback protection)
             |
             v
    Rust package manager: solver -> verify -> stage -> activate -> rollback
             |
             +---- base OS / kernel / drivers / system tools
             +---- KDE profile (initial)
             +---- GNOME profile (future)
             +---- Flatpak integration for desktop applications

    Advanced compatibility import (disabled by default):
    RPM / DEB -> inspect -> policy gate -> sandboxed rebuild/import
              -> Deku-native artifact only if policy and tests pass

## Non-goals for the first milestone

- Executing arbitrary RPM/DEB maintainer scripts as root.
- Supporting every upstream package with a promise of full compatibility.
- Rewriting Flatpak, RPM, DEB, or the Nix evaluator.
- Building a production ISO before package installation, rollback, boot recovery, and clean-install tests exist.
- Enabling untrusted community repositories by default.

## Implementation sequence and acceptance gates

1. **Specification:** define package schema, repository metadata, trust model, version constraints, conflict rules, filesystem ownership, and transaction states.
2. **Local prototype:** parse test fixtures, solve dependencies deterministically, verify content digests, and emit a plan without root privileges.
3. **Artifact/repository prototype:** sign test metadata, reject expired or revoked keys, test stale snapshot and rollback attacks, and publish immutable test artifacts.
4. **Safe installation prototype:** install into a temporary root, detect path collisions and symlink traversal, journal operations, and test interruption recovery.
5. **Build prototype:** execute only allowlisted recipe steps in disposable sandboxes; test no network, no host writes, resource limits, and provenance.
6. **System integration:** kernel and base-system transaction, boot entry, rollback, and recovery tests.
7. **Desktop integration:** KDE profile, Flatpak install/update/removal, portals and file associations.
8. **Image/installer:** only after the above gates pass in automated VM tests.

Every gate requires tests and review. A metadata validator or dependency planner alone is not a package manager.
