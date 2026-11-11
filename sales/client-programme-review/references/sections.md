# Sections, widget contracts and build wiring

Built on the `showcase-page` kit (`core.css`, `core.js`, `build.py`, `shoot.py`). One template, one stylesheet, one data script, one build script, one probe.

## Files

| File | Role |
|---|---|
| `engine/make.py` | `python3 make.py <client_dir> [--final]`. Runs `client.py`, loads the simulation run if there is one, applies the ledger gate, fills the template, calls the kit's `build.py`, then checks the built page against the ledger. |
| `engine/probe.py` | `python3 probe.py <client_dir>`. Drives every control in a browser and asserts the result. Skips sections the build drops. |
| `engine/review.tpl.html`, `engine/review.css` | Template and styles. Tokens: `{{c:key}}` copy from `COPY`, `{{h:name}}` a list rendered by `make.py`, `{{x:name}}` computed. |
| `<client_dir>/client.py` | The one file per client. |
| `<client_dir>/ledger.json` | The reconciliation ledger. An entry may carry `"section": "<id>"`; it is skipped when the build drops that section. |
| `<client_dir>/sim_notes.json` | Only with a simulation run: `fixes`, `asks`, `rewrite_note`, and the `ranking` the notes were written against. |

## The client.py contract

`make.py` reads these names. The sample defines every one, with comments.

| Name | What |
|---|---|
| `SLUG`, `CLIENT`, `BRAND`, `NOTE_TITLE`, `META` | File name, short client name used in sentences, the brand on the page, the first line of the send-back note, and the kit's page meta (title, chip, call to action, footer). |
| `LEADS` | One dict per lead. Required keys: `id` (1 to n, in order), `co`, `role`, `ind`, `mkt`, `named`. Every other key is yours and is referenced by the config below. |
| `SENDS` | `[name, dates, clicked, opened without a click, not opened, sent]` per send. |
| `UNIVERSE` | `contacts`, `emailed`, `dialled`. One dot is drawn per contact. |
| `NAMED` | `by` and `on`: who named the marked leads, and when. |
| `MARKETS` | Code to name. The first three get distinct dot colours. |
| `FILTERS` | `[key, label, field, value, negate]`. The first is the "all" filter with no field. |
| `CARD` | `facts` and `pills` shown on a lead card, and which answers read as `go`, `no` or `na` (not asked). |
| `DIMS`, `DISP`, `SUF` | The dimensions the win profile compares, display names for raw values, and suffixes. |
| `COPY` | Every sentence and list on the page. A missing key stops the build and names itself. |
| `SECTIONS` | Optional. The section ids to build, in page order. |
| `SIM_RUN` | Optional. Path to a simulation run. A variant label must end with the number of the send it was used in. |

## Sections

| Section | Must prove | Data it needs | Interaction |
|---|---|---|---|
| Hero, three stat cards | Status against the order in one number | Delivered, contracted, pending; one channel total; one quality signal | Count-up |
| Programme strip | Scope in five pills | Deliverable, markets, buyers, channels, window | None |
| The universe | How much of the addressable market has been touched | Contacts in profile, emailed, dialled, delivered | Pinned scroll: one stage per beat, dots light by stage. Clicking a beat jumps to it. Unpinned and fully lit in static export and below 1000px. |
| What we ran | The programme changed when the client asked | Dated steps; the list of reports the client received | Sticky heading, reveal on scroll |
| The messaging | What was sent and what each send returned | Per send: dates, sent, clicked. The copy as sent. | Radiogroup of sends with bars to scale. A selector re-pairs copy with a send by swapping, so each copy stays with exactly one send. |
| Simulation | Which copy a panel of the client's buyers prefers, against what happened | Ranking with bands, per-persona reactions, real click rate per copy | Radiogroup of messages; persona dots open their reaction. Real click rates follow the pairing chosen in the messaging section. |
| Lead board and win profile | Who the leads are, and what the progressing ones share | The lead table; which leads the client named, by whom, when | Mark up to three as moving; filter pills with counts; a profile panel that recomputes on every mark and lists the closest matches among the other leads. |
| What we learned | Each lesson changes how the next phase runs | Aggregates from the lead table and the send reports | Bars animate to value |
| What we need | The outcomes only the client can see | The asks | Tick list; the send-back note |
| Win profile study | What we will research once they name their wins | Dimensions known today and added by the study; public first pass on where the audience gathers | Drag-and-swap bento |
| Tiers | Three ways forward, each including the last | Tier contents; three numbers from the programme that make the case for the top tier | Radiogroup; detail panel |
| Closing line | The most concrete fact on the page | Computed | None |

## Widget contracts

**Lead board.** `named` on a lead row marks the ones the client has already named. With none named the board opens empty and offers no shortcut. With some named it opens on them, labels the panel "named by <who> on <date>", and offers one button to return to them. A fourth mark drops the oldest.

**Win profile panel.** For each dimension, a trait joins the pattern when at least two thirds of the marked leads share it. A dimension where fewer than that have any value on record is listed under "not on record", never under "no pattern". Closest matches are the unmarked leads sharing at least half the pattern.

**Pairing selector.** Choosing a copy for a send swaps it with the send that held it. The simulation's real click rates and the per-send simulated rank read the pairing. When the pairing is not the default, the comparison sentence in the simulation section is replaced by one that says the pairing was changed.

**Bento.** Vanilla port of 21st.dev Draggable Grid Dashboard (id 30238, swapy hover mode). Seven slots on a twelve-column grid: one double-height slot, four standard, two wide. The slot owns the rank badge and the size; the tile owns the content. Dragging over another slot moves that slot's tile into the dragged tile's home. The first three slots are the reader's priority and are read out in a live line. Arrow keys, Home and End on the handle reorder. Touch drags from the handle only. One column below 760px.

**State and the send-back note.** One object in `localStorage`, keyed by the page slug, skipped in static export. The note lists the marked leads, the ticked asks, the first three in the order (only when the reader changed it), the tier (only when the reader chose it) and the pairing (only when changed). Copy uses the clipboard and falls back to selecting the text, with a status line that says nothing was sent.

**Draft ribbon.** A fixed red strip naming every open ledger entry. Present in every non-final build, absent in a final one.

## Probe checklist

Every item is an assertion, not a screenshot: universe stages in order; board opens on the named leads or empty; a fourth mark keeps three; clear and restore; filter count; pairing swap changes the email shown, the real click rates and the note, and reset restores them; bento swap by keyboard keeps focus on the handle; bento swap by mouse leaves one tile per slot; reset restores the order; ticks, tier and copy write the note; a reload restores every mark; a fresh visitor's note claims nothing; no in-page anchor opens a new tab; zero console errors.
