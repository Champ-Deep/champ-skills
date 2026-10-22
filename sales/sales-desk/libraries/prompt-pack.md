# Prompt Pack

Thirty copy-paste prompts, five for each of the six desks in this pack, each one line, for when you want the step without opening the whole file.

## Give Claude
- The prompt from the desk below with {{braces}} replaced by your own text
- Optional: the matching file attached, if Claude needs the exact output format

## Claude does
1. Pick the desk, copy the line, replace the braces with your facts, paste it.
2. If the output misses the format you wanted, reply "follow the file format" with the file attached.

## Output
Thirty prompts, five per desk, one line each:
### find-buyers
- Turn this ICP into six weighted criteria, then score these companies 0 to 100 and rank them: {{ICP}} {{company list}}
- Map the buying roles for {{company}} from this description and give a LinkedIn search string per role: {{description}}
- Pull shared traits from these three best customers and give me 20 lookalikes, each marked verified or needs lookup: {{three customers}}
- Build a pass or fail verification checklist for this person with the exact searches to run: {{name, title, company}}
- List the disqualifiers for this ICP and mark which pasted companies fail them: {{ICP}} {{company list}}
### pipeline
- Score {{company}} out of 100 on these weights and show every no-data criterion: {{weights}} {{facts}}
- Turn these names, notes and email snippets into a one-page account map with inferred lines labelled: {{paste}}
- Find my warmest path into {{person}} at {{company}} from this connection list and my background: {{list}} {{background}}
- Build my discovery brief for this call: hypothesis, five questions, three objections, win sentence: {{context}}
- Break down this transcript into their words, meanings, commitments, risks and an 80-word CRM summary: {{transcript}}
### playbooks
- Rank these signals by strength and recency, drop anything over 30 days, then give a five-day plan with day-one messages: {{signals}} {{offer}}
- Structure a 30-minute demo for these attendees using only these three pains: {{attendees}} {{pains}} {{capabilities}}
- List the six AI SDR jobs, rank them by risk for my setup, and write the guardrail checklist: {{tools}} {{volume}}
- Rewrite this message to open on the actual signal with its date, under 100 words: {{message}} {{signal}} {{date}}
- Tell me what this demo must not show for this audience, and why: {{attendees}} {{capabilities}}
### libraries
- Give me the five questions from the discovery bank that fit this situation, with what a strong answer reveals: {{situation}}
- Match this objection to the bank and give acknowledge, reframe, question in my wording: {{objection}}
- Restructure this proposal into the standard order and mark every section lacking proof: {{draft}}
- Pick the right negotiation move for this ask and give the exact line plus the move I must not make: {{ask}} {{context}}
- Rewrite this paragraph to remove unsupported claims and list the proof I need to add: {{paragraph}}
### signals
- Score this signal for {{account}}, write the hiring and spend hypothesis, and draft a first touch: {{news}}
- Qualify this competitor-engagement signal and draft a first touch that never attacks the competitor: {{post}} {{who engaged}}
- This contact is new in role on {{date}}: give the angle and message for the 90-day window: {{person}} {{role change}}
- Combine these fit scores and signal dates into a ranked list and surface the top 5 percent: {{rows}}
- Format this signal as a row for my signals tracker: {{signal details}}
### templates
- Write a first-touch email under 100 words from this template using my facts: {{template}} {{facts}}
- Turn these call notes into my call-notes template fields with a next step and date: {{notes}}
- Fill this follow-up sequence for my situation while keeping the day schedule: {{situation}} {{sequence}}
- Give me a LinkedIn connection note under 300 characters using this signal: {{signal}}
- Update my pipeline tracker with this row and tell me which next step and date fields are missing: {{row}}

## Rules
- One line per prompt, one desk per group, five prompts per desk, thirty total.
- Every prompt must run from pasted text with no CRM or tool attached.
- Never add a prompt that needs data the rep cannot paste.
- Braces mark what the rep replaces; no prompt ships with a filled-in example.
- If a prompt needs a file format, it names the file rather than describing it loosely.
- No prompts that generate guessed emails, phone numbers or fake statistics.
