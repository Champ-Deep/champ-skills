---
name: remote-podcast-recording
description: "Use when setting up a podcast or webinar recording."
---

# Remote podcast recording

A recording has four deliverables in order: capture (the only thing that cannot be redone), the host's script, the show notes, then the copilot if it is wanted on air. A beautiful show notes page with no isolated audio track is a failed recording.

## Step 1: Establish the facts before advising

The host does not choose the platform, so the tier decides everything downstream. Ask, do not assume, in one batch:

- Which platform and which **edition** (Zoom Webinar vs Webinar Plus vs Events; Riverside, Zencastr, SquadCast, StreamYard). The tier is the difference between having isolated tracks and having a single mixed file.
- Is there a live audience? A webinar with attendees needs registration and a moderated Q&A; without attendees it is a closed studio and no link should go out.
- Who owns the record button and who joins as a panelist.
- Is the guest on the same platform or dialling in by phone (phone audio cannot be isolated from the host's track).
- The exact start time in IST, and whether it was said in the invite, the calendar or chat. Present a conflict as one `needs_input` block with the times and platforms as options; never pick a recording time yourself.

A claim about a tier must come from the vendor's own page fetched in the same session, quoted back with its URL. Vendor tier tables change and the guest's host account is the authority, not the vendor's marketing page.

## Step 2: Get isolated tracks out of the host's platform

Zoom Webinar (verified on Zoom's own pages): **Recording Studio** records each person locally and uploads the files, and Zoom's help article scopes it to Webinars Plus and Events sessions, not plain Webinars. Without it, the cloud recording settings are the substitute: "Record active speaker, gallery view and shared screen separately" (three files) plus "Record a separate audio file of each participant" (one audio file per person). Set both, because the editor needs a clean two-up, a speaker cut, the screen share on its own and per-person audio.

In the call, every panelist does the same four things or the track is unusable: Original Sound on (Zoom app Audio settings), HD video on, touch-up and virtual background off, wired headphones on. A guest who joins by computer audio but on speakers feeds the host's mic.

## Step 3: Belt and braces on the host's own machine

Every local track is a bet against the platform, so run one independent capture on the host's Mac for the whole session: QuickTime, New Movie Recording, camera and mic at Maximum quality. It costs nothing and it is the only track that survives a platform failure.

Two things make it work: test it in the tech check that QuickTime and the platform share the camera cleanly (macOS will otherwise take the camera from one of them), and have every participant clap once together right after Record so the local track can be synced.

If a second independent service is wanted (the guest records their own side), Zencastr and VDO.Ninja are the usual free options; the guest records their own side only if they are comfortable, and the host asks once rather than assuming.

## Step 4: Run a real tech check, then stage the host's script

The tech check is 15 minutes with the host and the guest: record 60 seconds, download the files, listen on headphones. It is the only proof the tracks exist; a green "recording" indicator is not proof.

The host's script is a second-screen page, not a document. It must separate three kinds of text by look, not by colour alone: **spoken lines** very large with a left accent bar, **stage directions** smaller and muted, **verify tags** (anything to confirm before broadcast, `[Confirm ...]`) as an amber chip. Reading distance is about 70 cm beside a camera. Port the spoken lines verbatim from the source pack; never rewrite the guest's answers or the host's confessions into "better" copy.

Structure it as a run of show with a minute window per step, a clock that counts up from Record, arrow-key or space to advance, a collapsible "do not say" card, and the active listening cues permanently on screen (wait two seconds, reuse her words, take every principle to one example, summarise every second question, pause on a quotable phrase instead of adding to it).

Give the opening both ways and let the host toggle: version A has the producer hand over in ten seconds, version B is the host alone. Record the guest's own words for why she is qualified rather than a summary of them.

When the guest has arrived with her own prepared questions, they go in word for word as the large spoken lines. Never paraphrase them, never expand them into a longer version, and never rewrite them into "better" questions: she has rehearsed that exact wording, and the script's job is to hand her back what she prepared. Around each question, one short conversational lead-in is enough ("Let's start with the dashboards themselves."), and the probes stay to two, skipped when she already answered them in the answer itself.

Shortening the script means cutting spoken lines, not the minute windows. The run-of-show parser keys off the fixed window prefixes (`0 to 2`, `5 to 13`, ...), so a redo that renumbers the windows must update the parser's row regex in the same pass or the build asserts out. When the interview itself will be shorter, say so on the page (the host can stop early) instead of padding the script to fill the clock.

## Step 5: Show notes as a tool roundup, not a marketing page

The page must be hosted as a public URL that loads before the episode airs, not a file on disk: it gets shared on air and afterwards, and a local file cannot be pasted anywhere. Deep rules on hosting; the build sets it up and confirms the live URL loads. Full structure and the hosted-link rule: `celsus-client-call-prep`, "Audience-facing resource page for a live episode".

Deep's rule for a podcast resources page: the tools are the content. One card each with a real screenshot taken in the build, a short description taken from the tool's own page or README, a "why it is here" line and one link. No testimonials, no pricing, no scroll animation, no performance claims, no star counts. Exclusions are deliberate: internal tools, competitor tools, unverified tools and anything whose assessment has not been read are left out and listed as exclusions in the handover.

Every link is curl-checked before a card ships and a dead link drops the card rather than the whole page. Do not invent a description because the page cannot be fetched; drop it.

## Step 6: The copilot (optional, and only if a permission exists)

A live copilot that listens to the guest must capture the Mac's own output, which macOS gates behind Screen & System Audio Recording permission. Without that permission the capture layer fails with a declined TCC error and the page shows a stopped status; the fix is the permission, not a code change, and it cannot be granted from inside a session. Ask for it in System Settings before the recording, and test with one played video before relying on it.

Serve it on `127.0.0.1` and add `Access-Control-Allow-Origin: null` to its JSON response, or a page opened from `file://` (which sends a null origin) cannot read it. Only the guest's transcript text should leave the machine; the audio stays local, and the advice model goes out on the shared OpenRouter key, which has a weekly limit to check first.

## Pitfalls
- **Never give a recording time as advice.** Two different surfaces will state two times for one recording; presenting both as a `needs_input` block with the times as options is the whole answer, and picking one silently risks a missed recording.
- **Do not promise Riverside-equivalent quality on a tier that does not have it.** Ask the host's edition first and quote the vendor page; if the edition lacks local tracks, say so and fall back to the separate-track cloud settings plus a local backup on each end.
- **A summary of the guest's own introduction is a rewrite.** Use her words verbatim for why she is qualified, because she is the one on the call and the summary will be checked against her answer.
- **Never leave verify tags in spoken text.** Anything unconfirmed gets an amber chip and a confirm-before-broadcast line, so a fact that is wrong on air is caught in the tech check, not by the audience.
- **A copilot that cannot capture is a permission problem, not a broken feature.** Report the permission to grant and the one-line proof of it working; do not describe the code path as working.
- **Show notes are not the place for internal names.** The public page must not carry producer names, internal tool names, file paths or card ids; those live in the host's private script.
