# Navigator / Operator Rating Instrument — Segment Level

This is the instrument used to classify conversation **segments** as Navigator-mode
or Operator-mode from the text alone. It is built from ten characteristic behaviors —
five Navigator markers and five Operator markers — each scored present (1) or absent
(0) within the segment. Classification is **derived from the marker tally**, not
assigned by gut feeling.

The unit is the segment, not the person. The same user may produce a Navigator-mode
segment in one moment and an Operator-mode segment in another; that is expected, and
the instrument is designed to capture it.

---

## What a segment is

A segment is a contiguous stretch of 3–7 turns taken from a longer human–AI
conversation, cut at a natural boundary (topic shift, task transition, or closure of a
sub-goal). A single conversation may contain multiple segments, and the same user may
produce Navigator-mode segments and Operator-mode segments within the same conversation.
That is expected, not a problem.

A segment is scored on its own terms. The rater does not read beyond the segment
boundary to form a judgment, and does not import information from other parts of the
parent conversation. What the user does *inside the segment* is the entire basis for
classification.

---

## What the rater is scoring

The **mode of communication** visible in the user's turns within the segment. Not the
person. Not the parent conversation. Not the topic. Not the task outcome. Only what the
user does across the 3–7 turns of this segment.

A user leading a conversation in Navigator-mode in one segment and Operator-mode in
another segment is not a contradiction — it is the taxonomy working as intended. Both
modes are legitimate communication styles appropriate to different task types. The rater
is not judging the user; the rater is classifying the shape of the exchange.

---

## Navigator Markers (N1–N5)

Each marker is scored 1 (present in the segment) or 0 (absent from the segment).

| Code | Marker | Definition (segment-level) | Score 1 if... |
|------|--------|---------------------------|---------------|
| **N1** | Iterative refinement within the segment | The user returns to refine, deepen, or redirect the model's output during the segment | Within the segment, the user explicitly builds on, modifies, or challenges a response the model produced earlier in the same segment |
| **N2** | Domain knowledge injection | The user contributes substantive knowledge the model did not provide | Within the segment, the user introduces specific facts, frameworks, terminology, or context not present in the model's prior responses in the segment |
| **N3** | Assumption challenging | The user questions or contradicts the model's framing or conclusions | Within the segment, the user explicitly pushes back on something the model stated — in words ("but what about," "that's not right because") or through visible refusal to accept the output and a redirect |
| **N4** | Cross-domain bridging | The user connects the segment's topic to a different field, framework, or context | Within the segment, the user introduces a concept from outside the segment's primary domain to create a new connection |
| **N5** | Evaluative reasoning request | The user asks for comparison, tradeoff analysis, or conditional assessment | Within the segment, the user requests "which is better," "what are the tradeoffs," "under what conditions would this change," or equivalent |

---

## Operator Markers (O1–O5)

Each marker is scored 1 (present in the segment) or 0 (absent from the segment).

| Code | Marker | Definition (segment-level) | Score 1 if... |
|------|--------|---------------------------|---------------|
| **O1** | Single-shot delegation | The user provides a task and accepts the first output without meaningful modification | Within the segment, the pattern is task → response → closure, or task → response → new unrelated task, with no substantive engagement in between |
| **O2** | Template/formula request | The user asks for a standard format, template, or formulaic output | Within the segment, the user says "write me a," "give me a template for," "draft a," "create a list of," or equivalent |
| **O3** | Acceptance without evaluation | The user accepts model output without questioning accuracy or depth | Within the segment, the user responds with "thanks," "great," "perfect," or moves on without substantive follow-up |
| **O4** | Outsourced judgment | The user defers a decision or judgment entirely to the model | Within the segment, the user asks "what should I do" or "which one is better" without contributing constraints, criteria, or context of their own |
| **O5** | Repetitive re-prompting | The user repeats the same request with minor variations rather than building on prior responses | Within the segment, the user restates the same core query without adding new information, changing angle, or building on what the model produced |

---

## Classification rule

Count N markers present in the segment. Count O markers present in the segment.

| N total | O total | Segment classification |
|---------|---------|------------------------|
| Higher than O | Lower than N | **Navigator-mode segment** |
| Lower than N | Higher than O | **Operator-mode segment** |
| Equal | Equal | **Excluded** (tie — not eligible for matched-pair tracing; retained where rater disagreement is itself the data) |

The classification is *derived* from the marker scores. The rater does not pick the
label by gut feeling and then backfill markers. Score the ten markers honestly on what
is visible in the segment, tally, and the numbers decide.

---

## Edge cases

- **A segment can contain both Navigator and Operator markers.** This is normal and
  expected. The higher count determines the label.
- **A segment can be very short on markers.** A segment with only one N marker and zero
  O markers classifies as Navigator. A segment with one O marker and zero N markers
  classifies as Operator. Sparse marker counts are not an error — they reflect
  low-intensity segments, which are real.
- **Do not read beyond the segment.** If a segment contains a question the user answers
  in a later segment, that later answer is not part of this segment's scoring. Each
  segment stands alone.
- **Do not classify the parent conversation.** A high-confidence Navigator classification
  at the conversation level does not transfer to a segment drawn from that conversation.
  The segment is rated on its own behavior.
- **Direction-by-restraint is a known instrument gap.** Users who exercise high agency
  through restraint rather than verbal challenge may be under-detected by the current
  markers. This is documented as a limitation; no marker is added to cover it in this
  version.

---

## Confidence label

After scoring a segment and deriving its classification, the rater assigns a confidence
label, recording how cleanly the stance is expressed — assigned from the text, before
and independent of any trace:

- **HIGH** — Marker pattern is unambiguous. Two or more markers of the dominant class
  present, zero or one of the opposite class. No edge-case reasoning required.
- **MEDIUM** — Marker pattern is present but sparse, or involves one edge-case judgment
  (e.g., borderline N3 vs. not present).
- **LOW** — Marker pattern is sparse and involved multiple edge-case judgments. The rater
  was unsure on more than one marker.

Only segments rated HIGH are eligible for matched-pair circuit tracing. MEDIUM and LOW
segments remain in the classifier pool.
