# Library and improvement loop

## One owner, small reusable parts

This skill owns Deep's talking-face editing workflow. Use the existing FFmpeg/HyperFrames/GSAP tools rather than building another editor, plugin platform or database. Keep source media and feedback ledgers in a private project folder, not in the shared skill repository. The current local library root is `~/Movies/editorial-house-style/library`; create a project-local equivalent on another machine.

Start the pattern catalog from proven work, not an aspirational inventory. The event proof supplies three design recipes: contrast/gap, progressive process, return-to-speaker. They have evidence for narrative usefulness in that proof. Its old captions and motion polish are not approved merely because the story was praised. A whole proof is a seed composition, not three independently implemented renderers.

For each library item record id, version, purpose, inputs, source composition, test case, status, approved dimensions and known limits. Status is one of candidate, rendered, approved, retired. Use separate status fields for narrative, type and motion. New fact-card, split-screen, B-roll and comparison templates enter only when a real video needs them and a real example has been rendered. Do not fill the library with empty templates.

Read `templates/style-tokens.json` as candidate settings. Freeze a copy in each video project so later library edits cannot change an older approved render. Keep the previous good version for rollback. Use `templates/review-record.json` for the smallest feedback record; no app or service is required.

## After every video

1. Save exact source/output paths, edit map and preset versions in its private review record.
2. Separate automated technical checks from human judgments of pacing, typography, naturalness, sound and brand fit.
3. Record the user's actual correction with its dimension and timestamp if provided. Praise for the story is not approval of the captions. Missing feedback remains unreviewed, not accepted.
4. Turn specific corrections into narrow rules. Preserve explicit vetoes so later successes do not reintroduce them. Explicit preferences outrank inferred ones.
5. Change one dimension at a time for a controlled comparison where practical. If changing both typography and motion, name both and do not claim which caused the preference.
6. Render and compare against the previous version with the same source interval. Run technical checks and inspect the actual encoded revision, not cached screenshots.
7. Promote only the part the user approved, retaining source evidence. Recurring inferred preferences require consistent evidence across distinct videos; a single accepted clip establishes a candidate pattern, not a universal aesthetic law.
8. Increment the affected item version, update this skill when the lesson generalizes, and preserve a short changelog. Keep video-specific notes in the private ledger.

This is an explicit review-and-update workflow, not automatic model training and not an unattended service. No self-improvement claim is valid unless the stored feedback changed a subsequent output. Performance metrics such as retention or leads require actual measurements; visual approval alone is not engagement evidence.
