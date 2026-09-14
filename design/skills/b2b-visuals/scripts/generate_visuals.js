/**
 * Generates 12 separate, standalone growth-visual images (16:9) for a client,
 * from a config.json (see ../assets/config.example.json).
 *
 * Usage:
 *   node generate_visuals.js path/to/config.json path/to/output_dir/
 *
 * Pipeline: builds one pptxgenjs slide per image (LAYOUT_WIDE = 13.333x7.5in,
 * true 16:9), exports the deck to PDF via LibreOffice, then rasterizes each
 * page to its own high-res PNG via pdftoppm. The result is 12 independent
 * image files, never a combined collage — that split-into-files step happens
 * in this script's own postGenerate() using child_process, so a single
 * `node generate_visuals.js ...` call is enough; nothing else to run by hand.
 *
 * Read references/twelve_images_playbook.md before changing any slide copy —
 * it has the required headline pattern and visual elements per image.
 */
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const pptxgen = require("pptxgenjs");

const [, , configPath, outDir] = process.argv;
if (!configPath || !outDir) {
  console.error("Usage: node generate_visuals.js path/to/config.json path/to/output_dir/");
  process.exit(1);
}
const cfg = JSON.parse(fs.readFileSync(configPath, "utf8"));
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const PRIMARY = (cfg.brand_colors && cfg.brand_colors.primary) || "6D08BE";
const DEEP = shade(PRIMARY, -0.35);
const ACCENT = "FFB703";
const ALT = "E8033A";
const INFO = "0095A0";
const INK = "1A1030", GRAY = "6B6478", LIGHTBG = "F7F5FC", CARDLINE = "E1DCEF", WHITE = "FFFFFF";

function shade(hex, amt) {
  const n = parseInt(hex, 16);
  let r = (n >> 16) & 0xff, g = (n >> 8) & 0xff, b = n & 0xff;
  r = Math.max(0, Math.min(255, Math.round(r + r * amt)));
  g = Math.max(0, Math.min(255, Math.round(g + g * amt)));
  b = Math.max(0, Math.min(255, Math.round(b + b * amt)));
  return [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("").toUpperCase();
}

const CLIENT = cfg.client_name || "[Client Name]";
const TARGET = (cfg.target_account_example && !cfg.target_account_example.use_generic && cfg.target_account_example.real_name)
  ? cfg.target_account_example.real_name
  : (cfg.target_account_example && cfg.target_account_example.generic_descriptor) || "a priority target account";

let pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in — true 16:9
const PGW = 13.333, PGH = 7.5;

// ---- Shared poster chrome ----
function posterSlide(eyebrow, headlineParts, fillBody) {
  let s = pres.addSlide();
  s.background = { color: WHITE };
  // top band
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: PGW, h: 1.05, fill: { color: DEEP } });
  s.addText(eyebrow.toUpperCase(), { x: 0.6, y: 0.32, w: 10, h: 0.4, fontFace: "Montserrat", fontSize: 12, bold: true, color: ACCENT, charSpacing: 2, margin: 0 });
  // headline (array of {text, color, bold})
  s.addText(headlineParts, { x: 0.6, y: 1.3, w: 12.1, h: 1.15, fontFace: "Montserrat", fontSize: 27, bold: true, color: INK, margin: 0, lineSpacingMultiple: 1.05 });
  fillBody(s);
  // footer
  s.addText("Powered by LakeB2B", { x: PGW - 3.0, y: PGH - 0.4, w: 2.6, h: 0.3, fontFace: "Montserrat", fontSize: 9.5, color: GRAY, align: "right", margin: 0 });
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: PGH - 0.42, w: 0.14, h: 0.14, fill: { color: PRIMARY } });
  s.addText(cfg.client_industry || "", { x: 0.85, y: PGH - 0.44, w: 6, h: 0.3, fontFace: "Montserrat", fontSize: 9.5, color: GRAY, margin: 0 });
  return s;
}
function appFrame(s, x, y, w, h, barColor, label) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: WHITE }, line: { color: CARDLINE, width: 1 }, shadow: { type: "outer", color: PRIMARY, opacity: 0.18, blur: 10, offset: 3, angle: 90 } });
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.32, rectRadius: 0.08, fill: { color: barColor }, line: { type: "none" } });
  s.addShape(pres.ShapeType.rect, { x, y: y + 0.16, w, h: 0.16, fill: { color: barColor }, line: { type: "none" } });
  [0, 1, 2].forEach((i) => s.addShape(pres.ShapeType.ellipse, { x: x + 0.12 + i * 0.17, y: y + 0.11, w: 0.08, h: 0.08, fill: { color: WHITE }, line: { type: "none" } }));
  if (label) s.addText(label, { x: x + 0.65, y, w: w - 0.9, h: 0.32, fontFace: "Montserrat", fontSize: 9, color: WHITE, valign: "middle", margin: 0 });
}
function tag(s, x, y, text, color) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w: text.length * 0.075 + 0.3, h: 0.32, rectRadius: 0.16, fill: { color, transparency: 88 }, line: { color, width: 1 } });
  s.addText(text, { x, y, w: text.length * 0.075 + 0.3, h: 0.32, fontFace: "Montserrat", fontSize: 9.5, bold: true, color, align: "center", valign: "middle", margin: 0 });
}

const HL = (parts) => parts; // headline helper: array of {text, color?, bold?}
const nameRun = (t) => ({ text: t, options: { color: PRIMARY } });
const plainRun = (t) => ({ text: t, options: {} });

// ============ Image 1 — Personalized Email Campaign ============
posterSlide("LakeB2B Data Activation", HL([plainRun("How "), nameRun(CLIENT), plainRun(` Can Reach ${cfg.icp?.title || "Priority Buyers"} Through Personalized Email`)]), (s) => {
  tag(s, 0.6, 2.55, cfg.icp?.geography || "Target Geography", INFO);
  tag(s, 3.1, 2.55, cfg.icp?.industry_descriptor || "Target Industry", PRIMARY);
  appFrame(s, 0.6, 3.1, 7.6, 3.5, DEEP, "New Message");
  s.addText([
    { text: "To:  ", options: { bold: true, color: GRAY } }, { text: "{{First Name}} @ {{Company Name}}\n", options: { color: INK } },
    { text: "Subject:  ", options: { bold: true, color: GRAY } }, { text: `Reducing operating costs at {{Company Name}}\n\n`, options: { color: INK, bold: true } },
    { text: `Hi {{First Name}},\n\nI noticed {{Company Name}} is ${cfg.trigger_context || "growing fast in your space"}. As teams scale, they often face ${cfg.primary_pain || "rising operating complexity"}.\n\n${CLIENT} helps organizations like {{Company Name}} ${cfg.primary_outcome || "simplify and reduce avoidable cost"}.\n\n` },
    { text: "Would a brief conversation next week be useful?", options: { italic: true } }
  ], { x: 0.85, y: 3.7, w: 7.1, h: 2.7, fontFace: "Calibri", fontSize: 11, color: INK, margin: 0, lineSpacingMultiple: 1.25, valign: "top" });

  s.addShape(pres.ShapeType.roundRect, { x: 8.55, y: 3.1, w: 4.15, h: 3.5, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Campaign flow", { x: 8.8, y: 3.3, w: 3.7, h: 0.3, fontFace: "Montserrat", fontSize: 12, bold: true, color: DEEP, margin: 0 });
  ["Data match & verify", "Personalize by role + trigger", "Send + reminder sequence", "Reply → meeting booked"].forEach((step, i) => {
    const y = 3.75 + i * 0.68;
    s.addShape(pres.ShapeType.ellipse, { x: 8.8, y, w: 0.32, h: 0.32, fill: { color: PRIMARY } });
    s.addText(String(i + 1), { x: 8.8, y, w: 0.32, h: 0.32, fontFace: "Montserrat", fontSize: 11, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(step, { x: 9.25, y: y + 0.02, w: 3.3, h: 0.32, fontFace: "Montserrat", fontSize: 10.5, color: INK, valign: "middle", margin: 0 });
  });
  const audLine = cfg.audience_count_illustrative
    ? `~${Number(cfg.audience_count_contacts || 0).toLocaleString()} matched contacts (preliminary estimate)`
    : `${Number(cfg.audience_count_contacts || 0).toLocaleString()} matched contacts`;
  s.addText(audLine, { x: 0.6, y: 6.75, w: 8, h: 0.3, fontFace: "Montserrat", fontSize: 10.5, italic: true, color: GRAY, margin: 0 });
});

// ============ Image 2 — LinkedIn and Social Outreach ============
posterSlide("LakeB2B Data Activation", HL([plainRun("Engage "), nameRun(`${cfg.icp?.title || "Target Decision Makers"}`), plainRun(" Across Social Channels")]), (s) => {
  const includeMeta = !!cfg.include_meta_ad;
  const cardW = includeMeta ? 3.9 : 5.9;
  appFrame(s, 0.6, 2.4, cardW, 2.5, "0A66C2", "LinkedIn — Connect");
  s.addText(`Hi {{First Name}}, following ${CLIENT}'s growth in ${cfg.client_industry || "your space"} — we help teams tackle ${cfg.primary_pain || "this challenge"}. Worth connecting?`, { x: 0.85, y: 2.95, w: cardW - 0.5, h: 1.7, fontFace: "Calibri", fontSize: 10.5, color: INK, margin: 0, lineSpacingMultiple: 1.25, valign: "top" });

  appFrame(s, 0.6 + cardW + 0.25, 2.4, cardW, 2.5, "004182", "LinkedIn — Sponsored Ad");
  s.addText(`Is your team losing time to ${cfg.primary_pain || "disconnected data"}?`, { x: 0.85 + cardW + 0.25, y: 2.95, w: cardW - 0.5, h: 0.8, fontFace: "Montserrat", fontSize: 12.5, bold: true, color: INK, margin: 0 });
  s.addShape(pres.ShapeType.roundRect, { x: 0.85 + cardW + 0.25, y: 4.35, w: 1.9, h: 0.4, rectRadius: 0.06, fill: { color: "0A66C2" }, line: { type: "none" } });
  s.addText("Download Guide", { x: 0.85 + cardW + 0.25, y: 4.35, w: 1.9, h: 0.4, fontFace: "Montserrat", fontSize: 9.5, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });

  if (includeMeta) {
    const x3 = 0.6 + (cardW + 0.25) * 2;
    appFrame(s, x3, 2.4, cardW, 2.5, "0866FF", "Meta Ads");
    s.addText("Grow with better customer intelligence", { x: x3 + 0.25, y: 2.95, w: cardW - 0.5, h: 0.8, fontFace: "Montserrat", fontSize: 12.5, bold: true, color: INK, margin: 0 });
    s.addShape(pres.ShapeType.roundRect, { x: x3 + 0.25, y: 4.35, w: 1.7, h: 0.4, rectRadius: 0.06, fill: { color: "0866FF" }, line: { type: "none" } });
    s.addText("Book a Consult", { x: x3 + 0.25, y: 4.35, w: 1.7, h: 0.4, fontFace: "Montserrat", fontSize: 9.5, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
  }

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 5.25, w: 12.1, h: 1.35, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Sequence: Connect → Follow-up (value share) → Sponsored ad retarget" + (includeMeta ? " → Meta lookalike" : ""), { x: 0.9, y: 5.45, w: 11.5, h: 0.4, fontFace: "Montserrat", fontSize: 11.5, bold: true, color: DEEP, margin: 0 });
  s.addText(`Filters: ${cfg.icp?.title || "target titles"} · ${cfg.icp?.industry_descriptor || "target industry"} · ${cfg.icp?.geography || "target geography"}`, { x: 0.9, y: 5.85, w: 11.5, h: 0.4, fontFace: "Montserrat", fontSize: 10.5, color: GRAY, margin: 0 });
});

// ============ Image 3 — AI-Agent Telemarketing ============
posterSlide("LakeB2B Data Activation", HL([plainRun("Turn Verified B2B Contacts into Qualified Conversations for "), nameRun(CLIENT)]), (s) => {
  appFrame(s, 0.6, 2.4, 7.6, 3.9, DEEP, "AI Agent Call — Live Transcript");
  const lines = [
    { spk: "AI Agent", t: `Hello, may I speak with {{First Name}}? This is Ava calling on behalf of ${CLIENT}. We help teams ${cfg.primary_outcome || "solve a specific challenge"}.` },
    { spk: "Prospect", t: "Sure, go ahead." },
    { spk: "AI Agent", t: `Is ${cfg.primary_pain || "this challenge"} a priority right now? Open to a 20-minute call with a specialist?` }
  ];
  let yy = 2.95;
  lines.forEach((l) => {
    s.addText(l.spk + ":", { x: 0.85, y: yy, w: 1.6, h: 0.28, fontFace: "Montserrat", fontSize: 10, bold: true, color: l.spk === "AI Agent" ? PRIMARY : INFO, margin: 0 });
    s.addText(l.t, { x: 0.85, y: yy + 0.26, w: 7.1, h: 0.7, fontFace: "Calibri", fontSize: 10.5, color: INK, margin: 0, lineSpacingMultiple: 1.15 });
    yy += 0.98;
  });
  s.addText("Compliant with opt-out + do-not-call handling", { x: 0.85, y: 6.05, w: 7, h: 0.25, fontFace: "Montserrat", fontSize: 9.5, italic: true, color: GRAY, margin: 0 });

  s.addShape(pres.ShapeType.roundRect, { x: 8.55, y: 2.4, w: 4.15, h: 3.9, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Call disposition", { x: 8.8, y: 2.6, w: 3.7, h: 0.3, fontFace: "Montserrat", fontSize: 12, bold: true, color: DEEP, margin: 0 });
  ["Interested", "Qualified opportunity", "Meeting booked", "Call later", "Referred", "Not interested"].forEach((d, i) => {
    const y = 3.05 + i * 0.5;
    s.addShape(pres.ShapeType.ellipse, { x: 8.8, y: y + 0.03, w: 0.14, h: 0.14, fill: { color: i < 3 ? PRIMARY : GRAY }, line: { type: "none" } });
    s.addText(d, { x: 9.05, y, w: 3.4, h: 0.32, fontFace: "Montserrat", fontSize: 10.5, color: INK, margin: 0 });
  });
});

// ============ Image 4 — SEO/AEO Visibility ============
{
  const seo = cfg.seo_search || null;
  const hasReal = seo && seo.results && seo.results.length;
  const headline = hasReal && seo.client_rank
    ? HL([plainRun("Buyers See Other Names Before "), nameRun(CLIENT), plainRun(" — Here's the Search That Proves It")])
    : HL([plainRun("Help "), nameRun(CLIENT), plainRun(" Be Found Where Buyers Search and Ask AI")]);
  posterSlide("LakeB2B Data Activation", headline, (s) => {
    const query = (seo && seo.query) || cfg.seo_search_query || "best providers in this category";
    const sourceLabel = hasReal ? `Live search — ${seo.source}` : "Illustrative search visibility analysis";
    appFrame(s, 0.6, 2.4, 7.6, 3.9, INK, sourceLabel);
    s.addShape(pres.ShapeType.rect, { x: 0.85, y: 3.0, w: 7.1, h: 0.5, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
    s.addText(`"${query}"`, { x: 1.0, y: 3.0, w: 6.8, h: 0.5, fontFace: "Calibri", fontSize: 11.5, italic: true, color: INK, valign: "middle", margin: 0 });
    let ry = 3.65;
    if (hasReal) {
      seo.results.slice(0, 5).forEach((r) => {
        const isClient = seo.client_rank && r.rank === seo.client_rank;
        s.addShape(pres.ShapeType.ellipse, { x: 0.9, y: ry + 0.03, w: 0.15, h: 0.15, fill: { color: isClient ? ALT : INFO }, line: { type: "none" } });
        s.addText(`#${r.rank} — ${r.name}`, { x: 1.15, y: ry, w: 6.6, h: 0.3, fontFace: "Montserrat", fontSize: 11, bold: !!isClient, color: isClient ? ALT : INK, margin: 0 });
        ry += 0.38;
      });
      if (!seo.client_rank) {
        s.addShape(pres.ShapeType.roundRect, { x: 0.9, y: ry + 0.05, w: 6.85, h: 0.45, rectRadius: 0.06, fill: { color: "FDECEF" }, line: { color: ALT, width: 1 } });
        s.addText(`✕  ${CLIENT} — not mentioned`, { x: 1.05, y: ry + 0.05, w: 6.6, h: 0.45, fontFace: "Montserrat", fontSize: 10.5, bold: true, color: ALT, valign: "middle", margin: 0 });
      }
    } else {
      (cfg.competitors || ["Competitor A", "Competitor B", "Competitor C"]).slice(0, 3).forEach((c, i) => {
        s.addShape(pres.ShapeType.ellipse, { x: 0.9, y: ry + 0.03, w: 0.15, h: 0.15, fill: { color: INFO }, line: { type: "none" } });
        s.addText(`${c} — ranked #${i + 1}`, { x: 1.15, y: ry, w: 6.6, h: 0.3, fontFace: "Montserrat", fontSize: 11, color: INK, margin: 0 });
        ry += 0.38;
      });
      s.addShape(pres.ShapeType.roundRect, { x: 0.9, y: ry + 0.05, w: 6.85, h: 0.45, rectRadius: 0.06, fill: { color: "FDECEF" }, line: { color: ALT, width: 1 } });
      s.addText(`✕  ${CLIENT} — not mentioned`, { x: 1.05, y: ry + 0.05, w: 6.6, h: 0.45, fontFace: "Montserrat", fontSize: 10.5, bold: true, color: ALT, valign: "middle", margin: 0 });
    }

    s.addShape(pres.ShapeType.roundRect, { x: 8.55, y: 2.4, w: 4.15, h: 3.9, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
    s.addText("Recommended content", { x: 8.8, y: 2.6, w: 3.7, h: 0.3, fontFace: "Montserrat", fontSize: 12, bold: true, color: DEEP, margin: 0 });
    ["Comparison pages", "Buyer guides & FAQs", "Original research", "Structured / AI-readable profiles", "Third-party mentions"].forEach((d, i) => {
      const y = 3.05 + i * 0.55;
      s.addShape(pres.ShapeType.ellipse, { x: 8.8, y: y + 0.03, w: 0.14, h: 0.14, fill: { color: ACCENT }, line: { type: "none" } });
      s.addText(d, { x: 9.05, y, w: 3.4, h: 0.34, fontFace: "Montserrat", fontSize: 10.5, color: INK, margin: 0 });
    });
  });
}

// ============ Image 5 — Talent Acquisition ============
posterSlide("LakeB2B Data Activation", HL([plainRun("Reach Specialist Talent Beyond Traditional Job Boards for "), nameRun(CLIENT)]), (s) => {
  const total = cfg.candidate_stats?.total || 0, passive = cfg.candidate_stats?.passive || 0;
  const activePct = total ? Math.round(((total - passive) / total) * 100) : 15;
  const passivePct = total ? Math.round((passive / total) * 100) : 85;
  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 2.4, w: 5.9, h: 2.6, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Job Boards", { x: 0.9, y: 2.6, w: 5.3, h: 0.35, fontFace: "Montserrat", fontSize: 13, bold: true, color: GRAY, margin: 0 });
  s.addText(`~${activePct}%`, { x: 0.9, y: 3.0, w: 5.3, h: 0.9, fontFace: "Montserrat", fontSize: 38, bold: true, color: GRAY, margin: 0 });
  s.addText("Active applicants only — already chased by every competitor's recruiter.", { x: 0.9, y: 3.9, w: 5.3, h: 1.0, fontFace: "Montserrat", fontSize: 11, color: GRAY, margin: 0, valign: "top" });

  s.addShape(pres.ShapeType.roundRect, { x: 6.75, y: 2.4, w: 5.95, h: 2.6, rectRadius: 0.08, fill: { color: DEEP } });
  s.addText("LakeB2B Reach", { x: 7.05, y: 2.6, w: 5.3, h: 0.35, fontFace: "Montserrat", fontSize: 13, bold: true, color: ACCENT, margin: 0 });
  s.addText(`~${passivePct}%`, { x: 7.05, y: 3.0, w: 5.3, h: 0.9, fontFace: "Montserrat", fontSize: 38, bold: true, color: WHITE, margin: 0 });
  s.addText("Passive, currently-employed candidates — reachable directly by title, skill, tenure.", { x: 7.05, y: 3.9, w: 5.3, h: 1.0, fontFace: "Montserrat", fontSize: 11, color: "E7DCF7", margin: 0, valign: "top" });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 5.25, w: 12.1, h: 1.3, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText(`"Hi {{First Name}} — your background at {{Current Company}} caught our attention for a role ${CLIENT} isn't advertising publicly yet. Not mass recruitment — open to a confidential chat?"`, {
    x: 0.9, y: 5.45, w: 11.5, h: 1.0, fontFace: "Calibri", fontSize: 11, italic: true, color: INK, margin: 0, lineSpacingMultiple: 1.25, valign: "top"
  });
});

// ============ Image 6 — KOL / Buying Committee ============
posterSlide("LakeB2B Data Activation", HL([plainRun("Map Every Stakeholder Influencing "), nameRun(CLIENT + "'s"), plainRun(" Purchase")]), (s) => {
  const roles = [
    { t: "Economic Buyer", r: "CEO / CFO / BU Head", c: PRIMARY },
    { t: "Technical Buyer", r: "CIO / CTO / IT Director", c: INFO },
    { t: "Business Sponsor", r: "VP, department head", c: DEEP },
    { t: "Champion", r: "Internal advocate", c: ACCENT },
    { t: "Procurement/Legal", r: "Gatekeepers", c: GRAY },
    { t: "KOL / Influencer", r: "Analyst / Consultant", c: ALT }
  ];
  const cw = 1.85, gap = 0.2, x0 = 0.6, y0 = 2.7;
  roles.forEach((r, i) => {
    const col = i % 6;
    const x = x0 + col * (cw + gap);
    s.addShape(pres.ShapeType.ellipse, { x: x + (cw - 0.85) / 2, y: y0, w: 0.85, h: 0.85, fill: { color: r.c } });
    s.addText(r.t, { x, y: y0 + 0.95, w: cw, h: 0.55, fontFace: "Montserrat", fontSize: 10.5, bold: true, color: INK, align: "center", margin: 0, valign: "top" });
    s.addText(r.r, { x, y: y0 + 1.45, w: cw, h: 0.5, fontFace: "Montserrat", fontSize: 9, color: GRAY, align: "center", margin: 0, valign: "top" });
  });
  s.addShape(pres.ShapeType.line, { x: x0 + 0.42, y: y0 + 0.42, w: 12.1 - 0.84, h: 0, line: { color: CARDLINE, width: 1.5, dashType: "dash" } });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 5.25, w: 12.1, h: 1.3, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText(`Priority accounts mapped first: ~${(cfg.buying_committee_priority_accounts || 100).toLocaleString()} — sequencing outreach by role, not blasting one contact.`, {
    x: 0.9, y: 5.5, w: 11.5, h: 0.8, fontFace: "Montserrat", fontSize: 12, color: INK, margin: 0, valign: "top"
  });
});

// ============ Image 7 — Data & Industry Analysis ============
posterSlide("LakeB2B Data Activation", HL([plainRun("Reveal Where "), nameRun(CLIENT + "'s"), plainRun(" Next Growth Opportunities Are Hiding")]), (s) => {
  appFrame(s, 0.6, 2.4, 7.6, 2.9, DEEP, "Input File & ICP Snapshot");
  const bars = [["Match rate", 0.94], ["ICP fit — current file", 0.61], ["Whitespace vs. TAM", 0.38]];
  let by = 3.0;
  bars.forEach(([lbl, pct]) => {
    s.addText(lbl, { x: 0.85, y: by, w: 2.6, h: 0.3, fontFace: "Montserrat", fontSize: 10.5, color: INK, margin: 0 });
    s.addShape(pres.ShapeType.rect, { x: 3.55, y: by + 0.02, w: 4.5, h: 0.26, fill: { color: "EFEAFA" }, line: { type: "none" } });
    s.addShape(pres.ShapeType.rect, { x: 3.55, y: by + 0.02, w: 4.5 * pct, h: 0.26, fill: { color: PRIMARY }, line: { type: "none" } });
    s.addText(Math.round(pct * 100) + "%", { x: 3.55 + 4.5 * pct + 0.08, y: by - 0.03, w: 0.6, h: 0.32, fontFace: "Montserrat", fontSize: 10, bold: true, color: DEEP, margin: 0 });
    by += 0.78;
  });

  s.addShape(pres.ShapeType.roundRect, { x: 8.55, y: 2.4, w: 4.15, h: 2.9, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Priority-account universe", { x: 8.8, y: 2.6, w: 3.7, h: 0.3, fontFace: "Montserrat", fontSize: 11.5, bold: true, color: DEEP, margin: 0 });
  const tam = cfg.tam || {};
  [["TAM", tam.companies], ["SAM (matched contacts)", tam.contacts], ["Current penetration", (tam.current_penetration_pct ?? "—") + "%"]].forEach(([l, v], i) => {
    s.addText(typeof v === "number" ? Number(v).toLocaleString() : v, { x: 8.8, y: 3.0 + i * 0.72, w: 3.6, h: 0.4, fontFace: "Montserrat", fontSize: 16, bold: true, color: DEEP, margin: 0 });
    s.addText(l, { x: 8.8, y: 3.38 + i * 0.72, w: 3.6, h: 0.3, fontFace: "Montserrat", fontSize: 9, color: GRAY, margin: 0 });
  });

  s.addText(tam.illustrative ? "Figures shown are a preliminary estimate, pending validation against live platform data." : "Whitespace, adjacent sectors, and cross-sell opportunities mapped from live platform data.", {
    x: 0.6, y: 5.55, w: 12.1, h: 0.5, fontFace: "Montserrat", fontSize: 10.5, italic: true, color: GRAY, margin: 0
  });
});

// ============ Image 8 — Org Chart / Account Profiles ============
posterSlide("LakeB2B Data Activation", HL([plainRun("Understand Priority Accounts from the Inside Out")]), (s) => {
  appFrame(s, 0.6, 2.4, 7.6, 3.9, DEEP, `Account Map — ${TARGET}`);
  const boxW = 2.0, boxH = 0.6;
  function box(x, y, t, sub) {
    s.addShape(pres.ShapeType.roundRect, { x, y, w: boxW, h: boxH, rectRadius: 0.05, fill: { color: LIGHTBG }, line: { color: PRIMARY, width: 1 } });
    s.addText(t, { x, y: y + 0.04, w: boxW, h: 0.3, fontFace: "Montserrat", fontSize: 10, bold: true, color: INK, align: "center", margin: 0 });
    s.addText(sub, { x, y: y + 0.32, w: boxW, h: 0.26, fontFace: "Montserrat", fontSize: 8.5, color: GRAY, align: "center", margin: 0 });
  }
  box(3.4, 2.85, "CEO", TARGET.length > 22 ? "Target Account" : TARGET);
  s.addShape(pres.ShapeType.line, { x: 4.4, y: 3.45, w: 0, h: 0.35, line: { color: CARDLINE, width: 1.5 } });
  s.addShape(pres.ShapeType.line, { x: 1.85, y: 3.8, w: 5.1, h: 0, line: { color: CARDLINE, width: 1.5 } });
  box(0.85, 3.8, "VP Sales", "Direct report");
  box(3.4, 3.8, "VP Marketing", "Direct report");
  box(5.95, 3.8, "VP Eng/IT", "Direct report");
  s.addShape(pres.ShapeType.line, { x: 4.4, y: 4.4, w: 0, h: 0.35, line: { color: CARDLINE, width: 1.5 } });
  box(3.4, 4.75, "Director, Ops", "Champion (fictional sample)");

  s.addShape(pres.ShapeType.roundRect, { x: 8.55, y: 2.4, w: 4.15, h: 3.9, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Executive profile (sample)", { x: 8.8, y: 2.6, w: 3.7, h: 0.3, fontFace: "Montserrat", fontSize: 11.5, bold: true, color: DEEP, margin: 0 });
  s.addText([
    { text: "Role: ", options: { bold: true } }, { text: "Director, Operations\n" },
    { text: "Focus: ", options: { bold: true } }, { text: `${cfg.primary_pain || "operational efficiency"}\n` },
    { text: "Opener: ", options: { bold: true } }, { text: `"Noticed {{Company Name}} is ${cfg.trigger_context || "scaling fast"}..."`, options: { italic: true } }
  ], { x: 8.8, y: 3.0, w: 3.7, h: 2.9, fontFace: "Montserrat", fontSize: 10.5, color: INK, margin: 0, lineSpacingMultiple: 1.3, valign: "top" });
});

// ============ Image 9 — LLM/API ============
posterSlide("LakeB2B Data Activation", HL([plainRun("Power "), nameRun(CLIENT + "'s"), plainRun(" AI, CRM and Applications with B2B Intelligence")]), (s) => {
  appFrame(s, 0.6, 2.4, 7.6, 3.9, INK, "POST /v1/enrich");
  s.addShape(pres.ShapeType.rect, { x: 0.85, y: 3.0, w: 7.1, h: 3.0, fill: { color: "12101E" } });
  const code = [
    "{", `  "company": "target_co_domain.com",`, `  "industry": "${cfg.client_industry || "target industry"}",`,
    '  "intent_signals": ["pricing_page", "competitor_search"],', '  "buying_committee": 4,', '  "confidence": 0.94', "}"
  ];
  s.addText(code.join("\n"), { x: 1.05, y: 3.15, w: 6.7, h: 2.7, fontFace: "Consolas", fontSize: 11.5, color: "9BE38A", margin: 0, lineSpacingMultiple: 1.3 });

  s.addShape(pres.ShapeType.roundRect, { x: 8.55, y: 2.4, w: 4.15, h: 3.9, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Powers", { x: 8.8, y: 2.6, w: 3.7, h: 0.3, fontFace: "Montserrat", fontSize: 11.5, bold: true, color: DEEP, margin: 0 });
  ["CRM enrichment", "AI sales copilot", "Lead scoring", "Account recommendations", "Market intelligence"].forEach((d, i) => {
    const y = 3.0 + i * 0.6;
    s.addShape(pres.ShapeType.ellipse, { x: 8.8, y: y + 0.03, w: 0.14, h: 0.14, fill: { color: ACCENT }, line: { type: "none" } });
    s.addText(d, { x: 9.05, y, w: 3.4, h: 0.36, fontFace: "Montserrat", fontSize: 11, color: INK, margin: 0 });
  });
});

// ============ Image 10 — Platform ============
posterSlide("LakeB2B Data Activation", HL([plainRun("Build the Digital Platform That Connects "), nameRun(CLIENT), plainRun(" to Its Market")]), (s) => {
  const platformName = cfg.platform_concept_name || `${CLIENT} Connect`;
  appFrame(s, 0.6, 2.4, 12.1, 3.9, DEEP, platformName);
  const cells = [
    ["Directory", "Searchable company + people profiles"],
    ["AI Search", "Natural-language buyer/partner discovery"],
    ["Community", "Content hub, events, forums"],
    ["Marketplace", "Lead gen, subscriptions, sponsorships"]
  ];
  const cw = 2.75, gap = 0.25, x0 = 0.95, y0 = 3.1;
  cells.forEach((c, i) => {
    const x = x0 + i * (cw + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y: y0, w: cw, h: 1.9, rectRadius: 0.06, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
    s.addText(c[0], { x: x + 0.15, y: y0 + 0.2, w: cw - 0.3, h: 0.4, fontFace: "Montserrat", fontSize: 13, bold: true, color: DEEP, margin: 0 });
    s.addText(c[1], { x: x + 0.15, y: y0 + 0.65, w: cw - 0.3, h: 1.1, fontFace: "Montserrat", fontSize: 9.5, color: GRAY, margin: 0, valign: "top" });
  });
  s.addText(`"${platformName}" — self-serve access to ${CLIENT}'s total addressable market, not a one-time file drop.`, {
    x: 0.95, y: 5.25, w: 11.4, h: 0.9, fontFace: "Montserrat", fontSize: 12, italic: true, color: GRAY, margin: 0
  });
});

// ============ Image 11 — Webinar ============
posterSlide("LakeB2B Data Activation", HL([plainRun("Fill "), nameRun(CLIENT), plainRun(" Webinars with the Right Decision Makers")]), (s) => {
  const wb = cfg.webinar || {};
  const wbTitle = wb.title || `${cfg.client_industry || "Industry"} Trends Webinar`;
  appFrame(s, 0.6, 2.4, 7.6, 2.3, DEEP, "Webinar Registration — Sample");
  s.addText([
    { text: `${wbTitle}\n`, options: { bold: true, color: PRIMARY, fontSize: 13 } },
    { text: "Live webinar · {{Sample Date}} · 45 min + Q&A\n\n", options: { color: GRAY } },
    { text: `Hi {{First Name}} — join ${cfg.icp?.title || "your peers"} for a session on ${cfg.primary_pain || "the challenge your team is facing"}.` }
  ], { x: 0.85, y: 3.0, w: 7.1, h: 1.6, fontFace: "Calibri", fontSize: 11, color: INK, margin: 0, lineSpacingMultiple: 1.2, valign: "top" });

  s.addShape(pres.ShapeType.roundRect, { x: 8.55, y: 2.4, w: 4.15, h: 2.3, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Reg. → attendance funnel", { x: 8.8, y: 2.55, w: 3.7, h: 0.3, fontFace: "Montserrat", fontSize: 11, bold: true, color: DEEP, margin: 0 });
  const regRate = wb.registration_pct ?? 12, attendRate = wb.attendance_pct ?? 45;
  [["ICP registration rate", regRate, PRIMARY], ["Show-up rate", attendRate, ACCENT]].forEach(([lbl, pct, color], i) => {
    const by = 2.95 + i * 0.6;
    s.addText(lbl, { x: 8.8, y: by, w: 1.9, h: 0.3, fontFace: "Montserrat", fontSize: 9.5, color: INK, margin: 0 });
    s.addShape(pres.ShapeType.rect, { x: 10.75, y: by + 0.02, w: 1.75, h: 0.22, fill: { color: "EFEAFA" }, line: { type: "none" } });
    s.addShape(pres.ShapeType.rect, { x: 10.75, y: by + 0.02, w: 1.75 * (pct / 50), h: 0.22, fill: { color }, line: { type: "none" } });
    s.addText(pct + "%", { x: 10.75 + 1.75 * (pct / 50) + 0.05, y: by - 0.02, w: 0.5, h: 0.3, fontFace: "Montserrat", fontSize: 9, bold: true, color: DEEP, margin: 0 });
  });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 4.95, w: 12.1, h: 1.6, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Registration list drawn from firmographic + intent data → reminder & no-show follow-up → poll/Q&A engagement feeds lead scoring → sales meeting.", {
    x: 0.9, y: 5.2, w: 11.5, h: 1.1, fontFace: "Montserrat", fontSize: 11.5, color: INK, margin: 0, valign: "top"
  });
});

// ============ Image 12 — Event Networking / Lunch ============
posterSlide("LakeB2B Data Activation", HL([plainRun("Convert Industry Events into High-Value Executive Meetings for "), nameRun(CLIENT)]), (s) => {
  const ev = cfg.event || {};
  const evTitle = ev.title || `${cfg.client_industry || "Industry"} Executive Roundtable — Sample`;
  appFrame(s, 0.6, 2.4, 7.6, 2.3, DEEP, "Event Invite — Sample");
  s.addText([
    { text: "You're invited: ", options: { bold: true, color: INK } }, { text: `${evTitle}\n`, options: { bold: true, color: PRIMARY } },
    { text: `In-person · ${ev.city || "your target region"} · {{Sample Date}}\n\n`, options: { color: GRAY } },
    { text: `Hi {{First Name}} — we're hosting a small group of ${cfg.icp?.title || "peers"} to discuss ${cfg.primary_pain || "the challenge your team is facing"}. Seats are limited.` }
  ], { x: 0.85, y: 3.0, w: 7.1, h: 1.6, fontFace: "Calibri", fontSize: 10.5, color: INK, margin: 0, lineSpacingMultiple: 1.2, valign: "top" });

  s.addShape(pres.ShapeType.roundRect, { x: 8.55, y: 2.4, w: 4.15, h: 2.3, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Predicted RSVP rate", { x: 8.8, y: 2.55, w: 3.7, h: 0.3, fontFace: "Montserrat", fontSize: 11, bold: true, color: DEEP, margin: 0 });
  const houseRate = ev.house_rsvp_pct ?? 8, icpRate = ev.icp_rsvp_pct ?? 22;
  [["House list", houseRate, GRAY], ["ICP-matched list", icpRate, PRIMARY]].forEach(([lbl, pct, color], i) => {
    const by = 2.95 + i * 0.6;
    s.addText(lbl, { x: 8.8, y: by, w: 1.9, h: 0.3, fontFace: "Montserrat", fontSize: 9.5, color: INK, margin: 0 });
    s.addShape(pres.ShapeType.rect, { x: 10.75, y: by + 0.02, w: 1.75, h: 0.22, fill: { color: "EFEAFA" }, line: { type: "none" } });
    s.addShape(pres.ShapeType.rect, { x: 10.75, y: by + 0.02, w: 1.75 * (pct / 30), h: 0.22, fill: { color }, line: { type: "none" } });
    s.addText(pct + "%", { x: 10.75 + 1.75 * (pct / 30) + 0.05, y: by - 0.02, w: 0.5, h: 0.3, fontFace: "Montserrat", fontSize: 9, bold: true, color: DEEP, margin: 0 });
  });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 4.95, w: 12.1, h: 1.6, rectRadius: 0.08, fill: { color: LIGHTBG }, line: { color: CARDLINE, width: 1 } });
  s.addText("Guest list from the same firmographic + intent layer → gets the whole buying committee in one room → post-event follow-up feeds lead scoring.", {
    x: 0.9, y: 5.2, w: 11.5, h: 1.1, fontFace: "Montserrat", fontSize: 11.5, color: INK, margin: 0, valign: "top"
  });
});

// ---- Build, then split into 12 separate PNGs ----
const IMAGE_NAMES = [
  "01_email_campaign", "02_social_outreach", "03_ai_telemarketing", "04_seo_aeo_visibility",
  "05_talent_acquisition", "06_kol_buying_committee", "07_data_industry_analysis", "08_org_chart_account_profile",
  "09_llm_api", "10_client_platform", "11_webinar_invitation", "12_event_networking"
];

const tmpPptx = path.join(outDir, "_tmp_visuals.pptx");
pres.writeFile({ fileName: tmpPptx }).then(() => {
  execSync(`python3 /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf --outdir "${outDir}" "${tmpPptx}"`, { stdio: "inherit" });
  const pdfPath = path.join(outDir, "_tmp_visuals.pdf");
  execSync(`pdftoppm -png -r 200 "${pdfPath}" "${path.join(outDir, "_page")}"`, { stdio: "inherit" });
  // pdftoppm names pages _page-1.png, _page-2.png, ... (or -01 depending on count); normalize.
  const files = fs.readdirSync(outDir).filter((f) => f.startsWith("_page"));
  files.sort((a, b) => {
    const na = parseInt(a.match(/(\d+)/)[1], 10), nb = parseInt(b.match(/(\d+)/)[1], 10);
    return na - nb;
  });
  files.forEach((f, i) => {
    if (!IMAGE_NAMES[i]) return;
    fs.renameSync(path.join(outDir, f), path.join(outDir, IMAGE_NAMES[i] + ".png"));
  });
  fs.unlinkSync(tmpPptx);
  if (fs.existsSync(pdfPath)) fs.unlinkSync(pdfPath);
  console.log(`Wrote 12 images to ${outDir}`);
});
