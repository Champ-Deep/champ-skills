import json, pathlib
from slop_lint import lint
FX = json.loads((pathlib.Path(__file__).parent / "fixtures.json").read_text())

def rules(text, **kw):
    return {f["rule"] for f in lint(text, **kw)}

def test_slop_fixtures_catch_expected_patterns():
    missed = {}
    for fx in FX["slop"]:
        got = rules(fx["text"])
        miss = set(fx["expect"]) - got
        if miss: missed[fx["id"]] = sorted(miss)
    assert not missed, f"missed patterns: {missed}"

def test_clean_controls_have_no_findings():
    fps = {}
    for fx in FX["clean"]:
        res = lint(fx["text"], is_push=fx.get("is_push", False))
        if res: fps[fx["id"]] = [(r["rule"], r["match"]) for r in res]
    assert not fps, f"false positives: {fps}"

def test_dash_detection_includes_en_dash_date_range():
    assert "dash" in rules("Pilot runs Sep 3\u20139.")

def test_quoted_examples_ignored_but_dashes_not():
    assert rules('Avoid "leverage" in emails.') == set()
    assert "dash" in rules('Avoid "a\u2014b" in emails.')

def test_regression_cases_from_blind_judge():
    missed = {}
    for fx in FX["regression"]:
        miss = set(fx["expect"]) - rules(fx["text"])
        if miss: missed[fx["id"]] = sorted(miss)
    assert not missed, f"missed patterns: {missed}"

def test_gated_outputs_stay_clean():
    fps = {fx["id"]: [(r["rule"], r["match"]) for r in lint(fx["text"])] for fx in FX["clean_generated"]}
    fps = {k: v for k, v in fps.items() if v}
    assert not fps, f"findings on judged-clean text: {fps}"

if __name__ == "__main__":
    import sys, traceback
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try: fn(); print("PASS", name)
            except AssertionError as e: fails += 1; print("FAIL", name, "\n   ", e)
    sys.exit(1 if fails else 0)
