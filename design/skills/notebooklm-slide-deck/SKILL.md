---
name: "notebooklm-slide-deck"
description: "Create a Google NotebookLM notebook from a set of prepared documents (client context files, meeting prep, research briefs, or any other document set for any client) and generate a Studio slide deck, then have Claude itself author speaker talking points from the finished deck. Use whenever the user has assembled or been handed a document set for NotebookLM and wants a notebook + slide deck generated — triggers: \"create a notebooklm slide deck\", \"feed this into notebooklm\", \"put these docs in notebooklm and make a deck\", \"notebooklm deck\", \"generate the slide deck from these sources\", or as the natural follow-on after meeting-prep, case-study-builder, or any workflow producing a \"documents + prompt for NotebookLM\" deliverable. Entity-agnostic: works for any client/project using whatever documents exist in the session, never hardcoded to one company. Drives the browser via Claude in Chrome MCP tools, never native computer-use."
---


# NotebookLM Slide Deck

Turns a document set (already gathered — e.g. a client context folder, a meeting prep pack, a
research brief, or any other collection of source material for any project) plus a generation
prompt into a live NotebookLM notebook with a Studio slide deck, then has Claude write the
presenter's speaking notes from the finished deck. This skill is generic: it applies to whatever
client, project, or entity the current task involves. Never hardcode a specific company name,
folder path, or deck topic into the skill itself — those come from the task at hand.

The documents and the prompt should already exist by the time this skill runs; this skill's job
is purely the mechanical NotebookLM setup and the follow-on script-writing, not deciding what
should go in the deck.

## Before touching the browser: verify the document set is complete — for real, not just a mental check

This is the step most likely to go wrong, and it has gone wrong before: a full context folder was
gathered (profile, meeting history, pain points, solution mapping) but the actual finished
deliverable the whole exercise was built to support — the meeting prep document itself — got left
out of the upload. A mental "does this look complete" pass is not enough to catch that, because
the supporting docs *look* like a complete set on their own.

Do this instead, every time:

1. Run an actual directory listing (`ls` or the file tool's directory view) of every folder the
   documents came from — the client/project context folder AND wherever the primary deliverable
   lives (e.g. a separate meeting-notes location, a standalone brief, a deck draft). Don't rely on
   memory of what you created earlier in the conversation.
2. Write out the full list of files you're about to upload and check it against that listing.
   If a folder produced 5 files but only 4 are in your upload list, stop and find out why before
   proceeding — don't assume the 4 were "the important ones."
3. The rule of thumb: if a task involved *preparing* something (a prep doc, a brief, a proposal)
   before it involved *packaging* it for NotebookLM, the prepared thing itself is a source, not
   just the research that fed it.

## Writing the generation prompt: slide content only, never a verbatim script

Never write a prompt that asks NotebookLM to put a "near-verbatim speaker script" or word-for-word
talking points onto the slides themselves. A slide deck is a visual surface — concise headlines,
key figures, short phrases. The deck-generation prompt should ask only for slide *content*: what
appears on screen, kept tight. The speaker script is handled entirely differently — see the next
section — it is never requested from NotebookLM at all.

## Writing the speaker script: Claude authors it, not NotebookLM

Once the deck exists, the presenter's talking points are written by Claude, reading the finished
deck directly, not generated as a NotebookLM follow-up query. This keeps the script tightly bound
to what's actually on each rendered slide (NotebookLM's own text extraction of its own deck can
drift from what actually got rendered) and lets Claude apply the user's actual speaking voice and
context (who's presenting, to whom, what's diplomatically sensitive) rather than a generic prompt.

To do this:

1. **Export the deck as a PDF or image set** from NotebookLM Studio (or have the user upload the
   exported file if they've already downloaded it).
2. **Render the deck to images first, then strip any watermark from the rendered images** — do
   this before reading the slides, not after. Convert PDF pages to PNG with `pdftoppm` (PDF text
   layers from slide exports are often unreliable or absent, so the rendered image is the source
   of truth anyway), then clean each page image:
   - **Preferred tool: the ChamPDF API** (`Champ-Deep/ChamPDF`, `v2` branch), if a deployment is
     configured for this workspace. Verified working 2026-07-30 against a live instance at
     `https://champdf-api.64.227.154.215.sslip.io`: `POST /api/remove-image-watermark` is a
     no-API-key legacy endpoint (LaMa inpainting) that takes multipart `file` plus a `regions` form
     field — a JSON array of `{"x":,"y":,"w":,"h":}` pixel rectangles (note: `w`/`h`, not
     `width`/`height` — the API returns `Invalid regions JSON: 'w'` if you send the wrong keys).
     Tested end-to-end against a synthetic bottom-corner text watermark and the output was clean
     with no visible artifact. Two gotchas confirmed on this deployment: (a) `auto_detect=true` and
     the sibling `GET /api/detect-watermark` endpoint both depend on reference templates that
     aren't configured on this instance (`has_templates:false`, and `GET /api/capabilities` reports
     `watermark_autodetect:false`, `gemini_inpaint:false`) — auto-detection will not find anything,
     so **regions must be supplied manually** (eyeball the rendered page image for the watermark's
     pixel box); (b) nginx on this deployment rejects uploads above roughly 1MB with a bare
     `413 Request Entity Too Large` — downscale full-resolution slide renders before upload (e.g.
     resize, or render at a lower `pdftoppm -r` DPI) if a page image is large. The richer PDF-native
     endpoint (`POST /api/v1/pdf/remove-watermark`, region rects in PDF-point coordinates, cleans
     the whole PDF in one call) exists and is documented in `backend/API_V1.md`, but requires an
     `Authorization: Bearer <api_key>` header — self-serve key minting is disabled on this instance
     (`api_self_serve_keys:false`), so that path needs an existing key or the admin token before
     it's usable. Until a key is available, use the no-key per-image endpoint above.
   - **Fallback**, if ChamPDF isn't reachable or isn't configured for this workspace: a small
     Python/Pillow crop-and-fill, a PDF utility from the `pdf` skill, or manual removal by the user
     before upload. Don't treat watermark removal as a hard blocker either way; it's a mechanical
     cleanup step, and a watermark that can't be stripped shouldn't stop the script-writing that
     follows.
3. **Read every rendered slide image** (already produced in step 2 above) — this is what the
   script gets grounded in, not any text layer extracted from the PDF.
4. **Write the talking points slide-by-slide**, grounded only in what's actually on each slide plus
   whatever context the user has already established about the audience and goal. Keep the tone
   conversational and speakable, not a formal script to recite verbatim, unless the user specifically
   wants a word-for-word script.
5. **Package the result** in whatever format the user asked for — commonly an executive one-pager
   (see the `executive-one-pager` skill) with an overview plus a slide-by-slide talking-points
   section, but follow the user's actual request rather than defaulting to one format.

## Steps

1. **Get browser tab context.** Call `tabs_context_mcp` (with `createIfEmpty: true` if no tab
   exists yet) to get a valid `tabId` before doing anything else.

2. **Navigate to NotebookLM.** `navigate` to `notebooklm.google.com` on that tab. If prompted to
   sign in, stop and ask the user to sign in manually — never attempt to fill credentials.

3. **Start a new notebook.** Use `find` to locate the "Create notebook" control (first-run) or
   the equivalent action if notebooks already exist, then `computer` with `left_click` on it.
   NotebookLM will drop you into an empty notebook's source-upload view.

4. **Verify the document set (see section above), then upload via `file_upload` — never by
   clicking the upload button and driving a native file picker.** The native OS file dialog that
   appears after clicking "Upload files" is invisible to browser tools and cannot be navigated
   with clicks or keystrokes; that's exactly the situation `file_upload` exists to skip. Use
   `read_page` or `find` to locate the hidden file `<input>` element behind the "Upload files"
   control, then call `file_upload` with its `ref`, the `tabId`, and the absolute paths of every
   verified document. All files in one call is fine as long as their combined size stays under
   10MB; split into multiple calls if the set is larger. Only files already shared with the
   session (attachments, the session's outputs/uploads folders, or connected folders like a vault)
   can be uploaded — confirm the documents live somewhere in that scope before starting.

5. **Wait for source processing.** NotebookLM ingests and titles the notebook automatically once
   sources are added — this can take a little while for longer documents. Use `read_page` or a
   `computer` `screenshot` to confirm all sources show as processed (not still spinning) before
   moving on.

6. **Open the Slide deck generator.** In the Studio panel, `find` and click "Slide deck". This
   opens a "Customise slide deck" modal with format (Detailed deck / Presenter slides), length,
   source-selection, and a free-text description field.

7. **Paste the prepared prompt into the description field** — slide content only, per the rule
   above. Sanity-check any prompt written before this rule existed, since it may still ask for
   verbatim scripts on-slide.

8. **Generate.** Click "Generate" and let NotebookLM produce the deck. This runs asynchronously
   in Studio — report back to the user once generation has kicked off rather than waiting
   silently, since it can take a few minutes.

9. **Once the deck is ready, move to the speaker-script phase** (see section above): export,
   render to images, de-watermark the rendered images, read every slide, and write the talking
   points as their own artifact — never as a NotebookLM follow-up query.

10. **Capture the notebook URL.** Once the notebook exists, note its URL (visible in the address
    bar) and, if the source documents came from a client or project context folder, save the URL
    back into that folder's profile note (e.g. append `NotebookLM: {url}` to the relevant profile
    file) so future work on the same client/project can find and reuse the notebook instead of
    creating a duplicate.

## Notes

- If NotebookLM's UI has changed since this was written (button labels, modal layout), fall back
  to `read_page` with `filter: "interactive"` to re-discover the current controls rather than
  guessing at coordinates from memory.
- If `file_upload` reports a file was rejected, it's almost always because the path isn't within
  the session's shared scope — check the path before retrying, don't just repeat the same call.
- If a PDF export has more than 10-15 pages, render and read it in batches — some environments
  reject very large batched image reads in one call.
- This skill produces two artifacts: a NotebookLM notebook with a slide deck, and a separate
  Claude-authored speaker-notes deliverable. It does not further edit the deck itself — if the
  user wants the deck's visual content changed, treat that as a separate follow-up in NotebookLM.

