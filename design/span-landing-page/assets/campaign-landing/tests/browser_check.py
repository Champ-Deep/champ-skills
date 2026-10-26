#!/usr/bin/env python3
"""Focused real-browser preview and board regression checks. No lead data leaves the page.
Usage: python browser_check.py --out /absolute/qa-directory
Builds both examples with the adjacent builder and serves them on loopback port 3100+.
"""
import argparse
import functools
import hashlib
import http.server
import json
import subprocess
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://share.lakeb2b.com/f/iZ0AciBa/span-msp-landing-us-preview__1_.html'


def check(condition, label):
    assert condition, label
    print('PASS', label, flush=True)


def geometry(page):
    return page.evaluate('''() => [...document.querySelectorAll('body *')].filter(e => {
      const r=e.getBoundingClientRect(); const s=getComputedStyle(e);
      return r.width && r.height && s.visibility!=='hidden' && s.display!=='none' &&
        !e.closest('.skip') && (r.left < -1 || r.right > innerWidth+1);
    }).map(e=>({tag:e.tagName,id:e.id,cls:e.className,left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right}))''')


def no_overlap(page):
    return page.evaluate('''() => [...document.querySelectorAll('.board')].every(b=>{
      const rr=[...b.querySelectorAll('.wg')].map(e=>e.getBoundingClientRect());
      return rr.every((a,i)=>rr.every((c,j)=>i===j || a.right<=c.left+1 || c.right<=a.left+1 || a.bottom<=c.top+1 || c.bottom<=a.top+1));
    })''')


def board_state(page, side):
    return page.locator('.board[data-side="'+side+'"] .wg').evaluate_all('(els)=>els.map(e=>[e.dataset.id,e.dataset.x,e.dataset.y])')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    for name in ('span-msp-us', 'span-peo-eor'):
        subprocess.run([sys.executable, str(ROOT/'build.py'), str(ROOT/'examples'/name), '--out', str(out/(name+'.html'))], check=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(out))
    for port in range(3100, 3200):
        try:
            server = http.server.ThreadingHTTPServer(('127.0.0.1', port), handler)
            break
        except OSError:
            continue
    else:
        raise RuntimeError('No free QA port in 3100..3199')
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{port}'
    evidence = {'base':base, 'widths':[], 'screenshots':[]}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width in (375, 390, 768, 834, 1440):
            ctx = browser.new_context(viewport={'width':width,'height':900}, reduced_motion='reduce', device_scale_factor=1)
            page = ctx.new_page()
            errors, logs, writes = [], [], []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: (errors.append(m.text) if m.type=='error' else logs.append(m.text)))
            def intercept(route):
                req = route.request
                if req.method != 'GET' or req.resource_type in ('fetch','xhr'):
                    writes.append({'method':req.method,'type':req.resource_type,'url':req.url})
                    route.fulfill(status=204)
                else:
                    route.continue_()
            page.route('**/*', intercept)
            page.add_init_script('window.__gtag=[];window.gtag=(...a)=>window.__gtag.push(a);window.dataLayer=[];')
            page.goto(base+'/span-msp-us.html', wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            page.add_style_tag(content='html{scroll-behavior:auto!important}')
            check(page.title().startswith('MSP Email List'), f'{width} exact artifact')
            check(page.locator('link[rel=canonical]').get_attribute('href')==SOURCE, 'source canonical')
            check('noindex' in page.locator('meta[name=robots]').get_attribute('content'), 'noindex')
            check(page.locator('.band,.clients,.board,.srcs').count()==0, 'unsupported proof sections absent')
            check(page.locator('label[for=segment]').inner_text()=='Requirement', 'requirement label')
            check(page.locator('label[for=provider]').inner_text()=='Custom requirements', 'custom label')
            check(page.locator('label[for=phone]').inner_text()=='Phone (optional)', 'optional phone label')
            check(set(page.locator('#segment option').all_text_contents())=={'MSP contact list','MSSP/cybersecurity list','Cloud MSP list','Custom list','Not sure yet'}, 'source requirement choices')
            expect(page.locator('#previewDisclosure')).to_be_visible()
            check('Illustrative sample layout, not real data' in page.locator('#dossier').inner_text(), 'illustrative caveat')
            check(page.locator('#dossier .ok').count()==0, 'no dummy verification badge')
            text=page.locator('body').inner_text()
            check(not any(s in text for s in ('GDPR','CCPA','CAN SPAM','one business day','Not a free batch','name@company.com')), 'no inherited MSP claims')
            if width in (390,1440):
                page.screenshot(path=str(out/f'msp-{width}-fold.png'))
                for label, selector in [('hero','.hero'),('dossier','#dossier'),('faq','.faqwrap'),('footer','#hwf')]:
                    # Fixed bars are excluded only from section crops, not fold or geometry checks.
                    page.locator(selector).screenshot(path=str(out/f'msp-{width}-{label}.png'), style='.bar,.sticky{visibility:hidden!important}')
                    evidence['screenshots'].append(str(out/f'msp-{width}-{label}.png'))
            check(not geometry(page), f'{width} element rectangles within viewport: {geometry(page)}')
            initial = page.locator('#dither').evaluate('(c)=>c.toDataURL()')
            page.wait_for_timeout(250)
            check(initial==page.locator('#dither').evaluate('(c)=>c.toDataURL()'), 'reduced-motion dither stable')
            for i in range(1,6):
                page.locator(f'#tab{i}').click()
                expect(page.locator(f'#pane{i}')).to_be_visible()
                expect(page.locator(f'#tab{i}')).to_have_attribute('aria-selected','true')
                check(not geometry(page), f'{width} FAQ {i} geometry')
            page.locator('#tab5').press('ArrowDown')
            expect(page.locator('#tab1')).to_be_focused()
            expect(page.locator('#pane1')).to_be_visible()
            page.locator('#tab1').press('ArrowUp')
            expect(page.locator('#tab5')).to_be_focused()
            page.locator('#hwf').scroll_into_view_if_needed()
            page.wait_for_timeout(150)
            check(page.locator('#hwf canvas').evaluate('''c=>{const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let ink=0;for(let i=0;i<d.length;i+=4)if(d[i+1]>65)ink++;return ink>100;}'''), 'footer contains halftone pixels')
            page.locator('#name').fill('Preview Tester')
            page.locator('#consent').check()
            for email in ('preview@gmail.com','preview@outlook.co.uk'):
                page.locator('#email').fill(email)
                page.locator('.submit').click()
                check(page.locator('#email').evaluate('(e)=>e.closest(".field").classList.contains("bad")'), email+' rejected')
                check(page.locator('#form.done').count()==0, 'invalid email not done')
            page.locator('#email').fill('preview@example.org')
            page.locator('#name').fill('')
            page.locator('.submit').click()
            check(page.locator('#name').evaluate('(e)=>e.closest(".field").classList.contains("bad")') and not page.locator('#form.done').count(), 'missing name rejected')
            page.locator('#name').fill('Preview Tester')
            page.locator('#consent').uncheck()
            page.locator('.submit').click()
            check(page.locator('#consentWrap.bad').count()==1 and not page.locator('#form.done').count(), 'missing consent rejected')
            page.locator('#consent').check()
            page.locator('#segment').select_option('Custom list')
            page.locator('.submit').click()
            check(page.locator('#providerWrap.bad').count()==1 and not page.locator('#form.done').count(), 'missing custom requirements rejected')
            expect(page.locator('#providerWrap .err')).to_have_text('Please describe the list you need')
            page.locator('#provider').fill('Cloud MSPs in California')
            page.locator('.submit').click()
            expect(page.locator('#form')).to_have_class('form done')
            page.locator('#segment').select_option('MSP contact list')
            page.locator('.submit').click()
            expect(page.locator('.thanks h2')).to_have_text('Preview only, nothing sent')
            check(page.locator('#phone').input_value()=='' and page.locator('#name').input_value()=='Preview Tester', 'normal submit accepts blank optional phone and preserves inputs')
            check(not writes, f'zero POST/fetch/XHR: {writes}')
            check(page.evaluate('window.__gtag.length===0 && !window.dataLayer.some(e=>e.event==="lead_submit" || e.event==="conversion")'), 'zero lead conversions')
            check(not any('preview@' in m or 'Preview Tester' in m for m in logs), 'no personal payload console logging')
            check(not errors, f'{width} zero console/page errors: {errors}')
            if width in (390,1440):
                page.locator('#form').screenshot(path=str(out/f'msp-{width}-submitted.png'), style='.bar,.sticky{visibility:hidden!important}')
            evidence['widths'].append(width)
            ctx.close()
        ctx=browser.new_context(viewport={'width':1440,'height':1000})
        page=ctx.new_page()
        errors=[]
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type=='error' else None)
        page.goto(base+'/span-peo-eor.html', wait_until='networkidle')
        page.add_style_tag(content='html{scroll-behavior:auto!important}')
        check(page.locator('.band').evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(255, 255, 255)', 'PEO white band')
        check(page.locator('.band__n b').first.evaluate('(e)=>getComputedStyle(e).color')=='rgb(27, 107, 58)', 'PEO green figures')
        check(page.locator('.board[data-side=peo] .wg').count()==8 and page.locator('.board[data-side=eor] .wg').count()==8, '16 tiles split 8/8')
        check(no_overlap(page), 'boards initially no overlap')
        for side, other in [('peo','eor'),('eor','peo')]:
            before=board_state(page,side); untouched=board_state(page,other)
            tile=page.locator(f'.board[data-side={side}] .wg').first
            tile.press('Alt+ArrowRight')
            page.wait_for_timeout(300)
            check(board_state(page,side)!=before and board_state(page,other)==untouched, side+' independent keyboard reorder')
            check(no_overlap(page), side+' keyboard no overlap')
            page.locator('#bentoReset').click()
            page.wait_for_timeout(300)
            check(board_state(page,side)==before, side+' reset')
            tiles=page.locator(f'.board[data-side={side}] .wg')
            tiles.first.scroll_into_view_if_needed()
            a=tiles.first.bounding_box(); b=tiles.nth(3).bounding_box()
            page.mouse.move(a['x']+a['width']/2,a['y']+a['height']/2)
            page.mouse.down()
            page.mouse.move(b['x']+b['width']/2,b['y']+b['height']/2,steps=20)
            page.wait_for_timeout(150)
            page.mouse.up()
            page.wait_for_timeout(700)
            check(board_state(page,side)!=before and board_state(page,other)==untouched, side+' independent pointer reorder')
            check(no_overlap(page), side+' pointer no overlap')
            page.locator('#bentoReset').click()
            page.wait_for_timeout(300)
        tile=page.locator('.board[data-side=peo] .wg').first
        name=tile.locator('.wg__name').inner_text()
        tile.click()
        expect(tile).to_have_attribute('aria-pressed','true')
        check(page.locator('.wg__vs b').count()==15, 'pin populates 15 ratios')
        page.locator('#stripCta').click()
        expect(page.locator('#provider')).to_have_value(name)
        expect(page.locator('#segment')).to_have_value('A specific provider')
        page.locator('#name').fill('Preview Tester'); page.locator('#email').fill('preview@example.org'); page.locator('#consent').check()
        page.locator('.submit').click()
        check(page.locator('#phone').evaluate('(e)=>e.closest(".field").classList.contains("bad")') and not page.locator('#form.done').count(), 'PEO phone remains required')
        page.locator('#phone').fill('2025550100'); page.locator('.submit').click()
        expect(page.locator('.thanks h2')).to_have_text('Preview only, nothing sent')
        for width in (390,834,1440):
            page.set_viewport_size({'width':width,'height':1000}); page.wait_for_timeout(350)
            check(not geometry(page), f'PEO {width} rect overflow: {geometry(page)}')
            check(no_overlap(page), f'PEO {width} no tile overlap')
        check(not errors, f'PEO zero console/page errors: {errors}')
        for key in ('mssp','cloud','partner'):
            page.goto(base+'/span-msp-us.html?hl='+key,wait_until='networkidle')
            site=json.loads((ROOT/'examples/span-msp-us/site.json').read_text())
            expect(page.locator('#hl')).to_have_text(site['headlines']['variants'][key])
        check(not errors, 'headline variants and animated path zero errors')
        browser.close()
    server.shutdown()
    evidence['html_sha256']={n:hashlib.sha256((out/(n+'.html')).read_bytes()).hexdigest() for n in ('span-msp-us','span-peo-eor')}
    (out/'browser-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print('PASS all preview and regression checks',flush=True)


if __name__=='__main__':
    main()
