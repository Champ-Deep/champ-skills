# Picking 21st.dev components when the twentyfirst MCP is not in the session

The planner config can carry the `twentyfirst` MCP block while the session exposes no
`mcp__twentyfirst__*` tool. Do not stop and do not source the key. The public site and
registry give everything the component table needs.

1. Search: open `https://21st.dev/community/components/s/<query-with-dashes>` in the browser
   tool and collect `a[href^="/@"]` links. Paths look like `/@<author>/components/<slug>` or
   `/@<author>/components/<slug>/<demoSlug>`.
2. Ids: the component page HTML carries `"id":<component id>,"demoId":<demo id>,` then an
   optional `"demoSlug":...`, then `"slug":"<slug>"`. Match on the exact slug: the first
   `"kind":"component"` record on the page is often an unrelated related-item. Sibling cards
   have quoted the demo id as "id", so write both columns.
3. Install address: `@21st/<author>/<slug>` (the demo segment is not part of it). Verify with
   `curl -s https://21st.dev/r/<author>/<slug>`: a 403 JSON `authentication_required` with a
   `component` record means it exists; no key needed for that check.
4. Preview: the page's iframe `src` on `cdn.21st.dev/.../bundle.*.html` is the live preview. It
   loads lazily; poll for it a few seconds. Open it directly, screenshot, `vision_analyze`.
   Click the trigger (pointerdown plus click) to see a menu's open state.
5. Fit check in the preview DOM before choosing: count hashed CSS-module classes
   (`/^_[A-Za-z]+_[0-9a-z]{4,}_\d+$/`) and hex literals. CSS-module components cannot take
   the project's tokens; heavy inline hex means a full tokenising pass. Reject or flag them.

The browser session can drop mid-loop (`no close frame received`): write results to a
workspace JSON after every component, not at the end.
