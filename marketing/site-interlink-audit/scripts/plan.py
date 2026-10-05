#!/usr/bin/env python3
"""
Turn a crawl bundle into the three-layer plan for ANY site, with no per-client rules.

Pipeline: bundle -> entities -> funnel roles -> per-entity link plan -> scored worklist.

The plan is the same shape for every client:
  Layer 1  TOFU  research hub   (what it is, pros, cons, vs, reviews)   <- usually missing
  Layer 2  MOFU  comparison / guide  (vs-alikes, alternatives)            <- often thin
  Layer 3  BOFU  commercial list (users list, pricing, contact)          <- what exists
plus: inbound links from sibling pages, and unlinked mentions to convert.
"""
import json, re, collections, sys, math, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entities import build_clusters, count_mentions, STOP

# ---------------------------------------------------------------- scoring

NAV_ANCHOR = re.compile(
    r"^(read more|learn more|more|next|back|home|contact us|contact now|let'?s talk|"
    r"lets talk|talk to \w+|get a demo|request \w+|click here|view \w+|see more|"
    r"resources?|read \w+|submit|apply|download|subscribe|menu|homepage)$", re.I)


MENTION_CACHE = {}


def mention_strength(url, name):
    """
    How seriously a page discusses an entity: count whole-word occurrences in the body.
    0 = absent, 1 = single passing/facet mention, 2+ = editorial discussion worth linking.
    """
    key = (url, name)
    if key not in MENTION_CACHE:
        txt = TEXT_BY_URL.get(url) or ""
        if not txt:
            MENTION_CACHE[key] = 0
        else:
            words = [w for w in name.lower().split() if w not in STOP]
            if not words:
                MENTION_CACHE[key] = 0
            else:
                rx = re.compile(r"(?<![\w-])" + r"[\s\-]+".join(re.escape(w) for w in words)
                                + r"(?![\w-])", re.I)
                MENTION_CACHE[key] = len(rx.findall(txt))
    return MENTION_CACHE[key]


def is_editorial(anchor, is_chrome=None):
    """
    Is this an in-body link rather than a menu entry?

    The authoritative signal is DOM position, captured at crawl time as the fourth field of
    an edge. Anchor TEXT was the old test and it is wrong in both directions: it called the
    menu link "Data Enrichment" editorial because it is two capitalised words, and it called a
    real in-body citation reading "Read more" navigation. When DOM position is unavailable
    (an older bundle) fall back to the text heuristic rather than dropping the link.
    """
    if is_chrome is not None:
        return not is_chrome
    a = (anchor or "").strip()
    if not a:
        return False
    if NAV_ANCHOR.match(a):
        return False
    return len(a.split()) >= 2 or bool(re.search(r"[A-Z]", a))


def edge_is_content(edge):
    """
    Is this edge an in-body link?

    Edge layout is [src, dst, anchor, is_chrome]. Bundles crawled before the DOM-position
    change have only 3 fields, so fall back to the anchor-text heuristic for those instead
    of silently counting every menu link as an editorial one.
    """
    if len(edge) > 3:
        return not edge[3]
    return is_editorial(edge[2])


def norm_url(u):
    u = u.split("#")[0].rstrip("/")
    return re.sub(r"^https?://(www\.)?", "", u).lower()


def slug(u):
    tail = re.sub(r"^https?://[^/]+", "", u).rstrip("/").split("/")
    return tail[-1] if tail and tail[-1] else "/".join(tail)


def strip_type_tokens(toks):
    cut = len(toks)
    for i, t in enumerate(toks):
        if t in STOP:
            cut = i
            break
    return toks[:cut]


def entity_key(page_url):
    """The entity a page belongs to, or None if it is not an entity page."""
    s = slug(page_url).lower()
    if not s or s == "/":
        return None
    toks = [t for t in re.sub(r"\.(html?|php|aspx?)$", "", s).split("-") if t]
    if not toks:
        return None
    core = " ".join(strip_type_tokens(toks))
    return core or None


def page_is_faq(page_url):
    s = slug(page_url).lower()
    return s.startswith(("what", "who", "how", "why", "when", "which", "can", "do",
                         "does", "is", "are", "should", "will"))


TEXT_BY_URL = {}


# ---------------------------------------------------------------- the plan

# A page's URL is a stronger signal of what it is than its body copy. "Aviation Industry
# Mailing List" and "Zoho CRM Users List" are product pages that happen to be phrased like
# questions, so the text classifier called them TOFU and the Entities funnel bars were
# built on that. These overrides are path rules, not content rules.
ROLE_BY_PATH = (
    # a page that sells a list IS the commercial offer, whatever its copy sounds like
    (re.compile(r"/(technology-lists|healthcare-lists|industry-wise-lists|"
                r"geo-targeted-lists|professional-lists)/"), "BOFU"),
    (re.compile(r"-(users?-list|customers-list|email-list|email-database|"
                r"business-contacts|customers-list)$"), "BOFU"),
    (re.compile(r"/(services|solutions)/"), "BOFU"),
    # the blog is the research layer
    (re.compile(r"/blog/"), "TOFU"),
    (re.compile(r"/(guides?|white-paper|infographics?|case-studies)/"), "MID"),
)


def role_from_url(url, fallback):
    """Funnel role from URL shape. Falls back to the text classifier."""
    u = (url or "").lower()
    for pat, role in ROLE_BY_PATH:
        if pat.search(u):
            return role
    return fallback


def build_plan(bundle, max_links_per_page=3, redirects=None):
    """redirects: {normalized_url -> final_url} from the crawl. A proposed link that
    301s is wasted work and a canonical smell, so any target in that map is dropped and
    recorded in "redirecting_targets" for the report to show."""
    nodes = bundle["nodes"]
    # Normalise the redirect keys on the way in. Comparing a normalised hub URL against a
    # raw key silently never matched, so every redirecting target still reached the
    # worklist and the check looked like it was working.
    redirects = {norm_url(k): v for k, v in (redirects or {}).items()}
    bad_targets = set()
    for n in nodes:
        n["role"] = role_from_url(n.get("url"), n.get("role"))
        n["role_text"] = n.get("role")
    global TEXT_BY_URL
    TEXT_BY_URL = {n["url"]: (n.get("text") or "") for n in nodes}
    by_norm = {}
    for n in nodes:
        by_norm[norm_url(n["url"])] = n

    # ---- entity inventory ------------------------------------------------
    clusters, ents = build_clusters(bundle)

    # group name variants of the same brand: "sage 100", "sage 300", "sage 50" -> sage
    family = collections.defaultdict(set)
    for name in ents:
        root = name.split()[0]
        family[root].add(name)

    # ---- per-entity page assignment -------------------------------------
    pages_of = collections.defaultdict(list)
    for n in nodes:
        k = entity_key(n["url"])
        if not k:
            continue
        if k in ents:
            pages_of[k].append(n)
        else:
            # also attach "sage 100" pages to the "sage" family for rollup views
            root = k.split()[0]
            if root in family:
                pages_of[root].append(n)

    indeg = {n["id"]: n["in"] for n in nodes}

    # ---- adjacency for the entity graph ---------------------------------
    adj = collections.defaultdict(set)
    for e in bundle["edges"]:
        src, dst = e[0], e[1]
        if src in by_norm and dst in by_norm:
            a, b = norm_url(by_norm[src]["url"]), norm_url(by_norm[dst]["url"])
            adj[a].add(b)
            adj[b].add(a)

    rows = []
    for label, members, _ in clusters:
        for name in members:
            pset = {p["id"]: p for p in pages_of.get(name, [])}
            for p in pages_of.get(name, []):
                pset[p["id"]] = p

            role_counts = collections.Counter(p.get("role") for p in pset.values())
            tofu = [p for p in pset.values() if p.get("role") == "TOFU"]
            bofu = [p for p in pset.values() if p.get("role") == "BOFU"]
            mid = [p for p in pset.values() if p.get("role") in ("MID", "HUB")]
            def any_gap(key):
                return any(bool(p.get("gaps", {}).get(key)) for p in pset.values())
            has_pros = any_gap("pros")
            has_cons = any_gap("cons")
            has_cmp = any_gap("comparison")
            has_alt = any_gap("alternatives")
            has_review = any_gap("reviews") or any_gap("review")
            faq_pages = [p for p in pset.values() if page_is_faq(p["url"])]

            inbound = sum(p["in"] for p in pset.values())
            stranded = sum(1 for p in pset.values() if p["in"] == 0)
            mentions = len(ents.get(name, ()))

            rows.append({
                "entity": name,
                "cluster": label,
                "pages": len(pset),
                "faq": len(faq_pages),
                "tofu": len(tofu),
                "mofu": len(mid),
                "bofu": len(bofu),
                "inbound": inbound,
                "stranded": stranded,
                "mentions": mentions,
                "gaps": sorted({g for p in pset.values() for g, v
                                in (p.get("gaps") or {}).items() if v is True}),
                "hub": (sorted(pset.values(), key=lambda p: -p["in"])[0]["url"]
                        if pset else None),
            })

    # ---- per-page link worklist -----------------------------------------
    # A link is worth suggesting when the page TALKS about an entity but does not link
    # to it. That is the one interlink that is obviously missing and obviously useful.
    edges_by_src = collections.defaultdict(set)
    for e in bundle["edges"]:
        edges_by_src[e[0]].add(e[1])

    # Anchors like "Read more", "Let\'s Talk", "Resources" are navigation. An anchor that
    # names the target ("Zendesk Users List") is editorial and is what a reader follows.


    work = []
    ent_names = set(ents)
    # mention sets are needed per entity; build once
    ent_pages = {nm: set(ents[nm]) for nm in ent_names}

    for n in nodes:
        # Only editorial pages are worth editing. A hub index or an existing list page is
        # where links belong, not where they are missing.
        if n.get("role") not in ("MID", "TOFU") or n.get("in", 0) < 1:
            continue
        if page_is_faq(n["url"]):
            continue

        linked = edges_by_src.get(n["id"], set())
        linked_keys = set()
        for u in linked:
            k = entity_key(u)
            if k:
                linked_keys.add(k)
                linked_keys.add(k.split()[0])

        cands = []
        for name in ent_names:
            if name in linked_keys or name.split()[0] in linked_keys:
                continue
            if n["id"] not in ent_pages[name]:
                continue
            # require substantive editorial usage, not a single facet label
            if mention_strength(n["url"], name) < 2:
                continue
            cands.append(name)
        if not cands:
            continue

        # rank: prefer entities with more pages (more valuable targets) and closer in
        # topic (share the page's section)
        sec = n.get("section")
        scored = []
        for name in cands:
            tgt = pages_of.get(name, [])
            hub_pages = sorted(tgt, key=lambda p: -p["in"])
            hub = hub_pages[0] if hub_pages else None
            if not hub:
                continue
            same_sec = 1.5 if hub.get("section") == sec else 1.0
            val = (len(tgt) ** 0.5) * same_sec
            scored.append((val, name, hub))
        scored.sort(reverse=True)

        picks = []
        redirected = []
        for val, name, hub in scored[:max_links_per_page]:
            if norm_url(hub["url"]) == norm_url(n["url"]):
                continue
            # A proposed link that 301s is wasted editor time and a canonical smell.
            if norm_url(hub["url"]) in redirects:
                redirected.append(hub["url"])
                continue
            # An adversarial review found the worklist feeding pages that were already well
            # linked (median 51 inbound) while the real orphans got nothing. Prefer a target
            # nobody links to: adding a link to a page with 200 inbound changes almost
            # nothing, and one to an orphan is the whole point.
            hub_in = hub.get("in", 0)
            val = val * (3.0 if hub_in == 0 else (1.0 if hub_in <= 10 else 0.35))
            picks.append({
                "target": name,
                "url": hub["url"],
                "why": ("same section, %d %s under this entity"
                        % (len(pages_of[name]),
                           "page" if len(pages_of[name]) == 1 else "pages")
                        if hub.get("section") == sec else "entity already discussed here"),
                "val": round(val, 2),
            })
        if redirected:
            bad_targets.update(redirected)
        if picks:
            picks.sort(key=lambda p: -p["val"])
            work.append({
                "url": n["url"],
                "title": n.get("title", ""),
                "role": n.get("role"),
                "section": sec,
                "role_secondary": n.get("roles"),
                "in": n["in"],
                "out": n["out"],
                "links": picks,
            })

    # score the worklist: a page with high inbound and zero outlinks is the best edit
    for w in work:
        impact = (1 + math.log1p(w["in"])) * len(w["links"])
        w["score"] = round(impact, 2)

    work.sort(key=lambda w: -w["score"])

    # ---- site-level summary --------------------------------------------
    roles = collections.Counter(n.get("role") for n in nodes)
    summary = {
        "pages": len(nodes),
        "edges": len(bundle["edges"]),
        # An edge's 4th field is 1 when the link sits in nav/header/footer. Older bundles
        # have only 3 fields, so fall back to the anchor-text heuristic for those.
        "contextual_edges": sum(1 for e in bundle["edges"] if edge_is_content(e)),
        # Two different facts, previously conflated into one scary number.
        #   zero_in        = nobody links it at all, from anywhere
        #   zero_in_content = linked only from a menu, so no in-body path to it
        "zero_in": sum(1 for n in nodes if n["in"] == 0),
        # An adversarial review of the Span report found the "76% of the site is invisible"
        # headline was almost entirely /faq/ pages: 2,036 of 2,434 orphans were FAQ, and
        # Ahrefs showed the folder with zero organic traffic. Quoting 76% invited a plan to
        # "fix" 2,036 pages that should not exist. Report the all-pages figure AND the
        # figure with the low-value folder removed, so the headline cannot mislead.
        "redirecting_targets": sorted(bad_targets),
        "faq_pages": sum(1 for n in nodes if "/faq/" in n["url"]),
        "zero_in_ex_faq": sum(1 for n in nodes
                               if n["in"] == 0 and "/faq/" not in n["url"]),
        "pages_ex_faq": sum(1 for n in nodes if "/faq/" not in n["url"]),
        "zero_in_content": sum(
            1 for n in nodes if n.get("in_content", n["in"]) == 0),
        "menu_linked": sum(1 for n in nodes if n.get("in_menu", 0) > 0),
        "zero_out": sum(1 for n in nodes if n["out"] == 0),
        "in_sitemap": sum(1 for n in nodes if n.get("in_sitemap")),
        "roles": dict(roles),
        "entities": len(ents),
        "clusters": len(clusters),
        "work_pages": len(work),
        "work_links": sum(len(w["links"]) for w in work),
        "no_tofu": sum(1 for r in rows if r["tofu"] == 0 and r["bofu"] > 0),
        "faq_unsold": sum(r["faq"] for r in rows),
        # Coverage. `truncated` only covers the page cap; a crawl can also be partial
        # because the REST API exposes fewer objects than the sitemap lists. LakeB2B
        # fetched 2,533 of 5,438 sitemap URLs and nothing in the report said so.
        "sitemap_urls": bundle.get("sitemap_urls") or 0,
        "cap": bundle.get("cap") or 0,
        "truncated": bool(bundle.get("truncated")),
        "coverage": (round(100 * len(nodes) / bundle["sitemap_urls"])
                     if bundle.get("sitemap_urls") else None),
    }
    return {"summary": summary, "entities": rows, "work": work,
            "clusters": [{"label": l, "members": m} for l, m, _ in clusters]}


if __name__ == "__main__":
    path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else path.replace(".json", "-plan.json")
    bundle = json.load(open(path))
    plan = build_plan(bundle)
    json.dump(plan, open(out, "w"))
    s = plan["summary"]
    print(f"{os.path.basename(path)}")
    for k, v in s.items():
        print(f"   {k:20s} {v}")
    print(f"-> {out}")