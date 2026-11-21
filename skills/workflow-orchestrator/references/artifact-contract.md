# Data paths, content provenance, and portable Python entries

This is a file/evidence contract used by data preparation, code generation and package consumers. It does not change who may choose a model, execute a run or approve a result. The [inspection helper](../scripts/artifact_contract.py) uses the Python standard library; it never solves a model or passes a workflow gate.

## Resolve existing data in place

New projects default to `workspace/data/data_raw/`, `workspace/data/data_clean/` and `workspace/data/data_report.md`. Existing `workspace/data_raw/`, `workspace/data_clean/`, `workspace/data_clean/data_report.md` and `workspace/data_report.md` remain supported. Preserve existing inputs in their original locations; do not create an empty default folder and conclude that historical inputs are missing.

Before inventory, resolve the project root explicitly and inventory both layouts. Save `planning/data_paths.json` with the exact project-relative input paths, their SHA-256 values and the chosen report path. All consumers use that mapping; prose examples showing a default path are not a requirement to relocate existing data.

- One matching file: use its existing path.
- Same logical filename and identical content in both layouts: choose one deterministically and record both aliases. This is not two independent datasets.
- Same logical filename with different content: record `CONFLICT` and its two paths. Use an already-confirmed mapping if available; otherwise request only the missing source choice. Never let directory search order choose the dataset or overwrite either version.
- Data reports in different historical locations follow the same identity/conflict rule. A missing raw/clean group is explicitly listed; `RESOLVED` only means no path conflict, not that the dataset is ready for modeling.

Run with the helper path resolved from this installed skill, and absolute CLI paths for the project/output:

```text
python <skill>/scripts/artifact_contract.py data-layout --root <project> --output <project>/planning/data_paths.json
```

If a previously confirmed mapping resolves a conflict, pass `--mapping <project>/planning/data_choices.json`. The mapping is an object such as `{"clean:values.csv":"workspace/data_clean/values.csv","report":"workspace/data_report.md"}`. Logical names use case-folded relative filenames. All source files stay in place. The helper refuses to overwrite existing evidence; write a new version, review it and promote it according to the project's existing artifact policy.

## Qx freshness is a content comparison

A `frozen_at` timestamp and `mtime` are history, not freshness proof. Record a complete provenance object for each Qx containing:

- Every code file actually executed, including shared solver/helper code and the final submission entry.
- Every actual raw/clean input used, with upstream preprocessing dependencies when applicable.
- Effective parameters, seeds, splits, tolerances and stopping rules actually used, from an existing JSON record or its `parameters` field; include the inlined parameter object too.
- The actual environment/version record or dependency lock when calculations executed.
- The source run/result records supporting the frozen values and all upstream Qx snapshots on which this Qx depends.
- `schema_version: 2`, `question_id`, an `applicability` record, project-relative paths, per-file SHA-256 and a deterministic `fingerprint_sha256`.

Declare all dependencies from the actual run or derivation evidence, not just `code/Qx/`. For data-free theory, state a concrete `no_data_reason`. A complete manifest accompanies that evidence; hashing today's files cannot retroactively prove which inputs produced old results.

Roles describe existing evidence, not required filenames. The same `run_summary.json` may serve `parameters`, `environment` and `result_record`; repeat its path with those roles instead of inventing empty files. Parameter-free calculations can record `applicability.not_applicable.parameters` with the actual reason. Analytical work that executed no calculations uses `scope: analytical` and explicit reasons for absent code/runtime/parameters; its derivation or source result remains a required `result_record`. The helper permits these cases without dummy artifacts. For executed calculations, missing code or runtime evidence cannot be declared inapplicable. Declared real dependencies must exist regardless of scope, and reviewers still check that an inapplicability statement fits the actual work.

```text
python <skill>/scripts/artifact_contract.py capture --root <project> --question Q1 --dependency code=code/Q1/q1_main.py --dependency data=workspace/data/data_clean/values.csv --dependency parameters=results/Q1/experiments/final/effective_parameters.json --dependency environment=results/Q1/experiments/final/environment.json --dependency result_record=results/Q1/experiments/final/run_summary.json --output <project>/results/Q1/experiments/final/provenance.json
python <skill>/scripts/artifact_contract.py check --root <project> --question Q1 --snapshot <project>/results/Q1/reports/frozen_numbers.json
```

After existing review/sign-off prerequisites pass, the package builder embeds that recorded object as `frozen_numbers.json.provenance`; existing numerical fields remain intact. The helper's `capture` command only captures bytes and never writes the numerical freeze. Shared code, upstream snapshots and additional inputs use repeated `--dependency role=path` arguments.

For existing combined records, use for example `--dependency parameters=results/Q1/run_summary.json --dependency environment=results/Q1/run_summary.json --dependency result_record=results/Q1/run_summary.json`. For a genuine no-execution derivation, use `--scope analytical --dependency result_record=methods/Q1/derivation.md --no-data-reason "No dataset is used" --not-applicable "code=No program was executed" --not-applicable "environment=No computational runtime was used" --not-applicable "parameters=The identity has no selected numeric parameters"`. Each reason must describe the actual case; unsupported exclusions remain evidence gaps.

If effective parameters live in existing code constants or a non-JSON configuration, hash those actual files as `parameters` dependencies and supply `--effective-parameters '{"scale":2}' --parameter-locator 'code/Q1/q1_main.py: SCALE constant, verified against the actual run'`. This records `parameter_binding.mode: documented_inline`; it does not create an auxiliary parameter file. Reviewers reconcile the provided values with the cited source/run. Automatic JSON extraction uses `parameter_binding.mode: json_record`. Either form invalidates when its actual parameter source changes.

|Status|Meaning and required consumer behavior|
|---|---|
|`CURRENT`|Declared dependency content matches. Continue checking completeness, execution evidence and the existing decision gates; this status does not certify mathematical correctness or authorization.|
|`STALE`|At least one declared file changed or is missing. Mark this Qx and its dependent downstream results, figures, prose and audit records stale; retain old records and route to the appropriate authorized stage. A changed input alone is sufficient.|
|`UNVERIFIED_LEGACY`|Old mtime-only/code-only/no-provenance record. Keep its historical values and timestamp, mark provenance as unverified and avoid presenting it as a current freeze.|
|`INVALID`|Malformed/incomplete provenance, fingerprint mismatch or unsafe recorded path. Report the specific defect and keep downstream readiness false.|

Changing only a file's modification time keeps `CURRENT` when its bytes are unchanged. Changing input bytes, an effective parameter/configuration, environment record, result record, shared code or an upstream snapshot invalidates the affected Qx even if its own source-code mtime is unchanged. Validate dependency coverage separately: a hash check cannot discover an omitted input. Record reverse Qx dependencies in the dashboard so invalidation reaches consumers.

### Audit closure and the reviewed technical content

For the [first final-review cycle](decision-authority.md#first-final-review-cycle), record the exact reviewed manuscript/result hashes and preserve the pre-QA review identity plus its immutable technical findings. Audit closure status, cross-references and closure timestamps may be recorded separately from that reviewed-content manifest. A metadata-only final-completeness closure does not change the technical content QA inspected. Do not use the whole mutable audit report as a numerical-run dependency and thereby create a mutual invalidation loop. When an audit report itself is evidence, reference its retained pre-QA snapshot and separately record its closure link. This exception never ignores changes to actual inputs, code, effective parameters, numbers, claims or substantive findings; those changes invalidate their affected reviews. The helper has no generic ignored-field mechanism: every declared file dependency remains a full content hash.

## Migrate historical freezes without inventing evidence

`migrate-legacy --snapshot <old.json> --output <new-migration.json>` preserves the full legacy payload and its SHA-256 in a new record with `provenance: null` and `migration_status: UNVERIFIED_LEGACY`. It does not overwrite the original or upgrade its validity. An old `code_source_files[].mtime`, `source_hashes` covering code only, or a claimed `frozen_at` date cannot satisfy the complete new contract.

To close the migration, attach a complete provenance record demonstrably belonging to that historical run, or regenerate the affected results under the existing execution authority and retain the old version. Merely collecting current hashes beside old numbers is not migration evidence. The resulting freeze still follows all existing package sign-off and evidence requirements.

## Final Python submission entry

Candidate scripts and development helpers may be split while exploring methods. The default final submission has one readable, self-contained `code/Qx/qx_main.py` per question, with all of its model logic in that file, explicit data/config dependencies and commonly available declared third-party libraries. An applicable contest rule or explicit user requirement may specify a different packaging form. Shared development modules do not silently become undeclared final-entry dependencies.

The entry derives the project root from `Path(__file__).resolve().parents[2]` for the `code/Qx/` layout and supports `--project-root` for relocation. Input/output paths are project-relative or explicit absolute overrides, never based on `Path('.')` or the caller's working directory. Support an explicit input override and the resolved data mapping; reject conflicting historical inputs.

The [standalone interface example](../../python-model-code-generator/assets/standalone_entry/code/Q1/q1_main.py) demonstrates this contract using a clearly labeled CSV sum example, not a contest solution. It embeds its own input resolver and imports no repository helper. To verify a generated final entry, copy only that `.py` plus its declared input/config files into an isolated project, launch it once from the project root and once from an unrelated directory, then compare outputs and recorded parameters. Keep fixtures and logs; never use the actual user project as destructive test data.
