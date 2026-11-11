#!/usr/bin/env python3
"""python3 probe.py <client_dir>: drives every control of the built page in a real browser and asserts the result.

Needs Playwright with Chromium. Where no browser is available, say so in the handoff: the engine's behaviour was proven
on the sample and only the data changed, but this build's controls were not re-driven.
"""
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright

CD = pathlib.Path(sys.argv[1]).resolve()
D = json.loads((CD / "dist/data.json").read_text())
PAGE = (CD / "dist" / (D["slug"] + ".html")).as_uri()
L, C = D["leads"], D["copy"]
NAMED = [x["co"] for x in L if x.get("named")]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        pg = await (await b.new_context(viewport={'width': 1440, 'height': 900})).new_page()
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        await pg.goto(PAGE, wait_until='networkidle'); await pg.wait_for_timeout(1500)
        await pg.add_style_tag(content='html{scroll-behavior:auto!important}')
        J = pg.evaluate
        has = lambda s: J(f"!!document.querySelector('{s}')")
        view = lambda s: J(f"document.querySelector('{s}').scrollIntoView({{block:'center'}})")
        sel = lambda: J("[...document.querySelectorAll('.ep-card.sel h3')].map(h=>h.textContent)")
        order = lambda: J("[...document.querySelectorAll('#bento .btile')].map(t=>t.dataset.id)")
        note = lambda: pg.inner_text('#back')
        done = []

        if await has('#universe'):  # pinned scroll: one stage per quarter
            top = await J("document.querySelector('#universe').getBoundingClientRect().top+scrollY"); hh = await J("document.querySelector('#universe').offsetHeight-innerHeight"); st = []
            for i in range(4):
                await J(f"scrollTo(0,{top}+{hh}*{(i + .5) / 4})"); await pg.wait_for_timeout(700)
                st.append(await J("[...document.querySelectorAll('#beats li')].findIndex(l=>l.classList.contains('on'))"))
            assert st == [0, 1, 2, 3], st; done.append('universe')

        expect_sel = NAMED
        if await has('#cards'):  # opens on the leads the client named, or empty; holds three; filters
            await view('#leads'); assert sorted(await sel()) == sorted(NAMED), await sel()
            extra = [x for x in L if not x.get("named")][:2]
            for x in extra:
                await pg.click(f".ep-card[data-id='{x['id']}'] .ep-pick")
            s1 = await sel(); assert len(s1) == min(3, len(NAMED) + len(extra)) and extra[-1]["co"] in s1, s1
            await pg.click('#cl'); assert await sel() == []
            if NAMED:
                await pg.click('#rs'); assert sorted(await sel()) == sorted(NAMED)
            else:
                assert not await has('#rs'), 'no shortcut button when the client named nobody'
            if len(D["filters"]) > 1:
                q = D["filters"][1]; want = sum((x.get(q[2]) == q[3]) != bool(q[4] if len(q) > 4 else False) for x in L)
                await pg.click(f"#ldf [data-v='{q[0]}']"); got = await J("[...document.querySelectorAll('.ep-card')].filter(c=>!c.hidden).length"); assert got == want, (q, got, want)
                await pg.click(f"#ldf [data-v='{D['filters'][0][0]}']")
            done.append(f'leads({len(L)}, named {len(NAMED)})')

        if await has('#emrg') and len(D["sends"]) > 1:  # pairing: choosing a copy swaps it with the send that held it
            last = len(D["sends"]) - 1
            act = lambda: J("[...document.querySelectorAll('#orrg .ep-or-row')].map(b=>b.querySelector('.nm b').textContent+' '+b.querySelector('.ac').textContent).join(' | ')")
            await view('#emails'); a0 = await act(); await pg.click(f"#emrg [data-v='{last}']"); m0 = await pg.inner_text('#em-meta')
            await pg.select_option('#em-pair', '0'); m1 = await pg.inner_text('#em-meta'); await pg.click("#emrg [data-v='0']"); m2 = await pg.inner_text('#em-meta')
            assert C["mail"][0]["k"].upper() in m1.upper() and C["mail"][last]["k"].upper() in m2.upper() and m1 != m0, (m0, m1, m2)
            assert 'Copy paired with each send' in await note()
            if await has('#orrg [role=radio]'):
                assert await act() != a0 and 'pairing' in await pg.inner_text('#or-match')
            await pg.click('#em-pair-reset'); assert await act() == a0 and await J("getComputedStyle(document.querySelector('#em-pair-reset')).display") == 'none' and 'Copy paired' not in await note()
            done.append('pairing' + (' with simulation' if await has('#orrg [role=radio]') else ''))

        if await has('#lessons'):
            assert await J("document.querySelectorAll('#lessons article').length") == len(C["lessons"]); done.append(f'lessons({len(C["lessons"])})')

        o0 = None
        if await has('#bento'):  # keyboard swap keeps focus on the handle; mouse drag swaps; one tile per slot
            await view('#bento'); await pg.wait_for_timeout(500); o0 = await order(); assert len(o0) >= 4, 'the bento needs at least four tiles'
            await pg.focus('#bento .bslot:nth-child(1) .grip'); await pg.keyboard.press('ArrowRight'); o1 = await order()
            assert o1[:2] == [o0[1], o0[0]] and o1[2:] == o0[2:], (o0, o1); assert await J("document.activeElement.closest('.btile').dataset.id") == o0[0]
            box = lambda n: J(f"(()=>{{var r=document.querySelector('#bento .bslot:nth-child({n})').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}})()")
            a, c = await box(4), await box(1)
            await pg.mouse.move(a[0], a[1] + 20); await pg.mouse.down(); await pg.mouse.move(a[0] - 40, a[1] - 10, steps=4); await pg.mouse.move(c[0], c[1], steps=12); await pg.mouse.up(); await pg.wait_for_timeout(450)
            o2 = await order(); assert o2[0] == o1[3] and o2[3] == o1[0] and sorted(o2) == sorted(o0), (o1, o2)
            assert await J("[...document.querySelectorAll('#bento .bslot')].every(s=>s.querySelectorAll('.btile').length===1) && !document.querySelector('.btile.drag,.bslot.home')")
            assert 'Where to show up first: 1.' in await note(); done.append('bento')

        tiers = await has('#tierrg')
        await pg.check('#ticks li:nth-child(1) input')
        if tiers:
            await pg.click(f"#tierrg [data-v='{len(C['tiers']) - 1}']")
        await pg.click('#back-copy'); await pg.wait_for_timeout(300); n = await note()
        assert C["ticks_first"] in n and await pg.inner_text('#back-st') and (not tiers or C["tiers"][-1]["t"] in n) and (not NAMED or not await has('#cards') or NAMED[0] in n), n
        await pg.reload(wait_until='networkidle'); await pg.wait_for_timeout(800)  # marks survive a reload
        assert await pg.is_checked('#ticks li:nth-child(1) input') and (not tiers or await J("document.querySelector('#tierrg [aria-checked=true]').dataset.v") == str(len(C['tiers']) - 1))
        if await has('#cards'):
            assert sorted(await sel()) == sorted(expect_sel)
        if o0:
            assert await order() == o2; await pg.click('#bento-reset'); await pg.wait_for_timeout(400); assert await order() == o0 and 'order not changed' in await note()
        done.append('note, copy, reload')

        pg2 = await (await b.new_context(viewport={'width': 1440, 'height': 900})).new_page(); await pg2.goto(PAGE, wait_until='networkidle'); await pg2.wait_for_timeout(600)
        n2 = await pg2.inner_text('#back'); assert 'nothing ticked yet' in n2 and (not tiers or 'not chosen yet' in n2), n2  # a fresh visitor's note claims nothing
        assert await J("[...document.querySelectorAll('a[href^=\"#\"]')].filter(a=>a.target).length") == 0
        print('passed:', ', '.join(done)); print('draft ribbon:', await J("(document.querySelector('.ep-draft')||{}).textContent||'none'")); print('console errors:', errs or 'none')
        assert not errs; await b.close()

asyncio.run(main())
