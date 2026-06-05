#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Petya Sarafova
"""Reproduce the cohort statistics and bootstrap outputs from indicator_panel.csv.

Reads the per-pair indicator table, restricts to a cohort, and reports — for the
activation-weighted mean layer (the pre-specified primary endpoint) and the
influence-weighted mean layer (confirming secondary) — the NAV>OP directional
count with a two-sided exact binomial sign test, the mean paired difference with
a 95% t confidence interval, a Wilcoxon signed-rank test, and a bias-corrected
and accelerated (BCa) bootstrap 95% CI for the mean.

Cohorts reported:
    primary cohort (the clean, high-confidence matched pairs)
    all traced (primary + the lower-confidence sensitivity set)
    author-written subset of the primary cohort (strict robustness check)

Run from this folder:
    python cohort_stats.py
It prints the tables and writes ../results/bootstrap_outputs.txt.
"""
from __future__ import annotations
import csv
from pathlib import Path
import numpy as np
import scipy
from scipy import stats

HERE = Path(__file__).resolve().parent
CSV = HERE / "indicator_panel.csv"
OUT = HERE.parent / "results" / "bootstrap_outputs.txt"
SEED = 20260603        # fixed RNG seed so the BCa intervals are reproducible
N_RESAMPLES = 20000

PRIMARY_INDICATORS = [
    ("act_mean_l7_diff", "activation-weighted mean layer (PRIMARY)"),
    ("inf_mean_l7_diff", "influence-weighted mean layer (confirming secondary)"),
]


def load():
    with open(CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def diffs(rows, col):
    vals = []
    for r in rows:
        try:
            vals.append(float(r[col]))
        except (ValueError, KeyError):
            continue
    return np.asarray(vals, float)


def stat_line(d):
    n = len(d)
    nav = int((d > 0).sum())
    op = int((d < 0).sum())
    sign_p = stats.binomtest(nav, nav + op, 0.5).pvalue
    m = d.mean()
    sd = d.std(ddof=1)
    sem = sd / np.sqrt(n)
    tc = stats.t.ppf(0.975, n - 1)
    rng = np.random.default_rng(SEED)
    bca = stats.bootstrap((d,), np.mean, confidence_level=0.95,
                          n_resamples=N_RESAMPLES, method="BCa",
                          random_state=rng).confidence_interval
    wilcoxon_p = stats.wilcoxon(d, alternative="two-sided").pvalue
    return (f"n={n:2d} | {nav}/{n} NAV>OP ({100*nav/n:.0f}%) | sign p={sign_p:.3g} "
            f"| mean {m:+.3f} (SD {sd:.3f}), 95% t-CI [{m-tc*sem:+.3f}, {m+tc*sem:+.3f}] "
            f"| BCa 95% CI [{bca.low:+.3f}, {bca.high:+.3f}] | Wilcoxon p={wilcoxon_p:.3g}")


def cohort(rows, name):
    out = [f"## {name}  (n={len(rows)})"]
    for col, label in PRIMARY_INDICATORS:
        out.append(f"  {label}")
        out.append(f"    {stat_line(diffs(rows, col))}")
    return "\n".join(out)


def main():
    rows = load()
    primary = [r for r in rows if r["cohort"] == "primary"]
    all_traced = rows
    authored_primary = [r for r in primary if r["provenance"].startswith("author-written")]

    blocks = [
        "Veil companion - cohort statistics and bootstrap outputs",
        "(activation-weighted mean layer is the pre-specified primary endpoint)",
        "",
        cohort(primary, "Primary cohort"),
        "",
        cohort(all_traced, "All traced pairs (primary + sensitivity)"),
        "",
        cohort(authored_primary, "Author-written subset of the primary cohort"),
        "",
        f"BCa bootstrap: {N_RESAMPLES} resamples, fixed seed {SEED}; "
        f"computed with scipy {scipy.__version__}, numpy {np.__version__}.",
    ]
    report = "\n".join(blocks)
    print(report)
    OUT.write_text(report + "\n", encoding="utf-8")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
