---
name: cross-store-recall
description: Use when Deep asks what we came up with or what is done.
version: 1.0.0
author: Deep / Hermes
license: MIT
metadata:
  hermes:
    tags: [recall, sessions, kanban, verification]
    related_skills: [chat-decision-monitor, kanban-task-intake, celsus-vault]
---

# Cross-store recall and status verification

## When to Use

Use when Deep asks what was decided, proposed, or "come up with" in past sessions, which of several ideas are done, or where an idea went: any recall question that needs a status verdict (verified done, never captured, unverified) rather than a guess.

Deep recalls an idea, list, or decision from past sessions and asks what it was and whether any of it is done. The answer must be built from executed searches across every store plus executed proof for any "done" claim. There is no single index of past work; a term can live in zero, one, or all of these stores.

## Procedure (run the search steps, then the verification steps)

1. **Name the claims to verify.** Split the question into: (a) did the idea/discussion exist, (b) was it ever captured as a task/note, (c) is any part built and done. Each claim gets its own evidence below. Keep a short list of search terms: the user's exact term, its likely synonyms, and one broader query for homonyms (step 7).

2. **Vault first.** `TASKS.md` is the canonical record of tasks: `grep -in '<term>' /Users/deep/Celsus/TASKS.md`. Then a vault-wide content search across the other layers for the discussion itself (notes, Atlas, Efforts). If TASKS.md has no line, the idea never became a tracked task, regardless of what other stores show.

3. **Kanban via the tool, not the file.** Call `kanban_list` (filter by status/assignee if the term is a known lane). Never grep `~/.hermes/kanban/boards/<board>/board.json` for task content: that file is a stub/index, not the task store, and a grep of it returns nothing while looking authoritative. `kanban_list` returns only the newest rows (default 50, max 200, `truncated: true` on overflow) with no offset, so absence in that window proves nothing about older work: treat TASKS.md as the authoritative absence check and the tool as confirmation of current state.

4. **Sessions, per profile.** `session_search` defaults to the active profile; work routed to lanes lives in other DBs. Run the same query against each profile that exists under `~/.hermes/profiles/` (content, frontend, inbox, worker) plus default. FTS5 ANDs terms: start with the single rarest term alone, then broaden with `OR`, prefix (`term*`), and quoted phrases rather than adding more required words. When a hit matters, scroll it (`session_id` + `around_message_id`) to read the full exchange instead of re-searching: the snippet hides whether an idea was answered, deferred, or never answered (an empty assistant reply means the ask was never served).

5. **Side stores for stray captures.** Reminders: `remindctl list | grep -i '<term>'`. Apple Notes: `memo` search. A reminder-shaped ask that appears in no store in steps 2-4 usually never became a task; say so explicitly rather than implying it was lost later.

6. **Repos and code, bounded.** Search `~/repos` with a bounded command: `find /Users/deep/repos -maxdepth 3 -not -path '*/node_modules*' -not -path '*/.git/*' \( -name '*.md' -o ... \) -print0 | xargs -0 grep -il '<term>'`. Never an unbounded grep/rg over `/Users/deep/repos`: the tree is large enough to time out and yields nothing usable.

7. **Homonym pass.** Run one broad query to catch the term meaning something else (a palette name, product codename, theme token). Report the collision in the answer so future searches use a distinct word; a homonym is also why a zero-result search must not be reported as "never existed".

8. **Verify "done" with executed evidence.** For anything claimed built: enter the repo and run `git status -sb`, `git log --oneline -1`, `git remote -v`. A session's narrative that work shipped (including a subagent's self-report) is not proof; a pushed branch with a real commit hash is. Deployment is a separate claim from code done: check the deploy target before calling a thing live.

9. **Answer in three buckets, evidence attached:** (a) exists and verified done, with the commit/branch or tool output; (b) requested but never captured anywhere, naming the store gap (offer to capture it as a kanban card so it stops being a ghost idea); (c) collisions and unverified gaps. Never answer a recall question from memory alone, and never upgrade "not found in store X" to "never existed" without having run steps 2-6.

## Pitfalls

- Grep the kanban board file: it is a stub/index, so the grep returns empty and looks like proof of absence while task content lives behind the `kanban_list` tool.
- Treat a `truncated: true` kanban_list as a full inventory: it caps at the newest rows, and the idea you are hunting is usually older than the window.
- Add terms to an FTS5 session query until it returns nothing: AND semantics make every extra word a filter, so a two-word query can miss the one message that has the phrase. Query the rarest single term, then OR.
- Search only the active profile for past work: cards routed to content/frontend/inbox/worker sessions are stored in their own profile DBs and will not appear.
- Grep `/Users/deep/repos` unbounded: the walk times out on node_modules and .git before reaching a hit. Bound with `-maxdepth` and path excludes.
- Report "done" from a chat transcript or a delegated agent's summary: those are self-reports. Prove it with git output or a read-back of the target system.
- Report a zero-result search as "we never did X": name collisions (palette, codename, theme token) produce false zeros; run one homonym query and disclose what it found.