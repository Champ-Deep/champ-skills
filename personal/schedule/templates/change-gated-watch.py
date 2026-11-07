#!/usr/bin/env python3
"""Change-gated watcher: emits ONLY when observed state changed (or --force).

No-agent cron contract: unchanged state prints zero bytes, so the scheduler
stays silent. Copy this file, then edit the three marked blocks:
CONFIG (what to watch), snapshot() (how to read it), selftest() (the contract).

  <name>.py            first run emits a full report, second run emits nothing
  <name>.py --force    emit a full report even when nothing changed
  <name>.py --selftest assert: first run reports, rerun is silent, failure alerts

Rules encoded here (why, in one line each):
  - structured diff, never raw text: a timestamp or pid in the payload would
    otherwise fire a false alert every run.
  - read state DBs read-only (file:...?mode=ro): a watcher must never be able
    to write the thing it watches, and sqlite3.connect() defaults to create.
  - save the new snapshot even when emitting nothing: otherwise the next run
    diffs against stale state and re-reports the same change.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

# ---------------------------------------------------------------- CONFIG
HOME = Path.home() / ".hermes"
STATE_FILE = HOME / "state/<name>_watch.json"   # where the last snapshot lives
SESSION_ID = "<session id to watch>"            # drop this block if not watching a chat
CARDS = ("t_xxxxxxxx",)                         # kanban card ids to watch
# ------------------------------------------------------------ end CONFIG


def snapshot() -> dict:
    """Current observed state as JSON-safe structured fields only."""
    out: dict = {"session": {}, "cards": {}}
    db = HOME / "state.db"
    if SESSION_ID != "<session id to watch>" and db.exists():
        with sqlite3.connect(f"file:{db}?mode=ro", uri=True) as sdb:
            row = sdb.execute(
                "SELECT COUNT(*), COALESCE(MAX(id), 0) FROM messages WHERE session_id = ?",
                (SESSION_ID,),
            ).fetchone()
            lease = sdb.execute(
                "SELECT holder FROM session_turn_leases WHERE conversation_id = ?",
                (SESSION_ID,),
            ).fetchone()
            out["session"] = {
                "msg_count": row[0] if row else 0,
                "last_msg_id": row[1] if row else 0,
                "live": bool(lease),
            }
    kdb_path = HOME / "kanban.db"
    if CARDS != ("t_xxxxxxxx",) and kdb_path.exists():
        with sqlite3.connect(f"file:{kdb_path}?mode=ro", uri=True) as kdb:
            kdb.row_factory = sqlite3.Row
            for cid in CARDS:
                t = kdb.execute(
                    "SELECT status, assignee, current_run_id, last_failure_error "
                    "FROM tasks WHERE id = ?",
                    (cid,),
                ).fetchone()
                if not t:
                    continue
                comments = kdb.execute(
                    "SELECT COUNT(*) FROM task_comments WHERE task_id = ?", (cid,)
                ).fetchone()[0]
                ev = kdb.execute(
                    "SELECT kind FROM task_events WHERE task_id = ? ORDER BY id DESC LIMIT 1",
                    (cid,),
                ).fetchone()
                out["cards"][cid] = {
                    "status": t["status"],
                    "assignee": t["assignee"],
                    "run_id": t["current_run_id"],
                    "error": t["last_failure_error"],
                    "comments": comments,
                    "last_event": ev["kind"] if ev else None,
                }
    return out


# ------------------------------------------------------- evaluate + report
def evaluate(curr: dict, prev: dict | None, force: bool = False) -> list[str]:
    """One report line per changed element; [] when nothing moved."""
    lines: list[str] = []
    prev_cards = (prev or {}).get("cards", {})
    for cid, info in curr.get("cards", {}).items():
        if not force and prev_cards.get(cid) == info:
            continue
        err = f" ERROR={info['error']}" if info.get("error") else ""
        lines.append(
            f"[<name>] {cid} ({info.get('assignee')}): status={info.get('status')} "
            f"run={info.get('run_id')} comments={info.get('comments')} "
            f"last_event={info.get('last_event')}{err}"
        )
    if curr.get("session"):
        if force or curr.get("session") != (prev or {}).get("session"):
            s = curr["session"]
            lines.append(
                f"[<name>] session: msgs={s['msg_count']} last_id={s['last_msg_id']} live={s['live']}"
            )
    return lines


def selftest() -> int:
    """The no-agent contract: report once, then silence, then alert on failure."""
    sample = {
        "session": {"msg_count": 10, "last_msg_id": 99, "live": False},
        "cards": {
            "t_aaaaaaaa": {"status": "ready", "assignee": "default", "run_id": None,
                            "error": None, "comments": 0, "last_event": "skipped_nonspawnable"},
        },
    }
    first = evaluate(sample, None)
    assert first, "first run must report"
    assert evaluate(sample, sample) == [], "second run must be silent"
    failed = json.loads(json.dumps(sample))
    failed["cards"]["t_aaaaaaaa"]["status"] = "blocked"
    failed["cards"]["t_aaaaaaaa"]["error"] = "boom"
    alert = evaluate(failed, sample)
    assert len(alert) == 1 and "ERROR=boom" in alert[0], f"a failure must alert: {alert}"
    print("selftest ok")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    prev = None
    if STATE_FILE.exists():
        try:
            prev = json.loads(STATE_FILE.read_text())
        except (OSError, ValueError):
            prev = None
    curr = snapshot()
    lines = evaluate(curr, prev, force="--force" in argv)
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_name(STATE_FILE.name + ".tmp")
    tmp.write_text(json.dumps(curr, indent=2))
    tmp.replace(STATE_FILE)                   # atomic replace, never a half-written state
    if lines:
        print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))