#!/usr/bin/env python3
"""Dependency-free verifier for released CERT-Bench primal-dual witnesses.

This script intentionally imports only the Python standard library. It reads
serialized matrices, nominal weights, and witness JSONL files; it does not
import the analysis implementation or SciPy.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable


def dot(a: Iterable[float], b: Iterable[float]) -> float:
    return math.fsum(x * y for x, y in zip(a, b))


def load_matrix(path: Path) -> tuple[list[str], list[str], list[list[float]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        methods = header[1:]
        tasks = []
        matrix = []
        for row in reader:
            tasks.append(row[0])
            matrix.append([float(x) for x in row[1:]])
    return tasks, methods, matrix


def load_weights(path: Path) -> tuple[list[str], list[float]]:
    tasks, weights = [], []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            tasks.append(row["task"])
            weights.append(float(row["nominal_weight"]))
    return tasks, weights


def matrix_sha256(matrix: list[list[float]]) -> str:
    # Match the analysis hash: ASCII shape then C-order float64 bytes.
    import struct
    d = len(matrix)
    m = len(matrix[0]) if d else 0
    h = hashlib.sha256()
    h.update(str((d, m)).encode("ascii"))
    for row in matrix:
        for value in row:
            h.update(struct.pack("=d", float(value)))
    return h.hexdigest()


def verify_record(record: dict, matrix: list[list[float]], weights: list[float]) -> dict:
    tol = float(record["verification_tolerance"])
    wi = int(record["winner_index"])
    cj = int(record["competitor_index"])
    w0 = [float(x) for x in record["nominal_weights"]]
    w = [float(x) for x in record["primal_weights"]]
    u = [float(x) for x in record["primal_absolute_deviations"]]
    alpha = [float(x) for x in record["dual_alpha"]]
    beta = [float(x) for x in record["dual_beta"]]
    lam = float(record["dual_lambda"])
    nu = float(record["dual_nu"])
    if len(w0) != len(matrix) or len(weights) != len(matrix):
        raise ValueError("dimension mismatch")
    if max(abs(a-b) for a,b in zip(w0, weights)) > tol:
        raise ValueError("serialized nominal weights differ from released weight file")
    g = [row[cj] - row[wi] for row in matrix]

    primal_viol = []
    primal_viol.extend(-x for x in w)
    primal_viol.extend(-x for x in u)
    primal_viol.extend(wi_ - ui_ - b for wi_, ui_, b in zip(w, u, w0))
    primal_viol.extend(-wi_ - ui_ + b for wi_, ui_, b in zip(w, u, w0))
    primal_viol.append(dot(g, w))
    primal_viol.append(abs(math.fsum(w) - 1.0))
    max_primal = max(0.0, max(primal_viol))

    dual_w_slack = [a - b + lam*gi - nu for a,b,gi in zip(alpha,beta,g)]
    dual_u_slack = [0.5 - a - b for a,b in zip(alpha,beta)]
    dual_viol = []
    dual_viol.extend(-a for a in alpha)
    dual_viol.extend(-b for b in beta)
    dual_viol.append(-lam)
    dual_viol.extend(-s for s in dual_w_slack)
    dual_viol.extend(-s for s in dual_u_slack)
    max_dual = max(0.0, max(dual_viol))

    pobj = 0.5 * math.fsum(u)
    dobj = nu + dot(w0, [b-a for a,b in zip(alpha,beta)])
    objective_gap = abs(pobj-dobj)
    stored_pgap = max(abs(pobj-float(record["primal_objective"])), abs(dobj-float(record["dual_objective"])))

    slack1 = [b-wi_+ui_ for b,wi_,ui_ in zip(w0,w,u)]
    slack2 = [wi_+ui_-b for b,wi_,ui_ in zip(w0,w,u)]
    slack3 = -dot(g,w)
    comps = []
    comps.extend(a*s for a,s in zip(alpha,slack1))
    comps.extend(b*s for b,s in zip(beta,slack2))
    comps.append(lam*slack3)
    comps.extend(wi_*s for wi_,s in zip(w,dual_w_slack))
    comps.extend(ui_*s for ui_,s in zip(u,dual_u_slack))
    max_comp = max(abs(x) for x in comps)

    passed = (
        max_primal <= tol
        and max_dual <= tol
        and objective_gap <= tol
        and stored_pgap <= tol
        and max_comp <= 10.0*tol
    )
    return {
        "case_id": record["case_id"],
        "winner": record["winner"],
        "competitor": record["competitor"],
        "status": "PASS" if passed else "FAIL",
        "maximum_primal_violation": max_primal,
        "maximum_dual_violation": max_dual,
        "objective_gap": objective_gap,
        "stored_objective_recalculation_gap": stored_pgap,
        "maximum_complementarity_residual": max_comp,
        "verification_tolerance": tol,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.root.resolve()
    out_rows = []
    for witness_path in sorted((root / "witnesses").glob("*__primal_dual_witnesses.jsonl")):
        case_id = witness_path.name.replace("__primal_dual_witnesses.jsonl", "")
        matrix_path = root / "data" / "processed" / f"{case_id}__normalized_matrix.csv"
        weights_path = root / "data" / "processed" / f"{case_id}__nominal_weights.csv"
        tasks, methods, matrix = load_matrix(matrix_path)
        weight_tasks, weights = load_weights(weights_path)
        if tasks != weight_tasks:
            raise AssertionError(f"task order mismatch for {case_id}")
        mhash = matrix_sha256(matrix)
        with witness_path.open(encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                record = json.loads(line)
                if record["matrix_sha256"] != mhash:
                    raise AssertionError(f"matrix hash mismatch for {case_id}")
                if record["task_names"] != tasks or record["method_names"] != methods:
                    raise AssertionError(f"name/order mismatch for {case_id}")
                out_rows.append(verify_record(record, matrix, weights))

    qa = root / "qa"
    qa.mkdir(parents=True, exist_ok=True)
    csv_path = qa / "STANDALONE_VERIFIER_RESULTS.csv"
    fields = list(out_rows[0]) if out_rows else ["case_id","status"]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(out_rows)
    summary = {
        "verifier": "dependency-free Python standard-library verifier",
        "analysis_implementation_imported": False,
        "records_checked": len(out_rows),
        "all_pass": bool(out_rows) and all(r["status"] == "PASS" for r in out_rows),
        "maximum_objective_gap": max((r["objective_gap"] for r in out_rows), default=None),
        "maximum_primal_violation": max((r["maximum_primal_violation"] for r in out_rows), default=None),
        "maximum_dual_violation": max((r["maximum_dual_violation"] for r in out_rows), default=None),
        "maximum_complementarity_residual": max((r["maximum_complementarity_residual"] for r in out_rows), default=None),
    }
    (qa / "STANDALONE_VERIFIER_SUMMARY.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
