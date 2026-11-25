# Skills for a managed Claude agent

Mechanics verified against the Claude Platform docs ("Skills" page for Managed Agents). Read this when the assistant is a Console/managed agent that should work the way Deep's own skills make Hermes work.

## Two delivery routes, only one stays current

| Route | How | Currency |
|---|---|---|
| Attached | Upload a skill folder or zip to the workspace, get a `skill_*` id, list it in the agent's `skills` array (`version: latest` or a pinned version) | Frozen at upload. New upload = new version. Nothing tells you a source skill changed |
| Repository | Mount the repo as a `github_repository` resource; at session start it scans `.claude/skills/<name>/SKILL.md` | Always the checked-out branch. A push picked up by the next session, never the current one |

- Repository discovery is exactly one directory level deep from the repo root: `.claude/skills/<skill>/SKILL.md`. A bare `.claude/skills/SKILL.md`, a nested `.claude/skills/tools/<skill>/`, or a `skills/` folder outside `.claude` is not announced at session start.
- Discovery needs the agent's `read` tool enabled (it is on by default).
- Both routes at once are fine, and a name present in both yields both copies.
- The session cap is 500 skills, deduplicated across every agent in the session.
- Anthropic's own `pptx`, `xlsx`, `docx`, `pdf` ship in every workspace: never package a copy.

Rule: anything that must keep up with Deep's living skill library goes in the repo route. Uploading a freeze-frame and calling it current is the failure mode.

## Pack layout

Generate `.claude/skills/` from a manifest (`pack.json`) in the pack repo. The generated tree is never hand-edited; the source skill is edited in `champ-skills`, then rebuilt.

Manifest keys:

- `categories`: whole source folders (e.g. `design`). A skill added to that folder later arrives without anyone editing the manifest.
- `skills`: named skills from the rest of the library, with a short `description` override when the original is too long for the agent's trigger budget (1024 characters). Rewrite the description in the copy only, and frontload the "use when" clause.
- `hermes`: skills that exist only under `~/.hermes/skills` and not in the GitHub library. Copies live in `extra/` in the pack repo and are refreshed only when the build runs on Deep's Mac; GitHub cannot see the Mac, so a CI build reuses the committed copy. Third-party authored ones need a licence read and Deep's yes before the pack repo is made public.
- `excluded`: skills that other skills name but the agent must not chase, each with a one-line ruling ("use your built-in web fetch", "you never send", "needs Deep's vault") so a skill name never lands in the agent's lap without an answer.

Emit `SOURCE.json` with the source commit plus whether the source clone had uncommitted changes, so a stale pack is visible in the file rather than claimed later.

## Reference closure: the pass that makes a pack honest

1. For every packed skill, regex the backtick-quoted tokens out of every `.md` in its folder and keep the ones that match a real skill name in the source library.
2. Each match must land in exactly one of: packed, `excluded` with a ruling, or fetched on demand through a pointer skill that lists the whole library with paths.
3. Generate the not-included table from that pass instead of writing it by hand.
4. Re-run the same check on the entry-point skills (the ones Deep names first) and require an empty "unexplained" list before reporting the pack done.

Why it matters: a hand-picked subset fails silently. The agent reads its skill, calls for a companion that is not there, and improvises a weaker version.

## Guards that fail the build instead of shipping

- A manifest path with no `SKILL.md` in the source checkout.
- A description over the 1024-character trigger budget, or a frontmatter `name` that does not match its folder name (the agent addresses skills by folder name).
- A skill folder nested more than one level deep, which the repo scan will not announce.

## Deck and document routing inside the sandbox

- `power-design` gives the slide rules and the anti-slop checklist; its brand library holds outside brands only and its brand extraction needs Firecrawl, which the sandbox lacks. So the brand comes from the brand skill of the company that signs, never from scraping a URL or from that library.
- An editable deck copy comes from Anthropic's built-in `pptx` skill. HTML decks and `pptx` are two outputs of the same brief, not alternatives.
- Pipeline skills that need outside APIs (Proxycurl, Ahrefs, NotebookLM) cannot run in the sandbox: name them as unavailable in the brief rather than letting the agent try and half-succeed.
- `visual-verify` is the closing gate for anything visual; when the sandbox cannot render, the agent must say so in the private half of its deliverable instead of skipping the claim.