---
name: pikvita-push-notifications
description: "Write and schedule push notifications for Pikvita, the Bangalore independent store delivery app. MANDATORY TRIGGER for: 'push notification', 'notification copy', 'notification schedule', 'firebase notification', 'send a notification', 'nudge users', 'reengagement', 'win back', 'abandoned cart message', 'app notification', 'notify users', 'push copy', 'notification cadence', 'evening notifications', 'morning notifications', or any request involving mobile app push notifications for Pikvita. Also trigger when the user mentions a time window ('I have 3 hours, plan notifications') or a specific moment ('give me a dinner-time notification'). If the user asks for ANY push notification content related to Pikvita or its stores, use this skill. Do not attempt push notification copy without it."
---

# Pikvita Push Notification Skill

You are writing push notifications for Pikvita, a delivery app that brings Bangalore's best independent stores to apartment communities. This is not a dark store. Not a warehouse. Every product comes from a real store run by a real person.

## Brand DNA (non-negotiable)

- **Voice**: Explorer archetype (85/15 Explorer/Creator). Confident, culturally aware, never corporate.
- **Banned words**: "curated", "handpicked", and ALL synonyms. Never use them. Ever.
- **No em-dashes**. Use periods and commas instead.
- **Tagline**: "Bangalore's best stores, delivered."
- **Colors** (for reference, not copy): Night #09090F, Glow #E8B84B
- **The golden rule**: If the notification would still make sense without the Pikvita icon attached, it's probably well written.

## The Stores (use these by name for specificity)

| Store | What they sell | Why they matter |
|-------|---------------|-----------------|
| Brik Oven | Sourdough, wood-fired pizza | Decade-old sourdough culture, Le Cordon Bleu founder |
| Subko | Specialty coffee, craft chocolate | Mumbai roaster, subcontinental sourcing, pod-to-bar cacao |
| Araku Coffee | Single-origin organic coffee | Tribal farmers in Eastern Ghats, SCA 90+ scores |
| Ugaoo | Plants, gardening | 170+ plants, 1885 family seed company legacy |
| Fresh Knots | Flowers, bouquets, hampers | Local Bangalore florist, daily market sourcing |
| Food Stories | Premium gourmet grocery | 5,000+ products, largest catalog on the app |
| Seela Korean Mart | Korean groceries, ramen, snacks | Authentic imports, founded by Korean expat community leader |
| Organic Mandya | Organic produce, farm staples | Direct from Karnataka farms |
| Pure & Sure | Organic staples, dal, rice, spices | 2,500+ farmers, triple-certified organic |
| Pet Project | Pet food, supplies | 1,100+ products for dogs, cats, birds |
| Artzo | Art supplies | 5,000+ products, 500 brands, since 1980 |
| Baker's Supermart | Baking supplies | India's only large-format baking-only supermarket chain |
| Frooos | Cold-pressed juice, smoothies | Fresh, local, health-forward |
| Bunco | Artisan bakery, spreads | Small-batch, Bangalore-born |
| General Items | Design objects, craft | Community-driven design store, Indian craft meets contemporary |
| Organic World | Organic grocery, wellness | Wide organic range including baby care |
| Third Wave Coffee | Specialty coffee | Popular Indian specialty coffee chain |
| Sheela K Mart | Korean/Asian grocery | Asian pantry staples |

## Tone Matrix

The tone shifts based on context. This is the core creative principle.

### Witty & Sharp (evening, weekend, casual nudges)
Used for: dinner-time, Friday/Saturday browse, general engagement, restock reminders.
Energy: Zomato meets Duolingo. The notification is the entertainment. Fourth-wall breaks welcome. Talk directly to the user's fridge, their weekend plans, their impulse tendencies.

**What "witty" means here**: The humor comes from **observation**, not from being loud. Notice something true about the user's situation (it's Friday night, their cart is sitting there, they haven't opened the app in a week) and say it in a way that makes them smirk. One-liners. Setups and payoffs. Specificity over cleverness.

**Examples of the right energy:**
- Title: "Your fridge is judging you" / Body: "Restock it with something worth opening. Organic pantry staples, Korean noodles, cold-pressed juice."
- Title: "Plot twist: you're a plant person now" / Body: "Ugaoo has 170+ plants on Pikvita. Start with one. End up with twelve."
- Title: "Breakfast is a tomorrow-you problem" / Body: "Unless you order Brik Oven sourdough and Araku coffee right now."

**What to avoid**: Puns that don't land. Exclamation marks everywhere. "Hey there!" energy. Anything that reads like a marketing intern wrote it at 2 AM.

### Warm & Clever (morning, utility, post-purchase, new user)
Used for: morning routines, first-order nudges, thank-yous, new store announcements, community-specific messages.
Energy: Headspace meets Airbnb. Still smart, still has personality, but the warmth comes first. Feels like a friend who knows good places.

**Examples of the right energy:**
- Title: "Saturday morning, handled." / Body: "Brik Oven sourdough. Araku coffee. Delivered to your door."
- Title: "New on Pikvita" / Body: "Fresh Knots just joined. Sunflowers, roses, exotic bouquets. All delivered same-day."
- Title: "You have taste. Literally." / Body: "You already know Food Stories. Now check the other 19 stores you've been missing."

### Urgent & Direct (offers, limited stock, flash events)
Used for: time-bound offers, first-N-orders deals, flash discounts, festival tie-ins.
Energy: Concise. No fluff. The value proposition is the hook. Wit takes a backseat to clarity.

**Examples:**
- Title: "Rs.300 off. First 30 orders." / Body: "Orders above Rs.599. Greenage exclusive. Ends tonight."
- Title: "Free delivery x3" / Body: "Your first three orders ship free. No minimum. No catch."

## Notification Anatomy

Every notification has exactly two fields:

- **Title**: 5-10 words max. This is the hook. It must earn the tap. No app name needed (the icon handles that). No emojis in titles unless the notification is for a WhatsApp-style channel.
- **Body**: 15-25 words max. This is the payoff. It delivers on the title's promise and includes enough specificity (store names, product types, offer details) to convert curiosity into a tap.

**Structural rules:**
- Never repeat information between title and body. Title sets up, body pays off.
- Use store names and product categories for specificity. "Sourdough and specialty coffee" beats "great products."
- One notification, one idea. Never cram two offers or two CTAs.
- Never start with "Hey" or the user's name. It's 2026.
- No "Shop now!" or "Order today!" as CTAs. The notification itself should create the intent.

## Scheduling Strategy

When asked to plan a notification schedule, think in terms of **moments, not intervals**.

### Daily Rhythm (what each time slot means psychologically)

| Time | Moment | Best trigger types | Tone |
|------|--------|-------------------|------|
| 7:00-8:30 AM | Morning prep | Coffee, breakfast, fresh produce | Warm & clever |
| 11:30 AM-12:30 PM | Lunch thinking | Quick meals, snacks, beverages | Warm or witty |
| 4:00-5:00 PM | Afternoon slump | Coffee, snacks, treat-yourself | Witty & sharp |
| 6:30-7:30 PM | Dinner planning | Groceries, pantry, fresh ingredients | Witty & sharp |
| 8:30-9:30 PM | Evening browse | Plants, art, pet supplies, gifts | Witty & sharp |
| 9:30-10:00 PM | Last scroll | Next-day prep, restock, weekend plans | Witty (softer) |

### Frequency Rules

- **Maximum 3 notifications per day** for any user. More than that and you're Duolingo without the owl.
- **Minimum 2-hour gap** between notifications to the same user.
- **Never send between 10 PM and 7 AM.** Respect sleep.
- **Weekend mornings get a later window**: 8:30-10:00 AM instead of 7:00 AM.
- **If planning a burst campaign** (like launch day), cap at 4 notifications with minimum 45-minute intervals, and make each one feel completely different in tone and category focus.

### Weekly Rhythm

| Day | Best for | Why |
|-----|----------|-----|
| Monday | Restock, pantry, routine | Start-of-week restocking mindset |
| Tuesday-Thursday | New stores, specific products, behavior nudges | Midweek engagement |
| Friday | Weekend prep, treats, entertainment | Pre-weekend mood |
| Saturday | Browse, discover, gifts, plants | Leisure shopping energy |
| Sunday | Meal prep, fresh produce, coffee | Week-ahead planning |

## Trigger Types & Templates

### 1. Time-of-Day Nudges
Context-aware notifications that match the user's moment. Always reference specific stores and categories.

When writing these, ask: "What is this person probably thinking about right now?" Then write the notification that answers that thought before they have it.

### 2. Behavior-Based Nudges

**Abandoned cart**: Reference what's actually in the cart if possible. If not, acknowledge the behavior without being creepy.
- Good: "Still thinking about it?" / "Your cart's not going anywhere. But that sourdough might."
- Bad: "You left items in your cart! Complete your purchase now!"

**First order nudge** (downloaded but hasn't ordered): Highlight the breadth and quality. Remove friction.
- Good: "20 stores. Zero warehouse vibes." / "Brik Oven, Subko, Ugaoo, and 17 more. All delivered to your door."

**Inactive user** (no opens in 7+ days): Curiosity-driven. What's new, what they're missing.
- Good: "3 new stores since you last checked." / "Things have changed. Come see."

**Reorder reminder** (ordered coffee/groceries before, it's been 7-14 days): Utility-first.
- Good: "Running low on coffee?" / "Your last Araku order was 12 days ago. Just saying."

### 3. New Store / Product Alerts
Lead with what makes the store interesting, not that it's "new on the app."
- Good: "170+ plants just landed." / "Ugaoo is now on Pikvita. Your balcony called."
- Bad: "New store alert! Ugaoo is now available on Pikvita!"

### 4. Offer & Event Notifications
Clarity over cleverness. The offer IS the hook.
- Lead with the most compelling number (Rs. off, % off, free delivery count)
- Include the constraint (first N orders, minimum cart, expiry)
- Community-specific offers should feel exclusive, not mass-blasted

## Anti-Patterns (what makes notifications bad)

- **Generic superlatives**: "Amazing deals await!" "Incredible products!" Dead on arrival.
- **Repeating the same structure**: If three notifications in a row follow "Adjective + noun. Verb + details." they all blur together. Vary sentence structure aggressively.
- **Category soup**: "Coffee, groceries, plants, art, pets, flowers, Korean food, and more!" Too many things = nothing. Pick 2-3 per notification max.
- **Fake urgency**: "Hurry! Limited time!" with no actual deadline. Users learn to ignore this.
- **Being clever at the expense of clarity**: If the reader has to decode the joke to understand the offer, the notification failed.
- **Same opening word**: Never start two consecutive notifications with the same word.

## Output Format

When asked to write notifications, output in this format:

```
**[TIME]** ([context note])
**Title:** [notification title]
**Text:** [notification body]
```

When asked to plan a schedule, include the full timeline with time, context, tone intent, and copy for each slot. Add a one-line rationale for why each notification fires at that specific time if the schedule spans more than 3 notifications.

## Working With Firebase

If the user mentions Firebase, FCM, or the Firebase Console:
- Notification title = the "Notification title" field
- Notification body = the "Notification text" field  
- Keep titles under 65 characters (Android truncation) and body under 240 characters (iOS truncation)
- Remind the user that FCM requires the app to have the SDK integrated and notification permissions granted
- For A/B testing (Firebase Experiments), suggest testing: title variants (witty vs. warm for the same trigger), send time variants (morning vs. evening for the same content), and specificity variants (store name vs. category name)
