# Connector preflight

MCP tool names in this environment are prefixed with a server-specific ID that changes per install (e.g. `mcp__65e6b708-...__generate_image`), so don't hardcode a full tool name here. Instead, locate and check tools by capability.

## How to find the right tools

Use `ToolSearch` with a keyword for the capability you need, not a guessed tool name:
- `ToolSearch({query: "higgsfield image video generate", max_results: 15})` for creative generation.
- `ToolSearch({query: "zoom meeting search recording", max_results: 15})` for meeting history.

If the system prompt or an early system-reminder already lists deferred tools or servers-requiring-authentication, read that list first — it's faster than searching and tells you immediately whether a server is connected, deferred (connected but not yet loaded), or unauthenticated.

## What "connected" looks like vs. what "needs setup" looks like

- **Connected and loaded**: the tool appears directly in your active tool list. Use it.
- **Connected but deferred**: the tool name appears in a system-reminder as available via `ToolSearch` but its schema isn't loaded yet. Load it with `ToolSearch({query: "select:<exact_tool_name>"})` before calling it. This is normal and not a blocker.
- **Requires authentication**: a system-reminder explicitly lists the server under servers requiring authorization before use. This IS a blocker for anything that needs that server. Do not attempt the OAuth flow yourself (you can't, in a non-interactive session) and do not silently work around it. Tell the user which server needs authorizing and point them to claude.ai connector settings (for claude.ai connectors) or `claude mcp` / `/mcp` (for other MCP servers, in an interactive session).
- **Still connecting**: a system-reminder may say a server is "still connecting" — its tools aren't available yet but will be shortly. Call `ToolSearch` with a relevant keyword; it will wait for the server and search once available, rather than reporting it as missing.

## Preflight decision table

| Need | If connected | If unauthenticated | If absent entirely |
|---|---|---|---|
| Creative generation (Higgsfield or equivalent) | Proceed to Step 4 when the intake calls for images/video | Stop before intake; tell the user which connector to authorize and where; offer to proceed with research + playbook only in the meantime | Tell the user no image/video generation tool is available; offer research + playbook only, or ask if they want to connect one via the connector registry |
| Zoom meeting history | Use in Step 2 research | Note it in the research brief as unavailable; proceed without it, this is soft-optional | Same as above, soft-optional |
| Vault file read/write | Almost always available since it's the working directory | N/A | If writes fail, surface the actual error rather than assuming it's a permissions gate |

## The one thing to never do here

Never treat a missing or unauthenticated creative-generation connector as a reason to describe creatives in prose instead of generating them, or to hand-draw an approximation. If the tool isn't available, say so and stop that part of the work. Half-measures that look like a deliverable but aren't (a text description formatted to look like a creative brief, a placeholder image) waste the user's time worse than an honest "this needs to be connected first."
