---
name: chatgpt-query-spy
description: >-
  Reveal the exact web search queries ChatGPT runs behind any prompt (its fan-out sub-queries) by reading the conversation response in browser DevTools, then place that exact language across titles, slugs, H1s, opening sentences, FAQs and social posts to influence what ChatGPT says about a brand, product or category (GEO / AEO). MANDATORY TRIGGER for: "what did ChatGPT search", "see ChatGPT's search queries", "fan-out queries", "influence ChatGPT answers", "get ChatGPT to recommend us", "show up in ChatGPT", "ChatGPT visibility", "generative engine optimization", "answer engine optimization", "AEO", "GEO for AI search", a request to capture how an AI answer engine searches, or any prompt to test what ChatGPT says about a category we sell into. Pairs with seo-toolkit for on-page execution.
---

# ChatGPT Query Spy

ChatGPT answers are built from web searches you never see: it rewrites one prompt into several fan-out queries, searches each, then synthesizes. Those query strings are the exact language it reads the web with, so they are the highest-signal copy targets for generative engine optimization. This skill has two halves: CAPTURE (read the queries out of your own ChatGPT session) and WEAPONIZE (turn them into placements). It never guesses at queries and never presents a model's own reconstruction as an observed search.

## When to Use

- "What did ChatGPT search when I asked X?"
- Capture the fan-out queries behind a prompt about our category, product, client, or competitor.
- A client asks why ChatGPT recommends a competitor, or asks to get into ChatGPT's answers (GEO / AEO work).
- After a capture, deciding where the captured language should live.

Don't use for: classic keyword SEO (seo-toolkit), rank tracking, or Perplexity and Google AI Overviews query capture (those run server-side, see Pitfalls).

## Prerequisites

- Desktop Chrome or any Chromium browser, plus a logged-in chatgpt.com session. The method reads your own session traffic only.
- Web search enabled in ChatGPT (View all tools, then Search). A prompt that does not search produces no query field.

## Capture procedure

Do this in the human's browser while they watch, or hand them the numbered list. An agent cannot see a human's logged-in chatgpt.com session from its own browser stack.

1. Send the prompt in chatgpt.com and let the answer finish. Done when: the answer shows search citations (the source list under the reply).
2. Copy the conversation ID: the URL is `chatgpt.com/c/<id>`, copy only the part after `/c/`. Done when: a short ID string is on the clipboard.
3. Right-click the page, Inspect, open the Network tab. Confirm recording is on, enable Preserve log, set the filter to Fetch/XHR. Done when: the Fetch/XHR chip is selected.
4. Paste the conversation ID into the Network filter box, then reload the page with DevTools still open. Done when: one or a few requests matching the ID are listed.
5. Click the request whose path is `/backend-api/conversation/<id>`. Open its Response tab. Done when: a JSON body is visible.
6. Search the response body for `search_model_queries`. Expand `metadata`, then `search_model_queries`, then `queries`: those strings are the fan-out queries. Also search `search_queries` and read each object's `q` value. Done when: query strings are copied out, or "unavailable" is recorded.

The gotcha that wastes most attempts: typing a field name into the Network filter box filters request URLs, not response bodies. To search inside the response, use DevTools' search over response contents, or right-click the request, Copy response, paste into a text editor, then search there.

Field shapes (undocumented internals, checked September 2026, they change):

```json
{"metadata": {"search_model_queries": {"queries": ["CRM Gmail integration five users", "HubSpot vs Pipedrive Gmail integration"]}}}
{"metadata": {"search_queries": [{"q": "CRM Gmail integration five users"}]}}
```

Agent-assisted variant: with a live logged-in chatgpt.com session in a driven browser, hook `window.fetch` and `XMLHttpRequest` in the page console before sending the prompt, log conversation responses, then parse the saved payloads for the same two fields. Expect streaming chunks; only the completed message payload carries the metadata.

## Weaponize playbook

Given the captured query strings:

1. Cluster them: category ("best X for Y"), comparison ("X vs Y"), integration ("X with Gmail"), attribute ("X for 50 users"), navigational (brand named). Done when: every query sits in exactly one cluster.
2. Map each cluster to a target URL: category and attribute queries to an existing or new landing page, comparison queries to a dedicated vs page, integration queries to an integration or setup page. Done when: every cluster names a URL.
3. Place the exact query language: page title tag, URL slug, H1, first one or two sentences, repeated naturally through the body, and as an FAQ question. Observed query wording wins over prettier wording; do not paraphrase away the string you captured.
4. Publish social posts (LinkedIn, X) using the same query language, because answers pull from social and news results for recency.
5. Verify: rerun the same prompt in a fresh chat, check whether the target page now appears in the cited sources, and recapture to see whether the query set itself changed. Done when: either the citation appears, or a dated miss is recorded.
6. Keep a capture log per prompt: prompt text, date, model, observed queries, cited sources, target URL, outcome. Repeat a capture before betting on a pattern seen once.

## Honesty rules

- Observed is not generated. Asking ChatGPT "what did you search" returns suggestions, never a log. Only network metadata counts as observed.
- Absence proves nothing. No `search_model_queries` and no `search_queries` in the response means record "unavailable", then fall back to the cited sources. It does not mean no search ran.
- One response can hold multiple messages and regenerated branches. Associate each query with its message or turn; when you cannot, label it conversation-level instead of guessing.
- The same string appearing twice in one response is not two searches.
- The browser response is not a complete record of server-side search activity.

## Pitfalls

- Fresh or unsaved chats may not have a `/c/` URL yet. Send the prompt once, let it save, reload to get the ID, or watch new Fetch/XHR requests arrive live after sending.
- Streaming (SSE) splits payloads across events. Look for the completed message, not the first chunk.
- Browser only. The mobile app and the API expose nothing to inspect.
- Perplexity runs its searches server-side: you will see its own backend requests, not the underlying engine queries. Google AI Overviews expose nothing; infer from citations and label it as inference.
- Extensions that capture queries (for example ChatGPT Query Insight) show the same data but break whenever OpenAI changes internals. The manual method has no dependency to break beyond the field names, which the "unavailable" path already covers.
- The internal field paths are undocumented and change without notice. Treat the two names as a first guess, then read the surrounding metadata structure if both miss.

## Privacy

Before sharing any extract: strip unrelated chat text, personal details, cookies, and authorization headers. Never share an unreviewed HAR export.

## Verification

- A capture succeeded only if exact query strings were read from response metadata, or "unavailable" was recorded with the cited sources listed.
- A weaponize run succeeded only if placements are live at named URLs and a rerun prompt's citations were checked and logged.

## Sources

- getaiso.com/chatgpt-fan-out-queries: field formats and failure table
- link.sc/blog/how-to-see-what-ai-search-tools-actually-search-for: capture methods across engines
- OpenAI Help Center: "Searching the web with ChatGPT"
- Original manual method: Edward Sturm, YouTube Short x_LLGHec2d8, October 2026
