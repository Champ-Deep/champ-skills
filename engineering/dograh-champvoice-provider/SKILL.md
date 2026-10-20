---
name: dograh-champvoice-provider
description: "Use when maintaining the Dograh Champvoice provider."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [dograh, champvoice, voice, webhooks]
    related_skills: [adapter-seam-extension, verification-gate-integrity]
---

# Dograh Champvoice Provider

## When to Use

Use for a new Dograh provider feature, a Dograh webhook failure, or a Dograh integration update in Champvoice.

- Implement Dograh behind the existing provider interface, keep the Harbinger `agent_call` report shape unchanged, and add `dograh` to every routing enum and admin selector.
- Call `POST {DOGRAH_BASE_URL}/api/v1/public/agent/{DOGRAH_AGENT_UUID}` with `X-API-Key`, plus `phone_number`, allowed `initial_context` fields, and optional telephony IDs.
- Persist a `dropId` call-store entry before invoking Dograh because its public agent API has no idempotency header. Remove that entry if the request fails.
- Limit Dograh initial context to `drop_id`, `first_name`, `company`, `purpose`, `instruction`, and optional `greeting_override`. Render the full prompt into `instruction` and tell workflow authors to reference `{{initial_context.instruction}}`.
- Receive results through the workflow webhook node, not a global Dograh webhook. Verify the stored-credential custom header `X-Dograh-Webhook-Key` with `timingSafeEqual`, dedupe `X-Dograh-Delivery-Id`, and use `X-Dograh-Workflow-Run-Id` only as supplemental correlation.
- Configure the Dograh webhook payload from `services/champvoice/docs/dograh-webhook-template.json`; template values are strings, so parse duration defensively.
- Dograh transcript artifacts are line text such as `[timestamp] user: ...` and `assistant: ...`. Normalize that form and defensively accept JSON arrays for artifact-format drift.
- Map completed, answered, user_hangup, and normal agent end statuses to `human_answered`; busy, no-answer, and voicemail to `no_answer`; failed, canceled, error, and unknown values to `failed` while preserving provider status.
- Test outbound request body and errors, duplicate start refusal, each webhook authentication failure, redelivery dedupe, transcript normalization, status mapping, and routing enum acceptance. Run `pnpm test:champvoice`, `pnpm test`, `pnpm typecheck`, and `pnpm lint`.
- User-facing branding is ChampVoice, but wire identifiers are frozen: `X-Dograh-*`
  headers, the `dograh` provider enum value, managed model mode, env var names and
  API paths must keep their exact spelling or this integration breaks silently. When
  a rebrand pass proposes renaming them, refuse; relabel the visible string only.

## Rebrand pass: enforce it with a test, not a one-off grep

1. Write (or extend) a guard test that walks the UI source (`ui/src/branding.guard.test.ts`
   scans `.ts|.tsx|.css`) and fails on any visible brand string, with an explicit
   allowlist for protocol identifiers: quoted enum values, identifiers with the vendor
   name glued to word characters, separator-joined ids and paths, object keys, member
   access, outbound URLs. One `npx vitest run src/branding.guard.test.ts` replaces a
   hundred manual greps and catches regressions in the next feature branch.
2. When copy must truthfully name the upstream vendor (see the rule below), allowlist
   exactly one anchored sentence, never a broad `/vendor/i` pattern: every occurrence
   staying in the tree should remain a reviewed decision.
3. Verify the DEPLOYED assets, not the tab. Browsers cache favicons per-origin almost
   forever, so after a rebrand deploy fetch `/favicon.ico` and the logo files directly
   and compare against the repo before reporting the old mark as still live.
4. Ship brand art (mark, wordmark, favicon layers) as hand-written SVG rasterised to
   the exact filenames the code already references, so no import paths change; the
   `.ico` needs 16/32/48/64/128/256 layers and must be checked on a contact sheet at
   16 px against the dark sidebar colour.

## RULE: rebrand the label, not the truth

Stripping a vendor's name never permits inventing a substitute claim. Copy must not
name a non-existent entity ("provisioned by our admin team") or imply capability the
install lacks. Where money, hosting or accountability actually flows through the
upstream vendor, the copy says so once, plainly, and points at the escape hatch.
Hiding the paywall inside white-label wording turns a routine billing limit into a
trust failure the day credits run out.

## Model modes: who runs it, who bills it

| Mode | Runs on | Metered how |
|---|---|---|
| Managed | vendor's hosted transcriber, LLM and voice behind an auto-issued service key | credits at 1 credit = 1 cent; a fresh install carries a 500 credit trial; at zero, Managed runs refuse to start |
| BYOK | the operator's own provider keys | credits are never checked; providers bill directly |

Managed is a comparison lane; BYOK is the product. Any balance shown in the UI must
state which mode it meters, and BYOK being credit-free is the standing answer to
"what happens when the trial ends".
