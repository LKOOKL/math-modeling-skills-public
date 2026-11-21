---
name: modeler-decision-logger
description: Collect, stamp, and freeze human or explicitly delegated decisions into one canonical per-subquestion decision log. The decision version of frozen_numbers.json — it does NOT originate decisions, it makes the actual decision-maker's judgments traceable, append-only, and the single source every downstream narrative is transcribed from.
license: MIT
---

## Decision authority

Read the [shared decision-authority contract](../workflow-orchestrator/references/decision-authority.md) when this skill produces or consumes a judgment. Resolve explicit delegation, human-reserved decisions and existing-results writing scope before applying the rules below. Human-only instructions and unresolved-human examples below describe the reserved branch; delegated decisions use `decided_by: agent_under_user_delegation` with an authorization reference and actual evidence. Never label an agent decision as human-authored.

# Purpose

**Trace format:** Follow [tracking-format.md](../write-math-modeling-papers/references/tracking-format.md). In `.tex`, put `% decision_id: Qx-D0n` on a standalone line before the prose; Markdown may use its own comment or mapping field. Format-neutral `decision_id:` examples below are identifiers, not text to print in the paper. Audit the source mapping and final PDF separately.

Maintain one canonical, append-only log of human or explicitly delegated decisions, so that every modeling judgment a contest grades — which method and why, whether a result is good, what a number means, how confident the team is — has a single traceable home, and every downstream narrative (final method explanation, solution package, paper method-selection prose) is **transcribed from it, never re-invented**.

This is the decision-side parallel of the Frozen Numbers Convention. Just as `frozen_numbers.json` pins numbers so a bug fix can't silently shift the paper, the decision log pins judgments so the AI can't silently author what a judge grades, and so four different skills can't each re-compose the method-selection story and drift apart.

**This skill does NOT make decisions.** It never fills `modeler_decision` or `modeler_rationale`. It collects the valid human or delegated decision artifacts that judgment-bearing skills emit (`methods/Qx/decisions/<skill>_modeler_decision.md`), validates them mechanically, stamps them, and folds them into the canonical log. It pre-fills only the mechanical fields (`decision_id`, `options_considered`, `evidence`, `ai_suggestion`).

# When to use

Use this skill:

- After a judgment-bearing skill (`method-selector`; later `result-report-generator`, `robustness-checker`, `final-method-explainer`, `solution-package-builder`) has captured an authorized decision in its `*_modeler_decision.md` artifact, to fold it into the canonical log.
- As a precondition check at Gates G2.5 / G4.5 / G5: "does the log contain a `DECIDED` record for the required decision point of this Qx?"
- When `final-method-explainer` / `solution-package-builder` / `paper-section-writer` need the method-selection narrative — they read it FROM this log with `decision_id` provenance, they do not re-author it.
- After the contest, to render the decision log as post-mortem review material.

Do NOT use this skill:

- To author, suggest, or auto-fill any human decision or rationale.
- To decide which method is right, what a number means, or whether a result is good.
- To overwrite a past decision (the log is append-only; a changed mind appends with `supersedes`).

# Preconditions

- At least one `methods/Qx/decisions/<skill>_modeler_decision.md` artifact exists with `status: DECIDED`.
- The [shared decision-authority contract](../workflow-orchestrator/references/decision-authority.md) is the schema of record.

If an artifact is still PENDING because authority, a reserved choice or required evidence is unresolved, do not log it as DECIDED; report the actual remaining gap.

# Inputs

- `methods/Qx/decisions/*_modeler_decision.md` — the per-skill decision artifacts with actual actor and authority.
- The candidate pool / experiment reports the decision references (for `evidence` provenance).
- The existing `methods/Qx/qx_decision_log.md`, if any (to append to).
- `planning/session_config.json` (for `mode`, recorded per record).

# Workflow

1. Locate decided artifacts.
   - For the target Qx, find every `methods/Qx/decisions/<skill>_modeler_decision.md` with `status: DECIDED`.
   - Skip `PENDING` ones; report them as still-blocking.

2. Validate the shared decision record without inventing its judgment.
   - Apply the shared contract: DECIDED, valid actual actor, explicit delegation when applicable, no unresolved reservation or placeholder, and supported choice/reason/evidence.
   - Preserve `authorization_ref`, `decided_by`, `human_review` and any actual human-review evidence in the log. Never relabel an agent decision as human.
   - A documented human acceptance may match an earlier suggestion; a matching phrase alone is neither proof of acceptance nor a reason to reject it. Assess the recorded source, not a character-count floor.
   - Return an invalid artifact to its producer with the exact missing authority/evidence field. A human-reserved gap goes to the user; a delegated producer can repair its own record within scope.

3. Append to the canonical log.
   - Write one decision record per validated artifact into `methods/Qx/qx_decision_log.md`.
   - Stamp `decision_id` (monotonic `Qx-D01`, `Qx-D02`, …), `decision_point` (from the fixed taxonomy below), `timestamp`, and `captured_in_mode`.
   - **Append-only.** If this decision revises an earlier one, set `supersedes: <prior decision_id>` and append a new record; never edit the prior record.

4. Update the global index.
   - Maintain `planning/decision_log_index.md`: one row per decision across all Qx (id, Qx, decision_point, choice, confidence, supersedes).

5. Provide the narrative source for downstream skills.
   - When asked for the method-selection narrative, return the relevant `modeler_rationale` fields verbatim/near-verbatim, each tagged with its `decision_id`, so the consuming skill can cite provenance (`decision_id: Q1-D03`).
   - The AI consuming this is forbidden from writing a method-justification sentence that has no backing decision record.

6. Staleness check (mirrors frozen_numbers).
   - If a `code/Qx/*` change shifted a result that a `result_verdict` record was based on, mark that record `STALE — authorized decision-maker must review the changed result`. Do not silently keep a verdict adopted against now-changed numbers; retain the actual original actor and require an authorized reassessment.

# Decision-point taxonomy (fixed)

A record's `decision_point` is exactly one of:
`framing` · `method_choice` · `assumption_necessity` · `baseline` · `hyperparameter` · `result_verdict` · `confidence` · `claim_scope` · `figure_role`

For this suite's newly solved pipeline, four decision points are required before "Ready for Writer": `method_choice`, `result_verdict`, `confidence`, `assumption_necessity`. The rest are optional. `completeness-auditor` checks the applicable four per Qx. Supplied-result writing follows the main writing input contract and does not require inventing historical decision records.

# Outputs

- `methods/Qx/qx_decision_log.md` — the canonical append-only log for Qx.
- `planning/decision_log_index.md` — global roll-up across all Qx.

# Output format

`methods/Qx/qx_decision_log.md`:

```markdown
# Qx Decision Log

> Canonical, append-only record of actual human or delegated decisions for Qx.
> Downstream narratives transcribe from here with `decision_id` provenance. Never edited in place.

---

### Q2-D01 · method_choice · 2026-06-06T14:20+08:00 · mode: learning
- **options_considered**: M1 moving-average (baseline) / M2 ARIMA / M3 grey GM(1,1)   <!-- AI-filled, neutral -->
- **evidence**: PoC feasibility — M2 RMSE 2.4 on first 50 months (methods/Q2/poc/m2_poc_result.txt) <!-- AI-filled -->
- **ai_suggestion**: M2 ARIMA — best PoC fit   <!-- AI-filled, not a verdict -->
- **decided_by**: human
- **authorization_ref**: actual user response selecting M2
- **human_review**: false
- **modeler_decision**: M2 (CHOSEN)            <!-- actual human response in this example -->
- **modeler_rationale**: <actual recorded reason and supporting evidence>   <!-- HUMAN -->
- **confidence**: medium
- **supersedes**: —

### Q2-D02 · result_verdict · 2026-06-07T09:10+08:00 · mode: speed
...
```

`planning/decision_log_index.md`:

```markdown
# Decision Log Index (all subquestions)

| id | Qx | decision_point | choice | confidence | supersedes |
|----|----|----------------|--------|------------|------------|
| Q2-D01 | Q2 | method_choice | M2 | medium | — |
| Q2-D02 | Q2 | result_verdict | M2 CHOSEN | high | — |
```

# Post-contest review

Each record carries alternatives, evidence, the actual decision and reason, actor/authorization and a `supersedes` chain. A retrospective distinguishes the user's choices from delegated agent judgments and quotes only actual human wording as theirs. It can explain how decisions changed without inventing a human learning history.

# Rules

- Never author, suggest, or auto-fill `modeler_decision` or `modeler_rationale`. Pre-fill only `decision_id` / `options_considered` / `evidence` / `ai_suggestion`.
- Never decide which method is right, what a number means, or whether a result is good.
- Append-only. Never edit or delete a past record. A changed mind is a new record with `supersedes`.
- Do not log a `PENDING` artifact. Do not log an artifact that fails mechanical validation — return it to the gate.
- Validate identity, authority, completeness, source and current applicability using the shared contract; do not replace the producer's judgment with a new one.
- A method-choice narrative traces to the adopted rationale and actual decision-maker. Supplied-result writing may use its provided explanation/evidence matrix without inventing an internal historical log.
- Keep the mandatory decision-point set minimal (the four graded ones) to avoid authoring burden; the rest are opt-in.

# Verification

Before handing off, verify:

- Every `DECIDED` artifact for this Qx is reflected as exactly one record.
- No `PENDING` artifact was logged.
- The mandatory decision points (`method_choice`, `result_verdict`, `confidence`, `assumption_necessity`) exist for any Qx marked Ready-for-Writer.
- The global index matches the per-Qx logs.
- No record was edited in place; revisions used `supersedes`.
- No human field was authored by this skill.

# Failure modes

Stop and report a blocker if:

- A required decision artifact remains PENDING: return the specific authority/evidence gap to its responsible producer; a reserved user answer is not fabricated.
- A decision artifact fails mechanical validation (missing authority / unsupported actor / unresolved placeholder / absent evidence) — return it to the modeler with the exact field.
- A downstream skill asks this logger to author a rationale — refuse.
- A `result_verdict` record is stale (its underlying number changed) — flag for re-confirmation, do not silently keep it.

# Handoff

- To `final-method-explainer` / `solution-package-builder` / `paper-section-writer`: provide the `modeler_rationale` fields with `decision_id` tags as the narrative source.
- To `workflow-orchestrator`: report which mandatory decision points are present vs missing per Qx (gate input).
- To `consistency-auditor`: the log is a cross-media source — every "why we chose X" sentence in the paper must trace to a `decision_id` here.

# Relationship to the conventions

This skill operationalizes the [shared decision-authority contract](../workflow-orchestrator/references/decision-authority.md) by giving the scattered per-skill decision artifacts one canonical, append-only home, with the same immutability discipline as the **Frozen Numbers Convention**: append-with-`supersedes` is the decision-side analogue of `解冻 → 修改 → 重冻结`.
