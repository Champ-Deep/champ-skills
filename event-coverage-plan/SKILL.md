---
name: "event-coverage-plan"
description: "Use when Deep's team attends an expo, summit or conference."
---

# Event coverage plan

The deliverable is one shareable HTML page that tells each person where to start on the
floor, what to ask, and what to bring back, plus the decisions only Deep can settle. The
page is the output of the plan, not the plan: roster, sectors and source data are settled
first, then the page is built from them.

Build the page with `visual-report-builder` (craft, structure, brand) and close it with
`visual-verify` (audit, screenshots, critique). This skill is what goes into it and in
what order.

## When to Use

- "My team is heading to <event>" / "plan our team for <summit or expo>"
- "Who should cover what on the floor?"
- "What does the pass actually include?"
- Any multi-person conference attendance where each person needs a stall list, questions
  and a capture routine.

Not for a client meeting agenda (that is `client-call-prep`), and not for a timetable of
sessions to watch (a plain table, no skill).

## Step 1: lock the roster from one source

Take the attendee list from one authoritative surface (the kanban board, or the task
record) and reconcile every name you find anywhere else against it before designing a
single assignment. Names that appear in notes, indexes or a prior event's list but are not
on the roster get dropped and reported in chat, not kept "in case".

Why this comes first: an assignment built from a merged list names people who are not
going, and the page then ships an allocation nobody can act on. One source, reconciled
once, beats a union of plausible sources.

Also settle in this step, in writing: who has no sector, who attends only one day, and
who is out (travel, calls). Each of those gets an explicit option on the page or in chat,
never silence.

## Step 2: derive every sector from work the person already owns

A sector is assigned from evidence: the person's KRA scope, their recent commits, the
decisions on their own accounts. Never from an idea that would be interesting for them.
Tag each card two ways:

- **Set** for sectors the principal already scoped.
- **Proposed, confirm** for anything you inferred from their scope.

Every Proposed card is one `needs_input` decision card, not five: the options, your
recommendation first, and a reply format ("A on <card id>"). Do not move people into
sectors they were not scoped into and hope it reads as agreed. The page carries the tag
until the ruling lands, then the tags flip and the page is shared.

Where two people would chase the same thing (data quality, security, AI models), split
explicitly on the page and say who owns which half, so the plan does not send two of them
to the same stalls.

## Step 3: build the floor from the event's own sources

Pull, in this order:
1. **Pass entitlement page**: what the free or press pass covers and what it does not.
   Exhibit halls are usually covered; conference stages, masterclasses, networking,
   lunches and summit add-ons usually are not. Quote only what the page says.
2. **Exhibitor directory feed**: fetch the full directory as data (JSON endpoint behind
   the listing page) and work from that, not from a rendered page.
3. **Venue map**: the hall layout, food courts, stage halls. A PDF URL goes straight
   through `web_extract`.
4. **Programme pages**: only for items that must survive, and only if the page actually
   names them.

Never hand-transcribe a hall, stall code or URL. Look every one up inside the build
script against the fetched dataset and make the build fail when a reference does not
resolve: a typed identifier is a transcription error that reads as fact on the page.
Count the records you fetched and put that count in the footer with the fetch date.

Facts that are unpublished (which hall a named pavilion sits in, whether a session is
open to pass holders) are stated as unpublished with an owner to ask on site. Do not
guess them into a schedule.

Before you name a well-known company on the list, check the listed domain: a global brand
name on a local reseller's page means you would send someone to a partner, not the brand.
Say so on the row when it happens.

## Step 4: label what is checked and what is inferred

Every row that names a product or a stall carries its own status: **checked** (you
fetched the company's own site and the claim is there) or **listing only** (inferred from
the exhibitor's name or domain). Fetch the sites in batches and match on the keywords that
decide the claim, rather than reading them one at a time.

The footer states three things, as separate counts: how many references were checked and
against what, how many are listing-only, and what was not checkable at all. A single
blanket "unverified" line is wrong once part of it is checked, and a status held only in
the hero goes stale the moment you check more.

## Step 5: page structure

Sections, in this order, adapted to the event:
1. **Hero**: the dates and hours, the directory size, the share of exhibitors in the
   busiest hall (computed, labelled as computed).
2. **The pass**: a split of covered versus not covered. This is the first thing a person
   needs before they plan a day.
3. **The floor**: exhibitor counts per hall as bars, with a line naming what is still
   unpublished.
4. **Who covers what**: sticky name nav plus one card per person. Each card: sector,
   why (their own scope), where to start, the stall rows, four questions to ask, and one
   line on what to bring back. The questions must be answerable by booth staff, not by a
   brochure: how does it work, what does it cost, what do you use today, would you try
   ours.
5. **The sweep**: one shared pattern everyone spots and one person acts on, so the team
   does not all chase the same prize.
6. **Capture**: the note line, copyable.
7. **The two days**: own sector first, a regroup where each person names three stalls
   for the others, return visits, last entry time.

## Step 6: capture protocol

One note line, identical fields for everyone, copied into every contact: sector, what they
use, what they like, what they want changed, next step. Fixed fields are what make two
days of scanning add up to one sheet later. Ship it as a copyable element on the page,
not as a paragraph to retype.

If the capture tool the team was promised is not ready, say so in one block near the top
with the fallback (photograph every card, keep the photos) and where the fix is being
ruled on. A tool that half works costs more time on site than one that is honestly broken.

## Pitfalls

- Assert the card count against the roster size before handoff, and name anyone the build
  dropped: a silently omitted attendee reappears as an unassigned person standing at the
  wrong hall.
- Read the event's own hours page for every edition. Exhibition hours and last-entry
  times change year to year, and a window copied from a prior event sends the team to a
  door that is already closed.
- Directory data is a snapshot. Put the fetch date beside every count, because exhibitors
  are added between the fetch and the doors, and never present the snapshot as the final
  floor.
- A keyword hit on a company's site proves the product exists, not that the exhibitor
  sells it. Mark a row checked only when the page ties the product to the company
  presenting it; otherwise the row stays listing-only.
- Never soften a pass limit into a maybe. If the entitlement page does not include it,
  it is excluded, and the page says so plainly so nobody plans a day around a stage they
  cannot enter.

## Always-on rules

- **The page is shared with the team.** It carries no decision only Deep can make, no
  internal card ids, and no individual performance data (commit counts, missed targets,
  KRA slips) even when accurate. Those travel in chat or as `needs_input` cards. A
  personal note about one attendee on a page eleven people open is a privacy failure, not
  transparency.
- Mark the page internal in the topbar: it travels as an attachment.
- Every count on the page is computed from the fetched data and labelled when derived.
- One stall list per person sized to a day, not an inventory of every exhibitor in their
  hall. Depth beats coverage: four questions asked well at ten stalls beat a list of forty.
- Rhythm over completeness: own sector, regroup, return visits, then anything else. The
  regroup is where the team's coverage compounds, so it gets a fixed time on the page.
- End the plan with what is still open and who settles it. A plan that reads finished
  hides the one thing that must happen before the doors open.
