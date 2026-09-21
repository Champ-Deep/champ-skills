---
name: infratech-card-to-pitch
description: "Turns a business card or bare contact details into a researched Champions Infratech meeting request. Researches the company, assigns it to one of 14 audience categories, and produces a one-page contact brief plus ready-to-send outreach (email, LinkedIn note, WhatsApp nudge, call opener) aimed at booking a meeting. MANDATORY TRIGGER for: a pasted name/designation/company/website with any request to reach out, 'set up a meeting with this contact', 'chairman met them at [event]', 'cards from the event', 'who are these people and what do we pitch them', 'research this company and write the outreach', 'categorise this contact', 'Infratech pitch for [company]', 'lagoon pitch', 'Crystal Lagoons outreach', or any batch of event contacts needing qualification and follow-up. Also trigger when someone pastes a LinkedIn URL or company website with no instruction beyond 'pitch them'. Use it even when only a company name is available."
---

# Infratech Card to Pitch

Converts contacts collected at real estate, family office and investment events into researched, categorised, ready-to-send meeting requests for Champions Infratech.

The chairman (Subhakar Rao, Champions Group) collects cards at events. Someone else, usually Champ, has to work out who these people are and get a meeting booked before the memory of the handshake fades. Speed and accuracy both matter: a wrong-category pitch to a family office wastes the only warm introduction that contact will ever give.

## The company you are pitching

Champions Infratech builds man-made beach communities across India, designing and delivering Crystal Lagoons water technology as the anchor amenity for residential, township and hospitality projects. It positions itself as a licence holder of that technology. Investors can enter at project level alongside builders or at infrastructure level, and partners can participate through referrals into their own landlord, builder and investment-firm relationships.

Read `references/positioning.md` before writing any pitch. It carries the claim boundaries: what may be said, what must be verified first, and what must never be improvised.

## Workflow

### 1. Intake

Collect, from whatever the user pasted or attached: contact name, designation, company, website, email, phone, LinkedIn, the event where the card was collected, and the date of that event.

Proceed with whatever exists. A company name alone is enough to start. Ask only for what genuinely blocks the work, and ask it once, in a single line. Never stall a batch of twenty cards to chase one missing phone number.

If several cards arrive at once, run the whole batch and deliver a ranked table first (see Batch mode below).

### 2. Research

Search the web and read the company's own site. Aim for six facts, not sixty. What you need:

- What the company actually does, in one sentence, in its own words
- Scale signals: headcount, geography, portfolio size, recent projects, funds under management
- Whether they touch land, capital, delivery, design, demand or media
- A recent, verifiable hook: a launch, a fund close, an award, an expansion, a published view
- Their India footprint and the cities they operate in
- Anything that disqualifies them or flags risk

If the site is thin or the company is not findable, say so plainly in the brief and route the contact to the Others category with a qualification call as the ask. A fabricated hook is worse than a generic one.

Never invent numbers, project names, deal values or quotes. If a figure is not sourced, leave it out. See the claim rules in `references/positioning.md`.

### 3. Categorise

Assign exactly one primary category from the 14 in `references/pitch-matrix.md`. Assign a secondary only when the company plainly operates in two (a developer with an in-house fund, an architecture practice that also does interiors) and note which one the pitch leads with.

Category is decided by what the contact can give Champions Infratech, not by the company's self-description. A construction firm that owns large land parcels is a Builder / Developer for pitch purposes. Route by the person's designation when the company spans several: a CFO at a developer is closer to Finance Consultant thinking than the sales director in the next office.

When two categories fit equally, choose the one with the higher priority code, and say in the brief that you did.

### 4. Write the contact brief

One page, scannable in thirty seconds. Use this exact structure:

```
# [Contact name], [Designation], [Company]
Category: [primary] ([priority code]) | Secondary: [or "none"]
Met at: [event, date] | Confidence: [High / Medium / Low, and why in six words]

## Who they are
Two or three sentences. What the company does, its scale, its India footprint.

## What they actually want
Their commercial motive in their world, not ours. Two sentences.

## Where we fit
The specific reason this contact is worth a meeting. Name the parcel, the fund,
the practice, the mandate. If the fit is weak, say so and recommend dropping it.

## The pitch angle
Three lines the sender can say out loud, adapted from the category pitch to this
company's specifics.

## Why it works on them
For the sender's understanding only. Never read aloud, never in the email.

## The ask
One next step. One only.

## Watch-outs
Competing interests, unverified claims to avoid, anything awkward.

## Sources
Two to four links used. Mark anything unverified.
```

### 5. Write the outreach

Produce four assets, in this order. All of them are for the sender, not the chairman, unless the user says the chairman is sending.

**Email.** Subject line plus two alternates. Body of 90 to 130 words. It opens by anchoring the event and the chairman's conversation, states the one relevant thing about Champions Infratech in a single sentence, makes the category-specific offer, and closes with the ask and the scheduler link. No apologies, no jargon, no report formatting inside the body, no bullet lists unless the category genuinely needs three parallel items. Depth goes in an attachment, not the email.

**LinkedIn connection note.** Under 300 characters, references the event, no pitch beyond one clause.

**WhatsApp nudge.** Two lines, sent five to seven days after the email if there is no reply.

**Call opener.** Three sentences for when they pick up, plus the two questions to ask before pitching anything.

Templates and worked examples: `references/outreach-templates.md`.

### 6. Deliver

Default output is in-chat: the brief, then the four assets. Offer a file only when the user asks for one or when the batch runs past five contacts, in which case produce an HTML table plus one brief per contact.

## Batch mode

For multiple cards, lead with a ranked table before any individual brief:

| # | Contact | Company | Category | Priority | Fit read | Ask | Send when |

Sort by priority code, then by fit read. Then write full briefs for everything at priority 1 and 2, and short three-line briefs for the rest. This puts the chairman's best cards at the top of the page where they get acted on.

## Rules that hold everywhere

- No em dashes or en dashes anywhere, in any output or file. Use commas, periods, parentheses, colons, or restructure. Check before delivering.
- No invented figures. No price uplift percentages, lagoon costs, IRRs or sales velocity numbers unless the user supplies them and confirms they are approved.
- The Crystal Lagoons licence is stated as held. Do not describe its territory, exclusivity or duration in writing to an external contact until the user confirms those terms.
- One ask per message. A second ask halves the reply rate.
- The first two lines of every deliverable carry the whole message. Assume the reader stops there.
- Flag rather than guess. A line reading "not verifiable from public sources" is a useful output.

## Reference files

- `references/pitch-matrix.md` , the 14 categories: who they are, what they want, the pitch, why it works, the ask, priority. Read this every run.
- `references/positioning.md` , the Champions Infratech story, claim boundaries and the questions to resolve internally before certain categories go out.
- `references/outreach-templates.md` , email, LinkedIn, WhatsApp and call-opener patterns, with two worked examples.
