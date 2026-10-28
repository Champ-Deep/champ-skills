# Releasing a large change through main

Deep's standing instruction for a site-wide upgrade: test it end to end, merge
to main, prove it live, and make sure the chatbot still works. Steps in order,
because two of them are irreversible in the wrong sequence.

1. **Build on a branch, never on `main`.** Integration happens on a release
   branch that merges `origin/main` in (content keeps moving; merge, do not
   rebase, so the nightly publisher's history survives). Re-run gates after
   every content merge: link check, prerender, self-tests, `npm test`.
2. **Gate the merge on real verification, not a lane's self-report.** Open the
   QA screenshots yourself with `vision_analyze` (blank-page and layout bugs do
   not show up in a status code), confirm commits are pushed, and run the test
   suites locally. A card marked `done` by a lane is a claim, not evidence.
   A half-finished UI never merges just because the clock is late; hold the
   merge and say so.
3. **Check third-party embeds by URL after merge**, not just their presence in
   the HTML: the chat widget script, its `?bot=` id, and the assistant origin
   answering 200. CSP must allow the frame and script origins. The chatbot
   (`assistant.deependhq.com`, widgo) lives on the main site and survives a
   toolkit release only if the HTML pass-through still injects it.
4. **Merge to `main` and wait for Workers Builds, then verify live:** body size
   not ~16KB (blank-site signature), the CSP header present, the new host
   serving, and every previously working host still serving (see the
   custom-domain rule in SKILL.md: a deploy replaces the whole domain set).
5. **Copy the deployed tree back into the vault checkout the publisher reads.**
   The nightly loop rsyncs the vault folder over `main` and deletes anything
   not in it, so a release that lands only in a repo checkout is reverted
   overnight with a green `PUBLISHED`. Reconcile the vault copy the same day,
   and check `git log origin/main` freshness before any publish
   (`rsync --delete` clobbers newer remote commits).
6. **A feature with no backend behind it must fail honestly.** Missing secrets
   or a missing binding means the page says `setup needed` (402) rather than
   pretending to work, so the gate is a checked state, not a banner.
7. **Keys and config Deep supplies never enter chat or git.** He writes them to
   a gitignored `.dev.vars` in the repo and you run
   `npx wrangler secret bulk .dev.vars` from there without printing the file;
   non-secret config (admin emails, flags) goes in `wrangler.jsonc` `vars`.
   Resource IDs (database id, binding names) are not secret and belong in the
   config, committed.
8. **A credit or spending system ships with every cap at $0** until Deep
   approves numbers in a decision card (`needs_input` with the recommended
   defaults first). Fail closed; never pick a default that can spend money.

Pre-merge checklist (release branch):

```
node scripts/link-check.mjs && npm test && node scripts/selftest-worker.mjs
npx wrangler deploy --dry-run --outdir /tmp/dhdry   # validates routes + bindings without deploying
dig +short <newhost>                                # record exists before you claim the host works
```