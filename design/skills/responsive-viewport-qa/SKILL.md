---
name: responsive-viewport-qa
description: "Use when a built page must be checked at phone, tablet and laptop sizes."
license: MIT
---

# Responsive Viewport QA

Closing gate for any page or component that ships to a browser. Agents tune the laptop view and leave phones broken; this skill makes the check mechanical: screenshot every viewport, read the shots, fix, re-shoot.

Two lanes. Use the first if its tools are connected, else the second.

## Lane A: Responsively MCP (side-by-side devices)

Needs the Responsively App 2.0 (the MCP server is built in; the 1.x cask has none). Server name `responsively` in the profile config, shipped disabled until the app is installed.

Tools: `get_app_state`, `navigate`, `list_devices`, `set_active_devices`, `screenshot` (one or all devices, JPEG, max 1000px wide), `read_page`, `click`, `type_text`.

1. `set_active_devices` to a phone, a tablet and a laptop (for example 375, 768, 1440 wide).
2. `navigate` to the dev server URL, then `screenshot` all devices.
3. Open every shot. List each defect per device: overflow, clipped text, overlapping blocks, tap targets under 44px, nav that does not collapse.
4. Open menus and modals with `click`, then `screenshot` again. Menus break most often.
5. Fix the code, reload, re-shoot only the failing devices.

## Lane B: Playwright screenshots (works today, no app)

```bash
for w in 375x812 768x1024 1440x900; do
  npx -y playwright screenshot --viewport-size=${w/x/,} --full-page "$URL" "qa-$w.png"
done
```

Run on the nvm node (`/Users/deep/.nvm/versions/node/v24.13.1/bin` first on PATH). Open each PNG with `vision_analyze` and list defects as in Lane A. Menus and hover states need the browser tools or a Playwright script; the CLI only captures the loaded state.

## Done means

- Every viewport screenshot was opened, not assumed.
- Each reported defect has a before shot and an after shot at the same width.
- The final pass has zero horizontal scroll at 375 wide (`document.documentElement.scrollWidth <= innerWidth`).
- Hand the shots to `visual-verify` for the brand and contrast gate; this skill only covers fit.

## Pitfalls

- Full-page screenshots hide sticky and fixed elements that overlap content; check the first viewport separately.
- Responsively screenshots are downscaled; zoom with a crop before judging small type.
- A fix that works at 375 can break 768. Always re-shoot all widths after the last edit.
