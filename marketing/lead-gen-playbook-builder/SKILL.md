---
name: "lead-gen-playbook-builder"
description: "Turns a one-line campaign idea into a complete, rep-ready lead-gen playbook: intake, personas, multi-channel cadence, exact pitches per channel, reply-handling flowcharts, tracking and guardrails, plus CLF prospecting email rules, domain readiness and a rep training block. Trigger for build a lead gen playbook, campaign playbook, flesh out this campaign, outreach playbook, cadence for a campaign, channel-based messaging, decision flowchart for outreach, give my lead gen team a playbook, pitches for each channel, what do we send and when, sequence for a target, or any request to turn a rough campaign concept into an executable outreach plan. Works for B2B and B2C, event-based and always-on campaigns."
---

# Lead-Gen Playbook Builder

You take a rough campaign idea and turn it into a single document a lead-gen rep can open on Monday and run without asking a single follow-up question. The rep should never have to guess what to send, to whom, on which channel, in what order, or what to do when someone replies. That is the bar.

The reason this matters: most "campaigns" die because the idea was never decomposed into rep-level instructions. A founder says "let's do a World Cup campaign" or "let's chase Bangalore CXOs," a rep nods, and then nothing ships because nobody decided the persona, the opener, the day-2 touch, or the reply handling. Your job is to remove every one of those decisions from the rep's plate in advance.

## The build sequence

Work through these phases in order. Do not skip the intake even when the idea seems obvious. The intake is where you catch the assumptions that would otherwise sink the campaign.

### Phase 1: Intake (flesh out the idea)

Read `references/intake-questions.md`. Extract every answer you can from the conversation, the vault, connected data, or research, and only ask the user the gaps that genuinely block the build. Aim to ask once, in a single batched question, not in a drip.

The intake exists to lock four things: WHO you are chasing (personas), WHAT you are offering (the value and proof), WHY NOW (the trigger that earns a reply), and the CONSTRAINTS (timeline, channels available, compliance, pricing discipline, who has to approve what).

If a real contact dataset exists, profile it before inventing personas. Personas grounded in the actual title and industry distribution of the list beat invented ones every time, and they tell the rep exactly which rows to pull.

### Phase 2: Personas

Cluster the target audience into 3 to 6 clear personas. Each persona needs a data signature (real titles, industries, company profile), example named accounts if a dataset exists, what keeps them up at night, why this campaign chases them, and their priority. Personas are the spine of everything downstream: pitches, cadence weighting, and the target list pull all hang off them.

### Phase 3: Channel cadence (the waterfall)

Read `references/channel-playbooks.md`. Design a per-prospect channel waterfall, not a single-channel blast. The waterfall escalates commitment across touches: wide and low-friction first (email, social), narrowing to high-commitment (phone, sample, meeting), with the hard sell arriving last. Specify the day, channel, pitch round, and intent of every touch, tiered by persona priority.

The core discipline: lead with the prospect's problem, not your asset. The asset pitch is a closing move, not an opening one. A first touch that could be sent to a competitor's prospect and still make sense is a closing line in the wrong place.

### Phase 4: Exact pitches per channel

For every persona x channel x pitch-round combination the cadence calls for, write the actual copy, not a description of the copy. Use merge fields ({{first_name}}, {{vertical}}, {{company}}) so the rep personalizes line one and sends the rest. Channel-match the message: email carries the frame, LinkedIn connects without pitching, the DM carries the sample hook, phone carries urgency, the closing email carries the offer. Pull the per-channel voice and structure from `references/channel-playbooks.md`.

### Phase 5: Decision-based flowcharts

Read `references/decision-flowcharts.md`. For each channel, render a Mermaid flowchart that maps every realistic reply signal to the next action, the SLA, and the exact response pitch. This is the part reps most often lack and most need. "They said what's pricing" should resolve to a specific action, a time bound, and a script, not improvisation. Render flowcharts in Mermaid so they display in Obsidian and most markdown viewers.

### Phase 6: Operating system

Wrap the campaign in the machinery that makes it run: daily quotas per rep per channel, a real-time tracking schema (status stages, owner, last touch), reply-handling SLAs, pricing discipline, and the hard don'ts. Include explicit gates with dates where attendance or conversion can cascade.

Every playbook's operating system also includes:
- A **domain readiness checklist** with an owner and a date, completed before the first send: one-page website live on each prospecting domain (overview, services, contact, about, privacy policy), SPF, DKIM and DMARC set, sender identity aligned.
- A **rep training block** that teaches the eight prospecting email rules in plain language, with one good and one bad example email, so the team can adopt them without a meeting.
- A **gradual switch-over plan**: which live sequences finish on the old process and which start on the new rules, so nothing is stopped mid-cadence.

### Phase 7: Assemble

Assemble everything into the output structure in `references/output-template.md`. The finished playbook is one self-contained document. A rep with zero context should be able to execute from it alone.

## Guardrails to carry into every playbook

These recur across campaigns and you should bake the relevant ones into every build:

- **Anchor discipline.** If the campaign uses social proof (named attendees, named customers), only cite genuinely confirmed names. Unverified anchors that back out trigger a cascade where everyone who joined because of them also leaves. This is the single most common reason high-RSVP events collapse on the day.
- **Lead-with-problem.** Rounds 1 and 2 never lead with the asset, the SKU, or the price. Trust is upstream of the pitch.
- **Pricing discipline.** Define exactly when a rep may quote, what they may quote (indicative ranges vs firm numbers), and what needs sign-off. Reps quoting firm numbers without authority is a recurring own-goal.
- **Channel-fit and deliverability.** Respect per-inbox send caps, verified-only addresses, no info@/hello@, never re-mail bounces, rotate subject lines. A campaign that burns the domain is worse than no campaign. Every email pitch in the playbook follows the prospecting email rules below.
- **Parent-brand firewall.** Data and lead-gen campaigns never use Champions Group (name, domain, logo, signature). Sign as the selling brand and send from a dedicated prospecting domain.
- **Compliance per audience.** B2C consumer data needs opt-in and consent screening (CAN-SPAM, TCPA for SMS, state privacy). Regulated verticals (betting, finance, health) need jurisdiction screening. Never target minors; target the buying adult.
- **Real-time tracking.** "I think we have about ten" is how campaigns die undetected. The tracker is updated within the hour and is the single source of truth, reviewed at named gates.

## Prospecting email rules (CLF lead-gen standard, adopted Oct 2026)

These come from the lead-gen team that switched to them over three months and now books 15+ leads a month consistently. Sending domains with a live website outperform domains without one. Apply every rule to any prospecting or follow-up email this skill writes.

**Brand rule.** Never use Champions Group (name, domain, logo or signature) for data or lead-gen prospecting. Spam complaints and blocklists attach to whatever brand and domain the email carries, and Champions Group is the parent brand for Champion Lagoons, Royal Champion Yachts and the longevity businesses. Sign as the selling brand (LakeB2B, SPAN, Ampliz, Contact Consumers, MetricFox) and send from a dedicated prospecting domain, never from a primary brand domain.

**Before anything is sent (domain readiness).** Every prospecting domain needs:
- A basic one-page website that a prospect lands on when they search the domain: company overview, services or solutions, contact information, about or company information, and a privacy policy.
- SPF, DKIM and a valid DMARC record, plus a one-click unsubscribe for any bulk send.
- A matching identity: the sender address, website, company name and signature all name the same company. If any of these disagree, stop and fix it before writing copy.

**The eight email rules.**
1. Professional signature: sender name, title, company name, phone number, website.
2. One link only: the website in the signature. No links in the body, no tracking links, no calendar link until the prospect has replied.
3. First-touch email: 125 words maximum, ideally 100 to 125. Follow-ups are shorter.
4. Plain text only: no HTML templates, banners, images, colored fonts or heavy formatting.
5. Subject line: 2 to 4 words, natural, relevant to the message. No clickbait, no all caps, no punctuation tricks.
6. No spam or promotional language. Banned in subject and body: free, guaranteed, best price, act now, limited offer, risk-free, special promotion, urgent, 100%, no obligation, click here, exclusive deal.
7. Sender identity aligned: sending address, website, company name and signature are consistent and credible (see domain readiness).
8. Every prospecting domain has its website live before its first send (see domain readiness).

**Signature template (plain text):**
```
[Full Name]
[Title], [Selling Brand Name]
[Phone with country code]
[prospecting-domain website]
```

Roll this out gradually. Move each campaign onto these rules as its next sequence starts; do not stop live sequences mid-cadence.

## Output

Save the playbook as a single markdown file. If the user works in Obsidian, use [[wikilinks]] for internal references and Mermaid for flowcharts. Name it descriptively (e.g., `<Campaign>-LeadGen-Playbook.md`). If the user wants it to hand to a team, the document should open with a TL;DR and a "read this first" section, then flow from personas through cadence, pitches, flowcharts, to the operating system.

## Reference files

- `references/intake-questions.md`, the question battery that turns a one-line idea into a fully specified campaign. Read in Phase 1.
- `references/channel-playbooks.md`, per-channel voice, structure, cadence patterns, and pitch templates for email, LinkedIn, WhatsApp, phone, social DM, and newsletter. Read in Phases 3 and 4.
- `references/decision-flowcharts.md`, Mermaid patterns for reply-handling decision flows per channel. Read in Phase 5.
- `references/output-template.md`, the exact section structure of the finished playbook. Read in Phase 7.
- `examples/`, two complete worked playbooks (a B2B CXO-event campaign and a B2C consumer-moment campaign) showing the finished bar. Read when you want a model of the output.