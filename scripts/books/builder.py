"""Professional course book assembler and exporter."""

from __future__ import annotations

import html
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

import yaml

from .author import (
    AUTHOR_BIO_PARAGRAPHS,
    AUTHOR_EDUCATION,
    AUTHOR_HEADLINE,
    AUTHOR_LINKEDIN,
    AUTHOR_LOCATION,
    AUTHOR_NAME,
    AUTHOR_PHOTO,
    AUTHOR_ROLE,
    AUTHOR_WEBSITE,
)
from .cover_art import cover_art_svg
from .styles import BOOK_CSS, book_css, get_page_profile

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
BOOKS = ROOT / "books"
SITE_URL = "https://rebash.in"
AUTHOR_ASSET_NAME = "author.jpg"

SKIP_DEFAULT = frozenset(
    {
        "roadmap.md",
        "faq.md",
        "interview/index.md",
        "labs/index.md",
        "projects/index.md",
        "quizzes/index.md",
        "cheatsheets/index.md",
        "certifications/index.md",
        "capstone/index.md",
    }
)

STOP_INDEX = frozenset(
    """
    a an the and or of to in on for with from by as is are was were be been being
    this that these those it its you your we our they their if then else when what
    how why which who into over under about after before between through during
    also not no yes can may must should would could will just more most other such
    only own same so than too very using use used use use
    """.split()
)


def _ensure_homebrew_dyld() -> None:
    for libdir in ("/opt/homebrew/lib", "/usr/local/lib"):
        if not Path(libdir).is_dir():
            continue
        key = "DYLD_FALLBACK_LIBRARY_PATH"
        cur = os.environ.get(key, "")
        parts = [p for p in cur.split(":") if p]
        if libdir not in parts:
            os.environ[key] = ":".join([libdir, *parts]) if parts else libdir


_ensure_homebrew_dyld()


@dataclass
class Figure:
    fig_id: str
    chapter_num: int
    caption: str
    src: str  # relative to book out dir, e.g. assets/foo.svg


@dataclass
class Chapter:
    number: int
    title: str
    slug: str
    source: Path
    body_md: str
    module: str | None = None
    lab_url: str = ""
    figures: list[Figure] = field(default_factory=list)
    headings: list[tuple[str, str]] = field(default_factory=list)  # (id, text)
    index_terms: list[str] = field(default_factory=list)
    glossary: dict[str, str] = field(default_factory=dict)


def die(msg: str, code: int = 1) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def list_courses() -> list[str]:
    return sorted(p.parent.name for p in DOCS.glob("*/.pages"))


def load_pages(course: str) -> dict[str, Any]:
    path = DOCS / course / ".pages"
    if not path.is_file():
        die(f"no .pages for course '{course}' (expected {path})")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict) or "nav" not in data:
        die(f"{path} must contain a top-level 'nav' list")
    return data


def iter_nav(items: Iterable[Any], *, module: str | None = None) -> Iterable[tuple[str | None, str, str]]:
    for item in items:
        if isinstance(item, str):
            if item.endswith(".md"):
                stem = Path(item).stem.replace("-", " ").title()
                yield module, stem, item
            continue
        if not isinstance(item, dict):
            continue
        for key, value in item.items():
            key_s = str(key)
            if isinstance(value, str) and value.endswith(".md"):
                yield module, key_s, value
            elif isinstance(value, list):
                yield from iter_nav(value, module=key_s)


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    return (meta if isinstance(meta, dict) else {}), parts[2].lstrip("\n")


def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return s or "section"


def unescape_macros(text: str) -> str:
    text = re.sub(r"\{\{\s*'(\$\{#[^']+\})'\s*\}\}", r"\1", text)
    return text.replace("${{", "{{")


def strip_site_only_sections(text: str, course: str) -> str:
    """Remove Related/References (broken local links) and rewrite remaining course links.

    Important: never rewrite Markdown images ``![alt](path)`` — those must stay local
    so architecture diagrams can be copied into the book assets.
    """
    # Drop whole sections readers cannot use offline
    text = re.sub(
        r"^##\s+Related(?:\s+Tutorials)?\s*\n.*?(?=^##\s|\Z)",
        "",
        text,
        flags=re.M | re.S,
    )
    text = re.sub(
        r"^##\s+References\s*\n.*?(?=^##\s|\Z)",
        "",
        text,
        flags=re.M | re.S,
    )

    def link_repl(m: re.Match[str]) -> str:
        label, url = m.group(1), m.group(2).strip()
        # Skip image targets / media assets — handled by process_images_and_figures
        if re.search(r"\.(svg|png|jpe?g|gif|webp)(?:\s|$|\))", url, re.I):
            return m.group(0)
        if "/assets/" in url or url.startswith("../assets"):
            return m.group(0)
        if url.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        if url.startswith("../labs/") or url.startswith("../"):
            cleaned = url.replace("../", "").replace(".md", "").rstrip("/")
            return f"[{label}]({SITE_URL.rstrip('/')}/{cleaned}/)"
        if url.endswith(".md") or re.fullmatch(r"[a-z0-9][a-z0-9./-]*", url):
            slug = Path(url).stem
            return f"[{label}]({SITE_URL.rstrip('/')}/{course}/{slug}/)"
        return label  # drop unusable link, keep text

    # (?<!!) avoids matching the "[alt](url)" inside "![alt](url)"
    text = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    return text


def _md_fragment(text: str) -> str:
    """Render a Markdown fragment to HTML (for callout/answer bodies)."""
    import markdown as md

    return md.markdown(
        text.strip(),
        extensions=[
            "extra",
            "sane_lists",
            "tables",
            "fenced_code",
            "codehilite",
            "attr_list",
            "nl2br",
        ],
        extension_configs={
            "codehilite": {
                "guess_lang": True,
                "linenums": False,
                "noclasses": False,
                "pygments_style": "default",
            }
        },
        output_format="html5",
    )


def _md_inline(text: str) -> str:
    """Render inline Markdown (bold/code) for callout titles — no wrapping <p>."""
    import markdown as md

    html_out = md.markdown(
        text.strip(),
        extensions=["extra", "attr_list"],
        output_format="html5",
    ).strip()
    # markdown wraps a single line in <p>…</p>
    if html_out.startswith("<p>") and html_out.endswith("</p>") and html_out.count("<p>") == 1:
        html_out = html_out[3:-4].strip()
    return html_out


def convert_md_admonitions_to_html(text: str) -> str:
    """Convert !!! / ??? blocks to HTML callouts before the main Markdown pass.

    Interview ``??? success "Reveal answer"`` blocks become always-visible Answer
    callouts (no Reveal chrome). Bodies are Markdown-rendered here so nested
    formatting works outside the main document pass.
    """

    def strip_indent(body: str) -> str:
        lines = []
        for line in body.splitlines():
            if line.startswith("    "):
                lines.append(line[4:])
            elif line.startswith("\t"):
                lines.append(line[1:])
            else:
                lines.append(line)
        return "\n".join(lines).strip()

    def reveal_to_answer(m: re.Match[str]) -> str:
        # kind unused: book always shows the answer openly
        _kind, title, body = m.group(1), m.group(2), strip_indent(m.group(3))
        body_html = _md_fragment(body)
        # Drop interactive "Reveal answer" wording from printed books
        label = title.strip()
        if not label or label.lower() in {"reveal answer", "show answer", "answer"}:
            label = "Answer"
        return (
            f'\n<div class="callout callout-answer">'
            f'<p class="callout-title">{html.escape(label)}</p>\n'
            f"{body_html}\n</div>\n"
        )

    text = re.sub(
        r'^\?\?\?\s+(\w+)\s+"([^"]+)"\s*\n((?:[ \t].*\n?)*)',
        reveal_to_answer,
        text,
        flags=re.M,
    )
    # Untitled ??? blocks
    text = re.sub(
        r"^\?\?\?\s+(\w+)\s*\n((?:[ \t].*\n?)*)",
        lambda m: (
            f'\n<div class="callout callout-answer">'
            f'<p class="callout-title">Answer</p>\n'
            f"{_md_fragment(strip_indent(m.group(2)))}\n</div>\n"
        ),
        text,
        flags=re.M,
    )

    kind_map = {
        "tip": "tip",
        "hint": "tip",
        "note": "note",
        "info": "note",
        "warning": "warning",
        "caution": "warning",
        "danger": "danger",
        "bug": "danger",
        "failure": "danger",
        "success": "tip",
        "question": "interview",
        "abstract": "note",
    }

    def admon(m: re.Match[str]) -> str:
        raw_kind, title, body = m.group(1).lower(), m.group(2), strip_indent(m.group(3))
        kind = kind_map.get(raw_kind, "note")
        label_html = _md_inline(title) if title else html.escape(raw_kind.title())
        return (
            f'\n<div class="callout callout-{kind}">'
            f'<p class="callout-title">{label_html}</p>\n'
            f"{_md_fragment(body)}\n</div>\n"
        )

    text = re.sub(
        r'^!!!\s+(\w+)\s+"([^"]+)"\s*\n((?:[ \t].*\n?)*)',
        admon,
        text,
        flags=re.M,
    )

    def admon_untitled(m: re.Match[str]) -> str:
        raw_kind = m.group(1).lower()
        kind = kind_map.get(raw_kind, "note")
        body = strip_indent(m.group(2))
        return (
            f'\n<div class="callout callout-{kind}">'
            f'<p class="callout-title">{html.escape(m.group(1).title())}</p>\n'
            f"{_md_fragment(body)}\n</div>\n"
        )

    text = re.sub(
        r"^!!!\s+(\w+)\s*\n((?:[ \t].*\n?)*)",
        admon_untitled,
        text,
        flags=re.M,
    )
    return text


def wrap_try_it_yourself(text: str) -> str:
    """Insert a lab/challenge banner only — do not wrap the section in a <div>.

    Wrapping the body in HTML prevents Python-Markdown from parsing nested
    headings (so ``### Objective {#id}`` leaked as literal text and broke layout).
    """

    def insert_banner(title_pattern: str, label: str, text_in: str) -> str:
        pattern = rf"^(##|###) ({title_pattern})\s*$"

        def repl(m: re.Match[str]) -> str:
            return (
                f"{m.group(1)} {m.group(2)}\n\n"
                f'<div class="lab-banner">Try it yourself — {html.escape(label)}</div>'
            )

        return re.sub(pattern, repl, text_in, flags=re.M)

    text = insert_banner(r"Hands-on Lab", "Lab", text)
    text = insert_banner(r"Challenge exercise", "Challenge", text)
    return text


def mark_interview_block(text: str) -> str:
    """Insert an interview banner after the heading; leave Q&A as Markdown."""
    pattern = r"^(## Interview Questions)\s*$"

    def repl(m: re.Match[str]) -> str:
        return (
            f"{m.group(1)}\n\n"
            f'<div class="interview-banner">Interview practice</div>'
        )

    return re.sub(pattern, repl, text, flags=re.M)


# Headings / lab chrome that must never become index entries
_INDEX_HEADING_SKIP = re.compile(
    r"^(overview|prerequisites|learning objectives?|what (it|you)|why it|"
    r"how it works|key concepts|common (pitfalls|mistakes|errors)|best practices|"
    r"troubleshooting|security considerations|summary|next steps?|hands-on lab|"
    r"interview questions?|challenge exercise|objective|lab environment|"
    r"real-world scenario|step-by-step|validation|cleanup|learning outcomes|"
    r"task\s+\d+|step\s+\d+)",
    re.I,
)

# Commands / concepts worth indexing when seen in backticks
_INDEX_COMMAND_OK = frozenset(
    """
    apt apt-get dnf yum zypper apk rpm dpkg systemctl journalctl systemd-analyze
    cron crontab at ssh sshd ssh-keygen scp rsync sudo visudo useradd usermod
    groupadd passwd chmod chown chgrp umask ls ln findmnt df du lsblk blkid
    mount umount fdisk parted mkfs pvcreate vgcreate lvcreate free top ps kill
    pkill nice renice nohup tee grep awk sed cut sort uniq curl dig ping nc
    tcpdump iptables nft ufw fail2ban getenforce sestatus aa-status id getent
    uname hostnamectl timedatectl docker podman buildah runc nsenter unshare
    tar gzip openssl gpg chronyc ntpdate logrotate
    bash sh env printf read declare local export unset shift trap mapfile
    xargs find basename dirname realpath mktemp install jq yq curl wget
    shellcheck set getopts select case
    ip ss netstat route traceroute mtr dig host nslookup tcpdump wireshark
    nft iptables ip6tables ethtool nmcli resolvectl nginx haproxy envoy
    kubectl cilium calico bird
    python python3 pip venv pytest mypy ruff black poetry uv
    argparse click typer requests boto3 paramiko fabric docker
    pathlib asyncio subprocess logging json yaml
    """.split()
)


def extract_glossary_candidates(text: str) -> dict[str, str]:
    """Deprecated auto-scrape — books use curated docs/<course>/glossary.md only."""
    return {}


def extract_index_terms(text: str, meta: dict[str, Any]) -> list[str]:
    """Collect a small, useful index: tags + real commands + short topic headings."""
    terms: set[str] = set()
    for t in meta.get("tags") or []:
        if isinstance(t, str) and 1 < len(t) < 40:
            terms.add(t.replace("-", " ").strip())

    for m in re.finditer(r"^##\s+(.+)$", text, flags=re.M):
        h = re.sub(r"[`*_]", "", m.group(1)).strip()
        h = re.sub(r"\s*\{#[^}]+\}\s*$", "", h).strip()
        if not (3 < len(h) < 42):
            continue
        if _INDEX_HEADING_SKIP.search(h):
            continue
        if h.lower() in STOP_INDEX:
            continue
        terms.add(h)

    for m in re.finditer(r"`([A-Za-z][\w+-]{1,24})`", text):
        tok = m.group(1)
        base = tok.split("/")[-1].lower()
        if base in _INDEX_COMMAND_OK:
            terms.add(base)

    # Collapse case duplicates (prefer shorter / lowercase command form)
    by_lower: dict[str, str] = {}
    for t in terms:
        if t.lower() in STOP_INDEX:
            continue
        key = t.lower()
        prev = by_lower.get(key)
        if prev is None or (t.islower() and not prev.islower()) or len(t) < len(prev):
            by_lower[key] = t
    return sorted(by_lower.values(), key=str.lower)[:24]


def copy_image(src: Path, asset_dir: Path) -> str:
    dest = asset_dir / src.name
    if dest.exists() and dest.read_bytes() != src.read_bytes():
        dest = asset_dir / f"{src.stem}-{abs(hash(src.as_posix())) % 10_000}{src.suffix}"
    shutil.copy2(src, dest)
    return f"assets/{dest.name}"


def process_images_and_figures(
    text: str,
    course_dir: Path,
    asset_dir: Path,
    chapter_num: int,
    figures: list[Figure],
) -> str:
    """Copy local diagrams into the book and wrap them as numbered figures."""
    fig_counter = 0

    def resolve_image(path_part: str) -> Path | None:
        candidates = [
            (course_dir / path_part).resolve(),
            (DOCS / path_part.lstrip("./")).resolve(),
            (DOCS / "assets" / Path(path_part).name).resolve(),
            (DOCS / "assets" / "excalidraw" / Path(path_part).name).resolve(),
            (DOCS / "assets" / "images" / Path(path_part).name).resolve(),
        ]
        for cand in candidates:
            if cand.is_file():
                return cand
        return None

    def repl(m: re.Match[str]) -> str:
        nonlocal fig_counter
        alt, url = m.group(1), m.group(2).strip()
        # Already inlined as HTML figure from a prior pass
        if url.startswith(("data:",)):
            return m.group(0)

        path_part = unquote(url.split()[0].strip("<>"))
        # If a previous bad rewrite turned assets into site URLs, map back to docs/
        if path_part.startswith(("http://", "https://")):
            for prefix in (
                f"{SITE_URL.rstrip('/')}/assets/",
                "https://rebash.in/assets/",
                "http://rebash.in/assets/",
            ):
                if path_part.startswith(prefix):
                    rest = path_part[len(prefix) :].strip("/")
                    path_part = f"assets/{rest}"
                    break
            else:
                # External non-rebash image — leave as-is
                return m.group(0)

        src = resolve_image(path_part)
        if src is None:
            print(f"warning: missing diagram {path_part!r} (chapter {chapter_num})", file=sys.stderr)
            return m.group(0)

        rel = copy_image(src, asset_dir)
        fig_counter += 1
        fig_id = f"fig-{chapter_num}-{fig_counter}"
        caption = alt.strip() or f"Figure {chapter_num}.{fig_counter}"
        # Prefer shorter figure captions in the LOF
        if caption.lower().startswith("architecture diagram for "):
            caption = caption[len("Architecture diagram for ") :].strip()
        figures.append(
            Figure(
                fig_id=fig_id,
                chapter_num=chapter_num,
                caption=caption,
                src=rel,
            )
        )
        return (
            f'<figure class="figure" id="{fig_id}">'
            f'<img src="{html.escape(rel)}" alt="{html.escape(caption)}"/>'
            f"<figcaption>Figure {chapter_num}.{fig_counter}: {html.escape(caption)}</figcaption>"
            f"</figure>\n"
        )

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, text)


def add_heading_ids(text: str, chapter_num: int, headings: list[tuple[str, str]]) -> str:
    def repl(m: re.Match[str]) -> str:
        level = len(m.group(1))
        title = m.group(2).strip()
        # strip existing attr lists
        title = re.sub(r"\s*\{#[^}]+\}\s*$", "", title)
        hid = f"c{chapter_num}-{slugify(title)}"
        headings.append((hid, title))
        return f'{"#" * level} {title} {{#{hid}}}'

    return re.sub(r"^(#{2,3})\s+(.+)$", repl, text, flags=re.M)


def make_qr_png(url: str, dest: Path) -> None:
    import qrcode

    img = qrcode.make(url, border=1)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(dest))


def markdown_to_html(md_text: str) -> str:
    import markdown as md

    return md.markdown(
        md_text,
        extensions=[
            "extra",
            "sane_lists",
            "tables",
            "fenced_code",
            "codehilite",
            "attr_list",
            "nl2br",
        ],
        extension_configs={
            "codehilite": {
                "guess_lang": True,
                "linenums": False,
                "noclasses": False,
                "pygments_style": "default",
            }
        },
        output_format="html5",
    )


def load_optional_glossary(course: str) -> dict[str, str]:
    path = DOCS / course / "glossary.md"
    if not path.is_file():
        return {}
    _, body = split_frontmatter(path.read_text(encoding="utf-8"))
    gloss: dict[str, str] = {}
    for m in re.finditer(r"^[-*]\s+\*\*([^*]+)\*\*\s*[-:—]\s*(.+)$", body, flags=re.M):
        gloss[m.group(1).strip()] = m.group(2).strip()
    for m in re.finditer(r"^###?\s+(.+)\n\n(.+?)(?=\n#|\Z)", body, flags=re.S | re.M):
        gloss[m.group(1).strip()] = m.group(2).strip().split("\n\n")[0]
    return gloss


def collect_chapters(course: str, *, skip_index: bool) -> tuple[str, list[Chapter], Path]:
    data = load_pages(course)
    course_title = str(data.get("title") or course.replace("-", " ").title())
    course_dir = DOCS / course
    out_assets = BOOKS / course / "assets"
    out_assets.mkdir(parents=True, exist_ok=True)

    chapters: list[Chapter] = []
    seen: set[str] = set()
    num = 0
    for module, nav_title, filename in iter_nav(data["nav"]):
        rel = filename.replace("\\", "/")
        if rel in SKIP_DEFAULT:
            continue
        if skip_index and Path(rel).name == "index.md":
            continue
        if rel in seen:
            continue
        seen.add(rel)
        src = course_dir / rel
        if not src.is_file():
            print(f"warning: missing {src}", file=sys.stderr)
            continue
        meta, body = split_frontmatter(src.read_text(encoding="utf-8"))
        title = str(meta.get("title") or nav_title)
        slug = src.stem
        num += 1
        body = unescape_macros(body)
        body = re.sub(r"^#\s+.+\n+", "", body, count=1)

        # Diagrams first — while ../assets/... paths are still local
        figures: list[Figure] = []
        headings: list[tuple[str, str]] = []
        body = process_images_and_figures(body, course_dir, out_assets, num, figures)

        body = strip_site_only_sections(body, course)
        body = convert_md_admonitions_to_html(body)
        body = wrap_try_it_yourself(body)
        body = mark_interview_block(body)
        body = add_heading_ids(body, num, headings)
        gloss = extract_glossary_candidates(body)
        index_terms = extract_index_terms(body, meta)
        lab_url = f"{SITE_URL.rstrip('/')}/{course}/{slug}/"

        # QR
        qr_path = out_assets / f"qr-ch{num:02d}.png"
        make_qr_png(lab_url, qr_path)

        chapters.append(
            Chapter(
                number=num,
                title=title,
                slug=slug,
                source=src,
                body_md=body.strip() + "\n",
                module=module,
                lab_url=lab_url,
                figures=figures,
                headings=headings,
                index_terms=index_terms,
                glossary=gloss,
            )
        )
    if not chapters:
        die(f"no chapters for {course}")
    return course_title, chapters, course_dir


def ensure_author_photo(out_dir: Path) -> str | None:
    """Copy the author headshot into the book assets folder. Returns relative path or None."""
    if not AUTHOR_PHOTO.is_file():
        return None
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    dest = assets / AUTHOR_ASSET_NAME
    shutil.copy2(AUTHOR_PHOTO, dest)
    return f"assets/{AUTHOR_ASSET_NAME}"


def _pad_cover_to_trim(src: Path, dest: Path, canvas_w: int, canvas_h: int) -> None:
    """Letterbox cover art onto a trim canvas so footers are never cropped in PDF."""
    try:
        from PIL import Image
    except ImportError:
        shutil.copy2(src, dest)
        return
    raw = Image.open(src).convert("RGB")
    w, h = raw.size
    scale = min(canvas_w / w, canvas_h / h)
    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    fitted = raw.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (canvas_w, canvas_h), (11, 18, 32))  # book ink/navy
    canvas.paste(fitted, ((canvas_w - nw) // 2, (canvas_h - nh) // 2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, "PNG", optimize=True)


def ensure_cover_assets(
    out_dir: Path,
    course: str,
    course_title: str,
    *,
    page_size: str = "a4",
) -> dict[str, str]:
    """Prepare cover artwork. Prefer a designed PNG cover when present."""
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    profile = get_page_profile(page_size)
    canvas_w, canvas_h = profile["cover_px"]
    suffix = "" if page_size == "a4" else f"-{page_size.replace('/', '-')}"

    # Designed full-bleed covers: docs/assets/images/covers/<course>.png|.jpg
    # Prefer *-raw.png (unpadded source) when present, then pad to trim size.
    covers_dir = DOCS / "assets" / "images" / "covers"
    candidates = [
        covers_dir / f"{course}-raw.png",
        covers_dir / f"{course}.png",
        covers_dir / f"{course}.jpg",
        covers_dir / f"{course}.jpeg",
        covers_dir / f"{course}.webp",
    ]
    for src in candidates:
        if src.is_file():
            dest = assets / f"cover-{course}{suffix}.png"
            if src.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                _pad_cover_to_trim(src, dest, canvas_w, canvas_h)
            else:
                shutil.copy2(src, dest)
            paths["fullbleed"] = f"assets/{dest.name}"
            break

    # SVG fallback art (used when no designed PNG, or as background under overlay)
    cover_path = assets / "cover-art.svg"
    cover_path.write_text(cover_art_svg(course_title), encoding="utf-8")
    paths["art"] = "assets/cover-art.svg"

    logo_src = DOCS / "assets" / "images" / "logo.svg"
    if logo_src.is_file():
        logo_dest = assets / "logo.svg"
        shutil.copy2(logo_src, logo_dest)
        paths["logo"] = "assets/logo.svg"
    return paths


def render_cover(
    course_title: str,
    subtitle: str,
    author: str,
    year: int,
    photo_rel: str | None,
    cover_assets: dict[str, str] | None = None,
) -> str:
    cover_assets = cover_assets or {}
    fullbleed = cover_assets.get("fullbleed", "")

    # Designed marketing cover: full page image only (title/author already in artwork)
    if fullbleed:
        return f"""
<section class="cover cover-fullbleed">
  <img class="cover-fullbleed-img" src="{html.escape(fullbleed)}"
       alt="Cover: {html.escape(course_title)} by {html.escape(author)}"/>
</section>
"""

    art = cover_assets.get("art", "")
    logo = cover_assets.get("logo", "")
    art_img = (
        f'<img class="cover-art" src="{html.escape(art)}" alt=""/>'
        if art
        else ""
    )
    logo_img = (
        f'<img class="cover-logo" src="{html.escape(logo)}" alt="REBASH Academy"/>'
        if logo
        else ""
    )
    photo = ""
    if photo_rel:
        photo = (
            f'<img class="cover-photo" src="{html.escape(photo_rel)}" '
            f'alt="Portrait of {html.escape(author)}"/>'
        )
    return f"""
<section class="cover">
  {art_img}
  <div class="cover-overlay">
    <div class="cover-top">
      {logo_img}
      <div class="brand">REBASH Academy</div>
    </div>
    <hr class="rule"/>
    <h1>{html.escape(course_title)}</h1>
    <p class="subtitle">{html.escape(subtitle)}</p>
    <div class="cover-graphic-chips" aria-hidden="true">
      <span>Labs</span><span>CLI</span><span>Production habits</span>
    </div>
    <div class="meta">
      {photo}
      <p class="cover-author">{html.escape(author)}</p>
      <p>Course book · {year}</p>
      <p>rebash.in</p>
    </div>
  </div>
</section>
"""


def render_half_title(course_title: str) -> str:
    """KDP half-title: right-facing, title only, no headers/page numbers."""
    return f"""
<section class="half-title">
  <h1>{html.escape(course_title)}</h1>
  <p class="imprint">REBASH Academy</p>
</section>
"""


def render_title_page(course_title: str, subtitle: str, author: str) -> str:
    """KDP title page: right-facing; title, subtitle, author (no leading “by”)."""
    return f"""
<section class="title-page">
  <h1>{html.escape(course_title)}</h1>
  <p class="subtitle">{html.escape(subtitle)}</p>
  <p class="author">{html.escape(author)}</p>
  <p class="imprint">REBASH Academy · rebash.in</p>
</section>
"""


def render_copyright(course_title: str, author: str, year: int, *, kdp: bool = False) -> str:
    trim_note = (
        "<p>Paperback trim size: 6&nbsp;×&nbsp;9&nbsp;in (15.24&nbsp;×&nbsp;22.86&nbsp;cm). "
        "Interior: no bleed.</p>"
        if kdp
        else ""
    )
    return f"""
<section class="copyright-page frontmatter">
  <h1>Copyright</h1>
  <p><strong>{html.escape(course_title)}</strong></p>
  <p>Copyright © {year} {html.escape(author)} / REBASH Academy.</p>
  <p>All rights reserved. No part of this publication may be reproduced, distributed,
  or transmitted in commercial form without prior written permission, except for brief
  quotations in reviews or educational citations.</p>
  <p>Labs and online materials: <a href="{SITE_URL}">{SITE_URL}</a></p>
  <p><strong>Disclaimer:</strong> Commands and examples are for learning on practice systems.
  Always test changes on non-production hosts. The authors accept no liability for damage
  arising from use of this material.</p>
  <p>British English spelling is used throughout unless quoting product names or commands.</p>
  {trim_note}
  <p>Generated from the REBASH Academy curriculum on {date.today().isoformat()}.</p>
</section>
"""


def render_about_author(author: str, photo_rel: str | None, *, backmatter: bool = False) -> str:
    photo = ""
    if photo_rel:
        photo = (
            f'<img class="author-photo" src="{html.escape(photo_rel)}" '
            f'alt="Portrait of {html.escape(author)}"/>'
        )
    paras = "".join(f"<p>{html.escape(p)}</p>" for p in AUTHOR_BIO_PARAGRAPHS)
    place = "backmatter" if backmatter else "frontmatter"
    return f"""
<section class="about-author {place}" id="about-the-author">
  <h1>About the author</h1>
  <div class="author-card">
    {photo}
    <div class="author-meta">
      <p class="author-name">{html.escape(author)}</p>
      <p class="author-role">{html.escape(AUTHOR_ROLE)}</p>
      <p class="author-headline">{html.escape(AUTHOR_HEADLINE)}</p>
      <p class="author-location">{html.escape(AUTHOR_LOCATION)}</p>
      <p class="author-links">
        <a href="{html.escape(AUTHOR_LINKEDIN)}">LinkedIn</a>
        ·
        <a href="{html.escape(AUTHOR_WEBSITE)}">rebash.in</a>
      </p>
    </div>
  </div>
  {paras}
  <p><strong>Education:</strong> {html.escape(AUTHOR_EDUCATION)}</p>
</section>
"""


def render_toc(chapters: list[Chapter]) -> str:
    items = ['<section class="toc frontmatter" id="toc"><h1>Contents</h1><ul class="toc-list">']
    current_mod = None
    for ch in chapters:
        if ch.module and ch.module != current_mod:
            current_mod = ch.module
            items.append(f'<li class="mod">{html.escape(current_mod)}</li>')
        items.append(
            "<li>"
            f'<a href="#chapter-{ch.number}">Chapter {ch.number}. {html.escape(ch.title)}</a>'
            '<span class="dots"></span>'
            f'<a class="pg" href="#chapter-{ch.number}"></a>'
            "</li>"
        )
        for hid, htitle in ch.headings:
            if hid.startswith(f"c{ch.number}-") and htitle:
                # only ## level roughly: skip very long
                if len(htitle) > 70:
                    continue
                items.append(
                    "<li style=\"padding-left:1.1rem;font-size:0.88rem\">"
                    f'<a href="#{html.escape(hid)}">{html.escape(htitle)}</a>'
                    '<span class="dots"></span>'
                    f'<a class="pg" href="#{html.escape(hid)}"></a>'
                    "</li>"
                )
    items.append("</ul></section>")
    return "\n".join(items)


def render_lof(chapters: list[Chapter]) -> str:
    if not any(ch.figures for ch in chapters):
        return ""
    items = [
        '<section class="lof frontmatter" id="lof"><h1>List of figures</h1><ul class="lof-list">'
    ]
    for ch in chapters:
        for n, fig in enumerate(ch.figures, 1):
            items.append(
                "<li>"
                f'<a href="#{html.escape(fig.fig_id)}">Figure {ch.number}.{n}: {html.escape(fig.caption)}</a>'
                '<span class="dots"></span>'
                f'<a class="pg" href="#{html.escape(fig.fig_id)}"></a>'
                "</li>"
            )
    items.append("</ul></section>")
    return "\n".join(items)


def render_glossary(chapters: list[Chapter], course: str) -> str:
    """Render curated glossary only (docs/<course>/glossary.md)."""
    gloss = load_optional_glossary(course)
    # Soft merge: keep auto terms only if they look like real acronyms and glossary is thin
    if len(gloss) < 12:
        for ch in chapters:
            for k, v in ch.glossary.items():
                if re.fullmatch(r"[A-Z][A-Z0-9]{1,7}", k) and 12 <= len(v) <= 160:
                    gloss.setdefault(k, v)
    if not gloss:
        return ""

    # Cap length so the back matter stays useful
    items = sorted(gloss.items(), key=lambda kv: kv[0].lower())[:80]
    rows = []
    for term, definition in items:
        rows.append(f'<dt id="gloss-{html.escape(slugify(term))}">{html.escape(term)}</dt>')
        rows.append(f"<dd>{html.escape(definition)}</dd>")
    return (
        '<section class="glossary backmatter" id="glossary"><h1>Glossary</h1>'
        '<p class="backmatter-lead">Key terms used in this course. '
        "Acronyms are expanded on first use in the chapters as well.</p>"
        f"<dl>{''.join(rows)}</dl></section>"
    )


def render_index(chapters: list[Chapter]) -> str:
    """Compact index: commands and topics → chapter numbers (PDF page via target-counter)."""
    mapping: dict[str, list[int]] = {}
    display: dict[str, str] = {}  # lower -> preferred display form
    for ch in chapters:
        for term in ch.index_terms:
            key = term.strip()
            if len(key) < 2 or len(key) > 42:
                continue
            if _INDEX_HEADING_SKIP.search(key):
                continue
            if key.endswith((".txt", ".log", ".tgz", ".sh", ".md")):
                continue
            lk = key.lower()
            prev = display.get(lk)
            if prev is None or (key.islower() and not prev.islower()) or len(key) < len(prev):
                display[lk] = key
            mapping.setdefault(lk, [])
            if ch.number not in mapping[lk]:
                mapping[lk].append(ch.number)

    # Prefer terms that appear in more than one chapter; keep useful singles if few remain
    multi = {k: v for k, v in mapping.items() if len(v) >= 2}
    if len(multi) >= 40:
        mapping = multi
    else:
        # keep multi + a limited set of singles
        singles = sorted(
            ((k, v) for k, v in mapping.items() if len(v) == 1),
            key=lambda kv: kv[0].lower(),
        )
        mapping = dict(multi)
        for k, v in singles:
            if len(mapping) >= 120:
                break
            mapping[k] = v

    if not mapping:
        return ""

    items = [
        '<section class="index-section backmatter" id="index"><h1>Index</h1>',
        '<p class="backmatter-lead">Commands and topics with chapter page numbers.</p>',
        '<ul class="index-list">',
    ]
    current_letter = ""
    for lk in sorted(mapping.keys()):
        term = display.get(lk, lk)
        letter = term[0].upper() if term[0].isalpha() else "#"
        if letter != current_letter:
            current_letter = letter
            items.append(f'<li class="index-letter">{html.escape(letter)}</li>')
        links = " ".join(
            f'<a class="pg" href="#chapter-{num}"></a>' for num in mapping[lk]
        )
        items.append(
            "<li>"
            f'<span class="term">{html.escape(term)}</span>'
            '<span class="dots"></span>'
            f"{links}"
            "</li>"
        )
    items.append("</ul></section>")
    return "\n".join(items)


def render_chapter_html(ch: Chapter) -> str:
    body_html = markdown_to_html(ch.body_md)
    qr_rel = f"assets/qr-ch{ch.number:02d}.png"
    qr_block = f"""
<div class="lab-qr">
  <img src="{html.escape(qr_rel)}" alt="QR code for online lab"/>
  <div class="lab-qr-text">
    <strong>Online lab &amp; updates</strong>
    Scan or open the live tutorial (includes the hands-on lab):
    <a href="{html.escape(ch.lab_url)}">{html.escape(ch.lab_url)}</a>
  </div>
</div>
"""
    mod = f'<p class="chapter-kicker">{html.escape(ch.module)}</p>' if ch.module else ""
    return f"""
<section class="chapter" id="chapter-{ch.number}">
  <span class="chapter-title-mark">{html.escape(ch.title)}</span>
  {mod}
  <h1 class="chapter-heading">Chapter {ch.number}. {html.escape(ch.title)}</h1>
  {qr_block}
  {body_html}
</section>
"""


def write_html_book(
    out_dir: Path,
    course: str,
    course_title: str,
    chapters: list[Chapter],
    *,
    author: str,
    subtitle: str,
    page_size: str = "a4",
    include_cover: bool = True,
    html_name: str = "book.html",
    css_name: str = "book.css",
) -> Path:
    year = date.today().year
    kdp = page_size.startswith("kdp")
    css = book_css(page_size)
    (out_dir / css_name).write_text(css, encoding="utf-8")
    photo_rel = ensure_author_photo(out_dir)
    cover_assets = ensure_cover_assets(out_dir, course, course_title, page_size=page_size)

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en-GB">',
        "<head>",
        '<meta charset="utf-8"/>',
        f"<title>{html.escape(course_title)} — REBASH Academy</title>",
        f'<link rel="stylesheet" href="{html.escape(css_name)}"/>',
        "</head>",
        "<body>",
        f'<span class="course-title-mark">{html.escape(course_title)}</span>',
        f'<span class="author-name-mark">{html.escape(author)}</span>',
    ]
    if include_cover:
        parts.append(render_cover(course_title, subtitle, author, year, photo_rel, cover_assets))

    if kdp:
        # KDP front matter order:
        # https://kdp.amazon.com/en_US/help/topic/GDDYZG2C7RVF5N9J
        # half-title → title → copyright (verso) → TOC → (LOF) → body → back matter
        parts.extend(
            [
                render_half_title(course_title),
                render_title_page(course_title, subtitle, author),
                render_copyright(course_title, author, year, kdp=True),
                render_toc(chapters),
                render_lof(chapters),
            ]
        )
    else:
        parts.extend(
            [
                render_copyright(course_title, author, year, kdp=False),
                render_about_author(author, photo_rel),
                render_toc(chapters),
                render_lof(chapters),
            ]
        )

    for ch in chapters:
        # Module name is shown as the chapter kicker (no blank divider pages)
        parts.append(render_chapter_html(ch))

    if kdp:
        # Author bio is back matter on KDP (right-facing)
        parts.append(render_about_author(author, photo_rel, backmatter=True))
    parts.append(render_glossary(chapters, course))
    parts.append(render_index(chapters))
    parts.extend(["</body>", "</html>"])

    path = out_dir / html_name
    path.write_text("\n".join(p for p in parts if p), encoding="utf-8")
    return path


def write_markdown_book(out_dir: Path, course_title: str, chapters: list[Chapter], author: str) -> Path:
    photo_rel = ensure_author_photo(out_dir)
    parts = [
        "---",
        f'title: "{course_title}"',
        f'author: "{author}"',
        'lang: "en-GB"',
        "---",
        "",
        f"# {course_title}",
        "",
        f"Author: {author}",
        "",
        "## About the author",
        "",
    ]
    if photo_rel:
        parts.extend([f"![Portrait of {author}]({photo_rel})", ""])
    parts.extend(
        [
            f"**{author}** — {AUTHOR_ROLE}",
            "",
            f"*{AUTHOR_HEADLINE}*",
            "",
            f"{AUTHOR_LOCATION}",
            "",
            *[f"{p}\n" for p in AUTHOR_BIO_PARAGRAPHS],
            f"**Education:** {AUTHOR_EDUCATION}",
            "",
            f"LinkedIn: {AUTHOR_LINKEDIN}",
            "",
            f"Website: {AUTHOR_WEBSITE}",
            "",
            "## Contents",
            "",
        ]
    )
    for ch in chapters:
        parts.append(f"{ch.number}. {ch.title}")
    parts.append("")
    for ch in chapters:
        parts.extend(
            [
                "",
                f"# Chapter {ch.number}. {ch.title}",
                "",
                f"Online lab: {ch.lab_url}",
                "",
                ch.body_md,
                "",
            ]
        )
    path = out_dir / "book.md"
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def build_epub(html_path: Path, epub_path: Path, course_title: str, chapters: list[Chapter], out_dir: Path, author: str) -> None:
    from ebooklib import epub

    book = epub.EpubBook()
    book.set_identifier(f"rebash-{epub_path.stem}")
    book.set_title(course_title)
    book.set_language("en-GB")
    book.add_author(author)

    css = epub.EpubItem(
        uid="style",
        file_name="style/book.css",
        media_type="text/css",
        content=BOOK_CSS.encode("utf-8"),
    )
    book.add_item(css)

    photo_rel = ensure_author_photo(out_dir)
    cover_assets = ensure_cover_assets(out_dir, epub_path.stem, course_title)

    assets = out_dir / "assets"
    if assets.is_dir():
        for img in assets.iterdir():
            if not img.is_file():
                continue
            media = {
                ".svg": "image/svg+xml",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".gif": "image/gif",
                ".webp": "image/webp",
            }.get(img.suffix.lower(), "application/octet-stream")
            book.add_item(
                epub.EpubItem(
                    uid=f"img-{img.stem}",
                    file_name=f"assets/{img.name}",
                    media_type=media,
                    content=img.read_bytes(),
                )
            )
    # Cover chapter
    cover = epub.EpubHtml(title="Cover", file_name="cover.xhtml", lang="en-GB")
    cover.content = (
        "<html xmlns='http://www.w3.org/1999/xhtml'><head>"
        "<link rel='stylesheet' href='style/book.css'/></head><body>"
        + render_cover(
            course_title,
            "A practical course book from REBASH Academy",
            author,
            date.today().year,
            photo_rel,
            cover_assets,
        )
        + "</body></html>"
    )
    cover.add_item(css)
    book.add_item(cover)

    about = epub.EpubHtml(title="About the author", file_name="about.xhtml", lang="en-GB")
    about.content = (
        "<html xmlns='http://www.w3.org/1999/xhtml'><head>"
        "<link rel='stylesheet' href='style/book.css'/></head><body>"
        + render_about_author(author, photo_rel)
        + "</body></html>"
    )
    about.add_item(css)
    book.add_item(about)

    spine: list[Any] = ["nav", cover, about]
    toc = [cover, about]
    for ch in chapters:
        c = epub.EpubHtml(title=f"Chapter {ch.number}. {ch.title}", file_name=f"chap_{ch.number:02d}.xhtml", lang="en-GB")
        # chapter html already has assets/ paths
        inner = render_chapter_html(ch)
        c.content = (
            "<html xmlns='http://www.w3.org/1999/xhtml'><head>"
            f"<title>{html.escape(ch.title)}</title>"
            "<link rel='stylesheet' href='style/book.css'/></head><body>"
            f"{inner}</body></html>"
        )
        c.add_item(css)
        book.add_item(c)
        spine.append(c)
        toc.append(c)

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine
    epub.write_epub(str(epub_path), book)
    _ = html_path


def _finalize_kdp_pdf(pdf_path: Path) -> None:
    """Strip link annotations and ensure even page count for KDP manuscript upload.

    KDP treats hyperlink annotations as non-printable markup and often flags their
    bounding boxes as objects outside the margins.
    """
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        try:
            from PyPDF2 import PdfReader, PdfWriter  # type: ignore
        except ImportError:
            return

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    stripped = 0
    for page in reader.pages:
        if "/Annots" in page:
            try:
                del page["/Annots"]
                stripped += 1
            except Exception:  # noqa: BLE001
                pass
        writer.add_page(page)

    n = len(writer.pages)
    if n % 2 == 1:
        writer.add_blank_page(
            width=float(reader.pages[0].mediabox.width),
            height=float(reader.pages[0].mediabox.height),
        )
        print(f"  padded odd page count {n} → {n + 1} (blank last page)")

    tmp = pdf_path.with_suffix(".kdp.tmp.pdf")
    with tmp.open("wb") as fh:
        writer.write(fh)
    tmp.replace(pdf_path)
    if stripped:
        print(f"  stripped link annotations from {stripped} pages (KDP print-safe)")


def build_pdf(
    html_path: Path,
    pdf_path: Path,
    *,
    ensure_even_pages: bool = False,
    kdp_finalize: bool = False,
) -> None:
    from weasyprint import HTML

    HTML(filename=str(html_path), base_url=str(html_path.parent)).write_pdf(str(pdf_path))
    if kdp_finalize or ensure_even_pages:
        _finalize_kdp_pdf(pdf_path)


def which(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def build_kdp_pdfs(
    out_dir: Path,
    course: str,
    course_title: str,
    chapters: list[Chapter],
    *,
    author: str,
    subtitle: str,
    page_size: str = "kdp-6x9",
) -> tuple[Path, Path]:
    """Build KDP trim PDFs: with cover (preview) and interior (KDP manuscript)."""
    profile = get_page_profile(page_size)
    slug = page_size.replace("/", "-")
    css_name = f"book-{slug}.css"

    with_cover_html = write_html_book(
        out_dir,
        course,
        course_title,
        chapters,
        author=author,
        subtitle=subtitle,
        page_size=page_size,
        include_cover=True,
        html_name=f"book-{slug}.html",
        css_name=css_name,
    )
    interior_html = write_html_book(
        out_dir,
        course,
        course_title,
        chapters,
        author=author,
        subtitle=subtitle,
        page_size=page_size,
        include_cover=False,
        html_name=f"book-{slug}-interior.html",
        css_name=css_name,
    )

    with_cover_pdf = out_dir / f"{course}-{slug}.pdf"
    interior_pdf = out_dir / f"{course}-{slug}-interior.pdf"
    for stale in (with_cover_pdf, interior_pdf):
        if stale.is_file():
            stale.unlink()

    print(f"  KDP trim: {profile['label']} — {profile['notes']}")
    print(
        "  layout: half-title → title → copyright → TOC → chapters → "
        "about author → glossary → index (no interior bleed)"
    )
    build_pdf(with_cover_html, with_cover_pdf, kdp_finalize=True)
    print(f"  wrote {with_cover_pdf.relative_to(ROOT)} (with cover · preview)")
    build_pdf(interior_html, interior_pdf, kdp_finalize=True)
    print(f"  wrote {interior_pdf.relative_to(ROOT)} (no cover · KDP manuscript)")
    return with_cover_pdf, interior_pdf


def build_course(
    course: str,
    formats: set[str],
    *,
    skip_index: bool = True,
    author: str = AUTHOR_NAME,
    subtitle: str | None = None,
    page_size: str = "a4",
    kdp: bool = False,
) -> Path:
    course = course.strip().lower().rstrip("/")
    if course not in list_courses():
        die(f"unknown course '{course}'")
    if kdp:
        page_size = "kdp-6x9"
        formats = set(formats) | {"pdf"}
    try:
        profile = get_page_profile(page_size)
    except ValueError as exc:
        die(str(exc))

    course_title, chapters, _course_dir = collect_chapters(course, skip_index=skip_index)
    sub = subtitle or f"A practical {course_title} course book for Cloud & DevOps engineers"
    out_dir = BOOKS / course
    out_dir.mkdir(parents=True, exist_ok=True)

    if kdp:
        # Keep A4 free-download artefacts; only refresh KDP-named outputs.
        for pattern in (f"{course}-kdp-*.pdf", "book-kdp-*.html", "book-kdp-*.css"):
            for p in out_dir.glob(pattern):
                p.unlink()
    else:
        for pattern in ("*.epub", "*.pdf"):
            for p in out_dir.glob(pattern):
                # Preserve previously built KDP PDFs when rebuilding A4.
                if "-kdp-" in p.name:
                    continue
                p.unlink()
        for name in ("book.md", "book.html", "book.css"):
            p = out_dir / name
            if p.is_file():
                p.unlink()

    print(
        f"Assembling {len(chapters)} chapters for '{course_title}' "
        f"({profile['label']} · professional layout)…"
    )
    md_path = write_markdown_book(out_dir, course_title, chapters, author)
    print(f"  wrote {md_path.relative_to(ROOT)}")

    if kdp:
        try:
            build_kdp_pdfs(
                out_dir,
                course,
                course_title,
                chapters,
                author=author,
                subtitle=sub,
                page_size=page_size,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"  KDP PDF failed: {exc}", file=sys.stderr)
            raise
    else:
        html_path = write_html_book(
            out_dir,
            course,
            course_title,
            chapters,
            author=author,
            subtitle=sub,
            page_size=page_size,
            include_cover=True,
        )
        print(f"  wrote {html_path.relative_to(ROOT)}")

        if "epub" in formats:
            epub_path = out_dir / f"{course}.epub"
            try:
                build_epub(html_path, epub_path, course_title, chapters, out_dir, author)
                print(f"  wrote {epub_path.relative_to(ROOT)} (ebooklib)")
            except Exception as exc:  # noqa: BLE001
                print(f"  EPUB failed: {exc}", file=sys.stderr)
                if which("pandoc"):
                    subprocess.run(
                        [
                            "pandoc",
                            str(md_path),
                            "-o",
                            str(epub_path),
                            "--toc",
                            f"--metadata=title={course_title}",
                            f"--metadata=author={author}",
                            "--resource-path",
                            str(out_dir),
                        ],
                        check=True,
                    )
                    print(f"  wrote {epub_path.relative_to(ROOT)} (pandoc fallback)")

        if "pdf" in formats:
            pdf_name = f"{course}.pdf" if page_size == "a4" else f"{course}-{page_size}.pdf"
            pdf_path = out_dir / pdf_name
            try:
                build_pdf(html_path, pdf_path)
                print(f"  wrote {pdf_path.relative_to(ROOT)} (weasyprint)")
            except Exception as exc:  # noqa: BLE001
                print(f"  PDF failed: {exc}", file=sys.stderr)
                print(f"  HTML ready for print: {html_path.relative_to(ROOT)}", file=sys.stderr)

    # Feature checklist for operators
    figs = sum(len(c.figures) for c in chapters)
    cover_note = "cover+interior KDP pair" if kdp else "cover"
    print(
        f"  features: {cover_note}, copyright, about-the-author, TOC, LOF, syntax highlighting, "
        "headers/footers/page numbers, chapter numbers, glossary, index, "
        f"QR labs ({len(chapters)}), try-it-yourself + callouts"
        f" · figures={figs} · author={author} · page={page_size}"
    )
    return out_dir
