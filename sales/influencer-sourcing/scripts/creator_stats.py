#!/usr/bin/env python3
"""Creator vetting stats: subscribers, median recent views, Fuse price bands.

Usage: python3 creator_stats.py <channel> [<channel> ...] [--fuse slug1 slug2 ...]

A <channel> is any of:
  @handle            handle from the channel URL
  channel/UC...      full channel id (what yt-dlp --flat-playlist prints)
  UC...              bare channel id

- Subscribers: read from the channel page HTML.
- Median views: median view count across the channel's YouTube RSS feed
  (last 15 entries), fetched via the channel's externalId.
- Fuse bands: scraped from https://www.getfused.io/creators/<slug> when a
  slug is supplied (estimates, not quotes).

Harvest candidates first, then measure them:
  yt-dlp --socket-timeout 20 --flat-playlist --playlist-end 12 \
    --print '%(channel)s | %(channel_url)s | %(view_count)s | %(title)s' \
    "ytsearch12:<buyer question>"

Run inside execute_code (needs hermes_tools.terminal) or as plain python3
with curl available.
"""
import json, re, statistics, subprocess, sys
import xml.etree.ElementTree as ET

UA = ["-A", "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/120 Safari/537.36",
      "-H", "Accept-Language: en-US", "-b", "CONSENT=YES+1"]


def is_channel(a):
    return a.startswith("@") or a.startswith("channel/") or a.startswith("UC")


def curl(url):
    return subprocess.run(["curl", "-sL", "--max-time", "25", *UA, url],
                          capture_output=True, text=True).stdout


def channel_stats(handle):
    html = curl(f"https://www.youtube.com/{handle}")
    subs = re.findall(r'"content":"([\d\.,KM]+ subscribers)"', html) \
        or re.findall(r'([\d\.,]+[KM]? subscribers)', html)
    cid = re.search(r'"externalId":"(UC[\w-]+)"', html)
    if not cid:
        return {"handle": handle, "subs": subs[:1], "error": "no channel id"}
    feed = curl(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid.group(1)}")
    ns = {"a": "http://www.w3.org/2005/Atom",
          "m": "http://search.yahoo.com/mrss/"}
    views = []
    try:
        for e in ET.fromstring(feed).findall("a:entry", ns):
            st = e.find(".//m:statistics", ns)
            if st is not None:
                views.append(int(st.get("views")))
    except ET.ParseError:
        pass
    return {"handle": handle, "subs": subs[:1],
            "median_views": int(statistics.median(views)) if views else None,
            "feed_entries": len(views)}


def fuse_bands(slug):
    html = curl(f"https://www.getfused.io/creators/{slug}")
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html))
    if "Creator not found" in txt:
        return {"slug": slug, "found": False}
    out = {"slug": slug, "found": True}
    for key in ("Dedicated video", "Integration mention", "Social post",
                "Bundle (video + 2 social)"):
        m = re.search(re.escape(key) + r" (\$[\dK\.,\s-]+?) (?:LinkedIn|Twitter|TikTok|More platforms|Growth Trends|Recent Videos|View full)", txt)
        if m:
            out[key] = re.sub(r"\s+", " ", m.group(1)).strip(" ,-")
    return out


def main():
    args = sys.argv[1:]
    handles, slugs = [], []
    if "--fuse" in args:
        i = args.index("--fuse")
        handles = [a for a in args[:i] if is_channel(a)]
        slugs = args[i+1:]
    else:
        handles = [a for a in args if is_channel(a)]
    for h in handles:
        print(json.dumps(channel_stats(h)))
    for s in slugs:
        print(json.dumps(fuse_bands(s)))


if __name__ == "__main__":
    main()
