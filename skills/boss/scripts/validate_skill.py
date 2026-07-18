#!/usr/bin/env python3
"""Validate the self-contained OpenCode BOSS skill using the standard library."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_PROCEDURES = {
    "ask-matt",
    "code-review",
    "codebase-design",
    "create-issue",
    "diagnosing-bugs",
    "domain-modeling",
    "grill-with-docs",
    "implement",
    "improve-codebase-architecture",
    "prototype",
    "research",
    "resolving-merge-conflicts",
    "setup-boss",
    "setup-matt-pocock-skills",
    "tdd",
    "to-spec",
    "to-tickets",
    "triage",
    "wayfinder",
}
FORBIDDEN = {
    ".codex" + "-plugin": "legacy plugin manifest reference",
    "agents/" + "openai.yaml": "legacy UI metadata reference",
    "boss:" + "boss": "qualified legacy skill selector",
    "boss:" + "setup-boss": "qualified legacy setup selector",
    "HERDR" + "_ENV": "legacy multiplexer environment dependency",
    "HERDR" + "_WORKSPACE_ID": "legacy multiplexer workspace dependency",
}


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    require(text.startswith("---\n"), f"{path} must start with YAML frontmatter")
    parts = text.split("---", 2)
    require(len(parts) == 3, f"{path} frontmatter is not closed")
    raw = parts[1]
    values: dict[str, str] = {}
    top_level: set[str] = set()
    for line in raw.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        top_level.add(key.strip())
        values[key.strip()] = value.strip().strip('"').strip("'")
    allowed = {"name", "description", "license", "compatibility", "metadata"}
    require(top_level <= allowed, f"{path} has unsupported fields: {sorted(top_level - allowed)}")
    return values, text


def validate(root: Path) -> None:
    root = root.expanduser().resolve()
    skill_file = root / "SKILL.md"
    require(skill_file.is_file(), f"{root} is missing SKILL.md")
    nested = [path for path in root.rglob("SKILL.md") if path != skill_file]
    require(not nested, f"nested discoverable skill found: {nested[0] if nested else ''}")

    metadata, skill_text = frontmatter(skill_file)
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    require(NAME.fullmatch(name) is not None, "skill name must be lowercase kebab-case")
    require(name == root.name, "skill name must match its directory")
    require(1 <= len(description) <= 1024, "description must contain 1-1024 characters")
    require(metadata.get("compatibility") == "opencode", "compatibility must be opencode")

    required = {
        root / "references" / "default-organization.json",
        root / "references" / "delivery-gates.md",
        root / "references" / "handoff-contract.md",
        root / "references" / "procedure-directory.md",
        root / "scripts" / "init_project.py",
        root / "scripts" / "validate_profile.py",
    }
    for path in required:
        require(path.is_file(), f"required skill resource is missing: {path}")

    procedure_root = root / "references" / "procedures"
    actual = {
        child.name
        for child in procedure_root.iterdir()
        if child.is_dir() and (child / "PROCEDURE.md").is_file()
    }
    require(actual == REQUIRED_PROCEDURES, f"procedure set mismatch: {sorted(actual ^ REQUIRED_PROCEDURES)}")

    organization = json.loads(
        (root / "references" / "default-organization.json").read_text(encoding="utf-8")
    )
    require(organization.get("schema_version") == 2, "default profile must use schema version 2")
    roles = organization.get("roles")
    require(isinstance(roles, list) and len(roles) == 11, "default profile must define 11 roles")
    role_slugs = {role.get("slug") for role in roles if isinstance(role, dict)}
    require(
        role_slugs == {"boss", "priya", "mateo", "ellis", "nora", "sloane", "avery", "jordan", "rae", "kit", "devon"},
        "default profile role inventory is incomplete",
    )
    for department in organization.get("departments", {}):
        require(
            (root / "references" / "departments" / department / "roles.md").is_file(),
            f"missing role charter for {department}",
        )
        require(
            (root / "references" / "departments" / department / "procedures.md").is_file(),
            f"missing procedure index for {department}",
        )

    reference_root = root / "references"
    text_files = [skill_file, *reference_root.rglob("*.md"), *reference_root.rglob("*.json")]
    seen: set[Path] = set()
    for path in text_files:
        if path in seen:
            continue
        seen.add(path)
        text = path.read_text(encoding="utf-8")
        for token, label in FORBIDDEN.items():
            require(token not in text, f"{path} contains {label}: {token}")

    require("task" in skill_text, "SKILL.md must describe OpenCode task delegation")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Validate the standalone BOSS OpenCode skill.")
    result.add_argument("skill", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        validate(args.skill)
        print(f"BOSS OpenCode skill is valid: {args.skill.resolve()}")
        return 0
    except (ValidationError, OSError, json.JSONDecodeError) as error:
        print(f"BOSS skill validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
