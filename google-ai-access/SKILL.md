---
name: google-ai-access
description: "Use when picking Deep's lane for Google AI access."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [google, gemini, workspace, providers, billing]
    related_skills: [hermes-agent, model-api-capability-verification, knowledge-tier-boundaries]
---

# Google AI access lanes

## When to Use

- Deep asks whether he can use Gemini, Argon, or "his Google subscription"
  from Hermes, a CLI, or a script.
- Choosing between a Gemini API key, Vertex, or an AI plan for a task.
- Any question about what his Google plan does or does not pay for.
- Wiring Ask Gemini in Chat or a Drive folder into an agent workflow.

Google sells the same models through four lanes with four different billings.
Every "can I use Gemini/Argon here" question is answered by naming the lane
first; mixing lanes is how advice becomes wrong.

| Lane | What pays | What it covers | Wired into |
|---|---|---|---|
| Google AI plan (Plus/Pro/Ultra) | monthly subscription | Quota inside Google's own surfaces: AI Studio web UI, Gemini app, NotebookLM, Antigravity, Jules | human use, Antigravity (`agy`) |
| Gemini API key | Google Cloud billing, pay per token with a spend cap; free tier exists but is rate-limited | Programmatic Gemini API | Hermes `gemini` provider: `GOOGLE_API_KEY` or `GEMINI_API_KEY` in `~/.hermes/.env`, then `hermes model` |
| Vertex AI | Google Cloud billing | Same models under enterprise controls | Hermes `vertex` provider via Application Default Credentials |
| Workspace agent (Ask Gemini in Chat) | eligible Google Workspace subscription | Gemini inside Chat/Gmail/Drive/Docs, reading that account's Workspace data | Google Chat, admin-enabled |

## Always-on rules

- **Subscription coverage stops at Google's own UI surfaces.** Google's docs
  state plan benefits apply "only within the Google AI Studio web interface"
  and that direct API use "is billed and managed separately". Never promise
  that an API key, a CLI, or a script will draw on the Google AI plan.
- **Check entitlement on the live account, not the plan table.** Published tier
  tables lag account-level rollouts; Deep has run models that his plan's table
  lists as higher-tier only. Follow the method in
  `model-api-capability-verification`: his account screen outranks the docs.
- **An agent lane needs paid billing or acceptance of throttling.** The Gemini
  API free tier cannot carry long agent runs because Hermes makes several model
  calls per turn. Any API-key setup gets billing enabled with a spend cap.
- **Antigravity is the subscription-covered Google CLI surface.** Google
  redirects personal Gemini CLI logins to the Antigravity suite, so do not
  build automation on the personal Gemini CLI login path.
- **Account topology decides visibility.** The consumer Google account holds
  the AI plan, personal Drive, AI Studio, and Antigravity. The Workspace
  account (Deep admins `championsmail.com`) is what Ask Gemini in Chat and
  Workspace agent features search. A folder or file must live on the account
  the agent reads; see `knowledge-tier-boundaries` before syncing anything up.

## Pitfalls

- Do not treat "Deep uses Gemini in the app daily" as API capacity: different
  lane, different billing, separate quota.
- Do not recommend a consumer-account folder to a Workspace agent. Ask Gemini
  in Chat reads Workspace Drive data, not the personal Gmail drive.
- Do not count Google One AI credits toward AI Studio or API usage; they are a
  separate credit system Google documents as not supported in AI Studio.
- Do not pick models from a docs price table alone. Availability per lane and
  per account moves; read the live model picker in AI Studio or the provider
  registry in Hermes.

## References

- `references/ask-gemini-in-chat.md` — setup gates, entry points, what Ask
  Gemini in Chat can and cannot reach.
