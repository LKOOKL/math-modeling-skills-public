---
name: quality-assurance-auditor
description: Audit the complete mathematical modeling solution before final submission and identify blocking issues.
license: MIT
---

## Decision authority

Read the [shared decision-authority contract](../workflow-orchestrator/references/decision-authority.md) when this skill produces or consumes a judgment. Resolve explicit delegation, human-reserved decisions and existing-results writing scope before applying the rules below. Human-only instructions and unresolved-human examples below describe the reserved branch; delegated decisions use `decided_by: agent_under_user_delegation` with an authorization reference and actual evidence. Never label an agent decision as human-authored.

# Purpose

Audit the complete mathematical modeling contest solution before final submission.

This skill is the **third of three independent auditors** that together form Gate G6. It runs after `consistency-auditor` and `completeness-auditor` and consumes their reports as inputs — it does NOT re-do their checks. Each auditor catches a different failure mode:

- `consistency-auditor` → cross-media numbers / files / symbols / parameters (does the paper claim match the code?)
- `completeness-auditor` → audit/review files exist on disk with ≥ 5 pass items (did the producer skills actually write what they claimed?)
- **`quality-assurance-auditor` (this skill)** → workflow completeness, three critical rules, anti-fabrication, paper quality (is the whole pipeline coherent and defensible?)

This skill checks whether the solution answers every subquestion, whether models / code / results / figures / robustness checks / paper sections are mutually coherent, whether the full workflow completeness requirements are met, and whether unsupported claims or missing artifacts block final delivery.

Resolve the input route first. For an internal solve, verify the performed delivery chain: candidate methods (with PoC) → experiments → final method explanation → final result analysis → solution package (with frozen_numbers.json) → paper sections. For supplied-results writing, verify the supplied-source/evidence matrix, manuscript scope, preserved evidence status and actual writing/visual/audit checks. Unperformed internal stages are not applicable, not missing completed work; missing technical support still limits the corresponding claims.

This skill does not invent missing results, rewrite the full paper, rerun models, or approve submission when evidence is incomplete. **It approves final delivery only after the two sibling audits and final closure pass for the same scope and content** — the three are orthogonal and all must converge.

# When to use

Use this skill:

- After `paper-section-writer` has drafted paper sections for all subquestions.
- Before final delivery or submission.
- When checking whether the solution is logically complete.
- When identifying blocking issues, minor issues, and repair actions.
- When deciding whether to return to an upstream skill.

# Preconditions

First record `input_route` and intended delivery scope. The following list describes internal-solve inputs; equivalent supplied technical material and its evidence matrix serve the writing route. Do not reconstruct absent solver artifacts solely for writing QA:

- Parsed problem and subquestions.
- Problem classification.
- Candidate method pools per subquestion.
- Data report and cleaned data summary, if data is used.
- Reviewed model code.
- Model result artifacts per subquestion.
- Robustness or sensitivity reports per subquestion.
- Figure-table plans per subquestion.
- Paper section drafts for all subquestions.

If paper sections are missing, hand back to `paper-section-writer`.

If model results needed for a claim are missing, flag that claim and its required source. Route new computation to a solver only when separately authorized; supplied-results writing continues supported portions with the gap explicit.

# Inputs

Use or request:

- `workspace/problem/problem-parser/problem_parse.json`
- `workspace/problem/problem-classifier/problem_classification.json`
- `methods/Qx/qx_method_candidates.md` (all subquestions)
- `methods/Qx/qx_method_iteration_log.md` (all subquestions)
- `methods/Qx/qx_final_method_explanation.md` (all subquestions)
- `results/Qx/reports/qx_final_result_analysis.md` (all subquestions)
- `results/Qx/reports/qx_solution_package_for_writer.md` (all subquestions)
- Result files under `results/Qx/experiments/`
- Robustness reports under `robustness/Qx/`
- Figure-table plans under `methods/Qx/`
- Figures under `results/Qx/experiments/*/figures/` and `paper/figures/`
- Paper drafts under `paper/sections/`
- Generated code under `code/`
- `planning/progress_dashboard.md` (workflow status)
- Contest requirements or submission rules if available

# Workflow

0. **Resolve the input route and verify sibling auditors (independent audit layer prerequisite).**
   - Record `internal_solve` or `supplied_results_writing`, intended delivery and applicable source map. A scoped writing review cannot certify numerical checks that were not performed or a complete solution while material gaps remain.
   - Check that `paper/audits/cross_media_consistency_audit.md` exists with verdict PASSED.
   - Check that `paper/audits/completeness_audit.md` has a PASSED pre_qa or final scope covering the currently adopted content. In the first cycle, QA may be SCHEDULED in that pre_qa report.
   - If either is missing, route to it first — do not pretend QA can substitute for them.
   - If either has FAILED verdict, treat that as a BLOCKING issue and inherit its repair routing.
   - Proceed when consistency and the applicable pre_qa completeness scope pass. A missing upstream artifact still blocks. QA does not require its own completed report before it runs.

   QA is the third independent auditor, not a super-auditor that subsumes the others.

1. Check problem coverage.
   - Verify every original subquestion is represented in the paper.
   - Verify each subquestion has a corresponding model, result, and written answer.
   - Mark unanswered or partially answered subquestions as blocking issues.

2. **Check workflow completeness (NEW — expanded check).**
   - For each internally solved subquestion, verify the full delivery chain:
     1. Candidate method pool exists (`methods/Qx/qx_method_candidates.md`).
     2. Experiment reports exist (at least one round at `results/Qx/experiments/roundN/`).
     3. Method iteration log exists (`methods/Qx/qx_method_iteration_log.md`).
     4. Final method explanation exists (`methods/Qx/qx_final_method_explanation.md`).
     5. Final result analysis exists (`results/Qx/reports/qx_final_result_analysis.md`).
     6. Solution package exists (`results/Qx/reports/qx_solution_package_for_writer.md`).
     7. Robustness report exists (`robustness/Qx/qx_robustness_report.md`) or a justified exception.
     8. Figure-table plan exists (`methods/Qx/qx_figure_table_plan.md`).
   - In the internal-solve route, mark a missing required link as blocking. In the supplied-results writing route, check coverage against the evidence matrix and record unperformed internal stages as not applicable; do not require PoCs or a reconstructed history.

3. Check source fidelity (the three critical rules for internal handoff).
   - Rule 1: Verify paper model description matches the final method explanation (not an early candidate pool).
   - Rule 2: Verify paper results come from the final result analysis (not raw experiment outputs directly).
   - Rule 3: Verify the solution package exists and the paper writer used it.
   - For supplied-results writing, apply the equivalent source checks: the model, numerical claims and judgments match the adopted supplied material and evidence matrix; preserve unsupported or unverified items as gaps. The three internal filenames are not prerequisites for this route.

4. Check artifact lineage.
   - Trace each major paper claim back to problem parse, method explanation, data, code, result, figure, or robustness artifact.
   - Mark claims without artifacts as unsupported.

5. Check model consistency.
   - Verify models match the classified problem types.
   - Verify baseline models exist for main models unless explicitly justified.
   - Verify the paper describes the final method (from `qx_final_method_explanation.md`), not an earlier candidate.
   - Verify eliminated methods are mentioned appropriately.

6. Check data and result consistency.
   - Verify raw data was not overwritten.
   - Verify cleaned data and field mappings are documented.
   - Verify result tables come from reviewed scripts or accepted computation.
   - Verify units, variables, and dimensions are consistent.

7. Check paper quality.
   - Judge task coverage, sources and boundaries. Word/character counts and discussion dimensions are editorial prompts, not internal minimum quotas; short deterministic or non-applicable sections can be sufficient. Missing applicable evidence remains a local gap and blocks only unsupported completion claims.
   - Check [format-specific trace markers](../write-math-modeling-papers/references/tracking-format.md): TeX provenance uses independent `%` lines or an external mapping, while Markdown can use comments. Verify identifiers stay out of PDF body text and the following intended prose remains present; compilation success alone does not establish this.
   - Compare the expanded top-level chapter sequence against [the user-template contract](../write-math-modeling-papers/references/user-template-contract.md), including data preprocessing, per-Qx model/solution blocks, strengths/limitations/generalization, and appendices. Verify minor-edit records and the basis for any structural exception; template examples and metadata are not factual evidence.
   - Audit a `Qx → final model → pseudocode/flowchart → local manuscript location → source` coverage table. Each model needs at least one actual display inside its Qx section, unique label, prose reference/explanation, inputs, outputs and sufficient real steps. Check loops/branches/termination only when applicable; a theory model may use an existing reasoning flow. A generic all-paper flowchart, K-Means placeholder, appendix-only display or mere filename fails coverage. Check transcription fidelity without executing or inventing technical steps.
   - Expand the actual `main.tex` input/include order and verify each Qx `\section` contains separate results-analysis, error-analysis and sensitivity-analysis `\subsection` blocks, plus other applicable check subsections. Record explicit user or mandatory-template exceptions. File names alone do not establish heading ownership.
   - For each block, verify Qx-specific results, interpretation and boundaries, or a concrete missing-evidence/not-applicable record. Shared definitions and methods may be referenced; a global validation section, appendix pointer or bare cross-reference does not replace local analysis. Missing or misassigned subsections are structural failures; material evidence gaps prevent a completion claim. Repair prose/structure through the writer and route new computation to the authorized solver/checker. See [the per-question structure contract](../write-math-modeling-papers/references/chapter-workflow.md#逐问结果分析的层级与归属).
   - Verify every referenced figure or table exists on disk.
   - Verify figures in the paper match the figure-table plan's Type 3 (论文图) classification.
   - Verify no Type 1 (诊断图) figures accidentally appear in the paper.
   - Verify every figure or table has a source artifact.
   - Verify captions support the intended claim.
   - Verify assumptions are necessary and linked to modeling needs.
   - Verify notation is defined before use and consistent with the global symbol table.
   - Verify conclusions map back to subquestions.
   - Verify limitations are not hidden.
   - Reject decorative or unsupported visuals.

8. Check for fabrication and exaggeration.
   - Verify no references are fabricated.
   - Verify no numerical values are invented.
   - Verify no experiments are claimed that were not run.
   - Verify robustness claims do not exceed completed checks.
   - Verify conclusions do not exceed evidence.
   - Flag any claim that cannot be traced to an artifact.

9. **Produce a QA report — MANDATORY substantive file on disk.**
   - Save to `paper/qa_report.md`.
   - **List ≥ 5 explicit pass items** with file:line evidence (concrete checks, not "all good"). These are checked by `completeness-auditor`.
   - Separate blocking issues from minor issues.
   - Provide a repair plan.
   - Route each repair to the appropriate upstream skill.
   - Record QA's own check verdict. On a first successful run, use `audit_closure: PENDING_FINAL_COMPLETENESS` until completeness verifies this report in final scope. Final delivery requires all three substantive reports for the same adopted content; draft assembly and compilation may precede audit.
   - If sibling auditors are missing or failed (step 0), QA cannot approve final delivery — note this and route appropriately.

# Outputs

Produce a QA report at:

- `paper/qa_report.md`

Containing:

- `qa_status` (passed / failed)
- `final_assembly_allowed` (true / false)
- `blocking_issues`
- `minor_issues`
- `workflow_completeness_check` (per subquestion)
- `three_critical_rules_check`
- `unsupported_claims`
- `fabrication_risks`
- `artifact_traceability`
- `subquestion_coverage`
- `repair_plan`
- `recommended_next_skill`

# Output format

```markdown
# QA Report

## Overall Status

- **QA Status**: passed / failed
- **qa_checks**: PASSED / FAILED
- **audit_closure**: PENDING_FINAL_COMPLETENESS / CLOSED / BLOCKED
- **Final Delivery Allowed** (`final_assembly_allowed` compatibility field): true only when all three auditors pass for the adopted content and completeness is final-scope
- **Date**: [timestamp]

## Sibling Auditor Status (Gate G6 prerequisite)

| Auditor | Report Path | Verdict |
|---------|-------------|---------|
| consistency-auditor | paper/audits/cross_media_consistency_audit.md | PASSED / FAILED / MISSING |
| completeness-auditor | paper/audits/completeness_audit.md | PRE_QA_PASSED / FINAL_PASSED / FAILED / MISSING |
| quality-assurance-auditor (this report) | paper/qa_report.md | PASSED / FAILED |

**Cross-auditor verdict**: ALL_PASSED (final delivery allowed) / PENDING_FINAL_COMPLETENESS (QA checks passed; final closure due) / ONE_OR_MORE_FAILED (delivery blocked)

## Pass Items (≥ 5 REQUIRED for this audit to count as substantive)

1. ✅ Every subquestion (Q1, Q2, Q3, Q4) has paper/sections/qx.tex on disk and non-empty.
2. ✅ Each adopted Qx snapshot matches its recorded input, parameter, implementation and result hashes for the roles applicable to that run; upstream snapshots match. Record the question and fingerprint as evidence.
3. ✅ Every main model has a baseline comparison in its results section.
4. ✅ No fabricated references detected (cross-checked against reference-manager's reference_audit.md).
5. ✅ Every figure in `paper/figures/` is Type 3 (论文图) or Type 4 (附录图); no Type 1 (诊断图) leaked in.
6. ✅ ...

## Workflow Completeness Check

| Check | Q1 | Q2 | Q3 | Q4 |
|-------|----|----|----|-----|
| 1. Candidate method pool | ✅ | ✅ | ✅ | ❌ |
| 2. Experiment report(s) | ✅ (R2) | ✅ (R1) | ❌ | ❌ |
| 3. Method iteration log | ✅ | ❌ | ❌ | ❌ |
| 4. Final method explanation | ✅ | ❌ | ❌ | ❌ |
| 5. Final result analysis | ✅ | ❌ | ❌ | ❌ |
| 6. Solution package | ✅ | ❌ | ❌ | ❌ |
| 7. Robustness report | ✅ | ❌ | ❌ | ❌ |
| 8. Figure-table plan | ✅ | ❌ | ❌ | ❌ |

## Three Critical Rules Check

| Rule | Q1 | Q2 | Q3 | Q4 | Status |
|------|----|----|----|-----|--------|
| Rule 1: Paper method matches final method explanation | ✅ | ❌ (no final explanation) | N/A | N/A | Q2 FAIL |
| Rule 2: Paper results from final result analysis | ✅ | N/A | N/A | N/A | PASS |
| Rule 3: Solution package exists and was used | ✅ | ❌ (no package) | N/A | N/A | Q2 FAIL |

## Subquestion Coverage

| Subquestion | Answered in Paper | Model Exists | Results Exist | Robustness Exists | Results/Error/Sensitivity Subsection Ownership | Status |
|-------------|-------------------|-------------|---------------|-------------------|-----------------------------------------------|--------|
| Q1 | ✅ | ✅ (entropy-TOPSIS) | ✅ | ✅ | Each is a subsection within Q1; evidence checked | Complete |
| Q2 | ⏳ (partial draft) | ❌ (no final) | ❌ | ❌ | Missing local evidence/subsections | Blocked |
| Q3 | ❌ | ❌ | ❌ | ❌ | Not drafted | Blocked |
| Q4 | ❌ | ❌ | ❌ | ❌ | Not drafted | Blocked |

## Blocking Issues

| # | Issue | Affects | Why It Matters | Repair Skill |
|---|-------|---------|---------------|--------------|
| 1 | Q2 has no final method explanation | Q2 completion | Paper cannot describe the final model | `final-method-explainer` |
| 2 | Q3 not started | Q3 completion | Subquestion unanswered | `workflow-orchestrator` |
| 3 | Q4 not started | Q4 completion | Subquestion unanswered | `workflow-orchestrator` |

## Minor Issues

| # | Issue | Affects | Repair Skill |
|---|-------|---------|--------------|
| 1 | Q1 Figure 1.3 caption does not state the main takeaway | Q1 paper section | `paper-section-writer` |
| 2 | Q1 robustness report missing boundary condition statement | Q1 robustness section | `robustness-checker` |

## Unsupported Claims

| # | Claim | Location | Why Unsupported | Action |
|---|-------|----------|----------------|--------|
| 1 | "The model is globally stable." | paper/sections/q1.tex | Robustness only checked ±10% weight perturbation | Downgrade to "stable under moderate perturbation" |

## Fabrication Risks

| # | Risk | Location | Evidence |
|---|------|----------|----------|
| — | (none detected) | — | — |

## Artifact Traceability (spot check)

| Paper Claim | Source Artifact | Traceable? |
|-------------|----------------|------------|
| "City A ranks highest with score 0.88." | `results/Q1/experiments/final/tables/m2_scores.csv` | ✅ |

## Repair Plan

1. **BLOCKING**: Run `final-method-explainer` for Q2 to produce `methods/Q2/q2_final_method_explanation.md`.
2. **BLOCKING**: Run `workflow-orchestrator` to plan Q3 and Q4 execution.
3. **MINOR**: Update Q1 Figure 1.3 caption via `paper-section-writer`.
4. **MINOR**: Add boundary condition statement to Q1 robustness report via `robustness-checker`.

## Recommended Next Skill

- **If QA failed**: `workflow-orchestrator` (with repair plan)
- **If QA passed**: `workflow-orchestrator` (for final delivery)
```

# Expanded QA checklist

## Workflow completeness (internal-solve subquestions)
For supplied-results writing, use evidence-matrix coverage and actual executed-review records; mark unperformed internal stages not applicable with a reason.
- [ ] Candidate method pool exists
- [ ] Experiment report(s) exist
- [ ] Method iteration log exists
- [ ] Final method explanation exists
- [ ] Final result analysis exists
- [ ] Solution package exists
- [ ] Robustness report exists (or justified exception)
- [ ] Figure-table plan exists

## Three critical rules (internal solve; equivalent source fidelity for supplied results)
- [ ] Paper model description matches final method explanation (not earlier candidate pool)
- [ ] Paper results come from final result analysis (not raw experiment outputs)
- [ ] Solution package exists and was used as primary source

## Problem coverage
- [ ] Every subquestion is answered in the paper
- [ ] Every answer has model-result-paper alignment

## Model consistency
- [ ] Every main model has a baseline or justified exception
- [ ] Paper describes the final method, not an early draft
- [ ] Eliminated methods are mentioned where appropriate

## Evidence quality
- [ ] Every numerical claim has a result artifact
- [ ] Every figure or table has a source artifact
- [ ] Every figure in the paper exists on disk
- [ ] No Type 1 (诊断图) figures in the paper
- [ ] Every robustness claim has robustness evidence

## Paper quality
- [ ] Every conclusion maps to a subquestion
- [ ] Assumptions are necessary and stated clearly
- [ ] Notation is defined and consistent (cross-check with global symbol table)
- [ ] Code outputs match paper claims
- [ ] Raw data is preserved
- [ ] Limitations are stated

## Anti-fabrication
- [ ] No fabricated data, references, results, figures, or experiments
- [ ] No invented numerical values
- [ ] No unsupported superiority claims
- [ ] No hidden uncertainty

# Rules

- Do not fabricate missing evidence.
- Do not approve final delivery with blocking issues.
- **Do not approve final delivery unless ALL THREE auditors (consistency / completeness / this skill) PASS.** A single auditor's "✅" is not sufficient — the three are orthogonal.
- Do not re-do the work of `consistency-auditor` (cross-media number/file/symbol checks) or `completeness-auditor` (audit-file existence checks). Consume their reports as inputs.
- Do not approve "完成" verbally. Write the substantive `paper/qa_report.md` with ≥ 5 explicit pass items. `completeness-auditor` will flag a verbal-only QA as MISSING.
- Do not hide uncertainty.
- Do not treat planned artifacts as completed artifacts.
- Do not rewrite the full paper inside QA.
- Do not rerun models unless explicitly asked by the user.
- Do not change upstream artifacts silently.
- Route repairs to the correct upstream skill.
- Keep QA findings specific and actionable.
- Check workflow completeness — it's not just about paper quality.

# Verification

Before approving final delivery, verify:

- `blocking_issues` is empty.
- `workflow_completeness_check` passes for the declared scope and route (the eight internal-solve checks, or supplied-source/evidence coverage with justified not-applicable stages).
- `three_critical_rules_check` passes for internal-solve subquestions, or equivalent supplied-source fidelity passes in the writing route.
- `unsupported_claims` is empty or explicitly removed from final text.
- Every subquestion is covered.
- Baseline and robustness requirements are satisfied.
- All figures and tables are traceable.
- Final conclusions do not exceed evidence.
- No fabrication risks detected.
- **QA entry**: consistency PASSED and completeness pre_qa/final PASSED for the adopted content. **Final closure**: final-scope completeness additionally verifies this QA report; closure-only metadata updates do not invalidate checks on unchanged manuscript/results.
- **`paper/qa_report.md` exists with ≥ 5 explicit pass items** — this file is the output of THIS skill; verify it was actually written.
- `final_assembly_allowed` is a final-delivery compatibility field: it is true only when the cross-auditor verdict is `ALL_PASSED`, completeness is final-scope and the adopted content is unchanged. It does not block drafting or compilation.

# Failure modes

Stop and report a blocker if:

- Paper sections are missing.
- Model results are missing.
- Robustness evidence is missing before final delivery.
- Figures or tables are referenced but not available.
- Claims cannot be traced to artifacts.
- Subquestions are unanswered.
- Any critical rule is violated.
- Workflow completeness chain is broken.
- Final delivery is requested before QA passes. Draft assembly/compilation remains allowed for review.

# Stop conditions

This skill must stop instead of guessing when:

- An issue requires missing data or missing result artifacts.
- The paper and code describe incompatible models.
- Final conclusions depend on unsupported claims.
- Fixing the issue requires upstream modeling, code, or data work.
- Continuing would require inventing evidence.

When stopping, output:
- blocker
- why it matters
- affected section or subquestion
- required artifact
- recommended repair skill
- next action

# Handoff

If QA passes:
→ `workflow-orchestrator` with `final_assembly_allowed: true`.

If QA fails:
→ `workflow-orchestrator` with repair plan routing to the relevant upstream skill.

Repair routing:
- `problem-parser` → missing or misread subquestions
- `problem-classifier` → wrong task type mapping
- `method-selector` → missing candidate pool
- `data-auditor-cleaner` → data issues
- `model-code-analyzer` or code generators → missing code
- `code-reviewer` → code or artifact issues
- `result-report-generator` → missing experiment report or final result analysis
- `final-method-explainer` → missing final method explanation
- `solution-package-builder` → missing solution package
- `robustness-checker` → missing stability evidence
- `figure-table-planner` → unsupported visuals or missing figure plan
- `paper-section-writer` → writing or traceability issues

# Examples

## Example 1: QA fails — workflow incomplete (Q2 missing final method)

```json
{
  "qa_status": "failed",
  "final_assembly_allowed": false,
  "blocking_issues": [
    {
      "issue": "Q2 has no final method explanation (methods/Q2/q2_final_method_explanation.md missing).",
      "why_it_matters": "The paper cannot write the Q2 model construction section. Rule 1 violated.",
      "repair_skill": "final-method-explainer"
    }
  ],
  "workflow_completeness_check": {
    "Q1": {"passed": true, "missing": []},
    "Q2": {"passed": false, "missing": ["final_method_explanation", "final_result_analysis", "solution_package", "robustness_report"]},
    "Q3": {"passed": false, "missing": ["all"]},
    "Q4": {"passed": false, "missing": ["all"]}
  },
  "recommended_next_skill": "workflow-orchestrator"
}
```

## Example 2: QA fails — unsupported claim detected

```json
{
  "qa_status": "failed",
  "final_assembly_allowed": false,
  "unsupported_claims": [
    {
      "claim": "The prediction model is highly accurate.",
      "location": "paper/sections/q2.tex",
      "reason": "No error metric or baseline comparison is provided.",
      "repair_skill": "robustness-checker"
    }
  ],
  "recommended_next_skill": "robustness-checker"
}
```

## Example 3: QA passes

```json
{
  "qa_status": "passed",
  "final_assembly_allowed": true,
  "blocking_issues": [],
  "minor_issues": [
    {
      "issue": "Figure caption for Q1 Fig.1.3 could be more specific.",
      "repair_skill": "paper-section-writer"
    }
  ],
  "workflow_completeness_check": {
    "Q1": {"passed": true, "missing": []},
    "Q2": {"passed": true, "missing": []},
    "Q3": {"passed": true, "missing": []},
    "Q4": {"passed": true, "missing": []}
  },
  "three_critical_rules_check": {
    "Q1": {"all_passed": true},
    "Q2": {"all_passed": true},
    "Q3": {"all_passed": true},
    "Q4": {"all_passed": true}
  },
  "recommended_next_skill": "workflow-orchestrator"
}
```
