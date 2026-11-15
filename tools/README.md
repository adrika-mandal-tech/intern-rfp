# Tools

Three small Python scripts. All standard library except `extract_pages.py`, which you
almost certainly won't need to run. No accounts, no network, no configuration.

---

## `verify_quotes.py` — the one you'll use daily

Checks that every quote in your annotations actually appears on the page you claimed.

```bash
python tools/verify_quotes.py --claims your-work/worklist_A_random.jsonl
```

Add `--json` for machine-readable output.

| Verdict | Meaning |
|---|---|
| `verified` | The quote is on the claimed page |
| `off_by` | The quote is real, but on a different page — fix the page number |
| `not_found` | The text isn't anywhere in the document — **fix the row** |
| `empty_quote` | No quote, or under 25 characters |
| `n/a` | A `none` verdict, which carries no quote by design |

**Run it daily, not at the end.** A systematic mistake in how you copy quotes is much
cheaper to find after ten rows than after sixty.

It's deliberately lenient about *form* and strict about *content*: it normalises smart
quotes, dashes, line-break hyphenation and whitespace, because failing a true claim over
a curly apostrophe would just teach people to stop quoting. It is never lenient about
whether the words are there.

The 25-character minimum exists because a short quote like "the State" would "verify"
against almost any page, which would make the whole check theatre.

## `make_worklist.py` — already run for you

Draws the two annotation worklists in `your-work/`. They ship pre-drawn, so you don't
need to run this. It's here so the sample is reproducible and so you can see exactly how
it was drawn — which matters, because how a sample was drawn decides what its scores are
allowed to mean. The docstring explains why list A and list B must stay separate.

## `extract_pages.py` — already run for you

Rebuilds `work/kb_pages.json` and `work/rfp_pages.json` from the PDFs. Those ship with
this pack. Only needed if they're lost or you swap in a different document — and it
needs `pdfplumber` installed, which nothing else here does.

---

## `work/`

| File | What it is |
|---|---|
| `kb_pages.json` | Per-page text of the U.S. Bank proposal (214 pages) |
| `rfp_pages.json` | Per-page text of the Delaware RFP (127 pages) |
| `requirements_pp19-51.jsonl` | 496 requirements mined from the RFP's main questionnaire |
| `requirements_pp52plus.jsonl` | 126 more, from the later per-service questionnaires |

`page` in these files is always the **PDF page index**, 1-based — not the number printed
in the page footer.

The two requirements files are the source your worklists were drawn from. Worth opening
if you want to see the full 622, or to look up neighbouring requirements for context
while annotating.
