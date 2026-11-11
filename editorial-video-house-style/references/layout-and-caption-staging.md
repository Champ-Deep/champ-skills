# Face-first layout and caption staging

## Frame the person before placing text

Inspect the new source across its full duration, including head movement and hand gestures. Build protected regions for head, face and meaningful gestures, with breathing room. A face detector alone cannot certify gesture clearance. Confirm uncertain samples visually. Do not borrow the previous video's overlay coordinates.

Use platform exclusions as a starting safety envelope, not as proof that the remaining space is empty. On a1080x1920 canvas, start with the top250px, bottom400px and side120px excluded. Scale these with the canvas, then account for the intended platform and actual framing. Preserve safe space even when designing a top or bottom anchor: 'bottom' means the bottom of the usable region, not the physical frame edge.

## Brand and information cards

For Lake B2B name cards and similar on-camera information cards, center the entire card horizontally on the video canvas and center its text. `text-align:center` inside a left-positioned card does not center the card. At1080px width, the card's center is540px. A760px card therefore starts at160px; calculate and validate rather than copying an old left offset.

Choose one stable top-safe or bottom-safe anchor based on the source. Do not float a card over the middle of the torso just because it misses the mouth. Keep both the card and its complete entrance/exit path out of the protected head/gesture region. Favor a compact one- or two-line card over a large stacked panel. Do not resize or crop the person merely to accommodate decorative text.

If neither edge offers enough room, delay or omit the card, or use a separate explanatory scene. Never silently fall back to the middle. A card and a caption may coexist only when their regions and the person remain clear; otherwise stagger their timing. Do not hide necessary speech captions simply to make space for branding. Avoid repeating a spoken brand name in both a card and a separate caption when the card already provides the exact words; preserve complete subtitles separately.

This center/edge rule applies to on-camera cards and caption units, not every label inside a full-screen process diagram. Diagrams can retain useful left-aligned labels.

## Give captions hierarchy, not random effects

Plan three distinct jobs: readable dialogue, a selectively emphasized key phrase, and an explanatory visual for a concept that actually benefits from one. Use a consistent type family and palette, but vary hierarchy where the meaning changes. Phrase rhythm, size/weight hierarchy, line grouping, a restrained underline or a timed keyword mask can create emphasis without word bounce or reflow.

Do not fill the middle of the clip with the same generic badge treatment because the opening and ending already look designed. Audit the middle explicitly. Select important terms and conclusions from the transcript before building. A long run of undifferentiated captions is a design-review signal, not permission to invent decorative effects or make every word a headline.

Keep ordinary speech legible and stable in a measured edge lane. Never place generic captions in the center of the talking face. Use a dedicated graphic scene for dense teaching material rather than stacking a title, card, diagram and captions around the person. Do not prescribe a fixed maximum number of plain cues: a reflective passage may legitimately need quiet captions.

## Validation on the new video

Export actual rendered overlay rectangles and observed protected source regions at opening, middle, ending, card holds, gesture peaks and animation midpoints. Run `scripts/check_layout.py` on the measurements. Its inputs must be measured boxes, not the intended CSS values. Include breathing room in protected regions. Check both container centering and inner text alignment in the DOM.

The script verifies frame bounds, center/edge anchoring, two-line captions and collisions for the supplied samples. It does not detect people, infer unmeasured motion or prove full-timeline clearance. Pair it with visual inspection of the encoded frames and normal-speed playback. Reject a centered card that still crowds the face; numerical centering alone is not good composition.

Preserve the older renders as evidence of what was corrected. Test the new source from scratch before promoting the layout across formats.
