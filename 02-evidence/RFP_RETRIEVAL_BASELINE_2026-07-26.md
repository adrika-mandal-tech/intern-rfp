# RFP retrieval baseline — 2026-07-26

First measured numbers for the RFP-automation track (`dev/rfp-automation`). Scores
the **routing stage in isolation** via `/api/v1/rag/search`, per the methodology
frozen in `RETRIEVAL_EVAL_METHODOLOGY.md`.

**Read the caveat in §2 before quoting any number here.**

---

## 1. What was measured

| | |
|---|---|
| Knowledge base | U.S. Bank's genuine submitted proposal for Delaware `TRE18101-BANKINGSVC`, 214 pp |
| Queries | 50 requirements from Delaware `TRE25101-BANKINGSVC` — same buyer, same contract line, 7 years later |
| Golden set | `bench/rfp_finance/work/golden_set_candidate.jsonl` — 50 rows, human-adjudicated, 45 corroborated by two independent annotators, 38 quote-verified |
| Namespace | `rfp_finance` |
| Commit | `fc48f95` |
| Flags | All six pinned **explicitly** (`INGEST_TWO_PHASE=1 QA_TREE_EXPANSIONS=1 UNSTRUCTURED_EXTRACT_SKIP_GATE=1 UNSTRUCTURED_ER_V2=0 UNSTRUCTURED_ER_PASS=1 UNSTRUCTURED_LLM_CACHE=0`) |
| Dedup threshold | 0.90 (`rag_tuning.toml` default) |
| Pipeline state | **Phase-1 answerable; Phase-2 extraction still running.** Chunk retrieval is Phase-1 data, so these numbers should be stable — to be re-confirmed after completion rather than assumed. |

## 2. Page Recall@k — and why it must not be compared to 0.58

| k | 1 | 3 | 5 | 10 |
|---|---|---|---|---|
| **Page Recall** | 0.789 | **0.868** | 0.895 | 0.947 |

Found at some rank: **36 / 38**. Five sweeps, **zero variance** (identical to three decimals).

> **This is not comparable to the corpus-1 figure of 0.58.** That measures *document routing across ten documents*; this measures *page recall inside one document*. Ours is the easier problem. These numbers are not evidence that RFP retrieval outperforms corpus-1 retrieval, and should never be cited that way.

**Zero variance is expected, not suspicious.** Vector search over a fixed HNSW index with a fixed query embedding is deterministic; no LLM sits in this path. The ±4–7 band applies to LLM-judged QA accuracy. The practical value of running five sweeps anyway is that **any future movement in this metric is signal rather than noise**.

**Recall climbs with k, and that is the interesting part.** Corpus-1's standing finding is `Recall@1 ≈ Recall@3 ≈ Recall@5` — flat, meaning the answer-bearing document is absent from the candidate pool rather than ranked low. Here recall rises 0.789 → 0.947, so within a single document the answer-bearing page **is** in the pool and ranking is doing real work. Candidate generation is healthy at this scale; the corpus-1 diagnosis is about cross-document routing, which this configuration never exercises.

## 3. The finding that matters more than recall: similarity cannot detect gaps

Twelve golden rows are human-verified as having **no answer** in this proposal — mostly the Lockbox Services questionnaire, a service line U.S. Bank did not bid in 2018. They are true negatives, and they are rarer and more useful than the positives.

| | median | min | max |
|---|---|---|---|
| Answerable (n=38) | 0.682 | **0.408** | 0.781 |
| Gaps (n=12) | 0.426 | 0.332 | **0.678** |

**The ranges overlap.** Six of twelve gap queries score above the *lowest* answerable query.

| threshold | gaps caught | real answers lost |
|---|---|---|
| 0.40 | 6/12 | 0/38 |
| 0.50 | 9/12 | 3/38 |
| 0.65 | 11/12 | 16/38 |

No single similarity threshold separates them. **The POC's `GAP_FLOOR = 0.28` would catch none of these gaps** — every gap query scores above it.

The cause is legible in the data: the proposal is dense with topically-related banking content even where the specific answer is absent. Embeddings match topic. They cannot distinguish *"about lockboxes"* from *"answers this lockbox question"*.

**Consequences for the build:**

1. **The gap floor is a cost optimisation, not a safety mechanism.** It exists to avoid spending an LLM call on hopeless candidates. It must never be described, tuned, or relied on as gap detection.
2. **The LLM grounding-check does all the real work** of distinguishing coverage from absence. The Tier-1 safety criteria in the spec rest entirely on that call, so it is where verification effort belongs.
3. A benchmark built only from requirements the KB *does* answer would have reported 0.868 recall and called it success. **The true negatives are what made this visible**, and any future golden set must keep them.

## 4. Query shape (P0.6): broad multi-part requirements retrieve worse

| form | n | R@1 | R@3 | R@5 | R@10 |
|---|---|---|---|---|---|
| Interrogative (*"What fees…?"*) | 18 | 0.889 | **0.944** | 0.944 | 1.000 |
| Imperative (*"Describe…"*) | 16 | 0.688 | **0.750** | 0.812 | 0.875 |
| Other | 4 | 0.750 | 1.000 | 1.000 | 1.000 |

Both total misses are imperative:

- `R018` — *"Describe the backup and recovery capabilities in the event the proposed systems are unavailable…"*
- `R395` — *"Describe the Firm's involvement with the payment process. Discuss in detail any files that…"*

**The confound was declared before the data was seen and it holds:** in this corpus, form correlates with specificity. Imperatives are broad, often multi-part asks; interrogatives are narrow factual ones. Both misses are broad and compound, which points at breadth rather than grammar. This data cannot separate the two, and at n=16/18 a 19-point gap is suggestive, not conclusive.

**Actionable either way:** decomposing compound requirements into sub-queries before retrieval helps under both explanations, and RFP requirements skew imperative — so this is a real P3 lever rather than a curiosity.

## 5. Measurement notes worth inheriting

- **`/api/v1/rag/search` does not return page provenance.** It projects only `text` and `doc_id` (`rag.rs:2296`); `page_no` is written at ingest (`lexical_graph.rs:311`) but never reaches the caller. A scorer trusting the response would score every row a miss and report total retrieval failure. Pages are recovered here by matching chunk text back to the page dump — deterministic, offline, no production change.
- **Chunk text is not a substring of the page layer until the synthesized `"Section: …"` prefix is stripped.** Miss this and every lookup fails.
- 2 of 38 requirements returned results whose text resolves to no single page — chunks straddling a page break. Reported separately so a measurement limit is never read as a retrieval miss.
- `/rag/search` has **no namespace scoping of its own**; it applies only caller-supplied property filters. Chunks do carry a `namespace` property, so the filter works — but nothing requires it. Recorded as a tenancy finding in the spec (§5.2c).

## 6. Ingest: timing, quality, cost

| stage | window |
|---|---|
| parsing | 0 → 10 min |
| classifying | 10 → 12 |
| embedding | 12 → 14 |
| extracting | 14 → 28 |
| writing | 28 → 30 |
| narrating | 30 → 31 |

**14 min to answerable ≈ 3.9 s/page** (platform ~4.5–5). **31 min full ≈ 8.7 s/page** (platform ~10.5). A dense 214-page proposal with tables and exhibits ran slightly *faster* per page than the reference corpus.

Job quality: 750 chunks · 512 tree nodes (`tree_source: Deterministic`) · 1249 entities extracted → 803 after canonicalization (87 merged) · 692 relationships written · 16 images captioned · `parse_strategy: docling`, `parse_degraded: false` · **0 validation warnings, 0 errors**.

### Cost — and a correction worth inheriting

699 LLM calls · 2,523,611 prompt tokens (**1,627,264 cached = 64.5% hit**, against the platform's ~68%) · 270,830 completion tokens.

| | cost | per page |
|---|---|---|
| **Actual (`gpt-4o-2024-08-06`)** | **$6.98** | $0.0326 |
| Same run at `gpt-4o-mini` | $0.42 | $0.0020 |

**The spec's §8a estimated $0.82 and was 8.5× low.** It applied the platform's $0.00384/page to our page count — but that figure was measured **on mini**, while we ingested with the `gpt-4o` sitting in `.env`. The pipeline behaved as documented; the extrapolation carried a per-page cost across without carrying its model.

At library scale this stops being academic: **~$261 versus ~$16** for a 40-proposal corpus. P2 should gate the model choice on measured retrieval quality rather than inherit whatever `.env` holds.

## 6a. Post-extraction re-run: scores unchanged

The §2 numbers were taken while Phase 2 was still running. Re-scored after completion, five sweeps: **0.789 / 0.868 / 0.895 / 0.947, gap median 0.426 — identical to three decimals.** Chunk retrieval is unaffected by Layer-2 entity and relationship writes. Verified rather than assumed.

## 7. What this does not tell you

- Nothing about **answer quality** — no generation ran. This is routing only.
- Nothing about **multi-document routing**, which is the corpus-1 weakness and the thing P2 must measure with a real proposal library.
- Nothing about **requirement mining recall** — the 622-requirement extraction problem is untouched here.
- The 9 golden rows resolved by a single annotator plus adjudication carry less weight than the 41 corroborated ones.

---

## 8. Grounding-check validation (added same day)

§3 showed similarity scores cannot separate answerable requirements from
unanswerable ones. That leaves the LLM's own judgement as the only thing standing
between the product and invented coverage. It had never been measured. This
measures it against the same golden set — 38 verified answerable rows, 12 verified
true negatives (the lockbox component U.S. Bank never bid).

The test is adversarial by construction: retrieval *does* return plausible
lockbox-adjacent banking text for those 12, scoring up to 0.678. The model must
refuse on the merits, not because nothing came back.

| configuration | gap recall (safety) | false refusal | runs |
|---|---|---|---|
| top-k 3, baseline prompt | **12/12** | 15/38 (39%) | 1 |
| top-k 8, baseline prompt | 11/12 | 11/38 (29%) | **3, identical** |
| **top-k 8, + scope rule** | **12/12** | 11/38 (29%) | **3, identical** |

Zero invalid citations in every configuration — no response ever cited an excerpt
it had not been shown.

**The failure at k=8 is legible, reproducible, and the same error class as the
dedup defect.** The missed row is `R315`, a **lockbox-scoped** disaster-recovery
question, answered from **general-banking** disaster-recovery text. Retrieval
substitutes across components structurally (§10.0 of the spec); the generator does
it too once given enough adjacent context. One underlying weakness: the system
cannot distinguish *content about X for component A* from *content answering X for
component B*.

**The fix is one sentence, and the data was already there.** Chunk text carries the
section as a baked-in `"Section: …"` prefix, so the model could always see which
component each excerpt belonged to and simply was not using it. Adding an explicit
scope rule — *an excerpt from a different service component does not answer this
requirement, however similar the subject matter* — recovers the miss in all three
runs at no cost to false refusals.

**Recommended for P3: top-k 8 with the scope rule.** It dominates both
alternatives — the safety of k=3 with the lower false-refusal rate of k=8.

### What this does not establish

- **n=12 true negatives is a small safety sample.** The effect replicated perfectly
  three times, but it rests on recovering one row. P3's evaluation harness needs
  substantially more verified negatives before this threshold is load-bearing.
- **Generalisation is untested.** One corpus, one un-bid component. Whether the
  scope rule holds where components overlap more subtly is unknown.
- **29% false refusal is unexplained and unsolved.** It is not a safety problem, but
  at that rate roughly two in five answerable requirements reach an SME
  unnecessarily, which materially erodes the product's value. This is the next
  thing to investigate, and it is a *value* question rather than a *safety* one.

Total cost of this investigation: **~$0.40**.

---

## 9. Requirement mining at scale (P3.5, 2026-07-27)

The proof-of-concept miner capped at **80 requirements and 16 windows** of 12,000
characters. The reference RFP holds **622 human-annotated requirements across
pp19-64** — roughly 13 per page — so that design had a structural recall ceiling
near 13% and stopped partway through the questionnaire regardless of quality.

Rebuilt around page windows with overlap, no global cap, and no guessed page range.

| | |
|---|---|
| Mined | **740** requirements |
| Pages / windows | 127 / 63, **0 failed** |
| Duplicates removed across overlaps | 370 |
| Wall time | 17 min (one model call per window, sequential) |
| **Requirement recall** | **544/622 = 87.5%** |
| Precision (within annotated pages) | 544/570 = **95.4%** |
| Outside pp19-64 | 170 entries, **not scored** — no ground truth there |

Ground truth was produced by human-directed annotation **before this miner
existed**, using different models and a different method. It is not a system
grading itself.

### The 78 misses are segmentation, not blindness

Checking each missed requirement against what the miner produced on the same and
adjacent pages:

| | |
|---|---|
| Content clearly present in a mined entry, grouped differently | 34 |
| Partially present | 43 |
| **Genuinely not extracted** | **1** |

So two numbers answer two different questions, and both are honest:

- **87.5%** — agreement with human *segmentation*. The right figure for a
  compliance matrix, where each row is a discrete thing a person must answer.
- **~99.8%** — *content* coverage. The document was read.

Only pp60 and p64 produced nothing, both in the Attachments region. The annotators
split multi-part items aggressively — one recorded 482 entries where the other
recorded 468 from the same pages — so exact boundary agreement was never a
realistic target.

### ⚠ Safety-class classification is the weak result

**82/95** annotated `pricing`/`admin` requirements were found, but only **69/82
kept a non-generative class**. Thirteen commercial or legal requirements were
mined as something draftable.

The union rule in `routing` catches these downstream by re-checking the text for
commercial markers — which is precisely why it is a union and not a model verdict
— so nothing reaches a draft unchecked. But the miner should not be producing them,
and 13 of 82 is not a rounding error.

This reproduces, in production code, exactly what the dual-annotation run measured:
a capable model systematically under-classifies toward `technical` (31 of 33
disagreements ran that direction). Seeing it again in a different model, a
different prompt and a different codebase makes it a property of **the task**
rather than of any one configuration.

**Consequence:** the union rule is not a belt-and-braces nicety, it is load-bearing.
Any future change that makes classification "trust the model" would put invented
numbers in bids. Treat the 13 as the expected failure rate of LLM classification on
this axis, not as a bug to tune away.

### 9a. Safety-class follow-up: the obvious fix would have made it worse

The 13 pricing/admin requirements mined as draftable looked like a bug to fix by
applying `routing::has_commercial_marker` at **mining** time rather than only at
answer time. Measured offline against ground truth (no re-mine, no API spend), that
change is a net loss:

| | |
|---|---|
| Safety class stored correctly | 69/82 → **77/82** (+8) |
| Draftable requirements wrongly upgraded | **28/460 (6.1%)** |

**Net −20 on stored-class accuracy.** And it buys no safety at all, because
`is_human_routed` is already `class ∈ {pricing, admin} OR has_commercial_marker(text)`
— a fee question mined as `technical` is **already routed at answer time**. The
metric was measuring the *stored* class, not the safety outcome. Rejected.

### 9b. The measured residual: 5 of 82, and what it actually risks

Requirements that **neither** signal catches — mined as draftable AND carrying no
lexical marker — are the genuine exposure:

| truth | text (abridged) |
|---|---|
| pricing | Does the program provide **free access** to funds at ATMs, retail stores, and bank branches? |
| pricing | Is there an **annual minimum** number of cards the State needs to issue for this program? |
| pricing | Discuss the Firm's adaptability of its system to organization requests for changes… |
| pricing | What are the available options to add other recipients/parent organizations? |
| pricing | Does the Firm return items if an overdraft exists? If yes, how flexible is this policy? |

**5 of 82 = 6%.** They are not uniformly misclassifications: the first two carry real
pricing signals the markers miss (`free access`, `annual minimum`), while the last
two read as policy questions the annotators judged commercial. Reasonable people
would label them differently.

**The harm is narrower than "an invented number".** The grounding check still
applies, so a draft can only assert what the knowledge base contains. The exposure
is *unflagged stale fee content* — a 2018 fee answer presented without the pricing
flag that would make a reviewer scrutinise it.

**Recommendation: record this as measured residual risk, do not chase it with more
markers.** Both safety rules in this module have already over-fired when
strengthened without measuring what they catch (`rate` inside "separately",
`acknowledg` inside a technical ACK, and the 28 above). At 6%, on a sample of 82,
with several entries genuinely arguable, further lexical tuning buys noise. The
durable fixes are a larger annotated safety sample and reviewer-facing display of
*why* something was or was not flagged — not a longer word list.
