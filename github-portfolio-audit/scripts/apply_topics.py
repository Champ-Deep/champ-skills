#!/usr/bin/env python3
"""
Set GitHub topics for every active repo via the dedicated topics endpoint.

Why this file exists: PATCH /repos/{owner}/{repo} with a `topics` form field
returns HTTP 200 and silently does nothing. The response comes back with
topics=[] and the repo stays untagged. Topics only stick through
PUT /repos/{owner}/{repo}/topics with a JSON body {"names": [...]}.

That failure is invisible unless you re-read the repo afterwards, which is why
this script verifies every write with an independent GET.

Usage: apply_topics.py evidence.json [--dry-run]
"""
import json
import os
import subprocess
import sys
import time

SP = os.path.dirname(os.path.abspath(__file__))


def gh_json(path, method="GET", body=None, timeout=45, tries=4):
    last = None
    for i in range(tries):
        cmd = ["gh", "api", path, "-X", method]
        if body is not None:
            # gh reads the request body from stdin ONLY when told to. Without
            # --input - the JSON on stdin is discarded and the API rejects the
            # request as malformed (HTTP 422 "links/0/schema, nil is not an object").
            cmd += ["--input", "-"]
        try:
            p = subprocess.run(cmd, input=body, capture_output=True, text=True,
                               timeout=timeout)
            if p.returncode == 0:
                try:
                    return json.loads(p.stdout) if p.stdout.strip() else {}
                except json.JSONDecodeError:
                    return {}
            err = p.stderr or ""
            if any(c in err for c in ("502", "503", "504", "TLS handshake timeout",
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
    targets = {k: v for k, v in ev.items() if v["derived_topics"]}
    print(f"{'DRY RUN' if dry else 'APPLYING'} topics to {len(targets)} repos\n")

    ok = err = 0
    failures = []
    for full, v in targets.items():
        names = v["derived_topics"]
        if dry:
            print(f"  would  {v['name']:32s} {','.join(names)}")
            continue
        body = json.dumps({"names": names})
        r = gh_json(f"repos/{full}/topics", "PUT", body)
        if "__error__" in r:
            print(f"  ERROR  {v['name']:32s} {r['__error__'][:100]}")
            failures.append(v["name"])
            err += 1
            continue
        # Verify independently. A 200 is not proof the write landed.
        chk = gh_json(f"repos/{full}/topics")
        got = sorted(chk.get("names", []))
        if got == sorted(names):
            print(f"  ok     {v['name']:32s} {len(got)} topics")
            ok += 1
        else:
            print(f"  MISMATCH {v['name']:26s} sent={names} got={got}")
            failures.append(v["name"])
            err += 1
    print(f"\nverified ok={ok} errors={err}")
    if failures:
        print("failed:", ", ".join(failures))
    if err:
        sys.exit(1)


if __name__ == "__main__":
    main()
