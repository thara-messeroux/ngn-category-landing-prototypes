# Handoff: NGN category landing page redesign

Last updated Friday, July 31, 2026. This is the one page to read first. It says where the work stands, where everything lives, and what is left.

## What this is

A redesign of the category landing pages for news.northeastern.edu, using `/category/university-news/` as the worked example. The deliverable so far is a self-contained static HTML prototype that simulates the page, built only from design-system-v2 tokens and the existing component vocabulary. Nothing ships from here and nothing is wired into WordPress. The prototype is a design artefact for stakeholder review and, eventually, a reference for the developer who builds it.

Designer: Thara Messeroux.

## Where everything lives

**Work repo (private).** `https://github.com/News-at-Northeastern/environment`, branch `chore-category-landing-prototypes`, path `private/prototypes/category-landing/`. This is the source of truth.

**Public mirror (for shareable preview links).** `https://github.com/thara-messeroux/ngn-category-landing-prototypes`, branch `main`, served by GitHub Pages. It mirrors the phase folders only. Every change is pushed to both repos so the live link never goes stale.

**Live previews**, public, no login, safe to send to anyone or embed in Pastel:

- Phase 1: https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-1-concepts/
- Phase 2: https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-2-live-data/
- Phase 3: https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-3-synthesis/
- Phase 4: https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-4-mobile-refinement/
- Phase 5: https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-5-stakeholder-refinement/
- Phase 6, current: https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-6-final-round/

**Zach's Pastel review board:** https://usepastel.com/link/4wejp064/

**Reference component** the Seen around campus carousel was rebuilt from: https://news.northeastern.edu/2025/10/22/spongebob-25th-anniversary-tv-culture/

Each phase is one folder holding `index.html` and a `README.md`. The `index.html` is fully self-contained, with images and fonts embedded as base64, so it opens straight from disk with no server and no network. That is also why the files are large, around 5MB.

## Phases

Every phase is a frozen copy of the one before it, so each stakeholder review keeps its own record and nothing is overwritten.

| Phase | Dates | Status |
| --- | --- | --- |
| 1, concepts | July 14 | Frozen |
| 2, live data | July 21 to 22 | Frozen |
| 3, synthesis | July 23 | Frozen, presented |
| 4, mobile refinement | July 23 to 24 | Frozen, presented July 27 |
| 5, stakeholder refinement | July 28 to 30 | Frozen, presented July 30 |
| 6, final round | from July 31 | **Active** |

Phase 6 is the last design round. When it closes, the work moves to development.

## Done in Phase 5

Full detail with the reasoning for each is in `phase-5-stakeholder-refinement/README.md`. In short:

- **Seen around campus** kept and given its own full width band on a tinted surface, after Stephanie Sim asked for it against Zach's note suggesting removal. The photographers recently lost one of their main display placements.
- **A Video section** added, giving the videographers the same standing the photographers have. Full width, three columns, six real videos with real links and running times, ordered by recency. No bylines, because a video is usually a team and one name would misattribute it.
- **Section headers** rebuilt on the live site's real pattern: hairline rule, bold uppercase Lato title, black pill button. Verified against the live markup rather than eyeballed. Every button names its own destination instead of repeating "See All", which matters for screen reader users.
- **Subtopic pages** cleaned up. "University News" appeared four times on one page and now appears once. The Latest moved into the same two column shape as the landing page, taking headlines from 131 characters a line to 44, against the 50 to 75 Nielsen Norman recommends. More stories and Load More stay full width.
- **Seen around campus carousel** rebuilt from the real component used on feature articles, with its stylesheet and script read off the live page rather than approximated. Then, over several rounds of feedback: made to run the full width of the section, sized off the photos' real 3:2 ratio so the open photo is never cropped, reduced from six columns to five with the closed photos stepping down in width by a constant ratio, and its top spacing brought in line with the rest of the page.

## Open

The live list is in `phase-6-final-round/README.md`. Summary:

**Feedback from the final round** is not recorded yet. That is the first thing to capture in Phase 6.

**Carried over from Phase 5:** photo forward opening for subtopic pages; highlighted hierarchy for recent images at the top of subtopic pages; search within a topic, raised by Stephanie, currently proposed for the archive page rather than the category page; confirming the photographer names, which were inferred from filename initials and never verified; confirming whether Seen around campus should be newest first or an editor's pick; and Most Read's 40px top gap where every other section is at 24px.

**Zach's Pastel board:** comments 1 and 5 closed, 2 reopened and needing a conversation with him, and 3, 4, 6 to 16 untouched. Items 8 and 12 may already be answered by the two column shape built in Phase 5 and are worth checking against the current build first.

## For development, do not lose this

- The Seen around campus carousel **is not a shared component**. On the live site its CSS and JS are inline in one article, not in the theme. Building it into the category page means creating the component properly, not reusing an existing one. Verified by searching the repo, which returns no matches.
- The article version of that carousel **carries a real bug**. It builds its transform by joining a minus sign to the offset, so a negative offset produces a `translateX` with two minus signs, which browsers reject and silently drop. It never surfaces on the article page because the offset there is always positive. The prototype fixes it. Do not copy the original as is.
- Photographer names in the prototype are **unverified**, inferred from image filenames. They must be confirmed before anything using them ships.

## Stakeholders

Zach Christensen, Stephanie Sim, Xris Anderton, Denis Skarep. Zach's feedback comes through the Pastel board. Stephanie speaks for the photo desk. Xris flagged that the carousel already exists on the site, which is what prompted rebuilding it from the real component rather than designing a new one.

## How this work has been running

Conventions worth keeping, because they were arrived at deliberately:

- **Verify against the real thing.** Layout and visual claims are checked in a real browser at real breakpoints, and against the live site's computed styles rather than screenshots, before saying something works. That discipline is what caught the carousel bug and the two Pages deploys that silently served stale versions.
- **Push to both repos after every change**, so the live link matches what is being discussed.
- **GitHub Pages has twice failed to pick up a pushed commit**, leaving the live link showing an old version and making a fixed problem look unfixed. If the live page looks stale, force a build: `gh api -X POST repos/thara-messeroux/ngn-category-landing-prototypes/pages/builds`, then confirm with `gh api repos/thara-messeroux/ngn-category-landing-prototypes/pages/builds --jq '.[0]|"\(.status) \(.commit[0:7])"'`.
- **Keep the phase README current** as work lands, with the reasoning and not just the change. It is the record stakeholders and the eventual developer read.
- **Writing style:** plain and human, no em dashes, no emoji. Say what changed and why.
- **Editorial, content and photo desk decisions are not the designer's or the assistant's to make.** Surface them and let the team decide. Several open items above are exactly this.
