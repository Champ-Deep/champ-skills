---
name: "client-call-prep"
description: "Build the shareable client call agenda page (agenda, outcomes, attendees, asks, after-call steps) for any external call, plus the invite, email and Zoom chat text to send it."
---

# Client Call Prep

Every external call (client, prospect, partner) gets a one page agenda the client sees before the call. This skill turns five answers into that page, publishes it as a link, and writes the three snippets that carry the link: calendar invite, email, Zoom chat.

This is the light, team-wide version. Deep's own SPIN dossier and cheat sheet live in the meeting-prep skill. Use this skill for the page the counterparty sees.

## Step 1: Intake (ask only what is missing)

Get these five things. If the person pasted them, do not ask again.

1. Client name, and who is coming from each side with titles.
2. Why this call is happening now, in one sentence.
3. The outcomes, written as decisions ("agree the pilot scope"), 2 to 4 of them.
4. Date, time with time zones, length in minutes, and the Zoom link.
5. What we need from the client before the call, and what we will send them.

Also collect: host name, role, email, and the agenda items with minutes and owner. If the person has no agenda items, propose them. The minutes must add up to the call length.

## Step 2: Build the page

Start from the template `Other/Skills/client-call-prep/template.html` in the Celsus vault. It is one self-contained HTML file with the Champions Group logos embedded and all copy in a JSON block with id `agenda-data`. Replace only that JSON. Do not change the CSS or script.

If the vault is not mounted, ask the person to attach template.html. Do not rebuild the page by hand.

JSON keys: sample (set false), host {brand, name, role, email}, client, headline (wrap the client name in curly braces to colour it), lead, purpose, when {short, date, time, also, minutes, zoom}, outcomes[], agenda[] {min, title, owner, detail}, people[] {name, role, org, why}, fromYou[], fromUs[], after[] {when, what}, closing [main text, final punctuation], updated.

If a subsidiary hosts the call (LakeB2B, SPAN, Ampliz, MetricFox), load that brand skill and override the colour tokens and logos. Default is Champions Group orange and white.

## Step 3: Copy rules (run the no-ai-slop skill as the final gate)

1. Zero em dashes and en dashes anywhere. Use commas, periods or the word "to" for ranges.
2. The headline names the client and the outcome. The lead is one or two plain sentences.
3. Outcomes are decisions, not topics. Every agenda item has a time and an owner.
4. Nothing internal on the page: no internal notes, no doubts about the client, no pricing or terms that are not agreed, no names of other clients, no vendor names.
5. No apologies and no filler. Plain words, short sentences.
6. Spell names and titles correctly. Check LinkedIn if unsure.

## Step 4: Check

Run these before publishing: agenda minutes equal the call length; every item has an owner; no dash characters (grep for the two code points); the page renders at 1440 and 390 with no horizontal overflow and no console errors; the Zoom link, date, time zone and host email are right.

## Step 5: Publish and share

Publish with the Artifact tool. Title: "{Client} Call Agenda". Keep the same file path to update the same link. Published pages are private by default, so tell the person to open the page's Share menu and allow anyone with the link to view, then open the link in a private window to confirm it loads without a sign in. Do not say the page is ready to send until they confirm that test.

## Step 6: Hand over the snippets

Write these three, with the real link and names filled in:

1. Calendar invite description: "Agenda and what to prepare: [link]" plus one line on the outcomes.
2. Email: short and plain. Subject "Agenda for our call on [day, date]". Body: one line with "agenda for our call" as the hyperlinked words, one line saying it lists what we will decide and what we need from them, a request to reply with anything to add, sign off. In Outlook: select the words, Ctrl+K (Cmd+K on Mac), paste the link.
3. Zoom chat: "Welcome, everyone. Agenda for today: [link]. We have [N] minutes and [N] decisions to make."

Optional: a 2 hours before reminder and a same day recap email in the same thread.

## Timing standard

Link to the client at least 24 hours before. If the call is booked at short notice, within 30 minutes of booking or 2 hours before the call, whichever is sooner. Link goes in three places: invite, email, Zoom chat.

## Page by call type

First call: 30 minutes, who we are in two lines, questions we will ask, what we need from them, no pricing. Follow up: 30 to 45 minutes, recap and open items with owners. Proposal review: 45 to 60 minutes, the one decision and who must approve it. Problem or escalation: 30 minutes, what happened in plain words, what we are doing, the decision needed.

## After delivery

Ask for one critique of the page and fold it into this skill or the template.