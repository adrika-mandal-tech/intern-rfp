# RFP automation vs. questionnaire automation — a product decision memo

**Date:** 2026-07-28 · **Updated:** 2026-08-18 (post-Task 3) · **For:** the go/continue conversation with seniors
**Purpose:** the suggestion came up to test on questionnaires / answered datasets
because genuine RFP data is scarce. This separates two very different things that
suggestion can mean, and lays out the evidence for each so the decision is made on
merits, not on which data was easier to find.

> **UPDATE (2026-08-18):** Task 3 (Questionnaire Landscape) empirically tested the "data availability" premise in §2. **Finding: Completed questionnaires are NOT publicly available.** Blank templates exist; filled questionnaires with real vendor answers do not. Private answer libraries in GRC tools are customer data, not public. This invalidates the "abundant data" argument for pivoting. See §2 row "Data availability" and §4 below.

---

## The one distinction that matters

"Use questionnaires and answered datasets" can mean two completely different
things, and conflating them is the trap:

1. **Testing RFP on questionnaire data** — using Q&A datasets as a stand-in
   because real RFP pairs are scarce. **This is a mistake** (§1).
2. **Building questionnaire automation as the product** — a deliberate pivot to a
   different, adjacent market. **This is a legitimate strategic option, and
   possibly a stronger one than RFP** (§2–§4).

The rest of this memo argues 1 is a trap and 2 deserves a real hearing.

---

## §1 Why testing RFP on questionnaire data is a trap

An RFP is not a questionnaire. The four hard, valuable parts of RFP automation are
exactly the parts a Q&A dataset removes:

| Hard part of RFP | What a Q&A / questionnaire dataset does to it |
|---|---|
| **Mine requirements** from 100+ pages of prose | Hands you the questions pre-extracted. Skipped. |
| **Detect gaps** — refuse when the library can't answer | A curated dataset is answerable by construction. No gaps to detect. |
| **Route across a document library** | A Q&A pair is single-source. Skipped. |
| **Commercial safety** — never auto-draft an invented fee | No questionnaire exercises this. |

The consequence is not "a slightly less realistic test." It is **a reassuring
number that measures none of the actual risk.** Gap detection — the property we
measured at 5/12 → 9/12 with a hard ceiling this week — would score ~100% on an
answerable questionnaire set, because there is nothing to refuse.

This project's entire history is green numbers hiding real failures: 87% retrieval
on a document whose extraction had silently crashed; a "cautious" system that had
discarded 35 of 50 answers on a formatting mismatch; a safety test that passed
because two unrelated bugs cancelled. **A questionnaire benchmark is that failure
mode adopted as strategy.** It would let us tell seniors "95% accurate" and be no
closer to knowing whether the product is safe in front of a real tender.

And the premise is only half-true. We did find the real thing: a genuine RFP plus
its genuine submitted proposal — same buyer, same contract line, seven years
apart. **One real pair produced the 622-requirement golden set and every safety
finding this project has.** The twelve verified-unanswerable rows ("the bank never
bid lockbox") have no equivalent in any Q&A dataset, and they are the most
valuable rows we own. The answer to data scarcity is **more real pairs** —
government procurement portals publish received proposals; Delaware did, other
states and municipalities do — not easier fake ones.

---

## §2 The two products, side by side

| | **RFP automation** | **Questionnaire automation** (SIG / CAIQ / vendor security & DDQ) |
|---|---|---|
| Input | 100+ pp unstructured tender prose | a structured questionnaire — discrete, pre-listed questions |
| Requirement mining | **Hard** — extract 600+ reqs from prose | **Free** — questions are already discrete rows |
| Knowledge base | past proposals (scarce, confidential) | past answered questionnaires (private GRC libraries — **not public**) |
| Answer shape | multi-paragraph prose, tracked citations | often short/constrained (yes-no, controlled phrasing) + evidence |
| Gap/safety stakes | high — a bid is a contract | high — a security attestation is a liability |
| Deal frequency | few, large, episodic | **many, repetitive, continuous** (vendors fill these constantly) |
| Data availability | **scarce** — genuine pairs almost unobtainable | **scarce for public completed questionnaires** — blank templates exist; filled ones are private |
| Output artifacts | DOCX + filled XLSX | filled questionnaire (often the same XLSX/portal format) |

---

## §3 What of today's work transfers — component by component

This is the part that makes the decision concrete rather than abstract.

| Component (built / validated) | Transfers to questionnaires? |
|---|---|
| Retrieval over a past-answer library (`retrieve_all`) | **Yes, fully** — same operation |
| Grounded drafting + citation validation (0 invalid cites) | **Yes, fully** |
| Page/document routing (Doc Recall@1 0.97–1.0) | **Yes** — still "find the right past answer" |
| Commercial/legal routing to a human (union rule) | **Yes** — still relevant |
| **Requirement mining** (87.5% recall, hard-won) | **No** — questionnaires need none of it |
| **Gap detection** (the fragile 9/12 safety property) | **Partly** — still needed, but on discrete factual questions it is a far easier problem than on lockbox-scoped RFP prose |
| Two-phase ingest, tree retriever, storage fixes | **Yes** — pipeline is shared |

Read the honest implication: **a pivot to questionnaires keeps the parts that work
(retrieval, grounded drafting, citation, routing) and drops the two parts that are
hardest and most fragile (mining, and gap detection on prose).** That is an
argument *for* questionnaires, not against — we would be standing on the solid
half of what we built and shedding the risky half.

The counter to keep honest: gap/safety discipline does not vanish for
questionnaires — a wrong "yes, we encrypt at rest" is a real liability — but the
questions are more factual and constrained, so the "is this text *about* X or does
it *answer* X" trap that breaks RFP gap detection is materially smaller.

---

## §4 The honest scorecard

**RFP automation**
- Strengths: high value per deal; we have a genuine validated corpus; the hard
  parts are largely built and measured.
- Weaknesses: **data scarcity is structural, not temporary** — you cannot easily
  build or buy a large corpus of RFP+proposal pairs; long, episodic sales cycles;
  the hardest parts (mining, prose gap detection) are the fragile ones.

**Questionnaire automation**
- Strengths: discrete questions remove the hardest component (mining); high-frequency, repetitive pain = a clearer, more continuous buying motive; reuses the solid half of our stack (retrieval + grounded drafting).
- Weaknesses: **data scarcity mirrors RFP** — public completed questionnaires do not exist (Task 3, 2026-08-18); private answer libraries in GRC tools are customer data, not accessible; more crowded/adjacent to existing GRC tooling; per-deal value likely lower; answer format mismatch (Yes/No/pick-list + evidence vs. prose with citations).

**What today's measurements actually license us to say:**
- The retrieval + grounded-drafting + citation core is **validated and safe** on
  the product path (Doc Recall@1 0.97–1.0, false refusals 1/38, 0 invalid
  citations, realistic multi-document library holds).
- RFP-specific mining works (87.5%) but gap detection has a **characterized
  ceiling** whose fix is real pipeline work (see the audit finding of 2026-07-28).
- None of the safety validation transfers as-is to a claim about questionnaires —
  it would need its own golden set — **but the same machinery would measure it.**

---

## §5 Recommendation

1. **Do not test RFP on questionnaire data.** It manufactures confidence in the
   exact dimension (gap safety) that is fragile, and this project has been burned
   by false-green numbers all week. If the goal is more RFP signal, spend a day
   sourcing additional real published proposal pairs.

2. **Treat questionnaire automation as a genuine product option, evaluated on its
   own merits** — not as a testing convenience. **However, the "abundant data" premise (July 2026) has been invalidated by Task 3 (August 2026): public completed questionnaires do not exist. Private GRC libraries are inaccessible.** The pivot case now rests on: discrete questions (no mining), continuous buying motive, and partial stack reuse — but against same data scarcity, answer format mismatch, and crowded GRC market.

3. **The decision is a business call, not a technical one.** Both are buildable on
   what exists. The real question is which market to enter first, and that turns on
   deal value vs. deal frequency, competitive landscape, and which data you can
   actually acquire at volume — **where questionnaires no longer have a structural edge** (same scarcity, different format).

The one thing to refuse is the blended version: "we tested it on questionnaires
and it works." That sentence is true of neither product and would hide exactly the
risk we spent this week surfacing.
