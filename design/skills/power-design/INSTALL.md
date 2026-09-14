# Power Design (Cowork-packaged build)

Slimmed-down build of [ItsssssJack/power-design](https://github.com/ItsssssJack/power-design) v1.0, packaged as a `.skill` file for Cowork install.

## What changed vs. the source repo

| Item | Status |
|------|--------|
| `SKILL.md` | Included. Patched to remove dead reference to stripped images. |
| `lib/extract-brand.md` | Included as-is. |
| `principles/design-principles.md` | Included as-is. The text source of truth. |
| `brands/` (72 brand systems + template) | Included as-is. |
| `principles/images/` (21 PNGs, ~19MB) | **Stripped.** Marketing/README assets, not functional. |
| `README.md` | Included. Image tags in it point to stripped files (cosmetic only). |

The skill operates identically without the images. They were stripped only to fit Cowork's install size envelope. See https://power-design.vercel.app for the illustrated reference if you want it.

## Original credits

Built by Jack Roberts. Brand library forked from [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md). MIT licensed.

## How to use after install

In Claude / Cowork, the skill triggers on requests like:
- "make me a deck for stripe.com about our Q3 launch"
- "design slides in the linear.app style"
- "build a presentation using power-design"

The skill will prompt for brand (URL, library pick, or default) and content brief, then emit a single self-contained HTML deck.
