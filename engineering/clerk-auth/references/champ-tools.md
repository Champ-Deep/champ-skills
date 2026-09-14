# Champions Group team tools — Clerk auth status

The internal web tools the team uses, their stack, and where they stand on
authentication. Source: the `Champ-Deep` GitHub org and the Celsus vault, as
of 2026-05-24. When the user says "add auth to [tool]", find it here, read its
stack, and load the matching reference file.

## Already on Clerk

| Tool | Repo | Stack | Notes |
|---|---|---|---|
| ChampUTM | `Champ-Deep/ChampUTM` | React/Vite + TypeScript | UTM link generator. Public generator + Clerk-gated premium features. The reference pattern for this skill. |
| ChampLens | `Champ-Deep/ChampLens` | Next.js + TypeScript | QR-to-Video AR business card platform. Clerk added recently. |

## Internal web tools — candidates for Clerk

| Tool | Repo | Stack | Auth status |
|---|---|---|---|
| Event Scout | `Champ-Deep/event-scout` | HTML PWA | Contact manager with card scanner. No auth. Good candidate. |
| LakeB2B Social Post Generator | `Champ-Deep/LakeB2B_Social_Post_Generator` | TypeScript | No auth. |
| ChampCMS | `Champ-Deep/ChampCMS` | TypeScript (Astro) | CMS, WordPress successor. Needs real auth. |
| LakeB2B SlideSmith | `Champ-Deep/LakeB2B-SlideSmith` | Python | Slide generator. Has a UI surface. |
| ChamPDF | `Champ-Deep/ChamPDF` | JavaScript | PDF tool. No auth. |
| Image-to-HTML | `Champ-Deep/Image-to-HTML` | TypeScript | Newsletter builder. No auth. |
| 5-Level Email Personalizer | `Champ-Deep/five-level-email-personalizer` | FastAPI + React | React frontend → Clerk; FastAPI backend → token verification. |
| VCU Unapproved Campaign Dashboard | `Champ-Deep/VCU-Unapproved-Campaign-Dashboard` | Next.js + TypeScript | Internal dashboard. Should be gated. |
| LakeB2B Affiliate Portal | `Champ-Deep/lakeb2b-affiliate-portal` | Next.js + TypeScript | Has Supabase. Confirm whether to use Clerk or keep Supabase auth before changing. |
| Partner Portal | `Champ-Deep/Partner-Portal` | JavaScript | Partner-facing. |
| Champions Club Affiliate Portal | `Champ-Deep/champions-club-affiliate-portal` | HTML | Affiliate tracking. |
| ChampVideo | `Champ-Deep/champvideo` | TypeScript | Avatar video studio. |
| ChampQuest | `Champ-Deep/ChampQuest` | JavaScript | Gamified task tracker for teams. Multi-user, so auth matters. |
| LakeStream | `Champ-Deep/LakeStream` | Python | B2B scraping system. Mostly an API/service; if it gets a UI, gate it; otherwise use backend token verification. |
| AI Resume Parser | `Champ-Deep/ai-resume-parser` | Python | Resume parser with Salesforce integration. |

## Platforms and services (not simple "add Clerk" jobs)

These are larger products or backend services. They may use Clerk eventually,
but auth is a design decision, not a quick retrofit: ChampIQ, ChampMail,
ChampGraph, ChampOracle, ChampHarbinger, ChampCerebro, B2B-Pulse, LakeCurrent,
Graphiti-knowledge-graph.

## Brand / marketing sites (usually no auth needed)

`deependhq-site`, `thedeependhq`, `About-Us-Page` — public sites. Add Clerk
only if a gated area is introduced.

> Note: a couple of names the user has used informally — "ChampUTF" is the
> UTM tool (ChampUTM); "Champ Lens" is ChampLens. If the user mentions a tool
> not in this table, check the `Champ-Deep` GitHub org for the current repo
> list, then update this file.
