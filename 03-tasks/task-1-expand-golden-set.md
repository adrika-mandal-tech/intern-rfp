# Task 1 — Expand the golden set

**Time:** about 4–5 days · **Deliverable:** 60 annotated rows in `your-work/`
**Everything you need ships with this pack. No accounts, no server, no internet.**

---

## 1. What you're doing, in one sentence

For each of 60 requirements from the Delaware RFP, you will read the 214-page U.S. Bank
proposal, decide whether it answers that requirement, and record your decision with a
verbatim quote and a page number.

## 2. Why it matters

Our entire safety claim — "the system correctly refuses when it doesn't know" — is
measured against **12 hand-verified rows**. One of the most important findings the
project has rests on **a single row**.

That's not enough to know anything. A safety property measured on twelve examples can
pass by luck, and we would not be able to tell. The report itself says so:

> *"n = 12 true negatives is a small safety sample and the whole effect rests on
> recovering one row. The eval harness needs far more verified negatives before this is
> load-bearing."*

You are producing exactly that. When you're done, the safety sample roughly triples.

**And it has to be done by a human.** The golden set is the ruler we measure the system
with. If we let the system produce its own ruler, it scores near-perfect and we learn
nothing. This is a genuine constraint, not busywork handed downward: the reason nobody
has done it is that it can only be done by someone reading the documents.

## 3. Before you start

Make sure you have:

- [ ] Read [../01-context/what-is-an-rfp.md](../01-context/what-is-an-rfp.md), especially
      §5 (why similarity can't detect gaps) and §7 (the scope trap).
- [ ] Opened `02-evidence/golden_set_50rows.jsonl` and read fifteen or twenty rows.
      **This is your model for what good output looks like.**
- [ ] Run the setup check from [../START_HERE.md](../START_HERE.md) §7 successfully.
- [ ] Both PDFs from `05-source-docs/` open in your PDF viewer.

## 4. Your worklists

Two files, already drawn for you, in `your-work/`:

| File | Rows | What it is |
|---|---|---|
| `worklist_A_random.jsonl` | 40 | A fair, stratified sample across the whole RFP |
| `worklist_B_lockbox.jsonl` | 20 | Lockbox questionnaire only — a deliberately biased draw |

**Why they're separate, and why you must keep them separate.** List A is a fair sample,
so a score computed over it describes the RFP as a whole. List B deliberately
over-samples the Lockbox questionnaire, because U.S. Bank didn't bid lockbox — those
rows are the cheapest source of the verified `none` verdicts we're short of. That bias
is exactly what makes B useful for building a safety sample and completely invalid for
computing a rate. "Gap detection is 95%" computed over list B would be an impressive
number about nothing.

Do **not** merge the files. Do **not** report a combined percentage.

Each row arrives pre-filled with the requirement and blank fields for you to complete.

## 5. The three verdicts

For each requirement, decide which one the proposal does:

### `answered`
The proposal contains text that answers the requirement — the substance of what was
asked, for the service that was asked about. Not necessarily well or completely, but a
reader would agree the question was addressed.

### `partial`
Part of the requirement is answered and part isn't. Very common, because requirements
frequently ask two things in one sentence.

> Real example — `R011`: *"How often will the primary relationship manager attend
> on-site meetings…? Describe a typical meeting agenda for this on-site meeting."*
> The proposal gives the cadence ("quarterly, plus a monthly touch-point call") but only
> points at sample agendas in an exhibit that isn't part of the document. Cadence
> answered, agenda not. → `partial`.

### `none`
The proposal does not answer it at all.

**A `none` verdict must carry `page: 0` and an empty `quote`.** You're asserting an
absence, so there's nothing to quote — and the checker will reject a `none` that carries
a quote.

`none` is not a failure or a cop-out. **These are our most valuable rows.** Say it
plainly when it's true.

## 6. The three rules that decide the hard cases

These aren't invented for you — they're the rules a human adjudicator applied to
resolve the disagreements in the existing 50 rows. Apply the same ones so your rows are
consistent with the set you're extending.

### Rule 1 — Different service line ⇒ `none`

If the requirement is scoped to a service the vendor didn't bid, and the proposal
describes that same capability for a *different* service, the verdict is **`none`** —
not `partial`.

> The proposal has an excellent disaster-recovery section for general banking. A
> **lockbox** disaster-recovery question is still `none`. A commitment about the general
> banking platform is not a commitment about lockbox.

Why so strict: this exact substitution is the system's dominant failure mode. If the
golden set blesses it, we'd be training and scoring the system to do the thing we most
need it not to do.

**Only the requirement's own scope decides this** — not whether the headings match. RFP
headings and proposal headings come from different documents with unrelated taxonomies,
so they nearly always differ. A differing heading is normal and means nothing on its
own. (We once shipped a rule that treated it as meaningful, and it started refusing 18
of 38 answerable requirements.)

### Rule 2 — Answered but stale ⇒ still `answered`

The proposal is from 2018. It names people who've moved on, quotes asset figures that
have changed, says "available in the fall of 2018". **Staleness does not make it
`none`.** The requirement was answered; the content simply needs refreshing. We're
measuring whether the library *contains* an answer, not whether it's publication-ready.

### Rule 3 — The answer is in an exhibit ⇒ `partial`

If the proposal says "see the sample agendas in the Exhibits section" and the exhibit
isn't in the document, that's **`partial`** — a genuine pointer to real content, but
nothing our system could retrieve. We measure what's findable in the text we actually
have.

### When none of the rules resolve it

**Don't force a verdict.** Record your best judgement, set `confidence` to `low`, and
explain the tension in `reasoning`. Then add the row to your questions list. Genuinely
ambiguous rows are findings — the existing set has five, and each one exposed a real
definitional question about the product. Flagging one is a good outcome, not a failure.

## 7. How to do it — the loop

For each row:

**1. Read the requirement.** Note what it actually asks. If it asks two things, note
both — you'll need that for `partial`.

**2. Note its service line.** General Banking? Lockbox? Purchasing Card? It's in the
`section` field. Rule 1 depends on this.

**3. Search the proposal.** Ctrl-F in your PDF viewer. Practical technique:

   - Search the *distinctive nouns*, not the whole question. For "How are charges
     assessed for receiving addenda information?", search `addenda`, not the sentence.
   - Try two or three different terms before concluding it's absent. Vendors use their
     own vocabulary — "remittance processing" where the RFP says "lockbox".
   - Use the proposal's table of contents to jump to the right service section first,
     then search within it.
   - **Check the section heading of every hit before trusting it.** The proposal repeats
     near-identical boilerplate across service components; a keyword search lands you in
     the wrong one constantly. This is the single most common way to get a row wrong.

**4. Decide the verdict**, applying §6 where relevant.

**5. Copy the quote — literally.** Select the text in the PDF and paste it. Don't retype
it, don't tidy it, don't fix the line breaks. The checker compares it against the PDF's
text layer.

   - **25 characters minimum.** A short quote like "the State" would "match" almost any
     page and makes the check meaningless.
   - Quote the sentence that *does the answering*, not the heading above it.

**6. Record the page — from your PDF viewer's page counter,** not the number printed at
the bottom of the page. In this proposal the printed footer runs one behind. Everywhere
in this project, "page" means the PDF page index.

**7. Write the `reasoning`.** One or two sentences: what you found and why it gives that
verdict. For `partial`, say which half is missing. For `none`, say what you searched for.

> Real example of good reasoning, from the existing set:
> *"Meeting cadence is answered directly (quarterly plus monthly teleconference), but
> the requested typical agenda is only pointed to as Sample Agendas in the un-extracted
> Exhibits Section, and the on-site versus virtual split is never addressed."*

Someone can check that without asking you anything. That's the bar.

**8. Set `confidence`** to `high`, `medium` or `low`. Be honest — `low` is useful signal,
not an admission.

### A filled row looks like this

```json
{"req_id": "R011", "rfp_page": 20, "section": "Vendor Questionnaire / B. Key Proposed Personnel", "class": "team", "requirement": "After the initial transition, how often will the primary relationship manager attend on-site meetings...", "doc": "kb", "verdict": "partial", "page": 20, "quote": "We will meet with the State quarterly, and also suggest a monthly touch point teleconference call to\ndiscuss any outstanding issues. Sample Agendas are included in the Exhibits Section", "confidence": "high", "reasoning": "Cadence is answered directly; the requested agenda is only pointed to in an exhibit that is not part of the document."}
```

Keep the pre-filled fields as they are. Fill in `verdict`, `page`, `quote`,
`confidence`, `reasoning`.

## 8. Check your own work — every day

At the end of each day, run:

```bash
python tools/verify_quotes.py --claims your-work/worklist_A_random.jsonl
```

It checks every quote against the actual PDF text and reports one of:

| Verdict | Meaning | What to do |
|---|---|---|
| `verified` | The quote is on the page you claimed | Nothing |
| `off_by` | The quote is real but on a *different* page | Fix the page number. Usually the footer-vs-index slip |
| `not_found` | The text isn't anywhere in the document | **Fix this row.** Something was retyped, mangled, or the quote spans a page break |
| `empty_quote` | No quote, or under 25 characters | Add a real quote |
| `n/a` | A `none` verdict, nothing to check | Nothing — this is correct |

**Run it daily, not at the end.** If you're making a systematic mistake — say, copying
quotes in a way that breaks across line wraps — you want to find that after ten rows,
not after sixty.

A `not_found` is not a telling-off. It's the tool doing its job. The distinction between
a golden set and a pile of plausible assertions is precisely that one of them gets
checked.

## 9. Definition of done

- [ ] All 40 rows of `worklist_A_random.jsonl` have a verdict, confidence and reasoning.
- [ ] All 20 rows of `worklist_B_lockbox.jsonl` likewise.
- [ ] `verify_quotes.py` reports **zero `not_found`** and **zero `empty_quote`** on both
      files.
- [ ] Every `none` row has `page: 0` and an empty quote.
- [ ] Every row has non-empty `reasoning`.
- [ ] A short summary written from
      [../04-templates/annotation-summary-template.md](../04-templates/annotation-summary-template.md):
      verdict counts per list (**separately**), how many rows you marked `low` confidence,
      the rows you want a second opinion on, and any traps you hit that aren't listed in
      §7.

That last item is a real deliverable, not paperwork. Both previous annotators found
traps nobody had documented, and those findings changed how the extractor gets built.

## 10. Pace, and what to do if you're stuck

Expect 15–20 minutes per row at first, dropping to 5–10 once you know the proposal's
layout. Sixty rows is roughly four days at a steady pace. **Don't rush** — a wrong row
in a golden set is worse than a missing one, because it silently corrupts every future
measurement taken against it.

If a single row is eating more than 20 minutes: mark it `low` confidence, write down
what makes it hard, move on, and bring it to the questions list. Do that rather than
sinking an hour — the fact that a row is hard to call is itself information we want.

---

**Next:** [task-2-source-real-pairs.md](task-2-source-real-pairs.md)
