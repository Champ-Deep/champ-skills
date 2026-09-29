---
name: anniversary-gift
description: Build a personalized, single-file HTML gift page for a work anniversary or birthday. Use this skill whenever someone wants to create a digital gift for a colleague, employee, or team member — whether for a work anniversary, birthday, retirement, or milestone. MANDATORY TRIGGER for: "anniversary gift", "birthday page", "make a gift for", "personalized gift for [name]", "create something special for [person]", "milestone gift", "tribute page for [name]", "work anniversary for [name]", or any request to build a meaningful HTML experience for a specific person. Also trigger when a name + years of service + occasion appear in the same message. The output is a standalone HTML file: no build tools, no dependencies, no server required.
---

# Anniversary Gift Skill

Build a deeply personal, single-file HTML gift page for a specific person's work anniversary, birthday, or milestone. The goal is something that feels like it was made *for them* — not a branded template with their name dropped in.

The Sundar Raj 23-year anniversary page is the reference implementation. Read it if you need structural or code patterns: `/sessions/friendly-quirky-allen/mnt/Celsus/sundar-raj-23-years.html`

---

## Philosophy

**Personalization is the whole point.** Generic-looking pages are a miss. The design, color, tone, quiz content, and story visual should feel like they could only be about this specific person.

- Someone who loves cricket and data gets different imagery than someone who leads yoga retreats.
- A warm, earthy palette for a nature person. Clean blues for a tech architect.
- Quiz questions that only people who actually know this person could answer.

If the intake data is thin, push back gently and ask for more. One good personal detail is worth ten generic facts.

---

## Phase 1: Intake Interview

Before writing a single line of HTML, collect the following. Use `AskUserQuestion` if confidence is below 80%. Otherwise state your assumptions and proceed.

### Required

| Field | What to collect |
|-------|----------------|
| **Person's name** | Full name and any nickname they go by |
| **Occasion** | Work anniversary (N years), birthday (age optional), retirement, milestone |
| **Role and company** | Current title and where they work |
| **3-5 defining traits** | How colleagues would describe this person in a meeting. Think adjectives + a signature behavior. |
| **Sender** | Who is gifting this? Name and/or company. Default: [[Champions Group]], from [[Sreedeep Surapaneni|Sreedeep]] |

### Strongly recommended (push for these)

| Field | Why it matters |
|-------|----------------|
| **A personal memory or story** | Powers the tribute section and optional visual. One specific moment beats a general impression. |
| **Hobbies and interests** | Used for the story visual if no specific memory exists, and for quiz questions |
| **Something they are known for** | The thing everyone says about them. Their signature. |
| **A funny or affectionate quirk** | Makes quiz options feel alive instead of generic |
| **LinkedIn URL or social handle** | Used to research quiz questions. Ask if sender can share. |

### Optional

| Field | Notes |
|-------|-------|
| **Supabase project URL + anon key** | Only needed if the sender wants a persistent guestbook or quiz score leaderboard. Do not require this. |
| **Brand [[colors]]** | If sender has specific brand [[colors]] they want to use. Otherwise pick palette from person's personality. |
| **Deployment preference** | Local file only, or does sender want to deploy? Suggest Netlify at the end regardless. |

### Asking about the personal story visual

This is optional but strongly encouraged. Prompt the sender:

> "Is there a specific shared memory, trip, challenge, or moment with this person that we could turn into a little illustrated story? Even something simple — a trip they took, a presentation they saved, a time they went above and beyond — works great here. If not, I can build something around their known interests."

If they give a memory: build the visual around that memory (SVG illustration, path animation, or similar).  
If they don't: build around their strongest hobby or interest (sports, nature, music, technology, etc.).  
If interests are also unclear: skip the visual and use a strong typographic tribute instead.

---

## Phase 2: Research (LinkedIn / Social)

If the sender provides a LinkedIn URL or handle, use web search or `mcp__487bb3b1-6fe9-4e75-9269-69aef501c61c__enrich-prospects` (Proxycurl) to pull:
- Career highlights and tenure
- Consistent themes in recommendations (if visible)
- Posts that reveal personality, interests, or values
- Any public talks, awards, or notable contributions

Use this to generate quiz questions that feel insider and specific. Questions like "What is [Name]'s superpower in a meeting?" are only good if the options are so specific they make people think, not generic flattery.

If no social profile is available: rely entirely on intake answers. Make the quiz feel local and personal to the team context.

---

## Phase 3: Design Palette

Do NOT default to a fixed aesthetic. Derive the color palette from the person's personality and interests.

### Palette generation logic

| Person type | Suggested direction |
|-------------|---------------------|
| Nature person, trekker, outdoors | Earthy greens, warm tans, forest tones |
| Tech architect, data person | Clean blues, slate, monochrome with accent |
| Creative, design, arts | Warm terracotta, gold, off-white |
| Leadership, executive presence | Deep navy, champagne, minimal |
| Sports, energy, competitive | Bold primary [[colors]], high contrast |
| Default / [[Champions Group]] sender | Orange (`#F26722`), soft peach (`#FFF4EC`), warm white |

Define 3-4 CSS custom properties at minimum:

```css
:root {
  --primary: /* dominant color */;
  --accent: /* highlight / CTA color */;
  --bg: /* page background */;
  --surface: /* card background */;
  --text: /* body text */;
  --text-muted: /* secondary text */;
}
```

Always verify contrast: text on colored backgrounds must be explicitly white or dark enough to pass readability. Never rely on inheritance from a parent that might override it.

---

## Phase 4: Page Structure

Build a single-file HTML page with this section order. Sections can be renamed, reordered, or removed based on context — this is a starting framework, not a rigid template.

```
1. Hero             — Name, occasion, opening line. Big visual moment.
2. Timeline / Stats — Career milestones or years counter. Animated counters preferred.
3. Traits           — 3-4 defining characteristics. Cards or tiles.
4. Tribute          — Personal letter / tribute text with typing animation. 
                      Include story visual here if one exists.
5. Quiz             — "Observer Proficiency Test" or similar. 4-6 questions.
6. Guestbook        — Optional. Only include if Supabase is provided.
7. Sign-off         — From sender, with warmth.
```

### Hero

- Name prominently displayed
- Occasion line: "23 Years of [Name]" or "Happy 40th, [Name]"
- Optional: animated particle effect, gradient background, or hand-drawn SVG element
- Brief tagline that captures their essence in one phrase

### Timeline / Stats

Animated counters on scroll (IntersectionObserver):
- Years served
- 1-2 other meaningful numbers (projects shipped, offices opened, whatever is known)

If no numbers are known, use a visual timeline of 3-5 milestones instead.

### Traits

3-4 trait cards. Each card has a title (the trait) and a 1-2 line description that makes it feel specific to this person.

Use a flip card mechanic OR a simple hover-reveal. Keep it light — this is not the main content.

### Tribute Section

The emotional heart of the page. A personal letter or tribute in the sender's voice.

- Typing animation for the first paragraph (character-by-character)
- Remaining paragraphs fade in after the first finishes
- If a story visual exists: reveal it between the first and second paragraphs
- Keep tone warm and specific. Avoid generic superlatives.

### Story Visual (if applicable)

An SVG animation tied to a specific memory or interest. Examples from Sundar Raj page:
- Mountain trek path drawn progressively with stroke-dashoffset animation
- A code terminal typing a message
- A cricket pitch with an animated ball
- A data chart building itself

**Key implementation patterns:**
```js
// Path draw animation
const pathEl = document.getElementById('pathId');
const len = pathEl.getTotalLength();
pathEl.style.strokeDasharray = len;
pathEl.style.strokeDashoffset = len;
// CSS transition or requestAnimationFrame to animate to 0

// Replay function with DOM reflow trick
function replayStory() {
  const pathEl = document.getElementById('pathId');
  pathEl.style.transition = 'none';
  pathEl.style.strokeDashoffset = pathEl.getTotalLength();
  void pathEl.offsetWidth; // force reflow
  pathEl.style.transition = 'stroke-dashoffset 3s ease-in-out';
  pathEl.style.strokeDashoffset = 0;
}
```

Position the visual inline within the tribute body, not as a separate section. It should feel woven into the narrative.

### Quiz Section

Title it something fun: "The Observer Proficiency Test", "[Name] Certified", "How Well Do You Know [Name]?"

4-6 questions, each with 4 answer options in a 2×2 grid. Multiple correct answers per question are fine (and encouraged for variety).

**Critical quiz rules:**

1. **Answer distribution:** Do NOT put the correct answer in the same grid position every time. Randomize: use positions 1, 2, 3, 4, or diagonals across questions so it doesn't feel like a pattern.

2. **Answer truthiness check:** Answers that are `false` must not block navigation. Use key existence, not value truthiness:

```js
// WRONG — blocks navigation when a wrong answer is selected
if (!answers[String(current)]) return;

// CORRECT — only blocks if question hasn't been answered yet
if (!(String(current) in answers)) return;
```

3. **Score panel placement:** The score result panel must be placed OUTSIDE `.quiz-panels { overflow: hidden }`. If it's inside, it will be clipped.

```html
</div> <!-- closes .quiz-panels -->
<div class="quiz-nav">...</div>
<!-- Score panel: intentionally OUTSIDE .quiz-panels -->
<div class="score-panel" id="scorePanel">...</div>
```

4. **Quiz questions should be genuinely specific.** Good quiz question ingredients:
   - A trait that could go multiple ways ("What does [Name] do when a project is at risk?")
   - An inside reference ("What does [Name] always have at their desk?")
   - Something pulled from their LinkedIn or the intake interview
   - A fun "which of these is NOT true" format

5. **If Supabase is connected:** After quiz completion, show score and offer to save it alongside the guestbook entry. Pre-fill the name field. Include a link back to guestbook: "Leave a note in the record →"

6. **If no Supabase:** Show score with a congratulatory message. No save button needed.

### Guestbook (Supabase only)

Only build this if the sender provides `SB_URL` and `SB_KEY`. Otherwise skip entirely.

Use anonymous fetch calls to Supabase REST API:
```js
const SB_HDRS = {
  'apikey': SB_KEY,
  'Authorization': 'Bearer ' + SB_KEY,
  'Content-Type': 'application/json',
  'Prefer': 'return=minimal'
};
```

Include a nudge above the guestbook form: "Haven't taken the quiz yet? Take it first →" with a `jumpToQuiz()` scroll function. Hide the nudge once the quiz is completed.

### Sign-off

Simple, warm closing. From the sender. If sender is [[Sreedeep Surapaneni|Sreedeep]] / [[Champions Group]]:
- Sign "With gratitude, [Name] & The [[Champions Group]] Family"
- Use [[Champions Group]] brand [[colors]] for this section

---

## Phase 5: Technical Implementation

### File structure

Everything in a single `.html` file. No external CSS files, no external JS files. Google Fonts via CDN link is acceptable. No frameworks. No build tools.

### Animations

Use IntersectionObserver for scroll-triggered animations. Unified observer preferred — one observer can fire multiple effects when a card enters viewport.

```js
new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !started) {
      started = true;
      // trigger typing, counters, path draw, etc.
    }
  });
}, { threshold: 0.20 }).observe(document.getElementById('cardId'));
```

### Dark mode

Add dark mode toggle if the page has a dedicated color scheme. Use `body.dark` class overrides:

```css
body.dark {
  --bg: #1a1a1a;
  --surface: #2a2a2a;
  --text: #f0f0f0;
}
```

Always verify contrast in both modes before finishing.

### Typography

- Google Fonts via CDN (Playfair Display for headings, Inter or Lato for body is a safe default)
- Match font personality to the person: serif for warmth/legacy, sans-serif for modern/technical

### Scrolling / jump functions

```js
function jumpToSection(id) {
  document.getElementById(id).scrollIntoView({ behavior: 'smooth', block: 'start' });
}
```

Use `block: 'start'` not `block: 'nearest'` — nearest only scrolls minimally, start guarantees the section is at the top of the viewport.

---

## Phase 6: Output and Delivery

1. Save the file as `[person-name-slug]-[occasion].html` in the workspace folder
2. Provide a `computer://` link so the sender can open it directly
3. Brief note on what's inside (1-2 sentences max)

**Then say:**

> "Want to share this as a live link? You can deploy it to Netlify in about 30 seconds: drag the HTML file to [drop.netlify.com](https://drop.netlify.com) and you'll get a shareable URL. No account needed for a basic deploy."

Only say this once. Don't repeat it or push it.

---

## Quick Reference: Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Score never shows after quiz | Check that score panel is outside `overflow: hidden` container |
| "Next" button frozen after wrong answer | Use `if (!(String(current) in answers))` not `if (!answers[...])` |
| All correct answers feel like position 3 | Redistribute: use positions 1, 4, 2, diagonal, etc. |
| Trek/visual plays once then won't replay | Use DOM reflow trick in replay function (`void el.offsetWidth`) |
| Dark text on dark background | Explicitly set `color: white` on elements with colored backgrounds — don't inherit |
| Scrolling jumps to wrong position | Use `block: 'start'` not `block: 'nearest'` |
| em-dashes in output | NEVER use em-dashes. Periods, commas, colons, or restructure. |

---

## Test Prompts (for eval)

Use these to verify the skill works end-to-end:

**Test 1 — Minimal input, no Supabase:**
> "Make an anniversary gift page for Priya Nair, our VP of Engineering at [[Lake B2B]], who's completing 10 years. She loves hiking and is known for making complex systems look effortless. Sender is me, [[Sreedeep Surapaneni|Sreedeep]]."

**Test 2 — Rich input with memory:**
> "Create a birthday gift page for Marcus Webb, turning 50. He's our Head of Sales at [[SPAN Global Services]], been with us 8 years. Story: he once drove 4 hours to close a deal in person when everyone else was doing Zoom, and landed it. Known for his laugh and his obsession with cricket. Sender: The [[SPAN Global Services|Phoenix]] Team."

**Test 3 — Supabase guestbook:**
> "Build an anniversary page for Ramona Salgado, 15 years at [[Champions Accelerator]]. She's the quiet force behind everything operational. Personality: calm, precise, never misses a detail. Interests: classical music, Carnatic specifically. I have a Supabase project set up: [URL] [KEY]. Sender: [[Sreedeep Surapaneni|Sreedeep]] and the team."

---

*Reference implementation: `/sessions/friendly-quirky-allen/mnt/Celsus/sundar-raj-23-years.html`*

## Related
[[Skills MOC]] | [[Sreedeep Surapaneni]]
