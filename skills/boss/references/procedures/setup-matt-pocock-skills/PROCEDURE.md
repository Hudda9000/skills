# Set up imported engineering procedures

Scaffold the per-repository configuration assumed by the bundled issue, triage, specification, ticketing, and domain-modeling procedures:

- **Issue tracker** — GitHub, GitLab, local Markdown, or a documented custom tracker.
- **Triage labels** — mappings for the five canonical triage states.
- **Domain docs** — locations for `CONTEXT.md`, a context map, and ADRs.

This is a prompt-driven procedure. Explore read-only, return findings and decision-ready questions through BOSS, obtain approval, then write only inside the assigned mutation boundary.

## 1. Explore

Inspect without assuming:

- `git remote -v` and `.git/config`;
- root `AGENTS.md` or `CLAUDE.md` and any existing `## Agent procedures` section;
- `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, and context-scoped ADR directories;
- `docs/agents/` and `.scratch/`;
- whether the active workflow uses the bundled `triage` procedure;
- genuine monorepo signals such as `pnpm-workspace.yaml`, package workspaces, or multiple populated packages.

## 2. Return configuration decisions

Return findings to BOSS one section at a time, with a recommended answer.

### Issue tracker

Recommend GitHub when the remote is GitHub, GitLab when it is GitLab, and local Markdown when there is no tracker. Also allow a custom tracker whose workflow the product owner describes. Record the approved choice in `docs/agents/issue-tracker.md`.

The GitHub and GitLab templates default external pull/merge requests as a triage surface to off. Do not raise that choice unless the product owner asks.

### Triage labels

Run this section only when the delivery workflow uses `triage`. Recommend the canonical mappings `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. Collect overrides only when the repository already uses different labels. Record them in `docs/agents/triage-labels.md`.

### Domain docs

Default to a single root `CONTEXT.md` plus `docs/adr/`. Offer a `CONTEXT-MAP.md` with per-context files only when exploration found a genuine multi-context repository.

## 3. Confirm the exact edits

Return a draft of:

- the `## Agent procedures` block for the existing root instruction file;
- `docs/agents/issue-tracker.md`;
- `docs/agents/domain.md`;
- `docs/agents/triage-labels.md` when triage is in use.

Wait for BOSS to relay product-owner approval before writing.

## 4. Write

Edit `CLAUDE.md` when it exists; otherwise edit `AGENTS.md`. If neither exists, return that choice to BOSS rather than selecting one. Update an existing block in place and preserve surrounding user content.

Use these bundled templates:

- [issue-tracker-github.md](issue-tracker-github.md)
- [issue-tracker-gitlab.md](issue-tracker-gitlab.md)
- [issue-tracker-local.md](issue-tracker-local.md)
- [triage-labels.md](triage-labels.md)
- [domain.md](domain.md)

For a custom tracker, write `docs/agents/issue-tracker.md` from the approved workflow description.

## 5. Hand off

Return the files changed, approved choices, verification, and the bundled procedures that will consume the configuration using the [handoff contract](../../handoff-contract.md). Note that the product owner may edit `docs/agents/*.md` directly later; rerun this procedure only to change the configuration deliberately.
