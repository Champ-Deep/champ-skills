# Sound and energy layer

Use a music bed and a few coordinated accents when Deep asks for more energy. Preserve the narrative, legible captions and natural speech. The previous Cipher selection and its scaling were criticized: do not reuse that track or mix as the series default or interpret 'this works' as approval of its music. Choose a fresh, cleared track that fits the new source and audition its relationship to the voice. Do not change every dimension at once or turn a restrained explainer into an effects reel.

## Source and rights

Load media-use and inspect reusable candidates before searching. If its catalog needs unavailable authentication, state that limitation and use a verified artist/library source rather than installing or authorizing a new paid service. Record exact title, creator, download URL, license URL and modifications. Keep required attribution with every distributed video, not only in an internal ledger or metadata a platform may strip. A bundled SFX credit is provenance, not permission to distribute the SFX separately. Never copy commercial music from a reference video.

## Mix

Keep the existing voice stem untouched before the final mix; do not synthesize or replace speech. Match music level from measurements, fade the edges and make room dynamically in the speech band. Prefer the HyperFrames audio carve when available. A reproducible FFmpeg alternative can split the music with acrossover, sidechain-compress the speech band against the voice, recombine without normalization, then apply gentle full-bed ducking. That is a documented alternate mix, not a claim that the native carve ran. Freeze the resulting mix WAV and mount it once so preview and export share the same sound.

Mute the source video's audio when mounting a premixed track, otherwise the voice doubles. Verify the final exported audio against the expected mix with correlation and level checks. Compare the added music/effect signal against the dry voice to prove it is actually present. Measure final integrated loudness and true peak, not just intermediate WAV peaks. Meter checks do not prove musical taste or intelligibility; report listening as unverified when it was not performed.

No universal volume constant: source tracks have different mastering levels. Start voice-first, then audition whether the groove is audible without masking consonants. Evaluate the opening, quietest speech, busiest music and ending on headphones and a phone speaker when available. Offer a restrained and a more present short mix of the same excerpt if balance is uncertain. Do not call LUFS, peak or waveform-correlation checks proof of an appropriate music choice or balance. If listening is unavailable, mark the mix provisional. Long release prevents the bed from pumping between syllables. Put the carve on the music, never on the voice.

## Accents and visual payoff

Use a short transition texture for a meaningful surface change, quiet tactile cues for key stages and one soft resolution accent. Sync cues to actual visual events rather than claiming beat sync from a published BPM alone. One final node fill/ring can establish completion without competing with the captions. Avoid confetti, full-screen flashes, perpetual pulsing and effects on every word.

Keep music choice, music level, SFX intensity and visual flourish as separate feedback dimensions. 'This is good, needs more music' supports keeping the current visual direction; it does not approve a newly selected track. Store the candidate mix, settings and source licenses privately with the video, then update reusable settings only after feedback.

## Implementation pitfalls

FFmpeg duration-valued options require a leading zero for fractional values: use `d=0.8`, not `d=.8`. Surface subprocess stderr on failure so the actual parse error is visible. Preserve the previous good render and use a new versioned output.
