#!/usr/bin/env python3
"""
LakeB2B document builder.

Renders a LakeB2B HTML document (built from this skill's template and
components) into a polished, print-ready PDF using WeasyPrint. WeasyPrint gives
faithful print-CSS fidelity for the green/gold palette, gradients, the cover
scene SVG, tables, and the running footer.

Usage:
    python build_pdf.py input.html                  # -> input.pdf
    python build_pdf.py input.html output.pdf
    python build_pdf.py input.html output.pdf --vars vars.json

--vars (optional): a JSON object of {{TOKEN}} -> value replacements applied to
the HTML before rendering. Tokens that are not present in the JSON are left
untouched, so a finished template with no tokens renders exactly as written.
Any {{TOKENS}} still present after substitution are reported so nothing ever
ships with a raw {{...}} visible.

Dependencies:
    pip install weasyprint --break-system-packages

Fonts:
    Headlines use Lora, body uses Poppins (both ship with most google-fonts
    packages). The template CSS falls back to Georgia / DejaVu Serif and a
    system sans if those are missing, so it always renders.
"""
import json
import re
import sys
from pathlib import Path


def load_vars(path):
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def apply_vars(html, variables):
    for key, value in variables.items():
        html = html.replace("{{" + key + "}}", str(value))
    return html


def render(html, out_path, base_dir):
    try:
        from weasyprint import HTML
    except ImportError:
        print("WeasyPrint is not installed. Run:")
        print("    pip install weasyprint --break-system-packages")
        return 2
    HTML(string=html, base_url=str(base_dir)).write_pdf(str(out_path))
    print(f"Wrote {out_path}")
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1

    in_path = Path(argv[1])
    if not in_path.exists():
        print(f"Input not found: {in_path}")
        return 1

    out_path = None
    if len(argv) > 2 and not argv[2].startswith("--"):
        out_path = Path(argv[2])
    if out_path is None:
        out_path = in_path.with_suffix(".pdf")

    variables = {}
    if "--vars" in argv:
        variables = load_vars(argv[argv.index("--vars") + 1])

    html = in_path.read_text(encoding="utf-8")
    html = apply_vars(html, variables)

    leftover = sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", html)))
    if leftover:
        print("Warning: unfilled tokens left in output: " + ", ".join(leftover))

    return render(html, out_path, in_path.parent)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
