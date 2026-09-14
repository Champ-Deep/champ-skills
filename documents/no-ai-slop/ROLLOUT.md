---
layer: 3
scope: how the no-ai-slop gate is rolled into writing skills
---
# No AI slop rollout

Source: github.com/petergyang/no-ai-slop (MIT), adapted 2026-09-11 with zero dashes and a Gate mode. Master skill: `SKILL.md` in this folder. Canonical rule: `_config/conduct.md`, "Writing style".

Apply the block below to the end of every skill listed here, in the account skills and in the champions-skills repo at cutover. Legal skills (champions-nda) are exempt on purpose.

## Skills that carry the gate

- outbound-email
- reach-engage
- reach-cadence
- reach-activate
- reach-hold
- meeting-followup
- send-kit
- b2b-blog-writer
- case-study-builder
- vinh-copywriting
- asset-title
- clf-meeting-prep
- prospect-deck
- deck-doctor
- landing-page
- page-refresh
- paa-seo-builder
- seo-rapid-ranker
- pikvita-push-notifications
- champions-ranch-docs
- prospect-campaign-plan
- prospect-creative-campaign-builder
- lead-gen-playbook-builder
- b2b-growth-showcase
- blog-enhancer
- reddit-reply
- vendor-lead-handoff
- infratech-card-to-pitch
- executive-one-pager

## Brand skills that carry the voice gate

- champions-group-brand
- lakeb2b-brand-guidelines
- ampliz-brand-guidelines

## page-refresh exception

Source copy stays word for word. The gate runs Detect mode on it (findings listed for the user) and Gate mode only on text the skill writes itself.

## pikvita and asset-title notes

Pikvita keeps its witty push-title fragments (brand voice); asset-title contrarian titles state the claim directly instead of the "X Won't. Y Will." shape.

## vinh-copywriting reconciliation

Talking-point example rewritten (no "Here's the thing", no "Not because X. Because Y."), a note under Law 3 against stacked fragments, checklist row 11 (no AI slop), and five example lines rewritten (the "That's it. And it works." After example, the "But here's what most people miss" LinkedIn turn, the "That's what better data does" kicker, and two dashes in example copy).

## vendor-lead-handoff placement

The gate sits above the append-only Decision log, not below it.

## Tests

See `evals/EVAL-REPORT.md`. Run `python3 evals/test_slop_lint.py` after any rule change.

## Gate block (writing skills)

## Final gate: no AI slop (mandatory before delivery)

Everything this skill produces that a person will read (client, prospect, vendor, partner, public, or the sales team) passes a no-AI-slop check before it is delivered. Load the `no-ai-slop` skill in Gate mode and run its Eval on the final copy. If that skill cannot be loaded, apply this minimum:

- Zero em dashes and en dashes anywhere, including headings, titles, subject lines, and date ranges. Use periods, commas, colons, parentheses, or restructure.
- Cut binary contrasts ("It's not X, it's Y", "Not because X. Because Y."), throat-clearing openers ("Here's the thing"), faux-insight setups ("What nobody tells you"), colon reveals ("The best part: it learns"), dramatic fragments ("That's it."), rhetorical setups, fake-profound kickers, and recap endings.
- Cut puffery and weasel attribution ("a testament to", "pivotal moment", "experts agree", "studies show"). Name the source or drop the claim. Never invent a source, stat, or quote.
- Banned words: delve, foster, leverage, utilize, facilitate, empower, streamline, robust, cutting-edge, seamless, unlock, synergy, game changer, tapestry, realm, beacon, multifaceted, meticulous, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving.
- Portability test: a sentence that could move unchanged to another company is filler. Replace it with a name, number, date, or mechanism, or cut it.
- Repeat the right word instead of cycling synonyms. Active voice, human subjects, direct verbs. No decorative bold or emoji headings.
- This gate governs style only. It never overrides this skill's factual, brand, or client-safety rules (vendor firewall, entity separation, verified numbers).

## Voice gate block (brand skills)

## Voice gate: no AI slop

All copy written under this brand (decks, emails, posts, one-pagers, web pages, captions) passes the `no-ai-slop` skill in Gate mode before delivery. Brand voice is the voice it preserves. Minimum if that skill cannot be loaded: zero em dashes or en dashes; no "It's not X, it's Y" contrasts, "Here's the thing" openers, colon reveals, dramatic fragments, kicker lines, or recap endings; none of delve, leverage, utilize, empower, streamline, robust, cutting-edge, seamless, unlock, synergy, transformative, elevate, game changer; every claim carries a real name, number, or mechanism, or it goes. Official taglines, vertical names, and product names stay exactly as written.
