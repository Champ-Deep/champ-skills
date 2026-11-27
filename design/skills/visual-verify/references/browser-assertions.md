# Browser assertion and CSP mismatches

Keep the application's strict Content Security Policy intact when a browser assertion fails. A string `wait_for_function` predicate can trigger the page's `unsafe-eval` prohibition even while normal controls work. Wait with a locator assertion such as `expect(page.locator('#status')).to_contain_text('saved')`, rather than weakening the app's CSP to make the test pass.

Cross-check disabled select options through their actual DOM property and attribute. A locator's `is_disabled()` can report false for an `<option>` whose `disabled` property and attribute are both true. Inspect `locator.evaluate('(option) => option.disabled')` and `outerHTML`, then test whether selection is actually blocked. A QA-driver mismatch is not an application defect.

Close a pinned dialog every way a user can, with a real pointer, then assert the state around it. When a dialog returns focus to a trigger that is also a hover-card (Radix HoverCard opens on focus), the × and outside-click paths reopen the preview on the returned focus, and it stays up after the pointer leaves, while Escape looks fine. For each of ×, outside click and Escape at a hover-capable width: move the pointer off the scene, then require `.preview` count 0, and if a preview or focus state pauses animation, require the animated transform to change within 1 s once focus leaves. A test that closes only with Escape, or asserts only that focus returned, passes a page that sticks a floating card and freezes the scene on every × close.

When a verification helper disagrees with computed state, reduce it to one control and one state before changing product code. Preserve the reproduction and record the limitation beside the test results.
