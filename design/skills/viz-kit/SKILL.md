---
name: "viz-kit"
description: "Brand-independent charts and executive landing pages from one component kit (US map, pyramid, treemap, log ladder, matrix, countdowns, live builder). Use for any data viz or exec page."
---

# Viz Kit

One kit for every chart and every executive landing page, for any brand. Components are token-driven: a brand changes values in one `:root` block, never markup. Other page skills (executive-one-pager, visual-report-builder, landing-page, campaign-visualization, meeting-growth-visuals) call this skill for their charts and visual blocks.

**Reference implementation:** `Other/Skills/viz-kit/gallery.html` in the Celsus vault (also published as the "Viz Kit Gallery" artifact, https://claude.ai/artifact/3zArqRTh8VFmxaSVVZ8aCc; read it with the Artifact tool, action read). It renders all 20 components with sample data and a Neutral / Forest / Plum brand switcher. Copy component CSS and markup from it. US state shapes: `Other/Skills/viz-kit/us-states-albers.json`.

## When to use

- Any request for a chart, graph, map, dashboard block, KPI tiles or data visualization.
- Any executive landing page, product landing page prototype, working-session page, board or leadership page that argues with numbers.
- Any time another skill needs a chart. That skill owns the page story; this skill owns the visuals.

Load the bundled `dataviz` skill too when choosing colours for more than one series. Load `artifact-design` before publishing an artifact.

## Step 1. Get the brand tokens

Ask which brand the page is for only if it is unclear. Then:

1. If a brand skill exists (lakeb2b-brand-guidelines, ampliz-brand-guidelines, metricfox-brand-guidelines, champions-group-brand, ab7-brand-guidelines, span-blog-builder, deependhq-design-system), read it and map its values onto the token contract below.
2. If the brand has a design system file in the vault (for example the SGS design prompt under `Atlas/Context Docs/SPAN Global Services/`), use that.
3. Otherwise use the Neutral tokens below.

Never mix two brands' palettes on one page.

### Token contract

Every component reads only these tokens. Fill all of them, light and dark.

| Token | Role |
|---|---|
| `--bg`, `--surface`, `--surface-alt` | Page, card, alternate band |
| `--ink`, `--body`, `--muted`, `--line`, `--grid` | Headings, text, captions, borders, hero grid |
| `--accent`, `--accent-soft` | Primary brand colour, its tint for fills and table heads |
| `--panel`, `--on-panel`, `--on-panel-dim`, `--panel-texture` | Dark proof panel (hero stats, countdowns, builder results) and its texture (`background-image` value) |
| `--hl`, `--hl-bg` | Highlight for "us" in comparisons, callouts, placeholders, data-needs pills. Reserved: never a data series colour |
| `--s0` to `--s5`, `--s-ink-lo`, `--s-ink-hi` | One-hue sequential ramp, light to dark (dark mode reverses lightness so high values stay prominent), and label ink on light or dark steps |
| `--tip-bg`, `--tip-fg` | Tooltip |
| `--f-display`, `--f-body`, `--f-data` | Display face, body face, mono face for every number |

Neutral defaults (light, with both dark blocks). Paste, then overwrite values for the brand:

```css
:root{
  --bg:#FFFFFF; --surface:#FFFFFF; --surface-alt:#F6F7F9; --ink:#15181D; --body:#3B4350; --muted:#69717E; --line:#E2E5EA; --grid:rgba(21,24,29,.045);
  --accent:#2457D6; --accent-soft:#EAF1FF; --panel:#14213D; --on-panel:#FFFFFF; --on-panel-dim:rgba(255,255,255,.7);
  --panel-texture:radial-gradient(rgba(255,255,255,.07) 1px,transparent 1.2px);
  --hl:#B45309; --hl-bg:#FEF3E2;
  --s0:#EAF1FF; --s1:#C3D6FF; --s2:#8DB0FF; --s3:#4F82F7; --s4:#2457D6; --s5:#163A94; --s-ink-lo:#15181D; --s-ink-hi:#FFFFFF;
  --tip-bg:#15181D; --tip-fg:#FFFFFF;
  --f-display:"Archivo",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  --f-body:"Public Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  --f-data:"IBM Plex Mono",ui-monospace,"SFMono-Regular",Menlo,monospace;
  --r:6px;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0F1217; --surface:#13171D; --surface-alt:#151A21; --ink:#E8ECF1; --body:#C2C9D3; --muted:#8C95A2; --line:#262D37; --grid:rgba(232,236,241,.04);
  --accent:#6B9BFF; --accent-soft:#18243A; --panel:#14213D; --on-panel:#FFFFFF; --on-panel-dim:rgba(255,255,255,.7);
  --hl:#F59E0B; --hl-bg:#2A2010;
  --s0:#18243A; --s1:#1D3360; --s2:#244A8E; --s3:#3366C4; --s4:#5F8FF0; --s5:#A9C4FF; --s-ink-lo:#E8ECF1; --s-ink-hi:#0F1217;
  --tip-bg:#E8ECF1; --tip-fg:#0F1217; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0F1217; --surface:#13171D; --surface-alt:#151A21; --ink:#E8ECF1; --body:#C2C9D3; --muted:#8C95A2; --line:#262D37; --grid:rgba(232,236,241,.04);
  --accent:#6B9BFF; --accent-soft:#18243A; --panel:#14213D; --on-panel:#FFFFFF; --on-panel-dim:rgba(255,255,255,.7);
  --hl:#F59E0B; --hl-bg:#2A2010;
  --s0:#18243A; --s1:#1D3360; --s2:#244A8E; --s3:#3366C4; --s4:#5F8FF0; --s5:#A9C4FF; --s-ink-lo:#E8ECF1; --s-ink-hi:#0F1217;
  --tip-bg:#E8ECF1; --tip-fg:#0F1217; color-scheme:dark}
```

## Step 2. Pick components by the job the data does

| Data job | Component |
|---|---|
| The answer in one line plus 3 to 4 headline figures | C01 Hero thesis + C02 Proof panel |
| One fact the reader must remember | C03 Callout (one per page) |
| Figures that are the argument, each with a source | C04 Proof tiles |
| Values by US state | C05 Choropleth + C06 Ranked bar list + C07 Table view |
| Levels, tiers, funnel stages | C08 Pyramid (centered bars) |
| Parts of a whole with many categories, drill-down | C09 Treemap |
| Ranking with one entity that matters ("us") | C10 Highlight bars |
| Several sources disagree on one number | C11 Disagreeing estimates with a dashed placeholder bar |
| Values spanning orders of magnitude (prices, sizes) | C12 Log-scale ladder (dot plot, verified vs estimate, range whisker, proposal band) |
| Who has which capability | C13 Capability matrix (filled, half, hollow dots, "?" to confirm, our row highlighted) |
| A deadline that forces a decision | C14 Countdown card (live days left) |
| Shares of one total in an order (age, stage) | C15 Composition strip |
| A distribution across ordered bins | C16 Column chart |
| What one unit of the product contains | C17 Record anatomy (grouped fields, focus on click) |
| A product people query | C18 Live count builder (filters, live results on the panel) |
| Who to target first | C19 Ranked segments table |
| What we decide in the room | C20 Decision table with ticks |
| Internal prototype review | Data-needs overlay: a toggle that shows a dashed pill per section listing the exact data it needs |

A single chart request gets one component, not a page. An executive page uses at most 8 to 10 components and opens with C01 and C02.

## Step 3. Build

- Self-contained HTML. For an Artifact publish, write the page content without doctype or html/head/body (the publisher wraps it). For a vault copy, wrap it in a full document.
- Fonts from Google Fonts only, with fallback stacks. No other external hosts except pinned cdnjs scripts when truly needed. The kit needs no chart library.
- Full width: wrapper `max-width:1520px` with `padding-inline:clamp(16px,3.5vw,56px)`. Never a narrow centered column.
- Every colour from tokens. Body has an explicit `background:var(--bg)`.
- Every number in `--f-data` with tabular figures.
- Every chart: hover tooltip (`data-tip` attribute plus the shared tooltip), selective direct labels, recessive grid, one axis only, labels in text tokens never the series colour. Maps and long rankings get a table view.
- Scroll motion: use the `.reveal` (translate only) and `.fill.grow` classes from the gallery. They run only under `animation-timeline: view()` and finish once an element is fully in view, so screenshots, print and thumbnails always show the end state. Never animate opacity from zero. Respect `prefers-reduced-motion`.
- Sample or modelled numbers: say so on the page (ribbon or caption). Mark estimates (hollow dot, "est." badge). Every figure carries a source line.
- Unique element ids. A section id that matches a chart id breaks the page (the chart renderer writes into the section). Check with `grep -o 'id="[^"]*"' file | sort | uniq -d`.

### Core helpers (VK)

Paste this block once per page, then call the functions. Shapes are documented above each function.

```js
const VK=(()=>{
  const NS='http://www.w3.org/2000/svg';
  const fmt=n=>Math.round(n).toLocaleString('en-US');
  const cpt=n=>(n>=1e6?(n/1e6).toFixed(n>=1e7?0:1)+'M':n>=1e3?(n/1e3).toFixed(n>=1e4?0:1)+'K':String(Math.round(n))).replace(/\.0(?=[KM])/,'');
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  /* tooltip: any element with data-tip */
  function tooltips(){const tip=document.getElementById('tip');document.addEventListener('mousemove',e=>{const t=e.target.closest('[data-tip]');if(!t){tip.hidden=true;return}tip.innerHTML=t.dataset.tip;tip.hidden=false;tip.style.left=Math.min(e.clientX+14,innerWidth-300)+'px';tip.style.top=(e.clientY+14)+'px'})}
  /* quantile breaks rounded to 2 significant figures */
  function breaks(vals,k=6){const v=[...vals].sort((a,b)=>a-b),q=p=>v[Math.floor(p*(v.length-1))],nice=x=>{if(x<=0)return 0;const p=Math.pow(10,Math.max(0,Math.floor(Math.log10(x))-1));return Math.round(x/p)*p};const out=[];for(let i=1;i<k;i++)out.push(nice(q(i===k-1?.93:i/k)));return out}
  const step=(v,b)=>{let i=0;while(i<b.length&&v>=b[i])i++;return i};
  /* C05 choropleth. states:[{a,n,d,c}], values:{AA:number} */
  function choropleth(svg,states,values,o={}){
    const b=breaks(states.map(s=>values[s.a]||0)),small=new Set(o.noLabel||['RI','DE','DC','CT','NJ','MA','NH','VT','MD','HI']);let h='';
    states.forEach(s=>{const v=values[s.a]||0,k=step(v,b);h+=`<path class="st${o.selected===s.a?' on':''}" d="${s.d}" data-a="${s.a}" style="fill:var(--s${k})" data-tip="<b>${esc(s.n)}</b><br>${fmt(v)} ${o.unit||''}"/>`});
    states.forEach(s=>{if(small.has(s.a))return;const k=step(values[s.a]||0,b);h+=`<text class="lbl" x="${s.c[0]}" y="${s.c[1]}" style="fill:${k>=3?'var(--s-ink-hi)':'var(--s-ink-lo)'}">${s.a}</text>`});
    svg.innerHTML=h;if(o.onClick)svg.onclick=e=>{const p=e.target.closest('.st');if(p)o.onClick(p.dataset.a)};return b}
  function legend(el,b){el.innerHTML=[0,...b].map((x,i)=>`<div><i style="background:var(--s${i})"></i><span>${i?cpt(x):'0'}+</span></div>`).join('')}
  /* C06 bar list. rows:[{key,name,v,label?}] */
  function barList(el,rows,o={}){const mx=Math.max(...rows.map(r=>r.v));el.innerHTML=rows.map(r=>`<${o.onClick?'button type="button"':'div'} class="bar-row${o.selected===r.key?' on':''}" data-key="${r.key||''}"><span class="name">${esc(r.name)}</span><span class="track"><span class="fill grow" style="width:${r.v/mx*100}%"></span></span><span class="v">${r.label??cpt(r.v)}</span></${o.onClick?'button':'div'}>`).join('');if(o.onClick)el.onclick=e=>{const b=e.target.closest('[data-key]');if(b)o.onClick(b.dataset.key)}}
  /* C08 pyramid. rows top to bottom:[{name,v,note?}] */
  function pyramid(svg,rows){const mx=Math.max(...rows.map(r=>r.v)),cx=330,half=170,rh=50,gap=12,shades=['--s5','--s4','--s3','--s2','--s1'];svg.setAttribute('viewBox',`0 0 640 ${rows.length*(rh+gap)+8}`);
    svg.innerHTML=rows.map((r,i)=>{const w=Math.max(6,r.v/mx*half*2),y=6+i*(rh+gap);return `<rect x="${cx-w/2}" y="${y}" width="${w}" height="${rh}" rx="4" style="fill:var(${shades[Math.min(i,4)]})" data-tip="<b>${esc(r.name)}</b><br>${fmt(r.v)}"/><text x="0" y="${y+rh/2-6}" dominant-baseline="middle">${esc(r.name)}</text><text class="m" x="0" y="${y+rh/2+11}" dominant-baseline="middle">${r.note||''}</text><text class="v" x="640" y="${y+rh/2}" text-anchor="end" dominant-baseline="middle">${fmt(r.v)}</text>`}).join('')}
  /* C09 squarified treemap. items:[{n,v,...}] */
  function squarify(items,x,y,w,h){const out=[],tot=items.reduce((s,i)=>s+i.v,0),sc=w*h/tot;let rest=items.map(i=>({...i,a:i.v*sc}));const worst=(row,side)=>{const s=row.reduce((a,b)=>a+b.a,0),mx=Math.max(...row.map(r=>r.a)),mn=Math.min(...row.map(r=>r.a));return Math.max(side*side*mx/(s*s),(s*s)/(side*side*mn))};
    while(rest.length){const side=Math.min(w,h);let row=[rest[0]],i=1;while(i<rest.length&&worst([...row,rest[i]],side)<=worst(row,side)){row.push(rest[i]);i++}rest=rest.slice(i);const s=row.reduce((a,b)=>a+b.a,0);
      if(w>=h){const cw=s/h;let cy=y;row.forEach(r=>{const rh=r.a/cw;out.push({...r,x,y:cy,w:cw,h:rh});cy+=rh});x+=cw;w-=cw}else{const ch=s/w;let cx=x;row.forEach(r=>{const rw=r.a/ch;out.push({...r,x:cx,y,w:rw,h:ch});cx+=rw});y+=ch;h-=ch}}return out}
  function treemap(el,items,o={}){const W=1000,H=460,rects=squarify([...items].sort((a,b)=>b.v-a.v),0,0,W,H);el.innerHTML='';rects.forEach((r,i)=>{const k=Math.max(1,5-Math.floor(i/2)),b=document.createElement('button');b.type='button';b.className='tile'+(o.selected===r.n?' on':'');b.style.cssText=`left:${r.x/W*100}%;top:${r.y/H*100}%;width:${r.w/W*100}%;height:${r.h/H*100}%;background:var(--s${k});color:${k>=3?'var(--s-ink-hi)':'var(--s-ink-lo)'}`;b.innerHTML=`<h4>${esc(r.n)}</h4><div><span class="num">${cpt(r.v)}</span><small>${r.sub||''}</small></div>`;b.onclick=()=>o.onClick&&o.onClick(r.n);el.appendChild(b)})}
  /* C10/C11 horizontal bars with highlight and optional placeholder row */
  function hbars(svg,rows,o={}){const L=110,R=560,T=8,rh=o.rh||34,max=o.max||Math.max(...rows.map(r=>r.v))*1.05,n=rows.length+(o.placeholder?1:0),ticks=o.ticks||[0,max/4,max/2,max*3/4,max].map(Math.round);svg.setAttribute('viewBox',`0 0 640 ${T+n*rh+30}`);let h='';
    ticks.forEach(v=>{const x=L+(R-L)*v/max;h+=`<line class="gl" x1="${x}" x2="${x}" y1="${T}" y2="${T+n*rh}"/><text class="m" x="${x}" y="${T+n*rh+16}" text-anchor="middle">${cpt(v)}</text>`});
    rows.forEach((r,i)=>{const y=T+i*rh+(rh-20)/2,w=Math.max(3,(R-L)*r.v/max),hl=r.key===o.highlight,col=hl?'var(--hl)':'var(--accent)';h+=`<text x="${L-10}" y="${y+10}" text-anchor="end" dominant-baseline="middle" style="${hl?'font-weight:700;fill:var(--hl)':''}">${esc(r.name)}</text><path d="M${L},${y} H${L+w-4} q4,0 4,4 V${y+16} q0,4 -4,4 H${L} Z" style="fill:${col}"/><text class="v" x="${L+w+8}" y="${y+10}" dominant-baseline="middle" style="${hl?'fill:var(--hl);font-weight:700':''}">${r.label??fmt(r.v)}</text><rect class="hit" x="0" y="${y-6}" width="640" height="${rh}" data-tip="<b>${esc(r.name)}</b><br>${r.label??fmt(r.v)}${r.src?'<br>'+esc(r.src):''}"/>`});
    if(o.placeholder){const y=T+rows.length*rh+(rh-24)/2;h+=`<text x="${L-10}" y="${y+12}" text-anchor="end" dominant-baseline="middle" style="font-weight:700;fill:var(--hl)">${esc(o.placeholder.name)}</text><rect x="${L}" y="${y}" width="${R-L}" height="24" rx="4" style="fill:var(--hl-bg);stroke:var(--hl)" stroke-dasharray="5 4"/><text x="${L+12}" y="${y+12}" dominant-baseline="middle" style="fill:var(--hl);font-weight:600">${esc(o.placeholder.text)}</text>`}
    svg.innerHTML=h}
  /* C12 log ladder. pts:[{n,v,verified,note,max?}], o:{lo,hi,zone:[a,b,label],ticks} */
  function ladder(svg,pts,o){const L=40,R=1170,base=230,lo=Math.log10(o.lo),hi=Math.log10(o.hi),X=v=>L+(R-L)*(Math.log10(v)-lo)/(hi-lo);let h='';
    if(o.zone)h+=`<rect x="${X(o.zone[0])}" y="20" width="${X(o.zone[1])-X(o.zone[0])}" height="${base-20}" rx="4" style="fill:var(--hl-bg);stroke:var(--hl)" stroke-dasharray="5 4"/><text x="${(X(o.zone[0])+X(o.zone[1]))/2}" y="38" text-anchor="middle" style="fill:var(--hl);font-weight:600">${esc(o.zone[2])}</text>`;
    o.ticks.forEach(v=>{const x=X(v);h+=`<line class="gl" x1="${x}" x2="${x}" y1="20" y2="${base}"/><text class="m" x="${x}" y="${base+20}" text-anchor="middle">${o.prefix||''}${cpt(v)}</text>`});
    h+=`<line class="ax" x1="${L}" x2="${R}" y1="${base}" y2="${base}"/><text class="m" x="${R}" y="${base+42}" text-anchor="end">${esc(o.axis||'')}</text>`;
    const placed=[];pts.forEach(p=>{const x=X(p.v);let lane=0;while(placed.some(q=>q.lane===lane&&Math.abs(q.x-x)<100))lane++;placed.push({x,lane});const y=base-28-lane*48;
      if(p.max)h+=`<line x1="${x}" x2="${X(p.max)}" y1="${y}" y2="${y}" style="stroke:var(--accent)" stroke-width="2"/><line x1="${X(p.max)}" x2="${X(p.max)}" y1="${y-5}" y2="${y+5}" style="stroke:var(--accent)" stroke-width="2"/>`;
      h+=`<line x1="${x}" x2="${x}" y1="${y+8}" y2="${base}" style="stroke:var(--line)"/><circle cx="${x}" cy="${y}" r="7" style="fill:${p.verified?'var(--accent)':'var(--surface)'};stroke:var(--accent)" stroke-width="2.5"/><text x="${x}" y="${y-14}" text-anchor="middle" style="font-weight:600">${esc(p.n)}</text><circle class="hit" cx="${x}" cy="${y}" r="18" data-tip="<b>${esc(p.n)}</b><br>${esc(p.note)}<br>${p.verified?'Verified':'Estimate'}"/>`});
    svg.innerHTML=h}
  /* C13 matrix dots */
  const dot=(k,l)=>`<svg width="16" height="16" viewBox="0 0 16 16" role="img" aria-label="${l}" style="vertical-align:middle"><circle cx="8" cy="8" r="6" style="fill:${k==='y'?'var(--accent)':'none'};stroke:var(--accent)" stroke-width="2"/>${k==='p'?'<path d="M8,2 A6,6 0 0 0 8,14 Z" style="fill:var(--accent)"/>':''}</svg>`;
  function matrix(tbody,rows,us){const L={y:'Yes',p:'Partly',n:'No'};tbody.innerHTML=rows.map(r=>`<tr${r[0]===us?' class="us"':''}><th>${esc(r[0])}</th>${r.slice(1).map(c=>c==='?'?'<td class="c q">?</td>':`<td class="c">${dot(c,L[c])}</td>`).join('')}</tr>`).join('')}
  function matrixKey(el){el.innerHTML=[['y','Yes'],['p','Partly'],['n','No']].map(([k,l])=>`<span>${dot(k,l)} ${l}</span>`).join('')+'<span style="color:var(--hl)">? To confirm</span>'}
  /* C14 countdown */
  function countdowns(){const now=new Date();document.querySelectorAll('[data-cd]').forEach(el=>{const [y,m,d]=el.dataset.cd.split('-').map(Number);el.textContent=fmt(Math.max(0,Math.ceil((new Date(y,m-1,d)-now)/864e5)))})}
  /* C15 strip. parts:[{l,v}] shares, darkest first */
  function strip(el,key,parts){const st=['--s5','--s4','--s2','--s1','--s0'];el.innerHTML=parts.map((p,i)=>`<i style="width:${p.v*100}%;background:var(${st[i]})" data-tip="${esc(p.l)}: ${Math.round(p.v*100)}%"></i>`).join('');key.innerHTML=parts.map((p,i)=>`<div><i style="background:var(${st[i]})"></i>${esc(p.l)}<b>${Math.round(p.v*100)}%</b></div>`).join('')}
  /* C16 columns. rows:[{l,v}] as shares */
  function columns(svg,rows,o={}){const mx=Math.max(...rows.map(r=>r.v)),top=Math.ceil(mx*10)/10,L=40,R=630,T=16,B=250,bw=(R-L)/rows.length;let h='';
    for(let k=0;k<=4;k++){const y=B-(B-T)*k/4;h+=`<line class="gl" x1="${L}" x2="${R}" y1="${y}" y2="${y}"/><text class="m" x="${L-8}" y="${y}" text-anchor="end" dominant-baseline="middle">${Math.round(top*k/4*100)}%</text>`}
    rows.forEach((r,i)=>{const bh=(B-T)*r.v/top,x=L+i*bw+bw*.18,w=bw*.64;h+=`<path d="M${x},${B} V${B-bh+4} q0,-4 4,-4 H${x+w-4} q4,0 4,4 V${B} Z" style="fill:var(--accent)" data-tip="${esc(r.l)}: ${Math.round(r.v*100)}%"/><text class="v" x="${x+w/2}" y="${B-bh-8}" text-anchor="middle">${Math.round(r.v*100)}%</text><text class="m" x="${x+w/2}" y="${B+20}" text-anchor="middle">${esc(r.l)}</text>`});
    if(o.axis)h+=`<text class="m" x="${(L+R)/2}" y="292" text-anchor="middle">${esc(o.axis)}</text>`;svg.innerHTML=h}
  /* C17 record anatomy. groups:[{id,name,why,fields:[[k,v]]}] */
  function record(gEl,lEl,groups){gEl.innerHTML=groups.map(g=>`<div class="grp" data-g="${g.id}"${g.wide?' style="grid-column:1/-1"':''}><h4>${esc(g.name)} <span>${g.fields.length} fields</span></h4><dl>${g.fields.map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl></div>`).join('');
    lEl.innerHTML=groups.map(g=>`<button type="button" data-g="${g.id}" aria-pressed="false"><b>${g.fields.length}</b><span><strong>${esc(g.name)}</strong>${esc(g.why)}</span></button>`).join('');
    lEl.onclick=e=>{const b=e.target.closest('[data-g]');if(!b)return;const on=b.getAttribute('aria-pressed')!=='true';lEl.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(on&&x===b)));gEl.classList.toggle('focus',on);gEl.querySelectorAll('.grp').forEach(x=>x.classList.toggle('on',on&&x.dataset.g===b.dataset.g))}}
  /* C20 decision ticks remembered per viewer */
  function ticks(){document.querySelectorAll('.check input').forEach(c=>{try{c.checked=localStorage.getItem('vk-'+c.id)==='1'}catch(_){}c.addEventListener('change',()=>{try{localStorage.setItem('vk-'+c.id,c.checked?'1':'0')}catch(_){}})})}
  /* data-needs overlay */
  function reqToggle(id){const t=document.getElementById(id);t.addEventListener('change',()=>document.body.classList.toggle('show-req',t.checked))}
  return {fmt,cpt,esc,tooltips,breaks,choropleth,legend,barList,pyramid,squarify,treemap,hbars,ladder,matrix,matrixKey,countdowns,strip,columns,record,ticks,reqToggle};
})();
```

Typical calls:

```js
VK.tooltips();
const b = VK.choropleth(svgEl, STATES, valuesByStateCode, {unit:'accounts', selected, onClick:code=>...});
VK.legend(legendEl, b);
VK.barList(el, rows.slice(0,10), {selected, onClick:key=>...});
VK.pyramid(svgEl, [{name:'C-level', v:565000, note:'6%'}, ...]);
VK.treemap(el, [{n:'ERP', v:236000, sub:'34 products'}, ...], {selected, onClick:n=>...});
VK.hbars(svgEl, rows, {highlight:'us', max, ticks});
VK.hbars(svgEl, estimates, {placeholder:{name:'Us', text:'Our verified figure'}});
VK.ladder(svgEl, pts, {lo:100, hi:60000, ticks:[100,300,1000,3000,10000,30000], prefix:'$', zone:[1000,10000,'Proposed zone'], axis:'US dollars per year, log scale'});
VK.matrix(tbodyEl, [['Vendor A','y','n','p'], ['Us','?','y','y']], 'Us'); VK.matrixKey(keyEl);
VK.countdowns();  // fills every [data-cd="YYYY-MM-DD"]
VK.strip(stripEl, keyEl, [{l:'0 to 30 days', v:.41}, ...]);
VK.columns(svgEl, [{l:'1 to 49', v:.55}, ...], {axis:'Employees'});
VK.record(groupsEl, listEl, [{id:'co', name:'Company', why:'...', fields:[['HQ','Fargo, ND']]}, ...]);
VK.ticks(); VK.reqToggle('reqToggle');
```

### US map data

Load `Other/Skills/viz-kit/us-states-albers.json` (51 states with `a` code, `n` name, `d` SVG path, `c` label centroid, pre-projected to a 975 x 610 viewBox) and inline it as `const STATES = [...]`. If the file is not reachable, regenerate it (needs network for npm):

```bash
mkdir map && cd map && npm init -y >/dev/null && npm install us-atlas@3 topojson-client@3 topojson-simplify@3 d3-geo@3
cat > gen.mjs <<'JS'
import fs from 'fs';
import * as topo from 'topojson-client';
import * as simp from 'topojson-simplify';
import { geoPath } from 'd3-geo';
const us = JSON.parse(fs.readFileSync('node_modules/us-atlas/states-albers-10m.json'));
let t = simp.presimplify(us);
t = simp.simplify(t, 0.5);
const states = topo.feature(t, t.objects.states).features;
const path = geoPath(null).digits(1);
const abbr = {"01":"AL","02":"AK","04":"AZ","05":"AR","06":"CA","08":"CO","09":"CT","10":"DE","11":"DC","12":"FL","13":"GA","15":"HI","16":"ID","17":"IL","18":"IN","19":"IA","20":"KS","21":"KY","22":"LA","23":"ME","24":"MD","25":"MA","26":"MI","27":"MN","28":"MS","29":"MO","30":"MT","31":"NE","32":"NV","33":"NH","34":"NJ","35":"NM","36":"NY","37":"NC","38":"ND","39":"OH","40":"OK","41":"OR","42":"PA","44":"RI","45":"SC","46":"SD","47":"TN","48":"TX","49":"UT","50":"VT","51":"VA","53":"WA","54":"WV","55":"WI","56":"WY","72":"PR","60":"AS","66":"GU","69":"MP","78":"VI"};
const out = states.filter(f=>abbr[f.id] && !['PR','AS','GU','MP','VI'].includes(abbr[f.id])).map(f=>{const c=path.centroid(f);return {a:abbr[f.id], n:f.properties.name, d:path(f), c:[Math.round(c[0]),Math.round(c[1])]};});
const mesh = path(topo.mesh(t, t.objects.states, (a,b)=>a!==b));
fs.writeFileSync('states.json', JSON.stringify(out));
console.log(out.length, JSON.stringify(out).length, mesh.length);
JS
node gen.mjs   # writes states.json
```

For world or other countries, use the same pattern with `world-atlas` and a d3 projection. For dense point data use deck.gl with MapLibre instead.

## Step 4. Write the words

- Assertion headlines: each section heading states the conclusion ("Three vendors disagree 4x on one count"), not a topic.
- First two lines of the page carry the whole message.
- Zero em dashes or en dashes anywhere, including ranges ("1 to 49").
- Run the no-ai-slop rules as the final gate on all copy.

## Step 5. Check, once

Run one render check before publishing (Playwright is available in the cloud workspace; use `executablePath:'/opt/pw-browsers/chromium'`):

1. 1440px light, 1440px dark, 400px phone. `document.documentElement.scrollWidth` must equal the viewport width.
2. No console errors.
3. Look at the screenshot for label collisions, clipped text and empty charts. Emulate `reducedMotion:'reduce'` so the shot shows the end state.
4. Dash scan returns zero; duplicate id scan returns nothing.
5. Run `Other/Skills/no-ai-slop/slop_lint.py` on the page text when the vault is reachable.

## Step 6. Deliver

- Publish as an Artifact (it gets a URL Champ can share) and save the full-document copy to the relevant Celsus vault folder.
- Tell Champ in one or two lines what the page shows. Remind him he can take the page into Claude Design for further visual polish.
- Ask for changes or critiques. When he gives a reusable correction, propose an update to this skill so the next page starts from it.

## Lessons already learned

- A section id equal to a chart id wiped a whole section. Keep ids unique.
- Opacity-based scroll reveals made full-page screenshots look broken. Translate only.
- SVG bars with CSS scale transforms misplace labels. Animate HTML bars only.
- Unicode half-circle glyphs render tiny; use the SVG dot from `VK.matrix`.
- Log axes need explicit tick labels in plain money ("$1K", not "$1.0K").
- Never put a count on a buyer-facing page that the data team has not confirmed; ship prototypes with a visible "illustrative" ribbon.