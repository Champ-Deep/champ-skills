#!/usr/bin/env python3
"""Self-test for prep_gate.py. Run from this folder: python3 test_prep_gate.py. Exits non-zero on any assert."""
import copy
import json
import os

from prep_gate import check, timing_gap_minutes

here = os.path.dirname(os.path.abspath(__file__))
good = json.load(open(os.path.join(here, "..", "references", "example-state.json")))


def mutate(fn):
    s = copy.deepcopy(good)
    fn(s)
    return check(s)


# 11:00 AM PST is 2:00 PM Eastern, the other surface says 2:30 PM Eastern: a 30 minute conflict.
assert timing_gap_minutes("2030-01-15", good["timing"]["spoken"], good["timing"]["host_pack"]) == 30
assert check(good) == [], check(good)
assert any("no conflict is recorded" in f for f in mutate(lambda s: s["timing"].update(conflict_recorded=False)))
assert any("new timing decision" in f for f in mutate(lambda s: s["timing"].update(new_decision_cards=["t_x"])))
assert any("held follow-up" in f for f in mutate(lambda s: s.update(released_cards=["t_example2"])))
assert any("rewritten" in f for f in mutate(lambda s: s["questions"].update(script=["A better question."])))
assert any("isolated_tracks" in f for f in mutate(lambda s: s["claims_made"].append("isolated_tracks")))
assert any("pre-event draft" in f for f in mutate(lambda s: (s["occurrence"].update(recording_ready_mail_found=True), s["drafts"].update(pre_event_staged=["sound check"]))))
assert any("route discrepancy" in f for f in mutate(lambda s: s["route"].update(resolution="picked /podcasts")))
assert any("not verified 200" in f for f in mutate(lambda s: s["resources"]["links"].append({"url": "https://dead.example", "status": 404})))
assert any("forbidden" in f for f in mutate(lambda s: s["public_text"].update(resources_page="Host Name wrote this \u2014 x")))
assert any("read back" in f for f in mutate(lambda s: s["drafts"].update(staged=[{"subject": "x", "deduped": True, "read_back": False}])))
assert any("ruling is not recorded" in f for f in mutate(lambda s: s["timing"].update(ruling="")))
assert any("superseded" in f for f in mutate(lambda s: s["timing"].update(superseded="")))
assert any("owner_status" in f for f in mutate(lambda s: s["timing"].pop("owner_status")))
assert any("required term" in f for f in mutate(lambda s: s["public_text"].update(resources_page="Nothing useful here.")))
try:
    timing_gap_minutes("2030-01-15", {"clock": "11:00 AM", "zone": "CET"}, good["timing"]["host_pack"])
    raise SystemExit("unknown zone was accepted")
except ValueError as err:
    assert "unknown time zone" in str(err)
print("OK: example passes and 14 mutations are each caught")
