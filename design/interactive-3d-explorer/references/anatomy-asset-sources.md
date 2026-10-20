# Anatomy asset sources (verified)

For a body/anatomy viewer that must ship locally with no install and no network at runtime, source meshes and shape data up front and bundle them.

## MakeHuman (CC0)

The MakeHuman community repository is CC0 and hosts its full data tree:

- Repo: `https://github.com/makehumancommunity/makehuman`
- Raw fetch pattern: `https://raw.githubusercontent.com/makehumancommunity/makehuman/master/makehuman/data/<path>`
- Shape targets live under `makehuman/data/targets/`. Macro body shapes: `macrodetails/universal-<sex>-young-<muscle>-<weight>.target` (e.g. `universal-male-young-averagemuscle-averageweight.target`). These are small (hundreds of bytes) delta files keyed to the base mesh, ideal for male/female preset switching.
- List the tree before guessing paths: `GET https://api.github.com/repos/makehumancommunity/makehuman/git/trees/master?recursive=1` and filter client-side; guess-and-fetch 404s are slower than one tree call.

## Shipping rules (always)

- Copy the asset license file into the artifact's distribution folder and credit it in the page (a footer or About dialog line naming CC0 / MakeHuman is enough).
- Keep `three`'s own `LICENSE` beside the bundle too: it is a dependency of the shipped code.
- Fetch and transform assets at build time. At runtime the page must make zero network requests; prove it with `visual-verify`'s `scripts/offline-check.py`.
- A base mesh from a generic source is a *generic reference*, not the user's anatomy: label it as such in the scene and in any export, and do not ship derived layers (muscle, bone) built from shapes you have not fitted and visually checked yet. Disable the controls instead.
