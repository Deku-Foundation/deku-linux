# Upstream Code Reuse Map: Building Deku from Proven Components

- **Status:** Engineering proposal for implementation review.
- **Last reviewed:** 2026-10-25.
- **Product rule:** Deku is an independent distribution. Fedora, Void, Nix, Alpine and Debian are upstream code/reference sources, not Deku runtime bases.
- **Current focus:** Reuse and adapt proven package/build/bootstrap/installer infrastructure; connect it through Deku-owned contracts; do not prioritize an ISO ahead of those capabilities.

## 1. The intended result

Deku should not rewrite everything from zero. It should own the distribution integration, package/recipe policy, configuration, system profile, identity, release process and user experience, while reusing maintained upstream implementations where their code, interfaces and licenses fit.

"Independent distribution" means the installed system is assembled from an explicitly selected and versioned Deku package closure, uses Deku-controlled repository metadata and updates, and does not require another distribution's root filesystem, package database or repositories at runtime. It does not mean rewriting Linux, glibc, compilers, systemd, GRUB, cryptography or an installer without a concrete reason.

No runtime Fedora image is part of this target. Anaconda is evaluated strictly as reusable installer source/components; that does not make Fedora the system base.

## 2. Void's actual architecture — what we should learn

Void is useful because its repositories form a working end-to-end package ecosystem:

- `void-packages` contains package templates, shared build policy, patches, configuration, bootstrap logic and the `xbps-src` build orchestrator. A template builds to a staging destination and produces an XBPS binary package.
- `xbps` is the package manager and its supporting library/tools. Its responsibilities include package metadata, dependency planning, installation state, package integrity, repository indexes and signing tools.
- `void-mklive` produces root filesystems, live/install media and architecture-specific images. It calls XBPS and assumes Void's package conventions; upstream explicitly says it is not guaranteed to work on other distributions or in containers.
- The package/bootstrap docs distinguish a binary bootstrap from a source bootstrap. A source bootstrap needs staged rebuilds because initial binaries built with the host toolchain are not yet independent or reproducible.

Primary sources:
- https://github.com/void-linux/void-packages
- https://github.com/void-linux/xbps
- https://github.com/void-linux/void-mklive
- https://docs.voidlinux.org/xbps/repositories/
- https://docs.voidlinux.org/installation/live-images/

The key lesson is the connected pipeline, not a set of repository names. Deku must achieve the same operational chain with Deku recipes, Deku-controlled artifacts/metadata, a trusted package transaction path and a rootfs/image assembler.

## 3. Map upstream responsibilities to the repositories that already exist

| Upstream capability | Deku owner today | Required adaptation / implementation |
|---|---|---|
| `void-packages`: package templates, patches, build options, dependency declarations | `deku-recipes` | Evolve the schema from descriptive metadata into reviewed, versioned build recipes with immutable source and patch digests, license expression, dependencies by build/host/runtime class, test commands, outputs and maintainer/review history. Do not copy the entire Void tree and assume it is portable. |
| `xbps-src`: source acquisition, bootstrap, package build roots and package output orchestration | `deku-build` + `deku-recipes` | Implement a real verified fetcher, disposable unprivileged build worker, bootstrap stages, build environment/toolchain lock, package assembly, archive inspection, logs, results and provenance. The current plan validator is not a build worker. |
| `xbps`: package format, repository tools, dependency solver, installation state and transactions | `deku-pkg` | Make an explicit architecture decision: adapt/fork proven XBPS source as the first package substrate, or continue the new Rust implementation and accept responsibility for reaching equivalent install/upgrade/recovery coverage. Do not maintain two competing package formats or transaction owners. |
| `void-mklive`: rootfs, initramfs, boot assets and ISO/image layout | `deku-system` | Port or selectively reuse generic image/rootfs/boot-layout routines only after tracing license and dependencies. Replace XBPS-specific package resolution with an input contract that accepts a verified, locked Deku rootfs. Add UEFI first; treat BIOS and Secure Boot as separate gates. |
| Installer flow and storage handling | `deku-installer` | Evaluate Anaconda's reusable source and integration seams, or another mature installer if its backend fits better. Connect it to Deku package deployment and boot setup; do not inherit DNF/RPM as an implicit system requirement. |
| Declarative build/profile inputs | `deku-profiles` | Keep separate native Deku bootstrap and minimal-system profiles. Lock exact package/version/source/artifact identities; never repurpose a foreign-distro profile as the production manifest. |
| System/release validation | `deku-tests` | Extend beyond metadata and a boot marker: install, package ownership, upgrade, interrupted transaction, rollback, kernel/initramfs, networking and recovery tests in disposable VMs. |
| Repository trust, signing, publishing, mirroring and promotion | `deku-signing`, `deku-release`, `deku-infra`, `deku-mirrors` | Implement the actual trust roots, signed/versioned repository metadata, publication, mirror verification, key rotation/revocation, retention and promotion gates. Keep signing keys outside build workers and untrusted PR jobs. |

These repositories already cover the principal responsibility boundaries. The present deficiency is mostly missing executable implementations and integration contracts, not missing repository names.

## 4. Should we create another repository?

**Not yet. Do not create another repository merely to imitate Void's directory/repository layout.** Its `xbps-src` lives in `void-packages`, and bootstrap recipes are part of its package/build system. The equivalent Deku responsibilities can stay in the existing repositories:

- bootstrap package recipes and pinned bootstrap manifest: `deku-recipes`;
- bootstrap/build execution and build stages: `deku-build`;
- package artifacts, metadata/index client and transaction implementation: `deku-pkg`;
- locked closure and target profile: `deku-profiles`;
- rootfs/boot/image assembly: `deku-system`.

A separate `deku-repo` service is not required to start. First define and implement repository-index generation and authenticated metadata as a package-system interface; its client/format belongs with `deku-pkg`, promotion belongs with `deku-release`, and hosting/mirroring belongs with `deku-infra`/`deku-mirrors`. Split it into a repository only if it later acquires an independent service lifecycle, operators, or security boundary.

A dedicated `deku-bootstrap` repository is similarly unnecessary at this stage. Create one only if the seed toolchain/artifacts need independent governance and lifecycle after the initial staged-bootstrap design is implemented.

## 5. Reuse code, not assumptions

Before copying a file or importing an upstream repository, record its exact commit/tag, license expression, copyright and NOTICE files, changed-file list, rationale, upstream update procedure and maintenance owner.

- **XBPS:** upstream documents a 2-clause BSD license, which permits adaptation subject to preserving the required notices and disclaimer. It is C and has meaningful tested package/install/repository functionality. Evaluate this as an actual code-reuse candidate rather than assuming a new Rust package manager is automatically more economical.
- **void-packages:** its top-level `COPYING` has a permissive 2-clause BSD notice for the collection, but each package source, patch and embedded file retains its own licensing obligations. A template contains Void/ XBPS conventions and sometimes Void-specific patches; adapt individual recipes and preserve their provenance instead of claiming the entire recipe tree can be used unchanged.
- **void-mklive:** its scripts are closely coupled to XBPS and Void's boot/rootfs conventions. Port only the parts whose dependencies and licensing have been verified; replace package resolution with a Deku rootfs interface.
- **Nixpkgs:** its MIT license applies to repository expressions/build code, not automatically to the upstream packages or all bundled patches. Its useful lessons are dependency closure, declarative inputs and controlled rebuilds.
- **Anaconda:** the upstream repository is GPL-2.0. Reusing/deriving substantial code requires compatible distribution terms and preservation of notices, plus an audit of its installer-service dependencies. Taking its installer code does not require taking Fedora as the runtime base.
- **Package sources and assets:** every upstream package and desktop/theme asset still needs its own license/provenance review.

The license of a repository's build scripts is not a blanket license for every program those scripts build.

## 6. The practical bootstrap sequence we must implement

This is the first functional milestone, inspired by `xbps-src` bootstrap and staged toolchain methods such as Linux From Scratch:

1. **Seed manifest:** define a very small, version-pinned bootstrap set: compiler/binutils, libc headers and runtime, shell/core utilities, archive tools, build tools and necessary certificates. Record the source revision, source digest, licence and bootstrap exception for each seed.
2. **Stage 0:** use an explicitly identified host toolchain or trusted seed artifacts to create the first build environment. Mark it as a bootstrap input, never as a reproducible final artifact.
3. **Stage 1:** rebuild the foundational toolchain and core libraries in the isolated Deku build environment using the seed outputs; capture complete build inputs and output digests.
4. **Stage 2:** rebuild the same bootstrap set using Stage 1 outputs, then compare independent builds where feasible. Define precisely which host paths, timestamps, locale, environment and tool versions must be normalized.
5. **First native package:** build one small, license-clear package through the complete path: recipe → verified source → isolated build → real artifact → output verification → authenticated local repository metadata → dependency/install plan.
6. **Minimal rootfs:** resolve and lock the closure, compose a Deku-owned rootfs, add upstream Linux/initramfs/bootloader components as pinned packages, and boot it in a disposable VM.
7. **Installer and update path:** only after rootfs boot and package installation/upgrading work, integrate installer storage operations, release media and recoverable updates.

Bootstrap is a special trust boundary. A first-stage binary can be necessary, but it must be explicitly recorded, replaced by a rebuilt output where possible, and never silently become a permanent dependency on a foreign distribution.

## 7. Decisions and gates

1. **Package manager decision (urgent):** compare (A) adopting/adapting XBPS as the first implementation and focusing Deku's engineering on its recipes/integration, against (B) continuing the Rust manager and implementing its full production semantics. Decide before adding more package format or transaction code.
2. **Recipe/build contract:** specify stable recipe fields and build-environment identity. Recipes are reviewed executable instructions and must never run on a trusted host with secrets.
3. **Repository trust:** define the signed metadata/index format and lifecycle; use TUF-compatible roles or the existing `tough` integration rather than inventing cryptographic protocols.
4. **Bootstrap profile:** create a non-empty, explicitly pinned Deku bootstrap closure. Current example manifests and digest values are fixtures, not packages or usable seed artifacts.
5. **System-root update owner:** choose one transactional model and prove rollback/recovery. Do not stack two mechanisms that both mutate the same root.
6. **Image builder:** port the generic live-rootfs/boot/ISO stages from Void only after the rootfs contract exists; image generation consumes Deku artifacts and must not fetch another distribution's runtime package set.
7. **Promotion:** require source/license inventory, artifact hashes, package inventory/SBOM, provenance, repository signature checks and clean VM install/upgrade/recovery evidence before supporting a release.

## 8. Acceptance rule

A milestone counts as implemented only when source code, integration tests and reproducible evidence exist. A schema validator, repository name, sample manifest or successful compile does not count as a working package builder, package repository, installer or system image.
