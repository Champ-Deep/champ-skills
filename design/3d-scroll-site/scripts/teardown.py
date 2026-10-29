#!/usr/bin/env python3
"""Motion teardown of reference sites: libraries in use, running animations, canvas/WebGL, pinned elements,
and a scroll sweep contact sheet per site. Usage: teardown.py out_dir url [url...]"""
import sys, json, re, os, time
from playwright.sync_api import sync_playwright
from PIL import Image

out = sys.argv[1]; urls = sys.argv[2:]; os.makedirs(out, exist_ok=True)
LIBS = ["gsap", "scrolltrigger", "lenis", "three", "webgl", "rive", "spline", "lottie", "framer", "webflow",
        "locomotive", "swiper", "splitting", "split-type", "matter.js", "pixi", "canvas", "video", "<model-viewer"]
PROBE = """() => {
  const anims = document.getAnimations ? document.getAnimations().length : -1;
  const sticky = [...document.querySelectorAll('*')].filter(e => { const p = getComputedStyle(e).position; return p === 'sticky' || p === 'fixed'; }).length;
  const canvases = [...document.querySelectorAll('canvas')].map(c => ({w: c.width, h: c.height, gl: !!(c.getContext && (c.getContext('webgl2') || c.getContext('webgl')))}));
  const videos = document.querySelectorAll('video').length;
  const t3d = [...document.querySelectorAll('*')].filter(e => /matrix3d|perspective/.test(getComputedStyle(e).transform + getComputedStyle(e).perspective)).length;
  const fonts = [...new Set([...document.querySelectorAll('h1,h2,p')].map(e => getComputedStyle(e).fontFamily.split(',')[0]))].slice(0,4);
  const bg = getComputedStyle(document.body).backgroundColor;
  const h = document.documentElement.scrollHeight;
  return {anims, sticky, canvases, videos, t3d, fonts, bg, h, vh: innerHeight};
}"""
report = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for u in urls:
        name = re.sub(r"\W+", "-", u.split("//")[1]).strip("-")
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, user_agent="Mozilla/5.0 (Macintosh) Chrome/124")
        pg = ctx.new_page(); srcs = set()
        pg.on("request", lambda r: srcs.add(r.url))
        try:
            pg.goto(u, wait_until="networkidle", timeout=60000)
        except Exception as e:
            pg.goto(u, wait_until="load", timeout=60000)
        time.sleep(3)
        html = pg.content().lower()
        blob = html + "\n" + "\n".join(srcs).lower()
        libs = [l for l in LIBS if l in blob]
        frames = []
        probe0 = pg.evaluate(PROBE)
        H = probe0["h"]; vh = probe0["vh"]
        for i, f in enumerate([0, .1, .2, .3, .4, .5, .6, .7, .8, 1.0]):
            pg.evaluate(f"window.scrollTo(0, {f} * (document.documentElement.scrollHeight - innerHeight))")
            time.sleep(1.2)
            fp = f"{out}/{name}-{i:02d}.png"; pg.screenshot(path=fp); frames.append(fp)
        probe = pg.evaluate(PROBE)
        # contact sheet 5 x 2
        ims = [Image.open(f).resize((480, 300)) for f in frames]
        sheet = Image.new("RGB", (480 * 5, 300 * 2), "white")
        for i, im in enumerate(ims): sheet.paste(im, ((i % 5) * 480, (i // 5) * 300))
        sheet.save(f"{out}/{name}-sheet.png")
        report[u] = {"libs": libs, "scrollHeight": H, "screens": round(H / vh, 1), "probe_top": probe0, "probe_end": probe,
                     "script_hosts": sorted({re.sub(r"https?://([^/]+).*", r"\1", s) for s in srcs if s.endswith(".js")})[:8]}
        ctx.close()
    b.close()
json.dump(report, open(f"{out}/teardown.json", "w"), indent=1)
for u, r in report.items():
    print(f"\n## {u}\n  libs: {r['libs']}\n  height: {r['scrollHeight']}px = {r['screens']} screens; anims top/end {r['probe_top']['anims']}/{r['probe_end']['anims']}; sticky/fixed {r['probe_top']['sticky']}; canvas {r['probe_top']['canvases']}; video {r['probe_top']['videos']}; 3d-transformed els {r['probe_end']['t3d']}; fonts {r['probe_top']['fonts']}; bg {r['probe_top']['bg']}")
