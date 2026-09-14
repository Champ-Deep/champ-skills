/**
 * Generates the "10 Ways [Client] Can Use B2B Data" showcase deck.
 *
 * Usage:
 *   node generate_deck.js path/to/config.json path/to/output.pptx
 *
 * See ../assets/config.example.json for the input schema.
 * See ../references/ten_ways_playbook.md for the methodology each slide follows.
 *
 * Palette lives in the PALETTES block below. Only "lakeb2b" and "champions" are
 * confirmed brand colors (from the org's brand-guideline skills). If config.brand
 * is anything else, this falls back to lakeb2b and prints a warning — don't invent
 * a palette for a brand you haven't confirmed.
 */
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const [, , configPath, outPath] = process.argv;
if (!configPath || !outPath) {
  console.error("Usage: node generate_deck.js path/to/config.json path/to/output.pptx");
  process.exit(1);
}
const cfg = JSON.parse(fs.readFileSync(configPath, "utf8"));

const PALETTES = {
  lakeb2b: { PRIMARY: "6D08BE", DEEP: "3D0570", ACCENT: "FFB703", ALT: "E8033A", INFO: "0095A0", brandLabel: "LakeB2B  ·  Enabling Growth" },
  champions: { PRIMARY: "2D2D2D", DEEP: "1A1A1A", ACCENT: "C9A84C", ALT: "B0654A", INFO: "3A3A3A", brandLabel: "Champions Group  ·  Empowering Innovation" }
};
let brandKey = (cfg.brand || "lakeb2b").toLowerCase();
if (!PALETTES[brandKey]) {
  console.warn(`Unrecognized brand "${cfg.brand}" — falling back to lakeb2b palette. Confirm the real brand colors before shipping.`);
  brandKey = "lakeb2b";
}
const PAL = PALETTES[brandKey];
const PRIMARY = PAL.PRIMARY, DEEP = PAL.DEEP, ACCENT = PAL.ACCENT, ALT = PAL.ALT, INFO = PAL.INFO;
const WHITE = "FFFFFF", INK = "1A1030", GRAY = "6B6478", LIGHTBG = "F7F5FC", CARDLINE = "E1DCEF";

const CLIENT = cfg.client_name || "[Client Name]";
const TARGET = (cfg.target_account_example && !cfg.target_account_example.use_generic && cfg.target_account_example.real_name)
  ? cfg.target_account_example.real_name
  : (cfg.target_account_example && cfg.target_account_example.generic_descriptor) || "a priority target account";

let pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const PGW = 13.333, PGH = 7.5;

function slide(bg = WHITE) { let s = pres.addSlide(); s.background = { color: bg }; return s; }
function pageNum(s, n, total) {
  s.addText(`${String(n).padStart(2, "0")} / ${total}`, { x: PGW - 1.3, y: PGH - 0.45, w: 1.0, h: 0.3, fontFace: "Montserrat", fontSize: 9, color: GRAY, align: "right", margin: 0 });
}
function footer(s) {
  s.addText(PAL.brandLabel, { x: 0.6, y: PGH - 0.45, w: 5, h: 0.3, fontFace: "Montserrat", fontSize: 9, color: GRAY, margin: 0 });
}
function appFrame(s, x, y, w, h, barColor, label) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: WHITE }, line: { color: CARDLINE, width: 1 }, shadow: { type: "outer", color: PRIMARY, opacity: 0.18, blur: 10, offset: 3, angle: 90 } });
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.34, rectRadius: 0.08, fill: { color: barColor }, line: { type: "none" } });
  s.addShape(pres.ShapeType.rect, { x, y: y + 0.17, w, h: 0.17, fill: { color: barColor }, line: { type: "none" } });
  [0, 1, 2].forEach(i => s.addShape(pres.ShapeType.ellipse, { x: x + 0.12 + i * 0.18, y: y + 0.12, w: 0.09, h: 0.09, fill: { color: WHITE }, line: { type: "none" } }));
  if (label) s.addText(label, { x: x + 0.7, y, w: w - 1, h: 0.34, fontFace: "Montserrat", fontSize: 9, color: WHITE, valign: "middle", margin: 0 });
}
function bulletBox(s, x, y, w, h, heading, pts) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText(heading, { x: x + 0.3, y: y + 0.15, w: w - 0.6, h: 0.35, fontFace: "Montserrat", fontSize: 12, bold: true, color: DEEP, margin: 0 });
  s.addText(pts.map((p, i) => ({ text: p, options: { bullet: { code: "2022", color: ACCENT }, breakLine: i !== pts.length - 1, paraSpaceAfter: 8 } })), {
    x: x + 0.3, y: y + 0.55, w: w - 0.6, h: h - 0.75, fontFace: "Montserrat", fontSize: 11, color: INK, margin: 0, valign: "top"
  });
}

const INCLUDE_EVENT_SLIDE = cfg.include_event_slide !== false; // on by default
const TOTAL_SLIDES = INCLUDE_EVENT_SLIDE ? 13 : 12;
function useCaseSlide(n, title, oneLiner, fillRight) {
  let s = slide(WHITE);
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 4.5, h: PGH, fill: { color: LIGHTBG } });
  s.addText(String(n).padStart(2, "0"), { x: 0.5, y: 0.55, w: 2.2, h: 1.1, fontFace: "Montserrat", fontSize: 54, bold: true, color: ACCENT, margin: 0 });
  s.addShape(pres.ShapeType.line, { x: 0.55, y: 1.75, w: 1.0, h: 0, line: { color: PRIMARY, width: 2.5 } });
  s.addText(title, { x: 0.5, y: 2.0, w: 3.7, h: 1.5, fontFace: "Montserrat", fontSize: 21, bold: true, color: INK, margin: 0, lineSpacingMultiple: 1.05 });
  s.addText(oneLiner, { x: 0.5, y: 3.55, w: 3.7, h: 2.5, fontFace: "Montserrat", fontSize: 12.5, color: GRAY, margin: 0, lineSpacingMultiple: 1.35, valign: "top" });
  s.addText(`SAMPLE FOR ${CLIENT.toUpperCase()}`, { x: 4.9, y: 0.5, w: 8, h: 0.3, fontFace: "Montserrat", fontSize: 10, bold: true, color: PRIMARY, charSpacing: 1.5, margin: 0 });
  fillRight(s);
  pageNum(s, n + 1, TOTAL_SLIDES);
  footer(s);
}

// ---------- Slide 1: Title ----------
{
  let s = slide(DEEP);
  s.addShape(pres.ShapeType.ellipse, { x: 9.8, y: -1.5, w: 5, h: 5, fill: { color: PRIMARY }, line: { type: "none" } });
  s.addShape(pres.ShapeType.ellipse, { x: 11.3, y: 4.5, w: 3.5, h: 3.5, fill: { color: ACCENT }, line: { type: "none" } });
  s.addText(PAL.brandLabel.toUpperCase(), { x: 0.7, y: 0.65, w: 9, h: 0.35, fontFace: "Montserrat", fontSize: 12, bold: true, color: ACCENT, charSpacing: 2, margin: 0 });
  const titleCount = INCLUDE_EVENT_SLIDE ? "11 Ways" : "10 Ways";
  s.addText(`${titleCount} Our B2B Data\nDrives Growth for ${CLIENT}`, { x: 0.7, y: 1.6, w: 10.8, h: 2.4, fontFace: "Montserrat", fontSize: 36, bold: true, color: WHITE, margin: 0, lineSpacingMultiple: 1.08 });
  s.addText(`Personalized data, campaign, and market-expansion blueprint for ${CLIENT} (${cfg.client_domain || ""}).`, { x: 0.7, y: 3.95, w: 9, h: 0.7, fontFace: "Montserrat", fontSize: 14, color: "D8CDEF", margin: 0 });
  pageNum(s, 0, TOTAL_SLIDES);
  s.addText(PAL.brandLabel, { x: 0.7, y: PGH - 0.5, w: 4, h: 0.3, fontFace: "Montserrat", fontSize: 9, color: "B9A6DD", margin: 0 });
}

// ---------- Slide 2: Email ----------
useCaseSlide(1, "Email Campaigns",
  `A ready-to-send, personalized outreach template built from our contact and firmographic layers — targeting ${cfg.icp?.title || "your priority buyers"} at ${cfg.icp?.industry_descriptor || "your target segment"}.`,
  (s) => {
    appFrame(s, 4.9, 0.95, 7.7, 3.2, DEEP, "New Message");
    s.addText([
      { text: "To:  ", options: { bold: true, color: GRAY } }, { text: "{{First Name}} @ {{Company Name}}\n", options: { color: INK } },
      { text: "Subject:  ", options: { bold: true, color: GRAY } }, { text: `Reducing operating costs at {{Company Name}}\n\n`, options: { color: INK, bold: true } },
      { text: `Hi {{First Name}},\n\nI noticed {{Company Name}} is ${cfg.trigger_context || "growing fast in your space"}. As teams scale, they often face ${cfg.primary_pain || "rising operating complexity"}.\n\n${CLIENT} helps organizations like {{Company Name}} ${cfg.primary_outcome || "simplify and reduce avoidable cost"}.\n\n` },
      { text: "Would a brief conversation next week be useful?", options: { italic: true } }
    ], { x: 5.15, y: 1.55, w: 7.2, h: 2.5, fontFace: "Calibri", fontSize: 11, color: INK, margin: 0, lineSpacingMultiple: 1.25, valign: "top" });

    const audienceLine = cfg.audience_count_illustrative
      ? `We identified an estimated ${Number(cfg.audience_count_contacts || 0).toLocaleString()} decision-makers matching this ICP (illustrative — confirm against live counts).`
      : `We identified ${Number(cfg.audience_count_contacts || 0).toLocaleString()} decision-makers who match this ICP.`;
    bulletBox(s, 4.9, 4.35, 7.7, 2.35, "Why it works", [
      "Built from verified, role-matched contact records — not scraped lists",
      "Trigger events pulled straight into the opening line",
      audienceLine
    ]);
  });

// ---------- Slide 3: Social ----------
useCaseSlide(2, "Social Campaign Outreach",
  "LinkedIn and Meta creative built around lookalike audiences drawn from our firmographic and intent data — not platform guesswork.",
  (s) => {
    appFrame(s, 4.9, 0.95, 3.7, 3.1, "0A66C2", "LinkedIn Ad");
    s.addShape(pres.ShapeType.rect, { x: 5.05, y: 1.55, w: 3.4, h: 1.15, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
    s.addText(`Is ${CLIENT} losing revenue\nto disconnected data?`, { x: 5.15, y: 1.62, w: 3.2, h: 0.9, fontFace: "Montserrat", fontSize: 11, bold: true, color: INK, margin: 0 });
    s.addText(`Sponsored · Reaching: ${cfg.icp?.title || "target buyers"}`, { x: 5.05, y: 2.8, w: 3.4, h: 0.5, fontFace: "Montserrat", fontSize: 8.5, color: GRAY, margin: 0 });
    s.addShape(pres.ShapeType.roundRect, { x: 5.05, y: 3.4, w: 1.7, h: 0.4, rectRadius: 0.05, fill: { color: "0A66C2" }, line: { type: "none" } });
    s.addText("Download Guide", { x: 5.05, y: 3.4, w: 1.7, h: 0.4, fontFace: "Montserrat", fontSize: 9, color: WHITE, align: "center", valign: "middle", margin: 0 });

    appFrame(s, 8.9, 0.95, 3.7, 3.1, "0866FF", "Meta Ads");
    s.addShape(pres.ShapeType.rect, { x: 9.05, y: 1.55, w: 3.4, h: 1.15, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
    s.addText("Grow with better\ncustomer intelligence", { x: 9.15, y: 1.62, w: 3.2, h: 0.9, fontFace: "Montserrat", fontSize: 11, bold: true, color: INK, margin: 0 });
    s.addText(`Custom audience seeded from ${CLIENT}'s ICP`, { x: 9.05, y: 2.8, w: 3.4, h: 0.5, fontFace: "Montserrat", fontSize: 8.5, color: GRAY, margin: 0 });
    s.addShape(pres.ShapeType.roundRect, { x: 9.05, y: 3.4, w: 1.6, h: 0.4, rectRadius: 0.05, fill: { color: "0866FF" }, line: { type: "none" } });
    s.addText("Book a Consult", { x: 9.05, y: 3.4, w: 1.6, h: 0.4, fontFace: "Montserrat", fontSize: 9, color: WHITE, align: "center", valign: "middle", margin: 0 });

    bulletBox(s, 4.9, 4.35, 7.7, 2.35, "Why it works", [
      "Custom & lookalike audiences seeded from the verified account universe, not platform defaults",
      "Buyer-committee targeting — not just one title",
      "Meta only where the ICP is consumer-adjacent (SMB owners, clinicians, retail, hospitality, education)"
    ]);
  });

// ---------- Slide 4: Telemarketing / AI Agent ----------
useCaseSlide(3, "Customer Acquisition — Telemarketing",
  "An AI voice agent script generated from verified contact and firmographic data, so every call opens with real context.",
  (s) => {
    appFrame(s, 4.9, 0.95, 7.7, 3.4, DEEP, "AI Agent Call — Live Transcript");
    const lines = [
      { spk: "AI Agent", t: `Hello, may I speak with {{First Name}}? This is Ava calling on behalf of ${CLIENT}. We work with organizations to help them ${cfg.primary_outcome || "solve a specific challenge"}.` },
      { spk: "Prospect", t: "Sure, go ahead." },
      { spk: "AI Agent", t: `Is ${cfg.primary_pain || "this challenge"} currently a priority for your team? Would you be open to a 20-minute discussion with a specialist?` }
    ];
    let yy = 1.55;
    lines.forEach(l => {
      s.addText(l.spk + ":", { x: 5.15, y: yy, w: 1.6, h: 0.3, fontFace: "Montserrat", fontSize: 10, bold: true, color: l.spk === "AI Agent" ? PRIMARY : INFO, margin: 0 });
      s.addText(l.t, { x: 5.15, y: yy + 0.28, w: 7.2, h: 0.85, fontFace: "Calibri", fontSize: 10.5, color: INK, margin: 0, lineSpacingMultiple: 1.2 });
      yy += 1.05;
    });
    bulletBox(s, 4.9, 4.55, 7.7, 2.15, "Why it works", [
      "Script auto-populates trigger events, title, and company detail per call",
      "Outcome taxonomy (interested / qualified / meeting booked / referred) feeds straight back into the CRM",
      "Scales outbound without scaling headcount — treat funnel numbers as illustrative until validated"
    ]);
  });

// ---------- Slide 5: SEO / AEO ----------
useCaseSlide(4, "SEO Optimization / AEO",
  "A snapshot of how AI answer engines and search already talk about this category — with competitors showing up, and the client absent.",
  (s) => {
    appFrame(s, 4.9, 0.95, 7.7, 3.6, INK, `Search — "${cfg.seo_search_query || "best providers in this category"}"`);
    s.addShape(pres.ShapeType.rect, { x: 5.1, y: 1.55, w: 7.3, h: 0.55, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
    s.addText(`"${cfg.seo_search_query || "best providers in this category"}"`, { x: 5.25, y: 1.55, w: 7.0, h: 0.55, fontFace: "Calibri", fontSize: 12, italic: true, color: INK, valign: "middle", margin: 0 });
    const comps = (cfg.competitors && cfg.competitors.length ? cfg.competitors : ["Competitor A", "Competitor B", "Competitor C"]).slice(0, 3);
    let ry = 2.3;
    comps.forEach((c, i) => {
      s.addShape(pres.ShapeType.ellipse, { x: 5.15, y: ry + 0.03, w: 0.16, h: 0.16, fill: { color: INFO }, line: { type: "none" } });
      s.addText(`${c} — ranked #${i + 1}`, { x: 5.4, y: ry, w: 6.8, h: 0.3, fontFace: "Montserrat", fontSize: 11, color: INK, margin: 0 });
      ry += 0.42;
    });
    s.addShape(pres.ShapeType.roundRect, { x: 5.15, y: ry + 0.05, w: 7.05, h: 0.5, rectRadius: 0.06, fill: { color: "FDECEF" }, line: { color: ALT, width: 1 } });
    s.addText(`✕  ${CLIENT} — not mentioned`, { x: 5.3, y: ry + 0.05, w: 6.8, h: 0.5, fontFace: "Montserrat", fontSize: 11, bold: true, color: ALT, valign: "middle", margin: 0 });

    bulletBox(s, 4.9, 4.75, 7.7, 1.95, "Why it matters", [
      "Confirm this is a live, dated search before presenting it — never a fabricated screenshot",
      `Buyers now ask AI engines before Google — if competitors are cited and ${CLIENT} isn't, that's lost pipeline before a rep ever calls`
    ]);
  });

// ---------- Slide 6: Talent Acquisition ----------
useCaseSlide(5, "Talent Acquisition / Recruitment",
  "A passive-candidate pitch built from our professional database — reaching great candidates who aren't on job boards at all.",
  (s) => {
    const total = cfg.candidate_stats?.total || 0, passive = cfg.candidate_stats?.passive || 0;
    const activePct = total ? Math.round(((total - passive) / total) * 100) : 15;
    const passivePct = total ? Math.round((passive / total) * 100) : 85;
    s.addShape(pres.ShapeType.roundRect, { x: 4.9, y: 0.95, w: 3.7, h: 3.1, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
    s.addText("Job Boards", { x: 5.1, y: 1.1, w: 3.3, h: 0.35, fontFace: "Montserrat", fontSize: 12, bold: true, color: GRAY, margin: 0 });
    s.addText(`~${activePct}%`, { x: 5.1, y: 1.5, w: 3.3, h: 0.9, fontFace: "Montserrat", fontSize: 40, bold: true, color: GRAY, margin: 0 });
    s.addText("Active applicants only — already being chased by every competitor's recruiter.", { x: 5.1, y: 2.5, w: 3.3, h: 1.4, fontFace: "Montserrat", fontSize: 10.5, color: GRAY, margin: 0, valign: "top" });

    s.addShape(pres.ShapeType.roundRect, { x: 8.9, y: 0.95, w: 3.7, h: 3.1, rectRadius: 0.08, fill: { color: DEEP } });
    s.addText(`${brandKey === "champions" ? "Champions" : "LakeB2B"} Reach`, { x: 9.1, y: 1.1, w: 3.3, h: 0.35, fontFace: "Montserrat", fontSize: 12, bold: true, color: ACCENT, margin: 0 });
    s.addText(`~${passivePct}%`, { x: 9.1, y: 1.5, w: 3.3, h: 0.9, fontFace: "Montserrat", fontSize: 40, bold: true, color: WHITE, margin: 0 });
    s.addText("Passive, currently-employed candidates — reachable directly by title, skill, tenure.", { x: 9.1, y: 2.5, w: 3.3, h: 1.4, fontFace: "Montserrat", fontSize: 10.5, color: "E7DCF7", margin: 0, valign: "top" });

    bulletBox(s, 4.9, 4.35, 7.7, 2.35, "Sample pitch opener", [
      `"Hi {{First Name}} — your background at {{Current Company}} caught our attention for a role ${CLIENT} isn't advertising publicly yet. Not mass recruitment — open to a confidential chat?"`,
      cfg.candidate_stats?.illustrative ? `${total.toLocaleString()} qualified professionals identified, incl. ${passive.toLocaleString()} passive candidates (illustrative)` : `${total.toLocaleString()} qualified professionals identified, incl. ${passive.toLocaleString()} passive candidates`
    ]);
  });

// ---------- Slide 7: KOL / Buying Committee ----------
useCaseSlide(6, "KOL & Buyer Committee Identification",
  "Mapping who actually influences and signs off on a deal — not just the one contact who filled out a form.",
  (s) => {
    const roles = [
      { t: "Economic Buyer", r: "CEO / CFO / BU Head", c: PRIMARY },
      { t: "Technical Evaluator", r: "CIO / CTO / IT Director", c: INFO },
      { t: "Champion", r: "Internal advocate", c: ACCENT },
      { t: "KOL / Influencer", r: "Analyst / Consultant", c: ALT }
    ];
    const cw = 1.75, gap = 0.15, x0 = 4.9, y0 = 1.3;
    roles.forEach((r, i) => {
      const x = x0 + i * (cw + gap);
      s.addShape(pres.ShapeType.ellipse, { x: x + (cw - 0.9) / 2, y: y0, w: 0.9, h: 0.9, fill: { color: r.c } });
      s.addText(r.t, { x, y: y0 + 1.0, w: cw, h: 0.6, fontFace: "Montserrat", fontSize: 10.5, bold: true, color: INK, align: "center", margin: 0, valign: "top" });
      s.addText(r.r, { x, y: y0 + 1.55, w: cw, h: 0.6, fontFace: "Montserrat", fontSize: 9, color: GRAY, align: "center", margin: 0, valign: "top" });
    });
    s.addShape(pres.ShapeType.line, { x: x0 + 0.5, y: y0 + 0.45, w: 6.9, h: 0, line: { color: CARDLINE, width: 1.5, dashType: "dash" } });

    bulletBox(s, 4.9, 3.9, 7.7, 2.8, "Why it works", [
      "Maps the full buying committee at target accounts, not just one inbound lead",
      "Surfaces industry KOLs/analysts worth briefing before a deal even opens",
      `Prioritized for ${(cfg.buying_committee_priority_accounts || 100).toLocaleString()} top accounts first — sequencing outreach by role lifts close rates`
    ]);
  });

// ---------- Slide 8: Data & Industry Analysis ----------
useCaseSlide(7, "Data & Industry Analysis",
  "The input-file and ICP analysis itself becomes a deliverable — match quality, segment mix, and whitespace mapped before any campaign runs.",
  (s) => {
    appFrame(s, 4.9, 0.95, 7.7, 3.2, DEEP, "Input File & ICP Snapshot");
    const bars = [["Match rate", 0.94], ["ICP fit — current file", 0.61], ["Whitespace vs. TAM", 0.38]];
    let by = 1.65;
    bars.forEach(([lbl, pct]) => {
      s.addText(lbl, { x: 5.15, y: by, w: 3.0, h: 0.3, fontFace: "Montserrat", fontSize: 10.5, color: INK, margin: 0 });
      s.addShape(pres.ShapeType.rect, { x: 5.15, y: by + 0.32, w: 6.9, h: 0.28, fill: { color: "EFEAFA" }, line: { type: "none" } });
      s.addShape(pres.ShapeType.rect, { x: 5.15, y: by + 0.32, w: 6.9 * pct, h: 0.28, fill: { color: PRIMARY }, line: { type: "none" } });
      s.addText(Math.round(pct * 100) + "%", { x: 5.15 + 6.9 * pct + 0.05, y: by + 0.28, w: 0.7, h: 0.35, fontFace: "Montserrat", fontSize: 10, bold: true, color: DEEP, margin: 0 });
      by += 0.85;
    });
    bulletBox(s, 4.9, 4.35, 7.7, 2.35, "Why it works", [
      "Turns a raw customer file into a QBR-ready analysis, not just a match report",
      `Flags expansion whitespace beyond ${cfg.client_industry || "the client's current segment"}`,
      "Sets a baseline to prove ROI against on every renewal"
    ]);
  });

// ---------- Slide 9: Org Chart / Profiles ----------
useCaseSlide(8, "Company Org Chart / Profiles",
  "Full account intelligence — org structure, reporting lines, and role profiles — so reps walk in already knowing the map.",
  (s) => {
    appFrame(s, 4.9, 0.95, 7.7, 3.4, DEEP, `Account Map — ${TARGET}`);
    const boxW = 1.9, boxH = 0.55;
    function box(x, y, t, sub) {
      s.addShape(pres.ShapeType.roundRect, { x, y, w: boxW, h: boxH, rectRadius: 0.05, fill: { color: LIGHTBG }, line: { color: PRIMARY, width: 1 } });
      s.addText(t, { x, y: y + 0.03, w: boxW, h: 0.28, fontFace: "Montserrat", fontSize: 9.5, bold: true, color: INK, align: "center", margin: 0 });
      s.addText(sub, { x, y: y + 0.29, w: boxW, h: 0.24, fontFace: "Montserrat", fontSize: 8, color: GRAY, align: "center", margin: 0 });
    }
    box(7.75, 1.55, "CEO", TARGET.length > 22 ? "Target Account" : TARGET);
    s.addShape(pres.ShapeType.line, { x: 8.7, y: 2.1, w: 0, h: 0.35, line: { color: CARDLINE, width: 1.5 } });
    s.addShape(pres.ShapeType.line, { x: 6.4, y: 2.45, w: 4.6, h: 0, line: { color: CARDLINE, width: 1.5 } });
    box(5.5, 2.45, "VP Sales", "Direct report");
    box(7.75, 2.45, "VP Marketing", "Direct report");
    box(10.0, 2.45, "VP Eng", "Direct report");
    s.addShape(pres.ShapeType.line, { x: 6.45, y: 3.0, w: 0, h: 0.35, line: { color: CARDLINE, width: 1.5 } });
    box(5.5, 3.35, "Dir. Sales Ops", "Champion");

    bulletBox(s, 4.9, 4.55, 7.7, 2.15, "Why it works", [
      "Reps see reporting lines and role profiles before the first call",
      "De-risks multi-threading into an account — no more guessing who else to loop in"
    ]);
  });

// ---------- Slide 10: LLM / API ----------
useCaseSlide(9, "Powering LLM & API Infrastructure",
  "The same verified dataset that fuels campaigns also powers structured API and LLM/RAG pipelines — real-time enrichment at the point of use.",
  (s) => {
    appFrame(s, 4.9, 0.95, 7.7, 3.4, INK, "POST /v1/enrich");
    s.addShape(pres.ShapeType.rect, { x: 5.05, y: 1.55, w: 7.4, h: 2.65, fill: { color: "12101E" } });
    const code = [
      "{", `  "company": "${(TARGET || "target_co").toLowerCase().replace(/\s+/g, "_")}",`,
      `  "industry": "${cfg.client_industry || "target industry"}",`,
      '  "intent_signals": ["pricing_page", "competitor_search"],', '  "buying_committee": 4,', '  "confidence": 0.94', "}"
    ];
    s.addText(code.join("\n"), { x: 5.25, y: 1.65, w: 7.0, h: 2.5, fontFace: "Consolas", fontSize: 11, color: "9BE38A", margin: 0, lineSpacingMultiple: 1.25 });

    bulletBox(s, 4.9, 4.55, 7.7, 2.15, "Why it works", [
      "One of the largest verified B2B datasets available — confirm the current, verified figure before quoting size externally",
      "API-first access means enrichment happens inline, not as a batch afterthought"
    ]);
  });

// ---------- Slide 11: Platform ----------
useCaseSlide(10, "A Platform Connecting You to Your TAM",
  `A branded, always-on portal — "${cfg.platform_concept_name || CLIENT + " Connect"}" — giving ${CLIENT}'s own team self-serve access to their total addressable market.`,
  (s) => {
    appFrame(s, 4.9, 0.95, 7.7, 3.4, DEEP, cfg.platform_concept_name || `${CLIENT} Growth Platform`);
    const tam = cfg.tam || {};
    const cells = [
      [Number(tam.companies || 0).toLocaleString(), "Companies in TAM"],
      [Number(tam.contacts || 0).toLocaleString(), "Verified contacts"],
      [`${tam.current_penetration_pct ?? "—"}%`, "Currently penetrated"],
      ["Live", "Refresh cadence"]
    ];
    const cw = 1.85, gap = 0.05, x0 = 5.1, y0 = 1.65;
    cells.forEach((c, i) => {
      const x = x0 + i * (cw + gap);
      s.addShape(pres.ShapeType.roundRect, { x, y: y0, w: cw, h: 1.5, rectRadius: 0.06, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
      s.addText(c[0], { x, y: y0 + 0.25, w: cw, h: 0.6, fontFace: "Montserrat", fontSize: 18, bold: true, color: DEEP, align: "center", margin: 0 });
      s.addText(c[1], { x: x + 0.1, y: y0 + 0.9, w: cw - 0.2, h: 0.55, fontFace: "Montserrat", fontSize: 9, color: GRAY, align: "center", margin: 0, valign: "top" });
    });
    s.addText(tam.illustrative ? "TAM figures illustrative — confirm against live platform counts before external use." : "Filter by industry, geo, tech stack, and intent — export or push straight to CRM.",
      { x: 5.1, y: 3.35, w: 7.3, h: 0.4, fontFace: "Montserrat", fontSize: 10, italic: true, color: GRAY, margin: 0 });

    bulletBox(s, 4.9, 4.55, 7.7, 2.15, "Why it works", [
      "Moves the relationship from a periodic data drop to a standing, self-serve platform",
      "Every login is a renewal touchpoint — the account team sees usage, not just an invoice"
    ]);
  });

// ---------- Slide 12 (optional): Event & Webinar Attendee Acceleration ----------
if (INCLUDE_EVENT_SLIDE) {
  const ev = cfg.event || {};
  const format = ev.format || "executive roundtable lunch";
  const evTitle = ev.title || `AI-Powered Quality Intelligence — ${format.charAt(0).toUpperCase() + format.slice(1)}`;
  const evCity = ev.city || "your target region";
  const houseRate = ev.house_rsvp_pct ?? 8;
  const icpRate = ev.icp_rsvp_pct ?? 22;
  useCaseSlide(11, "Event & Webinar Attendee Acceleration",
    `Turn a webinar, plant-tour lunch, or executive roundtable from a generic invite blast into a targeted, buyer-committee-matched guest list — with a predictable RSVP lift.`,
    (s) => {
      appFrame(s, 4.9, 0.95, 7.7, 2.05, DEEP, "Event Invite");
      s.addText([
        { text: `You're invited: `, options: { bold: true, color: INK } }, { text: `${evTitle}\n`, options: { bold: true, color: PRIMARY } },
        { text: `${format === "webinar" ? "Live webinar" : "In-person · " + evCity} · {{Date}}\n\n`, options: { color: GRAY } },
        { text: `Hi {{First Name}} — as {{Company Name}} ${cfg.trigger_context || "grows in this space"}, we're hosting a small group of ${cfg.icp?.title || "peers"} to discuss ${cfg.primary_pain || "the challenge your team is facing"}. Seats are limited.` }
      ], { x: 5.15, y: 1.55, w: 7.2, h: 1.35, fontFace: "Calibri", fontSize: 10.5, color: INK, margin: 0, lineSpacingMultiple: 1.2, valign: "top" });

      // RSVP comparison bars
      s.addShape(pres.ShapeType.roundRect, { x: 4.9, y: 3.2, w: 7.7, h: 1.5, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
      s.addText("Predicted RSVP rate", { x: 5.15, y: 3.32, w: 5, h: 0.3, fontFace: "Montserrat", fontSize: 11, bold: true, color: DEEP, margin: 0 });
      [["House list (generic invite)", houseRate, GRAY], [`ICP-matched invite list`, icpRate, PRIMARY]].forEach(([lbl, pct, color], i) => {
        const by = 3.68 + i * 0.5;
        s.addText(lbl, { x: 5.15, y: by, w: 2.6, h: 0.3, fontFace: "Montserrat", fontSize: 9.5, color: INK, margin: 0 });
        s.addShape(pres.ShapeType.rect, { x: 7.85, y: by + 0.02, w: 4.4, h: 0.22, fill: { color: "EFEAFA" }, line: { type: "none" } });
        s.addShape(pres.ShapeType.rect, { x: 7.85, y: by + 0.02, w: 4.4 * (pct / 30), h: 0.22, fill: { color }, line: { type: "none" } });
        s.addText(pct + "%", { x: 7.85 + 4.4 * (pct / 30) + 0.05, y: by - 0.03, w: 0.6, h: 0.32, fontFace: "Montserrat", fontSize: 9.5, bold: true, color: DEEP, margin: 0 });
      });

      bulletBox(s, 4.9, 4.9, 7.7, 1.8, "Why it works", [
        "Invite list drawn from the same firmographic + intent layer as every other campaign — not a static house list",
        "Personalized by role and trigger event, with a no-show follow-up sequence built in",
        "Post-event engagement (attended / no-show / requested follow-up) feeds straight back into lead scoring"
      ]);
    });
}

// ---------- Slide 13: Closing ----------
{
  let s = slide(DEEP);
  s.addShape(pres.ShapeType.ellipse, { x: -2, y: 4, w: 5, h: 5, fill: { color: PRIMARY }, line: { type: "none" } });
  const chCount = INCLUDE_EVENT_SLIDE ? "Eleven" : "Ten";
  s.addText(`${chCount} channels. One dataset.`, { x: 0.7, y: 1.2, w: 11, h: 1.0, fontFace: "Montserrat", fontSize: 34, bold: true, color: WHITE, margin: 0 });
  s.addText(`Every use case in this deck draws from the same verified B2B data reservoir, personalized for ${CLIENT}.`, { x: 0.7, y: 2.25, w: 9.5, h: 0.9, fontFace: "Montserrat", fontSize: 14, color: "D8CDEF", margin: 0 });
  const items = ["Email", "Social", "Telemarketing", "SEO/AEO", "Recruiting", "KOL Mapping", "Data Analysis", "Org Charts", "LLM/API", "Platform"];
  if (INCLUDE_EVENT_SLIDE) items.push("Events");
  let ix = 0.7, iy = 3.6;
  items.forEach((it, i) => {
    s.addShape(pres.ShapeType.roundRect, { x: ix, y: iy, w: 2.1, h: 0.55, rectRadius: 0.27, fill: { color: PRIMARY }, line: { type: "none" } });
    s.addText(`${i + 1}. ${it}`, { x: ix, y: iy, w: 2.1, h: 0.55, fontFace: "Montserrat", fontSize: 10.5, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    ix += 2.25;
    if ((i + 1) % 5 === 0) { ix = 0.7; iy += 0.75; }
  });
  pageNum(s, TOTAL_SLIDES - 1, TOTAL_SLIDES);
  s.addText(PAL.brandLabel, { x: 0.7, y: PGH - 0.5, w: 4, h: 0.3, fontFace: "Montserrat", fontSize: 9, color: "B9A6DD", margin: 0 });
}

pres.writeFile({ fileName: outPath }).then(() => console.log("Wrote " + outPath));
