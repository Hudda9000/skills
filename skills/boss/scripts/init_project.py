#!/usr/bin/env python3
"""Initialize project-owned BOSS configuration without overwriting local state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def skill_root() -> Path:
    root = Path(__file__).resolve().parent.parent
    if not (root / "SKILL.md").is_file():
        raise ValueError(f"Could not locate the BOSS skill root from {__file__}")
    return root


def repository_root(start: Path) -> Path:
    resolved = start.expanduser().resolve()
    if resolved.is_file():
        resolved = resolved.parent
    for candidate in (resolved, *resolved.parents):
        if (candidate / ".git").exists():
            return candidate
    raise ValueError(f"Could not locate a Git repository from {resolved}")


def project_profile(name: str, slug: str) -> dict[str, Any]:
    template = json.loads(
        (skill_root() / "references" / "default-organization.json").read_text(
            encoding="utf-8"
        )
    )
    template["organization"] = {"name": name, "slug": slug}
    return template


def write_if_missing(
    path: Path,
    content: str,
    created: list[str],
    preserved: list[str],
    root: Path,
) -> None:
    relative = str(path.relative_to(root))
    if path.exists():
        preserved.append(relative)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(relative)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Create a project-owned BOSS profile and architecture decision log."
    )
    result.add_argument("--repository", type=Path, default=Path.cwd())
    result.add_argument("--organization-name", required=True)
    result.add_argument("--organization-slug", required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    name = args.organization_name.strip()
    organization_slug = args.organization_slug.strip()
    if not name:
        print("--organization-name must not be empty", file=sys.stderr)
        return 2
    if not SLUG.fullmatch(organization_slug):
        print("--organization-slug must be lowercase kebab-case", file=sys.stderr)
        return 2
    try:
        repository = repository_root(args.repository)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    created: list[str] = []
    preserved: list[str] = []
    boss_root = repository / ".boss"
    files = {
        boss_root / "organization.json": json.dumps(
            project_profile(name, organization_slug), indent=2
        )
        + "\n",
        boss_root / "README.md": """# BOSS project configuration

This directory is owned by the project, not the installed BOSS skill. Updating the skill must not overwrite it.

- `organization.json` configures company identity and roles. Disabling a specialist makes its routes and gates unavailable; it never silently waives a gate. BOSS cannot be disabled.
- `decisions.md` records only critical, approved architecture decisions with canonical references.

Keep ordinary context in canonical project artifacts. Never store secrets, transcripts, delivery status, or general-purpose memory here.
""",
        boss_root / "decisions.md": """# Critical architecture decisions

Record only hard-to-reverse, approved architecture decisions with date, owner, rationale, and a canonical ADR, issue, or pull-request link.
""",
    }
    for path, content in files.items():
        write_if_missing(path, content, created, preserved, repository)

    print(
        json.dumps(
            {"repository": str(repository), "created": created, "preserved": preserved},
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
