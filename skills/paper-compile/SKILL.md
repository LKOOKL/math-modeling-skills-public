---
name: paper-compile
description: Compile an existing LaTeX paper or section, diagnose typesetting errors, and inspect the resulting PDF while preserving previous successful artifacts. Use for paper compilation, PDF building, and layout checks within the supplied project and current submission rules.
---

# Safe LaTeX Paper Compilation

Build the requested source in a fresh isolated directory. Preserve the existing source, successful PDF and logs. Report compilation, PDF parsing, content checks and visual review separately; none of them establishes mathematical correctness or submission approval.

## Scope and prerequisites

1. Identify the actual project root, entry `.tex`, requested scope (section or full paper), existing delivery PDF and current build configuration. Record the original source/PDF hashes before changing anything.
2. Inspect the entry and included files, build scripts, latexmk configuration, bibliography hooks, `filecontents`, shell escape and external commands. Only typesetting and the project's actual bibliography processing are in scope. Solver runs, data preparation, numerical plotting and experiments need a separately authorized route; report the exact trigger and missing pre-generated artifact, and continue independent writing or safe typesetting.
3. Use the project's engine and bibliography tool. CJK/fontspec commonly requires XeLaTeX or LuaLaTeX, but inspect the actual configuration rather than assuming an engine. Do not substitute a fixed pdfLaTeX chain or install packages without the required authorization.
4. Record applicable contest/year/venue requirements and the user's template. No fixed conference page limit, minimum PDF byte count or mandatory independent Conclusion chapter applies across projects. If rules are unavailable, continue the build and mark submission compliance unverified.
5. Check the required fonts, classes, included sources, figures and bibliography. Missing technical content remains a named gap; do not invent citations, equations, graphics or results to make compilation pass.

## Isolate the build and preserve previous versions

- Create a new, collision-free run directory, for example `paper/build/run-<timestamp>-<suffix>/`, with a `work/` snapshot and `work/out/` products. Use an ASCII path if the local TeX toolchain has path-encoding restrictions. Never reuse a directory containing a prior successful build as disposable scratch space.
- Copy only the required project sources and known dependencies into the snapshot, preserving relative paths; explicitly account for dependencies outside the paper directory. Exclude previous build directories and delivery outputs. Record the copied file manifest and hashes. A full project source snapshot may be needed for relative appendix/code references; copying it does not authorize executing those sources.
- Run from the snapshot, with output directed to the fresh `out/` directory. Review any source-side write directives before running; protect bibliography and other maintained files. Keep shell escape disabled unless a specific required typesetting command and its permissions have been inspected and authorized.
- Ordinary builds have no cleanup phase. Do not run destructive clean commands, remove old PDFs, or overwrite the previous successful delivery before the new build and requested checks pass. Any separately requested deletion must obey the user's and host's file-protection mechanism.
- Keep the working directory and output directory explicit. Resolve engine executables for the current host; shell examples are not portable verbatim between PowerShell and Bash.

## Run the inspected typesetting chain

The following are examples for a project already confirmed to use XeLaTeX. `work/` is the copied source directory; `out/` already exists in this run. Choose the actual engine and entry for the project. An audited project build script may be used only if it follows the same isolation and no-computation boundaries.

PowerShell, from the snapshot working directory:

```powershell
# Set these from inspected project configuration; keep the engine path explicit.
$enginePath = (Get-Command -Name xelatex -CommandType Application -ErrorAction Stop).Source
$buildOut = 'out' # Existing output directory relative to this isolated work directory.
$buildArgs = @('-no-shell-escape', '-interaction=nonstopmode',
    '-halt-on-error', '-recorder', "-output-directory=$buildOut", 'main.tex')
& $enginePath @buildArgs *> (Join-Path $buildOut 'pass-1.stdout.log')
if ($LASTEXITCODE -ne 0) {
    throw 'Build failed; preserve this run and the previous delivery PDF.'
}
```

Bash, from the snapshot working directory:

```bash
# Set engine_path to the inspected executable and create out before this call.
"$engine_path" -no-shell-escape -interaction=nonstopmode -halt-on-error \
  -recorder -output-directory=out main.tex > out/pass-1.stdout.log 2>&1
build_status=$?
if [ "$build_status" -ne 0 ]; then
  printf '%s\n' 'Build failed; preserve this run and the previous delivery PDF.'
  exit "$build_status"
fi
```

After a successful first pass, run the bibliography tool only if the project actually requires it, directing its inputs/outputs to the run directory (for an inspected Biber project: `biber --input-directory=out --output-directory=out main`). Ensure the `.bcf` and bibliography paths resolve inside the snapshot. Repeat the engine only to resolve outstanding references or after a necessary typesetting edit. Keep each command, exit status and stdout/stderr log. Avoid automatic dependency installers or uninspected latexmk hooks.

## Diagnose and repair within writing scope

- Read the first actionable error in the log and locate its source in the snapshot. Repair TeX syntax, resource paths, font configuration, bibliography syntax and pure layout defects. Preserve equations, numerical values, evidence scope and user-maintained bibliography entries.
- An undefined citation requires an existing verified source or an explicit missing-source record; do not fabricate a `.bib` entry. Missing plots require supplied/pre-generated figures, not a new computation during the build.
- Track unreferenced source files as informational; do not delete them. Resolve the actual `input`/`include` expansion before judging heading ownership.
- After repeated failure of the same class, preserve logs and report the specific dependency or defect. Continue independent authorized work. Never label the old delivery as the new build's result.
- If snapshot fixes should enter the maintained source, apply only the reviewed diff within the requested scope, preserve the prior version, and rebuild from the updated snapshot. No whole-file replacement is needed for a local correction.

## Acceptance checks

Check only what the current task requests, and record any wider checks left pending:

1. **Build:** successful exit for the complete inspected chain, a newly generated PDF, and logs from this run. A stale PDF alongside a failed command is not success.
2. **Parse and contents:** open the PDF with an available parser, count actual pages and verify expected text/page content. A valid small PDF is acceptable; byte size alone does not prove validity or completeness.
3. **References and glyphs:** inspect warnings and extracted text for undefined references, missing citations or glyphs; text extraction is supplemented by visual review where required.
4. **Structure and page scope:** use current submission rules plus actual source labels and page positions for front matter, body, references and appendix. A mathematical-modeling paper can end its answers in each Qx and its evaluation/generalization chapter, without a standalone Conclusion chapter. Keep each Qx section, local results/error/sensitivity subsections, and source-backed pseudocode/flowchart coverage intact.
5. **Trace markers:** follow [tracking-format.md](../write-math-modeling-papers/references/tracking-format.md). TeX uses standalone `% decision_id: ...` or `% evidence_id: ...` lines. Verify both that internal identifiers are absent from PDF body text and that the following intended prose remains visible. Markdown HTML comments must be converted before TeX insertion.
6. **Visual review:** render and inspect the relevant pages for clipping, overlap, font problems, isolated headings, table/algorithm completeness and figure-text proximity. State the exact pages inspected; parsing or a zero exit code is not a visual pass.
7. **Rules and evidence:** compare size/pages/anonymity against actual current limits only when verified. Compilation may pass while a missing sensitivity report leaves the manuscript a partial draft. Do not compute missing analyses to close a writing gap.

## Delivery and report

On failure, retain the failed run and logs; verify the previous successful PDF remains unchanged by hash. Report the failed run explicitly and link the previous version only with its original status.

On success, deliver the checked PDF as a new version or retain it in its isolated run. Update a canonical delivery path only within the authorized scope, after preserving its previous version and passing the required checks. Do not delete prior artifacts.

The report records: source/snapshot identity, engine and actual commands, run directory, exit statuses, PDF path/hash/page count, parsing/content results, visual pages, applicable rule source, unresolved warnings and material gaps. Recommend the scoped writing or review skill for remaining issues; do not assume an uninstalled `/paper-write` command. Uploading, submitting and making compliance claims require their own actual authorization and evidence.
