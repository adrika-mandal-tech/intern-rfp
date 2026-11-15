"""Draw the two annotation worklists for Task 1.

    python tools/make_worklist.py

Writes into your-work/:
    worklist_A_random.jsonl   40 rows, stratified across sections, unbiased
    worklist_B_lockbox.jsonl  20 rows, drawn only from the Lockbox questionnaire

The output files ship with this pack already drawn, so you do not need to run
this. It is here so the draw is reproducible and so you can see exactly how the
sample was chosen -- which matters, because how a sample was drawn decides what
its scores are allowed to mean.

Why two lists rather than one
-----------------------------
List A is a fair sample. Scores computed over it describe the RFP as a whole.

List B is deliberately unfair: it over-samples the Lockbox Services questionnaire
because U.S. Bank did not bid lockbox, so those rows are the cheapest source of
verified `none` verdicts -- the rows the safety measurement is starved of. That
bias is useful for building a safety sample and *invalid* for computing a headline
rate. A gap-detection score over list B would look impressive and mean nothing.

Keeping them in separate files makes that distinction structural rather than
something a reader has to remember.

Exclusions applied to both draws:
    - requirements already in the 50-row golden set (no paying twice)
    - `pricing` and `admin` classes -- routed to a human by policy regardless of
      whether the library can answer them, so knowledge-base evidence is neither
      expected nor wanted
    - rows with no class recorded, and rows not captured verbatim
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WORK = os.path.join(HERE, "work")
OUT = os.path.join(ROOT, "your-work")

SEED = 20260805
N_RANDOM = 40
N_LOCKBOX = 20
NON_GENERATIVE = {"pricing", "admin"}


def load_requirements() -> list[dict]:
    rows = []
    for name in ("requirements_pp19-51.jsonl", "requirements_pp52plus.jsonl"):
        with open(os.path.join(WORK, name), encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    rows.append(json.loads(line))
    return rows


def already_done() -> set[str]:
    path = os.path.join(ROOT, "02-evidence", "golden_set_50rows.jsonl")
    ids = set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                ids.add(json.loads(line)["req_id"])
    return ids


def eligible(row: dict, done: set[str]) -> bool:
    if row["id"] in done:
        return False
    cls = (row.get("class") or "").strip()
    if not cls or cls in NON_GENERATIVE:
        return False
    if row.get("verbatim") is False:
        return False
    return bool((row.get("text") or "").strip())


def blank(row: dict) -> dict:
    """A worklist row: the requirement, plus the fields you fill in."""
    return {
        "req_id": row["id"],
        "rfp_page": row.get("page"),
        "section": row.get("section"),
        "class": row.get("class"),
        "requirement": row.get("text"),
        # ---- you fill in everything below ----
        "doc": "kb",
        "verdict": "",
        "page": 0,
        "quote": "",
        "confidence": "",
        "reasoning": "",
    }


def stratified(rows: list[dict], n: int, rng: random.Random) -> list[dict]:
    """Round-robin across top-level sections, each pool shuffled once.

    Shuffling once and consuming with an advancing cursor is deliberate: an
    earlier version of this reshuffled inside the selection loop, which let the
    same requirement be drawn more than once. It produced 50 target lines holding
    41 unique rows and nobody noticed until the counts were reconciled.
    """
    pools: dict[str, list[dict]] = collections.defaultdict(list)
    for row in rows:
        pools[(row.get("section") or "").split(" / ")[0]].append(row)
    for pool in pools.values():
        rng.shuffle(pool)

    order = sorted(pools, key=lambda k: (-len(pools[k]), k))
    cursors = dict.fromkeys(order, 0)
    picked: list[dict] = []
    while len(picked) < n:
        progressed = False
        for key in order:
            if len(picked) >= n:
                break
            index = cursors[key]
            if index < len(pools[key]):
                picked.append(pools[key][index])
                cursors[key] = index + 1
                progressed = True
        if not progressed:
            break

    ids = [p["id"] for p in picked]
    assert len(ids) == len(set(ids)), "duplicate requirement drawn"
    return picked


def has_annotations(path: str) -> bool:
    """True if someone has already filled a verdict into this worklist."""
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip() and json.loads(line).get("verdict"):
                return True
    return False


def write(path: str, rows: list[dict], force: bool) -> None:
    if has_annotations(path) and not force:
        print(f"REFUSED {os.path.basename(path)}: it already holds annotations.")
        print("        Re-drawing would destroy them. Move the file aside first,")
        print("        or pass --force if you are certain you want it overwritten.")
        return
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(blank(row), ensure_ascii=False) + "\n")
    counts = collections.Counter((r.get("section") or "").split(" / ")[0] for r in rows)
    print(f"{os.path.basename(path)}: {len(rows)} rows")
    for key, count in counts.most_common():
        print(f"    {count:3d}  {key}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Draw the Task 1 annotation worklists.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite a worklist even if it already contains annotations",
    )
    args = parser.parse_args()

    os.makedirs(OUT, exist_ok=True)
    done = already_done()
    rows = [r for r in load_requirements() if eligible(r, done)]
    print(f"{len(rows)} eligible requirements ({len(done)} already annotated, excluded)\n")

    rng = random.Random(SEED)
    lockbox = [r for r in rows if "ockbox" in (r.get("section") or "")]
    write(os.path.join(OUT, "worklist_A_random.jsonl"), stratified(rows, N_RANDOM, rng), args.force)

    rng_b = random.Random(SEED + 1)
    rng_b.shuffle(lockbox)
    write(os.path.join(OUT, "worklist_B_lockbox.jsonl"), lockbox[:N_LOCKBOX], args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
