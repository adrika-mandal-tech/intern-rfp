# Clarifying Questions for Project Leads

**Context**: These questions emerged during Phase 0-1 analysis and represent ambiguities or decisions that affect how the annotation work should proceed and how phases 2-4 should be scoped.

---

## PHASE 1: Golden Set Annotation (Critical Path)

### Scope & Safety

**Q1.1: Rule 1 Boundary Case**
> "If a requirement is scoped to 'General Banking' but the proposal has an excellent answer for 'Treasury Management' (a broader category that includes general banking), is that `none` or `answered`?"

**Why it matters**: Rule 1 says "different service line = `none`". But service hierarchies overlap. Treasury Management might include General Banking, or might not.

**Current assumption**: Service categories in RFP `section` field are the authority. Broader service ≠ commitment to narrower service. Therefore `none`.

**Confirm?**

---

**Q1.2: Partial Definition Boundary**
> "A requirement asks two things (e.g., 'How often do you meet? What's the agenda?'). The proposal answers cadence but says 'agendas in Exhibits'. Is that `partial` or should I split it 50/50?"

**Why it matters**: Multi-part requirements are common. Deciding whether "answer 1 of 2" = `partial` or needs both parts.

**Current assumption**: If ANY part is unanswered/unreachable, mark `partial`. Do not split votes.

**Confirm?**

---

**Q1.3: Stale Data Boundary**
> "Proposal from 2018 lists a person who 'joined in 2015'. Does that count as 'years of experience' info if they might have left? Or should I note uncertainty?"

**Why it matters**: Rule 2 says staleness doesn't make it `none`. But missing data due to staleness is different from stale data that's still there.

**Current assumption**: If the text exists and answered the question when written, mark `answered`. Use `low` confidence if you suspect data rot.

**Confirm?**

---

### Annotation Mechanics

**Q1.4: Quote Extraction**
> "If the answer spans a page break and copying creates line-wrap artifacts, should I clean it up or paste exactly as copied?"

**Why it matters**: verify_quotes.py does exact text matching. Line breaks matter.

**Current assumption**: Paste exactly as copied, even if ugly. The checker will validate it against the PDF text layer.

**Confirm?**

---

**Q1.5: Confidence Scoring**
> "Should I mark `low` confidence when I'm uncertain about my verdict, or only when the requirement itself is ambiguously worded?"

**Why it matters**: `low` confidence flags rows that might need review. Different interpretations lead to different annotations.

**Current assumption**: Mark `low` if YOU'RE uncertain (either because verdict is hard to call OR the req is ambiguous). Both are valuable signals.

**Confirm?**

---

**Q1.6: Section Heading Mismatch**
> "RFP section says 'Lockbox' but proposal heading says 'Payment Processing'. Should I trust the RFP section or the proposal heading?"

**Why it matters**: This is a trap that corrupted earlier data (18 false negatives). Rule 1 depends on getting scope right.

**Current assumption**: Trust the RFP section field ONLY. Proposal headings come from a different taxonomy and nearly always mismatch. Ignore them.

**Confirm?**

---

### Edge Cases

**Q1.7: Marketing Fluff vs Answer**
> "A requirement asks 'What's your disaster recovery plan?' Proposal says 'We take security seriously and invest heavily in redundancy.' Is this an answer?"

**Why it matters**: Vendors often respond with buzzwords instead of specifics.

**Current assumption**: Buzzwords alone = `none`. An answer must make a specific claim (frequency, location, mechanism, etc).

**Confirm?**

---

**Q1.8: Indirect Answers**
> "Requirement: 'Do you support ACH?' Proposal: 'Our platform integrates with all standard payment networks including ACH, wire, and check.' Is that `answered`?"

**Why it matters**: Specificity trade-off. Explicit answer vs reasonable inference.

**Current assumption**: Yes, `answered`. A reasonable reader would infer ACH is supported from "all standard payment networks".

**Confirm?**

---

## PHASE 2: Sourcing Real Pairs (Strategic)

### Data Acquisition

**Q2.1: Confidentiality Handling**
> "If I find a perfect RFP-Proposal pair but it's under NDA or confidential, should I source it anyway?"

**Why it matters**: Better data but legal/ethical risk.

**Recommendation**: Document it as a candidate with confidentiality flag. Flag for legal review before ingesting.

---

**Q2.2: Vendor Agreement Scope**
> "Some proposals are submitted to public buyers (states, universities). Are these automatically public? Or do we need to request permission?"

**Why it matters**: Public procurement documents are often public record, but vendors sometimes contest it.

**Recommendation**: Check local public records law. Document status clearly.

---

### Pair Quality

**Q2.3: Domain Diversity**
> "Should Phase 2 prioritize finding banking/payments pairs (similar to Delaware) or diversify into other verticals (energy, IT, construction)?"

**Why it matters**: Similar domain = easier to annotate but less diverse. Different domain = better generalization but harder to annotate.

**Recommendation**: Start with 1-2 similar domain pairs to reduce annotation friction, then diversify if time permits.

---

**Q2.4: Pair Freshness**
> "Should I prioritize recent pairs (last 2-3 years) or will older pairs (5-10 years ago) work just as well for testing?"

**Why it matters**: Older = better public availability but may have obsolete language. Newer = better current relevance but harder to access.

**Recommendation**: Mix: at least 1 recent pair + 1-2 older pairs if available.

---

## PHASE 3: Questionnaire Landscape (Product Strategy)

### Market Research

**Q3.1: Definition Scope**
> "When you say 'questionnaire mode', do you mean: (A) RFP that's structured as a form submission, (B) Vendor pre-qualification questionnaires (different from RFP), or (C) Structured Q&A inside an RFP?"

**Why it matters**: These are very different markets.

**Recommendation**: Clarify which mode to evaluate. Probably (A) or (B).

---

**Q3.2: Vertical Focus**
> "Should I research questionnaire usage across all government sectors, or focus on procurement verticals similar to banking/payments?"

**Why it matters**: Focus = depth but limited scope. Broad = generalization but shallow.

**Recommendation**: Focus on government finance/payments initially; generalize if time permits.

---

### Technical Feasibility

**Q3.3: System Architecture Impact**
> "If we pivot to questionnaire mode, would it require retraining the retrieval model or just changing the prompt + extraction logic?"

**Why it matters**: Affects scope of Phase 3 conclusion (quick pivot vs major retooling).

**Recommendation**: Include architecture impact assessment in memo.

---

## PHASE 4: Competitor Landscape (Product Positioning)

### Market Analysis

**Q4.1: Definition of "Competitor"**
> "Should I include only direct RFP automation tools, or also broader proposal management platforms (Proposify, HubSpot, Salesforce) that have RFP modules?"

**Why it matters**: Direct competitors are rare. Broader platforms are numerous but may not be direct threats.

**Recommendation**: Include both, but segment analysis (direct vs adjacent).

---

**Q4.2: Claim Verification**
> "Some competitors claim 95%+ accuracy without disclosing their test set. Should I flag this as a red flag or assume it's credible?"

**Why it matters**: Affects competitive positioning (we're conservative vs they're overconfident).

**Recommendation**: Flag all unverified accuracy claims. Emphasize that we use a hand-verified golden set.

---

## PHASE 5: Explainer Review (Documentation)

### Clarity & Audience

**Q5.1: Intended Audience**
> "Is the explainer written for technical implementers, business stakeholders, or both? Should I review it differently depending on audience?"

**Why it matters**: Clarity standards differ. Technical audience can tolerate jargon; business audience cannot.

**Recommendation**: Note audience assumption in review. Flag sections that don't match assumed audience.

---

---

## Meta: Questions About the Workflow Itself

### Execution Logistics

**QM.1: Time Allocation**
> "Given the 2-day constraint, is it better to do Phase 1 perfectly (all 60 rows, 100% verified) or Phase 1 + Phase 2 partially (50 rows + 2-3 sourced pairs)?"

**Why it matters**: Trade-off between depth and breadth.

**Recommendation**: Phase 1 is the critical path. Don't compromise it. Phase 2-5 can be partial.

---

**QM.2: Daily Verification**
> "Should I run verify_quotes.py after every 10 rows, after every day, or only at the very end?"

**Why it matters**: Early errors are cheaper to fix. Late errors may cascade.

**Recommendation**: After every 10 rows minimum. After every day definitely.

---

**QM.3: Ambiguous Row Handling**
> "When I mark a row `low` confidence with a note that I need a second opinion, should I also submit a completed verdict or leave it blank for human review?"

**Why it matters**: Affects how downstream systems handle ambiguous data.

**Recommendation**: Submit a completed verdict (best judgment) + `low` confidence flag. That's useful signal.

---

### Success Metrics

**QM.4: Definition of "Done" for Phase 1**
> "Is the goal 60 perfect rows, or 60 rows with known errors that we can learn from?"

**Why it matters**: Affects annotation pace and perfectionism.

**Recommendation**: Perfect rows. A corrupt golden set is worse than a small one. Better to have 50 perfect rows than 60 wrong ones.

---

**QM.5: Verification Failure Handling**
> "If verify_quotes.py reports `not_found` on a quote, does that mean I should re-annotate that row or is there a way to debug the mismatch?"

**Why it matters**: Affects how to handle errors.

**Recommendation**: Re-annotate. `not_found` usually means the quote was retyped (even slightly) or spans a page break. Pull the text again from PDF.

---

## Summary: Questions Before Starting Phase 1

**MUST clarify before starting annotation:**
1. Q1.1: Rule 1 scope hierarchy
2. Q1.2: Partial definition when requirement has 2+ parts
3. Q1.6: RFP section vs proposal heading authority

**SHOULD clarify for quality:**
4. Q1.4: Quote extraction exact-matching vs cleanup
5. Q1.5: Low confidence scoring (uncertainty about verdict vs req)
6. Q1.7: Buzzwords vs specifics in disaster recovery answers

**Nice to clarify:**
7. Q1.3: Stale data boundary
8. QM.4: Perfect 50 rows vs imperfect 60 rows

---

**Next Step**: Schedule brief sync with leads to confirm Q1.1, Q1.2, Q1.6. Can proceed with Phase 1 while waiting for answers to other questions.
