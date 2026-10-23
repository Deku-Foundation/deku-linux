# Initial Threat Model

- **Status:** Draft
- **Date:** 2026-10-23
- **Scope:** Future package, build, update, and image delivery systems. This is not a security certification.

## Assets to protect

- source repositories and release branches;
- package recipes, patches, and dependency metadata;
- build workers, caches, and artifacts;
- repository metadata and signing keys;
- release images, update channels, and user trust;
- vulnerability reports and maintainer accounts.

## Threat actors and failure sources

- compromised upstream source or dependency;
- malicious or compromised contributor account;
- untrusted pull request attempting to influence a build;
- compromised CI action, runner, or build dependency;
- theft or misuse of a signing credential;
- compromised package mirror or transport;
- accidental maintainer error, faulty update, or corrupted storage;
- unsupported hardware or an untested upgrade path.

## Trust boundaries

1. Public contributions are untrusted until reviewed and validated.
2. Build execution is separate from release signing and publication.
3. Package sources and dependencies are verified before use.
4. A mirror may be unavailable or compromised; clients must verify signed metadata and package integrity.
5. Release artifacts must be traceable to reviewed source and a documented build process.
6. Recovery media and instructions must remain available when an update fails.

## Initial controls

- enable multi-factor authentication for maintainers and use least privilege;
- protect the default branch and require review where supported;
- pin third-party CI actions to full commit SHAs and minimize workflow permissions;
- avoid secrets in pull-request workflows;
- isolate package builds and avoid unnecessary root privileges;
- record immutable source revisions, checksums, licenses, logs, and artifact hashes;
- separate signing keys from build workers; document backup, rotation, revocation, and incident procedures;
- verify signed repository metadata and package hashes on clients;
- test failed and interrupted updates, rollback or recovery, and disk-space exhaustion;
- publish vulnerability reporting instructions and supported-version policy.

## Residual risks

These controls reduce risk but do not eliminate compromised upstreams, malicious maintainers, kernel vulnerabilities, hardware faults, or all build-platform compromises. The project must publish limitations and periodically review the model.

## Review triggers

Review this model before publishing binary packages, before the first public image, after a security incident, and when the trust or update architecture changes.
