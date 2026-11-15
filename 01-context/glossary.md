# Glossary

Keep this open while you work. Terms are grouped by where you'll meet them, not
alphabetically — but there's an index at the bottom.

---

## The domain

**RFP — Request for Proposal.** A document a buyer publishes describing what it wants
to purchase and asking vendors to respond. Typically 100–200 pages. Also seen: **RFQ**
(Request for Quote, price-focused), **RFI** (Request for Information, earlier and
looser), **ITB/IFB** (Invitation to Bid), **Tender** (the usual word outside the US),
**SOQ** (Statement of Qualifications). For our purposes they're all "a buyer asking
vendors questions".

**Proposal / bid / response.** The vendor's answer to an RFP. A single document,
usually longer than the RFP, answering every requirement. When we say "genuine
submitted proposal" we mean a document a real vendor actually submitted for a real
contract — not a template, sample, or marketing brochure.

**Requirement.** One thing in the RFP that the vendor must respond to. We say
*requirement* rather than *question* because many are imperatives ("Provide a brief
history of your organization") rather than questions. The Delaware RFP contains 622.

**Addendum.** An amendment issued after an RFP is published, changing or clarifying it.
Common in government procurement, and awkward for us because an amended RFP is nearly
identical to the original by construction.

**Compliance matrix.** The output artifact: one row per requirement showing its status,
the drafted answer, and the citation. It's what a bid manager works from, and its main
job is proving nothing was missed — buyers disqualify bids for unanswered requirements.

**Buyer / issuer.** The organisation publishing the RFP (here: the State of Delaware).
**Vendor / bidder.** The organisation responding (here: U.S. Bank).

**Service line / component.** A distinct service within one RFP — general banking,
lockbox, purchasing card, ePayables. A vendor may bid some and not others, and this
distinction is load-bearing for us: see **scope substitution** below.

**Lockbox.** A banking service where the bank receives and processes a customer's
incoming mail payments. You'll see it constantly, because U.S. Bank *didn't bid it* in
2018 — making every lockbox question in the 2025 RFP a verified gap.

## Our system

**Knowledge base / KB / library.** The collection of past proposals the system searches
for answers. In our test data the "library" is one document: the U.S. Bank proposal.

**Mining.** Extracting the discrete requirements out of RFP prose. Hard, because
requirements are buried in narrative text, numbered inconsistently, and split across
page breaks.

**Retrieval.** Searching the library for text relevant to a requirement.

**Grounding / grounded answer.** An answer traceable to specific source text, with a
citation. The opposite of a **hallucination** — fluent text the model invented, which
is what makes an ungrounded system unusable for a binding document.

**Citation.** A pointer to the document and page an answer came from. An **invalid
citation** points at a page that doesn't support the claim (or doesn't exist). We
measure these; the current count is zero.

**Gap.** A requirement the library genuinely cannot answer. The correct behaviour is to
say so and route it to a human.

**Gap detection / gap recall.** Of the requirements verified to be unanswerable, the
fraction the system correctly refused. **This is the project's headline safety metric.**
Currently 9/12 on a realistic library.

**False refusal.** The opposite error — the system refuses a requirement it *could*
have answered. Not a safety problem, but a value problem: too many and people stop
using it. Currently 8 of 38.

**Human routing.** Deliberately sending a requirement to a person rather than drafting
it. Some classes (pricing, legal, admin) are routed to humans *by policy*, regardless
of whether an answer exists — nobody wants an AI quoting a fee.

**Scope substitution.** Answering a question about service B using content about
service A. The dominant failure mode; see §7 of [what-is-an-rfp.md](what-is-an-rfp.md).

## Measurement

**Golden set.** A hand-verified set of correct answers used to score the system. Ours
has 50 rows. Two properties make it trustworthy: it was built by **humans reading the
PDFs**, never by the system it scores (otherwise it just measures the system against
itself), and every claim carries a **verbatim quote** that a script re-checks.

**True negative.** A golden-set row verified to have **no** answer in the library. Rare,
expensive to produce, and the most valuable kind of row we own — a golden set without
them cannot detect a system that answers everything. We have 12.

**Verdict.** The label an annotator gives a requirement: `answered`, `partial`, or
`none`. Definitions and boundary rules are in
[../03-tasks/task-1-expand-golden-set.md](../03-tasks/task-1-expand-golden-set.md).

**Annotator.** A person (or model) producing golden-set labels. We run **two independent
annotators** over the same rows and compare — agreement is evidence, a single opinion
isn't. Our two agreed on 37 of 41 overlapping rows.

**Corroborated / disputed / single-annotator.** Row provenance tiers: both annotators
agreed / they disagreed and a human adjudicated / only one annotator saw it. Reported
separately, because a single-annotator row shouldn't carry a headline number.

**Adjudication.** A human resolving a disagreement by a stated rule, with the rule
recorded on the row so the decision is reviewable.

**Recall@k.** Of the questions where the right page exists, how often is it in the top
*k* search results? We measure at k = 1, 3, 5, 10. Ours: 0.789 / 0.868 / 0.895 / 0.947.

**Variance / noise band.** How much a number moves when you re-run without changing
anything. Retrieval scores here are deterministic (zero variance across five runs), so
any movement is real signal. Model-judged scores are not, so small differences there
mean nothing.

**Baseline.** A recorded measurement of the current state, taken before changes, so you
can tell whether a change helped.

## Technical terms you'll encounter but don't need to master

**Embedding.** A numeric representation of text, such that similar text gets similar
numbers. How the search finds relevant passages.

**Similarity / cosine score.** How close two embeddings are, roughly 0 to 1. §5 of
[what-is-an-rfp.md](what-is-an-rfp.md) explains why this cannot detect gaps.

**Chunk.** A passage of a document (a few hundred to a couple of thousand characters),
the unit that gets embedded and retrieved.

**LLM.** Large language model — the component that reads retrieved excerpts, judges
whether they answer the requirement, and drafts prose.

**JSONL.** A text file with one JSON object per line. The annotation format. Readable
in any text editor; each line stands alone, so files merge and diff cleanly.

**Namespace.** How our system keeps one customer's data separate from another's.

**no lockbox response** typically means that an application, payment, or data access request sent to a processing facility (such as a USCIS immigration lockbox or a cloud security system) has not received an acknowledgment, receipt, or approval within the expected timeframe

**Grasph.** The name of our underlying platform — the graph database and document
pipeline this product is built inside.

---

## Index

addendum · adjudication · annotator · baseline · bid · buyer · chunk · citation ·
compliance matrix · corroborated · cosine · disputed · embedding · false refusal · gap ·
gap recall · golden set · Grasph · grounding · hallucination · human routing · ITB ·
JSONL · knowledge base · library · LLM · lockbox · mining · namespace · proposal ·
recall@k · requirement · retrieval · RFI · RFP · RFQ · scope substitution · service
line · similarity · SOQ · tender · true negative · variance · vendor · verdict
