# Phase B — manuscript appraisal protocol

Input: one manuscript file (epub, pdf, docx, txt, md). Output: a scored acquisition
report for an agent or editor.

**Do not search the web during appraisal.** An unpublished manuscript has no web
footprint; anything you find will be a different book with a similar title, and
acting on it corrupts the appraisal. The only exception is if the user explicitly
states the book is already published and asks for market context — and then it goes
in a clearly separated section, never into the score.

---

## Step 1 — Extract and sample

```bash
python3 scripts/extract_book.py "<path>"
python3 scripts/sample_book.py .appraisal_work/<stem>
```

Check the extractor output before continuing:

- `total_words` under 2,000 → extraction failed (likely a scanned PDF). Stop and
  tell the user it needs OCR. Do not appraise a broken extraction.
- Under 20,000 words → tell the user this is novella-length or a partial, and that
  the corpus is built from full-length books, before proceeding.
- If `headings_found` is 0 in a novel-length file, the sampler is slicing on word
  count alone; say so in the report's sampling note.

Use `--windows 5` when the book is over 150,000 words or has an unusual structure
(interleaved timelines, story collection, multi-part epic) — three windows can miss
a whole strand. Otherwise keep the default 3.

Read all three sample files in full before scoring anything.

## Step 2 — Declare the track first

Before scoring, state the track and category, based on the sampled text:

- **Track A (trade/mainstream)** — literary and upmarket fiction, book-club fiction.
- **Track B (genre/commercial)** — romance/romantasy, thriller, cosy mystery, SFF,
  and anything trope-forward or series-native.

The track changes what `PROSE_ACCESSIBILITY`, `TROPE_STACK` and `CATEGORY_FIT` mean.
Declaring it after scoring lets the score choose the track — which is backwards.
If the manuscript is genuinely between tracks, say so and score it as Track A.

## Step 3 — Score each intrinsic driver

Work through `driver-taxonomy.md` Part 1 in order. For each driver:

1. Decide the window it must come from (the taxonomy states the constrained ones).
2. Find evidence in the sampled text — or don't.
3. Score 0 / 1 / 2 and attach **verbatim quotes**, with a location.

Rules that are not negotiable:

- **No quote → score 0.** Not "probably present", not "implied", not "the setup
  suggests". `score_book.py` rejects the file if you break this.
- Quote the manuscript exactly, ≤25 words per quote, with a location such as
  `middle sample, para 41`.
- If a driver's required window is missing or unusable, mark `not_assessable`
  rather than guessing; its weight is redistributed, not counted as a failure.
- Judge only the sampled text. You have not read the whole book — never write as if
  you have, and never infer what happens in the unsampled 70%.
- Score against the corpus's drivers, not your taste. "I found it dull" is not a
  driver. If the text does something the taxonomy has no slot for, put it in
  `unmapped_observations` — it may earn a driver later, after evidence.

Write the result to `.appraisal_work/<stem>/ratings.json`:

```json
{
  "title": "", "author": "", "track": "A", "category": "",
  "sampling_summary": "3 windows, 10% each, 28,400 of 94,600 words (30.0%)",
  "ratings": [
    {"driver": "HOOK_VELOCITY", "score": 2, "window": "opening",
     "evidence": [{"quote": "", "location": "opening, para 6"},
                  {"quote": "", "location": "opening, para 22"}],
     "note": ""},
    {"driver": "ENDING_PAYOFF", "not_assessable": true,
     "note": "ending window is an appendix, not narrative"}
  ],
  "comps": [{"title": "", "author": "", "why": "shared driver profile: ..."}],
  "editorial_notes": []
}
```

Every intrinsic driver must appear exactly once, either scored or `not_assessable`.

## Step 4 — Score and report

```bash
python3 scripts/score_book.py .appraisal_work/<stem>/ratings.json --md report.md
```

If it exits with errors, fix the ratings file — do not work around the checks.

Then extend the generated report with the parts only you can write:

- **Verdict paragraph** — the band, in a sentence, with the two drivers that moved
  the score most in each direction.
- **Comparable titles** — drawn from the corpus, chosen by *shared driver profile*,
  each with the shared drivers named. Do not comp to books outside the corpus from
  memory; say "no close comp in corpus" if there isn't one.
- **What would move the score** — concrete, text-level, tied to specific drivers.
- **Unknowable factors** — the extrinsic checklist the script emits, presented as
  questions for the human, not as assumptions.

## Step 5 — What to tell the user honestly

Always state, in the report, in plain language:

- what fraction of the book was read and which parts;
- that the score is a similarity measure against past bestsellers, not a prediction;
- that extrinsic factors — platform, publisher spend, book club picks, timing —
  drove much of the corpus and none of them are in the score;
- how thin the evidence is behind any low-confidence weights used.

Never report a score without these. A number without them will be over-trusted, and
this is a tool for triage, not a verdict on a book.
