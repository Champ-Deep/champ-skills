#!/usr/bin/env python3
"""Podcast preparation gate. Usage: python3 prep_gate.py state.json  (exit 0 = pass, 1 = fail).

Reads one JSON state describing the prep and asserts the rules in
references/podcast-preparation-workflow.md. See references/example-state.json for the shape.
Stdlib only. Does not touch the network: link statuses are recorded by the caller from curl.
"""
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

FIXED = {"PST": -8, "PDT": -7, "EST": -5, "EDT": -4, "UTC": 0, "IST": 5.5}
REGION = {"PACIFIC": "America/Los_Angeles", "PT": "America/Los_Angeles",
          "EASTERN": "America/New_York", "ET": "America/New_York"}
# Strings that must never reach a public page. Callers add names via state["forbidden_public"].
DEFAULT_FORBIDDEN = [r"/Users/", r"\bt_[0-9a-f]{8}\b", r"\[VERIFY", r"[\u2014\u2013]",
                     r"(?i)\bvault\b", r"(?i)\bbarter\b", r"(?i)\bprivate\b"]
# Claims a button or a rehearsal cannot prove. Each needs an evidence entry before it may be asserted.
EVIDENCE_CLAIMS = {"isolated_tracks", "licence_tier", "file_quality", "publication_consent"}


def to_utc(date, clock, zone):
    """date 'YYYY-MM-DD', clock '2:30 PM', zone 'PST' or 'Eastern'."""
    t = datetime.strptime(f"{date} {clock.strip().upper()}", "%Y-%m-%d %I:%M %p")
    z = zone.strip().upper()
    if z not in FIXED and z not in REGION:
        raise ValueError(f"unknown time zone {zone!r}, use one of {sorted(FIXED) + sorted(REGION)}")
    if z in FIXED:
        return (t - timedelta(hours=FIXED[z])).replace(tzinfo=timezone.utc)
    return t.replace(tzinfo=ZoneInfo(REGION[z])).astimezone(timezone.utc)


def timing_gap_minutes(date, a, b):
    """Minutes between two stated times for the same event. 0 means they agree."""
    return int(abs((to_utc(date, a["clock"], a["zone"]) - to_utc(date, b["clock"], b["zone"])).total_seconds()) // 60)


def check(s):
    fails = []

    def need(ok, msg):
        if not ok:
            fails.append(msg)

    # 1. Guest-agreed questions survive verbatim into the script.
    for q in s["questions"]["agreed"]:
        need(q in s["questions"]["script"], f"guest-agreed question rewritten or missing: {q[:50]}")

    # 2. Timing: two surfaces that disagree must be recorded as a conflict and left with the owner card.
    t = s["timing"]
    gap = timing_gap_minutes(t["date"], t["spoken"], t["host_pack"])
    if gap:
        need(t.get("conflict_recorded") is True, f"timing differs by {gap} min and no conflict is recorded")
        need(bool(t.get("owner_card")), "timing conflict has no owner card named")
        need(not t.get("new_decision_cards"), "a new timing decision card was created, defer to the owner card")
        need(not t.get("picked_a_time"), "a time was picked silently")
        # The owner card is read first: once it has ruled, the ruling is the authority and the other surface is superseded.
        need(t.get("owner_status") in ("open", "ruled"), "owner_status must be open or ruled, read the owner card")
        if t.get("owner_status") == "ruled":
            need(bool(t.get("ruling")), "owner card has ruled but the ruling is not recorded")
            need(t.get("superseded"), "owner card has ruled but the losing surface is not named as superseded")

    # 3. Occurrence gate: pre-event sends are dead once the event has happened.
    occ = s["occurrence"]
    if occ["recording_ready_mail_found"]:
        need(not s["drafts"]["pre_event_staged"], "pre-event draft staged after the recording already happened")
    else:
        need(not occ.get("claimed_happened"), "claims the recording happened with no evidence")

    # 4. Held follow-ups stay held.
    # shortcut: trusts the declared held_cards list, so read the card status itself before declaring it empty; upgrade by passing live statuses in.
    need(not set(s["held_cards"]) & set(s["released_cards"]), "a held follow-up card was released")

    # 5. Consent and production: observed features are not evidence of tracks, licence, quality, consent.
    for c in s["claims_made"]:
        if c in EVIDENCE_CLAIMS:
            need(bool(s["evidence"].get(c)), f"claim '{c}' has no evidence (a button is not evidence)")

    # 6. Route discrepancy is recorded and deferred, never resolved by a new approval card.
    r = s["route"]
    if r["transcript"] != r["brief"]:
        need(r["resolution"] == "defer_to_owner_thread", "route discrepancy not deferred to the page owner's thread")
        need(not r.get("new_approval_card"), "route discrepancy produced a new approval card")

    # 7. Resource list: provisional until the actual episode says what was mentioned; links verified.
    res = s["resources"]
    need(res["status"] in ("provisional", "actual"), "resource list status must be provisional or actual")
    if res["status"] == "actual":
        need(bool(res.get("episode_evidence")), "actual resource list without episode evidence")
    for link in res["links"]:
        need(link["status"] == 200, f"link not verified 200: {link['url']}")

    # 8. Public text leak scan and dashes, on every text the state marks public.
    pats = DEFAULT_FORBIDDEN + [re.escape(x) for x in s.get("forbidden_public", [])]
    for name, text in s["public_text"].items():
        for p in pats:
            need(not re.search(p, text), f"public text '{name}' matches forbidden pattern {p}")
        # Required terms come from the latest brief version, checked on the real page text.
        for term in s.get("required_public", []):
            need(term in text, f"public text '{name}' is missing required term {term}")

    # 9. Nothing sent, posted or published; drafts need provider read-back.
    need(s["drafts"]["sent"] == 0 and not s["published"], "something was sent or published without approval")
    for d in s["drafts"]["staged"]:
        need(d.get("read_back") is True and d.get("deduped") is True, f"draft not deduped and read back: {d.get('subject')}")

    return fails


if __name__ == "__main__":
    out = check(json.load(open(sys.argv[1])))
    print("\n".join(f"FAIL: {f}" for f in out) or "PASS: all gates")
    sys.exit(1 if out else 0)
