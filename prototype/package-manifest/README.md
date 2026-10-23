# Deku package manifest prototype (v0)

This directory starts a platform-neutral package metadata prototype. It does **not** define the final package manager, repository format, dependency solver, or package build format.

## Goals

- Define a small, reviewable JSON manifest for source package metadata.
- Validate manifests with Python's standard library only.
- Keep the schema independent of the eventual base system and init system.
- Fail clearly on malformed or incomplete metadata.

## Validate a manifest

Run from the repository root:

```sh
python3 prototype/package-manifest/validate.py prototype/package-manifest/examples/hello.json
python3 -m unittest discover -s prototype/package-manifest/tests -v
```

## Status and limitations

This is an experimental v0 contract. It does not download or execute source code, resolve dependencies, build binaries, verify signatures, or install packages. A SHA-256 field is integrity metadata only; it is not a signature or proof of trust.

Changes to required fields should be discussed before stabilizing the format. Future work should add a formal schema, dependency metadata, provenance, signing, and reproducible-build tests only after requirements are agreed.
