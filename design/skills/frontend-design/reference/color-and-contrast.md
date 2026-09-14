# Color & Contrast

## Color Spaces: Use OKLCH

**Stop using HSL.** Use OKLCH (or LCH) instead. It's perceptually uniform, meaning equal steps in lightness *look* equal—unlike HSL where 50% lightness in yellow looks bright while 50% in blue looks dark.

The OKLCH function takes three components: `oklch(lightness chroma hue)` where lightness is 0-100%, chroma is roughly 0-0.4, and hue is 0-360. To build a primary color and its lighter / darker variants, hold the chroma+hue roughly constant and vary the lightness — but **reduce chroma as you approach white or black**, because high chroma at extreme lightness looks garish.

The hue you pick is a brand decision and should not come from a default. Do not reach for blue (hue 250) or warm orange (hue 60) by reflex — those are the dominant AI-design defaults, not the right answer for any specific brand.

## Building Functional Palettes

### Tinted Neutrals

**Pure gray is dead.** A neutral with zero chroma feels lifeless next to a colored brand. Add a tiny chroma value (0.005-0.015) to all your neutrals, hued toward whatever your brand color is. The chroma is small enough not to read as "tinted" consciously, but it creates subconscious cohesion between brand color and UI surfaces.

The hue you tint toward should come from THIS project's brand, not from a "warm = friendly, cool = tech" formula. If your brand color is teal, your neutrals lean toward teal. If your brand color is amber, they lean toward amber. The point is cohesion with the SPECIFIC brand, not a stock palette.

**Avoid** the trap of always tinting toward warm orange or always tinting toward cool blue. Those are the two laziest defaults and they create their own monoculture across projects.

### Palette Structure

A complete system needs:

| Role | Purpose | Example |
|------|---------|---------|
| **Primary** | Brand, CTAs, key actions | 1 color, 3-5 shades |
| **Neutral** | Text, backgrounds, borders | 9-11 shade scale |
| **Semantic** | Success, error, warning, info | 4 colors, 2-3 shades each |
| **Surface** | Cards, modals, overlays | 2-3 elevation levels |

**Skip secondary/tertiary unless you need them.** Most apps work fine with one accent color. Adding more creates decision fatigue and visual noise.

### The 60-30-10 Rule (Applied Correctly)

This rule is about **visual weight**, not pixel count:

- **60%**: Neutral backgrounds, white space, base surfaces
- **30%**: Secondary colors—text, borders, inactive states
- **10%**: Accent—CTAs, highlights, focus states

The common mistake: using the accent color everywhere because it's "the brand color." Accent colors work *because* they're rare. Overuse kills their power.

## Curated Palette Database (161 Palettes)

### Category 1: Professional / SaaS (24 palettes)
1. **Slate Pro** — oklch(25% 0.01 250) base, blue-tinted neutrals, indigo accent
2. **Carbon Dark** — oklch(15% 0.008 220) base, cool gray, electric blue
3. **Notion White** — oklch(98% 0.005 80) base, warm cream, black accent
4. **Linear Blue** — oklch(20% 0.015 255) base, deep blue, purple accent
5. **Vercel Dark** — oklch(10% 0.005 240) base, near-black, white accent
6. **Stripe Purple** — oklch(97% 0.003 280) base, lavender tint, indigo CTA
7. **PostHog Orange** — oklch(98% 0.004 70) base, warm white, orange #F54E00
8. **Supabase Green** — oklch(12% 0.01 160) base, dark green, neon green accent
9. **PlanetScale Blue** — oklch(8% 0.01 240) base, deep navy, bright blue
10. **Loom Coral** — oklch(97% 0.005 30) base, soft coral tint, salmon CTA
11. **Figma Dark** — oklch(18% 0.008 240) base, charcoal, bright purple
12. **Miro Yellow** — oklch(96% 0.006 90) base, warm white, vivid yellow
13. **Airtable Purple** — oklch(96% 0.004 280) base, lavender hint, grape CTA
14. **Intercom Blue** — oklch(97% 0.003 240) base, white, cobalt blue
15. **HubSpot Orange** — oklch(97% 0.004 50) base, warm, vibrant orange
16. **Salesforce Blue** — oklch(97% 0.003 220) base, ice white, Azure blue
17. **Zendesk Green** — oklch(97% 0.004 160) base, mint tint, forest green
18. **Atlassian Blue** — oklch(97% 0.003 240) base, clean white, royal blue
19. **Monday Yellow** — oklch(15% 0.008 240) base, dark charcoal, hot pink
20. **Asana Red** — oklch(97% 0.004 20) base, pink-white tint, vibrant coral
21. **Webflow Blue** — oklch(12% 0.015 240) base, deep navy, electric blue
22. **Framer Purple** — oklch(10% 0.012 280) base, dark purple, vivid violet
23. **Retool Dark** — oklch(16% 0.009 235) base, dark slate, cyan accent
24. **Amplitude Blue** — oklch(96% 0.005 240) base, cool white, electric blue

### Category 2: Developer Tools (16 palettes)
25. **Terminal Green** — oklch(8% 0.005 150) base, near-black, phosphor green
26. **VS Code Dark** — oklch(14% 0.007 230) base, charcoal, blue accent
27. **Dracula** — oklch(18% 0.012 275) base, dark purple, pink/cyan contrast
28. **Nord** — oklch(20% 0.015 220) base, arctic blue-gray, frost accents
29. **Monokai** — oklch(15% 0.008 250) base, charcoal, vivid multi-accent
30. **Catppuccin Mocha** — oklch(17% 0.01 265) base, mauve undertone, pastel accents
31. **One Dark** — oklch(16% 0.009 245) base, steel gray, rainbow syntax
32. **GitHub Dark** — oklch(12% 0.005 230) base, dark navy, blue CTA
33. **Raycast Dark** — oklch(10% 0.008 250) base, near-black, orange accent
34. **Warp Terminal** — oklch(12% 0.01 260) base, deep blue-black, teal
35. **Cursor Dark** — oklch(11% 0.007 240) base, dark slate, muted blue
36. **Tabnine Dark** — oklch(14% 0.009 250) base, dark navy, purple accent
37. **Windsurf Dark** — oklch(13% 0.01 245) base, deep slate, cyan
38. **Sourcegraph** — oklch(15% 0.011 255) base, dark purple, violet accent
39. **Sentry Dark** — oklch(12% 0.007 235) base, charcoal blue, hot pink
40. **Datadog Orange** — oklch(15% 0.008 240) base, dark, vibrant orange

### Category 3: Fintech / Finance (16 palettes)
41. **Trust Green** — oklch(97% 0.003 160) base, clinical white, forest green
42. **Wise Teal** — oklch(97% 0.004 180) base, teal-white, vibrant teal
43. **Revolut Black** — oklch(10% 0.005 240) base, near-black, neon gradient
44. **Coinbase Blue** — oklch(96% 0.004 230) base, clean white, Coinbase blue
45. **Stripe Violet** — oklch(97% 0.003 280) base, lavender-white, indigo
46. **PayPal Blue** — oklch(97% 0.003 215) base, white, royal blue + gold
47. **Klarna Pink** — oklch(97% 0.005 350) base, blush pink, hot pink
48. **Robinhood Green** — oklch(8% 0.005 150) base, near-black, vivid green
49. **Chime Teal** — oklch(97% 0.004 175) base, mint-white, teal accent
50. **Cash App Neon** — oklch(8% 0.003 145) base, black, cash green #00D632
51. **Bloomberg Terminal** — oklch(5% 0.003 220) base, near-black, amber text
52. **HSBC Red** — oklch(97% 0.003 20) base, clean white, HSBC red
53. **Morgan Stanley Blue** — oklch(97% 0.002 230) base, white, navy blue
54. **Fidelity Green** — oklch(97% 0.003 150) base, white, deep green
55. **Amex Blue** — oklch(20% 0.015 235) base, deep navy, gold + blue
56. **Brex Orange** — oklch(12% 0.008 45) base, dark, vivid tangerine

### Category 4: Creative / Design (14 palettes)
57. **Studio White** — oklch(99% 0.002 60) base, near-white, black accent
58. **Creative Dark** — oklch(8% 0.004 270) base, near-black, neon accents
59. **Figma Grape** — oklch(97% 0.004 280) base, soft lavender, grape
60. **Adobe Red** — oklch(97% 0.003 25) base, white, Adobe red
61. **Canva Purple** — oklch(97% 0.004 295) base, soft purple-white, vivid purple
62. **Behance Blue** — oklch(12% 0.01 240) base, dark navy, electric blue
63. **Dribbble Pink** — oklch(97% 0.005 350) base, blush-white, dribbble pink
64. **Sketch Gold** — oklch(96% 0.005 75) base, warm white, gold accent
65. **Procreate Dark** — oklch(10% 0.006 260) base, near-black, bright spectrum
66. **Affinity Blue** — oklch(97% 0.004 220) base, clean, affinity blue
67. **Pixelmator Purple** — oklch(97% 0.004 285) base, soft purple, vivid violet
68. **Inkscape Dark** — oklch(15% 0.008 250) base, dark, multicolor
69. **Blender Orange** — oklch(8% 0.003 240) base, dark, blender orange
70. **Cinema 4D Blue** — oklch(12% 0.01 225) base, deep blue, cyan

### Category 5: Consumer / Lifestyle (20 palettes)
71. **Airbnb Rausch** — oklch(97% 0.004 20) base, warm white, coral #FF5A5F
72. **Spotify Black** — oklch(8% 0.003 145) base, black, Spotify green #1DB954
73. **Apple Minimal** — oklch(97% 0.002 60) base, near-white, apple black
74. **Nike Black** — oklch(5% 0.002 220) base, pure black, white + red
75. **Calm Blue** — oklch(96% 0.004 215) base, sky-white, soft blue
76. **Headspace Orange** — oklch(97% 0.004 50) base, warm, warm orange
77. **Peloton Dark** — oklch(8% 0.003 220) base, near-black, hot red
78. **Duolingo Green** — oklch(97% 0.004 145) base, light, vivid green
79. **Pinterest Red** — oklch(97% 0.003 15) base, white, Pinterest red
80. **Instagram Gradient** — oklch(97% 0.003 50) base, warm, pink→purple gradient
81. **TikTok Black** — oklch(5% 0.002 200) base, black, teal + red
82. **Discord Blurple** — oklch(22% 0.015 260) base, blurple, soft background
83. **Slack Aubergine** — oklch(25% 0.015 285) base, deep purple, yellow accent
84. **Twitter/X Dark** — oklch(8% 0.004 220) base, near-black, X blue
85. **Reddit Orange** — oklch(97% 0.004 40) base, warm white, Reddit orange
86. **YouTube Red** — oklch(97% 0.003 20) base, white, YouTube red
87. **Netflix Red** — oklch(8% 0.003 20) base, black, Netflix red
88. **Hulu Green** — oklch(8% 0.004 145) base, dark, vivid green
89. **Twitch Purple** — oklch(20% 0.015 285) base, dark purple, Twitch purple
90. **Medium Green** — oklch(97% 0.004 155) base, clean, medium green

### Category 6: Healthcare / Wellness (12 palettes)
91. **Clinical White** — oklch(99% 0.001 200) base, sterile white, trust blue
92. **Wellness Sage** — oklch(97% 0.005 150) base, sage-white, forest green
93. **Recovery Calm** — oklch(97% 0.004 215) base, sky-white, calming blue
94. **Dental Clean** — oklch(99% 0.002 180) base, white, teal accent
95. **Pharmacy Blue** — oklch(97% 0.003 225) base, clean, pharmaceutical blue
96. **Mental Health Lavender** — oklch(97% 0.004 285) base, lavender, soft purple
97. **Fitness Red** — oklch(10% 0.006 20) base, dark, energetic red
98. **Nutrition Green** — oklch(97% 0.005 140) base, natural white, vivid green
99. **Sleep Dark** — oklch(12% 0.008 265) base, deep navy, soft blue glow
100. **Meditation Amber** — oklch(97% 0.005 70) base, warm, deep amber
101. **Hospital Blue** — oklch(97% 0.002 220) base, clinical white, hospital blue
102. **Therapy Warm** — oklch(97% 0.005 60) base, warm cream, earth tones

### Category 7: Education / Learning (10 palettes)
103. **Classroom Yellow** — oklch(97% 0.005 90) base, light, vivid yellow
104. **Academic Navy** — oklch(97% 0.003 235) base, white, deep navy + gold
105. **Duolingo Lime** — oklch(97% 0.005 140) base, light, bright lime
106. **Khan Orange** — oklch(97% 0.004 50) base, warm, KA teal
107. **Coursera Blue** — oklch(97% 0.003 230) base, white, Coursera blue
108. **edX Dark** — oklch(15% 0.01 260) base, dark, edX red
109. **Notion Academy** — oklch(98% 0.003 60) base, parchment, graphite
110. **Roam Research** — oklch(98% 0.003 70) base, warm white, black
111. **Obsidian Dark** — oklch(10% 0.007 265) base, near-black, purple accent
112. **Anki Purple** — oklch(97% 0.004 280) base, light, purple accent

### Category 8: E-commerce / Retail (12 palettes)
113. **Shopify Green** — oklch(97% 0.003 150) base, white, Shopify green
114. **Amazon Orange** — oklch(97% 0.004 50) base, warm white, Amazon orange
115. **Etsy Orange** — oklch(97% 0.004 40) base, warm, Etsy orange
116. **eBay Multi** — oklch(97% 0.002 60) base, white, 4-color wordmark
117. **ASOS Black** — oklch(5% 0.002 220) base, black, neon pink
118. **Zara Minimal** — oklch(99% 0.001 60) base, pure white, pure black
119. **H&M Red** — oklch(97% 0.003 20) base, white, H&M red
120. **Uniqlo Red** — oklch(97% 0.002 20) base, white, red + navy
121. **Supreme Red** — oklch(97% 0.002 20) base, white, Supreme red
122. **Off-White Black** — oklch(97% 0.002 60) base, off-white, black quotes
123. **Palace Blue** — oklch(8% 0.005 235) base, deep blue, white
124. **Kith Tan** — oklch(97% 0.005 70) base, tan/cream, olive + black

### Category 9: Food & Hospitality (12 palettes)
125. **Doordash Red** — oklch(97% 0.003 20) base, white, DoorDash red
126. **Uber Eats Black** — oklch(8% 0.003 145) base, black, Uber green
127. **Deliveroo Teal** — oklch(97% 0.004 175) base, teal-white, vivid teal
128. **Chipotle Brown** — oklch(97% 0.005 50) base, warm, chipotle brown
129. **Starbucks Green** — oklch(20% 0.015 155) base, dark green, Starbucks green
130. **McDonald's Yellow** — oklch(10% 0.005 220) base, dark, golden yellow + red
131. **Resy Dark** — oklch(12% 0.008 250) base, dark navy, coral
132. **OpenTable Red** — oklch(97% 0.003 15) base, white, OT red
133. **Yelp Red** — oklch(97% 0.003 15) base, white, Yelp red
134. **Tripadvisor Green** — oklch(97% 0.004 145) base, light, TA green + owl
135. **Booking Blue** — oklch(97% 0.003 225) base, white, Booking blue
136. **Airbnb Warm** — oklch(97% 0.004 30) base, warm cream, coral

### Category 10: Automotive / Industrial (9 palettes)
137. **Tesla Dark** — oklch(8% 0.003 220) base, near-black, white + red
138. **Ferrari Red** — oklch(97% 0.002 20) base, white, prancing horse red
139. **BMW Blue** — oklch(97% 0.003 225) base, white, BMW blue + silver
140. **Mercedes Silver** — oklch(80% 0.003 220) base, silver-white, star silver
141. **Porsche Black** — oklch(8% 0.002 225) base, black, gold accent
142. **Rivian Green** — oklch(15% 0.01 155) base, dark, Rivian lime
143. **Lucid Air** — oklch(97% 0.003 200) base, bright white, space gray
144. **Industrial Orange** — oklch(15% 0.005 220) base, dark gray, safety orange
145. **Construction Yellow** — oklch(8% 0.003 200) base, dark, CAT yellow

### Category 11: Media / Entertainment (10 palettes)
146. **HBO Dark** — oklch(8% 0.004 280) base, dark purple, HBO white
147. **Disney Blue** — oklch(10% 0.01 240) base, deep blue, gold star
148. **Pixar Blue** — oklch(12% 0.01 225) base, Pixar blue, warm white
149. **Warner Dark** — oklch(8% 0.003 220) base, near-black, WB gold + blue
150. **Apple TV Dark** — oklch(5% 0.002 220) base, pure black, Apple blue
151. **Hulu Black** — oklch(8% 0.004 145) base, dark, Hulu green
152. **Paramount Blue** — oklch(10% 0.01 230) base, deep blue, gold mountain
153. **Sony Dark** — oklch(8% 0.003 220) base, near-black, blue accent
154. **Universal Dark** — oklch(8% 0.004 235) base, dark, globe blue
155. **Blumhouse Dark** — oklch(5% 0.002 220) base, pure black, white + red

### Category 12: Government / Institutional (6 palettes)
156. **Federal Blue** — oklch(97% 0.002 235) base, white, US flag blue
157. **NHS Blue** — oklch(97% 0.003 230) base, clinical white, NHS blue
158. **UN Blue** — oklch(97% 0.003 215) base, white, UN sky blue
159. **European Blue** — oklch(20% 0.015 250) base, EU blue, gold stars
160. **Academic Crimson** — oklch(97% 0.002 20) base, white, Harvard crimson
161. **Gov.uk Green** — oklch(97% 0.003 150) base, white, GDS green

## Contrast & Accessibility

### WCAG Requirements

| Content Type | AA Minimum | AAA Target |
|--------------|------------|------------|
| Body text | 4.5:1 | 7:1 |
| Large text (18px+ or 14px bold) | 3:1 | 4.5:1 |
| UI components, icons | 3:1 | 4.5:1 |
| Non-essential decorations | None | None |

**The gotcha**: Placeholder text still needs 4.5:1. That light gray placeholder you see everywhere? Usually fails WCAG.

### Dangerous Color Combinations

These commonly fail contrast or cause readability issues:

- Light gray text on white (the #1 accessibility fail)
- **Gray text on any colored background**—gray looks washed out and dead on color. Use a darker shade of the background color, or transparency
- Red text on green background (or vice versa)—8% of men can't distinguish these
- Blue text on red background (vibrates visually)
- Yellow text on white (almost always fails)
- Thin light text on images (unpredictable contrast)

### Never Use Pure Gray or Pure Black

Pure gray (`oklch(50% 0 0)`) and pure black (`#000`) don't exist in nature—real shadows and surfaces always have a color cast. Even a chroma of 0.005-0.01 is enough to feel natural without being obviously tinted.

### Testing

Don't trust your eyes. Use tools:

- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- Browser DevTools → Rendering → Emulate vision deficiencies
- [Polypane](https://polypane.app/) for real-time testing

## Theming: Light & Dark Mode

### Dark Mode Is Not Inverted Light Mode

You can't just swap colors. Dark mode requires different design decisions:

| Light Mode | Dark Mode |
|------------|-----------|
| Shadows for depth | Lighter surfaces for depth (no shadows) |
| Dark text on light | Light text on dark (reduce font weight) |
| Vibrant accents | Desaturate accents slightly |
| White backgrounds | Never pure black—use dark gray (oklch 12-18%) |

In dark mode, depth comes from surface lightness, not shadow. Build a 3-step surface scale where higher elevations are lighter (e.g. 15% / 20% / 25% lightness).

### Token Hierarchy

Use two layers: primitive tokens (`--blue-500`) and semantic tokens (`--color-primary: var(--blue-500)`). For dark mode, only redefine the semantic layer—primitives stay the same.

## Alpha Is A Design Smell

Heavy use of transparency (rgba, hsla) usually means an incomplete palette. Alpha creates unpredictable contrast, performance overhead, and inconsistency. Define explicit overlay colors for each context instead. Exception: focus rings and interactive states where see-through is needed.

---

**Avoid**: Relying on color alone to convey information. Creating palettes without clear roles for each color. Using pure black (#000) for large areas. Skipping color blindness testing (8% of men affected).
