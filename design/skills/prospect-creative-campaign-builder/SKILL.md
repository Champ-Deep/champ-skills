---
name: prospect-creative-campaign-builder
description: >-
  Turns a prospect name into a full outbound package in one pass: vault +
  Zoom research, on-brand ad creatives (Higgsfield images/video), a
  multi-channel lead-gen playbook, and a visual HTML version of it. Runs a
  connector preflight (Zoom MCP, Higgsfield MCP) and a short intake (client,
  deliverable mix, brand assets, personas) before generating anything.
  MANDATORY TRIGGER for "build creatives for [prospect]", "package a pitch
  for [company]", "make ad creatives and a campaign playbook for [client]",
  "send over the creatives for [prospect]", "need a funnel example for
  [client]", "campaign package for [company]", or any request combining
  prospect research with creative generation and/or a lead-gen playbook.
  Also trigger for Higgsfield, LinkedIn ad creatives, or an
  "advertising-ops"-style ask alongside a client name. Orchestrates
  lead-gen-playbook-builder and visual-report-builder as sub-steps, so use
  this one first when the ask spans research + creatives + playbook.
---

# Prospect Creative + Campaign Builder

You take a prospect or client name and turn it into everything a rep needs to open outreach: researched context, ad creatives, a full campaign playbook, and a visual version of that playbook. This exists because that whole sequence used to get built by hand, one Higgsfield call and one Python script at a time, and it broke in the same three places every time: nobody checked the creative-gen connector was even authorized before starting, brand assets got recreated by AI instead of using the client's real files, and locked scope decisions (which specialties or personas are actually in play) got silently guessed at instead of surfaced. This skill exists to make those three failure points structurally impossible to skip.

## What this produces

Depending on what the intake confirms, some subset of:
- A short research brief (vault client note + relevant Zoom meeting history, if any)
- Ad creative images and/or a short video, on-brand, via Higgsfield
- A single-file HTML creative deck (all creatives embedded, shareable as one file)
- A full text campaign playbook (personas, channel waterfall, exact pitches, reply-handling flowcharts, operating system) via `lead-gen-playbook-builder`
- An editorial visual HTML version of that playbook via `visual-report-builder`
- An updated vault client note linking everything, so the next session has full context without re-deriving it

Not every run needs all of these. A rep might just want creatives, or just the playbook. The intake in Step 1 figures out which.

## Step 0: Connector preflight (do this first, every time)

Before asking the user anything or generating anything, confirm what's actually available. This step exists because generating half a campaign and then discovering the creative-gen tool was never authorized is a worse experience than finding out up front.

Read `references/connector-preflight.md` for the exact tool names and check sequence. In short:

1. Check whether the Higgsfield MCP (or whatever image/video generation MCP is connected) is reachable. If creatives were requested and it isn't connected or is unauthenticated, stop and tell the user which connector needs authorizing and where (claude.ai connector settings, or `/mcp` in an interactive session) — do not silently skip to a worse substitute like describing creatives in text instead of generating them.
2. Check whether a Zoom MCP (or equivalent meeting-history tool) is connected. This one is soft-optional: if it's missing, proceed without meeting research and say so plainly in the research brief rather than blocking the whole run on it.
3. Confirm vault file access (read/write to the client's folder). This is almost always available since it's the working directory; only flag it if writes genuinely fail.

Report the preflight result to the user in one line before moving to intake, e.g. "Higgsfield connected, Zoom MCP connected, vault writable — good to go" or "Higgsfield needs authorizing before I can generate creatives (claude.ai connector settings); everything else is ready. Want me to proceed with research + playbook now and slot creatives in once it's connected?" Never pretend a missing connector is fine and improvise around it — that's the exact failure mode this step is here to prevent.

## Step 1: Intake

Batch this into one `AskUserQuestion` call (or a plain question if the tool isn't available). Pull every answer you can from the current conversation first — client name, industry, prior context, specialties, brand mentions are frequently already sitting in what the user just said. Only ask what's genuinely missing.

Lock these four things before generating anything:
1. **Client / prospect name and industry.** Enough to find or create the vault client note.
2. **Deliverable mix.** Some combination of: ad creative images, short video, single-file creative deck HTML, text campaign playbook, visual HTML playbook. Don't assume all five; confirm.
3. **Personas / specialties / segments.** How many distinct buyer personas or product specialties does this campaign chase? This maps directly to how many creative variants and playbook persona sections get built. If the user has pasted specialty-specific pitch copy already (like a list of email templates per vertical), that copy IS the persona list — don't re-derive it, use it directly as the source content for Step 6.
4. **Brand assets.** Ask explicitly: "Do you have the client's actual logo/brand files, or should I pull from their public site?" This is the single most consequential question in the intake — see Step 3 for why.

If the win condition (a number, by a date) isn't already stated, ask for it too; the playbook step needs it for the TL;DR and the weekly review targets.

## Step 2: Research

Look in this order, stopping as soon as you have enough:
1. **Vault.** Search `Atlas/Clients/{client}/` for an existing client note. If one exists, it's the source of truth for prior engagement history, contacts, and TAM — read it before doing anything else.
2. **Zoom meeting history** (if connected per Step 0). Search for meetings mentioning the client name to pull prior conversation context, explicit asks ("send a concrete funnel example, not another deck"), and attendee names. Summarize rather than dumping full transcripts.
3. **Web search**, only for public-facing brand or market context (the client's own site, LinkedIn ad library precedent for the vertical). Treat this as supplementary, not primary.

If a locked scope decision already exists in the vault (e.g., a prior deck-review note says a specific persona or specialty is explicitly in or out), surface that explicitly to the user if the current request conflicts with it. Don't silently comply with the new request and don't silently override the vault record either — say "the vault has X locked from [date], your current ask includes Y, want me to update the scope or keep Y out?" and proceed once they've answered. Guessing wrong here is expensive because it produces client-facing collateral built on a wrong assumption.

## Step 3: Brand assets — read this before generating any creative

This is the step most likely to go wrong, so the rule is blunt: **if the user has the client's real brand files, use those exact files. Never recreate, composite, or approximate a logo when the real file is available or obtainable.** A prior run of this workflow spent real effort building a pixel-accurate composite of a client's logo onto generated creatives, and the user's reaction was "you made it worse, just use these images instead" — a high-signal correction. A recreation that is 95% accurate is still wrong in a way a client-facing creative cannot be.

Concrete sequence:
1. Ask (per Step 1) whether the user has the client's actual brand/logo files.
2. If yes, and the user has pasted images inline in chat: know that inline chat images do not materialize as files under the uploads path in this environment. Check the actually-connected/mounted folders (there may be more than one) for the files by modification time (`find <mounts> -newermt "-1 hour"` or similar) rather than assuming the chat upload path has them. If they're genuinely not accessible anywhere, say so plainly and ask the user to drop them into a connected folder rather than proceeding with a substitute.
3. If the user has no real files and none are findable, fall back to rendering the logo from the client's public website (their site usually has an SVG or a hi-res PNG in the footer/header) — `cairosvg` handles SVG-to-PNG conversion well for this. Flag clearly in the output that this is a fallback, not a guarantee of pixel accuracy, so the user can swap it later if it's off.
4. Never invent brand colors or a wordmark from scratch when a real source exists. If Higgsfield or any generative model invents its own version of a known brand's logo (it will, if not constrained), that generated version needs the same swap-for-real treatment before anything ships.

## Step 4: Creative generation (Higgsfield)

Read `references/creative-generation.md` for the current Higgsfield MCP tool surface, model selection, credit costs, and the concurrency limit workaround. In short: confirm the model's roles and constraints via `models_explore` (action `get`, or `recommend` for unusual cases) before generating; the image default is `marketing_studio_image` (1:1, 2k resolution), which takes the real brand logo as a reference media (imported via `media_import_url` for web assets or `media_upload_widget` for the user's local files — never pass raw URLs as media values). The plan caps concurrent jobs at 4 — batch submissions in groups of 4, poll with `job_display` (one job ID per call), and only submit the next batch once slots free up. Use `get_cost: true` to preflight credits on batches and video, and `balance` when budget matters. If a response includes a `recovery_tool`, call it immediately without asking first.

For video: `marketing_studio_video` for ad motion or `kling3_0_turbo` with a start-image reference for cinemagraph-style variants. **Hard rule: all first-draft videos generate at 480p (or the model's lowest supported resolution). Video is where credits burn, so prove the concept cheap, get the user's approval, then `upscale_video` the approved cut rather than regenerating at high resolution.** Also note that any logo baked into a generated video cannot be fixed with a static image swap later, it needs a full regenerate, so get the source image's brand asset right (Step 3) before generating video from it.

When downloading generated media, always re-query `job_display` for the specific job's exact result URL rather than constructing a CDN URL by hand — timestamps in these URLs are not guessable and a wrong guess produces a corrupt near-empty file that looks like it downloaded successfully until you check the byte count.

## Step 5: Assemble the creative deck

Once creatives exist (generated, brand-corrected, or both), combine them into a single self-contained HTML file so the whole set is shareable as one artifact. Use `scripts/build_creative_deck.py` for this rather than writing a new base64-embedding script from scratch each time — this exact pattern (read local images/video, base64-embed, drop into an HTML template) got rewritten five separate times during the workflow this skill is based on, which is exactly the kind of repeated work that belongs in a bundled script instead of reinvented per run.

## Step 6: Campaign playbook

Invoke the `lead-gen-playbook-builder` skill for the text playbook. Feed it the personas/specialties locked in Step 1, the research from Step 2, and the win condition. If the user already supplied exact per-persona pitch copy (e.g., pasted email templates for each specialty), pass that through as the literal source copy for Section 4 rather than regenerating it — the user's own words are the ground truth once supplied, your job is to structure them into the full playbook shape (waterfall, flowcharts, operating system) around that copy, not to rewrite copy that already exists.

If a scope conflict surfaces here too (a supplied persona conflicting with a locked vault decision), it's the same rule as Step 2: surface it, don't silently resolve it either direction.

## Step 7: Visual HTML version

If the intake confirmed a visual version is wanted, invoke `visual-report-builder` using the finished markdown playbook from Step 6 as source content. The visual version should mirror the markdown's content exactly (same personas, same pitches, same numbers) in editorial form, not add or drop scope. This is a re-expression, not a second draft.

## Step 8: File everything in the vault

Update (or create) `Atlas/Clients/{client}/{client}.md` with links to every deliverable produced this run, dated. Follow the existing vault convention: a dated subsection per work session, plain links to the files (not full paths), and a one-line note on what's still open (e.g., a video creative that still needs a brand-asset fix). Keep the creative deck and any raw generated media inside a `Creatives/` subfolder under the client's folder; keep the playbook markdown and visual HTML at the client's folder root alongside the client note itself.

Respect the vault's file-deletion rule: never delete or rename an existing file in the vault without asking first (superseded drafts get marked "superseded, kept for history" in the client note rather than removed). Overwriting a file in place with a corrected version is fine; deleting or renaming is not, without explicit confirmation.

## Step 9: Close the loop

Present the finished files to the user (creative deck, playbook, visual HTML — whichever were built). Keep the wrap-up short: what got built, where it lives, and the one thing still open if anything (an unresolved brand-asset gap on a video, a scope question not yet answered, etc.). Don't re-explain the whole workflow back to the user; they were there for the intake.

## Hard rules carried through every run

- No em-dashes in any generated output (playbook, creative copy, vault notes) — periods, commas, colons, or restructure.
- Never guess a locked scope decision silently in either direction; surface conflicts and let the user resolve them.
- Never treat a generative model's invented version of a real brand's logo, colors, or wordmark as acceptable — always prefer the client's real files, then their real public site as fallback, in that order.
- Never construct a media download URL by hand; always re-query the generation tool for the authoritative result URL.
- A user's own supplied copy (pitch templates, persona descriptions) is ground truth once given; structure around it, don't regenerate it.
- First-draft video is always 480p (or the model's minimum). Upscale approved cuts with `upscale_video`; never spend high-resolution credits on an unapproved concept.

## Reference files

- `references/connector-preflight.md` — exact tool names and check sequence for Step 0.
- `references/creative-generation.md` — Higgsfield model names, credit costs, concurrency handling, and download pattern for Step 4.
- `scripts/build_creative_deck.py` — reusable single-file HTML assembly script for Step 5. Run with `--help` for usage; takes a JSON manifest of {label, path, type} entries and a template style, outputs one self-contained HTML file with all media base64-embedded.
