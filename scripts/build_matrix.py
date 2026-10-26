#!/usr/bin/env python3
"""Validate the corpus and derive the weighted scoring matrix.

    python3 build_matrix.py --validate     # schema + evidence-bar check only
    python3 build_matrix.py                # write corpus/matrix.json

Weighting (deliberately simple and explainable):

    p_best  = smoothed prevalence of the driver among bestsellers
    p_ctrl  = smoothed prevalence among the control set
    disc    = clamp(p_best - p_ctrl, 0, 1)          # discriminating power
    weight  = p_best * (0.25 + 0.75 * disc)         # common-but-undiscriminating
                                                    # drivers keep a floor share
    normalised so the intrinsic weights sum to 1.

Prevalence uses Laplace smoothing (k+1)/(n+2) because the control set is small.
Evidence confidence is weighted: `documented` = 1.0, `attributed` = 0.5.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY = ROOT / "references" / "driver-taxonomy.md"
CORPUS = ROOT / "corpus"

CONFIDENCE_WEIGHT = {"documented": 1.0, "attributed": 0.5}


def load_taxonomy():
    """Parse driver IDs out of the taxonomy tables; Part 1 = intrinsic."""
    text = TAXONOMY.read_text("utf-8")
    parts = re.split(r"^## Part \d.*$", text, flags=re.M)
    if len(parts) < 3:
        raise SystemExit("taxonomy: could not find Part 1 / Part 2 sections")
    ids = lambda s: [m.group(1) for m in re.finditer(r"^\|\s*`([A-Z_]+)`", s, re.M)]
    intrinsic, extrinsic = ids(parts[1]), ids(parts[2])
    if not intrinsic or not extrinsic:
        raise SystemExit("taxonomy: no driver IDs parsed")
    return intrinsic, extrinsic


def load_set(name):
    books, files = [], sorted((CORPUS / name).glob("*.json"))
    for f in files:
        data = json.loads(f.read_text("utf-8"))
        for b in data.get("books", []):
            b["_bucket"] = data.get("bucket", f.stem)
            b["_file"] = f.name
            books.append(b)
    return books, files


def validate(books, intrinsic, extrinsic, is_control):
    known, errs = set(intrinsic) | set(extrinsic), []
    for b in books:
        where = f"{b.get('_file')}:{b.get('id') or b.get('title', '?')}"
        for field in ("title", "author", "year", "track"):
            if not b.get(field):
                errs.append(f"{where}: missing `{field}`")
        if is_control and len(b.get("non_sale_evidence") or []) < 2:
            errs.append(f"{where}: control needs >=2 non_sale_evidence proxies")
        if not is_control and not b.get("sales_evidence"):
            errs.append(f"{where}: no sales_evidence")
        seen = set()
        for d in b.get("drivers", []):
            did = d.get("driver")
            if did not in known:
                errs.append(f"{where}: unknown driver {did!r}")
                continue
            if did in seen:
                errs.append(f"{where}: duplicate driver {did}")
            seen.add(did)
            if d.get("confidence") not in CONFIDENCE_WEIGHT:
                errs.append(f"{where}/{did}: confidence must be documented|attributed")
            if not (d.get("quote") or "").strip():
                errs.append(f"{where}/{did}: missing verbatim quote")
            elif len((d["quote"]).split()) > 25:
                errs.append(f"{where}/{did}: quote exceeds 25 words")
            if not (d.get("url") or "").strip():
                errs.append(f"{where}/{did}: missing url")
        n = len(seen)
        if n < 3 and not b.get("evidence_thin"):
            errs.append(f"{where}: only {n} drivers — set evidence_thin:true or research further")
    return errs


def prevalence(books, driver):
    """Confidence-weighted count of books evidencing this driver."""
    total = 0.0
    for b in books:
        best = 0.0
        for d in b.get("drivers", []):
            if d.get("driver") == driver:
                best = max(best, CONFIDENCE_WEIGHT.get(d.get("confidence"), 0.0))
        total += best
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    args = ap.parse_args()

    intrinsic, extrinsic = load_taxonomy()
    best, best_files = load_set("bestsellers")
    ctrl, ctrl_files = load_set("control")

    errs = validate(best, intrinsic, extrinsic, False)
    errs += validate(ctrl, intrinsic, extrinsic, True)
    if errs:
        print(f"{len(errs)} validation problem(s):", file=sys.stderr)
        for e in errs:
            print("  - " + e, file=sys.stderr)
        if args.validate:
            sys.exit(1)
        sys.exit("refusing to build a matrix from an invalid corpus")
    print(f"corpus OK: {len(best)} bestsellers ({len(best_files)} buckets), "
          f"{len(ctrl)} control ({len(ctrl_files)} buckets)")
    if args.validate:
        return

    if not best:
        sys.exit("no bestseller records — run Phase A first")

    nb, nc = len(best), len(ctrl)
    rows = []
    for did in intrinsic:
        kb, kc = prevalence(best, did), prevalence(ctrl, did)
        p_best = (kb + 1) / (nb + 2)
        p_ctrl = (kc + 1) / (nc + 2) if nc else None
        disc = max(0.0, min(1.0, p_best - p_ctrl)) if p_ctrl is not None else 0.5
        rows.append({
            "driver": did,
            "n_bestsellers": round(kb, 1), "n_control": round(kc, 1),
            "p_bestsellers": round(p_best, 3),
            "p_control": round(p_ctrl, 3) if p_ctrl is not None else None,
            "discrimination": round(disc, 3),
            "weight_raw": p_best * (0.25 + 0.75 * disc),
            "low_confidence": kb < 5 or nc < 10,
        })

    total = sum(r["weight_raw"] for r in rows) or 1.0
    for r in rows:
        r["weight"] = round(r["weight_raw"] / total, 4)
        del r["weight_raw"]
    rows.sort(key=lambda r: -r["weight"])

    ext = sorted(
        ({"driver": d, "n_bestsellers": round(prevalence(best, d), 1)} for d in extrinsic),
        key=lambda r: -r["n_bestsellers"],
    )

    matrix = {
        "corpus_size": {"bestsellers": nb, "control": nc,
                        "buckets": sorted({b["_bucket"] for b in best})},
        "method": "weight = p_best * (0.25 + 0.75 * clamp(p_best - p_ctrl, 0, 1)), "
                  "Laplace-smoothed, confidence-weighted, normalised to sum 1",
        "limitations": [
            "Control group is small and non-random: it shows what distinguishes these "
            "bestsellers from these well-reviewed non-sellers, not what causes sales.",
            "Survivorship bias remains: unpublished and unreviewed books are absent.",
            "Extrinsic drivers are excluded from scoring but often dominate real outcomes.",
        ],
        "intrinsic_weights": rows,
        "extrinsic_prevalence": ext,
    }
    out = CORPUS / "matrix.json"
    out.write_text(json.dumps(matrix, indent=2), "utf-8")
    print(f"wrote {out}")
    for r in rows[:8]:
        flag = "  (low confidence)" if r["low_confidence"] else ""
        print(f"  {r['weight']:.4f}  {r['driver']}{flag}")


if __name__ == "__main__":
    main()
