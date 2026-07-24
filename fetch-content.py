#!/usr/bin/env python3
"""Pull real story content from news.northeastern.edu into content.json.

Prototype-only helper: grabs substantive stories across categories (presented
as if they were all University News) plus the 'seen around' photo features.
"""
import html
import json
import re
import urllib.request
import urllib.parse

BASE = "https://news.northeastern.edu/wp-json/wp/v2"


def get(path, **params):
    qs = urllib.parse.urlencode(params)
    url = f"{BASE}/{path}?{qs}"
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())


def strip_tags(markup):
    return html.unescape(re.sub(r"<[^>]+>", "", markup)).strip()


def img_of(post, size_pref=("large", "medium_large", "full")):
    med = (post.get("_embedded", {}).get("wp:featuredmedia") or [{}])[0] or {}
    sizes = med.get("media_details", {}).get("sizes", {})
    for s in size_pref:
        if s in sizes:
            return sizes[s]["source_url"]
    return med.get("source_url", "")


def author_of(post):
    a = (post.get("_embedded", {}).get("author") or [{}])[0] or {}
    return a.get("name", "")


def shape(post):
    return {
        "title": strip_tags(post["title"]["rendered"]),
        "dek": strip_tags(post["excerpt"]["rendered"])[:220],
        "byline": author_of(post),
        "date": post["date"][:10],
        "link": post["link"],
        "img": img_of(post),
    }


def fetch_category(slug_id, n, exclude_tags=None):
    params = dict(categories=slug_id, per_page=n, _embed="wp:featuredmedia,author")
    if exclude_tags:
        params["tags_exclude"] = exclude_tags
    return [shape(p) for p in get("posts", **params)]


seen_around = get("tags", slug="seen-around")[0]["id"]

out = {
    # substantive stories: university-news minus photo features, topped up
    # from other categories so layouts see realistic editorial variety
    "stories": [],
    "photos": [],
}

out["stories"] += fetch_category(7, 20, exclude_tags=seen_around)      # university news
out["stories"] += fetch_category(21443, 6)                              # research
out["stories"] += fetch_category(3, 5)                                  # science & tech
out["stories"] += fetch_category(612, 4)                                # health
out["stories"] += fetch_category(6, 4)                                  # society & culture
out["stories"] += fetch_category(8, 4)                                  # sports
out["stories"] += fetch_category(5, 3)                                  # arts

photos = get("posts", tags=seen_around, per_page=10,
             _embed="wp:featuredmedia,author")
out["photos"] = [shape(p) for p in photos]

# topic groups — 4 most recent stories per curated tag
TOPIC_TAGS = [
    ("Co-op", "co-op", 111),
    ("Experiential Learning", "experiential-learning", 199),
    ("Events", "events", 73),
    ("President Aoun", "president-joseph-e-aoun", 20527),
]
out["topics"] = [
    {"label": label, "slug": slug,
     "stories": [s for s in
                 (shape(p) for p in get("posts", tags=tag_id, per_page=8,
                                        _embed="wp:featuredmedia,author"))
                 if s["img"]][:6]}
    for label, slug, tag_id in TOPIC_TAGS
]

# staff photographers author the daily photo features; anything they byline
# is a photo post even without the seen-around tag
PHOTO_BYLINES = {"Matthew Modoono", "Alyssa Stone"}
out["stories"] = [s for s in out["stories"] if s["byline"] not in PHOTO_BYLINES]

# drop anything without an image; dedupe by link
seen = set()
for key in ("stories", "photos"):
    deduped = []
    for s in out[key]:
        if s["img"] and s["link"] not in seen:
            seen.add(s["link"])
            deduped.append(s)
    out[key] = deduped

with open("content.json", "w") as f:
    json.dump(out, f, indent=1)

print(f"stories={len(out['stories'])} photos={len(out['photos'])}")
