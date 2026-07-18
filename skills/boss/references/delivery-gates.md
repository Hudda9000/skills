# Delivery gates

The Director reviews each specialist handoff and advances only when the gate evidence exists. Return gaps to the responsible specialist; BOSS does not fill the gap by doing specialist work.

The generic profile enables every role below. Setting `enabled: false` makes that specialist and its role-specific routes unavailable; it does not satisfy or silently waive a gate. Before delivery begins, BOSS must report every disabled role and affected gate. If the chosen route requires a disabled role, stop unless the product owner has approved a project-specific workflow adapter that explicitly defines the replacement or omitted gate. BOSS may never act as the substitute specialist.

1. **Intent:** Product records the outcome, users, boundaries, acceptance criteria, and unresolved owner decisions.
2. **Design:** Architecture records affected seams, persistence and security boundaries, schema or migration ownership, test seams, dependencies, and safe parallelism under the repository's instructions.
3. **Scope approval:** BOSS reviews the Product and Architecture handoffs, then presents the exact scope, exclusions, risks, and delivery frontier. The product owner explicitly approves it.
4. **Implementation:** Feature Engineering works test-first in an isolated worktree and returns bounded commits plus verification. Material changes return to gate 3.
5. **Acceptance:** QA independently exercises acceptance criteria against the candidate head and records reproducible evidence.
6. **Independent review:** Standards reports findings and Specification separately reports findings. Neither edits the branch. BOSS reviews both reports for completeness without replacing their judgment. All actionable findings are resolved or explicitly accepted.
7. **Integration:** Release integrates accepted commits, resolves conflicts by documented intent, runs the full required verification, and prepares a linked draft PR.
8. **Merge decision:** BOSS summarizes scope, evidence, reviews, residual risks, and the exact PR head. Only the product owner, or an explicitly delegated role, merges.

## Parallelism rules

Parallelize only assignments with no unresolved dependency and no overlapping files, schema, or generated artifacts. Declare one exclusive owner for every schema or migration surface. Keep integration serial.

## Failure handling

- **Blocked:** inspect transcript, provide missing context or consolidate a decision for the owner.
- **Timeout:** inspect current pane state and output; retry only when the assignment is still safe and unambiguous.
- **Agent failure:** preserve its worktree and artifacts, start a replacement with the same role charter, and hand over durable context.
- **OpenCode Task unavailable or malformed response:** stop before further mutations and report the failed task and recovery action. Never guess an identifier.
