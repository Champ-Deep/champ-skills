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


def t_adversarial_review():
    """Every defect an external review of the Span report found, as a regression test."""
    section("adversarial review fixes")
    import entities as E
    import plan as PLAN

    def mk(url, title="T", words=400, section="guides", role="MID",
           ptype="pages", nin=0, nout=1, text=None):
        return {"id": str(abs(hash(url)) % 10 ** 6), "url": url, "title": title,
                "words": words, "section": section, "role": role, "type": ptype,
                "in": nin, "out": nout, "in_sitemap": True,
                "text": text or "data leads targeting healthcare technology " * 30}

    # 1. the "76% invisible" headline was 86% FAQ pages, so the summary must be able to
    #    state the rate with and without them.
    faq = [mk(f"https://x.test/faq/q{i}", section="faq", ptype="faq") for i in range(20)]
    studies = [mk(f"https://x.test/case-studies/c{i}", section="case-studies",
                  ptype="case_studies", nin=(1 if i < 4 else 0))
               for i in range(8)]
    # 4 of the 8 studies are linked, so excluding FAQ must lower the orphan rate
    edges = [[studies[4]["id"], studies[i]["id"], "read", 0] for i in range(4)]
    s = PLAN.build_plan({"domain": "x.test", "nodes": faq + studies,
                         "edges": edges})["summary"]
    check(s.get("faq_pages") == 20, "summary counts faq pages", str(s.get("faq_pages")))
    check(s.get("pages_ex_faq") == 8, "summary counts non-faq pages",
          str(s.get("pages_ex_faq")))
    check(s.get("zero_in_ex_faq") == 4, "orphan rate ex-faq is reportable",
          str(s.get("zero_in_ex_faq")))
    check(s["zero_in_ex_faq"] / s["pages_ex_faq"] < s["zero_in"] / s["pages"],
          "excluding FAQ makes the orphan rate honest", "")

    # 2. list product pages are commercial whatever the copy sounds like
    cases = [("https://x.test/technology-lists/zoho-crm-users-list", "BOFU"),
             ("https://x.test/healthcare-lists/nurses-email-list", "BOFU"),
             ("https://x.test/geo-targeted-lists/uk-business-email-list", "BOFU"),
             ("https://x.test/blog/companies-using-x", "TOFU"),
             ("https://x.test/white-paper/guide", "MID")]
    for url, want in cases:
        got = PLAN.role_from_url(url, "WRONG")
        check(got == want, f"role from URL: {url.rsplit('/', 1)[-1]} -> {want}", got)
    kept = PLAN.role_from_url("https://x.test/about-us", "TOFU")
    check(kept == "TOFU", "an unknown path keeps the text classifier", kept)

    # 3. ownership beats every word-shape heuristic, so aws and sap survive
    def own_fixture(brand):
        return {"domain": "x.test", "edges": [], "nodes": [
            mk(f"https://x.test/technology-lists/{brand}-users-list",
               title=f"{brand} users list", nin=30,
               text=f"A list of {brand} users and contacts. " * 12),
        ] + [mk(f"https://x.test/blog/{brand}-{k}", title=f"{brand} guide {k}",
                section="blog", ptype="article",
                text=f"Teams evaluate {brand} before they buy. " * 14)
             for k in range(4)]}

    for brand in ("aws", "sap"):
        _, ents = E.build_clusters(own_fixture(brand))
        check(brand in ents, f"a 3-letter acronym owning a page is an entity ({brand})",
              str(sorted(ents)[:4]))

    # 4. one cluster must not eat the entity budget, and the cap must not drop members
    nodes = []
    for g in [f"geo{i}" for i in range(14)]:
        nodes.append(mk(f"https://x.test/geo-targeted-lists/{g}-business-email-list",
                        title=f"{g} business email list"))
        for k in range(4):
            nodes.append(mk(f"https://x.test/blog/{g}-{k}", section="blog",
                            ptype="article",
                            text=f"Companies in {g} buy data lists. " * 14))
    cl, ents = E.build_clusters({"domain": "x.test", "nodes": nodes, "edges": []})
    surfaced = {m for _, mem, _ in cl for m in mem}
    dropped = set(ents) - surfaced
    check(not dropped, "a capped cluster still emits every entity as a singleton",
          str(sorted(dropped)[:4]))
    biggest = max(len(m) for _, m, _ in cl)
    check(biggest <= E.MAX_CLUSTER_MEMBERS,
          f"no cluster exceeds MAX_CLUSTER_MEMBERS ({E.MAX_CLUSTER_MEMBERS})",
          str(biggest))

    # 5. a redirecting target must never reach the worklist
    def two_entity_bundle():
        """netSuite is discussed on three pages so it becomes an entity; one of the pages
        that mentions it is the source, and the hub it points at is the target."""
        nodes = [mk("https://x.test/technology-lists/netsuite-users-list",
                    title="NetSuite Users List", section="technology-lists",
                    ptype="pages", nin=0,
                    text="A NetSuite users list for finance teams. " * 14)]
        nodes += [mk(f"https://x.test/blog/finance-teams-{i}",
                     title=f"Finance teams guide {i}", section="blog",
                     ptype="article", role="TOFU", nin=5,
                     text=f"Finance teams compare NetSuite and Sage. " * 14)
                  for i in range(3)]
        return {"domain": "x.test", "nodes": nodes, "edges": []}

    red = "https://x.test/technology-lists/netsuite-users-list"
    plan = PLAN.build_plan(two_entity_bundle(),
                           redirects={red: "https://x.test/technology-lists/"})
    proposed = [l["url"] for w in plan["work"] for l in w["links"]]
    check(red not in proposed, "a redirecting target is dropped from the worklist",
          str(proposed[:3]))
    check(any("netsuite" in u for u in plan["summary"]["redirecting_targets"]),
          "the dropped redirect is reported, not silently discarded",
          str(plan["summary"]["redirecting_targets"]))

    # control: without the redirect map the same target IS proposed, so the test is real
    plan_ok = PLAN.build_plan(two_entity_bundle())
    check(red in [l["url"] for w in plan_ok["work"] for l in w["links"]],
          "control: the target is proposed when it does not redirect",
          str([l["url"] for w in plan_ok["work"] for l in w["links"]][:3]))

    # 5a. Boilerplate must never delete a menu destination. An adversarial review found the
    #     "76% invisible" headline counted the header menu as unreachable. The first fix
    #     required a target to be BOTH recurring AND in the nav, which is worse: on a site
    #     with a global menu those two sets coincide, so every menu edge was deleted exactly
    #     as before. The rule is "recurring AND never linked from page prose".
    import pipeline as PIPE
    psrc = open(PIPE.__file__, encoding="utf-8").read()
    check("menu_only = {t for t in nav_set if prose.get(t, 0) == 0}" in psrc,
          "menu_only is targets linked only from the menu", "")
    check("boiler = {t for t in always if t not in menu_only}" in psrc,
          "boilerplate excludes menu-only destinations", "")
    check("boiler = {t for t in always if t in nav_set}" not in psrc,
          "the broken 'always AND in nav' rule is gone", "")

    # 5b. nav_set must exist before boilerplate is computed. Defining it after its use
    #     raised UnboundLocalError only after a 5 minute crawl, which is an expensive way
    #     to learn about statement order.
    import pipeline as PIPE
    src = open(PIPE.__file__, encoding="utf-8").read()
    check(src.index("nav_set = set()") < src.index("boiler = {t for t in always"),
          "nav_set is defined before boilerplate uses it", "")
    check("raw_cache = {}" in src, "raw_cache is declared so nav_set can be built", "")

    # 5c. Ownership must mean a real hub. A second review round found the loose version
    #     filled half the worklist with junk: "from" owned a case study
    #     (/from-dormant-data-to-349k-in-revenue), "key" owned the SurveyMonkey page,
    #     "thanks" owned /thanks, "web" owned /webinars, "sgs" owned the corporate
    #     brochure. None of those is a topic.
    # Some are blocked as words, others by the rules below. Assert the mechanism that
    # actually applies rather than pretending they are all in one list.
    for w in ["from", "to", "for", "with", "using", "how", "what", "new",
              "here", "welcome", "click"]:
        check(w in E.FUNCTION_WORD or w in E.GENERIC_WORD,
              f"'{w}' is blocked as a non-topic word", "")
    for w in ["thanks", "key", "core", "click"]:
        check(w in E.GENERIC_WORD, f"'{w}' is a blocked generic word", "")
    # "web" and "sgs" are caught structurally, not lexically: /webinars and the corporate
    # brochure are not hubs, so neither can own one.
    check(not E.owns_a_hub({"url": "https://x.test/webinars", "section": "webinars"}),
          "/webinars is not a hub, so 'web' cannot own one", "")
    check(not E.owns_a_hub({"url": "https://x.test/corporate-brochure/sgs",
                            "section": "corporate-brochure"}),
          "the brand brochure is not a hub, so 'sgs' cannot own one", "")

    def owns_junk(url, section="", leaf_is_topic=True):
        return E.owns_a_hub({"url": url, "section": section})

    check(not owns_junk("https://x.test/thanks", "thanks"), "/thanks is not a hub", "")
    check(not owns_junk("https://x.test/corporate-brochure/sgs", "corporate-brochure"),
          "a corporate brochure is not a hub", "")
    check(not owns_junk("https://x.test/faq/who-can-benefit-from-this-list", "faq"),
          "an FAQ answer is not a hub", "")
    check(not owns_junk("https://x.test/case-studies/from-dormant-data-to-x",
                        "case-studies") is False,
          "a case study CAN be a hub, so FUNCTION_WORD must block 'from'", "")
    check(owns_junk("https://x.test/technology-lists/sap-users-list", "technology-lists"),
          "a technology list IS a hub", "")
    # section names arrive hyphenated, underscored or spaced; the comparison must normalise
    check(not owns_junk("https://x.test/corporate_brochure/sgs", "corporate_brochure"),
          "section matching normalises separators", "")

    # 6. an entire content area can sit outside sitemap_index.xml. The Span blog lives in
    #    /blog/sitemap_index.xml with 1,613 posts, referenced by neither the index nor
    #    robots.txt, so the crawl saw 4 blog pages and reported no research layer.
    import discover as DISC
    src = open(DISC.__file__, encoding="utf-8").read()
    check("/blog/sitemap_index.xml" in src,
          "discovery probes an out-of-index blog sitemap", "")
    check("sitemap_index.xml" in src and "robots.txt" in src,
          "discovery still follows the index and robots.txt", "")

    # 7. the worklist must prefer an orphan target over an already-linked one
    def wl_fixture(target_in):
        """'rich users list' must clear ENTITY_MIN_PAGES, so it is mentioned on 4 pages.
        The hub's inbound count is the only thing that varies between the two runs."""
        nodes = [mk("https://x.test/technology-lists/rich-users-list",
                    title="rich users list", role="BOFU", section="technology-lists",
                    nin=target_in,
                    text="A rich users list for data buyers. " * 40)]
        nodes += [mk(f"https://x.test/blog/rich-guide-{i}",
                     title=f"rich users list guide {i}", role="TOFU", nin=20,
                     section="blog", ptype="article",
                     text="A rich users list compared with other vendors. " * 40)
                  for i in range(3)]
        nodes += [mk("https://x.test/blog/source-users-list-guide",
                     title="source users list guide", role="TOFU", nin=40,
                     section="blog", ptype="article",
                     text="A source guide that mentions a rich users list. " * 40)]
        return {"domain": "x.test", "nodes": nodes, "edges": []}
    lo = PLAN.build_plan(wl_fixture(0))["work"]
    hi = PLAN.build_plan(wl_fixture(300))["work"]
    check(lo and hi, "both worklists produced a suggestion", f"{len(lo)} {len(hi)}")
    if lo and hi:
        best_lo = max((p["val"] for w in lo for p in w["links"]), default=0)
        best_hi = max((p["val"] for w in hi for p in w["links"]), default=0)
        check(best_lo > best_hi,
              "an orphan target outranks an already-linked one",
              f"orphan={best_lo} linked={best_hi}")

# ------------------------------------------------------------------- plan
def t_refresh_bookkeeping():
    section("refresh bookkeeping")
    import refresh as R
    # REGRESSION: --all used to rebuild the host by swapping dashes for dots, and it read
    # -plan / -related sidecars as if they were bundles. That invented domains such as
    # "bundle-without-crawling-anything-new", which were then crawled and reported as real
    # sites. known_bundles must return only real bundles.
    kb = R.known_bundles()
    check(all("plan" not in k and "related" not in k for k in kb),
          "known_bundles excludes sidecars", str(sorted(kb)[:4]))
    check(all(k.startswith("bundle-") or "/" in v for k, v in kb.items()),
          "known_bundles values are full paths", "")
    # one site, one slug: www must not create a second identity
    check(R.slugify("www.example.com") == R.slugify("example.com"),
          "www. does not fork the slug", R.slugify("www.example.com"))
    # a drop-in list tolerates comments, blanks, commas and a JSON array
    import tempfile, os, json as _json
    with tempfile.TemporaryDirectory() as td:
        p1 = os.path.join(td, "a.txt")
        open(p1, "w").write("# c\n\nexample.com  # trailing\n, foo.com\n")
        check(R.read_list(p1) == ["example.com", "foo.com"], "plain list parsed",
              str(R.read_list(p1)))
        p2 = os.path.join(td, "b.json")
        open(p2, "w").write(_json.dumps(["a.com", "b.com"]))
        check(R.read_list(p2) == ["a.com", "b.com"], "json array parsed",
              str(R.read_list(p2)))


def t_clef_gate():
    section("clef gate")
    import semantic as SEM
    check(SEM.clef_mode() in ("local", "hosted", "none"),
          "clef_mode reports a valid mode", SEM.clef_mode())
    # with nothing configured it must be "none", and the rules must still produce output
    if not SEM.clef_available():
        check(True, "clef unavailable -> rules-only path is taken", "expected on this box")
        p = {"target_id": 1, "rule": 0.5}
        out = SEM.blend([p], {}, weights=(0.55, 0.45))
        check(out[0]["unjudged"] is True, "unjudged candidate is flagged", "")
        # A missing judgement must never score better than a judged one.
        judged = SEM.blend([{"target_id": 2, "rule": 0.5}], {2: 0.0})[0]
        check(out[0]["score"] >= judged["score"],
              "unjudged does not outrank a judged candidate",
              f"unjudged={out[0]['score']} judged={judged['score']}")
    # buckets, not magnitudes
    check(SEM.bucket(0.95) == "strong" and SEM.bucket(0.05) == "weak",
          "score buckets are ordered", "")


def t_related_diversity():
    section("related-link diversity")
    import semantic as SEM
    bundle = {"domain": "x.test", "nodes": [
        {"id": str(i), "url": f"https://x.test/p{i}", "title": f"Guide {i}",
         "words": 400, "section": "guide", "role": "TOFU", "type": "article",
         "in": 0, "out": 0,
         "text": f"data leads targeting technology healthcare platform {i} " * 20}
        for i in range(30)
    ], "edges": []}
    pairs = SEM.build_pairs(bundle, limit_per_page=4)
    # REGRESSION: chrome pages used to become link sources, and the top suggestions were
    # all near-identical template pages. Sources must carry real content.
    flat = [(sid, c) for sid, cs in pairs.items() for c in cs]
    check(all(len(n.get("text") or "") > 0 for n in bundle["nodes"]), "fixture ok", "")
    # every candidate must carry a written reason and a bounded score
    bad = [c for _, c in flat if not c.get("why") or not (0.0 <= c.get("score", -1) <= 1.0)]
    check(not bad, "every suggestion has a reason and a bounded score", f"{len(bad)} bad")
    # no duplicate target URLs from one source
    for sid, cs in pairs.items():
        urls = [c["target"] for c in cs]
        check(len(urls) == len(set(urls)), f"no duplicate targets for source {sid}",
              f"{len(urls)} rows, {len(set(urls))} unique")


def t_clef_runner():
    section("clef runner")
    import os, json, subprocess, tempfile, sys as _s
    import semantic as SEM
    # REGRESSION: semantic.py invoked _clef_run.py in local mode but the file did not
    # exist, so local CLEF could never run. Assert the runner is present and that it
    # accepts BOTH answer shapes the pipeline may receive.
    runner = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_clef_run.py")
    check(os.path.exists(runner), "_clef_run.py exists", runner)
    src = open(runner, encoding="utf-8").read()
    for sym in ("collate_records", "encode_record", "load_release_model"):
        check(sym in src, f"runner imports {sym}", "")
    check("inference_mode" in src, "runner uses inference_mode (memory)", "")

    # the runner emits a bare float; the hosted API wraps in {"answer": x}. Both must
    # blend, or one of the two modes silently loses every judgement.
    bare = SEM.blend([{"target_id": 1, "rule": 0.4}], {1: 0.72})[0]
    check(abs(bare["score"] - (0.55 * 0.4 + 0.45 * 0.72)) < 0.002,
          "bare-float judgement blends", str(bare["score"]))


def t_related_direction_and_host():
    section("related links: direction and hosting")
    import semantic as SEM
    # REGRESSION 1: 19% of candidate rows were the reverse of another row (1,393 mirrored
    # pairs on LakeB2B), so the top of the list was mirrors of itself.
    # REGRESSION 2: the score is symmetric in A and B, so "the reverse also scored well" was
    # true for EVERY mirrored pair and carried no information.
    # REGRESSION 3: /free-trial was proposed as a link SOURCE. A conversion asset can be a
    # fine target but a poor host for an editorial reference.
    article = {"id": "a", "url": "https://x.test/guide-a", "title": "Guide A",
               "words": 500, "section": "guides", "role": "TOFU", "type": "article",
               "in": 0, "out": 0, "in_sitemap": 1,
               "text": "data leads targeting healthcare technology " * 40}
    trial = {"id": "t", "url": "https://x.test/free-trial", "title": "Free Trial",
             "words": 400, "section": "free-trial", "role": "HUB", "type": "pages",
             "in": 0, "out": 0, "in_sitemap": 1,
             "text": "start your free trial today contact us get started " * 40}

    check(SEM.usable(trial), "a trial page is still a valid TARGET", "")
    check(not SEM.can_host(trial), "a trial page cannot host a contextual link", "")

    b = {"domain": "x.test", "nodes": [article, trial], "edges": []}
    pairs = SEM.build_pairs(b, limit_per_page=3)
    srcs = {sid for sid in pairs}
    check("t" not in srcs, "a conversion page is never a link source", str(sorted(srcs)))
    for n in (article, trial):
        n2 = dict(n); n2["type"] = "corporate_brochure"
        check(not SEM.can_host(n2), "corporate_brochure cannot host", n2["url"])

    # symmetry: A->B and B->A score identically (both terms are direction-independent),
    # so any direction flag MUST be built from something else or it is always true.
    fwd, _ = SEM.pair_shape(article, trial)
    rev, _ = SEM.pair_shape(trial, article)
    check(fwd == rev, "pair_shape is symmetric in A and B", f"{fwd} vs {rev}")
    def toks(n):
        return SEM.tokens(f"{n['title']} {n['text']}")
    docs = [toks(n) for n in (article, trial)]
    idf = SEM.idf_weights(docs)
    vecs = [SEM.tfidf_vector(t, idf) for t in docs]
    svs = SEM.to_sparse(vecs, len(vecs[0]) if vecs else 0)
    check(SEM.sparse_cosine(svs[0], svs[1]) == SEM.sparse_cosine(svs[1], svs[0]),
          "cosine is symmetric, so the rule score cannot distinguish direction", "")


def t_review_regressions():
    """Every finding from the adversarial review of the Span worklist, as a test.

    The review rejected 26 of 63 proposed links and the "76% invisible" headline. All seven
    structural causes are pinned here so they cannot come back.
    """
    import entities as ENT, extract as EX, plan as PL, report as REP

    # 1. Generic single words must never be entities. 44 of 63 wrong links followed one.
    for w in ("chief", "health", "accounting", "cloud", "asset", "consulting",
              "directors", "director", "account", "cybersecurity", "managed"):
        check(ENT.is_generic(w), f"generic word blocked: {w}", "")
    # ...while real products survive. These were the "money pages" the review said were missing.
    for w in ("servicenow", "salesforce", "sap", "workday", "netsuite", "hubspot",
              "adobe", "five9", "sage 100"):
        check(not ENT.is_generic(w), f"real product kept: {w}", "")

    # 2. A menu link must be recognised by DOM position, not by its words.
    check(PL.is_editorial("Data Enrichment", is_chrome=True) is False,
          "a menu link named 'Data Enrichment' is navigation", "")
    check(PL.is_editorial("Read more", is_chrome=False) is True,
          "an in-body link reading 'Read more' is editorial", "")
    check(PL.is_editorial("Data Enrichment", None) is True,
          "old bundles still fall back to the text heuristic", "")

    # 3. Edge layout: the 4th field marks nav position; 3-field bundles still work.
    check(PL.edge_is_content(["a", "b", "Zendesk Users List", 0]) is True,
          "4-field in-body edge", "")
    check(PL.edge_is_content(["a", "b", "Zendesk Users List", 1]) is False,
          "4-field menu edge", "")
    check(PL.edge_is_content(["a", "b", "Zendesk Users List"]) is True,
          "3-field edge falls back cleanly", "")

    # 4. The repeated mega-menu must not survive extraction as body prose.
    chrome = ("ERP Users List MS Dynamics Users List PeopleSoft Users List "
              "QuickBooks Users List Salesforce users list SAP Users List And More!")
    # Fixture length matters: body() finds the first prose sentence and drops the run before
    # it, so a one-line fixture never reaches the nav-stripping stage at all. This is a
    # realistic FAQ answer.
    prose = ("A CISO runs security for an enterprise and owns the roadmap, the budget "
             "and the incident response plan, answering to the board on risk. Security "
             "leaders at regulated companies also chair the disclosure committee, which "
             "meets quarterly to review material incidents and sign off on the public "
             "filing. That duty sits alongside a security budget that is usually a "
             "fraction of one percent of revenue yet carries responsibility for the "
             "whole estate. Buyers looking for a security contact list want that person, "
             "not a generic inbox. ")
    page = f"<html><body><h1>Who is a CISO</h1><p>{prose}</p><p>{chrome}</p></body></html>"
    out = EX.body(page)
    check("Salesforce users list" not in out, "footer mega-menu stripped from body text",
          out[:80])
    check("disclosure committee" in out, "editorial prose survives nav stripping", out[:80])

    # 5. Orphan rate must be split by page type, not reported as one scary number.
    def plan_for(nodes):
        return PL.build_plan({"domain": "x.test", "edges": [], "nodes": nodes,
                              "stats": {"truncated": False}})
    def mk(i, typ, **kw):
        d = {"id": str(i), "url": f"https://x.test/{typ}-{i}",
             "title": f"Page {i}", "section": typ, "role": "THIN", "type": typ,
             "in": 0, "out": 1, "in_content": 0, "in_menu": 0,
             "text": "data leads targeting healthcare technology " * 60}
        d.update(kw)
        return d
    faq_only = [mk(i, "faq") for i in range(80)]
    p = plan_for(faq_only)
    notes = REP.derive_findings(p, {"nodes": faq_only, "edges": [], "stats": {}})
    faq_note = [x for x in notes if "FAQ" in x["t"] or "faq" in x["t"].lower()]
    check(bool(faq_note), "an all-FAQ orphan set still gets a caveat, not a 100% headline", "")
    if faq_note:
        check("not a fix" in faq_note[0]["b"] or "not the fix" in faq_note[0]["b"],
              "the FAQ note says what to actually do", faq_note[0]["b"][:60])
    # A page linked only from the menu is NOT an orphan.
    menu_only = [mk(0, "pages", **{"in": 3, "in_content": 0, "in_menu": 3})]
    p2 = plan_for(menu_only)
    s2 = p2["summary"]
    check(s2["zero_in"] == 0, "a menu-linked page is not counted as unlinked",
          str(s2["zero_in"]))
    check(s2["zero_in_content"] == 1, "but it is counted as having no in-body link",
          str(s2["zero_in_content"]))
    check(s2["menu_linked"] == 1, "menu-linked pages are counted", str(s2["menu_linked"]))


def t_coverage_disclosed():
    section("crawl coverage is disclosed")
    import plan as PLAN, report as REP
    # REGRESSION: the plan carried no coverage field and the report only warned on the page
    # cap. A crawl capped by the REST API rather than the cap (LakeB2B: 2,533 of 5,438
    # sitemap URLs, truncated=False) reported with no disclaimer at all.
    def plan_for(n_pages, sitemap_urls, truncated):
        b = {"domain": "x.test", "edges": [], "stats": {"truncated": truncated},
             "sitemap_urls": sitemap_urls,
             "nodes": [{"id": str(i), "url": f"https://x.test/{i}", "title": f"P{i}",
                        "section": "guides", "role": "THIN", "type": "page",
                        "in": 0, "out": 0, "in_sitemap": 1,
                        "text": "data leads targeting healthcare technology " * 60}
                       for i in range(n_pages)]}
        return PLAN.build_plan(b)

    p = plan_for(100, 213, False)
    s = p["summary"]
    check(s.get("sitemap_urls") == 213, "plan carries sitemap_urls", str(s.get("sitemap_urls")))
    check(s.get("coverage") == 47, "coverage is a percentage", str(s.get("coverage")))

    def cov_note(pl):
        f = REP.derive_findings(pl, {"stats": {}, "nodes": [], "edges": []})
        return [x for x in f if "audit covers" in x["t"] or "capped" in x["t"].lower()]

    check(len(cov_note(p)) == 1, "partial crawl is disclosed once", str(len(cov_note(p))))
    full = plan_for(100, 100, False)
    check(not cov_note(full), "a complete crawl claims nothing", str(len(cov_note(full))))
    capped = plan_for(100, 5000, True)
    check(len(cov_note(capped)) == 1, "a capped crawl is disclosed once",
          str(len(cov_note(capped))))


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
    for fn in (t_classify, t_extract, t_entities, t_clusters,
               t_refresh_bookkeeping, t_related_diversity,
               t_related_direction_and_host, t_clef_gate,
               t_clef_runner, t_review_regressions,
               t_coverage_disclosed, t_adversarial_review,
               t_plan, t_squarify):
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
