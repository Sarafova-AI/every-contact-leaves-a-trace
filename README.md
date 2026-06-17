# Companion materials — *Every Contact Leaves a Trace*

Supplementary materials for the preprint *Every Contact Leaves a Trace* (subtitle:
*Navigator- versus Operator-style interaction leaves a measurable attribution-graph
signature*).

**Author:** Petya Sarafova, independent researcher.
**Paper:** https://theveil.dev — Preprint v1, June 2026 (arXiv link to follow)

**Revision note:** On 2026-06-17 the live preprint PDF at `theveil.dev` was refreshed
to clarify the blind-rating language: completed blind model-rater checks on the final
author-created batches are distinguished from independent human blind classification
across the full cohort as potential future work. No cohort statistics, chat files, or
analysis artifacts changed.

The study traces matched pairs of conversation segments that differ only in the user's
engagement style — Navigator-mode (specific, self-correcting, steering, deepening) versus
Operator-mode (directive and self-contained) — and measures where the resulting
computation sits inside a language model, using circuit tracing on `google/gemma-2-2b`
with GemmaScope transcoders. The pre-specified primary finding: the activation-weighted
mean layer sits later for Navigator-mode segments.

## What's inside

- **`rating-instrument/`** — the segment-level Navigator/Operator instrument: the ten
  markers, the scoring rule, and the confidence labels used to classify segments from the
  text.
- **`analysis/`**
  - `compute_indicators.py` — computes the L7+ attribution-graph indicators for a matched
    pair from the two graph JSONs circuit-tracer produces.
  - `cohort_stats.py` — reads the indicator table and reproduces the cohort-level
    statistics and bootstrap outputs (sign test, t confidence interval, Wilcoxon, BCa
    bootstrap).
  - `indicator_panel.csv` — the per-pair indicator table for every traced pair, with
    cohort and provenance labels.
- **`results/`** — `bootstrap_outputs.txt`, the regenerated cohort statistics and BCa
  bootstrap intervals.
- **`robustness/`** — outputs of the 2026-06-10 independent robustness pass: full
  recomputation of the cohort statistics from the raw indicator table, the layer-cutoff
  exclusion sweep, the feature-nodes-only composition check, the token-match audit, and
  full-precision values for the graph-morphology deltas. See `robustness/README.md`.
- **`chats/`** — the matched-pair conversation segments. `chats/authored/` holds the 35
  author-written pairs as full text (released for audit and reproduction);
  `chats/public_reference/` references the 19 public-dataset pairs (WildChat, LMSYS) by
  source ID with a reconstruction script, rather than re-hosting their text. See
  `chats/README.md`.

## Reproducing the headline numbers

The statistics in the paper are reproducible from the indicator table:

```
cd analysis
python cohort_stats.py
```

This reads `indicator_panel.csv`, restricts to the primary cohort, and reports the
activation-weighted mean layer (the pre-specified primary endpoint) and the
influence-weighted mean layer, writing the full output to `../results/bootstrap_outputs.txt`.
Requires Python with `numpy` and `scipy`.

`compute_indicators.py` shows how each per-pair indicator row is derived from a pair of
attribution-graph JSONs; it reads finished graphs and does not run the trace itself. The
trace model, tooling, and thresholds are described in the paper's Methods.

## How the indicators are computed

Indicators are measured over the **L7+ interior** of each attribution graph: embedding
nodes, logit nodes, and L0–L6 nodes are dropped, so a difference reflects where
attribution mass sits across the computational interior rather than input or read-out
bookkeeping. The two centering indicators are the activation-weighted and
influence-weighted mean layer; the rest are late-layer influence shares, error-reliance
ratios, and graph-morphology descriptors. The same routine is applied to every graph with
no per-pair tuning.

## Tooling

- Model: `google/gemma-2-2b`
- Transcoders: GemmaScope (`mwhanna/gemma-scope-transcoders`)
- Circuit tracing: `circuit-tracer`

## License

- Code under `analysis/` — MIT (`LICENSE`).
- Instrument, indicator table, results, docs, and author-written chats — CC BY 4.0
  (`LICENSE-CONTENT.md`).
- Public-corpus source texts (WildChat, LMSYS) are **not** relicensed here; they are
  referenced by source ID and remain under their original dataset licenses and terms.
