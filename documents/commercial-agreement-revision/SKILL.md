---
name: commercial-agreement-revision
description: Use when updating a stale client-facing agreement.
version: 1.0.0
metadata:
  hermes:
    tags: [Contracts, Legal, Redlining, Docx, Sales-Enablement]
    related_skills: [docx, document-to-action-items, no-ai-slop]
---

# Commercial Agreement Revision

Refresh an existing commercial agreement (reseller, partner, SOW, MSA, DPA) to
current terms, or audit an old one before it goes to a client. The deliverable is a
**draft plus a separate blocker list**, never a file that merely looks finished.

Commercial drafting support, not legal advice. Every output says so.

## When to Use

- "Update this reseller/partner/SOW agreement, most of it is from 2024"
- "These need to go out to clients, what has to change"
- "Audit this old agreement before we send it"
- A stale client-facing template with merge fields, wrong footer, or contradictions

Do not use for: NDAs with no commercial terms (use the house NDA system), or
extracting facts with no revision intent (use `document-to-action-items`).

## The core move: edit in place, never retype

**Open the original and edit it. Do not rebuild from extracted text.** Retyping is
how a revision silently drops a clause nobody was looking at. Editing the original
object makes untouched clauses provably intact, because the bytes never moved.

```python
from docx import Document
doc = Document(SRC)   # open the original
# ...mutate paragraphs, insert new ones...
doc.save(OUT)
```

Snapshot what you need **before** mutating. `doc.paragraphs` is a fresh list each
access, and once a block moves the indices shift under you:

```python
paras = doc.paragraphs                                    # snapshot once
sig_elements = [paras[i]._p for i in range(42, 47)]       # grab handles first
```

To move a block, detach the raw `w:p` elements and re-append them after the last
paragraph. Reordering by text is not supported.

To insert a paragraph after another, build the element and use `addnext`, then wrap
it back:

```python
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
el = OxmlElement("w:p")
anchor._p.addnext(el)
np = Paragraph(el, anchor._parent)
```

To replace paragraph text while keeping the first run's formatting, set `runs[0]`
and delete the rest. Assigning `p.text` wipes all run formatting.

## Procedure

### 1. Set up

The `docx` skill scripts need `python-docx`, often absent from the system
interpreter while several pythons sit on PATH. Build an isolated env once:

```bash
cd ~/.hermes/cache/scratch && uv venv docxenv --python 3.12
uv pip install --python ~/.hermes/cache/scratch/docxenv/bin/python python-docx
export PY=~/.hermes/cache/scratch/docxenv/bin/python
```

Without `uv`, `python3 -m venv` plus `pip install python-docx` is the fallback. This
is setup state, not a broken tool: the scripts work once the module exists.

### 2. Read before writing

Read the source, then establish its real shape. A flat text dump hides ordering and
duplication.

```bash
$PY scripts/docx_read.py "$F" --structure   # outline, paragraph/table counts
$PY scripts/docx_revisions.py list "$F"    # tracked changes present?
$PY scripts/docx_comments.py list "$F"     # reviewer comments to honour
$PY scripts/docx_validate.py "$F"          # package health
```

Then dump **every paragraph with its index and style** via python-docx. You need the
indices: they are your only stable handles, and the section headings the user names
by hand ("the Guarantee section") are usually plain bold text, not real headings. An
empty `--structure` outline on a contract is normal, not a defect.

### 3. Audit for structural defects

Work through `references/stale-agreement-defects.md` before drafting anything. Old
templates carry defects invisible in a text dump and fatal in front of a client:
another entity's name in the footer, signature blocks sitting before the terms they
sign, unfilled merge fields in operative text, guarantee clauses cancelled out by the
disclaimer.

Report these alongside the requested changes. The user asks for the upgrades they
already know about; the value is in the ones they do not.

### 4. Draft the requested clauses

`references/amendment-clause-recipes.md` has the drafting pattern for the recurring
amendment types (deliverability guarantee, retention/usage term, suppression and
permission pass, verification cadence, end-client delivery rights, turnaround).

Two rules decide most of the work:

- **A guarantee plus a warranty disclaimer is a contradiction until you add a
  precedence carve.** State the positive guarantee first, open the disclaimer with
  "Save for the Guarantee in...", and add a clause making the guarantee prevail on
  inconsistency. Placement alone is not enough: the disclaimer must name the
  carve-out or it will be read as swallowing the guarantee.
- **Remedy ladders escalate as performance falls.** At or above the higher threshold
  no remedy arises; between thresholds, replacement or credit at the buyer's
  election; below the lower threshold, replacement or refund. Giving the best remedy
  for the best performance is commercially backwards.

Anything unverifiable stays a visible `[CONFIRM: ...]` placeholder. Never invent
entity names, addresses, dates, thresholds, or metrics. An undefined acronym inside
a guarantee clause is a weak link the moment a client pushes back.

### 5. Prove nothing was lost

Diff the original against the revision at both paragraph and sentence level. This is
the step that catches a dropped clause.

```python
import difflib, re
from docx import Document
old = [p.text.strip() for p in Document(OLD).paragraphs if p.text.strip()]
new = [p.text.strip() for p in Document(NEW).paragraphs if p.text.strip()]
sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal":
        print(tag, old[i1:i2], "->", new[j1:j2])
# then: every original sentence >60 chars must appear verbatim in the revision
sent = [s.strip() for s in re.split(r"(?<=[.;])\s+", " ".join(old)) if len(s.strip()) > 60]
print([s for s in sent if s not in " ".join(new)])
```

Each vanished sentence must map to an intentional edit you can name. Anything
unexplained is a bug: revert and redo.

### 6. Validate the package

```bash
$PY scripts/docx_validate.py NEW.docx
```

Also confirm clause ordering (a guarantee must precede the disclaimer it survives),
the signature block is last, the intended footer name, and zero em dashes in output.

## Judgement calls belong to the user

When a fix needs a decision rather than a redraft, flag it in-text and in the blocker
list. Do not resolve it silently:

- Governing law and venue that contradict the contracting addresses
- Whether a trademark licence is granted or prohibited
- Whether a remedy ladder escalates or de-escalates
- Which of two documents owns a term appearing in both

Surface each as a decision with a stated default so the user can answer "yes" in one
reply. List every judgement call in a short section of the blocker list so a reversal
costs a minute.

## Deliverables

Two files, never one:

1. **The draft**, `[CONFIRM: ...]` placeholders intact.
2. **The blocker list**, separate from the sendable file, ordered by severity:
   blockers to fix before it goes out, then commercial gaps the user did not ask
   about, then judgement calls, then open items. Number each item so the conversation
   can reference it.

If the user pushes to send immediately, deliver the draft and say plainly what is
unverified. Speed is not a reason to launder unconfirmed terms into a file that looks
final.

## Pitfalls

- **Rebuilding from extracted text.** Guarantees silent clause loss. Edit the original
  object; untouched clauses are intact by construction.
- **Using keyword spot-checks to prove preservation.** A keyword that was never in the
  original reads as "LOST" and sends you chasing a phantom bug. Diff paragraphs and
  sentences, and confirm a flagged term is absent from the ORIGINAL before treating
  its absence from the revision as damage.
- **`docx_read.py --structure` showing an empty outline.** It reports heading
  *styles* only; paragraphs marked with `w:outlineLvl` will not appear. Verify outline
  levels by reading the XML, or use real heading styles.
- **Capturing `paras` after mutating.** Indices shift as soon as a block moves.
- **Assigning `paragraph.text`.** Destroys every run's formatting.
- **Fixing a governing-law mismatch without asking.** A legal decision with venue
  consequences. Flag it in-text and leave the original text beneath the note.
- **Trusting the section names the user used.** "The Guarantee section" may be a bold
  run in a Normal paragraph, and source numbering may be broken. Locate by index and
  repair duplicate or missing clause numbers while you are in there.
- **Leaving placeholder text in a sendable file.** Convert unfilled merge fields to
  blank signature lines; keep `[CONFIRM:]` markers only in the draft.

## Verification

- [ ] Preservation diff run; every vanished sentence maps to a named edit
- [ ] `docx_validate.py` exits 0
- [ ] Requested clauses present; guarantee precedes the disclaimer
- [ ] Signature block last; footer carries this entity's name
- [ ] No invented entity names, dates, thresholds, or metrics
- [ ] Blocker list delivered as a separate file, severity-ordered
- [ ] Judgement calls listed so they reverse cheaply
- [ ] No em dashes in any output
