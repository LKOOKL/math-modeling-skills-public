# Decision authority and provenance

Read this contract when a skill produces, records, consumes or checks a modeling decision. It is the package's shared authority contract; no external `CLAUDE.md` is required. User instructions and host permissions determine the authorized scope. A skill cannot expand that scope.

## Choose the authority before asking or deciding

| Situation | Action and record |
|---|---|
| The user explicitly delegates the relevant modeling decisions, for example “自主完成建模、求解和论文写作” | Continue within that scope. The responsible modeling/result skill may decide and document its reasoning as `agent_under_user_delegation`, citing the actual authorization. Do not ask again for the same delegated decision. |
| The user reserves a decision, asks to approve before execution, or an applicable mandatory rule requires actual human review | Keep that decision human-reserved. Prepare the evidence and a concrete choice for the user; complete independent authorized work while it is pending. A general delegation does not override a more specific reservation. |
| Authorization is absent, ambiguous or does not cover the decision | Ask one focused clarification about the consequential gap. Do not infer authorization from silence, elapsed time, a draft suggestion, a file's existence, or `mode: speed`. |
| The user has already decided or explicitly accepted a specified recommendation | Record the actual choice and its source as `human`; preserve the distinction between the user's acceptance and any agent-written explanatory text. Do not invent a human rationale. |

`learning` and `speed` control explanation and question presentation only. They do not grant or revoke authority. Use the learning-mode question-first exercise when the user chose that teaching interaction; explicit delegation still governs decisions within its scope.

## Shared record

Existing `*_modeler_decision.md` filenames and `modeler_rationale` keys remain readable for compatibility. The actual actor is determined by metadata, never by those legacy names. New records use these fields:

```yaml
schema_version: 1
skill: method-selector
scope: Q1
decision_id: q1_method_choice
decision_point: method_choice
status: PENDING                 # PENDING | DECIDED | STALE
authority: human_reserved       # human_reserved | delegated
authorization_ref: null         # session message or authorization record, including scope
decided_by: null                # human | agent_under_user_delegation; null while pending
decided_at: null
human_review: false             # true only for an actual, separately evidenced human review
human_review_ref: null
choice: null
rationale: null
evidence_refs: []
supersedes: null
```

The producing skill adds the decision-specific fields already required for that task: alternatives/reasons, result verdict, confidence, round decision, assumption labels, or per-claim `keep/downgrade/drop`. Evidence references identify the relevant result, candidate, assumption or source and its adopted version. The reason must explain the choice and its boundaries; fixed character floors are not a substitute for substance. Quantitative confidence or stability claims cite the actual metric supporting them.

For a delegated record, `authorization_ref` must identify the explicit delegation and show that this decision is covered. The agent writes its own choice/reason, sets `decided_by: agent_under_user_delegation`, and keeps `human_review: false` unless a separate human review actually occurred. Agent authorship is not a fabricated human answer. For a reserved decision, leave the choice pending until the user responds; record their actual response faithfully. An expressly accepted recommendation may resemble the earlier suggestion: similarity alone neither proves human participation nor invalidates a documented acceptance.

## Validity and downstream use

A decision passes its gate only when: (1) it is `DECIDED`; (2) the actual actor and scope of authority are evidenced; (3) the required choice/reason and supporting evidence exist without unresolved placeholders; and (4) the adopted technical evidence is still applicable. `human_review: true` additionally requires `human_review_ref`. Unsupported `decided_by: human`, missing delegation, unresolved scope conflicts and stale evidence fail the gate. Delegation never supplies missing technical evidence or waives numerical checks.

The designated producer makes a delegated judgment; `modeler-decision-logger` validates and appends it, and downstream writers/auditors preserve its provenance. A logger or writer does not silently change an existing choice. A change is a new authorized decision with `supersedes`, followed by review of affected claims. The coordinator may check a valid delegated record as passed; it may not infer a verdict from `ai_suggestion` or manufacture a record merely to turn a dashboard green.

For framing, assumptions, physical meaning and figure claims, apply the same authority rules to the judgment-bearing fields. A human-reserved field retains a concrete pending marker; an authorized producer may resolve a delegated field with evidence and actor metadata. Do not strip markers solely to make a check pass. Preserve unresolved evidence gaps even when decision authority is delegated. Historical human-mode examples and `<<<HUMAN>>>` placeholders illustrate the reserved branch, not a universal ban on delegated work.

## Existing-results writing route

When the current task is writing/layout from supplied technical material, route first to `write-math-modeling-papers`. Map the existing sources into its evidence matrix and keep source/verification status explicit. Equivalent supplied material can satisfy the writing input contract without recreating this suite's solver folders, PoCs, decision artifacts or frozen files. Missing technical evidence stays a named writing gap; continue independent supported text. Do not start the solve pipeline, run experiments, recreate historical decisions, or label supplied results as newly verified merely to satisfy a local workflow convention.

If the user separately authorizes new modeling or technical repair, apply the solve gates to that work. Writing-only permission remains insufficient for numerical work. Technical submission/release approval and actual human review retain their own explicit requirements; neither follows automatically from permission to write.

## First final-review cycle

Draft assembly and document compilation may occur before the final audit; they provide the material the auditors inspect. Final delivery remains gated on all three substantive reports for the same adopted manuscript/results.

1. `consistency-auditor` checks the current artifacts. `completeness-auditor` runs with `audit_scope: pre_qa`, checking only artifacts that should already exist. If QA has not run or claimed completion, record its report as `SCHEDULED`, not missing-completed work. `PASSED` here means pre-QA readiness only; `final_delivery_allowed: false`.
2. QA consumes the consistency PASS and pre-QA completeness PASS, performs its own checks, and writes `paper/qa_report.md`. A successful QA report may state `qa_checks: PASSED` and `audit_closure: PENDING_FINAL_COMPLETENESS`; this does not authorize delivery.
3. Completeness performs a narrow `audit_scope: final` closure: verify the QA report exists, contains substantive checks and no unresolved blocker, and that the audited manuscript/results have not changed. Preserve its earlier findings and record the prior pre-QA review identity. Pure closure metadata changes do not invalidate QA or require a fresh numerical review. If substantive inputs changed, review the affected content instead of relying on this exception.
4. The coordinator records G6 PASS only when consistency, final-scope completeness and QA's own checks all pass for the same adopted content, with no unresolved blocking issue. QA may record final closure as a metadata-only update referencing final completeness. No audit requires its own completed output as an input. A final-scope missing QA report is blocking.

This is an ordering rule, not an exemption from any final report. Track the reviewed content and scope; do not use one audit file's later modification time alone to create an endless mutual-review loop.
