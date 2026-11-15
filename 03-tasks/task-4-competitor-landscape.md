# Task 4 — Who else is building this

**Time:** about 2–3 days · **Deliverable:** a comparison memo in `your-work/`

---

## 1. The question

We are not the first people to think "software should help write proposals." There's an
established category of RFP-response tooling, and newer AI-native entrants.

We need to know what exists, what it claims, and — most importantly — **what it doesn't
do.** The decision this feeds is whether there's a real gap to build into, and if so,
what it is.

## 2. Who to look at

Start here and expand as you find others:

- **Responsive** (formerly RFPIO)
- **Loopio**
- **Qvidian** (Upland)
- **AutogenAI**
- **Arphie**
- Any AI-native entrant you turn up while researching — the space moves quickly and the
  newest ones are often the most relevant

If Task 3 came first and turned up questionnaire-automation vendors, note where the two
categories overlap. Several companies sell into both, which is itself a finding.

## 3. What to find out about each

- **What it claims to do**, in its own words. Quote the actual claim.
- **Pricing**, if public. Note it if it isn't — an unpublished price usually implies
  enterprise sales, which tells you something about the buyer.
- **Who it sells to** — company size, industries, which department buys it.
- **How does it get answers?** A searchable library of past answers? Generation? Both?
- **⭐ How does it handle not knowing?** This is the one to dig hardest on. Does it flag
  gaps? Cite sources? Have a human review step? Say anything at all about hallucination?
  This is where our project has spent nearly all its effort, so it's where we most need
  to know whether we're differentiated or reinventing.
- **What it explicitly does *not* do.** Often the most informative thing on a product
  page, and usually implied rather than stated.

## 4. The questions the memo has to answer

1. **Is the "answer library" idea already standard?** (We suspect yes.)
2. **Does anyone treat gap detection and refusal as a first-class feature** — or is it
   universally treated as the user's problem?
3. **Does anyone publish measurements?** Accuracy, refusal rates, citation validity,
   anything at all — or is it entirely unquantified marketing claims?
4. **Where's the genuine gap**, if there is one?
5. **Is anyone doing the requirement-mining half** — taking raw RFP prose and extracting
   the requirements — or does everyone start from a list the user has already made?

Question 5 matters more than it looks. If every existing tool assumes the user hands it
a clean list of questions, then mining from prose is either a real differentiator or a
problem everyone has decided isn't worth solving. Either answer is useful; we currently
don't know which it is.

## 5. Rules

- **Public information only.** No demos, no trials, no sales calls, no sign-ups.
- **Quote and cite.** Every claim gets a source URL and an access date.
- **Mark vendor claims as vendor claims.** "Responsive says X" is a fact about
  Responsive's marketing. "Responsive does X" is a much stronger statement you probably
  can't support. Keep the two visibly separate throughout.
- **Don't editorialise about competitors' quality.** You can't assess a product you
  haven't used. Report what they claim and what they're silent about; the silences are
  the interesting part.

## 6. Definition of done

A memo in `your-work/`, from
[../04-templates/research-memo-template.md](../04-templates/research-memo-template.md):

- [ ] A comparison table — one row per product, columns for the §3 items.
- [ ] A narrative section per product, two or three paragraphs, cited.
- [ ] Direct answers to all five questions in §4.
- [ ] A section on **what nobody seems to be doing**, with your reasoning.
- [ ] A "what I couldn't determine" section.

## 7. A note on reading marketing

Every page you read is written to make a sale, and the useful signal is usually in what
it *avoids*. If a product page talks at length about speed and content libraries and
never mentions accuracy, citations or review, that's information — it suggests the
buyers being targeted aren't asking about those things.

Note those silences explicitly. They're the most decision-relevant thing you'll produce
in this task.

---

**Next:** [task-5-explainer-review.md](task-5-explainer-review.md)
