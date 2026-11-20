# Proving claims about a live page before the draft asserts them

A fix list or a "confirmed, ship it" verdict about a campaign page is a set of claims about markup. Each claim needs one grep against the fetched page: a defect you cannot show in the markup does not go in the mail, and a defect you did not grep for can ship to customers with your confirmation on it.

## Fetch

```bash
curl -sL -A 'Mozilla/5.0' <campaign url> -o page.html
curl -sL -A 'Mozilla/5.0' <site root> -o home.html
```
Fetch both. A campaign banner is usually a homepage link or a timed modal, not an asset on the campaign URL, so a campaign-only fetch always reports the banner as missing.

## Prove each claim

- **Unfilled placeholder.** Grep the literal token as the reader sees it (`\[X\]`, `START DATE`, `END DATE`), not the words around it. A `[X]` inside a sentence is invisible in a read-through of the copy document and only visible in the live HTML, and it is the one defect that ships publicly.
- **Dead link.** `grep -oE 'href="[^"]*"'` on the fetched body, then open each link that resolves to `#` or to a real-looking path, and compare it with a path that cannot exist on the same host: a 404 on the control path plus a 200 on the link means the link is broken, the reverse means it is fine.
- **Title against promise.** `grep -oE '<title>[^<]*'`. The title is what a tab and a search result show, so when the title promises a flat number that the headline hedges, the title is what gets corrected.
- **Field required-ness.** Parse the form's own markup, not the screenshot:
  ```python
  for m in re.finditer(r'<(input|select)\b[^>]*>', html):
      t = re.sub(r'\s+', ' ', m.group(0))
      if 'hidden' in t: continue
      # name=, type=, and whether \brequired\b appears
  ```
  What the user sees is the rendered marker next to the label; enforcement may instead sit in a `required` attribute or in client-side JS. When the marker and the attribute disagree, report the marker as the observable fact and ask the build owner which one enforces, instead of asserting the field is optional.
- **Consent bundling.** A single required checkbox covering both "about my request" and "related offers" is a defect on any form that takes UK, German or French numbers: ask for it split into a required box and an optional one, and say why, so the fix reads as a real requirement rather than a preference.
- **Dashes in what ships.** `grep -c $'\xe2\x80\x93\|\xe2\x80\x94'` on the fetched HTML for on-page copy, and the same check on the reply text you are staging: the no-dash rule covers what goes to customers as much as what goes to recipients. Numeric ranges in option lists (`1-10 employees`) are the usual offender.

## Report shape

Name the page you fetched, the date of the fetch, and each defect with its exact on-page text (`within [X] business days`). A defect without the literal string is a claim; with it the build owner can fix it without asking what you meant, and Deep can check your work without opening the site.