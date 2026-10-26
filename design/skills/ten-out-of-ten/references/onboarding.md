# Setup check (step 0)

Run the check, show the table, then fix what's missing with the user's OK, one item at a time.

## 1. Run the check

```bash
ok() { printf '%-28s %s\n' "$1" "$2"; }
has_skill() { for d in "$HOME/.claude/skills/$1" "./.claude/skills/$1"; do [ -f "$d/SKILL.md" ] && return 0; done; find "$HOME/.claude/plugins/cache" -maxdepth 7 -type d -name "$1" 2>/dev/null | grep -q .; }
v=$(node -v 2>/dev/null | tr -d v | cut -d. -f1); [ -n "$v" ] && [ "$v" -ge 18 ] && ok "Node 18+" "✅ $(node -v)" || ok "Node 18+" "❌"
git --version >/dev/null 2>&1 && ok "git" "✅" || ok "git" "❌"
{ [ -d "/Applications/Google Chrome.app" ] || command -v google-chrome chromium chromium-browser >/dev/null 2>&1; } && ok "Chrome (screenshots)" "✅" || ok "Chrome (screenshots)" "❌"
for s in ui-ux-pro-max design-taste-frontend impeccable emil-design-eng web-design-guidelines; do has_skill "$s" && ok "skill: $s" "✅" || ok "skill: $s" ", "; done
command -v gh >/dev/null 2>&1 && ok "GitHub CLI (optional)" "✅" || ok "GitHub CLI (optional)" ", "
claude mcp list 2>/dev/null | grep -iE "mobbin|magic|21st|higgsfield" || echo "no design connectors found by 'claude mcp list'"
```

Then check your own tools for the rest: an **Artifact** tool that lists a "Design System" type (Claude Design), **Mobbin** tools, **21st.dev Magic** tools, **Higgsfield** tools. A connector that's listed but fails to connect (expired key, not signed in) counts as missing.

Show the result as one table: ✅ ready, ❌ required and missing,, optional and missing (with what happens without it).

## 2. What's needed

| Item | Needed? | Without it |
|---|---|---|
| Node 18+, git | Required | Can't build |
| Chrome / Chromium | Required | Can't screenshot, so can't score or QA |
| Claude Code on Opus 5.5 | Strongly recommended | Smaller models lose the thread on a whole site; tell the user to switch with `/model` |
| ui-ux-pro-max | Recommended | Use `taste.md` alone for type and palette direction |
| Taste (`design-taste-frontend`) | Recommended | `taste.md` is the floor anyway |
| Impeccable | Recommended | Skip its audit/critique; do the QA pass by hand |
| Emil Kowalski (`emil-design-eng`) | Optional | Follow `taste.md` § Motion |
| Vercel `web-design-guidelines` | Optional | Skip the code review pass |
| Mobbin connector | Recommended | Use Godly, Awwwards and competitor sites as references |
| 21st.dev Magic connector | Optional | Use the "Copy prompt" button on 21st.dev, or build components by hand |
| Claude Design (Artifacts) | Optional | `_brand/DESIGN.md` is the design system |
| Higgsfield | Optional, paid | No generated imagery (usually the right call) |
| GitHub account (+ `gh`) | Step 11 only | Create the repo on github.com instead |
| Vercel account | Step 11 only | Sign up at vercel.com with GitHub when shipping |

## 3. Installing (ask before each one)

Run an install only after the user says yes to it. Commands that start with `/` are typed by the user inside Claude Code; you can't run them for them.

- **ui-ux-pro-max:** the user types `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill`, then `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill`.
- **Taste:** `npx skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend`
- **Emil Kowalski:** `npx skills add https://github.com/emilkowalski/skills --skill emil-design-eng`
- **Vercel guidelines:** `npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines`
- **Impeccable** (inside the project folder, so its hooks only run there): `npx impeccable install --providers=claude --scope=project`, then the user types `/impeccable init`.
- **Mobbin:** `claude mcp add --transport http --scope user mobbin https://api.mobbin.com/mcp`, then the user types `/mcp`, picks mobbin and signs in with their Mobbin account.
- **21st.dev Magic:** see API keys below.
- **GitHub CLI:** `brew install gh` (macOS), then the user runs `gh auth login`.

If `npx skills add` asks interactive questions, have the user run it in their own terminal and pick Claude Code.

## 4. API keys

Keys never go through the chat. Tell the user where to get the key and give them the command with a placeholder to run in their own terminal:

- **21st.dev:** easiest is the hosted connector: add `https://21st.dev/api/mcp` as a custom connector in claude.ai (Settings → Connectors), sign in, and it shows up in Claude Code too. Or the local version: get a key at https://21st.dev/mcp, then run
  `claude mcp add magic --scope user --env API_KEY=<your key> -- npx -y @21st-dev/magic@latest`
  Either one is enough. If both are set up and one fails, use the one that's connected.

If a user pastes a key into the chat anyway: don't repeat it, don't write it into any project file, and suggest they rotate it if the screen is being recorded or shared. Never commit keys; check before any push.

## 5. After installing

Connectors and plugins load when Claude Code starts. If anything was added, tell the user to restart Claude Code and run `/ten-out-of-ten <url>` again. The setup check then passes in seconds, and the run starts.
