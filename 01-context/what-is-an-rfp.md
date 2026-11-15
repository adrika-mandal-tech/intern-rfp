# What an RFP is, and why automating it is hard

Plain language. No prior knowledge assumed. Every example below is real, taken from
the two PDFs in [../05-source-docs/](../05-source-docs/).

---

## 1. The buying process

When a company wants to buy software, it just buys it. When the **State of Delaware**
wants to buy banking services for the whole state, it can't — public money has to be
spent competitively and transparently. So it runs a formal process:

1. **The State publishes an RFP** — "Request for Proposal". A long public document
   describing what it needs and asking vendors to explain how they'd provide it.
2. **Vendors respond with proposals.** Each one is a document — often longer than the
   RFP itself — answering every question the RFP asked.
3. **The State scores the proposals** against published criteria and awards the
   contract.

Our two source documents are a real example of both sides:

- `RFP_Delaware_BankingServices_TRE25101.pdf` — 127 pages. Delaware asking banks to
  bid for its banking services in 2025.
- `KB_USBank_Proposal_DE_TRE18101.pdf` — 214 pages. **U.S. Bank's genuine submitted
  proposal** to the same buyer for the same contract line, seven years earlier.

That pairing is not a coincidence, and it is the single most valuable asset this
project owns. More on why in §6.

## 2. What's actually inside an RFP

Open the Delaware RFP and page through it. You'll find it is several very different
documents stapled together:

| Pages (roughly) | What it is |
|---|---|
| Front section | Legal and administrative terms — insurance, contract conditions, submission deadlines, how to format your bid |
| **pp. 19–51** | **The Vendor Questionnaire** — hundreds of numbered questions the vendor must answer |
| pp. 52+ | More questionnaires, one per service line (Purchasing Card, ePayables, Pre-Paid Debit Card…) |
| Attachments | Pricing sheets, sample forms, exhibits |

The questionnaire is where the work is. Here is a real question from page 19
(requirement `R002` in our data):

> Provide a brief history of your organization, including your company's primary
> business focus, inclusive of acquisitions or mergers, how long you have been
> providing business banking including treasury management services and your
> experience providing such services to governmental and municipal entities.

And one from page 20 (`R011`):

> After the initial transition, how often will the primary relationship manager attend
> on-site meetings with State staff (at minimum quarterly meetings are required
> virtually with one annual in-person)? Describe a typical meeting agenda for this
> on-site meeting.

Notice two things that will matter a lot to you later:

- **They are not all questions.** `R002` is an imperative — "Provide a brief history".
  `R011` is a genuine question. Both are *requirements*: things the vendor must
  respond to. We call them requirements, not questions, for this reason.
- **`R011` is really two requirements in one sentence** — how often, *and* describe the
  agenda. A response can satisfy one and miss the other. This is extremely common and
  it is why "did the system answer it?" is often not a yes/no.

We counted **622 discrete requirements** in this one RFP.

## 3. What's inside a proposal

Now open the U.S. Bank proposal. It answers those questions, in order, in prose —
usually restating the question and then answering it. Page 13, for instance, opens the
company-history answer with:

> Our history dates back to 1863 when First National Bank of Cincinnati opened for
> business.

It also contains a great deal that is *not* an answer to anything: cover letters,
marketing pages, organisational charts, biographies, fee schedules, exhibits.

## 4. What we're building

The system takes an incoming RFP and a library of the company's past proposals, and
for each requirement it:

1. **Finds the requirement** in the RFP prose (this is called **mining**).
2. **Classifies it** — is this a technical question we can answer from past writing, or
   is it a pricing or legal question that a human must own?
3. **Searches the library** for relevant past text.
4. **Decides whether that text actually answers it** — and this is the hard step.
5. Either **drafts an answer with a page citation**, or **flags a gap** and routes the
   requirement to a human.

The output is a **compliance matrix**: one row per requirement, showing the status
(answered / partial / gap / human), the draft, and the citation. It is the artifact a
bid manager actually works from — a checklist proving every requirement got a
response, which is exactly what a buyer disqualifies you for missing.

## 5. Why step 4 is hard — the finding that shapes everything

You'd think you could measure how *similar* the retrieved text is to the question, and
call it a gap if similarity is low. We measured this properly. It does not work.

U.S. Bank's 2018 proposal contains **no lockbox response at all** — they simply chose
not to bid that service line. So every lockbox question in the 2025 RFP is a verified,
genuine gap. But the proposal is 214 pages of dense banking language, so when you
search it for a lockbox question you get back plenty of banking text that *sounds*
relevant. Measured:

|  | median similarity | lowest | highest |
|---|---|---|---|
| Questions that **are** answered (38) | 0.682 | **0.408** | 0.781 |
| Questions with **no answer at all** (12) | 0.426 | 0.332 | **0.678** |

**The ranges overlap.** Six of the twelve genuine gaps score higher than the
lowest genuine answer. There is no threshold that separates them.

The one-line explanation, which is worth memorising:

> **Similarity measures whether text is *about* a topic. It cannot tell you whether the
> text *answers* the question.**

Text about lockboxes, text about banking generally, and text that actually answers a
specific lockbox question all look similar to a search engine. So the *only* thing
standing between this product and an invented answer is a language model being asked,
explicitly, "do these excerpts answer this requirement — yes or no?" That single
judgement carries all the safety.

Which is why the twelve verified-unanswerable rows are the most valuable data we own,
and why growing that set is [your first task](../03-tasks/task-1-expand-golden-set.md).

## 6. Why one pair of documents is a problem

Everything above was measured against **one** RFP and **one** proposal.

Genuine submitted vendor proposals are almost never public. They're commercially
sensitive; vendors don't publish them and buyers usually aren't required to. We found
this one only because Delaware publishes the proposals it receives. We looked hard for
others in banking and finance and came up mostly empty.

That means every safety claim this project makes rests on a single document pair, in a
single industry, from a single vendor. We cannot currently tell the difference between
"the system is safe" and "the system happens to work on this document". A second
genuine pair would be the single highest-value thing anyone could add to this project,
which is [your second task](../03-tasks/task-2-source-real-pairs.md).

## 7. The scope trap — read this before you annotate
a lockbox is a service where commercial banks collect, process, and deposit customer payments for a business. 

One more finding, because you will hit it directly.

The system was asked a lockbox question about disaster recovery. There was no lockbox
disaster-recovery content, so it found the *general banking* disaster-recovery
section — genuinely well-written, genuinely about disaster recovery — and answered
from it, confidently, with a citation.

That answer is wrong, and dangerously so. A statement about how the general banking
platform recovers from a disaster is **not** a commitment about the lockbox service.
Submitting it would be claiming a capability that was never described.

> **Content about X for service A does not answer a question about X for service B.**

Humans make this mistake too — it looks like a reasonable answer. When you're
annotating, this is the judgement call you'll face most often, and our rule is strict:
**a requirement scoped to a service the vendor did not bid scores `none`, even if the
same capability is described elsewhere for a different service.** Task 1 explains why
the rule is that strict.

---

**Next:** open [RFP_AUTOMATION_EXPLAINER.html](RFP_AUTOMATION_EXPLAINER.html) in your
browser, then read [how-we-work.md](how-we-work.md).
