# Can a user's AI subscription pay for a third-party app?

Deep asks this whenever a product (Harbinger, the toolkit agent) needs model
inference and someone suggests "let them sign in with ChatGPT / Claude instead of
billing them". Answer it from the vendor's own legal or developer docs, never
from training data, and separate the three claims below before saying anything.

## Three claims that are gated separately

1. **Identity sign-in.** "Continue with ChatGPT" can be live for everyone while
   plan usage is not. The two are separate permissions a user approves one at a
   time, so a working sign-in button proves nothing about billing.
2. **Plan usage by the app.** Only this makes the user's subscription pay for the
   app's model calls.
3. **Which models and which path.** Even when allowed, the share usually works
   through one vendor's own inference endpoint with the user's bearer token, not
   through a general API key.

## Verified positions (re-check the source pages; vendors change these)

| | Identity sign-in | Plan usage by the app | Who may integrate |
|---|---|---|---|
| OpenAI (`developers.openai.com/siwc`, `help.openai.com` Sign in with ChatGPT) | Yes, broadly | Yes, for Go, Plus and Pro users, with a weekly cap the user controls; OpenAI models only, called on the Responses API with the user's access token | Hosted commercial apps: a limited partner rollout reached through OpenAI's interest form, so approval is the gating item. Self-serve docs cover open-source clients that run on the user's own machine (browser opens OAuth, loopback callback, PKCE, client registered at first launch) |
| Anthropic (`code.claude.com/docs/en/legal-and-compliance`) | Not offered to third parties | Not permitted: plan credentials may not be routed through, and Claude.ai credentials or session tokens may not be collected, stored or intermediate | The user's own API key from Anthropic's console, or the user working inside Claude with a connector |

## Procedure

1. Read the vendor's legal / developer docs page for the auth scheme, not the
   marketing help-center article.
2. Split the answer into the three claims above and answer each with its own
   source URL.
3. Check hosted versus local: self-serve integration usually covers only clients
   running on the user's computer, so a hosted app needs the partner track.
4. Check what background jobs run on. A plan share covers requests carrying the
   user's token; a cron queue has no user session, so it still needs a server key
   unless the share is explicitly wired into that path.
5. Name approval as the gating item, and say plainly that pricing or roadmaps
   must not assume access that is still unapproved.
6. State the route that needs no vendor permission: expose the product as a
   connector inside the vendor's own app (MCP is the usual standard), so the
   model runs in the vendor's product on the user's plan. Private use needs no
   directory review; a public listing is a separate review.

## Pitfalls

- "Sign in with X" existing is not evidence that X lets apps bill the plan.
- One vendor permitting it is not evidence for another; the two dominant vendors
  currently differ, and quoting a capability across vendors is how the wrong
  claim gets made.
- A plan share usually pins you to that vendor's models, so a product already
  built on a multi-vendor router needs a second inference path before the share
  is worth anything.
