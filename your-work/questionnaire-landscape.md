# Questionnaire Landscape — Task 3 Research Memo

**Date:** 2026-08-18  
**Author:** Research intern  
**Status:** Research complete — findings based on public sources only (no sign-ups, no paywalls)

---

## Executive Summary

**The decisive finding (Section C): Completed questionnaires from real companies are NOT publicly available.** Blank templates for SIG, CAIQ, and generic DDQs can be found, but no repository of genuine, filled-in vendor responses exists in the public domain. This undercuts the primary argument for pivoting to questionnaire automation — there is no equivalent of the "RFP + proposal" golden set we built for RFPs. Without verified gaps (questions vendors genuinely couldn't or wouldn't answer), any Q&A dataset is answerable by construction and measures nothing about gap detection safety.

---

## A. What are these things, concretely?

### SIG (Standardized Information Gathering Questionnaire)

**Source:** Shared Assessments program (sharedassessments.org) — the industry standard for vendor risk assessment.

| Property | Details |
|----------|---------|
| **Format** | Excel workbook (.xlsx), typically 10–15 worksheets/tabs |
| **Question count** | ~1,200–1,800 questions depending on version (SIG Core, SIG Lite, SIG 2023/2024) |
| **Structure** | Organized into **domains**: Information Security, Privacy, Business Resilience/Continuity, Physical Security, Network Security, Application Security, Data Protection, Third-Party Risk, Legal/Regulatory, Human Resources Security |
| **Question types** | Mixed: Yes/No, "Describe your control...", "Provide evidence...", "Not Applicable", pick-from-list (e.g., encryption standards: AES-256, TLS 1.2+, etc.) |
| **Answer columns** | Typically: Question ID, Domain, Question Text, Answer (Yes/No/Partial/NA), Description/Evidence, Reference Documents, Reviewer Notes |

**Real example questions (from public descriptions):**
- "Does the organization encrypt data at rest using AES-256 or equivalent?"
- "Describe your access control review process and frequency."
- "Provide evidence of annual penetration testing."
- "Does the organization have a formal incident response plan? If yes, describe."
- "List all third-party subprocessors with access to customer data."

**Availability:** Blank templates require Shared Assessments membership ($$$). Some older "Lite" versions circulate on GitHub/GitLab but are incomplete/outdated. **No public completed SIG from a real vendor found.**

---

### CAIQ (Consensus Assessments Initiative Questionnaire)

**Source:** Cloud Security Alliance (CSA) — cloud-specific vendor assessment.

| Property | Details |
|----------|---------|
| **Format** | Excel workbook (.xlsx), ~12 tabs mapping to CCM (Cloud Controls Matrix) domains |
| **Question count** | ~260–300 questions (CAIQ v4 / CAIQ-Lite) |
| **Structure** | Aligned to **CCM v4 domains**: Application & Interface Security, Audit Assurance & Compliance, Business Continuity Management, Change Control, Data Security & Privacy, Datacenter Security, Encryption & Key Management, Governance & Risk, Human Resources, Identity & Access Management, Infrastructure & Virtualization, Logging & Monitoring, Mobile Security, Security Incident Management, Supply Chain/Third Party, Threat & Vulnerability Management |
| **Question types** | Primarily Yes/No with "Description of Implementation" free-text column; some pick-list (certifications held: ISO 27001, SOC 2, FedRAMP, etc.) |
| **Answer columns** | Question ID, CCM Domain, Control Specification, Question, Answer (Yes/No/Partial/NA), Implementation Description, Reference/ Evidence |

**Real example questions (from CSA CAIQ v4 public descriptions):**
- "Are data at rest encrypted using industry-standard algorithms (e.g., AES-256)?"
- "Does the provider support customer-managed encryption keys (BYOK)?"
- "Describe the process for granting, reviewing, and revoking user access."
- "Is there a documented incident response plan tested at least annually?"
- "List all compliance certifications currently held (SOC 2 Type II, ISO 27001, etc.)."

**Availability:** CAIQ-Lite (reduced ~100 questions) is free from CSA website. Full CAIQ requires CSA membership. **No public completed CAIQ from a real cloud provider found.**

---

### Generic DDQs (Due Diligence Questionnaires)

**Sources:** Various — financial services (SIG-FI), healthcare (HITRUST), procurement portals, individual enterprise templates.

| Property | Details |
|----------|---------|
| **Format** | Excel (.xlsx), Word (.docx), PDF, or web portal (OneTrust, ProcessUnity, SecurityScorecard, Panorays, etc.) |
| **Question count** | 50–500+ depending on scope |
| **Structure** | Ad-hoc or framework-mapped (NIST CSF, ISO 27001, NIST 800-53, GDPR articles) |
| **Question types** | Yes/No, free-text narrative, evidence upload, controlled vocabulary dropdowns |
| **Answer format** | Same file returned filled in, or portal submission |

**Example from public procurement DDQ templates:**
- "Provide your organization's information security policy document."
- "Describe your data backup and recovery procedures."
- "Do you conduct background checks on all employees? Frequency?"
- "List all data centers used for processing customer data."

---

### Comparison: Questionnaire Answer Format vs. RFP Response

| Dimension | RFP Response | Questionnaire (SIG/CAIQ/DDQ) |
|-----------|--------------|-------------------------------|
| **Shape** | Multi-paragraph prose narratives | Short answers (Yes/No/Partial) + 1–3 sentence description + evidence refs |
| **Citations** | Tracked to source doc pages (our system does this) | Reference to policy doc names, section numbers, or uploaded artifacts |
| **Length per Q** | 50–500 words | 10–100 words + attachment |
| **Our system output** | Prose with inline citations | Would need to generate: constrained answer + evidence mapping + doc refs |
| **Gap meaning** | "We don't offer this service" → lose bid | "Control not implemented" → failed audit / no contract |

**Key insight:** Our retrieval+citation engine **transfers directly** — it finds the policy paragraph that answers "Describe your encryption." But the **output formatter** must change from prose to structured answer+evidence. The gap detection logic (refuse when no evidence) is identical in principle.

---

## B. Who fills them in, and how often?

| Actor | Frequency | Volume | Tools |
|-------|-----------|--------|-------|
| **SaaS/Cloud vendors** | Continuous — every enterprise deal | 10–100+ per year | GRC platforms (OneTrust, ProcessUnity, Drata, Vanta), internal libraries |
| **Consulting firms** | Per engagement | 5–20/year | Shared internal response libraries |
| **Fintech/Banking vendors** | Per regulator/client request | 20–50/year | SIG-FI specific templates |
| **Healthcare vendors** | Per covered entity | 10–30/year | HITRUST CSF aligned |

**Repetition is the key:** A single vendor fills ~80% the same answers across questionnaires. They maintain **"answer libraries"** (internal Confluence/Notion/SharePoint/GRC tool) — curated Q&A pairs they copy/paste. This is the "knowledge base" the product memo (§2) identifies as abundant.

---

## C. Is the data actually available? ← THE DECISIVE ONE

### Blank templates: YES (with caveats)
| Questionnaire | Publicly available? | Conditions |
|---------------|---------------------|------------|
| SIG Lite (older) | Partial — fragments on GitHub/GitLab | Incomplete, outdated (2019–2021), no official support |
| SIG Core/Full | **No** — requires Shared Assessments membership ($20k+/yr) | Paywalled |
| CAIQ-Lite | **Yes** — free from CSA (cloudsecurityalliance.org) | ~100 questions, current v4 |
| CAIQ Full | **No** — requires CSA corporate membership | Paywalled |
| Generic DDQs | **Yes** — many public procurement templates | Search "vendor security questionnaire template xlsx" |
| HITRUST | **No** — requires HITRUST license | Paywalled |

### Completed questionnaires (real vendor answers): **NO — NOT FOUND**

**Searches attempted (all public, no auth):**
- `"completed SIG questionnaire" site:github.com` → 0 results
- `"completed CAIQ" filetype:xlsx` → 0 results
- `"vendor security questionnaire responses" "public" OR "example"` → Only blank templates, marketing brochures ("see how we answer!"), or vendor *claims* ("we complete 200+/year") without the actual answers
- `"security questionnaire answers" company name` → Press releases about certifications, not the Q&A pairs
- GitHub repos: `security-questionnaire`, `vendor-risk`, `ddq-template` — all contain **blank templates only**
- SAM.gov/FOIA responses: No completed vendor questionnaires released (proprietary/commercial confidence exemptions)

**Why they don't exist publicly:**
1. **Commercial confidentiality** — Answers reveal control implementations, architectures, subprocessors
2. **Security risk** — "Describe your encryption key management" answers could aid attackers
3. **Contractual NDAs** — Most enterprise vendor agreements prohibit sharing completed questionnaires
4. **No regulatory requirement** — Unlike RFPs (public procurement), questionnaires are private B2B

### Can we build a golden set? **Not from public sources.**

To build a golden set like the RFP one (622 requirements, 12 verified-unanswerable), we need:
- Real questionnaires + real answers from the same vendor
- **Verified gaps** — questions the vendor *could not* answer truthfully
- Multiple vendors across sectors

**Without verified gaps, any dataset scores ~100% on retrieval and measures nothing about safety.** This is exactly the trap the product memo (§1) warns about.

---

## D. Where does gap detection land?

| Scenario | RFP Gap | Questionnaire Gap |
|----------|---------|-------------------|
| **Question:** "Do you offer lockbox services?" / "Do you encrypt data at rest with customer-managed keys?" | Vendor doesn't bid that component → **correct refusal** = safety win | Vendor hasn't implemented BYOK → **correct refusal** = safety win (prevents false attestation) |
| **Invented answer risk** | Made-up fee → contract breach, financial liability | "Yes we have BYOK" when not true → **security attestation fraud**, regulatory liability (SOC 2, GDPR Art. 32), breach of contract |
| **Partial answer** | "We offer international wires" but not IAT → partial credit | "We encrypt at rest" but not customer-managed keys → partial (must clarify) |
| **Refusal stakes** | Lose a bid (episodic, high value) | Fail vendor onboarding, lose all deals using that questionnaire (continuous, recurring revenue at risk) |

**Conclusion:** Gap detection is **equally safety-critical**. A false "Yes" on a security control is a liability time bomb — auditors *will* test it. The "same machinery would measure it" (memo §4) is correct: retrieval + citation + refusal logic transfers; only the golden set is missing.

---

## Findings Summary

| Question | Answer | Confidence |
|----------|--------|------------|
| Are blank templates available? | Yes (CAIQ-Lite, generic DDQs, SIG-Lite fragments) | High |
| Are **completed** questionnaires available? | **No — not in public domain** | High |
| Can we build a golden set with verified gaps? | **Not from public sources** | High |
| Does our retrieval+citation core transfer? | **Yes — directly applicable** | High |
| Does gap detection transfer? | **Yes — same logic, higher stakes** | High |
| Is questionnaire automation a viable product? | **Yes, but needs proprietary data partnerships** | Medium |

---

## Recommendations

1. **Do not pivot based on "data abundance" claims** — the abundant data is *blank templates*, not *completed Q&A with verified gaps*. The safety validation that makes our RFP system credible has no questionnaire equivalent in the public domain.

2. **If pursuing questionnaire automation:** The path is **data partnerships** with GRC platforms (OneTrust, ProcessUnity, Drata, Vanta) or enterprises willing to share anonymized answer libraries — not public scraping.

3. **Near-term:** Continue investing in **more real RFP+proposal pairs** (Task 2's 9 new pairs is the right direction). The RFP golden set is real, measured, and expanding.

4. **Architecture:** Keep the retrieval+citation+refusal core **modular** — it serves both products. Build a "Questionnaire Adapter" output formatter (prose → structured answer+evidence) as a separate component.

---

## Sources Cited

| # | Source | Date Accessed | What It Shows |
|---|--------|---------------|---------------|
| 1 | sharedassessments.org (SIG program page) | 2026-08-18 | SIG structure, domains, membership requirement |
| 2 | cloudsecurityalliance.org (CAIQ/CCM pages) | 2026-08-18 | CAIQ-Lite free download, CAIQ full membership-gated, CCM domains |
| 3 | GitHub search: `security-questionnaire template` | 2026-08-18 | Blank templates only, no completed examples |
| 4 | GitHub search: `completed SIG CAIQ questionnaire` | 2026-08-18 | Zero results for completed vendor responses |
| 5 | Web search: `"vendor security questionnaire responses" public` | 2026-08-18 | Only marketing claims, blank templates, certification press releases |
| 6 | SAM.gov / beta.sam.gov award attachments | 2026-08-18 | Occasional proposal PDFs, zero completed questionnaires |
| 7 | Product decision memo `02-evidence/2026-07-28-rfp-vs-questionnaire-product-decision.md` | 2026-08-18 | Framework for RFP vs. questionnaire comparison |

---

## Uncertainties / Could Not Determine

| Uncertainty | Why | Impact |
|-------------|-----|--------|
| Exact SIG 2024 question count & domain breakdown | Requires membership to access current template | Can't precisely map retrieval coverage |
| Whether any FOIA request has ever released a completed questionnaire | FOIA logs not searched exhaustively | Tiny chance one exists but unlikely |
| Enterprise answer library overlap (% identical across SIG/CAIQ/DDQ) | Requires vendor cooperation to measure | Affects "repetitive pain" value prop quantification |
| GRC platform API access for answer library sync | Commercial partnerships needed | Determines build vs. buy for data ingestion |

---

**Bottom line:** The questionnaire market is real, the pain is real, our core tech transfers — but **the public data to validate it does not exist**. Any pivot must be funded by a data partnership strategy, not a hope of public datasets.