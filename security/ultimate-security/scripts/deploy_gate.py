#!/usr/bin/env python3
"""Deploy security gate for Deep's repos (ultimate-security Level 1 + Cloudflare security-audit trigger).

  check <dir> [--name N]   gitleaks + trivy (HIGH/CRITICAL, fixable) + sensitive-surface audit check
  pre-push                 git pre-push hook entry: gates pushes to deploy branches
  baseline <dir>           accept the current sensitive surface without an audit (first install only)
  stamp <dir> --run R      record a completed Cloudflare full-audit run as covering its source_ref
  install <dir>            wire pre-push hook, npm predeploy, scripts/publish.sh, then baseline
  coverage [--fix] <root>... list deploy repos and whether each is wired; --fix installs the missing ones

Exit: 0 pass, 1 secret or vuln, 3 audit required, 2 usage or tool failure (fails closed).
Override (Deep's approval only): DEPLOY_GATE_OVERRIDE="<reason>" passes and is logged.
Warn-only repos (legacy backlog under triage): names listed in <state>/gate-config.json "warn_only"
run every check and log it, but do not block. Remove a name to enforce.
Never prints secret values: gitleaks runs with --redact and only rule, file, line are shown.
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile, time

GATE = os.path.abspath(__file__)
STATE = os.environ.get("DEPLOY_GATE_STATE") or os.path.expanduser("~/security-audit-skill")
LOG = os.environ.get("DEPLOY_GATE_LOG") or os.path.expanduser("~/.hermes/logs/deploy-gate.log")
DEPLOY_BRANCHES = re.compile(r"^refs/heads/(main|master|production|prod|release)$")
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", ".wrangler", ".venv", "venv", "__pycache__", ".turbo", "coverage"}
# Paths whose change means the Cloudflare skill must run a full audit before deploy.
SENSITIVE = re.compile(
    r"(auth|login|logout|signin|signup|session|token|oauth|jwt|passw|credential|secret|billing|payment|checkout|"
    r"stripe|razorpay|invoice|subscription|webhook|admin|tenant|rbac|permission|acl|middleware|crypto|cookie|csrf|cors|"
    r"\.github/workflows/|dockerfile|migrations?/|schema\.(sql|prisma))", re.I)
NON_CODE = re.compile(r"\.(md|mdx|txt|png|jpe?g|gif|svg|webp|ico|css|scss|woff2?|ttf|pdf|lock|map|snap|mp3|mp4|wav)$", re.I)
HOOK = """#!/bin/sh
# deploy-gate (champ-skills security/ultimate-security). Gates pushes to deploy branches.
G="$HOME/champ-skills/security/ultimate-security/scripts/deploy_gate.py"
[ -f "$G" ] || { echo "deploy-gate: $G missing, push refused" >&2; exit 1; }
exec python3 "$G" pre-push "$@"
"""
PUBLISH_MARK = "# deploy-gate (champ-skills security/ultimate-security)"
PUBLISH_SNIPPET = PUBLISH_MARK + """: secrets, HIGH/CRITICAL deps, audit-required changes.
# Not skipped by PUBLISH_SKIP_GATES. Override only with Deep's approval: DEPLOY_GATE_OVERRIDE="<reason>".
python3 "$HOME/champ-skills/security/ultimate-security/scripts/deploy_gate.py" check . --name "$REPO_NAME" \\
  || { echo "PUBLISH-FAILED: security gate refused." >&2; exit 8; }
"""
PREDEPLOY = 'python3 "$HOME/champ-skills/security/ultimate-security/scripts/deploy_gate.py" check .'


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def log(name, verdict, detail=""):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S%z')}\t{name}\t{verdict}\t{detail}\n")


def is_git(d):
    # only a repo rooted at d counts; a plain folder nested inside another repo (e.g. ~) is not one
    top = run(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
    return bool(top) and os.path.realpath(top) == os.path.realpath(d)


def repo_name(d, name=None):
    if name or os.environ.get("DEPLOY_GATE_REPO"):
        return name or os.environ["DEPLOY_GATE_REPO"]
    url = run(["git", "-C", d, "remote", "get-url", "origin"]).stdout.strip()
    base = url.rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1] if url else os.path.basename(os.path.abspath(d))
    return base[:-4] if base.endswith(".git") else base


def list_files(d):
    if is_git(d):
        out = run(["git", "-C", d, "ls-files", "-co", "--exclude-standard", "-z"]).stdout
    else:
        # throwaway git dir so the folder's own .gitignore applies, matching what publish.sh's clone commits
        with tempfile.TemporaryDirectory() as g:
            run(["git", "init", "-q", "--bare", g])
            out = run(["git", f"--git-dir={g}", f"--work-tree={d}", "ls-files", "-o", "--exclude-standard", "-z"], cwd=d).stdout
    return sorted(p for p in out.split("\0") if p and os.path.isfile(os.path.join(d, p))
                  and not set(p.split("/")[:-1]) & SKIP_DIRS)


def is_sensitive(p):
    return bool(SENSITIVE.search(p)) and not NON_CODE.search(p)


def surface(d):
    """{path: sha256} for every sensitive file, plus one fingerprint over the set."""
    files = {}
    for p in list_files(d):
        if is_sensitive(p):
            with open(os.path.join(d, p), "rb") as f:
                files[p] = hashlib.sha256(f.read()).hexdigest()
    fp = hashlib.sha256("\n".join(f"{p}\0{h}" for p, h in sorted(files.items())).encode()).hexdigest()
    return fp, files


def stamps_path(name):
    return os.path.join(STATE, name, "gate-stamps.json")


def load_stamps(name):
    try:
        with open(stamps_path(name)) as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def add_stamp(name, rec):
    s = load_stamps(name) + [rec]
    os.makedirs(os.path.dirname(stamps_path(name)), exist_ok=True)
    with open(stamps_path(name), "w") as f:
        json.dump(s, f, indent=1)


def warn_only():
    try:
        with open(os.path.join(STATE, "gate-config.json")) as f:
            return set(json.load(f).get("warn_only", []))
    except FileNotFoundError:
        return set()


def scan_secrets(d, log_opts=None):
    exe = shutil.which("gitleaks")
    if not exe:
        return None, ["gitleaks not installed (brew install gitleaks)"]
    fd, rep = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    git_src = log_opts is not None or is_git(d)
    cmd = [exe, "git" if git_src else "dir", "--redact", "--no-banner", "--exit-code", "1", "-f", "json", "-r", rep]
    if log_opts:
        cmd.append(f"--log-opts={log_opts}")
    r = run(cmd + ["."], cwd=d)  # cwd so .gitleaksignore and .gitleaks.toml in the repo apply
    if r.returncode not in (0, 1) or not os.path.getsize(rep):
        os.unlink(rep)
        return None, [f"gitleaks failed: {r.stderr.strip()[-300:]}"]
    with open(rep) as f:
        found = json.load(f) or []
    os.unlink(rep)
    return len(found), [f"secret {x.get('RuleID')} {x.get('File')}:{x.get('StartLine')} commit {str(x.get('Commit', ''))[:8]}" for x in found]


def scan_trivy(d):
    exe = shutil.which("trivy")
    if not exe:
        return None, ["trivy not installed (brew install trivy)"]
    skip = ",".join(f"**/{x}" for x in SKIP_DIRS)
    r = run([exe, "fs", "--quiet", "--format", "json", "--scanners", "vuln,secret", "--severity", "HIGH,CRITICAL",
             "--ignore-unfixed", "--skip-dirs", skip, "."], cwd=d)
    if r.returncode != 0:
        return None, [f"trivy failed: {r.stderr.strip()[-300:]}"]
    out = []
    for res in json.loads(r.stdout or "{}").get("Results") or []:
        for v in res.get("Vulnerabilities") or []:
            out.append(f"vuln {v['Severity']} {v.get('VulnerabilityID')} {v.get('PkgName')} {v.get('InstalledVersion')} -> {v.get('FixedVersion')} ({res.get('Target')})")
        for s in res.get("Secrets") or []:
            out.append(f"secret {s['Severity']} {s.get('RuleID')} {res.get('Target')}:{s.get('StartLine')}")
    return len(out), out


def check(d, name=None, log_opts=None, secrets=None):
    d = os.path.abspath(d)
    name = repo_name(d, name)
    problems, error, block, audit = [], False, False, False
    for n, lines in (secrets or scan_secrets(d, log_opts), scan_trivy(d)):
        error |= n is None
        block |= bool(n)
        problems += lines
    fp, files = surface(d)
    stamps = load_stamps(name)
    if files and not any(s["fingerprint"] == fp for s in stamps):
        audit = True
        prev = stamps[-1]["files"] if stamps else {}
        changed = sorted(p for p in set(files) | set(prev) if files.get(p) != prev.get(p))
        problems.append(f"AUDIT-REQUIRED: {len(changed)} sensitive file(s) changed since the last audited state: "
                        + ", ".join(changed[:12]) + (" ..." if len(changed) > 12 else ""))
        problems.append(f"  Run the Cloudflare security-audit skill in full audit mode on {name}, then: "
                        f"deploy_gate.py stamp <repo> --run ~/security-audit-skill/{name}/run-N")
    verdict = 2 if error else 1 if block else 3 if audit else 0
    label = {0: "PASS", 1: "BLOCK", 2: "ERROR", 3: "AUDIT-REQUIRED"}[verdict]
    for p in problems:
        print(f"deploy-gate {name}: {p}", file=sys.stderr)
    override = os.environ.get("DEPLOY_GATE_OVERRIDE", "").strip()
    if verdict and name in warn_only():
        log(name, f"WARN({label})", "; ".join(problems)[:500])
        print(f"deploy-gate {name}: {label}, WARN-ONLY (in gate-config.json warn_only), not blocking", file=sys.stderr)
        return 0
    if verdict and override:
        log(name, f"OVERRIDE({label})", override)
        print(f"deploy-gate {name}: {label} overridden: {override}", file=sys.stderr)
        return 0
    print(f"deploy-gate {name}: {label} ({len(files)} sensitive files tracked)", file=sys.stderr)
    log(name, label, "; ".join(problems)[:500])
    return verdict


def pre_push():
    repo = run(["git", "rev-parse", "--show-toplevel"]).stdout.strip()
    name, rc = repo_name(repo), 0
    for line in sys.stdin.read().splitlines():
        parts = line.split()
        if len(parts) != 4 or not DEPLOY_BRANCHES.match(parts[2]) or set(parts[1]) == {"0"}:
            continue
        with tempfile.TemporaryDirectory() as tmp:  # gate exactly the pushed commit, not the dirty tree
            extract(repo, parts[1], tmp)
            # the archive has no history, so secrets are scanned on the real repo up to the pushed commit
            rc = max(rc, check(tmp, name, secrets=scan_secrets(repo, log_opts=parts[1])))
    return rc


def extract(repo, sha, dest):
    tar = subprocess.Popen(["git", "-C", repo, "archive", sha], stdout=subprocess.PIPE)
    subprocess.run(["tar", "-x", "-C", dest], stdin=tar.stdout, check=True)
    if tar.wait() != 0:
        sys.exit(f"deploy-gate: cannot read commit {sha} in {repo}")


def baseline(d, name=None):
    d = os.path.abspath(d)
    name = repo_name(d, name)
    surfaces = [surface(d)]  # working tree: what npm predeploy and publish.sh check
    if is_git(d) and run(["git", "-C", d, "rev-parse", "--verify", "-q", "HEAD"]).returncode == 0:
        with tempfile.TemporaryDirectory() as tmp:  # HEAD: what the pre-push hook checks
            extract(d, "HEAD", tmp)
            surfaces.append(surface(tmp))
    known = {s["fingerprint"] for s in load_stamps(name)}
    for fp, files in surfaces:
        if fp not in known:
            known.add(fp)
            add_stamp(name, {"fingerprint": fp, "files": files, "audited": False, "kind": "baseline", "at": time.strftime("%F %T")})
    print(f"deploy-gate {name}: baseline recorded, {len(surfaces[0][1])} sensitive files (unaudited)")
    return 0


def stamp(d, run_dir, name=None):
    d, run_dir = os.path.abspath(d), os.path.abspath(os.path.expanduser(run_dir))
    name = repo_name(d, name)
    with open(os.path.join(run_dir, "run-metadata.json")) as f:
        meta = json.load(f)
    if meta.get("run_status") != "complete":
        sys.exit(f"stamp refused: run_status is {meta.get('run_status')!r}, not 'complete'")
    v = run(["node", os.path.join(os.path.dirname(GATE), "../../security-audit/validate-findings.cjs"),
             os.path.join(run_dir, "findings.json")])
    if v.returncode != 0:
        sys.exit(f"stamp refused: findings.json fails validate-findings.cjs\n{v.stdout[-400:]}{v.stderr[-400:]}")
    with open(os.path.join(run_dir, "findings.json")) as f:
        bad = [x["title"] for x in json.load(f) if x.get("verdict") == "confirmed"
               and x.get("severity", {}).get("overall_severity") in ("high", "critical")]
    if bad:
        sys.exit("stamp refused: confirmed high/critical findings must be fixed and re-audited: " + "; ".join(bad))
    m = re.search(r"\b[0-9a-f]{7,40}\b", json.dumps(meta.get("source_ref")))
    if not m or "dirty\": true" in json.dumps(meta.get("source_ref")).lower():
        sys.exit("stamp refused: source_ref must name a clean commit sha")
    with tempfile.TemporaryDirectory() as tmp:  # fingerprint what was audited, not today's tree
        extract(d, m.group(0), tmp)
        fp, files = surface(tmp)
    add_stamp(name, {"fingerprint": fp, "files": files, "audited": True, "kind": "cloudflare-full-audit",
                     "run": run_dir, "source_ref": m.group(0), "profile": meta.get("profile"), "at": time.strftime("%F %T")})
    print(f"deploy-gate {name}: audit stamp recorded for {m.group(0)} ({len(files)} sensitive files)")
    return 0


def install(d):
    d = os.path.abspath(d)
    done = []
    for hook in hook_files(d):
        if os.path.exists(hook) and "deploy-gate" not in open(hook).read():
            done.append(f"{os.path.relpath(hook, d)} SKIPPED: an existing hook is not ours, wire it by hand")
            continue
        os.makedirs(os.path.dirname(hook), exist_ok=True)
        with open(hook, "w") as f:
            f.write(HOOK)
        os.chmod(hook, 0o755)
        done.append(f"{os.path.relpath(hook, d)} hook")
        if hook.startswith(os.path.join(d, ".husky") + os.sep) and "/_/" not in hook:
            # keep the local husky hook out of commits: teammates have no gate at this path
            exclude = os.path.join(d, run(["git", "-C", d, "rev-parse", "--git-path", "info/exclude"]).stdout.strip())
            os.makedirs(os.path.dirname(exclude), exist_ok=True)
            if "/.husky/pre-push" not in (open(exclude).read() if os.path.exists(exclude) else ""):
                with open(exclude, "a") as f:
                    f.write("\n/.husky/pre-push\n")
    pkg = os.path.join(d, "package.json")
    if os.path.exists(pkg):
        with open(pkg) as f:
            raw = f.read()
        data = json.loads(raw)
        scripts = data.get("scripts", {})
        if "deploy" in scripts and scripts.get("predeploy") != PREDEPLOY:
            if "predeploy" in scripts:
                done.append("predeploy SKIPPED: an existing predeploy script is not ours")
            else:
                scripts["predeploy"] = PREDEPLOY
                indent = 4 if '\n    "' in raw else 2
                with open(pkg, "w") as f:
                    f.write(json.dumps(data, indent=indent, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))
                done.append("npm predeploy")
    pub = os.path.join(d, "scripts", "publish.sh")
    if os.path.exists(pub):
        text = open(pub).read()
        anchor = 'cd "$TMP/repo"\n'
        if PUBLISH_MARK in text:
            done.append("publish.sh (already)")
        elif text.count(anchor) == 1:
            with open(pub, "w") as f:
                f.write(text.replace(anchor, anchor + "\n" + PUBLISH_SNIPPET))
            done.append("publish.sh")
        else:
            done.append("publish.sh SKIPPED: anchor not found, wire it by hand")
    baseline(d)
    print(f"deploy-gate install {d}: " + ", ".join(done))
    return 0


def hook_files(d):
    """pre-push files to own. Husky repos run .husky/pre-push from their stub, so own that one too."""
    if not is_git(d):
        return []
    hooks = run(["git", "-C", d, "rev-parse", "--git-path", "hooks"]).stdout.strip()
    stub = os.path.join(d, hooks, "pre-push") if not os.path.isabs(hooks) else os.path.join(hooks, "pre-push")
    if hooks.rstrip("/").endswith(".husky/_"):
        husky_stub = os.path.exists(stub) and "deploy-gate" not in open(stub).read()
        return [os.path.join(d, ".husky", "pre-push")] + ([] if husky_stub else [stub])
    return [stub]


def is_deploy_repo(d):
    names = set(os.listdir(d))
    if names & {"wrangler.jsonc", "wrangler.json", "wrangler.toml", "railway.json", "railway.toml", "vercel.json", "netlify.toml", "fly.toml"}:
        return True
    return os.path.exists(os.path.join(d, "scripts", "publish.sh"))


def wired(d):
    ok = all(os.path.exists(h) and "deploy-gate" in open(h).read() for h in hook_files(d))
    pkg = os.path.join(d, "package.json")
    if ok and os.path.exists(pkg) and "deploy" in json.load(open(pkg)).get("scripts", {}):
        ok = json.load(open(pkg))["scripts"].get("predeploy") == PREDEPLOY
    pub = os.path.join(d, "scripts", "publish.sh")
    if ok and os.path.exists(pub):
        ok = PUBLISH_MARK in open(pub).read()
    return ok


def coverage(roots, fix=False):
    rc = 0
    for root in roots:
        for n in sorted(os.listdir(root)):
            d = os.path.join(root, n)
            if os.path.isdir(d) and is_deploy_repo(d) and (os.path.exists(os.path.join(d, ".git")) or os.path.exists(os.path.join(d, "scripts", "publish.sh"))):
                w = wired(d)
                if not w and fix:
                    install(d)
                    w = wired(d)
                rc |= not w
                if not w or not fix:
                    print(f"{'wired  ' if w else 'MISSING'} {d}")
    return int(rc)


def main(a):
    if not a:
        print(__doc__)
        return 2
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    cmd, d = a[0], (a[1] if len(a) > 1 and not a[1].startswith("--") else ".")
    if cmd == "check":
        return check(d, opt("--name"))
    if cmd == "pre-push":
        return pre_push()
    if cmd == "baseline":
        return baseline(d, opt("--name"))
    if cmd == "stamp":
        return stamp(d, opt("--run"), opt("--name"))
    if cmd == "install":
        return install(d)
    if cmd == "coverage":
        return coverage([x for x in a[1:] if x != "--fix"] or [os.path.expanduser("~/repos")], "--fix" in a)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
