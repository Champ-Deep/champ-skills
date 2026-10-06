#!/usr/bin/env python3
"""Render a built page: screenshots (static full page + motion viewport), console errors, overflow check, PNG 2x and PDF exports."""
import asyncio, sys, pathlib
from playwright.async_api import async_playwright
B = pathlib.Path(__file__).parent

async def run(slug, export=False):
    f = (B/'dist'/f'{slug}.html').resolve()
    shots = B/'shots'; shots.mkdir(exist_ok=True)
    exp = B/'export'; exp.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        errs = []
        for w, h in [(1440, 900), (390, 844)]:
            ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
            pg = await ctx.new_page()
            pg.on('console', lambda m: m.type in ('error', 'warning') and errs.append(f'{w} {m.type}: {m.text}'))
            pg.on('pageerror', lambda e: errs.append(f'{w} pageerror: {e}'))
            # motion mode: first viewport after load animation
            await pg.goto(f.as_uri(), wait_until='networkidle')
            await pg.wait_for_timeout(2600)
            await pg.screenshot(path=str(shots/f'{slug}-{w}-motion-top.png'))
            # scroll through so observers fire, then capture mid-page viewport
            H = await pg.evaluate('document.documentElement.scrollHeight')
            for y in range(0, H, 300):
                await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(60)
            ow = await pg.evaluate('document.documentElement.scrollWidth - innerWidth')
            print(slug, w, 'height', H, 'h-overflow px', ow)
            # small tap targets
            small = await pg.evaluate('''[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.height<44)}).map(e=>e.textContent.trim().slice(0,30)+':'+Math.round(e.getBoundingClientRect().height))''')
            if w == 390: print('  small targets:', small)
            # static full page
            await pg.goto(f.as_uri() + '?static=1', wait_until='networkidle')
            await pg.wait_for_timeout(600)
            await pg.screenshot(path=str(shots/f'{slug}-{w}-static.png'), full_page=True)
            await ctx.close()
        if export:
            ctx = await b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
            pg = await ctx.new_page()
            await pg.goto(f.as_uri() + '?static=1', wait_until='networkidle'); await pg.wait_for_timeout(800)
            await pg.screenshot(path=str(exp/f'{slug}.png'), full_page=True)
            # flatten the hero atmosphere (SVG filters + stars) into one JPEG so the PDF stays small
            await pg.add_style_tag(content='.nav,.hero-inner,.floaters{visibility:hidden!important}')
            hero = await pg.query_selector('.hero')
            jpg = await hero.screenshot(type='jpeg', quality=86)
            import base64
            uri = 'data:image/jpeg;base64,' + base64.b64encode(jpg).decode()
            await pg.add_style_tag(content='.nav,.hero-inner,.floaters{visibility:visible!important}'
                                   '.hero{background:url(' + uri + ') center/100% 100% no-repeat!important}'
                                   '.hero .stars,.hero .clouds,.hero .glow{display:none!important}.hero::after{display:none!important}')
            await pg.wait_for_timeout(300)
            H = await pg.evaluate('document.documentElement.scrollHeight')
            await pg.emulate_media(media='screen')
            await pg.pdf(path=str(exp/f'{slug}.pdf'), width='1440px', height=f'{H+2}px', print_background=True,
                         margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}, page_ranges='1')
            print('  exported png+pdf, height', H)
            await ctx.close()
        await b.close()
        print('  console errors/warnings:', errs or 'none')

if __name__ == '__main__':
    asyncio.run(run(sys.argv[1], export='--export' in sys.argv))
