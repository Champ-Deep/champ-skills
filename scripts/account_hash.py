#!/usr/bin/env python3
"""Cloud side of the daily sync. Hash every skill in the Claude account's synced skills
folder and write account.json for scripts/account_sync.py on the Mac.

  python3 account_hash.py [skills_dir] [out_file]
Defaults: skills_dir = first /root/.claude/skills/synced/*/ ; out_file = ./account.json
Skills shipped by Anthropic under an all-rights-reserved licence (docx, pdf, pptx, xlsx and
similar) are marked excluded: this repo is public and they are not ours to republish.
"""
import glob
import hashlib
import json
import os
import sys

src = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else (glob.glob("/root/.claude/skills/synced/*/") or [""])[0]
out = sys.argv[2] if len(sys.argv) > 2 else "account.json"
if not src or not os.path.isdir(src):
    print("skills directory not located", file=sys.stderr)
    sys.exit(2)

skills = {}
for name in sorted(os.listdir(src)):
    d = os.path.join(src, name)
    if not os.path.isfile(os.path.join(d, "SKILL.md")):
        continue
    files = {}
    for r, ds, fs in os.walk(d):
        ds[:] = [x for x in ds if not x.startswith(".") and x != "__pycache__"]
        for f in fs:
            if f.startswith(".") or f.endswith(".pyc"):
                continue
            p = os.path.join(r, f)
            files[os.path.relpath(p, d)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    entry = {"files": files}
    lic = os.path.join(d, "LICENSE.txt")
    if os.path.isfile(lic) and "Anthropic, PBC. All rights reserved" in open(lic, errors="ignore").read(400):
        entry["excluded"] = "Anthropic proprietary licence, not republished to a public repo"
    skills[name] = entry

json.dump({"source": src, "skills": skills}, open(out, "w"), indent=1)
print(f"{len(skills)} account skills hashed -> {out}")
