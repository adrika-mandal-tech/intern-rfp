"""Mechanically verify page-level evidence claims against the source PDF text.

This is what separates a golden set from a pile of plausible assertions. An
annotator claiming "requirement R012 is answered on page 47" is an assertion. The
same claim carrying a verbatim quote is *checkable*: either that text is on page
47 or it is not, and this script decides which.

    python bench/rfp_finance/verify_quotes.py --claims work/evidence_X.jsonl
    python bench/rfp_finance/verify_quotes.py --claims ... --json

Input JSONL, one claim per line:
    {"req_id": "R012", "doc": "kb", "page": 47, "quote": "<verbatim span>"}

`doc` selects the page-text file: "kb" or "rfp" -> work/{doc}_pages.json.

Verdicts:
    verified        the quote is on the claimed page
    off_by          the quote is on a nearby page instead (page numbering slip;
                    the evidence is real but the label needs correcting)
    not_found       the quote is nowhere in the document — treat the claim as
                    fabricated or badly mangled, and never promote it
    empty_quote     no quote supplied, so the claim is unverifiable by design

Matching is deliberately lenient about *form* and strict about *content*: PDF text
layers vary in whitespace, hyphenation and quote glyphs, and failing a true claim
over a curly apostrophe would push people to stop quoting. It is never lenient
about whether the words are present.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")

# How far either side of the claimed page to look before declaring not_found.
NEARBY = 2
# Quotes shorter than this cannot discriminate — "the State" would "verify"
# against almost any page and would make the check theatre.
MIN_QUOTE_CHARS = 25


def normalize(text: str) -> str:
    """Collapse the incidental differences between a PDF text layer and a quote.

    Unicode-normalize, fold smart punctuation and dashes to ASCII, join words
    broken across a line by a hyphen, then collapse all whitespace. Case is
    preserved — a quote should reproduce the source, and casefolding here would
    hide sloppy transcription.
    """
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = re.sub(r"[‐-―]", "-", text)
    text = re.sub(r"-\s*\n\s*", "", text)  # de-hyphenate across line breaks
    return re.sub(r"\s+", " ", text).strip()


def load_pages(doc: str) -> dict[int, str]:
    path = os.path.join(WORK, f"{doc}_pages.json")
    with open(path, encoding="utf-8") as fh:
        return {p["page"]: normalize(p["text"]) for p in json.load(fh)}


def check(claim: dict, pages: dict[int, str]) -> tuple[str, str]:
    # A "none" verdict asserts the document does NOT answer the requirement, so it
    # has no quote by construction. Reporting that as a failure would penalise the
    # honest gap — the one answer we most need annotators to feel safe giving.
    if str(claim.get("verdict", "")).lower() == "none":
        if claim.get("quote") or int(claim.get("page", 0)):
            return "not_found", "verdict 'none' must carry page 0 and an empty quote"
        return "n/a", "verdict 'none': nothing to verify"

    quote = normalize(str(claim.get("quote", "")))
    if not quote:
        return "empty_quote", "no quote supplied"
    if len(quote) < MIN_QUOTE_CHARS:
        return "empty_quote", f"quote too short to discriminate ({len(quote)} chars)"

    claimed = int(claim.get("page", 0))
    if claimed in pages and quote in pages[claimed]:
        return "verified", ""

    for offset in range(1, NEARBY + 1):
        for candidate in (claimed - offset, claimed + offset):
            if candidate in pages and quote in pages[candidate]:
                return "off_by", f"found on page {candidate}, claimed {claimed}"

    for page, text in pages.items():
        if quote in text:
            return "off_by", f"found on page {page}, claimed {claimed} (far)"

    return "not_found", "quote does not appear anywhere in the document"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claims", required=True, help="JSONL of evidence claims")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    claims = []
    with open(args.claims, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                claims.append(json.loads(line))

    caches: dict[str, dict[int, str]] = {}
    results = []
    for claim in claims:
        doc = claim.get("doc", "kb")
        if doc not in caches:
            caches[doc] = load_pages(doc)
        verdict, detail = check(claim, caches[doc])
        results.append({**claim, "verdict": verdict, "detail": detail})

    counts: dict[str, int] = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1

    if args.json:
        print(json.dumps({"counts": counts, "results": results}, indent=2))
    else:
        for r in results:
            # n/a rows are expected and numerous; listing them buries the real
            # problems in noise. They are still counted in the summary.
            if r["verdict"] not in ("verified", "n/a"):
                quote = str(r.get("quote", ""))[:70].replace("\n", " ")
                print(
                    f"{r['verdict']:<12} {r.get('req_id', '?'):<8} "
                    f"p{r.get('page', '?'):<5} {r['detail']}\n"
                    f"{'':<13}quote: {quote}..."
                )
        total = len(results)
        ok = counts.get("verified", 0)
        na = counts.get("n/a", 0)
        checkable = total - na
        print(f"\n{ok}/{checkable} quote-bearing claims verified against the source pages")
        if na:
            print(f"  ({na} 'none' verdicts carry no quote by construction and are not scored)")
        for verdict in ("off_by", "not_found", "empty_quote"):
            if counts.get(verdict):
                print(f"  {verdict}: {counts[verdict]}")
        if counts.get("not_found"):
            # ASCII only: the Windows console codepage mangles non-ASCII
            # punctuation, and a garbled warning is one people learn to skip.
            print(
                "\nnot_found means the quoted text is absent from the document. "
                "Do not promote those\nclaims to the golden set on any amount of "
                "annotator agreement. Agreement is not evidence."
            )

    return 1 if counts.get("not_found") or counts.get("empty_quote") else 0


if __name__ == "__main__":
    sys.exit(main())
