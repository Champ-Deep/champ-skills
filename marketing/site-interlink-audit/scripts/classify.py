#!/usr/bin/env python3
"""
Classify any site's pages by funnel role and content type, with no site-specific rules.

The method: read the page's own text and look for the signals that actually distinguish
  TOFU  an informational page that answers a question   (what is, how to, guide, comparison)
  MID   a page that explains an approach               (solutions, use cases, industries)
  BOFU  a page that asks for the sale                  (contact, demo, pricing, buy, sample)
  HUB   a page that exists to route people onward       (index, category, all lists)
These are content signals, not URL guesses, because URL conventions differ per platform.
"""
import re

TOFU = [
    ("what is", r"\bwhat\s+is\b|\bwhat\s+are\b|\bmeaning of\b|\bdefinition\b"),
    ("how to", r"\bhow to\b|\bhow do\b|\bhow does\b|\bsteps?\b|\btutorial\b|\bguide\b"),
    ("comparison", r"\bvs\.?\b|\bversus\b|\bcompared to\b|\bcomparison\b|\balternative"),
    ("pros cons", r"\bpros\b.{0,200}\bcons\b|\badvantages\b.{0,140}\bdisadvantages\b|"
                  r"\bpros and cons\b|\bstrengths\b.{0,140}\bweakness"),
    ("reviews", r"\breviews?\b|\bratings?\b|\btestimonial|\bwhat users say\b"),
    ("pricing explainer", r"\bpricing\b|\bcost\b|\bper seat\b|\bfree tier\b|\bplans?\b"),
    ("features", r"\bfeatures?\b|\bcapabilit|\bwhat.*\bincludes\b"),
]
MID = [
    ("use cases", r"\buse cases?\b|\bfor teams\b|\bfor sales\b|\bworkflow\b|\bsolution"),
    ("industries", r"\bindustr(?:y|ies)\b|\bfor financial services\b|\bfor healthcare\b|"
                   r"\bby team\b|\bby role\b"),
    ("integrations", r"\bintegrat|\bconnects? with\b|\bworks with\b|\bapi\b|\bplug-?in"),
    ("methodology", r"\bhow we\b|\bour approach\b|\bmethodolog|\bprocess\b|\bframework\b"),
    ("case studies", r"\bcase stud|\bcustomer stor|\bsuccess stor"),
]
BOFU = [
    ("contact cta", r"contact us|get a quote|request a quote|book a demo|get a demo|"
                    r"schedule a call|talk to (?:sales|an expert)"),
    ("trial signup", r"start (?:a )?free trial|sign up|get started|create (?:an?|your) account|"
                     r"free sample|request a sample|download the (?:sample|report)"),
    ("pricing table", r"\bpricing\b|\bplans?\b|\bper month\b|\bper user\b|\bchoose a plan\b"),
    ("record counts", r"\b\d[\d,]{2,}\+?\s*(?:records?|contacts?|leads?|users?|companies|"
                      r"profiles?|accounts?)\b|\bno\. of records\b"),
    ("money talk", r"\bminimum order\b|\bper contact\b|\bcredits?\b|\bquote\b|\baffordable\b"),
]
HUB = [("index", r"\ball\b|\bindex\b|\bbrowse\b|\beverything\b|\bdirectory\b|\blisting\b|\blibrary\b")]

INTENT = [("informational", r"\bwhat is\b|\bhow to\b|\bguide\b|\bwhy\b|\bmeaning\b"),
          ("commercial", r"\bpricing\b|\bbuy\b|\bdemo\b|\bcontact\b|\bfree trial\b")]

# CTA phrases. Every page's footer carries these, so presence alone proves nothing: what
# distinguishes a conversion page is how often they appear and how early.
CTA = re.compile(r"contact us|get a quote|request a quote|book a demo|get a demo|"
                 r"schedule a call|talk to (?:sales|an expert)|start (?:a )?free trial|"
                 r"sign ?up|get started|create (?:an?|your) account|free sample|"
                 r"request a sample|download the (?:sample|report)|choose a plan",
                 re.I)

# Where does the body actually end? Everything past the footer is chrome.
FOOTER = re.compile(r"(privacy policy|terms (?:of|&) (?:use|service)|cookie preferences|"
                    r"all rights reserved|do not sell|unsubscribe|©\s*\d{4})", re.I)


def body_portion(text):
    """Trim the shared footer so chrome cannot be mistaken for page content."""
    m = FOOTER.search(text)
    if m and m.start() > len(text) * 0.35:
        return text[:m.start()]
    return text


def cta_profile(text):
    """(count, first_position_ratio) for conversion CTAs in the real body."""
    hits = list(CTA.finditer(text))
    if not hits:
        return 0, 1.0
    first = hits[0].start() / max(len(text), 1)
    return len(hits), first


def classify(text, url=""):
    """
    Return {role: [signals]}. Roles are decided by signal STRENGTH, not presence:
      TOFU needs 2+ informational signals
      MID  needs 2+ solution/use-case signals
      BOFU needs CTA repetition or an early CTA, not a single footer mention
    """
    body = body_portion(text)
    roles = {}

    info = [n for n, rx in TOFU if re.search(rx, body, re.I | re.S)]
    sol = [n for n, rx in MID if re.search(rx, body, re.I | re.S)]
    if len(info) >= 2:
        roles["TOFU"] = info
    if len(sol) >= 2:
        roles["MID"] = sol

    n_cta, first = cta_profile(body)
    money = [n for n, rx in BOFU if n not in ("contact cta", "trial signup")
             and re.search(rx, body, re.I | re.S)]
    if n_cta >= 3 or (n_cta >= 1 and first < 0.12) or len(money) >= 2:
        roles["BOFU"] = (["contact cta"] if n_cta else []) + money

    hub = [n for n, rx in HUB if re.search(rx, body, re.I | re.S)]
    if hub:
        roles["HUB"] = hub
    return roles


def primary_role(roles):
    """
    Decide what a page is FOR. A comparison page is TOFU even when it carries CTAs, and a
    short product page is BOFU even when it explains features.
    """
    if "BOFU" in roles:
        # a strong editorial signal outranks a commercial one
        if len(roles.get("TOFU", [])) >= 3:
            return "TOFU"
        return "BOFU"
    for r in ("HUB", "MID", "TOFU"):
        if r in roles:
            return r
    return "THIN"


def score_page(roles):
    base = {"BOFU": 70, "HUB": 55, "MID": 60, "TOFU": 55, "THIN": 0}[primary_role(roles)]
    n = sum(len(v) for v in roles.values())
    return min(100, base + n * 4)


def content_type(url, h1=""):
    p = re.sub(r"^https?://[^/]+", "", url) or "/"
    seg = [s for s in p.split("/") if s]
    if not seg:
        return "home"
    head = seg[0]
    if head in ("blog", "news", "insights", "magazine", "resources", "guides", "academy"):
        return "content"
    if head in ("faq", "help", "support"):
        return "faq"
    if re.search(r"(users?|customers?|contacts?|companies|leads?)-(?:list|database)", p):
        return "entity-list"
    if re.search(r"\b(what-is|what-is-a|guides?|academy|academy/|learn)\b", p):
        return "educational"
    if re.search(r"\b(pricing|plans?|contact|demo|quote|trial|signup|sign-up)\b", head):
        return "conversion"
    if head in ("solutions", "use-cases", "industries", "products", "platform", "features"):
        return "solution"
    if re.search(r"\b(in|for)-[a-z-]+$", seg[-1]):
        return "variant"
    return head


def gap_signals(text):
    """Landing-page quality signals, measured on the body only."""
    body = body_portion(text)
    g = {}
    g["answers_first"] = bool(re.search(
        r"^.{0,400}?\b(what is|are you looking|everything you need|"
        r"\d[\d,]{2,}\+?\s*(?:records?|contacts?|leads?|users?|companies))", body[:600],
        re.I | re.S))
    g["trust"] = bool(re.search(
        r"\b(?:trusted by|clients?:|customers?:|\d[\d,]*\+?\s*(?:clients|customers|companies)|"
        r"case stud|testimonial|guarantee|certified|iso\s?27001|soc\s?2|gdpr|reviews?:)",
        body, re.I))
    g["proof_numbers"] = len(re.findall(r"\b\d[\d,]{2,}\+?\b", body))
    n_cta, first = cta_profile(body)
    g["cta_count"] = n_cta
    g["clear_cta"] = n_cta >= 1
    g["cta_early"] = first < 0.12
    g["faq_block"] = bool(re.search(r"frequently asked|\bfaq\b|questions? and answers",
                                    body, re.I))
    g["scannable"] = len(re.findall(r"\n<h[23]>\n", text, re.I))
    words = len(body.split())
    g["words"] = words
    g["fold_ok"] = 400 <= words <= 1300
    g["thin"] = words < 350
    return g


def landing_score(g):
    """0-100 composite, weighted for: answer first, then proof, then a way to act."""
    s = 0.0
    s += 26 if g["answers_first"] else 0
    s += 18 if g["trust"] else 0
    s += min(14, g["proof_numbers"] * 2.0)
    s += 10 if g["clear_cta"] else 0
    s += 8 if g["cta_early"] else 0
    s += 6 if g["faq_block"] else 0
    s += 10 if g["fold_ok"] else 0
    s += 8 if g["scannable"] >= 4 else (4 if g["scannable"] >= 2 else 0)
    return round(min(100, s), 1)
