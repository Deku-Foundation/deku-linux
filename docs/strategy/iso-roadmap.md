# ISO Roadmap

Status: engineering proposal, 2026-10-23.

## Decision
Deku has seven component repositories, but they are prototypes rather than a complete image pipeline. Do not create empty repositories to reserve names. Keep `main` and `dev`; develop on `dev` and promote only after checks pass.

## Repository gaps
- `deku-profiles` — the only recommended future repository, created only when a real KDE Plasma x86_64 profile exists and needs separate maintenance. Until then keep profiles in `deku-system`.
- `deku-tests` — defer; add only when VM boot/installer/recovery tests become genuinely shared across projects.
- `deku-release` — defer; begin release manifests and publication in `deku-infra` until release complexity warrants a split.

Do not create `deku-kernel`, `deku-init`, `deku-libc`, `deku-desktop`, `deku-themes`, `deku-mirrors`, `deku-signing`, `deku-updater` or a repository for each package now. Use upstream components and the existing recipe directories unless independent maintenance is justified.

## Existing responsibilities
- `deku-linux`: architecture decisions, ADRs and policies.
- `deku-recipes`: reviewed package recipes, immutable source pins and license metadata.
- `deku-build`: isolated unprivileged builds, input/output manifests and provenance.
- `deku-pkg`: native package client and repository trust; not yet production-ready.
- `deku-system`: profiles, root filesystem composition, initramfs and image assembly.
- `deku-installer`: installer integration and safe storage operations; currently validation-only.
- `deku-infra`: CI, artifact retention, publication and release trust boundaries.
- `Deku-Foundation.github.io`: public status and evidence, not a build system.

## Upstream tools to evaluate
- Void `void-packages`/`xbps-src`: https://github.com/void-linux/void-packages
- Fedora `mock`: https://github.com/rpm-software-management/mock
- Arch `archiso`: https://github.com/archlinux/archiso
- Fedora `Lorax` and `livemedia-creator`: https://github.com/weldr/lorax
- Fedora installer Anaconda: https://github.com/rhinstaller/anaconda
- NixOS image building in `nixpkgs`: https://github.com/NixOS/nixpkgs
- systemd `mkosi`: https://github.com/systemd/mkosi
- OSTree/bootc for atomic updates: https://github.com/ostreedev/ostree and https://github.com/bootc-dev/bootc
- in-toto provenance: https://github.com/in-toto/attestation

These are evaluation candidates, not a decision to adopt all of them. NixOS image generation is now supported through `nixos-rebuild build-image`; do not start a new project around the deprecated `nixos-generators` repository.

## Architecture decisions required
Before committing to an image pipeline, record decisions for: independent distro versus bootstrap/derivative strategy; initial libc/ABI; init and service manager; UEFI bootloader, kernel and initramfs; package/update model; mutable versus atomic image model; build isolation and network policy; installer scope.

## Minimal ISO gates
1. Approve the architecture decisions and define what the prototype does not support.
2. Pin source revisions, package versions, toolchain, image builder and configuration; verify digests and license metadata.
3. Use a mature image builder if compatible; produce a minimal root filesystem, kernel, initramfs, bootloader configuration and ISO from one declarative profile.
4. Boot the ISO in disposable QEMU/KVM UEFI x86_64 CI; check userspace/init, root mount, services and console/desktop; retain logs.
5. Test installation on disposable virtual disks only after boot succeeds.
6. Publish ISO, SHA-256, provenance/SBOM, source commit, test evidence and known limitations. Do not claim production readiness because one boot passed.

## Current blockers
`deku-build` does not execute isolated builds; `deku-recipes` does not build packages; `deku-pkg` does not install packages or authenticate a production repository; `deku-system` does not assemble rootfs/ISO; `deku-installer` does not write disks; `deku-infra` does not operate production package/signing/release services. More repositories do not fix these gaps; integration is the priority.

## Branch policy
Keep persistent `main` and `dev` only. Work on `dev`; merge/promote to `main` only after review and required checks. Avoid persistent feature branches. Never force-push or delete `main`/`dev`.