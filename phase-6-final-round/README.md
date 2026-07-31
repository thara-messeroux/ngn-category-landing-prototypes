# Phase 6: Final Round

**Live preview (public, opens in any browser, no login):**

https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-6-final-round/

Status: active, opened Friday, July 31, 2026. Started as an exact copy of phase-5-stakeholder-refinement as it stood at the end of that phase. Phase 5 is frozen as the record of what was reviewed on July 30. All new work happens here.

Target: this is the last design round. No further design reviews are planned. When everything below is closed, the work moves to development.

## New feedback from the final stakeholder round, July 31

- [x] **Remove the Video section for now.** Removed the `.vband` markup and its dedicated stylesheet block. Phase 5 keeps the full build as the record, so it can come back without redoing the work.
- [ ] **Seen around campus belongs to University News only.** Other categories do not carry a campus photo module. The module is currently drawn as though every category has one.
- [ ] **Build a second category page that has no Seen around campus**, so the difference between a category with the module and one without is visible side by side. Which category to use has not been chosen yet.
- [ ] **The "All Co-op stories" and "All Commencement stories" buttons are being confused with "Load More".** Several people read them as the same control. They sit directly under the Load More bar and both look like a button, so nothing signals that one loads more of the same page and the other leaves for a different page. Two parts to the fix, both requested:
  - [ ] Move the link higher up the page, possibly under the newsletter box, so it is not adjacent to Load More.
  - [ ] Give it a treatment that is more visual and distinctive than a plain button, so it reads as a doorway to a new page and it is obvious what happens on click.
- [ ] **Model the case where a subtopic has no page of its own.** Not every subtopic will have a dedicated page, and the categories are still being defined, so the design needs to show what a subtopic without a destination looks like. Experiential Learning is the suggested example. Right now every subtopic behaves as though it has a page.
- [x] **Remove the More topics bar at the bottom of the page.** Raised as redundant with the menu bar. Checked and it was: the topic nav is sticky and stays on screen at the bottom of the page, carrying the same seven topics. Removed the `.tv-more` block, its stylesheet, and the script that filled in its topic chips. The archive link above it is untouched and is now the last element in the subtopic view. See the note below on what to watch for.
- [x] **Center the sticky nav bar's contents.** Flagged during this round: the topic links sat with more space above them than below. The bar's own padding was already even top and bottom; the cause was `align-items: baseline` aligning the smaller topic links to the large serif title's text baseline instead of centering them as a block. Changed to `align-items: center`. Desktop only, since mobile already uses its own stacked layout and was not affected.

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
