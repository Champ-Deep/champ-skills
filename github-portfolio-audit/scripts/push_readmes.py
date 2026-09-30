#!/usr/bin/env python3
"""
Commit the written READMEs to their repos via the GitHub contents API.

Each README is committed on its own branch and merged, so history stays linear
and each change is independently revertable. A direct commit to the default
branch would be faster and would also be the one thing nobody can undo cleanly.

Every write is verified with an independent GET of the file, because a 200 from
the contents API means the blob was created, not that it is what you meant.

Usage: push_readmes.py readmes/ [--dry-run]
"""
import base64
import json
import os
import subprocess
import sys
import time

# file stem -> repo full name
TARGETS = {
    "ChampLens": "Champ-Deep/ChampLens",
    "Investor-Module": "Champ-Deep/Investor-Module",
    "ChampIQ": "Champ-Deep/ChampIQ",
    "Partner-Portal": "Champ-Deep/Partner-Portal",
    "pikvita-quiz": "Champ-Deep/pikvita-quiz",
    "ChampHQ": "Champ-Deep/ChampHQ",
}

BRANCH = "chore/readme"


def gh(path, method="GET", body=None, timeout=60, tries=4):
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
                last = err.strip()[:200]
                time.sleep(2 * (i + 1))
                continue
            return {"__error__": err.strip()[:400]}
        except subprocess.TimeoutExpired:
            last = "timeout"
            time.sleep(2 * (i + 1))
    return {"__error__": last or "unknown"}


def main():
    rd = sys.argv[1]
    dry = "--dry-run" in sys.argv
    print(f"{'DRY RUN' if dry else 'PUSHING'}: {len(TARGETS)} READMEs\n")
    ok = err = 0
    for stem, full in TARGETS.items():
        path = os.path.join(rd, f"{stem}.md")
        if not os.path.exists(path):
            print(f"  MISSING {stem}: no file at {path}")
            err += 1
            continue
        content = open(path, "rb").read()
        b64 = base64.b64encode(content).decode()

        info = gh(f"repos/{full}")
        db = info.get("default_branch", "main") if isinstance(info, dict) else "main"
        if dry:
            print(f"  would {stem:18s} -> {full} @{db} ({len(content)} bytes)")
            continue

        # 1. branch off the default
        ref = gh(f"repos/{full}/git/ref/heads/{BRANCH}")
        if isinstance(ref, dict) and "object" in ref:
            gh(f"repos/{full}/git/refs/heads/{BRANCH}", "PATCH",
               json.dumps({"sha": ref["object"]["sha"], "force": False}))
        else:
            base = gh(f"repos/{full}/git/ref/heads/{db}")
            made = gh(f"repos/{full}/git/refs", "POST", json.dumps(
                {"ref": f"refs/heads/{BRANCH}", "sha": base["object"]["sha"]}))
            if "__error__" in made:
                print(f"  ERROR {stem:18s} branch: {made['__error__'][:110]}")
                err += 1
                continue

        # 2. create/update README.md on that branch
        existing = gh(f"repos/{full}/contents/README.md?ref={BRANCH}")
        put = {"message": "docs: add README", "content": b64, "branch": BRANCH}
        if isinstance(existing, dict) and existing.get("sha"):
            put["sha"] = existing["sha"]
        r = gh(f"repos/{full}/contents/README.md", "PUT", json.dumps(put))
        if "__error__" in r:
            print(f"  ERROR {stem:18s} write: {r['__error__'][:130]}")
            err += 1
            continue

        # 3. merge into the default branch
        pr = gh(f"repos/{full}/pulls", "POST", json.dumps({
            "title": "docs: add README",
            "head": BRANCH, "base": db,
            "body": "Adds a README written from the repository's actual contents, "
                    "in the house style established by ChampHarbinger.",
        }))
        if "__error__" in pr:
            print(f"  ERROR {stem:18s} pr: {pr['__error__'][:130]}")
            err += 1
            continue
        num = pr["number"]
        m = gh(f"repos/{full}/pulls/{num}/merge", "PUT",
               json.dumps({"merge_method": "squash"}))
        if "__error__" in m:
            print(f"  ERROR {stem:18s} merge: {str(m['__error__'])[:120]}")
            err += 1
            continue

        # 4. verify independently on the default branch
        got = gh(f"repos/{full}/contents/README.md?ref={db}")
        if isinstance(got, dict) and got.get("content"):
            actual = base64.b64decode(got["content"])
            match = actual == content
            print(f"  {'ok  ' if match else 'DIFF'} {stem:18s} PR #{num} merged, "
                  f"README {len(actual)} bytes")
            ok += 1 if match else 0
            if not match:
                err += 1
        else:
            print(f"  VERIFY-FAIL {stem:16s} README not readable on {db}")
            err += 1

        # 5. clean up the working branch
        gh(f"repos/{full}/git/refs/heads/{BRANCH}", "DELETE")
        time.sleep(0.3)

    print(f"\nmerged+verified={ok} errors={err}")
    if err:
        sys.exit(1)


if __name__ == "__main__":
    main()
