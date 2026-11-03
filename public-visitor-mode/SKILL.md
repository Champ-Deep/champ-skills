---
name: public-visitor-mode
description: "Use when an authenticated app opens to anonymous visitors."
version: 1.0.0
license: MIT
author: Hermes Agent
metadata:
  hermes:
    tags: [public-access, quotas, auth, rate-limiting, ip-trust]
    related_skills: [risky-changes, verification-gate-integrity, cloudflare-workers-r2-apps]
---

# Public visitor mode

The app already assumes a session on every route. This opens a bounded slice of it
to people with no account without opening the rest.

## When to Use

"free chatbot with no login", "visitors can try it", "put the demo on the brand
site", "demo without signup", or any authenticated app being published on a public
domain. Quota and spend-cap design lives here too. Not for an API whose callers are
agents (`agent-first-products`), not for an outbound send path
(`permissioned-send-lane`).

## Steps, in order

1. **Put the caps in a decision card before writing code.** Caps are money, and the
   spend key choice (one shared weekly key vs a purpose-made capped key) is a billing
   decision. A purpose-made key with a small credit limit is the default
   recommendation: a public surface that leaks or gets abused must not be able to
   drain the shared key. See `risky-changes` step 4.
2. **Build the mode behind one flag, default off**, so every existing authenticated
   deploy stays unchanged. Tests toggle the flag explicitly instead of inheriting it
   from the environment.
3. **Install three caps, in this order of importance:**
   - **A shared daily USD cap across all visitors.** This is the only real bound.
     A per-question count sets no ceiling on spend, because cost per question moves
     with model, context length and how many tool calls the answer loop triggers.
   - **A per-identity daily question count**, for fairness: one visitor must not
     monopolise the shared budget.
   - **A model lock.** Visitors get the default model only. Letting the caller pick
     the model makes cost per unit unbounded and silently defeats the shared cap.
4. **Default deny, open by exception.** Carry an allowlist of the routes a visitor
   may touch (read a narrow aggregate, chat) and let everything else 401: upload,
   admin catalog, account, settings, profile. Listing what is *closed* instead means
   every admin route added later is public by default.
5. **Give visitors an identity you can count against**, and write usage under a key
   that survives a redeploy (a database row keyed by day and identity, not process
   memory). Otherwise every restart reopens the budget and the cap is per-boot, not
   per-day.
6. **Decide which client IP you trust, explicitly.** See the section below; this is
   the one step that silently decides whether the per-identity cap means anything.
7. **Expose a read-only aggregate for the public surface**, not the admin listing
   endpoint. The public view answers questions; it does not enumerate the dataset
   inventory, filenames or upload state.
8. **Prove both directions, then prove the cap fires.** See Verification.

## Which client IP you trust

Behind a reverse proxy the default forwarding header is client-settable, so a
per-IP cap or login lockout is attacker-controlled: the caller sends their own
header and picks the identity they are counted under.

- Trust a **proxy-specific** header (`cf-connecting-ip` behind Cloudflare) only when
  the proxy is the sole network path to the service, for example a router Worker
  fronting a container whose own route is never published. The header is trustworthy
  exactly because no client can reach the app to set it.
- If the service can also be reached directly (another port, an origin URL, a
  platform's own domain), **ignore forwarding headers entirely** rather than trusting
  one: with two paths in, the attacker chooses which path they arrive on.
- Where a platform's container entrypoint defaults to trusting all forwarded IPs,
  that default is the vulnerability. Narrow it, or pin a trusted header as above,
  and say in the report which of the two you did.

## Verification

A smoke script for this mode must assert from a client holding **no credentials**,
and assert both directions:

- **one allow and one deny per surface class.** Allows alone pass while the app is
  wide open; denies alone pass while visitors get nothing. Assert a visitor reads
  the aggregate and chats, and that the same visitor is refused on upload, admin
  catalog, account and settings.
- **drive a visitor to the cap and assert the refusal.** A quota that has never
  fired in a test is a quota nobody has seen work, and it is the cap standing
  between a public URL and an invoice.
- **never conclude from an authenticated session.** An admin cookie takes the admin
  path, so the visitor path stays entirely untested no matter how green the run.
- **run the script locally in the target mode before it gates a deployment**, per
  `verification-gate-integrity`, so its first run diagnoses the deployment rather
  than itself.

Report the fixture boundary plainly: a run against a local instance under the target
flag proves the contract, not the platform. The live URL still owes its own run of
the identical script.

## Pitfalls

- **A visitor can mint a fresh session, so the count cap is fairness, not a
  security boundary.** Only the shared spend cap cannot be dodged by starting over;
  never describe the count cap as the thing that protects the budget.
- **A default account created at deploy time is not a visitor.** Seeding an admin
  into a fresh database is correct, but the password lives in a keychain entry or a
  gitignored env file, never in a chat, a card, or the deploy log. Say in the report
  which entry holds it, and that the credential should be rotated after a showcase.
- **A smoke step gated on a provisioner's exit code is not gated.** Provisioner
  scripts often exit non-zero on their own success path, so retry loops and
  `|| true` wrappers both read as success. Gate on the effect: call what the step
  provisioned and assert it answers.
- **Quota accounting that only exists in process memory looks correct in every
  test** (tests run one process) and resets on every deploy in production.
- **Do not report the mode as live from the code alone.** The contract, the caps and
  the local smoke run are one claim; the deployed URL answering is a second, earned
  only by the same script pointed at the real host.

Pairs with `risky-changes` (caps go to Deep as a decision card with numbers) and
`verification-gate-integrity` (never report a gate you did not execute).