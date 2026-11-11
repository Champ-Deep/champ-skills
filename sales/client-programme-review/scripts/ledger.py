#!/usr/bin/env python3
"""Reconciliation ledger: one entry per client-facing figure. A page is final only when no entry is open.

  python3 ledger.py ledger.json [page.html] [--final]   table, then exit 1 on any error (and on any open entry with --final)
  python3 ledger.py --selftest

Entry: {"id", "claim", "shown", "source", "as_of", "status", "by", "caveat", "client_can_check", "note"}
  status   matched   checked against the client's own record ("by" names the record)
           owner     confirmed by the account owner in this build ("by" names who and when)
           sourced   traced to one of our dated files; not allowed when the client can check the figure themselves
           caveated  unconfirmed, and the page says so ("caveat" must appear on the page word for word)
           cut       removed from the page ("shown" must no longer appear)
           open      unresolved: blocks a final build
  shown    the figure exactly as printed on the page; checked against the built page so ledger and page cannot drift
"""
import html
import json
import pathlib
import re
import sys

STATUS = ("matched", "owner", "sourced", "caveated", "cut", "open")
NEED = ("id", "claim", "source", "as_of", "status")


def _squash(s):
    return re.sub(r"\s+", "", html.unescape(s)).lower()


def haystacks(page_html):
    """The raw page and the page with tags removed, both without whitespace, so markup inside a phrase never hides it."""
    return _squash(page_html), _squash(re.sub(r"<[^>]+>", "", page_html))


def on_page(text, hay):
    t = _squash(text)
    return bool(t) and any(t in h for h in hay)


def check(entries, page_html=None):
    """Returns (errors, open_entries). errors is a list of strings; open_entries the entries still unresolved."""
    errors, seen = [], set()
    hay = haystacks(page_html) if page_html is not None else None
    for e in entries:
        eid = e.get("id", "?")
        for k in NEED:
            if not str(e.get(k, "")).strip():
                errors.append(f"{eid}: missing {k}")
        if eid in seen:
            errors.append(f"{eid}: duplicate id")
        seen.add(eid)
        st = e.get("status")
        if st not in STATUS:
            errors.append(f"{eid}: status must be one of {', '.join(STATUS)}")
            continue
        if st in ("matched", "owner") and not str(e.get("by", "")).strip():
            errors.append(f"{eid}: {st} needs 'by' (the record, or who confirmed and when)")
        if st == "sourced" and e.get("client_can_check"):
            errors.append(f"{eid}: the client can check this themselves, so match it to their record, get the owner to confirm it, or caveat it")
        if st == "caveated":
            if not str(e.get("caveat", "")).strip():
                errors.append(f"{eid}: caveated needs the caveat text")
            elif hay and not on_page(e["caveat"], hay):
                errors.append(f"{eid}: caveat is not on the page: {e['caveat'][:70]!r}")
        shown = str(e.get("shown", "")).strip()
        if hay and shown:
            if st == "cut" and on_page(shown, hay):
                errors.append(f"{eid}: marked cut but {shown!r} is still on the page")
            if st not in ("cut", "open") and not on_page(shown, hay):
                errors.append(f"{eid}: ledger says {shown!r} but the page does not show it")
    return errors, [e for e in entries if e.get("status") == "open"]


def table(entries):
    w = max((len(e.get("id", "")) for e in entries), default=4)
    return "\n".join(f"{e.get('status', '?'):9} {e.get('id', '?'):{w}}  {e.get('claim', '')}" for e in sorted(entries, key=lambda e: STATUS.index(e["status"]) if e.get("status") in STATUS else 9))


def _selftest():
    page = "<p>We delivered <b>25</b> leads. Sized on our 2 September call.</p><script>var D={\"co\":\"Acme\"}</script>"
    ok = {"id": "a", "claim": "leads", "shown": "delivered 25 leads", "source": "client sheet", "as_of": "2026-01-01", "status": "matched", "by": "client sheet rows"}
    assert check([ok], page) == ([], [])
    assert check([{**ok, "by": ""}], page)[0], "matched without by must fail"
    assert check([{**ok, "shown": "26 leads"}], page)[0], "page drift must fail"
    assert check([{**ok, "status": "sourced", "client_can_check": True}], page)[0], "client-checkable cannot be only sourced"
    cav = {**ok, "id": "b", "status": "caveated", "caveat": "Sized on our 2 September call."}
    assert check([cav], page) == ([], [])
    assert check([{**cav, "caveat": "not there"}], page)[0], "missing caveat must fail"
    assert check([{**ok, "status": "cut"}], page)[0], "cut figure still shown must fail"
    assert check([{**ok, "shown": "Acme"}], page) == ([], []), "data inside the page script counts as on the page"
    op = {**ok, "id": "c", "status": "open"}
    assert check([op], page) == ([], [op])
    assert check([ok, ok], page)[0], "duplicate id must fail"
    print("ledger selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
        sys.exit()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    entries = json.loads(pathlib.Path(args[0]).read_text())
    errs, opens = check(entries, pathlib.Path(args[1]).read_text() if len(args) > 1 else None)
    print(table(entries))
    for x in errs:
        print("ERROR", x)
    print(f"{len(entries)} entries, {len(opens)} open, {len(errs)} errors")
    sys.exit(1 if errs or (opens and "--final" in sys.argv) else 0)
