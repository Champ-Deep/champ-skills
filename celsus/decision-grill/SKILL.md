---
name: decision-grill
description: "Grill a product brief into dated rulings, code-checked."
---
# Decision grill

Turn a spoken or scattered product brief into a set of dated, written-down rulings that
a build can start from. Deep invokes this by name ("Grill Me", "Grill Me with Docs") and
answers the questions himself, so the job is to ask well, not to decide for him.

## Before the first question

1. **Read the whole brief, then find what already exists.** Every question about "should we
   build X" must be answered by the code first, not by asking. Grep for the concept, read
   the model docstring, read the CONTEXT.md glossary. A feature described as missing is
   often a named model with a schema and live endpoints.
2. **Verify every doc claim against the checkout that will actually run.** Repos frequently
   keep a `docs/` set describing a superseded generation. Confirm a gap against the branch
   that runs before acting on it.
3. **Write down the decision points you expect**, so the grill stays ordered and you notice
   when an answer opens a question you had not planned for.

## Question shape

One question per turn, via the structured ask, not prose. Each carries:

- **The tension**, stated in one sentence, showing why it is a real fork.
- **The evidence** you already gathered: the file, the line, the locked ruling, the
  existing model that already half-solves it.
- **2 to 4 options**, recommended first, each a genuine answer rather than a strawman.
- **What you think is wrong in the brief**, plainly, when the code or the user profile
  disagrees. Deep responds well to a real objection and poorly to a rubber stamp.

Never batch several questions into one turn. The whole value is that each answer narrows
the next question.

## Mid-grill discipline

- **He answers in prose rulings, not option letters.** Read the prose as the ruling. He
  frequently combines two options ("both, and also") or corrects his own terminology
  mid-answer; treat a correction as changing the answer, then re-read the code before the
  next question rather than assuming the earlier reasoning still holds.
- **A ruling that combines options needs its failure mode named.** Combining "semantic
  drift" and "expiry" is legitimate, but ask what happens when the two disagree. That is
  where the real design risk hides.
- **Name the hole, then leave it unruled.** Flag the risk your reading of his answer leaves
  open, propose the missing signal, and record it as explicitly unruled. Do not silently
  patch the gap, and do not stall the grill waiting for it.
- **Distinguish a gate from a check.** A gate is a checkpoint a human must clear; a check is
  a rule an agent runs. Which one he is ruling on determines whether an existing locked
  ruling is being broken.
- **Scope a ruling to its true reach.** A ruling like "outbound needs human approval" is
  not answered by "approve each send" if what he wants is "approve once, reuse". Ask what
  invalidates an approval: literal text, semantic class, time, or client context.

## Writing the rulings down

Two files with different jobs. Write both.

| Where | What goes there |
|---|---|
| The project's own scope/lock file (e.g. `docs/SCOPE.md`) | Dated rows stating the ruling and why, because that file is the project's statement of what is locked. Record rulings that touch a locked row HERE. |
| The Celsus effort note under `Efforts/Active/` | The reasoning, the evidence, the gap table, what stays open, what was deliberately not decided. |

At the end, consolidate every ruling into **one dated decision table** so the answer is a
decision set rather than a thread. Include the sequencing consequences the grill revealed,
since a ruling often creates a dependency nobody had written down.

## Pitfalls

- Never run a contact-enrichment or lead-pull pipeline for a product brief. A brief is not a
  target list, and running one spends money and produces the wrong artifact.
- Do not implement anything mid-grill unless he asks. The deliverable of the grill is
  written rulings.
- Do not let appended sections leave the document out of order: after appending several
  parts, renumber every part heading to match its position and verify with a heading grep.
- Do not treat a correct-sounding name in a brief as a real product. Grep the repos and the
  vault for it; it is often a mis-dictation of an existing product, and building the
  "new" one duplicates solved problems.
- Do not claim a doc gap as a gap without checking the live branch. A doc set describing a
  dark theme will send you to rebuild tokens that already shipped under a light theme.
- No em dashes in any written ruling, in either file. Verify with a grep on added lines
  only, since pre-existing lines may contain them and are not yours to change.
- Deliver written files with `MEDIA:` plus the absolute path, not a bare path.
