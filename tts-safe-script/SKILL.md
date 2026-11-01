---
name: tts-safe-script
description: Use when any text will be spoken by an AI voice. Respell acronyms, caps runs and digits so TTS says them right.
version: 1.0.0
author: Deep / Hermes
license: proprietary
metadata:
  hermes:
    tags: [tts, voiceover, elevenlabs, heygen, kokoro, pronunciation, script]
    related_skills: [voiceover-design, outbound-voice-call, pixel-host-studio, faceless-explainer]
---

# tts-safe-script

## The rule (mandated, every voice, every provider)

**No raw acronym, initialism, caps run, or digit ever reaches a TTS engine.** Not SEO, not B2B, not KPI, not 2026, not 40%. The string the voice reads is respelled into plain spoken words. The string shown on screen or in captions keeps the real spelling. Two strings, always.

This applies to voiceovers, explainers, host videos, phone agents, voice agents, audio tags, and any prompt that tells a studio agent (ElevenLabs, HeyGen, Kokoro, Fish, Higgsfield, Dial, Bland, Vapi) what to say.

## Why

TTS models turn graphemes to phonemes from word precedent. A run of capitals like `SEO` or `B2B` has none: the model guesses, and the guess changes take to take ("see-oh", "sob", a dropped letter, a hallucinated syllable). Letter plus digit mixes are the worst case because they combine two unseen patterns. ElevenLabs' own guidance says the models are best on alphabetical text and that digits and symbols cause mispronunciation and voice hallucination, more so on small or fast models (Flash, Turbo, Kokoro). Their fix and everyone else's is the same: normalize to words before synthesis. A human reading the script stumbles in the same places the voice will.

## How to respell: three classes

| Class | Said as | Write for the voice | Never |
|-------|---------|---------------------|-------|
| Initialism (letter by letter) | SEO, CRM, KPI, CMO | `S E O`, `C R M`, plural `K P I's` | `SEO`, `S.E.O.` (periods can insert sentence pauses) |
| Letter plus digit | B2B, 24/7, AB7, Q3 | `B to B`, `twenty four seven`, `A B seven`, `Q three` | any digit |
| Acronym said as a word | SaaS, JSON, APAC, EBITDA | phonetic lowercase: `sass`, `jay-sawn`, `ay-pack`, `ee-bit-dah` | caps, which read as letters |
| Mixed compound or brand | OAuth, HubSpot, LinkedIn, ffmpeg | hyphenated or split lowercase run: `oh-auth`, `Hub Spot`, `Linked In`, `ff-mpeg` | spaced capitals, which read as isolated letters with hard stops |
| Numbers, money, percent, dates | 40%, $1.9T, 2026 | `forty percent`, `nearly two trillion dollars`, `twenty twenty six` | the glyphs |
| URLs, emails, handles | deependhq.com | `deep end H Q dot com`, `at` for @ | the literal |

Plurals take an apostrophe: `K P I's`, `C M O's`. Without it the voice says "iss". Versions, hashes, SKUs and ticket numbers are not spoken at all; the screen carries them.

When the caption tool aligns from word timings and must keep word count, use hyphenated letters (`S-E-O`, one token) instead of spaced; if the voice then slurs it into a word, fall back to spaced letters and fix the caption by hand.

## Procedure

1. Write the script normally, real spelling, for the eye.
2. Run the respeller on the spoken copy only: `python3 <SKILL_DIR>/scripts/tts_safe.py SCRIPT.txt > SCRIPT.tts.txt`. The lexicon in that file is the single source of truth for Deep's terms (Champions brands, marketing and finance initialisms, regions). Add a new term there, not in prose.
3. Gate: `python3 <SKILL_DIR>/scripts/tts_safe.py --check SCRIPT.tts.txt` must print `tts-safe: ok`. It lists any token with two or more capitals or any digit that the lexicon did not resolve. Respell it or write it out, then re-run. A failing check is a blocker, not a note.
4. Feed only the `.tts` copy to the engine. Captions, on-screen text, storyboard and transcript keep the original.
5. Provider extras, when available and only on top of respelling: ElevenLabs pronunciation dictionaries (alias rules per project, so SEO is said the same way in every film), `<phoneme>` tags on Flash v2 and Turbo v2 only, IPA in `/slashes/` on Eleven v3. HeyGen, Kokoro, Fish and phone agents have no such control, so respelling is the only lever.
6. Verify by ear, or by machine when nobody can listen: transcribe the take (Whisper, `media-use` transcribe route) and confirm every acronym line comes back as its letters. The first thing Deep listens to is the line with the most acronyms.

## Phone and voice agents

The agent's own LLM writes the spoken turns, so the rule goes into the system prompt as an instruction: "Say initialisms as spaced letters (S E O, C R M), say B2B as B to B, write every number, price, date and URL as words." On ElevenLabs Agents set `text_normalisation_type` to `elevenlabs` as well; it is more reliable than the prompt alone.

## Report line

Every voice deliverable states: "Spoken copy respelled with tts-safe-script, check passed, N terms added to the lexicon" or names what was not checked.
