# Matched-pair chats

Each pair is two conversation segments on the same surface topic, matched on length and
traced with identical settings. One side is a **Navigator-mode** segment (specific,
self-correcting, steering, deepening); the other is an **Operator-mode** segment
(directive and self-contained, fulfilled as stated rather than deepened). The only thing
that differs within a pair is the user's stance.

Per-pair indicators are in [`../analysis/indicator_panel.csv`](../analysis/indicator_panel.csv);
the `provenance` column there matches the split below.

## Two kinds of pair, handled differently

- **[`authored/`](authored/) — 35 author-written pairs, full text.** The Navigator side
  was written by the author in GPT-3.5-family sessions; the Operator side is a synthetic
  GPT-3.5-family control. Released for audit and reproduction.
- **[`public_reference/`](public_reference/) — 19 public-dataset pairs, referenced by ID,
  no text.** The Navigator side comes from WildChat or LMSYS-Chat-1M. Their text is **not**
  stored here; each pair is referenced by source identifiers, and a script reconstructs and
  verifies the exact segment from the original dataset.

## Why the public pairs are referenced, not re-hosted

WildChat and LMSYS-Chat-1M are released under their own terms. Rather than redistribute
their user text, the public-dataset segments are referenced by dataset + conversation ID
(plus a verification hash), keeping this repository low-risk and free of redistributed
user content while staying fully reproducible. WildChat is ODC-BY (attribution required);
LMSYS-Chat-1M is gated and does not permit re-hosting. See
[`public_reference/README.md`](public_reference/README.md).
