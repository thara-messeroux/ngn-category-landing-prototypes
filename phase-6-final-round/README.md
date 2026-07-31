# Phase 6: Final Round

**Live preview (public, opens in any browser, no login):**

https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-6-final-round/

Status: active, opened Friday, July 31, 2026. Started as an exact copy of phase-5-stakeholder-refinement as it stood at the end of that phase. Phase 5 is frozen as the record of what was reviewed on July 30. All new work happens here.

Target: this is the last design round. No further design reviews are planned. When everything below is closed, the work moves to development.

## New feedback from the final stakeholder round

Not yet recorded. Add each item here as a checkbox with the name of who raised it, then work through them.

- [ ]

## Carried over from Phase 5, still open

These were logged during Phase 5 and were not closed before it was frozen.

- [ ] Photo forward opening for subtopic pages. Give the newest stories more visual weight at the top instead of a uniform list.
- [ ] Add treatment or highlighted hierarchy at the top of subtopic pages to feature the most recent images. Related to the item above; both were raised on July 27.
- [ ] Search within a topic, raised by Stephanie Sim for finding older stories. The header search already covers the whole site, so the standing suggestion is to build this into the archive page rather than adding a second search box on the category page. Revisit once real story volumes per topic are known.
- [ ] Confirm the photographer names shown in the prototype. They were inferred from image filename initials and have never been checked against the real credits. This needs someone from the photo desk to confirm before the module goes further.
- [ ] Confirm whether Seen around campus should be newest first or an editor's pick. The module currently shows the five most recent, matching the rule the video section uses. This is a photo desk decision.
- [ ] Most Read sits 40px below its section rule where every other section sits at 24px. Left alone in Phase 5 because it was outside that pass. One line to bring in.

## Zach's July 24 Pastel review, still open

Board: https://usepastel.com/link/4wejp064/

Comments 1 and 5 are closed, and the header work is done. Comment 2 was reopened, see the note. The rest are untouched.

- [ ] 2. Heading font. Reopened, needs a conversation with Zach rather than a silent decision. The condensed face was applied as he asked, first to all headlines and then only to the lead, and it was rejected both times on the look. What is verified: a real article hero on the live site does use Kepler Std Condensed Subhead at weight 600, 1 to 1 line height, 0.07px letter spacing, but the live category list does not use the condensed face at all. The ligature fix from that work was a genuine improvement and was kept.
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
