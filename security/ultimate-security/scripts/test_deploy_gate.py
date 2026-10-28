#!/usr/bin/env python3
"""Self-check for deploy_gate.py against throwaway git repos. Run: python3 test_deploy_gate.py"""
import json, os, random, string, subprocess, sys, tempfile

GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy_gate.py")
tmp = tempfile.mkdtemp()
env = dict(os.environ, DEPLOY_GATE_STATE=os.path.join(tmp, "state"), DEPLOY_GATE_LOG=os.path.join(tmp, "gate.log"))
env.pop("DEPLOY_GATE_OVERRIDE", None)


def sh(*cmd, cwd=None, stdin=None, extra=None):
    return subprocess.run(cmd, cwd=cwd, input=stdin, capture_output=True, text=True, env=dict(env, **(extra or {})))


def gate(*a, **k):
    return sh("python3", GATE, *a, **k)


def git(repo, *a):
    r = sh("git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@t", *a)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def write(repo, path, text):
    os.makedirs(os.path.dirname(os.path.join(repo, path)), exist_ok=True)
    open(os.path.join(repo, path), "w").write(text)


repo = os.path.join(tmp, "app")
os.makedirs(repo)
git(repo, "init", "-q", "-b", "main")
write(repo, "src/index.js", "export default { fetch() { return new Response('ok') } }\n")
write(repo, "src/auth.js", "export function check(u) { return u && u.org }\n")
write(repo, "README.md", "auth docs\n")
write(repo, "package.json", json.dumps({"name": "app", "scripts": {"deploy": "wrangler deploy"}}, indent=2) + "\n")
write(repo, "wrangler.jsonc", "{}\n")
git(repo, "add", "-A"); git(repo, "commit", "-qm", "init")

# 1. no stamp yet: a sensitive file exists, so the audit is required
r = gate("check", repo, "--name", "app")
assert r.returncode == 3 and "src/auth.js" in r.stderr and "README.md" not in r.stderr, r.stderr

# 2. install wires hook + predeploy and baselines, so the same tree passes
r = gate("install", repo)
assert r.returncode == 0 and "pre-push hook" in r.stdout and "npm predeploy" in r.stdout, r.stdout + r.stderr
assert "predeploy" in json.load(open(os.path.join(repo, "package.json")))["scripts"]
r = gate("check", repo, "--name", "app")
assert r.returncode == 0 and "PASS" in r.stderr, r.stderr
r = gate("coverage", tmp)
assert r.returncode == 0 and "wired" in r.stdout, r.stdout

# 3. a non-sensitive change still passes; a sensitive change needs a fresh audit
write(repo, "src/index.js", "export default { fetch() { return new Response('ok2') } }\n")
assert gate("check", repo, "--name", "app").returncode == 0
write(repo, "src/auth.js", "export function check(u) { return true }\n")
r = gate("check", repo, "--name", "app")
assert r.returncode == 3 and "1 sensitive file(s) changed" in r.stderr, r.stderr

# 4. override passes and is logged with its reason
r = gate("check", repo, "--name", "app", extra={"DEPLOY_GATE_OVERRIDE": "test approval"})
assert r.returncode == 0 and "test approval" in open(env["DEPLOY_GATE_LOG"]).read()
git(repo, "checkout", "--", "src/auth.js")

# 5. a planted secret blocks, and the value never reaches the output
key = "ghp_" + "".join(random.choices(string.ascii_letters + string.digits, k=36))
write(repo, "src/config.js", f"export const token = '{key}'\n")
git(repo, "add", "-A"); git(repo, "commit", "-qm", "oops")
r = gate("check", repo, "--name", "app")
assert r.returncode == 1 and "secret" in r.stderr and key not in r.stderr + r.stdout, r.stderr

# 6. pre-push: feature branches pass untouched, main is gated on the pushed commit
sha = git(repo, "rev-parse", "HEAD")
hook = os.path.join(repo, ".git", "hooks", "pre-push")
r = sh(hook, "origin", "x", cwd=repo, stdin=f"refs/heads/f {sha} refs/heads/feature {'0'*40}\n")
assert r.returncode == 0, r.stderr
r = sh(hook, "origin", "x", cwd=repo, stdin=f"refs/heads/main {sha} refs/heads/main {'0'*40}\n")
assert r.returncode == 1 and key not in r.stderr, r.stderr
git(repo, "reset", "-q", "--hard", "HEAD~1")
sha = git(repo, "rev-parse", "HEAD")
r = sh(hook, "origin", "x", cwd=repo, stdin=f"refs/heads/main {sha} refs/heads/main {'0'*40}\n")
assert r.returncode == 0, r.stderr

# 7. stamp refuses an incomplete audit run and accepts a complete clean one
run = os.path.join(tmp, "run-1")
os.makedirs(run)
json.dump({"run_status": "incomplete", "source_ref": sha}, open(os.path.join(run, "run-metadata.json"), "w"))
json.dump([], open(os.path.join(run, "findings.json"), "w"))
r = gate("stamp", repo, "--run", run, "--name", "app2")
assert r.returncode != 0 and "not 'complete'" in r.stderr, r.stderr
json.dump({"run_status": "complete", "source_ref": {"commit": sha, "dirty": False}}, open(os.path.join(run, "run-metadata.json"), "w"))
r = gate("stamp", repo, "--run", run, "--name", "app2")
assert r.returncode == 0, r.stderr
assert gate("check", repo, "--name", "app2").returncode == 0

# 8. warn-only: the same blocking finding is reported and logged but does not block
write(repo, "src/auth.js", "export function check(u) { return 1 }\n")
assert gate("check", repo, "--name", "app").returncode == 3
json.dump({"warn_only": ["app"]}, open(os.path.join(env["DEPLOY_GATE_STATE"], "gate-config.json"), "w"))
r = gate("check", repo, "--name", "app")
assert r.returncode == 0 and "WARN-ONLY" in r.stderr and "WARN(AUDIT-REQUIRED)" in open(env["DEPLOY_GATE_LOG"]).read(), r.stderr

# 9. coverage --fix wires an unwired deploy repo
other = os.path.join(tmp, "other")
os.makedirs(other); git(other, "init", "-q"); write(other, "railway.json", "{}")
assert gate("coverage", tmp).returncode == 1
assert gate("coverage", "--fix", tmp).returncode == 0
assert gate("coverage", tmp).returncode == 0

# 10. husky repo: own .husky/pre-push (run by husky's stub) and keep it out of commits
hk = os.path.join(tmp, "husky")
os.makedirs(hk); git(hk, "init", "-q"); git(hk, "config", "core.hooksPath", ".husky/_")
write(hk, ".husky/_/pre-push", "#!/usr/bin/env sh\n. \"$(dirname \"$0\")/h\"")
write(hk, "railway.json", "{}")
r = gate("install", hk)
assert ".husky/pre-push hook" in r.stdout and "SKIPPED" not in r.stdout, r.stdout
assert "/.husky/pre-push" in open(os.path.join(hk, ".git", "info", "exclude")).read()
assert "deploy-gate" not in open(os.path.join(hk, ".husky/_/pre-push")).read()
assert ".husky/pre-push" not in git(hk, "status", "--porcelain", "-uall")

# 11. a plain folder nested inside another repo gets publish.sh wiring only, never the outer repo's hooks
nested = os.path.join(repo, "site")
write(nested, "scripts/publish.sh", 'set -e\ncd "$TMP/repo"\necho push\n')
before = os.listdir(os.path.join(repo, ".git", "hooks"))
r = gate("install", nested)
assert "publish.sh" in r.stdout and "hook" not in r.stdout, r.stdout
assert os.listdir(os.path.join(repo, ".git", "hooks")) == before
assert "deploy_gate.py\" check ." in open(os.path.join(nested, "scripts/publish.sh")).read()
assert sh("bash", "-n", os.path.join(nested, "scripts/publish.sh")).returncode == 0

print("deploy_gate self-check: 11 scenarios passed")
