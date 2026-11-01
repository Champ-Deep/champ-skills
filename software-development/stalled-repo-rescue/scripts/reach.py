#!/usr/bin/env python3
"""Reachability analysis from a real entrypoint.

Resolves relative imports transitively, separating bare (third-party) from
relative imports, and reports: reachable files, the dead set, and bare imports
reachable from browser code (those are Node-only packages a browser bundle
cannot resolve).

Usage:
    scripts/reach.py <repo> <entrypoint-relative-to-repo>

Example:
    scripts/reach.py ~/repos/myapp src/index.ts

Read-only. Prints a report; deletes nothing. See references/reachability-probe.md
for what to do with the dead set before deleting any of it.
"""
import re
import sys
from pathlib import Path

IMPORT_RE = re.compile(
    r"""(?:from\s+|import\s*\(|require\s*\()\s*['"]([^'"]+)['"]"""
)
EXTS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py")


def resolve(spec: str, importer: Path, root: Path):
    """Resolve a module specifier to a file, or None."""
    if spec.startswith("."):
        base = (importifier_dir(importer) / spec).resolve() if False else (importer.parent / spec).resolve()
        for cand in (base, *(base.with_suffix(e) for e in EXTS),
                     *(Path(str(base) + "/index" + e) for e in EXTS)):
            if cand.is_file():
                return cand
        return None
    return None  # bare import: not resolved to a file, tracked separately


def importifier_dir(p: Path) -> Path:  # pragma: no cover - kept for clarity
    return p.parent


def walk(root: Path, entry: Path):
    seen, queue, bare = set(), [entry], set()
    while queue:
        cur = queue.pop()
        if cur in seen or not cur.is_file():
            continue
        seen.add(cur)
        try:
            text = cur.read_text(errors="ignore")
        except OSError:
            continue
        for spec in IMPORT_RE.findall(text):
            if spec.startswith("."):
                tgt = resolve(spec, cur, root)
                if tgt and tgt not in seen:
                    queue.append(tgt)
            else:
                bare.add(spec.split("/")[0])
    return seen, bare


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    root = Path(sys.argv[1]).resolve()
    entry = (root / sys.argv[2]).resolve()
    if not entry.is_file():
        print(f"entrypoint not found: {entry}")
        return 2

    reachable, bare = walk(root, entry)
    all_files = {
        p for p in root.rglob("*")
        if p.suffix in EXTS
        and "node_modules" not in p.parts
        and ".git" not in p.parts
        and "dist" not in p.parts
        and "build" not in p.parts
    }
    dead = sorted(all_files - reachable)

    print(f"reachable: {len(reachable)}  dead: {len(dead)}  total: {len(all_files)}")
    print(f"bare imports reachable from entrypoint: {len(bare)}")
    print("\n-- dead set (entrypoint does not import) --")
    for p in dead:
        print(f"  {p.relative_to(root)}")

    # Node-only bare imports reachable from browser code are a packaging signal:
    # the file is browser code that would fail to bundle if it were reachable.
    node_only = sorted(b for b in bare if b in {"fs", "path", "os", "crypto", "child_process"})
    if node_only:
        print("\n-- Node-only bare imports reachable (check runtime target) --")
        for b in node_only:
            print(f"  {b}")
    return 0


if __name__ == "__main__":
    sys.exit(main())