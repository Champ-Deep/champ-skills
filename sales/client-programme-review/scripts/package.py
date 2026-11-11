#!/usr/bin/env python3
"""Package this skill as a zip for a Claude account (Settings, Capabilities, Skills, upload).

  python3 scripts/package.py [out_dir]     writes <out_dir>/client-programme-review.zip

Claude accounts validate frontmatter strictly (name, description, license, metadata only) and use the description
to decide when to load the skill, so the zip carries a fuller description than the one-line trigger this repo keeps.
"""
import pathlib
import re
import sys
import zipfile

SKILL = pathlib.Path(__file__).resolve().parent.parent
NAME = SKILL.name
DESCRIPTION = (
    "Builds a client programme review, renewal showcase, or weekly or monthly client report as one interactive HTML page, "
    "after reconciling every client-facing figure with the account owner. Use when an account owner asks for a programme review, "
    "a renewal or upsell showcase, a client report or 'the showcase page' for a live client, or shares lead sheets, send reports "
    "and call reports ahead of a client meeting. Produces a reconciliation ledger (nothing ships while a figure is unconfirmed), "
    "the page (universe, messaging, lead board with win profile, lessons, asks, tiers) and an internal call script."
)
SKIP = ("__pycache__", ".DS_Store", "/dist/", "/kit/cases/", "/kit/shots/", "/kit/export/", ".gitignore")

if __name__ == "__main__":
    md = (SKILL / "SKILL.md").read_text()
    m = re.match(r"---\n([\s\S]*?)\n---\n", md)
    assert m and f"name: {NAME}" in m.group(1), "SKILL.md frontmatter not found"
    version = re.search(r"^version: (\S+)", m.group(1), re.M).group(1)
    assert len(DESCRIPTION) <= 1024 and "<" not in DESCRIPTION
    front = f'---\nname: {NAME}\ndescription: "{DESCRIPTION}"\nlicense: MIT\nmetadata:\n  version: "{version}"\n  author: Champ\n---\n'
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve() / f"{NAME}.zip"
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{NAME}/SKILL.md", front + md[m.end():])
        for f in sorted(SKILL.rglob("*")):
            rel = "/" + f.relative_to(SKILL).as_posix()
            if f.is_file() and f.name != "SKILL.md" and not any(s in rel for s in SKIP):
                z.write(f, f"{NAME}{rel}"); n += 1
    print(out, f"{out.stat().st_size // 1024} KB, {n + 1} files, version {version}")
