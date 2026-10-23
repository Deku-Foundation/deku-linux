# ISO build gap analysis and repository plan

- **Status:** Research and implementation plan; not an accepted architecture decision.
- **Reviewed:** 2026-10-23
- **Immediate target:** A clearly labelled, x86_64 bootable proof-of-concept image, followed by a traceable developer ISO only after the package and root-filesystem path is real.
- **Release rule:** Do not publish or advertise a supported Deku ISO until the release gates below pass.

## Executive decision

Do not create another repository for the ISO. The original eight core repositories cover the integration path; the organization now also has supplementary repositories for profiles, testing, releases, trust, desktop integration, themes, kernel tracking, mirrors, updates and Rukn. Their existence does not mean those capabilities are implemented. The missing pieces are still working implementations and integration contracts, not repository names.

Use upstream tools where they reduce risk, but do not quietly turn Deku into a Void, Fedora, NixOS, or Arch derivative while describing it as an independent distribution. A temporary upstream-based boot demo must be labelled as a prototype and must not be presented as a native Deku system.

## What upstream projects teach us

| Project/tool | Reuse as a reference for | Important boundary |
|---|---|---|
| Void void-packages + XBPS | Recipe/build separation, binary repositories, package integrity and repository signatures | XBPS and Void package conventions are not implemented by Deku. Do not claim compatibility without an explicit adapter or decision. |
| Void void-mklive | Live-rootfs and ISO assembly workflow, boot media, installer-image layout | It expects the Void/XBPS ecosystem; it is not a drop-in image generator for Deku's future native package format. |
| NixOS nixos-rebuild build-image | Declarative configuration and pinned build inputs | Adopting the full NixOS system model would be an architectural choice, not a neutral helper. |
| Fedora Lorax / livemedia-creator / Anaconda | Mature installer-media pipeline, live images, automated installation and test practices | Deep integration expects Fedora/RPM ecosystem assumptions; evaluate components and licensing before reuse. |
| systemd/mkosi | General-purpose OS image assembly, image layouts, initramfs/UKI-related workflows and integration tests | A builder cannot replace package building, authenticated inputs, repository metadata, or a trusted release process. Test whether it can consume the chosen rootfs/package flow. |
| archlinux/archiso | Transparent profile-based live media configuration | It is Arch-specific and maintained on Arch Linux GitLab; do not assume its scripts are a general-purpose distro backend. |
| OSInside/kiwi | Declarative appliance/image descriptions and image tests | Evaluate only if it fits the chosen package/rootfs strategy; avoid adopting multiple competing image builders. |
| bootc / OSTree family | Image-based operating-system delivery and transactional updates | This would affect system updates, boot flow, and recovery. Compare against generation-based rootfs before choosing one; do not stack both transaction owners. |

Upstream references:
- https://github.com/void-linux/void-packages
- https://github.com/void-linux/xbps
- https://github.com/void-linux/void-mklive
- https://nix.dev/tutorials/nixos/building-bootable-iso-image.html
- https://github.com/weldr/lorax
- https://github.com/rhinstaller/anaconda
- https://github.com/systemd/mkosi
- https://gitlab.archlinux.org/archlinux/archiso
- https://github.com/OSInside/kiwi
- https://github.com/bootc-dev/bootc

## Repository gap inventory

### Core repositories: keep and implement

1. **deku-linux** — project charter, accepted ADRs, threat model, roadmap, release criteria and integration contracts. It must not become a dumping ground for build scripts.
2. **deku-recipes** — reviewed, versioned recipe metadata, source pins, licenses, patch references and maintainer/review records. A recipe validator is not a package builder.
3. **deku-build** — verified source acquisition, disposable unprivileged build workers, resource limits, network policy, logs, output manifests, provenance and reproducibility experiments. Keep signing keys out of workers.
4. **deku-pkg** — define package format and dependency/version semantics, authenticate repository metadata, validate file ownership/path safety, install and remove packages safely, and implement journaled transactions/recovery before system use.
5. **deku-system** — own system profiles, pinned package manifests, rootfs assembly, kernel/initramfs integration, boot configuration and image-builder adapter. This is the natural owner for the ISO pipeline.
6. **deku-installer** — device discovery, safe partition plan, explicit destructive-action confirmation, filesystem creation, rootfs deployment, bootloader setup and post-install validation. Start with VM-only tests.
7. **deku-infra** — CI/release workflows, artifact storage/publication policy, mirror strategy, signing-key custody design, backups and incident response. Do not pretend documentation is a running production service.
8. **Deku-Foundation.github.io** — public status, architecture, documentation, release notes and verified download links. Never show an ISO download link until a real artifact and its verification files exist.

### Capabilities currently missing (not new repositories)

- Accepted platform ADRs: architecture/ABI, libc, init/service manager, kernel policy, boot mode, filesystem and release/update model.
- A real build of one harmless test package inside a disposable, unprivileged environment.
- A source fetcher that verifies immutable revisions and content digests and defends against unsafe redirects/DNS/IP targets.
- An authenticated binary repository format: signed metadata, expiry/freshness, rollback protection, key rotation and revocation. SHA-256 alone does not authenticate a publisher.
- A small real package set sufficient to construct a root filesystem.
- A repeatable rootfs assembler with a pinned manifest and an explicit ownership boundary for /etc, /usr, /var and boot assets.
- Kernel, firmware, initramfs, bootloader and live-media configuration.
- A VM test harness that checks boot, console/login, storage detection, network basics, shutdown and failure diagnostics.
- SBOM, build provenance/attestation, checksums and signed release metadata.
- An installer integration path, only after the live image can boot and the package/rootfs format is stable.
- Release publication and retention that keep generated ISO files out of ordinary Git history.

## Supplementary repositories that now exist

These repositories have been created and seeded with scope/status documentation. Treat them as real project boundaries, but do not invent work or claim services exist just to populate them.

| Repository | Intended ownership | Current honest status |
|---|---|---|
| `deku-profiles` | Declarative architecture/desktop profiles and package selection | Experimental Fedora 44 x86_64 UEFI profile; no independently validated image input yet |
| `deku-tests` | Shared integration contracts, disposable VM acceptance and recovery tests | Unit-tested QEMU/UEFI serial-marker harness; no Deku ISO has passed it yet |
| `deku-release` | Release manifests, acceptance evidence and artifact promotion | Manifest contract only; no release pipeline |
| `deku-signing` | Repository/release trust policy, keys, rotation and verification integration | Threat-model proposal; no production keys or signing service |
| `deku-updater` | Client-side update orchestration after package transactions are safe | Future component; no update engine |
| `deku-kernel` | Upstream Linux configuration and a narrow, justified patch queue | Tracking scope only; not a Linux fork or kernel build service |
| `deku-desktop` | KDE Plasma integration, defaults and desktop acceptance tests | Bootstrap scope; no supported desktop image |
| `deku-themes` | Original, licensed theme and branding assets | Bootstrap repository; asset provenance must be recorded |
| `deku-mirrors` | Mirror policy, health and eventual repository synchronization | Planning only; no production mirrors |
| `deku-rukn` | Independent Arabic-first programming language and Rust toolchain | Separate experimental language project; not an ISO dependency |
| `.github` | Organization-wide public profile and shared project guidance | Organization metadata; not a system component |
| `Deku-Foundation.github.io` | Multilingual website and verified public release information | Static website; no ISO download until a real artifact passes acceptance |

No additional repository is needed for the first ISO. Keep profiles, image building, package trust and release contracts in their defined owners; add source code only when it has a concrete tested responsibility. In particular, do not build a mirror, signing service, updater, or physical-disk installer before the relevant repository format and recovery behavior exist.

## Proposed implementation sequence

The first Fedora 44/Lorax pipeline now exists on `deku-system/dev`. Its first attempt installed the image's packages and generated the live root filesystem, but ISO generation failed because the GRUB BIOS module directory lacked `moddep.lst`. The Kickstart now explicitly includes GRUB PC and module packages, the boot-marker service no longer orders itself after `multi-user.target`, and the next run must still prove the result. This is a build experiment, not a claim that an ISO is ready.

### Gate A — decide the platform (no ISO claim yet)

- [ ] Accept ADRs for x86_64 ABI/libc, init/service manager, kernel/LTS policy, UEFI-first boot scope, filesystem and release model.
- [ ] Decide whether Deku is initially a native independent distribution or a clearly labelled upstream-based technology demo. Do not mix the two claims.
- [ ] Select exactly one image assembly backend after a small technical spike; compare mkosi and native scripting against the selected package/rootfs model.
- [ ] Decide rootfs update/rollback ownership: generation-based root or image-based OSTree/bootc-style. Document recovery and migration costs.

### Gate B — first traceable package and rootfs

- [ ] Build one harmless package in an unprivileged disposable worker with network disabled during build execution.
- [ ] Emit source pin, toolchain/configuration identity, logs, artifact digest, license data and provenance.
- [ ] Install a small base package set into a staged rootfs without mutating the host.
- [ ] Verify file ownership, paths, permissions, dynamic linking, service startup and boot dependencies.
- [ ] Produce an SBOM and machine-readable rootfs manifest.

### Gate C — first bootable VM ISO

- [ ] Build an x86_64 UEFI ISO from pinned inputs.
- [ ] Verify the ISO filesystem and bootloader configuration; test Secure Boot only if the full signing chain is implemented.
- [ ] Boot in QEMU/KVM or another disposable VM; capture logs and exit status.
- [ ] Test live boot, console/login, storage/network basics, shutdown and failure diagnostics.
- [ ] Run at least one clean rebuild and compare outputs; document any non-determinism instead of claiming reproducibility.
- [ ] Publish only as a development artifact with checksums, provenance, limitations and a clear non-production warning.

### Gate D — installable developer preview

- [ ] Add a VM-tested installer path, with explicit target-disk confirmation and safeguards against host-device access.
- [ ] Test fresh install, reboot, package update, interrupted operation and recovery in disposable VMs.
- [ ] Authenticate repository metadata and test expired metadata, rollback attempts, invalid signatures and key rotation.
- [ ] Publish signed checksums, SBOM, provenance/attestation, source revision, build instructions and release notes.
- [ ] Only then add a public ISO download to the website.

## Modern supply-chain controls

Use GitHub Actions as orchestration, not as proof of trust by itself:
- Pin third-party Actions to reviewed full commit SHAs where practical.
- Keep GITHUB_TOKEN permissions minimal and separate untrusted pull-request builds from release credentials.
- Use public-repository GitHub artifact attestations where suitable; verify the attestation independently.
- Produce SBOMs (SPDX or CycloneDX), build provenance and checksums for each published artifact.
- Keep signing keys outside build workers and source control; prefer a documented offline or tightly controlled signing boundary.
- Pin toolchains, package revisions and configuration. Reproducibility is a measured result, not a label.
- Retain test logs and evidence for each image; never let a green metadata-validation job imply that an ISO booted.

Reference: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations

## Definition of done for the first ISO

The first ISO milestone is complete only when a reviewer can reproduce the documented build from a clean checkout or controlled runner, verify its provenance and checksums, boot it in a disposable VM, inspect the test evidence, and understand exactly which components are native Deku code versus upstream software.

A successful CI syntax test, a validated manifest, or a generated ISO file alone does not satisfy this definition.
