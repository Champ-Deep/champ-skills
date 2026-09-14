# no-ai-slop: tests and evals (2026-09-11)

**Verdict:** the gate works. In a blind A/B test, copy written with the gate won 5 of 5 briefs and carried 4 slop patterns against 20 for the same model writing without it. One real weakness surfaced (numbers drifting in scope) and is fixed in the updated skill.

## What was tested

| Layer | What it checks | Result |
|---|---|---|
| Linter unit tests (`test_slop_lint.py`) | 8 slop fixtures, 6 clean controls, 3 regression cases from the blind run, 5 judged-clean outputs | 6 of 6 tests pass |
| Edit mode | Skill rewrites 14 drafts (8 sloppy, 6 clean), blind to which is which | Slop 46 linter findings to 0. Clean drafts left untouched (similarity 1.00). No numbers invented; the only number removed was an unsourced "studies show 70%" claim, which the skill flagged |
| Detect mode | Skill audits the same 14 drafts blind | 8 of 8 slop drafts flagged, 0 of 6 clean drafts flagged, 100% of expected patterns named |
| Generation A/B | Same model writes 5 briefs twice: plain, and with the Gate pass. A separate blind judge compares | Gated won 5 of 5. Slop instances 20 to 4. Unsupported claims 12 to 8 |

## What the baseline got wrong that the linter missed at first

The plain run used no em dashes and no banned words, so a word-list check scored it clean. The blind judge found the deeper tells: "Most AI SDR pilots don't fail because of the AI", "The problem wasn't the prompts, the sequences, or the model", "stops being a data problem. It becomes a field-force problem", a "Here's why" transition, parallel sentence pairs, a chiasmus closer, and a follow-up email that buried the 6pm ask in the middle. These shapes are now linter rules and regression tests.

## What the gated run still got wrong

The gated LinkedIn post turned "38% of contacts across 3 pilots" into "more than a third of each list". That is scope drift, not invention, and the old Eval did not catch it. The updated skill adds a "numbers keep their scope" principle and an Eval check.

## Limits, stated plainly

- The unit fixtures were written alongside the linter, so they prove the rules fire, not that they generalize. The regression cases came from unseen text, which is the better signal.
- The linter is deterministic and catches surface shapes only. Portability, voice, and fact drift still need the skill or a human.
- Five briefs and one judge is a small sample. Rerun `score.py` after any skill edit, and add a regression case for every miss.

## Files

- `slop_lint.py`: the linter. `python3 slop_lint.py draft.txt`, exit code 1 on any HIGH finding.
- `evals/test_slop_lint.py`: run with `python3 test_slop_lint.py`.
- `evals/fixtures.json`, `briefs.json`: test inputs (dash characters stored as escapes).
- `evals/score.py`, `judge_out.json`, `judge_key.json`, `blind_map.json`, `runs.zip`: the scored run (unzip it next to `score.py` before rerunning).
