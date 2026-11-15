# Start here

Welcome. This folder is everything you need to work on the **RFP automation** project.

You do not need to install our codebase, run our server, or get any accounts or API
keys. Everything in here works offline on your own machine. The only software you
need is a PDF viewer, a text editor, and Python (for one small self-check script).

Read this page top to bottom before anything else. It should take about ten minutes.

---

## 1. What the project is, in one paragraph

Large organisations — governments, banks, universities — buy things by publishing an
**RFP** (Request for Proposal): a long document, often 100–200 pages, that describes
what they want to buy and asks vendors hundreds of questions. Vendors who want the
business answer every question and submit a **proposal**. Writing that proposal takes
a team of people several weeks, and most of the answers are things the company has
already written in a previous proposal. We are building a system that reads an
incoming RFP, finds every question in it, searches the company's library of past
proposals for an answer, and drafts a response **with a citation to the exact page it
came from** — or, when the library genuinely has no answer, says so and sends that
question to a human instead of inventing something.

That last part is the hard part, and it is most of what this folder is about.

## 2. Why "says so" is the hard part

If the system invents an answer, the consequence is not an embarrassing typo. A
proposal is a **binding commercial document**. If it claims a capability the company
does not have, or quotes a fee nobody approved, the company can be held to it. So the
project's central engineering problem is not "can it write fluent text" — modern
language models do that easily — it is **"will it reliably refuse when it does not
know?"**

We measure that. The number we care most about is called **gap recall**: of the
questions we have verified the library genuinely cannot answer, how many did the
system correctly refuse? Right now that number is 9 out of 12. Getting it to 12 out
of 12 and *keeping* it there, on much more data than 12 rows, is the live problem.

## 3. What you'll be doing

Two tracks, in this order:

| | Task | Why it matters |
|---|---|---|
| **First** | [Expand the golden set](03-tasks/task-1-expand-golden-set.md) | The "12 verified unanswerable questions" above is the entire safety measurement. It is far too small to trust. You will grow it by hand. |
| **Second** | [Source new RFP → proposal pairs](03-tasks/task-2-source-real-pairs.md) | We own exactly **one** genuine RFP-and-its-real-proposal pair in the world. Every finding this project has came from it. A second pair roughly doubles what we can prove. |

Then, if there's time, three shorter research pieces:

- [Task 3 — the questionnaire market](03-tasks/task-3-questionnaire-landscape.md)
- [Task 4 — who else is building this](03-tasks/task-4-competitor-landscape.md)
- [Task 5 — read our explainer as a newcomer and tell us where it fails](03-tasks/task-5-explainer-review.md)

Full details, ordering and time budget: **[03-tasks/README.md](03-tasks/README.md)**.

## 4. Reading order for day one

Do these in order. Don't skip to the tasks.

1. **This page** (you're on it).
2. **[01-context/what-is-an-rfp.md](01-context/what-is-an-rfp.md)** — the domain, in plain
   language. What an RFP actually looks like, what a proposal looks like, what a
   compliance matrix is. ~15 min.
3. **[01-context/RFP_AUTOMATION_EXPLAINER.html](01-context/RFP_AUTOMATION_EXPLAINER.html)** —
   double-click it, it opens in your browser and works offline. This is the explainer
   we wrote for the wider team. Every section reads twice: plain language first, then
   the engineering detail. **Read the plain-language lane all the way through first**;
   come back for the engineering lane later. ~45 min.
4. **Open the two PDFs in [05-source-docs/](05-source-docs/)** and skim them — the
   Delaware RFP (127 pp) and the U.S. Bank proposal (214 pp). You do not need to read
   them. Get a feel for the shape: turn to page 19 of the RFP and read a few
   questions, then turn to page 13 of the proposal and read a few answers. Ten minutes
   with the real documents is worth more than an hour of description.
5. **[01-context/how-we-work.md](01-context/how-we-work.md)** — the working standards on
   this project. Short, and it is the thing most worth internalising. ~10 min.
6. **[01-context/glossary.md](01-context/glossary.md)** — skim it, then keep it open as a
   reference while you work.

That's day one. Don't start annotating on day one.

## 5. What's in this folder

```
intern-rfp/
├── START_HERE.md              you are here
├── 01-context/                what the project is and how we work
│   ├── what-is-an-rfp.md         the domain in plain language
│   ├── RFP_AUTOMATION_EXPLAINER.html   the team explainer (open in a browser)
│   ├── how-we-work.md            our working standards — read this properly
│   └── glossary.md               every term you'll hit, defined
├── 02-evidence/               what we have already measured
│   ├── README.md                 read this before the files it describes
│   ├── RFP_RETRIEVAL_BASELINE_2026-07-26.md      the core measurement
│   ├── 2026-07-28-rfp-vs-questionnaire-...md     the open product decision
│   ├── RFP_MULTIDOC_ROUTING_P2_0_2026-07-28.md   does it hold on a library?
│   ├── golden_set_50rows.jsonl                   the 50 rows you are extending
│   └── example_annotations_C.jsonl               worked examples to copy the style of
├── 03-tasks/                  your work, one brief per task
├── 04-templates/              start your deliverables from these
├── 05-source-docs/            the two real PDFs
├── tools/                     the self-check script and the page text it reads
└── your-work/                 put everything you produce in here
```

## 6. Rules of the road

**Put everything you produce in `your-work/`.** Don't edit files anywhere else in this
folder — if you think something here is wrong, that's a finding, and you should write
it down rather than silently fix it. (Finding errors in this pack is genuinely
welcome. See Task 5.)

**Never guess in a deliverable.** If you don't know something, the correct output is
"I don't know, here's what I checked and why it was inconclusive." That sentence is
worth more to us than a confident wrong answer, and this project has been burned by
confident wrong answers repeatedly — see `how-we-work.md`.

**Ask early.** If you're stuck for more than about half a day, ask. Being stuck
quietly is the only genuinely expensive mistake available to you here.

**Keep a daily log.** Start it from
[04-templates/research-log-template.md](04-templates/research-log-template.md). Two or
three lines a day: what you did, what you found, what blocked you. It costs you five
minutes and it is what makes your work reviewable.

## 7. One-time setup (five minutes)

You need Python 3.9 or newer. Check:

```bash
python --version
```

Then, from inside this folder, confirm the self-check tool runs:

```bash
python tools/verify_quotes.py --claims 02-evidence/example_annotations_C.jsonl
```

You should see:

```
41/41 quote-bearing claims verified against the source pages
  (9 'none' verdicts carry no quote by construction and are not scored)
```

If you see that, you're set up correctly — that command just re-checked 50 real
annotations against 214 pages of PDF text. If it errors, that's a setup problem worth
asking about immediately, because Task 1 depends on it.

(The page text it reads lives in `tools/work/` and ships with this pack. If you ever
need to regenerate it, `python tools/extract_pages.py` does that, but it needs
`pdfplumber` installed and you shouldn't normally need to.)

---

**Next:** [01-context/what-is-an-rfp.md](01-context/what-is-an-rfp.md)
