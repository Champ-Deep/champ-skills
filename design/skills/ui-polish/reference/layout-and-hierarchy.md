# Pillar 2: Layout and Information Hierarchy

Once the surface looks intentional, fix where things live. AI builds tend to expose everything at once: a sidebar with every route, a bare avatar circle, and cards loaded with competing buttons. Hierarchy is the discipline of deciding what is primary and hiding the rest until it is needed.

## Contents
- Consolidate navigation
- The account card
- Card optimization

---

## Consolidate navigation

A sidebar is not a sitemap. It is the set of places a person goes constantly. When it lists eleven items including custom domains, teams, integrations, and webhooks, the genuinely frequent destinations get lost.

**Target 5 to 7 primary destinations.** Everything else moves:
- **Secondary settings** (custom domains, team, billing, API keys, webhooks) go behind a Settings tab or section, not the top-level rail.
- **Infrequent power features** go behind a disclosure ("More") or a command palette.
- **Workspace and account switching** belong in the account card (below), not as sidebar rows.

How to decide what stays: if a user touches it on most sessions, it earns a top-level slot. If it is a configure-once item, it belongs in settings. When unsure, look at which routes carry daily traffic and promote those.

The result is a rail that feels calm and obvious. A person should be able to name what each item does without reading twice.

---

## The account card

The default AI pattern is a gradient circle with initials, floating in the corner doing nothing useful. Replace it with a real **account card**: a popover anchored to the avatar that tucks away the secondary surface of the app.

A good account card contains, in order:
1. **Identity block.** Avatar, name, email or workspace, all in the popover header so the chrome stays clean.
2. **Workspace or team switcher** if the product is multi-tenant.
3. **Account links.** Settings, Billing, Team, API or Integrations.
4. **Support and meta.** Help, docs, changelog, keyboard shortcuts.
5. **Sign out**, visually separated at the bottom.

Why this is better: it removes four or five rows from the sidebar, it gives billing and settings a consistent home, and it matches the mental model every mature SaaS has trained users on. The avatar becomes a real control instead of decoration.

A styled account-card popover is in `assets/snippets.html`.

---

## Card optimization

List and grid cards are where visual noise accumulates. A link row that shows the URL, three full buttons (Copy, Edit, Delete, Stats), a date string, and two colored text chips is fighting itself. Calm it down.

The moves:
- **Collapse actions into a kebab menu.** One triple-dot button opens Copy, Edit, QR, Delete, and the rest. Keep at most one inline quick-action (often Copy) if it is used constantly. This alone removes most of the clutter.
- **Center and quiet the dates.** A created or updated date should be secondary: smaller, muted, and aligned consistently (often centered in its column) so it never competes with the title.
- **Icons with tooltips instead of text chips.** A globe icon for the destination domain, a lock for password protection, a clock for expiry. Each carries the same meaning as a text chip in a fraction of the width, with a tooltip for the full label.
- **One strong title, everything else subordinate.** The short link or the name is the hero of the row. Destination URL, tags, and metadata sit beneath it in muted type.
- **Consistent column rhythm.** Align the same fields to the same positions across every row so the eye can scan a single vertical line for clicks, for date, for actions.

The principle underneath all of this: a card should have one clear focal point and a predictable place for everything else. Buttons and chips are the usual offenders because each one demands attention. Demote them.

An optimized list card with a kebab menu, icon-plus-tooltip metadata, and a quiet centered date is in `assets/snippets.html`.

---

## Quick wins, in order
1. Cut the sidebar to 5 to 7 items, move settings-type routes into a Settings area.
2. Replace the avatar circle with the account-card popover and relocate billing, team, and links into it.
3. Collapse per-row buttons into a kebab menu, keeping at most one inline quick-action.
4. Swap text chips for icon-plus-tooltip, quiet the dates, lock column alignment.
