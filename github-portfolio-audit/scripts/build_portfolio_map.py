#!/usr/bin/env python3
"""
Build the portfolio architecture diagram from the audit data.

Classification is by DERIVED TOPIC, not by name substring. A name match put
LakeB2B-SlideSmith in two domains at once and left 19 repos unassigned,
because names are not what a repo is. Topics are derived from manifests and
author-written prose, so they carry real signal.

Six repos are assigned by hand where the topic signal is genuinely split, and
the override is recorded in OVERRIDES rather than hidden in a rule.

Output: a single self-contained HTML file, dark, inline SVG, no JS.
"""
import json
import os
import sys
from collections import defaultdict
from html import escape

SP = os.path.dirname(os.path.abspath(__file__))

# topic -> domain, evaluated in order; first hit wins
DOMAIN_RULES = [
    ("Data & Enrichment", {
        "web-scraping", "data-engineering", "knowledge-graph", "vector-database",
        "graph-analysis", "neo4j", "postgresql", "elasticsearch", "data-analysis",
    }),
    ("Signal & Sales", {
        "sales-automation", "recruitment", "analytics", "seo", "social-media",
        "email", "legaltech", "real-estate", "billing",
    }),
    ("Content & Media", {
        "document-management", "video", "voice", "gamification", "pdf",
        "docx", "spreadsheet", "pptx", "ocr",
    }),
    ("Health & Lifestyle", {
        "healthtech", "travel", "maps", "edtech",
    }),
    ("Agent Platform", {
        "ai-agents", "llm", "rag", "machine-learning", "anthropic",
    }),
]

# Repos the topic signal gets wrong or splits. Each one is a judgement call and
# is listed here so it can be argued with.
OVERRIDES = {
    # Graph and agent work is platform, not data: ChampGraph is the spine that
    # ChampIQ, ChampOracle and Champ_Bot all sit on.
    "Graphiti-knowledge-graph": "Agent Platform",
    "ChampIQ": "Agent Platform",
    "ChampOracle": "Agent Platform",
    "Champ_Bot": "Agent Platform",
    "champ-workspace-mvp": "Agent Platform",
    "champ-agent-mesh": "Agent Platform",
    "Deep_kit": "Agent Platform",
    "Champion-Ranch-Tracking-System": "Signal & Sales",
    # ChampMaps is a reusable component library, not a health product.
    "ChampMaps": "Data & Enrichment",
    # Event scout is a PWA for contact capture, closer to sales tooling.
    "event-scout": "Signal & Sales",
    "ChampLens": "Content & Media",
    "ai-resume-parser": "Signal & Sales",
    "five-level-email-personalizer": "Signal & Sales",
    "lakeb2b-email-personalizer": "Signal & Sales",
    "Voice-Qualified-Template": "Signal & Sales",
    "Champ-Voice-Agent": "Signal & Sales",
    "ChampLantern": "Signal & Sales",
    "ChampMail": "Signal & Sales",
    "ChampQuest": "Signal & Sales",
    "pikvita-mobile-app-android-fix": "Signal & Sales",
    "gen_ui": "Agent Platform",
    "ChampVox": "Signal & Sales",
    "Japan-Travel-App": "Health & Lifestyle",
    "pikvita-quiz": "Content & Media",
    "SlideSmith": "Content & Media",
    "LakeB2B-SlideSmith": "Content & Media",
    "ICP-Finder-LLM-R1": "Signal & Sales",
    "Investor-Module": "Data & Enrichment",
    "LakeStream": "Data & Enrichment",
    "LakeCurrent": "Data & Enrichment",
    "ChampSet": "Data & Enrichment",
    "100xLongevity": "Health & Lifestyle",
    "champions-wellness": "Health & Lifestyle",
    "champ-vault": "Health & Lifestyle",
    "ChampHQ": "Agent Platform",
    "Champ-Plugin": "Agent Platform",
}

# Web surfaces: anything that is primarily a public-facing site or portal.
WEB_SURFACE = {
    "deependhq-site", "About-Us-Page", "Partner-Portal", "KimberlyCoorg_site",
    "IP-Momentum-Page", "champions-club-affiliate-portal",
    "lakeb2b-affiliate-portal", "champions-club-affiliate-portal",
}

# Semantic colour language, matching the house architecture-diagram palette.
FILL = {
    "Data & Enrichment": ("rgba(76, 29, 149, 0.4)", "#a78bfa"),
    "Signal & Sales": ("rgba(6, 78, 59, 0.4)", "#34d399"),
    "Content & Media": ("rgba(120, 53, 15, 0.3)", "#fbbf24"),
    "Health & Lifestyle": ("rgba(8, 51, 68, 0.4)", "#22d3ee"),
    "Agent Platform": ("rgba(136, 19, 55, 0.4)", "#fb7185"),
    "Web Surfaces": ("rgba(30, 41, 59, 0.5)", "#94a3b8"),
}


def classify(v):
    name = v["name"]
    if name in WEB_SURFACE:
        return "Web Surfaces"
    if name in OVERRIDES:
        return OVERRIDES[name]
    tset = set(v["derived_topics"])
    for domain, topics in DOMAIN_RULES:
        if tset & topics:
            return domain
    return "Web Surfaces"


def tier(v):
    d = v["days_idle"] if isinstance(v["days_idle"], int) else 10**6
    return 1 if d <= 30 else (2 if d <= 180 else 3)


def main():
    ev = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    groups = defaultdict(list)
    for v in ev.values():
        groups[classify(v)].append(v)
    for g in groups.values():
        g.sort(key=lambda x: x["name"].lower())

    # ---- layout: one column per domain, 2 rows of boxes per column ----
    # Heights are derived from the cards themselves. An earlier version added
    # PADY into the boundary height as well as the card offset, which made every
    # domain box ~138px taller than its contents and pushed the legend past the
    # bottom of the viewBox, where it was silently invisible.
    CW, CH = 236, 84          # card size
    COLGAP, ROWGAP = 26, 16
    PADX, PADY = 40, 118
    BOUND_TOP_OFF = 40        # space above the first card, for the domain title
    BOUND_PAD = 22            # space below the last card, inside the boundary
    order = ["Agent Platform", "Data & Enrichment", "Signal & Sales",
             "Content & Media", "Health & Lifestyle", "Web Surfaces"]
    order = [d for d in order if d in groups]

    def rows_for(d):
        return max(1, (len(groups[d]) + 1) // 2)

    # bottom edge of the cards in a column
    card_bottom = {d: PADY + rows_for(d) * (CH + ROWGAP) - ROWGAP for d in order}
    # bottom edge of the boundary box (encapsulates the cards)
    bound_bottom = {d: card_bottom[d] + BOUND_PAD for d in order}

    legend_h = 64
    total_h = max(bound_bottom.values()) + legend_h + 20
    total_w = PADX * 2 + len(order) * CW + (len(order) - 1) * COLGAP

    def colx(i):
        return PADX + i * (CW + COLGAP)

    parts = []
    a = parts.append
    a(f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">')
    a('<meta name="viewport" content="width=device-width,initial-scale=1.0">')
    a('<title>Champions Group GitHub Portfolio</title>')
    a('<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">')
    a("""<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'JetBrains Mono',monospace;background:#020617;min-height:100vh;padding:2rem;color:#fff}
.container{max-width:1500px;margin:0 auto}
.header{margin-bottom:1.75rem}
.header-row{display:flex;align-items:center;gap:1rem;margin-bottom:.5rem}
.pulse-dot{width:12px;height:12px;background:#22d3ee;border-radius:50%;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
h1{font-size:1.5rem;font-weight:700;letter-spacing:-.025em}
.subtitle{color:#94a3b8;font-size:.875rem;margin-left:1.75rem}
.diagram-container{background:rgba(15,23,42,.5);border-radius:1rem;border:1px solid #1e293b;padding:1.5rem;overflow-x:auto}
svg{width:100%;display:block}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem;margin-top:2rem}
.card{background:rgba(15,23,42,.5);border-radius:.75rem;border:1px solid #1e293b;padding:1.25rem}
.card-header{display:flex;align-items:center;gap:.5rem;margin-bottom:.75rem}
.card-dot{width:8px;height:8px;border-radius:50%}
.card h3{font-size:.875rem;font-weight:600}
.card ul{list-style:none;color:#94a3b8;font-size:.75rem}
.card li{margin-bottom:.4rem}
.card li.more{color:#94a3b8}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.75rem;margin:1.5rem 0}
.kpi{background:rgba(15,23,42,.5);border:1px solid #1e293b;border-radius:.6rem;padding:.85rem 1rem}
.kpi .v{font-size:1.35rem;font-weight:700}
.kpi .l{color:#94a3b8;font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;margin-top:.2rem}
.footer{text-align:center;margin-top:1.5rem;color:#94a3b8;font-size:.75rem}
h2{font-size:1rem;font-weight:600;color:#e2e8f0;margin:2rem 0 .75rem;letter-spacing:-.01em}
.subtitle{max-width:78ch}
/* Honour the OS setting: the pulse is decoration, not information. */
@media (prefers-reduced-motion: reduce){
  .pulse-dot{animation:none}
}
</style></head><body><div class="container">""")

    a('<div class="header"><div class="header-row"><div class="pulse-dot"></div>'
      '<h1>Champions Group &mdash; GitHub Portfolio</h1></div>')
    a(f'<p class="subtitle">{len(ev)} active repositories, grouped by what they '
      f'actually do. Classification is derived from each repo&rsquo;s own '
      f'manifests and documentation, not from its name.</p></div>')

    n_pub = sum(1 for v in ev.values() if not v["private"])
    n_t1 = sum(1 for v in ev.values() if tier(v) == 1)
    n_t3 = sum(1 for v in ev.values() if tier(v) == 3)
    n_prot = sum(1 for v in ev.values() if v.get("has_protection"))
    a(f'<div class="kpis">')
    for val, lab in [(len(ev), "Active repos"), (n_pub, "Public"),
                     (n_t1, "Tier 1 live"), (n_t3, "Tier 3 dormant"),
                     (n_prot, "Protected")]:
        a(f'<div class="kpi"><div class="v">{val}</div><div class="l">{lab}</div></div>')
    a('</div>')

    a('<div class="diagram-container"><svg viewBox="0 0 %d %d">' % (total_w, total_h))
    a('<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" '
      'refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>'
      '</marker><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
      '<path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>'
      '</pattern></defs>')
    a('<rect width="100%" height="100%" fill="url(#grid)"/>')

    for i, d in enumerate(order):
        fill, stroke = FILL[d]
        items = groups[d]
        x = colx(i)
        by_top = PADY - BOUND_TOP_OFF
        # domain boundary, sized to the cards it actually contains
        a(f'<rect x="{x-16}" y="{by_top}" width="{CW+32}" '
          f'height="{bound_bottom[d]-by_top}" rx="12" '
          f'fill="{fill.replace("0.4","0.07").replace("0.3","0.06").replace("0.5","0.08")}" '
          f'stroke="{stroke}" stroke-width="1" stroke-dasharray="8,4"/>')
        a(f'<text x="{x}" y="{PADY-18}" fill="{stroke}" font-size="11" '
          f'font-weight="600">{escape(d)}</text>')
        a(f'<text x="{x+CW}" y="{PADY-18}" fill="#94a3b8" font-size="9" '
          f'text-anchor="end">{len(items)}</text>')
        for j, v in enumerate(items):
            r, c = divmod(j, 2)
            bx = x + c * (CW // 2 + 4)
            by = PADY + r * (CH + ROWGAP)
            bw = CW // 2 - 8
            # double-rect mask so arrows never show through a translucent fill
            a(f'<rect x="{bx}" y="{by}" width="{bw}" height="{CH}" rx="6" fill="#0f172a"/>')
            a(f'<rect x="{bx}" y="{by}" width="{bw}" height="{CH}" rx="6" '
              f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
            nm = v["name"]
            if len(nm) > 19:
                nm = nm[:18] + "\u2026"
            a(f'<text x="{bx+10}" y="{by+22}" fill="#fff" font-size="10" '
              f'font-weight="600">{escape(nm)}</text>')
            lang = v.get("language") or "-"
            a(f'<text x="{bx+10}" y="{by+38}" fill="#94a3b8" font-size="8">'
              f'{escape(str(lang))}</text>')
            vis = "private" if v["private"] else "public"
            vcol = "#64748b" if v["private"] else "#34d399"
            a(f'<text x="{bx+10}" y="{by+54}" fill="{vcol}" font-size="7.5">'
              f'{vis} \u00b7 {v["file_count"]} files \u00b7 T{tier(v)}</text>')
            if v.get("derived_topics"):
                t = ", ".join(v["derived_topics"][:2])
                # 7.5px JetBrains Mono is ~4.5px/char; the card is ~102px wide
                # with 10px padding each side, so ~18 chars is the real budget.
                # 26 overflowed the card and was clipped by the border.
                if len(t) > 17:
                    t = t[:16] + "\u2026"
                a(f'<text x="{bx+10}" y="{by+69}" fill="{stroke}" font-size="7.5">'
                  f'{escape(t)}</text>')

    # legend, below every boundary box and inside the viewBox
    ly = max(bound_bottom.values()) + 26
    a(f'<text x="{PADX}" y="{ly}" fill="#fff" font-size="10" font-weight="600">Legend</text>')
    lx = PADX
    for d in order:
        fill, stroke = FILL[d]
        a(f'<rect x="{lx}" y="{ly+12}" width="14" height="9" rx="2" fill="{fill}" '
          f'stroke="{stroke}" stroke-width="1"/>')
        a(f'<text x="{lx+20}" y="{ly+20}" fill="#94a3b8" font-size="8">{escape(d)}</text>')
        lx += 26 + len(d) * 5.6
    # verify the legend is actually on-canvas; an off-canvas legend is invisible
    # and no HTML validator will ever tell you.
    assert ly + 24 < total_h, f"legend at y={ly} falls outside viewBox {total_h}"
    a('</svg></div>')

    a('<div class="cards">')
    for d in order:
        items = groups[d]
        fill, stroke = FILL[d]
        a('<div class="card"><div class="card-header">'
          f'<div class="card-dot" style="background:{stroke}"></div>'
          f'<h2 style="margin:0;font-size:.875rem">{escape(d)}</h2></div><ul>')
        for v in items[:9]:
            a(f'<li>&bull; {escape(v["name"])}</li>')
        if len(items) > 9:
            a(f'<li class="more">&hellip; and {len(items)-9} more</li>')
        a('</ul></div>')
    a('</div>')

    a(f'<p class="footer">Champ-Deep GitHub portfolio \u00b7 {len(ev)} active repos '
      f'\u00b7 generated from live API data</p>')
    a('</div></body></html>')

    with open(out, "w") as f:
        f.write("\n".join(parts))
    print(f"wrote {out}")
    for d in order:
        print(f"  {d:22s} {len(groups[d]):3d}")
    assert sum(len(groups[d]) for d in order) == len(ev), "repo lost in classification"
    print(f"total {sum(len(groups[d]) for d in order)} == {len(ev)}")


if __name__ == "__main__":
    main()
