#!/usr/bin/env python3
"""Deterministically slice an extracted manuscript into three reading windows.

Default: first 10%, middle 10%, last 10% by word count, snapped to paragraph
boundaries. Each slice is capped (default 12,000 words) so a very long book
cannot blow up the context window; capping is recorded in the output.

Usage:
    python3 sample_book.py <workdir> [--pct 10] [--cap 12000] [--windows 3]

Writes into <workdir>/samples/: opening.txt, middle.txt, ending.txt, plan.json
"""

import argparse
import json
from pathlib import Path


def slice_by_words(paras, offsets, total, start_frac, end_frac, cap):
    start_w, end_w = start_frac * total, end_frac * total
    idx = [i for i, off in enumerate(offsets)
           if off + len(paras[i].split()) > start_w and off < end_w]
    if not idx:
        idx = [min(range(len(offsets)), key=lambda i: abs(offsets[i] - start_w))]

    chosen, used, capped = [], 0, False
    for i in idx:
        w = len(paras[i].split())
        if used + w > cap and chosen:
            capped = True
            break
        chosen.append(i)
        used += w
    return {
        "first_paragraph": chosen[0],
        "last_paragraph": chosen[-1],
        "words": used,
        "capped": capped,
        "start_pct": round(offsets[chosen[0]] / total * 100, 1),
        "end_pct": round((offsets[chosen[-1]] + len(paras[chosen[-1]].split())) / total * 100, 1),
        "text": "\n\n".join(paras[i] for i in chosen),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir")
    ap.add_argument("--pct", type=float, default=10.0, help="percent of book per window")
    ap.add_argument("--cap", type=int, default=12000, help="max words per window")
    ap.add_argument("--windows", type=int, default=3, choices=(3, 5),
                    help="3 = open/middle/end; 5 adds quarter and three-quarter points")
    args = ap.parse_args()

    wd = Path(args.workdir)
    paras = [p for p in (wd / "full.txt").read_text("utf-8").split("\n\n") if p.strip()]
    manifest = json.loads((wd / "manifest.json").read_text("utf-8"))
    offsets, total = manifest["paragraph_word_offsets"], manifest["total_words"]

    f = args.pct / 100.0
    if args.windows == 3:
        spec = [("opening", 0.0), ("middle", 0.5 - f / 2), ("ending", 1.0 - f)]
    else:
        spec = [("opening", 0.0), ("quarter", 0.25 - f / 2), ("middle", 0.5 - f / 2),
                ("three_quarter", 0.75 - f / 2), ("ending", 1.0 - f)]

    out_dir = wd / "samples"
    out_dir.mkdir(exist_ok=True)
    plan = {"total_words": total, "pct_per_window": args.pct,
            "cap_per_window": args.cap, "windows": []}

    for name, start in spec:
        s = slice_by_words(paras, offsets, total, start, min(start + f, 1.0), args.cap)
        text = s.pop("text")
        (out_dir / f"{name}.txt").write_text(text, "utf-8")
        s["name"] = name
        s["file"] = str(out_dir / f"{name}.txt")
        plan["windows"].append(s)

    plan["total_sampled_words"] = sum(w["words"] for w in plan["windows"])
    plan["coverage_pct"] = round(plan["total_sampled_words"] / total * 100, 1)
    (out_dir / "plan.json").write_text(json.dumps(plan, indent=2), "utf-8")
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
