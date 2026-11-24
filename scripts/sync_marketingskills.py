#!/usr/bin/env python3
"""Vendor skills from coreyhaines31/marketingskills into marketing/<name>/.

Copies each upstream skills/<name>/ tree verbatim, drops evals/, and writes
UPSTREAM.md plus marketing/LICENSE-marketingskills. A second run against the
same upstream SHA does not change files.

Safety: a marketing/<name>/ folder is written only when it does not exist yet,
or when its UPSTREAM.md already points at coreyhaines31/marketingskills. Any
other existing folder is left untouched and reported as a conflict.

Usage:
  python3 scripts/sync_marketingskills.py --self-test
  python3 scripts/sync_marketingskills.py --report /tmp/marketingskills-report.json
  python3 scripts/sync_marketingskills.py --open-pr --report /tmp/marketingskills-report.json

--open-pr pushes branch sync/marketingskills and opens or updates a pull
request. It refuses to run unless GITHUB_ACTIONS=true or --allow-push is set,
and it never pushes main.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

SOURCE_URL = "https://github.com/coreyhaines31/marketingskills"
MARKER = "coreyhaines31/marketingskills"
LOCK_REL = ".sync/marketingskills.json"
LICENSE_REL = "marketing/LICENSE-marketingskills"
README_REL = "marketing/README.md"
SYNC_BRANCH = "sync/marketingskills"
RESERVED_NAMES = {"README.md", "LICENSE-marketingskills", "LICENSE"}
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
COUNT_RE = re.compile(r"\*\*\d+ skills\*\* in this folder\.")
FANCY_DASHES = (("\u2014", "em dash"), ("\u2013", "en dash"), ("\u2015", "horizontal bar"))
COPYRIGHT_RE = re.compile(r"^Copyright \(c\) .+$", re.M)
VERSION_HEADING_RE = re.compile(r"^(\d+\.\d+\.\d+)\b")
PIN_RE = re.compile(r"\bat ([0-9a-f]{7,40})\b")


def assert_no_fancy_dashes(text, label):
    for ch, name in FANCY_DASHES:
        if ch in text:
            raise SystemExit(f"{label} contains an {name}")


def scrub_dashes(text):
    text = text.replace(" \u2014 ", ", ").replace("\u2014", ", ")
    text = text.replace(" \u2013 ", "-").replace("\u2013", "-")
    text = text.replace(" \u2015 ", ", ").replace("\u2015", ", ")
    return text


def version_key(value):
    if not value:
        return None
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", str(value).strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def run(cmd, cwd=None, check=True, capture=False):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if check and result.returncode != 0:
        detail = ""
        if capture:
            detail = "\n" + (result.stderr or "") + (result.stdout or "")
        raise SystemExit(f"command failed ({result.returncode}): {' '.join(cmd)}{detail}")
    return result


def read_text(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def file_mode(path):
    return stat.S_IMODE(os.lstat(path).st_mode)


def write_bytes(path, data, mode):
    """Write path when the bytes or mode differ. Return True if a write happened."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    if os.path.isfile(path) and not os.path.islink(path):
        if read_bytes(path) == data and file_mode(path) == mode:
            return False
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, mode)
    return True


def write_text(path, text):
    assert_no_fancy_dashes(text, path)
    data = text.encode("utf-8")
    return write_bytes(path, data, 0o644)


def load_json(path):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path, payload):
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    assert_no_fancy_dashes(text, path)
    return write_text(path, text)


def skill_names(skills_dir):
    names = []
    odd = []
    if not os.path.isdir(skills_dir):
        raise SystemExit(f"upstream skills directory is missing: {skills_dir}")
    for name in sorted(os.listdir(skills_dir)):
        path = os.path.join(skills_dir, name)
        if not os.path.isdir(path) or os.path.islink(path):
            continue
        if not os.path.isfile(os.path.join(path, "SKILL.md")):
            continue
        if name in RESERVED_NAMES or not NAME_RE.match(name):
            odd.append(name)
            continue
        names.append(name)
    return names, odd


def classify_destination(dest):
    """Return new, vendored, or conflict."""
    if os.path.islink(dest):
        return "conflict", "path is a symlink"
    if not os.path.exists(dest):
        return "new", ""
    if not os.path.isdir(dest):
        return "conflict", "path exists and is not a directory"
    upstream = os.path.join(dest, "UPSTREAM.md")
    if os.path.isfile(upstream) and not os.path.islink(upstream):
        text = read_text(upstream)
        if MARKER in text:
            return "vendored", ""
    return "conflict", "existing folder has no UPSTREAM.md pointing at coreyhaines31/marketingskills"


def iter_skill_files(skill_dir):
    """Yield (relpath, abspath) for files to vendor. evals/ is omitted."""
    skill_real = os.path.realpath(skill_dir)
    for dirpath, dirnames, filenames in os.walk(skill_dir, followlinks=False):
        dirnames[:] = [name for name in dirnames if name != "evals" and name != ".git"]
        for filename in filenames:
            if filename in {".DS_Store", "UPSTREAM.md"}:
                continue
            full = os.path.join(dirpath, filename)
            if os.path.islink(full):
                real = os.path.realpath(full)
                if not (real == skill_real or real.startswith(skill_real + os.sep)):
                    raise SystemExit(f"refusing to copy a symlink that leaves the skill: {full}")
            rel = os.path.relpath(full, skill_dir)
            if rel.split(os.sep)[0] == "evals":
                continue
            yield rel, full


def upstream_note(sha, version, copyright_line):
    text = (
        f"Vendored from {SOURCE_URL} at {sha}, version {version}, license MIT, "
        f"{copyright_line}. Unmodified except evals/ removed. "
        f"Re-vendor from upstream rather than editing in place.\n"
    )
    assert_no_fancy_dashes(text, "UPSTREAM.md")
    return text


def prune_empty_dirs(root):
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if dirpath == root:
            continue
        if not dirnames and not filenames:
            os.rmdir(dirpath)


def replace_skill(src, dest, note):
    """Copy src into dest, dropping evals/. Return 'content' or 'provenance' or 'unchanged'."""
    desired = {}
    for rel, full in iter_skill_files(src):
        mode = file_mode(full)
        if not mode & 0o111:
            mode = 0o644
        else:
            mode = 0o755
        desired[rel] = (read_bytes(full), mode)
    desired["UPSTREAM.md"] = (note.encode("utf-8"), 0o644)

    os.makedirs(dest, exist_ok=True)
    content_changed = False
    wrote = False
    keep = set(desired)
    for dirpath, dirnames, filenames in os.walk(dest):
        dirnames[:] = [name for name in dirnames]
        for filename in filenames:
            full = os.path.join(dirpath, filename)
            rel = os.path.relpath(full, dest)
            if rel not in keep:
                os.remove(full)
                wrote = True
                if rel != "UPSTREAM.md":
                    content_changed = True
    prune_empty_dirs(dest)
    for rel, (data, mode) in sorted(desired.items()):
        path = os.path.join(dest, rel)
        changed = write_bytes(path, data, mode)
        if changed:
            wrote = True
            if rel != "UPSTREAM.md":
                content_changed = True
    if not wrote:
        return "unchanged"
    if content_changed:
        return "content"
    return "provenance"


def remove_tree(path):
    if os.path.islink(path) or os.path.isfile(path):
        os.remove(path)
        return
    shutil.rmtree(path)


def marketing_skill_count(repo_root):
    marketing = os.path.join(repo_root, "marketing")
    count = 0
    if not os.path.isdir(marketing):
        return 0
    for name in os.listdir(marketing):
        if os.path.isfile(os.path.join(marketing, name, "SKILL.md")):
            count += 1
    return count


def update_marketing_count(repo_root, count):
    path = os.path.join(repo_root, README_REL)
    if not os.path.isfile(path):
        return False
    text = read_text(path)
    repl = f"**{count} skills** in this folder."
    new, found = COUNT_RE.subn(repl, text, count=1)
    if found != 1:
        return False
    if new == text:
        return False
    assert_no_fancy_dashes(new, path)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(new)
    return True


def parse_versions(text):
    """Return [(version, section_markdown)] from VERSIONS.md, newest first."""
    marker = "## Recent Changes"
    index = text.find(marker)
    if index < 0:
        return []
    body = text[index:]
    parts = re.split(r"(?m)^### ", body)
    sections = []
    for part in parts[1:]:
        heading, _, _rest = part.partition("\n")
        match = VERSION_HEADING_RE.match(heading.strip())
        if not match:
            continue
        sections.append((match.group(1), "### " + part.strip() + "\n"))
    return sections


def changelog_excerpt(versions_text, old_version, new_version, limit=8000):
    if not versions_text:
        return "VERSIONS.md was not in the upstream tree."
    sections = parse_versions(versions_text)
    if not sections:
        return "VERSIONS.md has no Recent Changes section."
    old_key = version_key(old_version)
    new_key = version_key(new_version)
    chosen = []
    if old_key and new_key:
        chosen = [section for version, section in sections if old_key < version_key(version) <= new_key]
    elif new_key:
        chosen = [section for version, section in sections if version_key(version) == new_key]
    if not chosen:
        chosen = [sections[0][1]]
        note = "No version range matched. The newest VERSIONS.md section is included.\n\n"
    else:
        note = ""
    excerpt = scrub_dashes(note + "\n".join(chosen).strip() + "\n")
    if len(excerpt) > limit:
        excerpt = excerpt[:limit].rstrip() + "\n\nExcerpt truncated. Read VERSIONS.md at the new SHA for the rest.\n"
    return excerpt


def read_upstream_meta(upstream_root):
    plugin = os.path.join(upstream_root, ".claude-plugin", "plugin.json")
    version = ""
    if os.path.isfile(plugin):
        version = str(json.loads(read_text(plugin)).get("version") or "")
    if not version:
        marketplace = os.path.join(upstream_root, ".claude-plugin", "marketplace.json")
        if os.path.isfile(marketplace):
            meta = json.loads(read_text(marketplace)).get("metadata") or {}
            version = str(meta.get("version") or "")
    if not version:
        raise SystemExit("upstream plugin version was not found")
    license_path = os.path.join(upstream_root, "LICENSE")
    if not os.path.isfile(license_path):
        raise SystemExit("upstream LICENSE is missing")
    license_text = read_text(license_path)
    match = COPYRIGHT_RE.search(license_text)
    if not match:
        raise SystemExit("upstream LICENSE has no Copyright line")
    versions_path = os.path.join(upstream_root, "VERSIONS.md")
    versions_text = read_text(versions_path) if os.path.isfile(versions_path) else ""
    return version, match.group(0), license_text, versions_text


def previous_pins(repo_root):
    marketing = os.path.join(repo_root, "marketing")
    found = set()
    if not os.path.isdir(marketing):
        return []
    for name in os.listdir(marketing):
        path = os.path.join(marketing, name, "UPSTREAM.md")
        if os.path.isfile(path):
            text = read_text(path)
            if MARKER in text:
                found.update(PIN_RE.findall(text))
    return sorted(found)


def apply_vendor(repo_root, upstream_root, sha, version, copyright_line, license_text, versions_text):
    skills_dir = os.path.join(upstream_root, "skills")
    names, odd = skill_names(skills_dir)
    marketing = os.path.join(repo_root, "marketing")
    os.makedirs(marketing, exist_ok=True)
    old_lock = load_json(os.path.join(repo_root, LOCK_REL)) or {}
    pins = previous_pins(repo_root)

    added, content, provenance, unchanged = [], [], [], []
    skipped = []
    for name in odd:
        skipped.append({
            "name": name,
            "reason": "skill name is not a single safe path segment under marketing/",
        })
    vendored = []
    for name in names:
        dest = os.path.join(marketing, name)
        kind, reason = classify_destination(dest)
        if kind == "conflict":
            skipped.append({"name": name, "reason": reason})
            continue
        note = upstream_note(sha, version, copyright_line)
        if kind == "new":
            os.makedirs(dest, exist_ok=True)
            replace_skill(os.path.join(skills_dir, name), dest, note)
            added.append(name)
        else:
            outcome = replace_skill(os.path.join(skills_dir, name), dest, note)
            if outcome == "content":
                content.append(name)
            elif outcome == "provenance":
                provenance.append(name)
            else:
                unchanged.append(name)
        vendored.append(name)

    removed = []
    upstream_set = set(names)
    for name in sorted(os.listdir(marketing)):
        dest = os.path.join(marketing, name)
        if name in upstream_set or name in RESERVED_NAMES:
            continue
        if not os.path.isdir(dest) or os.path.islink(dest):
            continue
        kind, _reason = classify_destination(dest)
        if kind == "vendored":
            remove_tree(dest)
            removed.append(name)

    license_changed = write_text(os.path.join(repo_root, LICENSE_REL), license_text if license_text.endswith("\n") else license_text + "\n")
    conflicts = sorted(item["name"] for item in skipped)
    lock = {
        "conflicts": conflicts,
        "copyright": copyright_line,
        "license": "MIT",
        "omit": ["evals"],
        "sha": sha,
        "skills": vendored,
        "source": SOURCE_URL,
        "version": version,
    }
    lock_changed = dump_json(os.path.join(repo_root, LOCK_REL), lock)
    count_changed = update_marketing_count(repo_root, marketing_skill_count(repo_root))
    files_changed = bool(added or content or provenance or removed or license_changed or lock_changed or count_changed)

    old_sha = old_lock.get("sha")
    old_version = old_lock.get("version")
    report = {
        "added": added,
        "changelog": changelog_excerpt(versions_text, old_version, version),
        "conflicts": skipped,
        "content_updated": content,
        "copyright": copyright_line,
        "files_changed": files_changed,
        "new_sha": sha,
        "new_version": version,
        "old_sha": old_sha,
        "old_version": old_version,
        "previous_pins": pins,
        "provenance_updated": provenance,
        "removed": removed,
        "source": SOURCE_URL,
        "unchanged": unchanged,
        "vendored": vendored,
    }
    return report


def category_readme_paths(repo_root):
    script = os.path.join(repo_root, "scripts", "build_index.py")
    spec = importlib.util.spec_from_file_location("champ_build_index", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    paths = [
        os.path.join(repo_root, "INDEX.md"),
        os.path.join(repo_root, "README.md"),
    ]
    for folder, _label, _blurb in module.CATEGORIES:
        paths.append(os.path.join(repo_root, folder, "README.md"))
    return module, paths


def snapshot(paths):
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.encode("utf-8"))
        digest.update(b"\0")
        if os.path.isfile(path):
            digest.update(read_bytes(path))
        else:
            digest.update(b"<missing>")
        digest.update(b"\0")
    return digest.hexdigest()


def clone_upstream(url, dest):
    run(["git", "clone", "--quiet", "--depth", "1", url, dest])
    sha = run(["git", "-C", dest, "rev-parse", "HEAD"], capture=True).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise SystemExit(f"unexpected upstream SHA: {sha}")
    return sha


def render_pr_body(report):
    old_sha = report.get("old_sha") or "none"
    new_sha = report["new_sha"]
    old_version = report.get("old_version") or "none"
    new_version = report["new_version"]
    lines = [
        "## Marketingskills sync",
        "",
        f"Upstream: {SOURCE_URL}",
        f"Old SHA: `{old_sha}`",
        f"New SHA: `{new_sha}`",
        f"Old version: {old_version}",
        f"New version: {new_version}",
        "",
    ]
    if report.get("old_sha"):
        lines.append(f"Compare: {SOURCE_URL}/compare/{report['old_sha']}...{new_sha}")
    else:
        lines.append(f"Commit: {SOURCE_URL}/commit/{new_sha}")
    lines.append("")

    def section(title, rows):
        lines.append(f"### {title}")
        lines.append("")
        if not rows:
            lines.append("None.")
        else:
            lines.extend(rows)
        lines.append("")

    section("Added", [f"- `{name}`" for name in report.get("added") or []])
    updated_rows = [f"- `{name}` (content)" for name in report.get("content_updated") or []]
    updated_rows += [f"- `{name}` (provenance only)" for name in report.get("provenance_updated") or []]
    section("Updated", updated_rows)
    section("Removed", [f"- `{name}`" for name in report.get("removed") or []])
    skipped_rows = []
    for item in report.get("conflicts") or []:
        skipped_rows.append(f"- `{item['name']}`: {item['reason']}")
    section("Skipped", skipped_rows)
    lines.append("### Upstream changelog")
    lines.append("")
    lines.append("Excerpt from VERSIONS.md when that file is present. Skill files themselves are copied verbatim.")
    lines.append("")
    lines.append(report.get("changelog") or "No changelog excerpt.")
    lines.append("")
    lines.append(
        "This workflow uses the default GITHUB_TOKEN with contents: write and "
        "pull-requests: write. It pushes only the branch `sync/marketingskills` and "
        "opens or updates a pull request. It does not push to main. If organization "
        "settings block GitHub Actions from creating pull requests, enable "
        "\"Allow GitHub Actions to create and approve pull requests\" in the "
        "repository or organization Actions settings. The job fails with that "
        "reason instead of pushing to main."
    )
    lines.append("")
    body = "\n".join(lines)
    body = scrub_dashes(body)
    assert_no_fancy_dashes(body, "pull request body")
    return body


def github_output(changed):
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"changed={'true' if changed else 'false'}\n")


def sync_repo(repo_root, report_path=None):
    with tempfile.TemporaryDirectory(prefix="marketingskills-") as tmp:
        upstream_root = os.path.join(tmp, "src")
        sha = clone_upstream(SOURCE_URL, upstream_root)
        version, copyright_line, license_text, versions_text = read_upstream_meta(upstream_root)
        report = apply_vendor(
            repo_root, upstream_root, sha, version, copyright_line, license_text, versions_text
        )
    module, paths = category_readme_paths(repo_root)
    before = snapshot(paths)
    module.main()
    after = snapshot(paths)
    changed = bool(report["files_changed"] or before != after)
    report["changed"] = changed
    github_output(changed)
    print(
        "marketingskills {sha} v{version}: added {added}, content {content}, "
        "provenance {provenance}, unchanged {unchanged}, skipped {skipped}, removed {removed}, "
        "changed {changed}".format(
            sha=report["new_sha"][:12],
            version=report["new_version"],
            added=len(report["added"]),
            content=len(report["content_updated"]),
            provenance=len(report["provenance_updated"]),
            unchanged=len(report["unchanged"]),
            skipped=len(report["conflicts"]),
            removed=len(report["removed"]),
            changed=str(changed).lower(),
        )
    )
    if report_path:
        parent = os.path.dirname(report_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, sort_keys=True)
            handle.write("\n")
    return report


def current_branch(repo_root):
    result = run(["git", "-C", repo_root, "rev-parse", "--abbrev-ref", "HEAD"], capture=True)
    return result.stdout.strip()


def porcelain_paths(repo_root):
    result = run(["git", "-C", repo_root, "status", "--porcelain"], capture=True)
    paths = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path.strip())
    return paths


def assert_safe_changes(repo_root, report):
    allowed_skills = set(report.get("added") or [])
    allowed_skills.update(report.get("content_updated") or [])
    allowed_skills.update(report.get("provenance_updated") or [])
    allowed_skills.update(report.get("removed") or [])
    module, paths = category_readme_paths(repo_root)
    allowed_readmes = {os.path.relpath(path, repo_root) for path in paths}
    unexpected = []
    for path in porcelain_paths(repo_root):
        if path in allowed_readmes or path == LOCK_REL or path == LICENSE_REL:
            continue
        if path.startswith("marketing/"):
            parts = path.split("/")
            skill = parts[1] if len(parts) > 1 else ""
            if skill in allowed_skills:
                continue
        unexpected.append(path)
    if unexpected:
        raise SystemExit("refusing to commit unexpected paths: " + ", ".join(unexpected))
    # module is loaded to share the category list; silence unused warnings.
    del module


def open_pull_request(repo_root, report_path, allow_push):
    if os.environ.get("GITHUB_ACTIONS") != "true" and not allow_push:
        raise SystemExit("refusing to push outside GitHub Actions without --allow-push")
    report = load_json(report_path)
    if not report:
        raise SystemExit(f"report is missing: {report_path}")
    if not report.get("changed"):
        print("no changes, pull request not opened")
        return
    if current_branch(repo_root) == SYNC_BRANCH:
        raise SystemExit("refusing to start from the sync branch itself")
    assert_safe_changes(repo_root, report)
    run(["git", "-C", repo_root, "checkout", "-B", SYNC_BRANCH])
    if current_branch(repo_root) != SYNC_BRANCH:
        raise SystemExit("refusing to commit because HEAD is not the sync branch")
    run(["git", "-C", repo_root, "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"])
    run(["git", "-C", repo_root, "config", "user.name", "github-actions[bot]"])
    run(["git", "-C", repo_root, "add", "--", "marketing", LOCK_REL, "INDEX.md", "README.md"])
    # Category README tables live above marketing/ as well. Stage those paths only.
    _module, paths = category_readme_paths(repo_root)
    rels = [os.path.relpath(path, repo_root) for path in paths]
    run(["git", "-C", repo_root, "add", "--", *rels])
    assert_safe_changes(repo_root, report)
    staged = run(["git", "-C", repo_root, "diff", "--cached", "--name-only"], capture=True).stdout.strip()
    if not staged:
        print("no staged changes, pull request not opened")
        return
    version = report.get("new_version") or "unknown"
    sha = report.get("new_sha") or "unknown"
    message = (
        f"Sync marketingskills to v{version} ({sha[:12]})\n\n"
        f"Old SHA: {report.get('old_sha') or 'none'}\n"
        f"New SHA: {sha}\n"
    )
    assert_no_fancy_dashes(message, "commit message")
    run(["git", "-C", repo_root, "commit", "-m", message])
    push_sync_branch(repo_root)
    body = render_pr_body(report)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".md") as handle:
        handle.write(body)
        body_path = handle.name
    title = f"Sync marketingskills to v{version}"
    assert_no_fancy_dashes(title, "pull request title")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    owner = repository.split("/")[0] if "/" in repository else ""
    head = f"{owner}:{SYNC_BRANCH}" if owner else SYNC_BRANCH
    listed = run(
        ["gh", "pr", "list", "--base", "main", "--head", head, "--state", "open", "--json", "number"],
        cwd=repo_root,
        capture=True,
    )
    existing = json.loads(listed.stdout or "[]")
    try:
        if existing:
            number = str(existing[0]["number"])
            result = run(
                ["gh", "pr", "edit", number, "--title", title, "--body-file", body_path],
                cwd=repo_root,
                capture=True,
            )
            print(result.stdout.strip() or f"updated pull request #{number}")
        else:
            result = run(
                ["gh", "pr", "create", "--base", "main", "--head", SYNC_BRANCH, "--title", title, "--body-file", body_path],
                cwd=repo_root,
                capture=True,
            )
            print(result.stdout.strip())
    except SystemExit as error:
        text = str(error).lower()
        blocked = (
            "not permitted to create" in text
            or "resource not accessible" in text
            or "pull request creation" in text and "not permitted" in text
        )
        if blocked:
            raise SystemExit(
                "GitHub Actions could not create or update the pull request. "
                "Organization or repository settings are blocking pull requests from "
                "GITHUB_TOKEN. Enable \"Allow GitHub Actions to create and approve "
                "pull requests\" and rerun this workflow. main was not pushed."
            ) from error
        raise
    finally:
        os.remove(body_path)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(body)
            handle.write("\n")


def push_sync_branch(repo_root):
    if current_branch(repo_root) != SYNC_BRANCH:
        raise SystemExit("refusing to push because HEAD is not sync/marketingskills")
    probe = run(
        ["git", "-C", repo_root, "ls-remote", "--heads", "origin", SYNC_BRANCH],
        capture=True,
    )
    if probe.stdout.strip():
        run(
            ["git", "-C", repo_root, "fetch", "origin", f"+refs/heads/{SYNC_BRANCH}:refs/remotes/origin/{SYNC_BRANCH}"]
        )
        run(
            [
                "git", "-C", repo_root, "push", "--force-with-lease",
                "-u", "origin", f"HEAD:refs/heads/{SYNC_BRANCH}",
            ]
        )
    else:
        run(["git", "-C", repo_root, "push", "-u", "origin", f"HEAD:refs/heads/{SYNC_BRANCH}"])


def tree_signature(root):
    digest = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name != ".git")
        for filename in sorted(filenames):
            full = os.path.join(dirpath, filename)
            rel = os.path.relpath(full, root)
            digest.update(rel.encode("utf-8"))
            digest.update(b"\0")
            if os.path.islink(full):
                digest.update(b"link")
                digest.update(os.readlink(full).encode("utf-8"))
            else:
                digest.update(read_bytes(full))
                digest.update(str(file_mode(full)).encode("utf-8"))
            digest.update(b"\0")
    return digest.hexdigest()


def self_test():
    with tempfile.TemporaryDirectory(prefix="ms-self-") as tmp:
        repo = os.path.join(tmp, "repo")
        upstream = os.path.join(tmp, "upstream")
        os.makedirs(os.path.join(repo, "marketing"))
        os.makedirs(os.path.join(upstream, "skills", "already", "references"))
        os.makedirs(os.path.join(upstream, "skills", "already", "evals"))
        os.makedirs(os.path.join(upstream, "skills", "fresh"))
        os.makedirs(os.path.join(upstream, "skills", "owner-skill"))
        os.makedirs(os.path.join(upstream, ".claude-plugin"))
        with open(os.path.join(upstream, "skills", "already", "SKILL.md"), "w", encoding="utf-8") as handle:
            handle.write("---\nname: already\n---\nnew body\n")
        with open(os.path.join(upstream, "skills", "already", "references", "a.md"), "w", encoding="utf-8") as handle:
            handle.write("ref\n")
        with open(os.path.join(upstream, "skills", "already", "evals", "bad.md"), "w", encoding="utf-8") as handle:
            handle.write("nope\n")
        with open(os.path.join(upstream, "skills", "fresh", "SKILL.md"), "w", encoding="utf-8") as handle:
            handle.write("fresh\n")
        with open(os.path.join(upstream, "skills", "owner-skill", "SKILL.md"), "w", encoding="utf-8") as handle:
            handle.write("hijack\n")
        license_text = "MIT License\n\nCopyright (c) 2025 Corey Haines\n\nPermission is hereby granted.\n"
        with open(os.path.join(upstream, "LICENSE"), "w", encoding="utf-8") as handle:
            handle.write(license_text)
        with open(os.path.join(upstream, ".claude-plugin", "plugin.json"), "w", encoding="utf-8") as handle:
            json.dump({"version": "9.9.9"}, handle)
        versions = (
            "# Versions\n\n## Recent Changes\n\n"
            "### 9.9.9 (2026-11-23)\n\n- Fresh skill with a dash \u2014 here.\n\n"
            "### 9.9.8 (2026-11-01)\n\n- Older note.\n"
        )
        with open(os.path.join(upstream, "VERSIONS.md"), "w", encoding="utf-8") as handle:
            handle.write(versions)

        already = os.path.join(repo, "marketing", "already")
        os.makedirs(os.path.join(already, "evals"))
        with open(os.path.join(already, "SKILL.md"), "w", encoding="utf-8") as handle:
            handle.write("old\n")
        with open(os.path.join(already, "extra.txt"), "w", encoding="utf-8") as handle:
            handle.write("local\n")
        with open(os.path.join(already, "evals", "keep.md"), "w", encoding="utf-8") as handle:
            handle.write("eval\n")
        with open(os.path.join(already, "UPSTREAM.md"), "w", encoding="utf-8") as handle:
            handle.write(f"Vendored from {SOURCE_URL} at abcdef1, version 9.9.8, license MIT.\n")
        owner = os.path.join(repo, "marketing", "owner-skill")
        os.makedirs(owner)
        with open(os.path.join(owner, "SKILL.md"), "w", encoding="utf-8") as handle:
            handle.write("owner original\n")
        retired = os.path.join(repo, "marketing", "retired-skill")
        os.makedirs(retired)
        with open(os.path.join(retired, "SKILL.md"), "w", encoding="utf-8") as handle:
            handle.write("gone\n")
        with open(os.path.join(retired, "UPSTREAM.md"), "w", encoding="utf-8") as handle:
            handle.write(f"Vendored from {SOURCE_URL} at abcdef1, version 9.9.8, license MIT.\n")
        with open(os.path.join(repo, "marketing", "README.md"), "w", encoding="utf-8") as handle:
            handle.write("# Marketing\n\n**1 skills** in this folder.\n\n| Skill | What it does |\n|---|---|\n")

        version, copyright_line, license_out, versions_text = read_upstream_meta(upstream)
        report = apply_vendor(repo, upstream, "a" * 40, version, copyright_line, license_out, versions_text)
        owner_text = read_text(os.path.join(owner, "SKILL.md"))
        if owner_text != "owner original\n":
            raise SystemExit("self-test failed: owner skill was overwritten")
        if os.path.exists(os.path.join(owner, "UPSTREAM.md")):
            raise SystemExit("self-test failed: owner skill gained UPSTREAM.md")
        if os.path.exists(os.path.join(already, "extra.txt")) or os.path.exists(os.path.join(already, "evals")):
            raise SystemExit("self-test failed: stale or evals files remain")
        if "new body" not in read_text(os.path.join(already, "SKILL.md")):
            raise SystemExit("self-test failed: vendored skill was not refreshed")
        if not os.path.isfile(os.path.join(repo, "marketing", "fresh", "SKILL.md")):
            raise SystemExit("self-test failed: new skill was not added")
        if os.path.exists(retired):
            raise SystemExit("self-test failed: retired vendored skill was not removed")
        note = read_text(os.path.join(already, "UPSTREAM.md"))
        if MARKER not in note or "a" * 40 not in note or "9.9.9" not in note or "MIT" not in note:
            raise SystemExit("self-test failed: UPSTREAM.md is missing sha, version, or license")
        assert_no_fancy_dashes(note, "UPSTREAM.md")
        if "owner-skill" not in {item["name"] for item in report["conflicts"]}:
            raise SystemExit("self-test failed: owner skill was not reported as a conflict")
        if report["added"] != ["fresh"] or report["removed"] != ["retired-skill"]:
            raise SystemExit(f"self-test failed: unexpected added/removed {report['added']} {report['removed']}")
        if "already" not in report["content_updated"]:
            raise SystemExit("self-test failed: content update was not reported")
        if not read_text(os.path.join(repo, LICENSE_REL)).startswith("MIT License\n"):
            raise SystemExit("self-test failed: license was not copied")
        if "**3 skills** in this folder." not in read_text(os.path.join(repo, README_REL)):
            raise SystemExit("self-test failed: marketing count was not updated")
        excerpt = changelog_excerpt(versions, "9.9.8", "9.9.9")
        if "\u2014" in excerpt or "here" not in excerpt or "Older note" in excerpt:
            raise SystemExit("self-test failed: changelog excerpt was not scrubbed")
        body = render_pr_body(report)
        if "\u2014" in body or "\u2013" in body:
            raise SystemExit("self-test failed: pull request body contains a fancy dash")
        first = tree_signature(repo)
        again = apply_vendor(repo, upstream, "a" * 40, version, copyright_line, license_out, versions_text)
        second = tree_signature(repo)
        if first != second:
            raise SystemExit("self-test failed: second vendor run changed files")
        if again["added"] or again["content_updated"] or again["provenance_updated"] or again["removed"]:
            raise SystemExit("self-test failed: second run reported changes")
        if "already" not in again["unchanged"] or "fresh" not in again["unchanged"]:
            raise SystemExit("self-test failed: second run did not mark skills unchanged")
    print("self-test ok")


def main(argv):
    parser = argparse.ArgumentParser(description="Vendor coreyhaines31/marketingskills into marketing/.")
    parser.add_argument("--self-test", action="store_true", help="run the offline safety test and exit")
    parser.add_argument("--report", help="write a JSON report to this path (outside the repo in CI)")
    parser.add_argument("--open-pr", action="store_true", help="commit the current vendor result and open or update the sync PR")
    parser.add_argument("--allow-push", action="store_true", help="allow --open-pr outside GitHub Actions")
    parser.add_argument("--repo-root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = parser.parse_args(argv)
    repo_root = os.path.abspath(args.repo_root)
    if args.self_test:
        self_test()
        return 0
    if args.open_pr:
        if not args.report:
            raise SystemExit("--open-pr requires --report")
        open_pull_request(repo_root, args.report, args.allow_push)
        return 0
    sync_repo(repo_root, args.report)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
