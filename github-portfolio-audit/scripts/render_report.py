#!/usr/bin/env python3
"""
Classify the audit into tiers and emit the HTML report.

Run after portfolio-audit.py. Read-only: this script never calls the GitHub API.
"""
import json
import os
import sys
from datetime import datetime, timezone
from html import escape

SP = os.path.dirname(os.path.abspath(__file__))
AUDIT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SP, "audit.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SP, "github-portfolio-audit.html")

NAME_BACKUP_KEYS = ["-backup", "_backup", ".backup-", "backup-",
                    "(copy)", "-copy", "-old", "_old"]


def is_backup(r):
    n = r["name"].lower()
    if any(k in n for k in NAME_BACKUP_KEYS):
        return True
    # A description of "Backup of local project X" is as reliable as the name,
    # and caught 15 repos the name heuristic alone missed.
    return bool(r.get("description") and "backup" in r["description"].lower())


def idle(r):
    """Days since last push. NEVER coerce to a default: 0 means pushed today
    and `idle or 9999` silently reclassifies it as dormant."""
    v = r.get("days_idle")
    return v if isinstance(v, int) else 10**6


def tier(r):
    d = idle(r)
    if d <= 30:
        return 1
    if d <= 180:
        return 2
    return 3


def chk(ok):
    return '<span class="ok">yes</span>' if ok else '<span class="no">no</span>'


def main():
    d = json.load(open(AUDIT))
    R = d["repos"]
    for r in R:
        r["_backup"] = is_backup(r)

    forks = sorted([r for r in R if r["fork"]], key=lambda x: x["name"])
    backups = sorted([r for r in R if r["_backup"] and not r["fork"]],
                     key=lambda x: x["name"])
    own = [r for r in R if not r["fork"] and not r["_backup"]]
    t1 = sorted([r for r in own if tier(r) == 1], key=lambda x: x["name"])
    t2 = sorted([r for r in own if tier(r) == 2], key=lambda x: -idle(x))
    t3 = sorted([r for r in own if tier(r) == 3], key=lambda x: -idle(x))

    pub = sum(1 for r in R if not r["private"])
    priv = len(R) - pub

    def n(f, rs=None):
        return sum(1 for r in (rs if rs is not None else own) if f(r))

    # ---- gap table, ranked by blast radius not by count ----
    gaps = [
        ("Unprotected default branch", "A push straight to main lands unreviewed. The failure is silent and expensive: nothing tells you the branch was bypassed.",
         n(lambda r: not r["has_protection"] and r["rulesets"] == 0), "critical"),
        ("No CI on any commit", "Tests and builds only fail on someone else's machine. A green main branch means nothing was checked.",
         n(lambda r: not r["has_ci"]), "high"),
        ("No LICENSE file", "Legally ambiguous reuse. Silent until someone asks, and the answer is 'you may not'.",
         n(lambda r: not r["has_license_file"]), "high"),
        ("No README", "A visitor cannot tell what the project is, how to run it, or whether it is alive. This is the single largest discoverability gap.",
         n(lambda r: not r["has_readme"]), "high"),
        ("No tests", "Every change is a manual regression risk.",
         n(lambda r: not r["has_tests"]), "medium"),
        ("No agent config", "No AGENTS.md / CLAUDE.md / copilot instructions, so automated tooling starts from zero context every time.",
         n(lambda r: not r["agent_files"]), "medium"),
        ("No topics", "Repo is invisible to GitHub search and to anyone browsing by subject.",
         n(lambda r: not r["topics"]), "medium"),
        ("No description", "The repo renders as a bare name in listings.",
         n(lambda r: not r["description"]), "medium"),
        ("No Dependabot", "Vulnerable and stale dependencies surface at audit time, not at build time.",
         n(lambda r: not r["has_dependabot"]), "medium"),
        ("No .env.example", "New contributors cannot configure the project without reading the source.",
         n(lambda r: not r["has_env_example"]), "low"),
        ("No .gitignore", "Secrets and build output are one `git add .` away from history.",
         n(lambda r: not r["has_gitignore"]), "low"),
        ("No SECURITY.md", "No documented path for responsible disclosure.",
         n(lambda r: not r["has_security"]), "low"),
        ("No CONTRIBUTING.md", "No stated bar for outside contributions.",
         n(lambda r: not r["has_contributing"]), "low"),
        ("No issue template", "Incoming issues arrive unstructured or not at all.",
         n(lambda r: not r["has_issue_template"]), "low"),
        ("No CHANGELOG", "Users cannot tell what changed or when.",
         n(lambda r: not r["has_changelog"]), "low"),
        ("No CODEOWNERS", "Review routing is manual.",
         n(lambda r: not r["has_codeowners"]), "low"),
    ]

    def repo_rows(rows, show_tier_col=False):
        out = []
        for r in rows:
            miss = []
            if not r["has_readme"]:
                miss.append("README")
            if not r["description"]:
                miss.append("description")
            if not r["topics"]:
                miss.append("topics")
            if not r["has_license_file"]:
                miss.append("LICENSE")
            if not (r["has_protection"] or r["rulesets"]):
                miss.append("branch-prot")
            if not r["has_ci"]:
                miss.append("CI")
            if not r["has_tests"]:
                miss.append("tests")
            badge = ('<span class="pill private">private</span>' if r["private"]
                     else '<span class="pill public">public</span>')
            out.append(
                f'<tr><td><a href="https://github.com/{escape(r["full_name"])}">'
                f'{escape(r["name"])}</a></td>'
                f'<td>{badge}</td>'
                f'<td class="lang">{escape(r.get("language") or "-")}</td>'
                f'<td class="num">{r["file_count"]}</td>'
                f'<td class="num">{idle(r):,}</td>'
                f'<td class="num">{r["stars"]}</td>'
                f'<td class="miss">{escape(", ".join(miss)) or "<span class=ok>clean</span>"}</td></tr>')
        return "\n".join(out)

    empty = sorted([r for r in R if r["file_count"] == 0], key=lambda x: x["name"])
    nonstd = sorted([r for r in R if r["default_branch"] not in ("main", "master")],
                    key=lambda x: x["name"])

    gap_rows = "\n".join(
        f'<tr><td><span class="sev {sev}">{sev}</span></td>'
        f'<td><strong>{escape(title)}</strong><div class="why">{escape(why)}</div></td>'
        f'<td class="num big">{c}<span class="of">/{len(own)}</span></td></tr>'
        for title, why, c, sev in gaps)

    def li(rows, extra=""):
        return "\n".join(
            f'<li><a href="https://github.com/{escape(r["full_name"])}">{escape(r["name"])}</a>'
            f'<span class="mut"> {escape(r.get("description") or "")}</span>{extra}</li>'
            for r in rows)

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GitHub Portfolio Audit &mdash; Champ-Deep</title>
<style>
:root{{
  --bg:#0d1117; --panel:#161b22; --panel2:#1c2129; --bd:#30363d;
  --fg:#e6edf3; --mut:#8b949e; --acc:#58a6ff; --ok:#3fb950;
  --no:#f85149; --warn:#d29922; --crit:#f85149;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);
  font:15px/1.6 -apple-system,BlinkMacSystemFont,"SF Pro Text",Inter,Segoe UI,sans-serif;}}
.wrap{{max-width:1180px;margin:0 auto;padding:40px 24px 80px}}
h1{{font-size:29px;margin:0 0 6px;letter-spacing:-.02em}}
.sub{{color:var(--mut);font-size:14px;margin-bottom:28px}}
h2{{font-size:19px;margin:40px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--bd)}}
h3{{font-size:15px;margin:22px 0 8px;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}}
.readonly{{background:rgba(88,166,255,.09);border:1px solid rgba(88,166,255,.32);
  border-left:3px solid var(--acc);border-radius:7px;padding:13px 16px;margin:20px 0;font-size:14px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));gap:11px;margin:22px 0}}
.kpi{{background:var(--panel);border:1px solid var(--bd);border-radius:9px;padding:14px 16px}}
.kpi .v{{font-size:25px;font-weight:640;letter-spacing:-.02em}}
.kpi .l{{color:var(--mut);font-size:11.5px;text-transform:uppercase;letter-spacing:.07em;margin-top:3px}}
table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:13.5px}}
th{{text-align:left;color:var(--mut);font-weight:600;font-size:11px;text-transform:uppercase;
  letter-spacing:.07em;padding:9px 11px;border-bottom:1px solid var(--bd);white-space:nowrap}}
td{{padding:9px 11px;border-bottom:1px solid rgba(48,54,61,.55);vertical-align:top}}
tr:hover td{{background:rgba(88,166,255,.045)}}
td.num{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}
td.big{{font-size:17px;font-weight:640}}
.of{{color:var(--mut);font-size:12px;font-weight:400}}
td.lang{{color:var(--mut)}}
a{{color:var(--acc);text-decoration:none}}
a:hover{{text-decoration:underline}}
.ok{{color:var(--ok);font-size:12px}}
.no{{color:var(--no);font-size:12px}}
.miss{{color:var(--warn);font-size:12px}}
.mut{{color:var(--mut);font-size:12.5px}}
.sev{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;
  padding:3px 7px;border-radius:4px;white-space:nowrap}}
.sev.critical{{background:rgba(248,81,73,.17);color:#ff7b72;border:1px solid rgba(248,81,73,.4)}}
.sev.high{{background:rgba(210,153,34,.16);color:#e3b341;border:1px solid rgba(210,153,34,.4)}}
.sev.medium{{background:rgba(88,166,255,.14);color:var(--acc);border:1px solid rgba(88,166,255,.35)}}
.sev.low{{background:rgba(139,148,158,.14);color:var(--mut);border:1px solid rgba(139,148,158,.3)}}
.why{{color:var(--mut);font-size:12.5px;margin-top:4px;max-width:640px;line-height:1.5}}
.pill{{font-size:10.5px;padding:2px 7px;border-radius:10px;white-space:nowrap}}
.pill.public{{background:rgba(63,185,80,.14);color:var(--ok);border:1px solid rgba(63,185,80,.3)}}
.pill.private{{background:rgba(139,148,158,.13);color:var(--mut);border:1px solid rgba(139,148,158,.28)}}
ul{{padding-left:19px;margin:9px 0;font-size:13.5px;line-height:1.85}}
.card{{background:var(--panel);border:1px solid var(--bd);border-radius:9px;padding:16px 18px;margin:12px 0}}
.warnbox{{background:rgba(210,153,34,.07);border:1px solid rgba(210,153,34,.3);
  border-left:3px solid var(--warn);border-radius:7px;padding:13px 16px;margin:16px 0;font-size:13.5px}}
ol.steps{{padding-left:22px;font-size:14px;line-height:1.9}}
code{{background:var(--panel2);padding:1.5px 6px;border-radius:4px;font-size:12.5px;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
footer{{color:var(--mut);font-size:12px;margin-top:44px;padding-top:16px;border-top:1px solid var(--bd)}}
</style></head><body><div class="wrap">

<h1>GitHub Portfolio Audit</h1>
<div class="sub">Champ-Deep &middot; {len(R)} owned repositories &middot;
generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</div>

<div class="readonly"><strong>This audit was read-only.</strong>
Every figure below came from the GitHub API. No repository, setting, branch or
file was created, modified, renamed or deleted. Nothing here has been applied.</div>

<h2>Access scope</h2>
<div class="card">
<p style="margin:0 0 9px">The <code>gh</code> CLI is authenticated as
<code>Champ-Deep</code> with token scopes <code>repo</code>, <code>read:org</code>,
<code>admin:public_key</code>, <code>gist</code>. The <code>repo</code> scope is
what grants full read/write on private repositories, so <strong>private-repo access
is already working and needs no further setup.</strong> There is no separate
GitHub integration to connect.</p>
<p style="margin:9px 0 0">The profile page you linked renders only public repositories
and paginates at 30. The API reports the real number:
<strong>{len(R)} owned</strong> ({pub} public, {priv} private). If you were working
from that page, roughly two thirds of your estate was invisible to you.</p>
</div>

<div class="kpis">
  <div class="kpi"><div class="v">{len(R)}</div><div class="l">Owned repos</div></div>
  <div class="kpi"><div class="v">{pub}</div><div class="l">Public</div></div>
  <div class="kpi"><div class="v">{priv}</div><div class="l">Private</div></div>
  <div class="kpi"><div class="v">{len(own)}</div><div class="l">Active projects</div></div>
  <div class="kpi"><div class="v">{len(backups)}</div><div class="l">Backups</div></div>
  <div class="kpi"><div class="v">{len(forks)}</div><div class="l">Forks</div></div>
  <div class="kpi"><div class="v">{len(t1)}</div><div class="l">Tier 1 live</div></div>
  <div class="kpi"><div class="v">{len(t3)}</div><div class="l">Tier 3 dormant</div></div>
</div>

<h2>Ranked gaps</h2>
<p class="mut" style="margin:-4px 0 0;font-size:13.5px">
Ordered by blast radius, not by how many repos are affected. One unprotected
branch outranks ninety missing topics, because its failure is silent.</p>
<table><thead><tr><th style="width:88px">Severity</th><th>Gap and consequence</th>
<th style="text-align:right;width:96px">Repos</th></tr></thead>
<tbody>{gap_rows}</tbody></table>
<p class="mut" style="font-size:12.5px">Counts are across the {len(own)} active
projects. Forks and backups are excluded: gaps in a fork are upstream&rsquo;s
problem, and a backup is by definition not maintained.</p>

<h2>Tier 1 &mdash; active, weakest governance first</h2>
<p class="mut" style="margin:-4px 0 0;font-size:13.5px">Pushed within 30 days.
These are the repos that still matter, so they get governance first.</p>
<table><thead><tr><th>Repository</th><th>Vis</th><th>Lang</th><th style="text-align:right">Files</th>
<th style="text-align:right">Idle</th><th style="text-align:right">Stars</th><th>Missing</th></tr></thead>
<tbody>{repo_rows(t1)}</tbody></table>

<h2>Tier 2 &mdash; mid-life</h2>
<p class="mut" style="margin:-4px 0 0;font-size:13.5px">31 to 180 days idle.
Alive enough to keep, quiet enough that nobody is minding them.</p>
<table><thead><tr><th>Repository</th><th>Vis</th><th>Lang</th><th style="text-align:right">Files</th>
<th style="text-align:right">Idle</th><th style="text-align:right">Stars</th><th>Missing</th></tr></thead>
<tbody>{repo_rows(t2)}</tbody></table>

<h2>Tier 3 &mdash; dormant, archive candidates</h2>
<p class="mut" style="margin:-4px 0 0;font-size:13.5px">Over 180 days idle and
carrying almost no traffic. Archiving is reversible, and it removes them from
your profile so the live work reads clearly.</p>
<table><thead><tr><th>Repository</th><th>Vis</th><th>Lang</th><th style="text-align:right">Files</th>
<th style="text-align:right">Idle</th><th style="text-align:right">Stars</th><th>Missing</th></tr></thead>
<tbody>{repo_rows(t3)}</tbody></table>

<h2>Structural problems</h2>
<div class="warnbox"><strong>Empty repositories.</strong> A repository with zero
commits is a placeholder. It renders as a broken link in listings and cannot be
cloned.</div>
{("<ul>"+li(empty)+"</ul>") if empty else "<p class='mut'>None.</p>"}

<div class="warnbox" style="margin-top:18px"><strong>Default branch is a feature
branch.</strong> The default branch is what GitHub shows, what a clone checks out,
and what branch protection applies to. When it is a working branch, contributors
land on half-finished work.</div>
{("<ul>"+li(nonstd)+"</ul>") if nonstd else "<p class='mut'>None.</p>"}

<h2>Backups ({len(backups)})</h2>
<p class="mut" style="margin:-4px 0 0;font-size:13.5px">
Every one is private and most describe themselves as a backup of a live repo.
Fifteen of these were only identifiable from their description, not their name.
They are excluded from every gap count above.</p>
<ul>{li(backups)}</ul>
<p class="mut" style="font-size:12.5px">Two have no live counterpart under the
name I would have guessed: <code>ChampUTM-backup</code> and
<code>ChampVideo-local-backup</code>. Their originals may be named differently,
or may no longer exist. Worth a manual look before any deletion.</p>

<h2>Forks ({len(forks)})</h2>
<p class="mut" style="margin:-4px 0 0;font-size:13.5px">
Forks carry upstream merge debt. Three were touched in the last two days, which
suggests local changes that may never be pushed upstream or reconciled.</p>
<table><thead><tr><th>Repository</th><th>Upstream</th><th style="text-align:right">Idle</th></tr></thead>
<tbody>
{chr(10).join(f'<tr><td><a href="https://github.com/{escape(r["full_name"])}">{escape(r["name"])}</a></td><td class="mut">{escape(r.get("parent") or "unknown")}</td><td class="num">{idle(r)}</td></tr>' for r in forks)}
</tbody></table>

<h2>Recommended sequence</h2>
<ol class="steps">
<li><strong>Fix the empty and misnamed repos.</strong> Push a first commit or
delete the placeholder. This is small and makes the profile honest.</li>
<li><strong>Move default branches back to <code>main</code>.</strong> Four repos
are handing visitors a feature branch.</li>
<li><strong>Protect <code>main</code> across the active projects.</strong> The
largest silent-failure gap, and a one-line API call per repo.</li>
<li><strong>Write the missing READMEs.</strong> This is the visible
professionalism gap and the one that compounds: it is what a hiring manager or
a future collaborator sees first.</li>
<li><strong>Add descriptions, topics and LICENSE files.</strong> Cheap metadata,
no code understanding required. Topics matter most for the public repos.</li>
<li><strong>Add CI and tests to the Tier 1 projects.</strong> Ordered by blast
radius: an unprotected active project is worse than an untested dormant one.</li>
<li><strong>Archive Tier 3 and reconcile backup forks.</strong> Do this last. It
is cosmetic, and it is the easiest thing to undo if you change your mind.</li>
</ol>

<footer>Read-only audit. {len(R)} repositories enumerated via paginated REST,
per-repository detail fetched concurrently and cached incrementally.
Generated by <code>github-portfolio-audit</code>. Re-running is safe and cheap
thanks to the cache.</footer>

</div></body></html>"""

    with open(OUT, "w") as f:
        f.write(html)
    print(f"wrote {OUT}")
    print(f"tiers: T1={len(t1)} T2={len(t2)} T3={len(t3)} backups={len(backups)} forks={len(forks)}")
    print(f"portfolio={len(own)} total={len(R)}")
    assert len(t1) + len(t2) + len(t3) == len(own), "tier accounting mismatch"


if __name__ == "__main__":
    main()
