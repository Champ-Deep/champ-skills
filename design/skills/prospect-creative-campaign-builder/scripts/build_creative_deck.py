#!/usr/bin/env python3
"""
build_creative_deck.py

Assemble a single self-contained HTML creative deck from local image/video files,
base64-embedding every asset so the result is one portable file with no external
references. This is the pattern that got rewritten from scratch five separate
times during manual creative-deck builds -- read local media, embed it, drop it
into a templated HTML shell. Use this instead of writing a new version of that
script per run.

Usage:
    python build_creative_deck.py --manifest manifest.json --title "Client Name Creative Deck" \
        --accent "#38b6e8" --output deck.html

Manifest JSON shape:
[
  {"section": "Dr. Smith Funnel", "label": "Stage 1: LinkedIn ad", "path": "/abs/path/img1.png", "type": "image", "caption": "optional caption text"},
  {"section": "Dr. Smith Funnel", "label": "Stage 2: Connection note", "path": "/abs/path/img2.png", "type": "image"},
  {"section": "Specialty Set", "label": "Podiatry", "path": "/abs/path/vid.mp4", "type": "video"}
]

Entries are grouped by "section" in the order first seen. Within a section,
entries render in a responsive card grid. Supports type "image" (png/jpg/jpeg/webp)
and "video" (mp4).
"""

import argparse
import base64
import json
import mimetypes
import sys
from pathlib import Path


def encode_media(path: Path) -> tuple[str, str]:
    """Return (mime_type, base64_data) for a local media file."""
    mime, _ = mimetypes.guess_type(str(path))
    if mime is None:
        # sensible fallback by extension
        ext = path.suffix.lower()
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".mp4": "video/mp4",
        }.get(ext, "application/octet-stream")
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return mime, data


def render_card(entry: dict) -> str:
    path = Path(entry["path"])
    if not path.exists():
        print(f"WARNING: missing file, skipping: {path}", file=sys.stderr)
        return ""
    mime, data = encode_media(path)
    label = entry.get("label", path.stem)
    caption = entry.get("caption", "")
    media_type = entry.get("type", "image")

    if media_type == "video":
        media_html = (
            f'<video controls loop muted playsinline class="pcb-media">'
            f'<source src="data:{mime};base64,{data}" type="{mime}"></video>'
        )
    else:
        media_html = f'<img src="data:{mime};base64,{data}" alt="{label}" class="pcb-media" />'

    caption_html = f'<p class="pcb-caption">{caption}</p>' if caption else ""
    return f"""
    <div class="pcb-card">
      {media_html}
      <h3 class="pcb-label">{label}</h3>
      {caption_html}
    </div>"""


def group_by_section(entries: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for e in entries:
        section = e.get("section", "Creatives")
        grouped.setdefault(section, []).append(e)
    return grouped


def build_html(entries: list[dict], title: str, accent: str, accent2: str) -> str:
    grouped = group_by_section(entries)
    sections_html = []
    for section_name, section_entries in grouped.items():
        cards = "".join(render_card(e) for e in section_entries)
        sections_html.append(f"""
        <section class="pcb-section">
          <h2 class="pcb-section-title">{section_name}</h2>
          <div class="pcb-grid">{cards}</div>
        </section>""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<style>
  :root {{
    --pcb-bg: #0a1220;
    --pcb-surface: #101b30;
    --pcb-border: rgba(255,255,255,0.08);
    --pcb-text: #e8edf5;
    --pcb-muted: #93a1b8;
    --pcb-accent: {accent};
    --pcb-accent-2: {accent2};
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--pcb-bg);
    color: var(--pcb-text);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    padding: 48px 32px;
  }}
  .pcb-title {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 8px;
    background: linear-gradient(90deg, var(--pcb-accent), var(--pcb-accent-2));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }}
  .pcb-subtitle {{ color: var(--pcb-muted); margin-bottom: 40px; }}
  .pcb-section {{ margin-bottom: 48px; }}
  .pcb-section-title {{
    font-size: 1.25rem;
    border-left: 3px solid var(--pcb-accent);
    padding-left: 12px;
    margin-bottom: 20px;
  }}
  .pcb-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
  }}
  .pcb-card {{
    background: var(--pcb-surface);
    border: 1px solid var(--pcb-border);
    border-radius: 12px;
    padding: 16px;
  }}
  .pcb-media {{
    width: 100%;
    border-radius: 8px;
    display: block;
    margin-bottom: 12px;
  }}
  .pcb-label {{ font-size: 1rem; margin: 0 0 4px 0; }}
  .pcb-caption {{ font-size: 0.85rem; color: var(--pcb-muted); margin: 0; }}
</style>
</head>
<body>
  <h1 class="pcb-title">{title}</h1>
  <p class="pcb-subtitle">Self-contained creative deck. All media embedded, no external files required.</p>
  {"".join(sections_html)}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifest", required=True, help="Path to JSON manifest file")
    parser.add_argument("--title", default="Creative Deck", help="Deck title")
    parser.add_argument("--accent", default="#38b6e8", help="Primary accent hex color")
    parser.add_argument("--accent2", default="#2b3990", help="Secondary accent hex color")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    entries = json.loads(manifest_path.read_text())

    html = build_html(entries, args.title, args.accent, args.accent2)
    Path(args.output).write_text(html)
    print(f"Wrote {args.output} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
