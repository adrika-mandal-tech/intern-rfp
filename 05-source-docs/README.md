# The source documents

Two real, public documents. Everything this project has measured came from them.

---

### `RFP_Delaware_BankingServices_TRE25101.pdf` — 127 pages

The State of Delaware's Request for Proposal for statewide banking services,
solicitation `TRE25101-BANKINGSVC`. The buyer's document: what it wants, and every
question it's asking vendors to answer.

**Where the questions are:**

| Pages | Content |
|---|---|
| 1–18 | Administrative and legal terms — deadlines, contract conditions, insurance |
| **19–51** | **Vendor Questionnaire** — where most requirements live |
| 52+ | Further questionnaires, one per service line |
| Attachments | Pricing sheets, forms, exhibits |

We extracted **622 discrete requirements** from it. They're in
`tools/work/requirements_pp19-51.jsonl` and `tools/work/requirements_pp52plus.jsonl`.

### `KB_USBank_Proposal_DE_TRE18101.pdf` — 214 pages

**U.S. Bank's genuine submitted proposal** to the same buyer for the same contract
line, seven years earlier (`TRE18101-BANKINGSVC`). Not a template, not a sample — a
document a real vendor really submitted for a real contract.

This is the "knowledge base": the past proposal the system searches for answers.

**The single most important thing to know about it:** U.S. Bank **did not bid Lockbox
Services**. The pricing and personnel tables say "Lockbox Services: Not applicable", and
the word "lockbox" appears six times in 214 pages, all incidental. So every lockbox
question in the 2025 RFP is a verified gap.

That's not a flaw in the data — it's the most valuable property it has. It's the only
reason we can measure whether the system correctly refuses. Two independent annotators
found it separately, from the same evidence.

---

## Why this pair is unusual

Same buyer, same contract line, seven years apart — a genuine re-bid scenario, which is
exactly the situation the product is for.

The 2025 RFP recycles the 2018 questionnaire nearly word-for-word in places, so many
requirements have a direct counterpart in the proposal. Where the seven-year gap shows
up, it's *staleness* (named staff who've moved on, dated asset figures) rather than
missing coverage. The one big hole is lockbox — and that's a **scope** gap, not an age
gap. It would be equally absent if the proposal had been written last week, because the
bank simply chose not to bid that service.

Genuine submitted proposals are almost never public. We found this one because Delaware
publishes the proposals it receives. It's the only pair we have, which is why
[Task 2](../03-tasks/task-2-source-real-pairs.md) exists.

---

## Working with them

- **Page numbers mean the PDF page index** — what your viewer's counter shows — not the
  number printed at the bottom of the page. They disagree in the proposal; the printed
  footer runs one behind.
- Both have complete text layers, so Ctrl-F works throughout. No OCR needed.
- The extracted per-page text is in `tools/work/kb_pages.json` and
  `tools/work/rfp_pages.json` — that's what `verify_quotes.py` checks against.
- The proposal repeats near-identical boilerplate across service components. **Always
  check the section heading of a search hit** before trusting it; landing in the wrong
  component is the most common annotation error.
