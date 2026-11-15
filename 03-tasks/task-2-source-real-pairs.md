# Task 2 — Source new RFP → proposal pairs

**Time:** about 4–5 days · **Deliverable:** a source log, any PDFs you find, and a
findings memo — all in `your-work/`

---

## 1. What you're doing

Finding more pairs of documents like the two in `05-source-docs/`: **a real RFP, and a
real proposal that a real vendor actually submitted in response to it.**

## 2. Why it matters

We own exactly one such pair. Every safety finding, every measurement, every claim this
project makes comes from it. We currently cannot distinguish "the system works" from
"the system works on this document".

A second genuine pair roughly doubles the evidence base. It's the highest-value single
addition anyone could make to this project, and our own product memo names it as the
answer to our biggest structural weakness.

## 3. Read this before you begin: this task may not succeed, and that's expected

Genuine submitted proposals are **hard to find, by their nature**. They're commercially
sensitive. Vendors don't publish them. Most buyers aren't required to. We searched
across banking and finance and found one.

So this brief is written differently from Task 1. **Success is tiered**, and every tier
is a real deliverable:

| Tier | What you found | Value |
|---|---|---|
| **A** | A genuine submitted proposal **and** the RFP it responds to | The goal. Even one is a significant contribution. |
| **B** | A genuine submitted proposal, RFP not findable | Still valuable — it's knowledge-base material |
| **C** | A *source* that publishes received proposals — a portal, an agency, a records archive — even if you didn't extract a usable pair | Very valuable. A repeatable source beats a lucky find. |
| **D** | A documented list of places that **don't** work, and why | **Genuinely useful.** It stops the next person spending a week rediscovering it. |

**Finishing at tier D is a successful outcome of this task**, provided the log is
specific enough that someone else can trust it and not repeat the work. What would make
this task fail is spending a week searching and producing nothing anyone can read.

So: **log as you go, from hour one.** The log is the deliverable. Anything you find is
a bonus on top of it.

## 4. How the one pair we have was found — the mechanism to exploit

Worth understanding, because it tells you what to look for.

In the United States, when a government body buys something, the proposals it receives
generally become **public records** after the award. Most agencies don't publish them
proactively — you'd have to file a records request. **Delaware does.** The state
treasurer's site posts the proposals it received alongside the RFP.

That's it. That's the whole mechanism. We didn't find a clever search; we found *an
agency with a proactive publication habit.*

Which means your highest-value target is not a document — **it's another agency with
that habit.** Find one and you get many pairs, not one.

Two specifics from that hunt, worth carrying:

- **Delaware's document server refuses some automated download tools while serving the
  same URL fine to a browser.** If a download misbehaves, try just opening the link in
  your browser and saving the file. And it rate-limits — a URL that worked ten minutes
  earlier can start returning an error page.
- **A file named `.pdf` isn't necessarily a PDF.** That server returned a 245-byte HTML
  block page saved under a `.pdf` name. §7 has the check.

## 5. Where to look

Treat all of these as **leads to verify, not a list of known-good sources.** Only the
Delaware one is proven. Confirming or ruling out each of the others is the work.

**Proven**
- The State of Delaware's treasury and bid-document sites — this is where our pair came
  from. Worth mining further: if they published one procurement's proposals, they may
  have published others.

**Strong hypotheses — the mechanism exists, we haven't checked**
- **Other US state treasuries and procurement portals.** Delaware isn't special
  legally; the habit is what varies. Work through states methodically and record what
  each one publishes. This is the single most systematic angle available to you.
- **Large city and county procurement portals.** Municipalities often run smaller, less
  polished sites — which sometimes means less filtering of what gets posted.
- **Public universities and school districts.** Same public-records regime, often very
  open document practices.
- **Transit authorities, port authorities, utility districts.** Big procurements, and
  they publish heavily.
- **Public-records request archives.** Some agencies run a portal where fulfilled
  records requests and their released documents stay publicly browsable. If someone has
  already requested a winning proposal, the PDF may be sitting there. Sites that host
  released public-records documents publicly are worth investigating for the same
  reason.
- **Award and protest documentation.** When a losing bidder protests an award, the
  decision documents sometimes quote or attach proposal content.

**Search recipes worth trying**

Search engines index a lot of these PDFs directly. The trick is searching for language
that appears in **proposals** rather than in RFPs — the two are easy to confuse and the
web is flooded with RFPs.

Phrases that tend to appear in a submitted proposal and rarely elsewhere:

- `"in response to RFP"` + a service word + `filetype:pdf`
- `"we are pleased to submit"` + `proposal` + `filetype:pdf`
- `"Proposal submitted by"` / `"Prepared for the"` + a state or agency name
- `"Technical Proposal"` + `"RFP #"` + `filetype:pdf`
- Combine with a sector: `banking services`, `treasury management`, `staffing`, `IT
  managed services`, `construction management`

**The reverse direction is usually easier, and most people miss it.** Proposals are rare;
RFPs are everywhere. So *start from the proposal*. Once you have one, it will name the
RFP number it's responding to somewhere in its first few pages — then search that number
and you'll usually find the RFP quickly. Hunting for an interesting RFP first and hoping
its proposals exist is the slow direction.

**Sectors to prefer.** Anything is useful, but a pair in a *different* industry from
banking is worth more to us than another banking pair, because it tests whether our
findings generalise. IT services, staffing, construction, consulting and facilities
management are all good.

## 6. Rules

- **Public, freely accessible documents only.** If it's behind a login, a paywall, or a
  registration form, stop — don't sign up, don't pay, don't create an account.
- **Don't misrepresent who you are** to obtain a document, and don't file records
  requests. If you find something that *would* need a request, log it as a lead and stop
  there.
- **Don't hammer a site.** If downloads start failing, you're likely being rate-limited;
  slow down or move on.
- If you're unsure whether something is fair to download, **ask before downloading**.

## 7. Verify everything you find

Every candidate gets checked against all four before it goes in the log as a find:

**1. Is it actually a PDF?** Open it. Check the file size is plausible (a real proposal
is megabytes, not kilobytes). A 200-byte file is a block page wearing a `.pdf` name.

**2. Is it a *genuine submitted* proposal?** This is the check people get wrong. It is
**not** a proposal if it's:
   - a *template* or *sample response form* the buyer published for vendors to fill in
   - a vendor's marketing brochure or capability statement
   - a consultant's *report* about a procurement
   - a "sample proposal" from a proposal-writing service

   It **is** a proposal if it's addressed to a specific buyer, references a specific
   RFP or solicitation number, is written in the vendor's voice ("U.S. Bank will…"),
   and answers the buyer's questions in order. A cover letter on vendor letterhead
   addressed to a named procurement officer is a strong signal.

**3. Can you identify the RFP it responds to?** Look in the first few pages for a
solicitation number. Record it even if you can't find the RFP itself — that turns a
tier-B find into a tier-A lead for someone else.

**4. Is it substantial?** A 4-page response has little to retrieve from. Prefer
anything over ~40 pages, and note the page count either way.

## 8. Keep the log as you go

Use [../04-templates/source-candidate-log.md](../04-templates/source-candidate-log.md).
One row per thing you check — **including the dead ends**, which are most of the value
in tiers C and D.

Each row records: what you checked, the URL, what you were hoping for, what you actually
found, and the verdict (`pair` / `proposal only` / `RFPs only` / `nothing usable` /
`blocked`). Two lines each. Do it as you go — reconstructing it on Friday from browser
history doesn't work and the detail that mattered will be gone.

**Be specific in the negatives.** "Nothing there" is worth little. "Publishes RFPs and
award notices, but no received proposals; checked 12 solicitations across 2023–2025" is
worth a lot — it's a conclusion someone can rely on instead of repeating.

## 9. Definition of done

- [ ] `source-candidate-log.md` completed, covering everything you checked — at least 25
      distinct sources, and more if they're going quickly.
- [ ] Any PDFs found saved in `your-work/found-documents/`, named clearly
      (`PROPOSAL_<vendor>_<buyer>_<year>.pdf`, `RFP_<buyer>_<number>_<year>.pdf`).
- [ ] Each find verified against all four checks in §7, with the results recorded.
- [ ] A findings memo from
      [../04-templates/sourcing-findings-template.md](../04-templates/sourcing-findings-template.md)
      answering:
      1. What did you find? (by tier)
      2. **Which sources publish received proposals, and which don't?** — the most
         reusable output of this task
      3. What search techniques worked, and which wasted time?
      4. If you had another week, where would you look next and why?

## 10. If you're getting nowhere

Normal. Expected. Read §3 again.

Things to try before concluding:

- **Switch industries.** Banking was hard. Construction, IT services and staffing
  procurements are more numerous and often more openly documented.
- **Switch to the reverse direction** (§5) if you've been starting from RFPs.
- **Go smaller.** Big state portals are professionally managed and filtered. A county
  water district's site is more likely to have posted something it didn't think about.
- **Follow a portal, not a query.** Pick one agency and read *everything* it publishes
  for one procurement. Understanding one agency's publication habit end-to-end is worth
  more than fifty shallow searches.
- **Check in.** If two days in you have no tier A/B/C, say so — that's a useful signal
  in itself and worth a conversation rather than a third day of the same approach.

---

**Next:** [task-3-questionnaire-landscape.md](task-3-questionnaire-landscape.md)
