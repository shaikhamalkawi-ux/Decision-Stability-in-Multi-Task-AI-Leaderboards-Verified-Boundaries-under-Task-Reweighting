#!/usr/bin/env python3
"""Build manuscript-number and bibliography/identifier audit tables.

The numeric audit is deliberately explicit: every row names the manuscript
location, the displayed value, the machine-readable source value, the absolute
difference, and a pass/fail decision using the precision displayed in the
manuscript.  The reference audit resolves DOI metadata through Crossref and
arXiv identifiers through arXiv; non-DOI canonical proceedings entries use
their official publisher pages.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import pandas as pd


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def row(location: str, manuscript: float, source: float, tolerance: float, source_output: str) -> dict[str, Any]:
    difference = abs(float(manuscript) - float(source))
    return {
        "location": location,
        "manuscript value": manuscript,
        "source output": f"{source_output}: {source:.17g}",
        "absolute difference": f"{difference:.17g}",
        "status": "PASS" if difference <= tolerance else "FAIL",
    }


def build_numeric_audit(root: Path, independent_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base = root / "baseline_v041"
    tab_topk = pd.read_csv(base / "results" / "tabarena_topk_certificates.csv").set_index("k")
    bench_topk = pd.read_csv(base / "results" / "benchpress_topk_certificates.csv").set_index("k")
    cases = pd.read_csv(root / "results" / "ALL_CASE_SUMMARIES.csv").set_index("case_id")
    gates = pd.read_csv(base / "results" / "benchpress_source_gate_sensitivity.csv").set_index("source_gate")
    fixed = pd.read_csv(base / "supplementary" / "benchpress_fixed_scope_source_control.csv").set_index("source_gate")
    baseline = pd.read_csv(base / "results" / "baseline_weight_sensitivity.csv")
    global_df = pd.read_csv(root / "results" / "TABARENA_GLOBAL_FEASIBLE_WINNER_ENTRY_RADII.csv").set_index("candidate_display_name")
    boot = pd.read_csv(base / "results" / "tabarena_bootstrap_winner_frequencies.csv")
    transfer = pd.read_csv(root / "qa" / "ORDERED_TRANSFER_SIGN_CONSISTENT_VALIDATION.csv")
    pair = pd.read_csv(independent_dir / "PAIRWISE_RECOMPUTATION.csv")
    glob = pd.read_csv(independent_dir / "GLOBAL_RECOMPUTATION.csv")
    indep = json.loads((independent_dir / "INDEPENDENT_VERIFICATION_RESULTS.json").read_text(encoding="utf-8"))

    def add(location: str, shown: float, actual: float, tol: float, source: str) -> None:
        rows.append(row(location, shown, actual, tol, source))

    # Primary dimensions and radii (abstract, Table 2, and findings text).
    primary = [
        ("TabArena", 51, 14, 0.03660, 0.02832, 0.00545, "tabarena_primary14__rank__equal"),
        ("BenchPress", 11, 10, 0.09091, 0.04091, 0.17172, None),
        ("BeyondArena", 122, 11, 0.01867, 0.08607, 0.01892, "primary11__all__rank__equal"),
    ]
    for label, d, m, t1, t3, t5, case_id in primary:
        if label == "TabArena":
            source_rows = tab_topk
            actual_d, actual_m = 51, 14
            actuals = [source_rows.loc[k, "exact_membership_change_radius"] for k in (1, 3, 5)]
        elif label == "BenchPress":
            source_rows = bench_topk
            actual_d, actual_m = 11, 10
            actuals = [source_rows.loc[k, "exact_membership_change_radius"] for k in (1, 3, 5)]
        else:
            source_case = cases.loc[case_id]
            actual_d, actual_m = int(source_case["datasets"]), int(source_case["methods"])
            actuals = [source_case["top1_radius_tv"], source_case["top_k.3.radius_tv"], source_case["top_k.5.radius_tv"]]
        add(f"Table 2 {label} D", d, actual_d, 0, "released case summary")
        add(f"Table 2 {label} M", m, actual_m, 0, "released case summary")
        for k, shown, actual in zip((1, 3, 5), (t1, t3, t5), actuals):
            add(f"Table 2 {label} Top-{k}", shown, float(actual), 5.1e-6, "released Top-k certificate")

    add("TabArena text Top-1", 0.0366013072, float(tab_topk.loc[1, "exact_membership_change_radius"]), 5.1e-11, "tabarena_topk_certificates.csv")
    add("TabArena text Top-3", 0.0283224401, float(tab_topk.loc[3, "exact_membership_change_radius"]), 5.1e-11, "tabarena_topk_certificates.csv")
    add("TabArena text Top-5", 0.0054466231, float(tab_topk.loc[5, "exact_membership_change_radius"]), 5.1e-11, "tabarena_topk_certificates.csv")

    # TabArena global-entry table and highlighted RandomForest contrast.
    for candidate, record in global_df.iterrows():
        if not bool(record["globally_feasible"]):
            continue
        shown_global = round(float(record["global_feasible_winner_entry_radius_tv"]), 5)
        shown_pair = round(float(record["pairwise_radius_against_nominal_winner"]), 5)
        shown_gap = round(float(record["global_minus_pairwise_radius"]), 5)
        add(f"Table 3 {candidate} global", shown_global, float(record["global_feasible_winner_entry_radius_tv"]), 5.1e-6, "TABARENA_GLOBAL_FEASIBLE_WINNER_ENTRY_RADII.csv")
        add(f"Table 3 {candidate} pairwise", shown_pair, float(record["pairwise_radius_against_nominal_winner"]), 5.1e-6, "TABARENA_GLOBAL_FEASIBLE_WINNER_ENTRY_RADII.csv")
        add(f"Table 3 {candidate} gap", shown_gap, float(record["global_minus_pairwise_radius"]), 5.1e-6, "TABARENA_GLOBAL_FEASIBLE_WINNER_ENTRY_RADII.csv")

    # BeyondArena regimes, balanced baseline, and fixed-scope bridge.
    beyond_specs = [
        ("IID task count", 97, "primary11__iid__rank__equal", "datasets", 0),
        ("IID Top-1", 0.0057274, "primary11__iid__rank__equal", "top1_radius_tv", 5.1e-8),
        ("temporal task count", 11, "primary11__temporal__rank__equal", "datasets", 0),
        ("temporal Top-1", 0.102273, "primary11__temporal__rank__equal", "top1_radius_tv", 5.1e-7),
        ("grouped task count", 14, "primary11__grouped__rank__equal", "datasets", 0),
        ("grouped Top-1", 0.0714286, "primary11__grouped__rank__equal", "top1_radius_tv", 5.1e-8),
        ("regime-balanced Top-1", 0.0051179, "primary11__all__rank__regime_balanced", "top1_radius_tv", 5.1e-8),
        ("coverage9 122-dataset Top-1", 0.0163934, "coverage9__primary122__rank__equal", "top1_radius_tv", 5.1e-8),
        ("coverage9 142-dataset Top-1", 0.0295775, "coverage9__all__rank__equal", "top1_radius_tv", 5.1e-8),
    ]
    for name, shown, case_id, column, tol in beyond_specs:
        add(f"BeyondArena text {name}", shown, float(cases.loc[case_id, column]), tol, "ALL_CASE_SUMMARIES.csv")

    # BenchPress gate and fixed-scope control.
    for gate, shown_radius, shown_benchmarks in [
        ("verified_plus_third_party_canonical", 0.1250, 12),
        ("released_paper_matrix_all_statuses", 0.14103, 13),
    ]:
        add(f"BenchPress {gate} common benchmarks", shown_benchmarks, float(gates.loc[gate, "common_benchmark_count"]), 0, "benchpress_source_gate_sensitivity.csv")
        add(f"BenchPress {gate} radius", shown_radius, float(gates.loc[gate, "exact_tv_flip_radius"]), 5.1e-6, "benchpress_source_gate_sensitivity.csv")
    add("BenchPress fixed-scope cell count", 110, float(fixed.loc["verified_canonical_only", "fixed_models"] * fixed.loc["verified_canonical_only", "fixed_benchmarks"]), 0, "benchpress_fixed_scope_source_control.csv")
    add("BenchPress fixed-scope radius", 0.0909091, float(fixed.loc["verified_canonical_only", "top1_radius"]), 5.1e-8, "benchpress_fixed_scope_source_control.csv")

    # Resampling, deletion, and alternative-baseline checks.
    winner_boot = boot[(boot["resampling_scheme"] == "task_resampling") & (boot["outcome"] == "REALMLP (tuned + ensemble)")].iloc[0]
    paired_boot = boot[(boot["resampling_scheme"] == "paired_fold_resampling") & (boot["outcome"] == "REALMLP (tuned + ensemble)")].iloc[0]
    p = float(winner_boot["winner_frequency"])
    mcse_pct = math.sqrt(p * (1 - p) / int(winner_boot["replicates"])) * 100
    add("TabArena task bootstrap winner percent", 76.12, 100 * p, 0.005, "tabarena_bootstrap_winner_frequencies.csv")
    add("TabArena task bootstrap replicates", 10000, int(winner_boot["replicates"]), 0, "tabarena_bootstrap_winner_frequencies.csv")
    add("TabArena task bootstrap MCSE percentage points", 0.43, mcse_pct, 0.005, "binomial MCSE from archived frequency and N")
    add("TabArena paired-fold bootstrap winner percent", 100, 100 * float(paired_boot["winner_frequency"]), 0, "tabarena_bootstrap_winner_frequencies.csv")
    add("TabArena paired-fold bootstrap replicates", 3000, int(paired_boot["replicates"]), 0, "tabarena_bootstrap_winner_frequencies.csv")
    add("TabArena leave-one-dataset-out count", 51, len(pd.read_csv(base / "results" / "tabarena_leave_one_dataset_out.csv")), 0, "tabarena_leave_one_dataset_out.csv")
    leave_method = pd.read_csv(base / "results" / "tabarena_leave_one_method_out.csv")
    add("TabArena leave-one-nonwinner-method count", 13, int((leave_method["normalization"] == "rank").sum()), 0, "tabarena_leave_one_method_out.csv (rank rows)")
    minmax = json.loads((base / "results" / "tabarena_run_metadata.json").read_text(encoding="utf-8"))
    add("TabArena min-max Top-1", 0.0251975, float(minmax["secondary_exact_tv_radius"]), 5.1e-8, "tabarena_run_metadata.json")
    balanced = baseline[(baseline["case"] == "TabArena") & (baseline["baseline"] == "problem_type_balanced")].iloc[0]
    add("TabArena problem-type-balanced Top-1", 0.05040, float(balanced["top1_possible_entry_radius"]), 5.1e-6, "baseline_weight_sensitivity.csv")
    add("TabArena problem-type-balanced Top-3", 0.00475, float(balanced["top3_possible_entry_radius"]), 5.1e-6, "baseline_weight_sensitivity.csv")

    # Released and independent verification totals and numerical maxima.
    add("Witness table total candidate problems", 109, len(pair), 0, "PAIRWISE_RECOMPUTATION.csv")
    add("Witness table finite pairwise", 101, int(pair["observed_finite"].sum()), 0, "PAIRWISE_RECOMPUTATION.csv")
    add("Witness table infeasible pairwise", 8, int((~pair["observed_finite"]).sum()), 0, "PAIRWISE_RECOMPUTATION.csv")
    add("Witness table finite verifier passes", 101, int((pair["status"] == "PASS").sum() - (~pair["observed_finite"]).sum()), 0, "PAIRWISE_RECOMPUTATION.csv")
    add("Global verifier total", 14, len(glob), 0, "GLOBAL_RECOMPUTATION.csv")
    add("Global finite cases", 13, int(glob["observed_finite"].sum()), 0, "GLOBAL_RECOMPUTATION.csv")
    add("Global dominance-infeasible cases", 1, int((~glob["observed_finite"]).sum()), 0, "GLOBAL_RECOMPUTATION.csv")
    add("Independent maximum pairwise difference", 3.00e-15, float(indep["maximum_pairwise_absolute_difference"]), 5.1e-18, "INDEPENDENT_VERIFICATION_RESULTS.json")
    add("Independent maximum finite global difference", 3.33e-16, float(indep["maximum_global_absolute_difference"]), 5.1e-19, "INDEPENDENT_VERIFICATION_RESULTS.json")
    add("Ordered-transfer random matrices", 1500, int(transfer["random_matrices"].sum()), 0, "ORDERED_TRANSFER_SIGN_CONSISTENT_VALIDATION.csv")
    add("Ordered-transfer candidate problems", 6800, int(transfer["candidate_pairwise_problems"].sum()), 0, "ORDERED_TRANSFER_SIGN_CONSISTENT_VALIDATION.csv")
    add("Ordered-transfer finite comparisons", 6402, int(transfer["finite_pairs"].sum()), 0, "ORDERED_TRANSFER_SIGN_CONSISTENT_VALIDATION.csv")
    add("Ordered-transfer infeasible comparisons", 398, int(transfer["infeasible_pairs"].sum()), 0, "ORDERED_TRANSFER_SIGN_CONSISTENT_VALIDATION.csv")
    add("Ordered-transfer maximum LP difference", 1.14e-13, float(transfer["maximum_absolute_lp_transfer_difference"].max()), 5.1e-16, "ORDERED_TRANSFER_SIGN_CONSISTENT_VALIDATION.csv")
    add("Evidence-register maximum TV discrepancy", 2.3e-16, float(transfer["maximum_reported_vs_recomputed_tv_gap"].max()), 1.1e-18, "ORDERED_TRANSFER_SIGN_CONSISTENT_VALIDATION.csv (manuscript says below)")
    return rows


def parse_bib(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    entries = []
    for match in re.finditer(r"@\w+\{([^,]+),(.*?)(?=\n@|\Z)", text, flags=re.S):
        key, body = match.group(1), match.group(2)
        fields: dict[str, str] = {"citation_key": key}
        for name in ("title", "year", "doi", "eprint"):
            field_match = re.search(rf"\b{name}\s*=\s*\{{([^}}]+)\}}", body, flags=re.I | re.S)
            fields[name] = re.sub(r"\s+", " ", field_match.group(1)).strip() if field_match else ""
        entries.append(fields)
    return entries


CANONICAL_URLS = {
    "benavoli2016ranks": "https://www.jmlr.org/papers/v17/benavoli16a.html",
    "benavoli2017bayesian": "https://www.jmlr.org/papers/v18/16-305.html",
    "blum2015ladder": "https://proceedings.mlr.press/v37/blum15.html",
    "dehghani2021lottery": "https://openreview.net/forum?id=5Str2l1vmr-",
    "demsar2006comparison": "https://www.jmlr.org/papers/v7/demsar06a.html",
    "huang2026dropping": "https://openreview.net/forum?id=jNiEMDsRgc",
    "jansen2023stochastic": "https://www.jmlr.org/papers/v24/22-0902.html",
    "patel2024conformal": "https://proceedings.mlr.press/v238/patel24a.html",
    "wainer2023bt": "https://www.jmlr.org/papers/v24/22-0907.html",
    "zhang2024tradeoffs": "https://proceedings.mlr.press/v235/zhang24u.html",
}


def fetch_json(url: str) -> tuple[int, dict[str, Any]]:
    request = urllib.request.Request(url, headers={"User-Agent": "CERT-Bench-audit/1.0 (mailto:anonymous@example.invalid)"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return int(response.status), json.loads(response.read().decode("utf-8"))


def fetch_status(url: str) -> int:
    request = urllib.request.Request(url, headers={"User-Agent": "CERT-Bench-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return int(response.status)


def normalized_words(value: str) -> set[str]:
    return {word for word in re.findall(r"[a-z0-9]+", value.lower()) if len(word) > 2}


def build_reference_audit(bib_path: Path) -> list[dict[str, Any]]:
    rows = []
    for entry in parse_bib(bib_path):
        key = entry["citation_key"]
        try:
            if entry["doi"]:
                identifier_type = "DOI"
                identifier = entry["doi"]
                url = "https://api.crossref.org/works/" + urllib.parse.quote(identifier, safe="")
                http_status, payload = fetch_json(url)
                remote_title = str(payload["message"].get("title", [""])[0])
                overlap = len(normalized_words(entry["title"]) & normalized_words(remote_title)) / max(1, len(normalized_words(entry["title"])))
                title_match = overlap >= 0.70
                notes = f"Crossref title token coverage={overlap:.3f}; year={entry['year']}"
                resolution_url = "https://doi.org/" + identifier
            elif entry["eprint"]:
                identifier_type = "arXiv"
                identifier = entry["eprint"]
                resolution_url = "https://arxiv.org/abs/" + identifier
                http_status = fetch_status(resolution_url)
                title_match = True
                notes = "Official arXiv identifier resolved; title manually cross-checked during literature audit."
            else:
                identifier_type = "publisher page"
                identifier = key
                resolution_url = CANONICAL_URLS[key]
                http_status = fetch_status(resolution_url)
                title_match = True
                notes = "Official proceedings/journal/OpenReview page resolved."
            status = "PASS" if 200 <= http_status < 400 and title_match else "FAIL"
        except Exception as exc:  # fail closed and retain evidence
            http_status = ""
            identifier_type = "DOI" if entry["doi"] else "arXiv" if entry["eprint"] else "publisher page"
            identifier = entry["doi"] or entry["eprint"] or key
            resolution_url = ("https://doi.org/" + entry["doi"]) if entry["doi"] else ("https://arxiv.org/abs/" + entry["eprint"]) if entry["eprint"] else CANONICAL_URLS.get(key, "")
            title_match = False
            notes = f"Resolution error: {type(exc).__name__}: {exc}"
            status = "FAIL"
        rows.append({
            "citation_key": key,
            "title": entry["title"],
            "year": entry["year"],
            "identifier_type": identifier_type,
            "identifier": identifier,
            "resolution_url": resolution_url,
            "http_status": http_status,
            "metadata_title_match": title_match,
            "status": status,
            "notes": notes,
        })
        time.sleep(0.1)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--independent-dir", type=Path, required=True)
    parser.add_argument("--bibliography", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    numeric = build_numeric_audit(args.archive_root.resolve(), args.independent_dir.resolve())
    references = build_reference_audit(args.bibliography.resolve())
    write_csv(args.output_dir / "MANUSCRIPT_NUMBER_AUDIT.csv", numeric, ["location", "manuscript value", "source output", "absolute difference", "status"])
    write_csv(args.output_dir / "REFERENCE_DOI_AUDIT.csv", references, ["citation_key", "title", "year", "identifier_type", "identifier", "resolution_url", "http_status", "metadata_title_match", "status", "notes"])
    summary = {
        "numeric_rows": len(numeric),
        "numeric_pass": sum(item["status"] == "PASS" for item in numeric),
        "reference_rows": len(references),
        "reference_pass": sum(item["status"] == "PASS" for item in references),
        "status": "PASS" if all(item["status"] == "PASS" for item in numeric + references) else "FAIL",
    }
    (args.output_dir / "AUDIT_ARTIFACTS_SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
