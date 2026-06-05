# Public-dataset pairs — referenced, not re-hosted

The Navigator side of these pairs comes from public conversation datasets (WildChat,
LMSYS-Chat-1M). Their **text is not stored in this repository.** Instead each pair is
referenced by source identifiers, and `extract_segments.py` reconstructs the exact traced
segment from the original dataset and verifies it against a recorded hash. This keeps the
repository low-risk and free of redistributed user text while remaining reproducible.

The Operator side of each of these pairs is a synthetic GPT-3.5-family control (the
author's own); it is described here rather than re-hosted, for uniformity with the
referenced Navigator side.

## `public_pairs.csv`

| column | meaning |
|---|---|
| `pair_id` | matches the row in `../../analysis/indicator_panel.csv` |
| `cohort` | primary / sensitivity |
| `source_dataset` | WildChat or LMSYS |
| `dataset_id` | Hugging Face dataset (`allenai/WildChat-4.8M`, `lmsys/lmsys-chat-1m`) |
| `conversation_id` | the source conversation identifier |
| `turn_window` | 1-indexed inclusive turn range used for the Navigator segment |
| `language` | segment language |
| `navigator_segment_sha256` | SHA-256 of the traced Navigator segment, for verification |
| `operator_side` | the matched Operator control (synthetic GPT-3.5-family) |
| `topic` | short subject label |
| `source_note` | per-pair provenance notes (see below) |

## Reproducing the segments

```
pip install datasets
python extract_segments.py            # verify against the recorded hashes
python extract_segments.py --write out/   # also write the reconstructed text
```

- **WildChat** (`allenai/WildChat-4.8M`) is openly downloadable under ODC-BY 1.0. Using
  these segments requires following ODC-BY, including attribution to the WildChat authors
  (Zhao et al., *WildChat*, arXiv:2405.01470).
- **LMSYS-Chat-1M** (`lmsys/lmsys-chat-1m`) is gated: accept the dataset agreement on
  Hugging Face and authenticate (`huggingface-cli login`) before running. The agreement
  does not permit re-hosting the dataset, which is why these segments are referenced here
  rather than included.

## Turn-window conventions

The `turn_window` is 1-indexed inclusive, but two source families recorded windows
differently, so read it accordingly:
- 8-pair and pilot segments: exchange-turn windows over the conversation.
- The four `S0x` segments: the source `window_id` records an original-conversation message
  range; `turn_window` reproduces that range.

The `navigator_segment_sha256` is the SHA-256 of the exact traced segment and is the
authoritative anchor — `extract_segments.py` checks reconstruction against it regardless of
indexing convention.

## Provenance notes

- **Pilot and earliest-showcase pairs** (P25, P29, P30, P32–P35): the `conversation_hash`
  originates in the original WildChat extract; the same conversation is in WildChat-4.8M.
- **P26 and S02 are the same source conversation** (different windows) — one WW2/wartime
  animation conversation appears as a primary-cohort pair and, at a different window, in the
  sensitivity set.
- **S17 (`hibernate mappedsuperclass`):** the source-of-record is WildChat (row 417460). The
  project's indicator table labels this pair LMSYS; that label is being reconciled. The text
  itself is WildChat, so it is referenced here as WildChat.
- **LMSYS pairs** (S14–S16): source model vicuna-13b; `language` is inferred from content
  (the dataset packet does not store a language field).
