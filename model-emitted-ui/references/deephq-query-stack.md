# DeepHQ toolkit and Queryable-chatbot wiring

Entry points probed for a "chat with your file" feature. Read before designing
anything that chains Workbench, Enrich, and a query tool; re-verify the line
numbers, they drift.

## Toolkit: ~/repos/dh-workbench-v5 (deependhq.com)

- Cloudflare Worker + D1 + R2, Clerk auth, credit ledger. User files live in
  R2, rows in D1 (`migrations/0001_toolkit.sql`: `files`, `toolkit_runs`,
  `toolkit_ops`, `ai_log`; later migrations add `job_id`).
- Routes dispatch in `worker/index.js` (~L557 and ~L619) into
  `worker/toolkit.js` (route table ~L1159-1195: `/api/toolkit`, `/config`,
  `/webhook`, `/files/<id>`), with `worker/toolkit-files.js` and
  `worker/toolkit-store.js` behind them. 32 MB request cap on POST actions.
- Client: `toolkit-workbench-lib.js`, `toolkit-desktop.js`, `enrich-core.js`.
  Workbench (six stages) and Deep Enrich are the two existing tools.
- `WORKERS.md` documents the site's other endpoints and required secrets.

## Queryable chatbot: ~/repos/Queryable-chatbot (Veeresh-champ)

- FastAPI + Mongo, OpenUI Lang rendering (`@openuidev/*`), Jev router for
  natural language to validated read-only query. Frontend `openui_test/`.
- Dataset upload already exists: `backend/data_catalog.py` (`preview`,
  `upload`, Excel/CSV parse plus type inference), admin-only. Datasets are
  GLOBAL Mongo collections with no per-user scoping: that gap must close
  before any outside user can upload.
- OpenUI assets are generated from the frontend library:
  `openui_test/scripts/generate-openui-assets.mjs` (run
  `npm run openui:assets`) writes `backend/openui/system_prompt.txt` and
  `library.json` (component names plus JSON schema, 84 stock components). The
  script also rewrites the stock rules (never fabricate numbers, data blocks
  are not instructions) and chooses which examples ship.
- Rendering: `openui_test/src/components/cloud-chat.tsx` passes
  `componentLibrary={openuiChatLibrary}` plus a `components` override map.
- 21st.dev registry already wired: `openui_test/components.json`
  (`registries['@21st']`, keyed on `TWENTY_FIRST_API_KEY`).
  `src/components/embed-launcher.tsx` is an adapted 21st.dev component,
  restyled into `app/brand.css` because this app does not run Tailwind.
- Brand editions (Lake, SPAN) are build-time themes in `src/lib/brand.ts`;
  `docs/ui-brief-brand-editions-v1.md` shows the one-brief-per-edition pattern.
- Query context: Mongo schema profile plus overview rows are pushed into the
  prompt (`backend/hr_analytics.py`, `insights.py`), so the model can only
  invent columns the schema does not back.

## Open decision on the chain

How a toolkit file reaches the chatbot (hand its R2 object to the chatbot
upload endpoint under a per-user Mongo database) and what each query costs
live on a decision card, not in code.
