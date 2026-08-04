# Phase 6: Final Round

**Live preview (public, opens in any browser, no login):**

https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-6-final-round/

Status: active, opened Friday, July 31, 2026. Started as an exact copy of phase-5-stakeholder-refinement as it stood at the end of that phase. Phase 5 is frozen as the record of what was reviewed on July 30. All new work happens here.

Target: this is the last design round. No further design reviews are planned. When everything below is closed, the work moves to development.

## Live stories, August 4

- [x] **Root cause of the old stories, and of photo captions showing up as headlines: the pages were reading the wrong post type.** Articles on this site are a custom type called `newspost`. The built-in WordPress `post` type still holds the retired photo-of-the-day and video items, and nothing else recent. So `/wp-json/wp/v2/posts` answered with the newest thing it had, which was a string of one-line photo captions from the Seen around campus module, while every real article was invisible to it. Both prototypes now read `/wp-json/wp/v2/newspost`. That single change is what fixed the stale dates and the captions-as-headlines problem at the same time; they were never two separate faults.

  One headline that still reads "Photos: ..." is a genuine article, not a caption: the weekly photo round-up runs about 1,600 words and appears on the real University News page. It is meant to be there.

- [x] **Every story section is now live, newest first, and refreshes on each page load.** Previously only the featured band and The Latest were live. Now the four topic bands lower down the landing page each fetch their own tag, and each subtopic page fetches its own tag for both The Latest and More stories. Nothing is hardcoded to a date any more. Verified section by section in a browser against the real API: all four bands moved from 2023 and 2024 captures to 2026, and all seven subtopic pages show their own distinct stories in descending date order rather than the one shared list they showed before.

- [x] **Captured stories are still what a reader without a connection sees.** The prototypes stay self-contained single files, so every fetch is additive: it replaces captured markup only on success. Verified by neutering the network calls and reloading, which leaves all four bands, the featured band, The Latest, Most Read, Seen around campus and every subtopic page intact, with Load More still working.

- [x] **Ordering fixed in the captured fallback too.** The captured stories were grouped by subject rather than by date, which showed on the Arts and Entertainment Books band as July 7, July 6, July 10. Each band now sorts newest first on load regardless of whether the live swap happens.

- [x] **A topic keeps its captured stories when its tag has nothing newer.** The guard added on July 31 still applies per section. Where it fires, that is a real content gap rather than a prototype fault, and it is worth knowing before the review:

  - **Sparse tags on University News.** Co-op is current, newest August 3. Experiential Learning stops at July 10, President Aoun at June 5, Events at April 16. Those are genuinely the newest articles carrying those tags.
  - **Sparse tags on Arts and Entertainment.** Movies, Music and Video Games are reasonably current. Television stops at February, Books at May, Theater at January, Streaming at July 2025.
  - **One inconsistency this creates, worth a decision.** A band keeps its curated stories when they are fresher than its tag, but the subtopic page behind the same heading always shows the pure tag feed. So Books shows July stories in the band and May stories on its own page. Whether a section should favour the fresher curated mix or match its tag exactly is an editorial call, not an engineering one.

- [x] **Today's date reads the visitor's own clock**, so it is correct whenever the page is opened rather than frozen at the build date.

- [x] **Real bug fixed: the gap above the newsletter box on mobile was two spacings stacked.** Reported as one gap, it was two different faults. On a subtopic page the story list carried a 48px bottom margin and the two column shell it sits in carried a 48px row gap, so the two added up to 96px. The margin was redundant, since the shell gap already owns that separation, and it is gone. On the landing page the same shell contributed a single 48px, which is correct as a gap between two columns on desktop but too wide once they stack into one column on mobile, where the story cards sit 32px apart.

  Both shells now set the column gap and the row gap separately: the column gap stays 48px so desktop is untouched, and the row gap is 32px so the stacked mobile order matches the card rhythm. Measured after the change: 32px on both pages, the same as the gap between story cards, down from 96px and 48px. Desktop re-measured to confirm nothing moved, including the 48px that still sits below the shell before More stories.

- [x] **The space above and below the newsletter box now matches, at 32px.** Fixing the gap above it left the space below it at 48px, so the box sat off centre between its neighbours. The 48px was not one rule but three different ones depending on which page you were on: Seen around campus carries its own top margin on the landing page, the More stories heading carried an inline 48px on subtopic pages, and on Arts and Entertainment a topic section opens the space instead, since that page has no campus band. All three are now 32px on mobile and unchanged on desktop, where the newsletter sits beside the stories rather than below them and the wider section rhythm is correct. Commencement's campaign card, the one thing that sits below the newsletter rather than after it, moved from 24px to 32px for the same reason.

  Measured after the change: 32px above and below on the landing page and on all seven University News subtopics, including Commencement with its card, and on Arts and Entertainment. Desktop confirmed unmoved at 48px throughout.

- [x] **Real bug found while measuring this: a stray unclosed brace was disabling a block of mobile styles.** A `@media (prefers-reduced-motion: reduce)` wrapper was left open and had swallowed the `@media (width < 840px)` block that follows it, so Seen around campus kept its desktop padding on phones and its heading kept its desktop size, unless a visitor happened to have reduced motion switched on. Closing the wrapper restored both. Worth knowing at handoff: this was invisible on the page because the values it should have applied were smaller, not different in kind. Every stylesheet block in both files is now brace balanced, checked programmatically rather than by eye.

## New feedback from the final stakeholder round, July 31

- [x] **Remove the Video section for now.** Removed the `.vband` markup and its dedicated stylesheet block. Phase 5 keeps the full build as the record, so it can come back without redoing the work.
- [ ] **Seen around campus belongs to University News only.** Other categories do not carry a campus photo module. The module is currently drawn as though every category has one.
- [ ] **Build a second category page that has no Seen around campus**, so the difference between a category with the module and one without is visible side by side. Which category to use has not been chosen yet.
- [x] **The "All Co-op stories" and "All Commencement stories" buttons are being confused with "Load More".** Several people read them as the same control. They sit directly under the Load More bar and both look like a button, so nothing signals that one loads more of the same page and the other leaves for a different page. Two parts to the fix, both requested:
  - [x] Move the link higher up the page, possibly under the newsletter box, so it is not adjacent to Load More. Moved into the rail, directly under the newsletter box. Load More is now the last element in the section with nothing beside it.
  - [x] Give it a treatment that is more visual and distinctive than a plain button, so it reads as a doorway to a new page and it is obvious what happens on click. Replaced the filled black pill, the same shape as Load More, with a bordered card and a trailing arrow that shifts on hover.
  - [x] **The campaign card is now a reusable pattern, not a Commencement one-off, and every subtopic uses it.** All seven subtopics use this card. Two variants from one lookup: a logo variant using the destination's own wordmark, and a type variant setting the topic name in the display serif. Commencement uses the logo variant since it is the only subtopic with a real microsite to point to; Co-op, Students, Faculty, Experiential Learning, Events and President Aoun use the type variant, each pointing at its own real tag archive (each checked directly, not assumed). All seven cards measure identical height, padding, radius and surface, confirmed at 1440 and 375. The mismatch this took two passes to close: the logo was originally sized by width, which rendered shorter than the text titles' line height; fixed by sizing the logo by height instead so both variants occupy the same vertical space. Keeping the real logo on Commencement rather than replacing it with plain text was a deliberate call, confirmed with Thara: the one intentional difference among otherwise identical cards.
  - [x] **Softened it.** The first version was a solid brand-red field, too strong for a page where red is otherwise only ever a small accent. It now uses the design system's own soft red surface (`primary-container`, `#ffdad8`) with the brand red for the heading and the page ink for the description, an outlined pill for the label, and the arrow mark dropped to a faint tint. `primary-container` and `on-primary-container` were added to the token block; both are real design-system values that simply were not declared here before. Measured on the new surface: brand red 4.56 to 1, body ink 13.28 to 1, both passing AA for normal text.
  - [x] **Which subtopics get a campaign card: answered, every subtopic does.** Confirmed with Thara: all seven use the card rather than five falling back to the plain one. Still open and not a design decision: the pill labels ("Special coverage", "Topic archive") and descriptions are placeholders for editorial to confirm, and Co-op's card points at its real tag archive as a placeholder since it has no hub page (`/co-op/` redirects to a 2013 article).
  - [x] **Text titles restyled to echo the Commencement logo's feel.** The six type-variant cards moved from the bold display serif to the regular-weight serif already used for body copy elsewhere (`.blurb`), which reads closer to the logo's lighter linework. Deliberately not italic: no italic face is embedded for either serif in this file, so italic would have forced a synthesized fake slant. Card height held at 166px across all seven.
  - [x] **Real bug found and fixed: Most Read and Seen around campus were bleeding onto every subtopic page.** Not a spacing issue, reported as one. Both are landing-page modules that were never added to the rule hiding other landing sections when a subtopic view is open, so Load More sat with a literal 0px gap before Most Read on every subtopic page. Confirmed this predates Phase 6: the identical incomplete rule exists in the frozen Phase 5 file. Added `.mr-strip` and `.campus-band` to the hide list. Load More is now confirmed the last visible element on a subtopic page; both modules still show normally on the landing page.
  - [x] **Commencement specifically, added July 31 afternoon.** Commencement is not a plain tag archive, it leads to a fully branded campaign microsite (`commencement-2026`), which the generic card did not communicate and which was pointing at the wrong URL entirely (a generated `/tag/commencement/` link, since Commencement has no landing-page topic group for the archive link to read its real URL from). Fixed the link, and gave Commencement its own card: a solid dark card carrying the campaign's real logo, pulled from the live site, with a short description. Every other subtopic keeps the plain bordered card; easy to extend to another subtopic later via a small lookup in the script. A real event photo was tried first and dropped, since the only stills available were either a close-up of a named speaker, not appropriate to reuse as decoration, or a fully text-and-crest title card with no actual photography in it.
- [ ] **Model the case where a subtopic has no page of its own.** Not every subtopic will have a dedicated page, and the categories are still being defined, so the design needs to show what a subtopic without a destination looks like. Experiential Learning is the suggested example. Right now every subtopic behaves as though it has a page.
- [x] **Remove the More topics bar at the bottom of the page.** Raised as redundant with the menu bar. Checked and it was: the topic nav is sticky and stays on screen at the bottom of the page, carrying the same seven topics. Removed the `.tv-more` block, its stylesheet, and the script that filled in its topic chips. The archive link above it is untouched and is now the last element in the subtopic view. See the note below on what to watch for.
- [x] **Center the sticky nav bar's contents.** Flagged during this round: the topic links sat with more space above them than below. The bar's own padding was already even top and bottom; the cause was `align-items: baseline` aligning the smaller topic links to the large serif title's text baseline instead of centering them as a block. Changed to `align-items: center`. Desktop only, since mobile already uses its own stacked layout and was not affected.
- [x] **Colour tokens corrected against the real design system.** These prototypes are standalone files with no build step, so they declare the `--ngn-v2-sys-color-*` tokens by hand rather than importing the design system. Five had drifted from the values in `themes/ngn-theme/src/styles/design-system-v2`: `on-surface` (`#1f1f1f` to `#281717`), `outline-variant` (`#e0e0e0` to `#cac4d0`), `surface-container` (`#f5f5f5` to `#f3f3f3`), `inverse-surface` (`#1f1f1f` to `#000`) and `inverse-on-surface` (`#f5f5f5` to `#fff`). All nine checked tokens now match. The visible difference is small but real: body text is the warm near-black the design system specifies rather than a neutral grey. The carousel dot colours are deliberately left alone, since they are copied from the article component this carousel was rebuilt from and matching it is the point.

### On removing the More topics bar

Agreeing with this, with one thing to keep an eye on. The bar is genuinely redundant, and that is verified rather than assumed: at the very bottom of the page the sticky nav is still visible and holds the same topics. Repeating them adds nothing.

What it does do is give the page an ending. Take it away and the last thing on the page is a topic section, which can feel like the page just stops. If that reads badly once it is gone, the answer is not to put the bar back but to give the page a proper close, and the newly designed link to the full archive is the obvious candidate for that job.

## Answered by stakeholders, July 31

These were open questions waiting on a person. They now have answers.

- [x] **Do not show photographer names.** This removes the module's dependency on the names that were inferred from filenames and never verified, so that risk is gone.
- [x] **Seen around campus shows the latest first, for now.** Newest first rather than an editor's pick. "For now" is theirs, so treat it as a decision that may be revisited rather than a permanent rule.
- [x] **The current heading font stays.** Zach's Pastel comment 2 is closed. The condensed face is not being adopted. The ligature fix made during that work was a genuine improvement and stays.

## Carried over from Phase 5, still open

These were logged during Phase 5 and were not closed before it was frozen.

- [ ] Photo forward opening for subtopic pages. Give the newest stories more visual weight at the top instead of a uniform list.
- [ ] Add treatment or highlighted hierarchy at the top of subtopic pages to feature the most recent images. Related to the item above; both were raised on July 27.
- [ ] Search within a topic, raised by Stephanie Sim for finding older stories. The header search already covers the whole site, so the standing suggestion is to build this into the archive page rather than adding a second search box on the category page. Revisit once real story volumes per topic are known.
- [x] Photographer names. Answered on July 31: do not show them.
- [x] Newest first or editor's pick for Seen around campus. Answered on July 31: newest first for now.
- [x] Most Read sits 40px below its section rule where every other section sits at 24px. Checked on July 31: it is already 24px, measured against the rendered page at 1440, 768 and 375, matching Seen around campus exactly. Something upstream of this note, most likely the Phase 5 section header rebuild, already fixed it. No change made here since there was nothing left to change.

## Zach's July 24 Pastel review, still open

Board: https://usepastel.com/link/4wejp064/

Comments 1, 2 and 5 are closed and the header work is done. The rest are untouched.

- [x] 2. Heading font. Closed on July 31: the current font stays and the condensed face is not being adopted. For the record, a real article hero on the live site does use Kepler Std Condensed Subhead at weight 600, 1 to 1 line height, 0.07px letter spacing, but the live category list does not use the condensed face at all. The ligature fix from that work was kept.
- [ ] 3. Slightly more space above the links than below.
- [ ] 4. App bar item, flagged by Zach as not strictly page related.
- [ ] 6. "We can drop this." Needs Zach to point at the element, unclear from the comment alone.
- [ ] 7. Navigation redundancy now that the nav has switched and University News sits right above.
- [ ] 8. The Latest section feels excessively wide.
- [ ] 9. One heading can be significantly smaller or removed.
- [ ] 10. Add a small Featured section near the top.
- [ ] 11. Vertical spacing on mobile is inconsistent.
- [ ] 12. Place the Latest stories side by side to use the width better.
- [ ] 13. Same treatment applies to another section.
- [ ] 14. The menu and search icons read heavier than the rest of the app bar.
- [ ] 15. Reduce top and bottom padding on one section.
- [ ] 16. Consider removing the secondary nav entirely on mobile.

Items 8 and 12 may already be answered by the two column shape built in Phase 5. Worth checking against the current build before spending time on them.

## Carried into development

Not design work, but it must not get lost at handoff.

- The Seen around campus carousel is not a shared component. On the live site its CSS and JS are inline in a single article, not in the theme, so building it into the category page means creating the component properly rather than reusing an existing one. Verified by searching the repo, which returns no matches for it.
- The article version of that carousel carries a real bug. It composes its transform by joining a minus sign to the offset, so a negative offset produces a translateX with two minus signs, which browsers reject and silently drop. It does not surface on the article page because the offset there is always positive. The prototype fixes it. Whoever builds the component should not copy the original as is.

## How to view

Live preview: https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-6-final-round/

Interactive version: download `index.html` and open it in a browser. It is self-contained and needs no server.
