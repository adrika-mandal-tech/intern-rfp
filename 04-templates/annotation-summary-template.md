# Annotation summary — Task 1

Copy to `your-work/annotation-summary.md`. Write it while the work is fresh, not a week
later.

---

## 1. What was annotated

| | List A (random) | List B (lockbox) |
|---|---|---|
| Rows completed | | |
| `answered` | | |
| `partial` | | |
| `none` | | |
| Marked `low` confidence | | |

**Report the two lists separately and do not add them together.** List B deliberately
over-samples a service line the vendor didn't bid, so a combined rate would describe
neither the RFP nor anything else. (Task 1 §4 explains this.)

## 2. Verification

Output of `verify_quotes.py` on each file:

```
(paste it here)
```

- Any rows that came back `not_found` or `off_by`, and what you did about them:

## 3. Rows I want a second opinion on

The ones where the rules didn't cleanly resolve it. For each: the `req_id`, the verdict
you recorded, and one or two sentences on the tension.

These are valuable — the existing golden set has five such rows and each one exposed a
real definitional question about the product. Don't under-report them to look decisive.

| req_id | My verdict | Why it's unclear |
|---|---|---|
| | | |

## 4. Traps and surprises

Things that made a row hard, that weren't already listed in Task 1 §7. Both previous
annotators found traps nobody had documented, and those findings changed how the system
gets built — so this section is a real deliverable, not a postscript.

Examples of the kind of thing worth recording: page numbering that doesn't behave as
documented, content that straddles page breaks in a way that breaks searching, tables
that don't read as text, repeated boilerplate that sends searches to the wrong place.

## 5. Anything I noticed about the documents themselves

Free text. You've now read this proposal more closely than anyone else here. Anything
odd, interesting, or that made you think differently about the problem?

Particularly: were there places where you thought *"a system could never get this right
from the text alone"*? Those are worth knowing about.

## 6. How the rules held up

- Did Rules 1–3 (Task 1 §6) cover the cases you hit?
- Was any of them ambiguous in practice?
- Would you add a fourth rule? What would it say?

A rule that turned out to be incomplete is a finding about the rule, not about you.
