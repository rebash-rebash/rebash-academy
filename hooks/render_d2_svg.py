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
CACHE_VERSION = "v7-svg-intrinsic-size"
D2_FENCE = re.compile(r"```d2\s*\n(.*?)```", re.DOTALL)

# Flagship theme; dagre with wider node/edge separation for clean arrows.
D2_THEME = "3"
D2_DARK_THEME = "201"
D2_LAYOUT = "dagre"
D2_PAD = "48"
D2_NODESEP = "110"
D2_EDGESEP = "70"

# Applied to every diagram unless it already defines global node styles.
STYLE_PREAMBLE = """
*: {
  style: {
    border-radius: 16
    font-size: 16
    bold: true
    shadow: true
    stroke-width: 2
  }
}

(** -> **)[*]: {
  style: {
    stroke-width: 2
    font-size: 13
    bold: true
    font-color: "#0f172a"
  }
}
""".strip()


def _find_d2() -> str | None:
    env = os.environ.get("D2_BIN")
    if env and Path(env).is_file():
        return env
    return shutil.which("d2")


def _cache_path(source: str) -> Path:
    digest = hashlib.sha256(f"{CACHE_VERSION}\n{source}".encode("utf-8")).hexdigest()
    return CACHE_DIR / f"{digest}.svg"


def _normalize_quoted_newlines(source: str) -> str:
    """Keep D2's \\n escape; collapse converter-doubled \\\\n in quoted labels."""

    def _fix(match: re.Match[str]) -> str:
        text = match.group(0)
        # File often has \\\\n (two backslashes) after _quote() escaped \\n.
        while "\\\\n" in text:
            text = text.replace("\\\\n", "\\n")
        return text

    return re.sub(r'"(?:\\.|[^"\\])*"', _fix, source)


def _with_style(source: str) -> str:
    """Inject REBASH visual defaults without clobbering author styles."""
    source = _normalize_quoted_newlines(source)

    # Strip animated edges — dashed motion often overlaps and looks noisy.
    source = re.sub(r"(?m)^\s*style\.animated:\s*true\s*\n?", "", source)
    source = re.sub(r"(?m)^\s*animated:\s*true\s*\n?", "", source)

    if re.search(r"(?m)^\*:\s*\{", source):
        # Still bump edge label readability when author provided *: block.
        if "font-color:" not in source and "(** -> **)[*]" not in source:
            source = (
                source.rstrip()
                + "\n\n(** -> **)[*]: {\n"
                + "  style.stroke-width: 2\n"
                + "  style.font-size: 13\n"
                + "  style.bold: true\n"
                + '  style.font-color: "#0f172a"\n'
                + "}\n"
            )
        return source
    if "border-radius:" in source:
        return source
    return f"{STYLE_PREAMBLE}\n\n{source.strip()}\n"


def _normalize_svg(svg: str) -> str:
    """Center diagrams and keep intrinsic size so CSS frames can hug content."""
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg, count=1)
    # Drop opaque white page background so the figure card shows through.
    svg = re.sub(
        r'<rect\b[^>]*class="[^"]*fill-N7[^"]*"[^>]*stroke-width="0"\s*/>',
        "",
        svg,
        count=1,
    )
    svg = re.sub(
        r'<rect\b[^>]*fill="#FFFFFF"[^>]*stroke-width="0"\s*/>',
        "",
        svg,
        count=1,
    )
    # Center content inside the SVG viewport when letterboxed.
    if "preserveAspectRatio=" in svg:
        svg = re.sub(
            r'preserveAspectRatio="[^"]*"',
            'preserveAspectRatio="xMidYMid meet"',
            svg,
            count=1,
        )
    else:
        svg = svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1)

    # Ensure the outer <svg> has explicit width/height from viewBox.
    # Without them, width:fit-content frames + max-width:100% collapse to ~0.
    open_tag = re.match(r"<svg\b[^>]*>", svg)
    if open_tag:
        tag = open_tag.group(0)
        vb = re.search(r'\bviewBox="([^"]+)"', tag)
        has_w = re.search(r'\bwidth="[^"]*"', tag)
        has_h = re.search(r'\bheight="[^"]*"', tag)
        if vb and (not has_w or not has_h):
            parts = vb.group(1).split()
            if len(parts) == 4:
                try:
                    w = abs(float(parts[2]))
                    h = abs(float(parts[3]))
                    attrs = ""
                    if not has_w:
                        attrs += f' width="{w:g}"'
                    if not has_h:
                        attrs += f' height="{h:g}"'
                    svg = svg.replace(tag, tag[:-1] + attrs + ">", 1)
                except ValueError:
                    pass

    # Soft constraints only — do not force width/height:auto (collapses fit-content).
    style = 'style="max-width:100%;height:auto;display:block;margin:0 auto"'
    if re.search(r"<svg\b[^>]*\bstyle=", svg):
        svg = re.sub(r'(<svg\b[^>]*?)\bstyle="[^"]*"', rf"\1{style}", svg, count=1)
    else:
        svg = re.sub(r"(<svg\b)", rf"\1 {style}", svg, count=1)
    return svg


def _unique_svg_ids(svg: str, salt: str) -> str:
    """Avoid colliding IDs when multiple diagrams appear on one page."""
    return svg.replace('id="d2-', f'id="{salt}-').replace("url(#d2-", f"url(#{salt}-")


def _render_svg(source: str, salt: str) -> str | None:
    source = _with_style(source)
    cached = _cache_path(source)
    if cached.exists():
        return cached.read_text(encoding="utf-8")

    d2_bin = _find_d2()
    if not d2_bin:
        log.warning("D2 CLI not found on PATH (install from https://d2lang.com)")
        return None

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Prefer dagre (cleaner arrows); fall back to spaced ELK for nested-edge graphs.
    attempts = [
        [
            f"--layout={D2_LAYOUT}",
            f"--dagre-nodesep={D2_NODESEP}",
            f"--dagre-edgesep={D2_EDGESEP}",
        ],
        [
            "--layout=elk",
            "--elk-nodeNodeBetweenLayers=120",
            "--elk-edgeNodeBetweenLayers=80",
            "--elk-padding=[top=40,left=40,bottom=40,right=40]",
        ],
    ]

    with tempfile.TemporaryDirectory(prefix="rebash-d2-") as tmp:
        input_path = Path(tmp) / "diagram.d2"
        output_path = Path(tmp) / "diagram.svg"
        input_path.write_text(source.rstrip() + "\n", encoding="utf-8")

        last_err = ""
        for layout_flags in attempts:
            command = [
                d2_bin,
                f"--theme={D2_THEME}",
                f"--dark-theme={D2_DARK_THEME}",
                *layout_flags,
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

            if result.returncode == 0 and output_path.exists():
                svg = output_path.read_text(encoding="utf-8")
                cached.write_text(svg, encoding="utf-8")
                return svg

            last_err = (result.stderr or result.stdout or "unknown error").strip()
            output_path.unlink(missing_ok=True)

        log.warning("D2 render error: %s", last_err[:500])
        return None


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
