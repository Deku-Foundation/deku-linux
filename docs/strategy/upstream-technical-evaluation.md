# Upstream technical evaluation

**Status:** Initial review, not an architecture decision. No upstream source code has been imported by this document.

## Void Linux package workflow

The Void `void-packages` manual describes package templates that declare metadata and build phases such as fetch, extract, patch, configure, build, check, install, and package. This is a useful model because package intent is reviewable in version control and tests are an explicit phase. The repository also has a detailed contribution guide and a documented process for keeping forks synchronized with upstream.

Sources:
- https://github.com/void-linux/void-packages/blob/master/Manual.md
- https://github.com/void-linux/void-packages/blob/master/CONTRIBUTING.md
- https://github.com/void-linux/xbps

Deku should prototype a similarly explicit lifecycle, but should not copy templates wholesale before the applicable license, helper scripts, assumptions, and dependency model have been reviewed. We should compare XBPS/xbps-src reuse with other approaches using a small package experiment, not a full repository import as the first step.

## Nix and Nixpkgs lessons

The Nix ecosystem is worth studying for isolated build environments, explicit inputs, caching, and reproducibility workflows. Those are properties Deku can evaluate independently of choosing Nix as its package manager. Nixpkgs also demonstrates the scale and maintenance demands of a large package collection: automated checks and contributor conventions matter as much as the package expression format.

Sources:
- https://github.com/NixOS/nix
- https://github.com/NixOS/nixpkgs
- https://nixos.org/manual/nix/stable/

Deku should measure reproducibility by rebuilding the same inputs in independent environments and comparing artifacts. A declarative file, pinned source, or hash by itself does not prove that outputs are reproducible or trustworthy.

## Proposed experiments

1. Pick one small, low-risk upstream package with a permissive, verified license.
2. Record source URL, immutable version, source digest, build dependencies, runtime dependencies, and required patches.
3. Build it in a disposable, unprivileged environment using a candidate backend.
4. Run its tests and inspect the installed file list, ownership, permissions, and metadata.
5. Rebuild in a second clean environment and compare output hashes.
6. Compare effort, failure clarity, security boundaries, and update burden against an alternative backend.
7. Record results and the final recommendation in a numbered ADR before importing more packages.

## Current recommendation

Reuse mature tools where they solve a demonstrated problem. Keep Deku-owned integration, release policy, package metadata requirements, security controls, and documentation under Deku's governance. Avoid maintaining a fork unless a specific unmet requirement justifies the ongoing upstream merge burden.
