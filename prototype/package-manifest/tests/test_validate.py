import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "validate.py"
SPEC = importlib.util.spec_from_file_location("deku_manifest_validate", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def valid_manifest():
    return {
        "manifest_version": 0,
        "name": "hello",
        "version": "1.2.3",
        "release": 1,
        "summary": "Example package",
        "license": "MIT",
        "architectures": ["x86_64"],
        "source": {
            "url": "https://example.org/source.tar.gz",
            "sha256": "a" * 64,
        },
    }


class ManifestValidationTests(unittest.TestCase):
    def test_valid_manifest(self):
        self.assertEqual(MODULE.validate_manifest(valid_manifest()), [])

    def test_rejects_non_object_root(self):
        self.assertIn("manifest root must be a JSON object", MODULE.validate_manifest([]))

    def test_rejects_http_source(self):
        manifest = valid_manifest()
        manifest["source"]["url"] = "http://example.org/source.tar.gz"
        self.assertTrue(any("HTTPS" in error for error in MODULE.validate_manifest(manifest)))

    def test_rejects_invalid_hash(self):
        manifest = valid_manifest()
        manifest["source"]["sha256"] = "not-a-hash"
        self.assertTrue(any("sha256" in error for error in MODULE.validate_manifest(manifest)))

    def test_rejects_unknown_architecture(self):
        manifest = valid_manifest()
        manifest["architectures"] = ["mips"]
        self.assertTrue(any("architectures entries" in error for error in MODULE.validate_manifest(manifest)))

    def test_rejects_boolean_release(self):
        manifest = valid_manifest()
        manifest["release"] = True
        self.assertTrue(any("release must be int" in error for error in MODULE.validate_manifest(manifest)))

    def test_rejects_duplicate_architectures(self):
        manifest = valid_manifest()
        manifest["architectures"] = ["x86_64", "x86_64"]
        self.assertTrue(any("duplicates" in error for error in MODULE.validate_manifest(manifest)))


if __name__ == "__main__":
    unittest.main()
