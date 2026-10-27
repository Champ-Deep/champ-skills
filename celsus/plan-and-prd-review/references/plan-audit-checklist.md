# Plan audit checklist

Walk a plan or PRD section by section, in this order. Every question is asked of
the document itself; an unanswered question is a finding, not an omission to fill
in silently.

## Requirement mapping (do this first)

One row per requirement the plan states, four columns:

| Requirement (section) | Existing code | State | Proof |
|---|---|---|---|
| what the plan asks for, with its section number | file, module, service; name the sibling repo if it lives elsewhere | exists / partial / absent | how it was shown to run, or "read only" |

Rules:

- `exists` requires a run, not a read: an import, an execution, or a returned
  identifier read back. "Read only" belongs in the proof column until then.
- `partial` is the work plan, not `exists`. Code that imports but never executes
  its main path is partial with a note on which path is dead.
- Search sibling repos before marking anything `absent`.
- If most rows are `exists`, the review's headline is a build decision: skip,
  wire, and build only the absent rows.

## Per-section questions

| Section | The question |
|---|---|
| Goal | What number or state makes this done, and could a bad result still be reported as success? |
| Thresholds | For each metric: measurement method, named denominator, ship bar, kill value? |
| Phasing | Does each phase end in a gate that can fail, or in the phase merely being written? |
| Architecture | Which parts already exist elsewhere, and were they run to confirm it? |
| End-to-end journey | What does the user see in the first three seconds, and what are the named paths through? |
| Handoff | What triggers escalation, what does the human receive, where, how fast, and what is the user told meanwhile? |
| Security and abuse | Injection through the user's own input, retention, tenant isolation as a threat, cost exhaustion, third-party script surface? |
| Cost model | Cost per interaction, per outcome, and break-even against one outcome? |
| Failure modes | One row per dependency: what the user sees when it is down, rate limited, or empty? |
| Feedback loop | What is collected, reviewed on what cadence, and which single number is trended? |
| Decisions | Is every open ruling listed with a recommendation and an owner, rather than buried in prose? |
| Compliance / legal | What obligations does the plan carry that it never states? |

## After landing new sections

Confirm every `section N` reference in the body resolves to a heading that
exists, re-check heading order, and sweep the file for em and en dashes. Cross
references break silently when sections are inserted.

A plan that ends in open rulings is not finished in the document: give each
independent ruling its own decision card (see the `kanban-task-intake` skill)
so it gets answered as a decision instead of waiting for the reader to reopen
the file.
