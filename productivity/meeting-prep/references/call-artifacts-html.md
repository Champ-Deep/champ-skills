# Call prep HTML artifacts (visual page and call script)

Deep expects prep visuals and call scripts as standalone HTML pages, not themed chat widgets. Both are posters: they set their own background, fonts and margins (the app lets standalone pages override the widget theming).

## Shared style

- Dark war-room palette: near-black background, panel surfaces, muted text, mono font stack for numbers and labels, system sans for prose. Define all colors as CSS variables at `:root`.
- Cards with a 2px colored top accent set via `--ac` on the card: red = risk/blocker, green = proof of work or commitments, amber = the uncomfortable part, blue = agenda, teal = asks.
- Big tabular mono numerals for data bands (e.g. 691 accounts, minus 260, minus 13, minus 1, equals 417 eligible), with the formula shown as a flow line.
- Responsive: grid collapses to one column under ~900px so it works on a phone during the call.
- No em dashes in the HTML text either.

## The visual page

Sections, top to bottom: headline band stating the real nature of the call ("this is no longer a delivery call", with the client-side context as status chips), three cards for the things to settle or lead with before noon, the proof-of-work numbers band with the country/segment split, the timed agenda, the commitments, the objection bank, the two questions to ask, the do-not-say list, the after-call list, and a straight-talk footer.

## The call script page

- Timed sections (0:00 to 0:03, 0:03 to 0:10, ...) as rows: time stamp, section title, a stage-direction line in italics, then the words to say in bordered quote blocks with a small uppercase "You say" label.
- For a question with an unresolved fork, show both variants in the same section: the main line and an "alt" quote block (amber border), with the branch condition stated in the direction line.
- Objection bank: each objection as a question header (amber) with a "Say this" quote block, including stage directions in italics where a reply must not over-explain.
- Do-not-say list pinned near the bottom, plus the after-call checklist (file the outcome note, send the written recap within two hours, close the open task).

## Interactive pieces

When the call turns on figures Deep does not hold yet, build the page as a form, not static text: editable inputs for the counterparty's figures, the currency converter as an editable assumption, a live verdict line that re-colors against the benchmark band, and a totals row that recalculates as rows are edited. Every unknown figure renders as an amber `[PASTE ...]` placeholder and a banner at the top states what could not be found, so the page never implies data that does not exist. Money bands and per-item math go in tabular mono so columns line up while being edited.

## Two variants: internal prep vs partner-facing

The dark war-room style above is for pages only Deep sees: prep visuals and call scripts, opened as a second screen during the call. When the page is built for a partner to receive or to see on screen share, invert every choice in that section:

- Light, warm background on the partner's brand (their logo and accent, not ours), co-branded header lockup with both marks and an anchor nav.
- Interactive over dense: clickable stepper driving a detail panel, model tabs, a tickable decisions list that persists across reload (`localStorage`), rather than wall-to-wall text.
- Every position framed as proposed: eyebrow pills (proposed by us / for discussion), the counterparty's own figures badged as theirs, unconfirmed counts listed as open items.
- Section shape that ends the call with decisions: status, staged path with dates to their enforcement date, partnership roles and channel models, pilot checks, tickable decisions, owners-and-dates table.

Both variants ship from a template plus a build script kept in the scratch dir, with the vault file as the built output, so a fix is one re-run rather than an edit inside a 140KB generated file.

## The paired kit: a shared showcase plus a private script

Two files, two windows: `1 - SHOWCASE (share this screen).html` in the counterparty's brand
(their logo base64-inlined so it opens from disk with no CDN) and `2 - SCRIPT AND NOTES (keep
private).html` in the dark war-room style above. Never one file with a hide-internal toggle:
Deep must read the script while the showcase is on screen, and a toggle gets left open.

- The showcase top bar links to one anchor per section (`#who-we-are`, `#next-step`), and every
  script phase carries a "be on showcase section" pointer to that anchor, so he can drive the
  screen in one click while reading.
- The script carries a countdown to the invite's own start time and a running timer after
  dialling, the minute rail with word-for-word lines, the cheat-sheet facts, the objection
  lines, and a `DO NOT SAY` block built from the showcase's exclusions (see
  11c in `SKILL.md`: the two files are mirrors, and a category hidden on one side but unsaid
  on the other is a leak waiting to happen).
- **Leak-test the showcase before delivery**, in addition to the dash count: grep the showcase
  text for the internal-word set (script, internal, private, the do-not-say block's own
  headings, employee names, vault paths, verdict and candidate labels) and require zero hits.
  A leak test that only counts dashes passes a page with the internal notes still on it.
- Persist the script's tickables and notes box in `localStorage`, one key per item, and prove
  the state comes back after a reload (see the harness recipe under Verification).

Because both files carry brand and `visual-verify` gates, route the build as a frontend
kanban card rather than `delegate_task` when the window is tight.

## Resolving the counterparty's name before you build

Deep says names phonetically, and the spelling he gives often exists nowhere in the vault: zero hits under one spelling while the folder, the prep notes and the attendee address all read another. Treat a zero-result vault sweep as a spelling miss before treating it as a missing record: search the clients folder by case-insensitive fragments, read past the handful of false hits (usually unrelated binary noise), and resolve against the calendar's event subjects and attendee addresses, because the invite carries the counterparty's own spelling. Also reconcile the variant in our own files: TASKS.md can carry one first name where every other record says another, and the page must use the record's spelling, not the task's.

When the calendar view comes back as a blob too large for context, parse it from its spillover file instead of re-requesting it, tolerating the trailing note after the JSON:

```python
import json
t = open(spillover_path).read(); i = t.find('{')
d, _ = json.JSONDecoder().raw_decode(t[i:])   # json.loads dies on the trailing text
for e in d['value']:
    print(bool(re.search(r'frag', json.dumps(e), re.I)), e['start']['dateTime'], e['subject'])
```

Batch that with the Wispr search and the mail search on counterparty domain and personal names in the same turn: the last real discussion is usually a transcript or a thread, not a file.

## Filling in the owed items on an existing page

When Deep asks for the info behind a "we owe them" list on a prep page, he wants each item filled, not restated. Recon first, in one batch: the `TASKS.md` rows for the counterparty, the `Atlas/Ops/Dispatch/` Ready to Send files and `Atlas/Zoom Triage/Send Kits` that carried the item, the weekly follow-up reviews (a kit still listed as carried is the proof it never went), and the client folder's meeting history and solution mapping. The send claim always gets checked against the mailbox search before it is written up: a kit marked READY through several reviews plus an empty Sent search means it never went, and that is the fact the section is built on. The send kits usually hold the verbatim commitment, which is what the timeline quotes.

Then write each item as one block carrying five parts:

1. **Status chip** with the state and when it was made ("Promised 17 Sep · not sent").
2. **One plain sentence** of what is actually owed and what is missing.
3. **Timeline**: the dated sequence from commitment to today, from the send kits and dispatch logs.
4. **Evidence line**: the `TASKS.md` row numbers and the file path, in mono.
5. **Say-it line**: the word-for-word line for the call, plus an amber branch for when he pushes back.

Where the record has no owner or no figure, say so as a callout on the card ("no sales owner is recorded anywhere in the vault") and make naming it a pre-call action. Never fill the gap with a plausible value. A hero stat strip above the ledger gives the page its at-a-glance shape: days slipped, items owed, minutes before the hard stop.

## Verification

1. Grep the file for em dashes: the count must be zero.
2. Drive the page's JS in a scripted DOM harness (jsdom installed into the scratch dir): dispatch `input` events on every calculator, table and scorecard control, then assert the computed totals and verdict text. This proves the behavior with no browser in the loop. A `localStorage` tick that must survive a reload gets the same treatment: set it, reload, assert the state came back.
3. Shoot at 1440 and 390 with Playwright when the browser bridge is down, and say plainly that the layout check ran through a script rather than the usual gate:

```bash
cd ~/.hermes/cache/scratch && uv run --with playwright python shot.py   # installs into a throwaway env
```

   The probe script needs `document.documentElement.scrollWidth > innerWidth` at both widths, a `pageerror` listener for console faults, and a full-page PNG per width to open with vision. Judge the Pngs, do not just count them.
4. A partner-facing page clears the full `visual-verify` gate instead: audit at 390 and 1440 (zero FAILs), shoot, open every PNG, critique, fix, re-shoot. The jsdom harness covers logic only; it cannot see layout, and a replayed entrance animation in a capture reads as empty space (see `visual-verify` on forcing the animated end state in CSS for captures).
5. State honestly which layer was verified. A passing DOM harness covers logic, not layout; if no browser could be opened, say the layout is unchecked instead of implying a rendered check.

## Pitfalls of the built page

- **A comparison table scrolls sideways on a phone.** `overflow-x: auto` on the wrapper passes every overflow probe while half the text sits off screen, which is fatal on a page read live during a call. Stack it instead: `table, thead, tbody, tr, th, td { display:block }`, `thead{display:none}`, each `td` carrying `data-l="Column"` rendered as a label through `td::before{content:attr(data-l)}`, first cell's label suppressed. Re-shoot at 390 and confirm no cell is cut off: a rect probe cannot tell a readable cell from a truncated one.
- A write over a file that was only partly read is refused. Read every page first, or re-read in full when the refusal comes back; the stale retry fails the same way and burns the window.
- A restyle rewrites the file, so restate every section in the new markup in its original order and run the dash grep again: a rewrite drops the section nobody mentioned.

## Delivery

1. Write the file into the vault next to the prep note (`Calendar/Meetings/` for time-bound meeting artifacts).
2. Internal pages render inline in chat with `::preview{file="/abs/path.html"}` on its own line.
3. Partner-facing pages are delivered as file cards instead: `MEDIA:/abs/path.html` plus a PDF print of the same page beside it (Playwright `page.pdf(...)`), since the partner may need to open or forward them outside chat.
4. Mention the saved path so Deep can open it full-screen as a second-screen aid.
