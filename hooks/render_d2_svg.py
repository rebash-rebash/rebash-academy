"""Render D2 diagrams to inline SVG at build time (no browser JS)."""

from __future__ import annotations

import hashlib
import logging
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.render_d2_svg")

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache" / "d2"
# Bump when render settings change so stale cache is ignored.
CACHE_VERSION = "v1-d2-theme5"
D2_FENCE = re.compile(r"```d2\s*\n(.*?)```", re.DOTALL)

# Mixed Berry Blue + dark mauve; ELK layout; compact pad for docs.
D2_THEME = "5"
D2_DARK_THEME = "200"
D2_LAYOUT = "elk"
D2_PAD = "40"


def _find_d2() -> str | None:
    env = os.environ.get("D2_BIN")
    if env and Path(env).is_file():
        return env
    return shutil.which("d2")


def _cache_path(source: str) -> Path:
    digest = hashlib.sha256(f"{CACHE_VERSION}\n{source}".encode("utf-8")).hexdigest()
    return CACHE_DIR / f"{digest}.svg"


def _normalize_svg(svg: str) -> str:
    """Make SVGs responsive inside the content column."""
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg, count=1)
    if re.search(r"<svg\b[^>]*\bwidth=", svg) is None:
        svg = svg.replace("<svg ", '<svg width="100%" ', 1)
    else:
        svg = re.sub(r'(<svg\b[^>]*?)\bwidth="[^"]*"', r'\1width="100%"', svg, count=1)
    svg = re.sub(r'(<svg\b[^>]*?)\bheight="[^"]*"\s*', r"\1", svg, count=1)
    if "max-width" not in svg[:400].lower():
        svg = re.sub(
            r"(<svg\b)",
            r'\1 style="max-width:100%;height:auto"',
            svg,
            count=1,
        )
    return svg


def _unique_svg_ids(svg: str, salt: str) -> str:
    """Avoid colliding IDs when multiple diagrams appear on one page."""
    # D2 already supports --salt; this is a safety net for cached SVGs.
    return svg.replace('id="d2-', f'id="{salt}-').replace("url(#d2-", f"url(#{salt}-")


def _render_svg(source: str, salt: str) -> str | None:
    cached = _cache_path(source)
    if cached.exists():
        return cached.read_text(encoding="utf-8")

    d2_bin = _find_d2()
    if not d2_bin:
        log.warning("D2 CLI not found on PATH (install from https://d2lang.com)")
        return None

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="rebash-d2-") as tmp:
        input_path = Path(tmp) / "diagram.d2"
        output_path = Path(tmp) / "diagram.svg"
        input_path.write_text(source.rstrip() + "\n", encoding="utf-8")

        command = [
            d2_bin,
            f"--theme={D2_THEME}",
            f"--dark-theme={D2_DARK_THEME}",
            f"--layout={D2_LAYOUT}",
            f"--pad={D2_PAD}",
            "--scale=1",
            "--no-xml-tag",
            "--omit-version",
            f"--salt={salt}",
            str(input_path),
            str(output_path),
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(ROOT),
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            log.warning("D2 CLI failed: %s", exc)
            return None

        if result.returncode != 0 or not output_path.exists():
            err = (result.stderr or result.stdout or "unknown error").strip()
            log.warning("D2 render error: %s", err[:500])
            return None

        svg = output_path.read_text(encoding="utf-8")
        cached.write_text(svg, encoding="utf-8")
        return svg


def on_page_markdown(markdown: str, page, config, files) -> str:
    if "```d2" not in markdown:
        return markdown

    counter = {"n": 0}

    def replace(match: re.Match[str]) -> str:
        source = match.group(1).strip()
        if not source:
            return match.group(0)

        salt = f"d2-{hashlib.sha1(source.encode()).hexdigest()[:10]}"
        svg = _render_svg(source, salt)
        if not svg:
            log.warning("Left D2 fence as code on %s", page.file.src_uri)
            return match.group(0)

        counter["n"] += 1
        svg = _normalize_svg(_unique_svg_ids(svg, salt))
        if 'role="img"' not in svg:
            svg = svg.replace("<svg ", '<svg role="img" aria-label="Diagram" ', 1)

        return f'\n<figure class="rebash-diagram" markdown="0">\n{svg}\n</figure>\n'

    updated = D2_FENCE.sub(replace, markdown)
    if counter["n"]:
        log.info("Rendered %s D2 diagram(s) on %s", counter["n"], page.file.src_uri)
    return updated
