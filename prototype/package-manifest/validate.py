#!/usr/bin/env python3
"""Validate a Deku package manifest v0 without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9+._-]{0,127}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
ALLOWED_ARCHITECTURES = {"x86_64", "aarch64", "noarch"}


class ManifestError(ValueError):
    """Raised when a manifest does not satisfy the v0 contract."""


def validate_manifest(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest root must be a JSON object"]

    required = {
        "manifest_version": int,
        "name": str,
        "version": str,
        "release": int,
        "summary": str,
        "license": str,
        "architectures": list,
        "source": dict,
    }
    for field, expected_type in required.items():
        if field not in data:
            errors.append(f"missing required field: {field}")
        elif type(data[field]) is not expected_type:
            errors.append(f"{field} must be {expected_type.__name__}")

    if errors:
        return errors

    if data["manifest_version"] != 0:
        errors.append("manifest_version must be 0 for this prototype")
    if not NAME_RE.fullmatch(data["name"]):
        errors.append("name must use lowercase letters, digits, '+', '.', '_', or '-'")
    if not data["version"].strip():
        errors.append("version must not be empty")
    if data["release"] < 1:
        errors.append("release must be an integer greater than or equal to 1")
    if not data["summary"].strip():
        errors.append("summary must not be empty")
    if not data["license"].strip():
        errors.append("license must not be empty")

    architectures = data["architectures"]
    if not architectures:
        errors.append("architectures must contain at least one architecture")
    elif any(not isinstance(arch, str) or arch not in ALLOWED_ARCHITECTURES for arch in architectures):
        errors.append(
            "architectures entries must be one of: "
            + ", ".join(sorted(ALLOWED_ARCHITECTURES))
        )
    elif len(set(architectures)) != len(architectures):
        errors.append("architectures must not contain duplicates")

    source = data["source"]
    for field in ("url", "sha256"):
        if field not in source:
            errors.append(f"source is missing required field: {field}")
        elif not isinstance(source[field], str):
            errors.append(f"source.{field} must be a string")

    if isinstance(source.get("url"), str):
        parsed = urlparse(source["url"])
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append("source.url must be an absolute HTTPS URL")
    if isinstance(source.get("sha256"), str) and not SHA256_RE.fullmatch(source["sha256"]):
        errors.append("source.sha256 must contain exactly 64 hexadecimal characters")

    return errors


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print(f"usage: {Path(sys.argv[0]).name} MANIFEST.json", file=sys.stderr)
        return 2

    path = Path(args[0])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}", file=sys.stderr)
        return 2

    errors = validate_manifest(data)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"valid manifest: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
