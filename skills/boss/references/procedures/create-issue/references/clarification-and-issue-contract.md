# Clarification and Issue Contract

## Contents

1. [Questioning strategy](#questioning-strategy)
2. [Requirement coverage](#requirement-coverage)
3. [Shared-understanding test](#shared-understanding-test)
4. [Issue body template](#issue-body-template)
5. [Quality checks](#quality-checks)

## Questioning strategy

Use progressive clarification rather than a single exhaustive questionnaire.

### Round 1: outcome and boundary

Establish:

- the affected user or actor;
- the problem in current behavior;
- the desired observable outcome;
- urgency or motivating scenario;
- what is explicitly outside this issue.

### Round 2: repository reality

After inspecting code, reconcile the request with:

- current behavior and terminology;
- existing entities and ownership rules;
- reusable slices/components;
- conflicting assumptions;
- likely schema, API, or UI impact;
- related issues or partial implementations.

Phrase findings as evidence: “The current component/API/schema does X in `<path>`; should the new behavior preserve Y or replace it?”

### Round 3: behavior details

Resolve:

- primary user journey;
- entry points and navigation;
- required inputs and defaults;
- success state;
- validation and error messages;
- empty, loading, retry, cancellation, and destructive-action behavior;
- persistence and refresh expectations;
- permissions and tenant isolation;
- mobile/accessibility expectations when relevant.

### Round 4: delivery and acceptance

Resolve:

- migration/backward-compatibility requirements;
- external services or credentials;
- performance, privacy, logging, or audit needs;
- automated test expectations;
- browser walkthrough and screenshot evidence;
- rollout or feature-flag needs;
- explicit exclusions and deferred follow-ups.

Do not mechanically ask irrelevant questions. Use code evidence and prior answers to select the next highest-value uncertainty.

## Requirement coverage

Evaluate each category as decided, irrelevant, or explicitly deferred:

| Category | Questions to settle |
|---|---|
| User | Who acts, and whose data is affected? |
| Outcome | What new capability or corrected behavior results? |
| Entry point | Where does the user begin and how do they navigate there? |
| Inputs | Which fields, formats, defaults, and limits apply? |
| Success | What visible and persisted result proves completion? |
| Failure | What validation, error, retry, and recovery behavior is required? |
| State | What happens for empty, loading, existing, archived, or conflicting data? |
| Ownership | How is authorization and cross-user isolation enforced? |
| Data | What schema, migration, retention, or provenance behavior changes? |
| Integrations | Which external systems, credentials, quotas, and compensation paths matter? |
| Compatibility | What existing data/API/UI behavior must remain stable? |
| Quality | What accessibility, performance, security, privacy, and observability constraints apply? |
| Evidence | Which tests and browser actions prove acceptance? |
| Boundary | What is explicitly excluded or deferred? |

## Shared-understanding test

The requirement is ready for final approval only if both parties could independently answer:

1. Who experiences the problem?
2. What does the system do today?
3. What exactly should it do afterward?
4. How does the user reach and perform the behavior?
5. What data changes, and who owns it?
6. What happens when inputs or dependencies fail?
7. Which observable scenarios prove acceptance?
8. What is intentionally not included?

Continue clarification if any answer would materially differ.

## Issue body template

```markdown
## Problem

Describe the user problem and why it matters.

## Current behavior

Describe verified repository behavior and cite relevant paths or existing issues.

## Desired outcome

Describe the user-visible capability or corrected behavior.

## User journey

1. The user ...
2. The system ...
3. The user sees ...

## Requirements

### Functional

- ...

### Validation and error behavior

- ...

### Data, ownership, and security

- ...

### Compatibility and operations

- ...

## Acceptance criteria

- [ ] Given ..., when ..., then ...
- [ ] ...

## Verification expectations

- Unit: ...
- Integration: ...
- Browser walkthrough: ...
- Required evidence: ...

## Out of scope

- ...

## Assumptions and decisions

- ...

## Dependencies and risks

- ...

## Relevant code

- `path/to/file`: reason
```

Omit sections that are genuinely irrelevant; do not leave placeholders in the approved issue.

## Quality checks

Before previewing the final issue, confirm:

- The title describes an outcome, not an implementation task alone.
- The problem is distinct from the proposed solution.
- Current behavior is based on code evidence rather than assumption.
- Requirements do not contradict acceptance criteria.
- Acceptance criteria are observable and independently testable.
- Security and tenant isolation are explicit when user data is involved.
- Failure and validation behavior is not left to the implementer when product behavior matters.
- Exclusions prevent obvious adjacent scope from leaking into delivery.
- Deferred decisions have a stated default or follow-up boundary.
- The issue contains no secret, credential, personal data, or irrelevant internal reasoning.
- Another agent could implement the issue without rediscovering product intent.
