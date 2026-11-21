"""Inspect data aliases and content provenance. Never run models or approve gates."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


DATA_ROOTS = {
    "raw": ("workspace/data/data_raw", "workspace/data_raw"),
    "clean": ("workspace/data/data_clean", "workspace/data_clean"),
}
REPORT_PATHS = (
    "workspace/data/data_report.md", "workspace/data_clean/data_report.md",
    "workspace/data_report.md",
)
REQUIRED_ROLES = {"code", "parameters", "environment", "result_record"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def project_path(root: Path, relative: str) -> Path:
    """Resolve project-relative records without escaping the project."""
    if Path(relative).is_absolute():
        raise ValueError("Recorded paths must be project-relative")
    path = (root.resolve() / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Recorded path escapes project root")
    return path


def write_new(path: Path, value: dict) -> None:
    """Evidence is append-only: an existing record is never silently replaced."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def resolve_data_layout(root: Path, selections: dict | None = None) -> dict:
    """Inventory both historical layouts in place; identical aliases stay visible."""
    root = root.resolve()
    selections = {} if selections is None else selections
    if not isinstance(selections, dict):
        raise ValueError("Data mapping must be a JSON object")
    groups = {}
    conflicts = []
    for kind, locations in DATA_ROOTS.items():
        entries = {}
        for location in locations:
            directory = project_path(root, location)
            if not directory.exists():
                continue
            if not directory.is_dir():
                raise ValueError(f"Data directory is not a directory: {location}")
            for path in sorted(directory.rglob("*")):
                if path.is_file():
                    if not path.resolve().is_relative_to(root):
                        raise ValueError("Data symlink escapes project root")
                    logical = path.relative_to(directory).as_posix()
                    # Case-folding catches collisions in portable Windows exports.
                    key = logical.casefold()
                    entry = entries.setdefault(key, {"name": logical, "candidates": []})
                    entry["candidates"].append({
                        "path": path.relative_to(root).as_posix(), "sha256": digest(path),
                    })
        for key, entry in entries.items():
            chosen = selections.get(f"{kind}:{key}")
            candidates = entry["candidates"]
            if chosen is not None:
                matches = [item for item in candidates if item["path"] == chosen]
                if len(matches) != 1:
                    raise ValueError(f"Selection is not an inventoried candidate: {kind}:{key}")
                entry["selected"] = matches[0]["path"]
                entry["resolution"] = "explicit_mapping"
            elif len({item["sha256"] for item in candidates}) == 1:
                entry["selected"] = candidates[0]["path"]
                entry["resolution"] = "identical_aliases" if len(candidates) > 1 else "single_source"
            else:
                entry["selected"] = None
                entry["resolution"] = "conflict"
                conflicts.append(f"{kind}:{key}")
        groups[kind] = entries
    reports = [{"path": p, "sha256": digest(project_path(root, p))}
               for p in REPORT_PATHS if project_path(root, p).is_file()]
    report_choice = selections.get("report")
    if report_choice is not None and report_choice not in [p["path"] for p in reports]:
        raise ValueError("Selected data report is not an inventoried candidate")
    if report_choice is None and reports:
        if len({p["sha256"] for p in reports}) == 1:
            report_choice = reports[0]["path"]
        else:
            conflicts.append("report")
    known = {f"{kind}:{key}" for kind, entries in groups.items() for key in entries} | {"report"}
    if set(selections) - known:
        raise ValueError("Mapping contains an unknown logical input")
    return {"schema_version": 1, "status": "CONFLICT" if conflicts else "RESOLVED",
            "files": groups, "reports": reports, "selected_report": report_choice,
            "conflicts": conflicts,
            "missing_groups": [kind for kind, entries in groups.items() if not entries]}


def fingerprint(record: dict) -> str:
    identity = {key: record[key] for key in
                ("schema_version", "question_id", "dependencies", "parameters", "no_data_reason", "applicability")}
    if "parameter_binding" in record:
        identity["parameter_binding"] = record["parameter_binding"]
    encoded = json.dumps(identity, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_coverage(roles: set, applicability: dict, no_data_reason: str) -> None:
    """Require actual evidence, while making genuinely inapplicable roles explicit."""
    if not isinstance(applicability, dict) or applicability.get("scope") not in {"executed", "analytical"}:
        raise ValueError("scope must be executed or analytical")
    omitted = applicability.get("not_applicable", {})
    if not isinstance(omitted, dict) or set(omitted) - {"code", "parameters", "environment"}:
        raise ValueError("Unknown not-applicable role")
    for role, reason in omitted.items():
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Each not-applicable role needs its actual reason")
        if role in roles:
            raise ValueError("A role cannot be both supplied and not applicable")
        if role in {"code", "environment"} and applicability["scope"] != "analytical":
            raise ValueError("Executed calculations need code and environment evidence")
    if "code" in roles and "environment" in omitted:
        raise ValueError("Executed code still needs its environment evidence")
    if REQUIRED_ROLES - roles - set(omitted):
        raise ValueError("Missing dependency roles: " + ", ".join(sorted(REQUIRED_ROLES - roles - set(omitted))))
    if "data" not in roles and not no_data_reason.strip():
        raise ValueError("Declare data dependencies or a concrete no-data reason")
    if "data" in roles and no_data_reason:
        raise ValueError("A data-dependent run cannot also declare no data")


def capture_provenance(root: Path, question: str, dependencies: list[tuple[str, str]],
                       no_data_reason: str = "", scope: str = "executed",
                       not_applicable: dict | None = None, effective_parameters: dict | None = None,
                       parameter_locator: str = "") -> dict:
    """Capture actual dependencies of a Qx computation or documented derivation."""
    if not question.startswith("Q") or not question[1:].isdigit():
        raise ValueError("question_id must look like Q1")
    root = root.resolve()
    roles = {role for role, _ in dependencies}
    applicability = {"scope": scope, "not_applicable": not_applicable or {}}
    validate_coverage(roles, applicability, no_data_reason)
    inline_parameters = effective_parameters is not None
    if inline_parameters and (not isinstance(effective_parameters, dict) or
                              not parameter_locator.strip() or "parameters" not in roles):
        raise ValueError("Inline effective parameters require an object, source locator and parameters dependency")
    if parameter_locator and not inline_parameters:
        raise ValueError("A parameter locator requires inline effective parameters")
    items = []
    parameters = effective_parameters if inline_parameters else None
    for role, relative in dependencies:
        path = project_path(root, relative)
        if not path.is_file():
            raise ValueError(f"Dependency is missing: {relative}")
        normalized = path.relative_to(root).as_posix()
        if any(item["path"].casefold() == normalized.casefold() and item["role"] == role for item in items):
            raise ValueError(f"Duplicate dependency path and role: {normalized}")
        items.append({"role": role, "path": normalized, "sha256": digest(path)})
        if role == "parameters" and not inline_parameters:
            if parameters is not None:
                raise ValueError("Use one JSON file for effective run parameters")
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
            parameters = payload.get("parameters", payload) if isinstance(payload, dict) else payload
            if not isinstance(parameters, dict):
                raise ValueError("Effective parameters must be a JSON object")
    record = {"schema_version": 2, "question_id": question,
              "captured_at": datetime.now(timezone.utc).isoformat(),
              "dependencies": sorted(items, key=lambda item: (item["role"], item["path"])),
              "parameters": parameters if parameters is not None else {},
              "no_data_reason": no_data_reason, "applicability": applicability}
    record["parameter_binding"] = (
        {"mode": "documented_inline", "source_locator": parameter_locator} if inline_parameters else
        {"mode": "json_record" if "parameters" in roles else "not_applicable"})
    record["fingerprint_sha256"] = fingerprint(record)
    return record


def check_provenance(root: Path, snapshot: dict, expected_question: str | None = None) -> dict:
    """CURRENT only means unchanged declared bytes; it never certifies correctness."""
    if not isinstance(snapshot, dict):
        return {"status": "INVALID", "changes": [], "reason": "Snapshot must be a JSON object"}
    record = snapshot.get("provenance", snapshot)
    if not isinstance(record, dict) or record.get("schema_version") != 2:
        return {"status": "UNVERIFIED_LEGACY", "changes": [],
                "reason": "Legacy timestamp/code-only record lacks complete content provenance"}
    try:
        if not isinstance(record.get("dependencies"), list) or not record["dependencies"]:
            raise ValueError("Dependencies must be a nonempty list")
        if not isinstance(record.get("parameters"), dict) or not isinstance(record.get("no_data_reason"), str):
            raise ValueError("Invalid parameters/no-data fields")
        question = record.get("question_id", "")
        if not isinstance(question, str) or not question.startswith("Q") or not question[1:].isdigit():
            raise ValueError("Invalid question_id")
        if expected_question is not None and question != expected_question:
            raise ValueError("Provenance belongs to another question")
        if fingerprint(record) != record.get("fingerprint_sha256"):
            raise ValueError("Provenance fingerprint does not match its contents")
        roles = {item["role"] for item in record["dependencies"]}
        validate_coverage(roles, record["applicability"], record["no_data_reason"])
        binding = record.get("parameter_binding", {"mode": "json_record" if "parameters" in roles else "not_applicable"})
        if not isinstance(binding, dict) or binding.get("mode") not in {"json_record", "documented_inline", "not_applicable"}:
            raise ValueError("Invalid parameter binding")
        mode = binding["mode"]
        parameter_count = sum(item["role"] == "parameters" for item in record["dependencies"])
        if mode == "json_record" and parameter_count != 1:
            raise ValueError("Use one parameters source when effective parameters exist")
        if mode == "documented_inline" and (not parameter_count or
                not isinstance(binding.get("source_locator"), str) or not binding["source_locator"].strip()):
            raise ValueError("Inline parameters need their actual source dependency and locator")
        if mode == "not_applicable" and parameter_count:
            raise ValueError("A parameters source cannot be declared inapplicable")
        if not parameter_count and record["parameters"]:
            raise ValueError("Parameters cannot be populated when declared not applicable")
        seen = set()
        changes = []
        for item in record["dependencies"]:
            identity = (item["role"], item["path"].casefold())
            if identity in seen:
                raise ValueError("Duplicate dependency path and role")
            seen.add(identity)
            if not re_full_sha(item["sha256"]):
                raise ValueError("Invalid SHA-256 value")
            path = project_path(root, item["path"])
            if not path.is_file():
                changes.append({"path": item["path"], "reason": "missing", "role": item["role"]})
            elif digest(path) != item["sha256"]:
                changes.append({"path": item["path"], "reason": "content_changed", "role": item["role"]})
            elif item["role"] == "parameters" and mode == "json_record":
                payload = json.loads(path.read_text(encoding="utf-8-sig"))
                effective = payload.get("parameters", payload) if isinstance(payload, dict) else payload
                if effective != record["parameters"]:
                    raise ValueError("Parameter values disagree with the recorded file")
        return {"status": "STALE" if changes else "CURRENT", "question_id": record["question_id"],
                "changes": changes, "scope": "declared_dependency_bytes_only"}
    except (KeyError, TypeError, ValueError, OSError, AttributeError) as error:
        return {"status": "INVALID", "changes": [], "reason": str(error)}


def re_full_sha(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def migrate_legacy(source: Path, output: Path) -> dict:
    """Preserve historical data without manufacturing historical execution evidence."""
    legacy = json.loads(source.read_text(encoding="utf-8-sig"))
    record = {"schema_version": 2, "migration_status": "UNVERIFIED_LEGACY",
              "legacy_snapshot_sha256": digest(source), "legacy_snapshot": legacy,
              "provenance": None,
              "required_action": "Attach matching historical full provenance, or rerun under existing authorization"}
    write_new(output, record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    layout = commands.add_parser("data-layout")
    layout.add_argument("--root", type=Path, required=True)
    layout.add_argument("--mapping", type=Path)
    layout.add_argument("--output", type=Path, required=True)
    capture = commands.add_parser("capture")
    capture.add_argument("--root", type=Path, required=True)
    capture.add_argument("--question", required=True)
    capture.add_argument("--dependency", action="append", required=True, metavar="ROLE=PATH")
    capture.add_argument("--no-data-reason", default="")
    capture.add_argument("--scope", choices=("executed", "analytical"), default="executed")
    capture.add_argument("--not-applicable", action="append", default=[], metavar="ROLE=REASON")
    capture.add_argument("--effective-parameters", help="Inline JSON object for parameters stored in code/non-JSON sources")
    capture.add_argument("--parameter-locator", default="", help="Actual source locations and reconciliation of inline parameters")
    capture.add_argument("--output", type=Path, required=True)
    check = commands.add_parser("check")
    check.add_argument("--root", type=Path, required=True)
    check.add_argument("--snapshot", type=Path, required=True)
    check.add_argument("--question", help="Reject a snapshot belonging to another Qx")
    migrate = commands.add_parser("migrate-legacy")
    migrate.add_argument("--snapshot", type=Path, required=True)
    migrate.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "data-layout":
            choices = json.loads(args.mapping.read_text(encoding="utf-8-sig")) if args.mapping else {}
            record = resolve_data_layout(args.root, choices)
            write_new(args.output, record)
        elif args.command == "capture":
            pairs = [tuple(value.split("=", 1)) for value in args.dependency]
            if any(len(pair) != 2 for pair in pairs):
                raise ValueError("Use --dependency ROLE=PROJECT_RELATIVE_PATH")
            omitted = [tuple(value.split("=", 1)) for value in args.not_applicable]
            if any(len(pair) != 2 for pair in omitted) or len(dict(omitted)) != len(omitted):
                raise ValueError("Use one --not-applicable ROLE=REASON per omitted role")
            record = capture_provenance(args.root, args.question, pairs, args.no_data_reason,
                                        args.scope, dict(omitted),
                                        json.loads(args.effective_parameters) if args.effective_parameters is not None else None,
                                        args.parameter_locator)
            write_new(args.output, record)
            record = {"status": "CAPTURED", "question_id": args.question,
                      "fingerprint_sha256": record["fingerprint_sha256"]}
        elif args.command == "migrate-legacy":
            migrate_legacy(args.snapshot, args.output)
            record = {"status": "UNVERIFIED_LEGACY", "original_preserved": True}
        else:
            record = check_provenance(args.root, json.loads(args.snapshot.read_text(encoding="utf-8-sig")), args.question)
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return 0 if record["status"] in {"CURRENT", "CAPTURED", "RESOLVED"} else 2
    except (ValueError, OSError) as error:
        print(json.dumps({"status": "ERROR", "reason": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
