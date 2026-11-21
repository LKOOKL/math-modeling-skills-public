---
name: decision-prompt-builder
description: Ask focused questions for human-reserved or materially unclear modeling decisions, preserving existing delegation and recording actual responses.
license: MIT
---

## Decision authority

Read the [shared decision-authority contract](../workflow-orchestrator/references/decision-authority.md) when this skill produces or consumes a judgment. Resolve explicit delegation, human-reserved decisions and existing-results writing scope before applying the rules below. Human-only instructions and unresolved-human examples below describe the reserved branch; delegated decisions use `decided_by: agent_under_user_delegation` with an authorization reference and actual evidence. Never label an agent decision as human-authored.

# Purpose

Ask only for a consequential modeling decision that remains human-reserved or materially unclear after reading the current request and existing authorization. Frame the relevant trade-off and record the actual answer. This question-builder does not itself decide; when the user explicitly delegates the choice, route to the responsible decision producer with that authorization instead of refusing the delegation or asking the same question again.

# When to use

Use this skill for the unresolved human-reserved branch of these judgment gates; delegated branches proceed to the responsible producer under the shared contract:

- **G1 framing** — before `problem-classifier` shows `ai_suggested_type`: what output does the team want to defend?
- **G2 / G2.5 method choice + baseline** — before `method-selector` shows its `ai_suggestion`.
- **post-experiment (G4.5)** — before `result-report-generator` / `robustness-checker` show their suggested verdicts: which result is the headline, how confident, is it robust enough?
- **G5 claim scope / figure role** — before `paper-section-writer` / `figure-table-planner` finalize: what is the contribution, what claim does this figure defend?

A modeling judgment alone does not require a new question. Check whether it is already answered or delegated before invoking this question step.

Do NOT use this skill:

- During mechanical stages (code generation, review, freeze, render-check, the auditors) — there is no modeling judgment to ask about, and a question there is friction theatre.
- To ask a question whose answer is mechanically determinable (e.g. "should the seed be fixed?" — that is AI-owned; never ask it).

# Inputs

- The current gate / judgment point and the candidate options the downstream skill will present (so the questions are grounded in the actual trade-off).
- `planning/session_config.json` — the `mode` (`learning` | `speed`), which controls verbosity and anchor-timing only.
- The problem parse / classification for context.

# Workflow

1. Resolve existing answers and authority. If this choice is delegated within scope, hand off that authorization without a question. Otherwise identify the single reserved or unclear judgment (method / framing / result / confidence / claim scope).

2. Derive the 2-3 questions that, if answered, narrow the decision space the most. Rank them by how load-bearing they are. Each question MUST:
   - Be framed as a **trade-off**, not a leading question: "Q3 can be cast as optimization or as evaluation — optimization gives you a defensible 'optimal' claim but needs a clean objective; evaluation is safer but weaker. Which does your team want to defend?"
   - Name the consequence of each side, not the recommended side.
   - Be answerable only by a human with modeling judgment (not by computing something).

3. Emit at most 3 questions. If everything looks like a question, you have failed to prioritize — pick the 3 that matter. (Anti-fatigue: if the human is asked everything, they tune out, and the gate degrades into rubber-stamping.)

4. Hand the human's answers to the downstream skill / decision artifact. Do not author the answers. Do not mark any artifact DECIDED.

# Mode behavior (learning vs speed — scaffolding only, never gate strictness)

The `mode` in `planning/session_config.json` changes presentation, not authority or evidence requirements. Apply question-first learning exercises when requested; an explicit delegation remains effective in either mode.

| | learning mode | speed mode |
|---|---|---|
| Question count & framing | full 2-3 questions, each option's trade-off explained | one terse question, trade-off compressed to a clause |
| AI suggestion timing | **withheld** until after the human has written their answer (anti-anchoring) | shown alongside, since the expert wants a draft to react to |
| Term definitions | inline (defines TOPSIS, RMSE, etc.) | assumed known |
| Post-answer reflection | "would this convince a judge? what's the weakest part?" | omitted |

**Anchor suppression is the key learning-mode mechanic.** In learning mode, the downstream skill's `ai_suggestion` must be withheld until the human commits their own answer, then revealed for comparison ("you chose ARIMA for trend-fit; the AI also flagged seasonality you didn't mention"). This directly attacks the anchoring bias that makes a human "decision" just an echo of the AI's pick. In speed mode anchoring is an accepted trade-off for an expert who can critically evaluate a draft.

The mode is recorded as presentation context (`captured_in_mode`), separately from decision authority and actual authorship. It does not establish whether a human reviewed a decision.

# Outputs

A `decision_prompt` block injected at the top of the judgment skill's output (not a saved file unless the skill persists it):

```markdown
## Decision prompt — your call, not the AI's  (mode: learning)

Before you see the AI's suggestion, answer these (most load-bearing first):

1. **[output form]** Q3's answer can be a *plan* (optimization — you can claim "optimal", but you need a clean
   objective and constraints) or a *score/ranking* (evaluation — safer, but you can't claim optimality). Which
   does your team want to defend, and why?
2. **[baseline]** The simplest honest reference here is greedy allocation. Do you accept that as the baseline, or
   is there a more meaningful one for this problem?

(The AI's suggestion is withheld until you've written your answer above — so it doesn't anchor you.)
```

# Rules

- Ask, never answer. Refuse to state or pre-select the answer to your own questions, even when the human is unsure.
- Never pre-fill a `modeler_decision` / `modeler_rationale` field. Never mark an artifact DECIDED.
- At most 3 questions per gate. Fewer is better.
- Only ask genuine modeling-judgment questions — never one whose answer is mechanically determinable.
- Frame trade-offs (name both consequences); never frame a leading question that telegraphs the "right" answer.
- The mode changes presentation only. It never replaces the shared authority/evidence checks or independently grants delegation.
- Do not run during mechanical stages.

# Verification

Before handing off, verify:

- ≤ 3 questions, each a genuine human-judgment question framed as a trade-off.
- No question has a pre-selected or AI-supplied answer.
- In learning mode, the downstream `ai_suggestion` is withheld until after the human answers.
- No decision artifact field was authored or marked DECIDED by this skill.

# Failure modes

Stop and report if:

- The user delegates an earlier question: record the delegation and route it to the responsible producer. If the authority remains unclear or the choice is explicitly reserved, ask only the unresolved point.
- There is no genuine modeling judgment at this point (it's a mechanical stage) — do not invent a question.

# Handoff

- To the judgment-bearing skill (`method-selector`, `result-report-generator`, etc.): the human's answers, to flow into the decision artifact.
- To `modeler-decision-logger`: the `captured_in_mode` value for the decision record.

# Relationship to the posture shift

For unresolved human-reserved decisions, this skill helps the user express a real choice and its basis. Learning-mode anchor suppression is a teaching option. An explicit acceptance may validly match a prior suggestion; check its actual source instead of rejecting text similarity. When the user explicitly delegates the decision, route it to the responsible producer and preserve agent authorship.
