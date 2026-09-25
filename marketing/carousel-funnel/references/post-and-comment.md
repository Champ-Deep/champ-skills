# Post copy, first comment, and the posting routine

The carousel does the teaching. The post copy earns the click on the document. The first comment carries the tracked link. All three ship together or the funnel has a hole in it.

## Why the link goes in the comment

LinkedIn ranks posts with an external link in the body lower than posts without one, and a document post with a body link competes with itself (the doc or the link). Put the link in the first comment, posted within a minute of the post going live, from the same account. Say "link in the first comment" on the CTA slide and in the last line of the post. Then pin the comment where the platform allows it and like it from the page.

Instagram does not link from comments or captions. The CTA slide and caption say "link in bio". Point the bio link (or the link-in-bio page) at the tracked URL with `utm_source=instagram`.

## Post copy formula (LinkedIn, 120 to 220 words)

Line 1 is the only line most people read before "see more". It is the hook slide's claim, reworded so the two are not identical, under 140 characters, no emoji, no "I" statements about being excited.

Then:

1. Two to four short lines that set up the problem in the reader's world (who, when, what goes wrong). Line breaks between them. No bullet characters.
2. One line naming what the carousel gives them and how long it takes to read ("Ten slides. Four minutes.").
3. Optional: one line of proof or a specific number from the asset.
4. Last line: "Full playbook, free and ungated, in the first comment."
5. Up to three hashtags on their own line, all specific (`#RevOps #IntentData #B2BSales`). Zero is fine.

Voice per the LakeB2B Social Media Voice and Tone Guide: declarative, specific, no performative positivity, first-person plural allowed. Run `no-ai-slop` on the copy before it ships.

## First comment (LinkedIn)

One or two lines, then the tracked URL on its own line. Example:

> The full Intent Signal Playbook (scorecard, gates, message framework, cheat sheet). No form, no sales call attached.
> https://lakeb2b.com/playbooks/intent-signals?utm_source=linkedin&utm_medium=organic-social&utm_campaign=lakeb2b_intent-signal-playbook_sep2026&utm_content=carousel_v1-comment

LinkedIn shows the raw URL in comments, so keep the path short and readable. UTMs are fine to leave visible; nobody minds. If a branded short link is used, it must 301 to the full UTM URL, never strip it.

## Replies

Everyone who comments substantively gets a reply that includes the link again with `utm_content=carousel_v1-reply`. Anyone who asks for it by DM gets `utm_content=carousel_v1-dm`. Employees who reshare use `utm_content=carousel_v1-reshare-<firstname>`. Different `utm_content` values are how the weekly report tells you which touch did the work.

## Document title

LinkedIn asks for a title when uploading the PDF. It is searchable and shows above the carousel. Use the asset name, not the hook: "The Intent Signal Playbook (LakeB2B)". Under 60 characters.

## Posting routine

1. Upload the LinkedIn PDF (`out/linkedin/<slug>-linkedin.pdf`), set the document title.
2. Paste the post copy. Check the first line reads whole on a phone.
3. Post. Within 60 seconds, add the first comment with the `-comment` link. Pin it.
4. Like the comment from the page. Ask two named colleagues to comment with a real reaction (not "great post") in the first 30 minutes and to reshare with a sentence of their own.
5. Instagram: post the ten 4:5 PNGs from `out/linkedin/` (same aspect), caption reworked to Instagram voice, "link in bio". Update the bio link to the `-bio` URL first.
6. Log the post in the tracking sheet (see `tracking-setup.md`) with the post URL, date, and every UTM variant in use.
7. Day 2 and day 7: record impressions, document opens, and average swipe depth from LinkedIn analytics next to the page sessions and identified companies for the same UTMs.

## Timing

Tuesday to Thursday, 8:30 to 10:00 in the audience's main timezone (U.S. Eastern for LakeB2B's SaaS ICP, which is 18:00 to 19:30 IST). Never Friday afternoon. One document carousel per week per page at most; more and each one cannibalises the last.
