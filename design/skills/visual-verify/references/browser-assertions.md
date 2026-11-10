# Browser assertion and CSP mismatches

Keep the application's strict Content Security Policy intact when a browser assertion fails. A string `wait_for_function` predicate can trigger the page's `unsafe-eval` prohibition even while normal controls work. Wait with a locator assertion such as `expect(page.locator('#status')).to_contain_text('saved')`, rather than weakening the app's CSP to make the test pass.

Cross-check disabled select options through their actual DOM property and attribute. A locator's `is_disabled()` can report false for an `<option>` whose `disabled` property and attribute are both true. Inspect `locator.evaluate('(option) => option.disabled')` and `outerHTML`, then test whether selection is actually blocked. A QA-driver mismatch is not an application defect.

When a verification helper disagrees with computed state, reduce it to one control and one state before changing product code. Preserve the reproduction and record the limitation beside the test results.
