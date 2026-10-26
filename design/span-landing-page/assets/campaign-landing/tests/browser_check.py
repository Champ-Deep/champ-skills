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
import re
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
        !e.closest('.skip') && !e.parentElement.closest('.sheet__scroll') && (r.left < -1 || r.right > innerWidth+1);
    }).map(e=>({tag:e.tagName,id:e.id,cls:e.className,left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right}))''')


def no_overlap(page):
    return page.evaluate('''() => [...document.querySelectorAll('.board')].every(b=>{
      const rr=[...b.querySelectorAll('.wg')].map(e=>e.getBoundingClientRect());
      return rr.every((a,i)=>rr.every((c,j)=>i===j || a.right<=c.left+1 || c.right<=a.left+1 || a.bottom<=c.top+1 || c.bottom<=a.top+1));
    })''')


def board_state(page, side):
    return page.locator('.board[data-side="'+side+'"] .wg').evaluate_all('(els)=>els.map(e=>[e.dataset.id,e.dataset.x,e.dataset.y])')


def settle_boards(page):
    # Wait through resize debounce, stable heights and live tile transforms, not an arbitrary sleep.
    page.evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
    page.evaluate('window.__boardProbe={last:null,since:performance.now()}')
    page.wait_for_function('''() => {
      const boards=[...document.querySelectorAll('.board')];
      const state=JSON.stringify(boards.map(b=>[b.getBoundingClientRect().height,
        ...[...b.querySelectorAll('.wg')].map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})]));
      const p=window.__boardProbe, now=performance.now();
      if(p.last!==state){p.last=state;p.since=now;return false;}
      return now-p.since>=160 && boards.every(b=>!b.querySelector('.held') &&
        [...b.querySelectorAll('.wg')].every(e=>{
          const r=e.getBoundingClientRect(), br=b.getBoundingClientRect();
          return r.left>=br.left-1 && r.right<=br.right+1 && r.bottom<=br.bottom+1 &&
            e.getAnimations().every(a=>a.playState==='finished') &&
            [...b.querySelectorAll('.wg')].every(other=>{
              const o=other.getBoundingClientRect();
              return e===other || r.right<=o.left+1 || o.right<=r.left+1 || r.bottom<=o.top+1 || o.bottom<=r.top+1;
            });
        }));
    }''', timeout=2000, polling='raf')


def widget_checks(page, i):
    widget = page.locator(f'#pane{i} [data-widget]')
    nodes = widget.locator('[data-node]')
    nodes.first.click()
    expect(widget).to_have_attribute('data-selected','0')
    nodes.nth(1).focus()
    expect(nodes.nth(1)).to_have_class(re.compile(r'.*is-active.*'))
    nodes.nth(1).press('Enter')
    expect(widget).to_have_attribute('data-selected','1')
    if i == 1:
        expect(widget.locator('[data-wire="1"]')).to_have_class('is-active')
        expect(widget).to_have_class(re.compile(r'.*is-pulsing.*'))
    elif i == 2:
        expect(widget).to_have_class(re.compile(r'.*is-exploring.*'))
        arc = widget.locator('.orbit__arc')
        page.locator('#tab2').focus(); page.mouse.move(0,0)
        check(arc.evaluate('e=>getComputedStyle(e).animationName')=='none', 'reduced-motion arc has no animation without hover or focus')
        before = arc.evaluate('e=>getComputedStyle(e).transform')
        page.wait_for_timeout(300)
        check(before == arc.evaluate('e=>getComputedStyle(e).transform'), 'reduced-motion arc snapshots identical at 300ms')
    elif i == 3:
        expect(nodes.nth(1)).to_have_attribute('aria-expanded','true')
    elif i == 4:
        expect(widget.locator('.record__row.is-active')).to_have_count(1)
    elif i == 5:
        expect(widget).to_have_attribute('data-step','2')
        nodes.nth(2).press('Enter')
        expect(widget).to_have_attribute('data-step','3')
        widget.locator('.widget__reset').click()
        expect(widget).to_have_attribute('data-step','0')
    check(True, f'FAQ {i} pointer and keyboard change widget state')


def orbit_checks(page, width, out, evidence):
    check(page.locator('.sample-record').evaluate('e=>Math.abs(e.getBoundingClientRect().left-document.querySelector("#hl").getBoundingClientRect().left)<1'), f'{width} hero card flush with headline')
    check(page.locator('.sample-record__pills span').evaluate_all('els=>els.every(e=>e.getBoundingClientRect().top===els[0].getBoundingClientRect().top && Math.abs(e.getBoundingClientRect().width-els[0].getBoundingClientRect().width)<1)'), f'{width} four equal pills in one row')
    check(page.locator('.hero__copy').evaluate('''e=>{
        const lede=e.querySelector('.hero__lede').getBoundingClientRect(),card=e.querySelector('.sample-record').getBoundingClientRect(),pills=e.querySelector('.sample-record__pills').getBoundingClientRect(),callout=e.querySelector('.buy').getBoundingClientRect();
        return Math.abs(card.top-lede.bottom-24)<1 && Math.abs(pills.top-card.bottom-16)<1 && Math.abs(callout.top-pills.bottom-32)<1;
    }'''), 'hero 24/16/32 vertical rhythm')
    check(page.locator('.ot-node').count()==4 and page.locator('#picker').count()==0, 'four orbit nodes, no MSP picker')
    page.locator('.ot-root').scroll_into_view_if_needed()
    check(page.locator('.ot-root').evaluate('''root=>[...root.querySelectorAll('.ot-node')].every((node,i)=>{
        const n=node.getBoundingClientRect(),o=root.querySelectorAll('.ot-orbit')[i].getBoundingClientRect();
        return Math.abs(Math.hypot(n.x+n.width/2-o.x-o.width/2,n.y+n.height/2-o.y-o.height/2)-o.width/2)<2;
    })'''), 'orbit nodes within 2px of their radii')
    before=page.locator('.ot-node').evaluate_all('els=>els.map(e=>e.style.transform)')
    record=page.locator('.sample-record__panel.is-current').inner_text()
    page.wait_for_timeout(300)
    check(before==page.locator('.ot-node').evaluate_all('els=>els.map(e=>e.style.transform)'), 'reduced-motion rotation frozen after 300ms')
    check(page.locator('.ot-core,.ot-blob').evaluate_all('els=>els.every(e=>getComputedStyle(e).animationName==="none")'), 'reduced-motion core and blobs frozen')
    check(page.locator('.ot-emit').evaluate_all('els=>els.every(e=>getComputedStyle(e).display==="none")'), 'reduced-motion emitters hidden')
    if width in (390,1440):
        page.locator('#market').screenshot(path=str(out/f'msp-{width}-orbit-idle.png'),style='.bar,.sticky{visibility:hidden!important}')
        evidence['screenshots'].append(str(out/f'msp-{width}-orbit-idle.png'))
    data=json.loads((ROOT/'examples/span-msp-us/site.json').read_text())['orbit']['items']
    for i in range(4):
        button=page.locator('.ot-node').nth(i)
        expected=data[i]['formValue']
        button.click()
        expect(page.locator('.ot-card')).to_have_attribute('aria-hidden','false')
        expect(page.locator('.ot-card-title')).to_have_text(data[i]['title'])
        check(not geometry(page), f'{width} orbit open {i} geometry')
        if width==390:
            check(page.locator('.ot-card').evaluate('e=>Math.abs(e.parentElement.getBoundingClientRect().bottom-e.getBoundingClientRect().bottom-12)<1'), 'narrow orbit card docked 12px from bottom')
        if i==0 and width in (390,1440):
            page.locator('#market').screenshot(path=str(out/f'msp-{width}-orbit-open.png'),style='.bar,.sticky{visibility:hidden!important}')
            evidence['screenshots'].append(str(out/f'msp-{width}-orbit-open.png'))
        page.locator('.ot-use').click()
        expect(page.locator('#segment')).to_have_value(expected)
        expect(page.locator('.ot-card')).to_have_attribute('aria-hidden','true')
        expect(page.locator('#provider' if expected=='Custom list' else '#segment')).to_be_focused()
        check(page.locator('#segment').evaluate('e=>{const r=e.getBoundingClientRect();return r.top>=0 && r.bottom<=innerHeight}'), 'segment handoff scrolls to form')
        button.focus();button.press('Enter');page.locator('.ot-use').press('Enter')
        expect(page.locator('#segment')).to_have_value(expected)
        check(page.locator('#providerWrap').is_visible()==(expected=='Custom list'), 'orbit custom field sync')
    page.locator('.ot-year').first.click()
    page.keyboard.press('ArrowRight');expect(page.locator('.ot-card-title')).to_have_text(data[1]['title'])
    page.keyboard.press('ArrowLeft');expect(page.locator('.ot-card-title')).to_have_text(data[0]['title'])
    page.locator('.ot-prev').click();expect(page.locator('.ot-card-title')).to_have_text(data[3]['title'])
    page.locator('.ot-next').click();expect(page.locator('.ot-card-title')).to_have_text(data[0]['title'])
    page.keyboard.press('Escape');expect(page.locator('.ot-card')).to_have_attribute('aria-hidden','true')
    expect(page.locator('.ot-node').first).to_be_focused()
    check(record==page.locator('.sample-record__panel.is-current').inner_text(), 'reduced-motion record static throughout interactions')
    page.locator('.sheet__unlock a').click()
    page.wait_for_function('location.hash==="#form" && document.querySelector("#form").getBoundingClientRect().top>=-1 && document.querySelector("#form").getBoundingClientRect().top<innerHeight')
    check(True, 'sample unlock scrolls to form within subpixel rounding')


def animated_orbit_checks(page):
    page.wait_for_timeout(2000);page.mouse.move(0,0)
    before=page.locator('.ot-node').evaluate_all('els=>els.map(e=>e.style.transform)')
    page.wait_for_timeout(300)
    check(before!=page.locator('.ot-node').evaluate_all('els=>els.map(e=>e.style.transform)'), 'orbit rotation advances over 300ms')
    page.locator('.ot-year').first.hover()
    before=page.locator('.ot-node').evaluate_all('els=>els.map(e=>e.style.transform)')
    page.wait_for_timeout(300)
    check(before==page.locator('.ot-node').evaluate_all('els=>els.map(e=>e.style.transform)'), 'orbit hover pauses rotation')
    page.locator('.ot-year').first.click();page.mouse.move(0,0)
    before=page.locator('.ot-node').evaluate_all('els=>els.map(e=>e.style.transform)')
    page.wait_for_timeout(300)
    check(before==page.locator('.ot-node').evaluate_all('els=>els.map(e=>e.style.transform)'), 'orbit selection pauses rotation')
    page.keyboard.press('Escape')
    current=page.locator('.sample-record__panel.is-current').inner_text()
    page.wait_for_function('(previous)=>document.querySelector(".sample-record__panel.is-current").innerText!==previous',arg=current,timeout=5000)
    check(True, 'record rotates within the 4-second interval')
    page.locator('.sample-record__pause').click()
    current=page.locator('.sample-record__panel.is-current').inner_text()
    page.wait_for_timeout(4100)
    check(current==page.locator('.sample-record__panel.is-current').inner_text(), 'record pause preserves accessible reading state')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    for name in ('span-msp-us', 'span-peo-eor'):
        subprocess.run([sys.executable, str(ROOT/'build.py'), str(ROOT/'examples'/name), '--out', str(out/(name+'.html'))], check=True)
    fixture = out/'mixed-fixture'
    fixture.mkdir(exist_ok=True)
    mixed = json.loads((ROOT/'examples/span-msp-us/site.json').read_text())
    mixed['compare'] = json.loads((ROOT/'examples/span-peo-eor/site.json').read_text())['compare']
    mixed['picker'] = {'title':'Pick your list','hint':'Choose a list','items':[dict(item,size='wide') for item in mixed['orbit']['items']]}
    (fixture/'site.json').write_text(json.dumps(mixed))
    (fixture/'logo.png').write_bytes((ROOT/'examples/span-msp-us/logo.png').read_bytes())
    subprocess.run([sys.executable,str(ROOT/'build.py'),str(fixture),'--out',str(out/'mixed-fixture.html')],check=True)
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
            check(page.locator('.band,.clients,.book,.srcs').count()==0, 'unsupported proof sections absent')
            check(page.locator('label[for=segment]').inner_text()=='Requirement', 'requirement label')
            check(page.locator('label[for=provider]').inner_text()=='Custom requirements', 'custom label')
            check(page.locator('label[for=phone]').inner_text()=='Phone (optional)', 'optional phone label')
            check(set(page.locator('#segment option').all_text_contents())=={'MSP contact list','MSSP/cybersecurity list','Cloud MSP list','Custom list','Not sure yet'}, 'source requirement choices')
            expect(page.locator('#previewDisclosure')).to_be_visible()
            check('Illustrative sample layout, not real data' in page.locator('#dossier').inner_text(), 'illustrative caveat')
            check(page.locator('#dossier .ok').count()==0, 'no dummy verification badge')
            check(page.locator('.sample-record__panel.is-current .sample-record__row').count()==5, 'hero masked record fields present')
            check(page.locator('.hero .ticks').count()==0, 'hero tick list replaced')
            check(page.locator('.sheet tbody tr').count()==6, 'six illustrative sample rows')
            orbit_checks(page, width, out, evidence)
            page.locator('#segment').select_option('MSP contact list')
            for i in range(6):
                label = page.locator('.sheet__label').nth(i)
                page.locator('#name').focus()
                label.hover()
                expect(page.locator(f'.sheet td[data-column="{i}"].is-highlighted')).to_have_count(6)
                page.mouse.move(0,0)
                label.focus()
                expect(page.locator(f'.sheet th[data-column="{i}"].is-highlighted')).to_have_count(1)
                expect(page.locator('.sheet td.is-highlighted')).to_have_count(6)
                label.click()
                expect(page.locator(f'.sheet th[data-column="{i}"]')).to_have_attribute('aria-sort','ascending')
                ascending = page.locator('.sheet tbody tr').evaluate_all('els=>els.map(e=>e.dataset.row)')
                label.press('Enter')
                expect(page.locator(f'.sheet th[data-column="{i}"]')).to_have_attribute('aria-sort','descending')
                check(page.locator('.sheet tbody tr').evaluate_all('els=>els.map(e=>e.dataset.row)')==list(reversed(ascending)), 'sort reverses masked records')
                label.press('Tab')
                if i<5:
                    expect(page.locator('.sheet__label').nth(i+1)).to_be_focused()
                    expect(page.locator(f'.sheet td[data-column="{i+1}"].is-highlighted')).to_have_count(6)
            page.locator('#name').focus()
            expect(page.locator('.sheet .is-highlighted')).to_have_count(0)
            page.locator('.sheet__scroll').evaluate('e=>e.scrollLeft=0')
            text=page.locator('body').inner_text()
            check(not any(s in text for s in ('GDPR','CCPA','CAN SPAM','one business day','Not a free batch','name@company.com')), 'no inherited MSP claims')
            page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
            page.screenshot(path=str(out/f'msp-{width}-fold.png'))
            if width in (390,1440):
                for label, selector in [('hero','.hero'),('sample','#sample-layout'),('footer','#hwf')]:
                    # Fixed bars are excluded only from section crops, not fold or geometry checks.
                    page.locator(selector).screenshot(path=str(out/f'msp-{width}-{label}.png'), style='.bar,.sticky{visibility:hidden!important}')
                    evidence['screenshots'].append(str(out/f'msp-{width}-{label}.png'))
                page.locator('.hero__object').screenshot(path=str(out/f'msp-{width}-hero-object.png'), style='.bar,.sticky{visibility:hidden!important}')
            check(not geometry(page), f'{width} element rectangles within viewport: {geometry(page)}')
            initial = page.locator('#dither').evaluate('(c)=>c.toDataURL()')
            page.wait_for_timeout(250)
            check(initial==page.locator('#dither').evaluate('(c)=>c.toDataURL()'), 'reduced-motion dither stable')
            for i in range(1,6):
                page.locator(f'#tab{i}').click()
                expect(page.locator(f'#pane{i}')).to_be_visible()
                expect(page.locator(f'#tab{i}')).to_have_attribute('aria-selected','true')
                check(not geometry(page), f'{width} FAQ {i} geometry')
                check(bool(page.locator(f'#pane{i} .diagram').get_attribute('aria-label')), f'FAQ {i} accessible summary')
                widget_checks(page, i)
                check(not geometry(page), f'{width} FAQ {i} interacted geometry')
                if width in (390,1440):
                    path = out/f'msp-{width}-faq-{i}.png'
                    page.locator(f'#pane{i}').screenshot(path=str(path), style='.bar,.sticky{visibility:hidden!important}')
                    evidence['screenshots'].append(str(path))
            page.locator('#tab1').focus()
            for i in range(2,6):
                page.keyboard.press('ArrowDown')
                expect(page.locator(f'#tab{i}')).to_be_focused()
                expect(page.locator(f'#pane{i}')).to_be_visible()
            for i in range(4,0,-1):
                page.keyboard.press('ArrowUp')
                expect(page.locator(f'#tab{i}')).to_be_focused()
                expect(page.locator(f'#pane{i}')).to_be_visible()
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
        page.goto(base+'/mixed-fixture.html', wait_until='networkidle')
        page.add_style_tag(content='html{scroll-behavior:auto!important}')
        animated_orbit_checks(page)
        settle_boards(page)
        other = {side:board_state(page,side) for side in ('peo','eor')}
        initial = board_state(page,'picker')
        tiles = page.locator('.picker__board .wg')
        tiles.first.press('Alt+ArrowRight')
        settle_boards(page)
        check(board_state(page,'picker')!=initial, 'picker Alt+ArrowRight changes layout')
        check(all(board_state(page,side)==state for side,state in other.items()), 'picker keyboard leaves both count boards unchanged')
        page.locator('#pickerReset').click(); settle_boards(page)
        check(board_state(page,'picker')==initial, 'picker reset restores initial layout')
        tiles.first.scroll_into_view_if_needed()
        a=tiles.first.bounding_box(); b=tiles.nth(1).bounding_box()
        page.mouse.move(a['x']+a['width']/2,a['y']+a['height']/2); page.mouse.down()
        page.mouse.move(b['x']+b['width']/2,b['y']+b['height']/2,steps=20)
        page.wait_for_timeout(150); page.mouse.up(); settle_boards(page)
        check(board_state(page,'picker')!=initial, 'picker pointer drag changes layout')
        check(all(board_state(page,side)==state for side,state in other.items()), 'picker drag leaves both count boards unchanged')
        check(no_overlap(page), 'mixed boards no overlaps after picker drag')
        page.locator('#pickerReset').click(); settle_boards(page)
        check(board_state(page,'picker')==initial, 'picker drag reset restores initial layout')
        for button in page.locator('.picker__board .wg').all():
            requirement=button.get_attribute('data-requirement')
            button.click()
            expect(button).to_have_attribute('aria-pressed','true')
            expect(button.locator('.wg__choose')).to_have_text('Selected')
            expect(page.locator('#segment')).to_have_value(requirement)
            expect(page.locator('#provider' if requirement=='Custom list' else '#segment')).to_be_focused()
            button.focus();button.press('Enter')
            expect(page.locator('#segment')).to_have_value(requirement)
        check(all(board_state(page,side)==state for side,state in other.items()), 'legacy picker click/Enter handoff leaves count-board order unchanged')
        page.locator('#sample-layout').scroll_into_view_if_needed()
        sheet=page.locator('.sheet'); r=sheet.bounding_box()
        page.mouse.move(r['x']+r['width']*.8,r['y']+r['height']*.25)
        check(sheet.evaluate("e=>Math.abs(parseFloat(e.style.getPropertyValue('--ry')))>0 && Math.abs(parseFloat(e.style.getPropertyValue('--ry')))<=4"), 'sheet tilt active and capped at 4 degrees')
        page.mouse.move(0,0)
        check(sheet.evaluate("e=>e.style.getPropertyValue('--rx')==='0deg' && e.style.getPropertyValue('--ry')==='0deg'"), 'sheet spring return target resets')
        page.locator('#tab2').click(); page.locator('.orbit').scroll_into_view_if_needed()
        page.locator('#name').focus(); page.mouse.move(0,0)
        arc=page.locator('.orbit__arc'); before=arc.evaluate('e=>getComputedStyle(e).transform')
        page.wait_for_timeout(300)
        check(before!=arc.evaluate('e=>getComputedStyle(e).transform'), 'normal-motion orbit animates')
        page.locator('.orbit [data-node]').first.hover()
        check(arc.evaluate('e=>getComputedStyle(e).animationPlayState')=='paused', 'orbit pauses on hover')
        page.locator('.orbit [data-node]').nth(1).focus()
        check(arc.evaluate('e=>getComputedStyle(e).animationPlayState')=='paused', 'orbit pauses on keyboard focus')
        check(not errors, 'animated widgets and mixed-board fixture zero console errors')
        page.goto(base+'/span-peo-eor.html', wait_until='networkidle')
        page.add_style_tag(content='html{scroll-behavior:auto!important}')
        check(page.locator('.band').evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(255, 255, 255)', 'PEO white band')
        check(page.locator('.band__n b').first.evaluate('(e)=>getComputedStyle(e).color')=='rgb(27, 107, 58)', 'PEO green figures')
        check(page.locator('.board[data-side=peo] .wg').count()==8 and page.locator('.board[data-side=eor] .wg').count()==8, '16 tiles split 8/8')
        peo = json.loads((ROOT/'examples/span-peo-eor/site.json').read_text())
        check([i['visual'] for i in peo['faq']['items']]==['calls','sources','renewal','sample','roles'], 'legacy visual kinds unchanged')
        for i, item in enumerate(peo['faq']['items'],1):
            page.locator(f'#tab{i}').click()
            expect(page.locator(f'#pane{i}')).to_be_visible()
            expect(page.locator(f'#pane{i} .faq__lead')).to_have_text(item['lead'])
        for side, data in [('peo',peo['compare']['left']),('eor',peo['compare']['right'])]:
            counts = page.locator(f'.board[data-side={side}] .wg__n').all_text_contents()
            check(sum(int(n.replace(',','')) for n in counts)==data['total'], side+' rendered count total unchanged')
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
            page.set_viewport_size({'width':width,'height':1000}); settle_boards(page)
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
