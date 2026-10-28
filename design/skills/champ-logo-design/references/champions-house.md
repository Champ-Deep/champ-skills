# Champions house layer

Read this first on any Champions Group logo job. It sits on top of the upstream process and wins where they differ.

## 1. Brand locks and equity

| Brand | Source of truth | Rule |
|---|---|---|
| Champions Group (parent) | `champions-group-brand` skill | Locked. Sub-brand marks must not borrow the parent mark unless the brief asks for an endorsed lockup. |
| Lake B2B | `lakeb2b-brand-guidelines` | Locked |
| SPAN Global Services | `span-brand-guidelines` | Locked |
| Ampliz | `ampliz-brand-guidelines` | Locked |
| MetricFox | `metricfox-brand-guidelines` | Locked |
| AB7 Solutions | `ab7-brand-guidelines` | Locked |
| deependhq.com (Deep personal) | `deependhq-design-system`, then `identity-kit` | Locked |
| IP Momentum | no brand skill | Equity sampled 2026-10-28 from the live logo PNG: red disc `#EC222A` holding "IP", blue pill about `#4A80C2` holding "momentum", trailing dots. It is a VoIP and business telephony provider. "IP" means Internet Protocol. |
| Recruit Champ | no brand skill | Written `recruitChamp`. Equity sampled 2026-10-28 from recruitchamp.com/assets/images/logo.png: blue `#0090D0`, light blue `#A8E0F0`, orange `#F06028` (orange carries "Champ"). |

A locked brand is out of scope for a new mark unless the user says the new work replaces it. For any brand without a skill, run the **equity check** before concepts:

1. Fetch the live site and find the logo file (`<img>` in the header, `og:image`, favicon).
2. Download it and sample the colours from its pixels with Pillow. Do not trust site CSS for logo colours: in testing, the CSS navy was not in the logo at all.
3. Write down the equity in one line: shapes, colours, letters, anything people already recognise.
4. Treat it as equity to weigh, not as a lock. At least one concept must be an **equity evolution** (see `originality.md`).

## 2. Asking vs assuming

- **Live chat:** if confidence in the brief is below 80%, ask once, in one batch, with the `clarify` tool. Offer choices the way a designer shows mood boards: a personality question (bold geometric, crafted, typographic, playful), a focus question (what we do, how it feels, who we are), and an inspiration question with three or four **real brands from that company's own sector**, never a generic tech list.
- **Headless run (kanban card, cron, delegated child):** nobody can answer. State the assumptions at the top of the brief, run the fast track, and stop at the checkpoint. Complete the card with the overview image as an artifact. If the user must choose before any more work happens, block the card with `kind=needs_input`, listing the options and your recommendation first.

## 3. Which model does the drawing

Concept quality tracks the model. On identical briefs, a small delegation model produced generic shapes. Opus 5.5 produced ideas grounded in true facts about the name. `delegate_task` children run on the configured delegation model, not on the parent's model. When the work is concept generation, do it in the main session or in a kanban card pinned with `model` and `provider`. Use cheap children only for mechanical work: rendering, exporting, building an already-chosen geometry.

## 4. Where files go

- Working files go to the vault: `/Users/deep/Celsus/Efforts/Active/<Brand> Logo/` (or the brand's existing effort folder). Never leave deliverables in the scratch dir; it is pruned after 24 hours of idleness.
- Keep `brief.md`, `concepts/` (every iteration), `renders/<size>/`, `final/`, `concept-overview.png` and a `report.md` (one line per concept, recommendation, honest 1 to 10 rating, every tool issue hit).
- The vault path contains spaces. Quote every path passed to a script.

## 5. House rules on output

- No em dashes or en dashes anywhere: SVG titles, HTML sheets, reports, chat. Before delivering, scan the output folder for U+2013 and U+2014.
- Never put a real team member's or client's name on a mark, board or mockup.
- Only true copy on boards: real taglines, real URLs. No invented stats, phone numbers or clients.
- Nothing is sent to a brand owner on Deep's behalf. A brand belongs to its company head (IP Momentum: Vasan, see `_config/people.md`), so the usual next step is "show the owner", staged as a decision for Deep.
- Ownership: marks that began as AI output should get a human redraw and a professional trademark search before any filing. Say so in the report.

## 6. When code drawing is not enough

SVG-by-code is strongest for geometric marks, lettermarks and wordmarks. Mascots, illustrative emblems and hand-made textures hit a ceiling fast. For those, switch to `identity-kit`, which generates vectors with Higgsfield Recraft (paid credits: state the cost first), then use this skill's tests (`pixel_check.py`, `svg_audit.py`, `preview_sheet.py`) on the cleaned result.
