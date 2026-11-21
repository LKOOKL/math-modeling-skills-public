---
name: workflow-orchestrator
description: Manage the full mathematical modeling contest workflow and decide which skill should be used next.
license: MIT
---

## Decision authority

Read the [shared decision-authority contract](references/decision-authority.md) when this skill produces or consumes a judgment. Resolve explicit delegation, human-reserved decisions and existing-results writing scope before applying the rules below. Human-only instructions and unresolved-human examples below describe the reserved branch; delegated decisions use `decided_by: agent_under_user_delegation` with an authorization reference and actual evidence. Never label an agent decision as human-authored.

# Purpose

**Trace format:** Follow [tracking-format.md](../write-math-modeling-papers/references/tracking-format.md). In `.tex`, put `% decision_id: Qx-D0n` on a standalone line before the prose; Markdown may use its own comment or mapping field. Format-neutral `decision_id:` examples below are identifiers, not text to print in the paper. Audit the source mapping and final PDF separately.

Coordinate the full mathematical modeling contest workflow from problem intake to final QA.

This skill is a **gate-driven scheduler**, not a stage-sequential scheduler. The difference matters: a stage scheduler answers "what stage are we in, what's the next stage?" — which lets work advance even when the current stage's outputs are unreliable. A gate-driven scheduler answers "does the current stage's gate pass — and if not, what's the fallback?" — which prevents drift from propagating downstream.

This skill does not solve models, write code, generate figures, or draft paper sections directly. Its role is to inspect the current project state across ALL subquestions, track per-question progress through a defined state machine, identify missing or blocked artifacts, **evaluate each workflow gate against its enter_condition / pass_criteria / fail_fallback contract**, route to the independent audit layer (consistency-auditor + completeness-auditor + quality-assurance-auditor) before final delivery, and decide the next appropriate skill to use.

This skill is the single source of truth for "what should we do next?"

# Route the current request first

- **Existing results; writing or layout only:** use `write-math-modeling-papers` and its input/evidence contract before the solve state machine. Record supplied sources and their actual verification status; fixed solver-folder names, missing PoCs or this suite's historical decision logs do not prevent writing supported material. Keep a missing sensitivity result as a local gap; do not run new calculations to fill it.
- **New modeling or authorized technical repair:** apply the solve gates below only to the requested technical scope. Carry explicit delegation and reserved decisions from the shared authority contract through every producer and consumer.
- **Audit/reproduction:** inspect the requested evidence; execute reproduction only when it is within the user's authorized scope. Existing results are not newly verified merely because they were supplied.

The three fixed-file handoff rules below govern artifacts produced by this solve pipeline. For supplied-result writing, equivalent traceable material satisfies the writing contract; report real evidence gaps without reconstructing an unrequested solve history.

# Task-scoped environment checks

For new solving, inspect the relevant environment below. For writing-only work, inspect only the supplied materials and document-build tools actually needed; do not create solver folders or import numerical packages as an entry requirement.

1. **Working tree status**: `git status --short`. If dirty (uncommitted changes, untracked files), surface the dirty files to the user before proceeding. Dirty working tree from a collaborator's in-progress work is the most common "git status looks weird" cause — flag it; do not silently work around it.
2. **Python availability**: `python --version` (or `python3 --version`). Flag if missing or wrong version.
3. **MATLAB / 北太天元 availability**: only when any Qx targets MATLAB. Check with `which matlab` or `command -v matlab`; if missing, report "MATLAB not in PATH — confirm 北太天元 will be used or switch implementation target to Python".
4. **Required scientific packages** (only when Python is the target): `python -c "import numpy, pandas, matplotlib"` — flag missing packages.
5. **Workspace skeleton**: verify `planning/`, `methods/`, `code/`, `results/`, `robustness/` and `paper/`. First resolve both historical data layouts in place using [the artifact contract](references/artifact-contract.md#resolve-existing-data-in-place); preserve existing paths in `planning/data_paths.json`. New-project defaults use `workspace/data/data_raw/` and `workspace/data/data_clean/`. A same-name content conflict requires an explicit mapping, not a new empty folder or an implicit search-order choice.

Report the environment ping result in the very first response of a new session. **Do not start state-machine work** until the user has seen this report, since downstream skills will silently fail if the environment isn't there. A two-line summary is enough: "Env OK: Python 3.11, MATLAB found, working tree clean" or "Env WARN: MATLAB missing, working tree has 3 uncommitted files in code/Q2/".

# When to use

Use this skill:

- At the beginning of a new mathematical modeling contest task.
- After any major artifact is created, updated, or reviewed.
- When the user is unsure what to do next or asks "what's the status?"
- When the user asks specific status questions: "is Q1 ready for the writer?", "what's blocking Q3?", "which question can be handed to the paper writer?", "who should work on what?"
- Before generating code, writing paper text, assembling the final paper, or submitting results.
- When the workflow appears inconsistent, incomplete, or out of order.
- When a subquestion needs to be returned to the modeler for method revision.

# Preconditions

This skill can run with minimal context. At least one of the following should be available:

- A contest problem statement.
- A workspace directory.
- Existing workflow artifacts.
- A user-provided status update.
- A request to determine the next step.

If none of these exists, ask the user to provide the problem statement, workspace tree, or current progress summary.

# Inputs

Inspect or request the following, depending on availability:

- Problem statement or problem file location.
- Current workspace tree (all directories).
- Existing artifacts under:
  - `planning/` — global plan, problem parse, classification, symbol table, model assumptions, question dependency.
  - `methods/Q1/`, `methods/Q2/`, `methods/Q3/`, `methods/Q4/` — method candidates, iteration logs, final method explanations.
  - `code/Q1/`, `code/Q2/`, `code/Q3/`, `code/Q4/` — generated scripts.
  - `results/Q1/`, `results/Q2/`, `results/Q3/`, `results/Q4/` — experiment outputs, reports, final result analyses, solution packages.
  - `robustness/Q1/`, `robustness/Q2/`, `robustness/Q3/`, `robustness/Q4/` — robustness reports.
  - `paper/sections/` — drafted paper sections.
  - `paper/figures/` — final paper figures.
- Existing progress dashboard at `planning/progress_dashboard.md` (update if present).
- User constraints such as contest deadline, allowed tools, preferred language, or team role distribution.

# Workflow

1. Inspect the current task state ACROSS ALL SUBQUESTIONS.
   - Check each subquestion's artifacts independently — different subquestions may be at different stages.
   - Identify available files, user-provided context, and completed artifacts.
   - Do not assume that a stage is complete only because a later file exists.
   - Do not assume all subquestions are at the same stage.

2. Determine each subquestion's status using the selected route: the per-question state machine for internal solves, or evidence intake and supported writing coverage for supplied-results writing.

3. Enforce workflow gates (see "Workflow Gates" section below for the enter_condition / pass_criteria / fail_fallback contract of each gate).
   - Gates for newly performed modeling steps (apply only when those steps are in scope):
     - Do not allow method selection before problem parsing and classification.
     - Do not allow code generation before a validated method plan exists.
     - Do not allow paper claims before model results exist.
     - Require all three auditor reports and final closure before final delivery; draft assembly and compilation may precede them.
   - Internal-solve handoff gates (the three critical rules; supplied-results writing uses the equivalent evidence intake):
     - Rule 1: Do not allow paper writing for Qx before `methods/Qx/qx_final_method_explanation.md` exists.
     - Rule 2: Do not allow writer handoff for Qx before `results/Qx/reports/qx_final_result_analysis.md` exists.
     - Rule 3: The paper writer should use `results/Qx/reports/qx_solution_package_for_writer.md` as primary source; if missing, Qx is NOT Ready for Writer.
   - **Gate failure propagation**: When any gate fails for Qx at stage N, mark all downstream Qx artifacts (stages > N) as DIRTY in the progress dashboard. Existing files at stages > N are not automatically valid just because they exist on disk — they may be downstream of a number that was wrong upstream.

4. Identify missing or blocked artifacts.
   - Mark missing files explicitly.
   - Mark blocked steps separately from merely incomplete steps.
   - If the blocker is user-side information, state exactly what is needed.
   - Per-subquestion blocking reasons must be specific (e.g., "Q2 needs method revision because round 2 experiment report shows M2 constraint violation").

5. Select the next skill.
   - Choose exactly one primary next skill.
   - Provide a short reason for the choice.
   - Provide concrete next actions for the user or agent.
   - If multiple subquestions need work, prioritize by dependency order (Q1 before Q2 if Q2 depends on Q1).

6. Update or produce the progress dashboard.
   - Save to `planning/progress_dashboard.md`.
   - Keep it up to date with current subquestion statuses.

7. Return a workflow state report.
   - Include the progress dashboard.
   - Include next skill recommendation.
   - Do not perform the downstream skill's work inside this skill.

# Workflow Gates (enter_condition / pass_criteria / fail_fallback)

Each gate is a hard checkpoint with three explicit parts. Do not skip a gate; do not advance on partial satisfaction. The state machine and the gates run together — the state machine says "what stage am I in", the gates say "can I leave this stage".

## Gate G1: PROBLEM_PARSED
- **enter_condition**: User provides a problem statement (file or text).
- **pass_criteria**:
  - Mechanical: `planning/parse/` exists (goals / objects / constraints / data / outputs / subquestions filled); `planning/classification/` exists with an `ai_suggested_type` per Qx.
  - Decision evidence: the evaluation criteria, chosen problem type, framing rationale and adopted relationships have supported sources and a valid decision owner under the shared contract. Unresolved placeholders in these required fields keep G1 pending; delegation may resolve a judgment but does not supply missing evidence.
- **fail_fallback**: Mechanical gaps → `problem-parser` / `problem-classifier`. Unresolved judgments → the authorized producer or, for a reserved decision, the user. Do not advance to G2 while the applicable fields remain unresolved.

## Gate G2: METHOD_VALIDATED  (load-bearing — most-violated boundary)
This is the method→code boundary. Most "漂亮方案到代码阶段才崩" issues happen because G2 was treated as soft.
- **enter_condition**: G1 passed; `data-auditor-cleaner` ran; `planning/symbol_table.md` and `planning/model_assumptions.md` exist.
- **pass_criteria**:
  - `methods/Qx/qx_method_candidates.md` exists with 2-4 candidates.
  - Every candidate has a runnable ≤30-line PoC script saved under `methods/Qx/poc/` AND a small-scale feasibility result (a number, a runtime, or a "fails on this data" verdict). A candidate without a PoC counts as "not yet validated".
  - Every candidate has a baseline designation or one of the candidates IS the baseline.
- **fail_fallback**: Route to `method-selector` to add the missing PoC. If PoC feasibility fails for a candidate, mark it `[REJECTED]`, move the PoC script to `workspace/archived/`, and route back to `method-selector` for an alternative.

## Gate G2.5: METHOD_CHOICE_RECORDED
- **enter_condition**: G2 passed; feasible candidates and their evidence are available.
- **pass_criteria**: the method-selector decision artifact is `DECIDED`, names a real candidate, explains the choice and alternatives using evidence, and passes the [authority/actor validity rules](references/decision-authority.md#validity-and-downstream-use). A delegated record is valid only within explicit authorization; a reserved decision requires the user's actual choice.
- **fail_fallback**: keep `code_generation_allowed_Qx = false`. Send the exact authority/evidence gap to the responsible decision producer; ask the user only for a still-reserved or unclear decision. Continue independent authorized work.
- **encoding**: `code_generation_allowed_Qx = G2_mechanical_pass ∧ G2.5_decision_pass`. A proposal alone is not a decision; the coordinator checks the record rather than inventing it.

## Gate G3: CODE_REVIEWED
- **enter_condition**: G2 passed; `code/Qx/` (Python) or `code/matlab/Qx/` (MATLAB) has scripts; experiments ran.
- **pass_criteria**:
  - Code-reviewer artifact exists at `code/Qx/reviews/qx_python_review.md` or `code/matlab/Qx/reviews/qx_matlab_review.md` with ≥ 5 explicit pass items.
  - Scripts produced `results/Qx/experiments/roundN/` with `run_summary.json` and at least one figures/tables/metrics file.
- **fail_fallback**: Route to `<lang>-code-reviewer`. If the review is insufficient (< 5 pass items), route back to the same reviewer with `completeness-auditor`'s gap report attached.

## Gate G4.5: RESULT_DECISIONS_RECORDED
- **enter_condition**: G3 passed; actual experiment and robustness evidence exists.
- **pass_criteria**: `result-report-generator` records per-method verdicts, the next-round decision and claim confidence; `robustness-checker` records stability and its supporting metrics; `final-method-explainer` records assumption labels and the adopted evaluation threshold. Their decision artifacts are `DECIDED` and satisfy the shared authority contract. Method-selection prose retains its existing decision source.
- **fail_fallback**: keep `freeze_allowed_Qx = false` for a missing decision, missing authorization or missing technical evidence. An authorized producer may complete a delegated judgment; a human-reserved point stays pending for the user's answer. Do not infer verdicts from `ai_suggestion`.
- **encoding**: `freeze_allowed_Qx = G3_mechanical_pass ∧ G4.5_decision_pass`; the package sign-off at G4 is additionally required.

## Gate G4: RESULTS_FROZEN  (load-bearing — second-most-violated boundary)
This is the results→paper boundary. Most "论文里数字与最新 results 错位" issues happen because G4 was treated as soft. **G4 now requires G4.5 to have passed** (the valid decision records must exist before the freeze) plus the package sign-off.
- **enter_condition**: G4.5 passed (`freeze_allowed_Qx = true`); `results/Qx/reports/qx_final_result_analysis.md` exists.
- **pass_criteria**:
  - `methods/Qx/decisions/solution-package-builder_modeler_decision.md` is `DECIDED` (`decision_id: qx_package_signoff`): per-flagged-claim `approve ∈ {keep,downgrade,drop}` + package confidence recorded by the authorized decision-maker under the shared contract.
  - `results/Qx/reports/frozen_numbers.json` exists with a `frozen_at` timestamp.
  - `frozen_numbers.json.provenance` follows [the content-hash contract](references/artifact-contract.md#qx-freshness-is-a-content-comparison), covers the actual code/data/parameters/environment/result/upstream dependencies and is `CURRENT`. Input-only changes invalidate the affected Qx and dependent results, figures, prose and audits; mtime-only changes do not. Legacy mtime/code-only records remain `UNVERIFIED_LEGACY` until supported migration closes the gap.
  - `results/Qx/reports/qx_solution_package_for_writer.md` exists; every numerical claim in it is sourced from `frozen_numbers.json`; every "why we chose X" sentence traces to a `decision_id` in `methods/Qx/qx_decision_log.md`.
- **fail_fallback**: If the package sign-off is missing/PENDING, build the human-readable package but DO NOT emit `frozen_numbers.json` — route to the authorized sign-off producer, retaining any human reservation. After freeze, if `consistency-auditor` later detects drift, route to the **解冻 → 修改 → 重冻结** three-step:
  1. The authorized modeler/programmer resolves which value is canonical from the underlying evidence and records the actual actor; a human-reserved choice stays with the user.
  2. Update the canonical source (code or analysis report).
  3. Re-run `solution-package-builder` to re-freeze. Do not edit `frozen_numbers.json` by hand.

## Gate G5: PAPER_SECTION_READY
- **enter_condition**: internal solve handoff has passed G4, or supplied-results writing has completed evidence intake for the intended scope; the supported `paper/sections/qx.tex` draft exists.
- **pass_criteria**:
  - Evidence and presentation: the section answers its question, links its adopted evidence and explains relevant conditions and limits; figures exist and have the required visual checks. Word-count ranges and suggested discussion dimensions are editorial prompts, not pass/fail thresholds. Brief deterministic or not-applicable cases may be concise; missing applicable evidence remains a real gap.
  - Structure: each Qx is a `\section` with separate `\subsection` blocks for results analysis, error analysis, sensitivity analysis and other applicable checks. Each block contains Qx-specific evidence, explanation and boundaries, or an explicit missing-evidence/not-applicable record. Shared methods may be referenced; a global validation chapter does not replace per-Qx analysis. Check the expanded LaTeX hierarchy, following [the per-question structure contract](../write-math-modeling-papers/references/chapter-workflow.md#逐问结果分析的层级与归属); document any explicit user or mandatory-template exception. A material evidence gap still prevents a completed-paper claim.
  - Template and procedure coverage: follow [the user-template contract](../write-math-modeling-papers/references/user-template-contract.md) for chapter order and allowed minor edits. Every final model in every Qx has at least one source-backed pseudocode or flowchart inside that Qx's model/solution section, with a label and prose explanation. Missing coverage routes to `figure-table-planner`/`paper-section-writer`; missing underlying technical steps route to the authorized modeler/solver, without silently expanding writing into computation.
  - Decision provenance: physical interpretation, paper seeds and figure claims use the supplied evidence and valid decision records within the current writing scope. Preserve the actual decision-maker and the document-appropriate provenance marker. Delegated reasoning is not labeled human-authored; unresolved reserved decisions and technical gaps stay explicit.
- **fail_fallback**: missing or wrongly assigned analysis subsections and presentation gaps → `paper-section-writer`; missing technical evidence → the authorized upstream producer, without expanding writing into new computation. Unresolved human-reserved decisions go to the user. A short section or fewer discussion dimensions alone is not a failure.

## Gate G6: AUDIT_LAYER_PASSED (final delivery)
The legacy field `final_assembly_allowed` means approval for final delivery; it does not prohibit assembling or compiling a draft for review.
This is the independent-audit gate. No single skill's "完成" claim can bypass it.
- **enter_condition**: the intended manuscript scope is drafted, available evidence and gaps are recorded, and references are managed. Draft assembly/compilation precedes audit when needed to inspect the actual document.
- **pass_criteria** (all three independent audits must PASS):
  - `paper/audits/cross_media_consistency_audit.md` — verdict PASSED.
  - `paper/audits/completeness_audit.md` — final-scope verdict PASSED, including the completed QA report.
  - `paper/qa_report.md` — verdict PASSED.
- **fail_fallback**: Route to whichever auditor failed. Never approve `final_assembly_allowed=true` on partial audit. The three auditors are orthogonal — passing one does not imply the others.

First review follows [pre-QA and final closure](references/decision-authority.md#first-final-review-cycle): completeness may pass its `pre_qa` scope with QA marked `SCHEDULED`; QA then runs; completeness checks the QA artifact in `final` scope. Final delivery requires all three reports for the same adopted content and no unresolved blocker. Closure-only report metadata updates do not themselves invalidate the preceding QA.

## Gate dependency graph

```text
New solve: G1 → G2 → G2.5 → G3 → G4.5 → G4 → G5
Writing from supplied results: evidence intake → supported manuscript + explicit gaps → G5
Final review: consistency + pre_qa completeness → QA → final completeness → G6 → delivery
```

Decision gates apply the same authority contract to a human-reserved choice and an explicitly delegated choice, preserving their different actors. A failed technical gate marks affected downstream artifacts for review; recovery requires the missing authority/evidence and checks on affected content, not a fresh request for permission already granted.

# Per-Question State Machine

Each subquestion Qx moves through these states in order. The state is determined by which artifacts exist.

```
[01] Method Candidates Drafted
      → methods/Qx/qx_method_candidates.md exists
      ↓
[02] Code Implementation In Progress
      → code/Qx/ has scripts, experiment not yet run or running
      ↓
[03] Experiment Report Ready (Round N)
      → results/Qx/experiments/roundN/qx_experiment_report_roundN.md exists
      ↓  (may loop back to [01] or [02] if method revision needed)
[04] Needs Method Revision
      → experiment report indicates issues; loop back to modeler
      ↓  (after revision, return to [02] or [03])
[05] Final Method Selected
      → a valid final-method decision records the actual authorized actor
      ↓
[06] Final Method Explained
      → methods/Qx/qx_final_method_explanation.md exists
      ↓
[07] Final Result Analyzed
      → results/Qx/reports/qx_final_result_analysis.md exists
      ↓
[08] Solution Package Built
      → results/Qx/reports/qx_solution_package_for_writer.md exists
      ↓
[09] Ready for Writer
      → all [06], [07], [08] exist; writer can start
      ↓
[10] Writer Draft Ready
      → paper/sections/qx.tex or equivalent exists
      ↓
[11] Reviewed by Modeler
      → model-role review verifies the paper against the adopted method and records its actual reviewer
      ↓
[12] Reviewed by Programmer
      → code-role review verifies results and figures against outputs and records its actual reviewer
      ↓
[13] Finalized
      → all reviews passed; ready for final delivery
```

The orchestrator determines which state each subquestion is in by checking which files exist and reading the latest experiment report verdicts. The state labels describe roles, not a requirement to invent human reviews: delegated technical reviews record the agent as reviewer, while explicitly reserved or mandatory human review remains pending until actually performed. This state machine applies to the internal solve route; supplied-results writing uses its evidence intake instead of reconstructing states 01–09.

# Progress Dashboard

Maintain per-question status, applicable gate results, unresolved evidence/authority gaps and the next action in `planning/progress_dashboard.md`. Record the current task route and distinguish pre-QA readiness from final delivery. See the [dashboard example](references/examples.md#progress-dashboard) only when a concrete format is needed.

# Expanded Workflow Stages (Global)

The full global workflow now includes per-subquestion iteration loops:

```
【0】全题启动阶段 (Global Setup)
problem-parser → problem-classifier → related-paper-analyzer
    → global symbol table → global model assumptions → question dependency map
    ↓
【1】候选方法池阶段 (Per-Question Start)
method-selector → methods/Qx/qx_method_candidates.md
    ↓
【2】编程实验阶段 (Per-Question, Multi-Round)
model-code-analyzer → python/matlab-model-code-generator → code-reviewer
    → results/Qx/experiments/roundN/
    ↓
【3】实验报告阶段 (Per-Question, Per-Round)
result-report-generator → results/Qx/experiments/roundN/qx_experiment_report_roundN.md
    ↓
【4】方法迭代循环 (Per-Question Loop)
    ← modeler reviews report → revises methods → back to 【2】
    OR → proceed to 【5】
    ↓
【5】最终方法锁定
final-method-explainer → methods/Qx/qx_final_method_explanation.md
    ↓
【6】最终结果分析
result-report-generator (final mode) → results/Qx/reports/qx_final_result_analysis.md
    ↓
【7】稳健性分析
robustness-checker → robustness/Qx/qx_robustness_report.md
    ↓
【8】论文材料包
solution-package-builder → results/Qx/reports/qx_solution_package_for_writer.md
    ↓
【9】图表规划
figure-table-planner → paper/figures/ planning
    ↓
【10】论文写作 (Per-Question)
paper-section-writer → paper/sections/qx.tex
    ↓
【11】建模手审核 → 【12】编程手审核
    ↓
【13】独立审计层 (NEW — three orthogonal audits, all must PASS to advance)
  ├─ consistency-auditor   → paper/audits/cross_media_consistency_audit.md
  ├─ completeness-auditor  → paper/audits/completeness_audit.md
  └─ quality-assurance-auditor → paper/qa_report.md
    ↓ (only if all three PASS — Gate G6)
【14】终稿交付
Deliver the audited main.tex + sections + figures and final PDF; assemble/compile drafts before audit when needed.

If any of the three audits FAIL:
  → route to the failed auditor's recommended repair skill
  → re-run the failed audit after repair
  → never advance to 【14】 on partial audit
```

# The Three Critical Rules (internal-solve handoff)

These file-based rules govern the suite's internal solve route. Supplied-results writing uses equivalent adopted technical sources and an evidence matrix; missing historical internal files do not require reconstruction:

## Rule 1: No final paper writing without final method explanation

`paper-section-writer` MUST NOT write final paper sections for Qx based only on `qx_method_candidates.md` or early method plans. The orchestrator checks that `methods/Qx/qx_final_method_explanation.md` exists before routing Qx to the paper writer.

For an internal-solve handoff, a missing final method explanation blocks that gate and routes to `final-method-explainer`. For supplied material, the writer checks the supplied method and marks only missing technical details as gaps.

## Rule 2: No writer handoff without final result analysis

Program execution outputs alone are NOT sufficient for writer handoff. The orchestrator checks that `results/Qx/reports/qx_final_result_analysis.md` exists before marking Qx as Ready for Writer.

For an internal-solve handoff, raw outputs alone do not complete the result-analysis gate; route the missing analysis to `result-report-generator`. For supplied-results writing, first use the writing intake to identify supported material and exact interpretation gaps; do not automatically trigger new solving.

## Rule 3: Writer reads from the solution package, not scattered results

The paper writer's primary source for Qx is `results/Qx/reports/qx_solution_package_for_writer.md`. The orchestrator checks that this file exists before routing Qx to the paper writer.

If the internal-solve package is missing, route to `solution-package-builder`. Supplied-results writing uses its source matrix and does not create a historical package solely to pass this rule.

# Status Query Responses

The orchestrator should be able to answer these questions precisely:

- **"Q1 现在卡在哪？"** → State the exact status (e.g., "Q1 is at state [08] Solution Package Built — waiting for solution-package-builder. It needs: nothing. It is blocked by: nothing.")
- **"哪个小问可以交给论文手？"** → List subquestions at state [09] Ready for Writer (e.g., "None yet. Q1 is closest at [08] — one step away.")
- **"哪个小问缺最终方法详解？"** → List subquestions at state [05] or earlier (e.g., "Q2, Q3, Q4 are missing final method explanations. Q2 is at [04] Needs Method Revision.")
- **"哪个小问只有结果没有解释？"** → List subquestions with results but no analysis report (e.g., "Q3 has raw results in results/Q3/experiments/round1/ but no analysis report.")
- **"哪个小问需要退回建模手？"** → List subquestions at state [04] Needs Method Revision (e.g., "Q2 needs method revision — M2 constraint violation.")

# Outputs

Produce a workflow state report containing:

- `current_global_stage`
- `progress_dashboard` (link to or contents of `planning/progress_dashboard.md`)
- `per_question_status` (state machine state for each Qx)
- `completed_artifacts`
- `missing_artifacts`
- `blocked_items` (global and per-question)
- `workflow_gates` (global and per-question)
- `three_critical_rules_check`
- `next_skill`
- `next_actions`
- `handoff_context`
- `runners_up` (alternative next skills if the primary is already in progress)

# Output format

Return the current task route, per-question status, allowed actions, concrete blockers, next skill and its source inputs. A supplied-results writing request need not instantiate the solve dashboard schema. The [JSON example](references/examples.md#output-format) is an optional representation.

# Rules

- Do not solve the mathematical model.
- Do not select specific algorithms unless the next step is only to route to `method-selector`.
- Do not write code.
- Do not draft paper sections.
- Do not fabricate missing artifacts.
- Do not infer completion without evidence.
- Do not skip workflow gates for speed.
- Do not approve final delivery without the full audit layer passing (Gate G6 — consistency + completeness + QA all green).
- Do not treat one auditor's PASS as sufficient for final delivery; all three reports and final closure are required. Draft assembly/compilation may run earlier.
- Resolve the task route, then run the task-relevant environment ping. Writing-only work does not require numerical imports or solver-folder creation.
- Check G2.5 and G4.5 against the shared authority contract. A valid delegated record may pass; never invent human participation or promote a proposal into a verdict without a recorded authorized decision.
- Use `decision-prompt-builder` only for a still-reserved or materially unclear decision. Explicit delegation and `learning`/`speed` are separate inputs; presentation mode never creates authority or revokes an existing delegation.
- Enforce route-applicable source-fidelity rules at each handoff: internal packages for the solve route, or adopted supplied sources/evidence matrix for writing.
- Track per-question status separately — different subquestions are at different stages.
- Update the progress dashboard whenever the state changes.
- Keep recommendations tied to traceable artifacts.
- Prefer one clear next step over many speculative branches.
- If a subquestion is blocked, state exactly what needs to happen to unblock it.
- If the modeler or programmer needs to act, be specific about what they need to do.

# Verification

Before handing off, verify:

- The chosen `next_skill` matches the earliest incomplete required stage for the highest-priority subquestion.
- No workflow gate is bypassed (global or per-question).
- Source fidelity is checked for the target subquestion according to its internal-solve or supplied-results route.
- Missing artifacts are explicitly listed.
- Blocked items are separated from ordinary incomplete items.
- The next actions are concrete enough to execute.
- The handoff context includes the minimum inputs needed by the next skill.
- The progress dashboard reflects the current state (update if needed).

# Failure modes

Stop and report a blocker if:

- The problem statement is missing.
- The user asks to generate code but no method plan exists.
- The user asks to write numerical conclusions but no model results exist.
- The user requests final delivery or submission before QA and final audit closure pass. Draft assembly or compilation for review remains allowed.
- An internal-solve writer handoff lacks `qx_final_method_explanation.md` (Rule 1); supplied-results writing checks the equivalent provided method.
- An internal-solve writer handoff lacks `qx_final_result_analysis.md` (Rule 2); supplied-results writing checks the supported result interpretation and records gaps.
- An internal-solve writer handoff lacks its required solution package (Rule 3); an external-source matrix satisfies the equivalent supplied-results route.
- The workspace state is inconsistent, such as paper claims existing without corresponding results.
- Multiple incompatible interpretations of the current task exist and the choice affects workflow order.
- A subquestion dependency is violated (e.g., Q2 code references Q1 results that don't exist).

# Stop conditions

This skill must stop instead of guessing when:

- Required artifacts cannot be located.
- The current stage cannot be determined from available context.
- A downstream skill would need fabricated data, fabricated results, or unsupported assumptions.
- A route-applicable required gate cannot pass within the current authorization or available evidence; identify that exact conflict rather than stopping supported independent work.
- The per-question state cannot be determined because artifacts are missing and the user cannot clarify.

When stopping, output:

- the blocker
- why it matters
- the minimum information or artifact needed to continue
- which subquestion is affected
- the recommended next skill once the blocker is resolved

# Handoff

Typical handoff order (global, then per-question):

1. `problem-parser`
2. `problem-classifier`
3. `related-paper-analyzer`
4. **Create global symbol table, model assumptions, dependency map** (planning stage)
5. `method-selector` (per Qx — can run in parallel for independent subquestions)
6. `model-code-analyzer`
7. `python-model-code-generator` or `matlab-model-code-generator`
8. `code-reviewer`
9. `result-report-generator` (round N experiment report)
10. **Loop back to 5 or 6** if method revision needed
11. `result-report-generator` (final result analysis, when method is locked)
12. `final-method-explainer`
13. `robustness-checker`
14. `figure-table-planner`
15. `solution-package-builder`
16. `paper-section-writer`
17. **Modeler review → Programmer review**
18. `reference-manager` (verify citations are real)
19. `paper-polisher` (style / hedging / formula consistency within paper)
20. **Independent audit layer (Gate G6 — three orthogonal audits, all must PASS):**
    - `consistency-auditor` (cross-media numbers / files / symbols / parameters)
    - `completeness-auditor` (every claimed completion has a substantive artifact on disk)
    - `quality-assurance-auditor` (workflow completeness + three critical rules + anti-fabrication + paper quality)
21. Back to `workflow-orchestrator` for final delivery (only when Gate G6 passes)

If the workflow is complete and **all three audits pass**, hand off to final delivery or user review. A single auditor "✅" is NOT sufficient — the three are orthogonal and must converge.

# Examples

Read [routing and output examples](references/examples.md) when resolving a task-route or first-review ambiguity. The authority and gate contracts above remain the source of requirements.
