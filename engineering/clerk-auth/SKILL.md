---
name: clerk-auth
description: >-
  Add Clerk authentication (sign-in, sign-up, user accounts, protected routes)
  to any web project. Use this skill whenever the user wants to add auth, add
  login, add sign-in, gate a tool behind accounts, "put this behind a login",
  add user management, or wire up Clerk to a React/Vite or Next.js app. Also
  trigger on "add Clerk", "set up authentication", "make this require login",
  "add accounts to [tool]", or when retrofitting auth onto an existing
  Champions Group internal tool (ChampUTM, ChampLens, LakeStream, Event Scout,
  ChampCMS, the affiliate portals, dashboards, and similar). Use it even if the
  user only says "add auth" without naming Clerk. This is the standard,
  repeatable way auth gets added to Champions Group projects.
---

# Clerk Auth

A repeatable playbook for bolting Clerk authentication onto any web project,
new or existing. The goal is that adding auth becomes a 15-minute, low-thought
task instead of a research project every time.

This skill was built off the pattern already used on **ChampUTM** and
**ChampLens**. Follow it and every Champions Group tool ends up with the same
auth shape, the same env var conventions, and the same deploy story.

## What "done" looks like

A working project where: unauthenticated visitors can sign up and sign in,
signed-in users see a profile/avatar button, and the routes that should be
private actually reject anonymous users. Keys live in environment variables,
never in committed code. The deploy target (Vercel/Netlify) has the same keys
set so production works too.

## Step 0: Detect the framework before doing anything

Clerk's integration differs by framework, and guessing wrong wastes a round
trip. Inspect the repo first:

1. Read `package.json`. Look at `dependencies`.
2. Classify:
   - `next` present → **Next.js**. Then check for an `app/` directory (App
     Router) versus a `pages/` directory (Pages Router). App Router is the
     default for anything recent.
   - `vite` present and `react` present, no `next` → **React + Vite**.
   - `react` present, no `vite`, no `next` (e.g. Create React App) → treat as
     **React + Vite** steps; the only difference is the env var prefix (CRA
     uses `REACT_APP_`). Flag this to the user.
   - A Python backend only (`requirements.txt`, FastAPI, no frontend) → see
     the "Python / backend APIs" section below.
3. State what you detected in one line, then load the matching reference file.

| Detected stack | Reference file |
|---|---|
| React + Vite (or CRA) | `references/react-vite.md` |
| Next.js App Router | `references/nextjs-app-router.md` |
| Next.js Pages Router | `references/nextjs-pages-router.md` |
| Python / FastAPI backend | section below + `references/nextjs-app-router.md` for token notes |

Do not load all reference files. Load only the one that matches. Each file is
a complete, self-contained walkthrough with copy-pasteable code.

## Step 1: The Clerk dashboard (the one manual part)

Clerk needs an application created in its dashboard before any code works.
This part the user must do, because it requires their Clerk login. Give them
exactly these instructions, then wait:

1. Go to `dashboard.clerk.com` and create a new application (or pick an
   existing one if this tool should share a user base with another).
2. Choose the sign-in methods. Email + Google is the sensible default for
   Champions Group internal tools. Confirm with the user if unsure.
3. From the application's **API keys** page, copy two values:
   - the **Publishable key** (starts with `pk_`)
   - the **Secret key** (starts with `sk_`) — only needed for Next.js and
     backends, not for a pure React/Vite SPA.
4. Have the user paste those keys into the chat, or set them in the env file
   themselves. Never commit them.

If the user already has a Clerk app for a sibling tool and wants shared
accounts, reuse its keys instead of creating a new application.

## Step 2: Follow the reference file

Open the framework reference file from the table above and execute it
top to bottom. Every reference file follows the same five-part shape so the
process feels identical regardless of stack:

1. Install the Clerk SDK.
2. Set environment variables (and `.gitignore` them).
3. Wrap the app in `<ClerkProvider>`.
4. Add sign-in / sign-up / user-button UI.
5. Protect the routes that should be private.

## Champions Group conventions

These keep every tool consistent. Apply them on top of whatever the reference
file says.

**Environment variable names.** Use Clerk's standard names so the reference
code works unchanged: `VITE_CLERK_PUBLISHABLE_KEY` for Vite,
`NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` + `CLERK_SECRET_KEY` for Next.js. Do not
invent custom names.

**Env files.** Put real keys in `.env.local`. Commit a `.env.example` with the
key names and empty values so the next person knows what to set. Confirm
`.env.local` and `.env*.local` are in `.gitignore` before finishing. If they
are not, add them. Leaked Clerk secret keys are a real incident, not a
hypothetical.

**Deploy targets.** A tool that works locally but 500s in production almost
always has missing env vars on the host. After the code works locally, remind
the user to add the same keys in the deploy dashboard:
- Vercel: Project → Settings → Environment Variables.
- Netlify: Site configuration → Environment variables.
Set them for all environments (production + preview). Then trigger a redeploy,
because env var changes do not apply to existing builds.

**Shared vs separate user pools.** Each Clerk application is its own user
directory. Two tools using the same Clerk app share accounts; two tools with
separate apps do not. Decide deliberately. Internal team tools that the same
people use (ChampUTM, ChampLens, dashboards) are good candidates for one
shared Clerk app. Ask the user if it is not obvious.

## Python / backend APIs

Several team tools have Python backends (LakeStream, the five-level email
personalizer, ChampIQ services). Clerk secures the frontend; the backend's job
is to verify the session token the frontend sends.

The short version: the React/Next frontend gets a session token from Clerk
(`useAuth().getToken()`), sends it as a `Bearer` token on API calls, and the
Python backend verifies it. Use Clerk's official Python SDK
(`clerk-backend-api`) or verify the JWT against Clerk's JWKS endpoint. Full
backend verification is its own task; for most internal tools, protecting the
frontend routes is enough to start. Flag to the user whether they need
backend enforcement too (they do if the API is reachable directly, not just
through the protected UI).

## Verification before you call it done

Do not claim success without checking. Run through this:

1. The dev server starts with no Clerk-related console errors.
2. Visiting a protected route while signed out redirects to sign-in (or shows
   the signed-out UI), not the protected content.
3. Sign-up works, then the user lands signed-in and the `<UserButton>` /
   avatar appears.
4. Sign-out returns to the signed-out state.
5. `git status` shows no `.env.local` staged. Grep the diff for `pk_` and
   `sk_` to be certain no key is about to be committed.
6. If deploying: the deploy dashboard has the keys set.

Report what you verified, not just what you wrote.

## Which team tools this applies to

`references/champ-tools.md` lists the Champions Group tools, their stack, and
current auth status. Read it when the user says "do this for [tool]" or asks
which tools still need auth. ChampUTM and ChampLens already have Clerk; the
rest of the internal web tools are candidates.
