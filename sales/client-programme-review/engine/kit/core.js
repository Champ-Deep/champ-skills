(function(){
  var root=document.documentElement;
  var q=new URLSearchParams(location.search);
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isStatic=q.get('static')==='1'||location.hash==='#static'||reduce||!('IntersectionObserver' in window);
  root.classList.add(isStatic?'static':'motion');

  /* headline word split */
  document.querySelectorAll('[data-words]').forEach(function(h){
    var html=h.innerHTML.trim(); var parts=html.split(/(\s+)/); var i=0; var out='';
    parts.forEach(function(p){ if(/^\s+$/.test(p)){out+=' ';} else if(p){out+='<span class="w" style="--i:'+(i++)+'">'+p+'</span>';} });
    h.innerHTML=out;
  });

  /* waffle builder */
  document.querySelectorAll('[data-waffle]').forEach(function(w){
    var total=+w.dataset.total, on=+w.dataset.on, cols=(innerWidth<600&&w.dataset.colsSm)?+w.dataset.colsSm:(+w.dataset.cols||36);
    w.style.setProperty('--cols',cols);
    var cA=w.dataset.ca||'#6D08BE', cB=w.dataset.cb||'#DD1286';
    function mix(a,b,t){a=parseInt(a.slice(1),16);b=parseInt(b.slice(1),16);
      var r=Math.round(((a>>16)&255)*(1-t)+((b>>16)&255)*t),g=Math.round(((a>>8)&255)*(1-t)+((b>>8)&255)*t),bl=Math.round((a&255)*(1-t)+(b&255)*t);
      return 'rgb('+r+','+g+','+bl+')';}
    var frag=document.createDocumentFragment();
    for(var k=0;k<total;k++){var d=document.createElement('i');var row=Math.floor(k/cols),col=k%cols;
      if(k<on){d.className=(w.dataset.frac&&k===total-1)?'on part':'on';d.style.setProperty('--c',mix(cA,cB,cols>1?col/(cols-1):0));} else d.className='off';
      d.style.setProperty('--d',Math.round((row*cols*0.0+col)*18+row*22));frag.appendChild(d);}
    w.appendChild(frag);
  });

  /* count up */
  var fmt=function(v,dec){return v.toLocaleString('en-US',{minimumFractionDigits:dec,maximumFractionDigits:dec});};
  function countUp(el){
    var to=parseFloat(el.dataset.count), dec=+(el.dataset.dec||0), pre=el.dataset.pre||'', suf=el.dataset.suf||'';
    if(isStatic){el.textContent=pre+fmt(to,dec)+suf;return;}
    var dur=+(el.dataset.dur||1600), t0=null, delay=+(el.dataset.delay||0);
    function step(t){ if(t0===null)t0=t; var p=Math.min(1,(t-t0)/dur); var e=1-Math.pow(2,-10*p); if(p===1)e=1;
      el.textContent=pre+fmt(to*e,dec)+suf; if(p<1)requestAnimationFrame(step);}
    setTimeout(function(){requestAnimationFrame(step);},delay);
  }
  var counters=[].slice.call(document.querySelectorAll('[data-count]'));
  if(!isStatic){counters.forEach(function(el){var dec=+(el.dataset.dec||0);el.textContent=(el.dataset.pre||'')+fmt(0,dec)+(el.dataset.suf||'');});}

  /* reveal on scroll */
  var targets=[].slice.call(document.querySelectorAll('[data-reveal],[data-waffle],.map,[data-counter-scope]'));
  if(isStatic){ targets.forEach(function(t){t.classList.add('in');}); counters.forEach(countUp); }
  else{
    var io=new IntersectionObserver(function(es){es.forEach(function(e){ if(e.isIntersecting){ var t=e.target; t.classList.add('in');
      (t.matches('[data-count]')?[t]:[].slice.call(t.querySelectorAll('[data-count]'))).forEach(function(c){ if(!c.dataset.done){c.dataset.done=1;countUp(c);} });
      io.unobserve(t);} });},{threshold:.18,rootMargin:'0px 0px -6% 0px'});
    targets.forEach(function(t){io.observe(t);});
    var io2=new IntersectionObserver(function(es){es.forEach(function(e){ if(e.isIntersecting){var c=e.target; if(!c.dataset.done){c.dataset.done=1;countUp(c);} io2.unobserve(c);} });},{threshold:.4});
    counters.forEach(function(c){ if(!c.closest('[data-reveal],[data-counter-scope]')) io2.observe(c); });
  }

  /* progress bar + nav state */
  var bar=document.querySelector('.progress i'), nav=document.querySelector('.nav'), hero=document.querySelector('.hero');
  var ticking=false;
  function onScroll(){ ticking=false; var h=document.documentElement.scrollHeight-innerHeight; var p=h>0?scrollY/h:0;
    if(bar)bar.style.setProperty('--p',p.toFixed(4));
    if(nav){ nav.classList.toggle('scrolled',scrollY>24); var hb=hero?hero.getBoundingClientRect().bottom:0; nav.classList.toggle('light',hb<70);} }
  addEventListener('scroll',function(){ if(!ticking){ticking=true;requestAnimationFrame(onScroll);} },{passive:true});
  onScroll();

  /* pointer tilt + sheen on floating cards */
  if(!isStatic){ document.querySelectorAll('.fcard').forEach(function(c){
    c.addEventListener('animationend',function(){c.style.animation='none';c.style.opacity='1';});
    var raf=null, MAX=6, hideT=null;
    function upd(x,y){ var r=c.getBoundingClientRect(); var px=Math.max(0,Math.min(100,(x-r.left)/r.width*100)), py=Math.max(0,Math.min(100,(y-r.top)/r.height*100));
      if(raf)cancelAnimationFrame(raf); raf=requestAnimationFrame(function(){ c.style.setProperty('--px',px+'%');c.style.setProperty('--py',py+'%');
        c.style.setProperty('--ry',((px-50)/50*MAX).toFixed(2)+'deg');c.style.setProperty('--rx',(-(py-50)/50*MAX).toFixed(2)+'deg');c.style.setProperty('--s','1.03');}); }
    function reset(){ if(raf)cancelAnimationFrame(raf); raf=requestAnimationFrame(function(){c.style.setProperty('--rx','0deg');c.style.setProperty('--ry','0deg');c.style.setProperty('--s','1');}); }
    c.addEventListener('mousemove',function(e){upd(e.clientX,e.clientY);});
    c.addEventListener('mouseleave',reset);
    c.addEventListener('touchstart',function(e){var t=e.touches[0];if(!t)return;clearTimeout(hideT);upd(t.clientX,t.clientY);c.classList.add('lit');},{passive:true});
    c.addEventListener('touchmove',function(e){var t=e.touches[0];if(t)upd(t.clientX,t.clientY);},{passive:true});
    function end(){reset();hideT=setTimeout(function(){c.classList.remove('lit');},400);}
    c.addEventListener('touchend',end);c.addEventListener('touchcancel',end);
  }); }

  /* pointer-following brand glow on buttons */
  document.querySelectorAll('.mk-glow').forEach(function(btn){
    btn.addEventListener('pointermove',function(e){var r=btn.getBoundingClientRect();btn.style.setProperty('--gx',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');});
  });

  /* scroll-spy spotlight rail on step lists */
  if(!isStatic){ document.querySelectorAll('.steps').forEach(function(list){
    var rail=document.createElement('span'); rail.className='rail'; rail.setAttribute('aria-hidden','true'); list.appendChild(rail);
    var steps=[].slice.call(list.querySelectorAll('.step')); var cur=null;
    function spy(){ var mid=innerHeight*0.45, best=null, bd=1e9;
      steps.forEach(function(s){var r=s.getBoundingClientRect(); var d=Math.abs((r.top+r.height/2)-mid); if(d<bd){bd=d;best=s;}});
      var lr=list.getBoundingClientRect(); var inView=lr.bottom>innerHeight*0.2&&lr.top<innerHeight*0.8;
      list.classList.toggle('spy',inView);
      if(best&&best!==cur){ if(cur)cur.classList.remove('active'); best.classList.add('active'); cur=best;
        rail.style.top=(best.offsetTop+22)+'px'; rail.style.height=(best.offsetHeight-44)+'px'; } }
    addEventListener('scroll',function(){requestAnimationFrame(spy);},{passive:true}); spy();
  }); }

  /* sortable tables */
  document.querySelectorAll('table[data-sortable]').forEach(function(tb){
    var ths=[].slice.call(tb.querySelectorAll('thead th'));
    ths.forEach(function(th,ci){ var b=th.querySelector('button'); if(!b)return;
      b.addEventListener('click',function(){ var dir=th.getAttribute('aria-sort')==='descending'?'ascending':'descending';
        ths.forEach(function(o){o.removeAttribute('aria-sort');}); th.setAttribute('aria-sort',dir);
        var body=tb.tBodies[0]; var rows=[].slice.call(body.rows);
        rows.sort(function(a,b2){ var x=a.cells[ci].dataset.v, y=b2.cells[ci].dataset.v; var nx=parseFloat(x), ny=parseFloat(y);
          var r=(!isNaN(nx)&&!isNaN(ny))?nx-ny:String(x).localeCompare(String(y)); return dir==='ascending'?r:-r; });
        var first=new Map(); rows.forEach(function(r){first.set(r,r.getBoundingClientRect().top);});
        rows.forEach(function(r){body.appendChild(r);});
        if(!isStatic){ rows.forEach(function(r){ var dy=first.get(r)-r.getBoundingClientRect().top; if(!dy)return;
          r.classList.remove('moving'); r.style.transform='translateY('+dy+'px)'; r.getBoundingClientRect();
          r.classList.add('moving'); r.style.transform=''; r.addEventListener('transitionend',function h(){r.classList.remove('moving');r.removeEventListener('transitionend',h);}); }); } });
    });
  });
})();
