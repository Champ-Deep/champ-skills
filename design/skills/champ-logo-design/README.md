# champ-logo-design

The Champions Group edition of [kaankiziltug/logo-design-skill](https://github.com/kaankiziltug/logo-design-skill) at upstream commit `7340903`, MIT licence (LICENSE kept, library trademark notice in TRADEMARKS.md). Everything upstream has is still here: 7-phase process, 13 references, the 1,400+ logo library, all 8 scripts and the templates. This file is for maintainers and reviewers. Agents read SKILL.md.

## Why this base

Chosen by a logo skill bake-off on 2026-10-28 (vault: `Efforts/Active/Logo Skill Bakeoff/README.md`). Two skills were each run on two brands (IP Momentum, Recruit Champ), under two models, eight runs in total.

| | kaan logo-design (this base) | op7418 logo-generator |
|---|---|---|
| Licence | MIT | none, so it cannot be vendored |
| Built-in QA | audit, preview sheet, shelf test, concept sheet | none (the agent improvised its own) |
| Output with Opus 5.5 | 7/10 picks on both brands | 6.5 to 7/10 |
| Extras | 1,400+ reference library, kit and board scripts | showcase step needs a Gemini key |

Outside sources: Reddit and Hacker News threads on agent logo skills, plus repo issues. The consistent feedback: idea quality decides the result, minimal geometry converges on lookalike marks, and people are tired of featureless "AI minimalism". Those findings became `references/originality.md`.

## What changed from upstream

| Area | Change | Why (from the test runs) |
|---|---|---|
| House layer | New `references/champions-house.md`: brand locks, an equity check that samples live logo pixels, ask vs assume (headless runs block with `needs_input`), which model draws, vault file locations, house rules | Concepts that evolved the existing equity scored best. Site CSS colours were wrong for the logo. |
| Originality | New `references/originality.md`: six concept slots including a mandatory equity evolution, each concept grounded in a fact, early prior-art kills, a list of AI-logo tells, honest ratings | The strongest concepts rested on true facts ("p is momentum", Doppler). |
| Verification | New `references/verification.md`: pixel truth over vision models, cairosvg setup for Deep's Mac, engine pitfalls (`<mask>` is ignored by cairosvg, `currentColor`, arc flags), a done checklist | Vision models were confidently wrong in every run. The Chrome fallback hung shells. |
| New script | `scripts/pixel_check.py`: renders on white, prints ASCII dumps at 16/32 px, measured margins and centring offsets, weight offset, flags | Replaces the hand-rolled pixel dumps every Opus run had to write |
| New script | `scripts/outline_text.py`: outlines a word in a real font file (variable axes, tracking) to path-only SVG | Every run hand-rolled fontTools code to get lockups free of `<text>` |
| render_png.py | Batch renders put the size in the file name (`a-16.png`). HTML screenshots without `--height` shoot tall and trim the empty tail. | 16 px renders silently overwrote 512 px renders, and long sheets were cropped at the fold |
| svg_audit.py | INFO note when transforms or strokes make its margin maths approximate | Its centring verdicts were wrong on transformed marks |
| search_library.py | Maps Champions sectors the library lacks (telecom, VoIP, recruitment, HR, staffing, B2B data, martech, fitness, hospitality, real estate) to the nearest category, and says so | Both brands fell outside the tech-heavy taxonomy |
| Text | Every em and en dash replaced (house rule), name and trigger-style description, Hermes metadata, Hermes `MEDIA:` delivery | House rules |
| Tests | `tests/smoke_test.py` adapted to this layout, plus checks for the house sector map, batch renders at several sizes, pixel_check (including transforms), outline_text, missing references and a ban on dashes | |

Dropped: upstream's plugin manifests, packaging tool and CI workflow. Champ-skills is the distribution, so they are not needed.

## Test

```bash
python3 tests/smoke_test.py      # 28 checks; the PNG, pixel and outline checks skip cleanly without a renderer, Pillow or fontTools
```

## Not done yet (candidates for v2)

- A real kerning pass in `outline_text.py`. It needs `uharfbuzz`, a new dependency, so it was left out.
- A trademark pre-screen script (USPTO and WIPO image search have no free API, so it stays a manual step).
- Re-running the bake-off briefs through this edition to measure the gain. Only the scripts were tested, not a full design run.
- Upstream sync. There is no automation; diff against a new upstream commit by hand.
