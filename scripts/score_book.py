#!/usr/bin/env python3
"""Turn a filled ratings file into a weighted score and a report.

    python3 score_book.py <ratings.json> [--matrix corpus/matrix.json] [--md out.md]

Enforces the evidence rule mechanically: score 1 needs >=1 verbatim manuscript
quote, score 2 needs >=2. Violations are errors, not warnings — the report will
not be produced. `not_assessable` drivers are excluded and their weight is
redistributed across the drivers that were assessed.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BANDS = [
    (80, "Pursue", "Profile matches the corpus's discriminating drivers closely."),
    (65, "Strong consider", "Several high-weight drivers strongly evidenced."),
    (50, "Consider", "Mixed profile; identifiable strengths and identifiable gaps."),
    (35, "Weak consider", "Few high-weight drivers evidenced in the sampled text."),
    (0, "Pass on text basis", "Sampled text evidences little of what the corpus rewards."),
]


def band(score):
    for cut, label, note in BANDS:
        if score >= cut:
            return label, note
    return BANDS[-1][1], BANDS[-1][2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ratings")
    ap.add_argument("--matrix", default=str(ROOT / "corpus" / "matrix.json"))
    ap.add_argument("--md", default=None)
    args = ap.parse_args()

    r = json.loads(Path(args.ratings).read_text("utf-8"))
    mpath = Path(args.matrix)
    if not mpath.exists():
        sys.exit(f"no matrix at {mpath} — run build_matrix.py (Phase A) first")
    matrix = json.loads(mpath.read_text("utf-8"))
    weights = {w["driver"]: w for w in matrix["intrinsic_weights"]}

    errs, assessed = [], []
    for item in r.get("ratings", []):
        did = item.get("driver")
        if did not in weights:
            errs.append(f"{did}: not an intrinsic driver in the matrix")
            continue
        if item.get("not_assessable"):
            continue
        score = item.get("score")
        if score not in (0, 1, 2):
            errs.append(f"{did}: score must be 0, 1 or 2")
            continue
        quotes = [e for e in item.get("evidence", []) if (e.get("quote") or "").strip()]
        if score >= 1 and len(quotes) < score:
            errs.append(f"{did}: score {score} needs {score} verbatim quote(s), got {len(quotes)}")
            continue
        assessed.append((did, score, quotes, item.get("note", "")))

    missing = set(weights) - {a[0] for a in assessed} - {
        i["driver"] for i in r.get("ratings", []) if i.get("not_assessable")}
    for did in sorted(missing):
        errs.append(f"{did}: no rating supplied (use score 0 or not_assessable)")

    if errs:
        print(f"{len(errs)} problem(s) — no report produced:", file=sys.stderr)
        for e in errs:
            print("  - " + e, file=sys.stderr)
        sys.exit(1)

    wsum = sum(weights[d]["weight"] for d, *_ in assessed) or 1.0
    earned = sum(weights[d]["weight"] * (s / 2) for d, s, *_ in assessed)
    # Whole numbers only: one driver moving one point shifts the score by roughly
    # 3 points, so decimals would imply resolution the method does not have.
    score = round(earned / wsum * 100)
    label, note = band(score)
    near = min((abs(score - cut) for cut, *_ in BANDS if cut), default=99)
    boundary = (
        f"\n**This score sits within {near} point(s) of a band boundary.** The "
        "method's resolution is about ±3 points, so the neighbouring band is not "
        "ruled out. Treat the driver profile below as the finding, not the label."
        if near <= 3 else ""
    )

    lc = [d for d, *_ in assessed if weights[d]["low_confidence"]]
    rows = sorted(assessed, key=lambda a: -weights[a[0]]["weight"])

    lines = [
        f"# Manuscript appraisal — {r.get('title', 'untitled')}",
        "",
        f"**Author:** {r.get('author', 'n/a')}  ",
        f"**Declared track:** {r.get('track', 'n/a')} · **Category:** {r.get('category', 'n/a')}",
        "",
        f"## Score: {score} / 100 — {label}",
        "",
        note,
        boundary,
        "",
        "## Driver profile",
        "",
        "| Driver | Weight | Score | Contribution | Evidence |",
        "|---|---:|---:|---:|---|",
    ]
    for did, s, quotes, _ in rows:
        w = weights[did]["weight"]
        ev = quotes[0]["quote"][:70] + "…" if quotes else "no evidence in sample"
        lines.append(f"| `{did}` | {w:.3f} | {s} | {w * s / 2 * 100 / wsum:.1f} | {ev} |")

    na = [i["driver"] for i in r.get("ratings", []) if i.get("not_assessable")]
    if na:
        lines += ["", f"**Not assessable from the sampled windows:** {', '.join(na)}."]

    lines += ["", "## Unknowable from the manuscript", "",
              "These drove books in the corpus but cannot be judged from a text file. "
              "A human must assess them before any acquisition decision:", ""]
    for f in matrix["extrinsic_prevalence"]:
        lines.append(f"- `{f['driver']}` — present in {f['n_bestsellers']} corpus bestsellers")

    lines += ["", "## Method and limitations", "",
              f"Corpus: {matrix['corpus_size']['bestsellers']} bestsellers and "
              f"{matrix['corpus_size']['control']} well-reviewed non-sellers across "
              f"{len(matrix['corpus_size']['buckets'])} five-year bucket(s).", ""]
    for lim in matrix["limitations"]:
        lines.append(f"- {lim}")
    if lc:
        lines.append(f"- Thin evidence behind the weights for: {', '.join(sorted(lc))}.")
    lines += ["- Scoring used a sample of the manuscript, not the whole text: "
              f"{r.get('sampling_summary', 'see samples/plan.json')}.",
              "- This is a pattern-match against past bestsellers, not a prediction. "
              "It cannot see novelty, and the corpus cannot contain the next new thing."]

    md = "\n".join(lines)
    if args.md:
        Path(args.md).write_text(md, "utf-8")
        print(f"wrote {args.md}")
    print(json.dumps({"score": score, "band": label,
                      "assessed_drivers": len(assessed)}, indent=2))
    if not args.md:
        print("\n" + md)


if __name__ == "__main__":
    main()
