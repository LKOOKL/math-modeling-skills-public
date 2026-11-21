"""Behavioral regressions; preserve all dedicated fixtures and write evidence."""
import argparse
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
import uuid
from datetime import datetime, timezone

sys.dont_write_bytecode = True
SKILL = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("artifact_contract", SKILL / "scripts/artifact_contract.py")
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)
ENTRY = SKILL.parent / "python-model-code-generator/assets/standalone_entry/code/Q1/q1_main.py"
RUN = None
CASES = []


class ArtifactContractTests(unittest.TestCase):
    def setUp(self):
        self.root = RUN / self.id().rsplit(".", 1)[-1]
        self.root.mkdir(parents=True)

    def put(self, relative, contents):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
        return path

    def capture(self, extra=()):
        files = [("code", "code/Q1/q1_main.py", "print('example')\n"),
                 ("data", "workspace/data_clean/input.csv", "value\n1\n2\n"),
                 ("parameters", "results/Q1/effective_parameters.json", '{"scale":2,"seed":2026}'),
                 ("environment", "results/Q1/environment.json", '{"python":"test-fixture"}'),
                 ("result_record", "results/Q1/run_summary.json", '{"example_fixture":true,"value":6}')]
        files.extend(extra)
        for _, path, contents in files:
            self.put(path, contents)
        return contract.capture_provenance(self.root, "Q1", [(role, path) for role, path, _ in files])

    def note(self, **details):
        CASES.append({"case": self.id().rsplit(".", 1)[-1], **details})

    def test_both_historical_layouts_are_consumed_in_place(self):
        observed = []
        for name, raw, clean, report in [
            ("nested", "workspace/data/data_raw", "workspace/data/data_clean", "workspace/data/data_report.md"),
            ("flat", "workspace/data_raw", "workspace/data_clean", "workspace/data_clean/data_report.md"),
        ]:
            project = self.root / name
            for relative, content in [(raw + "/input.csv", "raw\n"), (clean + "/input.csv", "value\n2\n"),
                                      (report, "Existing audit\n")]:
                self.put(name + "/" + relative, content)
            before = {p.relative_to(project).as_posix(): contract.digest(p) for p in project.rglob("*") if p.is_file()}
            result = contract.resolve_data_layout(project)
            self.assertEqual(result["status"], "RESOLVED")
            self.assertEqual(result["files"]["raw"]["input.csv"]["selected"], raw + "/input.csv")
            self.assertEqual(result["files"]["clean"]["input.csv"]["selected"], clean + "/input.csv")
            self.assertEqual(result["selected_report"], report)
            after = {p.relative_to(project).as_posix(): contract.digest(p) for p in project.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            observed.append({"layout": name, "selected_report": report, "originals_unchanged": True})
        self.note(layouts=observed)

    def test_conflicting_same_name_requires_explicit_mapping(self):
        first = self.put("workspace/data/data_clean/input.csv", "value\n1\n")
        second = self.put("workspace/data_clean/input.csv", "value\n9\n")
        hashes = [contract.digest(first), contract.digest(second)]
        conflict = contract.resolve_data_layout(self.root)
        self.assertEqual(conflict["status"], "CONFLICT")
        self.assertIsNone(conflict["files"]["clean"]["input.csv"]["selected"])
        selected = contract.resolve_data_layout(self.root, {"clean:input.csv": "workspace/data_clean/input.csv"})
        self.assertEqual(selected["status"], "RESOLVED")
        self.assertEqual(selected["files"]["clean"]["input.csv"]["selected"], "workspace/data_clean/input.csv")
        self.assertEqual(hashes, [contract.digest(first), contract.digest(second)])
        self.note(initial_status="CONFLICT", explicit_resolution="RESOLVED", both_originals_unchanged=True)

    def test_identical_aliases_and_report_conflict(self):
        for relative in ["workspace/data/data_raw/input.csv", "workspace/data_raw/input.csv"]:
            self.put(relative, "identical\n")
        self.put("workspace/data/data_report.md", "Report A\n")
        self.put("workspace/data_clean/data_report.md", "Report B\n")
        result = contract.resolve_data_layout(self.root)
        self.assertEqual(result["conflicts"], ["report"])
        self.assertEqual(result["files"]["raw"]["input.csv"]["resolution"], "identical_aliases")
        result = contract.resolve_data_layout(self.root, {"report": "workspace/data_clean/data_report.md"})
        self.assertEqual(result["status"], "RESOLVED")
        self.note(aliases_recorded=2, conflicting_reports_require_mapping=True)

    def test_only_mtime_changes_keep_current(self):
        provenance = self.capture()
        before = contract.check_provenance(self.root, {"provenance": provenance})
        for dependency in provenance["dependencies"]:
            path = self.root / dependency["path"]
            stat = path.stat()
            os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 3600_000_000_000))
        after = contract.check_provenance(self.root, {"provenance": provenance})
        self.assertEqual(before["status"], "CURRENT")
        self.assertEqual(after["status"], "CURRENT")
        self.note(before=before, after=after)

    def test_input_change_with_unchanged_code_and_restored_mtime_is_stale(self):
        provenance = self.capture()
        source_hash = contract.digest(self.root / "code/Q1/q1_main.py")
        data = self.root / "workspace/data_clean/input.csv"
        stat = data.stat()
        data.write_text("value\n1\n9\n", encoding="utf-8")
        os.utime(data, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        result = contract.check_provenance(self.root, provenance)
        self.assertEqual(result["status"], "STALE")
        self.assertEqual([item["role"] for item in result["changes"]], ["data"])
        self.assertEqual(source_hash, contract.digest(self.root / "code/Q1/q1_main.py"))
        self.note(result=result, source_unchanged=True, data_mtime_restored=True)

    def test_parameter_only_change_is_stale(self):
        provenance = self.capture()
        self.put("results/Q1/effective_parameters.json", '{"scale":3,"seed":2026}')
        result = contract.check_provenance(self.root, provenance)
        self.assertEqual(result["status"], "STALE")
        self.assertEqual([item["role"] for item in result["changes"]], ["parameters"])
        self.note(result=result)

    def test_shared_code_and_upstream_snapshot_invalidate_consumers(self):
        provenance = self.capture([
            ("code", "code/shared.py", "CONSTANT=1\n"),
            ("upstream", "results/Q0/frozen_numbers.json", '{"value":1}'),
        ])
        self.put("code/shared.py", "CONSTANT=2\n")
        self.put("results/Q0/frozen_numbers.json", '{"value":2}')
        result = contract.check_provenance(self.root, provenance)
        self.assertEqual(result["status"], "STALE")
        self.assertEqual({change["role"] for change in result["changes"]}, {"code", "upstream"})
        self.note(result=result)

    def test_legacy_migration_preserves_numbers_without_granting_validity(self):
        legacy = {"frozen_at": "2099-01-01T00:00:00Z", "values": {"answer": 6},
                  "code_source_files": [{"path": "code/Q1/q1_main.py", "mtime": "2000-01-01"}]}
        source = self.put("old/frozen_numbers.json", json.dumps(legacy))
        original_hash = contract.digest(source)
        self.assertEqual(contract.check_provenance(self.root, legacy)["status"], "UNVERIFIED_LEGACY")
        migrated = contract.migrate_legacy(source, self.root / "new/migration.json")
        self.assertEqual(migrated["legacy_snapshot"], legacy)
        self.assertEqual(contract.check_provenance(self.root, migrated)["status"], "UNVERIFIED_LEGACY")
        self.assertEqual(original_hash, contract.digest(source))
        with self.assertRaises(FileExistsError):
            contract.migrate_legacy(source, self.root / "new/migration.json")
        self.note(status="UNVERIFIED_LEGACY", original_unchanged=True, historical_values_preserved=True)

    def test_fingerprint_tampering_and_incomplete_roles_cannot_pass(self):
        provenance = self.capture()
        self.assertEqual(contract.check_provenance(self.root, provenance, "Q2")["status"], "INVALID")
        self.assertEqual(contract.check_provenance(self.root, [])["status"], "INVALID")
        provenance["parameters"]["scale"] = 99
        self.assertEqual(contract.check_provenance(self.root, provenance)["status"], "INVALID")
        with self.assertRaises(ValueError):
            contract.capture_provenance(self.root, "Q1", [("code", "code/Q1/q1_main.py")])
        with self.assertRaises(ValueError):
            contract.project_path(self.root, "../outside.txt")
        self.note(tampering="INVALID", wrong_question="INVALID", malformed_snapshot="INVALID",
                  incomplete_dependencies_rejected=True, path_escape_rejected=True)

    def test_standalone_entry_from_two_cwds_for_both_layouts(self):
        scenarios = []
        for layout in ["workspace/data/data_clean", "workspace/data_clean"]:
            name = "nested" if layout.count("/") == 2 else "flat"
            project = self.root / name / "project"
            entry = project / "code/Q1/q1_main.py"
            entry.parent.mkdir(parents=True)
            shutil.copyfile(ENTRY, entry)
            self.put(f"{name}/project/{layout}/values.csv", "value\n1\n2\n3\n")
            outside = self.root / name / "unrelated-directory"
            outside.mkdir(parents=True)
            outcomes = []
            for index, cwd in enumerate([project, outside]):
                command = [sys.executable, "-X", "utf8", str(entry), "--scale", "2", "--output", f"results/check-{index}.json"]
                run = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=True)
                output = json.loads((project / f"results/check-{index}.json").read_text(encoding="utf-8"))
                self.assertEqual(output, json.loads(run.stdout))
                self.assertEqual(output["value"], 12)
                outcomes.append(output)
            self.assertEqual(outcomes[0], outcomes[1])
            scenarios.append({"layout": layout, "value": outcomes[0]["value"],
                              "two_cwds_identical": True, "project_modules_copied": 1})
        self.note(scenarios=scenarios)

    def test_standalone_entry_rejects_conflict_and_accepts_explicit_input(self):
        entry = self.root / "code/Q1/q1_main.py"
        entry.parent.mkdir(parents=True)
        shutil.copyfile(ENTRY, entry)
        self.put("workspace/data/data_clean/values.csv", "value\n1\n")
        self.put("workspace/data_clean/values.csv", "value\n9\n")
        rejected = subprocess.run([sys.executable, "-X", "utf8", str(entry)], cwd=self.root,
                                  capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(rejected.returncode, 0)
        accepted = subprocess.run([sys.executable, "-X", "utf8", str(entry), "--input", "workspace/data_clean/values.csv"],
                                  cwd=self.root, capture_output=True, text=True, encoding="utf-8", check=True)
        self.assertEqual(json.loads(accepted.stdout)["value"], 9)
        self.note(ambiguous_input_rejected=True, explicit_input_value=9)

    def test_cli_content_check_reports_stale_and_nonzero_exit(self):
        provenance = self.capture()
        snapshot = self.put("results/Q1/frozen_numbers.json", json.dumps({"value": 6, "provenance": provenance}))
        command = [sys.executable, "-X", "utf8", str(SKILL / "scripts/artifact_contract.py"), "check",
                   "--root", str(self.root), "--snapshot", str(snapshot)]
        first = subprocess.run(command, cwd=RUN, capture_output=True, text=True, encoding="utf-8", check=True)
        self.assertEqual(json.loads(first.stdout)["status"], "CURRENT")
        self.put("workspace/data_clean/input.csv", "value\n3\n4\n")
        second = subprocess.run(command, cwd=RUN, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(second.returncode, 2)
        self.assertEqual(json.loads(second.stdout)["status"], "STALE")
        self.note(cli_before="CURRENT", cli_after="STALE", stale_exit_code=second.returncode)

    def test_one_existing_record_can_cover_multiple_actual_roles(self):
        self.put("code/Q1/q1_main.py", "print(6)\n")
        self.put("data.csv", "value\n3\n")
        self.put("run_summary.json", '{"parameters":{"scale":2},"environment":{"python":"fixture"},"value":6}')
        dependencies = [("code", "code/Q1/q1_main.py"), ("data", "data.csv")]
        dependencies += [(role, "run_summary.json") for role in ("parameters", "environment", "result_record")]
        provenance = contract.capture_provenance(self.root, "Q1", dependencies)
        self.assertEqual(provenance["parameters"], {"scale": 2})
        self.assertEqual(contract.check_provenance(self.root, provenance)["status"], "CURRENT")
        self.note(existing_files=3, dependency_roles=5, shared_record_roles=["parameters", "environment", "result_record"])

    def test_analytical_no_execution_needs_no_dummy_code_or_parameter_files(self):
        self.put("methods/Q1/proof.md", "Example analytic identity and its source derivation.\n")
        omitted = {"code": "Symbolic reasoning only; no program was executed",
                   "environment": "No computational runtime was used",
                   "parameters": "Identity has no selected numeric parameters"}
        provenance = contract.capture_provenance(self.root, "Q1", [("result_record", "methods/Q1/proof.md")],
                                                  "Analytic identity has no dataset", "analytical", omitted)
        self.assertEqual(contract.check_provenance(self.root, provenance)["status"], "CURRENT")
        self.assertEqual(len([p for p in self.root.rglob("*") if p.is_file()]), 1)
        self.note(status="CURRENT", scope="analytical", evidence_files=1, dummy_files_created=False)

    def test_parameter_free_execution_and_missing_real_dependency(self):
        self.put("entry.py", "print(1+2)\n")
        self.put("run.json", '{"environment":{"python":"fixture"},"value":3}')
        dependencies = [("code", "entry.py"), ("environment", "run.json"), ("result_record", "run.json")]
        provenance = contract.capture_provenance(self.root, "Q1", dependencies,
                                                  "Constant expression has no external data", "executed",
                                                  {"parameters": "No runtime choices or tunable parameters"})
        self.assertEqual(contract.check_provenance(self.root, provenance)["status"], "CURRENT")
        with self.assertRaises(ValueError):
            contract.capture_provenance(self.root, "Q1", dependencies + [("data", "missing.csv")],
                                        not_applicable={"parameters": "No runtime parameters"})
        with self.assertRaises(ValueError):
            contract.capture_provenance(self.root, "Q1", dependencies[1:], "No data", "executed",
                                        {"parameters": "No runtime parameters", "code": "Missing script"})
        self.note(parameter_free_status="CURRENT", declared_missing_data_rejected=True,
                  executed_missing_code_cannot_be_excused=True)

    def test_actual_code_and_non_json_parameters_need_no_auxiliary_file(self):
        self.put("entry.py", "SCALE = 2\n")
        self.put("config.yaml", "offset: 1\n")
        self.put("run.json", '{"environment":{"python":"fixture"},"value":7}')
        dependencies = [("code", "entry.py"), ("parameters", "entry.py"), ("parameters", "config.yaml"),
                        ("environment", "run.json"), ("result_record", "run.json")]
        provenance = contract.capture_provenance(self.root, "Q1", dependencies,
            "Constant-expression fixture has no data", effective_parameters={"scale": 2, "offset": 1},
            parameter_locator="entry.py:SCALE and config.yaml:offset, checked against fixture run")
        self.assertEqual(contract.check_provenance(self.root, provenance)["status"], "CURRENT")
        self.assertEqual(len([p for p in self.root.rglob("*") if p.is_file()]), 3)
        with self.assertRaises(ValueError):
            contract.capture_provenance(self.root, "Q1", dependencies, "No data", effective_parameters={"scale": 2})
        self.put("config.yaml", "offset: 9\n")
        changed = contract.check_provenance(self.root, provenance)
        self.assertEqual(changed["status"], "STALE")
        self.assertEqual([item["path"] for item in changed["changes"]], ["config.yaml"])
        self.note(before="CURRENT", after=changed, original_files=3, auxiliary_parameter_file_created=False,
                  missing_parameter_locator_rejected=True)

    def test_cli_capture_uses_existing_parameter_source(self):
        self.put("entry.py", "SCALE = 2\n")
        self.put("run.json", '{"environment":{"python":"fixture"},"value":6}')
        output = self.root / "captured.json"
        command = [sys.executable, "-X", "utf8", str(SKILL / "scripts/artifact_contract.py"), "capture",
                   "--root", str(self.root), "--question", "Q1", "--dependency", "code=entry.py",
                   "--dependency", "parameters=entry.py", "--dependency", "environment=run.json",
                   "--dependency", "result_record=run.json", "--no-data-reason", "Fixed expression has no dataset",
                   "--effective-parameters", '{"scale":2}', "--parameter-locator", "entry.py:SCALE",
                   "--output", str(output)]
        result = subprocess.run(command, cwd=RUN, capture_output=True, text=True, encoding="utf-8", check=True)
        self.assertEqual(json.loads(result.stdout)["status"], "CAPTURED")
        provenance = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(contract.check_provenance(self.root, provenance)["status"], "CURRENT")
        self.note(cli_status="CAPTURED", check_status="CURRENT", parameter_source="entry.py")

    def test_mapping_selected_input_and_relocated_entry(self):
        entry = self.root / "relocated_entry.py"
        shutil.copyfile(ENTRY, entry)
        project = self.root / "project"
        self.put("project/workspace/data/data_clean/values.csv", "value\n1\n")
        self.put("project/workspace/data_clean/values.csv", "value\n9\n")
        mapping = contract.resolve_data_layout(project, {"clean:values.csv": "workspace/data_clean/values.csv"})
        self.put("project/planning/data_paths.json", json.dumps(mapping))
        command = [sys.executable, "-X", "utf8", str(entry), "--project-root", str(project)]
        result = subprocess.run(command, cwd=RUN, capture_output=True, text=True, encoding="utf-8", check=True)
        self.assertEqual(json.loads(result.stdout)["value"], 9)
        self.put("project/workspace/data_clean/values.csv", "value\n8\n")
        changed = subprocess.run(command, cwd=RUN, capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(changed.returncode, 0)
        self.assertIn("Input changed since the data mapping", changed.stderr)
        with self.assertRaises(ValueError):
            contract.resolve_data_layout(project, [])
        self.note(mapped_input_value=9, relocated_entry_passed=True, changed_mapped_data_rejected=True,
                  malformed_mapping_rejected=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-root", type=Path, required=True)
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    RUN = args.evidence_root.resolve() / stamp
    RUN.mkdir(parents=True)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ArtifactContractTests))
    log = stream.getvalue()
    (RUN / "test-run.log").write_text(log, encoding="utf-8")
    evidence = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests_run": result.testsRun,
                "failures": len(result.failures), "errors": len(result.errors), "cases": CASES,
                "fixture_policy": "dedicated test samples retained; no cleanup or deletion",
                "helper_sha256": contract.digest(SKILL / "scripts/artifact_contract.py"),
                "standalone_example_sha256": contract.digest(ENTRY)}
    (RUN / "evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(log)
    print(json.dumps({"status": evidence["status"], "tests_run": result.testsRun, "evidence_directory": str(RUN)}, ensure_ascii=False))
    raise SystemExit(0 if result.wasSuccessful() else 1)
