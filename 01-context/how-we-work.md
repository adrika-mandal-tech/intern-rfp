# How we work

Short, and the most important page in this folder. These aren't abstract values — each
one is here because ignoring it cost this project real time, and the stories are
included so the rules mean something.

---

## 1. Evidence before assertions

**Never claim something is done, working, or verified until you have run the check and
looked at the output.**

Not "this should work". Not "I've checked it carefully". Run it, read what came back,
then say what you found.

> An automated annotator on this project reported *"0 mismatches, verified
> programmatically."* An independent check of the same output found **16 entries** that
> didn't match the source. The report was confident, specific, and wrong.

Applies to you, to us, and to any tool either of us uses. A self-report is a claim, not
a verification.

## 2. A number that never moves isn't measuring anything

Before you trust a measurement, ask: **what would make this number go down?**

> A retrieval score of 87% looked healthy for days. The document it was scoring had
> failed extraction and was largely empty. The metric couldn't see the failure, so it
> reported success. Separately, a safety test passed at 12/12 — because two unrelated
> bugs cancelled each other out. Fixing either one alone would have made it *look*
> worse while actually being better.

If you can't describe the failure that would show up in your number, you haven't got a
measurement yet — you've got a reassuring number.

The practical version for your work: **a golden set with no verified negatives in it
cannot fail.** If every row is answerable, a system that answers everything scores
100%. That's the entire reason Task 1 pushes so hard for `none` rows.

## 3. Record *why*, not just *what*

When you make a judgement call, write down the reasoning next to the answer.

Six weeks later nobody can reconstruct why row 47 was marked `partial`, and the whole
row becomes unusable — you can't check reasoning you can't see. The annotation format
you'll use has a `reasoning` field for exactly this, and it is not optional.

This applies double to *negative* results. "Portal X does not publish received
proposals" is a genuinely useful finding — it stops the next person spending a day
re-discovering it. Write it down with the same care as a positive result.

## 4. "I don't know" is a complete and acceptable answer

There is no penalty here for not knowing something. There is a real penalty for
guessing and presenting it as fact, because someone downstream will build on it.

The good form is: *"I couldn't determine X. I checked A, B and C. A was inconclusive
because…, B and C didn't cover it. What I'd try next is D."* That's a useful
deliverable. "Probably around 60%" is not.

## 5. Strengthening a safety rule can make things worse

This one is subtle and it's the most interesting lesson the project has produced.

> To stop the system answering lockbox questions from general-banking text (§7 of
> [what-is-an-rfp.md](what-is-an-rfp.md)), we added a rule telling it to refuse when the
> evidence came from a different section. Safety improved. It also started refusing
> **18 out of 38 questions it could correctly answer** — because the section headings in
> an RFP and the section headings in a proposal are different documents' taxonomies,
> so they *always* differ.

A tool that refuses half the time gets switched off, and then it protects nobody. The
rule we learned:

> **Never measure what a safety rule catches without also measuring what it breaks.**
> Every safety test needs a counter-test.

The same shape appears in annotation work. If you resolve every hard call as `none` to
be safe, you produce a golden set that rewards a system for refusing everything. Be
strict where the rules say to be strict, and honest everywhere else.

## 6. Prefer the smaller, checkable claim

"The system is safe" is unfalsifiable. "Of 12 requirements verified to have no answer
in this proposal, the system correctly refused 9" is checkable, reproducible, and
somebody can disagree with it productively.

Write your findings in the second form. Always attach the sample size.

## 7. Things this project has learned the hard way

Practical traps, so you don't rediscover them:

- **PDF page numbers lie.** The number printed at the bottom of a page and the page's
  actual position in the file routinely disagree — in the U.S. Bank proposal the footer
  runs one behind. Everywhere in this project, "page" means the **PDF page index**,
  what your viewer's page counter shows.
- **A downloaded file isn't necessarily a PDF.** Some government sites return an HTML
  error page or a firewall block, saved under a `.pdf` filename. Always check the file
  actually opens and is the size you'd expect. Task 2 has a specific check for this.
- **The same boilerplate appears many times in a long proposal.** Searching for a phrase
  often lands you in the wrong section — one that repeats the same marketing language
  about a different service. Check the section heading before trusting a hit.
- **Two runs of the same thing don't always agree.** Mining the same RFP twice produced
  740 and 734 requirements. If a number matters, run it more than once and report the
  spread.

## 8. What good work looks like here

- It says what was measured, on what data, with what sample size.
- Its claims can be checked by someone else without asking you questions.
- It records the judgement calls and the reasoning behind them.
- It reports the things that didn't work as clearly as the things that did.
- It says "I don't know" where that's the truth.

Nothing about that requires seniority. It's just discipline, and it's the whole job.

---

**Next:** [glossary.md](glossary.md), then [../03-tasks/README.md](../03-tasks/README.md).
