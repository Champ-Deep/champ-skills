---
name: "champions-nda"
description: "Draft, review, or assess any NDA or confidentiality agreement for Champions Group entities: Mutual NDAs, Data/Database NDAs, Real Estate NDAs (InfraTech/SPV/lagoon projects: investors, contractors, JV/land partners), and the Luxury Club NDA system (Champions Club/Aventura/Ranch/Beach Cities: tour NDAs, investor NDAs, staff NDAs). MANDATORY TRIGGER for: \"draft an NDA\", \"review this NDA\", \"assess this NDA\", \"NDA for [client]\", \"confidentiality agreement\", \"mutual NDA\", \"data NDA\", \"real estate NDA\", \"site visit NDA\", \"tour NDA\", \"club NDA\", \"is this NDA safe to sign\", or any uploaded NDA document. Routes everything through the master-template system instead of ad-hoc drafting."
---

# Champions NDA System v2: Drafter & Reviewer

Draft and review NDAs for Champions Group using the master-template system. Core rule: **never draft an NDA from scratch. Anything not on a master goes back to the master.** Covers four families: Mutual, Database/Data, Real Estate, and Luxury Club.

**This is commercial drafting support, not legal advice. Every output carries a counsel-review disclaimer and every draft is a DRAFT until counsel signs off.**

## Canonical assets (Celsus vault)

| File | Location |
|---|---|
| Mutual NDA Master Template v1 | `Atlas/Context Docs/Legal/Champions_Group_Mutual_NDA_MASTER_TEMPLATE_v1.docx` |
| Database NDA Master Template v1 | `Atlas/Context Docs/Legal/Champions_Group_Database_NDA_MASTER_TEMPLATE_v1.docx` |
| NDA Playbook (rationale + July corpus review) | `Atlas/Context Docs/Legal/NDA Playbook and Assessment 2026-07-29.md` |
| Full corpus assessment + M6/M7 spec | `Atlas/Context Docs/Legal/NDA Corpus Assessment 2026-08-06.md` |
| Data Security control set (staff NDA base) | `Atlas/Context Docs/Legal/Data_Security_NDA_Marketing_Pilot.docx` |
| Best-drafted clause sources | EGS Health + Gorisco NDAs in the same Legal folder |
| Prior/executed NDAs | `Atlas/Clients/{client}/` folders and `Other/Archive/Legal Docs/` |

Always read the playbook, the corpus assessment, and the relevant master before producing anything. If the vault is not mounted, ask for it first.

## KNOWN BUGS in the v1 masters: fix in any document you generate

1. Mutual master Clause 12.3 survival list cites "14 (Remedies)" but 14 is Publicity and 16 is Remedies. Correct survival list: Clauses 5, 6, 9, 10, 11, 13, 14, 16.
2. Database master has NO exclusions clause and no Affiliate definition. Import both from the Mutual master (4-part exclusions + no-residuals).
3. Both masters' Affiliate lists omit the real estate and club brands. Add: InfraTech, Aventura, Champions Ranch, Beach Cities, Champions Club, and "any special purpose vehicle promoted or controlled by" the contracting entity.
4. Never leave internal pre-execution checklists inside a sendable .docx. Checklists live in the vault assessment note only.
5. Give every Schedule 1 row a stated default so an unfilled row never leaves forum or modules undetermined.

## Workflow

### Step 0: Intake (one AskUserQuestion round max; skip what context answers)
Determine: counterparty legal entity + jurisdiction, purpose (pull the client note in `Atlas/Clients/` first), whether records/data move and in which direction, which Champions companies and properties are involved, whether physical site access happens, dates/terms already agreed.

### Step 1: Pick the document(s)

| Situation | Document |
|---|---|
| Post-discovery services exploration, no data moving | Mutual NDA |
| Sample file to prove coverage | Mutual NDA (Clause 6 covers samples) |
| Client buying records; delivery imminent | Mutual NDA **and** Database NDA |
| Pure data transaction | Database NDA alone |
| Client sending US their data (suppression file, CRM export, fleet/tanker data, lookalike seed) | Database NDA with Schedule 5 |
| Investor, fundraise, prospectus, capital intro | Mutual NDA + M2 |
| Agency, reseller, channel partner | Mutual NDA + M3 (+ Database NDA if records move) |
| Healthcare counterparty | Mutual NDA + M1, BAA before any PHI |
| RE investor / family office reviewing SPVs or fund models | Mutual NDA + M2 + M6-INV |
| Architect, contractor, lagoon tech consultant | Mutual NDA + M6-CON |
| JV or land partner (title docs, deal terms) | Mutual NDA + M6-JV |
| Any counterparty physically visiting a site or property | Add the Site Visit & Premises Rider |
| Club partner/investor reviewing membership economics | Mutual NDA + M7 |
| Prospective member/buyer touring a club property | **Tour NDA short form** (1 page) |
| Club staff, vendors, photographers, caterers | Staff & Experience NDA |
| M&A / acquisition target diligence | Mutual NDA + M2, NC mandatory, trade-secret carve-out mandatory |

### Step 2: Module system (Annexure A, toggled in Schedule 1; unused modules stay visible but off)

| Module | Switch on for | Key content |
|---|---|---|
| M1 | Healthcare, HIPAA | PHI handling, 24h incident notice, BAA gate |
| M2 | Securities, investment, fundraising, GIFT City structures | MNPI handling, mutual securities warranties |
| M3 | Agency/reseller/sub-processing | End-client consent, flow-down undertakings |
| M4 | Cross-border (party, group, or data subjects outside India) | Transfer basis, DPDPA + GDPR/CCPA mapping |
| M5 | Counterparty operates AI/automation products | Outputs and embeddings deemed CI; enterprise no-training carve-out only with evidence |
| **M6-INV** | RE investors/family offices | SPV structure charts, fund models, waterfall/IRR as defined CI; **standstill**: no direct approach to landowners, co-investors, lenders, or authorities; exclusivity toggle in Schedule 1; Disclosed Methodology extended to fund structures |
| **M6-CON** | Contractors/consultants | "Project Materials" defined class (drawings, lagoon specs, BOQs, soil/site surveys); numbered-copy control; no derivative designs; no bid-shopping of BOQs; sub-consultant flow-down |
| **M6-JV** | JV/land partners | Title documents inspection-only (data room or registrar copies, no originals leave custody); no caveat/encumbrance filings from disclosed title info; no approaches to landowners or revenue authorities |
| **M7** | Club partners/investors | Membership economics, member counts, churn, pricing tiers, expansion pipeline as defined CI; **member PII expressly barred** (override master 9.2, which limits data to business contacts and is wrong for member lists); non-disparagement; celebrity/UHNI heightened-care standard; standstill on approaching members, staff, venue landlords |

**Applies with any M6/M7:** RERA carve-out for mandatory disclosures + pre-launch pricing/inventory restriction; broker non-circumvention (Introduced Party extended to brokers, channel partners, landowners, RERA agents).

### Site Visit & Premises Rider (attach whenever anyone sets foot on a property)
Escorted access only; no photography, videography, or audio recording; **explicit drone/aerial-imaging ban** (DGCA point); no geo-tagged or contemporaneous social posts; visitor log incorporated by reference; identities of other visitors, members, and guests confidential.

### Tour NDA short form (luxury club, 1 page, tablet-signable)
For prospective members/buyers. Frictionless by design, plain language, luxury tone. Contents, all of it and nothing more: no photography/recording/social media on premises; member and guest identity privacy (UHNI/celebrity protection: you do not disclose whom you saw); quoted membership pricing confidential; staff and experience details confidential; non-disparagement-lite (no public commentary on private areas or persons); DPDP notice for the visitor's own captured data; 3-year survival; India law, Bengaluru venue. Never send the 19-clause master to a tour guest.

### Staff & Experience NDA
Base: `Data_Security_NDA_Marketing_Pilot.docx` control set. Add: guest/member privacy, no photography of guests, non-disparagement, define "affiliated brands" explicitly, IP assignment for work product, individual acknowledgment signature table.

### Step 3: Entity check (non-negotiable)
- Champions party = **registered legal entity + CIN**, then defined as "Champions" (the ZebPay pattern done right: expand the full name once).
- Default: **Champions Superior Capital**. Confirm with Srivatsav/Finance which entity holds the relevant licence, property, or SPV before execution. Real estate NDAs may need the SPV itself or InfraTech's registered entity; ask, do not assume.
- **NEVER** sign as "Champions Group", "Champions Accelerator", or any trading name. Trading names cannot hold rights, enforce non-circumvention, or be sued.
- Affiliate definition pulls in the operating companies actually involved (Lake B2B, Champions Infometrics, SPAN, InfraTech, Aventura, Ranch, Beach Cities, Champions Club, SPVs).
- Signatory: Director of the contracting company, never "CEO, Champions Accelerator".

### Step 4: Standard positions (Schedule 1 defaults)

| Term | Champions position |
|---|---|
| Governing law / venue | India / exclusive jurisdiction Bengaluru (arbitration optional). Never cede venue by default (Moneybee ceded Mumbai, ZebPay ceded Hyderabad; both were mistakes). |
| Term | 2 years |
| Survival | 3-5 years **from termination** (never "from disclosure"); trade secrets and Personal Data perpetual |
| Non-circumvention | 24 months where purpose involves referral, introductions, revenue share, brokers, or capital sourcing. With fee/commission recovery and 10-day prior-relationship notice. Never disclaim NC/NS against a vendor touching lead flow (the Arkentech mistake). |
| Non-solicit | 12 months, mutual |
| Incident notice | 48 hours (24 hours for PHI or delivered data) |
| Residuals | Expressly excluded + no-combination rule. Strike any "indistinguishable expertise" carve-out on sight (the LakeB2B-archive loophole). |
| Sample data deletion | 15 days from request or evaluation end |
| Liquidated damages (Database NDA) | Greater of a fixed USD floor or 3x list licence value; 48h no-notice audit on suspicion; never leave the amount blank |
| Perpetual survival of ALL CI | Refuse (the executed ZebPay term). Perpetual applies to trade secrets and Personal Data only. |
| One-way data warranties on Champions | Refuse or mutualise |

### Step 5: Red-flag review checklist (run on ANY draft, ours or theirs)
1. **Entity defect:** trading name or blank CIN on either side?
2. **Agency leak:** anything stopping internal circulation beyond a deal team, or handing material to their agency/contractors? ("Employees and advisors with a need to know" alone is NOT enough.) Require deal-team ring-fence, agency consent gate, disclosure log.
3. **Data as a subclause:** if records move either direction, require the Database NDA (prohibited uses, seeding with prima facie breach presumption, security schedule, liquidated damages).
4. **Non-circumvention missing** where purpose involves introductions, brokers, members, landowners, or investors = deal-killer gap.
5. **Residuals clause** present? Strike it.
6. **AI ingestion** unaddressed? Add the bar.
7. **NC/NS expressly disclaimed?** Reverse it.
8. **Venue ceded?** Push for Bengaluru.
9. **Survival from disclosure instead of termination? Perpetual all-CI? One-way warranties?** Flag all three.
10. **Facts right:** product names, property names, meeting dates, purpose recitals must match the client's vault note exactly (AtlasFive, not "Atlas V").
11. **Site access contemplated but no premises rider?** Add it.
12. **Member/guest PII in scope but only "business contact data" permitted?** Fix the scope both ways: permit what is needed, bar the rest expressly.

### Step 6: Deliverables
- **Drafting:** .docx via the docx skill, built from the relevant master with Schedule 1/2 completed, modules toggled, and the Known Bugs fixes applied. Filename: `NDA_Champions_x_{Counterparty}_{Mutual|Database|RE|Club|Tour|Staff}_{YYYY-MM-DD}.docx`. Save to `Atlas/Clients/{client}/`; Legal folder copies stay canonical.
- **Reviewing:** vault note `Atlas/Context Docs/Legal/NDA Assessment - {Counterparty} {YYYY-MM-DD}.md`: Verdict up top (patch vs reissue-on-master), what the draft gets right, defects table in priority order, actions checklist, wikilinks throughout.
- Unresolved facts stay as visible `[CONFIRM: ...]` placeholders plus a closing "Items to confirm before sending" checklist, delivered SEPARATELY from the sendable file. Never invent entity names, addresses, dates, or terms.
- End every deliverable: "Commercial drafting for internal use, not legal advice." Recommend a counsel pass on modified clauses; India s.27 restraint-of-trade risk on NC/methodology bars is specifically flagged for counsel.

## Clause library (harvest sources when drafting)
Seeding + reversed burden of proof (EGS 6.3 / DB master 9.2) · NC fee recovery + prior-relationship notice (EGS 10.3-10.4) · deal-team ring-fence + agency consent gate + disclosure log (EGS 4.2-4.3) · residuals exclusion + no-combination (EGS/Gorisco 7) · AI outputs deemed CI (EGS 23) · LD formula + no-notice audit (DB master 13.2/9.3) · individual personnel acknowledgment table (Cirralogix vendor template) · LinkedIn Profile access/ownership/platform-compliance trio (LakeB2B archive; the only part of that form to keep) · data ownership absent SOW (Arkentech 4b) · liability-cap disapplication for confidentiality/data breaches (Moneybee 11 / Gorisco 16.2).

## Style rules
- No em-dashes anywhere.
- Defined terms capitalized and consistent; every defined term must be used.
- Plain, tight legal English. Tour NDA reads warm and human, not legalese.
- Tables for comparisons in review notes; wikilinks for vault references.

## Escalation
- PHI, MNPI, title documents, or member PII in scope: flag for counsel explicitly, not just the standard disclaimer.
- Asked to weaken Clause 4/5/10 protections, accept perpetual all-CI survival, or accept one-way warranties: present the risk in one paragraph, let the user decide, never weaken silently.
- Counterparty insists on their paper: run Step 5 against it and negotiate the gaps rather than accepting wholesale.

