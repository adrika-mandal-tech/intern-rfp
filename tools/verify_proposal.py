#!/usr/bin/env python3
"""
Verify a downloaded proposal/RFP meets Task 2 §7 criteria.

Usage:
    python tools/verify_proposal.py your-work/found-documents/PROPOSAL_*.pdf
    python tools/verify_proposal.py your-work/found-documents/RFP_*.pdf
"""

import sys
import re
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("Install PyPDF2: pip install PyPDF2")
    sys.exit(1)


def extract_text(pdf_path: Path, max_pages: int = 10) -> str:
    """Extract text from first N pages of PDF."""
    text_parts = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages[:max_pages]):
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def verify_proposal(pdf_path: Path) -> dict:
    """Run Task 2 §7 four checks on a proposal PDF."""
    text = extract_text(pdf_path, max_pages=10).lower()
    filename = pdf_path.name

    results = {
        "filename": filename,
        "checks": {},
        "overall": "FAIL",
    }

    # Check 1: Genuine vendor voice ("we will", "our solution", "proposes")
    vendor_voice_patterns = [
        r"\bwe (will|propose|offer|provide|recommend|suggest)\b",
        r"\bour (solution|approach|methodology|team|experience)\b",
        r"\b(proposes|offers|provides|delivers)\b",
        r"\binsight (will|proposes|offers)\b",  # vendor name example
        r"\b(caci|booz allen|randstad|deloitte|accenture|crowdstrike|aecom|aws|cdw)[-\s]?g?\b",
    ]
    check1 = any(re.search(p, text) for p in vendor_voice_patterns)
    results["checks"]["vendor_voice"] = {
        "pass": check1,
        "evidence": "Found first-person vendor language" if check1 else "No clear vendor voice in first 10 pages",
    }

    # Check 2: Specific RFP reference (solicitation number, buyer name, due date)
    rfp_patterns = [
        r"\brfp\s*#?\s*[\w\-]+\b",
        r"\bsolicitation\s*#?\s*[\w\-]+\b",
        r"\b(tre|um|az|ma|itd|nv)[-\s]?\d{4,}\b",  # known patterns from log
        r"\bdue (date|by)\b.*\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}",
        r"\bsubmitted (to|for)\b.*\b(city|state|university|county)\b",
    ]
    check2 = any(re.search(p, text) for p in rfp_patterns)
    results["checks"]["rfp_reference"] = {
        "pass": check2,
        "evidence": "Found RFP/solicitation reference" if check2 else "No RFP number or buyer reference in first 10 pages",
    }

    # Check 3: Sequential response structure (numbered requirements)
    seq_patterns = [
        r"\b\d+\.\s+[A-Z]",  # "1. Requirement"
        r"\b\d+\.\d+\b",      # "1.1", "2.3"
        r"\bsection\s+\d+\b",
        r"\brequirement\s+\d+\b",
        r"\bquestion\s+\d+\b",
    ]
    check3 = sum(1 for p in seq_patterns if re.search(p, text)) >= 2
    results["checks"]["sequential_structure"] = {
        "pass": check3,
        "evidence": "Found numbered requirement structure" if check3 else "No clear sequential Q&A structure",
    }

    # Check 4: Substantial length (>40 pages)
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        page_count = len(reader.pages)
    check4 = page_count >= 40
    results["checks"]["substantial_length"] = {
        "pass": check4,
        "evidence": f"{page_count} pages" if check4 else f"Only {page_count} pages (need ≥40)",
    }

    results["page_count"] = page_count
    results["overall"] = "PASS" if all(c["pass"] for c in results["checks"].values()) else "FAIL"
    return results


def verify_rfp(pdf_path: Path) -> dict:
    """Verify an RFP PDF has requirements content."""
    text = extract_text(pdf_path, max_pages=15).lower()
    filename = pdf_path.name

    results = {
        "filename": filename,
        "checks": {},
        "overall": "FAIL",
    }

    # RFP should have requirements/questions for vendors
    req_patterns = [
        r"\b(the vendor|the proposer|the bidder|the offeror)\s+(shall|must|will|should)\b",
        r"\brequirements?\b.*\d+",
        r"\bquestionnaire\b",
        r"\bproposal (requirements|instructions)\b",
        r"\bevaluation criteria\b",
        r"\bscope of work\b",
    ]
    has_requirements = any(re.search(p, text) for p in req_patterns)

    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        page_count = len(reader.pages)

    results["checks"]["has_requirements"] = {
        "pass": has_requirements,
        "evidence": "Found buyer requirements language" if has_requirements else "No clear requirements in first 15 pages",
    }
    results["checks"]["substantial_length"] = {
        "pass": page_count >= 20,
        "evidence": f"{page_count} pages",
    }

    results["page_count"] = page_count
    results["overall"] = "PASS" if all(c["pass"] for c in results["checks"].values()) else "FAIL"
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_proposal.py <pdf_file> [pdf_file...]")
        sys.exit(1)

    for arg in sys.argv[1:]:
        pdf_path = Path(arg)
        if not pdf_path.exists():
            print(f"✗  Not found: {pdf_path}")
            continue

        print(f"\n{'='*60}")
        print(f"Verifying: {pdf_path.name}")
        print(f"{'='*60}")

        if pdf_path.name.startswith("PROPOSAL_"):
            results = verify_proposal(pdf_path)
        elif pdf_path.name.startswith("RFP_"):
            results = verify_rfp(pdf_path)
        else:
            print("⚠  Unknown file type (expected PROPOSAL_* or RFP_*)")
            results = verify_proposal(pdf_path)

        print(f"Pages: {results['page_count']}")
        print(f"Overall: {results['overall']}")
        print()
        for check_name, check_result in results["checks"].items():
            status = "✓" if check_result["pass"] else "✗"
            print(f"  {status} {check_name}: {check_result['evidence']}")

    print(f"\n{'='*60}")
    print("Done.")


if __name__ == "__main__":
    main()