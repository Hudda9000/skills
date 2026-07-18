#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("init_project.py")
PROFILE_VALIDATOR = Path(__file__).with_name("validate_profile.py")


class InitProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repository = Path(self.temporary.name) / "sample-repository"
        self.repository.mkdir()
        (self.repository / ".git").mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_script(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--repository",
                str(self.repository),
                "--organization-name",
                "Sample Company",
                "--organization-slug",
                "sample-company",
                *arguments,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_initializes_schema_two_profile_and_decision_log(self) -> None:
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        profile_path = self.repository / ".boss" / "organization.json"
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        self.assertEqual(2, profile["schema_version"])
        self.assertEqual({"name": "Sample Company", "slug": "sample-company"}, profile["organization"])
        self.assertTrue(
            all(department["charter"].startswith("boss://departments/") for department in profile["departments"].values())
        )
        self.assertEqual(11, len(profile["roles"]))
        self.assertTrue((self.repository / ".boss" / "README.md").is_file())
        self.assertTrue((self.repository / ".boss" / "decisions.md").is_file())
        validated = subprocess.run(
            [sys.executable, str(PROFILE_VALIDATOR), "--repository", str(self.repository)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, validated.returncode, validated.stderr)

    def test_repeated_initialization_preserves_existing_state(self) -> None:
        self.assertEqual(0, self.run_script().returncode)
        decisions = self.repository / ".boss" / "decisions.md"
        decisions.write_text("# Decisions\n\nKeep this.\n", encoding="utf-8")
        profile = self.repository / ".boss" / "organization.json"
        original_profile = profile.read_text(encoding="utf-8")
        result = self.run_script()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("# Decisions\n\nKeep this.\n", decisions.read_text(encoding="utf-8"))
        self.assertEqual(original_profile, profile.read_text(encoding="utf-8"))
        report = json.loads(result.stdout)
        self.assertIn(".boss/decisions.md", report["preserved"])
        self.assertIn(".boss/organization.json", report["preserved"])

    def test_rejects_invalid_slug_without_writing(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--repository",
                str(self.repository),
                "--organization-name",
                "Sample Company",
                "--organization-slug",
                "Not Valid",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("lowercase kebab-case", result.stderr)
        self.assertFalse((self.repository / ".boss").exists())


if __name__ == "__main__":
    unittest.main()
