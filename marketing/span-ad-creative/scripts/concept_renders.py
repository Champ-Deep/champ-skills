"""Generate SPAN Thanksgiving concept renders via Higgsfield GPT Image 2.5, then composite the real SPAN logo.
Usage: python3 gen.py [concept filter]  (writes out/<concept>-<format>.png and out/log.json)
"""
import json, re, subprocess, sys, os, concurrent.futures as cf, urllib.request
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
LOGO = "~/.hermes/cache/scratch/span-logo.png"

STYLE = ("Flat, premium B2B advertising graphic, exact brand colours: dark navy #0F2B3C, SPAN green #1B6B3A, "
         "light green #3DBE6E, amber #F5A623, off white #F5F7F9. Headline in a bold geometric sans serif like Montserrat, "
         "body in a clean sans serif like Inter. Spell every word exactly as written. Use no hyphens, no dashes, no extra words. "
         "Leave the bottom left corner empty for a logo.")

CONCEPTS = {
  "A-thank-you": {
    "visual": "Overhead editorial still life photo: a folded cream thank you card on an off white linen tablecloth, "
              "a small round SPAN green wax seal with a white check mark, two amber autumn leaves, one soft window light from the left, shallow depth of field.",
    "ground": "off white #F5F7F9 ground, dark text #1E2A32, SPAN green headline #1B6B3A",
    "h": "Thank you for a great year.",
    "s": "Before January, let us check your list. Free, for existing clients.",
    "cta": "Claim your free list check",
    "cta_style": "solid SPAN green #1B6B3A rectangular button with white text",
  },
  "B-no-leftovers": {
    "visual": "Overhead photo: one clean white dinner plate on a deep navy #0F2B3C tablecloth, a single bright green #3DBE6E check mark "
              "sits in the centre of the plate like a garnish, a folded amber linen napkin beside it, one hard light source, crisp shadow.",
    "ground": "dark navy #0F2B3C ground, white text",
    "h": "Leave the bounces with the leftovers.",
    "s": "Free list check from a vertical data specialist.",
    "cta": "Check my list free",
    "cta_style": "solid light green #3DBE6E rectangular button with dark navy text",
  },
  "C-count": {
    "visual": "Typographic poster, SPAN green gradient #1B6B3A to #2D9B55 ground, an autumn leaf drawn only from small amber #F5A623 "
              "tally dots like a data plot, placed to the right of the text, generous white space.",
    "ground": "SPAN green gradient ground, white text",
    "h": "Count your blessings. We count your market.",
    "s": "Free technology count for your vertical: Healthcare, Cybersecurity, Legal Tech.",
    "cta": "Get my count",
    "cta_style": "solid amber #F5A623 rectangular button with dark navy text",
  },
}

FORMATS = {
  "social-4x5":  ("4:5",  "LinkedIn feed ad 1080 by 1350. Visual fills the top sixty percent, text block below it on the {ground}."),
  "web-21x9":    ("21:9", "Website hero banner, wide. Visual on the left forty percent, text block on the right on the {ground}, vertically centred."),
  "display-5x4": ("5:4",  "Small display ad 300 by 250, tight: headline, one line subline and the button only, small visual detail in a corner, on the {ground}."),
}

# Typographic concept: no photo region, or the model invents a scene to fill it.
TYPO_LAYOUT = {
  "social-4x5": "LinkedIn feed ad 1080 by 1350, text led. Headline, subline and button left aligned in the top two thirds on the {ground}. The dotted leaf sits alone in the lower right, never touching any text.",
  "web-21x9":   "Website hero banner, wide, text led. Headline, subline and button left aligned inside the left sixty percent on the {ground}. The dotted leaf sits alone inside the right twenty five percent, never touching any text.",
}

def prompt(c, f):
    cc, (ratio, layout) = CONCEPTS[c], FORMATS[f]
    if c == "C-count" and f in TYPO_LAYOUT:
        layout = TYPO_LAYOUT[f]
    txt = (f'Headline text exactly: "{cc["h"]}" Subline text exactly: "{cc["s"]}" '
           f'Button text exactly: "{cc["cta"]}", {cc["cta_style"]}.')
    return ratio, " ".join([layout.format(ground=cc["ground"]), cc["visual"], txt, STYLE])

def run(c, f):
    ratio, p = prompt(c, f)
    cmd = ["higgsfield", "generate", "create", "gpt_image_2_5", "--prompt", p, "--aspect_ratio", ratio,
           "--quality", "medium", "--resolution", "1k", "--wait", "--wait-timeout", "15m", "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    urls = re.findall(r'https?://[^"\s]+?\.(?:png|jpe?g|webp)[^"\s]*', r.stdout)
    rec = {"concept": c, "format": f, "ratio": ratio, "prompt": p, "rc": r.returncode, "urls": urls, "err": r.stderr[-400:]}
    if urls:
        path = os.path.join(OUT, f"{c}-{f}.png")
        urllib.request.urlretrieve(urls[0], path)
        rec["file"] = path
    return rec

def white_logo(h):
    im = Image.open(LOGO).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and abs(r - g) < 8 and abs(g - b) < 8:  # grey wordmark pixels -> white
                px[x, y] = (255, 255, 255, a)
            elif a and r < 20 and 90 < g < 115:  # dark green tagline and overlap diamond: illegible on navy, lift to light green
                px[x, y] = (61, 190, 110, a)
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)

def dark_logo(h):
    im = Image.open(LOGO).convert("RGBA")
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)

def composite(rec):
    """Paste the real logo bottom left. Dark grounds get the white wordmark."""
    im = Image.open(rec["file"]).convert("RGBA")
    pad = round(im.width * 0.045); h = max(28, round(im.height * (0.045 if rec["format"] != "web-21x9" else 0.09)))
    corner = im.crop((pad, im.height - pad - h, pad + 3 * h, im.height - pad)).convert("L")
    dark = sum(corner.getdata()) / (corner.width * corner.height) < 128
    logo = white_logo(h) if dark else dark_logo(h)
    im.alpha_composite(logo, (pad, im.height - pad - h))
    im.convert("RGB").save(rec["file"])
    rec["logo"] = "white" if dark else "dark"

if __name__ == "__main__":
    flt = sys.argv[1] if len(sys.argv) > 1 else ""
    fflt = sys.argv[2] if len(sys.argv) > 2 else ""
    logp = os.path.join(OUT, "log.json")
    old = json.load(open(logp)) if os.path.exists(logp) else []
    if flt == "--recomposite":  # re-download originals and paste the logo again (logo recolour changed)
        for r in old:
            if r.get("file") and fflt in r["concept"]:
                urllib.request.urlretrieve(r["urls"][0], r["file"]); composite(r); print("recomposited", r["file"], r["logo"])
        json.dump(old, open(logp, "w"), indent=1); sys.exit()
    jobs = [(c, f) for c in CONCEPTS for f in FORMATS if flt in c and fflt in f]
    with cf.ThreadPoolExecutor(3) as ex:
        recs = list(ex.map(lambda j: run(*j), jobs))
    for r in recs:
        if r.get("file"):
            composite(r)
    keep = [o for o in old if (o["concept"], o["format"]) not in {(r["concept"], r["format"]) for r in recs}]
    json.dump(keep + recs, open(logp, "w"), indent=1)
    for r in recs:
        print(r["concept"], r["format"], "OK" if r.get("file") else "FAIL", r.get("logo", ""), r["err"] if not r.get("file") else "")
