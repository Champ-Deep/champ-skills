---
name: sprite-art-pipeline
description: Build layered sprite art and prove every spec renders.
---

# Sprite Art Pipeline

Turn a 2D game's hand-drawn or procedural character art into real pixel art by compositing
layers from an attribution-licensed base library, then prove with a test that every
combination the game can produce actually exists on disk. The pipeline is data-driven:
game specs drive the art, never the other way round.

## When to Use

Building or replacing character, enemy or item art in a game or interactive app; a sprite
editor or character customiser; a gallery of rendered asset combinations. Triggers on
"make the sprites look real", "replace the procedural art", "add a character creator",
"sprite test", "every outfit/weapon/hair variant".

Don't use for: generated illustrations or photos (image generation skills), motion-graphics
compositions (`hyperframes-*`), or layout verification of the surrounding UI (`visual-verify`).

## Prerequisites

- A base asset library with per-layer PNG strips plus JSON definitions carrying z-order,
  coordinates and an attribution `credits` block per asset (the Liberated Pixel Cup
  generator is the reference shape: `body`, `hair`, `beard`, `eyes`, `ears`, `head`,
  `clothes`, `feet`, `legs`, `weapon`, plus a monster/enemy set).
- Pillow for the builder (`terminal: python3 -c "import PIL"` to confirm).
- License check before committing: base libraries ship CC-BY-SA 3.0 and/or GPL 3.0, which
  force attribution on the whole app. Serve the credit file, see `references/licensing.md`.

## Procedure

1. **Inventory the base library into scratch, not the repo.** Clone or download it to the
   scratch directory (the cache prunes it, the repo does not), and read its sheet
   definitions to learn layer names, z-order, animation rows and coordinate offsets.
   Done when you can name every layer the builder will consume.

2. **Write the spec table first.** Enumerate every visible variation the game offers as
   data (race, body, outfit x colourway, hair style x colour, beard, accessory, skin, eye,
   weapon, enemy type, size class) with its layer mapping. The spec table is the contract;
   the builder, the manifest and the test all read it. Done when the table covers every
   customization the editor can produce.

3. **Build the compositor** (`tools/` in the repo): for each spec, stack layer strips in
   z-order onto a canvas at the target cell size, recolour layers that ship greyscale via
   their mask, and write one strip per animation row (idle, walk, slash, thrust, cast,
   shoot, hurt). Emit a manifest mapping spec keys to strip files with the draw order so
   the client never guesses z-order. Done when the gallery route renders every spec.

4. **Wire the game to the manifest.** The runtime picks strips by animation row and
   recolours nothing; palette is baked at build time. Keep the in-game editor: it edits
   spec fields, not pixels, so it keeps working unchanged. Done when the editor's changes
   appear as different strips, and the old procedural path is gone rather than kept as a
   fallback (two art paths double the test surface).

5. **Write the sprite test before you trust anything.** Read the spec table from the game
   code, derive every combination it can produce, and assert the composed file exists for
   each. Count and print the resolved combinations. Done when the test fails loudly if you
   delete one strip, and passes on a clean build.

6. **Verify visually, then on the deployed artifact.** Shoot the gallery route (every
   combination at once: fastest way to spot a blank or mis-z-ordered composite), then each
   game surface that shows a sprite (stage, editor, tracker thumbnails, avatars) with a
   CDP screenshot script. Ask the vision pass a defect-shaped question per surface
   ("is the character blank or pixel-art?", "is the label clipped?") rather than "does this
   look good". Finish through the `visual-verify` gate, including the production URL.

## Pitfalls

- **A missing strip fails silently.** An `<img>` that 404s or a canvas with no loaded
  image renders blank with no console error, so the failure mode is a character-shaped hole
  in the game. Only the spec-driven file-existence test and a look at the gallery catch it;
  a green unit test suite does not.
- **Hand-counting expected sprites in the test drifts from the spec table.** A hardcoded
  "expect 464" passes after you add a variant that never built. Derive the expectation from
  the spec data so a new spec without art fails the build.
- **Animation rows are per weapon position, not per animation name.** A thrust row exists
  for spears, not for swords; an animator keyed only on animation name picks an empty row
  and the attack draws nothing. Key on weapon class, and scale oversize weapon layers at
  composite time or the swing reads tiny against a 64px body.
- **Art drawn by code reads as amateur next to real art.** Procedural blocks cannot compete
  with hand-drawn layers at the same size; if a base library covers the style, migrate
  instead of polishing the generator. The migration is cheaper than the third polish pass.
- **Order the fixed-height readout by what the table must act on.** Prompts (vote, act)
  above passive lists (initiative, log), or the clip eats the prompt exactly when the
  session is busiest. See `visual-verify` for the verification half of this rule.
- **Attribution is not optional.** CC-BY-SA and GPL base art require authorship, file and
  licence to travel with the app. Generate the credit file from the asset definitions, do
  not type it by hand, and serve it at a stable route.

## Verification

- `terminal: npm test` (or the repo's test command) green, with the sprite test printing
  the number of resolved combinations against the number of existing strips.
- Gallery route shot: every combination visible, none blank, none mis-layered.
- Per-surface shots: stage, editor, tracker, avatar; each read with a defect-shaped vision
  question and the answer recorded.
- Production: `curl -o /dev/null -w "%{http_code}"` on the manifest, a sample strip and the
  credit route, then the same screenshot set against the live URL.

## References

- `references/licensing.md` — licence obligations, credit file generation, what to serve.