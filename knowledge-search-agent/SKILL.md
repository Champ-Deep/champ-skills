---
name: "knowledge-search-agent"
description: "Use when building a Q&A agent over Deep's notes." 
---

# Knowledge search agent

A Q&A agent over vault notes: files are staged into chunks, indexed in D1 with FTS5, retrieved on ask, answered by a Cloudflare Workers AI model streamed back to a small static page behind one passcode.

Order of work: corpus and index first, then retrieval, then answer streaming, then auth, then UI, then eval, then verify against the deployed URL. Each step has a check that fails loudly; do not proceed on an unchecked step.

## 1. Corpus and index

- Stage source files into a scratch cache, chunk them, and write an index. Keep this as a separate script from the ingest so re-indexing is repeatable.
- User-added notes live in a separate namespace from staged source files, and ingest must preserve them. Prove it: add a note, run the full rebuild, confirm the note is still listed and still cited by a question about it.
- Delete a note through the API only after confirming the answer that cited it no longer returns it.

## 2. Retrieval

- Keyword FTS5 over chunks beats naive relevance for this corpus shape; filter by weight, cap the context fed to the model, and always return the chunk's source title, type and date so the UI can show them.

## 3. Answer rendering (the defect class that costs the most rounds)

- Render markdown in the browser, never raw. Model output arrives as `**bold**`, `| tables |` and `- lists`; shipping it as text is what makes responses look bad.
- Normalise citation markers before escaping: some models emit fullwidth `【n】` instead of `[n]`, which a plain `[n]` regex misses, so the answer and the chip parser must map `【`/`】` to `[`/`]` first.
- Show citations as inline number chips plus source cards (type badge, date, snippet), not as raw `[n, date]` text. Clicking a chip should highlight its card.
- Strip YAML front matter and leading `#` from a source snippet before display, or the card shows `--- type: ... ---` to the user.
- Use a local date string (`new Date().toLocaleDateString('sv')`) for date inputs, not `toISOString()`, which returns the previous day for an IST user.

## 4. Auth: one passcode, asked once

Deep's standing rule for shared tools: "I can't have them running through so many hoops". One passcode the browser remembers, like his other agents. No URL-fragment keys, no key-plus-passcode pairs, no signing in again per question.

- Check a single passcode on every request as a header (the page sends `x-access-key`).
- Prompt in a `<dialog>` on the first request, store the passcode in `localStorage`, and clear the stored value if the server rejects it.
- Gate the prompt on whether a passcode is stored, never on whether the page was reloaded: a reload after passing must not ask again.
- Verify both directions in a browser: first ask prompts and then stores; second ask in the same session does not prompt.

## 5. Eval

- Normalise whitespace out of the answer before matching (`re.sub(r"\s+", " ", ans)`): models emit narrow no-break spaces inside phrases like "2 hours", so a literal-space regex fails on a correct answer and reports a defect that does not exist.
- Run the suite more than once before trusting a pass. One-shot failures on refusal questions are usually model non-determinism; fix only the failures that repeat.
- Print the failing answer and its sources with each FAIL, so a regex miss is distinguishable from a wrong answer.

## 6. Verify on the deployed URL

Close with `visual-verify`: dash count, audit, screenshots, then actually open the PNGs. For this class specifically:

- Drive the deployed URL with Playwright using `channel="chrome"` when the bundled browser is unavailable; seed `localStorage` to reach authenticated pages, and capture console/page errors into the report.
- Assert behaviour, not appearance: passcode stored after the first ask, no dialog on the second, no raw `**` or `|` in the answer text, citation chips present, source cards present.
- Report the platforms actually tested and name the untested ones (typically phone and Safari) rather than implying broad coverage.

A web UI you decide not to adopt (a CopilotKit-style framework, a Next.js app) can still be worth reading for its interaction ideas. Borrow the pattern, keep the stack.
