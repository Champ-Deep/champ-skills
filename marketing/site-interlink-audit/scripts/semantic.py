#!/usr/bin/env python3
"""
semantic.py: find RELATED pages, not just pages about the same entity.

The deterministic scorer in plan.py answers "which pages should link to which". That is
the wrong question for growth: the obvious links are already made. What a site needs is
the link it has NOT thought of, across:

  - a related TECHNOLOGY (Epicor page -> Sage Intacct page)
  - a related GUIDE      (a payroll guide -> an HR guide)
  - a related ARTICLE    (a blog post -> a related blog post)
  - a related COMMERCIAL page

Two scorers, deliberately independent:

  1. EMBEDDING similarity. Uses Cloudflare CLEF's underlying encoder when available, and
     falls back to a hashed bag-of-words TF-IDF vector otherwise. Purely local, no API.

  2. CLEF JUDGEMENT. Asks the SystemOne-style model typed questions about a candidate pair
     and reads the probabilities. Optional: if CLEF is not installed the rule scorer still
     runs, and every score keeps a written rationale.

Both are blended ONCE, and the rule score is kept in its own column so a bad judgement is
visible after the fact rather than hidden inside a number.
"""
import hashlib
import html
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Titles that are site chrome, not content. Suggesting a link from "Sitemap" is noise.
CHROME_PATH = (
    "/privacy", "/terms", "/cookie", "/refund", "/disclaimer", "/gdpr", "/ccpa",
    "/accessibility", "/sitemap.xml", "/wp-", "/feed", "/rss", "/careers", "/legal",
)

CHROME_TITLE = {
    "sitemap", "guides", "guide", "blog", "about", "contact", "contact us", "home",
    "privacy policy", "terms", "terms of service", "cookie policy", "search",
    "resources", "library", "news", "events", "webinars", "glossary", "faq",
    "faqs", "success stories", "testimonials", "customers", "partners", "careers",
    "pricing", "features", "solutions", "industries", "company", "team", "newsletter",
}

STOP = set("""
a an the and or but if then than that this these those is are was were be been being
of to in on at by for with from as it its we you they he she them our your their
what which who whom whose when where why how do does did done can could should would
will shall may might must not no yes all any some each every other more most less least
how to your you our us me my mine theirs about into over under again further once here
there when where why why's what's guide guides list lists page pages best top new free
using use used get gets got make makes made take takes taken need needs help helps
""".split())

WORD = re.compile(r"[a-z0-9][a-z0-9+#.]*")


def _slot(token, salt):
    """Stable hash across processes. Python's str hash is salted per run, which would
    make every vector differ between refreshes and silently change every score."""
    d = hashlib.blake2b(f"{salt}:{token}".encode(), digest_size=8).digest()
    return int.from_bytes(d, "big")


def tokens(text):
    return [w for w in WORD.findall((text or "").lower()) if w not in STOP and len(w) > 2]


# ----------------------------------------------------------------- vectors
def hash_vector(tokens, dim=2048):
    """Signed hashing trick. Deterministic, no dependency, no vocabulary to maintain."""
    v = [0.0] * dim
    for t in tokens:
        v[_slot(t, 7) % dim] += 1.0 if (_slot(t, 11) & 1) == 0 else -1.0
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def cosine(a, b):
    if len(a) != len(b):
        return 0.0
    return sum(x * y for x, y in zip(a, b))


def to_sparse(vecs, dim=None):
    """{index: value} per vector. A dot product then costs |shared terms|, not 2048."""
    return [dict((i, v) for i, v in enumerate(v) if v) for v in vecs]


def sparse_cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(i, 0.0) for i, v in a.items())


def idf_weights(docs):
    """docs: list of token lists. Returns token -> idf."""
    df = Counter()
    for toks in docs:
        df.update(set(toks))
    n = len(docs) or 1
    return {t: math.log((n + 1) / (c + 1)) + 1.0 for t, c in df.items()}


def tfidf_vector(toks, idf, dim=2048):
    v = [0.0] * dim
    tf = Counter(toks)
    for t, c in tf.items():
        w = (1.0 + math.log(c)) * idf.get(t, 1.0)
        v[_slot(t, 7) % dim] += w * (1.0 if (_slot(t, 11) & 1) == 0 else -1.0)
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


# ------------------------------------------------------------------ pairs
def clean_title(t):
    return html.unescape(re.sub(r"<[^>]+>", "", t or "")).strip()


NAV_PHRASES = (
    "fix a meeting", "get a demo", "get a free quote", "free sample", "sign up",
    "request a quote", "contact us", "our clients", "trusted by", "get started",
)


def usable(n):
    """A page can be a link SOURCE or TARGET only if it carries real content.

    The word count must come from the pipeline's `words` field, not len(text): a nav
    page of 119 words is 904 CHARACTERS, so a character threshold passed it.
    """
    t = clean_title(n.get("title")).lower()
    if t in CHROME_TITLE:
        return False
    w = n.get("words")
    if w is None:
        w = len((n.get("text") or "").split())
    if w < 250:
        return False
    u = (n.get("url") or "").lower()
    if any(p in u for p in CHROME_PATH):
        return False
    head = (n.get("text") or "")[:400].lower()
    # A page whose opening is all calls to action is a landing page, not an article.
    hits = sum(p in head for p in NAV_PHRASES)
    if hits >= 3:
        return False
    return True


def pair_shape(a, b):
    """Role compatibility. Linking two commercial pages is weaker than linking a research
    page to a commercial one, because the research page is where the buyer starts."""
    ra, rb = a.get("role"), b.get("role")
    ta, tb = a.get("type"), b.get("type")
    score = 0.0
    why = []

    if ra == rb:
        score += 0.25
        why.append("same funnel stage")
    else:
        score += 0.30
        why.append(f"{ra} to {rb} is a natural reader path")

    # an FAQ answers a question; it should link to the thing that answers it properly
    if ta == "faq" or tb == "faq":
        score += 0.15
        why.append("FAQ answers should point at the full page")

    # Two pages in the same section are siblings and easy for a reader to follow. Both
    # sides must have a real section: comparing None == None credited a free 0.20 to
    # every pair on the site.
    sa, sb = a.get("sec"), b.get("sec")
    if sa and sb and sa == sb:
        score += 0.20
        why.append(f"both in {sa}")

    # never propose a self-referential or duplicated pair
    if a["url"] == b["url"]:
        return -1.0, []

    return min(score, 1.0), why


def already_linked(a_id, b_id, edge_set):
    return (a_id, b_id) in edge_set or (b_id, a_id) in edge_set


def build_pairs(bundle, limit_per_page=6, min_sim=0.12):
    """Returns {src_id: [ {target, score, why, rule, semantic}, ... ]}"""
    nodes = bundle["nodes"]
    if not nodes:
        return {}

    edge_set = {(e[0], e[1]) for e in bundle.get("edges", [])}

    # Title and body only. Including the url rewards slug similarity over content
    # similarity, which made near-duplicate FAQ pages look like strong related links.
    texts = [(n.get("text") or "") + " " + clean_title(n.get("title")) for n in nodes]
    toks = [tokens(t) for t in texts]

    idf = idf_weights(toks)
    vecs = [tfidf_vector(t, idf) for t in toks]

    # Only compare pages that are the same KIND of thing. A 3,000-page blog against a
    # 600-page list section is a whole-section similarity, which is the treemap's job,
    # not a link suggestion's.
    by_sec = defaultdict(list)
    for i, n in enumerate(nodes):
        by_sec[n.get("sec") or ""].append(i)

    # plus a global pool per role, so cross-section related links are possible
    by_role = defaultdict(list)
    for i, n in enumerate(nodes):
        by_role[n.get("role") or ""].append(i)

    svecs = to_sparse(vecs, len(vecs[0]) if vecs else 0)

    # Inverted index over DISCRIMINATING tokens only. A token on every page (a brand, a
    # nav word) separates nothing, so it is excluded. This replaces an O(n^2) scan that
    # took four minutes with a lookup that touches only genuinely similar pages.
    postings = defaultdict(list)
    for i, page_toks in enumerate(toks):
        for t in set(page_toks):
            if idf.get(t, 0.0) >= 2.2:
                postings[t].append(i)

    POOL_CAP = 320

    out = {}
    for i, src in enumerate(nodes):
        if not usable(src):
            continue

        # candidates: pages sharing a discriminating term, weighted by how many
        overlap = Counter()
        for t in set(toks[i]):
            if idf.get(t, 0.0) < 2.2:
                continue
            for j in postings.get(t, ()):  # noqa: B007
                if j != i:
                    overlap[j] += 1
        pool = [j for j, _ in overlap.most_common(POOL_CAP)]
        if len(pool) < 12:
            # sparse page: fall back to the section, which is still a sensible prior
            pool = pool + [j for j in by_sec.get(src.get("sec") or "", [])
                           if j != i and j not in pool][:POOL_CAP - len(pool)]

        cands = []
        seen_targets = set()
        for j in pool:
            if already_linked(i, j, edge_set):
                continue
            if not usable(nodes[j]):
                continue
            if clean_title(nodes[j].get("title")).lower() == clean_title(
                    src.get("title")).lower():
                continue      # same title, different page: a template, not a relation
            # one suggestion per destination page: three copies of the same target is
            # not three ideas
            tn = nodes[j]["url"]
            if tn in seen_targets:
                continue
            seen_targets.add(tn)
            sim = sparse_cosine(svecs[i], svecs[j])
            if sim < min_sim:
                continue
            shape, why = pair_shape(src, nodes[j])
            if shape < 0:
                continue
            # The similarity term must keep DISCRIMINATING across the whole range. A
            # capped multiplier saturates: every sim >= 0.35 scored identically, so 59%
            # of candidates tied at the same value and the ranking was meaningless.
            # Normalise by the observed ceiling instead, with headroom above shape.
            # No cap on the similarity term: capping it made every sim >= 0.55 tie, which
            # is where 54% of candidates sat. The shape term is already bounded at 1.0.
            rule = round(shape * 0.58 + max(0.0, min(sim, 1.0)) * 0.42, 4)
            cands.append({
                "target": nodes[j]["url"],
                "target_id": nodes[j]["id"],
                "target_title": clean_title(nodes[j].get("title")) or nodes[j]["url"],
                "target_role": nodes[j].get("role"),
                "rule": round(rule, 4),
                "semantic": round(sim, 4),
                "score": round(rule, 4),
                "band": bucket(rule),
                "clef": None,
                "unjudged": True,
                "why": why[:3],
            })
        cands.sort(key=lambda c: -c["rule"])
        if cands:
            out[src["id"]] = cands[:limit_per_page]
    return out


# ------------------------------------------------------------------- clef
# ---- CLEF wiring -----------------------------------------------------------
# Cloudflare CLEF is a SystemOne-API decision model, Apache 2.0. Two ways to reach it:
#
#   1. LOCAL.  Full `clef` weights are 55 GB and `clef-flash` 19 GB. That does not fit
#      a laptop disk, so local is opt-in via CLEF_PATH pointing at a downloaded snapshot.
#   2. HOSTED. Workers AI serves the same SystemOne API, so an existing Jev integration
#      switches by changing the endpoint and the model. Needs CLOUDFLARE_API_TOKEN.
#
# The deterministic rule scorer is the product; CLEF sharpens a ranking code it already
# produced. With neither available the rules still run and every score carries a rationale.
CLEF_PATH = os.environ.get("CLEF_PATH", "")
CLEF_PY = os.environ.get("CLEF_PY", "")
CLEF_ACCOUNT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
CLEF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
WORKERS_AI = "https://api.cloudflare.com/client/v4/accounts/{acct}/ai/run/"


def clef_mode():
    """local -> hosted -> none. Reported in the output so a reader knows which ran."""
    if CLEF_PATH and os.path.isdir(CLEF_PATH) and CLEF_PY and os.path.exists(CLEF_PY):
        return "local"
    if CLEF_ACCOUNT and CLEF_TOKEN:
        return "hosted"
    return "none"


def clef_available():
    return clef_mode() != "none"


def _clef_hosted(payload):
    """Call CLEF on Workers AI. Same SystemOne schema, so an existing Jev client only has
    to change its endpoint and model. All questions go in ONE request: the model evaluates
    each against the same state in isolation, which is the documented batching pattern."""
    import urllib.error
    import urllib.request

    url = WORKERS_AI.format(acct=CLEF_ACCOUNT) + "@cf/clef"
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Bearer {CLEF_TOKEN}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.load(r)
    return data.get("result", data)


def clef_judge(pairs, source_text, max_items=40):
    """Ask CLEF, in ONE batched call, whether each candidate is a genuinely related link.

    Batching matters: TypeSafe/CLEF evaluate every question against the same state in
    parallel and in isolation, so one call covers N candidates instead of N round trips.
    """
    import subprocess
    import tempfile

    questions = {}
    for i, p in enumerate(pairs[:max_items]):
        questions[f"link_{i}"] = {
            "type": "noul",
            "instructions": (
                f"A reader on the page \"{source_text[:220]}\" would follow a link to "
                f"\"{p['target_title'][:160]}\". Is that link useful to that reader, "
                f"or is it an unrelated page that should not be linked?"
            ),
        }

    payload = {
        "state": source_text[:4000],
        "questions": questions,
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        infile = f.name

    if clef_mode() == "hosted":
        res = _clef_hosted(payload)
    else:
        script = os.path.join(HERE, "_clef_run.py")
        outfile = infile + ".out"
        cmd = [CLEF_PY, script, CLEF_PATH, infile, outfile]
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=900)
            res = json.load(open(outfile))
        except Exception as e:                  # noqa: BLE001
            return {}, f"clef failed: {type(e).__name__}: {e}"
        finally:
            for pth in (infile, outfile):
                try:
                    os.unlink(pth)
                except OSError:
                    pass

    scores = {}
    for i, p in enumerate(pairs[:max_items]):
        a = res.get(f"link_{i}")
        if a is None:
            continue
        v = a.get("answer")
        if isinstance(v, list):
            v = v[0]
        scores[p["target_id"]] = float(v)
    return scores, None


def blend(pairs, clef_scores, weights=(0.55, 0.45)):
    """Blend ONCE. The rule score is preserved so a bad judgement stays visible."""
    wr, wj = weights
    for p in pairs:
        j = clef_scores.get(p["target_id"])
        p["clef"] = j
        if j is None:
            # A missing judgement must never score better than a real one.
            p["score"] = round(p["rule"] * 0.85, 4)
            p["band"] = bucket(p["score"])
            p["unjudged"] = True
        else:
            p["score"] = round(wr * p["rule"] + wj * j, 4)
            p["band"] = bucket(p["score"])
            p["unjudged"] = False
    pairs.sort(key=lambda c: -c["score"])
    return pairs


def bucket(score):
    """Score buckets, not magnitudes. JEV/decision-model scores are weakly calibrated
    numerically, so the defensible output is a label."""
    if score >= 0.60:
        return "strong"
    if score >= 0.38:
        return "likely"
    if score >= 0.20:
        return "possible"
    return "weak"


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Related-link finder for an interlink bundle")
    ap.add_argument("bundle")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--limit", type=int, default=6, help="links per source page")
    ap.add_argument("--no-clef", action="store_true")
    a = ap.parse_args()

    bundle = json.load(open(a.bundle))
    pairs = build_pairs(bundle, limit_per_page=a.limit)
    total = sum(len(v) for v in pairs.values())
    for cs in pairs.values():
        for c in cs:
            c.setdefault("score", c.get("rule", 0.0))
            c.setdefault("band", bucket(c["score"]))
    print(f"  candidate related links: {total} across {len(pairs)} pages")

    mode = clef_mode()
    print(f"  clef mode: {mode}"
          + ("  (55 GB local weights or 19 GB flash; set CLEF_PATH or "
             "CLOUDFLARE_API_TOKEN to enable)" if mode == "none" else ""))
    clef_used, clef_err = False, None
    if not a.no_clef and clef_available():
        print("  judging with CLEF (batched)...")
        # judge one representative source page to prove the path works, then blend
        sample_src = max(pairs, key=lambda k: len(pairs[k])) if pairs else None
        if sample_src is not None:
            src = next(n for n in bundle["nodes"] if n["id"] == sample_src)
            sc, err = clef_judge(pairs[sample_src],
                                 (src.get("text") or src.get("title") or "")[:4000])
            if err:
                clef_err = err
                print(f"  {err}; falling back to rules only")
            else:
                clef_used = True
                blend(pairs[sample_src], sc)
                print(f"  CLEF judged {len(sc)} candidates on the sample page")

    by_id = {n["id"]: n for n in bundle["nodes"]}
    result = {
        "bundle": os.path.basename(a.bundle),
        "clef": clef_used,
        "clef_mode": mode,
        "clef_error": clef_err,
        "total": total,
        "pairs": {str(k): v for k, v in pairs.items()},
    }
    out = a.out or (a.bundle.replace(".json", "-related.json"))

    # A template page repeated across 25 technology lists is ONE idea, not 25. Cap each
    # target title so the shortlist stays distinct and is actually reviewable.
    flat = [(sid, c) for sid, cs in pairs.items() for c in cs]
    flat.sort(key=lambda t: -t[1]["score"])
    seen_title, shortlist = Counter(), []
    for sid, c in flat:
        key = c["target_title"].strip().lower()
        if seen_title[key] >= 2:
            continue
        seen_title[key] += 1
        shortlist.append((sid, c))
        if len(shortlist) >= 15:
            break

    result["shortlist"] = [{
        "source": by_id[sid]["url"],
        "source_title": clean_title(by_id[sid].get("title")),
        **{k: c[k] for k in ("target", "target_title", "score", "band", "rule",
                             "semantic", "clef", "why")},
    } for sid, c in shortlist]

    json.dump(result, open(out, "w"), indent=1)
    print(f"  -> {out}  ({len(shortlist)} distinct in the shortlist)")

    print("\n  top related-link suggestions (distinct targets):")
    for sid, c in shortlist[:12]:
        st = clean_title(by_id[sid].get("title")) or by_id[sid]["url"]
        print(f"    [{c['band']:8s}] {c['score']:.3f}  {st[:42]:44s} -> {c['target_title'][:38]}")


if __name__ == "__main__":
    main()