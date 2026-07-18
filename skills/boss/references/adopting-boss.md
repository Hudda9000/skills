# Adopt BOSS in another repository

BOSS is one OpenCode Agent Skill. Its source directory is `skills/boss`; install it by copying that directory to `.opencode/skills/boss` for a project or `~/.config/opencode/skills/boss` for a personal installation.

1. Allow the `boss` skill and OpenCode's `general` and `explore` subagents through `permission.skill` and `permission.task`.
2. Start a new OpenCode session and ask it to load the `boss` skill.
3. Ask BOSS to initialize the consuming repository. Initialization creates `.boss/organization.json` and `.boss/decisions.md` without modifying the installed skill.
4. Keep project-specific workflow adapters in the destination repository, not in BOSS core. Keep durable project conventions in `AGENTS.md`.
5. Setting `enabled` to `false` makes a specialist and its routes or gates unavailable. BOSS must report the impact and may not silently waive the gate. BOSS itself cannot be disabled.
6. Run `scripts/validate_profile.py --repository <repository>` after changing a profile.

The initializer and validator accept explicit repository paths, so a global skill can operate against any Git worktree. Schema version 2 uses `boss://departments/<slug>` for bundled charters and repository-relative paths for custom charters stored under `.boss/`.

Profiles from the former plugin are a clean break. Preserve any approved decisions, remove the legacy organization profile, and initialize again. BOSS never overwrites existing `.boss` files automatically.
