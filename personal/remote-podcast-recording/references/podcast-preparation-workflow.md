# Podcast preparation workflow (per episode)

The procedure that turns a booked episode into a host script, a resource guide and a clean handoff, without sending, posting or promising anything. Run it top to bottom; every step names the evidence that closes it. `scripts/prep_gate.py` asserts the gates at the end.

## 0. Reuse before building

Search the vault, the board and the mailbox for the same episode first: an existing host pack, script page, resources page, Manu-style page request, questions mail. Extend what exists. A second build or a second draft for the same ask is a defect, not progress. Existing cards own their own work: link them, never recreate them.

## 1. Questions: the guest's wording wins

Read the questions the guest actually agreed to (sent mail, her reply, the booking thread) before touching the script. Carry each one verbatim as a spoken line. Add one lead-in and at most two probes around it. Rewriting is allowed only for the host's own lines, never the guest's questions. If the current agreed list cannot be read (no mail access), say so and keep the last known list marked unverified. Do not resend an old questions mail; first read Sent for it.

## 2. Roles and script

- Greeting and handoff: name who opens (producer or host), the exact handoff line, and which on-air name the guest knows each person by. A corrected name never erases the other name from the page.
- Loose script, not a teleprompter: run of show with minute windows, one lead-in and two probes per question, "you add" stories kept short, and the active listening cues always visible (count two, reuse her words, one example per principle, one line of summary before a new question, pause on a quotable phrase).
- Include off-air minutes: how she wants to be introduced, recording and publication comfort, topics to skip, anything visual she will show.
- Keep a "do not say" card: fees, barter, audience size, publish date, client names, unverified figures.
- Anything unconfirmed is an amber verify chip, never spoken text. Send the redo to the producer only as a staged draft (step 8).

## 3. Rehearsal checks

Record what the rehearsal showed, and only that. Typical observed items: the host cannot turn video on until rejoining as a panelist; spotlight works and non-video participants can be hidden; local recording is available to the producer; the virtual background is not mirrored. These are observations. They do not establish isolated tracks, licence tier, tested file quality or publication consent, so each of those stays "unverified" until a downloaded file or an admin page proves it (see Step 2 and Step 4 of the main skill). A record button, a green indicator or a feature menu is never evidence.

## 4. Consent and production evidence

Two separate records: (a) consent, meaning the on-recording consent line plus the guest's off-air yes, and (b) production, meaning downloaded files you listened to. Having a button, a licence page or a setting does not close either. Write each as "evidenced by <artifact>" or "unverified".

## 5. Safe screen share

Share one browser window (the resources page or prepared screenshots), never the desktop. Use a clean browser profile or prepared captures. Kanban, mail and the vault carry client data and are never on screen. Do not demo anything whose live URL or health check failed in the last 48 hours; use a screenshot or skip it.

## 6. Resource guide

- Before the recording the list is **provisional**: tools the host might mention. Label it so.
- After the episode the list becomes **actual** only from the real recording or its transcript: what was said, not what was planned. Drop planned tools that were never mentioned.
- Every card: a tool's own tagline or README (never memory), a real capture, one link. Curl every link and ship only 200 (or a redirect ending in 200). A dead link drops its card, not the page.
- Copyable agent skills are de-identified: no vault paths, names, client data, card ids, tokens, internal URLs. Copy them into the guide as reviewed text, then grep the result.
- No private vault, client or credential content in any public text. Run the leak scan in `prep_gate.py` on the exact public text.

## 7. Page route and ownership

A page route stated in a transcript can differ from the route in the page request (for example `/podcast` against `/podcasts`). Record both as proposals, name the page owner's current thread as the place to settle it, and do not create an approval card or a second page. Publishing waits for that thread and for the owner's go.

## 8. Lanes and drafts

- Mail work goes to the inbox lane as a draft brief: recipient, subject, points, the proven event state. Never ask for a send. Draft only.
- Visual work goes to the frontend lane as a full brief naming the component ids. Brand check, `visual-verify`, `responsive-viewport-qa` and `no-ai-slop` close it.
- Before staging any draft: search Drafts and Sent for the same ask (dedupe). After staging: read the draft back from the provider (To, Cc, subject, body) before calling it done.
- Do not write past-tense side effects into a draft body that has not been executed and read back.

## 9. Timing and occurrence gates

- Two surfaces that state different times (a spoken zone, a host pack, an invite body, an invite start field) are a conflict. Convert both to UTC for the same date, name the gap in minutes, record it, and leave the choice to the card that owns timing. Never pick a time. Open one `needs_input` block only when no card owns timing yet; never a second one.
- A pre-event send (join early for sound check, share questions, agenda) needs proof the event has not happened: search the mailbox for a recording-ready mail and read the dated meeting notes. If the event already happened, the send is obsolete; stage nothing.
- "Happened" is claimed only from such evidence, never from the plan.
- Post-event follow-ups (support offers, barter, consulting) stay held until the occurrence is proven and the owner releases them. Preparing a skill or a guide never releases them.

## 10. Close

1. Fill a state JSON like `references/example-state.json` from real evidence.
2. `python3 scripts/prep_gate.py state.json` must print `PASS`.
3. `python3 scripts/test_prep_gate.py` proves the gate itself still catches each failure.
4. Hand to the reviewer lane with the note, the gate output and what was not checked. Nothing is sent, posted or published by the preparer.
