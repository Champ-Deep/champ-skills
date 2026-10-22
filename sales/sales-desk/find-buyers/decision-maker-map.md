# Decision-Maker Map

Maps one account to the three to five people who buy, champion or block the deal, each with a LinkedIn verification step, before you spend a touch.

## Give Claude
- The account name and what it does: paste the About text, site copy or a short description
- What you sell and who normally signs for it, in two lines
- Optional: names and titles you already have, from an email signature, call note or pasted list
- Optional: the roles you usually sell into, so the map matches your motion
- Optional: a pasted LinkedIn profile text or team page, if you already found one

## Claude does
1. List three to five roles for this purchase: the buyer, the champion, the blocker, plus any evaluator or user role the input suggests.
2. For each role, give what they care about in one line and two or three job title variants to search.
3. Place every pasted name into a role, with the reason it fits; names that fit nothing go to an unplaced list.
4. For each person, give the exact LinkedIn search string: name plus company plus title variant.
5. Give the two details that confirm the right person: title match and a current date range on the profile.
6. For roles with no name yet, give the search string and title variants in priority order.
7. Flag conflicts, such as two names claiming the same role, with what to check to resolve them.
8. Keep roles to five. If a sixth appears, cut the least likely to affect the decision.

## Output
- Role table with this header: `role (buy / champion / block) | title to search | what they care about | verify with | status`.
- Placed people: name, title, role, the search string used, status (found / needs lookup).
- Unplaced names and unmapped roles, each with the next search to run.
- Verification note per found person: title seen, date range seen, source.
- Conflict list: what disagrees, and the one check that settles it.

## Rules
- Never guess a person's title, tenure or reporting line. Not in the input means "needs lookup".
- Do not invent names of people at the account, even plausible ones.
- Verification means search and read only: current title and dates, nothing more.
- Never produce email addresses or phone numbers in this file's output.
- Five roles maximum; if you listed more, cut the weakest and say which.
- If the input names no one and gives no profile, ask for one source before mapping.
