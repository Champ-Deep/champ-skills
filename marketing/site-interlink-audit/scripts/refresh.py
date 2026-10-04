#!/usr/bin/env python3
"""
refresh.py: keep a set of audited sites current from a drop-in list.

    # one site
    python3 refresh.py --site spanglobalservices.com

    # every site in a list file (one domain per line, # comments allowed)
    python3 refresh.py --list sites.txt

    # re-audit everything already stored, no crawl of new ones
    python3 refresh.py --all

A refresh means: crawl (or reuse a cached bundle), build the plan, render the report,
verify it, and write a JSON summary. It is safe to re-run: unchanged bundles are reused
unless --force is passed.

Exit code is non-zero if any site fails, so this is CI-usable.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import interlink_audit as IA          # noqa: E402  (shares slugify + run)

SUMMARY = os.path.join(HERE, "refresh-summary.json")
LOCK = os.path.join(HERE, ".refresh.lock")


def slugify(host):
    host = re.sub(r"^https?://", "", host.strip().strip("/")).split("/")[0]
    host = re.sub(r"^www\.", "", host)   # one site, one slug
    return re.sub(r"[^a-z0-9]+", "-", host.lower()).strip("-")


def read_list(path):
    """One domain per line. Blank lines and # comments ignored. Also accepts a JSON
    array of strings, or a newline/comma separated blob, so a team member can paste
    whatever they have without reformatting it."""
    raw = open(path, encoding="utf-8").read().strip()
    if not raw:
        return []
    items = []
    if raw.startswith("["):
        try:
            items = json.loads(raw)
        except json.JSONDecodeError:
            pass
    if not items:
        items = []
        for line in raw.replace(",", "\n").splitlines():
            line = line.split("#", 1)[0].strip()
            if line and not line.startswith("http://"):
                items.append(line)
    out = []
    for it in items:
        d = re.sub(r"^https?://", "", str(it).strip()).strip("/").split("/")[0]
        if d and d not in out:
            out.append(d)
    return out


def known_bundles():
    """slug -> bundle path. Excludes the -plan and -related sidecars: they are outputs of
    a bundle, not bundles themselves, and reading them as bundles produced domains that
    do not exist."""
    found = {}
    for f in os.listdir(HERE):
        if not f.startswith("bundle-") or not f.endswith(".json"):
            continue
        if f.endswith("-plan.json") or f.endswith("-related.json"):
            continue
        found[f[len("bundle-"):-len(".json")]] = os.path.join(HERE, f)
    return found


def refresh_one(host, cap, force, skip_verify, skip_audit):
    slug = slugify(host)
    stem = f"bundle-{slug}"
    bundle = os.path.join(HERE, f"{stem}.json")
    plan = os.path.join(HERE, f"{stem}-plan.json")
    # name artefacts by SLUG, never by the bundle stem: one site, one predictable path
    out = os.path.join(HERE, "reports", f"interlink-{slug}.html")
    wslug = slug

    os.makedirs(os.path.join(HERE, "reports"), exist_ok=True)

    t0 = time.time()
    rec = {"host": host, "stem": stem, "report": out}

    # ---- 1. crawl (or reuse) --------------------------------------------
    reuse = os.path.exists(bundle) and not force
    if reuse:
        print(f"  [{host}] reusing cached crawl ({os.path.getsize(bundle)//(1024*1024)} MB)")
        IA.run([sys.executable, "-B", "plan.py", bundle], "plan")
    else:
        print(f"  [{host}] crawling (cap {cap})...")
        r = IA.run([sys.executable, "-B", "pipeline.py", host, "--cap", str(cap)], "crawl")
        IA.run([sys.executable, "-B", "plan.py", bundle], "plan")
        rec["crawl_log"] = r.strip().splitlines()[-4:]

    # ---- 2. report -------------------------------------------------------
    IA.run([sys.executable, "report.py", bundle, plan, "-o", out], "report")

    # ---- 3. verify -------------------------------------------------------
    if not skip_verify:
        p = subprocess.run([sys.executable, "-B", "verify_report.py", out],
                           cwd=HERE, capture_output=True, text=True)
        tail = [l for l in p.stdout.strip().splitlines() if l.strip()][-1:]
        rec["verify"] = tail[0] if tail else ""
        if p.returncode != 0:
            rec["ok"] = False
            rec["error"] = "verification failed"
            rec["verify_detail"] = [l for l in p.stdout.splitlines() if l.startswith("FAIL")]
            print(f"  [{host}] VERIFY FAILED")
            rec["seconds"] = round(time.time() - t0, 1)
            return rec
        print(f"  [{host}] {rec['verify']}")

    # ---- 3b. related links + site widget --------------------------------
    IA.run([sys.executable, "-B", "semantic.py", bundle, "--no-clef"], "related")
    rec["related"] = os.path.join(HERE, f"{stem}-related.json")
    cat = os.path.join(HERE, "catalog.json")
    if os.path.exists(cat):
        wdir = os.path.join(HERE, "widget-" + wslug)
        IA.run([sys.executable, "-B", "component.py", "--bundle", bundle,
                "--catalog", cat, "-o", wdir], "widget")
        rec["widget"] = os.path.join(wdir, "related-sites.html")

    # ---- 4. visual audit -------------------------------------------------
    if not skip_audit:
        audit = "/Users/deep/champ-skills/design/skills/visual-verify/scripts/audit.py"
        if os.path.exists(audit):
            fails = []
            for w in (1440, 390):
                p = subprocess.run([sys.executable, audit, out, "--width", str(w)],
                                   capture_output=True, text=True)
                m = re.search(r"(\d+) fail", p.stdout)
                if m and int(m.group(1)):
                    fails.append(f"w={w}:{m.group(1)}")
            rec["visual"] = "0 fail" if not fails else " ".join(fails)
            print(f"  [{host}] visual: {rec['visual']}")

    # ---- 5. headline numbers --------------------------------------------
    pl = json.load(open(plan))
    ents = len(pl.get("entities", []))
    work = len(pl.get("work", []))
    links = sum(len(w.get("links", [])) for w in pl.get("work", []))
    rec.update({"ok": True, "entities": ents, "work_pages": work,
                "work_links": links, "seconds": round(time.time() - t0, 1)})
    print(f"  [{host}] {ents} entities, {links} links across {work} pages "
          f"({rec['seconds']}s)")
    return rec


def load_summary():
    if os.path.exists(SUMMARY):
        try:
            return json.load(open(SUMMARY))
        except json.JSONDecodeError:
            pass
    return {"sites": {}}


def acquire_lock():
    """Two refreshes writing the same bundles and reports interleave and corrupt both.
    Fail fast instead."""
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
    except FileExistsError:
        try:
            pid = int(open(LOCK).read().strip() or 0)
        except (OSError, ValueError):
            pid = 0
        alive = False
        if pid:
            try:
                os.kill(pid, 0)
                alive = True
            except OSError:
                alive = False
        if alive:
            sys.exit(f"refresh: another refresh is already running (pid {pid}).\n"
                     f"  Wait for it, or delete {LOCK} if you are sure it is stale.")
        os.unlink(LOCK)
        return acquire_lock()
    return True


def release_lock():
    try:
        os.unlink(LOCK)
    except OSError:
        pass


def main():
    ap = argparse.ArgumentParser(description="Refresh interlink audits from a site list")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--site", help="one domain")
    g.add_argument("--list", help="file with one domain per line, or a JSON array")
    g.add_argument("--all", action="store_true", help="refresh every stored bundle")
    ap.add_argument("--cap", type=int, default=6000)
    ap.add_argument("--force", action="store_true", help="re-crawl even if a bundle exists")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--no-audit", action="store_true")
    args = ap.parse_args()

    if args.site:
        hosts = [args.site]
    elif args.list:
        if not os.path.exists(args.list):
            sys.exit(f"refresh: no such list file: {args.list}")
        hosts = read_list(args.list)
        if not hosts:
            sys.exit(f"refresh: {args.list} contained no usable domains")
    else:
        # Read the host each bundle actually recorded. Reconstructing it from the
        # filename by swapping dashes for dots invents domains that do not exist.
        hosts = []
        for stem in sorted(known_bundles()):
            try:
                b = json.load(open(os.path.join(HERE, f"bundle-{stem}.json")))
            except (OSError, json.JSONDecodeError):
                continue
            h = (b.get("host") or b.get("base") or "").strip()
            if h:
                hosts.append(h)

    if not hosts:
        sys.exit("refresh: nothing to do. Pass --site, --list, or store a bundle first.")

    acquire_lock()
    try:
        _run(args, hosts)
    finally:
        release_lock()


def _run(args, hosts):

    print(f"=== refresh {len(hosts)} site(s) at "
          f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} ===\n")

    summary = load_summary()
    results = []
    for h in hosts:
        print(f"[{h}]")
        try:
            rec = refresh_one(h, args.cap, args.force, args.no_verify, args.no_audit)
        except SystemExit as e:
            print(f"  [{h}] ERROR: {e}")
            rec = {"host": h, "ok": False, "error": str(e)}
        except Exception as e:                       # noqa: BLE001
            print(f"  [{h}] ERROR: {type(e).__name__}: {e}")
            rec = {"host": h, "ok": False, "error": f"{type(e).__name__}: {e}"}
        rec["checked"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        summary["sites"][h] = rec
        results.append(rec)
        print()

    ok = [r for r in results if r.get("ok")]
    bad = [r for r in results if not r.get("ok")]
    summary["last_run"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    summary["totals"] = {"total": len(results), "ok": len(ok), "failed": len(bad)}
    with open(SUMMARY, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("=" * 68)
    print(f"{len(ok)}/{len(results)} sites ok")
    for r in results:
        mark = "ok  " if r.get("ok") else "FAIL"
        bits = []
        if r.get("entities") is not None:
            bits.append(f"{r['entities']} entities")
            bits.append(f"{r.get('work_links', 0)} links")
        if r.get("visual"):
            bits.append(f"visual {r['visual']}")
        if r.get("error"):
            bits.append(r["error"][:60])
        print(f"  [{mark}] {r['host']:34s} {'  '.join(bits)}")
    print(f"\nsummary -> {SUMMARY}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()