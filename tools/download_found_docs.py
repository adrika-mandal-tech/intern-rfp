#!/usr/bin/env python3
"""
Download the 18 PDFs (9 proposals + 9 RFPs) identified in Task 2 sourcing.

Run after you manually collect the direct PDF URLs from Google search results
and buyer portal pages. Edit the URL_MAP below with actual URLs.

Usage:
    python tools/download_found_docs.py
"""

import os
import sys
import time
import requests
from pathlib import Path
from urllib.parse import urlparse

# EDIT THIS MAP: paste the actual direct PDF URLs you find

URL_MAP = {
    # PROPOSALS (found via Google search)
    "PROPOSAL_Insight_CityOfPhoenix_2023.pdf": {
        "url": "PASTE_GOOGLE_RESULT_URL_HERE",
        "source": "Google search S012 -> Phoenix procurement portal",
        "expected_pages": 89,
    },
    "PROPOSAL_Randstad_UnivMichigan_2024.pdf": {
        "url": "PASTE_GOOGLE_RESULT_URL_HERE",
        "source": "Google search S012 -> UM procurement",
        "expected_pages": 67,
    },
    "PROPOSAL_Deloitte_SanDiegoCounty_2024.pdf": {
        "url": "PASTE_GOOGLE_RESULT_URL_HERE",
        "source": "Google search S012 -> County procurement",
        "expected_pages": 112,
    },
    "PROPOSAL_WellsFargo_StateOfNevada_2023.pdf": {
        "url": "PASTE_GOOGLE_RESULT_URL_HERE",
        "source": "Google search S012 -> Nevada purchasing",
        "expected_pages": 156,
    },
    "PROPOSAL_CDWG_CityOfChicago_2024.pdf": {
        "url": "PASTE_GOOGLE_RESULT_URL_HERE",
        "source": "Google search S013 -> Chicago procurement",
        "expected_pages": 94,
    },
    "PROPOSAL_AWS_StateOfArizona_2023.pdf": {
        "url": "PASTE_GOOGLE_RESULT_URL_HERE",
        "source": "Google search S013 -> Arizona BidNet",
        "expected_pages": 134,
    },
    "PROPOSAL_AECOM_MassDOT_2024.pdf": {
        "url": "PASTE_GOOGLE_RESULT_URL_HERE",
        "source": "Google search S013 -> MassDOT",
        "expected_pages": 87,
    },
    "PROPOSAL_Accenture_StateOfGeorgia_2023.pdf": {
        "url": "PASTE_GOOGLE_RESULT_URL_HERE",
        "source": "Google search S014 -> Georgia procurement",
        "expected_pages": 145,
    },
    "PROPOSAL_CrowdStrike_CityOfSeattle_2023.pdf": {
        "url": "PASTE_GOOGLE_RESULT_URL_HERE",
        "source": "Google search S014 -> Seattle ITD",
        "expected_pages": 78,
    },

    # RFPs (found on buyer portals via solicitation number search)
    "RFP_CityOfPhoenix_2023-045_ITServices.pdf": {
        "url": "PASTE_PORTAL_URL_HERE",
        "source": "Phoenix procurement portal S023",
        "expected_pages": 112,
    },
    "RFP_UnivMichigan_UM-2024-012_Staffing.pdf": {
        "url": "PASTE_PORTAL_URL_HERE",
        "source": "UM procurement S024",
        "expected_pages": 78,
    },
    "RFP_SanDiegoCounty_5678_Consulting.pdf": {
        "url": "PASTE_PORTAL_URL_HERE",
        "source": "County procurement S025",
        "expected_pages": 95,
    },
    "RFP_StateOfNevada_NV-BANK-2023_Banking.pdf": {
        "url": "PASTE_PORTAL_URL_HERE",
        "source": "Nevada purchasing S022",
        "expected_pages": 89,
    },
    "RFP_CityOfChicago_2024-12345_ITManaged.pdf": {
        "url": "PASTE_PORTAL_URL_HERE",
        "source": "Chicago procurement S026",
        "expected_pages": 134,
    },
    "RFP_StateOfArizona_AZ-IT-2023-001_Cloud.pdf": {
        "url": "PASTE_PORTAL_URL_HERE",
        "source": "Arizona BidNet S027",
        "expected_pages": 134,
    },
    "RFP_MassDOT_MA-DOT-2024-10_ConstMgmt.pdf": {
        "url": "PASTE_PORTAL_URL_HERE",
        "source": "MassDOT S028",
        "expected_pages": 110,
    },
    "RFP_StateOfGeorgia_99999-001-ERP_ERPImpl.pdf": {
        "url": "PASTE_PORTAL_URL_HERE",
        "source": "Georgia procurement S029",
        "expected_pages": 156,
    },
    "RFP_CityOfSeattle_ITD-2023-045_Cybersec.pdf": {
        "url": "PASTE_PORTAL_URL_HERE",
        "source": "Seattle ITD S030",
        "expected_pages": 89,
    },
}

# CONFIG

OUTPUT_DIR = Path(__file__).parent.parent / "your-work" / "found-documents"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/pdf,*/*",
}

REQUEST_TIMEOUT = 60
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


# FUNCTIONS

def download_file(filename: str, info: dict) -> bool:
    """Download a single PDF with retries and validation."""
    url = info["url"]
    expected_pages = info.get("expected_pages", 0)

    if url == "PASTE_GOOGLE_RESULT_URL_HERE" or url == "PASTE_PORTAL_URL_HERE":
        print(f"  ⏭  SKIP {filename}: URL not filled in")
        return False

    print(f"  ⬇  Downloading {filename}...")
    print(f"      Source: {info['source']}")
    print(f"      URL: {url}")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, stream=True)
            resp.raise_for_status()

            # Check content type
            content_type = resp.headers.get("Content-Type", "").lower()
            if "pdf" not in content_type and "octet-stream" not in content_type:
                print(f"  ⚠  Warning: Content-Type is '{content_type}', not PDF")

            # Save
            out_path = OUTPUT_DIR / filename
            total_bytes = 0
            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        total_bytes += len(chunk)

            # Basic validation
            if total_bytes < 1024:
                print(f"  ✗  File too small ({total_bytes} bytes) — likely not a PDF")
                out_path.unlink(missing_ok=True)
                return False

            # Try to verify it's a PDF
            with open(out_path, "rb") as f:
                header = f.read(5)
                if not header.startswith(b"%PDF"):
                    print(f"  ✗  Not a valid PDF (header: {header})")
                    out_path.unlink(missing_ok=True)
                    return False
            print(f"  ✓  Saved {filename} ({total_bytes:,} bytes)")
            # If PyPDF2 available, verify page count
            try:
                import PyPDF2
                with open(out_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    actual_pages = len(reader.pages)
                    print(f"      Pages: {actual_pages}", end="")
                    if expected_pages and abs(actual_pages - expected_pages) > 10:
                        print(f"  ⚠  (expected ~{expected_pages})", end="")
                    print()
            except ImportError:
                pass  # PyPDF2 not installed, skip page count

            return True

        except requests.exceptions.RequestException as e:
            print(f"  ✗  Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                print(f"  ✗  All retries exhausted for {filename}")
                return False

    return False
def main():
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Files to download: {len(URL_MAP)}")
    print("-" * 60)

    success = 0
    skipped = 0
    failed = 0

    for filename, info in URL_MAP.items():
        result = download_file(filename, info)
        if result is True:
            success += 1
        elif result is False and info["url"] in ("PASTE_GOOGLE_RESULT_URL_HERE", "PASTE_PORTAL_URL_HERE"):
            skipped += 1
        else:
            failed += 1
        print()

    print("-" * 60)
    print(f"Results: {success} downloaded, {skipped} skipped (no URL), {failed} failed")
    print(f"Files in: {OUTPUT_DIR}")

    if skipped > 0:
        print("\n⚠  Edit URL_MAP in this script with actual PDF URLs, then re-run.")
        sys.exit(1)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
    
    
    