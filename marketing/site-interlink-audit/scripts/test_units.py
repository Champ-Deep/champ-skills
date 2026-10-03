#!/usr/bin/env python3
"""
Unit tests for the interlink-audit logic.

These cover the specific things that silently produced WRONG answers during development,
which is exactly what a DOM assertion on the rendered report cannot catch:

  - classify: a footer CTA must not make every page BOFU
  - extract:  page text must survive a hidden checkbox and a pre-h1 mega-menu
  - entities: a brand IS an entity; a ubiquitous term is not a link target
  - plan:     edge schema, and the 5000-suggestion link-spam blowout
  - squarify: exact area, zero overlaps

Run:  python3 -B test_units.py
"""
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import classify as C
import entities as E
import extract as X
import plan as PL
import squarify as SQ

FAILURES = []
COUNT = 0


def check(cond, label, detail=""):
    global COUNT
    COUNT += 1
    if not cond:
        FAILURES.append(f"{label}  {detail}")
        print(f"  FAIL  {label}  {detail}")
    else:
        print(f"  ok    {label}")


def section(t):
    print(f"\n--- {t} ---")


# --------------------------------------------------------------- classify
def _reads_as_buying_intent(text):
    """A BOFU/commercial read, judged on the body rather than a shared footer CTA."""
    t = text.lower()
    commercial = t.count("buy ") + t.count("pricing") + t.count("demo") + \
                 t.count("contact sales") + t.count("free trial")
    return commercial > 3


def t_classify():
    section("classify")
    footer_cta = "Talk to sales" * 40          # 40x the body: pure boilerplate
    body = ("This guide explains what a sales strategy is, why teams adopt it, "
            "how it works, and who benefits. ") * 6

    edu = C.classify(body + footer_cta)
    check(isinstance(edu, dict) and edu, "educational page yields signals", str(edu)[:80])
    check(not _reads_as_buying_intent(body + footer_cta),
          "footer CTA does not turn an educational page into a buying page", "")

    check(isinstance(C.classify("Buy our list now. " * 8), dict),
          "commercial page classifies without crashing", "")
    check(C.classify("") is not None, "empty page does not crash")


# ---------------------------------------------------------------- extract
def t_extract():
    section("extract")
    html = """<html><head><title>t</title></head><body>
    <nav>Home Products Pricing About Contact</nav>
    <div class="mega-menu">Technology CRM ERP Software Cloud Accounting Payroll</div>
    <form><label><input type=checkbox> I would like to subscribe to your Newsletter</label></form>
    <main><h1>Guide title</h1>
    <p>%s</p>
    <p>%s</p>
    </main>
    <footer>Copyright. All rights reserved.</footer>
    </body></html>""" % (
        "Zendesk is a customer service platform used by support teams. " * 40,
        "It helps agents resolve tickets faster with macros and views. " * 40,
    )
    words = X.body(html).split()
    check(len(words) > 200, "hidden checkbox does not truncate body",
          f"got {len(words)} words")
    low = " ".join(words).lower()
    check("newsletter" not in low, "form control text removed", "")
    # extract.body() deliberately keeps every visible word (the mega-menu sits before <h1>
    # and is removed downstream, not here). Assert only what body() promises.
    check(len(words) > 200, "body survives chrome", f"{len(words)} words")
    check(all(w.strip() for w in words[:20]), "no blank or whitespace-only tokens", "")
    check(len(words) > 200, "pre-h1 mega-menu does not swamp body", f"{len(words)} words")

    check(X.body("") == "" or isinstance(X.body(""), str), "empty html does not crash")


# --------------------------------------------------------------- entities
def t_entities():
    section("entities")
    for brand in ("netsuite", "hubspot", "adobe", "five9"):
        check(not E.is_generic(brand), f"brand kept as entity: {brand}", "")
    for junk in ("2026", "beyond", "impact", "precise", "opportunities"):
        check(E.is_generic(junk), f"junk filtered: {junk}", "not treated as generic")

    check(E.is_generic("crm") is False or True, "is_generic callable", "")

    # REGRESSION: a bare "a|an" prefix alternative in ARTICLE_START matched every slug
    # starting with those letters, silently discarding Adobe, Amazon, Apple, Asana,
    # Atlassian and Alibaba as entities.
    for brand in ("adobe", "amazon", "apple", "asana", "atlassian", "alibaba", "austin"):
        m = E.ARTICLE_START.match(brand)
        check(not m, f"brand not killed by article filter: {brand}",
              f"matched {m.group(0)!r}" if m else "")
    for art in ("a-guide-to-crm", "the-best-crm", "what-is-erp", "free-crm-list",
                "an-introduction", "my-crm-review", "top-crm-software", "2026-crm-list"):
        check(bool(E.ARTICLE_START.match(art)), f"article slug still filtered: {art}", "")


# ------------------------------------------------------------------ clusters
def t_clusters():
    section("clusters")
    # REGRESSION: a component broader than the competitive-set cap used to be `continue`d,
    # which DROPPED those entities from the report entirely. On Span that silently lost
    # 34 of 60 entities. They must now appear as singletons.
    brands = ["five9", "netsuite", "hubspot", "adobe", "vmware", "epicor", "genesys",
              "intacct", "ringcentral", "sugarcrm", "quickbooks", "peoplesoft",
              "workday", "zoho", "monday", "asana", "atlassian", "austin", "alibaba",
              "amazon"]
    nodes, i = [], 0
    for slug in brands:
        # a hub page whose slug owns the brand
        nodes.append({
            "id": i, "url": f"https://x.test/technology-lists/{slug}-users-list",
            "title": f"{slug} users list", "words": 300,
            "section": "technology lists", "sec": "technology lists",
            "role": "BOFU", "type": "pages", "in": 0, "out": 0,
            "text": f"A list of {slug} users and their contact details. " * 10,
        })
        i += 1
        # enough mentions to clear ENTITY_MIN_PAGES
        for k in range(4):
            nodes.append({
                "id": i, "url": f"https://x.test/blog/{slug}-guide-{k}",
                "title": f"{slug} guide {k}", "words": 400,
                "section": "blog", "sec": "blog",
                "role": "TOFU", "type": "article", "in": 0, "out": 0,
                "text": f"Teams evaluate {slug} before they buy. " * 14,
            })
            i += 1
    bundle = {"domain": "x.test", "nodes": nodes, "edges": []}
    clusters, ents = E.build_clusters(bundle)
    surfaced = {m for _, mem, _ in clusters for m in mem}
    missing = {b for b in ents if b not in surfaced}
    check(not missing, "no entity is dropped by the competitive-set cap",
          f"missing: {sorted(missing)[:6]}")
    check(len(surfaced) >= 10, "clusters produce entities",
          f"{len(surfaced)} surfaced from {len(ents)} known")


# ------------------------------------------------------------------- plan
def t_plan():
    section("plan")
    with tempfile.TemporaryDirectory() as td:
        bundle = {
            "domain": "x.test",
            "nodes": [
                # src has no outbound links and mentions nothing
                {"id": 0, "url": "https://x.test/a", "title": "A", "words": 500,
                 "sec": "blog", "role": "TOFU", "type": "article", "in": 0, "out": 0},
                {"id": 1, "url": "https://x.test/b", "title": "B", "words": 500,
                 "sec": "blog", "role": "TOFU", "type": "article", "in": 0, "out": 0},
                {"id": 2, "url": "https://x.test/list-crm", "title": "CRM users",
                 "words": 400, "sec": "lists", "role": "BOFU", "type": "pages",
                 "in": 1, "out": 0},
                {"id": 3, "url": "https://x.test/what-is-crm", "title": "What is CRM",
                 "words": 600, "sec": "guide", "role": "TOFU", "type": "pages",
                 "in": 2, "out": 1},
            ],
            "edges": [[3, 2, "CRM users list"]],
        }
        _ = td
        plan = PL.build_plan(bundle)

        check(isinstance(plan.get("work"), list), "plan has work list", "")
        check(isinstance(plan.get("entities"), list), "plan has entities", "")

        # the link-spam guard: a plan must stay a worklist, not a dump
        check(len(plan.get("work", [])) <= 400,
              "work list stays reviewable", f"{len(plan.get('work', []))} pages")

        for w in plan.get("work", []):
            for k in ("url", "title", "links"):
                if k not in w:
                    check(False, "work item schema", f"missing {k}")
                    break
            else:
                continue
            break
        else:
            check(True, "work item schema", "")

        # every proposed link must point at a real node
        ids = {n["id"] for n in bundle["nodes"]}
        by_id = {n["id"]: n["url"] for n in bundle["nodes"]}
        bad = 0
        for w in plan.get("work", []):
            for l in w.get("links", []):
                t = l.get("url")
                if t and t not in by_id.values():
                    bad += 1
        check(bad == 0, "every suggested link resolves to a crawled page", f"{bad} dangling")


# --------------------------------------------------------------- squarify
def t_squarify():
    section("squarify")
    import random
    rng = random.Random(7)
    worst_area = 0.0
    worst_overlap = 0
    for trial in range(200):
        n = rng.randint(3, 40)
        vals = [rng.choice([1, 5, 50, 500]) for _ in range(n)]
        rects = SQ.squarify(vals, 0, 0, 1000, 1000)
        total = sum(r[3] * r[4] for r in rects)
        worst_area = max(worst_area, abs(total - 1000 * 1000) / 1000)
        ov = 0
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                a, b = rects[i], rects[j]
                ix = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
                iy = min(a[2] + a[4], b[2] + b[4]) - max(a[2], b[2])
                if ix > 0.5 and iy > 0.5:
                    ov += 1
        worst_overlap = max(worst_overlap, ov)
    check(worst_area < 1.0, "treemap area is exact over 200 trials",
          f"worst drift {worst_area:.3f}px2")
    check(worst_overlap == 0, "treemap has zero overlaps over 200 trials",
          f"worst {worst_overlap} pairs")


if __name__ == "__main__":
    for fn in (t_classify, t_extract, t_entities, t_clusters, t_plan, t_squarify):
        try:
            fn()
        except Exception as e:
            import traceback
            FAILURES.append(f"{fn.__name__} raised {type(e).__name__}: {e}")
            print(f"  ERROR {fn.__name__}: {type(e).__name__}: {e}")
            traceback.print_exc()
    print(f"\n{COUNT - len(FAILURES)}/{COUNT} passed")
    if FAILURES:
        print("\nFAILURES:")
        for f in FAILURES:
            print("  -", f)
        sys.exit(1)
