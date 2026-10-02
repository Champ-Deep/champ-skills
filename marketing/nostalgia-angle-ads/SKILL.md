---
name: "nostalgia-angle-ads"
description: "Turn a campaign theme into ad concepts by borrowing a world the buyer grew up with and mapping its objects to their data pain, then A/B test two looks per brand (the LakeB2B and Span Q4 2026 method). Use for ad concepts, quarterly themes, retro creative or display ads."
---

# Nostalgia angle ads

This skill teaches the method behind the Q4 2026 LakeB2B and Span ads so the team can reuse it with any theme or brand. Borrow a world the buyer already knows by heart, find the objects in that world that already look like their problem, and let each object carry one headline and one action. A stack of burned CDs labelled `leads_FINAL_v2.csv` explains flat-file chaos faster than any sentence about "data hygiene". A dial-up dialog explains a slow, half-broken CRM. "Your CRM survived Y2K. Did your contacts?" explains data decay with a joke the buyer gets in one second.

When the team can't agree on a world, don't vote. Build the same pain points in two worlds and let a LinkedIn A/B test pick the look that converts (step 4).

Follow the steps in order. Most weak ads come from skipping step 3 (the angle map) and jumping straight to pictures.

## Why this works (keep these in mind when making judgment calls)

- **Recognition beats explanation.** Millennial decision makers (roughly 30 to 45 in 2026) and the Gen X leaders above them recognise a burned CD, a dial-up dialog or a continue screen instantly. If the object already looks like the pain, the ad needs no explaining copy.
- **The joke lands on the situation, never on the buyer.** Laugh at the old way of working and invite the buyer out of it. Ads that mock the buyer get scrolled past or resented.
- **One idea per ad.** One object, one headline, one action. Apollo built eight creatives from a single sentence in its 1995 campaign; repetition with variation is what makes a theme stick.
- **The action lives in the picture.** A sticker, price tag or coin inside the image reads as the next step before the viewer reaches the platform's button.
- **Pain points are fixed; worlds are swappable.** Decide the pain point and rough CTA for each ad first. The world only changes how the pain looks. That is what makes a two-world test readable.
- **The offer never changes inside a brand.** For LakeB2B in Q4 2026 every ad sells "send 10 names, get them back complete"; every Span ad asks for its free sample list. Changing the offer per ad makes the test unreadable.

## Step 1. Collect the inputs

Ask for or find these before generating anything. The Celsus vault (`Efforts/Active/`) and the brand skills usually hold most of them.

1. Brand, its positioning this quarter, and its brand skill (for example `lakeb2b-brand-guidelines`, `span-brand-guidelines`).
2. The one offer per brand and the landing page it goes to. If the page does not exist yet, say so; ads that send clicks to an unfinished page waste the budget and turn an A/B test into a click test.
3. The buyer's roles, industries and rough age band.
4. Three to five pain points per brand, each with a rough CTA (an offer, not final copy), in the buyer's own words (bounced emails, people who left, flat files nobody trusts, missing direct dials, not knowing a prospect's tech stack).
5. The world or the two candidate worlds, if already chosen.
6. Competitor check: open the LinkedIn Ad Library for the main competitor and note which props and devices they are using this quarter. Those are off limits for us.
7. Channels and sizes: LinkedIn single image 1200x1200, Google responsive display 1200x1200 and 1200x628.
8. Test budget. A LinkedIn A/B test needs at least $700 per brand for two weeks. If nobody has agreed where that money comes from, flag it before building.

## Step 2. Pick the world (or two)

A good world has three properties: the buyer lived in it, it is full of physical or on-screen objects, and its objects carry a feeling (warmth, mild alarm, play). Worlds that worked:

| Theme | World borrowed | Feeling |
|---|---|---|
| Retro Music | Burned CDs with marker labels, cassettes and J-cards, mixtapes, record labels, track lists | Warm and personal; fits white-glove service |
| Retro Gaming | 16-bit screens, arcades, invented consoles, save files, power-ups, continue screens, lobbies | Play and progress; fits self-serve and tech buyers |
| Y2K computing | 1999 to 2002: dial-up, millennium bug, instant messenger buddy lists | Warm nostalgia with a wink |
| Best Before | Neighbourhood supermarket and deli: date stamps, food labels, fridge leftovers | A small jolt, then relief |

Pick a different slice of an era when a competitor owns the obvious one. Apollo owned 1995 (beige PCs, corded phones, Windows 95) in late 2026, so LakeB2B moved to music objects and 16-bit games.

Worlds to leave out: anything that copies one franchise (GTA-style crime games were raised and dropped for IP risk), slot machines and casino imagery (LinkedIn reviews gambling content), and any real console, player or album.

## Step 3. Mine the world and build the angle map

List 15 to 25 objects, interfaces, rituals and phrases from the world. Then build an angle map, one row per pain point:

| Pain point (fixed) | Rough CTA (fixed) | Object from the world | Headline (in-world language, 8 words or fewer) | CTA in the image (2 to 5 words) |
|---|---|---|---|---|

Keep a row only when it passes all four tests:

1. **No explaining needed.** The object already looks like the pain. Burned CDs with `FINAL_v2` labels pass. A floppy disk "because data" fails.
2. **The offer fixes it.** The CTA in the image must be the brand's real offer in the world's language ("Insert 10 names", "Send 10 names instead", "Check 10 records free").
3. **The buyer would say "that's us".** Test it on someone in sales or marketing ops.
4. **Nobody else owns it this quarter.** Check the competitor notes from step 1.

If one world can't produce a passing row for a pain point, borrow from a neighbouring set before dropping the pain point (the Q4 gaming arm reused the New Game+ continue screen and power-up ads for two LakeB2B rows).

## Step 4. Build the two-arm A/B matrix

When two worlds are in play, make one ad per pain point in each world. Everything except the image stays identical across the pair: pain point, offer, post copy, platform headline and button. The in-image headline changes only to speak the world's language. That way the test measures the look and nothing else.

Worked matrix, Q4 2026 (Arm A Retro Music, Arm B Retro Gaming):

LakeB2B, API enrichment ("why send a file when you can do it securely"):

| # | Pain point | Rough CTA | Arm A headline | Arm B headline |
|---|---|---|---|---|
| L1 | Sharing contact files is slow and insecure | Send 10 names instead (no file) | Still emailing leads_FINAL_v2.csv? | Stop trading save files. Go online. |
| L2 | Holiday campaigns going to people who left | Check 10 records free | Holiday wishes to an empty inbox? | Holiday wishes to an empty inbox? |
| L3 | Contacts changed companies and titles | Find who moved | Your contacts signed with new labels. | Continue? Your CRM has three lives left. |
| L4 | Records missing emails, dials and titles | Fill 10 records free | Missing tracks? We fill them in. | Your pipeline needs a power-up. |

Span, tech and SaaS data:

| # | Pain point | Rough CTA | Arm A headline | Arm B headline |
|---|---|---|---|---|
| S1 | Pitching without knowing the prospect's tech stack | Free tech list sample | Know their playlist before you pitch. | Scout their loadout before you pitch. |
| S2 | Finding companies that use a competitor's product | Get a competitor list | Find every fan of your competitor. | See who plays for the other team. |
| S3 | New SaaS and AI tools launch every week | Get this week's list | New releases every week. Reach them first. | New players joined the lobby this week. |

Before a row goes in, confirm the brand can deliver the offer (S3 needed a yes on a weekly new-launch list). If a pain point gets swapped, both arms change together.

### Single-world angle maps (for refreshes and bench ads)

Y2K computing:

| Object | Pain | Headline | CTA |
|---|---|---|---|
| Dial-up connection dialog | Slow, failing CRM records | Your CRM still sounds like dial-up. | Enrich 10 records free |
| Millennium bug countdown | The system survived, the people moved | Your CRM survived Y2K. Did your contacts? | Run a free record check |
| A mix made by hand | Custom, white-glove lists | We still make lists by hand. | Get your sample mix |
| Buddy list going offline | Contacts who left | Some of your contacts signed off years ago. | Find who is still online |

Best Before:

| Object | Pain | Headline | CTA |
|---|---|---|---|
| Best-before stamp on a rolodex card | Records expire quietly | Your CRM has a best-before date. | Free freshness check |
| Nutrition label ("Contact Facts") | Buying a list blind | Read the label before you buy a list. | See a sample label |
| Fridge leftovers labelled leads_2021 | Old event and webinar lists | Some lists don't keep. | Swap 10 for fresh |
| Deli package, packed to order | Custom, white-glove lists | Custom lists, packed to order. | Get your sample |
| Holiday end cap | Consumer audiences at peak | Holiday audiences, packed fresh for Black Friday. | Free sample audience |

New Game+ (now folded into Retro Gaming):

| Object | Pain | Headline | CTA |
|---|---|---|---|
| Character select of buyer roles | Choosing target personas | Choose your players for 2027. | Build my roster |
| Save point | Year-end cleanup | Save your progress before 2027. | Free record check |
| Bonus stage | Consumer peak season | Bonus level: Black Friday audiences. | Free sample audience |

## Step 5. Write the copy

For each row, write:

- **Headline in the image:** the angle map headline, unchanged.
- **CTA in the image:** the rough CTA in the world's language, styled as an object from the world (gold starburst or CD sticker for music, pixel coin or badge for games, price-gun label for the supermarket).
- **Post copy:** two or three sentences, shared by both arms. The pain in plain words, the offer, one line of proof ("a person checks every contact"). Keep it under about 150 characters before the "see more" cut where possible.
- **Platform headline:** the offer in five to seven words, shared by both arms. Don't repeat the post copy's wording; the lint flags it.
- **Google responsive display text:** short headlines of 30 characters or fewer, long headlines of 90 or fewer, descriptions of 90 or fewer. Count the characters with a script.

Copy rules that matter here:

- No numbers we cannot prove. "Half your contacts left" is a claim; "Some of your contacts signed off years ago" is not. Freshness promises ("updated daily") need evidence first.
- No promise of a product that isn't live. In Q4 2026 no ad could promise API access until the docs existed, so "no file" and "synced securely" carried the API idea.
- No em dashes or en dashes anywhere, including image text. Run the `no-ai-slop` skill (and `slop_lint.py`) as the last gate on all copy.
- Never name a competitor, a real product, a game, a console, an artist or a celebrity in copy or image prompts.

## Step 6. Design rules for the image

- **The world fills the frame.** Staged photo (a 2000-era portrait, a holiday table, a record shop) or a full-screen invented interface (a dialog box, an item menu, a game lobby). Avoid a flat brand background with a prop pasted on.
- **Diegetic text carries the joke.** Marker labels on CDs, rows in a track list, items in an RPG menu, a "message could not be delivered" box. These small in-world details are what make the ad feel made by hand.
- **One headline, top of frame,** in a type style native to the world: chrome bubble letters for music and Y2K, pixel arcade type for games, hand-painted shop-sign lettering for the supermarket.
- **Brand palette as the light.** Tint the world with the brand colors instead of adding brand graphics.
  - LakeB2B: purple #6D08BE, gold #FFB703, magenta #DD1286, red #E8033A. Bottom band navy #0E1131.
  - Span: green #1B6B3A, light green #3DBE6E, teal #00D4AA, amber #F5A623 for the CTA. Bottom band navy #0F2B3C. Fonts Montserrat and Inter.
- **Reserve the bottom 11% as a flat navy band.** The real logo goes there later. Never let the image model draw the logo.
- **Invent every interface, product and company.** No real operating system chrome, game characters, console or controller shapes, album art, packaging or wallpapers. Company names on screens must be invented too (a draft once showed real company names and had to be edited to names like Larkspur Health and Quillfield Cloud). Search any new name before launch. If a draft looks like a real product, regenerate it.

Also make one or two **brand-style variations** that carry the strongest message in the brand's own house look. For LakeB2B that is the brand book's social post system: black field, a neon-lit person on the right holding a prop from the world, the logo's orange-to-purple loop line, Montserrat headline in white and gold on the left, orange web address. Keep these on the bench and run one against the winning arm later if the team wants to check theme against house style.

## Step 7. Generate in Higgsfield

Use the Higgsfield MCP.

1. Create or reuse one project per campaign (`create_project`, then pass its `default_folder_id` as `folder_id` on every generation).
2. Model `gpt_image_2_5`, `quality: high`, `resolution: 2k`, `aspect_ratio: 1:1`. It renders headline and label text well. A high 2k image costs about 2.75 credits.
3. Submit one or two jobs at a time with `generate_image_batch`. Larger batches hit `429 rate_limit_reached` on most items. Wait with `jobs_wait`, then send the next one or two.
4. Prompt template for a themed ad:

```
Square LinkedIn ad, [world and era] [photo or full-screen interface] style.
[Scene: the object, where it sits, what it looks like, lighting, grain.]
[Diegetic text: every label, row or menu item in quotes, exactly as it should read.]
Brand palette as light and props: [brand hex colors].
Top of the image: large [world-native lettering style] headline reading exactly: '[line 1]' / '[line 2]'.
Lower right: a [gold or amber] [starburst sticker | CD sticker | pixel coin badge | price-gun label] with bold black text '[CTA]'.
The bottom 11% of the image is a flat solid deep navy ([band hex]) band with nothing in it.
All company names, products and characters are invented. No logos, no brand names, no real products, games, consoles, characters or trademarks, no other text.
```

5. Prompt template for a brand-style background: describe the person, the neon lighting, the prop and the loop line, and end with "The left 45% of the image is clean empty black space. No text, no letters, no logos anywhere." The text goes on in step 8.
6. Review every result at full size for: misspelled words in labels (the model wrote "Demond" and "RevOfs" in early drafts), garbled background text, real company names, props that look like real products (an early controller looked like a real console's), and anything that reads as a different product (a "FRESH CONTACTS" box once came out looking like contact lens packaging).
7. Fix small errors with an edit instead of a re-roll: call `generate_image` with the bad job id as `medias: [{value: <job_id>, role: "image_references"}]` and a prompt that says "Edit this exact image. Change only ... Keep every other element exactly the same."

## Step 8. Finish the files

Composite the real logo and export in code so the brand marks are exact.

- **Logo:** use the brand's own file. For LakeB2B, take it from the brand book PDF (page 5, the full-color logo on navy), render at 600 dpi, crop, and remove the navy background with a color-to-alpha step. Logos may sit only on approved backgrounds (white, light grey, purple, navy). The vault had no Span logo file in Q4 2026, so Span ads carried a "SPAN / GLOBAL SERVICES" wordmark placeholder; swap in the official logo before launch.
- **Band:** draw a navy band over the reserved bottom area with the logo on the left and the web address on the right (lakeb2b.com, spanglobalservices.com). Detect the band height from the image (scan up from the bottom until rows stop matching the band color) so the overlay covers it exactly.
- **Brand-style text:** an HTML overlay with Montserrat 800 to 900 headline (white, second line gold), a short sub line, a gold pill CTA, the logo top left and the orange web address bottom left, with a left-to-right black scrim so the text stays readable over the neon line.
- **Render** each ad as a small HTML page and screenshot it with Playwright at 1200x1200 (and 1200x628), saving JPG at quality 92.
- **Landscape:** make 1200x628 only for the winning arm. Use Higgsfield `outpaint_image` at 21:9 or 16:9 on the square job id, then crop to 1.91:1 with `background-size: cover`. Check each result: outpainting sometimes recomposes the scene, shrinks the navy band, invents unreadable background signs, or pushes the headline to the edges. Fixes that worked: shift the crop position, use a navy tab across only the left half for the logo, or place the logo directly on the existing band.

## Step 9. Plan the test

Two-arm LinkedIn test (the default when two worlds are in play):

- LinkedIn Campaign Manager A/B test, one per brand, with the creative as the variable.
- 14 days minimum, and a $700 floor per two-week test; plan about $1,500 per brand so each arm gets enough delivery.
- An audience of 300,000 members or more per test.
- Judge on cost per sample request in the CRM, not on clicks. Click-through only breaks ties.
- No edits for 14 days. Mid-flight edits are why LinkedIn produced nothing in earlier quarters.
- If the arms finish within about 10%, let each brand keep the arm that fits its buyer.
- After the read, the winning look goes to Google display, social, nurture and the next month's ads. The losing arm's best ad stays as a refresh.

Google display pairs (when running single-world sets):

- Same budget per ad; pairs that answer one question each (energy versus fatigue in the same scene, themed versus brand style on the same message).
- At about 3,000 impressions per ad, pause anything under half the median click-through rate, then judge survivors on cost per sample request in the CRM.

## QA checklist before anything is shared

- [ ] Both arms of every pair carry the same pain point, offer, post copy, platform headline and button.
- [ ] Every offer's landing page is live, and the brand can deliver what the CTA promises.
- [ ] Headline, CTA and every diegetic label are spelled correctly at full size.
- [ ] No real products, interfaces, games, characters, consoles, artists, competitor names or real company names, in image or copy.
- [ ] No prop or device the main competitor is running this quarter; no franchise look-alikes or gambling imagery.
- [ ] No unprovable numbers, guarantees or promises of unreleased products.
- [ ] Real logo, approved background, minimum 180 px wide in digital (placeholder wordmarks swapped).
- [ ] No em dashes or en dashes in any file; `no-ai-slop` run on all copy.
- [ ] Google text lengths counted with a script.
- [ ] Test budget agreed and owner named for setup.

## What to deliver

1. An A/B board artifact: a test design card and the open decisions up top, then one tab per brand with one row per pain point (pain point, rough CTA, post copy and headline with copy buttons, Arm A and Arm B side by side), plus a bench tab for ads outside the test. Full width, never a narrow centered column, and stacked arms on phones.
2. A copy document as the same matrix (pain point, CTA, Arm A file and headline, Arm B file and headline, post copy, platform headline) with the test design and the before-launch list.
3. Final JPGs and the copy document saved in Celsus under `Efforts/Active/<effort name>/Ads/`, and the effort note updated with what changed.
4. The Higgsfield project name, so designers can rework the raw images.
5. A short recommendation: which arm you expect to win and why, and what has to be true before launch (budget, live pages, logo, deliverable offers).