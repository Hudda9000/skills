# BOSS architecture-decision contract

Store mutable organization choices and only critical architecture decisions under `.boss/` so an externally installed skill can be upgraded or replaced without losing project-owned configuration.

- `organization.json` owns the company name, label slug, department membership, role identities, lifecycles, and role enablement. Omit `enabled` or set it to `true` to use a role. Setting it to `false` makes that specialist and its role-specific routes and gates unavailable; it never silently waives a gate. BOSS/the Director cannot be disabled.
- `decisions.md` records only approved, hard-to-reverse architecture decisions with date, owner, concise rationale, and a canonical ADR, issue, or pull-request link.

Do not store general project context, delivery status, raw handoffs, transcripts, speculative findings, credentials, or duplicated instructions under `.boss/`. Read ordinary context from its canonical source. Put mandatory instructions in `AGENTS.md`.

BOSS reviews decision entries. Specialists may propose an entry in a handoff, but do not independently rewrite the shared decision record unless their assignment explicitly grants that authority. Initializers and skill updates must preserve all existing `.boss/` files.
