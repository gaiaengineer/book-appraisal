# Phase A — corpus build protocol

Goal: a citable evidence base of *why specific books sold*, plus a control set of
*books that were good but did not sell*, from which the scoring matrix is derived.

Run one bucket at a time. Each bucket is self-contained and resumable — write the
JSON file at the end of each bucket before starting the next.

---

## 1. Buckets and quotas

| Bucket | Bestsellers | Control |
|--------|-------------|---------|
| 1995–1999 | 15 | 4 |
| 2000–2004 | 15 | 4 |
| 2005–2009 | 15 | 4 |
| 2010–2014 | 15 | 4 |
| 2015–2019 | 15 | 4 |
| 2020–2024 | 15 | 4 |

Within each bucket's 15, aim for roughly:

- **9 × Track A — trade/mainstream:** traditionally published fiction that hit
  NYT/Sunday Times lists, won or shortlisted for major prizes, or both.
- **6 × Track B — genre/commercial/author-native:** mass-market genre, self-published
  or Amazon-native, KU-driven, or social-media-driven titles. For pre-2010 buckets
  Track B means mass-market genre paperback (romance, thriller, fantasy) rather
  than self-publishing, which barely existed at scale before Kindle in 2007.

Include at least 2 non-US-origin titles per bucket where the evidence supports it.
Do not fill quota with sequels by an author already in the same bucket.

---

## 2. Source hierarchy

**`references/sources.md` is the full registry** — named sources per tier with URLs,
access quirks, and a provenance log of what has already been researched. Read it
before you start searching, and append the bucket's provenance to its Part 2 when
you finish. The summary below is the shape; that file is the detail.

Use the highest tier available for each claim.

**Tier 1 — sales and honours (for *selection*, i.e. "did it sell?")**
NYT Best Sellers list archive · Sunday Times / Bookseller charts · Nielsen
BookScan figures reported in trade press · Publishers Weekly annual bestseller
tallies · Booker, Pulitzer, Women's Prize, National Book Award, Hugo, Nebula,
Edgar, RITA/Vivian official records · Goodreads Choice Awards.

**Tier 2 — reception and reasons (for *drivers*, i.e. "why did it sell?")**
Reviews in NYT, Guardian, Washington Post, TLS, Kirkus, Publishers Weekly,
Booklist, LA Times · trade analysis in The Bookseller and Publishers Weekly ·
prize citations · publisher-reported advance/print-run figures in trade press.

**Tier 3 — supporting context**
Author interviews · Goodreads/StoryGraph aggregate rating counts · documented
BookTok view counts · book club selection announcements.

**Not acceptable as evidence:** blog opinion without an identifiable outlet,
retailer marketing copy, AI-generated summaries, Wikipedia plot sections, your own
reading of the book, "it is well known that…".

---

## 3. The evidence bar

Every driver attributed to a book requires **all** of:

1. A **verbatim quote** of ≤25 words from the source, in quotation marks.
2. The **source name**, **URL**, and **publication date**.
3. A **driver ID** from `driver-taxonomy.md`.
4. A **confidence tier**:
   - `documented` — the source explicitly names this quality as a reason for the
     book's success or appeal.
   - `attributed` — the source praises this quality prominently but does not tie it
     to sales.
   - Nothing else is recordable. If it is neither, drop it.

Maximum 2 quotes per individual source per book — synthesise, don't transcribe.

**Hard prohibitions.** Do not record a driver because it seems plausible, because
the genre usually has it, because other books in the bucket have it, or because you
recall the book. No quote → no driver. If a book yields fewer than 3 evidenced
drivers after a genuine search, keep it with what it has and set
`"evidence_thin": true` rather than padding it.

---

## 4. The control set

Purpose: without it, the matrix only shows what bestsellers have in common, which
is not the same as what makes books sell. The control isolates drivers that are
*discriminating* rather than merely *common*.

**Control criteria — a book qualifies if all hold:**
- Published in the bucket's window, in the same broad market.
- Received at least one Tier-2 positive review (starred trade review, major
  broadsheet review, or a prize longlisting).
- Shows no evidence of bestseller-scale readership.

**Evidence of non-selling is scarce; use these checkable proxies, in order:**
1. Absent from NYT/Sunday Times list archives for its publication year.
2. Goodreads/StoryGraph rating count at least an order of magnitude below the
   bucket's bestsellers — record the actual number and the date you checked it.
3. No mass-market/paperback reissue, or went out of print.
4. Trade-press or author statements about disappointing sales.
5. Inclusion in a reputable outlet's "overlooked/underrated books of <year>" feature.

Record which proxies applied in `non_sale_evidence`. A control book needs at least
proxies 1 and 2.

Goodreads blocks WebFetch and returns the wrong book for guessed IDs. Get counts
from the Goodreads **search listing** in the browser tool — it prints
`avg rating — N ratings` directly, e.g.
`https://www.goodreads.com/search?q=Assembly+Natasha+Brown`. Always record the
number and the date you checked it; these counts drift. Score its drivers with the same evidence bar as bestsellers —
reviews of well-reviewed flops are usually rich in driver evidence.

Control books are a **weak, non-random comparison group**, not a matched control.
This limitation must be restated in every report the skill produces.

---

## 5. Record format

One file per bucket: `corpus/bestsellers/<start>-<end>.json` and
`corpus/control/<start>-<end>.json`. Both use the same record shape.

```json
{
  "bucket": "2020-2024",
  "set": "bestsellers",
  "compiled_on": "2026-08-11",
  "books": [
    {
      "id": "slug-of-title",
      "title": "",
      "author": "",
      "year": 2021,
      "market": "US|UK|other",
      "track": "A|B",
      "category": "literary fiction | thriller | romantasy | ...",
      "sales_evidence": [
        {"claim": "", "quote": "", "source": "", "url": "", "date": ""}
      ],
      "non_sale_evidence": [],
      "drivers": [
        {
          "driver": "HOOK_VELOCITY",
          "kind": "intrinsic|extrinsic",
          "confidence": "documented|attributed",
          "quote": "",
          "source": "",
          "url": "",
          "date": ""
        }
      ],
      "unmapped_observations": [],
      "evidence_thin": false
    }
  ]
}
```

---

## 6. Known biases of this evidence base

Observed while compiling 2020–2024. State these when reporting corpus results, and
do not silently correct for them by inventing evidence.

- **Reviews under-report propulsion.** Critics write about voice, theme, character
  and prose; they rarely praise a fast opening or a well-placed chapter break. So
  `HOOK_VELOCITY`, `PROPULSION_MECHANICS`, `PACE_CONSISTENCY` and `ENDING_PAYOFF`
  come out with low weights even though trade wisdom treats them as central. The
  weights measure *what reviewers said*, not *what readers responded to*. Treat a
  low weight on those four as an artefact until a bucket sources them from reader-
  and trade-side evidence rather than criticism.
- **Track B is under-reviewed.** Several of the period's biggest sellers have
  essentially no professional review record. Their driver counts are low because
  the coverage is absent, not because the qualities are.
- **Prizes are weak sales evidence.** A Pulitzer winner in this bucket converted to
  roughly 12,000 copies of demand. Do not let prize status stand in for sales.
- **Backlist re-sellers break the buckets.** Titles published years earlier can
  become a bucket's biggest sellers. Place a book by *when it sold*, and say so in
  the record.

## 7. Working order per bucket

1. Build the candidate list from Tier-1 sources only. Record the sales evidence
   *before* looking at any review — selection must not be driven by narrative.
2. Fix the 15. Note any candidate you dropped and why, in `dropped` at file level.
3. For each book, search reviews and trade analysis; extract driver evidence.
4. Assemble the control set for the same window.
5. Write both JSON files. Validate: `python3 scripts/build_matrix.py --validate`.
6. Report to the user: books covered, drivers evidenced, evidence-thin count, and
   anything you could not source.
