#!/usr/bin/env python3
"""Showcase page kit: assemble premium scroll pages from core.css + core.js + cases/<id>.html and cases/<id>.json.
Outputs dist/<slug>.html (full standalone doc) and dist/<slug>.artifact.html (fragment for Artifact publish)."""
import base64, json, math, random, re, sys, pathlib
B = pathlib.Path(__file__).parent
CORE_CSS = (B/'core.css').read_text()
CORE_JS = (B/'core.js').read_text()
def logo_uri(path):
    p = pathlib.Path(path); p = p if p.is_absolute() else B/p
    mime = 'image/svg+xml' if p.suffix == '.svg' else 'image/png'
    return f'data:{mime};base64,' + base64.b64encode(p.read_bytes()).decode()
# brand defaults (LakeB2B); override per page in cases/<id>.json
BRAND = {'logo': 'assets/lakeb2b-logo.png', 'logo_reversed': 'assets/lakeb2b-logo-reversed.png', 'logo_alt': 'LakeB2B, Enabling Growth', 'home_url': 'https://www.lakeb2b.com',
         'home_label': 'lakeb2b.com', 'cta_url': 'https://www.lakeb2b.com/contact-us', 'cta_label': 'Book a 20 minute data review',
         'brand_line': 'LakeB2B. Enabling Growth.', 'nav_label': 'Case study'}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..700,0..100,0..1'
         '&family=IBM+Plex+Mono:wght@400;500;600&family=Montserrat:wght@400;500;600;700&display=swap">')

def stars(n=140, seed=7):
    r = random.Random(seed); out = []
    for i in range(n):
        cls = r.choices(['s1','s2','s3'], weights=[5,8,1])[0]
        x = r.uniform(0,100); y = r.uniform(0,100)**1.25/100**0.25
        out.append(f'<i class="{cls}" style="left:{x:.2f}%;top:{y:.2f}%;background:#fff;animation-delay:-{r.uniform(0,6):.2f}s;opacity:{r.uniform(.45,1):.2f}"></i>')
    return '<div class="stars" aria-hidden="true">' + ''.join(out) + '</div>'

def clouds():
    layers = [
        # id, seed, baseFreq, alphaK, alphaB, y, colors(top,bottom), surface
        ('ca', 4, '.0021 .0085', 3.0, -1.20, 40,  ('#B45BC8','#F08AB4'), 8),
        ('cb', 11, '.0026 .0105', 3.3, -1.32, 190, ('#F06E9A','#FFB38A'), 9),
        ('cc', 23, '.0032 .0125', 3.6, -1.42, 330, ('#FFB089','#FFE3C4'), 10),
    ]
    defs = []; rects = []
    for (i, seed, bf, k, b, y, (c1, c2), ss) in layers:
        defs.append(f'''<linearGradient id="g{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<linearGradient id="m{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".38" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="k{i}"><rect x="0" y="{y}" width="1600" height="{600-y}" fill="url(#m{i})"/></mask>
<filter id="f{i}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="{bf}" numOctaves="5" seed="{seed}" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  {k} 0 0 0 {b}" result="a"/>
<feGaussianBlur in="a" stdDeviation="1.4" result="ab"/>
<feDiffuseLighting in="ab" surfaceScale="{ss}" diffuseConstant="1.1" lighting-color="#ffffff" result="lit"><feDistantLight azimuth="255" elevation="42"/></feDiffuseLighting>
<feComposite in="SourceGraphic" in2="lit" operator="arithmetic" k1="0.85" k2="0.32" k3="0" k4="0" result="sh"/>
<feComposite in="sh" in2="ab" operator="in"/>
</filter>''')
        rects.append(f'<rect x="0" y="{y}" width="1600" height="{600-y}" fill="url(#g{i})" filter="url(#f{i})" mask="url(#k{i})"/>')
    return ('<div class="clouds" aria-hidden="true"><svg viewBox="0 0 1600 600" preserveAspectRatio="xMidYMax slice"><defs>'
            + ''.join(defs) + '</defs>' + ''.join(rects) + '</svg></div><div class="glow" aria-hidden="true"></div>')

ARR = '<span class="arr" aria-hidden="true"><i>&#8594;</i><i>&#8594;</i></span>'
def swap(t):
    return f'<span class="swap"><span class="cur">{t}</span><span class="inc" aria-hidden="true">{t}</span></span>'

def nav(chip, short='Book a review', hold=False, b=BRAND):
    LOGO = logo_uri(b['logo']); LOGO_R = logo_uri(b.get('logo_reversed', b['logo']))
    return f'''<div class="progress" aria-hidden="true"><i></i></div>
<header class="nav"><div class="wrap">
<a class="nav-pill" href="{b['home_url']}" target="_blank" rel="noopener" aria-label="Home"><img class="on-dark" src="{LOGO_R}" alt="{b['logo_alt']}" width="180" height="51"><img class="on-light" src="{LOGO}" alt="" aria-hidden="true" width="180" height="51"><span class="sep"></span><span class="lbl">{b['nav_label']}</span></a>
<span class="chip-ind">{chip}</span>{'<span class="hold-pill" role="note">HOLD until 9 Oct</span>' if hold else ''}<span class="sp"></span>
<a class="btn btn-dark mk-glow" href="{b['cta_url']}" target="_blank" rel="noopener"><span class="gl a" aria-hidden="true"></span><span class="gl b" aria-hidden="true"></span><span class="long">{swap(b['cta_label'])}</span><span class="short">{swap(short)}</span>{ARR}</a>
</div></header>'''

def cta(h, p, b=BRAND):
    return f'''<section class="cta-sec"><div class="wrap"><div class="cta" data-reveal>
{stars(60, 3).replace('class="stars"','class="stars"')}
<div><h2 class="display">{h}</h2><p>{p}</p></div>
<div class="acts"><a class="btn btn-light mk-glow" href="{b['cta_url']}" target="_blank" rel="noopener"><span class="gl a" aria-hidden="true"></span><span class="gl b" aria-hidden="true"></span>{swap(b['cta_label'])}{ARR}</a>
<a class="btn btn-ghost mk-shine" href="{b['home_url']}" target="_blank" rel="noopener">{swap(b['home_label'])}</a></div>
</div></div></section>'''

def foot(note, b=BRAND):
    return f'''<footer class="foot"><div class="wrap"><span>{b['brand_line']}</span><span class="mono">{note}</span></div></footer>'''

def sea_map(markets):
    dots = json.load(open(B/'data/sea_dots.json'))
    lon0, lat1, s = 93.0, 21.5, 20.0
    X = lambda lon: (lon-lon0)*s
    Y = lambda lat: (lat1-lat)*s
    parts = []
    for lon, lat, c in dots:
        cls = 'dot t' if c in ('PH','MY','SG','ID') else 'dot'
        parts.append(f'<circle class="{cls}" cx="{X(lon):.1f}" cy="{Y(lat):.1f}" r="3.3"/>')
    vmax = max(m['v'] for m in markets); rmax = 46
    bubs = []
    for i, m in enumerate(markets):
        cx, cy = X(m['lon']), Y(m['lat']); r = rmax*math.sqrt(m['v']/vmax)
        lx, ly, anchor = m['label']
        lx, ly = X(lx), Y(ly)
        lead = ''
        if m.get('leader'):
            lead = f'<path class="lead" d="M{cx:.1f},{cy:.1f} L{lx + (-6 if anchor=="start" else 6):.1f},{ly-10:.1f}"/>'
        bubs.append(f'''<g class="bub" style="--d:{300+i*220}">{lead}<circle class="ring" cx="{cx:.1f}" cy="{cy:.1f}" r="{r+6:.1f}"/><circle class="core" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}"/>
<text class="v" x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="30" paint-order="stroke" stroke="#fff" stroke-width="6" stroke-linejoin="round">{m["v"]:,}</text>
<text class="l" x="{lx:.1f}" y="{ly+20:.1f}" text-anchor="{anchor}" font-size="13" paint-order="stroke" stroke="#fff" stroke-width="5" stroke-linejoin="round">{m["name"]}</text></g>''')
    W, H = (128-93)*s, (21.5+11)*s
    return (f'<svg viewBox="0 30 {W:.0f} {H-60:.0f}" role="img" aria-label="Dot map of Southeast Asia with qualified contacts by market">'
            + ''.join(parts) + ''.join(bubs) + '</svg>')

def tiles(rows):
    rows = sorted(rows, key=lambda r: -r[2])
    mx = math.log10(max(r[2] for r in rows)+1)
    def mix(a, b, t):
        a = [int(a[i:i+2],16) for i in (1,3,5)]; b = [int(b[i:i+2],16) for i in (1,3,5)]
        return '#%02x%02x%02x' % tuple(round(x*(1-t)+y*t) for x, y in zip(a, b))
    out = []
    for i, (seg, worked, mapped) in enumerate(rows):
        t = math.log10(mapped+1)/mx
        bg = mix('#EFE7F6', '#5A06A0', t**1.4); fg = '#FFFFFF' if t**1.4 > .45 else '#1A1230'
        thin = ' thin' if worked <= 5 else ''
        out.append(f'<div class="tile{thin}" style="--bg:{bg};--fg:{fg};--d:{i*28}" title="{seg}: {worked} worked, {mapped:,} mapped">'
                   f'<span class="seg">{seg}</span><span class="m">{mapped:,}</span><span class="wk">{worked} worked</span></div>')
    return '<div class="tiles" role="img" aria-label="38 target accounts: decision makers mapped versus contacts worked">' + ''.join(out) + '</div>'

def build(case):
    meta = json.loads((B/f'cases/{case}.json').read_text())
    b = {**BRAND, **meta.get('brand', {})}
    body = (B/f'cases/{case}.html').read_text()
    repl = {
        '{{NAV}}': nav(meta['chip'], meta.get('short','Book a review'), meta.get('hold', False), b),
        '{{STARS}}': stars(), '{{CLOUDS}}': clouds(),
        '{{CTA}}': cta(meta['cta_h'], meta['cta_p'], b),
        '{{FOOT}}': foot(meta['foot'], b),
        '{{HOLD}}': '',
    }
    if 'map' in meta: repl['{{MAP}}'] = sea_map(meta['map'])
    if 'tiles' in meta: repl['{{TILES}}'] = tiles(meta['tiles'])
    for k, v in repl.items(): body = body.replace(k, v)
    assert '{{' not in body, re.findall(r'\{\{\w+\}\}', body)
    title = meta['title']
    head = f'<title>{title}</title>\n<meta name="description" content="{meta["desc"]}">\n{FONTS}\n<style>\n{CORE_CSS}\n{meta.get("css","")}\n</style>\n'
    frag = head + body + f'\n<script>\n{CORE_JS}\n</script>\n'
    full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + body + f'\n<script>\n{CORE_JS}\n</script>\n</body>\n</html>\n')
    out = B/'dist'; out.mkdir(exist_ok=True)
    (out/f'{meta["slug"]}.html').write_text(full)
    (out/f'{meta["slug"]}.artifact.html').write_text(frag)
    for f in (full,):
        n = len(re.findall('[\\u2013\\u2014]', f))
        print(meta['slug'], 'bytes', len(full), 'dashes', n)
        if n: sys.exit('DASH FOUND')

if __name__ == '__main__':
    for c in sys.argv[1:]: build(c)
