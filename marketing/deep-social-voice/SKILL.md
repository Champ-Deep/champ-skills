---
name: deep-social-voice
description: "Use when drafting any social post as Deep (LinkedIn, X, Bluesky, Substack). His daily post formula, modeled on Nick Saraev and Nate Herk: bold hook, proof, tight list, one free artifact behind a comment word. Owns the daily draft card and the Postiz send."
---

# Deep's social voice

Deep posts daily as an operator, not a guru: Group CMO across 12 companies who ships agent systems and gives the working files away. The two creators he models are Nick Saraev (bold claim, hard number, tight list, comment-to-get) and Nate Herk ("I built X, here is what it does", plain explanation, link to the long version). Borrow the structure, keep Deep's register: direct, warm, no hype words, no em dashes.

## What performs (from 200+ analyzed posts across both creators)

| Pattern | Share | What it looks like |
|---|---|---|
| Bold statement hook | ~70% of Saraev's hooks | "Most pipeline reviews are vibes." First line stands alone. |
| Value promise hook | ~20% | "Here is the 100-point score my reps hand to Claude." |
| Proof hook | ~10% | A number the reader can check: file count, repo stars, a result with its source. |
| Door, not lesson | every Herk post, most Saraev posts | The post gives away one real artifact. "Comment WORD and I send it." Comments beat likes. |
| Scan speed | all | 1 to 3 sentence paragraphs, then a list, then one ask. Written for a phone. |
| Humbling founder story | top performers | "I built this and it did the wrong thing. Here is the fix." |
| Contrarian rule | top performers | "No. Do not do that." with the better move. |

Volume matters more than timing: Saraev posts ~8 times a week. Daily is the floor.

## Deep's angle (what makes it his, not theirs)

1. Scale proof: 12 companies, several sales teams, one shared public skill library (`github.com/Champ-Deep/champ-skills`, 200+ skills). Nobody else posting in this lane runs that surface.
2. Operator honesty: the system that misfired, the rule that came from a real failure (the linker that broke 38% of vault links, the agent factory that must never merge).
3. The giveaway is always real and already public. The post never promises a file that does not exist in `champ-skills`.

## Post shape

```
<Hook: one line, bold claim or hard number. No question marks, no "excited to share".>

<1 to 2 lines of context: who it is for, why now.>

<List: 3 to 6 items, each one line, each an outcome or a file.>

<One line of proof or the honest caveat.>

Comment "<WORD>" and I'll send it. (or a soft ask: try it on one account today)
```

Length: 120 to 220 words on LinkedIn. Lists use a line break per item, no bullet glyphs except the arrow "→" if the list is steps.

## Platform cuts

| Platform | Cut | Limit |
|---|---|---|
| LinkedIn | Full post | 220 words, no links in body, link in first comment |
| X | Hook + two strongest lines + CTA | 280 chars, or a thread of 3 when the list is the point |
| Bluesky | Same as X cut | 300 chars |
| Substack | Weekly: the seven posts of the week stitched into one issue with a 3-line intro | Saturday, manual |

Substack has no posting API and Postiz does not support it: the weekly issue is pasted by hand.

## Rules

- No em dashes, no en dashes. Periods, commas, colons.
- Every number traces to a source Deep can point to (a repo count, a skill file, a team result already written down). No "booked 47 meetings" unless it is in the vault.
- Every claim traces to a file: the number *and* the anecdote. If the story is not in a source file ("reps hated it until they didn't", "it shipped three wrong changes"), cut it or replace it with what the file actually shows. Unsourceable anecdotes are the one thing that turns a proof post into a guru post, and they are caught only by a read-back pass over the finished draft before it is written out.
- Repeat offenders to cut on that pass: adoption stories ("everyone switched"), before/after sentiment ("they hated it, then loved it"), and failure counts with no log behind them.
- Banned words: excited, thrilled, game-changer, unlock, supercharge, leverage (as a verb), revolutionary, 10x.
- Never name a client or a prospect. Teams and brands are fine.
- One giveaway per post, one comment word per post, words never reused within 30 days.
- The comment word maps to a real path in `champ-skills` and the post log records it.


## Background music taste for reels and shorts (added 2026-10-27)

Modelled on the bed under Adrien's Short "Why Long-Term Plans Break With AI" (youtu.be/shorts/Pc9ICx0K4kc), measured on this machine. The exact track was not identifiable (Shazam: no match; the Short credits no sound), so this is the measured profile, not a track name.

| Measured on the reference | Value | Use it as |
|---|---|---|
| Tempo | 129 BPM (beats well under speech) | mid-tempo 100-130 BPM |
| Key | A minor (low confidence: voice-over dominates) | minor for data and hard truths, major for wins |
| Brightness | 1,924 Hz centroid, warm not tinny | warm low-mid bed, no shrill top |
| Dynamic range | 20.7 dB, calm | near-static bed that never spikes over the voice |

Rules when picking a track:
- Instrumental only, no vocals, no sung hooks: the voice-over owns attention.
- Bed sits clearly under speech (roughly 15-20 dB below), duck on speech if the track has drum hits.
- Dark minimal electronic / lo-fi pulse for AI and data posts; brighter percussive for launch and milestone posts.
- Verified free sources: YouTube Audio Library (copyright-safe on YouTube, some tracks need attribution, check per track) and Pixabay Content License (free, no attribution required, may not be resold standalone).
- Never reuse one track across a whole week of posts; rotate 3-4 tracks and keep a favorite star on the ones that work.

## Daily draft process (cron `social-daily-draft`)

1. Read the last 14 entries in `/Users/deep/Celsus/Efforts/Active/Social Posts/log.md` to avoid repeating a topic or a comment word. Then reconcile against the dated files: a `log.md` row with no `<date>.md` next to it means the post was pre-drafted in a batch, so pull that day's cuts out of the batch file (`Week 1 Posts.md`, sections `## Day N (<date>)`) instead of drafting a duplicate. Stop if `<date>.md` already exists.
2. Pick today's source, in this order of preference: something Deep shipped in the last 48 hours (check `git log` in `~/champ-skills` and recent `Calendar/` daily notes), else the next unused Sales Desk file, else a standing rule from `_config/standing-orders.md` told as a story.
3. Draft the LinkedIn post, the X/Bluesky cut, and the comment word.
4. Write `/Users/deep/Celsus/Efforts/Active/Social Posts/<YYYY-MM-DD>.md` with the three cuts and the artifact path, and append one line to `log.md`: `date | topic | WORD | artifact path | status: draft`.
5. Create a kanban card for profile `content`, title `Social post <date>: <hook>`, body = the three cuts plus "Approve by replying POST, or edit the file and reply POST". Block it as `needs_input` so it reaches Deep as a decision card.
6. On approval the content worker sends through Postiz (`~/postiz/README.md` has the API call) and flips the log line to `status: posted <platforms>`.

## Batch-writing a week

When a week is drafted up front (launch week, a planned series), write all seven posts in one pass and keep them in `Week 1 Posts.md` as `## Day N (<date>)` sections with `**LinkedIn**` / `**X / Bluesky**` cuts and an `Artifact:` line, then seed `log.md` with one row per date. Seeding the log is what makes the cron pick each batch post up on its own date rather than drafting a second post for the same day. Comment words across the batch must be unique and must not collide with existing log rows.
