# Compatible software strategy and upstream research

**Research date:** 2026-10-23  
**Status:** Engineering baseline for prototypes; not a claim of production readiness.

## The compatibility goal: broad intake, honest guarantees

“Supports everything” cannot be achieved by converting archive formats alone. Conversion does not translate CPU instructions, C library/ABI assumptions, runtime dependencies, kernel interfaces, service-manager conventions, filesystem layout, or permissions. A package may unpack correctly and still be broken or unsafe. Deku should aim for broad software intake with explicit compatibility tiers, not promise that every package runs.

### Required compatibility tiers

1. **Tier A — Native Deku packages (default):** build from reviewed Deku recipes with pinned source revisions and digests, license/provenance metadata, declared dependencies, file manifests, tests, and signed repository metadata.
2. **Tier B — Upstream-source rebuild (preferred):** verify a source release or immutable commit, apply reviewed patches, build for Deku’s target ABI in a disposable sandbox, run tests, and emit a native Deku artifact. A recipe converter may generate metadata and build inputs; it must not blindly execute upstream installer scripts.
3. **Tier C — Flatpak applications:** integrate upstream Flatpak runtime, builder, portals, permissions and update model for desktop applications. Show the remote and requested permissions. Flathub is a separate trust domain and must not inherit trust from Deku implicitly.
4. **Tier D — Read-only RPM/DEB inspection, then gated compatibility:** inspect metadata, archive paths, dependencies, scriptlets/maintainer scripts, triggers, file conflicts, licenses and ABI requirements without executing package-provided code. Prefer rebuilding from source. Import payloads only when required semantics fit a declared compatibility profile and are re-tested. Reject or isolate unsupported packages.
5. **Tier E — AppImage, portable binaries and OCI/container/VM:** optional app-level paths for software not yet rebuilt natively. State the isolation boundary and host access. A container is not a VM; neither replaces host drivers, kernel modules, boot-critical components or system services.

Each tier needs an origin label, update owner, version/ABI constraints, removal semantics and an explicit trust decision. Unsupported packages should fail with an actionable reason instead of silently bypassing policy.

## Lessons from upstreams

| Project | Patterns to adopt | Limits and cautions |
|---|---|---|
| **Nix** | Immutable store paths, profiles, simultaneous package versions, garbage-collection roots and rollback semantics. | A content-addressed store does not solve FHS paths, ELF interpreters/RPATH, plugins, desktop files, D-Bus, services, udev or kernel modules automatically. Do not rewrite the Nix evaluator or adopt the entire Nix language without a measured requirement. |
| **Fedora / rpm-ostree / bootc** | Staged transactional deployments, pending changes, deployment history and a previous bootable deployment. bootc delivers a host OS as an OCI image while the host userspace still runs normally. | Do not operate two transaction owners over the same host paths. Compare an image-based deployment (OSTree/bootc) with Deku-managed root generations in a disposable-VM spike. Define ownership of /usr, boot artifacts, /etc merging and rollback before deciding. |
| **Void / XBPS / xbps-src** | Separate source recipes/building from binary package installation; explicit dependency and reverse-dependency handling, repository signatures, integrity checks, file ownership and a substantial test suite. xbps-src builds in a restricted master directory and should not run as root. | Reusing a recipe does not automatically trust its build scripts. Port recipe data and patches under review, pin source inputs and toolchains, restrict network during builds, and keep the builder separate from the package manager. |
| **Flatpak** | Reuse its maintained app/runtime format and sandbox/portal model. Prefer default-deny access with explicit filesystem, device, network and D-Bus permissions. | Not a system package format for kernels, initramfs, host daemons, drivers or core host libraries. App permissions and remote trust remain meaningful. |
| **The Update Framework (TUF)** | Root/targets/snapshot/timestamp roles, versioned and expiring metadata, threshold signing, key rotation, and detection of rollback, freeze, mix-and-match and mirror attacks. | A checksum authenticates neither the repository publisher nor metadata freshness. Do not invent a minimal signature format and call it equivalent to TUF. Evaluate maintained implementations and conformance tests. |
| **SLSA / in-toto** | Machine-readable build provenance and evidence that authorized steps ran over identified inputs; separate trusted orchestration from recipe-controlled build steps; strengthen isolation and signed attestations progressively. | Provenance is evidence, not proof that source code is benign. Keep review, testing, sandboxing and vulnerability response. |
| **Landlock / namespaces / seccomp** | Layer restrictions for filesystem access, mounts, process visibility and system calls. Run builds as unprivileged users with disposable state and resource limits. | Namespaces alone are not a complete security boundary; no single primitive replaces a threat model. Missing required isolation must fail closed for release builds. |

## Proposed package and repository trust boundaries

- **Source/recipe:** canonical schema pins source URL, immutable revision plus digest, patches, license expression, target architecture/ABI, dependencies, environment and build/test steps. Parsing recipes has no side effects.
- **Build worker:** fetch sources before entering the network-restricted build phase; verify digests; run as a non-root isolated worker with read-only input, a writable temporary output, bounded CPU/RAM/disk/time/processes, restricted syscalls and disposable state. Never expose signing keys to recipe steps.
- **Artifact:** record a canonical manifest (path, type, mode, symlink target, content digest, ownership/integration class), target ABI, build inputs, test evidence and provenance. Compare independent builds for selected high-risk/base packages.
- **Repository publication:** publish immutable content-addressed artifacts plus versioned signed metadata. Separate repository-root/delegation keys from builder-attestation keys; keep root keys offline and define rotation/revocation/recovery before public release.
- **Client verification:** bound metadata and artifact sizes; verify canonical schema, signatures, trust role, expiry/version, target architecture, digest and manifest. Persist highest trusted metadata versions to detect rollback. A stale or compromised mirror must not replace trusted metadata.
- **Plan and transaction:** produce a deterministic plan before mutation; detect dependency cycles, version conflicts, file collisions, disk-space problems, protected paths and kernel/boot implications. Download to a temporary location, verify, stage, journal state transitions, then activate. Recover interrupted transactions to a documented safe state.
- **Runtime integration:** install only integration types with explicit policies and tests. systemd units, D-Bus activation, desktop files/icons, shared-library cache, udev rules, kernel modules and configuration migration are distinct capabilities—not arbitrary package hooks.
- **State separation:** administrator configuration stays under /etc, mutable system data under /var, and user state in XDG locations. Uninstall must not remove user data or overwrite local configuration without a defined merge policy.
- **Privilege separation:** queries/planning run unprivileged. A narrow privileged helper accepts a validated transaction plan and revalidates sensitive invariants; it never interprets arbitrary package scripts.

## Proposed storage model and a key open decision

Prototype the Nix-inspired payload layout:

- /deku/store/<verified-content-id>/ — immutable payloads, writable only during staging and read-only after verification.
- /deku/profiles/system/<generation>/ — manifest of one coherent tested package set.
- /deku/var/transactions/ — durable journals and recovery records.
- /deku/var/cache/ — disposable downloads and cache.

This is a target design, not an implemented filesystem contract. Do not choose a live /usr switch mechanism by assumption. First build a disposable-VM spike comparing (A) complete Deku-managed root generations and (B) image-based deployment such as OSTree/bootc. Test power loss during activation, bootloader behavior, /etc merging, kernel/initramfs replacement, disk pressure, recovery and rollback. Select one owner for the host root; do not layer a custom generation switch on top of a second transaction manager for the same files.

## Kernel policy

As checked against kernel.org on 2026-10-23, Linux 7.3 is mainline dated 2026-10-18, while 7.2.12 is listed as stable dated 2026-10-21. Test 7.3 in a clearly marked experimental image; base stable milestones on a pinned stable kernel that passes Deku’s hardware, suspend/resume, graphics, storage, networking, update and recovery tests. Preserve a previous known-good kernel and boot entry. Pin source tag, signature, configuration, compiler/toolchain and patch series.

## Acceptance gates before a host-changing release

1. **Model/parser:** strict schemas, raw metadata size limits before deserialization, object/count bounds, canonical digest/version tokens, malformed-input and fuzz/property tests.
2. **Trust:** valid/invalid signatures, role separation, threshold policy, expired metadata, key rotation, revoked keys, stale mirrors, rollback/freeze/mix-and-match attacks, and compromised-key recovery.
3. **Dependency planner:** deterministic output, architecture/version constraints, conflicts, virtual provides, cycles, large graphs, and no network/filesystem/privilege side effects.
4. **Store:** corruption detection, immutability after verification, symlink/path traversal, concurrent writers and safe garbage collection.
5. **Transaction:** install/update/remove into a temporary root, collision handling, crash/power-loss injection at every state, idempotent recovery, configuration preservation and rollback.
6. **Build system:** no network after source acquisition, non-root isolation, resource caps, secret isolation, provenance, attestations and independent-build comparisons.
7. **Compatibility:** hostile/malformed RPM/DEB fixtures; prove scriptlets and maintainer scripts never execute during inspection; test unsupported dependency expressions and ABI mismatch rejection.
8. **System integration:** disposable VM boot, clean install, upgrade, failed update, previous-kernel boot, graphics/network/storage smoke tests and recovery.
9. **Desktop:** KDE-first smoke tests plus Flatpak runtime/update/removal/portal/permission tests; GNOME is a later profile sharing the tested base.
10. **Release:** pinned/reproducible inputs, signed artifacts and metadata, checksums, SBOM/provenance, known issues, security contact and published test evidence.

No ISO or “supports all packages” claim should be made until the relevant gates have passing automated evidence.

## Primary references

- Nix manual: https://nix.dev/manual/nix/latest/
- Nix store and profiles: https://nix.dev/manual/nix/2.30/store/
- bootc overview: https://bootc.dev/bootc/
- rpm-ostree administrator handbook: https://coreos.github.io/rpm-ostree/administrator-handbook/
- Void source package collection: https://github.com/void-linux/void-packages
- Void source package manual: https://github.com/void-linux/void-packages/blob/master/Manual.md
- XBPS project/capabilities: https://github.com/void-linux/xbps
- Flatpak documentation: https://docs.flatpak.org/en/latest/
- Flatpak sandbox and portals: https://docs.flatpak.org/en/latest/basic-concepts.html
- The Update Framework: https://theupdateframework.io/specification/latest/
- SLSA 1.2: https://slsa.dev/spec/v1.2/
- in-toto documentation: https://in-toto.io/docs/
- Landlock: https://landlock.io/
- Debian maintainer scripts: https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html
- Linux kernel release status: https://www.kernel.org/
