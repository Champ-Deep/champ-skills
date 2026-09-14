# Creative generation (Higgsfield MCP)

These specifics come from repeated use generating LinkedIn-style ad creatives and short videos for prospect campaigns, updated against the current Higgsfield MCP tool surface. Tool names carry a per-install server prefix (see connector-preflight.md), so they're referred to here by their base name: `generate_image`, `generate_video`, `models_explore`, `media_import_url`, `media_upload_widget`, `job_display`, `balance`, `upscale_image`, `upscale_video`.

## Picking a model

- Don't guess model IDs from memory. If the use case is at all unusual, call `models_explore(action: "recommend", query: "<goal + input context>")` first and let it pick. For known cases, call `models_explore(action: "get", model_id: "<id>")` before generating to confirm supported aspect ratios, resolutions, duration limits, and the exact `medias[].roles` the model accepts. Roles vary per model and passing a wrong role fails or gets silently coerced.
- **Images**: `marketing_studio_image` is the default for commercial/product/ad creatives. `aspect_ratio: "1:1"` for LinkedIn feed ads, `resolution: "2k"`. It accepts reference media with role `image`, which is how you ground the real brand logo (see Brand accuracy below). Other image defaults per the server: `soul_2` for portraits/UGC/editorial, `nano_banana_pro` for 4K/text-heavy/diagrams.
- **Video**: `marketing_studio_video` for ad/product motion; `kling3_0_turbo` for fast single-start-frame animation of an existing still (cinemagraph-style). Pass the source still via the model's declared start-image role (check `models_explore` for the exact role name, typically `start_image`).

## Video resolution policy: 480p first, always

Video burns credits fast and first drafts get rejected often. So: **every first-pass video generates at the lowest resolution the model supports (480p or the model's minimum), never higher.** Treat the 480p output as the concept proof. Only after the user approves the concept do you spend on quality, and even then prefer `upscale_video` on the approved output over regenerating at high resolution, since upscaling is cheaper and keeps the approved motion exactly as signed off. Regenerate at higher resolution only if the model's low-res artifacts are themselves the objection. Never submit a first-draft video at 1080p+ without the user explicitly asking for it.

## Cost preflight

- `get_cost: true` on any `generate_image`/`generate_video` call returns the credit cost without submitting the job. Use it before any batch bigger than a handful of images or any video, and before anything at high resolution.
- `balance` returns remaining credits and plan. Check it at Step 0 preflight time when the run includes video or a large image batch; don't assume.

## Getting reference media in

- `medias[].value` must be a `media_id` (from `media_import_url` / `media_upload_widget`) or a prior generation's `job_id`. Never pass an https URL as a media value.
- **Web-hosted brand assets**: `media_import_url` imports an HTTPS image/video/audio URL and returns a confirmed `media_id`. Practical trick for logos: Wikimedia's `https://commons.wikimedia.org/wiki/Special:FilePath/<File_Name>.svg?width=1024` redirect serves a rendered PNG of most major brand logos, and `media_import_url` follows it fine. The client's own site (footer SVG/PNG) is the other standard source.
- **User's local files**: in Apps-UI-capable clients call `media_upload_widget` immediately; do not ask the user to attach files in chat, because remote MCP tools cannot read chat attachments.

## Concurrency limit

The pro plan caps concurrent jobs at 4. Submitting more than 4 generation jobs at once returns a rate-limit error, not a queue. Handle it by submitting 4, polling `job_display` (one job ID per call) until a slot frees, then submitting the next batch. A `count` of up to 4 on a single call counts as that many jobs. Don't treat the rate-limit error as a reason to reduce the total creative count; it's pacing, not quota.

## Recovery tool

If any generation response includes a `recovery_tool`, call it immediately. Don't explain the situation to the user first or ask permission; the server is telling you the exact next call to make.

## Downloading results

Once a job completes, `job_display` returns the authoritative result URL. Always re-query `job_display` for the specific job ID and read that field directly rather than constructing a CDN URL by hand from a remembered pattern. These URLs embed a timestamp that is not predictable; a guessed value produces a file that downloads without an HTTP error but is a corrupt fragment, often under a few hundred bytes. After downloading, verify byte counts before declaring the assets saved.

## Brand accuracy

Higgsfield (like most generative models) will invent its own version of a real brand's logo, wordmark, or palette if not explicitly constrained, and it will get it wrong in a way anyone who knows the brand notices instantly. In order of preference:

1. **Best**: import the real brand asset (`media_import_url` or `media_upload_widget`) and pass it as a reference media on the generation, with the prompt explicitly instructing "use the provided logo exactly as supplied, do not redraw or restyle it."
2. **Acceptable fallback for stills only**: generate without logo accuracy, then composite the real logo on afterward. This does not work for video, where the invented logo is baked into every frame; fix the brand asset on the source still first, then generate video from the corrected still.

Either way, never ship a creative with an AI-invented version of a real, identifiable client's brand mark without the user explicitly signing off first.
