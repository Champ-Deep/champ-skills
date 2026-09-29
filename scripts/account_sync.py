#!/usr/bin/env python3
"""Plan and record the daily sync of Champ's Claude account skills into this repo.

The account skills live in the cloud session (/root/.claude/skills/synced/<id>/<skill>/),
the repo lives on the Mac. The scheduled task hashes the account side in the cloud, drops
the result at .sync/account.json, then runs this script on the Mac:

  python3 scripts/account_sync.py plan     -> prints a JSON plan (what to copy, what to skip)
  python3 scripts/account_sync.py record S1 S2 ...  -> marks those skills as synced

Safety model (so a stale account copy never overwrites newer repo work):
  .sync/account-manifest.json holds, per skill, the account hash that was last pushed.
  - account hash == manifest hash           -> account unchanged since last sync: skip
  - account changed, repo copy still equals the manifest-era content -> UPDATE (safe)
  - account changed AND repo copy also changed since last sync       -> CONFLICT, skip, report
  - skill not in repo at all                 -> NEW (the task picks the category)
Hashes cover only the files the account copy has, so extra repo files (evals, scripts
added later) never count as drift and are never deleted.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYNC = os.path.join(ROOT, ".sync")
ACCOUNT = os.path.join(SYNC, "account.json")
MANIFEST = os.path.join(SYNC, "account-manifest.json")
SKILL_ROOTS = ["design/skills", "design/brand-guidelines", "marketing", "sales", "research",
               "documents", "engineering", "software-development", "productivity", "vault"]


def load(p, default):
    try:
        return json.load(open(p))
    except Exception:
        return default


def combined(files):
    """files: {relpath: sha256}. Same formula the cloud side uses."""
    return hashlib.sha256("\n".join(f"{k}:{files[k]}" for k in sorted(files)).encode()).hexdigest()


def repo_skills():
    out = {}
    for base in SKILL_ROOTS:
        d = os.path.join(ROOT, base)
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            if os.path.isfile(os.path.join(d, name, "SKILL.md")):
                out[name] = f"{base}/{name}"
    for name in os.listdir(ROOT):
        if not name.startswith(".") and os.path.isfile(os.path.join(ROOT, name, "SKILL.md")):
            out.setdefault(name, name)
    return out


def repo_hash(path, rels):
    files = {}
    for r in rels:
        p = os.path.join(ROOT, path, r)
        if not os.path.isfile(p):
            return None
        files[r] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return combined(files)


def plan():
    acct = load(ACCOUNT, None)
    if acct is None:
        print(json.dumps({"error": "missing .sync/account.json"}))
        return 2
    man = load(MANIFEST, {})
    repo = repo_skills()
    res = {"new": [], "update": [], "conflict": [], "repo_ahead": [], "unchanged": 0, "excluded": []}
    for skill, info in sorted(acct.get("skills", {}).items()):
        if info.get("excluded"):
            res["excluded"].append({"skill": skill, "reason": info["excluded"]})
            continue
        a_hash = combined(info["files"])
        if skill not in repo:
            res["new"].append({"skill": skill, "files": sorted(info["files"])})
            continue
        path = repo[skill]
        r_hash = repo_hash(path, info["files"].keys())
        last = man.get(skill)
        if r_hash == a_hash:
            res["unchanged"] += 1
        elif last == a_hash:
            res["repo_ahead"].append({"skill": skill, "path": path})
        elif last is None or r_hash == last:
            res["update"].append({"skill": skill, "path": path, "files": sorted(info["files"])})
        else:
            res["conflict"].append({"skill": skill, "path": path})
    print(json.dumps(res, indent=1))
    return 0


def record(skills):
    acct = load(ACCOUNT, {"skills": {}})
    man = load(MANIFEST, {})
    for s in skills:
        if s in acct["skills"]:
            man[s] = combined(acct["skills"][s]["files"])
    os.makedirs(SYNC, exist_ok=True)
    json.dump(dict(sorted(man.items())), open(MANIFEST, "w"), indent=1)
    print(f"recorded {len(skills)} skill(s)")
    return 0


def baseline():
    """One-time: record every account skill whose repo copy matches, plus repo-ahead ones."""
    acct = load(ACCOUNT, {"skills": {}})
    man = load(MANIFEST, {})
    repo = repo_skills()
    n = 0
    for s, info in acct["skills"].items():
        if info.get("excluded") or s not in repo:
            continue
        man[s] = combined(info["files"])
        n += 1
    os.makedirs(SYNC, exist_ok=True)
    json.dump(dict(sorted(man.items())), open(MANIFEST, "w"), indent=1)
    print(f"baseline recorded for {n} skill(s)")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "plan"
    if cmd == "plan":
        sys.exit(plan())
    if cmd == "record":
        sys.exit(record(sys.argv[2:]))
    if cmd == "baseline":
        sys.exit(baseline())
    print(__doc__)
    sys.exit(1)
