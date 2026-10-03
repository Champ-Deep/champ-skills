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
import json, os, sys, math, collections, html as _h

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from squarify import squarify

HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------ payload

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
        items.append({"sec": "other sections",
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
    bundle = json.load(open(a.bundle))
    plan = json.load(open(a.plan))
    p = make_payload(bundle, plan)
    out = render(p)
    open(a.out, "w", encoding="utf-8").write(out)
    print(f"{a.out}  {os.path.getsize(a.out)//1024} KB")
    print("  pages:", len(p["pages"]), " edges:", len(p["edges"]),
          " entities:", len(p["entities"]), " work:", len(p["work"]))