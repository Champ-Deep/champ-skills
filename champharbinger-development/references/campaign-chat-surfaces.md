# Campaign chat and planning surfaces

Where a chat-driven planning behaviour plugs into ChampHarbinger, and how to prove one
works before anything is hosted. Paths checked on branch `test/explee-campaign-loop`
(base 8752b78). Re-grep before citing: line numbers drift.

## Reuse before you build

| Need | Read |
|---|---|
| A conversation scoped to one campaign | `src/components/campaign/workbench/campaign-conversation.tsx`, campaign-scoped chat store |
| The workbench shell and its view nav | `src/components/campaign/workbench/campaign-workbench.tsx` |
| Link from a campaign into the workbench | `src/app/(app)/campaigns/[id]/page.tsx` |
| Idea or account intake | `POST /api/pilot/[id]/accounts` |
| What needs attention today | `GET /api/pilot/[id]/decisions` |
| Counts the UI shows | `src/lib/tools/sequence-review-tools.ts`, read stored state, never an estimate |
| The review gate before anything sends | `src/lib/pilot/send-gate.ts` |
| Behaviour text the model reads | `src/lib/system-prompt.ts` |
| Its regression tests | `src/lib/system-prompt-context.test.ts` |
| What the chat can call at all | `src/lib/tools/index.ts` |

Rules that hold for every addition on this surface:

- Prompt text is advice, not a boundary. For a text-only Workbench mode, pass the mode on both submit and regenerate. In that route branch require a resolved campaign, ignore focus overrides, pass no tool registry, disable slash-command forcing, and retain only user/assistant text from shared chat history. Keep normal chat as a positive test control. This limits that request mode, not the user's separate access to normal chat.
- When running Vitest under an empty HOME after a frozen install, use the worktree's installed `node_modules/.bin/vitest` on Node 24. `pnpm exec` can try to download the pinned pnpm again in the empty HOME. If the full suite is red, reproduce named failures on the exact clean base under the same environment before attributing them to the change.
- A count the user sees comes from stored state. The model may phrase it, never derive it,
  and an outcome with no record renders as unknown instead of being inferred.
- Reuse the existing review gate. A second approval path beside it means two places to
  keep honest.
- No live transports, no scheduled sends, no real recipient data until Deep picks the
  deployment decision card.
- The marketing-to-sales handoff (who owns a booked meeting) is not built yet. Say so
  rather than implying a booking closes the loop.

## Verification recipe for a planning-loop change

Synthetic accounts only, two campaigns fed the identical list:

1. Ask campaign one for a plan and one sample pitch. Record time and steps to the first
   reviewable result. That ratio is the point of the change; anything else is anecdote.
2. Change the targeting in campaign one. Campaign two must be untouched. A proposal that
   bleeds across campaigns fails the loop.
3. Ask what needs attention today. Every number must match stored state, and an outcome
   with no record stays unknown.
4. Drive the UI to the review step and stop there. If review is reachable without
   reading the brief, the prompt is doing work the route should do.

Then read the diff scope back (`git status --short` limited to the named files) and state
in the handoff which gates ran, by command, and which never ran: full suite, provider
calls, authenticated use of the reference product. A peer's reported outcome numbers are
a hypothesis about the interaction, not a target to hit; label them as reported.
