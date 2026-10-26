# Criteria and quantification

What the 18 appraisal criteria are, where they came from, which parts of the score
are arithmetic and which are judgement, and how much the number can actually bear.

Read this before defending a score to anyone.

---

## Part 1 — Where the criteria came from

### The honest provenance

The taxonomy was **authored before the corpus was compiled**, not derived from it.
That ordering matters and is easy to misrepresent, so it is stated first:

- **Membership** — which qualities are on the list — is a **judgement**, made from
  trade practice and constrained by the sampling method. It is not data-derived.
- **Weights** — how much each one counts — are **arithmetic**, computed from the
  corpus evidence.

So the corpus can tell you that `EMOTIONAL_AMPLITUDE` outranks `SERIES_POTENTIAL`.
It cannot tell you that both belong on the list, or that nothing is missing. A
quality no one thought to name is not discovered by this method; it is invisible to
it. The `unmapped_observations` field in every corpus record exists to catch those,
and it has already caught two candidates (unlikeable-narrator appeal; pre-existing
fanfiction readership).

### The membership test

A quality earns a place only if it passes all four:

1. **Text-observable in a 30% sample.** Not "the plot resolves satisfyingly" —
   you're not reading the whole plot. `ENDING_PAYOFF` survives only because the
   sampler always reads the last 10%.
2. **Nameable by a reviewer or a trade reader.** If no source would ever write a
   sentence evidencing it, it can never be scored above 0, and a criterion that can
   only score 0 is decoration.
3. **Non-redundant.** Distinguishable from every other driver by the evidence that
   would support it, not just by its name.
4. **Not an identity or biography attribute.** Text only. See below.

### What was deliberately excluded

- **"Originality", "literary merit", "marketability", "voice quality".** All fail
  test 2 — they cannot be evidenced by quotation, only asserted. They are exactly
  the invented-quality failure mode this skill was built to prevent.
- **The 11 extrinsic drivers** — platform, publisher spend, BookTok, book-club
  picks, adaptations, prizes, timing. They fail test 1. They demonstrably drove the
  corpus, so they are recorded and reported, but they cannot be scored from a file
  and are excluded from the arithmetic entirely.
- **Author identity or background.** Fails test 4 on principle, not on
  observability. The corpus records `AUTHOR_BIOGRAPHY_POSITIONING` where a source
  documents how a book was *marketed*; the appraisal never scores it, and the skill
  produces no output rating an author.

### Where the split falls

18 intrinsic (scored) · 11 extrinsic (recorded, reported, never scored).

In the 2020–2024 bucket the extrinsic factors were not marginal: `PRIZE_RECOGNITION`
appears in 5 of 15 bestsellers, `SOCIAL_VIRALITY` in 4.5, `AUTHOR_PLATFORM` in 2.5.
The score cannot see any of it. That is why the report carries an unknowable-factors
checklist rather than a bare number.

---

## Part 2 — How quantified is it, really

### The chain, stage by stage

| # | Stage | Kind | Constrained by |
|---|-------|------|----------------|
| 1 | Which qualities are criteria | **Judgement** | Fixed in advance; changing it requires editing the taxonomy |
| 2 | Which quotes evidence which driver, per corpus book | **Judgement** | Verbatim quote + URL + confidence tier required; validator rejects otherwise |
| 3 | Driver weights | **Arithmetic** | Deterministic function of stage 2 |
| 4 | Scoring the manuscript 0/1/2 | **Judgement** | Quote count must match score; scorer rejects otherwise |
| 5 | Weighted score and band | **Arithmetic** | Deterministic function of stages 3 and 4 |

**Two of five stages are arithmetic, and they are not the two that decide the
answer.** Stages 2 and 4 — both judgement — determine almost everything. What the
math buys is not objectivity; it is *reproducibility and auditability*. Every number
traces to a quote, and the same quotes always produce the same score.

The quote requirement is the actual quantification. It converts "this feels
propulsive" into "these two sentences, at these locations, or it scores zero."

### The weight formula

```
p_best = (k_best + 1) / (n_best + 2)          Laplace-smoothed prevalence
p_ctrl = (k_ctrl + 1) / (n_ctrl + 2)
disc   = clamp(p_best − p_ctrl, 0, 1)         discriminating power
weight = p_best × (0.25 + 0.75 × disc)        normalised so Σ weights = 1
```

`k` is confidence-weighted, not a raw count: `documented` = 1.0, `attributed` = 0.5.
Hence the half-values in the table below.

The `0.25` floor is a judgement call: a driver present in most bestsellers *and*
most control books still counts for something, on the reasoning that it may be table
stakes rather than noise. Set it to 0 and undiscriminating drivers vanish entirely.
That is a defensible alternative and it is one line in `build_matrix.py`.

Final score: `Σ(weight × rating/2) ÷ Σ(weight of assessed drivers) × 100`, so
`not_assessable` drivers are excluded rather than counted as failures.

### What the current numbers actually look like

From `corpus/matrix.json`, one bucket, 15 bestsellers vs 4 control:

| Driver | weight | n_best | n_ctrl | discrimination |
|---|---:|---:|---:|---:|
| TOPICAL_RESONANCE | 0.111 | 7.0 | 2.0 | **0.000** |
| EMOTIONAL_AMPLITUDE | 0.109 | 5.0 | 0.5 | 0.103 |
| CHARACTER_INVESTMENT | 0.093 | 4.5 | 0.5 | 0.074 |
| VOICE_DISTINCTIVENESS | 0.083 | 5.0 | 2.0 | **0.000** |
| PROSE_ACCESSIBILITY | 0.081 | 3.5 | 0.0 | 0.098 |
| SETTING_SALIENCE | 0.079 | 4.0 | 0.5 | 0.044 |
| CATEGORY_FIT | 0.067 | 3.0 | 0.0 | 0.069 |
| HIGH_CONCEPT | 0.065 | 3.5 | 0.5 | 0.015 |
| TROPE_STACK | 0.054 | 2.5 | 0.0 | 0.039 |
| PROPULSION_MECHANICS | 0.049 | 2.5 | 1.0 | **0.000** |
| SERIES_POTENTIAL | 0.043 | 2.0 | 0.0 | 0.010 |
| STRUCTURAL_DEVICE | 0.042 | 2.0 | 1.0 | **0.000** |
| RELATABILITY_ANCHOR | 0.035 | 1.5 | 0.0 | **0.000** |
| PACE_CONSISTENCY | 0.028 | 1.0 | 0.0 | **0.000** |
| ENDING_PAYOFF | 0.021 | 0.5 | 0.0 | **0.000** |
| HOOK_VELOCITY | 0.014 | **0.0** | 0.0 | **0.000** |
| PREMISE_LEGIBILITY | 0.014 | **0.0** | 0.0 | **0.000** |
| QUOTABILITY | 0.014 | **0.0** | 0.5 | **0.000** |

Four things in that table need saying out loud.

**1. Nine of eighteen drivers have zero discriminating power — including the
top-weighted one.** `TOPICAL_RESONANCE` scores highest not because it separates
bestsellers from non-sellers but because it is common: the control books are
*slightly more* topical (0.500) than the bestsellers (0.471). Its rank comes
entirely from prevalence and the 0.25 floor. Right now the control set is barely
functioning as a control — with only 4 books it mostly cannot resolve anything.

**2. Three drivers have literally no corpus evidence.** `HOOK_VELOCITY`,
`PREMISE_LEGIBILITY` and `QUOTABILITY` were evidenced zero times in 15 bestsellers.
Their 0.014 weight is pure Laplace smoothing — a placeholder, not a measurement.
This is the review-bias problem from the research protocol: critics do not write
about fast openings. Do not read their low rank as "openings don't matter."

**3. The whole spread is 8:1, and the bottom of it is an artifact.** Among drivers
that were actually evidenced the real spread is roughly 5:1. The matrix is closer to
"mildly weighted" than "sharply weighted."

**4. All 18 are flagged `low_confidence`,** and correctly so — the flag trips below
5 supporting books or fewer than 10 control books, and both conditions hold.

### Resolution — how many digits the score can carry

One driver moving a single point (0→1 or 1→2) changes the final score by:

| | points |
|---|---:|
| Highest-weight driver | 5.5 |
| Median-weight driver | 2.7 |
| Lowest-weight driver | 0.7 |

So the practical resolution is roughly **±3 points**. `score_book.py` therefore
reports a whole number. Two manuscripts at 58 and 61 are not distinguishable, and
neither are 49 and 52 — even though the second pair straddles a band boundary. The
bands (35 / 50 / 65 / 80) are convenience labels for a continuum, not thresholds
with evidence behind them. A book near a boundary should be described as near a
boundary, never rounded into a verdict.

### What is not quantified at all

Deliberately: the track declaration, the comparable titles, the verdict paragraph,
the "what would move the score" notes, and the extrinsic checklist. These are the
parts an acquiring editor will actually act on, and they are prose because the
evidence for them is prose.

---

## Part 3 — What it would take to trust this more

In rough order of value per unit of work:

1. **More control books.** The single biggest weakness. At 4 books the control
   cannot discriminate; the protocol's 24 across six buckets would let
   `discrimination` do real work instead of collapsing to zero.
2. **The remaining five buckets.** Weights computed from 15 books are unstable;
   90 would let you see which drivers hold across eras and which are 2020s-specific.
3. **Non-review evidence for the pacing drivers.** Until `HOOK_VELOCITY` and
   `PROPULSION_MECHANICS` are sourced from trade and reader-side material, their
   weights are measuring critics' interests rather than readers'.
4. **A held-out validation run.** Score a set of manuscripts *before* their outcomes
   are known, then check correlation.

### The status of the thing, stated plainly

**No validation has been performed.** The matrix is a *description* of what
distinguished 15 bestsellers from 4 well-reviewed non-sellers in the review record
of one five-year period. It has never been tested against an unseen book with a
known outcome, so there is no evidence about its predictive power in either
direction.

Two facts from the corpus itself set the ceiling on what any such score could claim.
*Shuggie Bain* was rejected by at least 30 publishers and went on to win the Booker
and sell 1.5 million copies. *It Ends with Us* sold about 21,000 copies in its first
month, then 4.1 million — with an unchanged text. What changed was distribution, and
distribution is exactly what a manuscript file cannot show you.

Use the score to rank a slush pile and to make the read reproducible across people.
Do not use it to decide anything on its own.
