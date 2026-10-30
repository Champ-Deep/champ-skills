---
name: interview-prep
description: "Build interview prep materials for a job candidate before you talk to them, a prep note (candidate snapshot, role-fit analysis, real risks/tensions to probe, must-ask questions, verdict framework) plus a companion live-scoring HTML scorecard you can click through during the call. Saves both into the vault's Atlas/Hiring/ folder in house style (dark theme, orange accent, click-to-score dots, auto-verdict). Use this whenever anyone on the team is about to interview a candidate for any role at any Champions Group company, for example 'prep me for my 10am with the candidate', 'help me get ready for this interview', 'I'm interviewing someone for the SDR role, can you help', 'screen this resume before we talk', 'build a scorecard for this candidate', or when a resume/CV is shared alongside any mention of a call, interview, or meeting with that person. Trigger even if they don't say the word skill, don't name a format, or just paste or attach a resume and say something like 'help me prep for this.'"
---

# Interview Prep

Turns a resume plus whatever you already know about the role into two things a hiring manager can actually use in the room: a written prep note, and a live-scoring HTML sheet to click through during the call. The goal is not a generic question bank, it's a prep grounded in the specific tension between what this candidate actually is and what this specific seat, on this specific team, at this specific stage, actually needs.

## Why the two-document split

The prep note is for reading beforehand and re-reading afterward, it's the narrative: who is this person, why might they be a fit, where's the real risk. The scorecard is for during the call, when you don't have time to read paragraphs, you need a question, a "what a good answer sounds like," and a button. Keep them separate. Don't try to cram live-scoring UI into the markdown note or narrative analysis into the HTML.

## Step 1: Gather what you have

- If a resume or CV was attached (PDF, docx, or pasted text), read it fully. Don't skim, the details that matter most (a date overlap, a vague claim next to a specific one, a certification from a course mill versus a real credential) are easy to miss on a fast pass.
- Note the role and company/team if given. If it's ambiguous, check the vault: `Atlas/Companies/`, `Atlas/Products/`, any existing job description, and prior notes in `Atlas/Hiring/` for the same or an adjacent role. Reaching 95% confidence on WHO this is for and WHAT seat it is matters more here than in most tasks, because a prep built against the wrong seat is actively misleading in the room. If no job description exists anywhere, infer the seat from the team's actual products and say so explicitly in the note, naming which products the inference came from and telling the user to correct you if their version differs. An inferred seat that is flagged stays useful; an inferred seat that is stated as fact misleads the interviewer in the room.
- Check the user's calendar if you have access, to confirm the meeting exists and get the time right. If you can't find it, say so plainly rather than assuming it's fine, a wrong meeting-time assumption in a prep doc is a bad look.
- While you have the invite open, verify three things and report them: (a) does the invite title name the same role you were told this is, invites get reused across seats and a mismatch means nobody knows which seat this actually is; (b) does any attendee email match a contact on the resume, a mismatch is worth one line in the note; (c) does the entry actually carry a join link, calendar APIs often return a null online-meeting field even when the invite body has one, so check and tell the user where to find it instead of letting them discover a missing link at start time.
- Check the candidate's public footprint where the resume claims one: a linked npm package, a GitHub profile, a portfolio. Verify existence and read what is really there, then write what you found into the note as a `Checked online` block. A verified public artifact (package published, repos pinned or absent) is far stronger evidence in the room than any resume bullet, and "1 weekly download" style facts are exactly what turns a "production use" claim into a fair question to ask. If the resume arrives as a mail attachment (Outlook/Graph), pull the bytes with the authenticated download tool to a scratch path and read that file, don't guess the content from the mail body or from an older copy of the same-named resume.
- Look for prior candidate reviews or scorecards in `Atlas/Hiring/` for context on how this team has evaluated similar roles before, and to keep scoring dimensions and tone consistent across candidates.

## Step 2: Understand what "good" looks like for this seat

Don't write generic PM/engineer/sales questions. Read enough about the actual team, product, and stage to know what's really being tested. A two-person freelance build has completely different needs than a 50-person org, an early MVP has different needs than a mature product, a regulated domain has different needs than an unregulated one. This context usually lives in the vault (product dossiers, `CLAUDE.md` files in relevant repos, prior meeting notes) — read it before drafting questions, the same way you would before writing anything else for this user.

The single most valuable thing you can find is a genuine tension: a place where the candidate's strongest instinct might actually work against what this role needs. That tension, if it's real, should become the "must-ask" question that decides the meeting. Don't manufacture one if it doesn't exist, if the candidate is a clean fit, say so and focus the prep on confirming depth rather than inventing conflict.

## Step 3: Write the prep note

Save as `Atlas/Hiring/Interview Prep - <Candidate Name> (<Role / Team>).md`. Structure:

```markdown
---
type: interview-prep
candidate: <name>
role: <role and team/company>
interviewer: <who's taking the interview>
date: <today>
source-resume: <filename if applicable>
tags: [hiring, prep]
---

# Interview Prep: <Candidate>, <Role>

**Meeting:** <time/logistics: invite title (flag if it names a different role), attendee emails, whether a join link exists and where to find it>

## Candidate snapshot
<table: current role, tenure, prior roles, education, certifications, core domain, relevant technical/functional fluency>

**What I checked online:** <verified public footprint: package published or not, repo profile, portfolio, plus what was absent. One or two lines>

## Why they're in the room
<grounded fit analysis: what specifically about their background maps onto this seat's actual needs, referencing real project/product context, not generic "strong communicator" filler>

## Where the fit is genuinely uncertain
<real tensions and gaps, not manufactured ones. Distinguish "worth probing" from "should assume the worst." If something looks like a resume red flag (date overlap, unverified claim, tenure pattern), name it plainly and note it deserves a direct, non-accusatory question rather than a verdict>

## Must-ask (2-4 questions that decide the meeting)
<the highest-leverage questions, each with a one-line "why this matters">

## Secondary probes
<lower-priority questions, time permitting>

## Verdict framework
<what a genuine pass looks like vs a genuine fail, tied to the must-ask questions, not a vague "good vibes" bar>

## Related
<wikilinks to relevant vault notes: product dossiers, prior candidate reviews, role context>
```

Ground every claim in something you actually read, either the resume or the vault. If you're speculating (e.g., "he might expect enterprise-scale process"), say so as a hypothesis to test in the interview, not a fact.

## Step 4: Build the live-scoring scorecard

Start from `assets/scorecard-template.html` in this skill's directory. It has the full dark-theme CSS and the scoring JavaScript already built and tested, don't regenerate this from scratch, that's exactly the kind of boilerplate that's easy to get subtly wrong (broken score math, mismatched question IDs between the buttons and the JS array) if rewritten each time. Read the template, then fill in the placeholders and duplicate the `<section class="q">...</section>` block once per question:

- Title, hero copy, and candidate snapshot card: replace directly with content from the prep note.
- One `<section class="section">` per dimension you're testing (3 to 6 sections is usually right, more than that and interviewers stop using it live).
- One `<div class="q">` per question inside each section, each with:
  - `qtext`: the actual question to ask
  - `why`: one italic line on what it's testing
  - `good` / `bad` / `probe` boxes: what a strong answer, a red-flag answer, and a "push here" moment look like
  - a `scorerow` with 1 to 5 score buttons, `data-q` attribute matching a unique question ID
- Update the JavaScript `allQ` array at the bottom to list every question ID you used, in the same order they appear. This array drives the running total, the progress bar, and the auto-verdict, if it's out of sync with the buttons on the page the scoring will silently break. Build the sections, questions, snapshot, flags and `allQ` in one pass of a script or one edit, not by hand-editing eight near-identical question blocks, hand-editing is where a `data-q` id drifts out of sync with its array entry.
- If one or more questions are decisive (the "must-ask"s that gate the whole hire), wire their IDs into the verdict logic the same way the template does, so a low score on any of them overrides an otherwise-good total. The template carries a `gates` array; with one gate, use a one-element array. Not every scorecard needs this, only add it if a question genuinely gates. Gate and percentage verdicts only evaluate once every question has a score, so a partially scored card reads "In progress" no matter how good the scored answers are, don't read that as a verdict.
- Save as `Atlas/Hiring/<Candidate Name> - <Role short> Interview Scorecard.html`.

**Verify the scorecard before you hand it over.** Filling a multi-question template by hand is the failure-prone part: two independent breakages are invisible to the eye and to a static screenshot. (a) Grep the saved file for `{{` and `}}`, both must print 0, an unfilled placeholder ships as literal text. (b) Count `data-q` attributes and compare against `allQ.length`, a mismatch silently drops scores from the total. (c) Run the em dash check: the page must contain zero em dashes and zero en dashes in any form, the literal UTF-8 characters (grep for the bytes directly, `grep -c $'\xe2\x80\x94'`), the HTML entities (`mdash`, `ndash`), and any other dash entity. A byte-level grep for `mdash` alone is not sufficient, it counts the entity form and misses a literal `—` that the same fill step may have introduced, and both render a dash on screen. (d) Prove the verdict logic runs, not just that the page looks right: the buttons and the gate are JavaScript, and no screenshot exercises them. Headless Chrome in one shell loop, swapping an injected `<script>` before `</body>` per scenario, is enough and needs no browser tooling:

```bash
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # probe your own path
mk(){ sed "s#</body>#<script>$1</script></body>#$F" > t.html;
  "$C" --headless=new --disable-gpu --virtual-time-budget=2000 --dump-dom file://$PWD/t.html 2>/dev/null \
    | grep -o 'id="dockVerdict">[^<]*'; }
mk "document.querySelectorAll('.dots').forEach(d=>d.querySelector('[data-v=\"5\"]').click())"   # expect Strong yes
mk "...click all 5s, then click a gate's data-v=2 button"                                        # expect No hire (gate fail)
```

Cover at least: all-high (advance), a gate scored 2 or low (gate fail), a middling total (borderline), and a low total with the gate cleared (capability gaps). That is four verdict paths, each a separate scenario, and they are the whole point of the file: a scorecard whose math you did not exercise is an unverified deliverable regardless of how it renders. Then shoot the page once and open the image (see Step 5 and the visual-verify gate) for layout, contrast and clipping. Screenshot from a scratch copy whose path has no spaces, `cp "$OUT" shot.html && "$C" ... file://$PWD/shot.html`; an unquoted or unescaped space in the file path splits the URL argument and Chrome exits without writing an image, and the only symptom is a missing output file.

If the call is imminent (under an hour) and the user already has the chat prep, the scorecard is the whole remaining job: skip the markdown prep note, go straight to the filled template, and say in the handoff that the note is not written. A live-scoring sheet beats a note the interviewer cannot click while the candidate is talking.

## Step 5: Wrap up

Present both files. Keep the chat summary short, the documents speak for themselves and the user is about to walk into (or is already in) a meeting. Lead with anything time-sensitive (a calendar mismatch, a missing piece of context you couldn't find) before the content summary. Don't re-explain everything that's already written in the prep note.

## Notes for future interviews

- This skill is deliberately not tied to one role or company. The pattern (snapshot, grounded fit analysis, real tensions, must-ask questions, live scorecard) works for an SDR, an engineer, a PM, a designer, anywhere in the Champions Group. What changes each time is the research in Step 2.
- If the user already has a job description or a set of must-have criteria, use those directly instead of inferring role needs from vault context alone, an explicit JD always beats an inferred one.
- If this is a second or third round for the same candidate, check `Atlas/Hiring/` for the earlier prep or a post-interview review, and build on it rather than starting cold, carry forward open questions that didn't get resolved last time.
