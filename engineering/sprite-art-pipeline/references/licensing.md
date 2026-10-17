# Sprite art licensing and attribution

Base sprite libraries are almost never public domain. Two licences dominate pixel-art
asset collections, and both bind the app that ships the art, not just the folder it sits in.

## The obligations, in order

1. **Identify the licence before you build.** Read the library's licence file and the
   per-asset `credits` blocks. LPC-family collections are dual-licensed CC-BY-SA 3.0 and
   GPL 3.0; some asset sets carry a third, more permissive licence (CC0/BY) that the
   per-asset block overrides for that file only. Licence is per asset, so the credit file
   must be per asset, not one blanket line.
2. **Attribute every used asset.** Author(s), source file, licence name and a licence URL
   for each. "Art from LPC" is not attribution; an asset with three authors needs three
   names.
3. **ShareAlike propagates.** CC-BY-SA on the art means derivative art in the app carries
   the same licence. Keep the game code under its own licence and state explicitly that
   the art and the code are separate works, or a reader will assume the whole repo is
   SA-licensed.
4. **Serve the credit file with the app.** Attribution must be reachable by anyone who
   plays, not only by people who clone the repo: put it at the repo root and serve a copy
   from the static root at a stable route (e.g. `/CREDITS.md`), then curl that route on the
   production host as part of verification.

## Generate, do not hand-write

The credit file is derivable data. Walk the layer definitions the builder already loads,
dedupe on `(file, authors)`, and emit one line per asset with authors, licences, urls and
any notes. Hand-writing it guarantees drift the moment an asset set is updated, and drift
in attribution is the compliance failure that actually gets noticed.

Emit at minimum per asset: file path in the library, author list, licence identifiers, and
the URL the asset came from. Keep the generator in `tools/` next to the sprite builder so
both read the same definitions.

## What to state in the game's own docs

- Which art library the sprites derive from, and its repository URL.
- That the art is CC-BY-SA 3.0 / GPL 3.0 as applicable, with a pointer to the served
  credit file.
- That the game's code licence does not extend to the art, and the art's licence does not
  extend to the code.

## Verification

`curl -o /dev/null -w "%{http_code}" <production-host>/CREDITS.md` returns 200, and the
file's asset count matches the definitions the builder reads (same dedupe key, so a count
mismatch means a stale file).