# Adding a tool action to the Deep End Toolkit (dh-toolkit-v4)

Recipe for "a new thing a user can run in the toolkit", written from the Sonar build. Main lane owns the backend and every design decision; a frontend card owns the window. Read `references/release-and-toolkit-host.md` for deploy and local-suite facts first.

## The pattern: model proposes, browser computes

Never let a model compute a number the user will read. Split every "AI answers a question about my data" feature into two halves that both validate:

1. **Server half (main lane).** The model sees a *profile* of the data only: column names, inferred types, row count, a handful of sample values per column. Never the rows. It returns a plan: view kind, filter, group by, measure, a headline template, follow-up questions. Server runs the whole gate below, then logs and bills.
2. **Browser half.** Re-validates the plan against the real headers (`validatePlan`), then computes every value locally with a pure shared module. The rendered digits come from `runPlan`, always.
3. **Serve both halves from ONE module** (`sonar-core.js` shape: pure functions, no imports beyond what it is given) so server and browser cannot drift. Selftest the module on its own (`node scripts/selftest-sonar.mjs`), then assert the *wiring* in the existing action selftest (that the profile reaches the model, that rows do not).

Rules that hold for any model-emitted output, not just plans:

- **Reject a headline containing a digit** when the plan itself supplies one. A template with a placeholder (`{top} leads with {top_value}`) is fine; a baked-in number is the model guessing at data it never saw. Drop it and fall back to the neutral description of the plan.
- **A plan that fails validation renders as a question, not as a chart.** Show the model's `question` text so a refusal still reads as help.
- **Never render a truncated result without saying it is truncated.** "first 20 rows" is honest; "all matching rows" over a capped preview is a data-honesty failure (the site's honesty rule).
- Budget the grammar deliberately: count / sum / avg / min / max / distinct over filters plus one group-by covers most real questions. Anything past it comes back as a clarifying question, which is the designed behavior, not a bug to hide.

## Steps

1. **Contract first.** Write the action's request and response shape into `docs/toolkit-v4-api.md` (the section every lane reads) before any code. This is the file the frontend card quotes verbatim.
2. **Pure core** (`<tool>-core.js` at repo root, loaded by both sides): profile, validate, compute, format, describe. Keep it dependency free so the browser can import it directly.
3. **Worker action** in `worker/toolkit.js`: register the action name, parse and bound the input (file size caps live in one place, do not restate them), call the provider through `cols.routing(llm)` with `require_parameters` and `max_price` at the reserved rates (one OpenRouter model id spans endpoints priced up to ~25x apart; without it a call can bill above its reserve), scrub anything user-supplied out of the prompt, reserve then settle the billing the way intake does, and log to `ai_log`.
4. **Selftests.** New pure-module selftest plus a block in the v4 selftest covering wire shape (response format, model, history passed, profile not rows), billing reserve/settle, input validation, prompt scrubbing. Wire the new selftest into the `package.json` test script.
5. **Run the full gate and read the real exit codes**: `npm test`; `node scripts/selftest-worker.mjs`, `-segment`, `-copy`, `-digest`, `-privacy` (all five, always); `node scripts/guard.mjs` (em dashes and denylist, fails the build); then `git status --short` and `git log -1` so the commit you name is the tree you tested.
6. **Fixture reply** in `tests/fixture_server.py` for the new action: one canned plan-shaped reply plus a second for the failure path. The local suite is `fixture_server.py` on 3175 and `node scripts/toolkit-browser-server.mjs` on 3176; start both with `subprocess.Popen` from `execute_code`, the terminal tool refuses `&`.
7. **Browser proof** with Playwright from `/opt/anaconda3/bin/python3` (the only python with playwright): drive the real UI, then *compute the expected value independently in the test* from the same fixture CSV and assert the rendered digits equal it. A screenshot is not a number check.
8. **Card the UI.** Frontend card body carries the contract verbatim, the core module's exported functions with signatures, a worked example with real expected output, the component ids the main lane picked, and a "do not touch" list naming the backend files. Set `workspace_kind=dir` at the checkout you just tested, and set `parents` to the decision card that approved the shape so the UI only starts once that decision is closed.
9. **Close the decision before releasing the child.** `kanban_complete` on the decision card (metadata carries the decision, the branch, the pricing default) is what promotes the UI card out of `todo`. An approval that exists only in chat means the card never starts.
10. **Deploy last, behind the gates.** `ultimate-security` deploy gate plus a `security-audit` pass over the diff, then the release path. Nothing reaches the live host without Deep's word.

## Pitfalls

- A worktree's `node_modules` is a symlink; `Cannot find package '@clerk/backend'` means it points at a tree without the toolkit deps. Repoint it at `/Users/deep/repos/dh-toolkit-v4/node_modules`, never reinstall.
- A model reply that is not valid JSON must degrade to a designed state, not an exception: treat parse failure exactly like a null plan (the question / setup message the UI already renders).
- The pricing question does not need a new price. Reusing the existing metering (reserve, settle at real token cost, daily cap) is a default worth stating on the decision card, not a decision to invent around.
- Keep the browse-and-enrich chain cheap: hand the next tool the rows it already has (`w.load(rows, name)`) instead of re-uploading, and keep that handoff to one function call.
