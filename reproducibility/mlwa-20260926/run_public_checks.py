#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run unchanged numerical/witness checkers and report their exact release scope."""
from __future__ import annotations

import csv
import io
import json
import math
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def run_script(arguments: list[str]) -> None:
    completed = subprocess.run([sys.executable, "-B", *arguments], cwd=ROOT, text=True, capture_output=True)
    if completed.returncode:
        print(completed.stdout)
        print(completed.stderr, file=sys.stderr)
        raise RuntimeError(f"Checker failed: {arguments[0]}")


def main() -> int:
    run_script(["verification/independent_outputs/independent_verify.py", "--archive-root", ".", "--output-dir", "verification/public_recheck", "--matrix-only"])
    run_script(["standalone_verify_witnesses.py", "--root", "."])
    run_script(["standalone_verify_global_winners.py"])
    suite = unittest.defaultTestLoader.discover(str(ROOT / "verification" / "independent_outputs"), pattern="test_independent_verify.py")
    captured = io.StringIO()
    tests = unittest.TextTestRunner(stream=captured, verbosity=2).run(suite)
    if not tests.wasSuccessful():
        print(captured.getvalue(), file=sys.stderr)
        raise RuntimeError("Independent numerical unit tests failed")

    recomputation = read_json("verification/public_recheck/INDEPENDENT_VERIFICATION_RESULTS.json")
    pairwise = read_json("qa/STANDALONE_VERIFIER_SUMMARY.json")
    global_witnesses = read_json("qa/STANDALONE_GLOBAL_WINNER_VERIFIER_SUMMARY.json")
    residuals = []
    for relative in ("qa/STANDALONE_VERIFIER_RESULTS.csv", "qa/STANDALONE_GLOBAL_WINNER_VERIFIER_RESULTS.csv"):
        with (ROOT / relative).open(newline="", encoding="utf-8") as stream:
            for row in csv.DictReader(stream):
                value = row.get("maximum_complementarity_residual")
                if value not in (None, ""):
                    residuals.append(float(value))
    tight_complementarity = bool(residuals) and all(math.isfinite(x) and x <= 1e-8 for x in residuals)
    checks = {
        "three_primary_cases": recomputation["primary_cases_pass"] == recomputation["primary_cases_total"] == 3,
        "109_pairwise_cases": recomputation["pairwise_pass"] == recomputation["pairwise_total"] == 109 and recomputation["pairwise_finite"] == 101,
        "14_global_cases": recomputation["global_pass"] == recomputation["global_total"] == 14 and recomputation["global_finite"] == 13,
        "matrix_only_scope": recomputation["implementation"]["raw_matrix_reconstruction_requested"] is False and recomputation["matrix_reconstruction"] == [],
        "101_finite_pairwise_witnesses": pairwise["records_checked"] == 101 and pairwise["all_pass"] is True,
        "14_global_witnesses": global_witnesses["records"] == global_witnesses["pass"] == 14 and global_witnesses["finite_records"] == 13 and global_witnesses["infeasible_certificates"] == 1,
        "three_unit_tests": tests.testsRun == 3 and tests.wasSuccessful(),
        "actual_complementarity_residuals_at_most_1e_8": tight_complementarity,
    }
    summary = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "release_version": "v0.8.1-mlwa-r2.20260926",
        "scope": "Derived-matrix recomputation, independent unit tests and archived primal-dual witness checks; no raw reconstruction or full experiment rerun.",
        "checks": checks,
        "unit_tests_run": tests.testsRun,
        "randomized_pairwise_lp_comparisons_in_unit_test": 120,
        "maximum_actual_complementarity_residual": max(residuals) if residuals else None,
        "unchanged_checker_threshold_note": "Archived checkers allow complementarity up to 10 times each record tolerance; this wrapper additionally tests actual residuals against 1e-8.",
        "software_environment": recomputation["implementation"],
        "reference_inputs_and_results_modified": False,
    }
    (ROOT / "qa" / "PUBLIC_CHECK_SUMMARY.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, allow_nan=False))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
