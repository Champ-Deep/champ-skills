# Bilingual pages: toggle contract, copy payloads, probe order

Read when one page ships two languages in one file (English and Chinese, or any pair).
Everything here sits on top of the house kit and the Phase 6 gate.

## Build contract

1. One wrapper per translatable string: `<span class="bi"><span class="en">...</span><span class="zh">...</span></span>`, inline for a phrase inside a line, block-paired when the two languages stack. Never build two parallel DOM trees: with one tree the claim audit (rule 6) stays honest, because one count renders in either language instead of drifting apart.
2. Language state lives on `<html data-view="en|zh|both">`, defaulting to `both`, and CSS only hides: `[data-view=en] .zh{display:none}` plus its mirror. The secondary line inside a compact cell drops to about `.95em` so a paired label does not outweigh the number it annotates.
3. The segmented control is a real radiogroup: `role="radiogroup"`, three `role="radio"` buttons carrying `aria-checked`, ArrowLeft/ArrowRight/Home/End keyboard support, and a visible focus ring. Position the sliding thumb by measuring the selected button's `getBoundingClientRect().left`, not with nth-child arithmetic: padding and gap change per breakpoint and the drift shows as a thumb sitting off its own label.
4. The view rides in the URL hash (`#zh`), restored on load and written on change, so a link forwarded to the Chinese team opens in Chinese. Update `document.documentElement.lang` (`en`, `zh-CN`) as well, or screen readers keep the English voice and the browser hyphenates Chinese by English rules.
5. CJK type: a self-contained file cannot load a CJK webfont, so put system CJK families after the Latin stack (`"PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif`). Never letter-space CJK to fill a line, and never translate numbers, units or model codes (45 TOPS, RMB, 4090 48GB): only the words around them move.
6. Full-width Chinese punctuation (，。？) in Chinese lines, ASCII in English lines. Mixed punctuation inside one Chinese line is the fastest tell that the string was machine-translated.

## Copy payloads: never read the DOM

A copy button in `both` view reading `innerText` of a bilingual element returns English and Chinese concatenated into one unusable blob, and the same button in `en` view returns only one language, so the payload silently depends on the toggle state the reader happens to have. Take the payload from a per-language source instead: a `<template>`, a `data-payload-zh` attribute, or a JS string keyed by language. Then assert it in the probe: first line, line count, and that it contains none of the other language (a Chinese character class test proves the English payload is English).

A message meant for a supplier is also selectable plain text on the page (a `white-space: pre-wrap` block), not only behind a button: the reader may open the file on a phone where clipboard permission is denied.

## Probe order

Run every budget probe in all three views. `both` is the default and the tallest state, so a fold that passes in `en` fails in `both`, and the page ships in `both`. In one loop per width assert: `documentElement.dataset.view`, `location.hash`, `document.documentElement.lang`, thumb rect against the selected radio, keyboard navigation, the disabled sweep, and one clipboard payload per button. Height, overflow and the fold all re-measure per view, because Chinese wraps to fewer lines than English and the two views do not share a layout.

## Phrases and lists

A stall phrase list runs English, Chinese, then pinyin with tone marks as a third mono line under its own Chinese line, never interleaved with the English. A forwardable shopping list is numbered plain text in the target language, one item per line, with quantity and the model name in the same order every time it appears.

## Pitfalls

- Fix one Chinese form per name and reuse it verbatim across the headline, the list, the message and the phrases (香橙派 Orange Pi 6 Plus). Suppliers match on the model name, so two translations of one product read as two products.
- Decide which language prints: hide the other in `@media print`, or the PDF doubles in height and the budget you measured no longer describes the artifact.
- Run the contrast audit per view as well; a muted secondary line on the accent panel passes in one language and fails in the other when only one of them wraps onto the panel.
