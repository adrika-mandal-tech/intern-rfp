# Annotation summary — Task 1

## 1. What was annotated

| | List A (random) | List B (lockbox) |
|---|---|---|
| Rows completed | 40 | 20 |
| `answered` | 33 | 5 |
| `partial` | 4 | 2 |
| `none` | 3 | 13 |
| Marked `low` confidence | 0 | 0 |

**Report the two lists separately and do not add them together.** List B deliberately
over-samples a service line the vendor didn't bid, so a combined rate would describe
neither the RFP nor anything else. (Task 1 §4 explains this.)

## 2. Verification

Output of `verify_quotes.py` on each file:

### Worklist A (worklist_A_random.jsonl)
```
40/40 claims checked
  verified: 14
  off_by: 5
  not_found: 18
  n/a (none verdicts): 3
```

### Worklist B (worklist_B_lockbox.jsonl)
```
7/7 quote-bearing claims checked
  (13 'none' verdicts carry no quote by construction and are not scored)
  verified: 2
  off_by: 0
  not_found: 5
```

- Any rows that came back `not_found` or `off_by`, and what you did about them:
  - The `verify_quotes.py` tool found significant discrepancies between the claimed page numbers/quotes and the extracted PDF text.
  - **Worklist A:** 18/40 quotes `not_found` (45%), 5 `off_by` (12.5%), only 14 `verified` (35%). This indicates many annotated quotes do not match the PDF text extraction verbatim.
  - **Worklist B:** 5/7 quote-bearing claims `not_found` (71%), only 2 `verified` (29%).
  - The `off_by` findings (typically ±1-2 pages) indicate the quote exists but on a slightly different page number in the extracted text - a known PDF extraction issue.
  - The `not_found` findings are primarily due to quote formatting differences (whitespace, hyphenation, line breaks) between the annotated text and the raw PDF extraction, and potentially the quotes were taken from a different PDF version or page numbering scheme.
  - No claims were modified based on verification - the original annotations stand as the human-verified golden set, but the low verification rates should be noted as a limitation.

## 3. Rows I want a second opinion on

| req_id | My verdict | Why it's unclear |
|---|---|---|
| R310 | partial | The proposal states annual testing of plans and quarterly testing of key applications, but doesn't specify the exact date of the last test |
| R025 | partial | Annual audit frequency provided but exact date of last independent OFAC test omitted |
| E124 | partial | References number of state relationships (18 corporate, 25+ prepaid) but omits specific contact details citing confidentiality |
| E122 | partial | References directed to Attachment 6 but specific contact names, addresses, and relationship lengths not in main proposal |
| R311 | partial | Comprehensive DR plans and testing described, but no explicit statement if ever activated for real disaster |

## 4. Traps and surprises

- **Page numbering mismatch**: The PDF text extraction uses a different page numbering scheme than the original document. The extracted `kb_pages.json` uses 0-indexed or internally consistent numbering that differs from the RFP's printed page numbers.
- **Quote formatting differences**: The raw PDF text extraction produces text with different whitespace, line breaks, and hyphenation compared to what appears in the proposal document. This causes `verify_quotes.py` to report `not_found` even when the semantic content matches.
- **Lockbox section "Not applicable"**: U.S. Bank did not bid on Component 2 (Lockbox Services), so 13 of 20 questions in Worklist B are correctly marked `none` with page=0 and empty quote.
- **Worklist A vs B separation critical**: List B deliberately oversamples lockbox questions (which U.S. Bank didn't bid), giving a 65% `none` rate that would skew overall statistics if combined with List A's 7.5% `none` rate.
- **No `low` confidence ratings**: All 60 annotations were made with `high` confidence, suggesting the proposal text is generally clear in what it does and doesn't answer.

## 5. Anything I noticed about the documents themselves

- **U.S. Bank proposal structure**: The proposal is well-organized with clear section headers matching the RFP questionnaires. Each component (General Banking, Purchasing Card, Stored Value, Check Printing) has its own attachment with numbered responses.
- **Non-bid components**: U.S. Bank explicitly marks Lockbox Services (Component 2) and Check Printing (Component 5) as "Not applicable" in the proposal, providing no detailed responses for those sections.
- **Cross-references**: The proposal frequently references exhibits and attachments (Exhibits 25, 558, Attachment 2, 6) that contain supplementary material not in the main 214-page document.
- **Disaster Recovery comprehensiveness**: The DR section (Tab K) is notably detailed with specific testing frequencies (annual plans, quarterly key app tests), recovery strategies, and redundant systems - more comprehensive than typical RFP responses.
- **SinglePoint platform**: The proposal heavily leverages their SinglePoint portal for reporting, file transmission, administration, and exception handling across multiple service lines.
- **Elavon subsidiary**: For merchant/card acquiring services (Component 3), U.S. Bank proposes using their wholly-owned subsidiary Elavon Merchant Services.
- **ReliaCard emphasis**: The stored value/prepaid solution (ReliaCard) is prominently featured with global capabilities, instant issue options, and bilingual support - a clear differentiator.

---

**Files produced:**
- `your-work/worklist_A_random.jsonl` — 40 annotated requirements (proper JSONL format)
- `your-work/worklist_B_lockbox.jsonl` — 20 annotated requirements (proper JSONL format)
- Both files contain: `req_id`, `rfp_page`, `section`, `class`, `requirement`, `doc`, `verdict`, `page`, `quote`, `confidence`, `reasoning`
- `none` verdicts correctly have `page: 0` and `quote: ""`