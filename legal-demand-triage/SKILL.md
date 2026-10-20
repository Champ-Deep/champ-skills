---
name: legal-demand-triage
description: "Use when a demand letter or lawsuit threat lands for review."
tags: [legal, privacy, compliance, cipa, demand-letter, litigation, triage]
---

# Legal demand triage

Use when a demand letter, draft complaint, arbitration notice, or lawsuit threat lands against a Champions entity (PDF attachment, email, or mail forwarded by a registered agent). Goal: a sourced verdict on merit plus a resolution path that never contacts the sender.

## When to Use

- A PDF or forwarded email is a legal demand, cease-and-desist, "informal dispute resolution" letter, arbitration notice, or draft/filed complaint naming a Champions entity or site.
- Deep asks whether a legal-looking letter is "real", "frivolous", or worth worrying about.
- A privacy/statute claim (tracking pixels, pen registers, wiretapping, CCPA/GDPR) arrives with a settlement figure and a deadline.
- NOT for routine contracts: NDAs and client agreements go to `champions-nda` / `commercial-agreement-revision`. NOT for site audits with no legal claim attached: those go to `site-growth-audit`.

## Always-on rules

1. **Never engage the sender.** No reply letter, no payment, no phone call, no "informal dispute resolution" correspondence. This is Deep's standing instruction, stated emphatically and repeated: a serial sender monetizes the response itself. Every outward step goes to counsel or the insurer instead.
2. **Verdict first, then evidence, then steps.** One line stating frivolous / credible / cannot-yet-tell, then a defense-vs-source table, then numbered resolution steps with an owner each. Deep reads the first line and decides from it.
3. **Never soften a finding.** If it is frivolous, write "frivolous" plus the sources that make it so. A hedged conclusion is worse than a wrong one for a legal decision.
4. **Split legal merit from technical hygiene.** A claim can be legally dead while the site behavior it points at still violates other laws or invites the next sender. State both verdicts separately.
5. **Flag unverified items explicitly.** If you could not reach the docket, could not confirm service, or a date is only the letter's own claim, label it "unverified" instead of assuming the favorable version.

## Procedure

### 1. Extract the full letter before judging

PDFs arrive as attachments; text-bearing PDFs extract cleanly.

```bash
python3 -c "import fitz,sys; d=fitz.open(sys.argv[1]); print('\n'.join(p.get_text() for p in d))" letter.pdf
```

Fallback: `pdftotext -layout`. Scanned pages: `pdftoppm -r 200` then vision on the rendered pages.

Capture, in this order: (a) which statute/claim, (b) who sent it, pro se or via a firm, (c) which entity and address it was sent to (registered-agent forwarding is common and explains late receipt), (d) all dates, (e) demand amount and deadline, (f) whether an actual complaint is attached or only a *draft* complaint. A draft means pre-suit; never write a response plan as if service happened.

### 2. Classify the sender

Search the sender's name plus the statute, and search a distinctive phrase from the letter in quotes.

- **Mass template / serial sender**: same letter hitting many companies, a settlement figure repeated across demands, or prior coverage by plaintiff-watch trackers (CIPAWorld, defense-firm client alerts). Treatment: the letter's own boilerplate and exhibits are usable against it; ignore the settlement offer.
- **Bespoke or counsel-backed**: real firm letterhead, company-specific facts, an alleged specific harm. Treatment: engage counsel early even if merit looks weak.

### 3. Re-verify the law; do not trust the letter's citations

Letters cite statutes as they were, and privacy statutes are perpetually mid-reform. For every claim:

1. Pull the live statute text: `https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PEN§ionNum=<NUM>` (other states: their legislature domains).
2. Search for pending or recently enacted amendments to that section. Read the **effective date** and, critically, any **retroactivity clause** (does it reach claims filed on or after a past date, or pending cases?). A statute that strips the private right of action for website tracking kills these demands wholesale, retroactively.
3. Search rulings on the theory: `<statute> website tracking motion to dismiss`, `<statute> demurrer sustained`. Appellate tentatives and firm client alerts surface within days of a decision.
4. Each authority goes into the verdict table with its URL and a one-line "what it does to this claim".

### 4. Verify the claimed facts on the live site

The letter's exhibits are a snapshot, often months old, often captured by an automated bot. Measure today's behavior yourself:

```bash
python3 scripts/pre_consent_probe.py https://www.example.com/ --wait 15
```

The probe loads the page with real Chrome headless, takes **no interaction and clicks nothing**, waits past any deferred-loader window, and reports: consent banner presence, cookies set, third-party tracker hosts hit pre-consent, plus tracker hosts *declared in page source* (catches scripts blocked or swallowed by a `window.fetch` monkeypatch). Read the page's custom loader scripts by hand too; the worst leaks are hand-rolled `setTimeout` / first-interaction loaders living outside the consent plugin.

Compare letter vs now. If the site was remediated after the letter's date, say so explicitly: the posture shifts from "ongoing violation" to "historical snapshot with a remediation date", which changes both leverage and the hygiene fix list.

### 5. Output shape

```
Verdict: frivolous | credible | cannot-yet-tell  (one line, why)

| Defense / exposure | Source |
|---|---|
| ... | statute URL, ruling, or probe output |

Resolution steps
1. <step> - owner - clock
```

Include a row for the sender's own evidence against itself: bot user-agent strings, unnatural viewport sizes, out-of-state IPs in their exhibits.

### 6. Resolution path (never the sender)

See `references/resolution-postures.md` for the decision table by posture. Common sequence: confirm nothing is filed via the court's public docket search (unfiled demand plus empty docket = stop, with a re-check date); give the verdict table to counsel in the entity's jurisdiction as a one-shot scoped review; notify the cyber/E&O insurer if a policy exists (demand letters often start the notice clock); fix site hygiene as a separate workstream owned by whoever owns the property, and re-run the probe after deploy.

## Pitfalls

- Believing the letter's "we will file in N days" as a real clock. Verify filing status on the docket yourself; unfiled drafts are the standard pressure tactic and many never get filed.
- Letting the sender's exhibits become your facts. Reproduce every technical claim on the live site before repeating it in your verdict.
- Treating a remediated site as a clean one. Prove the fix by re-running the probe, not by being told it was fixed.
- Answering "is this real?" with only the legal analysis. Deep always asks both questions at once: legal merit *and* is the site actually doing what the letter claims.
- Quoting a statute's current text without checking its effective date. A claim can be valid today and abolished with retroactive effect next quarter; he needs the answer that covers his whole exposure window.
- Treating receipt as service, or a registered agent's forward as delivery to the operating entity. Deadlines run from service, which is a separate fact to confirm.
