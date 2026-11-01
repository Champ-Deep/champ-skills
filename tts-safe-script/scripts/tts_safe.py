#!/usr/bin/env python3
"""Respell acronyms, caps runs and digit tokens so an AI voice says them right.

Usage:
  tts_safe.py FILE            print the respelled text (what the voice reads)
  tts_safe.py --check FILE    exit 1 and list tokens still unsafe for TTS
  tts_safe.py --self-test
Reads stdin when FILE is "-". Captions keep the original text; only the TTS string is rewritten.
The lexicon below is the single source of truth. Add a term here, not in prose.
"""
import re
import sys

# initialism -> spaced letters; word-acronym -> phonetic lowercase; compound -> hyphenated lowercase
LEXICON = {
    "SEO": "S E O", "SEM": "S E M", "PPC": "P P C", "CTR": "C T R", "CPL": "C P L", "CPC": "C P C",
    "CPM": "C P M", "CTA": "C T A", "ABM": "A B M", "ICP": "I C P", "GTM": "G T M", "MQL": "M Q L",
    "SQL": "S Q L", "SDR": "S D R", "BDR": "B D R", "SMB": "S M B", "NPS": "N P S", "USP": "U S P",
    "B2B": "B to B", "B2C": "B to C", "D2C": "D to C", "LakeB2B": "Lake B to B", "Lake B2B": "Lake B to B",
    "CMO": "C M O", "CEO": "C E O", "CFO": "C F O", "CTO": "C T O", "COO": "C O O", "CIO": "C I O",
    "CISO": "see-so", "CRO": "C R O", "VP": "V P", "HR": "H R", "HQ": "H Q",
    "CRM": "C R M", "ERP": "E R P", "EHR": "E H R", "API": "A P I", "SaaS": "sass", "SKU": "skew",
    "KPI": "K P I", "OKR": "O K R", "KRA": "K R A", "ROI": "R O I", "ARR": "A R R", "MRR": "M R R",
    "LTV": "L T V", "CAC": "C A C", "CAGR": "C A G R", "EBITDA": "ee-bit-dah", "YoY": "year on year",
    "QoQ": "quarter on quarter", "FY": "F Y", "Q1": "Q one", "Q2": "Q two", "Q3": "Q three", "Q4": "Q four",
    "AI": "A I", "LLM": "L L M", "GPT": "G P T", "ChatGPT": "Chat G P T", "OpenAI": "Open A I",
    "TTS": "T T S", "STT": "S T T", "ML": "M L", "RAG": "rag", "MCP": "M C P", "CLI": "C L I",
    "URL": "U R L", "HTML": "H T M L", "CSS": "C S S", "JSON": "jay-sawn", "OAuth": "oh-auth",
    "UI": "U I", "UX": "U X", "PDF": "P D F", "CSV": "C S V", "SDK": "S D K", "IP": "I P",
    "NDA": "N D A", "SLA": "S L A", "SOW": "S O W", "RFP": "R F P", "POC": "P O C", "MVP": "M V P",
    "GDPR": "G D P R", "CCPA": "C C P A", "TCPA": "T C P A", "DNC": "D N C", "IPO": "I P O", "VC": "V C",
    "FAQ": "F A Q", "ETA": "E T A", "FYI": "F Y I", "ASAP": "A S A P", "Q&A": "Q and A",
    "R&D": "R and D", "M&A": "M and A", "P&L": "P and L", "24x7": "twenty four seven", "24/7": "twenty four seven",
    "APAC": "ay-pack", "EMEA": "eh-mee-uh", "ANZ": "A N Z", "GCC": "G C C", "UK": "U K", "USA": "U S A",
    "MSME": "M S M E", "AB7": "A B seven", "DAK IT Hub": "Dak I T Hub", "SPAN": "Span",
    "MetricFox": "Metric Fox", "HubSpot": "Hub Spot", "LinkedIn": "Linked In", "ChampBeam": "Champ Beam",
    "deependhq.com": "deep end H Q dot com", "ffmpeg": "ff-mpeg", "GSAP": "jee-sap",
}

_UNSAFE = re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z0-9&/.]*[A-Z][A-Za-z0-9&/.]*[A-Z0-9][A-Za-z0-9&/.]*|[A-Za-z0-9&/.]*[0-9][A-Za-z0-9&/.]*)(?![A-Za-z0-9])")


def respell(text):
    for key in sorted(LEXICON, key=len, reverse=True):  # longest first so "Lake B2B" beats "B2B"
        # plural "KPIs" -> "K P I's": the apostrophe is what makes voices say "eyes", not "iss"
        text = re.sub(r"(?<![A-Za-z0-9])" + re.escape(key) + r"(s?)(?![A-Za-z0-9])",
                      lambda m: LEXICON[key] + ("'s" if m.group(1) else ""), text)
    return text


def unsafe_tokens(text):
    """Tokens with two or more capitals, or any digit, that the lexicon did not resolve."""
    return sorted({t.strip(".") for t in _UNSAFE.findall(respell(text)) if t.strip(".")})


def _self_test():
    assert respell("SEO for B2B CMOs.") == "S E O for B to B C M O's."
    assert respell("Lake B2B and LakeB2B") == "Lake B to B and Lake B to B"
    assert respell("Visit deependhq.com, Q&A at 24/7.") == "Visit deep end H Q dot com, Q and A at twenty four seven."
    assert respell("The CEO is it.") == "The C E O is it."  # lowercase words untouched
    assert unsafe_tokens("SEO is fine, XYZQ is not, 2026 is not, $1.9T is not") == ["1.9T", "2026", "XYZQ"]
    assert unsafe_tokens("Plain sentence with One Capital.") == []
    print("self-test ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--self-test"]:
        _self_test()
        sys.exit(0)
    check = "--check" in args
    paths = [a for a in args if a != "--check"]
    if len(paths) != 1:
        sys.exit(__doc__)
    src = sys.stdin.read() if paths[0] == "-" else open(paths[0], encoding="utf-8").read()
    if check:
        bad = unsafe_tokens(src)
        if bad:
            print("Unsafe for TTS, respell or write out:", ", ".join(bad))
            sys.exit(1)
        print("tts-safe: ok")
    else:
        sys.stdout.write(respell(src))
