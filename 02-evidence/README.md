# What we've already measured

Read this page before opening the files it describes. These are real internal
documents, written for engineers on the project, so they're denser than the context
pages — that's expected. You don't need to understand every line. What you *do* need
is the shape of what's known, what isn't, and where your work plugs in.

There's also a second reason to read them: they show what a finished piece of work
looks like here. Notice how consistently they state sample sizes, mark provisional
results as provisional, and describe their own limitations.

---

## The files, in the order worth reading them

### 1. `RFP_RETRIEVAL_BASELINE_2026-07-26.md` — the core measurement

**Read: §1, §2, §3. Skim the rest.**

The first proper measurement of the system, against the Delaware/U.S. Bank pair.

- **§2** — how well search finds the right page. Recall@3 = 0.868, five runs, zero
  variance. Note how carefully it warns against comparing that number to a different
  benchmark's 0.58: two numbers with the same name measuring different things is a
  standing hazard.
- **§3** — **the finding that shapes the whole product**: similarity scores cannot
  detect gaps, because the answerable and unanswerable ranges overlap. This is §5 of
  [what-is-an-rfp.md](../01-context/what-is-an-rfp.md), in its original form with the
  full data.
- One sentence to carry with you: *"A golden set without true negatives would have
  shown 0.868 and been called a success."*

### 2. `2026-07-28-rfp-vs-questionnaire-product-decision.md` — the open decision

**Read the whole thing. It's short.**

A memo written for a decision the seniors haven't yet made: should this be an *RFP*
automation product, or should it pivot to *questionnaire* automation (the security and
vendor-diligence questionnaires companies fill in constantly — SIG, CAIQ, DDQ)?

Two things to notice.

First, §1 rejects an appealing shortcut — testing the RFP system on questionnaire data
because real RFP data is scarce — on the grounds that a curated Q&A dataset is
answerable by construction, so gap detection would score ~100% while measuring
nothing. That's the "a number that never moves isn't measuring anything" rule from
[how-we-work.md](../01-context/how-we-work.md), applied to a strategy.

Second, the memo's own conclusion is that **the decision needs information nobody has
gathered yet** — market size, data availability, competitive landscape. That gap is
[Task 3](../03-tasks/task-3-questionnaire-landscape.md) and
[Task 4](../03-tasks/task-4-competitor-landscape.md). If you get to them, your research
is a direct input to a real decision.

### 3. `RFP_MULTIDOC_ROUTING_P2_0_2026-07-28.md` — does it hold on a real library?

**Read the warning box at the top, §1, §2. Skim §6.**

Everything above was measured against a library of one document. Real customers have
dozens. This tested whether performance survives as the library grows — it does, mostly
(0.970 of single-document performance).

The reason to read it is the **warning box**, which is a small masterpiece of honest
reporting. Partway through, the author discovered the benchmark was measuring a
retrieval path *the product doesn't actually use*. The numbers are correct, reproducible
and internally consistent — and scoped to the wrong component. Rather than quietly
re-running it, the report leads with the caveat and marks its own verdict provisional.

That's the standard. If you discover your own work measured the wrong thing, saying so
loudly is the right move and nobody will be annoyed.

### 4. `golden_set_50rows.jsonl` — the thing you're extending

The 50 hand-verified rows that everything above was scored against. **This is your
primary reference for Task 1** — the format, the tone of the reasoning, the level of
care. Open it in a text editor; one JSON object per line.

Composition, so you know what you're adding to:

| | count |
|---|---|
| `answered` | 31 |
| `partial` | 7 |
| **`none` (true negatives)** | **12** |
| — corroborated by two annotators | 45 |
| — disputed, resolved by human rule | 5 |
| Requirements in the RFP **not** covered by any row | **572** |

That last row is the point. The golden set covers **8%** of the RFP, and the safety
metric rests on **12 rows**.

### 5. `example_annotations_C.jsonl` — worked examples

The raw output of one annotator, before merging and adjudication — 50 rows in the exact
format you'll produce. Note the `reasoning` field on every row, and note that `none`
verdicts carry `page: 0` and an empty quote.

This is also the file the setup check in [START_HERE.md](../START_HERE.md) runs against,
so you've already seen it pass.

---

## Where the numbers stand today

| Measurement | Value | How much to trust it |
|---|---|---|
| Page Recall@3 | 0.868 | **Solid.** Five runs, zero variance, one document. |
| Document Recall@1 (5-doc library) | 0.947 | **Provisional** — measured on a retrieval path the product doesn't use. |
| Invalid citations | 0 | **Solid**, but on a small sample. |
| **Gap recall (safety)** | **9 / 12** | **Weak — n = 12.** The whole safety case rests on twelve rows, and one specific finding rests on a single row. |
| False refusals | 8 / 38 | Solid-ish. Not a safety issue; a usability one. |
| Requirement mining recall | 87.5% | Measured once. Two runs of the same document differ by ~1%. |
| Genuine RFP→proposal pairs owned | **1** | This is the number that limits everything else. |

The bottom two rows of that table are your two tasks. That's not a coincidence — they
were chosen because they're what's actually blocking.

---

**Next:** [../03-tasks/README.md](../03-tasks/README.md)
