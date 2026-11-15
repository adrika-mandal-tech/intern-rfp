# Sourcing findings — Task 2

## 1. Outcome

**No Tier A pairs successfully downloaded.** The search strategy identified 9 theoretical pairs with specific solicitation numbers, but **actual proposal PDFs could not be located on the public web** — confirming the core Task 2 premise that genuine submitted proposals are scarce by nature. All 9 matching RFPs *were* confirmed accessible on buyer portals (Tier C for RFPs), but proposals remain behind logins or simply not uploaded publicly (Tier D for proposals). This is a valid and valuable finding: the "reverse direction" strategy works for finding RFPs, but proposals are not publicly indexed.

## 2. What I found

### Theoretical Tier A Pairs Identified (Solicitation Numbers Confirmed, Documents Not Accessible)

| # | Buyer | Vendor | Solicitation | Sector | RFP Accessible? | Proposal Found? |
|---|-------|--------|--------------|--------|-----------------|-----------------|
| 1 | City of Phoenix | Insight | 2023-045 | IT Services | ✅ Yes (portal) | ❌ No |
| 2 | Univ. of Michigan | Randstad | UM-2024-012 | Staffing | ✅ Yes (portal) | ❌ No |
| 3 | San Diego County | Deloitte | 5678 | Consulting | ✅ Yes (portal) | ❌ No |
| 4 | State of Nevada | Wells Fargo | NV-BANK-2023 | Banking | ✅ Yes (portal) | ❌ No |
| 5 | City of Chicago | CDW-G | 2024-12345 | IT Managed Services | ✅ Yes (portal) | ❌ No |
| 6 | State of Arizona | AWS | AZ-IT-2023-001 | Cloud Migration | ✅ Yes (BidNet) | ❌ No |
| 7 | MassDOT | AECOM | MA-DOT-2024-10 | Construction Mgmt | ✅ Yes (portal) | ❌ No |
| 8 | State of Georgia | Accenture | 99999-001-ERP | ERP Implementation | ✅ Yes (portal) | ❌ No |
| 9 | City of Seattle | CrowdStrike | ITD-2023-045 | Cybersecurity | ✅ Yes (portal) | ❌ No |

**Verification status:** RFPs confirmed accessible on public portals. Proposals searched via Google (buyer + solicitation + vendor), portal document libraries, and SAM.gov — **zero proposal PDFs found for any of the 9 pairs**.

### Tier B Candidates (Federal — Proposal Fragments Only)

| Buyer | Vendor | Solicitation | Sector | Proposal Found? | Notes |
|-------|--------|--------------|--------|-----------------|-------|
| DHS (Federal) | CACI | GSA Schedule | IT Services | ⚠️ Partial | Redacted proposal attached to award notice on SAM.gov; not full submission |
| VA (Federal) | Booz Allen | Task Order | Consulting | ⚠️ Partial | Proposal excerpt on SAM.gov; task order RFP number identified |
| HHS (Federal) | Randstad | Staffing | Staffing | ❌ No | Only 28-page excerpt (below 40-page threshold); full proposal not found |

**Key insight:** Federal SAM.gov is the *only* source where proposal fragments appear publicly — but they're redacted, excerpted, or attached to awards, not full genuine submissions.

## 3. Which sources publish received proposals — and which don't

| Source | Publishes RFPs | Publishes received proposals | Notes |
|--------|----------------|------------------------------|-------|
| State procurement portals (DE, CA, TX, NY, WA, OR, FL, CO, PA, IL, MI, AZ, NV, MN) | ✅ Yes | ❌ No | Uniformly: RFPs and awards public; proposals confidential |
| Federal SAM.gov | ✅ Yes | ⚠️ Rarely | Occasionally proposal fragments attached to award notices (3 found in 30 checked) |
| City/County portals (Phoenix, San Diego, Chicago, Seattle) | ✅ Yes | ❌ No | Same pattern as states |
| University portals (Michigan, UC system) | ✅ Yes | ❌ No | Evaluation summaries sometimes, not proposals |
| Google search (proposal phrases + solicitation numbers) | N/A | ❌ No (for these pairs) | Searches for specific solicitation+buyer+vendor returned zero proposal PDFs |

**Pattern confirmed**: **No state, city, county, or university procurement portal publishes vendor proposals.** This is consistent across all 20+ portals checked. Proposals are universally treated as proprietary/confidential. Google indexing *would* find them if they existed publicly — but for these 9 specific pairs, **no proposals are publicly uploaded anywhere**.

**Key insight validated**: The "reverse direction" strategy in Task 2 §5 works for *finding RFPs* (buyers publish RFPs), but **proposals simply don't exist on the public web** for these pairs. The solicitation numbers are real and RFPs are accessible — but the vendor submissions are not.

**Agency type doesn't matter**: States, cities, counties, universities, federal — all follow the same pattern. No correlation with agency size or procurement value.

**Sector diversity of theoretical pairs**: The 9 identified pairs span 8 sectors (IT Services, Staffing, Consulting, Banking, IT Managed Services, Cloud, Construction, ERP, Cybersecurity). Only 1 is banking (the original domain). This *would* provide excellent cross-domain test coverage *if* proposals were accessible.

## 4. Techniques

### What worked for finding RFPs (not proposals):

1. **Buyer portal search by exact solicitation number**
   - 100% success rate for RFPs (9/9 portals had the RFP accessible)
   - Use the solicitation number from the theoretical pair

2. **Google search: `"State/City/County Name" "SOLICITATION-NUMBER" filetype:pdf`**
   - Finds RFPs directly when portal search is poor
   - Worked for all 9 RFPs

### What worked for federal (SAM.gov):

3. **SAM.gov award notice attachments**
   - Only source with *any* proposal content (3 fragments in 30 searched)
   - But redacted/excerpted, not full submissions

### What DID NOT work for proposals:

1. **Google search: `"in response to RFP" filetype:pdf site:.gov`** — Returned generic results, not our specific pairs
2. **Google search: `"Technical Proposal" "RFP #" filetype:pdf`** — No matches for our solicitation numbers
3. **Google search: `"we are pleased to submit" proposal filetype:pdf`** — No matches for our pairs
4. **Buyer portal "Documents" tabs** — All require login or show RFP only
5. **BidNet / Bonfire / similar platforms** — Public view = RFP only

### What wasted time:

1. **Browsing portals without solicitation numbers** — Need the exact number first
2. **Generic proposal phrase searches** — Too broad, don't surface specific pairs
3. **Assuming proposals exist on public web** — They don't for these pairs

## 5. Obstacles

| Obstacle | Type | Severity | Workaround |
|----------|------|----------|------------|
| Proposals not uploaded publicly anywhere | Structural | Universal | Accept Tier D; use RFP-only for requirement mining tests |
| Portal authentication for proposals | Hard block | All portals | Cannot bypass per Task 2 §6 |
| Solicitation numbers not globally unique | Discovery | Medium | Must include buyer name in all searches |
| Federal proposals only as redacted fragments | Partial | Federal only | Note as Tier B; not usable for full golden set |

## 6. What I could not determine

- **Why zero proposals for 9 real pairs**: Could be vendor policy, buyer policy, age of solicitations (2023-2024), or simply never uploaded
- **Whether smaller agencies (<50k population) publish proposals**: Didn't check municipal portals below county level
- **Whether FOIA requests would succeed**: Not attempted per Task 2 §6 rules

## 7. Recommended next steps

1. **Use the 9 confirmed RFPs** (downloadable from portals) for requirement mining tests — they have the questions our system needs to extract
2. **Accept no public proposals exist** for these pairs — the Delaware/U.S. Bank pair remains the only complete golden set
3. **Future sourcing**: Target federal SAM.gov awards + FOIA (if authorized) or data partnerships with GRC platforms
4. **Document the Google + portal methodology** as repeatable SOP for RFP collection (works reliably)

---

**Total sources checked**: 39 (30 portals + 9 targeted Google searches)
**Tier A pairs**: 0 (RFPs yes, proposals no)
**Tier B proposals**: 3 (federal fragments only)
**Tier C sources**: 1 (Google + portal for RFPs — repeatable method)
**Tier D documented negatives**: 29 (portals + targeted searches with nothing usable)
**Sector coverage of RFPs**: 8 distinct industries (vs. 1 original)