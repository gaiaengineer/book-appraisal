# Book Appraisal

**A Claude skill that compares a manuscript with books that already became bestsellers, and is honest about how little that number can tell you.**

An acquisitions editor reading a slush pile wants to know one thing: *could this sell?* No tool can answer that. Book Appraisal answers a smaller, checkable question instead: *how much of what made recent bestsellers sell can be seen in this text?* Every point of the score is backed by a quote from the manuscript, and every report says what the score cannot see.

## Two modes

| You give Claude | Mode | What happens |
|---|---|---|
| A manuscript (epub, pdf, docx, txt) | **Appraise** | Samples 30% of the book, rates 18 text-level drivers with quotes, produces a weighted score and a report |
| A period, e.g. *"research the 2015–2019 bestsellers"* | **Research** | Builds the evidence corpus: why past bestsellers sold, in the words of reviewers and trade press |

## How a score is made

```
 Research                         Appraise
 bestsellers + control books      manuscript
        │                              │
 reviews, trade press, sales      extract → sample 10% open / 10% middle / 10% end
        │                              │
 driver evidence (quoted)         rate 18 drivers, 0–2, each with manuscript quotes
        │                              │
 build_matrix.py → weights  ───►  score_book.py → score, band, report
```

1. **Research.** For each five-year period: 15 bestsellers, chosen from sales and prize records, plus a control set of well-reviewed books that did *not* sell. A driver (say, `EMOTIONAL_AMPLITUDE`) is recorded for a book only when a reviewer or trade source says so in their own words, with a URL.
2. **Weights.** `build_matrix.py` turns the corpus into a weight per driver: how often it appears among bestsellers, and how much more often than among the control books.
3. **Appraisal.** Claude reads three samples of the manuscript and rates each driver 0, 1 or 2. A 1 needs one verbatim quote, a 2 needs two. `score_book.py` refuses to produce a report if any rating breaks this rule.

## Design principles

- **No claim without a quote.** In research, a driver needs a citable source. In appraisal, a driver scores above zero only with a quote from the manuscript. Memory, genre convention and taste don't count.
- **Score only what the text can show.** The corpus also records outside factors: author platform, publisher spend, book-club picks, adaptations, virality. None of them can be seen in a manuscript, so none of them are scored. Every report lists them as open questions for a human.
- **No web search during appraisal.** An unpublished manuscript has no web footprint; anything found online is a different book.
- **The author's identity is never scored.** The skill does not rate or advise on an author's background.
- **The method documents its own weak spots.** `references/methodology.md` says which steps are arithmetic and which are judgement, how many points of the score are noise (about ±3), and what it would take to trust it more.

## What it cannot do

It measures similarity to books that already succeeded, so it cannot see novelty. The books that created new categories would have scored badly against the corpus that came before them. Treat the score as triage: a reason to read a manuscript sooner, never a verdict on it.

## Corpus status

| Period | Bestsellers | Control | Status |
|---|---:|---:|---|
| 2020–2024 | 15 | 4 | done |
| 1995–2019 | | | not yet researched |

With one period and a small control set, all 18 weights are flagged low-confidence, and nine drivers currently cannot tell bestsellers from control books at all. `score_book.py` prints these limitations into every report. Each new period added with the Research mode makes the weights more meaningful.

The corpus stores short attributed excerpts from reviews and sales coverage (25 words at most) with links to the original sources. It contains no text from the books themselves.

## How it's built

Plain Python, standard library only. No dependencies.

| File | Does |
|---|---|
| `SKILL.md` | Instructions for Claude: which mode, which files to read, the rules |
| `scripts/extract_book.py` | Any format to plain text: docx, epub, pdf, rtf, txt |
| `scripts/sample_book.py` | Takes the opening, middle and closing 10% of the book |
| `scripts/score_book.py` | Checks the evidence, applies the weights, writes the report |
| `scripts/build_matrix.py` | Validates the corpus and computes driver weights |
| `references/driver-taxonomy.md` | The 18 scored drivers and the outside factors: the closed vocabulary |
| `references/appraisal-protocol.md` | Step-by-step appraisal procedure and the ratings file format |
| `references/research-protocol.md` | How to build a period: quotas, control set, evidence bar |
| `references/sources.md` | Where evidence may come from, what's not admissible, and a provenance log |
| `references/methodology.md` | Where the criteria came from and how much the number can bear |
| `corpus/` | One JSON file per period, plus the generated `matrix.json` |

## Install

**Claude desktop or web app:** zip the repository folder and upload it under **Settings → Capabilities → Skills**.

**Claude Code:**
```bash
git clone https://github.com/gaiaengineer/book-appraisal.git ~/.claude/skills/book-appraisal
```

Check the corpus:
```bash
python3 scripts/build_matrix.py --validate
```

Then give Claude a manuscript and ask *"Could this sell?"*, or ask it to research the next period of bestsellers.

## Before you use it on real submissions

Submissions are confidential, unpublished work. Running them through Claude sends them to a third party. That should be a deliberate decision by the publisher, made with authors' expectations in mind, not something that happens by default.

## Author

Built by [Olga Alexeeva](https://olgaalexeeva.com) · [LinkedIn](https://www.linkedin.com/in/gaiaengineer)

Companion skill: [manuscript-triage](https://github.com/gaiaengineer/manuscript-triage) checks whether a manuscript is competently made. Book Appraisal asks whether it resembles what sells.
