#!/usr/bin/env python3
"""
Build a client-ready interlink report for ANY site from its crawl bundle + plan.

One self-contained HTML file. Three views:
  1. SITE MAP    treemap of every page, tinted by funnel role
  2. ENTITIES    which topics/products the site has pages for, and which it only talks about
  3. WORKLIST    the ranked edits, tickable, persisted locally

Design constraints that came out of earlier audits: 4.5px+ tap targets, no em dashes, WCAG
AA contrast on every computed pair, and a single dense JSON payload with no network calls.
"""
import json, sys, os, sys, math, collections, html as _h

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from squarify import squarify

HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ payload

def derive_findings(plan, bundle):
    """
    Turn the measurements into the sentences a client actually wants to hear.
    Every finding quotes the number it came from, so it cannot drift from the data.
    """
    s = plan["summary"]
    out = []
    pages = max(1, s["pages"])

    zi, zo = s["zero_in"], s["zero_out"]
    if zi / pages > 0.25:
        frac = round(100 * zi / pages)
        word = ("nearly all" if frac >= 90 else "most" if frac >= 60 else
                "over half" if frac >= 50 else "over a third" if frac >= 33 else "a quarter")
        out.append({
            "sev": "high", "t": f"{frac}% of the site is invisible to crawlers and readers",
            "b": f"{zi:,} of {s['pages']:,} pages have no inbound link from anywhere on the "
                 f"site. They cannot rank for anything, and a reader can only reach them by "
                 f"typing the address."})
    if zo / pages > 0.4:
        out.append({
            "sev": "high", "t": "Most pages are dead ends",
            "b": f"{zo:,} pages ({round(100*zo/pages)}%) contain no links out to related "
                 f"content. Every one of those is a reader who leaves instead of going deeper."})
    if s.get("no_tofu"):
        out.append({
            "sev": "high", "t": "No research layer feeding the commercial pages",
            "b": f"{s['no_tofu']} entities have a commercial page but no research page to "
                 f"earn the visit first. Competitors ranking for the research terms win "
                 f"the traffic those pages never see."})
    if s.get("work_links"):
        out.append({
            "sev": "mid", "t": "Existing mentions that never became links",
            "b": f"{s['work_links']} links across {s['work_pages']} pages are already "
                 f"warranted in the copy but missing from the markup. These are the cheapest "
                 f"wins on the list: no new writing required."})
    insm = s.get("in_sitemap", 0)
    if insm and insm / pages < 0.9:
        out.append({
            "sev": "mid", "t": "Sitemap does not describe the site",
            "b": f"{insm:,} of {s['pages']:,} crawled pages ({round(100*insm/pages)}%) "
                 f"appear in the XML sitemap."})
    elif insm:
        out.append({
            "sev": "low", "t": "Submission is not the problem here",
            "b": f"{insm:,} of {s['pages']:,} pages ({round(100*insm/pages)}%) are in the "
                 f"sitemap, so these pages can be discovered. What is missing is internal "
                 f"linking: a page in a sitemap with no inbound link still gets almost no "
                 f"traffic."})
    st = bundle.get("stats", {})
    if st.get("truncated"):
        out.append({
            "sev": "low", "t": "Crawl was capped",
            "b": f"This run fetched {st.get('pages')} of {st.get('candidates')} candidate "
                 f"URLs. The figures below cover what was fetched."})
    return out


def make_payload(bundle, plan, cap_entities=60, cap_work=400):
    nodes = bundle["nodes"]
    edges = bundle["edges"]

    ind = collections.Counter(e[1] for e in edges)
    outd = collections.Counter(e[0] for e in edges)
    live = {n["id"]: n for n in nodes}

    sections = collections.Counter(n.get("section") or "root" for n in nodes)
    role_by_section = collections.defaultdict(collections.Counter)
    for n in nodes:
        role_by_section[n.get("section") or "root"][n.get("role")] += 1

    # treemap groups: sections, plus a synthetic bucket for the long tail
    groups = []
    for sec, count in sections.most_common():
        groups.append({
            "sec": sec, "n": count,
            "roles": dict(role_by_section[sec]),
            "z": sum(1 for n in nodes if (n.get("section") or "root") == sec
                     and ind.get(n["id"], 0) == 0),
        })

    pages = [{"i": n["id"], "u": n["url"], "s": n.get("section") or "root",
              "r": n.get("role"), "t": n.get("title", ""),
              "i": ind.get(n["id"], 0), "o": outd.get(n["id"], 0),
              "w": n.get("words", 0)} for n in nodes]

    ents = sorted(plan["entities"], key=lambda e: -(e["mentions"] + e["pages"] * 5))
    ents = ents[:cap_entities]
    ents.sort(key=lambda e: -e["mentions"])

    work = [{"u": w["url"], "t": w.get("title") or "", "r": w.get("role"),
             "s": w.get("section") or "root", "i": w.get("in", 0),
             "o": w.get("out", 0), "score": w.get("score", 0),
             "links": w.get("links", [])}
            for w in plan["work"][:cap_work]]

    clusters = plan["clusters"][:30]

    # ---- treemap geometry, computed with the tested squarify -------------
    W, H, PAD = 1200.0, 620.0, 4.0
    groups = sorted(groups, key=lambda g: -g["n"])
    big, tail = groups[:11], groups[11:]
    items = list(big)
    if tail:
        items.append({"sec": "all other sections",
                      "n": sum(g["n"] for g in tail),
                      "z": sum(g["z"] for g in tail),
                      "tail": True})
    rects = squarify([g["n"] for g in items], PAD, PAD, W - PAD*2, H - PAD*2)
    for gi, (idx, rx, ry, rw, rh) in enumerate(rects):
        items[idx]["_rect"] = [round(rx, 1), round(ry, 1), round(rw, 1), round(rh, 1)]

    return {
        "mapw": W, "maph": H,
        "host": bundle.get("host", ""),
        "base": bundle.get("base", ""),
        "fetched": bundle.get("fetched_at", ""),
        "summary": plan["summary"],
        "findings": derive_findings(plan, bundle),
        "groups": items,
        "pages": pages,
        "edges": [[e[0], e[1]] for e in edges if e[0] in live and e[1] in live],
        "entities": ents,
        "clusters": clusters,
        "work": work,
    }


# ------------------------------------------------------------------ render

def render(payload):
    s = json.dumps(payload, separators=(",", ":"))
    tpl = open(os.path.join(HERE, "report_template.html"), encoding="utf-8").read()
    return tpl.replace("__PAYLOAD__", s)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle")
    ap.add_argument("plan")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    # Never exit 0 on a missing or unreadable input: a caller that discards stderr would
    # see success and keep serving the PREVIOUS output file, mistaking it for a fresh build.
    for f in (a.bundle, a.plan):
        if not os.path.exists(f):
            sys.exit(f"report.py: input not found: {f}")
    bundle = json.load(open(a.bundle))
    plan = json.load(open(a.plan))
    p = make_payload(bundle, plan)
    out = render(p)
    open(a.out, "w", encoding="utf-8").write(out)
    print(f"{a.out}  {os.path.getsize(a.out)//1024} KB")
    print("  pages:", len(p["pages"]), " edges:", len(p["edges"]),
          " entities:", len(p["entities"]), " work:", len(p["work"]))