#!/usr/bin/env python3
"""
NotebookLM Pipeline Script for prospect-deck skill.

Creates a NotebookLM notebook, adds research source files, generates a slide deck,
and downloads the result.

Usage:
    python nbml_create.py \
        --name "Prospect Name — Company Prospect Deck" \
        --sources file1.md file2.md file3.md \
        --output /path/to/output.pptx \
        --format pptx \
        --length detailed
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path


def check_auth():
    """Check if notebooklm-py is authenticated."""
    try:
        from notebooklm import NotebookLM
        # Try to initialize; this checks for stored credentials
        client = NotebookLM()
        return True
    except Exception as e:
        print(f"AUTH_FAILED: {e}", file=sys.stderr)
        return False


async def create_notebook_and_slides(
    name: str,
    source_files: list[str],
    output_path: str,
    output_format: str = "pptx",
    length: str = "detailed",
):
    """
    Full pipeline: create notebook, add sources, generate slides, download.

    Returns a dict with:
        - notebook_id: the created notebook ID
        - notebook_url: URL to access the notebook
        - output_file: path to downloaded slide deck
        - source_count: number of sources added
    """
    from notebooklm import NotebookLM

    client = NotebookLM()
    result = {
        "notebook_id": None,
        "notebook_url": None,
        "output_file": None,
        "source_count": 0,
        "errors": [],
    }

    # Step 1: Create notebook
    print(f"Creating notebook: {name}", file=sys.stderr)
    try:
        notebook = await client.create_notebook(title=name)
        result["notebook_id"] = notebook.id
        result["notebook_url"] = f"https://notebooklm.google.com/notebook/{notebook.id}"
        print(f"Notebook created: {result['notebook_url']}", file=sys.stderr)
    except Exception as e:
        result["errors"].append(f"Failed to create notebook: {e}")
        print(json.dumps(result))
        sys.exit(1)

    # Step 2: Add source files
    for source_file in source_files:
        path = Path(source_file)
        if not path.exists():
            result["errors"].append(f"Source file not found: {source_file}")
            continue

        print(f"Adding source: {path.name}", file=sys.stderr)
        try:
            content = path.read_text()
            await notebook.add_source(
                content=content,
                title=path.stem.replace("_", " ").title(),
            )
            result["source_count"] += 1
        except Exception as e:
            result["errors"].append(f"Failed to add {path.name}: {e}")

    if result["source_count"] == 0:
        result["errors"].append("No sources were added. Cannot generate slides.")
        print(json.dumps(result))
        sys.exit(1)

    # Step 3: Generate slide deck
    print(f"Generating {output_format} slides ({length} mode)...", file=sys.stderr)
    try:
        slides = await notebook.generate_content(
            content_type="slides",
            format=output_format,
            length=length,
        )

        # Step 4: Download the output
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        await slides.download(str(output))
        result["output_file"] = str(output)
        print(f"Slides saved to: {output}", file=sys.stderr)

    except Exception as e:
        result["errors"].append(f"Slide generation failed: {e}")

    # Output result as JSON for the calling skill to parse
    print(json.dumps(result))
    return result


def main():
    parser = argparse.ArgumentParser(description="NotebookLM prospect deck pipeline")
    parser.add_argument("--name", required=True, help="Notebook title")
    parser.add_argument(
        "--sources", nargs="+", required=True, help="Paths to source markdown files"
    )
    parser.add_argument("--output", required=True, help="Output file path for slides")
    parser.add_argument(
        "--format",
        default="pptx",
        choices=["pptx", "pdf"],
        help="Output format (default: pptx)",
    )
    parser.add_argument(
        "--length",
        default="detailed",
        choices=["brief", "detailed", "presenter"],
        help="Slide detail level (default: detailed)",
    )
    parser.add_argument(
        "--check-auth",
        action="store_true",
        help="Just check authentication status and exit",
    )

    args = parser.parse_args()

    if args.check_auth:
        if check_auth():
            print(json.dumps({"authenticated": True}))
            sys.exit(0)
        else:
            print(json.dumps({"authenticated": False}))
            sys.exit(1)

    asyncio.run(
        create_notebook_and_slides(
            name=args.name,
            source_files=args.sources,
            output_path=args.output,
            output_format=args.format,
            length=args.length,
        )
    )


if __name__ == "__main__":
    main()
