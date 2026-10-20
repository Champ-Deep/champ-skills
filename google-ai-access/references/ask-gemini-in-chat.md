# Ask Gemini in Google Chat: gates and reach

Verified against Google's Chat help page and the Workspace blog. Re-check the
help page if a feature list matters to a build; these features move.

## Gates (in order)

1. Eligible **Google Workspace subscription** (consumer Google AI plans do not
   unlock it). English only, for now.
2. Admin enables **Gemini in Workspace in Chat** and **Workspace Intelligence**
   for the org. Deep admins `championsmail.com`, so he flips these himself.
3. The user is enrolled in **Workspace Smart Features**.
4. Admin may need beta features on for message-level Ask Gemini.

## Entry points

- Google Chat or Gmail left rail: **Shortcuts > Ask Gemini**.
- Keyboard: Cmd+G on macOS (Ctrl+G on Windows/ChromeOS).
- Next to the search bar.
- Highlight text inside any Chat message, then the Ask Gemini icon (beta only).

## What it can reach and do

| Capability | Detail |
|---|---|
| Workspace search | Gmail, Drive, Calendar, with citations in the answer |
| Artifact creation | Google Docs, Slides, Sheets, images, all editable |
| Daily brief | On by default: to-dos, unread threads, urgent items |
| Skills | Workspace Studio skills, invoked in the prompt; the Workspace equivalent of Celsus skills |
| Deep research | Connected to Gmail, Docs, Drive and Chat |
| Third-party connectors | Asana, Jira, Salesforce confirmed (Oct 2026) |
| Sessions | Persistent across conversations; keeps context |
| Scheduling | Find, schedule, manage calendar events |
| Drafting | Email and chat drafts against Workspace context |

## What it cannot reach

- Pictures and videos in Drive that do not live inside a Doc, Sheet, Slide, or
  PDF.
- The consumer Gmail account's Drive. It reads the **Workspace** account's
  data only, so shared folders must be homed there.
- Obsidian semantics: `[[wikilinks]]` are plain text to it. Publish resolved
  paths.
- Non-English prompts (as of the checked help page).

## Design implication for the shared context layer

Everything Gemini produces lands as Google-native files in the folder it owns.
Hermes pulls those back with `gog docs export` / `gog drive download`; it never
edits them in place in Drive. Ownership rules are in
`knowledge-tier-boundaries`.
