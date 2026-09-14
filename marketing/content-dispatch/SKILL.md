---
name: content-dispatch
description: >
  Activates when a user pastes a bare URL (YouTube, blog, podcast, Twitter/X thread) with little or no text. Extracts content, analyzes business relevance via CLAUDE.md, creates a vault insight note with next steps, and plants reminders in the daily note Tasks section plus a Content Queue for the morning routine. MANDATORY TRIGGER when the message is primarily a URL (bare link, "check this out [link]", "thoughts on this [link]"). Also trigger on "dispatch this", "apply this to my business", "what can I learn from this". Do NOT trigger when the link is part of a larger request like "write a blog about this" or "summarize for my team". This is the "paste link, get business intel + vault note + task reminders" workflow.
---

# Content Dispatch

> Paste a link. Get business intelligence. Never lose an insight again.

Content Dispatch is your "capture and contextualize" skill. When you encounter a YouTube video, blog post, podcast episode, or Twitter/X thread that sparks an idea, just paste the link. This skill handles the rest: it extracts the content, maps it to your business world, files an insight note in your vault, and ensures it surfaces in your next morning routine so you can decide what to act on.

## When This Skill Activates

The trigger is simple: the user's message is **primarily a URL**. This means:

- A bare link with nothing else
- A link with minimal context like "check this out", "thoughts?", "interesting", "dispatch this"
- A link with a brief note like "saw this, might help with ChampGraph"

The skill does NOT activate when the link is part of a bigger ask. If the user says "write a blog post inspired by this link" or "summarize this article for my Lake B2B team", that is a different workflow handled by other skills (b2b-blog-writer, internal-comms, etc.). Content Dispatch is the "capture now, act later" path.

## The Pipeline

Content Dispatch runs four phases in sequence. Execute all four autonomously without stopping to ask permission between phases (the user trusts autonomous execution, per CLAUDE.md). Only pause if the vault routing is ambiguous (Phase 3).

### Phase 1: EXTRACT

Detect the link type and pull content.

**YouTube** (`youtube.com`, `youtu.be`):
1. Install yt-dlp if not present: `pip install yt-dlp --break-system-packages`
2. Extract transcript: `yt-dlp --write-auto-sub --sub-lang en --skip-download --print-to-file "%(title)s|||%(channel)s|||%(upload_date)s|||%(duration)s" info.txt <url>`
3. If auto-subs unavailable, try `--write-sub` for manual subs
4. Fallback: use WebFetch on the video page and extract whatever text is available
5. Collect: title, channel name, upload date, duration, transcript text

**Blog / Article** (any non-video, non-social, non-podcast URL):
1. Use WebFetch to retrieve the page
2. Extract main content (strip nav, ads, sidebar, footer boilerplate)
3. Collect: title, author (if available), publish date, domain, full article text

**Podcast** (`open.spotify.com/episode`, `podcasts.apple.com`, `podcasts.google.com`, or any URL containing `/podcast/` or `/episode/`):
1. Use WebFetch to retrieve the episode page
2. Extract: episode title, show name, publish date, show notes/description
3. If a transcript link is available on the page, fetch that too
4. Note: full transcripts may not always be available. Work with whatever the page provides (show notes are often rich enough for analysis).

**Twitter / X thread** (`twitter.com`, `x.com`):
1. Use WebFetch or get_page_text to retrieve the thread
2. Extract all tweets in the thread in order
3. Collect: author handle, display name, tweet text (all parts), date, engagement metrics if visible

**Output structure** (internal, not shown to user):
```
source_type: youtube | blog | podcast | twitter
source_url: <the URL>
title: <extracted title>
author_or_channel: <who made this>
date_published: <when>
duration: <if applicable>
full_text: <the extracted content>
```

After extraction, generate a **3-5 sentence summary** of the content that captures the core insight, argument, or takeaway.

### Phase 2: ANALYZE

Read the user's `CLAUDE.md` file to understand their business context. You already have this in your system prompt, so no need to re-read it. Use the following from CLAUDE.md:

- **Companies** (all 12, with current attention levels)
- **Products** (all 11, with engagement levels)
- **Active Efforts** (with status)
- **Key People** (for relevance matching)
- **Terms Decoder** (to connect jargon)
- **Current Attention Levels** (Deep Focus > Active > Aware)

Now analyze the extracted content through this lens. Produce:

1. **Key Takeaways** (3-5 bullets): What are the most important insights from this content? Be specific and actionable, not vague summaries.

2. **Business Application**: How does this content connect to the user's world? Name specific companies, products, efforts, or people using `[[wikilinks]]`. Prioritize connections to Deep Focus companies and Primary Build products. Example: "This video's approach to AI-driven email personalization directly applies to [[Champmail]]'s outreach cadence design. The sender rotation technique could reduce bounce rates in the Lake B2B pipeline."

3. **Recommended Next Steps** (2-3 concrete tasks): Frame these as checkbox items the user can act on. Each should be specific enough to execute without further research. Example: "Share the sender rotation technique with [[Charles]] for Champmail's next sprint" rather than "Consider improving email deliverability."

4. **Relevance Score**: Rate as High, Medium, or Low:
   - **High**: Directly applies to a Deep Focus company or Primary Build product, and the user could act on it this week
   - **Medium**: Applies to an Active company/product, or provides strategic insight that informs a current effort
   - **Low**: Interesting but tangential. Applies to Aware-level companies or general professional development

5. **Mapped Entities**: List all `[[wikilinked]]` companies, products, efforts, and people this connects to.

### Phase 3: STORE

Create the insight note and route it into the vault.

**Note filename**: `YYYY-MM-DD - {Sanitized Title}.md` (sanitize: remove special chars, truncate to 60 chars)

**Note template**:
```markdown
---
type: content-insight
source_type: youtube | blog | podcast | twitter
source_url: "{url}"
date_captured: "YYYY-MM-DD"
relevance: high | medium | low
mapped_to:
  - "[[Entity 1]]"
  - "[[Entity 2]]"
tags:
  - content-insight
  - {source_type}
  - {relevant domain tags from CLAUDE.md taxonomy}
---

# {Title}

**Source:** [{Author/Channel}]({url})
**Captured:** YYYY-MM-DD
**Relevance:** {Score}

## Key Takeaways

{3-5 bullet points}

## Business Application

{Analysis connecting to [[Company]], [[Product]], [[Effort]] with specific wikilinks}

## Recommended Next Steps

- [ ] {action 1}
- [ ] {action 2}
- [ ] {action 3}

## Original Summary

{3-5 sentence distillation of the content}
```

**Routing logic** (decide where to file the note):

1. **Single company match** (content primarily about/for one company): File in `Atlas/Context Docs/{Company}/` (e.g., `Atlas/Context Docs/Lake B2B/`)
2. **Single product match**: File alongside the product in `Atlas/Products/`
3. **Active effort match**: File in `Efforts/Active/` as reference material
4. **Personal/professional development** (leadership, productivity, general business): File in `Atlas/Context Docs/General/`
5. **Multi-entity match** (equally relevant to 2+ entities): Ask the user. Present the options: "This insight maps to both [[Champmail]] and [[ChampGraph]]. Where should I file it?" Options: the mapped entities + Inbox as fallback.
6. **Unclear**: File in `Inbox/` and let vault-keeper triage later.

After filing, add wikilinks from the note to all mapped entities. This strengthens the knowledge graph and ensures vault-keeper can maintain connections.

### Phase 4: SURFACE

Two-pronged reminder system to ensure the insight doesn't get lost.

**4A: Daily Note Task**

Find today's daily note at `Calendar/Daily Notes/YYYY-MM-DD.md`.

- If the daily note exists and has a `📋 Tasks` section with a `### New Today` subsection: append the task there.
- If the daily note exists but has no Tasks section yet: create the section with the task.
- If no daily note exists for today: create a minimal one with just the task (the daily-note-recap skill will fill in the rest later).

Task format:
```markdown
- [ ] 📺 Review insight: "{Title}" -- {one-line business application} [[{note filename without .md}]]
```

Use 📺 for YouTube, 📰 for blogs, 🎙️ for podcasts, 🐦 for Twitter/X.

**4B: Content Queue**

Maintain a running queue at `Inbox/Content-Queue.md`. This file persists across days and is the source the morning routine reads to present pending insights.

If the file doesn't exist, create it with this structure:
```markdown
---
type: content-queue
tags:
  - content-insight
  - queue
---

# Content Queue

> Insights captured via Content Dispatch. The morning routine surfaces pending items for prioritization.

## Pending

| Date | Title | Relevance | Mapped To | Status |
|------|-------|-----------|-----------|--------|
```

Append a new row to the Pending table:
```markdown
| YYYY-MM-DD | [[{Note title}]] | {High/Medium/Low} | [[Entity1]], [[Entity2]] | pending |
```

When an item is acted on (the user completes the task or explicitly skips it), update its status to `done` or `skipped`. Vault-keeper can clean up old done/skipped items during its regular triage.

## How This Connects to the Morning Routine

The morning routine's Phase 3 (interactive quiz) already reads the daily note for carried-forward tasks and asks the user to prioritize. Content Queue items with "pending" status are additional inputs for that phase. The morning routine can present them as drag-to-rank tiles or swipe cards:

- "You captured 2 insights yesterday. Prioritize them:"
  - 📺 "AI SDR Techniques" (High relevance, maps to ChampIQ) → **Act Today / Nice to Have / Skip**
  - 📰 "B2B Email Deliverability Guide" (Medium, maps to Champmail) → **Act Today / Nice to Have / Skip**

The content-dispatch skill itself does NOT modify the morning routine. It simply provides the data (Content Queue + daily note tasks) that the morning routine already knows how to consume. If the morning routine skill needs updating to read the Content Queue, that is a separate change.

## What This Skill Does NOT Do

- Does not handle PDFs, documents, or file attachments (those have their own workflows)
- Does not create scheduled tasks (reminders flow through daily notes and the Content Queue)
- Does not auto-execute recommended next steps (it suggests, you decide)
- Does not modify the morning-routine or interactive-quiz skills
- Does not activate when a link is part of a larger request (e.g., "write a blog about this")

## Edge Cases

**Transcript unavailable (YouTube):** If yt-dlp can't extract a transcript (private video, no captions), fall back to the video title + description from the page. Note this limitation in the vault note: "Note: Full transcript unavailable. Analysis based on title and description only."

**Paywalled articles:** If WebFetch returns minimal content due to a paywall, note this in the vault note and work with whatever was extracted. The user can manually add content later.

**Already-captured content:** Before creating a new note, check if a note with the same source_url already exists in the vault (grep for the URL). If it does, notify the user: "You've already captured this. See [[existing note]]." Do not create a duplicate.

**Multiple links in one message:** If the user pastes multiple links, process each one independently. Create separate vault notes and tasks for each.
