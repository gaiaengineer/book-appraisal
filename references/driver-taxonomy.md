# Driver taxonomy (closed vocabulary)

This is the **only** list of success drivers this skill recognises. Do not invent
drivers, rename them, or add ad-hoc ones during research or appraisal. If a source
describes something genuinely outside this list, record it in the corpus under
`unmapped_observations` with its citation — do not silently create a new driver.
New drivers get added here only by a deliberate edit, with the evidence that
justified them.

The taxonomy is split by **observability**, and that split is the backbone of the
whole skill.

---

## Part 1 — Intrinsic drivers (text-observable)

These can be evidenced from a manuscript excerpt. **These are the only drivers
that get scored during appraisal.**

| ID | Name | What counts as evidence in a manuscript |
|----|------|------------------------------------------|
| `HOOK_VELOCITY` | Speed to first disruption | A concrete change, threat, question or violation of the ordinary within the opening sample — not atmosphere or backstory |
| `HIGH_CONCEPT` | Self-selling premise | The situation contains an inherent "what if" a reader could repeat to a friend |
| `PREMISE_LEGIBILITY` | Clarity of what the book is | By the end of the opening sample, the book's central question is statable in one sentence using the text's own terms |
| `VOICE_DISTINCTIVENESS` | Non-interchangeable prose signature | Syntax, diction, humour or address that could not be swapped with a generic narrator |
| `PROSE_ACCESSIBILITY` | Friction level | Sentence and paragraph load appropriate to the track (see note below — this is *fit*, not *simplicity*) |
| `CHARACTER_INVESTMENT` | Legible, costly want | The protagonist wants something specific, and pursuing it costs them |
| `RELATABILITY_ANCHOR` | Recognisable lived experience | A named human experience (grief, ambition, marriage, illness, money, migration, motherhood…) rendered concretely |
| `EMOTIONAL_AMPLITUDE` | Reach for strong feeling | Scenes constructed to produce a nameable strong emotion, not merely to convey information |
| `TROPE_STACK` | Genre trope architecture | Identifiable, deliberately deployed genre conventions (enemies-to-lovers, locked room, chosen one, unreliable narrator…) |
| `PROPULSION_MECHANICS` | Forward pull at the seams | Chapter/scene endings that open a question rather than close one |
| `STRUCTURAL_DEVICE` | Formal hook | Dual timeline, multi-POV, epistolary, reverse chronology, framing device, mixed media |
| `SETTING_SALIENCE` | World doing work | Place/period/institution that shapes events rather than decorating them |
| `TOPICAL_RESONANCE` | Live public conversation | The text engages a subject under active public discussion |
| `QUOTABILITY` | Excerptable lines | Self-contained lines built to be lifted out and shared |
| `PACE_CONSISTENCY` | No mid-book sag | Middle sample sustains the tension density of the opening |
| `ENDING_PAYOFF` | Delivery on the promise | Closing sample resolves or detonates the question the opening raised |
| `SERIES_POTENTIAL` | Room to continue | World, cast or structure that visibly supports more books |
| `CATEGORY_FIT` | Legible shelf position | The text sits recognisably within a category a buyer could name |

**Note on `PROSE_ACCESSIBILITY`:** this is scored as *fit to declared track*, not as
"simpler is better". Dense prose in the literary track scores high; dense prose in
the commercial track scores low. The track is declared before scoring.

---

## Part 2 — Extrinsic drivers (non-textual)

These demonstrably drive bestsellers, and the corpus records them because leaving
them out would misrepresent why those books sold. **They are never scored during
manuscript appraisal** — nothing in a manuscript file can evidence them. They
appear in the report only as an *unknowable factors* checklist for the human.

| ID | Name |
|----|------|
| `AUTHOR_PLATFORM` | Pre-existing audience (following, podcast, column, prior fame) |
| `PRIOR_SALES_TRACK` | Author's previous titles sold |
| `CELEBRITY_BOOKCLUB` | Reese's / Oprah's / Jenna / Richard & Judy and equivalents |
| `PRIZE_RECOGNITION` | Longlist, shortlist or win |
| `PUBLISHER_INVESTMENT` | Reported advance size, print run, marketing spend, lead-title status |
| `SOCIAL_VIRALITY` | BookTok / Bookstagram / Booktube amplification |
| `SCREEN_ADAPTATION` | Film/TV deal or release, before or after publication |
| `RETAIL_PLACEMENT` | Supermarket, airport, table-front, Amazon merchandising, KU algorithm |
| `NEWS_CYCLE_TIMING` | Publication coincided with a related public event |
| `AUTHOR_BIOGRAPHY_POSITIONING` | The author's own identity or life story used as a positioning angle in marketing and reception |
| `IMPORT_MOMENTUM` | Success in another market preceding this one |

### Handling of `AUTHOR_BIOGRAPHY_POSITIONING`

This driver exists because sources document it — publishers position books on
author biography, and reviewers write about it. The corpus records it **only where
a citable source explicitly does so**, as a description of how a book was marketed
and received.

It is never scored, never inferred, and never a recommendation input. This skill
does not rate manuscripts on who wrote them, and must not produce output that
scores, ranks or advises on an author's identity. If a user asks the skill to weigh
a hypothetical author's background, decline that specific part and continue with
the text-based appraisal.

---

## Rating scale (appraisal only, intrinsic drivers only)

| Score | Meaning | Requirement |
|-------|---------|-------------|
| 0 | Not evidenced in the sampled text | State "no evidence in sample" |
| 1 | Present but weak or inconsistent | One verbatim quote + location |
| 2 | Present and strong | Two verbatim quotes + locations |

**A score above 0 without a verbatim quote from the manuscript is invalid.** If you
cannot quote it, it is 0. This rule is what keeps the appraisal from drifting into
invented qualities, and it applies with no exceptions.

Some drivers are only assessable from particular windows:
`ENDING_PAYOFF` → ending sample only. `PACE_CONSISTENCY` → middle vs opening.
`HOOK_VELOCITY`, `PREMISE_LEGIBILITY` → opening sample only. Scoring these from the
wrong window is an error; mark `not_assessable` if the needed window is missing.
