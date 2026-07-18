#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("validate_profile.py")
DEFAULT_PROFILE = Path(__file__).resolve().parent.parent / "references" / "default-organization.json"


class ValidateProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repository = Path(self.temporary.name) / "repository"
        self.repository.mkdir()
        (self.repository / ".git").mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_validator(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repository", str(self.repository), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def write_profile(self, payload: dict) -> Path:
        root = self.repository / ".boss"
        root.mkdir(exist_ok=True)
        profile = root / "organization.json"
        profile.write_text(json.dumps(payload), encoding="utf-8")
        return profile

    def default_payload(self) -> dict:
        return json.loads(DEFAULT_PROFILE.read_text(encoding="utf-8"))

    def test_default_profile_reports_all_roles(self) -> None:
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(11, len(report["roles"]))
        self.assertEqual([], report["disabled_roles"])
        self.assertEqual(4, len(report["departments"]))

    def test_disabled_role_reports_unavailable_gates(self) -> None:
        payload = self.default_payload()
        next(role for role in payload["roles"] if role["slug"] == "nora")["enabled"] = False
        self.write_profile(payload)
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(["nora"], report["disabled_roles"])
        self.assertIn("acceptance evidence gate", report["unavailable"]["nora"])
        selected = self.run_validator("--role", "nora")
        self.assertEqual(1, selected.returncode)
        self.assertIn("Disabled requested role", selected.stderr)

    def test_custom_relative_charter_is_allowed_inside_boss_directory(self) -> None:
        payload = self.default_payload()
        root = self.repository / ".boss"
        root.mkdir()
        (root / "custom-product.md").write_text("# Product roles\n", encoding="utf-8")
        payload["departments"]["product"]["charter"] = "custom-product.md"
        self.write_profile(payload)
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stderr)
        report = json.loads(result.stdout)
        product = next(item for item in report["departments"] if item["slug"] == "product")
        self.assertTrue(product["charter"].endswith("/.boss/custom-product.md"))

    def test_legacy_profile_is_rejected_with_clean_break_message(self) -> None:
        payload = self.default_payload()
        payload["schema_version"] = 1
        payload["departments"]["executive"]["charter"] = "bundle://departments/executive/roles.md"
        self.write_profile(payload)
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("schema_version 2", result.stderr)
        self.assertIn("regenerated", result.stderr)

    def test_boss_cannot_be_disabled(self) -> None:
        payload = self.default_payload()
        next(role for role in payload["roles"] if role["slug"] == "boss")["enabled"] = False
        self.write_profile(payload)
        result = self.run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn("BOSS must be enabled", result.stderr)


if __name__ == "__main__":
    unittest.main()
