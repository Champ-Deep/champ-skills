#!/usr/bin/env python3
"""Read-only audit of every Outlook draft: creates nothing, edits nothing, sends nothing.

Known-good invocation (Hermes's own interpreter, not the project one):

    env -u PYTHONPATH -u PYTHONHOME ~/.hermes/hermes-agent/venv/bin/python draft_audit.py [out.json]

Drives the inbox profile's stdio MCP mail client. Open that module for the
current client class name before importing it; the name is not stable.

Prints a JSON report (total drafts, flagged count, one row per flagged draft
with its flags and extracted [CONFIRM] items) and writes the same JSON to
out.json when a path is passed. See references/bulk-draft-audit.md.
"""
import asyncio
import json
import re
import sys

sys.path.insert(0, "/Users/deep/.hermes/profiles/inbox/inbox-bot")
from inbox_bot import McpMail

SELECT = (
    "id,subject,toRecipients,ccRecipients,body,bodyPreview,"
    "hasAttachments,categories,lastModifiedDateTime"
)

# Advisory scan only. For cold outbound drafts the outbound-email
# deliverability rules are the standard, not this list.
SPAM_WORDS = [
    "guarantee", "guaranteed", "100%", "urgent", "act now", "free",
    "risk-free", "no obligation", "winner", "exclusive deal", "limited time",
    "click here", "congratulations", "unlimited", "bonus", "cheap",
]

DASHES = (chr(0x2014), chr(0x2013))  # em dash, en dash: both banned by house rule


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
    for n, msg in enumerate(drafts):
        flags, confirms, to = audit(msg)
        if flags:
            rows.append({
                "n": n,
                "id": msg.get("id"),
                "subject": msg.get("subject"),
                "to": to,
                "flags": flags,
                "confirmations": confirms,
                "modified": msg.get("lastModifiedDateTime"),
            })
    report = {"total_drafts": len(drafts), "flagged": len(rows), "rows": rows}
    print(json.dumps(report, indent=2))
    if out_path:
        with open(out_path, "w") as fh:
            json.dump(report, fh, indent=2)
    return report


if __name__ == "__main__":
    asyncio.run(run(sys.argv[1] if len(sys.argv) > 1 else None))
