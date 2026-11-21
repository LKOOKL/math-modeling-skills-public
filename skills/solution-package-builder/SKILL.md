---
name: solution-package-builder
description: Integrate the modeler's final method explanation and the programmer's final result analysis into a single comprehensive writer-facing solution package that the paper writer can directly use to draft paper sections.
license: MIT
---

## Decision authority

Read the [shared decision-authority contract](../workflow-orchestrator/references/decision-authority.md) when this skill produces or consumes a judgment. Resolve explicit delegation, human-reserved decisions and existing-results writing scope before applying the rules below. Human-only instructions and unresolved-human examples below describe the reserved branch; delegated decisions use `decided_by: agent_under_user_delegation` with an authorization reference and actual evidence. Never label an agent decision as human-authored.

# Purpose

**Writing handoff:** Keep decision and evidence identifiers traceable using [tracking-format.md](../write-math-modeling-papers/references/tracking-format.md). Markdown comments or mapping fields in this package must be converted to standalone TeX comments when transferred into `.tex`; internal identifiers must not print in the paper. Word counts and a fixed number of discussion dimensions are editorial guidance, not grounds to invent missing analyses or reject a concise evidence-complete section.

Build the writer-facing solution package that integrates all modeling and results work into one coherent, self-contained document. This is the single source of truth that the paper writer uses to draft paper sections for a subquestion.

This skill merges:
- The modeler's final method explanation (what we did and why).
- The programmer's final result analysis (what we got and what it means).
- Planned and generated figures and tables (what visual evidence exists).
- Robustness and sensitivity findings (how stable our conclusions are).

Into one structured package that the paper writer can read and directly translate into paper content without needing to dig through scattered artifacts or guess at missing information.

This skill does not write the actual paper sections, select models, run experiments, generate figures, or perform QA.

Package confidence and claim scope follow the shared authority contract. This producer may decide delegated keep/downgrade/drop judgments using the actual evidence; a reserved sign-off waits for the user. Preserve the existing method-selection decision and its provenance. A valid package sign-off is required before freezing, with the true actor recorded.

# When to use

Use this skill:

- After `final-method-explainer` has produced `methods/Qx/qx_final_method_explanation.md`.
- After `result-report-generator` has produced `results/Qx/reports/qx_final_result_analysis.md`.
- When both modeling and results work are locked in and the paper writer is waiting.
- When the user says: "prepare the solution package for Q1", "package everything for the writer", "build the writer's material package", "I need to write the paper section for Q2".
- Before `paper-section-writer`.
- When the workflow status for a subquestion is "Ready for Writer".

# Preconditions (CRITICAL — enforced as gates)

The following three files MUST exist before this skill can produce a complete package:

1. `methods/Qx/qx_final_method_explanation.md` — the modeler's definitive method document.
2. `results/Qx/reports/qx_final_result_analysis.md` — the programmer's definitive result document.
3. The actual figure and table files referenced in the result analysis (must exist on disk, not just be planned).

Additionally, the freeze (`frozen_numbers.json`, Gate G4) is gated on valid authorized sign-off — it MUST NOT be emitted until BOTH:

4. The G4.5 result/stability verdicts are `DECIDED` in the decision log (`methods/Qx/qx_decision_log.md` carries `DECIDED` records for the `result_verdict` / `confidence` decision points from `result-report-generator`, and the stability verdict from `robustness-checker`).
5. This skill's own package sign-off decision artifact `methods/Qx/decisions/solution-package-builder_modeler_decision.md` exists with `status: DECIDED` (`decision_id: qx_package_signoff`).

If either is missing, build the readable evidence package and identify the unresolved record. Complete a supported delegated sign-off at step 7.4 when authorized; a reserved choice or missing technical evidence stays PENDING. Do not emit `frozen_numbers.json` until both applicable gates pass.

Additionally useful (but not strictly required):
- `results/Qx/experiments/final/` — final round outputs.
- `robustness/Qx/qx_robustness_report.md` — robustness and sensitivity analysis.
- Figure-table plan for this subquestion.

If `qx_final_method_explanation.md` is missing, stop and report: "This subquestion is not Ready for Writer — missing final method explanation. Hand back to the modeler or `final-method-explainer`."

If `qx_final_result_analysis.md` is missing, stop and report: "This subquestion is not Ready for Writer — missing final result analysis. Hand back to the programmer or `result-report-generator`."

If both exist but referenced figures/tables are missing, produce the package with warnings about missing visuals.

# Inputs

Use or request:

- `methods/Qx/qx_final_method_explanation.md` — REQUIRED.
- `results/Qx/reports/qx_final_result_analysis.md` — REQUIRED.
- `results/Qx/experiments/final/` — final experiment outputs directory.
- `robustness/Qx/qx_robustness_report.md` — robustness findings, if available.
- `methods/Qx/qx_method_candidates.md` — original candidate pool, for method selection narrative.
- `methods/Qx/qx_method_iteration_log.md` — iteration history, for demonstrating thoroughness.
- `methods/Qx/qx_decision_log.md` — REQUIRED for the freeze. The canonical, append-only log of the authorized decision-maker's `DECIDED` verdicts (method choice, result verdict, confidence, stability). The method-selection narrative is TRANSCRIBED from here with `decision_id` provenance, never re-authored. The G4.5 verdicts here gate the freeze.
- Figure-table plan relevant to this subquestion.
- Any existing paper draft sections for this subquestion (to check what's already been written).
- The problem parse for this subquestion's goals and constraints.

# Workflow

1. Verify prerequisites (gate check).
   - Confirm all three required files exist.
   - Verify referenced figures and tables exist on disk.
   - Read each input file thoroughly.
   - If any prerequisite is missing, stop and report exactly what is missing.

2. Extract and organize content.
   - From the final method explanation: extract the method name, selection justification, assumptions, symbols, mathematical model, solution procedure, and evaluation metrics.
   - From the final result analysis: extract key numerical results, figure interpretations, table interpretations, supported claims, and result limitations.
   - From the robustness report (if available): extract stable conclusions, fragile conclusions, perturbation results, and boundary conditions.
   - From the candidate pool (if available): extract the raw facts of method exploration (what was tried, what was dropped). **Do NOT re-author the selection verdict** — the *reason* the final method was chosen is TRANSCRIBED from the authorized decision-maker's `DECIDED` record in `methods/Qx/qx_decision_log.md` (carry the `decision_id` as provenance). The candidate pool supplies the inventory; the decision log supplies the verdict.

3. Build the solution overview.
   - Write a concise summary of the subquestion goal and how it was solved.
   - State the final method in one sentence (transcribed from the decision log's method-choice verdict, with `decision_id`).
   - State the key result in one sentence.
   - State the confidence level **as an `ai_suggestion`**, clearly labeled — do NOT render it as the verdict. The authorized decision-maker adopts or revises the confidence at the sign-off gate (step 7.4). Once `DECIDED`, transcribe the authorized decision-maker's confidence into the package.
   - This overview should be the first thing the paper writer reads.

4. Organize paper-ready content by section.
   - Map content into [the user's template framework](../write-math-modeling-papers/references/user-template-contract.md): front matter and data preprocessing, then each Qx model/solution section with its local results/error/sensitivity subsections, followed by evaluation/generalization and supporting materials. Do not turn these content categories into independent cross-question chapters.
   - For each section, extract the relevant content from the source documents.
   - Mark content as "ready to write as-is", "needs adaptation", or "for reference only".
   - For every final model in each Qx, supply a source-backed procedure description sufficient for at least one pseudocode or flowchart, and record its intended local label/location. Reuse existing steps and preserve their conditions; name missing inputs, outputs or steps explicitly. This is a writing handoff, not permission to invent an algorithm or run it.

5. Assign figures and tables to paper sections.
   - Every figure and table must be assigned to a specific paper section.
   - State what claim each visual supports.
   - Provide a draft caption for each.
   - Mark placement suggestions (top of section, after formula X, etc.).

6. Identify gaps and FLAG candidate overclaims (as suggestions, not verdicts).
   - If a paper section has no supporting content, state what the writer should do (skip, mark as future work, write a brief note).
   - If robustness evidence is missing for a top-line claim, **FLAG it as a candidate overclaim and SUGGEST a downgrade** in the `ai_suggestion` field of the sign-off artifact — do NOT silently downgrade, keep, or drop it yourself. The authorized decision-maker records `keep/downgrade/drop` per flagged claim at the sign-off gate (step 7.4), within the evidence and current scope.
   - If a figure exists but is not paper-quality, note what needs improvement.
   - Compile the full set of flagged candidate overclaims here — this list feeds directly into the sign-off artifact's per-claim `ai_suggestion` rows.

7. Write the solution package.
   - Save as `results/Qx/reports/qx_solution_package_for_writer.md`.
   - Make it comprehensive but scannable — the writer should be able to find what they need quickly.
   - Include direct quotes from source documents where useful.
   - Include file paths for every referenced artifact.

7.4. **Record the package sign-off before freezing (Gate G4).**
   - Use the [shared decision-authority contract](../workflow-orchestrator/references/decision-authority.md) for `methods/Qx/decisions/solution-package-builder_modeler_decision.md`, with `decision_id: qx_package_signoff` and `decision_point: claim_scope`.
   - Record package confidence and keep/downgrade/drop for each flagged top-line claim. Cite the final result analysis, robustness evidence and existing decision log; missing evidence stays explicit.
   - For an explicitly delegated decision, make the supported judgment, record the authorization source and scope, set `status: DECIDED`, `decided_by: agent_under_user_delegation`, and `human_review: false`. Preserve any user-reserved point as pending.
   - For a human-reserved decision, prepare the evidence and leave `status: PENDING`, `decided_by: null` until the actual response arrives. Ask only for the unresolved choice; never write agent reasoning as the user's words.
   - `learning`/`speed` affect presentation only. A valid DECIDED artifact goes to `modeler-decision-logger`; then continue within scope. A pending choice or unsupported conclusion blocks its dependent action, while independent authorized work continues.
   - Freezing still requires both this valid sign-off and the valid G4.5 result/stability decisions; authorization alone cannot supply missing results or checks.

7.5. **Freeze numerical claims — emit `frozen_numbers.json` (Gate G4 pass criterion).**
   This is mandatory, not optional, but **gated**: do NOT run this step until step 7.4's sign-off artifact is `DECIDED` AND the G4.5 result/stability verdicts are `DECIDED` in `methods/Qx/qx_decision_log.md`. Until then the freeze is blocked — emit the PENDING sign-off artifact and STOP. Once unblocked, freeze exactly as below. Without freezing, every bug fix in `code/Qx/` silently shifts paper numbers; with freezing, drift is detectable by `consistency-auditor`. The content-provenance schema below also detects changes to actual data and parameters; immutability and the 解冻/修改/重冻结 sequence remain required.

   - Walk the solution package and extract every numerical claim (every value the paper will report).
   - For each, record provenance: which file (final analysis report / metric file / code constant) it came from, which line, and its frozen value.
   - Save to `results/Qx/reports/frozen_numbers.json` with this schema:
     ```json
     {
       "subquestion": "Q1",
       "frozen_at": "2026-05-18T14:22:11+08:00",
       "frozen_by_skill": "solution-package-builder",
       "source_method": "entropy-TOPSIS",
       "provenance": {
         "schema_version": 2,
         "question_id": "Q1",
         "captured_at": "2026-05-18T14:20:00+08:00",
         "applicability": {"scope": "executed", "not_applicable": {}},
         "dependencies": [
           {"role": "code", "path": "code/Q1/q1_main.py", "sha256": "<actual_sha256>"},
           {"role": "data", "path": "workspace/data/data_clean/indicators.csv", "sha256": "<actual_sha256>"},
           {"role": "parameters", "path": "results/Q1/experiments/final/effective_parameters.json", "sha256": "<actual_sha256>"},
           {"role": "environment", "path": "results/Q1/experiments/final/environment.json", "sha256": "<actual_sha256>"},
           {"role": "result_record", "path": "results/Q1/experiments/final/run_summary.json", "sha256": "<actual_sha256>"},
           {"role": "result_record", "path": "results/Q1/experiments/final/metrics/topsis_scores.csv", "sha256": "<actual_sha256>"}
         ],
         "parameters": {"K": 30, "seed": 2026},
         "no_data_reason": "",
         "fingerprint_sha256": "<computed_by_capture_helper>"
       },
       "claims": [
         {
           "id": "q1_top_score",
           "label": "Top city score (city A, entropy-TOPSIS)",
           "value": 0.92,
           "unit": "score",
           "precision_for_paper": 2,
           "source_file": "results/Q1/experiments/final/metrics/topsis_scores.csv",
           "source_locator": "row=A, column=score",
           "verified_against": "results/Q1/reports/q1_final_result_analysis.md:section 2"
         },
         {
           "id": "q1_K",
           "label": "Number of indicators",
           "value": 30,
           "unit": "count",
           "source_file": "code/Q1/q1_main.py",
           "source_locator": "line 18: K = 30"
         }
       ]
     }
     ```
   - The file is **immutable by convention** — once written, do not edit it by hand. To change a frozen number, follow the **解冻 → 修改 → 重冻结** three-step:
     1. Log the reason for thaw in `results/Qx/reports/freeze_change_log.md` (create if missing, append entries).
     2. Update the canonical source (code or analysis report) and re-run experiments if needed.
     3. Re-invoke this skill to regenerate `frozen_numbers.json` with a new `frozen_at` timestamp.
   - **Content provenance invariant**: follow the [shared artifact contract](../workflow-orchestrator/references/artifact-contract.md#qx-freshness-is-a-content-comparison). Embed provenance captured with the actual run; enumerate the code/shared helpers, selected raw/clean data, effective parameters, environment, result records and upstream Qx snapshots actually used. One existing file may supply multiple roles; parameter-free or no-execution analytical work records justified applicability rather than manufacturing files. Replace all illustrative hash placeholders with real SHA-256 values. A matching content check is required; `frozen_at`/mtime only record history. Changed/missing actual input or parameters alone invalidate this Qx and its downstream artifacts, while an mtime-only change leaves unchanged content current.
   - **Legacy migration**: preserve old numerical payloads and timestamps. Records with only mtime or code hashes are `UNVERIFIED_LEGACY`, not automatically ready for writing. Use the helper's non-overwriting migration record, then attach matching historical full provenance or regenerate affected results within existing authority. Hashing current files beside old numbers does not prove a historical run.

   `paper-section-writer` reads numbers from this file, not from raw results. `consistency-auditor` compares paper text against this file. The freeze is the single canonical anchor.

8. Update the workflow status.
   - The subquestion becomes "Ready for Writer" ONLY after step 7.5's freeze has actually fired — i.e., the `qx_package_signoff` artifact is `DECIDED` and the G4.5 verdicts are `DECIDED`. If the freeze is still blocked, record the exact unresolved authorization, evidence or sign-off condition instead of claiming Ready for Writer.
   - Hand off to `paper-section-writer` only once `frozen_numbers.json` exists. Otherwise route the unresolved gate to its authorized producer; ask the user only for a reserved or unclear choice.

# Outputs

Produce:

- `results/Qx/reports/qx_solution_package_for_writer.md` — the human-readable writer-facing package (always produced).
- `methods/Qx/decisions/solution-package-builder_modeler_decision.md` — actual DECIDED/PENDING sign-off status, with package confidence, claim-scope choices, evidence and true actor/authority.
- `results/Qx/reports/frozen_numbers.json` — the immutable numerical snapshot (Gate G4 pass criterion). **Emitted ONLY after** the sign-off artifact is `DECIDED` and the G4.5 result/stability verdicts are `DECIDED`. Until then, this skill STOPS at the freeze and does not produce it.

The solution package is the document the paper writer reads; `frozen_numbers.json` is the canonical source from which the writer sources every numerical claim. The freeze without a valid sign-off is forbidden; the package without the (gated) freeze is not yet Ready for Writer.

# Output format

The solution package MUST contain all of the following sections:

```markdown
# Qx Solution Package for Paper Writer

> **Status**: Ready for Writer
> **Package built**: [date]
> **Sources**: [list of input files used]

---

## 0. Quick Reference

- **Subquestion**: [one-line description]
- **Final method**: [method name — transcribed from decision log, decision_id: qx_method_choice]
- **Key result**: [one-line main finding]
- **Confidence**: [PENDING sign-off → ai_suggestion: high/medium/needs caution | after DECIDED → validly recorded level from qx_package_signoff]
- **Estimated paper pages**: [rough estimate]

---

## 1. Subquestion Goal and Context

[2-3 sentences from problem parse: what this subquestion asks, what output is required, what constraints apply]

## 2. Method Overview

### 2.1 Final Method: [name]
[2-3 sentence summary from final method explanation]

### 2.2 Method Selection Narrative
[Brief story of exploration: what was tried, what was dropped. Source: candidate pool + iteration log. The *reason the final method was chosen* is TRANSCRIBED verbatim from the authorized decision-maker's DECIDED verdict in `methods/Qx/qx_decision_log.md` — cite the `decision_id` (e.g., qx_method_choice). Do NOT re-author the selection verdict here.]

### 2.3 Relationship to Other Subquestions
[Inputs from / outputs to other subquestions]

---

## 3. Content for Paper Sections

### 3A. For "Model Construction" Section

**What to write** (source: final method explanation sections 2-4):
- [Extracted assumptions with justification — ready to write]
- [Symbol table excerpt — ready to write]
- [Mathematical model formulation — ready to write]
- [Solution procedure — ready to write]
- [Evaluation metrics — ready to write]

**Key formulas to include**:
1. [formula reference] — [why important]
2. [formula reference] — [why important]

**Writer notes**:
- [Any adaptation needed, tone suggestions, things to emphasize or avoid]

### 3B. For "Results Analysis" Section

**What to write** (source: final result analysis sections 2-4):
- [Key numerical results — ready to write]
- [Result interpretation — ready to write]
- [Baseline comparison — ready to write]

**Writer notes**:
- [Confidence qualifiers, unsupported claims to avoid]

### 3C. For separate error, sensitivity and other validation subsections within Qx

Map the evidence to the corresponding Qx `\section` and separate analysis `\subsection` blocks. Include Qx-specific results, interpretation, boundaries and source locations; identify shared-method references, missing evidence or justified not-applicable items. Keep results analysis in Qx as well; a global robustness chapter does not replace these local subsections.

**What to write** (source: robustness report):
- [Stable conclusions — ready to write]
- [Fragile conclusions — ready to write]
- [Perturbation findings — ready to write]

**If robustness report is missing**:
- [What the writer should say instead, e.g., mark as planned or note limitation]

### 3D. For "Conclusion" (per-subquestion portion)

**What to write**:
- [Direct answer to subquestion — ready to write]
- [Key numbers to cite — ready to write]
- [Limitations to acknowledge — ready to write]

---

## 4. Figure and Table Assignments

### Figures

| Figure File | Paper Section | Claim Supported | Draft Caption | Status |
|------------|---------------|-----------------|---------------|--------|
| [path] | [section] | [what claim] | [draft caption text] | exists / needs revision |

### Tables

| Table File | Paper Section | Claim Supported | Draft Caption | Status |
|-----------|---------------|-----------------|---------------|--------|
| [path] | [section] | [what claim] | [draft caption text] | exists / needs revision |

---

## 5. Supported Claims Inventory

### Claims Ready for Paper (with evidence)
| # | Claim | Evidence | Confidence |
|---|-------|----------|------------|
| 1 | [claim] | [figure/table/metric] | high / medium |

### Flagged Candidate Overclaims (authorized decision-maker records keep/downgrade/drop at qx_package_signoff)
| # | Claim | Why AI Flagged It | ai_suggestion (keep/downgrade/drop + safer claim) | Human Verdict (from sign-off artifact) |
|---|-------|-------------------|--------------------------------------------------|----------------------------------------|
| 1 | [overclaim] | [missing evidence] | [SUGGESTED action — not a verdict] | [keep/downgrade/drop — PENDING until DECIDED] |

### Claims from Eliminated Methods (for demonstrating thoroughness)
| # | Method | Finding | Can Mention in Paper? |
|---|--------|---------|----------------------|
| 1 | [eliminated method] | [what we learned] | yes / no / only briefly |

---

## 6. Paper Writing Sequence Suggestion

1. Start with [section] — it has the most complete content.
2. Then write [section] — refer to figures [X, Y].
3. ...
4. Save [section] for last — it depends on [other subquestion/QA].

---

## 7. Cross-References

- Final method explanation: `methods/Qx/qx_final_method_explanation.md`
- Final result analysis: `results/Qx/reports/qx_final_result_analysis.md`
- Robustness report: `robustness/Qx/qx_robustness_report.md` (or: NOT YET AVAILABLE)
- Candidate methods: `methods/Qx/qx_method_candidates.md`
- Iteration log: `methods/Qx/qx_method_iteration_log.md`
- Experiment outputs: `results/Qx/experiments/final/`
- Global symbol table: `planning/symbol_table.md` (if exists)

---

## 8. Package Completeness Checklist

- [x] Method explained
- [x] Results analyzed
- [x] Figures and tables assigned
- [x] Claims inventoried
- [x] Robustness addressed (or flagged as missing)
- [x] Paper section mapping complete
- [ ] Writer has all needed information — [YES / NO, with explanation]
```

# Rules

- CRITICAL: Do not produce this package if `qx_final_method_explanation.md` or `qx_final_result_analysis.md` is missing. Stop and report the gap.
- Do not write the actual paper sections. This is a package for the writer, not the paper itself.
- Every figure and table must be verified to exist on disk before being listed as "exists".
- Claims must be traceable to specific evidence (figure, table, metric, robustness check).
- Do not fabricate claims, evidence, figure interpretations, or numerical results.
- Do not hide missing evidence — if robustness is missing, flag it.
- If a source document contains contradictory information, flag the contradiction rather than choosing one side silently.
- Keep the recommendation voice neutral — this package informs the writer, it does not command them.
- Mark content quality levels: "ready to write as-is", "needs adaptation", "for reference only".
- If the package reveals that the subquestion is NOT actually Ready for Writer (e.g., key results are missing, major claims are unsupported), report this honestly and recommend returning to the appropriate upstream skill.
- This decision producer may make an explicitly delegated judgment and record its own reasoning. For a human-reserved point, present the evidence and wait for the actual response. Use the shared authority contract; never manufacture human participation.
- Preserve genuine human wording when recording a human response. For a delegated judgment, write the agent rationale with its actual actor and authorization; do not leave an artificial human-input blocker after valid delegation.
- **The method-selection narrative is TRANSCRIBED, not re-authored.** The reason the final method was chosen comes verbatim (with `decision_id` provenance) from `methods/Qx/qx_decision_log.md`. Do not re-compose a fresh justification.
- **The freeze is gated on valid authorized sign-off.** Do NOT emit `frozen_numbers.json` until BOTH (a) the G4.5 result/stability verdicts are `DECIDED` in the decision log AND (b) the `qx_package_signoff` artifact is `DECIDED` with a supported rationale and valid actual actor/authority. Until then, emit the PENDING sign-off artifact and STOP at the freeze.
- **`frozen_numbers.json` is mandatory** (once unblocked) — without it, Gate G4 fails and the paper writer cannot proceed. The package alone is not enough; the freeze is the canonical anchor. But the freeze must never fire ahead of the valid authorized sign-off.
- **Never edit `frozen_numbers.json` by hand**. To change a frozen value, walk the `解冻 → 修改 → 重冻结` three-step (log the reason in `freeze_change_log.md`, update the source, re-invoke this skill).

# Verification

Before handing off, verify:

- Both required input files exist and have been read.
- Every referenced figure and table file exists on disk (or is explicitly marked as missing).
- All major content categories are covered: method, results, figures/tables, claims, robustness.
- Paper section mapping is complete.
- The quick reference (section 0) is accurate and self-contained.
- Cross-reference file paths are correct.
- No fabricated content exists.
- The package completeness checklist is honest.
- The confidence level and any claim downgrade/drop are presented as `ai_suggestion`, NOT as the skill's verdict, until the authorized decision-maker has signed off.
- The method-selection narrative is transcribed from the decision log with a `decision_id`, not freshly authored here.
- The sign-off artifact exists with the actual decision status: supported DECIDED when authorized, otherwise PENDING with the unresolved reserved choice/evidence gap. Apply the shared contract; do not require PENDING placeholders after a valid delegated sign-off.
- **The freeze precondition is satisfied before `frozen_numbers.json` is emitted**: the sign-off artifact's `status` is `DECIDED` (valid actor and authorization under the shared contract) AND the G4.5 result/stability verdicts are `DECIDED` in `methods/Qx/qx_decision_log.md`. If either is missing, the freeze must NOT have been emitted.
- **Once unblocked, `results/Qx/reports/frozen_numbers.json` exists** with actual-run provenance that passes the content-hash check and covers its code/data/parameters/environment/result/upstream dependencies. Historical timestamps alone do not establish freshness; old records lacking complete provenance remain `UNVERIFIED_LEGACY`.
- Every numerical claim in the package text appears in `frozen_numbers.json` with matching value (checked only after the freeze is unblocked and emitted).

# Failure modes

Stop and report a blocker if:

- `qx_final_method_explanation.md` is missing — the subquestion is not Ready for Writer.
- `qx_final_result_analysis.md` is missing — the subquestion is not Ready for Writer.
- Both files exist but directly contradict each other (e.g., method explanation says "entropy weights" but result analysis says "equal weights").
- All referenced figures and tables are missing — there is no visual evidence.
- The package reveals that major claims in the result analysis are unsupported by actual data.
- A required input file is corrupted or unreadable.

# Stop conditions

This skill must stop instead of guessing when:

- Required prerequisites are missing (see above).
- Source documents contradict each other on material facts and the contradiction cannot be resolved from available information.
- A figure or table is referenced but does not exist, and the gap is material to the paper.
- The content would require inventing bridging narrative between contradictory sources.
- The package would mislead the writer into making unsupported claims.
- **The freeze is requested but the valid authorized sign-off is not in place** — the `qx_package_signoff` artifact is not `DECIDED`, or the G4.5 result/stability verdicts are not `DECIDED` in the decision log. Build the package and emit the PENDING sign-off artifact, but STOP at the freeze; do NOT emit `frozen_numbers.json`, and do NOT hand off to the writer.

When stopping, output:

- the blocker
- which prerequisite or artifact is missing/problematic
- what the writer CAN still write (partial content)
- what must be resolved before the package can be completed
- recommended next skill (usually `workflow-orchestrator`, `final-method-explainer`, or `result-report-generator`)

# Handoff

After producing `results/Qx/reports/qx_solution_package_for_writer.md` AND the PENDING `qx_package_signoff` artifact, hand back to the **modeler** to render the sign-off (confidence + per-claim `keep/downgrade/drop`). The freeze and the writer handoff are blocked until that artifact is `DECIDED` and the G4.5 verdicts are `DECIDED`. `modeler-decision-logger` collects the sign-off into `methods/Qx/qx_decision_log.md`.

Only after the freeze has fired (`frozen_numbers.json` emitted), hand off to:

`paper-section-writer`
— with the solution package path, the frozen-numbers file, figure/table inventory, claims inventory, and section mapping.

If the package reveals missing prerequisites, hand back to:

`workflow-orchestrator`
— with specific gap report and recommendation for which upstream skill to invoke.

Do not hand off to `quality-assurance-auditor` directly — QA should run after paper sections are drafted.

# Relationship to the Three Critical Rules

This skill enforces the three critical rules from the workflow specification:

1. **No final paper without final method explanation**: This skill verifies that `qx_final_method_explanation.md` exists before building the package. Without it, the package cannot be built, and the writer cannot proceed.

2. **No writer handoff without final result analysis**: This skill verifies that `qx_final_result_analysis.md` exists before building the package. Raw results are not enough — the programmer must have analyzed them.

3. **Internal-solve writer handoff uses the solution package**: This skill produces the single document (`qx_solution_package_for_writer.md`) that the paper writer should use as their primary source. The writer should not need to hunt through scattered results, figures, and method notes.

# Examples (human-pending examples use the reserved branch)

## Example 1: Complete package for Q1

Input state:
- `methods/Q1/q1_final_method_explanation.md` exists (entropy-TOPSIS selected as final).
- `results/Q1/reports/q1_final_result_analysis.md` exists (final ranking, sensitivity).
- All figures exist on disk.
- Robustness report exists.

Output (summary):

```markdown
# Q1 Solution Package for Paper Writer

## 0. Quick Reference
- **Subquestion**: Evaluate and rank cities by resilience.
- **Final method**: Entropy-Weight TOPSIS.
- **Key result**: City A, B, C rank top 3 with stable ordering under ±10% weight perturbation.
- **Confidence**: High.

## 4. Figure and Table Assignments

| Figure File | Paper Section | Claim Supported | Draft Caption | Status |
|------------|---------------|-----------------|---------------|--------|
| `results/Q1/experiments/final/figures/q1_ranking_comparison.png` | Results Analysis | "Entropy-TOPSIS differentiates alternatives more clearly than equal-weight scoring." | "Figure X: Comparison of city rankings under equal-weight baseline and entropy-TOPSIS. The entropy-based method reveals clearer separation among middle-ranked cities." | exists |
```

## Example 2: Blocked — missing final method explanation

Input state:
- User says "build solution package for Q2".
- `results/Q2/reports/q2_final_result_analysis.md` exists.
- `methods/Q2/q2_final_method_explanation.md` does NOT exist.

Output:
```json
{
  "blocked_items": [
    "Q2 is NOT Ready for Writer. The final method explanation is missing at methods/Q2/q2_final_method_explanation.md."
  ],
  "what_exists": [
    "Final result analysis is available at results/Q2/reports/q2_final_result_analysis.md"
  ],
  "what_is_missing": [
    "methods/Q2/q2_final_method_explanation.md"
  ],
  "recommended_next_skill": "final-method-explainer",
  "recommended_next_action": "The modeler must confirm the final method for Q2, then run final-method-explainer to produce the method explanation document."
}
```

## Example 3: Package with robustness gap

Input state:
- All required files exist for Q3.
- Figures exist.
- No robustness report exists.

Output (excerpt from package):

```markdown
### 3C. For "Robustness and Sensitivity" Section

**What to write**:
⚠ NO ROBUSTNESS REPORT EXISTS for Q3.

**Writer guidance**: Do not fabricate robustness claims. Instead, in the paper section, state:
- "Constraint sensitivity analysis is planned but not yet completed."
- OR: "The optimization result is deterministic given fixed inputs; sensitivity to parameter uncertainty is addressed through scenario analysis in Section X."

**If the modeler or programmer can provide robustness results**, append them to this package before writing the final paper section.
```

## Example 4: Contradictory sources

Input state:
- Final method explanation says M2 was selected.
- Final result analysis describes outputs from M3.
- The method name mismatch exists.

Output:
```json
{
  "blocked_items": [
    "Source document contradiction: q1_final_method_explanation.md states the final method is 'M2: Entropy-TOPSIS', but q1_final_result_analysis.md describes results for 'M3: AHP-TOPSIS'. These must be reconciled before the package can be built."
  ],
  "recommended_next_skill": "workflow-orchestrator",
  "recommended_next_action": "The modeler and programmer must agree on which method is final and reconcile the two documents."
}
```
