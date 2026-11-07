---
name: whatsapp-channel-ops
description: "Use when wiring WhatsApp into Deep's agent workflows."
version: 1.0.0
author: Deep / Hermes
license: internal
metadata:
  hermes:
    tags: [whatsapp, messaging, channel, kanban, privacy]
    related_skills: [hermes-gateway-ops, telegram-brief]
---

# WhatsApp channel ops

## When to Use

- Deep asks to connect, link, or set up WhatsApp so the agent can read his groups or post to them.
- He asks how a WhatsApp channel would sync with the Champ board, or how to keep his personal chats out of it.
- A run needs to read a WhatsApp group's action items and turn them into cards or a follow-up summary.
- Deciding between a dedicated Champ number and linking his primary number for group access.

Do not use this for cold or bulk WhatsApp outreach campaigns (that is the provider decision in the vault note cited in step 6) or for gateway/platform failures (that is `hermes-gateway-ops`).

Deep wants his WhatsApp group traffic available to the agent: action items and questions from his work groups read, triaged and routed to the Champ board (the kanban), while his personal 1:1 chats stay out of scope. Isolation is a standing requirement, not a trade to make for setup speed, and nothing in this class ships until Deep picks the connection path.

## Always-on rules

- **Default scope is group-only on a primary account.** When Deep explicitly chooses a dedicated Champ account and asks for all its messages, that authorization includes its DMs and every joined group. Use a distinct store for that account; never expand the scope of an existing primary-account store. Account-wide sync is not the same as granting all senders agent/tool authority.
- **Group access is claimed only from a state read, never from a list command's exit code or an empty result.** See step 1 for why the two look alike.
- **Outbound is stage-only.** Draft the message and show it; Deep sends or approves the send lane, exactly as with email.
- **No number purchase, group creation, payment or contract originates from a WhatsApp conversation.** Promises made in chat (an NDA coming, a payment landing Monday) route to a needs_input decision card first.

## Procedure

1. **Read link state before anything else: `wacli doctor`** (CLI at `/Users/deep/.local/bin/wacli`, store `~/.wacli`). The verdict lives in the AUTHENTICATED / CONNECTED / SESSION_REVOKED / GROUPS / MESSAGES fields. The command exits 0 even when AUTHENTICATED is false, and `wacli groups list` / `wacli chats list` then print only their header rows: that reads like "no groups" but means "not linked". An unlinked store reports MESSAGES 0, so the honest report is "not linked, nothing to read", never "no groups found".
2. **Let Deep pick the connection path (decision card, recommendation first):**

   | Path | Isolation | Cost |
   |---|---|---|
   | A: a dedicated Champ number added only to the work groups | Real: his personal chats never touch the machine | Needs a number plus Deep adding it to each group |
   | B: link Deep's primary number (QR scan on his phone; `wacli --help` for the exact subcommand) with a group-JID allowlist | Software only: queries filter to groups, but the account-level store still writes to `~/.wacli` | Fast, one scan |

   Recommend A whenever personal isolation is the point; B only when Deep accepts the store on disk. The QR step happens on his phone and cannot be completed agent-side.
3. **On a primary account or a subset request, allowlist by exact group JID (`...@g.us`), never a name keyword.** On an explicitly authorized all-message dedicated account, do not add a group or mention filter that would silently discard traffic. Prefer passive `wacli sync` without agent auto-replies for ingestion. An open Hermes gateway can turn all inbound senders into tool callers and automatically respond; do not equate that with passive access. Verify one real DM and one unmentioned group message before claiming all-message receipt. Full-history pairing requests older history but cannot guarantee WhatsApp will provide all of it.
4. **Board sync (proposed design, not yet built): each allowlisted group maps to one Champ board lane or tag.** Incoming group messages become or update cards in that lane; outbound replies stay staged as drafts on the card. State plainly in the handoff that this mapping is designed, not live, until one real message has produced one real card.
5. **Extract and card action items at read time; do not plan to re-query a group later.** The store is empty whenever the link is down (an unlinked store reports MESSAGES 0), so anything worth keeping is persisted as a card or note when read.
6. **Volume and cold outreach never ride a linked personal session.** At-scale or first-touch WhatsApp goes through an official WhatsApp Business API path (Twilio number plus a Meta-approved BSP); linked-session gateways belong to warm reply and nurture traffic only, because Meta bans numbers used for cold bulk regardless of gateway quality. Provider detail and Deep's prior calls live in the vault: `Efforts/Active/AI SDR Infrastructure/Voice + WhatsApp Channel Providers - Twilio, ElevenLabs, OpenWA.md`.

## Pitfalls

- Deep names groups by title and titles repeat across clients. Resolve title to JID by listing groups and matching, and show the resolved JID in the handoff so a wrong pick is visible before anything is read from it.
- Filtering queries by JID is not isolation. A linked primary number still writes account-level metadata to `~/.wacli`; when Deep says his personal chats must stay out, the only hard answer is a separate number (path A). Say which guarantee each path actually gives instead of letting "I only query groups" stand in for it.