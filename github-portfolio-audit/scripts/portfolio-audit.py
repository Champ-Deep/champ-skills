#!/usr/bin/env python3
"""
Portfolio audit: enumerate every repo the viewer owns (public + private) and
collect per-repo governance / hygiene / discoverability evidence.

Design notes (these are the pitfalls the SKILL.md warns about):
  * REST, not GraphQL, for bulk enumeration. A nested GraphQL query over ~100
    repos asking for many fields returns 504/502.
  * affiliation=owner still returns repos where the viewer is a *member*.
    Filter by owner.login before counting anything as "owned".
  * Threaded (6-8 workers) because a full audit is ~12 calls/repo.
  * 403/404 are legitimate "not configured" answers (that is how absent branch
    protection and absent Dependabot are detected), not errors to retry.
  * Per-repo cache written incrementally so a late serialization bug or an
    interrupted run never costs the network work.
  * json.dump(..., default=list) because any set built during classification
    is not JSON serializable.

Usage:
  portfolio-audit.py --out /tmp/audit.json
  portfolio-audit.py --out /tmp/audit.json --refresh   # ignore cache
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

CACHE_DIR = os.path.expanduser("~/.cache/hermes-portfolio-audit")
VIEWER = os.environ.get("HERMES_GH_LOGIN", "Champ-Deep")

# Matches a test file or test directory at any depth: tests/, test_*.py,
# foo.test.ts, foo.spec.jsx, __tests__/...
TEST_RE = re.compile(
    r"(^tests?/)|(^__tests__/)|(test_[^/]+\.py$)|(_test\.(py|go|rb)$)"
    r"|(\.test\.[jt]sx?$)|(\.spec\.[jt]sx?$)"
)


def gh(path, timeout=45, tries=3):
    """gh api with retry only on transient 502/503/504."""
    last = None
    for attempt in range(tries):
        try:
            p = subprocess.run(
                ["gh", "api", path],
                capture_output=True, text=True, timeout=timeout,
            )
            if p.returncode == 0:
                if not p.stdout.strip():
                    return None
                try:
                    return json.loads(p.stdout)
                except json.JSONDecodeError:
                    return None
            err = (p.stderr or "").strip()
            # "HTTP 502" / "502 Bad Gateway" etc. -> transient, retry.
            if any(c in err for c in ("502", "503", "504")):
                last = err
                time.sleep(1.5 * (attempt + 1))
                continue
            # 403/404/422 = endpoint not enabled for this repo. Not an error.
            if any(c in err for c in ("403", "404", "422", "Not Found")):
                return {"__absent__": True}
            last = err
            break
        except subprocess.TimeoutExpired:
            last = "timeout"
            time.sleep(1.5 * (attempt + 1))
    return {"__error__": last or "unknown"}


def enumerate_owned(viewer):
    """All repos owned by viewer, public + private, via paginated REST."""
    out, page = [], 1
    while True:
        rows = gh(f"user/repos?per_page=100&page={page}&affiliation=owner&sort=pushed")
        if not isinstance(rows, list) or not rows:
            break
        out.extend(r for r in rows if r.get("owner", {}).get("login") == viewer)
        if len(rows) < 100:
            break
        page += 1
    return out


def cache_path(full_name):
    return os.path.join(CACHE_DIR, full_name.replace("/", "__") + ".json")


def load_cache(full_name):
    try:
        with open(cache_path(full_name)) as f:
            rec = json.load(f)
    except Exception:
        return None
    # Never replay a cached failure: it would look like a successful audit of a
    # repo that simply has no data. Re-fetch instead.
    if isinstance(rec, dict) and rec.get("__error__"):
        return None
    return rec


def _parent_name(parent):
    """`parent` arrives as a dict from the list payload, or as a plain
    full_name string after main()'s fork disambiguation. Accept both."""
    if isinstance(parent, str):
        return parent or None
    if isinstance(parent, dict):
        return parent.get("full_name")
    return None


def audit_one(repo, viewer):
    """~12 calls per repo. Returns an evidence dict, never raises."""
    full = repo["full_name"]
    name = repo["name"]

    def q(p):
        r = gh(p)
        return r

    # 1. branch protection on the default branch
    db = repo.get("default_branch") or "main"
    prot = q(f"repos/{full}/branches/{db}/protection")
    has_prot = isinstance(prot, dict) and "__absent__" not in prot and "__error__" not in prot

    # 2. protected branches (any)
    pb = q(f"repos/{full}/branches?protected=1")
    protected_branches = [b["name"] for b in pb] if isinstance(pb, list) else []

    # 3. any rulesets (modern replacement for branch protection)
    rs = q(f"repos/{full}/rulesets")
    rulesets = len(rs) if isinstance(rs, list) else 0

    # 4. CI workflows
    wf = q(f"repos/{full}/actions/workflows")
    workflows = []
    if isinstance(wf, dict):
        workflows = [w.get("name", "") for w in wf.get("workflows", [])]

    # 5. Dependabot
    dep = q(f"repos/{full}/dependabot/alerts?per_page=1")
    has_dependabot = isinstance(dep, list)

    # 6. secrets present (names only, never values)
    sec = q(f"repos/{full}/actions/secrets?per_page=100")
    secret_names = [s["name"] for s in sec.get("secrets", [])] if isinstance(sec, dict) else []

    # 7. contributors / activity
    con = q(f"repos/{full}/contributors?per_page=100")
    contributors = [c.get("login") for c in con] if isinstance(con, list) else []

    # 8. root tree -> detect README, LICENSE, agent config, tests, CI dir
    tree = q(f"repos/{full}/git/trees/{db}?recursive=1")
    paths = []
    truncated = False
    if isinstance(tree, dict):
        truncated = bool(tree.get("truncated"))
        paths = [t["path"] for t in tree.get("tree", []) if t.get("type") == "blob"]
    pset = set(paths)

    readmes = sorted(p for p in pset if p.lower().startswith("readme"))
    licenses = sorted(p for p in pset if p.upper().startswith("LICENSE")
                      or p.upper().startswith("COPYING"))
    has_ci_dir = any(p.startswith(".github/workflows/") for p in pset)
    has_tests = any(TEST_RE.search(p) for p in paths)
    agent_files = sorted(p for p in pset if p.upper() in {
        "AGENTS.MD", "CLAUDE.MD", "GEMINI.MD", "CURSOR.RULES", ".CURSORCURSORULES",
        "CONVENTIONS.MD", ".GITHUB/COPILOT-INSTRUCTIONS.MD",
    })
    has_issue_tpl = any(p.startswith(".github/ISSUE_TEMPLATE/") for p in pset)
    has_pr_tpl = ".github/pull_request_template.md" in pset or any(
        p.startswith(".github/PULL_REQUEST_TEMPLATE") for p in pset)
    has_codeowners = ".github/CODEOWNERS" in pset
    has_changelog = any(p.upper() in {"CHANGELOG.MD", "CHANGES.MD"} for p in pset)
    has_contributing = any(p.upper() == "CONTRIBUTING.MD" for p in pset)
    has_security = any(p.upper().startswith("SECURITY.MD") for p in pset)
    has_license_file = bool(licenses)
    env_example = any(p in {".env.example", ".env.sample", ".env.template"} for p in pset)
    gitignore = ".gitignore" in pset

    # 9. open issues / PRs (counts only, for the health table)
    issues = q(f"search/issues?q=repo:{full}+type:issue+state:open&per_page=1")
    n_issues = issues.get("total_count", 0) if isinstance(issues, dict) else 0
    prs = q(f"search/issues?q=repo:{full}+type:pr+state:open&per_page=1")
    n_prs = prs.get("total_count", 0) if isinstance(prs, dict) else 0

    # 10. releases
    rel = q(f"repos/{full}/releases?per_page=1")
    has_releases = isinstance(rel, list) and len(rel) > 0

    # 11. default branch commit count (rough churn signal)
    commits = q(f"repos/{full}/commits?per_page=1")
    has_commits = isinstance(commits, list) and len(commits) > 0

    # 12. stale PR/issue templates, repo size
    pushed = repo.get("pushed_at")
    days_idle = None
    if pushed:
        try:
            dt = datetime.strptime(pushed, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            days_idle = (datetime.now(timezone.utc) - dt).days
        except Exception:
            pass

    return {
        "full_name": full,
        "name": name,
        "private": repo.get("private", False),
        "fork": repo.get("fork", False),
        # NOTE: main() may have replaced the dict `parent` with a plain
        # full_name string. Accept both shapes.
        "parent": _parent_name(repo.get("parent")),
        "archived": repo.get("archived", False),
        "disabled": repo.get("disabled", False),
        "description": repo.get("description"),
        "homepage": repo.get("homepage") or None,
        "topics": repo.get("topics", []),
        "default_branch": db,
        "language": (repo.get("language") or None),
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "open_issues": repo.get("open_issues_count", 0),
        "size_kb": repo.get("size", 0),
        "visibility": "private" if repo.get("private") else "public",
        "created_at": repo.get("created_at"),
        "pushed_at": pushed,
        "days_idle": days_idle,
        "has_protection": has_prot,
        "protected_branches": protected_branches,
        "rulesets": rulesets,
        "workflows": workflows,
        "has_ci": has_ci_dir,
        "has_dependabot": has_dependabot,
        "secret_names": secret_names,
        "contributors": contributors,
        "tree_truncated": truncated,
        "file_count": len(paths),
        "readmes": readmes,
        "has_readme": bool(readmes),
        "readme_stale": None,  # filled by caller if we can cheaply read it
        "has_license_file": has_license_file,
        "licenses": licenses,
        "license_api": (repo.get("license") or {}).get("spdx_id"),
        "has_tests": bool(has_tests),
        "agent_files": agent_files,
        "has_issue_template": has_issue_tpl,
        "has_pr_template": has_pr_tpl,
        "has_codeowners": has_codeowners,
        "has_changelog": has_changelog,
        "has_contributing": has_contributing,
        "has_security": has_security,
        "has_env_example": env_example,
        "has_gitignore": gitignore,
        "n_open_issues": n_issues,
        "n_open_prs": n_prs,
        "has_releases": has_releases,
        "has_commits": has_commits,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--workers", type=int, default=7)
    args = ap.parse_args()

    os.makedirs(CACHE_DIR, exist_ok=True)

    print(f"[1/3] enumerating owned repos for {VIEWER} ...", file=sys.stderr)
    repos = enumerate_owned(VIEWER)
    print(f"      owned: {len(repos)} "
          f"({sum(1 for r in repos if r['private'])} private / "
          f"{sum(1 for r in repos if not r['private'])} public)", file=sys.stderr)

    # Disambiguate forks so they can be reported separately.
    for r in repos:
        if r.get("fork") and not r.get("parent"):
            d = gh(f"repos/{r['full_name']}")
            if isinstance(d, dict):
                r["parent"] = (d.get("parent") or {}).get("full_name")

    print(f"[2/3] auditing {len(repos)} repos with {args.workers} workers ...", file=sys.stderr)
    results = []
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs: dict = {}
        for r in repos:
            if not args.refresh:
                c = load_cache(r["full_name"])
                if c:
                    futs[ex.submit(lambda c=c: c)] = str(r["full_name"])
                    continue
            futs[ex.submit(audit_one, r, VIEWER)] = str(r["full_name"])
        for fut in as_completed(futs):
            try:
                rec = fut.result()
            except Exception as e:  # never lose the whole run to one repo
                # Surface it loudly: a silent per-repo failure looks identical
                # to a repo that genuinely has no data.
                print(f"      ! {futs[fut]}: {e!r}", file=sys.stderr)
                rec = {"full_name": futs[fut], "name": futs[fut].split("/")[-1],
                       "visibility": "unknown", "fork": False,
                       "__error__": repr(e)}
            results.append(rec)
            done += 1
            # Incremental cache write: a late failure never costs the network work.
            try:
                with open(cache_path(rec["full_name"]), "w") as f:
                    json.dump(rec, f, default=list)
            except Exception:
                pass
            if done % 10 == 0 or done == len(repos):
                print(f"      {done}/{len(repos)}", file=sys.stderr)

    results.sort(key=lambda r: r.get("name", ""))
    payload = {
        "viewer": VIEWER,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "owned_total": len(repos),
        "repos": results,
    }
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=1, default=list)
    print(f"[3/3] wrote {args.out} ({len(results)} records)", file=sys.stderr)


if __name__ == "__main__":
    main()
