---
name: incremental-document-revision
description: Use for pass 2+ of a document revision.
version: 1.0.0
metadata:
  hermes:
    tags: [Documents, Docx, Contracts, Renumbering, Verification]
    related_skills: [commercial-agreement-revision, docx]
---

# Incremental Document Revision

Governs pass 2 and later of any document revision, where an earlier pass already
established numbering and cross-references. The first pass is the easy part; every
subsequent pass is a structural edit to a document whose own internal references
now point at things you are about to move.

Use alongside the class-level revision skill, which covers auditing the source and
drafting the requested clauses. This skill covers what changes once numbering
exists.

## When to Use

- A stakeholder adds clauses after a revision is already numbered
- The user asks for a second pass, a lean pass, or a final pass
- New sections must slot into an existing numbered scheme
- A prior pass renamed or renumbered anything

## The ordering rule

**Run renumbering and cross-reference repair LAST, after every content insertion.**
A renumber pass placed before a later insertion silently misses the paragraphs
that did not exist yet, and the document ships with a stale numbering tail that
nothing flags. Sequence: insert all content, then renumber, then remap
references, then verify.

## Remapping references without cascading

Renumbering and rewriting `Section X.Y` strings must be **simultaneous**, in one
pass, because sequential rewriting cascades: mapping 3.2 to 3.4 then 3.4 to 3.6
moves the 3.2 text twice.

```python
ref_map = {"3.2": "3.4", "3.4": "3.6", "6": "5"}
text = re.sub(r"Section (\d+(?:\.\d+)?)",
              lambda m: "Section " + ref_map.get(m.group(1), m.group(1)),
              text)
```

Get the **direction** right. When a block is renumbered from 6 to 5, every
reference must follow it down to 5, so the map is `"6": "5"`, not `"5": "6"`.
Build the map by writing out what each new number came from, never by listing the
old numbers you expect to find.

## Index invalidation is the main source of self-inflicted bugs

`doc.paragraphs` is a fresh list on every access and indices shift the moment you
insert or move anything. Two failure modes repeat:

- **Writing to a heading index destroys the heading.** Setting text on the
  paragraph that *is* the heading replaces it with body text and leaves the
  original body as a duplicate. Write to the heading index only when replacing the
  heading itself; otherwise insert after it.
- **A matcher that assumes tab characters.** `startswith("Title:\tTitle: __")`
  fails when the tab was normalised or split across runs. Match on a prefix plus a
  substring check for the distinguishing feature, and give the lookup a
  `StopIteration` handler so a miss is visible instead of a stack trace.

After any edit, re-derive indices by locating text, never by reusing numbers
captured before the mutation.

## Verify the assembled document, not your own change log

A successful edit log proves the script ran, not that the output is correct. Read
the output and check invariants directly:

```python
import re
from docx import Document
t = [p.text for p in Document(NEW).paragraphs]
full = "\n".join(t)

# 1. every cross-reference resolves
defined = {m.group(1) for m in re.finditer(r"^(\d+(?:\.\d+)?)[\.\s]", full, re.M)}
dangling = [r for r in set(re.findall(r"Section (\d+(?:\.\d+)?)", full))
            if r not in defined]

# 2. no duplicated paragraphs
seen = {}
for i, s in enumerate(t):
    k = re.sub(r"\s+", " ", s).strip()
    if len(k) > 80:
        if k in seen: print("DUPLICATE", seen[k], i, k[:60])
        else: seen[k] = i
```

Also assert: section numbers ascend with no gaps or duplicates, parent headings
precede their first child, subclauses sit inside their parent rather than after
the next section heading, signature blocks sit last with fields in signing order,
and no two clauses govern the same subject.

Run these on **every** pass, not just the last. A defect introduced in pass 3 is
still in the file when pass 5 ships.

## Preservation diff between passes

Diff each pass against the one before it, not only against the original. Every
absent paragraph must map to a named intentional edit. A silent disappearance at
pass 3 is invisible if you only ever diff pass N against the pristine source.

## Stakeholder clauses that contradict their own rationale

When someone supplies clause text and a reason for it, check the clause against
the reason before pasting. A clause granting perpetual use on expiry can defeat a
stated goal of creating a renewal checkpoint.

Do not silently substitute your version. Draft the bounded alternative, write both
into the document as an explicit decision with a recommendation, and report the
conflict in one paragraph so the originator can settle it. Silently "improving" a
colleague's clause hides a decision they are entitled to make.

Also check supplied text for terms belonging to a different document. A clause
written for a direct client relationship may name the counterparty differently
from the document it is being pasted into, and the mismatched defined term is
itself a defect.

## Pitfalls

- **Renumbering before the last insertion.** The numbering tail goes stale and no
  check catches it.
- **Sequential reference rewriting.** Cascades; use one simultaneous substitution.
- **Getting the remap direction backwards.** Write the map old-to-new by reading
  the renumbered document itself.
- **Overwriting a heading index.** Silently converts a heading into duplicated
  body text.
- **Trusting the edit log.** Re-read the output and assert the invariants.
- **Verifying only the final pass.** Defects survive across passes; re-run every
  invariant every time.
- **Reusing pre-mutation indices.** Re-derive by text after any structural edit.

## Verification

- [ ] Renumbering ran after all content insertions
- [ ] Reference remap applied simultaneously, in the correct direction
- [ ] Zero dangling `Section X.Y` references
- [ ] Zero duplicate paragraphs
- [ ] Parent headings precede children; subclauses sit inside their parent
- [ ] Preservation diff against the prior version, every absence explained
- [ ] Package validates