# HTML Structure Reference

This file contains the full CSS scaffold and component patterns for the campaign plan document. Copy and adapt — do not reproduce verbatim; customize to the prospect's brand.

---

## Full CSS Scaffold

```css
:root {
  /* Override these with brand-derived colors */
  --primary:     #0E1238;
  --primary-light: #1a1f54;
  --accent:      #CAA05C;
  --accent-light: #e8c078;
  --accent-pale: #f5e9d3;
  --white:       #FFFFFF;
  --off-white:   #F8F7F4;
  --grey-100:    #F2F1EE;
  --grey-200:    #E5E3DC;
  --grey-600:    #6B6759;
  --grey-800:    #2C2A25;
  --success:     #2D6A4F;
  --font-serif:  'Playfair Display', Georgia, serif;
  --font-sans:   'DM Sans', Arial, sans-serif;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { font-family: var(--font-serif); background: var(--off-white); color: var(--grey-800); }

/* SIDEBAR NAV */
.sidenav {
  position: fixed; left: 0; top: 0; width: 240px; height: 100vh;
  background: var(--primary); padding: 32px 0; overflow-y: auto; z-index: 100;
}
.sidenav-logo { padding: 0 24px 32px; border-bottom: 1px solid rgba(202,160,92,0.3); }
.sidenav-logo span { display: block; font-size: 11px; letter-spacing: 3px; color: var(--accent); text-transform: uppercase; margin-bottom: 6px; font-family: var(--font-sans); }
.sidenav-logo strong { display: block; font-size: 15px; color: var(--white); line-height: 1.4; }
.sidenav ul { list-style: none; margin-top: 16px; }
.sidenav ul li a {
  display: block; padding: 11px 24px; color: rgba(255,255,255,0.65);
  text-decoration: none; font-family: var(--font-sans); font-size: 12px;
  letter-spacing: 0.5px; transition: all 0.2s; border-left: 3px solid transparent;
}
.sidenav ul li a:hover, .sidenav ul li a.active {
  color: var(--accent); border-left-color: var(--accent); background: rgba(202,160,92,0.08);
}
.sidenav ul li.nav-group {
  padding: 20px 24px 6px; font-size: 10px; letter-spacing: 2px;
  color: rgba(255,255,255,0.3); text-transform: uppercase; font-family: var(--font-sans);
}
.main { margin-left: 240px; min-height: 100vh; }

/* HERO */
.hero {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 50%, #0a0d2a 100%);
  padding: 80px 60px; position: relative; overflow: hidden;
}
.hero::before {
  content: ''; position: absolute; top: -50%; right: -10%; width: 600px; height: 600px;
  border: 1px solid rgba(202,160,92,0.15); border-radius: 50%;
}
.hero::after {
  content: ''; position: absolute; top: -20%; right: 10%; width: 400px; height: 400px;
  border: 1px solid rgba(202,160,92,0.08); border-radius: 50%;
}
.hero-tag {
  display: inline-block; background: rgba(202,160,92,0.15); border: 1px solid rgba(202,160,92,0.4);
  color: var(--accent); padding: 6px 16px; border-radius: 3px; font-size: 11px;
  letter-spacing: 3px; text-transform: uppercase; font-family: var(--font-sans); margin-bottom: 24px;
}
.hero h1 { font-size: 42px; color: var(--white); line-height: 1.2; max-width: 700px; margin-bottom: 16px; font-weight: normal; }
.hero h1 span { color: var(--accent); }
.hero p { color: rgba(255,255,255,0.7); font-size: 17px; max-width: 600px; line-height: 1.7; margin-bottom: 32px; }
.hero-meta { display: flex; gap: 40px; flex-wrap: wrap; }
.hero-meta-item span { display: block; font-family: var(--font-sans); font-size: 10px; letter-spacing: 2px; color: rgba(255,255,255,0.4); text-transform: uppercase; margin-bottom: 4px; }
.hero-meta-item strong { color: var(--accent); font-size: 14px; font-family: var(--font-sans); }
.hero-badges { display: flex; gap: 12px; margin-top: 32px; flex-wrap: wrap; }
.badge { padding: 6px 14px; border-radius: 3px; font-family: var(--font-sans); font-size: 11px; font-weight: bold; }
.badge-accent { background: var(--accent); color: var(--primary); }
.badge-outline { border: 1px solid rgba(255,255,255,0.3); color: rgba(255,255,255,0.7); }

/* SECTIONS */
.section { padding: 60px 60px; border-bottom: 1px solid var(--grey-200); }
.section:last-child { border-bottom: none; }
.section-tag { font-family: var(--font-sans); font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--accent); margin-bottom: 10px; }
.section h2 { font-size: 30px; color: var(--primary); margin-bottom: 8px; font-weight: normal; }
.section-desc { color: var(--grey-600); font-size: 16px; line-height: 1.7; margin-bottom: 36px; max-width: 700px; }

/* CARDS */
.card-grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.card-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.card-grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.card {
  background: var(--white); border: 1px solid var(--grey-200); border-radius: 6px;
  padding: 28px; position: relative; overflow: hidden;
}
.card-accent-left::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--accent); }
.card-dark { background: var(--primary); color: var(--white); border-radius: 6px; padding: 32px 28px; }
.card-dark h3 { color: var(--accent); font-size: 16px; letter-spacing: 1px; margin-bottom: 10px; font-family: var(--font-sans); }
.card-dark h4 { color: var(--white); font-size: 20px; margin-bottom: 12px; font-weight: normal; }
.card-dark p { color: rgba(255,255,255,0.7); font-size: 13px; line-height: 1.7; }

/* EMAIL MOCK COMPONENTS */
.email-card { background: var(--white); border-radius: 8px; overflow: hidden; box-shadow: 0 4px 24px rgba(14,18,56,0.08); margin-bottom: 48px; }
.email-meta-row { display: flex; gap: 12px; align-items: baseline; padding: 8px 0; border-bottom: 1px solid var(--grey-100); font-family: var(--font-sans); }
.email-meta-label { font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--grey-600); min-width: 90px; }
.email-meta-val { font-size: 13px; color: var(--grey-800); }
.email-type-badge { display: inline-block; padding: 4px 12px; border-radius: 3px; background: var(--accent); color: var(--primary); font-size: 10px; letter-spacing: 2px; font-family: var(--font-sans); font-weight: bold; }
.email-mock { background: #F0F0F0; padding: 24px; }
.em-preheader { background: #e8e8e8; color: #999; font-family: var(--font-sans); font-size: 11px; padding: 8px 20px; text-align: center; }
.em-header-top { background: var(--primary); padding: 12px 32px; display: flex; justify-content: space-between; align-items: center; }
.em-logo { color: var(--accent); font-size: 13px; letter-spacing: 2px; font-family: var(--font-sans); font-weight: bold; text-transform: uppercase; }
.em-logo-sub { font-size: 10px; color: rgba(255,255,255,0.5); font-family: var(--font-sans); letter-spacing: 1.5px; }
.em-header-links { display: flex; gap: 16px; }
.em-header-links a { color: rgba(255,255,255,0.5); font-family: var(--font-sans); font-size: 11px; text-decoration: none; }
.em-header-main {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  padding: 48px 32px; text-align: center; border-bottom: 3px solid var(--accent);
}
.em-header-main h2 { color: var(--white); font-size: 26px; margin-bottom: 12px; font-weight: normal; }
.em-hero-p { color: rgba(255,255,255,0.8); font-size: 15px; line-height: 1.7; max-width: 480px; margin: 0 auto; font-family: var(--font-sans); }
.em-wrapper { max-width: 600px; margin: 0 auto; background: var(--white); padding: 32px; }
.em-para { font-family: var(--font-sans); font-size: 14px; line-height: 1.8; color: #333; margin-bottom: 20px; }
.em-numbered-item {
  display: flex; gap: 16px; align-items: flex-start;
  background: var(--grey-100); border-radius: 6px; padding: 20px; margin-bottom: 16px;
}
.em-num-badge {
  width: 32px; height: 32px; border-radius: 50%; background: var(--accent);
  color: var(--primary); font-family: var(--font-sans); font-size: 13px;
  font-weight: bold; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.em-testimonial { background: var(--off-white); border-left: 3px solid var(--accent); padding: 24px 28px; margin: 24px 0; position: relative; }
.em-testimonial-quote { font-size: 48px; color: var(--accent); line-height: 1; font-family: var(--font-serif); position: absolute; top: 8px; left: 20px; opacity: 0.4; }
.em-testimonial-text { font-size: 15px; font-style: italic; color: var(--grey-800); line-height: 1.7; padding-left: 28px; margin-bottom: 16px; font-family: var(--font-serif); }
.em-testimonial-footer { display: flex; align-items: center; gap: 12px; padding-left: 28px; }
.em-avatar { width: 36px; height: 36px; border-radius: 50%; background: var(--accent); display: flex; align-items: center; justify-content: center; color: var(--primary); font-weight: bold; font-family: var(--font-sans); font-size: 13px; }
.em-testimonial-footer cite { font-family: var(--font-sans); font-size: 12px; color: var(--grey-600); font-style: normal; }
.em-checklist { background: var(--primary); border-radius: 6px; padding: 24px 28px; margin: 24px 0; }
.em-checklist h4 { color: var(--accent); font-family: var(--font-sans); font-size: 12px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px; }
.em-check-item { display: flex; gap: 10px; align-items: flex-start; margin-bottom: 10px; }
.em-check-icon { color: var(--accent); font-size: 14px; flex-shrink: 0; margin-top: 1px; }
.em-check-item span { color: rgba(255,255,255,0.85); font-family: var(--font-sans); font-size: 13px; line-height: 1.6; }
.em-cta-section { background: var(--accent-pale); text-align: center; padding: 32px; margin: 24px 0; border-radius: 6px; }
.em-cta-section p { font-family: var(--font-sans); font-size: 14px; color: var(--grey-800); line-height: 1.7; margin-bottom: 20px; }
.em-btn { display: inline-block; background: var(--primary); color: var(--white); padding: 14px 32px; border-radius: 4px; font-family: var(--font-sans); font-size: 13px; letter-spacing: 1px; text-decoration: none; font-weight: 600; text-transform: uppercase; }
.em-no-obligation { font-size: 11px; color: var(--grey-600); margin-top: 12px; font-family: var(--font-sans); }
.em-footer { background: var(--grey-100); padding: 20px 32px; text-align: center; }
.em-footer p { font-family: var(--font-sans); font-size: 11px; color: var(--grey-600); line-height: 1.8; }
.em-footer a { color: var(--grey-600); text-decoration: none; }
.em-stats { display: flex; background: var(--primary); border-radius: 4px; overflow: hidden; margin: 24px 0; }
.em-stat { flex: 1; padding: 20px; text-align: center; border-right: 1px solid rgba(202,160,92,0.2); }
.em-stat:last-child { border-right: none; }
.em-stat strong { display: block; font-size: 24px; color: var(--accent); font-family: var(--font-serif); margin-bottom: 4px; }
.em-stat span { font-size: 11px; color: rgba(255,255,255,0.6); font-family: var(--font-sans); letter-spacing: 1px; }

/* TABLES */
.table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.data-table { width: 100%; border-collapse: collapse; font-family: var(--font-sans); font-size: 13px; min-width: 600px; }
.data-table th { background: var(--primary); color: var(--accent); padding: 12px 16px; text-align: left; font-size: 11px; font-weight: normal; letter-spacing: 1px; }
.data-table td { padding: 12px 16px; border-bottom: 1px solid var(--grey-200); vertical-align: top; }
.data-table tr:nth-child(even) td { background: var(--grey-100); }
.data-table tr:hover td { background: var(--accent-pale); }
.cal-na { color: var(--grey-600); font-style: italic; font-size: 12px; }

/* MOBILE */
.mobile-header {
  display: none; position: fixed; top: 0; left: 0; right: 0; z-index: 200;
  background: var(--primary); height: 56px; align-items: center;
  padding: 0 20px; justify-content: space-between;
  border-bottom: 2px solid var(--accent);
}
.mobile-header-title { color: var(--accent); font-size: 13px; letter-spacing: 2px; text-transform: uppercase; font-family: var(--font-sans); }
.hamburger { background: none; border: none; cursor: pointer; padding: 6px; display: flex; flex-direction: column; gap: 5px; }
.hamburger span { display: block; width: 22px; height: 2px; background: var(--accent); border-radius: 2px; transition: all 0.3s; }
.nav-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 150; }
.nav-overlay.open { display: block; }
.sidenav.open { transform: translateX(0) !important; }

@media (max-width: 900px) {
  .card-grid-3, .card-grid-4 { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 768px) {
  .mobile-header { display: flex; }
  .sidenav { transform: translateX(-100%); transition: transform 0.3s ease; }
  .main { margin-left: 0; padding-top: 56px; }
  .hero { padding: 40px 24px; }
  .hero h1 { font-size: 28px; }
  .hero-meta { flex-wrap: wrap; gap: 20px; }
  .section { padding: 40px 24px; }
  .section h2 { font-size: 24px; }
  .card-grid-2, .card-grid-3, .card-grid-4 { grid-template-columns: 1fr; }
  .em-stats { flex-direction: column; }
  .em-stat { border-right: none; border-bottom: 1px solid rgba(202,160,92,0.2); }
  .em-wrapper { padding: 20px 16px; }
}
@media (max-width: 480px) {
  .hero h1 { font-size: 22px; }
  .hero, .section { padding: 28px 16px; }
}
```

---

## Mobile Nav JavaScript

Place immediately after `<body>` tag, before the sidenav:

```html
<header class="mobile-header">
  <span class="mobile-header-title">[Company Short Name]</span>
  <button class="hamburger" onclick="toggleNav()" aria-label="Open navigation">
    <span></span><span></span><span></span>
  </button>
</header>
<div class="nav-overlay" id="navOverlay" onclick="toggleNav()"></div>
<script>
function toggleNav(){
  document.querySelector('.sidenav').classList.toggle('open');
  document.getElementById('navOverlay').classList.toggle('open');
}
document.querySelectorAll('.sidenav a').forEach(function(a){
  a.addEventListener('click', function(){
    if(window.innerWidth<=768){
      document.querySelector('.sidenav').classList.remove('open');
      document.getElementById('navOverlay').classList.remove('open');
    }
  });
});
</script>
```

---

## Sidebar Nav Structure

```html
<nav class="sidenav">
  <div class="sidenav-logo">
    <span>Campaign Plan</span>
    <strong>[Company Name]</strong>
  </div>
  <ul>
    <li class="nav-group">Strategy</li>
    <li><a href="#champ">CHAMP Analysis</a></li>
    <li><a href="#personas">Audience Personas</a></li>
    <li><a href="#messaging">Messaging</a></li>
    <li class="nav-group">Execution</li>
    <li><a href="#channels">Channels</a></li>
    <li><a href="#email">Email Templates</a></li>
    <li><a href="#linkedin">LinkedIn Templates</a></li>
    <li><a href="#calendar">Content Calendar</a></li>
    <li class="nav-group">Measurement</li>
    <li><a href="#budget">Budget</a></li>
    <li><a href="#kpis">KPI Framework</a></li>
    <li><a href="#pivot">Pivot Plan</a></li>
  </ul>
</nav>
```

---

## Google Fonts Import (inside `<head>`)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
```
