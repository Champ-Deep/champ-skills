---
name: vault-wide-rename
description: "Use when renaming a misspelled name vault-wide."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [vault, rename, migration, verification, wikilinks, generators]
    related_skills: [vault-keeper, obsidian, fix-proof-by-measurement]
---

# Vault-wide rename

Trigger on: "it is X not Y", "fix the spelling everywhere", "rename that across the vault",
"correct the name in all files", or any identifier change that must reach notes, filenames,
generated pages and structured data at once.

This is not a find-and-replace. A content-only sweep leaves the corpus reporting clean
while whole layers still hold the old string, and the next generator run recreates the
old filenames regardless of what you renamed by hand.

## Procedure

1. **Enumerate before touching.** Build the file list first and print the counts. Report
   files and occurrences as two separate numbers: `grep -l` counts files, `-o` counts
   occurrences, and quoting one figure for both under-reports by an order of magnitude
   when a term is dense in one file.
2. **Back up the exact matched set.** `tar czf backup.tar.gz -T filelist`, then confirm the
   archive is non-trivial in size before writing anything. A version-control checkout is a
   second net, not the first.
3. **Change the source of every generated name, then regenerate.** Output slugs normally
   derive from a source field, not from a filename. Edit that field, rerun each generator,
   and only then look at outputs. Renaming generated files by hand guarantees the next
   build undoes it.
4. **Sweep content, case-insensitively, across all text extensions.** Notes are a minority
   of the corpus: HTML, JSON, JSONL, JS, test fixtures and eval cases are usually most of
   it. Enumerate by extension, not by assuming it is prose.
5. **Rename paths.** Notes, meeting files, and any folder or file named after the
   identifier. Skip a rename whose target already exists and report it rather than
   overwriting.
6. **Rewrite structured files through a parser.** Load and dump JSON rather than doing a
   blind string replace, then assert the file still parses. Blind replaces break quoting
   and structure invisibly.
7. **Repoint links.** Every wikilink whose target is the old name must be rewritten, and
   the renamed note must exist at the new path or the link is a phantom.
8. **Search outside the usual reach.** Generator scripts, gates, skill files and any
   throwaway script you wrote for the sweep all hold the string too. Remove the sweep
   script afterward so its own literal does not become the next false positive.

## Verification

Finish with two independent methods agreeing on zero. One method reporting zero is a claim
about the method, not about the corpus.

```bash
# content, case-insensitive, both directions
grep -rIil "OLDNAME" . --exclude-dir=node_modules --exclude-dir=.git
# filenames, case-insensitive
find . -iname "*oldname*" -not -path "*/node_modules/*" -not -path "./.git/*"
```

Run a Python scan alongside the shell grep. If the two disagree, believe the one that
found more and find out why the other missed it before reporting clean.

Then assert each link target resolves and every generated artifact rebuilds identically:
rerun the generators and confirm a clean rerun reproduces the output.

## Pitfalls

- **A timed-out search reports zero, not an error.** `timeout N grep ... > out; wc -l < out`
  prints `0` on a kill and is indistinguishable from a genuine no-match. Check the exit
  status, or drop the timeout and let it finish. A zero from a bounded search is not
  evidence of absence.
- **Case-sensitive search misses the same token in another case.** An all-caps heading, a
  JSON string value and an HTML `value=` attribute all survive a case-sensitive sweep that
  reported the corpus clean. Name corrections are swept case-insensitively, always.
- **Content edits do not touch paths, and path edits do not touch generated output.** All
  three layers have to be handled or the old string survives somewhere that matters.
- **Machine-written files carry the string.** Build outputs and run logs are not
  decoration; a stale slug inside one leaves a broken reference in a record someone will
  read later.
- **Renaming an id means touching every map keyed by it.** Any lookup table, edge list,
  ordering array or per-person config keyed on the old id silently stops matching.
- **A script written to do the sweep contains the old string.** Delete it, or grep will
  keep reporting a hit that is the tool rather than the data.
- **Report what the sweep could not prove.** Name the layers you did not sweep and say
  why, rather than implying full coverage.