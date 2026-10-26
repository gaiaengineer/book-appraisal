---
name: book-appraisal
description: Appraise a book manuscript for commercial potential against an evidence-based bestseller corpus, or build/extend that corpus by researching what made past bestsellers sell. Use when the user hands over a manuscript (epub, pdf, docx, txt) and asks whether it could sell, for an acquisition or slush-pile read, a bestseller-potential score, a driver/comp profile, or an editorial read on commercial strengths and gaps. Also use when asked to research bestsellers of a period, extend the corpus, add a five-year bucket, or rebuild the scoring matrix. Keywords - manuscript appraisal, bestseller potential, acquisition triage, slush pile, submission read, commercial viability, comp titles, book scoring.
---

# Book appraisal

Two modes. Pick by what the user gave you.

| They gave you | Mode | Read |
|---|---|---|
| A manuscript file | **Appraise** | `references/appraisal-protocol.md` |
| A period, a bucket, or "extend the corpus" | **Research** | `references/research-protocol.md` + `references/sources.md` |
| Neither, just a question about the method | `references/methodology.md` |

Read `references/driver-taxonomy.md` in **both** modes, always. It is the closed
vocabulary of success drivers and the source of truth for what may be scored.

---

## The one rule everything else serves

**No claim without a quote.** In research, a driver is only attributed to a book if
a citable source says so in its own words. In appraisal, a driver only scores above
zero if you can quote the manuscript. Plausibility, genre convention, memory of the
book, and your own taste are all inadmissible.

`scripts/build_matrix.py` and `scripts/score_book.py` enforce this mechanically and
will refuse to produce output from unevidenced input. Fix the input; never work
around the check.

## The observability split

Drivers are either **intrinsic** (visible in the text) or **extrinsic** (author
platform, publisher spend, book-club picks, adaptations, virality, timing).

The corpus records both, because extrinsic factors demonstrably drove many
bestsellers. **Only intrinsic drivers are ever scored** — nothing in a manuscript
file can evidence an author's platform or a marketing budget. Extrinsic factors
appear in every report as an explicit "unknowable from the manuscript" checklist
for the human. Reports that quietly drop them overstate what the score knows.

The skill does not score, rank, or advise on an author's identity or background.
See the note on `AUTHOR_BIOGRAPHY_POSITIONING` in the taxonomy.

---

## Appraise (the common case)

```bash
python3 scripts/extract_book.py "<manuscript>"        # → .appraisal_work/<stem>/
python3 scripts/sample_book.py .appraisal_work/<stem> # → 10% open / 10% mid / 10% end
```

Read the three sample files, declare the track, score every intrinsic driver with
manuscript quotes into `ratings.json`, then:

```bash
python3 scripts/score_book.py .appraisal_work/<stem>/ratings.json --md report.md
```

Full procedure, the ratings file format, and the required honesty statements are in
`references/appraisal-protocol.md`. Follow it step by step.

**Do not search the web during appraisal.** An unpublished manuscript has no web
footprint; whatever you find will be a different book.

## Research (corpus build)

Six five-year buckets, 1995–2024. Per bucket: 15 bestsellers and 4 well-reviewed
books that did *not* sell. Selection comes from sales and prize records; driver
evidence comes from reviews and trade press. One bucket at a time, writing the JSON
before starting the next.

```bash
python3 scripts/build_matrix.py --validate   # check the corpus
python3 scripts/build_matrix.py              # → corpus/matrix.json
```

Full procedure, control-set criteria and record format are in
`references/research-protocol.md`. Every source to search, with access quirks and
what is inadmissible, is in `references/sources.md` — read it before searching, and
append that bucket's provenance to its Part 2 when you finish.

## Corpus state

`corpus/bestsellers/` and `corpus/control/` hold one JSON file per completed bucket;
`corpus/matrix.json` is generated. Check what exists before either mode — if a
bucket is missing, say so rather than scoring against a partial corpus silently.
The matrix carries its own limitations list, and `score_book.py` prints it into
every report. Do not delete it from a report.

## Defending the number

`references/methodology.md` sets out where the 18 criteria came from, which stages of
the score are arithmetic and which are judgement, and what the current weights can
and cannot support. Read it before presenting a score to anyone who will act on it,
and whenever the user asks how the scoring works or why a driver is weighted as it
is. Short version: the resolution is about ±3 points, nine of eighteen drivers
currently have zero discriminating power, and the method has never been validated
against an unseen book.

## What this tool cannot do

It measures similarity to books that already succeeded. It cannot see novelty, and
the corpus by construction cannot contain the next new thing — the books that
created categories would have scored badly against the corpus that preceded them.
The control set is small and non-random. Say this plainly when the user asks the
score to mean more than it does.
