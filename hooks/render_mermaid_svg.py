"""Render Mermaid diagrams to inline SVG at build time (no browser JS)."""

from __future__ import annotations

import hashlib
import logging
import re
import subprocess
import tempfile
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.render_mermaid_svg")

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache" / "mermaid"
MERMAID_CLI = "@mermaid-js/mermaid-cli@11.4.0"
MERMAID_CONFIG = ROOT / "config" / "mermaid-build.json"
MERMAID_FENCE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)


def _cache_path(source: str) -> Path:
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    return CACHE_DIR / f"{digest}.svg"


def _unique_svg_ids(svg: str, prefix: str) -> str:
    """Avoid colliding SVG ids when multiple diagrams appear on one page."""
    svg = svg.replace('id="my-svg"', f'id="{prefix}"', 1)
    svg = svg.replace("#my-svg", f"#{prefix}")
    svg = svg.replace("my-svg_", f"{prefix}_")
    svg = svg.replace("my-svg-", f"{prefix}-")
    return svg


def _render_svg(source: str) -> str | None:
    cached = _cache_path(source)
    if cached.exists():
        return cached.read_text(encoding="utf-8")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="rebash-mermaid-") as tmp:
        input_path = Path(tmp) / "diagram.mmd"
        output_path = Path(tmp) / "diagram.svg"
        input_path.write_text(source + "\n", encoding="utf-8")

        command = [
            "npx",
            "--yes",
            MERMAID_CLI,
            "-i",
            str(input_path),
            "-o",
            str(output_path),
            "-b",
            "transparent",
        ]
        if MERMAID_CONFIG.exists():
            command.extend(["-c", str(MERMAID_CONFIG)])

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=180,
                cwd=str(ROOT),
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            log.warning("Mermaid CLI failed: %s", exc)
            return None

        if result.returncode != 0 or not output_path.exists():
            err = (result.stderr or result.stdout or "unknown error").strip()
            log.warning("Mermaid render error: %s", err[:400])
            return None

        svg = output_path.read_text(encoding="utf-8")
        cached.write_text(svg, encoding="utf-8")
        return svg


def on_page_markdown(markdown: str, page, config, files) -> str:
    if "```mermaid" not in markdown:
        return markdown

    counter = {"n": 0}

    def replace(match: re.Match[str]) -> str:
        source = match.group(1).strip()
        if not source:
            return match.group(0)

        svg = _render_svg(source)
        if not svg:
            log.warning("Left Mermaid fence as code on %s", page.file.src_uri)
            return match.group(0)

        counter["n"] += 1
        prefix = f"mmd-{hashlib.sha1(source.encode()).hexdigest()[:10]}"
        svg = _unique_svg_ids(svg, prefix)
        if 'role="img"' not in svg:
            svg = svg.replace("<svg ", '<svg role="img" aria-label="Diagram" ', 1)

        return (
            f'\n<figure class="rebash-diagram" markdown="0">\n{svg}\n</figure>\n'
        )

    updated = MERMAID_FENCE.sub(replace, markdown)
    if counter["n"]:
        log.info("Rendered %s Mermaid diagram(s) on %s", counter["n"], page.file.src_uri)
    return updated
