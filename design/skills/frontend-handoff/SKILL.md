---
name: frontend-handoff
description: "Turns a backend into a frontend. Ingests routes, endpoints, schemas, auth, roles, and error codes from OpenAPI, Postman, a route file, source code, or live Supabase introspection, maps every backend capability to screens, journeys, and UI states, then writes a design brief that routes into design-trends and frontend-design so the result is a considered product rather than a default CRUD admin panel. MANDATORY TRIGGER for: 'frontend handoff', 'backend handoff', 'here are our routes', 'here are our endpoints', 'map the backend', 'what screens do we need', 'turn this API into a UI', 'build the frontend for this', 'spec the frontend', 'endpoint to screen mapping', 'what does the frontend need from us', 'the backend is done', 'design the UI for this API', 'what states do we need to design', 'swagger', 'OpenAPI', 'Postman collection'. Use whenever backend work is done or in progress and someone needs the interface designed on top of it. Full triggers in assets/triggers.md."
---

# Frontend Handoff

Takes what the backend team has built and turns it into something a frontend designer or builder can act on: every route mapped, every screen derived, every state enumerated, and a design brief that gives the frontend a real point of view.

This skill runs in the opposite direction to `design-trends`. That one goes design to developer. This one goes **backend to frontend design**, and then hands to `design-trends` to make the result good rather than merely correct.

---

## The problem this solves

A backend engineer hands over a list of endpoints. It is complete, accurate, and almost useless, because **a route list is not a product.**

Backends are organised around resources and verbs. Frontends are organised around tasks and moments. The two do not line up:

- One screen usually needs three to six endpoints.
- One endpoint often serves four different screens, showing different fields each time.
- The most important frontend work, the empty states, the error states, the loading behaviour, the permission variations, is entirely invisible in a route list even though the backend already knows every one of them.

So the output of a good handoff is not a tidier route list. It is a **translation**, plus the three things backends know and never think to send: error taxonomy, latency profile, and realistic data extremes.

**The failure this prevents.** Given a bare route list, any competent builder produces the same thing: a sidebar, a table per resource, a modal per create action. It works. It is also the default CRUD admin panel that looks like every other one, and it is the exact "vibe coded, no point of view" failure that `design-trends` Mode B exists to diagnose. Preventing it costs one extra document, written here.

---

## The four steps

| Step | What happens | Output |
|---|---|---|
| 1 | **Inventory.** Capture or introspect the backend surface. | `BACKEND-MAP.md` |
| 2 | **Translate.** Derive screens, journeys, and states from the surface. | `SCREEN-MAP.md` |
| 3 | **Brief.** Give the frontend a design perspective, not a spec to obey. | `FRONTEND-BRIEF.md` |
| 4 | **Verify and hand over.** Block on gaps, list open questions. | Gap list, fixtures |

Steps 1 and 2 are mechanical and should be thorough. Step 3 is where the judgement lives.

---

## Step 1: Inventory the backend

Read `reference/backend-inventory.md` for the full capture spec. Fill `assets/BACKEND-MAP-template.md`.

### Introspect before asking

Do not send a questionnaire if the answer is already machine-readable. In order of preference:

1. **Supabase MCP connected.** Use `list_tables` for schema and relationships, `list_edge_functions` for custom endpoints, `generate_typescript_types` for exact shapes, `get_advisors` for security and performance notes, and `list_migrations` for what changed recently. This produces most of the map with no human effort, and it is the fastest path for any Champions Group tool already on Supabase.
2. **OpenAPI or Swagger spec.** Parse it. It carries paths, methods, request and response schemas, auth, and often error codes.
3. **Postman collection.** Parse it. Weaker on schemas, stronger on realistic example payloads, which are useful in Step 2.
4. **Source code.** Read the router or route definitions directly.
5. **Prose from the engineer.** Structure whatever they wrote, then run the gap check.

Whatever the source, the map must end up capturing per endpoint: method, path, purpose in one line, auth requirement, roles permitted, request shape, response shape, **every error code with its meaning**, pagination, latency profile, and whether writes are idempotent.

### The three fields backends always omit

These are the highest-value part of the inventory and they are almost never volunteered. Ask for them explicitly.

1. **Error taxonomy.** Every non-200 the endpoint can return, what causes it, and whether the user can do anything about it. The frontend has to design a message for each one, and "Something went wrong" for all of them is how products feel cheap.
2. **Latency profile.** p50 and p95 per endpoint. This decides the interaction pattern outright: under 100ms needs no spinner, 100ms to 1s needs a skeleton, over 1s needs optimistic UI or a progress affordance, over 10s needs a job queue and a notification rather than a screen that waits.
3. **Data extremes.** The longest string a field actually holds, the largest array, how many items a heavy account has, which fields are genuinely null in production. Layouts break on real data, never on lorem.

---

## Step 2: Translate to screens and states

Read `reference/translation.md`. Fill `assets/SCREEN-MAP-template.md`.

### Endpoint to screen matrix

Build the grid. Endpoints down the side, screens across the top, marked by how each screen uses each endpoint (read, write, poll, prefetch).

The matrix immediately surfaces three things that a route list hides:
- **Orphan endpoints** that no screen uses. Either a screen is missing or the endpoint is dead.
- **Overloaded screens** pulling from eight endpoints, which is a loading-sequence problem and usually a scope problem.
- **Shared endpoints** whose response shape must satisfy several screens at once, which is where field-level negotiation with the backend belongs.

### Derive states mechanically

Every endpoint a screen touches contributes states. Enumerate rather than improvise:

**Read endpoints:** loading (first load), loading (refetch, different treatment), empty, partial or paginated, full, stale, error per code, forbidden for this role.

**Write endpoints:** idle, validating, submitting, optimistic pending, success, conflict, validation error per field, server error, offline queued.

A screen's real complexity is the product of these, not the count of its endpoints. This enumeration is the single most valuable artefact for the frontend builder, and it is why handoffs done this way do not generate a stream of "what happens if" questions two weeks later.

### Data shape drives layout

A rule that converts schema facts into design constraints:

| Schema fact | Design consequence |
|---|---|
| String field, no length cap | Design truncation and the full-value affordance now |
| Nullable field | It needs a designed empty treatment, not a blank gap |
| Enum field | A designed badge or state set, one per value, including any future-proofing |
| Array field, unbounded | Needs a count, a cap, and an overflow pattern |
| Timestamp | Needs a format decision and a relative-time rule |
| Money or quantity | Needs alignment, tabular numerals, and a currency or unit rule |
| Foreign key | Implies a link, a hover preview, or an embedded summary. Decide which. |

### Permissions produce variants, not just hiding

Build the role matrix. For each role, per screen: what is visible, what is enabled, what is hidden entirely.

Two rules that keep this honest. Hiding a control is a UX courtesy, never a security measure, and the server rejects regardless. And a role that can see but not act needs a designed explanation of why, otherwise the interface reads as broken to the person with the least power in the system.

---

## Step 3: Write the frontend brief

Read `reference/design-brief.md`. Fill `assets/FRONTEND-BRIEF-template.md`.

**This is the step that stops the output being a CRUD panel.** Steps 1 and 2 describe what the software can do. This step decides what it should feel like to use, and it is deliberately written as a perspective to react to rather than a specification to obey.

The brief carries:

1. **Who uses this, and what room are they in.** The logo-cover test from `design-trends` applies here too. If the answer is "a user," go back and find out.
2. **The primary job.** The one task that, done well, makes the product worth opening. Everything else is secondary and should look secondary.
3. **The product archetype.** Is this a dashboard someone lives in for eight hours, a tool used for ninety seconds a week, a monitor watched passively, or a workflow run once a quarter? Each implies a completely different density, navigation, and motion posture. Get this wrong and every later decision is wrong.
4. **Two or three design directions**, each with a stated trade-off, so the frontend designer chooses rather than complies. Never one direction. One direction is an instruction wearing a brief's clothing.
5. **The trend routing.** Which `design-trends` mode applies and which trends fit this audience and archetype.
6. **Constraints that are real**, separated from preferences that are negotiable. Frontend designers work far better when they know which is which.

Then hand to `design-trends` and `frontend-design`. This skill produces the brief. Those skills produce the design.

---

## Step 4: Verify, then block on gaps

Run `assets/intake-questions.md` against the map. **Do not paper over gaps with assumptions.** An assumed field type or an invented error message costs more to unwind than the day it takes to get an answer.

Classify every gap:

- **Blocking.** The frontend cannot start. Auth model, primary entities, the core write path. Stop and ask.
- **Deferrable.** Work can begin with a stated placeholder. Exact error copy, pagination limits, sort defaults. Record the placeholder in the brief so it gets revisited rather than shipped.
- **Frontend's call.** Not a backend question at all. Say so explicitly, because backend engineers often over-specify presentation and under-specify semantics.

### Fixtures beat descriptions

Ask the backend for a seed fixture set rather than a description of the data, covering: a typical record, the longest and largest realistic record, a record with every nullable field null, an empty account, and one saved response body per error code.

This is a small ask that removes an enormous amount of back and forth, and it is the difference between a layout that survives production and one that breaks the first week.

---

## Working with the rest of the pipeline

| Skill | Relationship |
|---|---|
| `design-trends` | Receives the brief. Decides trend or identity direction, then does the design handoff back to the builder. |
| `frontend-design` | Receives the brief and the screen map. Builds structure and DESIGN.md. |
| `ui-polish` | Phase 2 on the built result. |
| `clerk-auth` | If auth is Clerk, the role matrix and protected-route list feed straight into it. |
| `frontend-resiliency-tester` | The state enumeration from Step 2 becomes the test matrix. Hand it over directly. |
| `engineering:architecture` | If the backend contract itself looks wrong, that is an ADR conversation, not a frontend workaround. Say so. |

**Order for a full build:** `frontend-handoff` → `frontend-design` → `ui-polish` → `design-trends` → `frontend-resiliency-tester`.

---

## Definition of done

- [ ] Every endpoint inventoried with method, path, auth, roles, request, response, errors, pagination, latency, idempotency.
- [ ] Error taxonomy complete. Every code has a cause and a user-facing consequence.
- [ ] Latency profile captured per endpoint, with the interaction pattern it implies.
- [ ] Data extremes documented. Longest string, largest array, genuinely nullable fields.
- [ ] Endpoint-to-screen matrix built. No orphan endpoints, no unexplained eight-endpoint screens.
- [ ] Every screen has its full state list enumerated, not improvised.
- [ ] Every nullable field has a designed empty treatment. Every enum has a designed value set.
- [ ] Role matrix complete. Visible, enabled, and hidden defined per role.
- [ ] Product archetype named, and the primary job stated in one sentence.
- [ ] Two or three design directions offered with trade-offs, never one.
- [ ] `design-trends` mode and trend selection recommended.
- [ ] Real constraints separated from negotiable preferences.
- [ ] Gaps classified as blocking, deferrable, or frontend's call. Blocking gaps escalated, not assumed.
- [ ] Fixture set requested or produced.
- [ ] No em dashes anywhere in the copy.

---

## Files

| File | Use |
|---|---|
| `reference/backend-inventory.md` | Capture and introspection spec, including Supabase MCP, OpenAPI, and code paths. |
| `reference/translation.md` | Endpoint-to-screen matrix, state derivation, data-shape rules, permission variants. |
| `reference/design-brief.md` | How to write a perspective brief, archetypes, direction options, trend routing. |
| `assets/BACKEND-MAP-template.md` | Fill-in backend inventory. |
| `assets/SCREEN-MAP-template.md` | Fill-in screen, journey, and state map. |
| `assets/FRONTEND-BRIEF-template.md` | Fill-in design brief for the frontend team. |
| `assets/intake-questions.md` | Blocking question set to run against any incomplete handoff. |
| `assets/triggers.md` | Complete trigger phrase list. |
