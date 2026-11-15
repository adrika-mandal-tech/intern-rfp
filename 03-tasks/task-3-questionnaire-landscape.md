# Task 3 — The questionnaire landscape

**Time:** about 3 days · **Deliverable:** a research memo in `your-work/`
**Prerequisite:** read `02-evidence/2026-07-28-rfp-vs-questionnaire-product-decision.md` first.

---

## 1. The question you're answering

There's an open decision the seniors haven't made: should this product target **RFPs**,
or pivot to **questionnaires**?

By "questionnaires" we mean the standardised forms companies are constantly asked to
fill in to prove they're safe to do business with — security questionnaires, vendor
due-diligence forms, compliance attestations. Named ones include **SIG** (Standardized
Information Gathering), **CAIQ** (Consensus Assessments Initiative Questionnaire),
**VSAQ**, and generic **DDQs** (due diligence questionnaires).

The argument for a pivot, from our memo: questionnaires arrive as **discrete, pre-listed
questions**, which removes the hardest component we built (mining requirements out of
prose). Companies fill them in constantly rather than occasionally. And the data may be
far more available.

The memo's own conclusion is that **this is a business decision that needs information
nobody has gathered.** That's what you're gathering.

## 2. What we need to know

Answer as many as you can. Depth on a few beats a shallow pass over all of them.

### A. What are these things, concretely?
- Find and read real examples of a SIG, a CAIQ, and one or two other common
  questionnaires. What format do they arrive in — spreadsheet, web portal, PDF?
- How many questions? What do the questions actually look like? Include real examples.
- Are answers free text, or constrained (yes/no, pick-a-list, "describe your control")?
- **How does the answer format compare to an RFP response?** Our system drafts
  multi-paragraph prose with citations. Is that what a questionnaire even wants?

### B. Who fills them in, and how often?
- Which companies get asked? Which functions own the answering — security, compliance,
  sales?
- How often? Weekly, monthly, per-deal?
- What's the current process — a spreadsheet of past answers, a dedicated tool, or
  someone's memory?
- **How painful is it, in the words of people who do it?** Look for practitioners
  describing the work — forum posts, blog write-ups, conference talks, job descriptions.
  Quote them directly; a real complaint in someone's own words is worth more than a
  vendor's claim about the market.

### C. Is the data actually available? ← the decisive one

This is the crux of the argument for pivoting, and it may not survive contact.

- Are blank/standard questionnaire templates publicly available? (Likely yes.)
- Are **completed** ones — real answers from real companies — available anywhere?
- Could we build a golden set from public sources, the way we did for RFP?
- **Be careful with the distinction.** A blank template is a list of questions. A
  *completed* questionnaire is a list of questions with answers. Only the second is a
  knowledge base, and only the second lets us measure anything. Our own memo warns that
  a curated Q&A set is answerable by construction — so a set of completed
  questionnaires with no verified gaps in it would score ~100% and measure nothing.

If the honest answer is "completed questionnaires are just as scarce as proposals",
**say so clearly.** That finding would undercut the main argument for pivoting, and it's
exactly the kind of thing that's better discovered now than after building.

### D. Where does gap detection land?
- If a questionnaire asks "do you encrypt data at rest?", is refusing to answer even
  meaningful — or does the company simply know?
- Is a wrong answer here as dangerous as an invented fee in a bid? (A security
  attestation is a liability too — but is it the *same* liability?)

## 3. Rules

- **Public sources only.** No sign-ups, no paywalls, no trials, no contacting vendors.
- **Cite everything.** Every claim gets a URL and the date you accessed it. A memo of
  uncited assertions can't be checked and won't be used.
- **Separate what you found from what you concluded.** Facts in one section, your reading
  of them in another, clearly labelled.
- **Flag uncertainty explicitly.** "I could not determine X" is a legitimate and useful
  finding — see [../01-context/how-we-work.md](../01-context/how-we-work.md) §4.

## 4. Definition of done

A memo in `your-work/`, built from
[../04-templates/research-memo-template.md](../04-templates/research-memo-template.md),
containing:

- [ ] One section per question group above, with cited sources.
- [ ] At least three **real example questionnaires** described concretely, with question
      counts and sample questions quoted.
- [ ] A clear, direct answer to **C** — is completed-questionnaire data obtainable, yes
      or no, with the evidence.
- [ ] A short section: *what I could not determine, and what I'd need to find out.*
- [ ] A closing paragraph: **on this evidence, does the pivot argument hold up?** Your
      view, stated plainly, with reasons. You've read more about this than anyone here
      has — an honest opinion is wanted, not a neutral summary.

## 5. Watch out for

Most of what you'll find on the first page of results is **marketing** — companies
selling questionnaire-automation software describing a market they'd like you to
believe in. Their numbers ("companies spend 500 hours a year on questionnaires") are
sales material until independently sourced. Use them as leads, mark them as vendor
claims, and go looking for the practitioner's version.

---

**Next:** [task-4-competitor-landscape.md](task-4-competitor-landscape.md)
