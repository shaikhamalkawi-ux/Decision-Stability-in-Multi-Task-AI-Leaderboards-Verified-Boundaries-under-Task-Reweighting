#!/usr/bin/env python3
"""Independent, fail-closed verification for the CERT-Bench v0.8/R2B state.

This module intentionally does not import any result-determining implementation
from the release archive.  Pairwise and Top-k boundaries use an ordered
mass-transfer calculation.  Global feasible-winner entries use a fresh SciPy
``linprog`` formulation built directly from released matrices.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import linprog
from scipy.stats import rankdata


TIE_TOLERANCE = 1e-12
AUDIT_TOLERANCE = 5e-8


CASE_FILES = {
    "primary11__all__rank__equal": "primary11__all__rank__equal",
    "primary11__iid__rank__equal": "primary11__iid__rank__equal",
    "primary11__temporal__rank__equal": "primary11__temporal__rank__equal",
    "primary11__grouped__rank__equal": "primary11__grouped__rank__equal",
    "primary11__all__rank__regime_balanced": "primary11__all__rank__regime_balanced",
    "primary11__all__minmax__equal": "primary11__all__minmax__equal",
    "coverage9__all__rank__equal": "coverage9__all__rank__equal",
    "coverage9__primary122__rank__equal": "coverage9__primary122__rank__equal",
    "living12__all__rank__equal": "living12__all__rank__equal",
    "tabarena_primary14__rank__equal": "tabarena_primary14__rank__equal",
    "benchpress_primary10__rank__equal": "benchpress_primary10__rank__equal",
}


PRIMARY_EXPECTED = {
    "TabArena": {
        "case_id": "tabarena_primary14__rank__equal",
        "shape": (51, 14),
        "winner": "REALMLP (tuned + ensemble)",
        "nearest": "GBM (tuned + ensemble)",
        "top1": 0.03660130718954256,
        "top3": 0.02832244008714597,
        "top5": 0.005446623093681942,
    },
    "BenchPress": {
        "case_id": "benchpress_primary10__rank__equal",
        "shape": (11, 10),
        "winner": "claude-opus-4.6",
        "nearest": "gpt-5.2",
        "top1": 0.09090909090909088,
        "top3": 0.040909090909091055,
        "top5": 0.17171717171717177,
    },
    "BeyondArena": {
        "case_id": "primary11__all__rank__equal",
        "shape": (122, 11),
        "winner": "TA-TABPFN-2.6 (default)",
        "nearest": "TA-TABICLv2 (default)",
        "top1": 0.018670309653916153,
        "top3": 0.08606557377049187,
        "top5": 0.01891551071878944,
    },
}


TABARENA_METHODS = [
    "CAT (tuned + ensemble)",
    "EBM (tuned + ensemble)",
    "FASTAI (tuned + ensemble)",
    "GBM (tuned + ensemble)",
    "KNN (tuned + ensemble)",
    "LR (tuned + ensemble)",
    "MNCA (tuned + ensemble)",
    "NN_TORCH (tuned + ensemble)",
    "REALMLP (tuned + ensemble)",
    "RF (tuned + ensemble)",
    "TABDPT (default)",
    "TABM (tuned + ensemble)",
    "XGB (tuned + ensemble)",
    "XT (tuned + ensemble)",
]


@dataclass
class MatrixCase:
    case_id: str
    tasks: list[str]
    methods: list[str]
    z: np.ndarray
    w0: np.ndarray


@dataclass
class BoundaryResult:
    radius: float
    weights: np.ndarray | None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_case(root: Path, case_id: str) -> MatrixCase:
    stem = CASE_FILES[case_id]
    matrix_path = root / "data" / "processed" / f"{stem}__normalized_matrix.csv"
    weights_path = root / "data" / "processed" / f"{stem}__nominal_weights.csv"
    matrix = pd.read_csv(matrix_path, index_col=0)
    weights = pd.read_csv(weights_path)
    if list(map(str, matrix.index)) != list(map(str, weights.iloc[:, 0])):
        raise ValueError(f"Task order mismatch for {case_id}")
    w0 = weights["nominal_weight"].to_numpy(float)
    z = matrix.to_numpy(float)
    if z.ndim != 2 or z.shape[0] != w0.size:
        raise ValueError(f"Invalid task x method orientation for {case_id}: {z.shape}")
    if not np.isfinite(z).all() or not np.isfinite(w0).all():
        raise ValueError(f"Non-finite admitted value in {case_id}")
    if np.any(w0 < -TIE_TOLERANCE) or not math.isclose(float(w0.sum()), 1.0, abs_tol=TIE_TOLERANCE):
        raise ValueError(f"Invalid nominal weights for {case_id}")
    return MatrixCase(
        case_id=case_id,
        tasks=list(map(str, matrix.index)),
        methods=list(map(str, matrix.columns)),
        z=z,
        w0=w0,
    )


def rank_normalize(values: np.ndarray, *, higher_is_better: bool) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    ranked = rankdata(-arr if higher_is_better else arr, axis=1, method="average")
    return (ranked - 1.0) / (arr.shape[1] - 1.0)


def pairwise_transport(
    z: np.ndarray,
    inside: int,
    outside: int,
    w0: np.ndarray,
    tolerance: float = TIE_TOLERANCE,
) -> BoundaryResult:
    """Nearest TV boundary at which ``outside`` ties or beats ``inside``.

    The calculation greedily removes mass from the largest entries of the
    task-wise gap and adds it to the smallest entries.  It is independent of
    the release LP implementation.
    """

    gap_vector = np.asarray(z[:, outside] - z[:, inside], dtype=float)
    remaining = float(w0 @ gap_vector)
    if remaining <= tolerance:
        return BoundaryResult(0.0, np.asarray(w0, dtype=float).copy())

    donors = np.argsort(-gap_vector, kind="stable")
    receivers = np.argsort(gap_vector, kind="stable")
    donor_mass = np.asarray(w0, dtype=float).copy()
    receiver_capacity = 1.0 - np.asarray(w0, dtype=float)
    witness = np.asarray(w0, dtype=float).copy()
    moved = 0.0
    donor_pos = receiver_pos = 0

    while remaining > tolerance and donor_pos < len(donors) and receiver_pos < len(receivers):
        donor = int(donors[donor_pos])
        receiver = int(receivers[receiver_pos])
        if donor_mass[donor] <= tolerance:
            donor_pos += 1
            continue
        if receiver_capacity[receiver] <= tolerance:
            receiver_pos += 1
            continue
        improvement = float(gap_vector[donor] - gap_vector[receiver])
        if improvement <= tolerance:
            break
        amount = min(
            float(donor_mass[donor]),
            float(receiver_capacity[receiver]),
            remaining / improvement,
        )
        if amount <= tolerance:
            break
        donor_mass[donor] -= amount
        receiver_capacity[receiver] -= amount
        witness[donor] -= amount
        witness[receiver] += amount
        moved += amount
        remaining -= amount * improvement
        if donor_mass[donor] <= tolerance:
            donor_pos += 1
        if receiver_capacity[receiver] <= tolerance:
            receiver_pos += 1

    if remaining > 1e-9:
        return BoundaryResult(float("inf"), None)
    witness[np.abs(witness) < tolerance] = 0.0
    return BoundaryResult(float(moved), witness)


def global_entry_lp(case: MatrixCase, candidate: int) -> BoundaryResult:
    d, m = case.z.shape
    objective = np.concatenate([np.zeros(d), np.full(d, 0.5)])
    rows: list[np.ndarray] = []
    rhs: list[float] = []
    for task in range(d):
        row = np.zeros(2 * d)
        row[task] = 1.0
        row[d + task] = -1.0
        rows.append(row)
        rhs.append(float(case.w0[task]))

        row = np.zeros(2 * d)
        row[task] = -1.0
        row[d + task] = -1.0
        rows.append(row)
        rhs.append(float(-case.w0[task]))

    for competitor in range(m):
        if competitor == candidate:
            continue
        row = np.zeros(2 * d)
        row[:d] = case.z[:, candidate] - case.z[:, competitor]
        rows.append(row)
        rhs.append(0.0)

    equality = np.zeros((1, 2 * d))
    equality[0, :d] = 1.0
    result = linprog(
        objective,
        A_ub=np.vstack(rows),
        b_ub=np.asarray(rhs),
        A_eq=equality,
        b_eq=np.array([1.0]),
        bounds=[(0.0, None)] * (2 * d),
        method="highs",
    )
    if result.status == 2:
        return BoundaryResult(float("inf"), None)
    if not result.success:
        raise RuntimeError(f"Global LP failed for {case.case_id}/{case.methods[candidate]}: {result.message}")
    return BoundaryResult(float(result.fun), np.asarray(result.x[:d], dtype=float))


def nominal_summary(case: MatrixCase) -> tuple[np.ndarray, int, int, float]:
    scores = case.w0 @ case.z
    order = np.argsort(scores, kind="stable")
    winner = int(order[0])
    radii = [
        (pairwise_transport(case.z, winner, competitor, case.w0).radius, competitor)
        for competitor in range(case.z.shape[1])
        if competitor != winner
    ]
    radius, nearest = min(radii, key=lambda item: item[0])
    return scores, winner, int(nearest), float(radius)


def top_k_boundary(case: MatrixCase, k: int) -> tuple[float, int, int]:
    scores = case.w0 @ case.z
    order = np.argsort(scores, kind="stable")
    if k < 1 or k >= len(order):
        raise ValueError(f"Unsupported k={k} for {case.case_id}")
    if abs(float(scores[order[k - 1]] - scores[order[k]])) <= TIE_TOLERANCE:
        return 0.0, int(order[k - 1]), int(order[k])
    candidates: list[tuple[float, int, int]] = []
    for inside in order[:k]:
        for outside in order[k:]:
            result = pairwise_transport(case.z, int(inside), int(outside), case.w0)
            candidates.append((result.radius, int(inside), int(outside)))
    return min(candidates, key=lambda item: item[0])


def max_abs_aligned(actual: pd.DataFrame, expected: pd.DataFrame) -> float:
    if set(actual.index) != set(expected.index) or set(actual.columns) != set(expected.columns):
        return float("inf")
    aligned = actual.loc[expected.index, expected.columns]
    return float(np.max(np.abs(aligned.to_numpy(float) - expected.to_numpy(float))))


def reconstruct_tabarena(root: Path) -> dict[str, Any]:
    raw_path = root / "baseline_v041" / "data" / "raw" / "df_results.csv"
    raw = pd.read_csv(raw_path).drop(columns=["Unnamed: 0"], errors="ignore")
    selected = raw.loc[raw["method"].isin(TABARENA_METHODS)].copy()
    duplicated = int(selected.duplicated(["dataset", "fold", "method"], keep=False).sum())
    nonfinite = int((~np.isfinite(pd.to_numeric(selected["metric_error"], errors="coerce"))).sum())
    loss = (
        selected.groupby(["dataset", "method"], as_index=False)["metric_error"]
        .mean()
        .pivot(index="dataset", columns="method", values="metric_error")
        .reindex(index=sorted(selected["dataset"].unique()), columns=TABARENA_METHODS)
    )
    reconstructed = pd.DataFrame(
        rank_normalize(loss.to_numpy(float), higher_is_better=False),
        index=loss.index,
        columns=loss.columns,
    )
    archived = pd.read_csv(
        root / "data" / "processed" / "tabarena_primary14__rank__equal__normalized_matrix.csv",
        index_col=0,
    )
    diff = max_abs_aligned(reconstructed, archived)
    passed = loss.shape == (51, 14) and not loss.isna().any().any() and duplicated == 0 and nonfinite == 0 and diff <= AUDIT_TOLERANCE
    return {
        "case": "TabArena",
        "raw_path": str(raw_path.relative_to(root)).replace("\\", "/"),
        "raw_sha256": sha256(raw_path),
        "raw_rows": int(len(raw)),
        "admitted_shape_tasks_by_methods": "51x14",
        "duplicate_dataset_fold_method_rows": duplicated,
        "nonfinite_admitted_rows": nonfinite,
        "missing_admitted_cells": int(loss.isna().sum().sum()),
        "score_direction": "metric_error lower_is_better",
        "max_abs_matrix_difference": diff,
        "status": "PASS" if passed else "FAIL",
    }


def reconstruct_benchpress(root: Path) -> dict[str, Any]:
    base = root / "baseline_v041" / "data" / "raw"
    score_path = base / "benchpress_scores_paper.csv"
    benchmark_path = base / "benchpress_benchmarks.csv"
    scores = pd.read_csv(score_path)
    canonical = scores["matches_canonical"].astype(str).str.lower().eq("true")
    gate = scores.loc[scores["audit_status"].eq("verified") & canonical].copy()
    coverage = (
        gate.groupby("model_id")["benchmark_id"]
        .nunique()
        .rename("coverage")
        .reset_index()
        .sort_values(["coverage", "model_id"], ascending=[False, True], kind="stable")
    )
    methods = coverage.head(10)["model_id"].tolist()
    pivot = (
        gate.loc[gate["model_id"].isin(methods)]
        .pivot_table(index="benchmark_id", columns="model_id", values="score", aggfunc="first")
        .dropna(axis=0, how="any")
        .reindex(columns=methods)
    )
    reconstructed = pd.DataFrame(
        rank_normalize(pivot.to_numpy(float), higher_is_better=True),
        index=pivot.index,
        columns=pivot.columns,
    )
    archived = pd.read_csv(
        root / "data" / "processed" / "benchpress_primary10__rank__equal__normalized_matrix.csv",
        index_col=0,
    )
    diff = max_abs_aligned(reconstructed, archived)
    metadata = pd.read_csv(benchmark_path).set_index("benchmark_id")
    direction_failures = 0
    for benchmark in pivot.index:
        try:
            higher = bool(json.loads(metadata.loc[benchmark, "canonical_setting_json"]).get("higher_is_better", True))
        except Exception:
            higher = True
        direction_failures += int(not higher)
    duplicates = int(gate.duplicated(["model_id", "benchmark_id"], keep=False).sum())
    nonfinite = int((~np.isfinite(pd.to_numeric(gate["score"], errors="coerce"))).sum())
    passed = (
        pivot.shape == (11, 10)
        and not pivot.isna().any().any()
        and nonfinite == 0
        and direction_failures == 0
        and diff <= AUDIT_TOLERANCE
    )
    return {
        "case": "BenchPress",
        "raw_path": str(score_path.relative_to(root)).replace("\\", "/"),
        "raw_sha256": sha256(score_path),
        "raw_rows": int(len(scores)),
        "verified_canonical_rows": int(len(gate)),
        "admitted_shape_tasks_by_methods": "11x10",
        "duplicate_admitted_model_benchmark_rows": duplicates,
        "nonfinite_admitted_rows": nonfinite,
        "missing_admitted_cells": int(pivot.isna().sum().sum()),
        "score_direction_registry_failures": direction_failures,
        "score_direction": "raw score higher_is_better; rank loss lower_is_better",
        "max_abs_matrix_difference": diff,
        "status": "PASS" if passed else "FAIL",
    }


def reconstruct_beyondarena(root: Path) -> dict[str, Any]:
    lock = json.loads((root / "config" / "DESIGN_AND_SCOPE_LOCK.json").read_text(encoding="utf-8"))
    variants: dict[str, str] = lock["method_variant_selection"]
    primary_artifacts: list[str] = lock["scopes"]["primary_published_11"]
    methods = [variants[item] for item in primary_artifacts]
    core = pd.read_csv(root / "data" / "raw" / "BeyondArena_core_tasks.csv")
    core_pairs = set((str(dataset), int(split)) for dataset, split in core[["dataset", "split"]].itertuples(index=False, name=None))
    rows: list[pd.DataFrame] = []
    duplicate_rows = nonfinite_rows = imputed_rows = 0
    for artifact in primary_artifacts:
        path = root / "data" / "raw" / artifact / "hpo_results.parquet"
        frame = pd.read_parquet(path)
        selected_method = variants[artifact]
        frame = frame.loc[frame["method"].eq(selected_method)].copy()
        imputed_rows += int(frame["imputed"].fillna(False).sum())
        keep = [(str(dataset), int(fold)) in core_pairs for dataset, fold in zip(frame["dataset"], frame["fold"])]
        frame = frame.loc[keep].copy()
        duplicate_rows += int(frame.duplicated(["dataset", "fold", "method"], keep=False).sum())
        nonfinite_rows += int((~np.isfinite(pd.to_numeric(frame["metric_error"], errors="coerce"))).sum())
        aggregated = frame.groupby("dataset", as_index=False)["metric_error"].mean()
        aggregated["method"] = selected_method
        rows.append(aggregated)
    long = pd.concat(rows, ignore_index=True)
    loss = long.pivot(index="dataset", columns="method", values="metric_error").reindex(columns=methods)
    complete = loss.dropna(axis=0, how="any").copy()
    reconstructed_rank = pd.DataFrame(
        rank_normalize(complete.to_numpy(float), higher_is_better=False),
        index=complete.index,
        columns=complete.columns,
    )
    archived_loss = pd.read_csv(
        root / "data" / "processed" / "primary_published_11__complete_case_loss_matrix.csv",
        index_col=0,
    )
    archived_rank = pd.read_csv(
        root / "data" / "processed" / "primary11__all__rank__equal__normalized_matrix.csv",
        index_col=0,
    )
    loss_diff = max_abs_aligned(complete, archived_loss)
    rank_diff = max_abs_aligned(reconstructed_rank, archived_rank)
    registry = pd.read_csv(root / "data" / "processed" / "BEYONDARENA_SCORE_DIRECTION_REGISTRY.csv")
    direction_failures = int((registry["score_direction"] != "lower_is_better").sum()) + int((registry["source_column"] != "metric_error").sum())
    passed = (
        complete.shape == (122, 11)
        and imputed_rows == 0
        and duplicate_rows == 0
        and nonfinite_rows == 0
        and direction_failures == 0
        and loss_diff <= AUDIT_TOLERANCE
        and rank_diff <= AUDIT_TOLERANCE
    )
    return {
        "case": "BeyondArena",
        "raw_artifact_count": len(primary_artifacts),
        "core_task_split_rows": int(len(core)),
        "dataset_union_count": int(loss.shape[0]),
        "complete_case_dataset_count": int(complete.shape[0]),
        "excluded_incomplete_datasets": int(loss.shape[0] - complete.shape[0]),
        "admitted_shape_tasks_by_methods": "122x11",
        "imputed_selected_variant_rows": imputed_rows,
        "duplicate_dataset_fold_method_rows": duplicate_rows,
        "nonfinite_admitted_rows": nonfinite_rows,
        "score_direction_registry_failures": direction_failures,
        "score_direction": "metric_error lower_is_better",
        "max_abs_loss_matrix_difference": loss_diff,
        "max_abs_rank_matrix_difference": rank_diff,
        "status": "PASS" if passed else "FAIL",
    }


def expected_pairwise_rows(root: Path) -> list[dict[str, Any]]:
    rows = pd.read_csv(root / "results" / "ALL_PAIRWISE_CERTIFICATES_FINITE_AND_INFINITE.csv").to_dict("records")
    for filename, case_id in [
        ("tabarena_primary14__rank__equal__complete_pairwise_witness_coverage.csv", "tabarena_primary14__rank__equal"),
        ("benchpress_primary10__rank__equal__complete_pairwise_witness_coverage.csv", "benchpress_primary10__rank__equal"),
    ]:
        frame = pd.read_csv(root / "results" / filename)
        for row in frame.to_dict("records"):
            rows.append(
                {
                    "case_id": case_id,
                    "winner": row["winner"],
                    "competitor": row["competitor"],
                    "finite": row["finite"],
                    "radius_tv_primal_dual": row["radius_tv"],
                }
            )
    return rows


def audit_pairwise(root: Path) -> tuple[list[dict[str, Any]], bool]:
    cache: dict[str, MatrixCase] = {}
    output: list[dict[str, Any]] = []
    all_pass = True
    for expected in expected_pairwise_rows(root):
        case_id = str(expected["case_id"])
        case = cache.setdefault(case_id, read_case(root, case_id))
        winner = case.methods.index(str(expected["winner"]))
        competitor = case.methods.index(str(expected["competitor"]))
        observed = pairwise_transport(case.z, winner, competitor, case.w0).radius
        expected_finite = str(expected["finite"]).lower() == "true"
        observed_finite = math.isfinite(observed)
        expected_radius = float(expected["radius_tv_primal_dual"])
        difference = abs(observed - expected_radius) if expected_finite and observed_finite else 0.0 if expected_finite == observed_finite else float("inf")
        passed = expected_finite == observed_finite and difference <= AUDIT_TOLERANCE
        all_pass &= passed
        output.append(
            {
                "case_id": case_id,
                "winner": expected["winner"],
                "competitor": expected["competitor"],
                "expected_finite": expected_finite,
                "observed_finite": observed_finite,
                "expected_radius_tv": expected_radius,
                "observed_radius_tv": observed,
                "absolute_difference": difference,
                "status": "PASS" if passed else "FAIL",
            }
        )
    return output, all_pass


def audit_global_tabarena(root: Path) -> tuple[list[dict[str, Any]], bool]:
    case = read_case(root, "tabarena_primary14__rank__equal")
    expected = pd.read_csv(root / "results" / "TABARENA_GLOBAL_FEASIBLE_WINNER_ENTRY_RADII.csv")
    rows: list[dict[str, Any]] = []
    all_pass = True
    for record in expected.to_dict("records"):
        candidate_name = str(record["candidate_method"])
        candidate = case.methods.index(candidate_name)
        observed = global_entry_lp(case, candidate).radius
        expected_radius = float(record["global_feasible_winner_entry_radius_tv"])
        expected_finite = bool(record["globally_feasible"])
        observed_finite = math.isfinite(observed)
        difference = abs(observed - expected_radius) if expected_finite and observed_finite else 0.0 if expected_finite == observed_finite else float("inf")
        dominator = ""
        if not observed_finite:
            for competitor in range(case.z.shape[1]):
                if competitor != candidate and np.all(case.z[:, competitor] < case.z[:, candidate] - TIE_TOLERANCE):
                    dominator = case.methods[competitor]
                    break
        passed = expected_finite == observed_finite and difference <= AUDIT_TOLERANCE and (observed_finite or bool(dominator))
        all_pass &= passed
        rows.append(
            {
                "candidate": candidate_name,
                "expected_finite": expected_finite,
                "observed_finite": observed_finite,
                "expected_radius_tv": expected_radius,
                "observed_radius_tv": observed,
                "absolute_difference": difference,
                "strict_taskwise_dominator_if_infeasible": dominator,
                "status": "PASS" if passed else "FAIL",
            }
        )
    return rows, all_pass


def audit_primary(root: Path) -> tuple[list[dict[str, Any]], bool]:
    rows: list[dict[str, Any]] = []
    all_pass = True
    for label, expected in PRIMARY_EXPECTED.items():
        case = read_case(root, str(expected["case_id"]))
        _, winner, nearest, top1 = nominal_summary(case)
        top3, top3_inside, top3_outside = top_k_boundary(case, 3)
        top5, top5_inside, top5_outside = top_k_boundary(case, 5)
        checks = {
            "shape": tuple(case.z.shape) == tuple(expected["shape"]),
            "winner": case.methods[winner] == expected["winner"],
            "nearest": case.methods[nearest] == expected["nearest"],
            "top1": abs(top1 - float(expected["top1"])) <= AUDIT_TOLERANCE,
            "top3": abs(top3 - float(expected["top3"])) <= AUDIT_TOLERANCE,
            "top5": abs(top5 - float(expected["top5"])) <= AUDIT_TOLERANCE,
        }
        passed = all(checks.values())
        all_pass &= passed
        rows.append(
            {
                "case": label,
                "D_tasks": case.z.shape[0],
                "M_methods": case.z.shape[1],
                "winner": case.methods[winner],
                "nearest_challenger": case.methods[nearest],
                "top1_radius_tv": top1,
                "top3_radius_tv": top3,
                "top3_displaced_inside": case.methods[top3_inside],
                "top3_entering_outside": case.methods[top3_outside],
                "top5_radius_tv": top5,
                "top5_displaced_inside": case.methods[top5_inside],
                "top5_entering_outside": case.methods[top5_outside],
                "maximum_locked_value_difference": max(
                    abs(top1 - float(expected["top1"])),
                    abs(top3 - float(expected["top3"])),
                    abs(top5 - float(expected["top5"])),
                ),
                "status": "PASS" if passed else "FAIL",
            }
        )
    return rows, all_pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--matrix-only",
        action="store_true",
        help="Skip raw-source reconstruction and verify the released derived matrices/results only.",
    )
    args = parser.parse_args()
    root = args.archive_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    matrix_rows = [] if args.matrix_only else [
        reconstruct_tabarena(root),
        reconstruct_benchpress(root),
        reconstruct_beyondarena(root),
    ]
    primary_rows, primary_pass = audit_primary(root)
    pairwise_rows, pairwise_pass = audit_pairwise(root)
    global_rows, global_pass = audit_global_tabarena(root)
    matrix_pass = all(row["status"] == "PASS" for row in matrix_rows)

    write_csv(output_dir / "MATRIX_RECONSTRUCTION_AUDIT.csv", matrix_rows)
    write_csv(output_dir / "PRIMARY_RECOMPUTATION.csv", primary_rows)
    write_csv(output_dir / "PAIRWISE_RECOMPUTATION.csv", pairwise_rows)
    write_csv(output_dir / "GLOBAL_RECOMPUTATION.csv", global_rows)

    summary = {
        "status": "PASS" if matrix_pass and primary_pass and pairwise_pass and global_pass else "FAIL",
        "implementation": {
            "analysis_implementation_imported": False,
            "raw_matrix_reconstruction_requested": not args.matrix_only,
            "pairwise_method": "ordered mass transfer",
            "global_method": "independent scipy.optimize.linprog formulation",
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scipy": scipy.__version__,
            "audit_tolerance": AUDIT_TOLERANCE,
            "tie_tolerance": TIE_TOLERANCE,
        },
        "matrix_reconstruction": matrix_rows,
        "primary_cases_pass": sum(row["status"] == "PASS" for row in primary_rows),
        "primary_cases_total": len(primary_rows),
        "pairwise_pass": sum(row["status"] == "PASS" for row in pairwise_rows),
        "pairwise_total": len(pairwise_rows),
        "pairwise_finite": sum(bool(row["observed_finite"]) for row in pairwise_rows),
        "global_pass": sum(row["status"] == "PASS" for row in global_rows),
        "global_total": len(global_rows),
        "global_finite": sum(bool(row["observed_finite"]) for row in global_rows),
        "maximum_pairwise_absolute_difference": max(float(row["absolute_difference"]) for row in pairwise_rows),
        "maximum_global_absolute_difference": max(float(row["absolute_difference"]) for row in global_rows if math.isfinite(float(row["absolute_difference"]))),
        "locked_results_changed": False,
    }
    (output_dir / "INDEPENDENT_VERIFICATION_RESULTS.json").write_text(
        json.dumps(summary, indent=2, allow_nan=False), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, allow_nan=False))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
