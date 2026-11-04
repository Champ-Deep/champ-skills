---
name: model-emitted-ui
description: Use when widening a model-emitted UI component library.
version: 1.0.0
license: AGPL-3.0
author: Deep
metadata:
  hermes:
    tags: [openui, generative-ui, 21stdev, components, chat]
    related_skills: [repo-design-probe-first, frontend-design]
---

# Widening a model-emitted UI component library

## When to Use

Any work where a chat model answers by emitting a component tree instead of
prose (OpenUI Lang in the Queryable-chatbot / DeepHQ toolkit stack): making a
new visual model-pickable, adopting a third-party (21st.dev) component into
the library, the model picking the wrong or too few components, or emitted
trees failing validation. Not for hand-built page or component UI
(frontend-design) or for deciding what the product should look like.

When a chat answers with a component tree rather than prose, the quality ceiling
is the component library: the model can only emit what the library declares.
Widening it is a curate-install-wrap-regenerate loop, never a runtime fetch.

## Procedure

1. **Find the library's source of truth before touching anything.** The
   backend's prompt and schema are generated from the frontend's library
   export (a script run by `npm run openui:assets`, output under
   `backend/openui/`). Never hand-edit the generated prompt or JSON: the next
   regeneration silently reverts it.

2. **Decide whether a needed visual already exists in the library.** Load the
   component list from `library.json` (or the frontend library object). Half of
   the requests are satisfied by components already declared, unused because
   the prompt's examples never show them.

3. **To add a component: install, then wrap, then declare.**
   - Install the third-party component through the registry already configured
     in `components.json` (21st.dev `@21st` registry in this stack), so its
     source lands in the repo and is reviewable.
   - Wrap it with `defineComponent` from `@openuidev/react-lang`: name, a
     `description` that tells the model WHEN to choose it, and Zod props with a
     `.describe()` per prop. The description is the model's only discovery
     channel; a component with a vague description never gets picked.
   - Register it in the library (`createLibrary` / the app's library object),
     then regenerate the backend assets and confirm the component name appears
     in both `library.json`'s component list and the prompt text.

4. **Check the app's styling stack first.** A Tailwind + shadcn component in an
   app styled with plain CSS renders as unstyled markup; verify the CSS pipeline
   (or restyle the wrapper into the app's own stylesheet) before adopting.

5. **Verify by rendering, not by compiling.** Ask the model a question the new
   component answers, confirm it emits it, and look at the rendered result.
   Compile-pass and schema-valid do not mean it renders.

6. **Grow the catalog on a schedule, not ad hoc.** A weekly worker card that
   searches the registry and proposes candidates keeps the library current;
   the frontend lane installs what is approved. Growth is a review loop with a
   human gate, so component choice never depends on whatever a registry returns
   mid-session.

## Pitfalls

- Never fetch and execute third-party component source at runtime: it is
  arbitrary code in the user's browser, it assumes a CSS toolchain that may not
  be present, and the model cannot be prompted about props it never sees.
- Keep an explicit never-fabricate rule in the library prompt. If an app
  replaces the stock rules, data blocks must be marked as data, not
  instructions, or the model will treat pasted content as commands.
- A shared, unscoped upload path in a multi-user product: a dataset or file
  endpoint written for admin use must gain per-user scoping before any outside
  user reaches it.
- An argument-heavy DSL breaks when optional positional args are skipped. If
  emitted trees fail validation, fix it in the prompt rules (show the exact
  argument order) rather than adding renderer tolerance.

## References
- `references/deephq-query-stack.md`: the DeepHQ toolkit and Queryable-chatbot
  wiring this skill was written against, with entry points and known gaps.
