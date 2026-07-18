# Structured handoff contract

Require every specialist to finish with these fields:

```text
STATUS: complete | blocked | changes-requested
ASSIGNMENT: issue/ticket and acceptance criteria addressed
ARTIFACTS: commits, issue comments, reports, screenshots, or none
EVIDENCE: exact commands/checks and outcomes
DECISIONS: decisions made within delegated authority, or none
RISKS: unresolved concerns, or none
NEXT_ROLE: recommended recipient
USER_DECISION: none, or one exact decision BOSS must request
```

`complete` means the bounded assignment and its evidence are complete, not that the feature is merged. `blocked` must identify the missing input or failed dependency. `changes-requested` must identify actionable findings and their affected acceptance criteria.

The Director reviews every handoff. Reject one that omits evidence, hides failing checks, expands scope, lacks artifact identifiers, or asks the product owner an unprioritized question. BOSS summarizes accepted handoffs but retains links and exact commands so another session can resume without conversation history. Return gaps to the specialist rather than researching or executing the missing work in the main thread.
