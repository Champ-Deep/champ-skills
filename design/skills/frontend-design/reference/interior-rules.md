# Interior rules for single-file pages

Source: interior.dev (github.com/ddoemonn/interior, MIT, 54 React + Tailwind + Motion components, about 976 stars when checked 2026-10-15). Its thesis: software feels cheap in the half-second after a click. The components are React, so we do not install them into single-file pages. We port the rules they enforce, plus vanilla ports of the three that earn a place on a showcase or readout page.

## Verdict

Useful, narrowly. Of the 54 components, three matter for our HTML pages: copy button, segmented control, scroll spy. The rest (swipe deck, OTP input, reorder list, hold to confirm, command palette) are app UI and do not belong on a report page. The value is the rule set, not the library.

## The rules

1. **Reserve space for every state.** A button that changes its label must not change its width. Stack all labels in one grid cell and fade between them. Never swap text and let the layout reflow.
2. **Retarget, never restart.** If the user acts again mid-animation, aim the motion at the new target from where it is. Clicks that arrive mid-flight must settle on the last choice with no stuck or half state.
3. **State without motion.** Everything the animation says must also be in text or `aria-*`. Reduced motion removes the transition and keeps the state.
4. **Say success and failure.** A copy or save control needs an explicit error state and a fallback path (`execCommand`), not a silent no-op.
5. **One timer, restarted.** A transient state (Copied) resets after a fixed time, and a second action restarts the timer.
6. **Roving focus for grouped controls.** `role="radiogroup"` with `role="radio"` and `aria-checked`, one tab stop, Arrow keys, Home and End.
7. **Announce changes.** A filter that hides rows writes "Showing 2 of 5" to a polite live region. A copy button writes its result to one.
8. **The reading line travels with scroll.** In scroll spy, a fixed line makes short last sections unreachable. Move the line from the top offset to the viewport bottom as scroll progress goes 0 to 1, and force the last section at the page bottom.
9. **A click holds the highlight.** A clicked nav link stays active until the scroll arrives or the user wheels or touches away. Otherwise it flickers through every section it passes.
10. **Measure the thumb.** After any sliding indicator, assert in the test that the thumb box equals the selected button box, at every breakpoint, after rapid clicks.

## Where these rules apply in our pages

| Element | Rules |
|---|---|
| Copy to clipboard buttons | 1, 3, 4, 5, 7 |
| Filter or tab pills over a table | 2, 3, 6, 7, 10 |
| Side rail and top nav on long pages | 8, 9, plus `aria-current="location"` |
| Any control with a loading or done state | 1, 3, 4 |

## Vanilla ports (proven in the SPAN website update page)

Helpers `$`, `$$` and `reduce` (the reduced-motion flag) are defined by the page shell (`core.js` in the showcase kit).

### CSS

```css
/* ---- interaction craft (ported from interior.dev rules: reserve space, retarget never restart, state without motion) ---- */
.sr-only{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.btn:active{transform:translateY(1px)}
.cb{gap:10px;min-height:48px}
.cb-ico{display:grid;width:14px;height:14px;flex:none}
.cb-ico svg,.cb-lbl>span{grid-area:1/1;transition:opacity .3s cubic-bezier(.2,.8,.2,1),transform .3s cubic-bezier(.2,.8,.2,1),filter .3s}
.cb-ico svg{width:14px;height:14px}
.cb-lbl{display:grid;position:relative}
.cb-lbl>span{white-space:nowrap}
.cb[data-state="idle"] .i-copied,.cb[data-state="idle"] .i-error,
.cb[data-state="copied"] .i-idle,.cb[data-state="copied"] .i-error,
.cb[data-state="error"] .i-idle,.cb[data-state="error"] .i-copied{opacity:0;transform:scale(.9)}
.cb[data-state="idle"] [data-s="copied"],.cb[data-state="idle"] [data-s="error"],
.cb[data-state="copied"] [data-s="idle"],.cb[data-state="copied"] [data-s="error"],
.cb[data-state="error"] [data-s="idle"],.cb[data-state="error"] [data-s="copied"]{opacity:0;transform:translateY(3px);filter:blur(3px)}
.seg{position:relative}
.seg button{display:block;transition:color .2s}
.seg button[role="radio"]:hover{color:var(--ink)}
.seg-thumb{position:absolute;left:0;top:0;z-index:2;overflow:hidden;pointer-events:none;background:var(--sel-bg);border-bottom:3px solid var(--orange);box-sizing:border-box;transition:transform .42s cubic-bezier(.2,.9,.25,1.08),width .42s cubic-bezier(.2,.9,.25,1.08),height .42s cubic-bezier(.2,.9,.25,1.08)}
.seg-inner{position:absolute;left:0;top:0;display:flex;flex-wrap:wrap;padding:4px;box-sizing:border-box;transition:transform .42s cubic-bezier(.2,.9,.25,1.08)}
.seg-inner button{color:var(--sel-fg)!important;cursor:default}
.seg.still .seg-thumb,.seg.still .seg-inner{transition:none}
.seg:has(button:focus-visible) .seg-thumb{outline:2px solid var(--orange);outline-offset:2px}
.rail a[aria-current="location"] span{opacity:1;transform:none}
.rail a[aria-current="location"] i{background:var(--orange);transform:scale(1.5)}
@media (prefers-reduced-motion:reduce){.cb-ico svg,.cb-lbl>span{transition:none;filter:none!important}.seg-thumb,.seg-inner{transition:none}}

```

### Copy button markup

```html
<button class="btn btn-primary cb" type="button" id="copy" data-state="idle" aria-label="Copy text">
  <span class="cb-ico" aria-hidden="true"><svg class="i-idle">...</svg><svg class="i-copied">...</svg><svg class="i-error">...</svg></span>
  <span class="cb-lbl" aria-hidden="true"><span data-s="idle">Copy</span><span data-s="copied">Copied to clipboard</span><span data-s="error">Copy failed</span></span>
  <span class="sr-only" role="status" aria-live="polite"></span>
</button>
```

### Segmented control JS (the onPick callback does the filtering)

```js
  /* segmented radiogroup: the thumb travels, labels recolour under it, keys work, retargeting never restarts */
  function segmented(root,onPick){
    var btns=$$('button[role="radio"]',root),thumb=document.createElement('span'),inner=document.createElement('span');
    thumb.className='seg-thumb';thumb.setAttribute('aria-hidden','true');inner.className='seg-inner';
    btns.forEach(function(b){var c=b.cloneNode(true);c.removeAttribute('role');c.removeAttribute('aria-checked');c.removeAttribute('data-f');c.tabIndex=-1;inner.appendChild(c)});
    thumb.appendChild(inner);root.insertBefore(thumb,root.firstChild);
    var idx=0;
    function place(){var t=btns[idx],x=t.offsetLeft,y=t.offsetTop;
      thumb.style.width=t.offsetWidth+'px';thumb.style.height=t.offsetHeight+'px';thumb.style.transform='translate('+x+'px,'+y+'px)';
      var cs=getComputedStyle(root),bw=parseFloat(cs.borderLeftWidth)+parseFloat(cs.borderRightWidth),bh=parseFloat(cs.borderTopWidth)+parseFloat(cs.borderBottomWidth),rb=root.getBoundingClientRect();
      inner.style.width=(rb.width-bw)+'px';inner.style.height=(rb.height-bh)+'px';inner.style.transform='translate('+(-x)+'px,'+(-y)+'px)'}
    function set(i,fromUser){idx=i;btns.forEach(function(b,k){b.setAttribute('aria-checked',k===i?'true':'false');b.tabIndex=k===i?0:-1});place();if(fromUser)onPick(btns[i].dataset.f)}
    function go(i){i=(i+btns.length)%btns.length;btns[i].focus();set(i,true)}
    btns.forEach(function(b,i){
      b.addEventListener('click',function(){if(i!==idx)set(i,true)});
      b.addEventListener('keydown',function(e){var k=e.key;
        if(k==='ArrowRight'||k==='ArrowDown'){e.preventDefault();go(i+1)}
        else if(k==='ArrowLeft'||k==='ArrowUp'){e.preventDefault();go(i-1)}
        else if(k==='Home'){e.preventDefault();go(0)}
        else if(k==='End'){e.preventDefault();go(btns.length-1)}})});
    root.classList.add('still');set(0,false);requestAnimationFrame(function(){requestAnimationFrame(function(){root.classList.remove('still')})});
    addEventListener('resize',function(){root.classList.add('still');place();requestAnimationFrame(function(){root.classList.remove('still')})});
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){root.classList.add('still');place();requestAnimationFrame(function(){root.classList.remove('still')})});
  }
```

### Copy button JS

```js
  /* copy button: width reserved by stacked labels, success and failure both stated, timer restarts */
  var wa=TEXT_TO_COPY;
  var cb=$('#copywa'),cbSay=$('[role="status"]',cb),cbTimer=0;
  function fallbackCopy(text){var a=document.createElement('textarea');a.value=text;a.setAttribute('readonly','');a.style.cssText='position:fixed;top:0;left:0;opacity:0';document.body.appendChild(a);
    var sel=document.getSelection(),prev=sel&&sel.rangeCount?sel.getRangeAt(0):null;a.select();var ok=false;try{ok=document.execCommand('copy')}catch(e){}
    document.body.removeChild(a);if(sel&&prev){sel.removeAllRanges();sel.addRange(prev)}return ok}
  function cbSet(st){cb.dataset.state=st;cbSay.textContent=st==='copied'?'Copied to clipboard':st==='error'?'Copy failed':'';clearTimeout(cbTimer);if(st!=='idle')cbTimer=setTimeout(function(){cbSet('idle')},st==='error'?3200:2000)}
  cb.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();
    var done=function(ok){cbSet(ok?'copied':'error')};
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(wa).then(function(){done(true)},function(){done(fallbackCopy(wa))});
    else done(fallbackCopy(wa))});

```

### Scroll spy JS

```js
  /* scroll spy: the reading line travels with scroll progress so the last short section can win; a click holds the highlight until you arrive */
  var spyLinks=$$('.rail a'),navLinks=$$('.nav-links a'),spyIds=spyLinks.map(function(a){return a.getAttribute('href').slice(1)}),OFF=96,spyLock=null,spyLockT=0,spyActive='',spyFrame=0,spySayT=0;
  var spySay=document.createElement('p');spySay.className='sr-only';spySay.setAttribute('role','status');spySay.setAttribute('aria-live','polite');document.body.appendChild(spySay);
  function spyMeasure(){var max=document.documentElement.scrollHeight-innerHeight,ratio=max>0?Math.min(1,Math.max(0,scrollY/max)):1,line=OFF+ratio*Math.max(0,innerHeight-OFF-1),cur='',last='';
    spyIds.forEach(function(id){var n=document.getElementById(id);if(!n)return;last=id;if(!cur)cur=id;if(n.getBoundingClientRect().top<=line+1)cur=id});
    return (scrollY+innerHeight>=document.documentElement.scrollHeight-2&&last)?last:cur}
  function spyPaint(id){if(id===spyActive)return;spyActive=id;
    spyLinks.concat(navLinks).forEach(function(a){if(a.getAttribute('href')==='#'+id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')});
    clearTimeout(spySayT);spySayT=setTimeout(function(){var a=spyLinks.filter(function(x){return x.getAttribute('href')==='#'+id})[0];if(a)spySay.textContent=a.textContent.replace(/\s+/g,' ').trim()},420)}
  function spyRelease(){spyLock=null;clearTimeout(spyLockT)}
  function spySync(){if(spyFrame)return;spyFrame=requestAnimationFrame(function(){spyFrame=0;var n=spyMeasure();if(!n)return;if(spyLock){if(spyLock===n)spyRelease();return}spyPaint(n)})}
  addEventListener('scroll',spySync,{passive:true});addEventListener('resize',spySync);
  addEventListener('wheel',function(){if(spyLock)spyRelease()},{passive:true});addEventListener('touchstart',function(){if(spyLock)spyRelease()},{passive:true});
  function spyGo(id){var n=document.getElementById(id);if(!n)return;spyLock=id;spyPaint(id);
    var max=Math.max(0,document.documentElement.scrollHeight-innerHeight),H=n.getBoundingClientRect().top+scrollY,
        top=Math.min(max,Math.max(0,H-84));
    scrollTo({top:top,behavior:reduce?'auto':'smooth'});
    if(!n.hasAttribute('tabindex'))n.setAttribute('tabindex','-1');n.focus({preventScroll:true});
    clearTimeout(spyLockT);spyLockT=setTimeout(function(){spyLock=null;spySync()},900)}
  spyLinks.concat(navLinks).concat($$('.hero .cta a[href^="#"],#navcta')).forEach(function(a){a.addEventListener('click',function(e){
    if(e.metaKey||e.ctrlKey||e.shiftKey||e.button!==0)return;var id=a.getAttribute('href').slice(1);if(spyIds.indexOf(id)<0)return;e.preventDefault();spyGo(id)})});
  spySync();

```

## Test recipe (add to visual-verify Step 3)

- Click each segment, arrow-key through, press Home and End, then click three segments within 300ms. Assert the thumb's left and top equal the selected button's, at 1440, 1100, 768 and 390 wide.
- Click the copy button with clipboard permission granted and assert `dataset.state`, the live region text, and that the button's width is identical in idle, copied and error. Force failure by stubbing `navigator.clipboard.writeText` to reject and `document.execCommand` to return false.
- Click every rail link and assert the highlighted link and that the target's top equals the offset. Scroll to the page bottom and assert the last link is active.
- Emulate `prefers-reduced-motion: reduce` and re-run the thumb assertion.
