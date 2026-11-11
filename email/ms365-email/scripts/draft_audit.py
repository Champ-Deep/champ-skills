#!/usr/bin/env python3
"""Read-only audit + send-readiness triage of every Outlook draft.

Creates nothing, edits nothing, sends nothing.

Known-good invocation (Hermes's own interpreter, not the project one):

    env -u PYTHONPATH -u PYTHONHOME ~/.hermes/hermes-agent/venv/bin/python draft_audit.py [out.json]

Drives the inbox profile's stdio MCP mail client. Open that module for the
current client class name before importing it; the name is not stable.

Prints a JSON report: total drafts, flagged count, one row per flagged draft
with its flags and extracted [CONFIRM] items, plus the send-readiness bucket
counts (needs-confirm / empty-to / stale / ready) and one bucketed row per
draft. Writes the same JSON to out.json when a path is passed.
See references/bulk-draft-audit.md sections 2-4.
"""
import asyncio
import datetime
import json
import re
import sys

sys.path.insert(0, "/Users/deep/.hermes/profiles/inbox/inbox-bot")
from inbox_bot import McpMail

SELECT = (
    "id,subject,toRecipients,ccRecipients,body,bodyPreview,"
    "hasAttachments,categories,lastModifiedDateTime,receivedDateTime"
)

# Advisory scan only. For cold outbound drafts the outbound-email
# deliverability rules are the standard, not this list.
SPAM_WORDS = [
    "guarantee", "guaranteed", "100%", "urgent", "act now", "free",
    "risk-free", "no obligation", "winner", "exclusive deal", "limited time",
    "click here", "congratulations", "unlimited", "bonus", "cheap",
]

DASHES = (chr(0x2014), chr(0x2013))  # em dash, en dash: both banned by house rule

# Heuristic, not policy: report the threshold alongside the counts.
STALE_DAYS = 6


def body_text(msg):
    body = msg.get("body")
    if isinstance(body, dict):
        return body.get("content") or ""
    if isinstance(body, str):
        return body
    return msg.get("bodyPreview") or ""


def confirm_items(text):
    """Extract [CONFIRM] / [CONFIRM: field] items, tolerating nested tags."""
    items = []
    for chunk in text.split("[CONFIRM")[1:]:
        chunk = chunk.lstrip(":").lstrip("]").strip()
        chunk = chunk.split("[", 1)[0].strip(" ;:,.")
        if chunk:
            items.append(chunk)
    return items


def age_days(msg):
    """Days since last touch; None when Graph gave no usable timestamp."""
    raw = msg.get("lastModifiedDateTime") or msg.get("receivedDateTime") or ""
    try:
        when = datetime.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (datetime.datetime.now(datetime.timezone.utc) - when).days


def audit(msg):
    text = body_text(msg)
    subject = msg.get("subject") or ""
    to = [r.get("emailAddress", {}).get("address", "")
          for r in (msg.get("toRecipients") or [])]
    flags = []
    confirms = confirm_items(text)
    if "[BOT:" in text:
        flags.append("bot-header")
    if confirms or "[CONFIRM" in text:
        flags.append("confirm-tag")
    haystack = subject + " " + text
    hits = sorted({w for w in SPAM_WORDS
                   if re.search(r"\b" + re.escape(w) + r"\b", haystack, re.I)})
    if hits:
        flags.append("spam:" + ",".join(hits))
    if any(d in haystack for d in DASHES):
        flags.append("em-en-dash")
    if re.search(r"\*\*|##\s|\]\(", text):
        flags.append("markdown-residue")
    if not to:
        flags.append("empty-to")
    if re.search(r"\b(Hi|Dear|Hello|Hey)\s+,", text):
        flags.append("nameless-salutation")
    return flags, confirms, to


def bucket(flags, age):
    """First match wins so the counts partition the folder."""
    if "bot-header" in flags or "confirm-tag" in flags:
        return "needs-confirm"
    if "empty-to" in flags:
        return "empty-to"
    if age is not None and age >= STALE_DAYS:
        return "stale"
    return "ready"


async def run(out_path=None):
    mail = McpMail()
    await mail.open()
    try:
        who = await mail.preflight()
        mailbox = who[0] if isinstance(who, list) and who else "deep@lakeb2b.com"
        res = await mail.call(
            "list-mail-folder-messages", mailbox,
            mailFolderId="drafts", select=SELECT, fetchAllPages=True,
        )
    finally:
        await mail.close()
    drafts = res.get("value", []) if isinstance(res, dict) else (res or [])

    rows = []
    triage = []
    counts = {"needs-confirm": 0, "empty-to": 0, "stale": 0, "ready": 0}
    for n, msg in enumerate(drafts):
        flags, confirms, to = audit(msg)
        age = age_days(msg)
        name = bucket(flags, age)
        counts[name] += 1
        row = {
            "n": n,
            "id": msg.get("id"),
            "subject": msg.get("subject"),
            "to": to,
            "age_days": age,
            "bucket": name,
            "flags": flags,
            "modified": msg.get("lastModifiedDateTime"),
        }
        triage.append(row)
        if flags:
            rows.append({**row, "confirmations": confirms})

    # The buckets are a partition: refuse to report a split that does not add up.
    assert sum(counts.values()) == len(drafts), "triage buckets do not partition the folder"

    report = {
        "total_drafts": len(drafts),
        "flagged": len(rows),
        "stale_threshold_days": STALE_DAYS,
        "triage_counts": counts,
        "rows": rows,
        "triage": triage,
    }
    print(json.dumps(report, indent=2))
    if out_path:
        with open(out_path, "w") as fh:
            json.dump(report, fh, indent=2)
    return report


if __name__ == "__main__":
    asyncio.run(run(sys.argv[1] if len(sys.argv) > 1 else None))
