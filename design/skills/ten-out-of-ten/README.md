# /ten-out-of-ten

A Claude Code skill that takes any website, scores it out of 10, and rebuilds it into a 10/10: real proof near the top, one clear call to action, a design that doesn't look AI-made, works on a phone, and can be found by ChatGPT. Then it walks you through putting it live on GitHub, Vercel and your domain.

## Install (2 minutes)

1. Unzip `ten-out-of-ten.zip`. You get a folder called `ten-out-of-ten`.
2. Move that folder into your Claude Code skills folder:
   - **Mac / Linux:** `~/.claude/skills/` (in Finder: Cmd+Shift+G, paste `~/.claude/skills`; create the folder if it isn't there)
   - **Windows:** `C:\Users\<you>\.claude\skills\`

   Or from the Terminal on a Mac, in one line:
   ```
   mkdir -p ~/.claude/skills && unzip ~/Downloads/ten-out-of-ten.zip -d ~/.claude/skills/
   ```
3. Restart Claude Code.

Easiest of all: open Claude Code and say *"install the skill in ~/Downloads/ten-out-of-ten.zip"*.

## Use it

1. Make a new empty folder for the new site and open Claude Code in it.
2. Use the best model you have (built and tested on **Opus 5.5**, high effort).
3. Run:
   ```
   /ten-out-of-ten https://your-website.com
   ```

The first run checks your setup: the design skills, Mobbin, 21st.dev, Chrome for screenshots. Anything missing, it offers to install with you one at a time and walks you through any API keys (keys never go in the chat). Everything except Node, git and Chrome is optional; it works with what you have.

## What it does

0. Checks your setup
1. Reads your whole site: every number, testimonial, logo, photo and video
2. Scores it out of 10 on checks you can actually verify
3. Applies taste rules that ban the "AI website" look
4. Drafts five directions for you to pick from, then builds a design system
5. Pulls real references (Mobbin, Godly, Awwwards, real brand design systems)
6. Builds it to convert: proof near the top, how it works shown not told, real results as cards
7. (Optional) generated imagery, only for physical businesses, priced before anything's spent
8. Phone and speed pass, scrolled frame by frame
9. AI visibility: llms.txt, schema, robots so ChatGPT can read and cite you
10. Scores it again, same test
11. Walks you through GitHub, Vercel and your domain

It never invents stats, testimonials or logos. If your site has no proof yet, it tells you what to collect instead of faking it.
