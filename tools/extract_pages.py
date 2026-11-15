"""Extract a per-page text layer from the two source PDFs.

    python tools/extract_pages.py

Writes tools/work/kb_pages.json and tools/work/rfp_pages.json in the shape
verify_quotes.py expects:

    [{"page": 1, "text": "..."}, {"page": 2, "text": "..."}, ...]

`page` is the 1-based PDF page index, NOT the number printed in the page footer.
Those two disagree in the U.S. Bank proposal -- the printed footer runs one
behind -- and every page number in this project means the PDF index. If you open
the PDF in a viewer, use the viewer's page counter, not the printed footer.

You should not normally need to run this: the output files ship with the package.
It is here so you can regenerate them, and so you can see exactly where the text
being checked comes from.
"""

from __future__ import annotations

import json
import os
import sys

try:
    import pdfplumber
except ImportError:
    sys.exit("pdfplumber is not installed. Run: pip install pdfplumber")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WORK = os.path.join(HERE, "work")
SRC = os.path.join(ROOT, "05-source-docs")

DOCS = {
    "rfp": "RFP_Delaware_BankingServices_TRE25101.pdf",
    "kb": "KB_USBank_Proposal_DE_TRE18101.pdf",
}


def main() -> int:
    os.makedirs(WORK, exist_ok=True)
    for name, filename in DOCS.items():
        path = os.path.join(SRC, filename)
        if not os.path.exists(path):
            print(f"MISSING {path}")
            return 1
        pages = []
        with pdfplumber.open(path) as pdf:
            for index, page in enumerate(pdf.pages, start=1):
                pages.append({"page": index, "text": page.extract_text() or ""})
        out = os.path.join(WORK, f"{name}_pages.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(pages, fh, ensure_ascii=False)
        empty = sum(1 for p in pages if not p["text"].strip())
        print(f"{name}: {len(pages)} pages -> {out}  ({empty} with no text layer)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
