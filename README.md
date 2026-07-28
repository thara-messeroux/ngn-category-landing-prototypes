# Category landing page prototypes (PROTOTYPE ONLY)

## Live previews (public, no login)

Open in any browser, no account needed.

| Phase | Public link |
| --- | --- |
| Phase 1: First concepts | https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-1-concepts/ |
| Phase 2: Live data | https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-2-live-data/ |
| Phase 3: Combined design (presented) | https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-3-synthesis/ |
| Phase 4: Mobile refinement (presented July 27) | https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-4-mobile-refinement/ |
| Phase 5: Stakeholder refinement (current) | https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-5-stakeholder-refinement/ |

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
| `phase-4-mobile-refinement/` | Phase 4, July 23 to 24 | Active | Continues from Phase 3 for the Monday, July 27, 2026 presentation. The July 24 build adds Zach's sticky header, the merged Daily newsletter (Monday to Saturday), the Most Read redesign, and a full mobile pass at phone width. |
| `shared/` | | | Prototype masthead (minimal app bar and section nav) and footer with the real NGN logo SVGs. |

Live previews (open in a browser): [Phase 1](https://claude.ai/code/artifact/2e2b272c-e653-4137-b25e-842fc698241f), [Phase 2](https://claude.ai/code/artifact/8c115f85-1cd6-4748-89f2-5bac57e920c1), [Phase 3](https://claude.ai/code/artifact/2f32b15a-ee01-4a2f-86a6-addb44696513), [Phase 4](https://claude.ai/code/artifact/9a299877-4ab2-4ee0-bf5e-91a4da8f654b). These are Thara's hosted previews; ask Thara if a link needs sharing access.

How to view: serve this folder (`python3 -m http.server`) or open any phase's `index.html` directly. Fonts are embedded, so no network is needed. Phase 1 needs the folder structure kept intact for `shared/ngn-shell.js`.

### Notable pattern (for the record)

In the July 23, 2026 review, the team liked a header pattern that Zach built on his own: one sticky bar with the page title on the left and the topics on the right (`.cat-bar`, see [`10-composite-v5.html`](10-composite-v5.html)). It is kept here as is, untouched, as the record of the version that earned that feedback. The team decided to adopt this header in [`phase-4-mobile-refinement/`](phase-4-mobile-refinement/).
