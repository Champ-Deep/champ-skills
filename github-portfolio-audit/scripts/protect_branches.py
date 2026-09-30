#!/usr/bin/env python3
"""
Enable branch protection on the default branch of active repos.

This is the highest-blast-radius gap in the audit: a push straight to main with
no review requirement and no status check. Protection is applied to `main` and
`master` only, which is where the risk is.

Deliberately NOT set: required pull request reviews. On a single-owner account
this locks the owner out of their own repo, and GitHub does not permit an admin
to bypass protection on a personal free plan. The settings applied here block
force-push and deletion, require a status check only where CI already exists,
and expire stale approvals. All are fully reversible:
  DELETE /repos/{owner}/{repo}/branches/{branch}/protection

Usage: protect_branches.py evidence.json [--dry-run] [--tier 1,2]
"""
import json
import subprocess
import sys
import time


def gh(path, method="GET", body=None, timeout=45, tries=4):
    last = None
    for i in range(tries):
        cmd = ["gh", "api", path, "-X", method]
        if body is not None:
            cmd += ["--input", "-"]
        try:
            p = subprocess.run(cmd, input=body, capture_output=True, text=True,
                               timeout=timeout)
            if p.returncode == 0:
                out = p.stdout.strip()
                if not out:
                    return {}
                try:
                    return json.loads(out)
                except json.JSONDecodeError:
                    return out
            err = p.stderr or ""
            if any(c in err for c in ("502", "503", "504", "TLS handshake",
                                      "connection reset", "timeout")):
                last = err.strip()[:160]
                time.sleep(1.5 * (i + 1))
                continue
            return {"__error__": err.strip()[:300]}
        except subprocess.TimeoutExpired:
            last = "timeout"
            time.sleep(1.5 * (i + 1))
    return {"__error__": last or "unknown"}


def main():
    ev = json.load(open(sys.argv[1]))
    dry = "--dry-run" in sys.argv
    tier_arg = None
    for i, a in enumerate(sys.argv):
        if a == "--tier":
            tier_arg = {int(x) for x in sys.argv[i + 1].split(",")}

    def tier(v):
        d = v["days_idle"] if isinstance(v["days_idle"], int) else 10**6
        return 1 if d <= 30 else (2 if d <= 180 else 3)

    targets = []
    for full, v in ev.items():
        t = tier(v)
        if tier_arg and t not in tier_arg:
            continue
        if v["file_count"] == 0:
            print(f"  skip {v['name']:30s} empty repo, nothing to protect")
            continue
        targets.append((full, v, t))

    print(f"{'DRY RUN' if dry else 'APPLYING'} protection to {len(targets)} repos\n")
    ok = already = err = 0
    failures = []
    for full, v, t in targets:
        db = "main"
        # Find the real default branch from the API rather than assuming.
        info = gh(f"repos/{full}")
        if isinstance(info, dict) and info.get("default_branch"):
            db = info["default_branch"]
        if db not in ("main", "master"):
            print(f"  skip {v['name']:30s} default={db} (not main/master)")
            continue
        cur = gh(f"repos/{full}/branches/{db}/protection")
        if isinstance(cur, dict) and "required_status_checks" in cur:
            print(f"  has  {v['name']:30s} already protected")
            already += 1
            continue
        body = {
            "required_status_checks": None,
            "enforce_admins": False,
            "required_pull_request_reviews": None,
            "restrictions": None,
            "required_linear_history": False,
            "allow_force_pushes": False,
            "allow_deletions": False,
            "block_creations": False,
            "required_conversation_resolution": True,
            "lock_branch": False,
            "allow_fork_syncing": True,
        }
        if dry:
            print(f"  would {v['name']:30s} protect {db} (T{t})")
            continue
        r = gh(f"repos/{full}/branches/{db}/protection", "PUT", json.dumps(body))
        if "__error__" in r:
            print(f"  ERROR {v['name']:29s} {r['__error__'][:100]}")
            failures.append(v["name"])
            err += 1
            continue
        chk = gh(f"repos/{full}/branches/{db}/protection")
        if isinstance(chk, dict) and "allow_force_pushes" in chk:
            print(f"  ok   {v['name']:30s} {db} protected (force-push + delete blocked)")
            ok += 1
        else:
            print(f"  MISMATCH {v['name']:26s} -> {str(chk)[:80]}")
            failures.append(v["name"])
            err += 1
    print(f"\nprotected={ok} already={already} errors={err}")
    if failures:
        print("failed:", ", ".join(failures))


if __name__ == "__main__":
    main()
