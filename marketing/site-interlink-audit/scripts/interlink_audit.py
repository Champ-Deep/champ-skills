#!/usr/bin/env python3
"""
interlink-audit: one command, any website, client-ready report.

    python3 interlink_audit.py <domain> [-o out.html] [--cap 6000] [--no-verify]

Runs the full pipeline and, unless --no-verify, fails loudly if the report does not
render correctly. This is the entry point a client or an agent invokes; the individual
modules stay usable on their own.
"""
import argparse, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))


def slugify(host):
    return re.sub(r"[^a-z0-9]+", "-", host.lower().replace("www.", ""))



def run(cmd, label):
    t0 = time.time()
    p = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    if p.returncode != 0:
        print(f"[{label}] FAILED ({p.returncode})", file=sys.stderr)
        print(p.stdout[-3000:], file=sys.stderr)
        print(p.stderr[-3000:], file=sys.stderr)
        sys.exit(p.returncode)
    print(p.stdout.rstrip())
    print(f"[{label}] {time.time()-t0:.1f}s\n")
    return p.stdout


def main():
    ap = argparse.ArgumentParser(description="Interlink architecture audit for any site")
    ap.add_argument("domain")
    ap.add_argument("-o", "--out", default=None, help="output HTML path")
    ap.add_argument("--cap", type=int, default=6000, help="max pages to fetch")
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--no-audit", action="store_true", help="skip the visual audit")
    args = ap.parse_args()

    host = re.sub(r"^https?://", "", args.domain.strip()).strip("/")
    stem = f"bundle-{slugify(host)}"
    bundle = f"{stem}.json"
    plan = f"{stem}-plan.json"
    out = args.out or f"/tmp/interlink-{slugify(host)}.html"

    print(f"=== interlink audit: {host} ===\n")

    # 1. crawl
    run([sys.executable, "-B", "pipeline.py", host, "--cap", str(args.cap)], "crawl")

    # 2. plan
    run([sys.executable, "-B", "plan.py", bundle], "plan")

    # 3. report
    run([sys.executable, "-B", "report.py", bundle, plan, "-o", out], "report")

    # 4. verify (mandatory)
    if not args.no_verify:
        p = subprocess.run([sys.executable, "-B", "verify_report.py", out],
                           cwd=HERE, capture_output=True, text=True)
        print(p.stdout.rstrip())
        if p.returncode != 0:
            print(p.stderr[-2000:], file=sys.stderr)
            print("\nREPORT FAILED VERIFICATION", file=sys.stderr)
            sys.exit(1)
        print()

    # 5. visual audit, when the skill is available
    if not args.no_audit:
        audit = "/Users/deep/champ-skills/design/skills/visual-verify/scripts/audit.py"
        if os.path.exists(audit):
            for w in (1440, 390):
                p = subprocess.run([sys.executable, audit, out, "--width", str(w)],
                                   capture_output=True, text=True)
                m = re.search(r"(\d+) fail\s+(\d+) warn", p.stdout)
                if m:
                    flag = "OK " if m.group(1) == "0" else "FAIL"
                    print(f"[audit {flag}] w={w}: {m.group(1)} fail, {m.group(2)} warn")
        else:
            print("[audit] visual-verify skill not found; skipped")

    # 6. headline numbers
    pl = json.load(open(os.path.join(HERE, plan)))
    s = pl["summary"]
    print("\n=== headline ===")
    for k in ("pages", "edges", "entities", "clusters", "zero_in", "zero_out",
              "no_tofu", "work_pages", "work_links"):
        print(f"  {k:14s} {s[k]}")
    bd = json.load(open(os.path.join(HERE, bundle)))
    if bd.get("stats", {}).get("truncated"):
        print(f"  WARNING crawl truncated at cap {bd['stats']['cap']} "
              f"of {bd['stats']['candidates']} candidate URLs")
    print(f"\nreport: {out}")


if __name__ == "__main__":
    main()