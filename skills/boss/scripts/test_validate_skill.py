#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parent.parent
SCRIPT = Path(__file__).with_name("validate_skill.py")


class ValidateSkillTests(unittest.TestCase):
    def run_validator(self, skill: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(skill)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_current_skill_is_valid(self) -> None:
        result = self.run_validator(SKILL)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_rejects_nested_discoverable_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "boss"
            shutil.copytree(SKILL, skill)
            nested = skill / "references" / "procedures" / "tdd" / "SKILL.md"
            nested.write_text("---\nname: tdd\ndescription: nested\n---\n", encoding="utf-8")
            result = self.run_validator(skill)
        self.assertEqual(1, result.returncode)
        self.assertIn("nested discoverable skill", result.stderr)

    def test_rejects_missing_procedure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "boss"
            shutil.copytree(SKILL, skill)
            (skill / "references" / "procedures" / "tdd" / "PROCEDURE.md").unlink()
            result = self.run_validator(skill)
        self.assertEqual(1, result.returncode)
        self.assertIn("procedure set mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()
