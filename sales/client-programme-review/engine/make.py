#!/usr/bin/env python3
"""Programme review engine: <client_dir>/client.py + ledger.json -> the page.

  python3 make.py <client_dir>           draft: builds, and shows a red ribbon while any ledger entry is open
  python3 make.py <client_dir> --final   refuses while the ledger has an open entry or disagrees with the page

Output: <client_dir>/dist/<slug>.html (standalone), <slug>.artifact.html (fragment), data.json (what the page was built from).
"""
import json
import pathlib
import re
import runpy
import shutil
import sys

E = pathlib.Path(__file__).resolve().parent
KIT = E / "kit"
sys.path[:0] = [str(KIT), str(E.parent / "scripts")]
import ledger  # noqa: E402

ALL = ["universe", "work", "emails", "simulation", "leads", "learned", "loop", "research", "tiers"]
NEED = ["SLUG", "CLIENT", "BRAND", "NOTE_TITLE", "META", "LEADS", "SENDS", "UNIVERSE", "NAMED", "MARKETS", "FILTERS", "CARD", "DIMS", "COPY"]
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def clean(s):
    return re.sub(r"\s*[\u2013\u2014]\s*", ", ", str(s or "")).strip()


def simulation(K, D):
    """Raw simulation run -> the small shape the page reads. Analyst prose is replaced by the hand-written sim_notes.json."""
    run = pathlib.Path(str(K.get("SIM_RUN") or "")).expanduser()
    if not K.get("SIM_RUN") or not run.exists():
        return None
    raw = json.loads(run.read_text())
    notes = json.loads((CD / "sim_notes.json").read_text())
    P = []
    for p in raw["audience"]["personas"]:
        name = clean(p.get("name") or p["id"])
        P.append({"id": p["id"], "name": name, "ini": name[:2].upper(),
                  "desc": clean(", ".join(str(b) for b in (p.get("role"), p.get("industry"), p.get("decision_role")) if b and b != "unknown"))})
    t = next(x["test"] for x in raw["tests"] if x["test"]["channel"] != "landing_page")
    sends, vs = D["sends"], []
    for r in t["ranking"]:
        m = re.search(r"(\d+)\s*$", r["label"])  # a variant label ends with the number of the send it was used in
        i = int(m.group(1)) - 1 if m and int(m.group(1)) <= len(sends) else None
        rx = {x["persona_id"]: {"l": round(x["likelihood"], 3), "q": clean(x.get("quote"))}
              for x in r["panel"]["reactions"] if x.get("likelihood") is not None}
        ls = [v["l"] for v in rx.values()]
        vs.append({"label": r["label"], "i": i, "rank": r["rank"], "point": r["point"], "low": r["low"], "high": r["high"],
                   "actual": (sends[i][2] / sends[i][5]) if i is not None else None, "rx": rx, "mean": sum(ls) / len(ls) if ls else 0})
    if notes.get("ranking"):
        assert [v["label"] for v in vs] == notes["ranking"], "the ranking moved since sim_notes.json was written: reread the run and rewrite the notes"
    sent = [v for v in vs if v["i"] is not None]
    for n, v in enumerate(sent):
        v["rk5"] = n + 1  # rank among the messages that were really sent
    by_send = sorted(sent, key=lambda v: v["i"])
    j = lambda xs: " and ".join([", ".join(xs[:-1]), xs[-1]] if len(xs) > 1 else xs)
    parts = [(w, [v["label"] for v in by_send if f(v)]) for w, f in (
        ("inside the simulated band for", lambda v: v["low"] <= v["actual"] <= v["high"]),
        ("above it for", lambda v: v["actual"] > v["high"]), ("below it for", lambda v: v["actual"] < v["low"]))]
    act = sorted(sent, key=lambda v: -v["actual"])
    match = ("The real click rate landed " + ", and ".join(f"{w} {j(xs)}" for w, xs in parts if xs) + ". "
             f"The panel ranked {sent[0]['label']} highest and {sent[-1]['label']} lowest of the {WORDS.get(len(sent), len(sent))}. "
             f"The sends ranked {act[0]['label']} highest and {act[-1]['label']} lowest. "
             "The simulation reads the copy only. It does not see send order, list freshness or timing, which is why it is a filter before a test and never the test.")
    scored = len({pid for v in vs for pid in v["rx"]})
    top = max(x["l"] for v in vs for x in v["rx"].values())
    for v in vs:  # client-facing name: the simulation and its rewrite carry the brand, never the tool or the model
        if v["i"] is None:
            v["label"] = K["BRAND"] + " rewrite"
    return {"n": len(P), "scored": scored, "personas": P, "match": match, "ceil": max(0.1, round(top, 1)),
            "note": K["COPY"]["sim_note"].format(n=len(P), scored=scored),
            "email": {"vars": vs, "fixes": notes["fixes"], "asks": notes["asks"], "rewrite_note": notes["rewrite_note"]}}


def blocks(C, sections):
    """The list-shaped copy, rendered to the markup the stylesheet expects."""
    tilt, lift, delay, dur = ["-3deg", "1.5deg", "3.2deg"], ["26px", "0px", "34px"], [900, 1050, 1200], [1100, 1400, 800]
    fl = []
    for i, c in enumerate(C["floaters"]):
        cnt = f'data-count="{c["count"]}" data-delay="{delay[i]}" data-dur="{dur[i]}"'
        v = (f'<div class="v"><span {cnt}>{c["text"]}</span><small>{c["small"]}</small></div>' if c.get("small") else f'<div class="v" {cnt}>{c["text"]}</div>')
        gold = ";background:linear-gradient(90deg,#FFB703,#FF6903)" if c.get("gold") else ""
        extra = ('<div class="flags">' + "".join(f"<span>{f}</span>" for f in c["flags"]) + "</div>" if c.get("flags")
                 else f'<div class="mini" aria-hidden="true"><i style="--w:{c["bar"]:g}%{gold}"></i></div>' if c.get("bar") is not None else "")
        fl.append(f'<article class="fcard" style="--tilt:{tilt[i]};--lift:{lift[i]};--i:{i}">\n<div class="k">{c["k"]}</div>\n{v}\n<span class="cmp">{c["cmp"]}</span>\n{extra}\n</article>')
    assert len(fl) == 3, "the hero carries exactly three stat cards"
    tags = lambda ts: ('<div class="tags">' + "".join(f'<span class="tag{" hot" if hot else ""}">{t}</span>' for t, hot in ts) + "</div>") if ts else ""
    colors = ["#DCD3EF", "#9A5CEB", "#DD1286", "#FFB703"]
    return {
        "floaters": "\n".join(fl),
        "pills": "\n".join(f'<span class="pill"><b>{a}</b>{b}</span>' for a, b in C["pills"]),
        "toc": "".join(f'<a href="#{s}">{C["nav"][s]}</a>' for s in ALL if s in sections),
        "beats": "\n".join(f'<li{" class=\"on\"" if i == 0 else ""}><b class="num">{n}</b><div><h3>{h}</h3><p>{p}</p></div></li>' for i, (n, h, p) in enumerate(C["beats"])),
        "uni_key": "".join(f'<span><i style="background:{colors[i]}"></i>{t}</span>' for i, t in enumerate(C["uni_key"])),
        "reports": "\n".join(f"<li>{x}</li>" for x in C["reports"]),
        "steps": "\n".join(f'<div class="step" data-reveal><div class="n">{n}</div><div><h3>{h}</h3><p>{p}</p>{tags(ts)}</div></div>' for n, h, p, ts in C["steps"]),
        "loop_steps": "\n".join(f'<div class="tstep" style="--d:{200 + 300 * i}"><span class="n">Step {i + 1}</span><h4>{h}</h4><p>{p}</p></div>' for i, (h, p) in enumerate(C["loop_steps"])),
        "ticks": "\n".join(f'<li><label><input type="checkbox"><span><b>{b}</b>{t}</span></label></li>' for b, t in C["ticks"]),
        "why": "\n".join(f'<div><b class="num">{n}</b><p>{p}</p></div>' for n, p in C["why"]),
    }


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    CD = pathlib.Path(args[0]).resolve()
    FINAL = "--final" in sys.argv
    K = runpy.run_path(str(CD / "client.py"))
    missing = [n for n in NEED if n not in K]
    assert not missing, f"client.py is missing {missing}"
    C, SLUG = K["COPY"], K["SLUG"]
    sections = K.get("SECTIONS") or ALL
    assert set(sections) <= set(ALL), f"unknown section in SECTIONS: {set(sections) - set(ALL)}"
    assert len(K["UNIVERSE"]) >= 3 and len(C["beats"]) == 4 and len(C["uni_key"]) == 4, "the universe has four stages: profile, emailed, dialled, delivered"
    assert len(C["mail"]) == len(K["SENDS"]), "one copy per send"
    assert sum(bool(x.get("named")) for x in K["LEADS"]) <= 3, "the board holds three marks"

    LEDGER = json.loads((CD / "ledger.json").read_text())
    LEDGER = [e for e in LEDGER if not e.get("section") or e["section"] in sections]  # an entry tied to a section this build drops is not on the page
    errs, opens = ledger.check(LEDGER)
    if FINAL and (errs or opens):
        sys.exit("not final: " + "; ".join(errs + ["open: " + e["id"] for e in opens]))

    D = {"slug": SLUG, "note_title": K["NOTE_TITLE"], "named": K["NAMED"], "leads": K["LEADS"], "sends": K["SENDS"], "agg": K.get("AGG", {}),
         "universe": K["UNIVERSE"], "markets": K["MARKETS"], "filters": K["FILTERS"], "card": K["CARD"], "dims": K["DIMS"],
         "disp": K.get("DISP", {}), "suf": K.get("SUF", {}),
         "copy": {**{k: C.get(k) for k in ("mail", "lessons", "dims", "tiles", "tiers", "pending")}, "ticks_first": C["ticks"][0][0]}}
    D["oracle"] = simulation(K, D) if "simulation" in sections else None

    tpl = (E / "review.tpl.html").read_text()
    for sid in ALL:
        if sid not in sections:
            tpl, n = re.subn(r'<section[^>]*\bid="%s"[\s\S]*?</section>\n' % sid, "", tpl, count=1)
            assert n == 1, sid
    H = blocks(C, sections)
    X = {"brand": K["BRAND"], "client": K["CLIENT"], "loop_n": str(len(C["loop_steps"])), "ceil": f'{(D["oracle"] or {}).get("ceil", 0.4):g}',
         "em_scale": "Bars to scale, max %d" % max(s[2] for s in K["SENDS"])}
    tpl = re.sub(r"\{\{h:(\w+)\}\}", lambda m: H[m.group(1)], tpl)
    tpl = re.sub(r"\{\{c:(\w+)\}\}", lambda m: str(C[m.group(1)]), tpl)  # a KeyError here names the copy key client.py lacks
    tpl = re.sub(r"\{\{x:(\w+)\}\}", lambda m: X[m.group(1)], tpl)
    ribbon = "" if not opens else ('<div class="ep-draft" role="note">Draft, not for sharing. ' + str(len(opens)) + " figure" + ("s are" if len(opens) > 1 else " is")
                                   + " not yet confirmed: " + "; ".join(e["claim"] for e in opens) + ".</div>")
    (KIT / "cases").mkdir(exist_ok=True)
    (KIT / "cases/_pr.html").write_text(tpl.replace("<!--@DRAFT@-->", ribbon).replace("/*@DATA@*/", "var D=" + json.dumps(D, separators=(",", ":")) + ";"))
    (KIT / "cases/_pr.json").write_text(json.dumps({**K["META"], "slug": SLUG, "css": (E / "review.css").read_text()}))
    import build  # noqa: E402  the showcase kit

    build.build("_pr")
    out = CD / "dist"
    out.mkdir(exist_ok=True)
    for suf in (".html", ".artifact.html"):
        f = KIT / "dist" / (SLUG + suf)
        s = re.sub(r'href="(#[\w-]+)" target="_blank" rel="noopener"', r'href="\1"', f.read_text())  # in-page anchors must not open a new tab
        assert not re.search("[\u2013\u2014]", s), "dash found: rewrite the sentence"
        f.write_text(s)
        shutil.copy(f, out / f.name)
    (out / "data.json").write_text(json.dumps(D))
    page = (out / (SLUG + ".html")).read_text()
    errs, _ = ledger.check(LEDGER, page)  # the built page against the ledger: caveats present, figures as recorded
    for e in errs:
        print("LEDGER", e)
    print("built", out / (SLUG + ".html"), "| sections", len(sections), "| simulation", "yes" if D["oracle"] else "no")
    print("ledger:", len(LEDGER), "entries,", len(opens), "open,", len(errs), "errors", "(FINAL)" if FINAL else "(draft)")
    sys.exit(1 if errs else 0)
