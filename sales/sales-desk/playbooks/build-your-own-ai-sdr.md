# Build Your Own AI SDR

Blueprint for the six jobs an AI SDR does, which to automate first, the guardrails, and what stays with a human.

## Give Claude
- What your team sends today: channels, rough volume, segments
- The tools you already have, by name: CRM, sequencer, data provider
- Optional: your best-performing message, pasted, as the style reference
- Optional: compliance rules you must respect: region, opt-out handling, industry
- Optional: how many sends a human can review per day

## Claude does
1. State the six jobs: find accounts, find contacts, verify contact data, write the first touch, follow up, log and hand off, one line each on what good looks like.
2. Rank them by risk and effort in your situation, and recommend the first two to automate, with reasons.
3. For each job, specify the input it needs, the output format, and the failure mode to watch for.
4. Write the guardrail checklist: what the system may never do, phrased as rules you could test for.
5. Draw the handoff line: the tasks that stay human (pricing, objections, negotiation, relationship repair) and the trigger that stops the AI mid-thread.
6. Define the review loop: what a human checks before send, sampled or full, based on the review capacity you gave.
7. Sequence the rollout: one job automated, one week of watched output, then the next job.
8. List the first thing to measure each week, so drift shows up early.

## Output
- Six-job table: `job | input | output format | automation order | failure mode`.
- Start-here note naming the first two jobs and why them.
- Guardrail checklist, each rule written as a testable "never".
- Human-retained list with the handoff trigger.
- Rollout sequence: job, week, review method, first measure.

## Rules
- Guardrails come before volume in the plan, never after.
- Never recommend sending to unverified addresses or pattern-guessed emails.
- No invented accuracy, response or productivity numbers. Rule of thumb or nothing.
- Assume no CRM integration unless you say you have one.
- Do not name tools the rep did not list.
- Anything involving money, contracts or legal terms stays human, always.
