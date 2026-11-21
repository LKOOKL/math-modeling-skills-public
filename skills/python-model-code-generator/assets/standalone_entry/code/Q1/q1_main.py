"""Submission-entry example: sum CSV `value` times a scale, not a contest model.

Keep this file at code/Q1/q1_main.py, or pass --project-root when relocating it.
Only the standard library and the declared data/config files are required.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path


def resolve_input(root, specified):
    if specified:
        path = Path(specified)
        return path if path.is_absolute() else root / path
    manifest = root / "planning/data_paths.json"
    if manifest.is_file():
        entry = json.loads(manifest.read_text(encoding="utf-8-sig"))["files"]["clean"]["values.csv"]
        if entry["selected"] is None:
            raise ValueError("Input mapping has an unresolved conflict")
        path = (root / entry["selected"]).resolve()
        if not path.is_relative_to(root):
            raise ValueError("Input mapping escapes the project")
        candidates = {item["path"]: item["sha256"] for item in entry["candidates"]}
        if hashlib.sha256(path.read_bytes()).hexdigest() != candidates[entry["selected"]]:
            raise ValueError("Input changed since the data mapping; refresh its audit first")
        return path
    candidates = [root / location / "values.csv" for location in
                  ("workspace/data/data_clean", "workspace/data_clean")]
    present = [path for path in candidates if path.is_file()]
    if not present:
        raise FileNotFoundError("Provide values.csv in an accepted layout or pass --input")
    if len({hashlib.sha256(path.read_bytes()).hexdigest() for path in present}) != 1:
        raise ValueError("Same-name inputs differ; pass --input with the confirmed project-relative path")
    return present[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--input")
    parser.add_argument("--scale", type=float, default=1.0)
    parser.add_argument("--output", default="results/Q1/experiments/final/tables/example.json")
    args = parser.parse_args()
    root = args.project_root.resolve()
    source = resolve_input(root, args.input).resolve()
    with source.open(encoding="utf-8-sig", newline="") as stream:
        values = [float(row["value"]) for row in csv.DictReader(stream)]
    result = {"example_only": True, "rows": len(values), "value": sum(values) * args.scale,
              "parameters": {"scale": args.scale}, "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    if output.resolve() == source:
        raise ValueError("Output cannot overwrite the input")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
