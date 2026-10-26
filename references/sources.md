# Sources

Two parts. **Part 1** is the standing registry — where to look when researching any
bucket, with access notes learned the hard way. **Part 2** is the provenance log for
what has actually been researched so far, so every record in `corpus/` can be traced
back to how it was obtained.

Append to Part 2 at the end of every bucket. A corpus whose provenance isn't written
down can't be audited, and an unauditable corpus is just an opinion with URLs.

---

# Part 1 — Standing source registry

## Selection sources (Tier 1) — "did it sell?"

Use these to build the candidate list, before reading a single review.

| Source | URL | Covers | Notes |
|---|---|---|---|
| NYT Best Sellers archive | `nytimes.com/books/best-sellers/` | US, 1931– | Weekly lists by category. Paywall varies; list pages usually render. |
| The Bookseller — charts | `thebookseller.com/bestsellers` | UK | Nielsen BookScan-derived weekly charts and trade commentary. Partial paywall. |
| Publishers Weekly — bestsellers & annual tallies | `publishersweekly.com` | US | Annual "Facts & Figures" issues give year-end unit sales. Best single source for actual numbers. |
| The Booker Prizes | `thebookerprizes.com` | UK/international | Full longlist/shortlist/winner records with judges' citations. |
| The Pulitzer Prizes | `pulitzer.org/prize-winners-by-category/219` | US fiction | Winners and finalists with citations, 1918–. |
| Women's Prize for Fiction | `womensprize.com` | UK | |
| National Book Awards | `nationalbook.org` | US | |
| Hugo / Nebula / Locus | `thehugoawards.org`, `nebulas.sfwa.org` | SFF | Essential for Track B in every bucket. |
| Edgar Awards | `theedgars.com` | Crime | |
| RITA / Vivian Awards | `rwa.org` | Romance | RITA discontinued 2019, replaced by Vivian — mind the boundary when bucketing. |
| Goodreads Choice Awards | `goodreads.com/choiceawards/best-books-<year>` | Reader-voted, 2009– | The only large reader-voted record; useful where trade coverage is absent. |

## Reception sources (Tier 2) — "why did it sell?"

Where driver evidence comes from.

| Source | URL | Why it earns a place |
|---|---|---|
| **Lit Hub Book Marks** | `bookmarks.reviews/reviews/all/<slug>/` | **The highest-yield source in this whole registry.** Aggregates attributed verbatim excerpts from 10–25 named outlets per book on one page. One fetch replaces a dozen. Start every Track A book here. |
| The Guardian / Observer books | `theguardian.com/books` | Open access, no paywall, strong UK and literary coverage. |
| NPR Books | `npr.org/sections/books` | Open access, US. |
| Kirkus Reviews | `kirkusreviews.com` | Pre-publication trade review; starred reviews matter for the control set. |
| Publishers Weekly reviews | `publishersweekly.com` | As above, plus trade analysis of *why* a title is being pushed. |
| Booklist | `booklistonline.com` | Library-market trade review. |
| NYT / WaPo / WSJ / LA Times | — | Paywalled; usually reachable via Book Marks excerpts instead. |
| The Bookseller — features | `thebookseller.com` | Best source for UK acquisition, advance and marketing-spend reporting. |
| TLS, LRB, New Yorker | — | Long-form; good on literary drivers, thin on commercial ones. |

## Supporting sources (Tier 3)

Goodreads / StoryGraph aggregate rating counts · author interviews in identifiable
outlets · documented BookTok view counts · book-club selection announcements ·
publisher press releases (sales figures only — never their descriptive copy).

## Not acceptable as evidence

Personal blogs and Substacks without an identifiable outlet · retailer and publisher
marketing copy · AI-generated summaries and "book analysis" content farms ·
Wikipedia plot summaries · your own reading of the book · unattributed
"it is well known that…".

Wikipedia is admissible for **one narrow purpose**: as a secondary aggregation of
sourced facts — list placements, prize records, sales figures. Cite it as
"Wikipedia (secondary aggregation)" so the record shows it was not a primary check,
and upgrade to the primary archive when there is time.

## Access notes

- **Goodreads blocks WebFetch**, and a guessed `/book/show/<id>` returns a different
  book entirely. Use the browser tool on the **search listing** —
  `goodreads.com/search?q=<title>+<author>` — which prints `avg rating — N ratings`
  directly in the results. Always record the number and the check date.
- **Book Marks slugs are not guessable.** A wrong slug silently returns the site
  homepage, and the fetch summariser will tell you the book "isn't there" rather
  than erroring. Worse, a colliding slug returns a *different book of the same
  title* — `/trust/` returns Domenico Starnone, not Hernan Diaz. Always confirm the
  author name appears in the fetched content before recording anything from it.
- **School Library Journal returns 403**, **Inlander returns 429** to WebFetch.
  Their content may still be reachable through the search index; if you quote from
  a search snippet rather than a direct fetch, mark it so in the record.

---

# Part 2 — Provenance log

## Bucket 2020–2024 · compiled 2026-08-11

### Fetched directly and successfully

**Lit Hub Book Marks** — attributed review excerpts, the source of most intrinsic
driver evidence in this bucket:

- `bookmarks.reviews/reviews/all/the-vanishing-half/`
- `bookmarks.reviews/reviews/all/shuggie-bain/`
- `bookmarks.reviews/reviews/all/klara-and-the-sun/`
- `bookmarks.reviews/reviews/all/lessons-in-chemistry/`
- `bookmarks.reviews/reviews/all/tomorrow-and-tomorrow-and-tomorrow/`
- `bookmarks.reviews/reviews/all/demon-copperhead/`
- `bookmarks.reviews/reviews/all/the-midnight-library/`
- `bookmarks.reviews/reviews/all/the-thursday-murder-club/`
- `bookmarks.reviews/reviews/all/yellowface/`
- `bookmarks.reviews/reviews/all/the-new-wilderness/` *(control)*
- `bookmarks.reviews/reviews/all/checkout-19/` *(control)*
- `bookmarks.reviews/reviews/all/assembly/` *(control)*

Outlets reached through those pages, each named in the `source` field of the record
that quotes it: Washington Post · New York Times / NYT Book Review · Wall Street
Journal · The Guardian · The Observer · NPR · Los Angeles Times · The New Yorker ·
London Review of Books · Times Literary Supplement · The Times · The Sunday Times ·
The Telegraph · The Scotsman · Irish Times · Irish Independent · Boston Globe ·
Chicago Review · USA Today · Entertainment Weekly · Vox · The A.V. Club · Paste ·
Bookforum · Harper's · The Nation · Jacobin · New Republic · Christian Science
Monitor · Star Tribune · Newsday · Pittsburgh Post-Gazette · Tampa Bay Times ·
Sydney Morning Herald · Harvard Crimson · Columbia Journal · Lambda Literary ·
Vulture · BookPage · Bookreporter · Booklist · Kirkus · Publishers Weekly ·
Library Journal · Shelf Awareness · The Arts Desk · ZYZZYVA · iNews · Jewish Book
Council · New York Journal of Books · Historical Novel Society.

**Publishers Weekly** — `publishersweekly.com/.../89252-the-netanyahus-frank-sonnets-among-2022-pulitzer-prize-winners.html`
Print-run and post-Pulitzer order figures for *The Netanyahus*; the strongest
non-sale evidence in the control set.

**University of Colorado Boulder, Arts & Sciences Magazine** —
`colorado.edu/asmagazine/2024/11/20/readers-are-taking-trash`
Academic commentary (Katie Little) on why BookTok romance sells; source of the
`PROSE_ACCESSIBILITY` evidence for *It Ends with Us*.

**Wikipedia** — used only as secondary aggregation of list placements, prize records
and sales figures, and labelled as such in every record:
`Fourth_Wing` · `Shuggie_Bain` · `Demon_Copperhead` · `The_Midnight_Library` ·
`The_Thursday_Murder_Club` · `The_Vanishing_Half` · `Yellowface_(novel)` ·
`Klara_and_the_Sun` · `Lessons_in_Chemistry_(novel)`

**Goodreads search listings, via browser tool, all checked 2026-08-11** — readership-
scale proxy for the control set:

| Book | Ratings | Query URL |
|---|---:|---|
| Fourth Wing *(bestseller benchmark)* | 3,900,856 | `goodreads.com/search?q=Fourth+Wing+Rebecca+Yarros` |
| Assembly *(control)* | 37,060 | `goodreads.com/search?q=Assembly+Natasha+Brown` |
| The Netanyahus *(control)* | 19,963 | `goodreads.com/search?q=The+Netanyahus+Joshua+Cohen` |
| The New Wilderness *(control)* | 16,993 | `goodreads.com/search?q=The+New+Wilderness+Diane+Cook` |
| Checkout 19 *(control)* | 9,690 | `goodreads.com/search?q=Checkout+19+Claire-Louise+Bennett` |

### Cited from the search index, not fetched directly

These URLs appear in `corpus/bestsellers/2020-2024.json` with quotes obtained through
the search tool rather than a direct page fetch — the page either blocked the fetch
or was not retrieved. Lower-confidence provenance; verify on a later pass.

- `slj.com/story/as-seen-on-booktok-...` — School Library Journal (403 on fetch);
  *Seven Husbands of Evelyn Hugo* list placement and BookTok status.
- `inlander.com/archive/how-spokane-based-audiobook-narrator-...` — Inlander (429 on
  fetch); all *Legends & Lattes* evidence.
- `bookouture.com/bookouture-sign-third-book-in-freida-mcfaddens-...` — publisher
  announcement; *The Housemaid* series sales.
- `thebookseller.com/bestsellers/freidas-carload-mcfadden-dominates-charts-...` —
  UK chart placement for *The Housemaid*.
- `penguinrandomhouse.com/books/690750/...` — publisher page; NYT list duration for
  *Tomorrow, and Tomorrow, and Tomorrow*.
- `thetempest.co/2021/12/28/books/ali-hazelwood-the-love-hypothesis-interview/` —
  author interview; *The Love Hypothesis* setting evidence.
- `en.wikipedia.org/wiki/It_Ends_with_Us`, `.../The_Housemaid_(novel)`,
  `.../The_Love_Hypothesis` — secondary aggregation.

### Search queries run

`"Fourth Wing" Rebecca Yarros sales figures bestseller BookTok Publishers Weekly 2023` ·
`Guardian review "The Vanishing Half" Brit Bennett` ·
`Guardian review "Shuggie Bain" Douglas Stuart Booker Prize 2020 citation` ·
`Guardian review "Lessons in Chemistry" Bonnie Garmus bestseller success why` ·
`"Tomorrow, and Tomorrow, and Tomorrow" Zevin review Guardian NPR bestseller` ·
`Colleen Hoover "It Ends With Us" BookTok why readers sold millions Publishers Weekly analysis` ·
`"Seven Husbands of Evelyn Hugo" Taylor Jenkins Reid BookTok backlist sales why popular analysis` ·
`Freida McFadden "The Housemaid" self-published bestseller sales figures Bookseller 2023` ·
`Travis Baldree "Legends and Lattes" self-published cozy fantasy Hugo nominee success` ·
`"The Netanyahus" Joshua Cohen Pulitzer surprise modest sales copies sold before prize` ·
`"The Love Hypothesis" Ali Hazelwood review fanfiction origin STEM romance bestseller appeal` ·
`"Evelyn Hugo" why readers love it queer bisexual representation emotional twist review analysis`

### Sources rejected during this bucket

Searching *Seven Husbands of Evelyn Hugo* returned mostly personal blogs and Medium
posts on its bisexual representation and late twist. All were rejected under Part 1's
exclusion rule, which is why that record carries a single driver and
`evidence_thin: true` rather than a full profile. The claim may well be true; it is
not yet evidenced to this corpus's standard.

`bookmarks.reviews/reviews/all/the-netanyahus/` and two slug variants for Hernan
Diaz's *Trust* did not resolve — one silently returned the homepage, one returned
Domenico Starnone's unrelated novel of the same title. Nothing was recorded from
either. *Trust* was dropped from the bucket and logged in `dropped`.
