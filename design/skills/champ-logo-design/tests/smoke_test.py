#!/usr/bin/env python3
"""Smoke-test every script in the skill the way an agent runs them (used by CI on Windows, macOS and Linux).

  python3 tests/smoke_test.py          # all checks; PNG checks run when a renderer is available

Each script runs in a subprocess with the platform's default console encoding (cp1252 on Windows), so
crashes such as UnicodeEncodeError on report symbols are caught. Standard library only.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # champ-logo-design/
SCRIPTS = os.path.join(SKILL, "scripts")
LIB = os.path.join(SKILL, "assets", "library", "svg")

SYMBOL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>Test symbol</title>
<circle cx="128" cy="128" r="96" fill="#0F7C80"/>
<path d="M80 150 L176 146 L176 170 L80 174 Z" fill="#FFFFFF"/></svg>
"""
LOCKUP = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 256"><title>Test lockup</title>
<circle cx="128" cy="128" r="96" fill="#0F7C80"/>
<rect x="280" y="100" width="560" height="56" rx="8" fill="#161616"/></svg>
"""

failures = []


def run(name, args, expect=(), cwd=None):
    """Run a script; fail on non-zero exit, a traceback, or missing expected text/files."""
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    p = subprocess.run([sys.executable] + args, cwd=cwd or SKILL, env=env, capture_output=True)
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    problems = []
    if p.returncode != 0:
        problems.append(f"exit code {p.returncode}")
    if "Traceback (most recent call last)" in out:
        problems.append("traceback")
    for e in expect:
        if os.path.isabs(e):
            if not os.path.exists(e):
                problems.append(f"missing file {e}")
        elif e not in out:
            problems.append(f"output lacks {e!r}")
    status = "ok  " if not problems else "FAIL"
    print(f"[{status}] {name}")
    if problems:
        failures.append(name)
        print("       " + "; ".join(problems))
        print("       " + out.strip().replace("\n", "\n       ")[-2500:])
    return out


def main():
    tmp = tempfile.mkdtemp(prefix="logo-smoke-")
    try:
        sym, lock = os.path.join(tmp, "a-symbol.svg"), os.path.join(tmp, "a-lockup.svg")
        for path, body in ((sym, SYMBOL), (lock, LOCKUP)):
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
        lib = sorted(f for f in os.listdir(LIB) if f.endswith(".svg"))[:3]
        S = lambda f: os.path.join(SCRIPTS, f)

        # manifest / frontmatter sanity
        text = open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8").read()
        m = re.match(r"---\nname: (.+)\ndescription: (.+?)\n", text)
        ok = bool(m) and m.group(1).strip() == "champ-logo-design" and len(m.group(2)) <= 1024
        print(f"[{'ok  ' if ok else 'FAIL'}] SKILL.md frontmatter")
        if not ok:
            failures.append("frontmatter")
        # house rule: no em or en dashes anywhere in the skill's text files
        dashed = [os.path.relpath(os.path.join(d, f), SKILL) for d, _, fs in os.walk(SKILL) for f in fs
                  if f.endswith((".md", ".py", ".json", ".html")) and
                  any(c in open(os.path.join(d, f), encoding="utf-8", errors="ignore").read() for c in "\u2013\u2014")]
        print(f"[{'ok  ' if not dashed else 'FAIL'}] no em or en dashes in skill text")
        if dashed:
            failures.append("dashes: " + ", ".join(dashed))
        refs = re.findall(r"`(references/[\w.-]+\.md)`", text)
        missing = [r for r in refs if not os.path.exists(os.path.join(SKILL, r))]
        print(f"[{'ok  ' if not missing else 'FAIL'}] every reference SKILL.md names exists ({len(set(refs))})")
        if missing:
            failures.append("missing refs: " + ", ".join(missing))

        run("build_catalog --check", [S("build_catalog.py"), "--check"], ["0 missing"])
        run("svg_audit (fixtures + library)", [S("svg_audit.py"), sym, lock] + [os.path.join(LIB, f) for f in lib],
            ["production-readiness score"])
        run("svg_audit --json", [S("svg_audit.py"), "--json", sym])
        run("search_library near-miss filter", [S("search_library.py"), "--industry", "finance", "--limit", "3"],
            ["using 'finance-banking'"])
        run("search_library house sector map", [S("search_library.py"), "--industry", "telecom", "--limit", "1"],
            ["using nearest 'social-communication'"])
        run("search_library --summary", [S("search_library.py"), "--technique", "negative-space", "--summary"],
            ["logos match"])
        out = run("search_library --format json", [S("search_library.py"), "--type", "letterform", "--format", "json",
                                                    "--limit", "2"])
        try:
            json.loads(out[out.index("["):])
        except ValueError:
            failures.append("search_library json output")
            print("[FAIL] search_library json output is not valid JSON")
        run("search_library --list-values", [S("search_library.py"), "--list-values"], ["mark_type:"])
        run("concept_sheet", [S("concept_sheet.py"), sym, sym, "--lockups", lock, lock, "--names", "A", "B",
                              "--notes", "One.", "Two.", "--recommend", "1", "-o", os.path.join(tmp, "concepts.png")],
            [os.path.join(tmp, "concepts.svg")])
        run("preview_sheet", [S("preview_sheet.py"), sym, lock, "--refs-industry", "finance-banking",
                              "-o", os.path.join(tmp, "preview.html")], [os.path.join(tmp, "preview.html")])
        run("presentation_board --list-mockups", [S("presentation_board.py"), "--list-mockups"], ["payment-card"])
        spec = {"brand": "Smoke & Café", "tagline": "Test", "brief": "A test brief.", "adjectives": ["calm"],
                "industry": "finance", "brand_color": "#0F7C80", "final": True, "greyscale": False,
                "concepts": [{"name": "Test", "symbol": sym, "lockup": lock, "idea": "An idea.",
                              "rationale": ["One", "Two"]}]}
        spec_path = os.path.join(tmp, "spec.json")
        with open(spec_path, "w", encoding="utf-8") as fh:
            json.dump(spec, fh)
        run("presentation_board", [S("presentation_board.py"), spec_path, "-o", os.path.join(tmp, "board.html")],
            [os.path.join(tmp, "board.html")])
        board = open(os.path.join(tmp, "board.html"), encoding="utf-8").read()
        ok = "@smokecafe" in board and "alex@smokecafe.com" in board
        print(f"[{'ok  ' if ok else 'FAIL'}] presentation_board handles strip punctuation and accents")
        if not ok:
            failures.append("presentation_board handles")
        run("export_variants (SVG)", [S("export_variants.py"), sym, "--out-dir", os.path.join(tmp, "export"),
                                      "--mono", "#0F7C80", "--icon-bg", "#0F7C80"])
        which = run("render_png --which", [S("render_png.py"), "--which"])
        if "available backends: none" not in which and "available backends:" in which:
            png = os.path.join(tmp, "a.png")
            run("render_png (PNG)", [S("render_png.py"), sym, "-o", png, "--size", "64"], [png])
            # batch renders at two sizes must not overwrite each other
            rd = os.path.join(tmp, "r")
            run("render_png batch 16", [S("render_png.py"), sym, "--out-dir", rd, "--size", "16"])
            run("render_png batch 64", [S("render_png.py"), sym, "--out-dir", rd, "--size", "64"],
                [os.path.join(rd, "a-symbol-16.png"), os.path.join(rd, "a-symbol-64.png")])
            try:
                import PIL  # noqa: F401
                has_pil = True
            except Exception:
                has_pil = False
            if has_pil:
                off = os.path.join(tmp, "off.svg")
                with open(off, "w", encoding="utf-8") as fh:
                    fh.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">'
                             '<g transform="translate(-60 0)"><circle cx="128" cy="128" r="60"/></g></svg>')
                run("pixel_check centred symbol", [S("pixel_check.py"), sym, "--sizes", "16"], ["-- 16 px", "#"])
                run("pixel_check sees transforms", [S("pixel_check.py"), off, "--sizes", "16"], ["WARN off-centre"])
            else:
                print("[skip] pixel_check (no Pillow)")
            run("export_variants --web-icons", [S("export_variants.py"), sym, "--out-dir", os.path.join(tmp, "web"),
                                               "--icon-bg", "#0F7C80", "--web-icons"],
                [os.path.join(tmp, "web", "favicon.ico")])
        else:
            print("[skip] PNG checks (no renderer on this machine)")
        try:
            import fontTools  # noqa: F401
            font = next((f for f in ("/System/Library/Fonts/Supplemental/Arial.ttf",
                                     "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                                     "C:/Windows/Fonts/arial.ttf") if os.path.exists(f)), None)
        except Exception:
            font = None
        if font:
            wm = os.path.join(tmp, "wm.svg")
            run("outline_text", [S("outline_text.py"), font, "Champ", "-o", wm], [wm, "no <text>"])
            run("outline_text passes audit", [S("svg_audit.py"), wm], ["production-readiness score"])
            ok = "<text" not in open(wm, encoding="utf-8").read()
            print(f"[{'ok  ' if ok else 'FAIL'}] outline_text output has no <text>")
            if not ok:
                failures.append("outline_text live text")
        else:
            print("[skip] outline_text (no fontTools or no system font)")

        caches = [d for d, _, _ in os.walk(SKILL) if os.path.basename(d) == "__pycache__"]
        print(f"[{'ok  ' if not caches else 'FAIL'}] no __pycache__ written into the skill folder")
        if caches:
            failures.append("__pycache__ in skill folder: " + ", ".join(caches))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed: {', '.join(failures)}")
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    main()
