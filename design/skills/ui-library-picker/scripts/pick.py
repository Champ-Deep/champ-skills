#!/usr/bin/env python3
"""ui-library-picker: task in, library out.

  pick.py "toast notifications"        one pick, why, install line, flags
  pick.py "drag to reorder" --all      every match, ranked
  pick.py --check path/to/package.json what is installed, what is hand-built or a competitor
  pick.py --list [layer]               the whole registry, optionally one layer
  pick.py --refresh                    re-read npm latest, licence and last publish for every npm package
  pick.py --selftest

Data lives in registry.json next to this file. Picks come from three sources, named per row:
Emil Kowalski's pick-ui-library list (MIT), Griffin Wooldridge's three-layer model (video, 7 Nov 2026),
and what Champ projects already use. Everything else is marked as ours.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = HERE.parent / "registry.json"

LAYER_ORDER = {"specialist": 0, "foundation": 1, "design": 2, "motion-data": 3, "plumbing": 4}


def load() -> dict:
    return json.loads(REG.read_text())


def tokens(text: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9+]+", text.lower()) if t]


def score(entry: dict, q: list[str], phrase: str) -> int:
    s = 0
    for kw in entry["tasks"]:
        k = kw.lower()
        if k in phrase:  # whole keyword or phrase found in the query
            s += 3 + len(k.split())
        elif any(t == k or (len(t) > 3 and (t in k or k in t)) for t in q):
            s += 1
    return s


def pick(query: str, reg: dict | None = None) -> list[dict]:
    reg = reg or load()
    q = tokens(query)
    phrase = " ".join(q)
    ranked = []
    for e in reg["libraries"]:
        sc = score(e, q, phrase)
        if sc > 0:
            ranked.append((sc, -LAYER_ORDER.get(e["layer"], 9), e))
    ranked.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [e for _, _, e in ranked]


def show(e: dict, full: bool = True) -> str:
    out = [f"{e['name']}  [{e['layer']}]", f"  for: {e['why']}"]
    if e.get("install"):
        out.append(f"  install: {e['install']}")
    meta = []
    if e.get("npm_latest"):
        meta.append(f"npm {e['npm_latest']} (published {e['npm_modified'][:10]})")
    if e.get("license"):
        meta.append(f"licence {e['license']}")
    meta.append("single-file HTML ok" if e.get("single_file_html") else "needs a React or bundler build")
    out.append("  " + "; ".join(meta))
    for f in e.get("flags", []):
        out.append(f"  FLAG: {f}")
    if full and e.get("avoid"):
        out.append(f"  avoid when: {e['avoid']}")
    out.append(f"  source: {e['source']}")
    return "\n".join(out)


def cmd_pick(query: str, show_all: bool) -> int:
    hits = pick(query)
    if not hits:
        print(f'Not covered by the list: "{query}".')
        print("Next: 21st.dev search with this query (marketplace, any author), then shadcn/ui, else say you left the list and why.")
        return 2
    chosen = hits if show_all else hits[:1]
    for e in chosen:
        print(show(e))
        print()
    if not show_all and len(hits) > 1:
        print("also matched: " + ", ".join(h["name"] for h in hits[1:4]) + "  (use --all)")
    return 0


def cmd_check(path: str) -> int:
    reg = load()
    pkg = json.loads(Path(path).read_text())
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    have = [e for e in reg["libraries"] if e.get("npm") and e["npm"] in deps]
    print(f"{len(deps)} dependencies; {len(have)} are on the picker list:")
    for e in have:
        flags = f"  FLAG: {e['flags'][0]}" if e.get("flags") else ""
        print(f"  ok  {e['name']} ({e['npm']} {deps[e['npm']]}){flags}")
    rep = 0
    for e in reg["libraries"]:
        for rival in e.get("replaces", []):
            if rival in deps:
                rep += 1
                print(f"  rival  {rival} is installed; list pick for that task is {e['name']}. Flag it, do not churn the dependency unasked")
    stack = [d for d in ("tailwindcss", "react", "next", "vite") if d in deps]
    print("stack seen: " + (", ".join(stack) or "none of react, next, vite, tailwind"))
    if "tailwindcss" in deps and "tailwind-merge" not in deps:
        print("  note: tailwindcss without tailwind-merge; shadcn components expect a cn() helper (clsx + tailwind-merge)")
    return 0


def cmd_list(layer: str | None) -> int:
    reg = load()
    for e in reg["libraries"]:
        if layer and e["layer"] != layer:
            continue
        print(f"{e['layer']:<11} {e['name']:<24} {e.get('npm_latest') or '-':<12} {e.get('license') or '-'}")
    return 0


def cmd_refresh() -> int:
    reg = load()
    changed = 0
    for e in reg["libraries"]:
        name = e.get("npm")
        if not name:
            continue
        u = "https://registry.npmjs.org/" + urllib.parse.quote(name, safe="@")
        try:
            meta = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"Accept": "application/vnd.npm.install-v1+json"}), timeout=20).read())
            latest = meta["dist-tags"]["latest"]
            full = json.loads(urllib.request.urlopen(u + "/latest", timeout=20).read())
        except Exception as ex:  # keep old data, say so
            print(f"  skip {name}: {str(ex)[:70]}")
            continue
        new = (latest, full.get("license"), meta.get("modified"))
        old = (e.get("npm_latest"), e.get("license"), e.get("npm_modified"))
        if new != old:
            changed += 1
            print(f"  {name}: {old[0]} -> {new[0]}")
        e["npm_latest"], e["license"], e["npm_modified"] = new
    reg["verified"] = dt.date.today().isoformat()
    REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False) + "\n")
    print(f"refreshed, {changed} changed, verified {reg['verified']}")
    return 0


def selftest() -> int:
    reg = load()
    names = {e["id"] for e in reg["libraries"]}
    assert len(names) == len(reg["libraries"]), "duplicate ids"
    for e in reg["libraries"]:
        for k in ("id", "name", "layer", "tasks", "why", "source"):
            assert e.get(k), f"{e.get('id')} missing {k}"
        assert e["layer"] in LAYER_ORDER, e["layer"]
    cases = {
        "toast notifications": "sonner",
        "bottom sheet drawer on mobile": "vaul",
        "command palette": "cmdk",
        "animate a price counter": "number-flow",
        "one time password input": "input-otp",
        "drag and drop sortable list": "dnd-kit",
        "very long list of 5000 rows": "virtuoso",
        "dialog modal popover accessible": "base-ui",
        "buttons inputs tabs": "shadcn",
        "streaming text agent approval card": "beautiful-ui",
        "landing page aurora background": "aceternity",
        "marquee globe animated component": "magic-ui",
        "need something specific from many authors": "21st-dev",
        "line chart dashboard": "recharts",
        "spring layout animation": "motion",
        "dark mode theme switch": "next-themes",
    }
    bad = []
    for q, want in cases.items():
        got = pick(q, reg)
        top = got[0]["id"] if got else None
        if top != want:
            bad.append((q, want, top))
    assert not bad, f"picker misses: {bad}"
    assert pick("quantum flux capacitor", reg) == [], "nonsense query must be 'not covered'"
    print(f"selftest PASS: {len(reg['libraries'])} libraries, {len(cases)} routing cases, 1 not-covered case")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--check")
    ap.add_argument("--list", nargs="?", const="")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if a.refresh:
        sys.exit(cmd_refresh())
    if a.check:
        sys.exit(cmd_check(a.check))
    if a.list is not None:
        sys.exit(cmd_list(a.list or None))
    if a.query:
        sys.exit(cmd_pick(a.query, a.all))
    ap.print_help()
