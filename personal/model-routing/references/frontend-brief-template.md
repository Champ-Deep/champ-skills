# Anatomy of a frontend lane brief

The main agent owns every design decision; the frontend lane executes exactly what
the card says. Brief quality equals output quality: a vague brief stalls, a precise
brief comes back reviewable. Assemble the sections in this order.

## 1. Reuse inventory (inspect before you spec)

Read the repo first: existing files, prior branch, working logic, assets. List the
paths the lane must reuse with one line each on what they contain (data file, build
script, scroll kit, logo). Say explicitly "port this exactly" for logic that is
correct (data classification, copy corrections) and "restyle only" for done
features (menus, filters). Without this section the lane rebuilds working code.

## 2. Deliverable format (probe the live host if it replaces one)

`curl -sIL <domain>` before naming the output: the serving stack decides it. A
host with no Node runtime takes only static files, so the brief must demand a
self-contained uploadable folder plus a short deploy doc (upload target, rollback
path), whatever stack produces it.

## 3. Design tokens and reference mapping

Give exact hex values with role names. When a reference mock uses another brand's
colours, include a mapping table (mock's dark becomes our primary, mock's accent
becomes ours, mock's light becomes ours) and one line banning the reference's
palette outright, or the lane copies it verbatim. State the type stack and say
whether it is locked.

## 4. Section-by-section spec

Number the page top to bottom in reference order. Per section: the content (real
product names, real prices), the source file for that content, and the motion
attached to it. Spell out the fix for any element the user called out as bad, down
to build details (shape, border, shadow, animation, reduced-motion fallback), or
the lane restyles the wrong thing.

## 5. Data honesty rules

- Every number and health claim cites its source file; mockups carry invented
  statistics, so forbid shipping them.
- No invented ratings, addresses, licence numbers, signatures.
- Unknown facts go in one config JSON at the repo root: empty string means hide
  the element or drop the sentence, never a public placeholder. List that file's
  empty fields in the handover so the user knows what to fill before upload.
- Remove internal scaffolding (draft bars, TBC highlighters, dev tweak panels)
  from the public output.

## 6. Stack choice

If more than one stack satisfies the deliverable format, give options, a default,
and require the lane to state its choice and why in the summary. Do not over-specify
architecture; do fix the constraints (host, data source, brand) that narrow it.

## 7. Acceptance criteria (name the gates)

- Reference-mock fidelity check, item by item, with the palette swap called out.
- Every interactive control listed and "tested in a real browser".
- Named QA skills with exact viewport widths and where screenshots land.
- A concrete content grep (e.g. forbidden characters) returning nothing.
- Reduced-motion emulation checked.
- Branch rules: work branch, main untouched, whether no-remote is fine.

Unmentioned gates read as optional to the lane. Anything you want verified must
be written here, not implied in the goal.

## 8. Do not touch

Exact paths and branches that are off limits (research files, data files, other
branches).

## 9. Handover contract

Require the review request to carry: stack choice and why, components used,
asset provenance (source URL and licence for any stock art), screenshot paths,
the config file's empty fields, and anything skipped.

## Pitfalls

- Write acceptance criteria as measurable commands, not adjectives: `curl -sI <url>`
  returns 200, `scrollWidth == 390`, gzipped JS under N KB reported from real build
  output, a scripted Playwright loop reaching the end state. A lane cannot fake a
  number and the reviewer can rerun the same command. Run every command whose output
  becomes an expected value BEFORE writing it into the brief, and paste the command
  with its real output as the criterion: a count you did not run is a guess, and a
  wrong expected number makes a correct build fail review or a wrong one pass. When
  your mental count and the command disagree, the command is the criterion.
- Name the negatives next to every permission granted (host, repo visibility, scope).
  Absence of a rule reads as permission to a lane working from the brief alone, so a
  custom domain or a public repo gets one line saying it stays out of bounds.
- Put the decision-card block contract in every body under a heading `If you must
  block` (DECISION / A recommended / B / C / default / reply format), so workers on
  any profile emit answerable cards without a config change.
- Gate dependent cards with `parents`, not `blocked`: agent-owned work created in
  `blocked` lands in front of Deep for no reason, while a parented review card
  promotes itself the moment the last build lands.
- Ask for screenshots and exports by absolute path in `artifacts`, or the completion
  notifier has nothing to deliver to Deep's chat.
- Reference images cannot ride in a card body: copy them into the repo (a
  `research/inspo/` folder) and point the brief at the paths, or the lane designs
  from a description instead of the image.
- State photo provenance requirements in the brief: stock or generated food
  photography must land with its source and licence written down, or fake product
  shots ship as real.
- Put the user's complaint into the brief as the fix spec, not as background: the
  called-out element gets its own designed replacement, everything else inherits
  the reference layout.
- Cap runtime (`max_runtime_seconds`) and require real verification output, or an
  an open-ended brief on a single-shot lane can end mid-build.

Worked example of this whole shape: `references/frontend-brief-worked-example.md`, a
shared-rules block plus per-card spec blocks assembled into five cards from one
template in a single pass.
