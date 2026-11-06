# Rolling one component across several repos and stacks

Use when Deep hands over a component (a paste, a library card, a URL) and asks for it
"in the tools that use it": one shared spec, N frontend cards, N repos, possibly N
stacks. Procedure first; the template sections in `frontend-brief-template.md` still
govern each card's own spec.

## 1. Capture the source, then pin the one shared spec

1. If Deep pasted the code, save the paste VERBATIM (attachment path or message body)
   into the effort folder as `<vendor>-<component>-source.txt` and point every card at
   that file. A URL or a library id is not a copy: the library's code step may be paid
   or rate-limited, and a lane that cannot fetch it hand-rolls a lookalike.
2. Write ONE shared brief in the same effort folder (`ui-brief-vN.md`) holding only
   what is identical everywhere: the component edit list (the exact deltas from the
   source), the targets table, and the acceptance rules. Cards carry their own goal,
   files, per-tool data mapping and gates, and name the shared file. A card that only
   says "follow ui-brief.md" is a thin card: the lane reads its body at spawn and will
   block on anything the body does not settle.
3. Keep the targets table in the shared brief as the roster: `tool | checkout | stack |
   files to edit | branch base | PR target | card id`. You will read it at review to
   check every row landed.

## 2. Gather per-repo facts BEFORE any card is written

One batched pass per repo, in parallel:

- Stack and component home: `package.json` (next/tailwind/lucide/motion versions),
  `components.json` (does shadcn already exist?), `lib/utils.ts` (is there a `cn`?),
  where the equivalent feature renders today (`grep -n` the current plain-text version
  and paste its line numbers into the card).
- The DATA CONTRACT the tool already emits: the response shape, which fields carry the
  claim text and the source, where the source record lives (API, DB join, Convex table,
  SSE payload). Paste the real shape and one worked example into the card. A lane
  guessing an API shape invents one.
- Branch reality: `git fetch`, `git status --short`, `git log -1`, and whether the
  feature even exists on `main` (`git cat-file -e origin/main:<path>`). Features that
  live only on a feature branch mean the PR targets that branch, not `main`.
- If the repo is not cloned locally, clone it to the fixed path `~/repos/<name>` first
  and use that as the card workspace; a card pointed at a non-existent directory starts
  from nothing.

Skip a tool that does not actually carry sources: a tool with no source field in any
response gets no card, and the roster row says why.

## 3. Pre-create isolated checkouts, then create the cards

- Per repo: `git worktree add -b <branch> <checkout> <base>` so each lane gets its own
  tree and branch, and a checkout with uncommitted work in the main clone is never
  touched. Point `workspace_kind="dir"` at the worktree and restate branch + PR target
  in the body.
- Repos that must not be committed (a folder inside the home repo, an unapproved
  commit) get a body line: "do not run git write commands, leave changes uncommitted and
  list changed files".
- Pin `model`/`provider` on every card per the standing override, cap
  `max_runtime_seconds`, and attach the QA skills you want loaded.

## 4. The shared edit list: decide the deltas ONCE

Write the component changes as a numbered list that reads the same on every card, so
review can grade four builds against one contract. Typical deltas for an adopted third-
party component:

1. Optional dependencies the source assumes (a link field that some tools have no value
   for; a helper like `cn` that some repos lack, with the minimal init command named).
2. Fields the source lacks but the data has (a date/sender line), stated as a new optional
   prop.
3. Demo/sample content removed from the production path, named explicitly: a copied
   component ships its demo array, and a tool rendering it shows fabricated sources.
4. Visibility switches for rows that would otherwise render an empty block.
5. Correctness nits (singular/plural label) so four lanes do not each fix it differently.
6. Theme integration: name the host's own dark-mode mechanism (class variant vs media
   query, `@custom-variant` in Tailwind v4) or the chip stays light on a dark page.

## 5. Data honesty rules that belong on every citations card

- Never render a source the backend did not return. No invented titles, snippets, urls.
  A claim with no source renders as plain text with no chip.
- Internal identifiers (row ids, passage ids, vault paths) are KEYS, not labels: they
  build the map, they never appear as visible text. Say this explicitly; a lane that has
  no friendly title will surface the id.
- Multi-stack means an adapter spec per stack, not one hope: React/shadcn repos vendor
  the component file; a static no-build page gets a porting spec (match timings, card
  width and visual states; no CDN scripts, no framework added). State the adapter in the
  card, since "use the component" is untrue for the stack that has no React.

## 6. Proof and review

- Same screenshot folder name and viewport pair in every card (`qa/citations/`, 375 +
  1280, light and dark) so review compares like with like; fixture-only runs label the
  file `stub` and the handover says so.
- A lane with no local credentials (DB, API, passcode) proves the UI with a route/
  network stub of the real payload shape, never by reading a secret to get past a gate.
- At review, check the roster row by row: card complete, PR target correct, screenshots
  on disk, no visible internal ids (`grep` for them yourself across all four checkouts),
  shared edit list satisfied in each build.
- Deferred rows (tools named as "etc" but not carded) go in the completion report as the
  roadmap, never dropped silently.
