# BOSS for OpenCode

BOSS — Business Orchestration & Specialist Supervisor — gives a product owner one Director who assigns and reviews work performed by named specialist roles. BOSS assigns and reviews; specialists research and execute in OpenCode child tasks.

This repository distributes one OpenCode Agent Skill: [`skills/boss`](skills/boss).

## Install

OpenCode discovers personal skills under `~/.config/opencode/skills/` and project skills under `.opencode/skills/`. Copy the skill from a clone of this repository so its bundled references remain inside OpenCode's normal configuration or project boundary.

Personal installation:

```bash
mkdir -p ~/.config/opencode/skills
cp -R /absolute/path/to/this-repository/skills/boss ~/.config/opencode/skills/
```

Project installation:

```bash
mkdir -p .opencode/skills
cp -R /absolute/path/to/this-repository/skills/boss .opencode/skills/
```

Allow the skill and the built-in subagents BOSS uses in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "skill": {
      "*": "ask",
      "boss": "allow"
    },
    "task": {
      "*": "deny",
      "general": "allow",
      "explore": "allow"
    }
  }
}
```

Start a new OpenCode session after installing or updating the skill.

## Use

Ask OpenCode to load the skill explicitly:

```text
Load the boss skill and deliver issue #42 through the named team.
```

For a new repository:

```text
Load the boss skill and initialize BOSS for this repository. Infer the organization name and slug, show every created file, and review the organization profile with me.
```

Initialization creates project-owned state that skill updates do not overwrite:

```text
<project>/
├── .boss/
│   ├── organization.json
│   ├── README.md
│   └── decisions.md
└── AGENTS.md
```

The profile uses schema version 2. Profiles created by the former Codex plugin are intentionally not compatible; preserve any decisions you need, remove the old `organization.json`, and initialize again.

## The company

| Employee | Role | Responsibility | Lifecycle |
|---|---|---|---|
| **BOSS** | Director | Assign work, review handoffs, own product-owner decisions, and advance gates | Parent session |
| **Priya** | Product and Domain Lead | Clarify outcomes, triage requests, model the domain, and write specifications | Resident/read-only |
| **Mateo** | Staff Architect | Investigate constraints, design deep seams, and identify safe parallelism | Resident/read-only |
| **Ellis** | Feature Engineer | Implement one approved vertical slice test-first | Isolated worktree |
| **Nora** | QA and Evidence Engineer | Independently prove acceptance in the real system | Isolated worktree |
| **Sloane** | Standards Reviewer | Review repository and engineering standards independently | Resident/read-only |
| **Avery** | Specification Reviewer | Compare the diff and evidence with approved intent | Resident/read-only |
| **Jordan** | Release and Integration Engineer | Integrate accepted commits and prepare the draft PR | Isolated worktree |
| **Rae** | Research Analyst | Answer bounded questions from primary sources | On demand |
| **Kit** | Prototype and UX Specialist | Test one design question with disposable work | Isolated worktree |
| **Devon** | Bug Investigator | Reproduce difficult failures and establish their cause | Isolated worktree |

BOSS never replaces independent specialist judgment. Mutating employees work in separate Git worktrees, and the product owner retains merge authority unless they explicitly delegate it.

## Configure roles

Edit `.boss/organization.json` to change the organization name or disable specialists. Omitting `enabled` means `true`. Setting it to `false` makes the role and its routes or evidence gates unavailable; it never silently waives a gate. BOSS cannot be disabled.

Bundled charters use `boss://departments/<slug>`. A custom charter may instead be a path relative to `.boss/` and must stay inside that directory.

## Validate

The validation suite uses only Python's standard library:

```bash
python3 skills/boss/scripts/validate_skill.py skills/boss
python3 skills/boss/scripts/test_validate_skill.py
python3 skills/boss/scripts/test_init_project.py
python3 skills/boss/scripts/test_validate_profile.py
```
