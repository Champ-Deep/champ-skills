#!/usr/bin/env python3
"""Scan a repo's open GitHub issues and batch them into kanban cards.

Quiet-when-idle contract (no_agent cron): diagnostics go to stderr, stdout is
the delivery channel and carries ONLY the run report. Empty stdout = no message
sent.

Configure via issue_autopilot_config.json next to this file:
  {"repos": ["owner/repo"], "assignee": "frontend", ...}
State (issue_autopilot_state.json, same dir): {"queued": {"owner/repo#12": ...}}

Usage:
  issue_autopilot.py --dry-run   # print the plan, change nothing
  issue_autopilot.py             # create cards, label + comment the issues
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "issue_autopilot_config.json"
STATE_PATH = HERE / "issue_autopilot_state.json"
GH = "gh"
DRY_RUN = "--dry-run" in sys.argv

DEFAULT_CONFIG = {
    "repos": [],            # e.g. ["owner/repo"]
    "assignee": "frontend",  # kanban profile that executes the cards
    "labels": ["bug", "enhancement"],  # empty list = all issues
    "max_cards_per_repo": 2,
    "max_issues_per_card": 3,
    "queued_label": "agent-queued",
    "goal_mode": True,
    "priority": 0,
}

EVENTS = []


def log(msg):
    print(msg, file=sys.stderr)


def run(args, input=None):
    return subprocess.run(args, capture_output=True, text=True, input=input)


def load_json(path, default):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def fetch_issues(repo, labels):
    args = [GH, "issue", "list", "-R", repo, "--state", "open",
            "--limit", "100", "--json", "number,title,body,labels,url,assignees"]
    r = run(args)
    if r.returncode != 0:
        log(f"[warn] gh issue list failed for {repo}: {r.stderr.strip()[:200]}")
        EVENTS.append(f"warning: could not list issues for {repo}: {r.stderr.strip()[:150]}")
        return []
    issues = json.loads(r.stdout or "[]")
    if labels:
        wanted = set(labels)
        issues = [i for i in issues if wanted & {l["name"] for l in i.get("labels", [])}]
    return issues


def group_issues(issues, max_per_card):
    """Bugs batch together; each enhancement gets its own card."""
    bugs, features = [], []
    for i in issues:
        names = {l["name"] for l in i.get("labels", [])}
        (bugs if "bug" in names else features).append(i)
    batches = [bugs[i:i + max_per_card] for i in range(0, len(bugs), max_per_card)]
    batches += [[f] for f in features]
    return [b for b in batches if b]


def branch_for(batch, kind):
    nums = "-".join(str(i["number"]) for i in batch)
    return f"feature/issues-{nums}" if kind == "bug" else f"feature/issue-{nums}"


def title_for(repo, batch):
    short = repo.split("/")[-1]
    nums = ", #".join(str(i["number"]) for i in batch)
    noun = "issues" if len(batch) > 1 else "issue"
    return f"{short}: implement {noun} #{nums}"


def card_body(repo, batch, branch):
    lines = [f"Implement the following GitHub issues from {repo} on branch `{branch}`.", ""]
    for i in batch:
        lines.append(f"- #{i['number']}: {i['title']} ({i['url']})")
        if i.get("body"):
            snippet = i["body"].strip().replace("\n", " ")[:600]
            lines.append(f"  {snippet}")
        lines.append("")
    lines += [
        "## Ground the work first",
        "Read the relevant code and cite `path:line` before changing anything; "
        "state the mechanism, not a guess.",
        "",
        "## Contract",
        "Push a feature branch and open a PR. DO NOT merge, delete branches, "
        "or touch anything outside this scope. Then request review.",
        "",
        "## Verification gates (all must pass)",
        "- typecheck/build clean",
        "- test suite green, including tests you added for the change",
        "- PR opened with the issue numbers in its description",
        "",
        "## Done means",
        "Branch pushed, PR URL in the completion summary, verification output "
        "quoted. Files changed and tests run reported in metadata.",
    ]
    return "\n".join(lines)


def ensure_label(repo):
    run([GH, "label", "create", "agent-queued", "-R", repo,
         "--color", "5319e7", "--description", "Queued to the Hermes agent board"])


def create_card(title, body, config):
    """Create via the `hermes kanban create` CLI (flags verified with --help)."""
    cmd = ["hermes", "kanban", "create", title,
           "--assignee", config["assignee"],
           "--body-file", "-",  # read body from stdin, survives newlines
           "--created-by", "issue-autopilot",
           "--idempotency-key", config["idem"], "--json"]
    if config.get("goal_mode"):
        cmd.append("--goal")
    return run(cmd, input=body)


def main():
    config = {**DEFAULT_CONFIG, **load_json(CONFIG_PATH, {})}
    state = load_json(STATE_PATH, {"queued": {}})
    queued = state["queued"]
    created = 0

    if not config["repos"]:
        log("[warn] no repos in issue_autopilot_config.json")
        EVENTS.append("warning: no repos configured")
        return

    for repo in config["repos"]:
        issues = fetch_issues(repo, config["labels"])
        fresh = []
        for i in issues:
            key = f"{repo}#{i['number']}"
            if key in queued:
                continue
            if i.get("assignees"):
                continue  # a human owns it
            fresh.append(i)
        if not fresh:
            log(f"[ok] {repo}: nothing new to queue")
            continue

        ensure_label(repo)
        for batch in group_issues(fresh, config["max_issues_per_card"]):
            if created >= config["max_cards_per_repo"]:
                log(f"[ok] {repo}: card cap reached")
                break
            kind = "bug" if "bug" in {l["name"] for l in batch[0].get("labels", [])} else "feature"
            branch = branch_for(batch, kind)
            title = title_for(repo, batch)
            nums = "-".join(str(i["number"]) for i in batch)
            idem = f"issue-autopilot:{repo}:{nums}"
            if DRY_RUN:
                print(f"[dry-run] would create card '{title}' (idem={idem})")
                continue

            body = card_body(repo, batch, branch)
            r = create_card(title, body, {**config, "idem": idem})
            if r.returncode != 0:
                log(f"[error] kanban create failed: {r.stderr.strip()[:300]}")
                EVENTS.append(f"error: kanban create failed for '{title}': {r.stderr.strip()[:200]}")
                continue
            try:
                card_id = json.loads(r.stdout).get("id") or json.loads(r.stdout).get("task_id")
            except Exception:
                card_id = r.stdout.strip()[:40]
            created += 1
            EVENTS.append(f"created card {card_id}: {title} -> branch {branch}")
            now = datetime.now(timezone.utc).isoformat()
            for i in batch:
                key = f"{repo}#{i['number']}"
                queued[key] = {"card": card_id, "at": now, "branch": branch}
                run([GH, "issue", "edit", str(i["number"]), "-R", repo,
                     "--add-label", config["queued_label"]])
                run([GH, "issue", "comment", str(i["number"]), "-R", repo, "--body",
                     f"Queued to the agent board as card {card_id} (branch {branch}). "
                     f"A PR will follow; it will not be merged without human review."])
            log(f"[created] {card_id}: {title}")

    if not DRY_RUN:
        STATE_PATH.write_text(json.dumps(state, indent=2))
    # stdout is the cron delivery channel: stay silent when nothing happened.
    if EVENTS:
        print("Issue Autopilot run report:")
        for e in EVENTS:
            print(f"- {e}")
    log(f"[done] cards created this run: {created}")


if __name__ == "__main__":
    main()
