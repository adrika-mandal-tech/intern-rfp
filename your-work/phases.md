# RFP Automation Internship — Complete Phase Roadmap

**Project Timeline:** 2 days (compressed from 2-3 weeks)  
**Total Deliverables:** 5 Tasks → 1 unified proposal evaluation system baseline

---

## PHASE 0: Context & Foundations (Day 1 — ~2 hours)

### Goal
Understand the RFP automation domain, safety constraints, and workflow standards.

### Tasks
- [ ] Read [01-context/what-is-an-rfp.md](../01-context/what-is-an-rfp.md) — especially §5 (similarity limits) & §7 (scope trap)
- [ ] Read [01-context/how-we-work.md](../01-context/how-we-work.md) — annotation standards & rules
- [ ] Read [01-context/glossary.md](../01-context/glossary.md) — key terms
- [ ] Review [RFP_AUTOMATION_EXPLAINER.html](../01-context/RFP_AUTOMATION_EXPLAINER.html) — visual overview
- [ ] Read 15-20 rows from `02-evidence/golden_set_50rows.jsonl` as reference examples

### Deliverable
- Mental model: What is a "gap"? Why does similarity fail? When is an answer "partial"?
- Understanding of the 3 Rules (different service line, staleness, missing exhibit)

### Checkpoint
You can explain: Why can't the system just use similarity scores to detect gaps?

---

## PHASE 1: Expand Golden Set via Manual Annotation (Day 1-2 — ~8-10 hours)

### Goal
Hand-verify 60 requirements against the U.S. Bank proposal PDF to build a test/training dataset. This is the **single most critical deliverable** because it's the ruler we measure the system with.

### Input
- **Worklist A** (`your-work/worklist_A_random.jsonl`): 40 questions from stratified random sample across full RFP
- **Worklist B** (`your-work/worklist_B_lockbox.jsonl`): 20 questions deliberately over-sampling lockbox (best source of verified `none` answers)
- **Source**: U.S. Bank proposal PDF (214 pages)

### Tasks
**For each of the 60 rows:**

1. **Read requirement** — Understand exactly what is being asked
2. **Note service line** (General Banking? Lockbox? Purchasing Card?) — critical for Rule 1
3. **Search PDF** (Cmd+F on Mac) using distinctive nouns, not full sentences
4. **Read search results** — Check section headings to confirm scope
5. **Decide verdict**:
   - `answered` = Proposal clearly answers it (even if stale per Rule 2)
   - `partial` = Part answered, part missing (or answer in missing exhibit per Rule 3)
   - `none` = Not answered at all (no quote, page: 0)
6. **Copy exact quote** (>25 chars, no retyping — compare against PDF text layer)
7. **Record page number** from PDF counter (not footer page numbers)
8. **Write reasoning** (1-2 sentences: what did you find and why that verdict?)
9. **Set confidence** (high/medium/low) — use `low` if genuinely ambiguous

### Key Rules (Non-Negotiable)

| Rule | Example | Verdict |
|------|---------|---------|
| **Rule 1: Scope** | Question asks "lockbox DR". Proposal says "general banking DR". → `none` (not partial) |
| **Rule 2: Staleness** | Proposal from 2018, names outdated people. → Still `answered` |
| **Rule 3: Exhibits** | "See sample in Exhibits", but Exhibits not in PDF. → `partial` |

### Quality Gates (Daily)
```bash
python tools/verify_quotes.py --claims your-work/worklist_A_random.jsonl
```
- `verified` = OK ✅
- `off_by` = Fix page number 🔧
- `not_found` = **FIX THIS ROW** (quote was corrupted) ⚠️
- `empty_quote` = Add real quote ⚠️

### Definition of Done
- [ ] All 40 rows in worklist_A complete (verdict + quote + page + reasoning + confidence)
- [ ] All 20 rows in worklist_B complete (likewise)
- [ ] Zero `not_found` errors from verify_quotes.py
- [ ] Zero `empty_quote` errors
- [ ] Every `none` verdict has `page: 0` and empty quote
- [ ] Write **Annotation Summary** from [04-templates/annotation-summary-template.md](../04-templates/annotation-summary-template.md):
  - Verdict counts per list (A & B separate!)
  - How many rows marked `low` confidence
  - Which rows need second opinion
  - Any traps or ambiguities beyond the 3 Rules

### Output Files
- `your-work/worklist_A_random.jsonl` (40 annotated rows)
- `your-work/worklist_B_lockbox.jsonl` (20 annotated rows)
- `your-work/annotation-summary.md` (findings memo)

### Pace & Stamina
- **Per-row time**: 8-15 min (5-10 min after learning PDF layout)
- **If stuck >20 min**: Mark `low` confidence, note the difficulty, move on
- **Don't rush** — a wrong row silently corrupts all future measurements taken against it

---

## PHASE 2: Source Real RFP-Proposal Pairs (Parallel — ~4-6 hours)

### Goal
Find additional RFP + proposal pairs beyond the Delaware pair to build evaluation diversity and reduce statistical dependency on one pair.

### Tasks

1. **Research procurement sources**:
   - State RFP repositories (state.xxx.gov RFPs)
   - Federal SAM.gov (government contracts)
   - Municipal/public agency procurement sites
   - University procurement records (often public)

2. **Identify candidate pairs** that match criteria:
   - RFP is 50-200 pages (reasonable scope)
   - Proposal exists and is accessible
   - Vendor actually bid on it (proof of response)
   - Different industry/vendor than Delaware/US Bank (for diversity)
   - Ideally: banking, payments, or procurement-adjacent services

3. **Document findings** in source candidate log (template at [04-templates/source-candidate-log.md](../04-templates/source-candidate-log.md)):
   - Pair name + date
   - Source URL
   - Document sizes
   - Availability (publicly available? Requires request?)
   - Feasibility (estimated difficulty to acquire)
   - Relevance score (1-5)

4. **Create sourcing findings memo** (template at [04-templates/sourcing-findings-template.md](../04-templates/sourcing-findings-template.md)):
   - Summary of research effort
   - Pairs found + viability assessment
   - Ranking by feasibility + relevance
   - Recommended next steps (which pairs to prioritize acquiring)

### Definition of Done
- [ ] Minimum 3 candidate pairs identified
- [ ] Source candidate log filled out for each
- [ ] Sourcing findings memo written
- [ ] Each pair assessed for legal/confidentiality risk

### Output Files
- `your-work/source-candidate-log.md` (candidate tracking)
- `your-work/sourcing-findings.md` (research summary + recommendations)

### Note on Confidentiality
If pair is under NDA or confidential: Document it anyway but note "confidential — requires approval to ingest"

---

## PHASE 3: Questionnaire Landscape Research (Parallel — ~2-3 hours)

### Goal
Evaluate whether a "questionnaire mode" (structured form instead of free-text RFP) would be a viable product pivot.

### Tasks

1. **Research questionnaire usage**:
   - Which government entities issue questionnaires instead of RFPs?
   - What % of procurement is questionnaire vs RFP in finance/payments space?
   - What tools/platforms do they use (Coupa, Ariba, custom forms)?

2. **Analyze tradeoffs vs RFP mode**:
   - Questionnaire benefits: structured, extractable, testable with baseline
   - Questionnaire costs: limited scope, less context, vendor creativity restricted
   - Market demand: who would pay for this?

3. **Write decision memo** (template at [04-templates/research-memo-template.md](../04-templates/research-memo-template.md)):
   - Question: Is a questionnaire-first product viable?
   - Research findings (market size, user needs, technical feasibility)
   - Recommendation: pursue / don't pursue / hybrid approach
   - Key unknowns for follow-up

### Definition of Done
- [ ] Memo written (500-800 words)
- [ ] At least 2-3 sources consulted
- [ ] Clear recommendation with justification
- [ ] Identified follow-up questions for team

### Output Files
- `your-work/questionnaire-landscape.md` (research memo)

---

## PHASE 4: Competitive Landscape Research (Parallel — ~1-2 hours)

### Goal
Understand what competitors offer in the RFP automation / proposal management space and identify market gaps.

### Tasks

1. **Identify competitor tools**:
   - Proposal generation (Proposify, HubSpot)
   - RFP response (Loopio, Winds)
   - Contract intelligence (Contract AI tools)
   - Internal tools (banking/payments vendors)

2. **Analyze their approach**:
   - Do they claim gap detection / safe refusal?
   - How do they validate citations?
   - What's their evidence of accuracy?
   - Do they mention golden sets or hand-verified testing?

3. **Write competitive findings memo** (template at [04-templates/research-memo-template.md](../04-templates/research-memo-template.md)):
   - Question: Where's the market gap for a safety-first RFP automation tool?
   - Competitor features + limitations
   - Our differentiators (grounded answers, explicit refusal, gap detection)
   - Recommendation: what's our unique value proposition?

### Definition of Done
- [ ] Memo written (500-800 words)
- [ ] At least 3-4 competitors analyzed
- [ ] Clear differentiation narrative
- [ ] Market positioning recommendation

### Output Files
- `your-work/competitor-landscape.md` (research memo)

---

## PHASE 5: Review Explainer & Polish (Final — ~1 hour)

### Goal
Identify confusing parts of the RFP automation explainer and document improvements for next iteration.

### Tasks

1. **Read** [01-context/RFP_AUTOMATION_EXPLAINER.html](../01-context/RFP_AUTOMATION_EXPLAINER.html) in full

2. **Document confusing sections**:
   - What concepts took multiple reads?
   - Where did the narrative jump?
   - What examples clarified understanding?
   - What terms need clearer definition?

3. **Write review memo** (template at [04-templates/research-memo-template.md](../04-templates/research-memo-template.md)):
   - Section-by-section feedback
   - Recommended rewrites (be specific)
   - Missing examples or diagrams
   - Suggested tone/style improvements

### Definition of Done
- [ ] Memo written (300-500 words)
- [ ] Specific, actionable feedback (not just "confusing")
- [ ] Suggested improvements or rewrites where applicable

### Output Files
- `your-work/explainer-review.md` (feedback memo)

---

## EXECUTION ROADMAP (2-Day Compression)

### Day 1 (Saturday)
```
09:00-11:00   Phase 0 (Context reading)
11:00-19:00   Phase 1 (Annotation: rows 1-30 + daily verification)
19:00-22:00   Phase 2-4 (Research: parallel on laptop while main brain rests)
```

### Day 2 (Sunday)
```
09:00-15:00   Phase 1 (Annotation: rows 31-60 + final verification)
15:00-17:00   Phase 2-4 (Finalize research memos)
17:00-18:00   Phase 5 (Explainer review)
18:00-19:00   Final polish + deliverables summary
```

---

## DELIVERABLES CHECKLIST

### Phase 1 (Core)
- [x] `worklist_A_random.jsonl` — 40 annotated rows ✓
- [x] `worklist_B_lockbox.jsonl` — 20 annotated rows ✓
- [x] `annotation-summary.md` — findings memo ✓

### Phase 2 (Research)
- [ ] `source-candidate-log.md` — pairs identified ✓
- [ ] `sourcing-findings.md` — recommendations ✓

### Phase 3 (Research)
- [ ] `questionnaire-landscape.md` — memo ✓

### Phase 4 (Research)
- [ ] `competitor-landscape.md` — memo ✓

### Phase 5 (Polish)
- [ ] `explainer-review.md` — feedback memo ✓

### Validation
- [ ] `verify_quotes.py` runs with **zero errors** ✓
- [ ] All memos follow template format ✓
- [ ] Summary document ties all phases together ✓

---

## Key Principles Throughout

1. **Evidence over assertion** — Every claim supported by source or quote
2. **Separate A and B** — Never merge worklist results; they have different purposes
3. **Quality over speed** — A wrong golden set row is worse than a missing row
4. **Document traps** — If you find an ambiguity, write it down; it's valuable
5. **Human judgment is the point** — This cannot and should not be automated

---

## Next: Immediate Actions

1. **Today**: Complete Phase 0 (read context)
2. **Then**: Start Phase 1 with R102 ✅ (1 down, 59 to go)
3. **Parallel**: Start Phase 2-4 research on a second screen/device
4. **Daily**: Run `verify_quotes.py` to catch errors early
5. **End of Day**: Write annotation summary from template

---

**Questions for leads** (see next document: `questions-for-leads.md`)
