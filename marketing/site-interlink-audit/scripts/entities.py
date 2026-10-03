#!/usr/bin/env python3
"""
Cluster a site's pages into topical entity groups, with no site-specific rules.

Instead of hardcoding "CRM" and "ERP" for one client, learn the groups from the site:
  1. pull candidate entities from URL segments and page titles
  2. score each entity by how many pages mention it (word-boundary, slug-aware)
  3. group entities that co-occur on the same pages more often than chance
  4. label each cluster from the entities that define it

This is the part that makes the tool reusable across unrelated verticals.
"""
import re, collections, itertools, math

# words that are page-type furniture, never an entity
STOP = {
    "users", "user", "list", "lists", "customers", "customer", "companies", "company",
    "contacts", "contact", "email", "emails", "leads", "lead", "data", "database",
    "databases", "directory", "records", "record", "info", "information", "page",
    "pages", "the", "and", "for", "of", "in", "to", "a", "an", "all", "best", "top",
    "new", "free", "online", "download", "software", "system", "systems", "service",
    "services", "solution", "solutions", "business", "b2b", "b2b2c", "industry",
    "industries", "market", "intelligence", "enrichment", "profiling", "verification",
    "cleansing", "append", "targeted", "verified", "sample", "request", "quote",
    # editorial/noun furniture that is not an entity
    "vs", "guide", "guides", "strategy", "strategies", "tips", "trends",
    "template", "templates", "course", "courses", "lesson", "lessons",
    "insights", "insight", "academy", "magazine", "playbook", "checklist",
    "what", "why", "how", "when", "which", "who", "does", "can", "do",
    "analytics", "management", "operations", "performance", "automation",
    "generation", "building", "building-tools", "outreach", "prospecting",
    "pricing", "plans", "plan", "vs", "com", "www", "index", "home", "about", "blog",
    "news", "guide", "guides", "resource", "resources", "case", "studies", "faq",
    "webinar", "whitepaper", "white", "paper", "brochure", "capability", "capabilities",
    "tool", "tools", "marketing", "sale", "selling", "team", "teams", "sign", "up",
    "united", "states", "usa", "uk", "canada", "india", "australia", "europe", "asia",
    "worldwide", "global", "niche", "wide", "specific", "custom", "various", "different",
}

ENTITY_MIN_PAGES = 3     # below this it is noise, not a hub
MAX_ENTITIES = 60        # keep the report readable


# A slug that reads as a question is FAQ furniture, not an entity.
QUESTION = re.compile(r"^(what|who|why|how|when|where|which|can|do|does|is|are|will|"
                      r"should|would|could)\b", re.I)


def looks_like_question(slug):
    w = slug.replace("-", " ").split()
    if not w:
        return True
    return bool(QUESTION.match(w[0]))

STOP |= {
    # navigation and service chrome that survived the first filter
    "our", "your", "we", "us", "they", "it", "this", "that", "who", "what", "how",
    "get", "set", "see", "read", "view", "show", "more", "less", "next", "back",
    "clients", "clientele", "become", "reseller", "resellers", "partner", "partners",
    "talk", "connect", "contacted", "buy", "purchase", "order", "shipping", "delivery",
    "medical", "healthcare", "legal", "physician", "physicians", "dental", "dentist",
    "digital", "channel", "channels", "president", "event", "events", "professional",
    "professionals", "corporate", "company", "enterprise", "startup", "startups",
    "segment", "segments", "big", "small", "medium", "large", "social", "content",
    "privacy", "policy", "terms", "contacted", "big", "totally", "addressable",
}
# very common lowercase words are chrome even when they look like products
GENERIC_LOWER = {"our", "our", "social", "big", "buy", "talk", "become", "content",
                 "medical", "privacy", "connect", "segment", "corporate", "digital"}


# Bare common nouns that describe site FURNITURE, not a topic. Having a page for "total"
# does not make "total" an entity worth cross-linking.
FURNITURE = {
    "total", "datasets", "mailing", "write", "search", "articles", "testimonials",
    "infographics", "reduce", "refund", "field", "cross", "double", "reach", "get",
    "request", "free", "sample", "compare", "compare your data", "resources", "guide",
    "whitepaper", "case study", "case studies", "industry", "industries", "sector",
    "company", "companies", "business", "contact", "contact us", "thank you page",
    "success", "customer", "customers", "client", "clients", "directory", "list",
    "lists", "index", "home", "about", "careers", "team", "teams", "changelog",
    "integrations", "security", "privacy", "terms", "cookie", "legal", "compliance",
    # page-type residue that survives the STOP list
    "video", "setting", "settings", "meeting", "meetings", "brand", "gallery",
    "appending", "append", "demand", "research", "testing", "test", "documents",
    "document", "development", "document", "appointment", "appointments",
    "advertising", "advertise", "banner", "banners", "button", "buttons",
    "campaign", "campaigns", "creative", "creatives", "creative services",
    "design", "designs", "designer", "hosting", "host", "domain", "domains",
    "seo", "sem", "ppc", "cpc", "banner", "social media", "social", "display",
    "affiliate", "affiliates", "partners", "partner", "resellers", "reseller",
    "vendors", "vendor", "suppliers", "supplier", "clients", "client",
    "process", "processes", "steps", "tips", "tricks", "ideas", "examples",
    "checklist", "templates", "template", "calculator", "calculators",
    "pricing plans", "plans", "plan", "enterprise", "starter", "professional",
    "university", "college", "school", "schools", "course", "training",
}

# Roles and verticals that are legitimately sellable entities on this kind of site.
ENTITY_OK_ROLE = re.compile(
    r"^(chief|c[tofimjo]s?|cio|vps?|vp|director|manager|owner|president|founder|"
    r"ceo|cfo|cmo|cro|coo|cso|cpo|cro|hr|it|sales|marketing|operations|finance|"
    r"accounting|engineering|legal|nurse|physician|doctor|dentist|surgeon|therapist|"
    r"attorney|lawyer|contractor|employee|professional|technician|analyst|architect|"
    r"consultant|teacher|professor|instructor|student|investor|banker|broker|agent|"
    r"technologist|programmer|developer|designer|marketer|specialist|technician)$", re.I)


YEAR = re.compile(r"^(19|20)\d{2}$")


KNOWN_VERTICALS = {
    "healthcare", "technology", "finance", "manufacturing", "retail", "logistics",
    "hospitality", "education", "legal", "insurance", "nonprofits", "pharmaceutical",
    "biotechnology", "automotive", "construction", "realty", "telecommunications",
    "aerospace", "banking", "energy", "agriculture", "mining", "shipping", "oil",
    "venture", "startups", "saas", "ecommerce", "media", "publishing", "gaming",
}


VERB = {
    "ways", "convert", "learn", "build", "built", "grow", "get", "make", "use",
    "find", "choose", "compare", "improve", "increase", "reduce", "save", "scale",
    "write", "reads", "understand", "know", "start", "stop", "boost",
    "drive", "follow", "engaging", "engage", "track", "close",
    "generate", "target", "reach", "sell", "sellers", "working", "work", "works",
    # gerunds and abstract nouns: real words, never link targets
    "delivering", "expanding", "helping", "targeting", "managing", "creating",
    "building", "driving", "growing", "leading", "scaling", "solving",
    "beyond", "impact", "point", "points", "precise", "opportunities", "types",
    "benefits", "results", "outcomes", "insights", "trends", "tips", "tools",
    "options", "features", "advantages", "challenges", "solutions", "examples",
    "levels", "factors", "reasons", "steps", "ideas", "goals", "plans",
    "services", "solutions", "products", "packages", "pricing", "rates",
    # bare verbs / gerunds that marketing copy uses constantly
    "active", "complete", "getting", "manage", "future", "message", "cases",
    "landing", "skills", "reporting", "quality", "clicks", "mobile", "sending",
    "alternatives", "conversion", "pipeline", "segmentation", "nurture",
    "details", "overview", "summary", "guide", "guides", "reports", "reviews",
}

# a candidate that STARTS with a numeral or a how/what/why word is an article title
# Each alternative must match a WHOLE leading token. A bare "a" alternative matches every
# slug starting with the letter a, which threw away Adobe, Amazon, Apple, Asana, Atlassian
# and Alibaba. `(?:a|an)\b` anchors the article to the full word.
ARTICLE_START = re.compile(
    r"^(?:\d+|how|what|why|when|where|which|who|top|best|new|simple|easy|free|"
    r"the|a|an|my|our|your|guide|what's|whats|whats)\b", re.I)


def is_generic(name):
    if YEAR.match(name.strip()):
        return True
    first = name.strip().split()[0] if name.strip().split() else ""
    if ARTICLE_START.match(name.strip()):
        return True
    if first.lower() in VERB:
        return True
    if name.lower() in GENERIC_LOWER:
        return True
    if len(name) < 3:
        return True
    n = name.strip()
    if n.lower() in FURNITURE:
        return True
    if n in KNOWN_VERTICALS or ENTITY_OK_ROLE.match(n):
        return False
    # Case does NOT discriminate: slugs lowercase everything, so "netsuite" and
    # "technology" look identical by case. The reliable signals are the STOPWORD and
    # FURNITURE lists above, which is what decides this.
    return False


def candidate_entities(bundle):
    """
    Entities the site itself proposes. Two sources, both slug-based:
      - <brand>-users-list style slugs: the entity is everything before the page-type tail
      - <brand>-<verb> slugs inside a section, when the first token is not a question word
    Question-shaped slugs are skipped outright: 64 "what is" slugs are FAQ, not entities.
    """
    votes = collections.Counter()
    kind = collections.defaultdict(set)
    for n in bundle["nodes"]:
        seg = [s for s in re.sub(r"^https?://[^/]+", "", n["url"]).split("/") if s]
        if not seg:
            continue
        slug = re.sub(r"\.(html?|php|aspx?|pdf)$", "", seg[-1].lower())
        if not slug or looks_like_question(slug):
            continue
        parts = [p for p in slug.split("-") if p]
        if not parts:
            continue
        # find where the page-type tail begins, and take what precedes it
        cut = len(parts)
        had_tail = False
        for i, p in enumerate(parts):
            if p in STOP:
                cut = i
                had_tail = True
                break
        core = parts[:cut]
        if had_tail:
            if not core or len(core) > 4:
                continue
        else:
            # No type tail. Two shapes matter:
            #   "<section>-<subject>-..."  -> the subject after the section
            #   "x-vs-y"                   -> the competitor on the right
            if "vs" in parts:
                i = parts.index("vs")
                core = parts[i + 1:] or parts[:i]
            else:
                core = parts[1:] or parts
            if not core or len(core) > 3:
                continue
        name = " ".join(core)
        if len(name) < 3 or all(p in STOP for p in core):
            continue
        if is_generic(name):
            continue
        votes[name] += 1
        kind[name].add(n["section"])
    return votes


def count_mentions(nodes, entity):
    """Pages whose body text mentions the entity as whole words."""
    words = [w for w in entity.lower().split() if w not in STOP]
    if not words:
        return set()
    rx = re.compile(r"(?<![\w-])" + r"[\s\-]+".join(re.escape(w) for w in words) + r"(?![\w-])",
                    re.I)
    hits = set()
    for n in nodes:
        t = n.get("text") or ""
        if t and rx.search(t):
            hits.add(n["id"])
    return hits


def build_clusters(bundle, text_by_id=None):
    """
    Return [(label, [entities], {entity: pages})] plus a per-page entity index.
    Grouping is co-occurrence based: two brands that keep appearing together belong to
    the same competitive set, which is exactly the "related technologies" link rule.
    """
    nodes = bundle["nodes"]
    n_pages = max(len(nodes), 1)
    if text_by_id:
        for n in nodes:
            n["text"] = text_by_id.get(n["id"], n.get("text") or "")

    votes = candidate_entities(bundle)
    if not votes:
        return [], {}

    mention = {}
    for name in votes:
        pages = count_mentions(nodes, name)
        if len(pages) >= ENTITY_MIN_PAGES:
            mention[name] = pages

    # rank by pages that mention the entity but do NOT already link to a page about it:
    # an entity that is widely discussed and poorly linked is the highest-value target
    name_by_id = {}
    for name, pages in mention.items():
        for pid in pages:
            name_by_id.setdefault(pid, set()).add(name)

    indeg = {n["id"]: n["in"] for n in nodes}
    # How distinctive is this term? A term on 80% of pages is chrome or the site theme.
    share = {}
    for name, pages in mention.items():
        share[name] = len(pages) / n_pages

    def entity_like(name):
        """
        A hub is a proper noun: one token, an acronym, or a digit/space mix. Multi-word
        English phrases like "total addressable" or "reduce" are copy, not products.
        """
        w = name.split()
        if len(w) == 1:
            return len(w[0]) >= 4 and not w[0].islower() or len(w[0]) >= 5
        if len(w) == 2:
            # allow "sage 100", "salesforce crm" but not "total addressable"
            return any(x.isdigit() or x.isupper() or not x.islower() for x in w)
        return False

    # An entity is something the site has a page FOR. A word that is merely discussed often
    # ("research", "pipeline", "buyer") is a topic, not a hub, and must not become a link
    # target. Build the slug->page index first, then filter.
    slug_index = {}
    for nd in nodes:
        seg = [x for x in re.sub(r"^https?://[^/]+", "", nd["url"]).split("/") if x]
        if not seg:
            continue
        sl = re.sub(r"\.(html?|php|aspx?|pdf)$", "", seg[-1].lower())
        toks = [t for t in sl.split("-") if t]
        cut = len(toks)
        had_tail = False
        for j, t in enumerate(toks):
            if t in STOP:
                cut = j
                had_tail = True
                break
        if had_tail:
            core = " ".join(toks[:cut])
        elif "vs" in toks:
            i2 = toks.index("vs")
            core = " ".join(toks[i2 + 1:] or toks[:i2])
        else:
            core = " ".join(toks[1:] or toks)
        if core:
            slug_index.setdefault(core.strip(), []).append(nd)
            # also index the full slug, so "ai-research" registers under its own name
            # rather than only under the stripped core

    scored = []
    for name, pages in mention.items():
        if not entity_like(name):
            continue
        # A single common word appearing on a large share of the site is the theme or the
        # brand, not a link target. Multi-word proper nouns ("sage 100", "fortune 500") are
        # never the site theme, so they are exempt.
        if len(name.split()) == 1 and share.get(name, 1.0) > 0.40:
            continue
        if len(name.split()) == 2 and share.get(name, 1.0) > 0.60:
            continue
        owned = slug_index.get(name.strip(), [])
        if not owned:
            continue
        discussed = len(pages)
        stranded = sum(1 for p in pages if indeg.get(p, 0) == 0)
        # owning a hub page is the strongest signal there is
        hub_bonus = 40 if owned else 0
        # specificity: mention count alone ranks "technology" above "servicenow". Reward
        # names that read as products (mixed case, acronym, digit, or multi-token proper
        # nouns) and damp ones that are plain common words.
        w = name.split()
        # multiplier in [0.15, 4]: how much does this look like a product, not a common word
        mult = 1.0
        if any(c.isupper() for c in name[1:]): mult += 1.0        # Salesforce, Sage, Workday
        if any(ch.isdigit() for ch in name):  mult += 0.8         # Sage 100, Dynamics 365
        if len(w) > 1:                        mult += 0.5         # multi-token proper noun
        if all(x.islower() for x in w) and len(w) == 1:
            mult -= 0.85                                          # "technology", "cloud"
        mult = max(0.15, min(4.0, mult))
        scored.append(((discussed + stranded * 2 + hub_bonus) * mult, name, pages))
    scored.sort(key=lambda x: -x[0])
    keep = [x for x in scored[:MAX_ENTITIES]]
    entities = {name: set(pages) | {p["id"] for p in slug_index.get(name.strip(), [])}
               for _, name, pages in keep}

    # ---- competitor sets -------------------------------------------------
    # Co-occurrence alone groups anything that shares a service page (avaya + hospital).
    # A real competitive relationship needs each entity to have its own hub URL, and the two
    # hubs to sit in the same section. That is what a client would call "our competitors".
    hub_url = {}
    for nd in nodes:
        seg = [x for x in re.sub(r"^https?://[^/]+", "", nd["url"]).split("/") if x]
        if not seg:
            continue
        slug = re.sub(r"\.(html?|php|aspx?)$", "", seg[-1].lower())
        toks = [t for t in slug.split("-") if t]
        cut = len(toks)
        for j, t in enumerate(toks):
            if t in STOP:
                cut = j
                break
        core = " ".join(toks[:cut]).strip()
        if core and core not in hub_url:      # first page wins; slugs are unique enough
            hub_url[core] = nd

    def has_hub(nm):
        return nm.lower() in hub_url

    co = collections.defaultdict(set)
    names = list(entities)
    for a, b in itertools.combinations(names, 2):
        if not (has_hub(a) and has_hub(b)):
            continue
        sa = hub_url[a.lower()]["section"]
        sb = hub_url[b.lower()]["section"]
        if sa != sb:
            continue
        pa, pb = entities[a], entities[b]
        inter = len(pa & pb)
        if not inter:
            # rivals that never share a page are still rivals: same section + both hubs
            co[a].add(b); co[b].add(a)
            continue
        small, large = (a, b) if len(pa) <= len(pb) else (b, a)
        contain = inter / max(len(entities[small]), 1)
        if contain >= 0.45:
            co[a].add(b)
            co[b].add(a)

    # connected components, then label from the most-discussed member
    seen, clusters = set(), []
    for name in names:
        if name in seen:
            continue
        comp, stack = set(), [name]
        while stack:
            cur = stack.pop()
            if cur in comp:
                continue
            comp.add(cur)
            stack.extend(co.get(cur, ()))
        seen |= comp
        members = sorted(comp, key=lambda m: -len(entities[m]))
        if not members:
            continue
        if len(members) > 14:
            # Too broad to be ONE competitive set, but the entities are still real and
            # still need to appear as link targets. Dropping the component silently lost
            # 34 of 60 entities on a real site. Emit each member as its own singleton.
            for m in members:
                clusters.append((m.title(), [m], {m: entities[m]}))
            continue
        label = members[0].title()
        if len(members) > 1:
            label += f" +{len(members)-1}"
        clusters.append((label, members, {m: entities[m] for m in members}))
    clusters.sort(key=lambda c: -len(c[1]))
    return clusters, entities
