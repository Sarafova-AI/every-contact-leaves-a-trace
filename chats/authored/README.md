# Author-written matched pairs

These 35 pairs are released **for audit and reproduction** — the matched segments the
analysis runs on, made inspectable. They are not offered as a representative sample of how
people talk to language models; they are the author-constructed evidence behind the
reported effect, published so the classification and the traces can be checked.

Each folder is one pair, named by its `pair_id` (matching
[`../../analysis/indicator_panel.csv`](../../analysis/indicator_panel.csv)) and topic:

```
<pair_id>_<topic>/
├── navigator.txt   # the Navigator-mode side
└── operator.txt    # the matched Operator-mode side
```

- **Navigator side** — the user turns were written by the author in a conversation with a
  GPT-3.5-family model. The stance is Navigator: specific, self-correcting, steering,
  deepening.
- **Operator side** — a synthetic control generated with the same GPT-3.5-family model on
  the same surface topic, matched on length. The stance is Operator: directive and
  self-contained, fulfilled as stated rather than deepened.

Both sides use `+User` / `+Assistant` role markers with blank lines between turns and LF
line endings — the exact text that was traced; the tracer is sensitive to the token
sequence, so the wrapping is held identical across both sides of every pair.

`P##` folders are primary-cohort pairs; `S##` folders are lower-confidence sensitivity-set
auxiliary windows. The public-dataset pairs are not here — they are referenced under
[`../public_reference/`](../public_reference/).
