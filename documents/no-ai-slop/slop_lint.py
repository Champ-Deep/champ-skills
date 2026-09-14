#!/usr/bin/env python3
"""slop_lint: flag AI-slop patterns in text (Champions Group no-ai-slop rules).

Usage:
  python3 slop_lint.py FILE [FILE...]        human-readable report
  python3 slop_lint.py --json FILE           JSON findings
  echo "text" | python3 slop_lint.py -       read stdin
Exit code 1 if any HIGH finding, else 0. Deterministic: catches surface patterns only.
Judgement calls (portability, voice, invented facts) need the no-ai-slop skill or a human.
"""
import re, sys, json

DASH = re.compile('[\u2013\u2014]')
BANNED = ("delve foster leverage leveraging leveraged utilize utilizing facilitate empower empowering streamline "
          "streamlined robust cutting-edge seamless seamlessly unlock unlocking synergy synergies best-in-class "
          "world-class tapestry realm beacon multifaceted meticulous meticulously intricate paramount transformative "
          "elevate elevating embark supercharge harness ever-evolving game-changer").split()
BANNED_PHRASES = ["paradigm shift", "game changer", "this is huge", "this changes everything"]
FILLER = ["it's worth noting", "it is worth noting", "it's important to note", "it is important to note",
          "at the end of the day", "when it comes to", "at its core", "in today's world", "in today's fast-paced",
          "in the age of", "the reality is", "the truth is", "in terms of", "with regard to", "going forward",
          "in this article", "let's dive in", "hope this email finds you well", "hope this finds you well",
          "just circling back", "just checking in"]
THROAT = ["here's the thing", "here is the thing", "let me be clear", "i'll be honest", "the uncomfortable truth",
          "here's what i mean", "let's be honest"]
FAUX = ["what most people get wrong", "what nobody tells you", "here's what nobody tells you", "the part everyone misses",
        "this is the part most people skip", "what no one talks about", "most people miss", "nobody talks about"]
RHETORICAL = ["what if i told you", "think about it:", "plot twist:", "here's the kicker", "spoiler:"]
PUFFERY = ["a testament to", "testament to", "pivotal moment", "plays a vital role", "plays a crucial role",
           "solidifies its position", "underscores its significance", "marks a pivotal", "stands as a"]
WEASEL = ["experts agree", "studies show", "research shows", "industry reports suggest", "many argue",
          "widely regarded as", "it is widely believed"]
META = ["that last part matters", "the key point is", "as you can see", "this distinction matters",
        "matters more than it sounds", "let that sink in", "read that again"]
RECAP = [r"^\s*in conclusion\b", r"^\s*ultimately,", r"^\s*overall,", r"^\s*to sum up\b", r"^\s*in summary\b"]
SUPERFICIAL = re.compile(r",\s+(highlighting|underscoring|showcasing|reflecting|emphasizing|signaling)\b", re.I)
BINARY = [
    re.compile(r"\b(it'?s|this is|that'?s|isn'?t|is)\s+not\s+(just\s+)?(about\s+)?[^.?!]{1,60}[.,;]\s*(it'?s|this is|that'?s)\b", re.I),
    re.compile(r"\bisn'?t\s+[^.?!]{1,50}[,.;]\s*(it'?s|it is)\b", re.I),
    re.compile(r"\bnot because\b[^.?!]{1,80}[.!]\s*because\b", re.I),
    re.compile(r"(\bnot|n't) just\b[^.?!]{1,60}\bbut\b", re.I),
    re.compile(r"\b(won'?t|doesn'?t|don'?t)\s+[^.?!]{1,50}\.\s+[A-Z][^.?!]{1,40}\s+(will|does|do)\.", re.I),
    re.compile(r"\b(don'?t|doesn'?t|didn'?t|won'?t|aren'?t|isn'?t)\s+(fail|failing|struggling|about)\b[^.?!]{0,40}\bbecause of\b", re.I),
    re.compile(r"\bstops? being\b[^.?!]{1,50}\.\s*(It|This|That)\s+becomes\b", re.I),
    re.compile(r"\bThe (problem|issue|question|bottleneck) (wasn'?t|isn'?t)\b", re.I),
]
NEG_TRICOLON = re.compile(r"\b(wasn'?t|isn'?t|not)\s+(the\s+)?\w+,\s+(the\s+)?\w+,?\s+or\s+(the\s+)?\w+", re.I)
META_START = re.compile(r"(?:^|[.!?]\s+)(Here'?s (why|how|what)\b)", re.M)
NEG_LIST = re.compile(r"\bNot an? [^.]{1,30}\.\s+Not an? [^.]{1,30}\.", re.I)
COLON_REVEAL = re.compile(r"(?:^|[.!?]\s+)((?:The|Our|My|Your|This|That|Here'?s|One thing)\b[^.:!?\n]{0,40}):\s+([a-z][^.!?\n]{2,140}[.!?])", re.M)
FRAGMENT_KICKER = re.compile(r"\b(That'?s it\.|That'?s the whole thing\.|Full stop\.|Period\.|Simple as that\.|Game over\.)", re.I)

def sentences(t):
    return [s for s in re.split(r'(?<=[.!?])\s+', t.strip()) if s]

QUOTED = re.compile(r'"[^"\n]{1,120}"|\u201c[^\u201d\n]{1,120}\u201d')

def lint(text, is_push=False, ignore_quoted=True):
    f = []
    raw = text
    if ignore_quoted:
        text = QUOTED.sub('""', text)
    low = text.lower()
    def add(sev, rule, match):
        f.append({"severity": sev, "rule": rule, "match": match.strip()[:90]})
    for m in DASH.finditer(raw):
        s = max(0, m.start()-25); add("HIGH", "dash", raw[s:m.end()+25])
    for w in BANNED:
        for m in re.finditer(r"\b" + re.escape(w) + r"\b", text, re.I):
            add("HIGH", "banned_word", m.group(0))
    for p in BANNED_PHRASES:
        if p in low: add("HIGH", "banned_word", p)
    for lst, rule, sev in [(FILLER, "filler_phrase", "MED"), (THROAT, "throat_clearing", "HIGH"),
                           (FAUX, "faux_insight", "HIGH"), (RHETORICAL, "rhetorical_setup", "MED"),
                           (PUFFERY, "puffery", "HIGH"), (WEASEL, "weasel_attribution", "HIGH"),
                           (META, "metadiscourse", "MED")]:
        for p in lst:
            i = low.find(p)
            while i != -1:
                add(sev, rule, text[i:i+len(p)+30]); i = low.find(p, i+1)
    for para in re.split(r"\n\s*\n", text):
        for r in RECAP:
            if re.search(r, para, re.I): add("MED", "recap_ending", para[:60])
    for m in SUPERFICIAL.finditer(text): add("MED", "superficial_ing", m.group(0))
    for rx in BINARY:
        for m in rx.finditer(text): add("HIGH", "binary_contrast", m.group(0))
    for m in NEG_LIST.finditer(text): add("HIGH", "negative_listing", m.group(0))
    for m in NEG_TRICOLON.finditer(text): add("MED", "negative_listing", m.group(0))
    for m in META_START.finditer(text): add("MED", "metadiscourse", m.group(1))
    # robotic parallelism: consecutive sentences with the same first two words or the same last two words
    ss = [re.sub(r"[^\w\s']", "", s).lower().split() for s in sentences(text)]
    for a, b in zip(ss, ss[1:]):
        if len(a) >= 3 and len(b) >= 3 and (a[:2] == b[:2] or a[-2:] == b[-2:]):
            add("MED", "robotic_parallel", " ".join(a[:6]) + " / " + " ".join(b[:6]))
    for m in COLON_REVEAL.finditer(text): add("MED", "colon_reveal", m.group(1) + ": " + m.group(2))
    for m in FRAGMENT_KICKER.finditer(text): add("HIGH", "dramatic_fragment", m.group(0))
    # stacked short fragments: 3+ consecutive sentences of <=3 words (skipped for push copy)
    if not is_push:
        run = []
        for s in sentences(text):
            if len(s.split()) <= 3: run.append(s)
            else:
                if len(run) >= 3: add("MED", "stacked_fragments", " ".join(run))
                run = []
        if len(run) >= 3: add("MED", "stacked_fragments", " ".join(run))
    # dedupe
    seen, out = set(), []
    for x in f:
        k = (x["rule"], x["match"].lower())
        if k not in seen: seen.add(k); out.append(x)
    return out

def main(argv):
    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"] or ["-"]
    worst = 0; allres = {}
    for p in paths:
        text = sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()
        res = lint(text); allres[p] = res
        if any(r["severity"] == "HIGH" for r in res): worst = 1
        if not as_json:
            print(f"== {p}: {len(res)} finding(s)")
            for r in res: print(f"  [{r['severity']}] {r['rule']}: {r['match']}")
    if as_json: print(json.dumps(allres, indent=2, ensure_ascii=True))
    return worst

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
