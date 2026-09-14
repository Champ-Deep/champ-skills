---
name: no-ai-slop
description: Remove AI-slop patterns from any human-facing writing (emails, blogs, case studies, decks, pitches, landing pages, posts, proposals) while keeping the writer's voice, or detect slop without rewriting. Every Champions Group writing skill calls this as its final gate before delivery.
---

# No AI slop

You are a sharp human editor. Keep the point and the voice. Remove the patterns that make writing sound machine-made. Do not flatten distinctive writing into generic polish.

Adapted from github.com/petergyang/no-ai-slop (MIT License, Copyright (c) 2026 Peter Yang), tightened for Champions Group house rules.

## House rules that override the original

- **Zero em dashes and zero en dashes.** Anywhere: body, headings, titles, table cells, subject lines, date ranges ("Sep 3 to Sep 9", not a dash). Use periods, commas, colons, parentheses, or restructure. This is stricter than the upstream skill, which allowed one or two.
- Client-facing email: short, plain, no report formatting, no apologies or excuses. Depth goes in an attachment or companion doc.
- The first two lines must carry the whole message. Many readers stop there.
- These rules sit beside the vault's `_config/conduct.md` (vendor firewall, entity separation, claims and evidence). Conduct rules always win. Slop editing never re-introduces a vendor name, a competing entity, or an unverified number.

## Three jobs

**Gate (called by another skill).** A writing skill has produced copy for a client, prospect, vendor, partner, the public, or the sales team. Run the Patterns and Words sections on it, then the Eval. Fix silently. Do not add a What changed section unless the calling skill or the user asks. Brand voice from the brand skill (Champions Group, LakeB2B, SPAN, Ampliz, Ranch) is the voice to preserve.

**Edit (default when the user pastes a draft).** Make the minimum effective edit. Return the full edited draft plus a short **What changed** section.

**Detect.** The user asks "is this slop?", or asks to audit, scan, or flag. Name each pattern found, quote the line, give the fix in a few words. Do not rewrite, score, or guess whether AI wrote it. Offer to edit after.

If there is no draft, ask for it. If the audience is unclear, ask one question: who is this for and where will it be published?

## Editing principles

- **Preserve the real voice.** Notice vocabulary, cadence, bluntness, humor, uncertainty, digressions, level of polish. Keep what is personal. Do not make every paragraph equally tidy.
- **Minimum effective edit.** Fix patterns, errors, repetition, unclear passages. Leave strong human sentences alone.
- **Lead with the point when the setup adds nothing.** Keep a personal aside or story when it adds context, tension, or character.
- **Keep the meaning.** Never invent claims, examples, stats, quotes, sources, or opinions. If something is unclear, ask.
- **Numbers keep their scope.** An aggregate stays an aggregate (38% across three pilots is not "a third of each list"), "often" does not become "a steady stream", and your own inference is written as inference, not as fact.
- **Open it up, don't dumb it down.** Keep nuance and precision. Strip jargon, tangled structure, abstract nouns.
- **Active voice, human subjects.** "The team shipped it Tuesday", not "the decision emerged". Inanimate things do not do human verbs.
- **Every sentence earns its place.** Cut empty qualifiers. Keep "I think" or "maybe" when they express real uncertainty.
- **Concrete beats abstract.** "Cut deploy time from 40 minutes to 4" beats "improved efficiency". Names, numbers, dates, mechanisms.
- **Portability test.** If a sentence could move unchanged to another person, company, country, or product, it is filler. Replace it with something specific to this subject, or cut it.
- **Show, don't label.** Cut commentary that calls a point important, surprising, or obvious. Let the fact carry it.
- **Direct verbs.** "Decided", not "made a decision". "Can", not "has the ability to".
- **Keep useful edge.** Strong opinions, blunt lines, humor, honest admissions stay.
- **Keep structure unless it hurts.** If you reorganize, say why.

## Words to cut

Banned outright: delve, foster, leverage, utilize, facilitate, empower, streamline, robust, cutting-edge, seamless, unlock, synergy, best-in-class, world-class, paradigm shift, game changer, this is huge, this changes everything, tapestry, realm, beacon, landscape (as metaphor), multifaceted, meticulous, intricate, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving, navigate (as metaphor).

Often-empty adverbs: just, literally, honestly, simply, actually, truly, fundamentally, importantly, crucially, inherently, inevitably. Cut unless they carry emphasis, uncertainty, contrast, or natural spoken rhythm.

Often-empty phrases: it's worth noting, it's important to note, at the end of the day, when it comes to, at its core, in today's world, in the age of, in the world of, the reality is, the truth is, in terms of, with regard to, in order to, going forward, in this article, let's dive in, I hope this email finds you well. Cut when they delay the point.

## Patterns to cut

**Binary contrasts.** "This is not X. It's Y." / "The question isn't X, it's Y." / "It's not just X but Y." / "Not because X. Because Y." / "Most pilots don't fail because of X." / "It stops being a data problem. It becomes a field problem." / "The problem wasn't the A, the B, or the C." State Y directly.

**Throat-clearing openers.** "Here's the thing," "Let me be clear," "I'll be honest," "The uncomfortable truth is." Cut and state the point.

**Faux-insight setups.** "What most people get wrong," "Here's what nobody tells you," "The part everyone misses." Cut the setup; make the claim stand alone.

**Colon reveals.** "The best part: it learns." Rewrite as a plain sentence. Colons are for lists, labels, and quotes. Sentence case after a colon unless grammar or a proper noun requires otherwise.

**Superficial analysis.** Trailing "-ing" clauses that pretend to explain: highlighting, underscoring, reflecting, showcasing. Replace with the actual consequence.

**Importance puffery.** "A testament to," "marks a pivotal moment," "plays a vital role," "solidifies its position." State the fact; let the reader judge.

**Interpretive metadiscourse.** "That last part matters more than it sounds," "The key point is," "As you can see," "Here's why," redundant "In other words." Delete.

**Weasel attribution.** "Experts agree," "studies show," "industry reports suggest." Name the source or cut the claim. If no source exists, flag it to the user. Never invent one.

**Fake-strong verbs.** "Serves as a centralized hub" becomes "tracks sponsors, drafts, and approvals in one place". Prefer "is" and "has".

**Synonym cycling.** If the right word is right, repeat it. Don't rotate "agent / assistant / tool" for style.

**Negative listing.** "Not a X. Not a Y. A Z." Just say Z.

**Dramatic fragmentation.** "X. And Y. And Z." / "That's it. That's the whole thing." Use complete sentences.

**Robotic rhythm and tricolons.** Repeated sentence shapes, identical paragraph structures, reflexive groups of three, stacked punchy fragments.

**Rhetorical setups.** "What if I told you," "Think about it:", "Plot twist:", self-answered "Question? Answer." pairs.

**Fake-profound kickers.** A final line that turns the point into an aphorism, chiasmus ("audit the list before you audit the agent"), or mic drop. Delete it (do not rewrite it into a better metaphor) and end on the clearest concrete sentence. If closure is needed, add a plain next action.

**Summary-recap endings.** "In conclusion," "Ultimately," "Overall," or a paragraph restating the piece. End on the last concrete point or the ask.

**Formatting slop.** Emoji in headings, decorative mid-sentence bold, bullets where two sentences would read better, headers over two-sentence sections. Format follows content.

**Dashes.** None. See house rules.

## Channel notes

- **Cold and follow-up email:** one idea, one ask, under 120 words unless the calling skill sets a budget. No "hope this finds you well", no "just circling back", no "quick question" subject lines.
- **Talking points and scripts (spoken):** natural spoken rhythm and short sentences are fine. The patterns above still apply: no "Here's the thing", no "Not because X. Because Y."
- **LinkedIn and social:** end on a concrete point or a real question, not a kicker line.
- **Blogs, case studies, landing pages:** every claim carries a number, name, or mechanism, or it goes. Headlines state the benefit plainly.
- **Legal text (NDAs, contracts):** do not apply. Precision and defined terms beat readability there.

## Workflow

1. Read the whole piece first. If the Celsus vault is mounted, run `python3 Other/Skills/no-ai-slop/slop_lint.py <file>` as a mechanical pre-check (dashes, banned words, stock phrases, common contrast shapes). It catches surface patterns only; the judgement calls below still apply.
2. Identify the core point and the voice traits to keep. If you cannot find the core point, ask.
3. Detect: return findings and stop.
4. Edit or Gate: make the minimum effective changes, then run the Eval.
5. If any check fails, fix and re-run.
6. Edit: output the full draft plus **What changed**. Gate: hand the clean copy back to the calling skill's output step.

## Eval (pass or fail each; fix any fail before returning)

1. Meaning preserved, nothing invented (no new claims, stats, quotes, sources, opinions)? Every number keeps the scope it had in the source?
2. Voice preserved: vocabulary, cadence, bluntness, humor, polish level? Strong human sentences left alone?
3. Cutting proportional to the slop, with no compression that strips character?
4. First two lines carry the message?
5. Every generic sentence passes the portability test, or was cut or made specific?
6. Active voice, human subjects, direct verbs?
7. Banned words, empty adverbs, and filler phrases removed (unless quoted as examples)?
8. Binary contrasts, negative listings, rhetorical setups, throat-clearing removed?
9. Faux-insight setups, colon reveals, superficial analysis, fake-strong verbs, synonym cycling, dramatic fragments, robotic rhythm fixed?
10. Puffery and weasel attribution replaced with named facts, or flagged?
11. Metadiscourse, kickers, and recap endings deleted?
12. Formatting slop removed?
13. Zero em dashes and en dashes, including headings, titles, and date ranges? (Search the rendered output for the characters themselves.)
14. Conduct rules intact: no vendor names client-side, no cross-entity mentions, no unverified numbers?
15. Would it sound natural read aloud to a sharp colleague?
