#!/usr/bin/env python3
"""Reconstruct the public-dataset Navigator segments referenced in public_pairs.csv.

The Navigator side of the public-dataset pairs is NOT re-hosted here. This script
rebuilds each referenced segment directly from its source dataset, so the exact text
that was traced can be reproduced and verified without this repository redistributing
the dataset's user text.

For each row in public_pairs.csv it:
  1. loads the source conversation from its dataset by conversation_id,
  2. slices the recorded turn window,
  3. renders it in the traced format (`+User` / `+Assistant`, blank-line separated, LF),
  4. computes the SHA-256 and checks it against navigator_segment_sha256.

Datasets and their terms:
  - WildChat (allenai/WildChat-4.8M) — ODC-BY 1.0; openly downloadable.
  - LMSYS-Chat-1M (lmsys/lmsys-chat-1m) — gated; you must accept the dataset
    agreement on Hugging Face and authenticate (`huggingface-cli login`) first.

Usage:
    python extract_segments.py                 # verify all rows that have IDs filled
    python extract_segments.py --write OUTDIR   # also write the reconstructed .txt files

Requires `datasets` (pip install datasets).
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = HERE / "public_pairs.csv"


def render(turns) -> str:
    """Render a list of {role, content} turns in the traced wrapping."""
    blocks = []
    for t in turns:
        role = "+User" if t["role"] in ("user", "human") else "+Assistant"
        blocks.append(f"{role}\n{t['content'].strip()}")
    return "\n\n\n\n".join(blocks) + "\n"


def load_conversation(dataset_id: str, conversation_id: str):
    """Return the list of turns for one conversation. Adapt field names per dataset."""
    from datasets import load_dataset
    ds = load_dataset(dataset_id, split="train", streaming=True)
    key = "conversation_hash" if "WildChat" in dataset_id else "conversation_id"
    for row in ds:
        if str(row.get(key)) == str(conversation_id):
            convo = row.get("conversation") or row.get("conversations") or []
            return [{"role": t.get("role") or t.get("from"),
                     "content": t.get("content") or t.get("value")} for t in convo]
    raise LookupError(f"{conversation_id} not found in {dataset_id}")


def parse_window(turn_window: str):
    """'1-4' -> (1, 4), 1-indexed inclusive."""
    a, b = turn_window.split("-")
    return int(a), int(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", metavar="OUTDIR", default=None,
                    help="write reconstructed navigator.txt files under OUTDIR/<pair_id>/")
    args = ap.parse_args()

    rows = list(csv.DictReader(REF.open(encoding="utf-8")))
    pending = [r for r in rows if "TO_RECOVER" in (r["conversation_id"], r["turn_window"])]
    ready = [r for r in rows if r not in pending]
    if pending:
        print(f"{len(pending)} rows still need conversation_id / turn_window filled in; skipping them.")

    ok = bad = 0
    for r in ready:
        turns = load_conversation(r["dataset_id"], r["conversation_id"])
        lo, hi = parse_window(r["turn_window"])
        text = render(turns[lo - 1:hi])
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        match = (digest == r["navigator_segment_sha256"])
        ok, bad = (ok + match, bad + (not match))
        print(f"  {r['pair_id']:4s} {r['source_dataset']:8s} sha256 {'OK' if match else 'MISMATCH'}")
        if args.write:
            d = Path(args.write) / r["pair_id"]
            d.mkdir(parents=True, exist_ok=True)
            (d / "navigator.txt").write_text(text, encoding="utf-8")

    print(f"verified {ok} ok, {bad} mismatched, {len(pending)} pending")


if __name__ == "__main__":
    main()
