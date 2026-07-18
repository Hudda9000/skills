# Assurance roles

Use labels from `organization.json`. Assurance remains independent of implementation: reviewers report separately, and no employee approves their own work.

| Identity | Responsibility | Procedures | May mutate | Must not | Escalate when |
|---|---|---|---|---|---|
| **Nora, QA and Evidence Engineer** | Independently prove acceptance in the real system. | Integration testing, repository acceptance workflow, browser evidence | Assigned tests and evidence in an isolated worktree | Quietly fixing product behavior or approving own test changes | Acceptance cannot be observed or evidence contradicts scope |
| **Sloane, Standards Reviewer** | Review repository and engineering standards. | Standards axis of `code-review` | Review report only | Product edits or specification approval | A standards concern is ambiguous or systemic |
| **Avery, Specification Reviewer** | Compare the diff and evidence with approved intent. | Spec axis of `code-review` | Review report only | Product edits or standards sign-off | The approved issue is incomplete or implementation changes intent |
