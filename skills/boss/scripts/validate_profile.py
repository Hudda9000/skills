#!/usr/bin/env python3
"""Validate a project-owned or bundled BOSS organization profile."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any


SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
LIFECYCLES = {"caller", "resident", "on-demand", "worktree"}
ROLE_IMPACTS = {
    "priya": ["product clarification", "triage", "specification"],
    "mateo": ["architecture gate"],
    "ellis": ["feature implementation"],
    "nora": ["acceptance evidence gate"],
    "sloane": ["standards review gate"],
    "avery": ["specification review gate"],
    "jordan": ["integration and draft PR"],
    "rae": ["external research"],
    "kit": ["prototype and UX investigation"],
    "devon": ["bug reproduction and diagnosis"],
}


class ProfileError(RuntimeError):
    """Raised when a BOSS profile violates its schema or safety rules."""


@dataclass(frozen=True)
class Department:
    slug: str
    name: str
    charter: str


@dataclass(frozen=True)
class Role:
    slug: str
    name: str
    title: str
    department: str
    lifecycle: str
    enabled: bool
    impacts: tuple[str, ...]


def skill_root() -> Path:
    root = Path(__file__).resolve().parent.parent
    if not (root / "SKILL.md").is_file():
        raise ProfileError(f"Could not locate the BOSS skill root from {__file__}")
    return root


def repository_root(start: Path) -> Path:
    resolved = start.expanduser().resolve()
    if resolved.is_file():
        resolved = resolved.parent
    for candidate in (resolved, *resolved.parents):
        if (candidate / ".git").exists():
            return candidate
    raise ProfileError(f"Could not locate a Git worktree from {resolved}")


def default_profile_path() -> Path:
    return skill_root() / "references" / "default-organization.json"


def active_profile_path(explicit: Path | None, repository: Path) -> Path:
    if explicit is not None:
        return explicit.expanduser().resolve()
    project_profile = repository / ".boss" / "organization.json"
    return project_profile if project_profile.is_file() else default_profile_path()


def required_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProfileError(f"Profile field {field!r} must be a non-empty string")
    return value.strip()


def slug(value: Any, field: str) -> str:
    result = required_string(value, field)
    if not SLUG.fullmatch(result):
        raise ProfileError(f"Profile field {field!r} must be lowercase kebab-case")
    return result


def resolve_charter(value: str, profile: Path, department: str) -> Path:
    if value.startswith("bundle://"):
        raise ProfileError(
            "Legacy bundle:// charter references are unsupported. Preserve any "
            ".boss/decisions.md content, remove the legacy organization profile, "
            "and initialize BOSS again to create schema version 2."
        )
    if value.startswith("boss://departments/"):
        named_department = value.removeprefix("boss://departments/")
        if named_department != department or not SLUG.fullmatch(named_department):
            raise ProfileError(
                f"Department {department!r} has invalid bundled charter {value!r}"
            )
        charter = skill_root() / "references" / "departments" / department / "roles.md"
    else:
        candidate = Path(value)
        if candidate.is_absolute():
            raise ProfileError(
                f"Department {department!r} custom charter must be relative to .boss"
            )
        charter = (profile.parent / candidate).resolve()
        try:
            charter.relative_to(profile.parent.resolve())
        except ValueError as error:
            raise ProfileError(
                f"Department {department!r} custom charter must stay inside {profile.parent}"
            ) from error
    if not charter.is_file():
        raise ProfileError(
            f"Department {department!r} charter does not exist: {charter}"
        )
    return charter.resolve()


def load_profile(path: Path) -> tuple[str, str, tuple[Department, ...], tuple[Role, ...]]:
    resolved = path.expanduser().resolve()
    try:
        payload = json.loads(resolved.read_text(encoding="utf-8"))
    except OSError as error:
        raise ProfileError(f"Could not read organization profile {resolved}: {error}") from error
    except json.JSONDecodeError as error:
        raise ProfileError(f"Organization profile {resolved} is not valid JSON: {error}") from error

    if not isinstance(payload, dict):
        raise ProfileError("Organization profile must contain a JSON object")
    version = payload.get("schema_version")
    if version != 2:
        legacy = " Legacy plugin profiles must be regenerated." if version == 1 else ""
        raise ProfileError(f"Organization profile must use schema_version 2.{legacy}")

    organization = payload.get("organization")
    if not isinstance(organization, dict):
        raise ProfileError("Organization profile must define an organization object")
    organization_name = required_string(organization.get("name"), "organization.name")
    organization_slug = slug(organization.get("slug"), "organization.slug")

    raw_departments = payload.get("departments")
    if not isinstance(raw_departments, dict) or not raw_departments:
        raise ProfileError("Organization profile must define at least one department")
    departments: list[Department] = []
    department_slugs: set[str] = set()
    for raw_slug, raw_department in raw_departments.items():
        department_slug = slug(raw_slug, "departments.<slug>")
        if not isinstance(raw_department, dict):
            raise ProfileError(f"Department {department_slug!r} must be an object")
        charter_value = required_string(
            raw_department.get("charter"), f"departments.{department_slug}.charter"
        )
        charter = resolve_charter(charter_value, resolved, department_slug)
        departments.append(
            Department(
                slug=department_slug,
                name=required_string(
                    raw_department.get("name"), f"departments.{department_slug}.name"
                ),
                charter=str(charter),
            )
        )
        department_slugs.add(department_slug)

    raw_roles = payload.get("roles")
    if not isinstance(raw_roles, list) or not raw_roles:
        raise ProfileError("Organization profile must define at least one role")
    roles: list[Role] = []
    seen: set[str] = set()
    for index, raw_role in enumerate(raw_roles):
        if not isinstance(raw_role, dict):
            raise ProfileError(f"Role {index} must be an object")
        role_slug = slug(raw_role.get("slug"), f"roles[{index}].slug")
        if role_slug in seen:
            raise ProfileError(f"Organization profile contains duplicate role {role_slug!r}")
        seen.add(role_slug)
        department = slug(raw_role.get("department"), f"roles[{index}].department")
        if department not in department_slugs:
            raise ProfileError(f"Role {role_slug!r} names unknown department {department!r}")
        lifecycle = required_string(raw_role.get("lifecycle"), f"roles[{index}].lifecycle")
        if lifecycle not in LIFECYCLES:
            raise ProfileError(f"Role {role_slug!r} has unsupported lifecycle {lifecycle!r}")
        enabled = raw_role.get("enabled", True)
        if not isinstance(enabled, bool):
            raise ProfileError(f"Profile field roles[{index}].enabled must be a boolean")
        roles.append(
            Role(
                slug=role_slug,
                name=required_string(raw_role.get("name"), f"roles[{index}].name"),
                title=required_string(raw_role.get("title"), f"roles[{index}].title"),
                department=department,
                lifecycle=lifecycle,
                enabled=enabled,
                impacts=tuple(ROLE_IMPACTS.get(role_slug, ())),
            )
        )

    boss = next((role for role in roles if role.slug == "boss"), None)
    if boss is None or boss.name != "BOSS" or boss.title != "Director":
        raise ProfileError("Role 'boss' must be named BOSS with title Director")
    if boss.lifecycle != "caller" or not boss.enabled:
        raise ProfileError("BOSS must be enabled with lifecycle 'caller'")
    return organization_name, organization_slug, tuple(departments), tuple(roles)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Validate a BOSS schema-version-2 profile.")
    result.add_argument("--repository", type=Path, default=Path.cwd())
    result.add_argument("--profile", type=Path)
    result.add_argument("--role", action="append", default=[])
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        repository = repository_root(args.repository)
        profile = active_profile_path(args.profile, repository)
        name, organization_slug, departments, roles = load_profile(profile)
        role_by_slug = {role.slug: role for role in roles}
        unknown = sorted(set(args.role) - set(role_by_slug))
        if unknown:
            raise ProfileError("Unknown requested role(s): " + ", ".join(unknown))
        selected = [role_by_slug[item] for item in args.role] if args.role else list(roles)
        disabled_requested = (
            [role.slug for role in selected if not role.enabled] if args.role else []
        )
        if disabled_requested:
            raise ProfileError("Disabled requested role(s): " + ", ".join(disabled_requested))
        disabled = [role for role in roles if not role.enabled]
        print(
            json.dumps(
                {
                    "organization": {
                        "name": name,
                        "slug": organization_slug,
                        "profile": str(profile),
                    },
                    "repository": str(repository),
                    "departments": [asdict(item) for item in departments],
                    "roles": [asdict(item) for item in selected if item.enabled],
                    "disabled_roles": [item.slug for item in disabled],
                    "unavailable": {
                        item.slug: list(item.impacts) for item in disabled
                    },
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    except ProfileError as error:
        print(f"BOSS profile validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
