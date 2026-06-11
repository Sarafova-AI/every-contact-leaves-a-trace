# Robustness review outputs (2026-06-10)

Outputs of an independent robustness pass over Preprint v1, run 2026-06-10 against the full local trace archive. Each check re-derives a claim in the paper from the raw artifacts rather than from the paper's own tables. Outputs are published exactly as produced. The generating scripts run against the local attribution-graph archive (paths outside this repository) and are not included here; they are available on request.

| Files | What the check does |
|---|---|
| `recompute_output.txt`, `recompute_results.json` | Independent re-derivation of all cohort-level statistics from the raw per-pair indicator table: row counts (35 primary, 19 sensitivity, 1 excluded), the primary endpoint (31/35, +0.554, sign p = 3.5×10⁻⁶), and the secondary indicators. |
| `exclusion_sweep_output.txt`, `exclusion_sweep_results.csv` | Layer-cutoff sweep over the graph JSONs: recomputes the primary indicator at every interior exclusion boundary, testing the claim that the direction holds at every cutoff from L5 up. |
| `feature_only_check_output.txt`, `feature_only_check.csv` | Composition-artifact check: the primary indicator over transcoder feature nodes only (31/35, +0.5535, sign p = 3.47×10⁻⁶), confirming the shift is not produced by error-node bookkeeping. |
| `matching_stats_clean_output.txt`, `matching_stats_clean.csv` | Token-match audit for all 54 pairs: per-pair relative token gaps (max |gap| 14.91%, no pair above the ±15% matching criterion) and the correlation between token gap and the primary effect (ρ = +0.113, p = 0.519). |
| `token_confound_output.txt`, `token_confound_joined.csv` | Token-count confound table across traced Navigator/Operator pairs joined from the graph metadata. |
| `edges_fullprec_output.txt` | Full-precision values for the graph-morphology deltas reported rounded in the paper (edges per node −19.956; feature ratio −0.0529). |
