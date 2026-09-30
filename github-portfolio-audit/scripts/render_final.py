#!/usr/bin/env python3
"""
Final before/after report, with the portfolio diagram embedded.

Compares audit.json (before) against audit2.json (after) on the same repo
population, and embeds the portfolio map inline so the deliverable is one file.

Read-only with respect to GitHub.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from html import escape

SP = os.path.dirname(os.path.abspath(__file__))

NAME_BACKUP = ["-backup", "_backup", ".backup-", "backup-", "(copy)", "-copy", "-old", "_old"]


def is_backup(r):
    n = r["name"].lower()
    if any(k in n for k in NAME_BACKUP):
        return True
    return bool(r.get("description") and "backup" in r["description"].lower())


def idle(r):
    v = r.get("days_idle")
    return v if isinstance(v, int) else 10**6


def main():
    before = json.load(open(sys.argv[1]))
    after = json.load(open(sys.argv[2]))
    out = sys.argv[3]
    mapfile = sys.argv[4] if len(sys.argv) > 4 else None

    def portfolio(A):
        return {r["name"]: r for r in A["repos"] if not r["fork"] and not is_backup(r)}

    o1, o2 = portfolio(before), portfolio(after)
    common = sorted(set(o1) & set(o2))

    # The population can shift between audits: a repo whose description used to
    # say "Backup of local project X" stops counting as a backup once a real
    # description is written. Compare like for like on the intersection and say
    # so, rather than reporting movement that came from reclassification.
    rows = [
        ("Topics set", lambda r: not r["topics"], "Discoverability: how a repo is found in GitHub search"),
        ("Description set", lambda r: not r["description"], "The one line shown in listings"),
        ("README present", lambda r: not r["has_readme"], "What a visitor reads first"),
        ("Default branch is main/master", lambda r: r["default_branch"] not in ("main", "master"),
         "A feature-branch default hands visitors half-finished work"),
        ("Default branch protected (non-empty repos)",
         lambda r: r["file_count"] > 0 and not r["has_protection"] and r["rulesets"] == 0,
         "Unreviewed pushes with no warning. Empty repos are excluded: they have no branch to protect."),
        ("LICENSE file", lambda r: not r["has_license_file"], "Legally ambiguous reuse"),
        (".gitignore present", lambda r: not r["has_gitignore"], "One `git add .` from leaking secrets"),
        ("CI configured", lambda r: not r["has_ci"], "Nothing verifies a commit"),
    ]

    def count(f, table):
        return sum(1 for n in common if f(table[n]))

    table_rows = []
    for label, f, why in rows:
        b = count(f, o1)
        a = count(f, o2)
        table_rows.append((label, why, b, a, b - a))

    # protected split, since the private/public split is the whole story
    pub = [n for n in common if not o2[n]["private"] and o2[n]["file_count"] > 0]
    priv = [n for n in common if o2[n]["private"] and o2[n]["file_count"] > 0]
    pub_prot = sum(1 for n in pub if o2[n]["has_protection"] or o2[n]["rulesets"] > 0)
    priv_prot = sum(1 for n in priv if o2[n]["has_protection"] or o2[n]["rulesets"] > 0)

    readme_fixed = [n for n in common if not o1[n]["has_readme"] and o2[n]["has_readme"]]
    branch_fixed = [n for n in common
                    if o1[n]["default_branch"] not in ("main", "master")
                    and o2[n]["default_branch"] in ("main", "master")]

    def rrow(label, why, b, a, d):
        cls = "good" if d > 0 else ("bad" if d < 0 else "flat")
        return (f'<tr><td><strong>{escape(label)}</strong>'
                f'<div class="why">{escape(why)}</div></td>'
                f'<td class="num">{b}</td><td class="num">{a}</td>'
                f'<td class="num {cls}">{d:+d}</td></tr>')

    body = "\n".join(rrow(*r) for r in table_rows)

    # inline the portfolio diagram (strip its <html>/<head>/<body> wrapper)
    diag = ""
    if mapfile and os.path.exists(mapfile):
        m = open(mapfile).read()
        svg = re.search(r"<svg.*?</svg>", m, re.S)
        cards = re.search(r'<div class="cards">.*?</div>\s*<p class="footer">', m, re.S)
        if svg:
            diag = svg.group(0)
        if cards:
            diag += re.sub(r"<p class=\"footer\">.*?</p>", "", cards.group(0), flags=re.S)

    forks = [r for r in after["repos"] if r["fork"]]
    backups = [r for r in after["repos"] if is_backup(r) and not r["fork"]]
    empty = [r for r in after["repos"] if r["file_count"] == 0]

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GitHub Portfolio: Before and After</title>
<style>
:root{{--bg:#0d1117;--panel:#161b22;--bd:#30363d;--fg:#e6edf3;--mut:#8b949e;
--acc:#58a6ff;--ok:#3fb950;--no:#f85149;--warn:#d29922}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.62 -apple-system,BlinkMacSystemFont,"SF Pro Text",Inter,sans-serif}}
.wrap{{max-width:1240px;margin:0 auto;padding:40px 24px 80px}}
h1{{font-size:29px;margin:0 0 6px;letter-spacing:-.02em}}
h2{{font-size:19px;margin:40px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--bd)}}
h3{{font-size:14px;margin:24px 0 8px;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}}
.sub{{color:var(--mut);font-size:14px;margin-bottom:26px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(132px,1fr));gap:11px;margin:22px 0}}
.kpi{{background:var(--panel);border:1px solid var(--bd);border-radius:9px;padding:14px 16px}}
.kpi .v{{font-size:25px;font-weight:640;letter-spacing:-.02em}}
.kpi .l{{color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.07em;margin-top:3px}}
table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:13.5px}}
th{{text-align:left;color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.07em;
padding:9px 11px;border-bottom:1px solid var(--bd)}}
td{{padding:10px 11px;border-bottom:1px solid rgba(48,54,61,.55);vertical-align:top}}
td.num{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;width:78px}}
td.good{{color:var(--ok);font-weight:640}} td.bad{{color:var(--no);font-weight:640}}
td.flat{{color:var(--mut)}}
.why{{color:var(--mut);font-size:12.5px;margin-top:3px;max-width:600px}}
a{{color:var(--acc);text-decoration:none}} a:hover{{text-decoration:underline}}
.card{{background:var(--panel);border:1px solid var(--bd);border-radius:9px;padding:16px 18px;margin:12px 0}}
.box{{border-radius:8px;padding:14px 16px;margin:14px 0;font-size:14px;max-width:78ch}}
.box.ok{{background:rgba(63,185,80,.08);border:1px solid rgba(63,185,80,.3);border-left:3px solid var(--ok)}}
.box.warn{{background:rgba(210,153,34,.07);border:1px solid rgba(210,153,34,.3);border-left:3px solid var(--warn)}}
.box.info{{background:rgba(88,166,255,.08);border:1px solid rgba(88,166,255,.3);border-left:3px solid var(--acc)}}
ul{{padding-left:20px;margin:9px 0;font-size:14px;line-height:1.8}}
code{{background:var(--panel);padding:1.5px 6px;border-radius:4px;font-size:12.5px;
font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
.diagram{{background:rgba(15,23,42,.5);border:1px solid #1e293b;border-radius:12px;padding:18px;overflow-x:auto;margin:14px 0}}
.diagram svg{{width:100%;display:block}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem;margin-top:1.5rem}}
.dcard{{background:rgba(15,23,42,.5);border-radius:.75rem;border:1px solid #1e293b;padding:1.1rem}}
.dcard h2{{margin:0 0 .6rem;font-size:.85rem;border:0;padding:0}}
.dcard ul{{list-style:none;padding:0;color:#94a3b8;font-size:.75rem;line-height:1.7}}
footer{{color:var(--mut);font-size:12px;margin-top:44px;padding-top:16px;border-top:1px solid var(--bd)}}
</style></head><body><div class="wrap">

<h1>GitHub Portfolio: Before and After</h1>
<div class="sub">Champ-Deep &middot; {before['owned_total']} owned repositories &middot;
{len(common)} active projects compared &middot;
{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</div>

<div class="kpis">
  <div class="kpi"><div class="v">{before['owned_total']}</div><div class="l">Owned repos</div></div>
  <div class="kpi"><div class="v">{len(common)}</div><div class="l">Active projects</div></div>
  <div class="kpi"><div class="v">{len(readme_fixed)}</div><div class="l">READMEs written</div></div>
  <div class="kpi"><div class="v">{len(branch_fixed)}</div><div class="l">Branches fixed</div></div>
  <div class="kpi"><div class="v">{pub_prot}/{len(pub)}</div><div class="l">Public protected</div></div>
  <div class="kpi"><div class="v">{len(backups)}</div><div class="l">Backups</div></div>
  <div class="kpi"><div class="v">{len(forks)}</div><div class="l">Forks</div></div>
</div>

<h2>What changed</h2>
<p class="sub" style="margin:-4px 0 0">Compared on the same {len(common)} repositories
present in both audits. Counts are repositories <em>missing</em> the item, so a
negative number is an improvement.</p>
<table><thead><tr><th>Item</th><th style="text-align:right">Before</th>
<th style="text-align:right">After</th><th style="text-align:right">Change</th></tr></thead>
<tbody>{body}</tbody></table>

<h2>READMEs written</h2>
<div class="box ok">Each was written from that repository&rsquo;s own source:
its manifests, route tables, ADRs, migrations and setup docs. Not templated.
{escape(", ".join(readme_fixed))}.</div>

<h2>Default branches</h2>
<div class="box ok">{escape(", ".join(branch_fixed))} were serving a working branch
as their default. In each case <code>main</code> was created at the same commit and
the default repointed. No branch was renamed or deleted, so existing clones and
open pull requests are unaffected.</div>

<h2>Branch protection: what is and is not possible</h2>
<div class="box ok"><strong>Public repositories: {pub_prot} of {len(pub)} protected.</strong>
Force-push and branch deletion are blocked and conversations must be resolved.</div>
<div class="box warn"><strong>Private repositories: {priv_prot} of {len(priv)} protected.</strong>
GitHub returns <code>403 Upgrade to GitHub Pro</code> for both branch protection
<em>and</em> rulesets on private repos. This is an account-tier limit, not a
settings problem, and it cannot be fixed from the API. Closing it needs GitHub Pro,
or moving a repo to public.</div>
<p class="sub" style="font-size:13px;max-width:78ch">Required pull-request reviews were
deliberately not enabled. On a single-owner account that locks the owner out of
their own repository, and the free plan does not allow an admin bypass.</p>

<h2>Portfolio map</h2>
<p class="sub" style="margin:-4px 0 0">All {len(common)} active projects grouped by
what they do, derived from each repo&rsquo;s manifests and documentation.</p>
<div class="diagram">{diag}</div>

<h2>Still outstanding</h2>
<div class="box warn"><strong>{escape(", ".join(r["name"] for r in empty)) if empty else "No empty repos"}</strong>
{("<code>"+escape(empty[0]["name"])+"</code> has zero commits. It renders as a broken link and cannot be cloned. It needs either a first commit or deletion, and only you can say which.") if empty else ""}</div>
<div class="box warn"><strong>Exposed credential.</strong>
<code>Partner-Portal</code> has <code>web/.env</code> committed, containing an
<code>AUTH_SECRET</code>, and its <code>.gitignore</code> does not cover
<code>.env</code>. The secret must be rotated and the file purged from history.
Deleting the file alone is not enough, because git retains it.</div>
<div class="box info"><strong>No LICENSE files: {count(lambda r: not r['has_license_file'], o2)} of {len(common)}.</strong>
Left alone deliberately. Most of these are internal Champions Group products and
the correct licence is a business decision, not a default to guess.</div>
<div class="box info"><strong>No CI: {count(lambda r: not r['has_ci'], o2)} of {len(common)}.</strong>
Worth adding to the active projects, in this order: {escape(", ".join(n for n in common if not o2[n]['has_ci'] and idle(o2[n])<=30))}.</div>
<div class="box info"><strong>{len(backups)} backups and {len(forks)} forks</strong> remain,
excluded from every count above. Two backups have no live counterpart under the
name I would have guessed (<code>ChampUTM-backup</code>,
<code>ChampVideo-local-backup</code>) and need a manual look. Fork merge debt is
real in three: <code>Champ-obscura</code>, <code>Champ_Onboarding</code> and
<code>self-hosted-ai-starter-kit</code> were touched recently without upstream sync.</div>

<footer>Generated from live GitHub API data by
<code>github-portfolio-audit</code>. Every figure was re-read from the API after
the change; nothing here is asserted from a write response.</footer>

</div></body></html>"""

    with open(out, "w") as f:
        f.write(html)
    print(f"wrote {out}")
    for label, why, b, a, d in table_rows:
        print(f"  {label:34s} {b:3d} -> {a:3d}  ({d:+d})")


if __name__ == "__main__":
    main()
