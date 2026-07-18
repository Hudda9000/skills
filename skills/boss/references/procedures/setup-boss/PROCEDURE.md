# Set up BOSS

Initialize the consuming repository while keeping its organization choices and critical architecture decisions outside the installed skill.

1. Read the repository's `AGENTS.md` and [the decision contract](references/decision-contract.md).
2. Determine the organization name and lowercase kebab-case slug from repository identity. Ask only when either is ambiguous.
3. From the BOSS skill directory, run:

   ```bash
   python3 scripts/init_project.py \
     --repository <repository> \
     --organization-name <name> \
     --organization-slug <slug>
   ```

4. Review the generated `.boss/organization.json` and `.boss/decisions.md`. Initialization is idempotent and never overwrites either file.
5. Before disabling a specialist, report the routes and evidence gates that become unavailable. Never disable BOSS.
6. Add concise BOSS guidance to the repository's root `AGENTS.md` when requested. Require BOSS to read `.boss/decisions.md`, record only approved critical architecture decisions with canonical links, and preserve `.boss/` during skill updates.
7. Validate without starting a child task:

   ```bash
   python3 scripts/validate_profile.py --repository <repository>
   ```

Do not change OpenCode personal memory or permissions automatically. Rebuild ordinary context from canonical issues, ADRs, documentation, code, and structured handoffs.
