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

# Words that carry no topic on their own. A slug like "from-dormant-data-to-349k" yields
# "from" once the page-type tail is stripped, and without this it becomes an entity.
FUNCTION_WORD = {
    "from", "to", "for", "with", "without", "and", "or", "but", "not", "the", "a", "an",
    "of", "in", "on", "at", "by", "as", "is", "are", "was", "were", "be", "been", "it",
    "its", "this", "that", "these", "those", "we", "our", "us", "you", "your", "they",
    "them", "their", "he", "she", "his", "her", "how", "why", "what", "when", "where",
    "who", "which", "can", "will", "should", "would", "could", "may", "into", "over",
    "under", "about", "after", "before", "than", "then", "there", "here", "all", "any",
    "some", "each", "more", "most", "less", "least", "very", "just", "only", "also",
    "via", "per", "up", "down", "out", "off", "again", "once", "ever", "never", "one",
    "two", "new", "best", "top", "how-to", "step", "steps", "guide", "using", "use",
}

ENTITY_MIN_PAGES = 3     # below this it is noise, not a hub
MAX_ENTITIES = 60        # keep the report readable
# One cluster must not eat the whole budget. A geography theme ("Netherlands +12") consumed
# 12 of 60 slots on the Span audit, which is how ServiceNow, Salesforce, AWS, SAP and
# Workday were crowded out of the entity set despite owning pages and driving revenue.
# Cap members per cluster; the report lists the largest members anyway.
MAX_CLUSTER_MEMBERS = 6

# An adversarial review of the Span worklist found 44 of 63 proposed links matched an
# ordinary English word rather than a topic: "chief" pulled ADP Payroll to Chief Medical
# Officers, "directors" matched "directory", "health" sent Meditech to a consumer Health and
# Wellness list. A word that names no organisation, place or product cannot be an entity, and
# no site-specific list can be exhaustive, so this is a general blocklist. Proper nouns that
# merely collide with a word are unaffected: only the bare lowercase form is blocked.
GENERIC_WORD = {
    # job titles and org structure
    "chief", "director", "directors", "officer", "officers", "executive", "executives",
    "president", "manager", "managers", "owner", "owners", "founder", "founders",
    "staff", "team", "teams", "employee", "employees", "senior", "junior",
    "lead", "leader", "leadership", "role", "roles", "title", "titles", "job", "jobs",
    "board", "member", "members", "head", "ceo", "cfo", "cio", "cmo", "cto", "coo",
    "president", "chairman", "chairwoman", "supervisor", "administrator",
    # generic business and technical vocabulary
    "account", "accounts", "accounting", "cloud", "asset", "assets", "managed",
    "consulting", "consultant", "consultants", "advisory", "application",
    "applications", "app", "computer", "computers", "network", "networks",
    "software", "hardware", "security", "secure", "cyber", "cybersecurity",
    "repository", "file", "files", "document", "documents", "content", "media",
    "channel", "channels", "campaign", "campaigns", "program", "programs",
    "project", "projects", "growth", "value", "values", "success", "quality",
    "results", "knowledge", "experience", "expertise", "support", "health",
    "healthy", "wellness", "care", "medical", "clinical", "financial", "finance",
    "legal", "compliance", "government", "public", "private", "buyer", "buyers",
    "partner", "partners", "vendor", "vendors", "supplier", "suppliers",
    "provider", "providers", "enterprise", "enterprises", "organization",
    "organizations", "organisation", "organisations", "general", "specific",
    "various", "different", "other", "others", "more", "most", "first", "last",
    "next", "previous", "current", "recent", "latest", "early", "high", "low",
    "medium", "large", "small", "major", "minor", "main", "global", "worldwide",
    "industry", "industries", "market", "sector", "vertical", "segment",
    "process", "processes", "tool", "tools", "product", "products", "platform",
    "platforms", "service", "services", "solution", "solutions", "technology",
    "technologies", "tech", "system", "systems", "database", "databases",
    "intelligence", "analytics", "analysis", "reporting", "directory", "record",
    "records", "customer", "customers", "client", "clients", "user", "users",
    "business", "company", "companies", "management", "strategy", "strategies",
    "insight", "insights", "performance", "marketing", "outreach", "automation",
    # courtesy, UI and fragment words. A second review round found these reaching the
    # worklist as link targets: "thanks" owns /thanks and recurs on 31 pages, "click"
    # owns nothing but matches CTA copy, and "key" matched the SurveyMonkey page.
    "thanks", "thank", "welcome", "regards", "sincerely", "click", "here", "learn",
    "key", "keys", "core", "point", "points", "link", "links", "item", "items",
    "explore", "discover", "browse", "viewall", "readmore", "continue", "begin",
}


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
    # courtesy and UI words. "thanks" owns /thanks, passes the length test and recurs on
    # 31 pages of a real site, so it became a link target for half the worklist.
    "thanks", "thank", "welcome", "regards", "sincerely", "click", "here", "learn",
    # "key" matched the SurveyMonkey page and became a link target. An ordinary noun that
    # is only ever a fragment of another brand's name.
    "key", "keys", "core", "point", "points", "link", "links", "item", "items",
    "explore", "discover", "browse", "viewall", "readmore", "continue", "begin",
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
    if name.lower() in GENERIC_LOWER or name.lower() in GENERIC_WORD:
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


# A page only counts as an entity's hub if it is a real destination for that topic.
# Everything here was letting junk be treated as owned: a question-shaped FAQ slug
# (/faq/who-can-benefit-from-this-list became the entity "from"), a vendor page that
# merely contains the word (the SurveyMonkey page claimed "key"), a utility page
# (/thanks, /web-testing, /webinars) and an append service.
NOT_A_HUB_SECTION = {
    "faq", "white-paper", "infographic", "guide", "case-studies", "resource",
    "corporate_brochure", "home_slider", "marketing_tool", "our_capability",
    "process_document", "testimonial", "client", "blog", "segment", "segment_2",
    "gdpr_2", "tech_logo_1", "technographic_2", "blogs_right_side",
    "person_salesforce_cem", "main_bx", "thankyou", "thanks",
}
# path fragments that mark a utility or append page rather than a topic hub
NOT_A_HUB_PATH = (
    "/data-append/", "/thank", "/thanks", "/web-testing", "/webinar", "/thank-you",
    "/sitemap", "/wp-", "/feed", "/rss", "/privacy", "/terms", "/disclaimer",
    "/cookie", "/gdpr", "/author/", "/tag/", "/category/", "/page/",
)


def owns_a_hub(node):
    """Does this page stand for a topic, or is it furniture that happens to match?"""
    u = (node.get("url") or "").lower().rstrip("/")
    if not u:
        return False
    seg = [x for x in re.sub(r"^https?://[^/]+", "", u).split("/") if x]
    if not seg:
        return False
    # a question-shaped slug is an FAQ answer, never a topic hub
    slug = re.sub(r"\.(html?|php|aspx?|pdf)$", "", seg[-1].lower())
    if looks_like_question(slug):
        return False
    # Section names arrive hyphenated, underscored or spaced depending on the theme, so
    # normalise before comparing. The corporate brochure compared "corporate_brochure"
    # against "corporate-brochure", never matched, and let the site's own brand page
    # qualify as a hub for itself.
    sec = re.sub(r"[\s_-]+", "_", (node.get("section") or "").strip().lower())
    if sec in NOT_A_HUB_SECTION:
        return False
    if any(p in u for p in NOT_A_HUB_PATH):
        return False
    # a bare utility page like /thanks or /web-testing: the whole slug is the path, and
    # the slug is not a topic. Require the leaf slug to actually name something.
    leaf = seg[-1].lower()
    if leaf in ("thanks", "thank-you", "thankyou", "web-testing", "web-testing-tools",
                "testimonials", "contact", "about", "contact-us", "about-us"):
        return False
    if len(seg) <= 2 and len(leaf) < 4:
        return False
    # the site is not its own entity
    if len(seg) <= 1:
        return False
    return True


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
        # Ownership, computed up front, is the exemption from every filter below. It must
        # mean "this name owns a HUB page", not "the string appears somewhere in a URL".
        # An adversarial review round two found the looser version let junk through: "from"
        # owned /faq/who-can-benefit-from-this-list, "key" owned the SurveyMonkey page,
        # "thanks" owned /thanks, and those three alone made up half the worklist. A name
        # that only appears in a question-shaped FAQ slug, a thank-you page or an append
        # service owns nothing.
        owned_early = [nd for nd in slug_index.get(name.strip(), []) if owns_a_hub(nd)]
        # The shape heuristic is a guess about words; ownership is evidence. "aws" and "sap"
        # are three-letter acronyms, which the length rule rejected outright, yet
        # /technology-lists/sap-users-list and complete-aws are two of the highest-traffic
        # technology pages on the site. A name that owns a product page is a product.
        # An ordinary English word is not an entity at all, whatever it owns. "thanks"
        # passed the shape test on length alone and then qualified on 31 pages.
        if name.strip().lower() in GENERIC_WORD:
            continue
        # The site is not one of its own topics. "sgs" owns the corporate brochure page,
        # appears on every page, and proposed /corporate-brochure/sgs-corporate-brochure
        # as a link target for the lead cost calculator.
        # the bundle records the host, and a site's short brand is not always its domain
        # stem ("spanglobalservices" versus the SGS in its own logo), so accept both plus
        # any acronym the host initialises to.
        host = re.sub(r"^www\.", "", (bundle.get("host") or bundle.get("domain") or "")).lower()
        stem = host.split(".")[0]
        self_names = {stem, stem.replace("-", ""), stem.replace("-", " ")}
        head = re.sub(r"[^a-z]", "", stem)
        if 3 <= len(head) <= 6:
            self_names.add(head)          # spanglobalservices -> sgs
        if name.strip().lower() in self_names:
            continue
        # Function words are never a topic, whatever page they came from. Splitting
        # /case-studies/from-dormant-data-to-349k-in-revenue on hyphens leaves "from",
        # which then owned that case study and was proposed as a link target for 9 pages.
        if name.strip().lower() in FUNCTION_WORD:
            continue
        if not entity_like(name) and not owned_early:
            continue
        # A single common word appearing on a large share of the site is usually the theme
        # or the brand. But an adversarial review of the Span report found the opposite
        # failure: ServiceNow, Salesforce, AWS, SAP, Workday and Microsoft Dynamics, the
        # pages that drive revenue, were all missing from the entity set while long-tail
        # single words survived. AWS sits on 58% of pages and SAP on 63%, so the share test
        # deleted exactly the money pages. The exemption is ownership: a name with its own
        # product page is a hub regardless of how often the word appears, because a footer
        # menu mentioning it everywhere is not the same as it being the site theme.
        owned_early = slug_index.get(name.strip(), [])
        if len(name.split()) == 1 and share.get(name, 1.0) > 0.40 \
                and not owned_early:
            continue
        # A single ordinary English word is not an entity, however often it appears.
        w0 = name.split()
        # Distinctiveness must hold for EVERY name, not only two-word ones. The old test
        # only ran for `len(name.split()) == 2`, so "chief" on 40% of pages sailed through
        # while a two-word phrase with the same share was dropped.
        if share.get(name, 1.0) > 0.60 and len(w0) >= 1 and not owned_early:
            continue
        # Case cannot be the test: slugs lowercase everything, so "servicenow" and "chief"
        # look identical here. What separates them is whether the name OWNS a page. A product
        # has "/technology-lists/servicenow-users-list"; "chief" owns nothing and only ever
        # appears inside a job-title list on someone else's page. slug_index already encodes
        # this, so rely on it rather than on a heuristic.
        owned = owned_early
        if not owned:
            continue
        discussed = len(pages)
        stranded = sum(1 for p in pages if indeg.get(p, 0) == 0)
        # owning a hub page is the strongest signal there is
        hub_bonus = 40 if owned else 0
        # specificity: mention count alone ranks "technology" above "servicenow". Reward
        # names that read as products (multi-token, or carrying a digit) and damp ones that
        # are plain single words.
        w = name.split()
        # multiplier in [0.15, 4]: how much does this look like a product, not a common word
        mult = 1.0
        if any(ch.isdigit() for ch in name):  mult += 0.8         # Sage 100, Dynamics 365
        if len(w) > 1:                        mult += 0.5         # multi-token proper noun
        if len(w) == 1:
            # A lowercase single word is only a real product if it OWNS a page. Slugs are
            # lowercase, so "servicenow" is indistinguishable from "chief" on case alone; what
            # separates them is that one has /technology-lists/servicenow-users-list and the
            # other owns nothing. The old flat -0.85 punished both, which is why ServiceNow,
            # Salesforce, SAP and Workday never survived the cut while long-tail single words
            # did.
            if owned:
                mult += 0.9                                       # a product with its own page
            else:
                mult -= 0.85                                      # a word in passing copy
        mult = max(0.15, min(4.0, mult))
        scored.append(((discussed + stranded * 2 + hub_bonus) * mult, name, pages))
    scored.sort(key=lambda x: -x[0])
    keep = scored[:MAX_ENTITIES]
    # Every entity that owns a product page earns a slot, whatever its score. The Span audit
    # dropped AWS, SAP, Workday, Five9 and VMware from the entity set because the cap was
    # filled by a geography cluster and long-tail topics. A page that sells a product is
    # never optional, so owned names are promoted past the cap instead of being discarded.
    if len(keep) < len(scored):
        chosen = {n for _, n, _ in keep}
        promoted = [x for x in scored if x[1] not in chosen and slug_index.get(x[1].strip(), [])]
        if promoted:
            keep = keep + promoted
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
        # A component wider than this is one theme (a geography set, a product family), not
        # a competitive set. Emit the capped members as ONE labelled cluster and every
        # remaining member as its own singleton, so no entity is ever dropped: the earlier
        # silent truncation lost 34 of 60 entities on a real site, and truncating without
        # singletons loses them again. The cap still stops one theme from monopolising the
        # cluster list, which is what crowded the money pages out of the entity budget.
        if len(members) > MAX_CLUSTER_MEMBERS:
            head = members[:MAX_CLUSTER_MEMBERS]
            label = head[0].title() + f" +{len(head)-1}"
            clusters.append((label, head, {m: entities[m] for m in head}))
            for m in members[MAX_CLUSTER_MEMBERS:]:
                clusters.append((m.title(), [m], {m: entities[m]}))
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
