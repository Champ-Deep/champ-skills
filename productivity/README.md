# Productivity & Meetings (`productivity/`)

Daily notes, meeting prep/intake/followup, planners, onboarding, interviews, quizzes.

Install: copy a skill folder into your agent's skills dir (e.g. `cp -R {cat}/<skill> ~/.claude/skills/`). Each skill is self-contained with `SKILL.md`.

| Skill | What it does |
|---|---|
| `clf-meeting-prep` | CLF (Champions Leadership Framework) pitch prep for sales and BD reps across all Champions Group brands: LakeB2B, SGS, Ampliz, and Champions Accelerator. Runs a structure |
| `daily-note-recap` | Generate a comprehensive daily note in the Celsus Obsidian vault recapping activity, PLUS a visual HTML executive report in Lake B2B branding, PLUS the nightly BearDrive  |
| `dashboard-refresh` | Regenerates dashboard-data.json in the Celsus vault root so that dashboard.html displays fresh calendar events, correct meeting prep status, and accurate effort health in |
| `day-planner` | Productivity planning skill that combines calendar awareness, energy levels, task priorities, and time constraints into an actionable daily plan with time blocks. Use thi |
| `interactive-quiz` | Create beautiful, interactive single-file HTML quizzes, surveys, and intake forms with diverse, creative interaction patterns that make people actually enjoy answering qu |
| `interactive-quiz-v2` | Extended interaction pattern library for the interactive-quiz skill. Adds 8 new interaction patterns focused on relational, spatial, and nuanced data capture. Use alongsi |
| `intern-onboarding-planner` | Generate a day-by-day first-month onboarding plan for a new hire or intern from resume plus role brief, as a single-file HTML dashboard that answers on screen one: what d |
| `interview-prep` | Build interview prep materials for a job candidate before you talk to them, a prep note (candidate snapshot, role-fit analysis, real risks/tensions to probe, must-ask que |
| `leaderboard` | Create beautiful internal leaderboards that rank people and teams across any metric. Produces screen-ready and print-friendly HTML with podium heroes, ranking tables, tre |
| `meeting-followup` | Executes the follow-up on a meeting or discussion for Sreedeep (Deep). Distinct from meeting-intake, which FILES a meeting; this skill ACTS on it. MANDATORY TRIGGER for:  |
| `meeting-intake` | Processes meeting notes, summaries, transcripts, or recordings into structured vault knowledge and actionable tasks. MANDATORY TRIGGER for: pasted meeting notes, meeting  |
| `meeting-prep` | SPIN-driven meeting preparation skill. Scans calendar, retrieves meeting history from Google Calendar, Notion, Celsus vault and Google Drive, auto-creates/updates persist |
| `morning` | Render the user's morning brief as a styled HTML artifact, or set it up as a recurring weekday task. Use only when the user explicitly asks to run, see, or set up their m |
| `morning-routine` | Multi-skill orchestrator for Sreedeep's daily startup routine, runs around 3pm (his day-start). Chains four skills in sequence: (1) vault-linker to connect yesterday's lo |
| `schedule` | Create a scheduled task that can be run on demand or automatically on an interval. |
| `sprint-mode` | Autonomous time-boxed task execution engine. Reads TASKS.md, ranks tasks by priority and feasibility within a given time window, then executes them with full autonomy usi |
| `weekly-review` | Gamified weekly review skill that aggregates Mon-Fri daily notes from Celsus vault, runs an interactive quiz for subjective reflection, then produces THREE outputs: (1) a |

See the master [INDEX.md](../INDEX.md) for every skill.