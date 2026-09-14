# PRD Template — CHAMP Framework

Use this template when the user requests a PRD after a Product-mode brainstorming session.
This is a feasibility-focused PRD designed for MVP planning and the journey from MVP to
milestones. It should feel like a battle-tested plan, not a wish list.

---

```markdown
# Product Requirements Document: [Product Name]

**Version:** 1.0 — MVP
**Author:** [User Name]
**Date:** [Date]
**Status:** Draft — Post-CHAMP Brainstorm

---

## 1. Problem Statement

[2-3 paragraphs. State the problem from the customer's perspective. Use their language.
Include the emotional and practical dimensions of the problem. Reference specific customer
insights from the C (Customer) phase of the brainstorm.]

### 1.1 Who Has This Problem?

**Primary Persona:**
- **Name/Archetype:** [e.g., "The Overwhelmed Solo Founder"]
- **Demographics:** [Age, location, role, company stage]
- **Behavioral Traits:** [How they currently cope, tools they use, habits]
- **Quote:** [A representative thing this person would say about their problem]

**Secondary Segments:**
[List 2-3 additional segments with brief differentiators]

### 1.2 Current Alternatives & Their Failures

| Alternative | What It Does Well | Where It Fails |
|------------|-------------------|----------------|
| [Competitor/Workaround 1] | [Strength] | [Gap] |
| [Competitor/Workaround 2] | [Strength] | [Gap] |
| [Do Nothing] | [Why people tolerate the status quo] | [Cost of inaction] |

---

## 2. Product-Market Fit Hypothesis

> "We believe [customer segment] will [desired behavior] because [unique value proposition]."

**Riskiest Assumption:** [From the H phase]

**Validation Method:** [How the MVP will test this — specific experiment design]

**Success Signal:** [What data point confirms product-market fit?]

**Failure Signal:** [What data point disproves it?]

---

## 3. Solution Overview

### 3.1 Core Value Proposition

[1-2 sentences. What does this product do and why should anyone care?]

### 3.2 Key Features — MVP Scope

| Feature | Priority (P0/P1/P2) | Description | Rationale |
|---------|---------------------|-------------|-----------|
| [Feature 1] | P0 | [What it does] | [Why it's essential for the hypothesis test] |
| [Feature 2] | P0 | [What it does] | [Why it's essential] |
| [Feature 3] | P1 | [What it does] | [Nice to have for MVP, critical for M1] |
| [Feature 4] | P2 | [What it does] | [Post-MVP, drives retention/growth] |

### 3.3 Explicitly Out of Scope for MVP

[List features or capabilities that are intentionally deferred. This is as important as
what's in scope — it prevents scope creep and keeps the team focused.]

- [Feature/capability] — Deferred to [Milestone X] because [reason]
- [Feature/capability] — Deferred to [Milestone X] because [reason]

---

## 4. User Journey

```
[Discovery] → [First Touch] → [Signup/Onboarding] → [Aha Moment] → [Habit Loop] → [Expansion]
```

**Critical Path (MVP):**
1. [Step 1: How user discovers the product]
2. [Step 2: First interaction — what happens in the first 30 seconds]
3. [Step 3: The "aha moment" — when the value becomes undeniable]
4. [Step 4: What brings them back]

---

## 5. Technical Approach

### 5.1 Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | [Framework] | [Why this choice] |
| Backend | [Framework/Language] | [Why this choice] |
| Database | [Database] | [Why this choice] |
| Infrastructure | [Cloud/Hosting] | [Why this choice] |
| Key APIs/Services | [List] | [What they enable] |

### 5.2 Architecture Overview

[Brief description of the system architecture. Include a simple diagram description
if helpful — e.g., "Client → API Gateway → Microservices → DB" or similar.]

### 5.3 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Plan] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Plan] |

---

## 6. Cost Estimate

### 6.1 Build Cost (MVP)

| Category | Estimate | Notes |
|----------|----------|-------|
| Engineering | [Cost/Hours] | [Team size, duration] |
| Design | [Cost/Hours] | [Scope of design work] |
| Infrastructure (monthly) | [Cost] | [Hosting, APIs, services] |
| Third-party services | [Cost] | [SaaS tools, licenses] |
| **Total MVP Build** | **[Total]** | |

### 6.2 Ongoing Monthly Cost (Post-Launch)

| Category | Monthly Estimate |
|----------|-----------------|
| Infrastructure | [Cost] |
| Third-party services | [Cost] |
| Support/Maintenance | [Cost] |
| **Total Monthly** | **[Total]** |

---

## 7. Success Metrics

| Metric | Type | Target (MVP) | Target (M1) | Measurement |
|--------|------|-------------|-------------|-------------|
| [North Star Metric] | North Star | [Target] | [Target] | [How] |
| [Leading Indicator 1] | Leading | [Target] | [Target] | [How] |
| [Leading Indicator 2] | Leading | [Target] | [Target] | [How] |
| [Guardrail Metric] | Guardrail | [Threshold] | [Threshold] | [How] |

---

## 8. Market & Positioning

**TAM:** [Total Addressable Market with logic]
**SAM:** [Serviceable Addressable Market]
**SOM:** [Serviceable Obtainable Market — realistic Year 1]

**Positioning Statement:**
For [target customer], [product name] is the [category] that [key benefit],
unlike [primary competitor], because [reason to believe].

**Competitive Differentiation:**
[2-3 sentences on what makes this genuinely different — not "better UI" but a
structural or strategic advantage]

---

## 9. Timeline & Milestones

### MVP → Launch

| Week | Focus | Deliverable | Gate Criteria |
|------|-------|-------------|---------------|
| 1-2 | [Phase] | [Deliverable] | |
| 3-4 | [Phase] | [Deliverable] | |
| 5-6 | [Phase] | [Deliverable] | |
| 7-8 | [Phase] | **MVP Launch** | [What must be true to launch] |

### Post-MVP Milestones

| Milestone | Target Date | Key Features | Gate to Next |
|-----------|------------|--------------|--------------|
| M1: [Name] | [Date] | [Features] | [Criteria to proceed] |
| M2: [Name] | [Date] | [Features] | [Criteria to proceed] |
| M3: [Name] | [Date] | [Features] | [Criteria to proceed] |

---

## 10. Pivot Strategy

**Pivot Triggers:**
- [Metric] falls below [threshold] for [duration]
- [Qualitative signal] observed in [number] user interviews
- [Market event] changes the competitive landscape

**Pivot Options:**

| Trigger | Pivot Direction | What Changes | What Stays |
|---------|----------------|-------------|------------|
| [Trigger 1] | [New direction] | [Scope/audience/model shift] | [Core assets preserved] |
| [Trigger 2] | [New direction] | [Scope/audience/model shift] | [Core assets preserved] |

**Kill Criteria:**
[The specific conditions under which the project should be shelved entirely.
Be honest and specific — this is what separates disciplined founders from stubborn ones.]

---

## Appendix

### A. CHAMP Brainstorm Session Notes
[Link to or embed the full brainstorm capture from each CHAMP letter]

### B. Research & References
[Any market research, competitor analysis, or data sources referenced]

---

*Generated via CHAMP Framework — Champions Accelerator*
```
