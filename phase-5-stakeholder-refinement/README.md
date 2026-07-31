# Phase 5: Stakeholder Refinement

**Live preview (public, opens in any browser, no login):**

https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-5-stakeholder-refinement/

Status: active. Started as an exact copy of phase-4-mobile-refinement, the version presented on July 27, 2026. Phase 4 stays untouched as the record of what was shown. All new work happens here.

Target: the final review on Thursday, July 30, 2026, where the design is expected to be ready to hand off for development.

## Decided in the July 27 stakeholder review

Present: Zach Christensen, Stephanie Sim, Denis Skarep. The design was well received. Refinements only, no rework.

### Seen around campus
- [x] Keep the module. Zach's Pastel note suggested removing it. Stephanie Sim asked to keep it: NGN photographers produce a high volume of work and recently lost one of their main display placements, so this module helps fill that gap.
- [x] Give it its own space with a more featured treatment. It is now a full width band between the Latest stories and the topic sections, on a tinted surface with larger photos, so the photography is featured rather than competing.
- [x] Keep the newsletter sticky, and move Seen around campus to its own placement. The newsletter is now alone in the sticky rail.

### Video (added July 28)
- [x] A Video section, giving the videographers a home the way Seen around campus does for the photographers. Full width, three columns, six videos: each column leads with one video and carries a second beneath it. Every frame keeps its true 16 by 9 shape and shows its running time.
- [x] The three most recent videos lead each column at full size. The next three sit beneath them as smaller cards, so the section is ordered by recency rather than by an arbitrary choice.
- [x] All videos points at the real Video Archives page on the live site.
- [x] Placed directly above Seen around campus, after The Latest. Video and photography are the two places where the newsroom shows off its own people, so they sit together and get the same standing on the page. The white background on Video and the tinted one on Seen around campus keep them from blurring into each other.
- [x] No byline on the video cards. Photos have one photographer, but a video is usually a team: the Operation Valkyrie piece carries four credits on its own page. Showing a single name would misrepresent who made it, and four names do not fit a card. Credits belong on the video page, where there is room to list everyone.
- [x] Every video links to its real page on the live site, checked.

### Subtopic pages
- [x] Removed the title redundancy. A subtopic page said University News four times and the topic name three. Cut: the line under the title that only restated the section, More University News (now More stories), the archive link repeating the heading above it, and the separate Back to University News link, since the sticky bar title already does that exact job and is already clickable. University News now appears once.
- [x] Subtopic pages now use the same two column shape as the landing page for The Latest. Headlines ran the full width, 131 characters on a single line, well past the 50 to 75 that Nielsen Norman recommends. That section now sits at the same measure as the landing page river with the newsletter sticky beside it, 44 characters a line. More stories and Load More stay full width below, back to 4 columns, since that section is a browsing grid rather than reading text and does not have the same line length problem.
- [ ] Photo forward opening for subtopic pages, still open. Give the newest stories more visual weight at the top instead of a uniform list.
- [ ] Search within a topic, raised by Stephanie for finding older stories. The header search already covers the whole site, so the suggestion is to build this into the archive page rather than adding a second search box here. Revisit once real story volumes per topic are known.
- [ ] Add treatment or highlighted hierarchy at the top of the page to feature the most recent images.

### Section headers (added July 30)
- [x] Section band headers now use the design system pattern from the live site instead of a serif heading with a leader line. Inspected the real markup on the home page: a hairline divider, then a bold uppercase Lato title at 13.6px on the left, and a black square cornered See All button on the right. Applied everywhere a section bar appears: Most Read, Video, Seen around campus, each topic group on the landing page, and the archive link on subtopic pages. The red arrow text links are gone. Most Read carries no button, since it has no archive to point at. Each button names its own destination rather than repeating See All, so the label makes sense on its own: All videos, All photos, More Co-op, All Commencement stories, and so on. That matters for anyone using a screen reader, who would otherwise hear See All five times with no context.

### Seen around campus, carousel (July 30)
- [x] Rebuilt from the carousel used on feature articles, for example the SpongeBob 25th anniversary piece. Its stylesheet and script were read off the live page and reused, so the sizes, easing, gap, drag threshold and dot behaviour are the originals: 560px open with 180px and 80px neighbours, dots that stretch from 8px to a 24px dark pill. Click a frame or a dot to open it, drag or swipe to move, arrow keys work when the carousel has focus. On phones it keeps the same carousel at the reference sizes, 280px open with 120px and 60px neighbours.
- [x] Two changes from the original: square corners instead of the 48px radius, and Kepler and Lato for the caption instead of Segoe UI. Everything else is left as built.
- [x] Fixed a bug carried over from the original. It composes its transform by joining a minus sign to the offset, so a negative offset produces translateX with two minus signs, which browsers reject. It never surfaced on the article page because the offset there is positive. Also dropped the centring maths, which assumes a container about 880px wide and left a large gap at this width; the open photo now lines up with the section heading.
- [x] Six real campus photos with their real titles, descriptions and links, up from three.
- [x] Five photos across instead of six, and the closed ones now step down in width instead of sitting at one size. With six, the four on the right were all the same narrow width and read as a block of offcuts rather than as photos. The four closed photos are now 134, 106, 83 and 65px on a desktop screen, each step 0.786 of the one before it, which is one over the square root of the golden ratio. Four steps at that rate stay clearly different from each other without the last one closing to a hairline. Widths are handed out walking right from the open photo and then outwards to the left, so each width is used exactly once wherever you are in the row and the row keeps its total width.
- [x] Dropping to five means dropping a photo. The module now carries the five most recent, same rule the video section uses. The sixth, Queued up for success from July 9, is still reachable through All photos. Worth confirming with the photo team that recency is the rule they want here rather than an editor's pick.
- [x] The open photo is shown at its real shape and the band is taller. Every photo in the module is 3 by 2, but the frame was a fixed 320px tall and close to 2 by 1, so each photo was being cropped top and bottom to fit. The frame height is now set from the photo ratio, so the open photo is shown whole. On a desktop screen the band goes from 320px to 497px tall. The collapsed photos either side are still cropped, which is the point of them: they are slivers that show what is coming next.
- [x] The height stays the same as you move through the photos. On wide screens the row always holds one open photo, one half open and four slivers, whichever photo is open, so the total width and the open photo's size never change. Without that the open photo would have to grow as it moved along the row to keep the row full, and the whole section would change height on every click.
- [x] The row now runs the full width of the section. The reference carousel uses a fixed 560px open photo, sized for the narrower column of an article page, which left a strip of empty background on the right here and read as inconsistent with every other full width section. The open photo now stretches to fill whatever space the collapsed photos do not use, with 560px as its floor, so the row ends flush with the section rule and the All photos button at every position. Checked at 1440, 1280, 1024, 768 and 375, and on all six photos: left edge lines up with the heading, right edge lines up with the button, no page overflow.

Note for the dev handoff: this carousel is not currently a shared component. On the live site its CSS and JS are inline in that single article, not in the theme, so building it into the category page means creating the component properly rather than reusing an existing one.

## Zach's July 24 Pastel review

Sixteen comments, all still marked active. Comment 1 is praise for the Most Read numerals, the other fifteen are actionable and tracked here.

Pastel board: https://usepastel.com/link/4wejp064/

- [x] 1. "This is a better use of these numbers." Praise for the Most Read numeral redesign, no action needed.
- [x] 2. Heading font, resolved. Inspected a real article hero on the live site directly: it uses Kepler Std Condensed Subhead at weight 600, a tight 1 to 1 line height, and 0.07px letter spacing. That exact style is now applied to the lead story headline only. Every other headline, the rail, the river, the subtopic list, keeps the display face as before, since the live category list itself does not use the condensed face.
- [ ] 3. Slightly more space above the links than below.
- [ ] 4. App bar item, flagged as not strictly page related.
- [x] 5. Newsletter placement. Resolved in the July 27 review: keep the newsletter, keep Seen around campus, give the photo module its own spot.
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

## Previews

Screenshots are added as the work lands.

## How to view

Live preview: https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-5-stakeholder-refinement/

Interactive version: download `index.html` and open it in a browser. It is self-contained and needs no server.
