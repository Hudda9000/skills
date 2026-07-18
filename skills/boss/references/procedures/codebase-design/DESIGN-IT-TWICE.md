# Design It Twice

When the product owner wants alternative interfaces for a chosen deepening candidate, use this independent named-employee pattern. Based on "Design It Twice" (Ousterhout) — your first idea is unlikely to be the best.

Uses the vocabulary in [PROCEDURE.md](PROCEDURE.md) — **module**, **interface**, **seam**, **adapter**, **leverage**.

## Process

BOSS is the only product-owner interface. The Staff Architect frames the architecture problem and recommends specialists who can contribute independent designs; BOSS assigns each brief and reviews their [company handoffs](../../handoff-contract.md). BOSS does not design the alternatives, and specialists do not create nested agents or ask the product owner questions directly.

Choose three or more named roles whose charter supplies a genuinely different perspective. Typical choices are the Staff Architect for interface depth, Feature Engineer for caller and implementation ergonomics, QA Engineer for test-surface design, UX Specialist for a UI-facing seam, and Release Engineer for integration constraints. Assign each a distinct design constraint from Step 2. Do not invent anonymous roles merely to increase the number of alternatives.

### 1. Frame the problem space

Before dispatching designers, write a user-facing explanation of the problem space for the chosen candidate:

- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [DEEPENING.md](DEEPENING.md))
- A rough illustrative code sketch to ground the constraints — not a proposal, just a way to make the constraints concrete

Return this explanation to BOSS, then immediately proceed to Step 2. The product owner can read and think while the designers work in parallel.

### 2. Dispatch independent designers

Return three or more independent briefs to BOSS, who assigns the selected named roles through OpenCode Task and reviews their handoffs. Each must produce a **radically different** interface for the deepened module.

Give each designer a separate technical brief (file paths, coupling details, dependency category from [DEEPENING.md](DEEPENING.md), what sits behind the seam). Keep the brief independent of the user-facing problem-space explanation in Step 1. Give each designer a different design constraint:

- Agent 1: "Minimize the interface — aim for 1–3 entry points max. Maximise leverage per entry point."
- Agent 2: "Maximise flexibility — support many use cases and extension."
- Agent 3: "Optimise for the most common caller — make the default case trivial."
- Agent 4 (if applicable): "Design around ports & adapters for cross-seam dependencies."

Include both [PROCEDURE.md](PROCEDURE.md) vocabulary and `CONTEXT.md` vocabulary in the brief so each designer names things consistently with the architecture language and the project's domain language.

Each designer outputs:

1. Interface (types, methods, params — plus invariants, ordering, error modes)
2. Usage example showing how callers use it
3. What the implementation hides behind the seam
4. Dependency strategy and adapters (see [DEEPENING.md](DEEPENING.md))
5. Trade-offs — where leverage is high, where it's thin

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by **depth** (leverage at the interface), **locality** (where change concentrates), and **seam placement**.

After comparing, give your own recommendation: which design is strongest and why. If elements from different designs combine well, propose a hybrid. Be opinionated—the product owner needs a strong read, not a menu. The Staff Architect returns the comparison and recommendation to BOSS for handoff review and presentation.
