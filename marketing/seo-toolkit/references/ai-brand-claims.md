# AI brand claims (ChatGPT Business Hub and equivalents)

Use when a brand must own how it appears inside an AI answer surface: claiming a business profile in ChatGPT's Business Hub, filling its facts, and wiring the platform's own mention and click metrics back into the revenue thread. Trigger phrases: "claim our business in ChatGPT", "Business Hub", "AI assistants showing our brand", "how does ChatGPT describe us".

This file is the evidence procedure. The document shape for a prospect audit is `site-growth-audit`; a multi-brand run is reported as a runbook plus a shared tracker.

## 1. Verify the platform claim before it reaches a team

A third-party video or thread is the input, never the source.

1. Get the platform's own text: launch announcement, help-centre article, policy page. `web_search` the exact claim sentence plus the vendor name, then read the announcement and the policy.
2. `web_extract` the official pages first. Vendor domains (notably openai.com) return 403 to plain fetches, so fall back to the `blocked-page-recovery` ladder rather than accepting a search snippet as the policy text.
3. Build two columns: what the platform actually says, and what the source claims. Split it into confirmed, overstated, unknown.
4. Mark the decisive unknown explicitly (for ChatGPT: is our industry category eligible at all). That unknown becomes the pilot's purpose and the thing the room is asked to decide.
5. Only numbers the platform itself publishes get quoted. No rate, no share of voice, no ranking position from a marketing video.

## 2. Build the claim matrix before touching any account

One row per brand in the group, in an .xlsx (build with the `xlsx` skill, read-back verification applies):

| Column | Rule |
|---|---|
| Website | **Curl it first, never take it from a wiki note.** Loop every candidate domain with `curl -sL -o /tmp/h.html -w '%{http_code} %{url_effective}'` plus a `<title>` grep. Vault domain lists carry dead domains, wrong spellings and redirects, and a parked or wrong host still answers with a plausible title, so one wrong line means an identity check against a domain the brand does not control. |
| Verify route | Prefer business email (a live mailbox on the brand's own domain needs no IT ticket), then phone, then a DNS TXT record, the only route that costs another team a ticket. |
| Owner | `[CONFIRM: owner]` when the vault does not say. Never assign an owner by guessing the most plausible name. |
| Status | Data-validation dropdown using the platform's own gate names, so a later sweep can count states mechanically. |

Sheets: `Claim tracker` (the matrix), `The N steps` (vendor procedure, who may do each step, what it costs), `Profile copy drafts` (one factual line per brand for the owner to approve, plus a rules row: no counts, rankings or accuracy claims unless sourced and signed off by the owner).

**Multi-brand groups need cross-reference guardrails in writing.** Sibling brands competing for the same buyers get separate profiles with no cross-link, and copy never names an outside delivery partner: a profile is a public statement of who is behind the brand.

## 3. Present it as a decision, not a status update

When the run belongs in Deep's recurring meeting, it rides the house decision-queue format (the vault's Marketing Meeting Operating System): one DECISION NEEDED block with context, affected, recommendation, deadline. Then a minute rail that sums to the segment length, an owner and a date per ask, and a guardrail list. Everything Deep alone can decide (which person hands a government ID to a third party, which account claims) is lifted out as options plus one recommendation and lands on a blocked `needs_input` kanban card carrying the same options, so the answer arrives where the work continues.

Stage, never claim, in the meeting: verification codes go to real mailboxes and phones, so the room only reads. Name the inviter if the invite does not exist yet, rather than assuming a calendar slot.

## 4. Guardrails for the run

- Claiming is not distribution. The platform may show the business without a claim, and a claim guarantees no recommendation lift. Write that in the runbook so nobody reports the claim as a ranking win.
- Platform policy demands truthful, current facts and bans fabricated reviews and unsupported guarantees. Copy obeys it literally: describe services, not slogans.
- Identity checks needing a government ID or business registration are a person decision, not a workflow step. Route them to Deep or the entity's signatory.
- Category rules can exempt whole segments (local venues limited to one country's listings). Check eligibility before spending an owner's time, and write "probably ineligible" in the matrix rather than silently dropping a brand.
- Metrics join the revenue thread: mentions and clicks become a ChampUTM and Lead Source line, and the baseline starts the day claims go in.

## 5. Outputs

| Artifact | Location |
|---|---|
| Runbook (verdict, agenda slot, minute rail, asks and owners, guardrails, not-verified list) | the effort folder under `Efforts/Active/` |
| Tracker with sheets | same folder, `MEDIA:` delivered, shared on screen in the meeting |
| Task line | `## Active` in `TASKS.md` pointing at both |
| Decisions only Deep can make | blocked kanban card, options first, recommendation first |

Report the not-verified list plainly: eligibility, owners, domains, and any meeting invite that does not exist. A clean matrix with guessed rows is worse than one carrying visible `[CONFIRM]` tags.
