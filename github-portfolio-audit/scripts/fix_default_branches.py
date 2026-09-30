#!/usr/bin/env python3
"""
Fix repos whose default branch is a feature or working branch.

A repo whose default branch is `claude/odysseus-productization-hp0dv0` hands
every visitor and every `git clone` half-finished work, and branch protection
attaches to that branch, so governance written against it protects the wrong
thing.

Two shapes, handled differently:
  * main already exists -> just repoint the default.
  * the feature branch is the ONLY branch -> create `main` at the same commit
    and repoint. Never rename: renaming the default branch breaks existing
    clones and open PRs for no gain, and creating it is reversible in one call.

The original branch is always left in place. Nothing is deleted.

Usage: fix_default_branches.py [--dry-run]
"""
import json
import subprocess
import sys
import time


def gh(args, body=None, timeout=45, tries=4):
    last = None
    for i in range(tries):
        cmd = ["gh", "api"] + args
        if body is not None:
            cmd += ["--input", "-"]
        try:
            p = subprocess.run(cmd, input=body, capture_output=True, text=True,
                               timeout=timeout)
            if p.returncode == 0:
                out = p.stdout.strip()
                if not out:
                    return {}
                # `--jq` returns a bare string, not JSON. Only attempt a parse
                # and fall back to the raw text.
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
    dry = "--dry-run" in sys.argv
    repos = [
        # (full_name, current_default, has_main)
        ("Champ-Deep/100xLongevity", "frontend-implementation", True),
        ("Champ-Deep/ChampHQ", "claude/odysseus-productization-hp0dv0", False),
        ("Champ-Deep/lakeb2b-affiliate-portal", "claude/plan-online-strategy-6z5gx", False),
    ]
    for full, cur, has_main in repos:
        print(f"\n── {full}  (default was {cur})")
        if not has_main:
            # Get the current default's commit so `main` is an exact copy.
            ref = gh([f"repos/{full}/git/ref/heads/{cur}"])
            if "__error__" in ref or "object" not in ref:
                print(f"   cannot read ref: {ref}")
                continue
            sha = ref["object"]["sha"]
            print(f"   creating main at {sha[:10]} (copy of {cur})")
            if dry:
                continue
            made = gh([f"repos/{full}/git/refs", "-X", "POST"],
                      body=json.dumps({"ref": "refs/heads/main", "sha": sha}))
            if "__error__" in made:
                print(f"   create failed: {made['__error__'][:120]}")
                continue
            print("   created refs/heads/main")
        if dry:
            print("   would set default_branch=main")
            continue
        upd = gh([f"repos/{full}", "-X", "PATCH", "-f", "default_branch=main"])
        if "__error__" in upd:
            print(f"   patch failed: {upd['__error__'][:140]}")
            continue
        chk = gh([f"repos/{full}", "--jq", ".default_branch"])
        print(f"   verified default_branch = {chk if not isinstance(chk, dict) else chk}")


if __name__ == "__main__":
    main()
