#!/usr/bin/env python3
"""
component.py: build the embeddable "related sites / related reading" carousel.

This is the piece that goes ON the website. It reads a JSON catalogue of sites and pages,
scores every catalogue entry against the CURRENT page, and emits a small self-contained
widget plus a JSON payload the site fetches at runtime.

Two modes:

  1. PAGE mode (recommended). One widget on the site. The page announces itself via a
     <meta> tag or a data attribute, the widget scores the catalogue against it, and only
     the relevant entries render. No per-page build.

  2. BUNDLE mode. Renders a preview page so the team can see what the widget would show
     for a given page before shipping it.

The catalogue is the deliverable a team maintains: drop new sites into sites.txt, re-run
refresh.py, and the widget's options grow.

Usage:
    python3 component.py --bundle bundle-spanglobalservices-com.json \\
                         --catalog catalog.json -o widget/
"""
import argparse
import json
import math
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from semantic import (clean_title, tokens, tfidf_vector,  # noqa: E402
                       idf_weights, sparse_cosine, to_sparse)

# What kind of site is this? The carousel tailors to the type, because "related" means
# something different on a data-broker site than on a consultancy.
SITE_PROFILES = {
    "data_broker": {
        "label": "Data & lead generation",
        "terms": ["email list", "b2b data", "contact data", "lead generation",
                  "prospect", "database", "verification", "enrichment",
                  "targeting", "segment", "mql", "campaign"],
        "affinity": ["salestech", "martech", "growthtech"],
    },
    "consultancy": {
        "label": "Advisory & consulting",
        "terms": ["strategy", "advisory", "consulting", "transformation",
                  "assessment", "roadmap", "operating model", "governance"],
        "affinity": [],
    },
    "saas": {
        "label": "Software & platform",
        "terms": ["platform", "integration", "api", "workflow", "automation",
                  "dashboard", "onboarding", "pricing"],
        "affinity": [],
    },
}


def profile_for(bundle):
    """Classify the SITE, not the page: which vocabulary does this whole corpus use most?

    Scored per THOUSAND WORDS over the pages actually sampled, so the number does not
    depend on how many pages were crawled."""
    nodes = bundle["nodes"]
    sample = nodes[:1200]
    if not sample:
        return "data_broker"
    total_words = 0
    blob = []
    for n in sample:
        w = n.get("words") or len((n.get("text") or "").split())
        total_words += max(w, 1)
        blob.append((n.get("text") or "")[:1200])
    alltext = " ".join(blob).lower()
    kw = max(total_words / 1000.0, 1.0)

    scored = []
    for key, prof in SITE_PROFILES.items():
        hits = sum(alltext.count(t) for t in prof["terms"])
        scored.append((hits / kw, key))
    scored.sort(reverse=True)
    return scored[0][1] if scored else "data_broker"


def build_catalog(sites):
    """sites: list of dicts {domain, name, blurb, tags[], url, pages[]}"""
    return {
        "version": 1,
        "sites": sites,
    }


def catalogue_vectors(catalog):
    docs = []
    for s in catalog["sites"]:
        docs.append(tokens(" ".join([s.get("name", ""), s.get("blurb", ""),
                                     " ".join(s.get("tags", []))])))
    idf = idf_weights(docs) if docs else {}
    vecs = [tfidf_vector(d, idf) for d in docs] if docs else []
    return idf, to_sparse(vecs)


def _host(url):
    return re.sub(r"^https?://", "", (url or "").strip()).strip("/").split("/")[0].lower()


def score_page(page_tokens, catalog, page_profile, self_host=None):
    """Score every catalogue site against the current page.

    Three signals, deliberately separable so the team can see WHY something was suggested:
      content  - vocabulary overlap with the site's description
      affinity - the catalogue entry is tagged for this site TYPE
      role     - a commercial page should not be pushed to a research page
    """
    idf, cvecs = catalogue_vectors(catalog)
    pvec = to_sparse([tfidf_vector(page_tokens, idf)])[0]

    prof = SITE_PROFILES.get(page_profile, SITE_PROFILES["data_broker"])
    out = []
    for i, s in enumerate(catalog["sites"]):
        if self_host and _host(s.get("url") or s.get("domain", "")) == self_host:
            continue      # never recommend the site you are already on
        content = max(0.0, sparse_cosine(pvec, cvecs[i]))

        aff = 0.0
        stags = {t.lower() for t in s.get("tags", [])}
        if stags & {a.lower() for a in prof["affinity"]}:
            aff = 0.30

        score = min(1.0, content * 0.85 + aff)
        if score < 0.10:
            continue
        out.append({
            "name": s.get("name"),
            "url": s.get("url") or s.get("domain"),
            "blurb": s.get("blurb", ""),
            "tags": s.get("tags", []),
            "score": round(score, 3),
            "why": (["shares your topic vocabulary"] if content > 0.12 else []) +
                   (["tagged for " + prof["label"].lower()] if aff else []),
        })
    out.sort(key=lambda x: -x["score"])
    return out


WIDGET_HTML = r"""<!-- related-sites widget: drop-in, no build step -->
<div class="rsw" id="related-sites-widget" hidden>
  <div class="rsw-head">
    <span class="rsw-title">Related sites and reading</span>
    <span class="rsw-nav">
      <button class="rsw-prev" type="button" aria-label="Previous recommendations">&#8592;</button>
      <button class="rsw-next" type="button" aria-label="Next recommendations">&#8594;</button>
    </span>
  </div>
  <div class="rsw-track" role="list" tabindex="0" aria-label="Related sites"></div>
  <p class="rsw-empty" hidden>Nothing related yet. Add entries to the catalogue.</p>
</div>
<style>
/* Theme defaults live on :root. Declaring them as `--x: var(--x, fallback)` on the
   component itself is a cycle: the fallback refers to the property being declared, the
   declaration becomes invalid at computed-value time, and EVERY property in the block
   resolves to "". That silently removed all borders and backgrounds. */
.rsw{--bg:var(--rsw-bg,#fff);--fg:var(--rsw-fg,#0d1424);
 --mut:var(--rsw-mut,#5b6678);--line:var(--rsw-line,#dde3ec);
 --acc:var(--rsw-acc,#1a56db);--face:var(--rsw-face,#fbfcfe);
 font:400 15px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
 color:var(--fg);margin:2.5rem 0}
.rsw[hidden]{display:none}
.rsw-head{display:flex;align-items:center;gap:.75rem;margin-bottom:.75rem}
.rsw-title{font-weight:600;font-size:.95rem;letter-spacing:.01em}
.rsw-nav{display:flex;gap:.4rem;margin-left:auto}
.rsw-prev,.rsw-next{width:40px;height:40px;border-radius:8px;border:1px solid var(--line);
 background:var(--bg);color:var(--fg);cursor:pointer;display:inline-flex;
 align-items:center;justify-content:center;transition:background .15s,border-color .15s}
.rsw-prev:hover,.rsw-next:hover{background:color-mix(in srgb,var(--acc) 9%,var(--face));
 border-color:var(--acc)}
.rsw-prev:focus-visible,.rsw-next:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.rsw-prev[disabled],.rsw-next[disabled]{opacity:.4;cursor:default}
.rsw-track{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(240px,1fr);
 gap:.75rem;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:.35rem}
.rsw-card{scroll-snap-align:start;border:1px solid var(--line);border-radius:12px;
 padding:1rem;background:var(--face);text-decoration:none;
 color:inherit;display:flex;flex-direction:column;gap:.4rem;min-height:118px}
.rsw-card:hover{border-color:var(--acc);box-shadow:0 2px 10px rgba(16,24,40,.07)}
.rsw-card:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.rsw-name{font-weight:600;font-size:.95rem}
.rsw-blurb{color:var(--mut);font-size:.85rem;
 display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.rsw-why{margin-top:auto;font-size:.75rem;color:var(--mut);opacity:.85}
.rsw-empty{color:var(--mut);font-size:.875rem}
@media (prefers-reduced-motion:reduce){.rsw-track{scroll-behavior:auto}}
</style>
<script>
(function(){
  var CFG = window.__RELATED_SITES__ || {};
  var w = document.getElementById('related-sites-widget');
  if(!w || !CFG.payload) return;

  // Which page is this? An explicit attribute wins, then the meta tag, then the path.
  function here(){
    var b = document.body;
    var a = b && b.getAttribute('data-related-profile');
    if(a) return {profile:a, tokens:CFG.pageTokens||[]};
    var m = document.querySelector('meta[name="related-profile"]');
    var t = document.querySelector('meta[name="related-tokens"]');
    return {
      profile: (m && m.content) || CFG.profile || 'data_broker',
      tokens: (t && t.content ? t.content.split(/[,\s]+/).filter(Boolean) : []) || CFG.pageTokens || []
    };
  }
  function host(u){ return String(u||'').replace(/^https?:\/\//,'').split('/')[0].toLowerCase(); }
  function score(page){
    var prof = CFG.profiles[page.profile] || {terms:[],affinity:[]};
    var tset = {}; page.tokens.forEach(function(t){ tset[t.toLowerCase()]=1; });
    var self = host(location.hostname);
    var out = [];
    CFG.payload.sites.forEach(function(s){
      if(host(s.url) === self) return;          // never recommend the current site
      var score = 0, why = [];
      var d = s.blurb.toLowerCase() + ' ' + s.name.toLowerCase() + ' ' + (s.tags||[]).join(' ').toLowerCase();
      var hit = 0;
      (s.tags||[]).forEach(function(g){ if(tset[g.toLowerCase()]) hit++; });
      if(hit) { score += hit*0.18; why.push('shares a topic tag'); }
      prof.terms.forEach(function(k){ if(d.indexOf(k)>=0) score += 0.12; });
      if(score >= 0.10) out.push({name:s.name,url:s.url,blurb:s.blurb,score:score,why:why});
    });
    out.sort(function(a,b){ return b.score-a.score; });
    return out.slice(0,12);
  }
  function render(items){
    var track = w.querySelector('.rsw-track');
    if(!items.length){ w.hidden = false; w.querySelector('.rsw-empty').hidden=false; return; }
    track.innerHTML = items.map(function(it){
      return '<a class="rsw-card" role="listitem" href="'+it.url+'" rel="noopener">'+
             '<span class="rsw-name"></span>'+
             '<span class="rsw-blurb"></span>'+
             (it.why.length?'<span class="rsw-why"></span>':'')+'</a>';
    }).join('');
    // textContent, never innerHTML, for anything from the catalogue
    Array.prototype.forEach.call(track.children, function(card,i){
      var it = items[i];
      card.querySelector('.rsw-name').textContent = it.name;
      card.querySelector('.rsw-blurb').textContent = it.blurb;
      if(it.why.length) card.querySelector('.rsw-why').textContent = it.why.join(' · ');
    });
    w.hidden = false;
  }
  var track = w.querySelector('.rsw-track');
  var prev = w.querySelector('.rsw-prev'), next = w.querySelector('.rsw-next');
  function nudge(dir){ track.scrollBy({left:dir*(track.clientWidth*0.8), behavior:'smooth'}); }
  prev.addEventListener('click', function(){nudge(-1);});
  next.addEventListener('click', function(){nudge(1);});

  // Hide the arrows when everything already fits, so the control is not decoration.
  function syncNav(){
    var over = track.scrollWidth - track.clientWidth;
    var atStart = track.scrollLeft <= 1;
    var atEnd = track.scrollLeft >= over - 1;
    prev.hidden = over <= 2;
    next.hidden = over <= 2;
    prev.disabled = atStart;
    next.disabled = atEnd;
  }
  track.addEventListener('scroll', syncNav, {passive:true});
  window.addEventListener('resize', syncNav);
  render(score(here()));
  syncNav();
})();
</script>
"""


def main():
    ap = argparse.ArgumentParser(description="Build the related-sites carousel widget")
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--catalog", default=os.path.join(HERE, "catalog.json"))
    ap.add_argument("-o", "--out", default=None,
                    help="output dir (default widget-<site-slug>)")
    ap.add_argument("--profile", default=None, help="override the detected site profile")
    a = ap.parse_args()

    bundle = json.load(open(a.bundle))
    _host_raw = (bundle.get("host") or
                 os.path.basename(a.bundle).replace(".json", "").replace("bundle-", ""))
    _host_raw = re.sub(r"^https?://", "", _host_raw).strip("/")
    _host_raw = re.sub(r"^www\.", "", _host_raw)      # one site, one directory
    slug = re.sub(r"[^a-z0-9]+", "-", _host_raw.lower()).strip("-")
    a.out = a.out or os.path.join(HERE, "widget-" + slug)
    profile = a.profile or profile_for(bundle)
    catalog = json.load(open(a.catalog))

    os.makedirs(a.out, exist_ok=True)
    prof_json = {k: {"label": v["label"], "terms": v["terms"], "affinity": v["affinity"]}
                 for k, v in SITE_PROFILES.items()}

    payload = {
        "profile": profile,
        "profiles": prof_json,
        "payload": {"sites": catalog["sites"]},   # nested: the runtime reads CFG.payload
    }
    with open(os.path.join(a.out, "related-sites.js"), "w", encoding="utf-8") as f:
        f.write("window.__RELATED_SITES__ = ")
        json.dump(payload, f, indent=1)
        f.write(";\n")

    with open(os.path.join(a.out, "related-sites.html"), "w", encoding="utf-8") as f:
        f.write(WIDGET_HTML)

    print(f"  profile: {profile} ({SITE_PROFILES[profile]['label']})")
    print(f"  catalogue: {len(catalog['sites'])} sites")
    print(f"  -> {a.out}/related-sites.html")
    print(f"  -> {a.out}/related-sites.js")

    # show what it would recommend for the whole-site profile, so a human can sanity check
    prof_terms = SITE_PROFILES[profile]["terms"]
    sample = tokens(" ".join(prof_terms) + " " + bundle["nodes"][0].get("title", ""))
    sc = score_page(sample, catalog, profile,
                    self_host=_host(bundle.get("host") or bundle.get("base") or ""))
    print(f"\n  sample recommendation (profile words): {len(sc)} items")
    for x in sc[:6]:
        print(f"    {x['score']:.3f}  {x['name'][:34]:36s} {','.join(x['why'])[:44]}")


if __name__ == "__main__":
    main()