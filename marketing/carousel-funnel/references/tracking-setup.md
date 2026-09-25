# Landing page, UTMs, and visitor intelligence

A carousel that sends people to a PDF is a carousel you cannot measure. Set the page and the tracking up before the post goes live, not after. This file is the checklist and the naming standard. Each item names an owner role so the team can split it.

## 1. The playbook page (owner: web or content)

The full asset lives on the brand site as an HTML page, not as a PDF link. Three reasons: visitor identification scripts cannot run inside a PDF, UTMs on a PDF URL never reach analytics, and an HTML page can be read on a phone straight from the LinkedIn app. Offer the PDF as a download at the bottom of the page, and track the download as an event.

Path convention: `/playbooks/<slug>` (for guides), `/reports/<slug>` (for data reports), `/case-studies/<slug>`. For the worked example: `https://lakeb2b.com/playbooks/intent-signals`.

Build the page with `pdf-to-html` (faithful conversion) or `visual-report-builder` (re-flowed, editorial), then `page-refresh` if it needs the brand's design language. Page must have:

- Title, one-line summary, and reading time above the fold. No hero image that pushes the content down.
- A sticky or top-of-page table of contents so the eight chapters are jumpable.
- Ungated. No form before the content. The only form on the page is optional: "Email me the PDF" at the end, which also creates a known contact for the visitor-intelligence match.
- One CTA at the end matching the asset's own CTA (for the playbook: book the 15-minute revenue growth strategy call).
- The download-PDF link tagged `data-event="playbook_download"` and the CTA tagged `data-event="playbook_cta_click"` so GA4 and Factors can pick them up as events.
- Open Graph tags so the URL unfurls with the hook slide as the image (1200 x 630 crop of slide 1).
- The visitor-intelligence script and GA4 present in the head (see sections 3 and 4). Verify with the browser's network tab before publishing.

## 2. UTM standard (owner: whoever posts)

House convention, generated and registered in ChampUTM so every brand's links are in one place:

```
{page_url}?utm_source={source}&utm_medium={medium}&utm_campaign={company}_{initiative}_{monthYYYY}&utm_content={format}_{variant}
```

| Parameter | Values for carousel work |
|---|---|
| `utm_source` | `linkedin`, `instagram`, `x`, `whatsapp`, `email` |
| `utm_medium` | `organic-social` for page and employee posts, `paid-social` for boosted, `dm` for direct messages |
| `utm_campaign` | `{brand}_{asset-slug}_{monYYYY}`, lowercase, hyphens inside segments, underscores between them. Example: `lakeb2b_intent-signal-playbook_sep2026` |
| `utm_content` | `carousel_v{n}-{touch}` where touch is `comment`, `reply`, `dm`, `bio`, `reshare-{firstname}`, `story` |

Rules: never change `utm_campaign` for the same asset within a month (it splits the report). Bump `v{n}` only when the slides change. Every link the team shares for this asset carries a UTM; a bare URL is a lost data point. Register each URL in ChampUTM with the post URL it appears on.

Complete set for the worked example:

```
https://lakeb2b.com/playbooks/intent-signals?utm_source=linkedin&utm_medium=organic-social&utm_campaign=lakeb2b_intent-signal-playbook_sep2026&utm_content=carousel_v1-comment
https://lakeb2b.com/playbooks/intent-signals?utm_source=linkedin&utm_medium=organic-social&utm_campaign=lakeb2b_intent-signal-playbook_sep2026&utm_content=carousel_v1-reply
https://lakeb2b.com/playbooks/intent-signals?utm_source=linkedin&utm_medium=dm&utm_campaign=lakeb2b_intent-signal-playbook_sep2026&utm_content=carousel_v1-dm
https://lakeb2b.com/playbooks/intent-signals?utm_source=instagram&utm_medium=organic-social&utm_campaign=lakeb2b_intent-signal-playbook_sep2026&utm_content=carousel_v1-bio
```

## 3. Website visitor intelligence with Factors.ai (owner: marketing ops)

Factors.ai is the standard for LakeB2B. It identifies the company behind anonymous visits, ties sessions to UTMs, and pushes matched accounts to the CRM. Setup, once per site:

1. Install the Factors tracking snippet on every page of the site through the tag manager (or the site head if there is no tag manager). Do not install it only on the playbook page: identification quality depends on seeing the whole visit.
2. Verify the domain in Factors and confirm events are arriving from a test visit that carries a UTM. Check that `utm_source`, `utm_medium`, `utm_campaign` and `utm_content` show up as session properties on that visit.
3. Turn on company identification (de-anonymisation) and connect the CRM so identified companies land against existing accounts rather than creating duplicates.
4. Create a saved segment per asset: sessions where the page path is the asset's path, grouped by `utm_campaign` and `utm_content`. Name it the same as the `utm_campaign` value.
5. Create an ICP filter on top of the segment (industry, employee band, geography, the same fit gate the playbook describes) so the alert only fires for accounts worth a rep's time.
6. Route ICP-fit identified companies to a Slack channel or CRM list within the hour, with the page they read and the UTM that brought them. This list is the "Engagement" and "Recency" input for the intent scorecard, which is the whole point of the loop.
7. Weekly: export identified companies by `utm_content` into the tracking sheet (section 5).

If a brand other than LakeB2B has no Factors seat, the same steps apply to whichever identification tool it uses; the segment and ICP filter are the non-negotiable parts.

Guardrail, lifted straight from the playbook: visitor identification tells the SDR which account to look at, never what to say. "I saw you read our intent playbook" is off limits. The follow-up references a public trigger and a plausible problem, exactly as chapter 6 prescribes.

## 4. GA4 (owner: marketing ops)

Factors covers who; GA4 covers how many and how far. On the playbook page, make sure these fire: `page_view` (default), `scroll` at 25, 50, 75, 90 percent (enhanced measurement), `playbook_download` and `playbook_cta_click` (custom events from the data attributes in section 1). Mark the two custom events as key events. Build one exploration: sessions by `utm_content` with scroll depth and key events as columns. That is the page-side half of the weekly report.

## 5. The tracking sheet and the weekly read (owner: whoever posts)

One row per post, in the brand's social tracking sheet. Columns:

`date, brand, asset, post_url, platform, utm_campaign, impressions_d2, doc_opens_d2, avg_swipe_depth_d2, link_clicks_d2, page_sessions_d2, identified_companies_d2, icp_fit_companies_d2, tier1_handoffs, impressions_d7, doc_opens_d7, page_sessions_d7, identified_companies_d7, icp_fit_companies_d7, notes`

The funnel that matters, in order: impressions, document opens, swipe depth past slide 5, comment link clicks, page sessions with the UTM, identified companies, ICP-fit companies, Tier 1 handoffs. If opens are high and sessions are low, the CTA slide or the comment is the problem. If sessions are high and identified companies are low, the visitor-intelligence install is the problem. If identified companies are high and ICP fit is low, the hook attracted the wrong crowd and the next carousel's hook should name the ICP.

Report the weekly read as a five-line note, not a dashboard: what was posted, the three numbers that moved, the one thing to change next week.
