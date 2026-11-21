---
name: auth-and-spend-caps
description: Use when an internal tool needs team sign-in and caps.
version: 1.0.0
author: Champ
license: MIT
metadata:
  hermes:
    tags: [auth, billing, caps, internal-tools]
---

# Sign-in, roles and spend caps for an internal tool

Deep's pattern for handing an internal tool to his teams: nobody self-registers,
he creates the account, each account carries its own spending allowance, and he
adjusts all of it from an admin screen. Auth, billing and data judgment stay in
the main lane; the UI goes to the frontend lane (`model-routing`, "Backend
contract first" for that handoff).

## When to Use

- Deep wants a tool handed to his teams with per-account capping and an admin
  screen he adjusts himself.
- An internal tool currently runs on one shared API key and needs real accounts,
  roles or spend limits instead.
- A review of an internal tool turns up self-service sign-up, an unbounded caller,
  or caps enforced only in the UI.
- A frontend lane is about to be handed a tool UI with sign-in, limits or usage
  screens: the endpoint contract must exist first.

Not for consumer apps built on Clerk (`clerk-auth`) and not for outbound send
paths (`permissioned-send-lane`).

## 1. Fix the access model before writing code

Decide and write down, in this order:

1. **Who may hold an account.** Public sign-up is off; accounts are created by
   the super admin. Domain allowlisting on his own company domains is the default
   gate, and the list is editable in the admin UI rather than hard-coded.
2. **Roles.** At minimum `user` and `admin`, plus exactly one super admin who
   cannot be demoted, banned or deleted by any endpoint. Enforce that in the
   mutation itself, never only in the UI.
3. **Money.** Three numbers: a per-person monthly cap, a per-run cap, and a
   company ceiling for the month. Each has a default, each allows a per-person
   override, and "use the default" is its own state.
4. **Tiers.** Optional capabilities (premium lookup, live reachability) are
   per-account switches, off by default, implicitly on for admins.
5. **Ownership.** Anything a person uploads or creates belongs to them; another
   account gets a 404 on that id, never a 403 that confirms it exists.

## 2. Auth plumbing

- Library: Better Auth is Deep's default for new sign-in work, not Clerk. Clerk stays only in apps that have not been migrated yet, and each of those moves on its own card. Read the current Better Auth setup through Context7 before writing code.
- Moving an app off another auth provider is a data migration, not an import swap: wallets, runs, files and API keys are keyed by the old provider's user id. Keep those ids, add a mapping from the new user to the old id matched on a verified email only, stage it behind a flag, rehearse the rollback, and make the cutover its own decision. A card that says "remove the old imports and rewire" orphans every account.
- Session cookie for the browser UI. No API key field anywhere in the UI: a key
  in the browser bypasses every per-account cap, and a shared key can only be
  bounded by the company ceiling.
- Password storage follows `credential-and-secret-handling`: slow salted hash,
  never SHA-256, never reversible encryption.
- Access is granted by a single-use, short-lived setup link minted by an admin
  endpoint, so the person sets their own password and no credential passes
  through Deep or a teammate. Deliver the link as a file with its expiry and
  reissue route (`credential-and-secret-handling`).
- Prove sign-up is closed rather than assuming it: the public sign-up route
  answers with a status saying it is disabled.

## 3. Enforce caps at the choke point, not in the UI

- Check the ceiling in the charged route itself, on every path that spends:
  single check, batch upload, background job run.
- **Reserve before, release after.** A batch reserves its full run ceiling up
  front and releases the unused remainder when it finishes, so two concurrent
  runs cannot spend the same allowance. Reserve against both the personal cap and
  the company ceiling.
- Failures carry the whole story: a 402 whose `detail` names spent, limit and
  company ceiling; a 403 whose `detail` names the tier and who can switch it on.
  The UI displays what the API returned and invents no numbers of its own.
- Admin cap edits validate bounds (a number or explicit null, sane range) and
  return every bad field in one response, so the admin screen can show them all
  at once.
- A run that crosses its ceiling stops on the request that crosses it and says so
  in the job note; it never silently truncates the list.

## 4. Admin surface

The super admin screen covers: people (list with effective caps and spend this
month, edit caps, switch on/off, reissue setup link, change role), limits
(allowed domains, default caps, company ceiling), usage (month, total against
the ceiling, spend by person, recent activity). Write that endpoint contract
verbatim into the brief; the frontend lane never invents endpoints.

## 5. Verify honestly

1. Local first, with every paid provider blanked and throwaway auth secrets
   (`workers-development`). Prove the blanking from an app response before any
   test that could call out.
2. Exercise every refusal, not just the happy path: wrong password, banned
   account, duplicate email, wrong domain, reusing a consumed setup link, a
   non-admin on an admin route, a person at a $0 cap, another person's job id, a
   self-service cap raise.
3. On the deployed URL, signed-out checks only unless Deep approves a paid probe:
   health, sign-in route present, public sign-up refused, signed-out API 401.
   Never bootstrap, create accounts or sign in on live to test.
4. When the paid provider has no key yet, do not stop at unit tests: put the provider's base URL behind one env var, run a local fake that plays each outcome (done, asks, capped, failed) with every payload labelled SAMPLE DATA, and drive the member journey over real HTTP on the local runtime. Report it as proven on a fake, with the provider's response shapes named as unverified.
5. Name which layer each claim rests on, and call an unexercised layer
   unexercised (`verification-gate-integrity`). A route-selection claim needs the
   probe that exercises it; otherwise report it as fixed in code, unproven in
   production.

## Pitfalls

- **Do not retire an old shared key on your own.** It is a cap bypass (bounded
  only by the company ceiling) and may still be wired into scripts; stage a
  decision card with keep/retire options and your recommendation first.
- **A null cap is "use the default", a 0 cap is "cannot spend".** Rendering them
  alike either blocks a person who should run free or silently zeroes someone who
  was meant to be limited.
- **A tier flag read raw off a user row lies for admins.** Show effective
  permissions, and state the display rule in the brief so the lane can be graded
  on it.
- **One-time links must be single-use and expiring, and their expiry must reach
  Deep.** Say when it expires and stage the reissue if the screen it unlocks
  lands later than that.
- **Do not hand the frontend lane architecture.** Land the endpoints, migration
  and pushed base branch first, paste the contract verbatim, then create the card.
