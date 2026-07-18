# Create Issue

Convert a rough requirement into a repository-informed, implementation-ready GitHub issue. Investigate and clarify only; do not implement the feature.

## Load guidance

1. Read the repository `AGENTS.md` and every applicable nested instruction file.
2. Read `references/clarification-and-issue-contract.md` completely.
3. Treat that reference as the required questioning and issue-body contract.

## Establish context

1. Restate the user's initial requirement without silently expanding it.
2. Inspect the Git remote and confirm the target repository.
3. Verify `gh auth status` before any GitHub operation. If authentication is unavailable, continue local investigation and clarification, then report authentication as the issue-creation blocker.
4. Search open and closed issues for likely duplicates or related work when GitHub is available.
5. Read applicable repository instructions and inspect the working tree.

Do not create branches, edit application files, implement code, or mutate GitHub during investigation.

## Investigate the codebase

Trace the requirement through the actual system. Inspect only relevant areas, including as applicable:

- domain entities and ownership boundaries;
- API slices, contracts, validation, and error behavior;
- database schema and migration conventions;
- frontend routes, components, services, and visible navigation;
- authentication, authorization, privacy, and external integrations;
- unit, integration, and browser-test coverage;
- runtime, deployment, and backward-compatibility constraints.

Separate observed facts from inferences. Cite concrete file paths and current behavior when explaining a gap or challenging an assumption.

## Clarify persistently

Question the user until both parties share one precise scope. Be rigorous, candid, and patient rather than abrasive.

1. Start with the highest-impact unknowns that could change architecture, user experience, data, security, or acceptance.
2. Ask one to three related questions per round so answers remain manageable.
3. Recommend a default for each question and explain its consequence.
4. Incorporate each answer into a living scope summary.
5. Challenge contradictions, undefined terms, happy-path-only requirements, unverifiable outcomes, and accidental scope expansion.
6. Probe edge cases, validation, errors, permissions, migration, empty/loading states, accessibility, observability, and explicit exclusions where relevant.
7. Do not repeat answered questions unless new code evidence creates a conflict.
8. Do not stop merely because an implementation seems obvious. Stop when every material requirement is decided or explicitly deferred.

Use direct questions such as:

- “Which user is affected, and what can they do afterward that they cannot do now?”
- “The current code behaves this way in `<path>`. Should this issue preserve or replace that behavior?”
- “What observable result would make you accept this in a browser?”
- “What must this issue deliberately not solve?”

## Reach shared understanding

When material questions are resolved, present a consolidated scope using the issue structure in the bundled reference. Include:

- proposed title;
- problem and user outcome;
- current repository behavior and evidence;
- functional and non-functional requirements;
- user journey;
- validation, errors, and edge cases;
- data, security, and compatibility implications;
- acceptance criteria as observable outcomes;
- test/evidence expectations;
- exclusions, assumptions, dependencies, risks, and deferred decisions.

Call out any remaining ambiguity. If ambiguity is material, continue questioning. If it is intentionally deferred, state the default and boundary explicitly.

## Require exact approval

Render the complete proposed issue title and Markdown body. Ask the user to approve that exact content or request changes.

Do not interpret agreement with the general idea as approval to create the issue. Require an explicit response such as “Create it,” “Approved,” or an equally clear instruction after the final preview.

If the user changes anything, revise the preview and seek approval again.

## Create the GitHub issue

After exact approval:

1. Reconfirm `gh auth status` and the target repository.
2. Write the approved body to a temporary file outside the repository.
3. Create the issue non-interactively with `gh issue create --repo <owner/repo> --title <title> --body-file <file>`.
4. Add labels, milestone, or assignee only if explicitly agreed and valid in the repository.
5. Open or fetch the created issue to verify its title, body, metadata, and URL.
6. Remove the temporary body file.
7. Return the issue number and clickable URL, plus any metadata that could not be applied.

Never expose GitHub credentials or include secrets/private data in the issue.

## Failure handling

- If GitHub authentication fails, preserve the approved title/body in the conversation and give the exact re-authentication command. Do not claim the issue exists.
- If a likely duplicate exists, show it and ask whether to update/comment, create a distinct issue, or stop.
- If the repository contradicts the requirement, explain the evidence and continue clarification.
- If the user refuses a material decision, record an explicit default or defer it out of scope before approval.
- If issue creation partially fails, inspect GitHub before retrying to avoid duplicates.

## Completion gate

Report completion only when:

- the relevant codebase was investigated;
- material gaps were resolved or explicitly deferred;
- the user approved the exact final issue;
- GitHub returned a created issue;
- the created issue was fetched and verified;
- its number and URL were returned to the user.
