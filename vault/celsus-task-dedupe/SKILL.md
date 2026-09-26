---
name: celsus-task-dedupe
description: "Use before appending to TASKS.md. Search, then append."
---

# Dedupe before appending to TASKS.md

## When to use

Every single time you are about to add a line to `/Users/deep/Celsus/TASKS.md`. This is not a final pass. It is the step before the write.

TASKS.md holds 1,389 open items in `## Active` and 1,516 open overall. The list stopped being a list because agents file the same task every week. Measured on 2026-09-26: the Santosh Core 7 ask exists **five times** (`TASKS.md:44, 75, 134, 358, 364`) and the Sales Leaders Update three times (`:45, 76, 135`). The Ampliz ownership question has regenerated for twelve straight weeks.

Every append costs the reader a triage decision later. Dedupe before you write, not after.

## The procedure

1. Build the search key before you compose the line: **company + verb + object**, lowercased, singular. `virtusa + recap + management call`, not "Virtusa management call recap draft thing".
2. Search `## Active` in `/Users/deep/Celsus/TASKS.md` for that key. Use `search_files` with `output_mode: content`, never eyeball the file. `## Waiting On` counts as a hit too, and so does `## Done`: a task closed and re-opened by a fresh append is a duplicate, not new work.
3. **Hit found:** do not create a line. Append a dated progress note inside the existing task body, so the history is one thread:

```
- [ ] **[P0] Original title** - original context. [e:...] [c:...] [captured:2026-09-20] (re-confirmed 2026-09-26, fourth week: still no answer)
```

If the existing line is three weeks old and has not moved, do not just re-confirm it. That is the three strikes rule below.

4. **No hit:** append a new line into `## Active` using the task format in `_config/conventions.md`. Every field is required: `[e:]`, `[c:]`, `[s:]`, `[captured:]`. Add `[link:]` when a source note exists. Never write past `## Done`.

## The three strikes rule

A task regenerated three weeks running with no movement becomes a forced choice, not a fourth line. Route it to the [[Efforts/Active/Agent Operating Plan W40/Agent Operating Plan W40|W40 plan]] Approval Queue as one of: do it, delegate to a named person, or drop it. A task with no owner and no movement is a task nobody wants.

## Matching, so you catch the real duplicate

Near-identical wording hides the duplicate, so match on structure:

- A weekly item recurs as the **company**, not the date. `week of [[2026-09-21]]` and `week of [[2026-09-14]]` are the same Sales Leaders Update.
- Re-filed under a different flag is still the same task. `[WEEKLY UPDATE]`, `[SALES DATA]`, `[BRAND SEO]` on the same account in the same week are one thread.
- A blocked variant is a duplicate. If last week's line says BLOCKED and this week's says the same thing, append the re-confirmation instead of a new task.

## Never

- Never estimate a number to avoid a gate. A missing input is a `BLOCKED` note, not a placeholder figure.
- Never name a vendor to a client in a task line that Deep may forward.
- Never write personnel, pay, visa, PIP or FNF content as anything other than facts. Agents gather, Deep answers.
- Never move `TASKS.md` or `dashboard.html`. Root only.

## Verify before you finish

Run the search key once more after writing. Zero new lines for a task you believed was new is a correct outcome, not a failure to find work.
