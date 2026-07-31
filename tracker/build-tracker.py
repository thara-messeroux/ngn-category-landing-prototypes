#!/usr/bin/env python3
"""Build the category landing page progress tracker.

Reads the embedded Kepler and Lato faces out of the Phase 6 prototype so the
tracker renders with the real NGN type offline, then writes tracker/index.html.

Edit ITEMS, DONE_LOG and PHASES below as work lands, then re-run:
    python3 tracker/build-tracker.py
"""

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "phase-6-final-round" / "index.html"
OUT = HERE / "index.html"

UPDATED = "Friday, July 31, 2026"

LIVE = "https://thara-messeroux.github.io/ngn-category-landing-prototypes/phase-6-final-round/"
PASTEL = "https://usepastel.com/link/4wejp064/"
WORK_REPO = "https://github.com/News-at-Northeastern/environment/tree/chore-category-landing-prototypes/private/prototypes/category-landing"

# Tiers of remaining work, in the order recommended for doing them.
# status: ready | blocked | parked | done
TIERS = [
    {
        "label": "Tier 1",
        "title": "Clear the deck",
        "note": "Two removals and two one-liners. All fast, all certain, and the two removals change the shape of the page that everything below gets designed into. Doing these first means designing once instead of twice.",
        "items": [
            {
                "title": "Remove the Video section",
                "why": "Asked for on July 31. It is being pulled, not changed, so Phase 5 stays as the record and it can come back without rebuilding it.",
                "effort": "S", "impact": "High", "status": "ready",
                "source": "New, July 31",
            },
            {
                "title": "Remove the More topics bar at the bottom",
                "why": "Verified redundant rather than assumed: at the bottom of the page the sticky nav is still on screen with the same seven topics. Watch that the page still has an ending once it is gone. The fix for that is the redesigned archive link below, not putting the bar back.",
                "effort": "S", "impact": "High", "status": "ready",
                "source": "New, July 31",
            },
            {
                "title": "Bring the Most Read top gap to 24px",
                "why": "It sits at 40px where every other section sits at 24px. The only section still out of step after the Phase 5 spacing pass. One line.",
                "effort": "XS", "impact": "Low", "status": "ready",
                "source": "Carried from Phase 5",
            },
            {
                "title": "Check Pastel 8 and 12 against the current build",
                "why": "Zach asked for The Latest to be narrower and set side by side. The two column shape built in Phase 5 may already answer both. If it does, two board items close for the cost of looking.",
                "effort": "XS", "impact": "Medium", "status": "ready",
                "source": "Pastel 8, 12",
            },
        ],
    },
    {
        "label": "Tier 2",
        "title": "Fix the one real usability problem",
        "note": "This is the only item on the list where people were actually unable to tell what a control would do. It earns going before the modelling work, and once the More topics bar is gone it also does the job of ending the page.",
        "items": [
            {
                "title": "Move the All [Topic] stories link away from Load More",
                "why": "Several people read the two as the same control. They sit next to each other and both look like a button, so nothing signals that one loads more of this page and the other leaves for a different one. Proposed new home is under the newsletter box.",
                "effort": "S", "impact": "High", "status": "ready",
                "source": "New, July 31",
            },
            {
                "title": "Redesign it as a doorway, not a button",
                "why": "Moving it stops the confusion. A more visual treatment is what makes it obvious you are leaving for another page. This is also the candidate for giving the page a proper close.",
                "effort": "M", "impact": "High", "status": "ready",
                "source": "New, July 31",
            },
        ],
    },
    {
        "label": "Tier 3",
        "title": "Model what stakeholders asked to see",
        "note": "Three items that make the prototype tell the truth about the real content. The comparison page depends on the scoping work above it, so they go in this order.",
        "items": [
            {
                "title": "Scope Seen around campus to University News only",
                "why": "No other category carries a campus photo module, but the prototype currently draws it as though every category has one. Fixing this is what makes the comparison page below meaningful.",
                "effort": "M", "impact": "High", "status": "ready",
                "source": "New, July 31",
            },
            {
                "title": "Build a second category page with no Seen around campus",
                "why": "So the difference between a category that has the module and one that does not is visible side by side instead of described.",
                "effort": "L", "impact": "High", "status": "blocked",
                "blocker": "Which category has not been chosen. Editorial call.",
                "source": "New, July 31",
            },
            {
                "title": "Model a subtopic with no page of its own",
                "why": "Not every subtopic will get a dedicated page and the categories are still being defined. Right now every subtopic in the prototype behaves as though it has a destination.",
                "effort": "M", "impact": "Medium", "status": "blocked",
                "blocker": "Experiential Learning is suggested, not confirmed. Depends on the taxonomy work.",
                "source": "New, July 31",
            },
        ],
    },
    {
        "label": "Tier 4",
        "title": "Depth on the subtopic pages",
        "note": "Raised on July 27 and carried through two phases. Real design work rather than a refinement, which is why it sits below the items above and not above them.",
        "items": [
            {
                "title": "Photo forward opening for subtopic pages",
                "why": "Give the newest stories real visual weight at the top instead of a uniform list, and feature the most recent images. Logged as two items in the README, but it is one piece of design work.",
                "effort": "L", "impact": "Medium", "status": "ready",
                "source": "Carried from Phase 5, covers 2 items",
            },
        ],
    },
    {
        "label": "Tier 5",
        "title": "Sweep Zach's Pastel board",
        "note": "Thirteen items still open. Grouped by what they actually cost, because they are not comparable: some are a spacing value, some are a design decision, and two cannot be started at all.",
        "items": [
            {
                "title": "The small and specific ones",
                "why": "3, more space above the links than below. 14, the menu and search icons read heavier than the rest of the app bar. 15, reduce top and bottom padding on a section. 11, vertical spacing on mobile is inconsistent. Best done as one pass.",
                "effort": "S", "impact": "Medium", "status": "ready",
                "source": "Pastel 3, 11, 14, 15",
            },
            {
                "title": "The ones that need a judgment call",
                "why": "7, navigation redundancy now that University News sits right above. 9, one heading can be smaller or removed. 10, add a small Featured section near the top. 13, the same treatment on another section. 16, remove the secondary nav entirely on mobile.",
                "effort": "M", "impact": "Medium", "status": "ready",
                "source": "Pastel 7, 9, 10, 13, 16",
            },
            {
                "title": "The two that cannot start yet",
                "why": "6, we can drop this, needs Zach to point at the element because the comment alone does not say which. 4, the app bar item he flagged himself as not strictly page related, which needs a confirm to close rather than design work.",
                "effort": "XS", "impact": "Low", "status": "blocked",
                "blocker": "Both need Zach. Worth asking now rather than at the end.",
                "source": "Pastel 4, 6",
            },
        ],
    },
    {
        "label": "Parked",
        "title": "Deliberately not in this round",
        "note": "Open, but the recommendation is not to build it in Phase 6. Kept on the tracker so it is a decision on the record and not something that quietly fell off.",
        "items": [
            {
                "title": "Search within a topic",
                "why": "Raised by Stephanie Sim for finding older stories. The header search already covers the whole site, so the standing proposal is to build this into the archive page rather than adding a second search box to the category page. Revisit once real story volumes per topic are known.",
                "effort": "M", "impact": "Medium", "status": "parked",
                "source": "Carried from Phase 5",
            },
        ],
    },
]

# Items that are not the designer's call. Surfaced early on purpose.
NOT_DESIGN = [
    ("Which category gets the comparison page",
     "Editorial. Blocks the second category page in Tier 3."),
    ("Which subtopic has no page of its own",
     "Editorial and taxonomy. Experiential Learning is a suggestion, not a decision. Blocks Tier 3."),
    ("Pastel 6, we can drop this",
     "Needs Zach to point at the element. Cannot be started from the comment alone."),
    ("Pastel 4, the app bar item",
     "Zach flagged it himself as not strictly page related. Needs a confirm to close it out."),
    ("Recency as the rule for Seen around campus",
     "Photo desk. Newest first was answered on July 31 for now, and for now is theirs, so treat it as revisitable."),
    ("Photographer name accuracy",
     "Answered for the prototype, names are not shown. Still true that the names inferred from filenames were never verified, so nothing may ship using them."),
]

PHASES = [
    ("1", "Concepts", "July 14", "Frozen", "phase-1-concepts",
     "Three opening directions. Drew 27 Pastel comments from 7 reviewers, which set up Phase 2."),
    ("2", "Live data", "July 21 to 22", "Frozen", "phase-2-live-data",
     "Four directions rebuilt on real stories, photos, bylines and archive counts from the live site."),
    ("3", "Synthesis", "July 23", "Frozen, presented", "phase-3-synthesis",
     "Zach's composite layout combined with Thara's Most Read rail, newsletter chooser and list styling."),
    ("4", "Mobile refinement", "July 23 to 24", "Frozen, presented July 27", "phase-4-mobile-refinement",
     "Full pass at 375px, the sticky header adopted, Most Read moved up, menu and search built, accessibility audit."),
    ("5", "Stakeholder refinement", "July 28 to 30", "Frozen, presented July 30", "phase-5-stakeholder-refinement",
     "Seen around campus given its own band, Video added, section headers rebuilt on the real pattern, carousel rebuilt from the live component."),
    ("6", "Final round", "from July 31", "Active", "phase-6-final-round",
     "The last design round. When this list closes, the work moves to development."),
]

DONE_LOG = [
    ("Answered by stakeholders on July 31", [
        "Do not show photographer names. This removes the module's dependency on names that were inferred from filenames and never verified, so that risk is gone.",
        "Seen around campus shows the latest first, for now. Newest first rather than an editor's pick, and for now is theirs.",
        "The current heading font stays. The condensed face is not being adopted, which closes Pastel comment 2. The ligature fix made during that work was a real improvement and stays.",
    ]),
    ("Phase 5, Seen around campus", [
        "Kept the module against Zach's note suggesting removal, after Stephanie Sim asked for it. The photographers produce a high volume of work and recently lost one of their main display placements.",
        "Given its own full width band on a tinted surface between the Latest and the topic sections, so the photography is featured rather than competing.",
        "The newsletter is now alone in the sticky rail.",
    ]),
    ("Phase 5, the carousel", [
        "Rebuilt from the carousel used on feature articles, with its stylesheet and script read off the live page rather than approximated, so sizes, easing, gap, drag threshold and dot behaviour are the originals.",
        "Two deliberate changes from the original: square corners instead of the 48px radius, and Kepler and Lato for the caption instead of Segoe UI.",
        "Fixed a real bug carried over from the original, which joins a minus sign to the offset and so produces a translateX with two minus signs on negative offsets. Browsers reject it silently. It never surfaces on the article page because the offset there is always positive.",
        "Dropped the centring maths, which assumes a container about 880px wide and left a large gap at this width.",
        "Six real campus photos with their real titles, descriptions and links, up from three.",
        "Top gap brought in line with the rest of the page, from 44px to 24px.",
        "Five photos across instead of six, with the closed ones stepping down in width by a constant ratio instead of sitting at one width and reading as a block of offcuts.",
        "The open photo shown at its real 3 by 2 shape, so it is no longer cropped top and bottom. The band goes from 320px to 497px tall on desktop.",
        "The band height holds steady as you move through the photos, so the section does not jump on every click.",
        "The row runs the full width of the section, flush with the heading on the left and the button on the right. Checked at 1440, 1280, 1024, 768 and 375, on all six photos.",
    ]),
    ("Phase 5, Video, since removed in Phase 6", [
        "A Video section giving the videographers the standing the photographers have. Full width, three columns, six real videos with real links and running times.",
        "The three most recent leading each column at full size with the next three beneath as smaller cards, so it is ordered by recency rather than by an arbitrary pick.",
        "No bylines, because a video is usually a team and one name would misattribute it. The Operation Valkyrie piece carries four credits.",
        "Placed above Seen around campus, with the white and tinted backgrounds keeping the two from blurring together.",
        "All videos points at the real Video Archives page. Every video links to its real page, checked.",
    ]),
    ("Phase 5, subtopic pages and section headers", [
        "Removed the title redundancy. A subtopic page said University News four times and the topic name three. It now appears once.",
        "The Latest on subtopic pages moved into the same two column shape as the landing page, taking headlines from 131 characters a line to 44 against the 50 to 75 Nielsen Norman recommends. More stories and Load More stay full width, since that is a browsing grid and not reading text.",
        "Section headers rebuilt on the live site's real pattern, read off the real markup rather than eyeballed: hairline rule, bold uppercase Lato at 13.6px, black square cornered button.",
        "Every button names its own destination instead of repeating See All, so a screen reader user does not hear See All five times with no context.",
    ]),
    ("Phase 4, mobile and accessibility", [
        "Full mobile pass at 375px across the header and nav, hero, Most Read, cards, archive grid, newsletter and footer.",
        "Adopted the sticky header pattern from Zach's composite: title left, topics right. On phones the title sits on its own line with a swipeable topic row and a fade hinting at more.",
        "Most Read moved up into a full width strip below the featured stories, with photos and large serif rank numerals, becoming a swipeable row on phones.",
        "Newsletter: the Daily and the Weekend merged into one option labelled with its schedule, and Faculty and Staff removed from the public chooser because it is a restricted list.",
        "Seen around campus first placed under the sticky newsletter so the right column stays full while the Latest list scrolls.",
        "The section title in the sticky bar enlarged and made a link back to the landing view from any topic page.",
        "Every see-more link put on one uppercase style.",
        "The hamburger opens a preview of the site-wide sections menu with the current section highlighted, and the search icon opens a working search bar that runs a real search on the live site. Both fit and work at phone width.",
        "Every section title made a real heading, so the page reads as a clean outline for screen readers. No visible change.",
        "The newsletter now leads with the benefit rather than the mechanic.",
        "Contrast verified against WCAG AA: muted text 9.34 to 1, red links 5.88 to 1.",
        "Topic pages: the small red Topic kicker removed, since the page already says where you are three other ways.",
    ]),
]

# Counts. Every number on the page is derived here so it stays auditable.
PHASE4_CLOSED = 15
PHASE5_CLOSED = 25
PHASE6_CLOSED_NEW = 2          # photographer names, newest first. The font item is Pastel 2, already counted in Phase 5.
PHASE6_BOARD_CLOSED = 3        # the three answered on July 31, as the Phase 6 board shows them
OPEN = 25                      # open checkboxes on the Phase 6 board

PROJECT_TOTAL = PHASE4_CLOSED + PHASE5_CLOSED + PHASE6_CLOSED_NEW + OPEN
PROJECT_CLOSED = PHASE4_CLOSED + PHASE5_CLOSED + PHASE6_CLOSED_NEW
PHASE6_TOTAL = OPEN + PHASE6_BOARD_CLOSED

OPEN_NEW = 8            # new July 31 feedback
OPEN_CARRIED = 4        # carried from Phase 5
OPEN_PASTEL = 13        # Zach's board
BLOCKED = 4             # items that need a person before they can start


def pct(n, d):
    return round(n / d * 100)


def fonts():
    src = SOURCE.read_text(encoding="utf-8")
    faces = re.findall(r"@font-face\{[^}]*\}", src)
    if not faces:
        raise SystemExit("no @font-face rules found in %s" % SOURCE)
    return "".join(faces)


def chip(text, kind):
    return '<span class="chip chip--%s">%s</span>' % (kind, text)


def render_items(tier):
    rows = []
    for n, item in enumerate(tier["items"], 1):
        status = item["status"]
        chips = [
            chip("Effort " + item["effort"], "effort"),
            chip("Impact " + item["impact"], "impact-" + item["impact"].lower()),
            chip({"ready": "Ready", "blocked": "Needs a person",
                  "parked": "Parked", "done": "Done"}[status], status),
        ]
        blocker = ""
        if item.get("blocker"):
            blocker = '<p class="blocker">%s</p>' % item["blocker"]
        rows.append("""
      <li class="item item--{status}">
        <div class="item__rank">{rank}</div>
        <div class="item__body">
          <h4 class="item__title">{title}</h4>
          <p class="item__why">{why}</p>
          {blocker}
          <p class="item__source">{source}</p>
        </div>
        <div class="item__chips">{chips}</div>
      </li>""".format(status=status, rank=n, title=item["title"], why=item["why"],
                      blocker=blocker, source=item["source"], chips="".join(chips)))
    return "".join(rows)


def render_tiers():
    out = []
    for tier in TIERS:
        out.append("""
    <section class="tier">
      <div class="tier__bar">
        <span class="tier__label">{label}</span>
        <h3 class="tier__title">{title}</h3>
        <span class="tier__count">{count} {word}</span>
      </div>
      <p class="tier__note">{note}</p>
      <ol class="items">{items}</ol>
    </section>""".format(label=tier["label"], title=tier["title"], note=tier["note"],
                         count=len(tier["items"]),
                         word="item" if len(tier["items"]) == 1 else "items",
                         items=render_items(tier)))
    return "".join(out)


def render_not_design():
    return "".join(
        '<li><strong>%s.</strong> %s</li>' % (title, note) for title, note in NOT_DESIGN)


def render_phases():
    rows = []
    for num, name, dates, status, folder, note in PHASES:
        active = " phase--active" if status == "Active" else ""
        rows.append("""
      <li class="phase{active}">
        <div class="phase__num">{num}</div>
        <div class="phase__body">
          <h4 class="phase__name">{name} <span class="phase__dates">{dates}</span></h4>
          <p class="phase__note">{note}</p>
        </div>
        <div class="phase__meta">
          <span class="phase__status">{status}</span>
          <a class="phase__link" href="https://thara-messeroux.github.io/ngn-category-landing-prototypes/{folder}/">View</a>
        </div>
      </li>""".format(active=active, num=num, name=name, dates=dates,
                      note=note, status=status, folder=folder))
    return "".join(rows)


def render_done_log():
    out = []
    for heading, entries in DONE_LOG:
        lis = "".join("<li>%s</li>" % e for e in entries)
        out.append("""
      <details class="done">
        <summary><span class="done__head">{heading}</span><span class="done__n">{n}</span></summary>
        <ul>{lis}</ul>
      </details>""".format(heading=heading, n=len(entries), lis=lis))
    return "".join(out)


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Category landing pages, progress tracker</title>
<style>
__FONTS__

:root{
  --red:#c8102e;
  --ink:#1f1f1f;
  --ink-soft:#49454f;
  --ink-faint:#79747e;
  --rule:#e0e0e0;
  --surface:#fff;
  --surface-low:#fafafa;
  --surface-container:#f5f5f5;
  --sans:lato,inter,helvetica,arial,sans-serif;
  --serif:kepler-std,georgia,serif;
  --display:kepler-std-display,kepler-std,georgia,serif;
  --sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px;
  --sp-5:24px; --sp-6:32px; --sp-7:40px; --sp-8:48px; --sp-9:64px;
  --wrap:1120px;
}

*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;
  background:var(--surface);
  color:var(--ink);
  font-family:var(--sans);
  font-size:16px;
  line-height:1.55;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 var(--sp-5)}

/* Masthead */
.masthead{border-top:4px solid var(--red);padding:var(--sp-7) 0 var(--sp-6)}
.eyebrow{
  font-size:12px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;
  color:var(--red);margin:0 0 var(--sp-3)
}
h1{
  font-family:var(--display);font-weight:700;
  font-size:clamp(2.25rem,5.5vw,3.5rem);line-height:1.04;
  letter-spacing:-.01em;margin:0 0 var(--sp-3)
}
.standfirst{
  font-family:var(--serif);font-size:clamp(1.0625rem,2.1vw,1.3125rem);
  line-height:1.5;color:var(--ink-soft);max-width:62ch;margin:0 0 var(--sp-5)
}
.updated{font-size:13px;color:var(--ink-faint);margin:0 0 var(--sp-5)}
.links{display:flex;flex-wrap:wrap;gap:var(--sp-2);list-style:none;margin:0;padding:0}
.links a{
  display:inline-block;padding:9px 16px;background:#000;color:#fff;
  text-decoration:none;font-size:12px;font-weight:900;
  letter-spacing:.09em;text-transform:uppercase;
}
.links a:hover{background:var(--red)}
.links a.ghost{background:transparent;color:#000;box-shadow:inset 0 0 0 1px #000}
.links a.ghost:hover{background:#000;color:#fff}

/* Section bar, the prototype's own pattern */
.bar{
  display:flex;align-items:baseline;gap:var(--sp-4);
  border-top:1px solid var(--rule);padding-top:var(--sp-3);
  margin:var(--sp-8) 0 var(--sp-5)
}
.bar h2{
  font-size:13.6px;font-weight:900;letter-spacing:.11em;text-transform:uppercase;
  margin:0;flex:1 1 auto
}
.bar .bar__aside{font-size:13px;color:var(--ink-faint)}

/* Gauges */
.gauges{display:grid;grid-template-columns:1fr 1fr;gap:var(--sp-5)}
.gauge{border:1px solid var(--rule);padding:var(--sp-5)}
.gauge--lead{background:var(--surface-low);border-color:#000;border-width:2px}
.gauge__label{
  font-size:12px;font-weight:900;letter-spacing:.11em;text-transform:uppercase;
  color:var(--ink-soft);margin:0 0 var(--sp-3)
}
.gauge__figure{display:flex;align-items:baseline;gap:var(--sp-3);margin-bottom:var(--sp-4)}
.gauge__pct{
  font-family:var(--display);font-weight:700;font-size:clamp(3rem,8vw,4.5rem);
  line-height:.9;letter-spacing:-.02em
}
.gauge--lead .gauge__pct{color:var(--red)}
.gauge__frac{font-size:14px;color:var(--ink-soft);padding-bottom:6px}
.meter{height:10px;background:var(--surface-container);overflow:hidden;display:flex}
.meter__fill{background:#000;height:100%}
.gauge--lead .meter__fill{background:var(--red)}
.gauge__legend{font-size:13px;color:var(--ink-soft);margin:var(--sp-3) 0 0}

/* Stat strip */
.stats{
  display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
  background:var(--rule);border:1px solid var(--rule);margin-top:var(--sp-5)
}
.stat{background:var(--surface);padding:var(--sp-4)}
.stat__n{font-family:var(--display);font-weight:700;font-size:2rem;line-height:1;display:block}
.stat--warn .stat__n{color:var(--red)}
.stat__l{
  font-size:11px;font-weight:900;letter-spacing:.09em;text-transform:uppercase;
  color:var(--ink-soft);display:block;margin-top:var(--sp-2)
}

/* Queue intro */
.intro{font-family:var(--serif);font-size:1.0625rem;line-height:1.6;color:var(--ink-soft);max-width:70ch;margin:0 0 var(--sp-6)}
.intro strong{color:var(--ink)}

/* Tiers */
.tier{margin-bottom:var(--sp-8)}
.tier__bar{
  display:flex;align-items:baseline;gap:var(--sp-3);flex-wrap:wrap;
  border-top:2px solid #000;padding-top:var(--sp-3);margin-bottom:var(--sp-3)
}
.tier__label{
  background:#000;color:#fff;padding:4px 10px;font-size:11px;font-weight:900;
  letter-spacing:.09em;text-transform:uppercase
}
.tier__title{font-family:var(--display);font-weight:700;font-size:1.5rem;line-height:1.1;margin:0;flex:1 1 auto}
.tier__count{font-size:12px;font-weight:900;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-faint)}
.tier__note{font-size:15px;color:var(--ink-soft);max-width:78ch;margin:0 0 var(--sp-5)}

.items{list-style:none;margin:0;padding:0}
.item{
  display:grid;grid-template-columns:56px 1fr 210px;gap:var(--sp-4);
  align-items:start;padding:var(--sp-5) 0;border-top:1px solid var(--rule)
}
.item:last-child{border-bottom:1px solid var(--rule)}
.item__rank{
  font-family:var(--serif);font-size:2.5rem;line-height:.9;color:var(--rule);
  font-weight:400;text-align:center
}
.item--ready .item__rank{color:#000}
.item--blocked .item__rank{color:var(--red)}
.item__title{font-family:var(--display);font-weight:700;font-size:1.1875rem;line-height:1.25;margin:0 0 var(--sp-2)}
.item__why{font-size:14.5px;line-height:1.6;color:var(--ink-soft);margin:0}
.blocker{
  font-size:13.5px;line-height:1.5;color:var(--red);margin:var(--sp-3) 0 0;
  padding-left:var(--sp-3);border-left:2px solid var(--red)
}
.item__source{
  font-size:11px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;
  color:var(--ink-faint);margin:var(--sp-3) 0 0
}
.item__chips{display:flex;flex-wrap:wrap;gap:var(--sp-2);justify-content:flex-end}
.chip{
  font-size:11px;font-weight:900;letter-spacing:.07em;text-transform:uppercase;
  padding:4px 9px;white-space:nowrap
}
.chip--effort{background:var(--surface-container);color:var(--ink-soft)}
.chip--impact-high{background:#000;color:#fff}
.chip--impact-medium{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink-faint)}
.chip--impact-low{background:transparent;color:var(--ink-faint);box-shadow:inset 0 0 0 1px var(--rule)}
.chip--ready{background:transparent;color:#000;box-shadow:inset 0 0 0 1px #000}
.chip--blocked{background:var(--red);color:#fff}
.chip--parked{background:var(--surface-container);color:var(--ink-faint)}
.chip--done{background:#000;color:#fff}

/* Not a design decision */
.callout{border-left:4px solid var(--red);background:var(--surface-low);padding:var(--sp-5) var(--sp-5) var(--sp-5) var(--sp-5)}
.callout p{margin:0 0 var(--sp-4);font-size:15px;color:var(--ink-soft);max-width:74ch}
.callout ul{margin:0;padding-left:var(--sp-5)}
.callout li{font-size:14.5px;line-height:1.6;color:var(--ink-soft);margin-bottom:var(--sp-3)}
.callout li strong{color:var(--ink)}

/* Phases */
.phases{list-style:none;margin:0;padding:0}
.phase{
  display:grid;grid-template-columns:48px 1fr 190px;gap:var(--sp-4);
  align-items:start;padding:var(--sp-4) 0;border-top:1px solid var(--rule)
}
.phase:last-child{border-bottom:1px solid var(--rule)}
.phase__num{
  font-family:var(--display);font-weight:700;font-size:1.75rem;line-height:1;
  color:var(--rule);text-align:center
}
.phase--active .phase__num{color:var(--red)}
.phase__name{font-size:15px;font-weight:900;margin:0 0 var(--sp-1)}
.phase__dates{font-weight:400;color:var(--ink-faint);font-size:13px}
.phase__note{font-size:14px;color:var(--ink-soft);margin:0}
.phase__meta{display:flex;flex-direction:column;align-items:flex-end;gap:var(--sp-2)}
.phase__status{font-size:11px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-faint);text-align:right}
.phase--active .phase__status{color:var(--red)}
.phase__link{
  font-size:11px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;
  color:#000;text-decoration:none;box-shadow:inset 0 0 0 1px #000;padding:4px 10px
}
.phase__link:hover{background:#000;color:#fff}

/* Done log */
.done{border-top:1px solid var(--rule)}
.done:last-of-type{border-bottom:1px solid var(--rule)}
.done summary{
  display:flex;align-items:center;gap:var(--sp-3);cursor:pointer;
  padding:var(--sp-4) 0;list-style:none
}
.done summary::-webkit-details-marker{display:none}
.done summary::before{
  content:"+";font-family:var(--serif);font-size:1.25rem;line-height:1;
  color:var(--red);width:16px;flex:0 0 16px
}
.done[open] summary::before{content:"\\2013"}
.done__head{font-size:14px;font-weight:900;flex:1 1 auto}
.done__n{
  font-size:11px;font-weight:900;letter-spacing:.08em;
  background:var(--surface-container);color:var(--ink-soft);padding:3px 9px
}
.done ul{margin:0 0 var(--sp-5);padding-left:var(--sp-9)}
.done li{font-size:14.5px;line-height:1.6;color:var(--ink-soft);margin-bottom:var(--sp-3)}

/* Footnote */
.footnote{
  border-top:1px solid var(--rule);margin-top:var(--sp-8);
  padding:var(--sp-5) 0 var(--sp-9);font-size:13px;line-height:1.65;color:var(--ink-faint)
}
.footnote h3{
  font-size:12px;font-weight:900;letter-spacing:.11em;text-transform:uppercase;
  color:var(--ink-soft);margin:0 0 var(--sp-3)
}
.footnote p{margin:0 0 var(--sp-3);max-width:80ch}

@media (width < 900px){
  .item{grid-template-columns:40px 1fr}
  .item__chips{grid-column:2;justify-content:flex-start;margin-top:var(--sp-2)}
  .item__rank{font-size:1.75rem}
  .phase{grid-template-columns:36px 1fr}
  .phase__meta{grid-column:2;flex-direction:row;align-items:center;justify-content:flex-start}
  .phase__status{text-align:left}
  .stats{grid-template-columns:1fr 1fr}
}
@media (width < 620px){
  .wrap{padding:0 var(--sp-4)}
  .gauges{grid-template-columns:1fr}
  .bar{margin-top:var(--sp-7)}
  .done ul{padding-left:var(--sp-6)}
  .links a{padding:8px 12px;font-size:11px}
}
</style>
</head>
<body>
<div class="wrap">

  <header class="masthead">
    <p class="eyebrow">Northeastern Global News &middot; Design tracker</p>
    <h1>Category landing pages</h1>
    <p class="standfirst">Phase 6 is the final design round. When the list below closes, the work moves to development. This page is the live record of what is done, what is left, and the order worth doing it in.</p>
    <p class="updated">Last updated __UPDATED__ &middot; Designer, Thara Messeroux</p>
    <ul class="links">
      <li><a href="__LIVE__">Live prototype, Phase 6</a></li>
      <li><a class="ghost" href="__PASTEL__">Zach's Pastel board</a></li>
      <li><a class="ghost" href="__WORK_REPO__">Work repo</a></li>
    </ul>
  </header>

  <div class="bar"><h2>Progress</h2><span class="bar__aside">Counted from the phase checklists. See how the numbers are counted at the foot of the page.</span></div>

  <div class="gauges">
    <div class="gauge gauge--lead">
      <p class="gauge__label">Phase 6, ready for development</p>
      <div class="gauge__figure">
        <span class="gauge__pct">__P6_PCT__%</span>
        <span class="gauge__frac">__P6_CLOSED__ of __P6_TOTAL__ items closed</span>
      </div>
      <div class="meter"><div class="meter__fill" style="width:__P6_PCT__%"></div></div>
      <p class="gauge__legend">This is the number that decides when design hands over. It is low because Phase 6 opened today.</p>
    </div>
    <div class="gauge">
      <p class="gauge__label">Whole project to date</p>
      <div class="gauge__figure">
        <span class="gauge__pct">__ALL_PCT__%</span>
        <span class="gauge__frac">__ALL_CLOSED__ of __ALL_TOTAL__ items closed</span>
      </div>
      <div class="meter"><div class="meter__fill" style="width:__ALL_PCT__%"></div></div>
      <p class="gauge__legend">Every tracked item across Phases 4, 5 and 6. Phases 1 to 3 were exploration and were not run as checklists, so they sit in the timeline instead.</p>
    </div>
  </div>

  <div class="stats">
    <div class="stat"><span class="stat__n">__OPEN_NEW__</span><span class="stat__l">New, July 31</span></div>
    <div class="stat"><span class="stat__n">__OPEN_CARRIED__</span><span class="stat__l">Carried from Phase 5</span></div>
    <div class="stat"><span class="stat__n">__OPEN_PASTEL__</span><span class="stat__l">On Zach's board</span></div>
    <div class="stat stat--warn"><span class="stat__n">__BLOCKED__</span><span class="stat__l">Need a person first</span></div>
  </div>

  <div class="bar"><h2>Do next, in order</h2><span class="bar__aside">__OPEN__ open items, grouped into __TIERS__ tiers</span></div>

  <p class="intro">The order is <strong>subtract first, then fix the one thing people could not understand, then model what stakeholders asked to see, then depth, then sweep the board</strong>. Two things drive it: what costs least for what it returns, and what has to be settled before the next thing can be designed. Pulling Video and the More topics bar changes the shape of the page, so anything designed before that would get designed twice. Effort and impact below are my estimate, not stakeholder input.</p>

__TIERS_HTML__

  <div class="bar"><h2>Not a design decision</h2><span class="bar__aside">Surface these now, not at handoff</span></div>

  <div class="callout">
    <p>Each of these needs someone other than the designer to answer. Four of them block work in the queue above. Raising them early is the difference between a decision and a blocker.</p>
    <ul>__NOT_DESIGN__</ul>
  </div>

  <div class="bar"><h2>Phases</h2><span class="bar__aside">Each phase is frozen when it closes, so every review keeps its own record</span></div>

  <ol class="phases">__PHASES__</ol>

  <div class="bar"><h2>Closed, with the reasoning</h2><span class="bar__aside">__ALL_CLOSED__ items. Open a group to read what changed and why</span></div>

__DONE_LOG__

  <div class="footnote">
    <h3>How the numbers are counted</h3>
    <p><strong>Whole project</strong> counts every distinct item once across the Phase 4, 5 and 6 checklists: __PHASE4__ closed in Phase 4, __PHASE5__ in Phase 5, __PHASE6NEW__ new in Phase 6, and __OPEN__ still open. <strong>Phase 6</strong> counts the items on the Phase 6 board only. The heading font decision appears on both the Phase 5 and Phase 6 boards, closed differently each time, which is why the two figures do not sum.</p>
    <p>The queue collapses some board items into one row where they are one piece of work: the two halves of the archive link fix, the two subtopic photo items, and Zach's thirteen board comments grouped into four rows by what they actually cost. Every open board item is represented.</p>
    <p>Source of truth is <code>phase-6-final-round/README.md</code> in the work repo. This page is generated from <code>tracker/build-tracker.py</code>, so it is regenerated rather than hand-edited as items land.</p>
  </div>

</div>
</body>
</html>
"""


def main():
    html = TEMPLATE
    subs = {
        "__FONTS__": fonts(),
        "__UPDATED__": UPDATED,
        "__LIVE__": LIVE,
        "__PASTEL__": PASTEL,
        "__WORK_REPO__": WORK_REPO,
        "__P6_PCT__": str(pct(PHASE6_BOARD_CLOSED, PHASE6_TOTAL)),
        "__P6_CLOSED__": str(PHASE6_BOARD_CLOSED),
        "__P6_TOTAL__": str(PHASE6_TOTAL),
        "__ALL_PCT__": str(pct(PROJECT_CLOSED, PROJECT_TOTAL)),
        "__ALL_CLOSED__": str(PROJECT_CLOSED),
        "__ALL_TOTAL__": str(PROJECT_TOTAL),
        "__OPEN_NEW__": str(OPEN_NEW),
        "__OPEN_CARRIED__": str(OPEN_CARRIED),
        "__OPEN_PASTEL__": str(OPEN_PASTEL),
        "__BLOCKED__": str(BLOCKED),
        "__OPEN__": str(OPEN),
        "__TIERS__": str(len(TIERS)),
        "__TIERS_HTML__": render_tiers(),
        "__NOT_DESIGN__": render_not_design(),
        "__PHASES__": render_phases(),
        "__DONE_LOG__": render_done_log(),
        "__PHASE4__": str(PHASE4_CLOSED),
        "__PHASE5__": str(PHASE5_CLOSED),
        "__PHASE6NEW__": str(PHASE6_CLOSED_NEW),
    }
    for key, value in subs.items():
        html = html.replace(key, value)
    leftovers = re.findall(r"__[A-Z0-9_]+__", html)
    if leftovers:
        raise SystemExit("unreplaced placeholders: %s" % sorted(set(leftovers)))
    OUT.write_text(html, encoding="utf-8")
    print("wrote %s (%.2f MB)" % (OUT, OUT.stat().st_size / 1024 / 1024))
    print("phase 6: %d%% (%d of %d)" % (pct(PHASE6_BOARD_CLOSED, PHASE6_TOTAL),
                                        PHASE6_BOARD_CLOSED, PHASE6_TOTAL))
    print("project: %d%% (%d of %d)" % (pct(PROJECT_CLOSED, PROJECT_TOTAL),
                                        PROJECT_CLOSED, PROJECT_TOTAL))


if __name__ == "__main__":
    main()
