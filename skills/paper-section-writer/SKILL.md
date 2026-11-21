---
name: paper-section-writer
description: Write mathematical modeling paper sections based only on available problem analysis, model plans, results, figures, and robustness reports.
license: MIT
---

## Decision authority

Read the [shared decision-authority contract](../workflow-orchestrator/references/decision-authority.md) when this skill produces or consumes a judgment. Resolve explicit delegation, human-reserved decisions and existing-results writing scope before applying the rules below. Human-only instructions and unresolved-human examples below describe the reserved branch; delegated decisions use `decided_by: agent_under_user_delegation` with an authorization reference and actual evidence. Never label an agent decision as human-authored.

# Purpose

**Trace format:** Follow [tracking-format.md](../write-math-modeling-papers/references/tracking-format.md). In `.tex`, put `% decision_id: Qx-D0n` on a standalone line before the prose; Markdown may use its own comment or mapping field. Format-neutral `decision_id:` examples below are identifiers, not text to print in the paper. Audit the source mapping and final PDF separately.

Write mathematical modeling paper sections from validated workflow artifacts.

This skill turns the final method explanation, final result analysis, solution package, and figure-table plan into structured paper section drafts. It must keep every claim traceable to an artifact and must not invent data, numerical results, figures, references, or unsupported conclusions.

**Select the input route first.** For an existing-results writing/layout request, use [write-math-modeling-papers](../write-math-modeling-papers/SKILL.md) as the primary entry and its source/evidence matrix; this section writer may then draft the supported parts. Equivalent supplied solutions, tables and procedure descriptions do not need to be converted into solver-stage files. Missing sensitivity evidence stays in that question's sensitivity subsection; writing does not run new checks. For a handoff from this suite's solve pipeline, enforce the three internal artifact rules below and the adopted frozen source. Do not treat internal filenames as universal writing prerequisites.

This skill does not run models, generate new results, create unsupported figures, perform final QA, or approve final submission.

# When to use

Use this skill:

- After `solution-package-builder` has produced the solution package for a subquestion.
- After `figure-table-planner` has produced the figure-table plan.
- When all three critical rule prerequisites are met for the target subquestion.
- When paper section drafts are needed.
- When existing section drafts need to be aligned with validated artifacts.
- Before `quality-assurance-auditor`.

For the internal solve-pipeline route, do NOT claim complete final sections:
- To write final paper sections for Qx when `methods/Qx/qx_final_method_explanation.md` is missing.
- To write final paper sections for Qx when `results/Qx/reports/qx_final_result_analysis.md` is missing.
- To write final paper sections for Qx when `results/QX/reports/qx_solution_package_for_writer.md` is missing (the writer's primary source).

# Gate G5: Section Quality (NEW — load-bearing for paper external quality)

In addition to the input checks for the selected writing route, assess whether each section answers its task with traceable evidence and clear limits. Length and discussion prompts below are editorial advice; required structure and material evidence checks remain completion criteria.

## G5.1 Length guidance (editorial advice)

Choose length from the question, available evidence and applicable submission rules. There is no internal minimum word or character count. A deterministic calculation or a task without raw samples may need only a short data-preprocessing statement; no cleaning operation may be invented to lengthen it. Compact sections can be complete when their purpose, answer, supporting source and relevant boundaries are clear.

Use section-level content prompts as a review aid: the abstract summarizes supported answers; model/solution sections explain the adopted model and actual procedure; results state and interpret the answer; evaluation connects strengths and limits to evidence. Record an actionable content gap only when required information is missing. Do not assign `under_floor` merely because prose is short, and do not add an independent conclusion chapter to satisfy a length target.

These recommendations do not relax the structure contract: every Qx remains a `\section`, with separate results-analysis, error-analysis and sensitivity-analysis `\subsection` blocks. Other applicable checks stay local. Each final model in each Qx retains at least one source-backed pseudocode or flowchart. Missing evidence is explicit in the affected subsection; justified non-applicability receives a concise reason.

## G5.2 Evidence-led discussion (editorial advice)

Select discussion that helps interpret the actual answer. Sensitivity, domain meaning, baseline comparison, cross-question consistency and uncertainty are optional prompts, not a required count per number. A descriptive table or deterministic answer does not need three artificial discussion dimensions. Identify the quantity, units, conditions and source, then explain the conclusions and limits supported by the materials.

Only discuss perturbations, confidence intervals or comparisons when corresponding evidence exists. Do not introduce an arbitrary plus/minus 10 percent test or run new calculations to fill a heading. Missing applicable sensitivity evidence leaves a named gap in that Qx sensitivity subsection while other supported writing continues. A truly inapplicable analysis retains its reason; missing evidence is not non-applicability.

Judgment-bearing interpretations follow the [decision-authority contract](../workflow-orchestrator/references/decision-authority.md); record the actual source, decision maker and review status without treating an AI draft as human review. In the output summary, use `discussion_review` to record applicable prompts, covered evidence, justified non-applicability and material gaps. Completion depends on task coverage and evidence, not on a dimension counter.

## G5.3 Claim selection and decision provenance

The abstract's `key_result_claim`, any supported `contribution_claim`, and each Qx's `why_this_method` must match the adopted technical material and actual decision records. For this suite's solve route, retain the logged decision and document-appropriate marker from [tracking-format.md](../write-math-modeling-papers/references/tracking-format.md). For supplied-result writing, cite the provided explanation and evidence matrix; do not reconstruct a fictional historical decision log.

Writing may organize supported answers and restate supplied interpretations. It does not create a new model-selection judgment or unsupported innovation claim. If a new consequential choice is needed, follow the shared authority contract: an already authorized producer can record a delegated decision, and a user-reserved choice stays pending. Actual actor and review status remain distinct. A missing applicable explanation or result is a concrete writing gap; a human-input marker is not required merely because the source reasoning was produced by an authorized agent.

# Three internal solve-pipeline handoff rules

Apply these fixed-file rules only to the internal solve-pipeline route. Supplied-result writing uses equivalent traceable materials under the main writing input contract; it may draft supported parts while naming specific gaps.

## Rule 1: No final paper writing without final method explanation

```
GATE CHECK: methods/Qx/qx_final_method_explanation.md MUST exist.
```

If missing: Stop. Do NOT write the paper section for Qx. The paper writer cannot write the model construction section without knowing the final method, its assumptions, symbols, and mathematical specification. Redirect to `workflow-orchestrator` with a clear blocker report.

The paper writer MAY write a partial draft for other sections that don't depend on the final method (e.g., problem restatement), but MAY NOT write the model construction or results analysis sections.

## Rule 2: No writer handoff without final result analysis

```
GATE CHECK: results/Qx/reports/qx_final_result_analysis.md MUST exist.
```

If missing: Stop. Do NOT write the results analysis section for Qx. Raw experiment outputs are not sufficient — the results must have been analyzed and interpreted by the programmer. Redirect to `workflow-orchestrator` with a clear blocker report.

## Rule 3: Writer reads primarily from the solution package

```
GATE CHECK: results/Qx/reports/qx_solution_package_for_writer.md MUST exist.
```

If missing: Stop. Do NOT write the paper section for Qx by hunting through scattered results and method notes. The solution package is the writer's curated source. If it's missing, the subquestion is NOT Ready for Writer. Redirect to `workflow-orchestrator` or `solution-package-builder`.

# Preconditions

For internal solve-pipeline handoff, the following artifacts are required. For external supplied-result writing, record equivalent sources and their status; no numerical work or fabricated historical records are authorized by this intake.

**REQUIRED (hard gates — verified at start)**:
1. `methods/Qx/qx_final_method_explanation.md`
2. `results/Qx/reports/qx_final_result_analysis.md`
3. `results/Qx/reports/qx_solution_package_for_writer.md`

**Also required for complete sections**:
- `methods/Qx/qx_figure_table_plan.md` (figure and table plan).
- Actual figure files referenced in the solution package (must exist on disk).
- Robustness report at `robustness/Qx/qx_robustness_report.md` (for robustness section).
- A validated problem parse (for problem restatement).
- Contest formatting requirements (if available).

**For global sections** (abstract, problem restatement, assumptions, symbols, conclusion):
- All subquestion final method explanations (for symbols and assumptions).
- All subquestion final result analyses (for abstract and conclusion).

If an applicable internal handoff artifact is missing, report that gap before calling the pipeline handoff complete. In supplied-result writing, judge the actual source content and continue supported sections.

# Inputs

Use or request (for Qx paper section):

**Primary sources (read first)**:
- `results/Qx/reports/qx_solution_package_for_writer.md` — THE primary source for the writer.
- `methods/Qx/qx_final_method_explanation.md` — method details.
- `results/Qx/reports/qx_final_result_analysis.md` — result details.

**Supporting sources**:
- `methods/Qx/qx_figure_table_plan.md` — figure/table assignments.
- `methods/Qx/qx_method_candidates.md` — for method selection narrative.
- `methods/Qx/qx_method_iteration_log.md` — for iteration history context.
- `robustness/Qx/qx_robustness_report.md` — for robustness section.
- Existing paper section drafts under `paper/sections/`, if any.
- Global symbol table and model assumptions (from `planning/`).
- Problem parse and classification artifacts.
- Contest paper structure or formatting notes.

# Workflow

1. **Select the input route and verify its evidence.**
   - For internal solve-pipeline handoff, check the three required artifacts and adopted frozen source.
   - For supplied-result writing, map the provided methods/results/procedures to the main writing evidence contract; fixed internal filenames are not prerequisites.
   - Report missing evidence in the affected question and continue independent supported text. Do not run a solver or reconstruct unprovided decisions.

2. Read the internal solution package or the supplied-material evidence matrix first.
   - The solution package is the writer's primary source. It summarizes everything.
   - Use it to understand the overall narrative before diving into detailed source files.
   - Follow its section mapping, claims inventory, and figure assignments.

3. Gather the detailed sources.
   - Read the final method explanation for model details.
   - Read the final result analysis for numerical claims.
   - Read the figure-table plan for visual assignments.
   - Read the robustness report for sensitivity claims.

4. Build a section map.
   - Apply [the user's national-contest template contract](../write-math-modeling-papers/references/user-template-contract.md): preserve its main chapter order and per-Qx "模型建立与求解" sections; integrate writing experience through local subsections, evidence and explanations. Record permitted minor edits; a different top-level structure needs an explicit basis.
   - Map each subquestion to the paper sections that should answer it.
   - Use one `\section` per Qx. Within it, create separate `\subsection` entries for results analysis, error analysis, sensitivity analysis, and each other applicable robustness, feasibility or comparison analysis. Follow [the per-question structure contract](../write-math-modeling-papers/references/chapter-workflow.md#逐问结果分析的层级与归属).
   - Shared definitions and check methods may be introduced once; each Qx subsection must retain its own results, interpretation, boundaries and evidence references. A combined validation chapter or a bare cross-reference cannot replace these local analyses. Record missing evidence or an evidence-based not-applicable reason in the corresponding subsection; writing does not execute new checks. A different hierarchy requires an explicit user or mandatory-template basis.
   - Map each model to its assumptions, variables, equations, results, figures, and tables.
   - For every final answer-producing model in every Qx, map at least one pseudocode or flowchart to its source procedure and a location in that Qx model/solution subsection. Faithful transcription of supplied algorithms/code into presentation-only LaTeX/TikZ is allowed; inventing steps, changing algorithms or running solvers is not. The template's K-Means is a presentation example only. Missing procedure evidence remains an explicit gap.
   - Map each major claim to a supporting artifact from the solution package's claims inventory.

5. Draft standard paper sections.
   - Write only the sections requested or appropriate for the current workflow stage.
   - Keep the writing concise, technical, and evidence-based.
   - Avoid filler prose.
   - For each section, verify that every claim is traceable to an artifact.

6. Maintain artifact traceability.
   - Every numerical claim must point to a result artifact.
   - Every figure or table reference must appear in the figure-table plan or existing files.
   - Every robustness claim must point to a robustness artifact.
   - Every model description must align with the final method explanation.
   - Use the solution package's claims inventory to verify each claim.

7. Write formulas and symbols carefully.
   - Use mathematical notation only when variables are defined in the final method explanation.
   - Keep notation consistent with the global symbol table.
   - Do not introduce new variables without defining them.

8. Handle missing evidence explicitly.
   - If a result, figure, table, or robustness check is missing, mark the section as incomplete.
   - Do not fill gaps with invented values or generic claims.
   - Recommend the upstream skill needed to complete the missing evidence.

9. Produce section drafts.
   - Save drafts under `paper/sections/`.
   - Use section-oriented LaTeX names: `q1.tex`, `abstract.tex`, `assumptions.tex`, etc. Markdown may hold evidence and handoff notes, while LaTeX remains the single manuscript body source.
   - Preserve a clear link between drafts and source artifacts.

10. Recommend final audit.
    - After section drafts are complete enough, hand off to `quality-assurance-auditor`.

# Outputs

Produce paper section drafts and a writing summary:

- `paper/sections/abstract.tex`
- `paper/sections/problem_restatement.tex`
- `paper/sections/problem_analysis.tex`
- `paper/sections/assumptions.tex`
- `paper/sections/symbols.tex`
- `paper/sections/data_preprocessing.tex`
- `paper/sections/q1.tex`
- `paper/sections/q2.tex`
- `paper/sections/q3.tex`
- `paper/sections/q4.tex`
- Error, sensitivity and other validation subsections inside each `paper/sections/qx.tex`; optional file fragments are input within that Qx section and retain its heading hierarchy.
- `paper/sections/strengths_limitations.tex` (the template's model strengths, limitations and generalization section)
- `paper/sections/conclusion.tex` only when an explicit user requirement or mandatory format calls for a separate conclusion chapter; otherwise conclude within Qx endings and model evaluation.
- Section-to-artifact mapping.
- Incomplete claims list.
- Recommended next skill.

# Output format

Prefer this JSON-compatible summary:

The example below is an internal handoff with user-reserved choices still pending. Supplied-result writing records its external evidence route and actual gaps; it does not manufacture the internal filenames or pending-human history shown here.

```json
{
  "paper_writing_summary": {
    "input_route": "internal_solve_handoff",
    "status": "awaiting_modeler",
    "target_subquestion": "Q1",
    "gate_check": {
      "rule1_method_explanation_exists": true,
      "rule2_result_analysis_exists": true,
      "rule3_solution_package_exists": true,
      "all_gates_passed": true
    },
    "primary_source_used": "results/Q1/reports/q1_solution_package_for_writer.md",
    "drafted_sections": [
      "paper/sections/q1.tex"
    ],
    "incomplete_sections": [],
    "unsupported_claims": [],
    "discussion_review": [
      {
        "claim": "supplied deterministic result",
        "applicable_prompts": ["domain_meaning", "conditions"],
        "evidence_refs": ["provided_result_table:row1"],
        "material_gaps": ["Q1 sensitivity evidence not supplied"],
        "status": "partial_draft_with_named_gap"
      }
    ],
    "paper_seeds": {
      "key_result_claim": { "present": false, "note": "[MODELER INPUT NEEDED] sentinel in abstract — human must pick the headline." },
      "contribution_claim": { "present": false, "note": "[MODELER INPUT NEEDED] sentinel in abstract — human must state the innovation." },
      "why_this_method": { "present": false, "provenance_marker": null, "note": "awaiting transcription from methods/Q1/qx_decision_log.md tagged decision_id: Q1-D0n." }
    },
    "surviving_sentinels": [
      "paper/sections/abstract.tex: key_result_claim, contribution_claim",
      "paper/sections/q1.tex: physical-meaning slot for RMSE; why_this_method"
    ],
    "artifact_mapping": [
      {
        "section": "q1.tex",
        "uses_artifacts": [
          "methods/Q1/q1_final_method_explanation.md",
          "methods/Q1/qx_decision_log.md",
          "results/Q1/reports/q1_final_result_analysis.md",
          "results/Q1/reports/q1_solution_package_for_writer.md",
          "results/Q1/experiments/final/figures/q1_ranking.png",
          "robustness/Q1/q1_robustness_report.md"
        ]
      }
    ],
    "recommended_next_skill": "modeler (replace [MODELER INPUT NEEDED] sentinels), then quality-assurance-auditor"
  }
}
```

If a JSON block is too rigid, use a concise Markdown report with the same fields.

# Paper section types

## Abstract
Summarize the problem, methods, supported key results and relevant boundaries. Organize only adopted evidence; do not invent values, superiority or innovation. Select the headline from supplied/recorded answers within the writing scope; any unresolved substantive decision follows G5.3.

## Problem restatement
Restate the problem in the team's own words. Include background, main goal, subquestions, required outputs, and constraints.

## Problem analysis
Explain how the problem is decomposed and why the workflow order is reasonable. Map each subquestion to its task type. Explain dependencies.

## Assumptions
State simplifying assumptions needed for modeling. Each assumption should be necessary, interpretable, and linked to a modeling need. Distinguish necessary from simplifying assumptions.

## Symbols and definitions
Define variables, parameters, sets, indices, functions, and outputs. Distinguish decision variables, state variables, parameters, inputs, and outputs. Include units where available. Keep notation consistent across sections.

## Data preprocessing
Explain data sources, field meanings, cleaning operations, and readiness. Mention missing values, outliers, units, transformations, and remaining risks.

## Model construction (per subquestion)
Present the final model: assumptions, symbols, objective function/ evaluation criterion, constraints, solution procedure. Align with the final method explanation. Include baseline before claiming improvement. Mention eliminated methods to demonstrate thoroughness.

## Model solution (per subquestion)
Explain how the model was solved or computed. Link to generated and reviewed scripts. Each final model must have pseudocode or a flowchart in this Qx section, with inputs, actual steps, outputs, appropriate conditions and a unique referenced label. A shared generic diagram or appendix-only artifact does not fulfill local coverage. Transcribe existing technical material without designing a new algorithm or executing code; for a theoretical model, an existing argument/derivation flow is acceptable. Explain the display in surrounding prose.

## Results analysis (per subquestion)
Explain adopted outputs using the supplied result tables, figures and interpretations. Keep conclusions proportional to evidence and distinguish descriptive from causal claims. Apply the authority contract to any new judgment; missing domain meaning stays a concrete gap rather than an invented explanation.

## Method selection narrative (per subquestion, optional)
Describe the actual candidate comparisons and adopted selection rationale from the decision log or supplied method explanation, with the appropriate source mapping. Preserve its technical meaning and actor. Missing selection rationale remains a named gap; do not invent exploration history or independently choose a new model.

## Error, sensitivity and other validation analysis (per subquestion)
Within each Qx `\section`, write separate error-analysis and sensitivity-analysis `\subsection` blocks, plus other applicable validation subsections. Use the existing robustness-checker outputs to explain the corresponding Qx metrics, stable or fragile conclusions, and boundaries. Shared methods may be referenced; keep the Qx-specific evidence and interpretation local. Missing evidence remains a named gap; a genuinely inapplicable analysis retains a short reason in its subsection. Do not invent or execute checks to fill headings.

## Strengths and limitations
Explain what the model does well and where it may fail. Be specific. Link limitations to assumptions, data, method, or robustness findings.

## Concluding statements and recommendations
Answer the original subquestions in their local endings and synthesize supported implications in the template's evaluation/generalization section. Create a separate conclusion chapter only with an explicit structural basis. Every conclusion should map to a subquestion and existing evidence; avoid unsupported recommendations.

## Appendix notes
Describe code, extra tables, parameter settings, or supplementary derivations. Link to scripts and outputs.

# Writing rules

- Write from validated artifacts, not memory or guesswork.
- Use the adopted internal solution package or the external supplied-material evidence matrix first, then compare with its identified sources.
- Internal solve-pipeline numbers come from the adopted `frozen_numbers.json`. Supplied-result writing uses the identified provided result source/version, with its actual verification status. Missing or conflicting values remain specific gaps; no new freeze or computation is required merely to write.
- Keep every major claim traceable to an artifact.
- Use concise, technical language.
- Do not write numerical claims without result artifacts.
- Do not cite figures or tables that do not exist.
- Do not invent references, experiments, or parameter values.
- Do not inflate conclusions beyond robustness evidence.
- Do not hide uncertainty.
- If evidence is missing, mark the section incomplete and name the missing artifact.
- If the solution package says a claim is "to avoid or downgrade", respect that.
- Avoid filler phrases that do not advance the argument.
- **Length is an editorial judgment.** Concise, evidence-complete writing may be drafted; identify actual missing content and avoid padding. Do not use an internal word-count floor as a completion gate.
- **Discussion follows evidence and purpose** (G5.2). Explain the answer and relevant boundaries; optional dimensions do not impose a numeric quota or authorize new computation.
- Preserve the real source and decision-maker for interpretations and headline/method claims. Use the shared authority contract for a new decision; writing alone does not authorize technical judgment or new computation. Keep unresolved reserved choices and missing evidence explicit.

# Rules

- Enforce the checks applicable to the selected input route before calling a section complete.
- A real evidence conflict blocks the dependent claim; continue independent supported writing and report the unresolved gap.
- Preserve the real source and decision-maker for interpretations and headline/method claims. Use the shared authority contract for a new decision; writing alone does not authorize technical judgment or new computation. Keep unresolved reserved choices and missing evidence explicit.
- Partial drafts may include any independently supported section or subsection. Mark the exact unresolved prerequisite and affected claim; do not call the dependent part complete.
- Do not run code, clean data, change models, or fabricate data/results/references/figures/tables.
- Do not perform final QA or approve final submission.
- Do not overwrite validated artifacts without permission.
- Do not introduce notation that conflicts with the global symbol table or final method explanation.
- Mark unsupported claims explicitly.
- Keep section drafts modular and reviewable.

# Verification

Before handing off, verify:

- The selected input route and its actual evidence requirements are recorded and satisfied for every claim marked complete.
- **Content coverage**: each section claimed complete answers its task with sources and appropriate boundaries; concise or inapplicable content is not rejected by a word-count floor.
- **Discussion review**: explanations and qualifications match the available evidence. Report missing applicable material in its local subsection; optional discussion dimensions have no minimum count.
- Required claims are supported and their actual source/actor is traceable. Unresolved applicable evidence or human-reserved choices remain named gaps; a valid agent-delegated decision does not require fabricated human wording.
- The adopted internal package or supplied-material evidence matrix was used as the primary source.
- Every drafted section uses only available artifacts.
- Every numerical claim maps to its adopted source: the pipeline freeze for internally solved work, or the provided result/version recorded for supplied-result writing.
- Every figure or table reference maps to the figure-table plan or existing file.
- Each adopted figure has an actual review record appropriate to its source and the requested scope. For internally generated figures, retain the generator's render log; for supplied figures, record file/version and the visual checks actually performed. Do not invent a generator log or rerun plotting code merely to write.
- Every robustness claim maps to a robustness artifact.
- Every subquestion has a corresponding draft section or is marked incomplete.
- Assumptions are connected to modeling needs.
- Variables and notation are defined before use.
- Limitations are not hidden.
- Unsupported claims are listed.
- The next skill is `paper-polisher`, then `consistency-auditor` / `completeness-auditor` / `quality-assurance-auditor` (audit layer).

# Failure modes

Report the affected writing gap; continue independent supported parts. The fixed-file failures below apply to internal solve-pipeline handoff only:

- **GATE FAILURE (Rule 1)**: `methods/Qx/qx_final_method_explanation.md` is missing. → Redirect to `workflow-orchestrator` or `final-method-explainer`.
- **GATE FAILURE (Rule 2)**: `results/Qx/reports/qx_final_result_analysis.md` is missing. → Redirect to `workflow-orchestrator` or `result-report-generator`.
- **GATE FAILURE (Rule 3)**: `results/Qx/reports/qx_solution_package_for_writer.md` is missing. → Redirect to `workflow-orchestrator` or `solution-package-builder`.
- Model results are missing for a section that requires them.
- A required figure/table or its source/placement cannot be established from the adopted plan or equivalent supplied materials.
- Robustness results are missing for a robustness claim.
- A requested section would require invented numerical values.
- A claim cannot be traced to any artifact.
- Final-delivery approval is requested while applicable QA remains unfinished; draft assembly for review can proceed within scope.
- The user asks to hide uncertainty or unsupported limitations.

# Stop conditions

Stop the dependent claim instead of guessing when:

- An applicable internal handoff artifact is missing; the external supplied-result route uses its evidence matrix and does not require those filenames.
- Drafting would require inventing data, results, figures, tables, references, parameters, or experiments.
- A section depends on missing technical material, whether from an internal artifact or external supplied source.
- The available artifacts contradict each other.
- A conclusion would exceed the evidence.
- A figure or table reference cannot be traced.
- Continuing would overwrite reviewed section drafts without permission.

When stopping, output:
- the blocker
- which gate failed (if applicable)
- why it matters
- affected section
- missing artifact or evidence needed
- safe partial draft if any
- recommended next action

# Handoff

After producing paper section drafts with all gates passed, hand off to:

`quality-assurance-auditor`

The handoff should include:
- drafted section paths
- gate check results
- artifact mapping
- figure and table references
- unsupported or incomplete claims
- missing artifacts
- known writing risks
- sections requiring human review

If missing model results block writing, hand back to the appropriate code generator or `code-reviewer`.

If missing robustness evidence blocks writing, hand back to `robustness-checker`.

If missing visual planning blocks writing, hand back to `figure-table-planner`.

If gates failed, hand back to `workflow-orchestrator` with the specific gate failure report.

# Examples

## Example 1: All gates pass — draft Q1 section, but seeds await the modeler (B-layer)

Input state:
- `methods/Q1/q1_final_method_explanation.md` exists.
- `results/Q1/reports/q1_final_result_analysis.md` exists.
- `results/Q1/reports/q1_solution_package_for_writer.md` exists.
- Figure-table plan exists.
- User asks: "write the Q1 paper section."

The AI drafts the mechanics (model construction, solution, baseline/sensitivity discussion) but leaves the graded judgments as sentinels: the physical-meaning slot per number, and the abstract's `key_result_claim` / `contribution_claim`, and the `why_this_method` paragraph (which must be transcribed from the decision log). Status is `awaiting_modeler`, not "drafted", until those sentinels are replaced by the human.

Output:
```json
{
  "paper_writing_summary": {
    "status": "awaiting_modeler",
    "target_subquestion": "Q1",
    "gate_check": {
      "rule1_method_explanation_exists": true,
      "rule2_result_analysis_exists": true,
      "rule3_solution_package_exists": true,
      "all_gates_passed": true
    },
    "drafted_sections": [
      "paper/sections/q1.tex (mechanics drafted; physical-meaning + why_this_method sentinels pending)"
    ],
    "paper_seeds": {
      "key_result_claim": { "present": false },
      "contribution_claim": { "present": false },
      "why_this_method": { "present": false, "provenance_marker": null }
    },
    "surviving_sentinels": [
      "paper/sections/abstract.tex: key_result_claim, contribution_claim",
      "paper/sections/q1.tex: physical-meaning slot per number; why_this_method"
    ],
    "primary_source_used": "results/Q1/reports/q1_solution_package_for_writer.md",
    "recommended_next_skill": "modeler (replace sentinels; transcribe why_this_method from methods/Q1/qx_decision_log.md), then quality-assurance-auditor"
  }
}
```

## Example 2: Gate failure — Rule 1 violation

Input state:
- User asks: "write the Q2 paper section."
- `methods/Q2/q2_final_method_explanation.md` does NOT exist (modeler hasn't confirmed final method).
- `results/Q2/reports/q2_final_result_analysis.md` exists.
- `results/Q2/reports/q2_solution_package_for_writer.md` does NOT exist (blocked by Rule 1).

Output:
```json
{
  "blocked_items": [
    "GATE FAILURE (Rule 1): Cannot write Q2 paper section. The final method explanation is missing at methods/Q2/q2_final_method_explanation.md."
  ],
  "gate_check": {
    "rule1_method_explanation_exists": false,
    "rule2_result_analysis_exists": true,
    "rule3_solution_package_exists": false,
    "all_gates_passed": false
  },
  "what_can_be_written": [
    "Problem restatement section (does not depend on final method).",
    "Data preprocessing section (if data report exists)."
  ],
  "recommended_next_skill": "workflow-orchestrator",
  "recommended_next_action": "The modeler must confirm the final method for Q2 and run final-method-explainer. Then solution-package-builder must produce the solution package. Only then can the paper writer proceed."
}
```

## Example 3: Gate failure — Rule 2 violation

Input state:
- Q3 has final method explanation.
- Q3 has raw experiment outputs but no final result analysis.
- User says: "Q3 is done, write it up."

Output:
```json
{
  "blocked_items": [
    "GATE FAILURE (Rule 2): Cannot write Q3 paper section. The final result analysis is missing at results/Q3/reports/q3_final_result_analysis.md. Raw experiment outputs are not sufficient — the programmer must analyze and interpret the results first."
  ],
  "gate_check": {
    "rule1_method_explanation_exists": true,
    "rule2_result_analysis_exists": false,
    "rule3_solution_package_exists": false,
    "all_gates_passed": false
  },
  "recommended_next_skill": "result-report-generator",
  "recommended_next_action": "Run result-report-generator in final mode to produce the final result analysis for Q3. Then run solution-package-builder."
}
```

## Example 4: Gate failure — Rule 3 violation

Input state:
- Q4 has final method explanation and final result analysis.
- But no solution package has been built.
- User says: "write Q4 paper section."

Output:
```json
{
  "blocked_items": [
    "GATE FAILURE (Rule 3): Cannot write Q4 paper section. The solution package is missing at results/Q4/reports/q4_solution_package_for_writer.md. The paper writer should use the solution package as primary source, not scatter through method and result files."
  ],
  "gate_check": {
    "rule1_method_explanation_exists": true,
    "rule2_result_analysis_exists": true,
    "rule3_solution_package_exists": false,
    "all_gates_passed": false
  },
  "recommended_next_skill": "solution-package-builder",
  "recommended_next_action": "Run solution-package-builder for Q4 to produce the writer-facing package. Then the paper writer can proceed."
}
```

## Example 5: Write only non-gated sections

Input state:
- Q2 gates fail (Rule 1).
- But the user needs to write problem restatement and data preprocessing sections (which don't depend on Q2's final method).

Output:
```json
{
  "paper_writing_summary": {
    "status": "partial_draft_only",
    "target_subquestion": "Q2",
    "gate_check": {
      "rule1_method_explanation_exists": false,
      "rule2_result_analysis_exists": true,
      "rule3_solution_package_exists": false,
      "all_gates_passed": false
    },
    "drafted_sections": [
      "paper/sections/problem_restatement.md (DRAFT — not Q2-dependent)",
      "paper/sections/data_preprocessing.md (DRAFT — not Q2-dependent)"
    ],
    "blocked_sections": [
      "paper/sections/q2.tex (BLOCKED — awaiting final method explanation and solution package)"
    ],
    "recommended_next_skill": "workflow-orchestrator"
  }
}
```
