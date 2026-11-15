# P2.0 — multi-document routing baseline (2026-07-28)

Gate fixed in advance:
`docs/superpowers/specs/2026-07-28-p2-0-multi-document-routing-design.md`.
Methodology: `RETRIEVAL_EVAL_METHODOLOGY.md`.

> ## ⚠ Read this before quoting any number below
>
> **These numbers measure `/api/v1/rag/search`. The RFP product does not use it.**
>
> `routes/rfp/answer.rs` retrieves through `retrieve_all` →
> `qa::find_relevant_sources_multi`. `/rag/search` is a separate implementation in
> `routes/rag.rs` that imports nothing from `qa.rs` and contains none of
> `find_relevant_sources_multi`, `dedup_near_identical` or
> `MAX_EXECUTED_SUB_QUERIES`.
>
> So every figure here describes a retriever the product does not run. The
> measurements are correct, reproducible and internally consistent — they are
> scoped to the wrong component. **Re-pointing the benchmark at `retrieve_all` is
> the outstanding work**; until then the gate verdict is provisional.
>
> How this surfaced is the useful part — see §6.

## 1. Verdict

**Gate PASSED provisionally.** Routing-induced loss **0.970** (≥ 0.90 band), so
P2 proceeds as a build task — subject to the scope caveat above.

## 2. What was measured

One namespace grown monotonically, so the U.S. Bank proposal's chunks stay
byte-identical across stages and the only variable is which other documents are
present. Every stage measured before the next ingest, because growth is one-way.

| stage | documents | doc@1 | doc@3 | pg@1 | **pg@3** | pg@5 | pg@10 | gap |
|---|---|---|---|---|---|---|---|---|
| **A** control | 1 | n/a | n/a | 0.789 | **0.868** | 0.895 | 0.947 | 0.427 |
| **B** library | 5 | 0.947 | 1.000 | 0.789 | **0.842** | 0.868 | 0.947 | 0.455 |
| **C1** + the RFP | 6 | 0.763 | 1.000 | 0.711 | **0.868** | 0.868 | 0.921 | 0.561 |
| **C2** + twin | 7 | 0.737 | 1.000 | 0.684 | **0.868** | 0.868 | 0.921 | 0.561 |

Queries: the 38 golden rows with a human-verified answer page. `|relevant| = 1` —
every golden answer lives in the U.S. Bank proposal, so every other document is a
distractor by construction.

## 3. Reproducibility is the strongest result here

The full staged run was executed **twice**, and the second time on a different
code base:

| | run 1 | run 2 |
|---|---|---|
| extraction model | gpt-4o-mini | gpt-4o-mini |
| store | wiped, rebuilt | wiped, rebuilt again |
| code | pre-merge | **post-merge** (fan-out fix, dedup guard, RRF fusion) |
| storage | `set_rel_property` broken | **fixed** |

**Every recall figure is identical across both runs.** Gap probe moved +0.001 on
two stages. Determinism within a run is spread 0.000 across three sweeps at every
stage.

Stage A also reproduced the *original* `gpt-4o` baseline exactly
(0.789 / 0.868 / 0.895 / 0.947), which settles a question this track had been
carrying: **the extraction model does not reach retrieval.** Chunk text and
embeddings are model-independent, as the two-phase design claims ("tree and
splitter have no LLM").

## 4. Findings the gate metric alone would have missed

### 4a. Self-retrieval is severe, and Page Recall@3 says the opposite

Ingesting the RFP the queries are drawn from takes **32.9% of retrieved chunks**
and pushes the proposal off rank 1 for **9 of 38** questions:

| | B | C1 |
|---|---|---|
| Document Recall@1 | 0.947 | **0.763** ▼ 19% |
| Page Recall@1 | 0.789 | **0.711** ▼ |
| gap probe | 0.455 | **0.561** ▲ 23% |
| **Page Recall@3** | 0.842 | **0.868** ▲ |

Page Recall@3 — the metric the gate turns on — went **up**, so routing-induced
loss reads **1.000, "PASS"**. The mechanism is benign: RFP chunks displaced
*LocalBank* chunks (55 → 37) more than correct proposal chunks, moving one row.
One row at n=38 is 0.026.

**A gate resting on that single number would have waved through a 19% drop in
rank-1 routing and a 23% rise in false evidence.** Exactly what the frozen
methodology warns about: *"when it doesn't move you cannot tell whether nothing
happened or two effects cancelled."*

The gap probe matters most. Unanswerable requirements now score 0.561 because the
RFP **restates the question**, and a question matches itself. Gap detection is the
product's core safety claim, and it degrades precisely because the wrong document
is in the library.

**Consequence:** *never ingest the RFP into the answering namespace* should be an
invariant with a test, not a convention. This measures the cost of getting it
wrong.

### 4b. Dedup did not collapse the near-identical pair — for two reasons

Adding a second rendering of TRE25101 **split** retrieval rather than one copy
swallowing the other:

| | C1 | C2 | combined |
|---|---|---|---|
| TRE25101 original | 125 | 65 | |
| near-identical twin | 0 | 59 | **124** |

The 98% chunk-level twinning measured offline did not produce a live collapse.
Two independent explanations, and only the first was found before run 2:

1. **Pools were starved.** Upstream `dee5d75` found `per_query_k` divided the
   budget by a 21-way decomposition while only 4 sub-queries ran — 96 of 100
   corpus-1 questions received exactly 12 candidates. With a pool that small,
   near-duplicates rarely co-occur to be compared. Upstream measured the dedup
   guard worth **+0.039 Recall@3 once unstarved, exactly 0 before**.
2. **The collapsing dedup pass is in `qa.rs`** — the path this benchmark never
   exercises (see the banner). `/rag/search` may not deduplicate at all.

**The pair is jointly stable but individually arbitrary.** Across the two runs the
proposal landed on exactly 202 chunks, LocalBank 38, Citizencredit 9, Illinois 7 —
while the twin pair moved 65/59 → 72/52 with the combined total fixed at 124.
Which copy wins a slot flips on tiny chunking differences. **An answer cited to
one of them is cited arbitrarily**, which is the same hazard as collapse wearing
different clothes.

### 4c. Distractor strength varies enormously; an average hides it

| document | chunks | share |
|---|---|---|
| U.S. Bank proposal *(relevant)* | 202 | 53.2% |
| TRE25101 (the RFP itself) | 72 | 18.9% |
| TRE25101 twin | 52 | 13.7% |
| Delaware LocalBank RFP | 38 | 10.0% |
| Citizencredit RFP | 9 | 2.4% |
| Illinois e-payments RFP | 7 | 1.8% |
| Tech Mahindra whitepaper | 0 | **never retrieved** |

Delaware LocalBank — same state, same service area — is the strongest genuine
distractor. The core-banking whitepaper never entered the top 10 of any of 38
queries despite scoring 0.700 on its own subject matter: indexed, reachable,
never competitive. Reporting "3.6% each" would have been true and useless.

## 5. Cost

Measured, `gpt-4o-mini-2024-07-18`:

| | |
|---|---|
| Distractor pages (run 1) | 269 → **$0.587**, 823 calls, **74% prompt-cache hit**, 53 min |
| 12-page probe | $0.057, 30% cache hit |
| Stage A, 214 pp | 1666 s, 7.79 s/page |

The probe projected ≤ $1.30; actual $0.587. It understated cache efficiency badly
(30% vs 74%) because larger documents reuse the static prefix far more.

## 6. How the scope error surfaced, and why it generalises

Run 2 was expected to move: it carried upstream's fan-out fix, cross-document
dedup guard and RRF fusion — changes that took corpus-1 from Recall@3 0.583 →
0.944.

**Nothing moved. Four stages, every metric, identical.**

That non-result was the finding. Tracing why led to `answer.rs` using
`retrieve_all` → `find_relevant_sources_multi` while the benchmark queries
`/rag/search`, a separate implementation sharing none of it.

The benchmark's own reasoning was sound — *"query `/rag/search`, which returns
ranked chunks without passing through the answer LLM, so a score change means
retrieval moved rather than the generator having a good day."* It isolates
retrieval from generation correctly. **It isolates a different retrieval.**

Same shape as every other defect on this track: correct in isolation, wrong where
it meets someone else's code. And it was only detectable because a change that
*should* have moved the number didn't. **A benchmark that never disagrees with a
code change is not measuring that code.**

## 7. Also found

`set_rel_property` bypassed the overflow store, so any relationship property over
51 bytes failed outright and took the document's entire Layer 2 with it — found
when a 214-page ingest died with `Value for key 37 is 76 bytes, max inline is 51
bytes`. Fixed in `c9ab1e2`; run 2's stage A completed where run 1's was
`extraction_failed`, confirming it on the document that exposed it.

It was invisible to every metric here: `ExtractionFailed` is deliberately
terminal-**but-answerable**, so pages and chunks stay queryable and a document
with zero entities scores identically to a healthy one.
`docs/audits/FINDING_set_rel_property_bypasses_overflow_2026-07-28.md`.

## 8. What this licenses

**Licensed:** P2 proceeds as a build task, provisionally. Routing does not
collapse at this corpus size on the measured path.

**Not licensed:** any claim about the retriever the product runs — that is
unmeasured. Nor any claim that routing scales to a real proposal library:
distractors here are different *kinds* of document, where a real library is many
proposals, which resemble each other far more.

**Next:** re-point the benchmark at `retrieve_all` and re-run. `/qa/ask` returns
`sources_used`, which reflects its output, at roughly $0.15 per sweep.
