# Route BOSS work

Use this playbook when the correct specialist procedure is unclear. BOSS remains the only product-owner interface and assigns every selected procedure to the enabled employee whose charter owns it.

## Main delivery flow

1. Sharpen an idea with `grill-with-docs` and `domain-modeling` when requirements are still unclear.
2. Use `prototype` when a runnable artifact is needed to answer a UI, state, or logic question.
3. For multi-session work, use `to-spec`, then `to-tickets`; for a bounded approved slice, use `implement` with `tdd`.
4. After implementation, assign `code-review` as independent Standards and Specification axes, then route accepted work to Release and Integration.

## On-ramps

- **Incoming issue or pull request:** `triage`, then join the main delivery flow at the matching route.
- **Difficult bug:** `diagnosing-bugs`, then obtain fix-scope approval and join at `implement`.
- **Large foggy effort:** `wayfinder` until the decisions are clear, then `to-spec` and `to-tickets`.
- **Architecture health:** `improve-codebase-architecture`, then use `codebase-design` for a selected seam.

## Supporting procedures

- `research` answers bounded external questions from primary sources.
- `domain-modeling` owns domain vocabulary and consequential domain decisions.
- `codebase-design` owns deep-module vocabulary and interface alternatives.
- `resolving-merge-conflicts` is assigned only to Release and Integration.
- `setup-boss` initializes project-owned BOSS state.
- `setup-matt-pocock-skills` configures the issue-tracker and document conventions assumed by several imported procedures.

Do not ask the product owner to manage this internal chain. Select the smallest route that satisfies the request, assign it through BOSS, and review every structured handoff before advancing.
