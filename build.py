#!/usr/bin/env python3
"""Generate the five category-landing prototype pages from content.json.

PROTOTYPE ONLY. Run: python3 build.py  (from this directory)
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
THEME_IMG = HERE / "../../../themes/ngn-theme/assets/images"

CONTENT = json.loads((HERE / "content.json").read_text())
STORIES = CONTENT["stories"]
PHOTOS = CONTENT["photos"]
FOOTER = (HERE / "footer-partial.html").read_text()
WORDMARK = (THEME_IMG / "ngn-wordmark.svg").read_text()
LETTERMARK = (THEME_IMG / "ngn-lettermark.svg").read_text()

# The prototype's fictional "now" — drives the appbar date stamp and
# the Google News-style relative dates.
PROTO_NOW = __import__("datetime").datetime(2026, 7, 21, 12, 0)
DATE_STAMP = PROTO_NOW.strftime("%A, %B %-d, %Y")

TOPICS = ["Commencement", "Co-op", "Students", "Faculty",
          "Experiential Learning", "Events", "President Aoun"]

ICON_MENU = ('<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" '
             'stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" '
             'stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"/></svg>')
ICON_SEARCH = ('<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" '
               'stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" '
               'stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 '
               '5.196a7.5 7.5 0 0010.607 10.607z"/></svg>')
ICON_CAMERA = ('<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" '
               'stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" '
               'stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"/>'
               '<path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z"/></svg>')


def fmt_date(iso):
    from datetime import date
    d = date.fromisoformat(iso)
    return d.strftime("%B %-d, %Y")


def fmt_when(iso):
    """Google News-style relative time up to 6 days, then the date."""
    from datetime import datetime
    d = datetime.fromisoformat(iso)
    days = (PROTO_NOW.date() - d.date()).days
    if days < 0:
        return d.strftime("%B %-d, %Y")
    if days == 0:
        mins = (PROTO_NOW - d).total_seconds() / 60
        if mins < 60:
            return f"{max(1, int(mins))} minutes ago"
        return f"{int(mins // 60)} hours ago"
    if days == 1:
        return "Yesterday"
    if days <= 6:
        return f"{days} days ago"
    return d.strftime("%B %-d, %Y")


def build_anim_wordmark():
    """Wordmark SVG with per-glyph classes for the scroll-condense animation.

    Path order inside the <g>: Northeastern (1-12), Global (13-18),
    News (19-22). The word-initial N/G/N glyphs get wm-k* classes and
    slide into the monogram arrangement; the rest travel with their
    word's initial while fading (wm-fade + wm-w*). The arrow polygon
    (wm-arrow) shrinks and top-aligns to match the NGN monogram.
    """
    svg = WORDMARK.replace('class="ngn-wordmark"',
                           'class="ngn-wordmark ngn-wordmark--anim"', 1)
    svg = svg.replace('ngn-wordmark__shapes ngn-wordmark__shapes-arrow',
                      'ngn-wordmark__shapes ngn-wordmark__shapes-arrow wm-arrow', 1)
    keep = {1: "wm-k0", 13: "wm-k1", 19: "wm-k2"}
    parts = svg.split('<path ')
    assert len(parts) == 23, f"expected 22 wordmark letter paths, got {len(parts) - 1}"
    out = [parts[0]]
    for i, chunk in enumerate(parts[1:], start=1):
        cls = keep.get(i) or ("wm-fade " + ("wm-w1" if i < 13 else "wm-w2" if i < 19 else "wm-w3"))
        out.append(f'<path class="{cls}" {chunk}')
    return "".join(out)


WORDMARK_ANIM = build_anim_wordmark()


def app_bar(sticky=False, anim_logo=False):
    """Logo_And_Date App Bar (ngn-app App_Bar component markup shape)."""
    wordmark = WORDMARK_ANIM if anim_logo else WORDMARK
    return f'''
<div class="ngn-bar is-config-logo-and-date has-bottom-divider{' is-sticky' if sticky else ''}">
  <div class="bar__wrapper">
    <div class="app-bar__leading">
      <button class="icon-button" aria-label="Menu">{ICON_MENU}</button>
    </div>
    <a class="app-bar__logo-link" href="https://news.northeastern.edu" rel="home"
       aria-label="Northeastern Global News">
      <span class="app-bar__logo app-bar__logo--mobile" style="height:24px">{LETTERMARK}</span>
      <span class="app-bar__logo app-bar__logo--desktop" style="height:22px">{wordmark}</span>
    </a>
    <div class="app-bar__trailing-elements">
      <div class="app-bar__text">{DATE_STAMP}</div>
      <button class="icon-button" aria-label="Search">{ICON_SEARCH}</button>
    </div>
  </div>
</div>'''


def meta(s, byline=True, date=True):
    parts = []
    if byline and s["byline"]:
        parts.append(f'<span class="byline">{s["byline"]}</span>')
    if date:
        parts.append(f'<time>{s.get("_when") or fmt_date(s["date"])}</time>')
    return f'<div class="post-meta">{" &middot; ".join(parts)}</div>' if parts else ""


def card(s, mode="stacked", kicker=None, blurb=True, byline=True, date=True,
         headline_px=21, ratio="3 / 2", radius=None):
    """story-link-v3-shaped card. Modes: stacked | rich | text | thumb."""
    k = f'<div class="kicker">{kicker}</div>' if kicker else ""
    b = f'<p class="blurb">{s["dek"]}</p>' if blurb and s["dek"] else ""
    m = meta(s, byline, date)
    r = f"border-radius:{radius};" if radius else ""
    media = (f'<div class="media-frame" style="{r}">'
             f'<img src="{s["img"]}" alt="" loading="lazy" style="aspect-ratio:{ratio}"></div>')
    text = (f'<div class="story__text">{k}'
            f'<h3 class="headline" style="font-size:{headline_px}px">{s["title"]}</h3>'
            f'{b}{m}</div>')
    if mode == "text":
        inner = text
    elif mode == "rich":
        inner = f'<div class="story--rich">{text}{media}</div>'
    elif mode == "thumb":
        inner = f'<div class="story--thumb">{text}{media}</div>'
    else:
        inner = f'{media}{text}'
    return f'<article class="story is-mode-{mode}"><a href="{s["link"]}">{inner}</a></article>'


def photo_module(photos, n=3, heading="Seen around campus", horizontal=False):
    cls = "photo-module--row" if horizontal else ""
    items = "".join(
        f'<a class="photo-module__item" href="{p["link"]}">'
        f'<div class="media-frame"><img src="{p["img"]}" alt="" loading="lazy"></div>'
        f'<div class="photo-module__caption"><strong>{p["title"]}</strong> {p["dek"][:90]}&hellip;</div>'
        f'</a>'
        for p in photos[:n])
    return f'''
<section class="photo-module {cls}">
  <div class="photo-module__head">{ICON_CAMERA}<span>{heading}</span>
    <a href="#" class="photo-module__more">All photos &rarr;</a></div>
  <div class="photo-module__items">{items}</div>
</section>'''


def page(title, css, body, sticky_bar=False, anim_logo=False):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — University News prototype</title>
<link rel="stylesheet" href="https://use.typekit.net/kab0ulp.css">
<link rel="stylesheet" href="shared.css">
<style>{css}</style>
</head>
<body>
<a href="#site-content" class="screen-reader-text">Skip to content</a>
<header class="site-header">{app_bar(sticky=sticky_bar, anim_logo=anim_logo)}</header>
<main id="site-content">{body}</main>
{FOOTER}
</body>
</html>'''


S = STORIES  # shorthand

# ======================================================================
# 01 — The Broadsheet (WSJ / Business Insider)
# ======================================================================

BROADSHEET_CSS = '''
.cat-head { padding-block: var(--sp-large) var(--sp-compact); border-bottom: 2px solid var(--ngn-v2-sys-color-on-surface); }
.cat-head h1 { font-family: var(--font-serif-display); font-size: 48px; font-weight: 700; letter-spacing: -1px; }
.cat-head .dek { font-family: var(--font-serif); font-size: 19.3px; color: var(--ngn-v2-sys-color-on-surface-variant); margin-top: var(--sp-base); }
.topic-line { display: flex; flex-wrap: wrap; gap: var(--sp-base) var(--sp-medium); padding-block: var(--sp-small); border-bottom: 1px solid var(--ngn-v2-sys-color-outline-variant); font-size: 13.6px; font-weight: 700; letter-spacing: 0.25px; }
.topic-line a:hover { color: var(--ngn-v2-sys-color-primary); }
.package { display: grid; grid-template-columns: 1fr; gap: var(--sp-large); padding-block: var(--sp-large); }
@media (width >= 840px) { .package { grid-template-columns: 260px 1fr 280px; } }
.rail { display: flex; flex-direction: column; }
.rail .story + .story { border-top: 1px solid var(--ngn-v2-sys-color-outline-variant); margin-top: var(--sp-compact); padding-top: var(--sp-compact); }
.rail .story .blurb { display: none; }
.rail-label { font-family: var(--font-sans); font-size: 12px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; padding-bottom: var(--sp-small); border-bottom: 1px solid var(--ngn-v2-sys-color-on-surface); margin-bottom: var(--sp-compact); }
.lead .story > a { display: block; }
.lead .headline { margin-top: var(--sp-small); }
.lead .blurb { margin-top: var(--sp-base); font-size: 17px; }
.lead .post-meta { margin-top: var(--sp-base); }
.lead-secondary { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-medium); border-top: 1px solid var(--ngn-v2-sys-color-outline-variant); margin-top: var(--sp-medium); padding-top: var(--sp-medium); }
.lead-secondary .blurb { display: none; }
.most-read { counter-reset: mr; }
.most-read .story { counter-increment: mr; display: flex; gap: var(--sp-small); }
.most-read .story::before { content: counter(mr); font-family: var(--font-serif-display); font-size: 34px; font-weight: 700; color: var(--ngn-v2-sys-color-outline); line-height: 1; min-width: 28px; }
.most-read .story + .story { border-top: 1px solid var(--ngn-v2-sys-color-outline-variant); margin-top: var(--sp-compact); padding-top: var(--sp-compact); }
.photo-module { border: 1px solid var(--ngn-v2-sys-color-outline-variant); padding: var(--sp-compact); margin-top: var(--sp-large); }
.photo-module__head { display: flex; align-items: center; gap: var(--sp-base); font-size: 12px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: var(--sp-compact); }
.photo-module__head svg { width: 18px; height: 18px; color: var(--ngn-v2-sys-color-primary); }
.photo-module__more { margin-left: auto; color: var(--ngn-v2-sys-color-primary); font-weight: 700; text-transform: none; letter-spacing: 0.25px; }
.photo-module__items { display: grid; gap: var(--sp-compact); }
.photo-module__caption { font-size: 12px; line-height: 1.45; color: var(--ngn-v2-sys-color-on-surface-variant); margin-top: var(--sp-base); }
.band { border-top: 2px solid var(--ngn-v2-sys-color-on-surface); padding-block: var(--sp-medium) 0; margin-top: var(--sp-base); }
.band .section-label { margin-bottom: var(--sp-medium); }
.band-grid { display: grid; grid-template-columns: 1fr; gap: var(--sp-medium); }
@media (width >= 600px) { .band-grid { grid-template-columns: repeat(2, 1fr); } }
@media (width >= 840px) { .band-grid { grid-template-columns: repeat(4, 1fr); } }
.band-grid .headline { font-size: 17px !important; }
.band-grid .blurb { display: none; }
.story--thumb { display: grid; grid-template-columns: 1fr 96px; gap: var(--sp-small); }
.story--thumb .media-frame img { aspect-ratio: 1 / 1; }
'''


def broadsheet():
    lead, sec1, sec2 = S[5], S[8], S[12]
    rail = S[13:18]
    most = S[0:5]
    band = S[18:22] + S[6:8]
    body = f'''
<div class="wrapper wrapper--wide">
  <header class="cat-head">
    <h1>University News</h1>
    <p class="dek">The latest from Northeastern&rsquo;s global campus network &mdash; academics, research, athletics and student life.</p>
  </header>
  <nav class="topic-line" aria-label="University News topics">
    {"".join(f'<a href="#">{t}</a>' for t in TOPICS)}
  </nav>
  <div class="package">
    <div class="rail">
      <div class="rail-label">Latest</div>
      {"".join(card(s, mode="text", blurb=False, byline=False, headline_px=17) for s in rail)}
    </div>
    <div class="lead">
      {card(lead, mode="stacked", kicker="The Big Story", headline_px=32, ratio="16 / 9")}
      <div class="lead-secondary">
        {card(sec1, mode="stacked", blurb=False, headline_px=19)}
        {card(sec2, mode="stacked", blurb=False, headline_px=19)}
      </div>
    </div>
    <div class="rail">
      <div class="rail-label">Most read</div>
      <div class="most-read">
        {"".join(card(s, mode="text", blurb=False, byline=False, date=False, headline_px=16) for s in most)}
      </div>
      {photo_module(PHOTOS, 2)}
    </div>
  </div>
  <section class="band">
    <div class="section-label">More University News <a href="#">View all &rarr;</a></div>
    <div class="band-grid">
      {"".join(card(s, mode="stacked", blurb=False, headline_px=17) for s in band[:4])}
    </div>
  </section>
  <div class="load-more"><button>Load more stories</button></div>
</div>'''
    return page("The Broadsheet", BROADSHEET_CSS, body)


# ======================================================================
# 02 — The Section Front (NYT World)
# ======================================================================

SECTION_CSS = '''
.cat-head { max-width: 840px; margin-inline: auto; padding: var(--sp-xl) 16px var(--sp-medium); text-align: left; }
.cat-head h1 { font-family: var(--font-serif-display); font-size: clamp(40px, 10vw, 64px); font-weight: 700; letter-spacing: -1px; line-height: 1.05; }
.cat-head .dek { font-family: var(--font-serif); font-size: 19.3px; color: var(--ngn-v2-sys-color-on-surface-variant); margin-top: var(--sp-small); max-width: 620px; }
.topic-chips { display: flex; flex-wrap: wrap; gap: var(--sp-base); margin-top: var(--sp-medium); }
.topic-chips a { border: 1px solid var(--ngn-v2-sys-color-outline-variant); border-radius: var(--shape-full); padding: 6px 16px; font-size: 13.6px; font-weight: 700; }
.topic-chips a:hover { background: var(--ngn-v2-sys-color-surface-container); }
.river { max-width: 840px; margin-inline: auto; padding-inline: 16px; }
.hero { border-top: 1px solid var(--ngn-v2-sys-color-on-surface); padding-block: var(--sp-large); }
.hero .story--rich { display: grid; grid-template-columns: 1fr; gap: var(--sp-medium); }
@media (width >= 600px) { .hero .story--rich { grid-template-columns: 5fr 7fr; } }
.hero .headline { font-size: 34px !important; }
.hero .blurb { margin-top: var(--sp-small); font-size: 17px; }
.hero .post-meta { margin-top: var(--sp-small); }
.river .story.is-mode-rich + .story.is-mode-rich { border-top: 1px solid var(--ngn-v2-sys-color-outline-variant); }
.river > .story.is-mode-rich { padding-block: var(--sp-medium); }
.river > .story .story--rich { display: grid; grid-template-columns: 1fr; gap: var(--sp-medium); align-items: start; }
@media (width >= 600px) { .river > .story .story--rich { grid-template-columns: 8fr 4fr; } }
.river .blurb { margin-top: var(--sp-base); }
.river .post-meta { margin-top: var(--sp-base); }
.photo-module { background: var(--ngn-v2-sys-color-surface-container-low); border-block: 1px solid var(--ngn-v2-sys-color-outline-variant); padding: var(--sp-medium) var(--sp-compact); margin-block: var(--sp-medium); }
.photo-module__head { display: flex; align-items: center; gap: var(--sp-base); font-size: 12px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: var(--sp-compact); }
.photo-module__head svg { width: 18px; height: 18px; color: var(--ngn-v2-sys-color-primary); }
.photo-module__more { margin-left: auto; color: var(--ngn-v2-sys-color-primary); font-weight: 700; text-transform: none; }
.photo-module__items { display: grid; gap: var(--sp-compact); }
@media (width >= 600px) { .photo-module__items { grid-template-columns: repeat(3, 1fr); } }
.photo-module__caption { font-size: 12px; line-height: 1.45; color: var(--ngn-v2-sys-color-on-surface-variant); margin-top: var(--sp-base); }
'''


def section_front():
    hero = S[9]
    river = S[10:14] + S[2:5] + S[15:18]
    river_cards = ""
    for i, s in enumerate(river):
        river_cards += card(s, mode="rich", headline_px=24, byline=True)
        if i == 3:
            river_cards += photo_module(PHOTOS, 3)
    body = f'''
<header class="cat-head">
  <h1>University News</h1>
  <p class="dek">The latest from Northeastern&rsquo;s global campus network &mdash; academics, research, athletics and student life.</p>
  <nav class="topic-chips" aria-label="University News topics">
    {"".join(f'<a href="#">{t}</a>' for t in TOPICS)}
  </nav>
</header>
<div class="river">
  <section class="hero">{card(hero, mode="rich", kicker="Featured", headline_px=34, ratio="3 / 2")}</section>
  {river_cards}
  <div class="load-more"><button>More stories</button></div>
</div>'''
    return page("The Section Front", SECTION_CSS, body)


# ======================================================================
# 03 — The Mosaic (Time)
# ======================================================================

MOSAIC_CSS = '''
.cat-head { background: var(--ngn-v2-sys-color-primary); color: var(--ngn-v2-sys-color-on-primary); }
.cat-head .wrapper { display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--sp-compact) var(--sp-large); padding-block: var(--sp-medium); }
.cat-head h1 { font-family: var(--font-serif-display); font-size: 40px; font-weight: 700; letter-spacing: -0.5px; }
.cat-head .dek { font-size: 15px; opacity: 0.9; }
.topic-pills { display: flex; flex-wrap: wrap; gap: var(--sp-base); padding-block: var(--sp-compact); }
.topic-pills a { background: var(--ngn-v2-sys-color-surface-container); border-radius: var(--shape-full); padding: 8px 18px; font-size: 13.6px; font-weight: 700; }
.topic-pills a:hover { background: var(--ngn-v2-sys-color-primary); color: var(--ngn-v2-sys-color-on-primary); }
.mosaic { display: grid; gap: var(--sp-compact); padding-block: var(--sp-compact) var(--sp-large); grid-template-columns: 1fr; }
@media (width >= 840px) { .mosaic { grid-template-columns: 2fr 1fr 1fr; grid-template-rows: 1fr 1fr; } .mosaic .overlay-card:first-child { grid-row: span 2; } }
.overlay-card { position: relative; display: block; overflow: hidden; min-height: 240px; }
.overlay-card img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.overlay-card::after { content: ""; position: absolute; inset: 0; background: linear-gradient(to top, rgb(0 0 0 / 78%) 0%, rgb(0 0 0 / 25%) 55%, transparent 100%); }
.overlay-card .story__text { position: absolute; inset: auto 0 0 0; z-index: 1; padding: var(--sp-compact); color: #fff; }
.overlay-card .kicker { color: #f8bc54; }
.overlay-card .headline { color: #fff; font-size: 19px; }
.overlay-card:first-child .headline { font-size: 32px; }
.overlay-card:first-child { min-height: 420px; }
.overlay-card .post-meta { color: rgb(255 255 255 / 75%); margin-top: var(--sp-micro); }
.feature-band { background: var(--ngn-v2-sys-color-inverse-surface); color: var(--ngn-v2-sys-color-inverse-on-surface); padding-block: var(--sp-large); margin-block: var(--sp-large); }
.feature-band .section-label { color: #fff; margin-bottom: var(--sp-medium); }
.feature-band .section-label a { color: #f8bc54; }
.feature-band .headline { color: #fff; }
.feature-band .post-meta, .feature-band .blurb { color: rgb(255 255 255 / 70%); }
.feature-band .band-scroll { display: grid; grid-auto-flow: column; grid-auto-columns: 78%; gap: var(--sp-compact); overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: var(--sp-base); }
@media (width >= 600px) { .feature-band .band-scroll { grid-auto-columns: 31%; } }
.feature-band .band-scroll > * { scroll-snap-align: start; }
.feature-band .headline { font-size: 18px !important; margin-top: var(--sp-small); }
.grid-section { padding-block: var(--sp-base); }
.grid-section .section-label { margin-bottom: var(--sp-medium); }
.card-grid { display: grid; grid-template-columns: 1fr; gap: var(--sp-medium); }
@media (width >= 600px) { .card-grid { grid-template-columns: repeat(2, 1fr); } }
@media (width >= 840px) { .card-grid { grid-template-columns: repeat(3, 1fr); } }
.card-grid .headline { margin-top: var(--sp-small); font-size: 19px !important; }
.card-grid .post-meta { margin-top: var(--sp-micro); }
.card-grid .blurb { display: none; }
.photo-module { padding-block: var(--sp-medium); }
.photo-module__head { display: flex; align-items: center; gap: var(--sp-base); font-size: 15px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: var(--sp-medium); }
.photo-module__head svg { width: 20px; height: 20px; color: var(--ngn-v2-sys-color-primary); }
.photo-module__more { margin-left: auto; color: var(--ngn-v2-sys-color-primary); font-weight: 700; text-transform: none; }
.photo-module__items { display: grid; grid-auto-flow: column; grid-auto-columns: 72%; gap: var(--sp-compact); overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: var(--sp-base); }
@media (width >= 600px) { .photo-module__items { grid-auto-columns: 31%; } }
.photo-module__items > * { scroll-snap-align: start; }
.photo-module__caption { font-size: 12px; line-height: 1.45; color: var(--ngn-v2-sys-color-on-surface-variant); margin-top: var(--sp-base); }
'''


def mosaic():
    heroes = [S[9], S[1], S[17], S[13], S[19]]
    def overlay(s, kicker=None):
        k = f'<div class="kicker">{kicker}</div>' if kicker else ""
        return (f'<a class="overlay-card" href="{s["link"]}"><img src="{s["img"]}" alt="" loading="lazy">'
                f'<div class="story__text">{k}<h3 class="headline">{s["title"]}</h3>'
                f'{meta(s, date=False)}</div></a>')
    band = S[2:6]
    grid = S[10:16]
    body = f'''
<header class="cat-head">
  <div class="wrapper wrapper--wide"><h1>University News</h1>
  <p class="dek">Academics, research, athletics and student life across the global campus network.</p></div>
</header>
<div class="wrapper wrapper--wide">
  <nav class="topic-pills" aria-label="University News topics">
    {"".join(f'<a href="#">{t}</a>' for t in TOPICS)}
  </nav>
  <section class="mosaic">
    {overlay(heroes[0], kicker="Featured")}
    {"".join(overlay(s) for s in heroes[1:])}
  </section>
</div>
<section class="feature-band">
  <div class="wrapper wrapper--wide">
    <div class="section-label">Spotlight: Research <a href="#">More research &rarr;</a></div>
    <div class="band-scroll">
      {"".join(card(s, mode="stacked", blurb=False, headline_px=18) for s in band)}
    </div>
  </div>
</section>
<div class="wrapper wrapper--wide">
  <section class="grid-section">
    <div class="section-label">The Latest <a href="#">View all &rarr;</a></div>
    <div class="card-grid">
      {"".join(card(s, mode="stacked", blurb=False, headline_px=19) for s in grid)}
    </div>
  </section>
  {photo_module(PHOTOS, 4, horizontal=True)}
  <div class="load-more"><button>Load more stories</button></div>
</div>'''
    return page("The Mosaic", MOSAIC_CSS, body)


# ======================================================================
# 04 — The Index (WaPo Politics)
# ======================================================================

INDEX_CSS = '''
.index-shell { display: grid; grid-template-columns: 1fr; gap: var(--sp-xl); padding-block: var(--sp-large); }
@media (width >= 840px) { .index-shell { grid-template-columns: 300px 1fr; } }
.identity { align-self: start; }
@media (width >= 840px) { .identity { position: sticky; top: var(--sp-medium); } }
.identity h1 { font-family: var(--font-serif-display); font-size: 44px; font-weight: 700; letter-spacing: -1px; line-height: 1.05; }
.identity .dek { font-family: var(--font-serif); font-size: 16px; color: var(--ngn-v2-sys-color-on-surface-variant); margin-top: var(--sp-small); }
.identity .rule { width: 48px; height: 3px; background: var(--ngn-v2-sys-color-primary); margin-block: var(--sp-compact); }
.identity-topics { display: flex; flex-direction: column; }
.identity-topics a { font-size: 14px; font-weight: 700; padding-block: 10px; border-bottom: 1px solid var(--ngn-v2-sys-color-outline-variant); display: flex; justify-content: space-between; }
.identity-topics a::after { content: "\\2192"; color: var(--ngn-v2-sys-color-outline); }
.identity-topics a:hover { color: var(--ngn-v2-sys-color-primary); }
.identity .newsletter { margin-top: var(--sp-medium); background: var(--ngn-v2-sys-color-surface-container); border-radius: var(--shape-md); padding: var(--sp-compact); font-size: 13.6px; }
.identity .newsletter strong { font-size: 15px; display: block; margin-bottom: 4px; }
.identity .newsletter button { margin-top: var(--sp-small); border: 0; background: var(--ngn-v2-sys-color-primary); color: #fff; font-weight: 700; font-size: 13px; padding: 8px 20px; border-radius: var(--shape-full); cursor: pointer; }
.day-group + .day-group { margin-top: var(--sp-large); }
.day-label { font-size: 12px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; color: var(--ngn-v2-sys-color-on-surface-variant); padding-bottom: var(--sp-small); border-bottom: 2px solid var(--ngn-v2-sys-color-on-surface); }
.day-group .story { padding-block: var(--sp-compact); border-bottom: 1px solid var(--ngn-v2-sys-color-outline-variant); }
.story--thumb { display: grid; grid-template-columns: 1fr 132px; gap: var(--sp-compact); align-items: start; }
.story--thumb .media-frame img { aspect-ratio: 3 / 2; }
.story--thumb .blurb { margin-top: 6px; font-size: 15px; }
.story--thumb .post-meta { margin-top: 6px; }
.day-photo { display: grid; grid-template-columns: 1fr; gap: var(--sp-compact); background: var(--ngn-v2-sys-color-surface-container-low); border: 1px solid var(--ngn-v2-sys-color-outline-variant); border-radius: var(--shape-md); padding: var(--sp-compact); margin-top: var(--sp-compact); }
@media (width >= 600px) { .day-photo { grid-template-columns: 180px 1fr; align-items: center; } }
.day-photo__label { display: flex; align-items: center; gap: var(--sp-base); font-size: 11px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; color: var(--ngn-v2-sys-color-primary); margin-bottom: 6px; }
.day-photo__label svg { width: 16px; height: 16px; }
.day-photo .headline { font-size: 17px; }
.day-photo .photo-caption { font-size: 13px; color: var(--ngn-v2-sys-color-on-surface-variant); margin-top: 4px; }
'''


def index_page():
    groups = [
        ("Today", S[0:3], PHOTOS[0]),
        ("Yesterday", S[3:6], PHOTOS[1]),
        ("This week", S[6:12], PHOTOS[2]),
        ("Earlier", S[12:18], None),
    ]
    rows = ""
    for label, stories, photo in groups:
        cards = "".join(card(s, mode="thumb", headline_px=19) for s in stories)
        pm = ""
        if photo:
            pm = (f'<a class="day-photo" href="{photo["link"]}">'
                  f'<div class="media-frame"><img src="{photo["img"]}" alt="" loading="lazy"></div>'
                  f'<div><div class="day-photo__label">{ICON_CAMERA} Photo of the day</div>'
                  f'<h3 class="headline">{photo["title"]}</h3>'
                  f'<p class="photo-caption">{photo["dek"][:120]}&hellip;</p></div></a>')
        rows += f'<section class="day-group"><div class="day-label">{label}</div>{cards}{pm}</section>'
    body = f'''
<div class="wrapper wrapper--wide index-shell">
  <aside class="identity">
    <h1>University News</h1>
    <div class="rule"></div>
    <p class="dek">Academics, research, athletics and student life across Northeastern&rsquo;s global campus network.</p>
    <nav class="identity-topics" aria-label="University News topics">
      {"".join(f'<a href="#">{t}</a>' for t in TOPICS)}
    </nav>
    <div class="newsletter"><strong>NGN in your inbox</strong>
      The day&rsquo;s top stories from Northeastern, every weekday morning.
      <button>Sign up</button></div>
  </aside>
  <div class="river">
    {rows}
    <div class="load-more"><button>Load more stories</button></div>
  </div>
</div>'''
    return page("The Index", INDEX_CSS, body, sticky_bar=True)


# ======================================================================
# 05 — The Athletic (NYT Athletic)
# ======================================================================

ATHLETIC_CSS = '''
.topic-bar { position: sticky; top: 64px; z-index: 90; background: var(--ngn-v2-sys-color-surface); border-bottom: 1px solid var(--ngn-v2-sys-color-outline-variant); }
.topic-bar__inner { display: flex; gap: var(--sp-micro); overflow-x: auto; padding-block: var(--sp-small); scrollbar-width: none; align-items: center; }
.topic-bar__inner::-webkit-scrollbar { display: none; }
.topic-bar h1 { font-family: var(--font-serif-display); font-size: 20px; font-weight: 700; padding-right: var(--sp-compact); margin-right: var(--sp-base); border-right: 1px solid var(--ngn-v2-sys-color-outline-variant); white-space: nowrap; }
.topic-bar a { white-space: nowrap; font-size: 13.6px; font-weight: 700; padding: 6px 14px; border-radius: var(--shape-full); }
.topic-bar a.is-active { background: var(--ngn-v2-sys-color-inverse-surface); color: var(--ngn-v2-sys-color-inverse-on-surface); }
.topic-bar a:not(.is-active):hover { background: var(--ngn-v2-sys-color-surface-container); }
.lead-package { display: grid; grid-template-columns: 1fr; gap: var(--sp-medium); padding-block: var(--sp-large); }
@media (width >= 840px) { .lead-package { grid-template-columns: 2fr 1fr; } }
.lead-main .headline { font-size: 34px; margin-top: var(--sp-compact); }
.lead-main .blurb { margin-top: var(--sp-base); font-size: 17px; }
.lead-main .post-meta { margin-top: var(--sp-base); }
.lead-side { display: flex; flex-direction: column; gap: var(--sp-medium); }
.lead-side .headline { font-size: 19px !important; margin-top: var(--sp-small); }
.lead-side .blurb { display: none; }
.grid-section { padding-block: var(--sp-medium); }
.grid-section .section-label { margin-bottom: var(--sp-medium); font-size: 19px; text-transform: none; letter-spacing: 0; }
.grid-section .section-label a { font-size: 13.6px; }
.card-grid { display: grid; grid-template-columns: 1fr; gap: var(--sp-medium); }
@media (width >= 600px) { .card-grid { grid-template-columns: repeat(2, 1fr); } }
@media (width >= 840px) { .card-grid { grid-template-columns: repeat(4, 1fr); } }
.card-grid .story > a { display: block; background: var(--ngn-v2-sys-color-surface); }
.card-grid .headline { font-size: 17px !important; margin-top: var(--sp-small); }
.card-grid .post-meta { margin-top: var(--sp-micro); }
.card-grid .blurb { display: none; }
.photo-module { background: var(--ngn-v2-sys-color-surface-container-low); border-radius: var(--shape-lg); padding: var(--sp-medium); margin-block: var(--sp-medium); }
.photo-module__head { display: flex; align-items: center; gap: var(--sp-base); font-family: var(--font-serif-display); font-size: 19px; font-weight: 700; margin-bottom: var(--sp-medium); }
.photo-module__head svg { width: 20px; height: 20px; color: var(--ngn-v2-sys-color-primary); }
.photo-module__more { margin-left: auto; font-family: var(--font-sans); font-size: 13.6px; font-weight: 700; color: var(--ngn-v2-sys-color-primary); }
.photo-module__items { display: grid; grid-auto-flow: column; grid-auto-columns: 72%; gap: var(--sp-compact); overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: var(--sp-base); }
@media (width >= 600px) { .photo-module__items { grid-auto-columns: 30%; } }
.photo-module__items > * { scroll-snap-align: start; }
.photo-module__caption { font-size: 12px; line-height: 1.45; color: var(--ngn-v2-sys-color-on-surface-variant); margin-top: var(--sp-base); }
'''


def athletic():
    lead = S[3]
    side = [S[7], S[11]]
    latest = S[0:2] + S[12:14]
    commencement = S[17:21]
    body = f'''
<nav class="topic-bar" aria-label="University News topics">
  <div class="wrapper wrapper--wide topic-bar__inner">
    <h1>University News</h1>
    <a href="#" class="is-active">Top Stories</a>
    {"".join(f'<a href="#">{t}</a>' for t in TOPICS)}
  </div>
</nav>
<div class="wrapper wrapper--wide">
  <section class="lead-package">
    <div class="lead-main">{card(lead, mode="stacked", kicker="Top story", headline_px=34, ratio="16 / 9")}</div>
    <div class="lead-side">
      {"".join(card(s, mode="stacked", blurb=False, headline_px=19) for s in side)}
    </div>
  </section>
  <section class="grid-section">
    <div class="section-label">The Latest <a href="#">See all &rarr;</a></div>
    <div class="card-grid">{"".join(card(s, mode="stacked", blurb=False) for s in latest)}</div>
  </section>
  {photo_module(PHOTOS, 4, horizontal=True)}
  <section class="grid-section">
    <div class="section-label">Athletics &amp; Campus <a href="#">See all &rarr;</a></div>
    <div class="card-grid">{"".join(card(s, mode="stacked", blurb=False) for s in commencement)}</div>
  </section>
  <div class="load-more"><button>Load more stories</button></div>
</div>'''
    return page("The Athletic", ATHLETIC_CSS, body, sticky_bar=True)


# ======================================================================
# 06 — The Composite (WaPo header + Time featured + NYT river +
#      full-bleed Seen Around slider + 4-column stack)
# ======================================================================

COMPOSITE_CSS = '''
/* typography: match the live homepage's v3 headlines —
   kepler-std condensed at weight medium */
.headline { font-family: var(--font-serif-condensed); font-weight: 500; letter-spacing: 0; line-height: 1.1; }

.cat-head { padding-block: var(--sp-medium) var(--sp-micro); text-align: center; }
.cat-head h1 { font-family: var(--h1-font, var(--font-display-condensed)); font-size: clamp(36px, 5vw, 48px); font-weight: var(--h1-weight, 400); letter-spacing: 0; line-height: 1.2; }

/* combined category bar: small heading left, topic links right */
.cat-bar { position: sticky; top: 63px; z-index: 90; background: var(--ngn-v2-sys-color-surface); border-bottom: 1px solid var(--ngn-v2-sys-color-outline-variant); }
.cat-bar__inner { display: flex; align-items: baseline; justify-content: space-between; gap: var(--sp-base) var(--sp-large); padding-block: var(--sp-compact); flex-wrap: wrap; }
.cat-bar h1 { font-family: var(--h1-font, var(--font-display-condensed)); font-weight: var(--h1-weight, 400); font-size: 28px; line-height: 1.1; letter-spacing: 0; }
.cat-bar__links { display: flex; flex-wrap: wrap; gap: var(--sp-base) var(--sp-medium); font-size: 15px; font-weight: 500; }
.cat-bar__links a:hover { text-decoration: underline; text-underline-offset: 4px; }

/* prototype-only H1 font switcher */
.proto-font-tool { position: fixed; bottom: 16px; right: 16px; z-index: 300; display: flex; gap: 10px; align-items: center; background: var(--ngn-v2-sys-color-inverse-surface); color: var(--ngn-v2-sys-color-inverse-on-surface); padding: 10px 14px; border-radius: var(--shape-sm); font-size: 12px; font-weight: 700; box-shadow: 0 4px 16px rgb(0 0 0 / 30%); }
.proto-font-tool label { display: flex; gap: 6px; align-items: center; }
.proto-font-tool select { font: 12px var(--font-sans); border-radius: var(--shape-xs); border: 0; padding: 4px 6px; }
.topic-line { display: flex; flex-wrap: wrap; justify-content: center; gap: var(--sp-base) var(--sp-large); padding-block: var(--sp-compact); border-bottom: 1px solid var(--ngn-v2-sys-color-outline-variant); font-size: 15px; font-weight: 500; }
.topic-line a:hover { text-decoration: underline; text-underline-offset: 4px; }

/* Time-inspired featured trio */
.featured-band { padding-block: var(--sp-xl); }
.featured-trio { display: grid; grid-template-columns: 1fr; gap: var(--sp-large); align-items: start; }
@media (width >= 840px) { .featured-trio { grid-template-columns: 1fr 2fr 1fr; } }
.featured-trio .story--center { text-align: center; }
@media (width >= 840px) { .featured-trio .story--center { order: 0; } .featured-trio .story--left { order: -1; } }
.featured-trio .story--center .headline { font-size: clamp(28px, 3vw, 40px); margin-top: var(--sp-compact); line-height: 1.1; }
.featured-trio .story--side .headline { font-size: 24px; margin-top: var(--sp-small); }
.featured-trio .post-meta { margin-top: var(--sp-base); font-size: 13.6px; }
.featured-trio .story--side .media-frame img { aspect-ratio: 4 / 3; }
@media (width >= 840px) { .featured-trio .story--side { padding-top: var(--sp-large); } }

/* sticky appbar: the bar's is-sticky needs a parent that spans the page,
   so pin the site-header wrapper itself */
.site-header { position: sticky; top: 0; z-index: 100; }

/* sticky topic subnav (below the sticky appbar) */
.topic-nav { position: sticky; top: 63px; z-index: 90; background: var(--ngn-v2-sys-color-surface); border-bottom: 1px solid var(--ngn-v2-sys-color-outline-variant); }
.topic-nav .topic-line { border-bottom: 0; }

/* scroll-condense logo: wordmark letters collapse into the NGN monogram */
.ngn-wordmark--anim path,
.ngn-wordmark--anim polygon { transition: opacity 0.35s ease, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); }
.app-bar__logo--desktop svg { transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); }
/* condensed targets derived from the NGN monogram asset: uniform 15.56u
   gaps at 102u letter height → 11.3u at the wordmark's 72u letters;
   arrow at half letter height, top-aligned */
.ngn-bar.is-condensed .app-bar__logo--desktop svg { transform: translateX(147px); }
.ngn-bar.is-condensed .wm-fade { opacity: 0; }
.ngn-bar.is-condensed .wm-w2,
.ngn-bar.is-condensed .wm-k1 { transform: translateX(-543px); }
.ngn-bar.is-condensed .wm-w3,
.ngn-bar.is-condensed .wm-k2 { transform: translateX(-777px); }
.ngn-bar.is-condensed .wm-w1 { transform: translateX(-80px); }
.ngn-wordmark--anim .wm-arrow { transform-box: fill-box; transform-origin: 0 0; }
.ngn-bar.is-condensed .wm-arrow { transform: translate(-972px, 0) scale(0.5); }
@media (prefers-reduced-motion: reduce) {
	.ngn-wordmark--anim path, .ngn-wordmark--anim polygon, .app-bar__logo--desktop svg { transition: none; }
}

/* NYT-inspired river + sticky newsletter rail */
.latest-shell { display: grid; grid-template-columns: 1fr; gap: var(--sp-xl); align-items: start; }
@media (width >= 840px) { .latest-shell { grid-template-columns: 2fr 1fr; } }
.river { min-width: 0; }
.river-label { font-size: 12px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; padding-block: var(--sp-large) var(--sp-small); border-bottom: 2px solid var(--ngn-v2-sys-color-on-surface); margin-top: var(--sp-base); }
.river > .story.is-mode-rich { padding-block: var(--sp-medium); }
.river .story.is-mode-rich + .story.is-mode-rich { border-top: 1px solid var(--ngn-v2-sys-color-outline-variant); }
.river > .story .story--rich { display: grid; grid-template-columns: 1fr; gap: var(--sp-medium); align-items: start; }
@media (width >= 600px) { .river > .story .story--rich { grid-template-columns: 8fr 4fr; } }
.river .blurb { margin-top: var(--sp-base); }
.river .post-meta { margin-top: var(--sp-base); }

/* interest-capture newsletter signup, sticky beside the river */
.newsletter-rail { position: sticky; top: 140px; margin-top: calc(var(--sp-large) + 34px); }
.newsletter-panel { background: var(--ngn-v2-sys-color-surface-container); border-radius: var(--shape-md); padding: var(--sp-medium); }
.newsletter-panel h2 { font-family: var(--font-serif-condensed); font-size: 23px; font-weight: 500; line-height: 1.15; }
.newsletter-panel .dek { font-size: 13.6px; color: var(--ngn-v2-sys-color-on-surface-variant); margin-top: var(--sp-base); }
.newsletter-panel fieldset { border: 0; margin: var(--sp-compact) 0 0; padding: 0; }
.newsletter-panel legend { font-size: 12px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; padding: 0; margin-bottom: var(--sp-small); }
.newsletter-panel .interests { display: flex; flex-wrap: wrap; gap: var(--sp-base); }
.newsletter-panel .interests label { display: inline-flex; align-items: center; gap: 6px; border: 1px solid var(--ngn-v2-sys-color-outline-variant); border-radius: var(--shape-full); padding: 6px 14px; font-size: 13px; font-weight: 700; cursor: pointer; background: var(--ngn-v2-sys-color-surface); }
.newsletter-panel .interests label:has(input:checked) { background: var(--ngn-v2-sys-color-inverse-surface); color: var(--ngn-v2-sys-color-inverse-on-surface); border-color: var(--ngn-v2-sys-color-inverse-surface); }
.newsletter-panel .interests input { appearance: none; margin: 0; }
.newsletter-panel .interests label:has(input:checked)::before { content: "\\2713"; font-size: 11px; }
.newsletter-panel .email-row { display: flex; gap: var(--sp-base); margin-top: var(--sp-compact); }
.newsletter-panel input[type="email"] { flex: 1; min-width: 0; border: 1px solid var(--ngn-v2-sys-color-outline); border-radius: var(--shape-full); padding: 10px 16px; font: 14px var(--font-sans); background: var(--ngn-v2-sys-color-surface); }
.newsletter-panel button { border: 0; background: var(--ngn-v2-sys-color-primary); color: var(--ngn-v2-sys-color-on-primary); font-weight: 700; font-size: 13.6px; padding: 10px 20px; border-radius: var(--shape-full); cursor: pointer; }
/* sans-serif deks under headlines */
.blurb { font-family: var(--font-sans); font-size: 15px; }

/* closing topic groups — 4 stories per curated tag */
.topic-group { padding-block: var(--sp-xl) 0; }
.topic-group .section-label { padding-bottom: var(--sp-small); border-bottom: 2px solid var(--ngn-v2-sys-color-on-surface); margin-bottom: var(--sp-medium); text-transform: none; font-size: 19px; letter-spacing: 0; }
.topic-group .more-btn { margin-left: auto; font-size: 12px; font-weight: 700; letter-spacing: 0.4px; color: var(--ngn-v2-sys-color-primary); white-space: nowrap; }
.topic-group .more-btn:hover { text-decoration: underline; text-underline-offset: 3px; }
.band-grid { display: grid; grid-template-columns: 1fr; gap: var(--sp-large) var(--sp-medium); }
@media (width >= 600px) { .band-grid { grid-template-columns: repeat(2, 1fr); } }
@media (width >= 840px) { .band-grid { grid-template-columns: repeat(4, 1fr); } }
.band-grid .headline { font-size: 20px !important; margin-top: var(--sp-small); }
.band-grid .blurb { display: none; }
.band-grid .post-meta { margin-top: var(--sp-micro); }
'''


def find(kw):
    return next(s for s in S if kw.lower() in s["title"].lower())


def with_when(s, staged_iso=None):
    return {**s, "_when": fmt_when(staged_iso or s["date"] + "T00:00")}


def composite_page(title, featured_html, featured_links, extra_css="",
                   combined_header=False, archive=False, font_switcher=False):
    """Shared composite shell: header, sticky topic nav, the given featured
    section, river + newsletter, topic groups, logo-condense script.

    combined_header — one row: small H1 left, topic links right.
    archive         — 4-column recent-stories grid ahead of the footer.
    font_switcher   — prototype-only floating control to swap the H1 font.
    """
    # curated by title keyword so a content re-fetch can't reshuffle the page
    river = [find("phone behind"), find("world cup"), find("fastest drones"),
             find("physical therapy meets"), find("iphone going to go up"),
             find("living laboratory")]

    # staged publish times for some river stories so the relative-date
    # treatment is visible (None = the story's real date; world cup's real
    # date already lands in the relative window)
    staged = ["2026-07-21T09:30", None, "2026-07-20T16:00",
              "2026-07-19T10:00", None, None]
    river = [with_when(s, t) for s, t in zip(river, staged)]

    # topic groups: 4 most recent per tag, deduped against the page above
    # and across groups
    seen_links = {s["link"] for s in river} | set(featured_links)
    groups = []
    for t in CONTENT["topics"]:
        stories = [s for s in t["stories"] if s["link"] not in seen_links][:4]
        seen_links.update(s["link"] for s in stories)
        groups.append({**t, "stories": [with_when(s) for s in stories]})

    interests = ["University News", "Science & Tech", "Health", "Sports"]
    newsletter = f'''
    <aside class="newsletter-rail">
      <form class="newsletter-panel" action="#" method="post">
        <h2>NGN in your inbox</h2>
        <p class="dek">The day&rsquo;s top stories from Northeastern, every weekday morning &mdash; tuned to what you care about.</p>
        <fieldset>
          <legend>I&rsquo;m interested in</legend>
          <div class="interests">
            {"".join(f'<label><input type="checkbox" name="interest" value="{i}"{" checked" if n == 0 else ""}>{i}</label>' for n, i in enumerate(interests))}
          </div>
        </fieldset>
        <div class="email-row">
          <input type="email" placeholder="Email address" aria-label="Email address" required>
          <button type="submit">Sign up</button>
        </div>
      </form>
    </aside>'''

    topic_sections = "".join(f'''
  <section class="topic-group">
    <div class="section-label">{g["label"]}
      <a class="more-btn" href="https://news.northeastern.edu/tag/{g["slug"]}/">More {g["label"]} stories &rarr;</a></div>
    <div class="band-grid">
      {"".join(card(s, mode="stacked", blurb=False, byline=False, headline_px=17) for s in g["stories"])}
    </div>
  </section>''' for g in groups)

    topic_links = "".join(f'<a href="#">{t}</a>' for t in TOPICS)
    if combined_header:
        head_html = f'''
<nav class="cat-bar" aria-label="University News topics">
  <div class="wrapper wrapper--wide cat-bar__inner">
    <h1>University News</h1>
    <div class="cat-bar__links">{topic_links}</div>
  </div>
</nav>'''
    else:
        head_html = f'''
<div class="wrapper wrapper--wide">
  <header class="cat-head"><h1>University News</h1></header>
</div>
<nav class="topic-nav" aria-label="University News topics">
  <div class="wrapper wrapper--wide topic-line">{topic_links}</div>
</nav>'''

    archive_html = ""
    if archive:
        remaining = sorted((s for s in S if s["link"] not in seen_links),
                           key=lambda s: s["date"], reverse=True)[:12]
        archive_html = f'''
  <section class="topic-group">
    <div class="section-label">All University News
      <a class="more-btn" href="#">Browse the archive &rarr;</a></div>
    <div class="band-grid">
      {"".join(card(with_when(s), mode="stacked", blurb=False, byline=False) for s in remaining)}
    </div>
  </section>
  <div class="load-more"><button>Load more stories</button></div>'''

    switcher_html = ""
    if font_switcher:
        fonts = [
            ("kepler-std-condensed-subhead", "Kepler Std Condensed Subhead"),
            ("kepler-std-condensed-display", "Kepler Std Condensed Display"),
            ("kepler-std-display", "Kepler Std Display"),
            ("kepler-std", "Kepler Std"),
            ("lato", "Lato (sans)"),
        ]
        font_opts = "".join(
            f'<option value="{v}"{" selected" if i == 0 else ""}>{label}</option>'
            for i, (v, label) in enumerate(fonts))
        weight_opts = "".join(
            f'<option value="{w}"{" selected" if w == 500 else ""}>{w}</option>'
            for w in (300, 400, 500, 600, 700))
        switcher_html = f'''
<div class="proto-font-tool">
  <label>H1 font <select id="h1-font">{font_opts}</select></label>
  <label>Weight <select id="h1-weight">{weight_opts}</select></label>
</div>
<script>
(() => {{
  const font = document.getElementById('h1-font');
  const weight = document.getElementById('h1-weight');
  const apply = () => {{
    document.documentElement.style.setProperty('--h1-font', font.value + ", kepler-std, georgia, serif");
    document.documentElement.style.setProperty('--h1-weight', weight.value);
  }};
  font.addEventListener('change', apply);
  weight.addEventListener('change', apply);
  apply();
}})();
</script>'''

    body = f'''
{head_html}
{featured_html}
<div class="wrapper wrapper--wide latest-shell">
  <div class="river">
    <div class="river-label">The Latest</div>
    {"".join(card(s, mode="rich", byline=False, headline_px=24) for s in river)}
  </div>
  {newsletter}
</div>
<div class="wrapper wrapper--wide">
  {topic_sections}
  {archive_html}
</div>
{switcher_html}
<script>
/* Logo condense: wordmark collapses to the NGN monogram once scrolled */
(() => {{
  const bar = document.querySelector('.ngn-bar');
  addEventListener('scroll',
    () => bar.classList.toggle('is-condensed', scrollY > 120),
    {{ passive: true }});
}})();
</script>'''
    return page(title, COMPOSITE_CSS + extra_css, body, sticky_bar=True, anim_logo=True)


def composite():
    trio = [with_when(find(kw)) for kw in
            ("invasive plant", "tumor cancers", "pseudonyms")]

    def featured(s, pos):
        big = pos == "center"
        return (f'<article class="story story--{pos}{"" if big else " story--side"}">'
                f'<a href="{s["link"]}">'
                f'<div class="media-frame"><img src="{s["img"]}" alt="" loading="lazy"'
                f' style="aspect-ratio:{"3 / 2" if big else "4 / 3"}"></div>'
                f'<h3 class="headline">{s["title"]}</h3>'
                f'{meta(s, byline=False)}'
                f'</a></article>')

    featured_html = f'''
<section class="featured-band">
  <div class="wrapper wrapper--wide">
    <div class="featured-trio">
      {featured(trio[0], "center")}
      {featured(trio[1], "left")}
      {featured(trio[2], "right")}
    </div>
  </div>
</section>'''
    return composite_page("The Composite", featured_html,
                          [s["link"] for s in trio])


BI_FEATURED_CSS = '''
/* v2 featured package: dominant lead with overlapping headline box + rail */
.featured-bi { padding-block: var(--sp-medium) var(--sp-large); }
.featured-bi__grid { display: grid; grid-template-columns: 1fr; gap: var(--sp-large); align-items: start; }
@media (width >= 840px) { .featured-bi__grid { grid-template-columns: 2fr 1fr; } }
.featured-bi__lead { position: relative; }
.featured-bi__lead .media-frame img { aspect-ratio: 16 / 10; }
.featured-bi__lead .lead-box { position: static; background: var(--ngn-v2-sys-color-surface); padding: var(--sp-compact) 0 0; }
@media (width >= 840px) { .featured-bi__lead .lead-box { position: absolute; left: 0; bottom: 0; max-width: 78%; padding: var(--sp-medium) var(--sp-medium) 0 0; } }
.featured-bi__lead .headline { font-size: clamp(24px, 2.6vw, 34px); }
.featured-bi__lead .post-meta { margin-top: var(--sp-base); }
.featured-bi__rail .story + .story { border-top: 1px solid var(--ngn-v2-sys-color-outline-variant); margin-top: var(--sp-compact); padding-top: var(--sp-compact); }
.featured-bi__rail .story--top .headline { font-size: 21px; margin-top: var(--sp-small); }
.featured-bi__rail .story--thumb-row a { display: grid; grid-template-columns: 1fr 96px; gap: var(--sp-compact); align-items: start; }
.featured-bi__rail .story--thumb-row .headline { font-size: 20px; }
.featured-bi__rail .story--thumb-row .media-frame img { aspect-ratio: 4 / 3; }
.featured-bi__rail .post-meta { margin-top: 6px; }
'''


def bi_featured():
    """The BI-style featured package markup, shared by v2 and v3."""
    lead = with_when(find("invasive plant"))
    rail_top = with_when(find("tumor cancers"))
    thumbs = [with_when(find("pseudonyms")), with_when(find("smash bros"))]

    thumb_rows = "".join(
        f'<article class="story story--thumb-row"><a href="{s["link"]}">'
        f'<div class="story__text"><h3 class="headline">{s["title"]}</h3>'
        f'{meta(s, byline=False)}</div>'
        f'<div class="media-frame"><img src="{s["img"]}" alt="" loading="lazy"></div>'
        f'</a></article>'
        for s in thumbs)

    featured_html = f'''
<section class="featured-bi">
  <div class="wrapper wrapper--wide featured-bi__grid">
    <article class="story featured-bi__lead"><a href="{lead["link"]}">
      <div class="media-frame"><img src="{lead["img"]}" alt=""></div>
      <div class="lead-box"><h3 class="headline">{lead["title"]}</h3>
        {meta(lead, byline=False)}</div>
    </a></article>
    <div class="featured-bi__rail">
      <article class="story story--top"><a href="{rail_top["link"]}">
        <div class="media-frame"><img src="{rail_top["img"]}" alt=""></div>
        <h3 class="headline">{rail_top["title"]}</h3>
        {meta(rail_top, byline=False)}
      </a></article>
      {thumb_rows}
    </div>
  </div>
</section>'''
    return featured_html, [s["link"] for s in [lead, rail_top] + thumbs]


def composite_v2():
    featured_html, links = bi_featured()
    return composite_page("The Composite V2", featured_html, links,
                          extra_css=BI_FEATURED_CSS)


# v3: same package, but the lead headline sits below the image instead of
# in an overlapping box
BI_V3_CSS = BI_FEATURED_CSS + '''
@media (width >= 840px) {
	.featured-bi__lead .lead-box { position: static; max-width: none; padding: var(--sp-compact) 0 0; }
}
'''


def composite_v3():
    featured_html, links = bi_featured()
    return composite_page("The Composite V3", featured_html, links,
                          extra_css=BI_V3_CSS)


def composite_v4():
    featured_html, links = bi_featured()
    return composite_page("The Composite V4", featured_html, links,
                          extra_css=BI_V3_CSS, combined_header=True,
                          font_switcher=True)


def composite_v5():
    featured_html, links = bi_featured()
    return composite_page("The Composite V5", featured_html, links,
                          extra_css=BI_V3_CSS, combined_header=True,
                          archive=True, font_switcher=True)


PAGES = {
    "01-broadsheet.html": broadsheet,
    "02-section-front.html": section_front,
    "03-mosaic.html": mosaic,
    "04-index.html": index_page,
    "05-athletic.html": athletic,
    "06-composite.html": composite,
    "07-composite-v2.html": composite_v2,
    "08-composite-v3.html": composite_v3,
    "09-composite-v4.html": composite_v4,
    "10-composite-v5.html": composite_v5,
}

for name, fn in PAGES.items():
    (HERE / name).write_text(fn())
    print("wrote", name)
