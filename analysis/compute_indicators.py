#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Petya Sarafova
"""Compute the L7+ attribution-graph indicator panel for a matched pair.

Point this at the two attribution-graph JSON files that circuit-tracer produces
for a pair — one Navigator side, one Operator side — and it returns the same
indicators reported in the paper, computed over the L7+ interior of each graph
(embedding nodes, logit nodes, and L0-L6 nodes are dropped so the measurement
reflects where attribution mass sits in the computational interior, not input or
read-out bookkeeping).

The two centering indicators are the activation-weighted and influence-weighted
mean layer; the rest are late-layer influence shares, error-reliance ratios, and
graph-morphology descriptors. The same routine is applied to every graph with no
per-pair tuning — the only thing that differs between pairs is the traced input.

This script reads finished graph JSONs; it does not run the trace itself. The
model and tooling (google/gemma-2-2b, GemmaScope transcoders, circuit-tracer) and
the canonical trace thresholds are described in the paper's Methods.

Usage:
    python compute_indicators.py NAV_graph.json OP_graph.json
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path


def comp_nodes(d):
    """Real computational nodes, dropping embedding and logit (non-layer) nodes."""
    out = []
    for n in d.get("nodes", []):
        ft = (n.get("feature_type") or "").lower()
        ls = str(n.get("layer", ""))
        if ls in ("", "E", "L") or ft in ("embedding", "logit"):
            continue
        try:
            layer = int(ls)
        except ValueError:
            continue
        out.append({"id": n.get("node_id"), "layer": layer,
                    "act": abs(n.get("activation", 0) or 0),
                    "inf": abs(n.get("influence", 0) or 0),
                    "trans": "transcoder" in ft, "err": "error" in ft})
    return out


def wmean(items, key):
    """Weighted mean layer; falls back to the unweighted mean if all weights are 0."""
    tot = sum(i[key] for i in items)
    if tot > 0:
        return sum(i["layer"] * i[key] for i in items) / tot
    return sum(i["layer"] for i in items) / len(items) if items else 0.0


def analyze(path):
    """Return the full L7+ indicator dict for one attribution-graph JSON."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    comp = comp_nodes(d)
    l7 = [c for c in comp if c["layer"] >= 7]
    ids7 = {c["id"] for c in l7}
    ti = sum(c["inf"] for c in l7)
    n_tr = sum(1 for c in l7 if c["trans"])
    n_er = sum(1 for c in l7 if c["err"])
    inf_mean = wmean(l7, "inf")
    inf_std = math.sqrt(sum(c["inf"] * (c["layer"] - inf_mean) ** 2 for c in l7) / ti) if ti else 0.0
    ent = 0.0
    if ti:
        for c in l7:
            p = c["inf"] / ti
            if p > 0:
                ent -= p * math.log(p)
    npos = nneg = 0
    absw = []
    for lk in d.get("links", []):
        if lk.get("source") in ids7 and lk.get("target") in ids7:
            w = lk.get("weight", 0) or 0
            absw.append(abs(w))
            if w > 0:
                npos += 1
            elif w < 0:
                nneg += 1
    layers7 = {c["layer"] for c in l7}
    return {
        "act_mean_l7": round(wmean(l7, "act"), 4),
        "inf_mean_l7": round(inf_mean, 4),
        "l20_25_inf_share": round(sum(c["inf"] for c in l7 if 20 <= c["layer"] <= 25) / ti, 4) if ti else 0.0,
        "l15_25_inf_share": round(sum(c["inf"] for c in l7 if 15 <= c["layer"] <= 25) / ti, 4) if ti else 0.0,
        "feature_ratio_l7": round(n_tr / len(l7), 4) if l7 else 0.0,
        "err_ratio_inf_l7": round(sum(c["inf"] for c in l7 if c["err"]) / ti, 4) if ti else 0.0,
        "err_ratio_count_l7": round(n_er / (n_er + n_tr), 4) if (n_er + n_tr) else 0.0,
        "edge_posneg_l7": round(npos / nneg, 4) if nneg else float("inf"),
        "edge_absmean_l7": round(sum(absw) / len(absw), 6) if absw else 0.0,
        "inf_layer_std": round(inf_std, 4),
        "inf_entropy": round(ent, 4),
        "edges_per_node_l7": round(len(absw) / len(l7), 4) if l7 else 0.0,
        "mid_continuity_l7_18": round(len([L for L in range(7, 19) if L in layers7]) / 12.0, 4),
        "l7_nodes": len(l7), "l7_edges": len(absw),
    }


# label, weighting/meaning, family, reporting tier (as in the paper's hierarchy)
INDICATORS = [
    ("act_mean_l7", "activation mean-layer", "depth", "primary"),
    ("inf_mean_l7", "influence mean-layer", "depth", "secondary"),
    ("l20_25_inf_share", "late-layer share L20-25", "depth-late", "support"),
    ("l15_25_inf_share", "late-layer share L15-25", "depth-late", "support"),
    ("mid_continuity_l7_18", "mid continuity L7-18", "depth-shape", "descriptive"),
    ("inf_layer_std", "influence layer spread", "spread", "descriptive"),
    ("inf_entropy", "influence entropy", "spread", "descriptive"),
    ("feature_ratio_l7", "feature ratio", "size/shape", "descriptive"),
    ("edges_per_node_l7", "edges per node", "density", "descriptive"),
    ("edge_posneg_l7", "edge pos:neg", "shape", "descriptive"),
    ("edge_absmean_l7", "edge |w| mean", "shape", "descriptive"),
    ("err_ratio_inf_l7", "error ratio (influence)", "incidental", "incidental"),
    ("err_ratio_count_l7", "error ratio (count)", "incidental", "incidental"),
]


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 1
    nav, op = analyze(argv[1]), analyze(argv[2])
    print(f"{'indicator':26s} {'NAV':>12s} {'OP':>12s} {'NAV-OP diff':>14s}")
    for key, label, _, _ in INDICATORS:
        nv, ov = nav[key], op[key]
        diff = (nv - ov) if (math.isfinite(nv) and math.isfinite(ov)) else float("nan")
        print(f"{label:26s} {nv:12.4f} {ov:12.4f} {diff:+14.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
