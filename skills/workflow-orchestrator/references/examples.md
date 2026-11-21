# Routing and output examples

Use these illustrations after the current request is routed by [the coordinator](../SKILL.md) and the [authority contract](decision-authority.md). Fixed-file solve examples apply to this suite's newly produced artifacts. Examples with pending modeler input illustrate a human-reserved decision; they do not override an explicit delegation. Draft compilation is allowed before final audit; final delivery requires closed G6.

## Explicit delegation

Request: “自主完成建模、求解和论文写作。” Actual PoCs and required result evidence are available. The responsible producers record their supported choices with `decided_by: agent_under_user_delegation`, the scoped authorization reference and `human_review: false`. The logger retains that actor; valid decision gates pass without asking the same method/result questions again. Missing results still block unsupported claims.

## Human-reserved method choice

Request: “列出可行方案，让我选方法，再写代码。” Prepare the comparison and question, leave the method choice PENDING and the model-code action disabled. Do independent authorized preparation. `mode: speed` does not authorize the choice. Record the actual response when received.

## Supplied results and a missing sensitivity result

Request: “已有解答和结果表，只重写论文；第二问没有敏感性结果。” Route to `write-math-modeling-papers`. Map supplied sources, write supported content, and keep the specific missing evidence in Q2's sensitivity subsection. Do not run the solver or demand reconstructed PoCs/frozen files merely to begin writing.

## First final-review run

Consistency passed, upstream artifacts are present, and QA has never run: completeness can pass `audit_scope: pre_qa` with QA SCHEDULED and final delivery false. QA then writes its checks; final completeness verifies that report and unchanged adopted content. G6 closes only after all three substantive reports pass. If an upstream review is missing or QA was already claimed complete but absent, the corresponding completeness pass fails.

# Progress Dashboard

Maintain this dashboard at `planning/progress_dashboard.md`.

The dashboard MUST be a Markdown table tracking all subquestions:

```markdown
# Project Progress Dashboard

> Last updated: [timestamp]

## Overall Status

| Stage | Q1 | Q2 | Q3 | Q4 |
|-------|----|----|----|-----|
| Method Candidates Drafted | ✅ | ✅ | ✅ | ❌ |
| Experiment Report Ready | ✅ (R2) | ✅ (R1) | ❌ | ❌ |
| Final Method Selected | ✅ | ❌ | ❌ | ❌ |
| Final Method Explained | ✅ | ❌ | ❌ | ❌ |
| Final Result Analyzed | ✅ | ❌ | ❌ | ❌ |
| Solution Package Built | ⏳ | ❌ | ❌ | ❌ |
| Ready for Writer | ⏳ | ❌ | ❌ | ❌ |
| Writer Draft Ready | ❌ | ❌ | ❌ | ❌ |
| Reviewed by Modeler | ❌ | ❌ | ❌ | ❌ |
| Reviewed by Programmer | ❌ | ❌ | ❌ | ❌ |
| **Finalized** | ❌ | ❌ | ❌ | ❌ |

## Current Status Summary

| Subquestion | Status | Blocked By | Next Action |
|-------------|--------|------------|-------------|
| Q1 | Solution Package in Progress | — | Run solution-package-builder |
| Q2 | Needs Method Revision | M2 constraint violation in R1 | Modeler to fix constraints, then re-run |
| Q3 | Not Started | Waiting on Q1 results (input dependency) | — |
| Q4 | Not Started | Global planning incomplete | Run problem-parser and classifier first |

## Blockers

| Blocker | Affects | Severity | Resolution |
|---------|---------|----------|------------|
| Q2 M2 infeasible | Q2 finalization | High | Modeler revises constraint formulation |
| Q4 not parsed | Q4 start | High | Run problem-parser for all subquestions |

## Global Artifact Status

| Artifact | Status | Path |
|----------|--------|------|
| Problem Parse | ✅ | planning/parse/ |
| Problem Classification | ✅ | planning/classification/ |
| Global Symbol Table | ✅ | planning/symbol_table.md |
| Model Assumptions (Global) | ⏳ | planning/model_assumptions.md |
| Question Dependency Map | ✅ | planning/question_dependency.md |
| Related Paper Analysis | ✅ | workspace/papers/related_paper_analysis.md |
| Data Report | ✅ | workspace/data/data_report.md |

## Three Critical Rules Check

| Rule | Q1 | Q2 | Q3 | Q4 |
|------|----|----|----|-----|
| 1: Final method explanation exists before paper writing | ✅ | ❌ | ❌ | ❌ |
| 2: Final result analysis exists before writer handoff | ✅ | ❌ | ❌ | ❌ |
| 3: Solution package exists as writer's primary source | ⏳ | ❌ | ❌ | ❌ |

## Recommended Next Skill

- **Skill**: `solution-package-builder` for Q1
- **Reason**: Q1 has both final method explanation and final result analysis; solution package is the next prerequisite for writer handoff.
- **Runners-up** (if Q1 is already assigned):
  - `method-selector` for Q2 revision (after modeler fixes M2)
  - `problem-parser` for Q4
```

# Output format

Prefer this JSON-compatible structure:

```json
{
  "current_global_stage": "per_question_iteration",
  "progress_dashboard_path": "planning/progress_dashboard.md",
  "per_question_status": {
    "Q1": {
      "state": "08_solution_package_built",
      "state_label": "Solution Package Built",
      "ready_for_writer": false,
      "blocked": false,
      "blocked_reason": null,
      "missing_for_next_state": [
        "paper/sections/q1.tex"
      ]
    },
    "Q2": {
      "state": "04_needs_method_revision",
      "state_label": "Needs Method Revision",
      "ready_for_writer": false,
      "blocked": true,
      "blocked_reason": "Round 1 experiment shows M2 constraint violation. Modeler must revise constraint formulation.",
      "missing_for_next_state": [
        "Revised method from modeler"
      ]
    },
    "Q4": {
      "state": "00_not_started",
      "state_label": "Not Started",
      "ready_for_writer": false,
      "blocked": false,
      "blocked_reason": null,
      "missing_for_next_state": [
        "Problem parse (all subquestions)",
        "Problem classification (all subquestions)",
        "methods/Q4/q4_method_candidates.md"
      ]
    }
  },
  "global_completed_artifacts": {
    "problem_parse": true,
    "problem_classification": true,
    "related_paper_analysis": true,
    "global_symbol_table": true,
    "global_model_assumptions": false,
    "question_dependency_map": true,
    "data_report": true,
    "cleaned_data": true
  },
  "per_question_completed_artifacts": {
    "Q1": {
      "method_candidates": true,
      "method_iteration_log": true,
      "experiment_report_round1": true,
      "experiment_report_round2": true,
      "final_method_explanation": true,
      "final_result_analysis": true,
      "solution_package": true,
      "robustness_report": true,
      "paper_draft": false,
      "figure_table_plan": true
    }
  },
  "blocked_items": [
    {
      "scope": "Q2",
      "item": "final_method_explanation",
      "reason": "Modeler has not confirmed final method. Round 1 experiment showed M2 constraint violation.",
      "resolution": "Modeler revises constraint formulation, then re-run code for M2."
    }
  ],
  "three_critical_rules_check": {
    "Q1": {
      "rule1_method_explanation_exists": true,
      "rule2_result_analysis_exists": true,
      "rule3_solution_package_exists": true,
      "ready_for_writer": true
    },
    "Q2": {
      "rule1_method_explanation_exists": false,
      "rule2_result_analysis_exists": false,
      "rule3_solution_package_exists": false,
      "ready_for_writer": false
    }
  },
  "workflow_gates": {
    "global": {
      "method_selection_allowed": true,
      "code_generation_allowed_Q1": true,
      "code_generation_allowed_Q2": true,
      "paper_writing_allowed_Q1": true,
      "paper_writing_allowed_Q2": false,
      "final_assembly_allowed": false
    }
  },
  "next_skill": "paper-section-writer",
  "next_actions": [
    "Write paper/sections/q1.tex using results/Q1/reports/q1_solution_package_for_writer.md as primary source.",
    "Reference figures from results/Q1/experiments/final/figures/."
  ],
  "runners_up": [
    {
      "skill": "workflow-orchestrator",
      "action": "Return Q2 to modeler for constraint revision."
    }
  ],
  "handoff_context": {
    "reason": "Q1 is Ready for Writer (all three critical rules satisfied).",
    "required_inputs_for_next_skill": [
      "results/Q1/reports/q1_solution_package_for_writer.md",
      "results/Q1/experiments/final/figures/",
      "robustness/Q1/q1_robustness_report.md"
    ]
  }
}
```

If a JSON block is too rigid for the situation, use a concise Markdown report with the same fields.

# Examples

## Example 1: New contest problem

Input state:
- Problem PDF exists.
- No parsed problem exists.

Output:
```json
{
  "current_global_stage": "global_setup",
  "next_skill": "problem-parser",
  "next_actions": [
    "Extract goals, objects, constraints, data, outputs, and subquestions.",
    "Save parsed result under planning/parse/."
  ]
}
```

## Example 2: User asks to generate code too early

Input state:
- Problem has been parsed.
- Problem has not been classified.
- Method plan does not exist.
- User asks for modeling code.

Output:
```json
{
  "current_global_stage": "global_setup",
  "blocked_items": [
    "Code generation is blocked because no validated method plan exists."
  ],
  "next_skill": "problem-classifier",
  "next_actions": [
    "Classify each subquestion before literature analysis and method selection.",
    "Then hand off to related-paper-analyzer, then method-selector."
  ]
}
```

## Example 3: Q1 is Ready for Writer

Input state:
- Q1: `methods/Q1/q1_final_method_explanation.md` exists.
- Q1: `results/Q1/reports/q1_final_result_analysis.md` exists.
- Q1: `results/Q1/reports/q1_solution_package_for_writer.md` exists.
- User asks "what's next?"

Output:
```json
{
  "per_question_status": {
    "Q1": {
      "state": "09_ready_for_writer",
      "state_label": "Ready for Writer",
      "ready_for_writer": true
    }
  },
  "three_critical_rules_check": {
    "Q1": {
      "rule1_method_explanation_exists": true,
      "rule2_result_analysis_exists": true,
      "rule3_solution_package_exists": true,
      "ready_for_writer": true
    }
  },
  "next_skill": "paper-section-writer",
  "next_actions": [
    "Write paper/sections/q1.tex using results/Q1/reports/q1_solution_package_for_writer.md as primary source."
  ],
  "handoff_context": {
    "reason": "Q1 satisfies all three critical rules. Writer can proceed with the solution package.",
    "required_inputs_for_next_skill": [
      "results/Q1/reports/q1_solution_package_for_writer.md"
    ]
  }
}
```

## Example 4: Q2 needs method revision (Rule 1 violation)

Input state:
- Q2 has experiment report round 1.
- Experiment report says M2 produces infeasible output.
- User says "let's just write the Q2 paper anyway."

Output:
```json
{
  "blocked_items": [
    "CRITICAL RULE 1 VIOLATION: Q2 paper writing is blocked because methods/Q2/q2_final_method_explanation.md does not exist. The experiment report indicates M2 is infeasible — the modeler must revise the method before a final method can be explained."
  ],
  "per_question_status": {
    "Q2": {
      "state": "04_needs_method_revision",
      "state_label": "Needs Method Revision",
      "ready_for_writer": false,
      "blocked_reason": "M2 constraint violation in round 1. Modeler must fix constraint formulation or select a different candidate method."
    }
  },
  "next_skill": "method-selector",
  "next_actions": [
    "Modeler: revise Q2 constraint formulation for M2, or select a different candidate method from the pool.",
    "After revision: regenerate code and run round 2 experiments.",
    "Do NOT start paper writing until final method is confirmed and explained."
  ]
}
```

## Example 5: User asks "which question can be handed to the paper writer?"

Input state:
- Q1: Solution package exists. Not yet drafted.
- Q2: Final method explanation exists but no final result analysis.
- Q3: Only method candidates drafted.
- Q4: Not started.

Output:
```json
{
  "query_response": "Q1 is ready for the paper writer. Q2, Q3, Q4 are not ready.",
  "ready_for_writer": ["Q1"],
  "almost_ready": [],
  "not_ready": {
    "Q2": "Missing final result analysis (Rule 2). Programmer must run final experiments and produce results/Q2/reports/q2_final_result_analysis.md.",
    "Q3": "Only at candidate method stage. Need experiments, method selection, method explanation, result analysis, and solution package.",
    "Q4": "Not started — needs problem parsing and classification first."
  },
  "next_skill": "paper-section-writer",
  "next_actions": [
    "Write paper/sections/q1.tex for Q1 (only subquestion Ready for Writer).",
    "Meanwhile: Q2 programmer should produce final result analysis."
  ]
}
```

## Example 6: User asks to assemble final paper before QA

Input state:
- Paper sections exist for all subquestions.
- QA report does not exist.

Output:
```json
{
  "current_global_stage": "quality_assurance",
  "blocked_items": [
    "Final assembly is blocked because QA has not passed."
  ],
  "next_skill": "quality-assurance-auditor",
  "next_actions": [
    "Audit problem coverage, model-result consistency, figure references, robustness checks, unsupported claims, and workflow completeness."
  ]
}
```

## Example 7: Progress dashboard update

Input state:
- After completing Q1 solution package, the orchestrator is invoked.

Output:
- Updated `planning/progress_dashboard.md` with:
  - Q1 state changed to [08] Solution Package Built.
  - Next recommended skill: `paper-section-writer` for Q1.
  - Three critical rules check updated for Q1 (all three ✅).
  - Q2, Q3, Q4 statuses unchanged.
