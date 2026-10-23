# Initial Architecture Principles

- **Status:** Accepted project principles; not a substitute for component ADRs.
- **Date:** 2026-10-23

## Context

A distribution combines packages, build pipelines, boot, updates, security, releases, and user experience. Early choices can be expensive to reverse, so decisions should be explicit and testable.

## Principles

### Start narrow

The initial target is x86_64. Additional architectures and desktop environments require evidence of maintainer capacity and automated test coverage.

### Prefer upstream components

Use established upstream projects unless a documented requirement cannot be met. Record the rationale and upstream status for maintained patches.

### Separate build, signing, and publication privileges

Build workers must not possess long-lived release-signing secrets. Signing and publication should be separate, auditable stages with narrowly scoped credentials.

### Treat packages as supply-chain artifacts

Record source locations, immutable revisions or checksums, license metadata, build dependencies, logs, and output hashes. Verify source integrity before compilation.

### Design updates and recovery together

Plan for interruption, rollback or recovery, disk-space limits, and diagnosis of failed upgrades.

### Make claims evidence-based

Claims such as secure, hardened, reproducible, compatible, and stable require documented scope and test evidence.

### Record consequential choices

Use ADRs for ABI, package format, trust roots, boot/update model, release cadence, and compatibility guarantees.

## Decisions intentionally left open

Separate ADRs must decide glibc versus musl; systemd versus runit/OpenRC or another option; package manager and recipe format; rolling versus fixed releases; kernel policy; image composition; desktop environment; and package signing format.

## Review triggers

Revisit these principles if target audience, maintainer capacity, security model, or supported hardware changes materially.
