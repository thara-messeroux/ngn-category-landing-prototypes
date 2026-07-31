# Category landing page prototypes (PROTOTYPE ONLY)

Six static HTML explorations of a redesigned category landing page
(`/category/university-news/` as the example), built strictly from
design-system-v2 tokens and existing component vocabulary. Nothing here
ships; nothing is wired into WordPress.

| File | Concept | Reference feel |
| --- | --- | --- |
| `01-broadsheet.html` | Three-column news package: latest rail, lead story, most-read + photos rail | WSJ / Business Insider |
| `02-section-front.html` | Oversized section header, hero, single-column river with dividers | NYT section fronts |
| `03-mosaic.html` | Red identity band, overlay-card mosaic hero, dark spotlight band, scroll strips | Time |
| `04-index.html` | Sticky identity/topic rail beside a day-grouped chronological river | Washington Post |
| `05-athletic.html` | Pinned topic pill bar, card grids, app-like sections | NYT Athletic |
| `06-composite.html` | WaPo header + Time featured trio + NYT river with sticky interest-capture newsletter + per-tag story groups. Sticky appbar with scroll-condensing wordmark→NGN logo animation, sticky topic subnav, Google News-style relative dates, no bylines. | Composite (the working direction) |
| `07-composite-v2.html` | Same shell as 06, but the featured section is a Business Insider-style package: dominant lead with an overlapping white headline box + right rail of top story and thumbnail rows. | Composite, alternate featured package |
| `08-composite-v3.html` | Like 07, but the lead headline sits below the image instead of overlapping it. | Composite, alternate featured package |
| `09-composite-v4.html` | Combined-header exploration + bottom archive + H1 font switcher | Composite, header iteration |
| `10-composite-v5.html` | Refined combined header: one sticky bar, title on the left and topics on the right (`.cat-bar`), plus bottom archive and H1 font switcher. **The team liked this nav pattern in the July 23, 2026 review. See the note below.** | Composite, header iteration |

Common to all: no border-radius on images, and the ngn-app
**Logo_And_Date App Bar** (compact nav;
lettermark below 600px, wordmark above), the production **site footer**
(markup lifted verbatim from the live site), a curated **tag-based topic
nav** (categories are flat — tags are the topic layer), and a designed
**"Seen around campus" photo module** for the daily photo features.

## Viewing

```
python3 -m http.server 8127 --directory private/prototypes/category-landing
# → http://localhost:8127/01-broadsheet.html … 05-athletic.html
```

(Or open the files directly — they hot-link production images and the
live Typekit kit, so a network connection is required either way.)

## Rebuilding

- `fetch-content.py` — pulls real headlines/deks/bylines/images from the
  production REST API into `content.json` (photo features filtered into
  their own pool).
- `build.py` — regenerates the five pages from `content.json` +
  `shared.css` + `footer-partial.html`.

`screenshots/` holds full-page desktop (1400px) and mobile (375px)
captures of each concept.


---

# Thara's prototypes: phased review sets

Interactive pages that let you switch between options with a pill at the bottom. Built from the digital team's 27 Pastel comments and hand sketches. Organized by phase so the progression is easy to follow for future presentations.

| Folder | Phase | Status | What's inside |
| --- | --- | --- | --- |
| `phase-1-concepts/` | Phase 1, July 14 | Frozen | Three layout directions (The Lead, Magazine Grid, Reading List) with placeholder images. Loads `shared/ngn-shell.js` for the masthead and footer. |
| `phase-2-live-data/` | Phase 2, July 21 to 22 | Frozen | Four directions (Section front, Briefing, Reader, Magazine) with live stories and photos, working section switching across 4 categories, clickable topic pages, and a paginated archive. Fonts are embedded, so it works offline. |
| `phase-3-synthesis/` | Phase 3, July 23 | Frozen. Presented to stakeholders. | Zach's composite base (`08-composite-v3.html`) combined with Thara's Option 2 and 3 elements (Most Read rail, all-newsletters chooser), the NGN section bar system, and clickable subtopic pages with an archive grid. |
| `phase-4-mobile-refinement/` | Phase 4, July 23 to 24 | Frozen. Presented July 27. | Zach's sticky header, the merged Daily newsletter (Monday to Saturday), the Most Read redesign, a working site menu and search, and a full mobile pass at phone width. |
| `phase-5-stakeholder-refinement/` | Phase 5, July 28 to 30 | Frozen. Presented July 30. | The July 27 stakeholder decisions: a dedicated featured spot for Seen around campus, a Video section for the videographers, section headers rebuilt on the live design system pattern, subtopic page cleanup, and the Seen around campus carousel rebuilt from the real article component. |
| `phase-6-final-round/` | Phase 6, from July 31 | Active | Continues from Phase 5 with the feedback from the final stakeholder round. Last design round before development. Carries the Phase 5 items that were still open and Zach's remaining Pastel comments. |
| `shared/` | | | Prototype masthead (minimal app bar and section nav) and footer with the real NGN logo SVGs. |

Live previews (public, open in any browser, no login needed): [Phase 1](https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-1-concepts/), [Phase 2](https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-2-live-data/), [Phase 3](https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-3-synthesis/), [Phase 4](https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-4-mobile-refinement/), [Phase 5](https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-5-stakeholder-refinement/), [Phase 6](https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-6-final-round/). These are served from a public mirror of this folder so they can be opened in incognito or embedded in Pastel.

Each phase folder keeps its own `README.md` with the decisions made in that phase and the reasoning behind them. The active phase's README is the working checklist; frozen phases are records. [`HANDOFF.md`](HANDOFF.md) is the one-page summary of where the work stands, written to be handed to a new session or a new person.

How to view: serve this folder (`python3 -m http.server`) or open any phase's `index.html` directly. Fonts are embedded, so no network is needed. Phase 1 needs the folder structure kept intact for `shared/ngn-shell.js`.

### Notable pattern (for the record)

In the July 23, 2026 review, the team liked a header pattern that Zach built on his own: one sticky bar with the page title on the left and the topics on the right (`.cat-bar`, see [`10-composite-v5.html`](10-composite-v5.html)). It is kept here as is, untouched, as the record of the version that earned that feedback. The team decided to adopt this header in [`phase-4-mobile-refinement/`](phase-4-mobile-refinement/).
