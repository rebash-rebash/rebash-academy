"""Print/EPUB stylesheet for professional course books (compact layout)."""

from __future__ import annotations

from typing import TypedDict


class PageProfile(TypedDict):
    label: str
    size_css: str
    width: str
    height: str
    margin_top: str
    margin_outside: str
    margin_bottom: str
    margin_inside: str
    mirrored: bool
    cover_px: tuple[int, int]
    notes: str


# Amazon KDP popular trade paperback trim. Interior manuscript page size must
# equal the trim size. Cover wrap is uploaded separately in KDP; the "with
# cover" PDF here is for preview / complete-book distribution.
PAGE_PROFILES: dict[str, PageProfile] = {
    "a4": {
        "label": "A4",
        "size_css": "A4",
        "width": "210mm",
        "height": "297mm",
        "margin_top": "14mm",
        "margin_outside": "12mm",
        "margin_bottom": "16mm",
        "margin_inside": "12mm",
        "mirrored": False,
        "cover_px": (2480, 3508),  # A4 @ ~300 dpi
        "notes": "Default academy download size",
    },
    "kdp-6x9": {
        "label": 'KDP 6" × 9"',
        "size_css": "6in 9in",
        "width": "6in",
        "height": "9in",
        # No-bleed interior (KDP: page size = trim).
        # Minima for 151–300 pages: gutter ≥0.5", outer/top/bottom ≥0.25".
        # Use generous values so running heads in margin boxes and wide code
        # still clear KDP's live-area check.
        # https://kdp.amazon.com/help/topic/GVBQ3CMEQW3W2VL6
        "margin_top": "0.7in",
        "margin_outside": "0.65in",
        "margin_bottom": "0.7in",
        "margin_inside": "0.75in",
        "mirrored": True,
        "cover_px": (1800, 2700),  # 6x9 @ 300 dpi
        "notes": "Amazon KDP paperback trim 6 x 9 in, no bleed (15.24 x 22.86 cm)",
    },
}


def list_page_profiles() -> list[str]:
    return list(PAGE_PROFILES)


def get_page_profile(page_size: str) -> PageProfile:
    key = page_size.strip().lower()
    if key not in PAGE_PROFILES:
        known = ", ".join(PAGE_PROFILES)
        raise ValueError(f"unknown page size {page_size!r}; choose one of: {known}")
    return PAGE_PROFILES[key]


def _mirrored_margin_block(profile: PageProfile, page_name: str = "") -> str:
    """Emit :left/:right margin rules so named pages keep KDP gutters."""
    sel = f"{page_name}:" if page_name else ""
    return f"""
@page {sel}left {{
  size: {profile["size_css"]};
  margin-top: {profile["margin_top"]};
  margin-bottom: {profile["margin_bottom"]};
  margin-left: {profile["margin_outside"]};
  margin-right: {profile["margin_inside"]};
}}
@page {sel}right {{
  size: {profile["size_css"]};
  margin-top: {profile["margin_top"]};
  margin-bottom: {profile["margin_bottom"]};
  margin-left: {profile["margin_inside"]};
  margin-right: {profile["margin_outside"]};
}}
""".strip()


def _page_chrome(profile: PageProfile, *, kdp: bool = False) -> str:
    """Generate @page rules for WeasyPrint.

    KDP: keep running heads compact (no full-width border rules that can
    paint into the gutter). Named pages must repeat mirrored margins —
    otherwise WeasyPrint falls back to undersized defaults and KDP flags
    “Insufficient gutter”.
    """
    if kdp:
        # Minimal chrome — page number only. Running heads as margin-box
        # text are a common KDP “text outside margins” false positive when
        # combined with tight top margins; body pages rely on larger margins.
        header_footer = """
  @bottom-center {
    content: counter(page);
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 9pt;
    color: #334155;
    padding-top: 2mm;
  }
""".rstrip()
    else:
        header_footer = """
  @top-left {
    content: string(course-title);
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 8pt;
    color: #64748b;
    vertical-align: bottom;
    padding-bottom: 2mm;
    border-bottom: 0.35pt solid #e2e8f0;
    width: 68%;
  }
  @top-right {
    content: string(chapter-title);
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 8pt;
    color: #64748b;
    vertical-align: bottom;
    padding-bottom: 2mm;
    border-bottom: 0.35pt solid #e2e8f0;
    text-align: right;
    width: 32%;
  }
  @bottom-center {
    content: counter(page);
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 8.5pt;
    color: #334155;
  }
""".rstrip()

    if profile["mirrored"]:
        margins = f"""
@page {{
  size: {profile["size_css"]};
{header_footer}
}}
{_mirrored_margin_block(profile)}
""".strip()
    else:
        margins = f"""
@page {{
  size: {profile["size_css"]};
  margin: {profile["margin_top"]} {profile["margin_outside"]} {profile["margin_bottom"]} {profile["margin_inside"]};
{header_footer}
}}
""".strip()

    extras = ""
    if kdp and profile["mirrored"]:
        # Repeat gutters on every named page used by the KDP layout.
        silent_chrome = """
  @top-left { content: none; border: none; }
  @top-right { content: none; border: none; }
  @bottom-center { content: none; }
""".rstrip()
        extras = f"""
{_mirrored_margin_block(profile, "frontmatter-silent")}
@page frontmatter-silent {{
  size: {profile["size_css"]};
{silent_chrome}
}}
{_mirrored_margin_block(profile, "frontmatter")}
@page frontmatter {{
  size: {profile["size_css"]};
{silent_chrome}
}}
@page :first {{
  size: {profile["size_css"]};
{silent_chrome}
}}
""".strip()
    else:
        extras = """
@page :first {
  @top-left { content: none; border: none; }
  @top-right { content: none; border: none; }
  @bottom-center { content: none; }
}

@page frontmatter {
  @top-left { content: none; border: none; }
  @top-right { content: none; border: none; }
  @bottom-center {
    content: counter(page, lower-roman);
    font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
    font-size: 8.5pt;
    color: #334155;
  }
}

@page frontmatter-silent {
  @top-left { content: none; border: none; }
  @top-right { content: none; border: none; }
  @bottom-center { content: none; }
}
""".strip()

    return (
        f"/* ===== Page chrome (WeasyPrint / print) — {profile['label']} ===== */\n"
        f"{margins}\n\n"
        f"{extras}\n"
    )


# KDP paperback interior layout overrides
# https://kdp.amazon.com/en_US/help/topic/GDDYZG2C7RVF5N9J
# https://kdp.amazon.com/help/topic/GVBQ3CMEQW3W2VL6
KDP_LAYOUT_CSS = r"""
/* --- KDP manuscript structure --- */
.author-name-mark { string-set: author-name content(); display: none; }

.half-title,
.title-page,
.copyright-page,
.toc,
.lof,
.blank-page {
  page: frontmatter-silent;
}

.half-title,
.title-page,
.toc,
.lof,
#chapter-1,
.backmatter {
  break-before: right;
  page-break-before: right;
}

.copyright-page {
  break-before: left;
  page-break-before: left;
}

.blank-page {
  break-after: page;
  page-break-after: always;
  height: 0.1in;
  visibility: hidden;
}

.half-title {
  break-after: page;
  page-break-after: always;
  text-align: center;
  padding-top: 2.2in;
}
.half-title h1 {
  font-size: 1.45rem;
  font-weight: 700;
  margin: 0;
  color: var(--ink);
}
.half-title .imprint {
  margin-top: 1.8in;
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.85rem;
  color: var(--muted);
}

.title-page {
  break-after: page;
  page-break-after: always;
  text-align: center;
  padding-top: 1.5in;
}
.title-page h1 {
  font-size: 1.75rem;
  margin: 0 0 0.5rem;
}
.title-page .subtitle {
  font-family: "Source Sans 3", sans-serif;
  font-size: 1rem;
  color: var(--muted);
  margin: 0 0 1.2rem;
  font-weight: 400;
}
.title-page .author {
  font-family: "Source Sans 3", sans-serif;
  font-size: 1.1rem;
  margin: 1.2rem 0 0;
  font-weight: 600;
}
.title-page .imprint {
  margin-top: 1.8in;
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.85rem;
  color: var(--muted);
}

.copyright-page {
  break-after: page;
  page-break-after: always;
  font-size: 0.88rem;
}
.copyright-page h1 { font-size: 1.05rem; }

.toc, .lof {
  break-after: page;
  page-break-after: always;
}

/* Body text — KDP guidance: justified */
.chapter p {
  text-align: justify;
  hyphens: auto;
}
.chapter > p {
  text-indent: 1.15em;
  margin: 0 0 0.15rem;
}
.chapter > h1 + p,
.chapter > h2 + p,
.chapter > h3 + p,
.chapter > h4 + p,
.chapter > .chapter-kicker + h1 + p,
.chapter > .lab-banner + p,
.chapter > .interview-banner + p,
.chapter > .figure + p,
.chapter > .callout + p,
.chapter > pre + p,
.chapter > .highlight + p {
  text-indent: 0;
}

/* Hard clip: nothing may paint outside the content box */
img, svg, .figure, .figure img, .lab-qr img {
  max-width: 100% !important;
  height: auto !important;
}
pre, .codehilite, .highlight, .highlight pre, .codehilite pre {
  overflow: hidden !important;
  overflow-x: hidden !important;
  white-space: pre-wrap !important;
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
  max-width: 100% !important;
  font-size: 0.72em !important;
}
table {
  table-layout: fixed !important;
  width: 100% !important;
  max-width: 100% !important;
}
th, td {
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
}
.toc-list, .lof-list, .index-list {
  max-width: 100%;
}
/* Index page numbers were painting past the trim (KDP object/text errors). */
.index-list {
  columns: 2 !important;
  column-gap: 0.3in !important;
  column-fill: auto;
  font-size: 0.7rem !important;
  max-width: 100% !important;
  overflow: hidden !important;
}
.index-list li {
  max-width: 100% !important;
  overflow: hidden !important;
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
  display: block !important;
}
.index-list .dots {
  display: none !important; /* leader dots + long page lists overflow columns */
}
.index-list .pg,
.index-list .pg::after {
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
}
.lab-qr {
  max-width: 100%;
  overflow: hidden;
}
.lab-qr a, .lab-qr .lab-qr-text {
  word-break: break-all;
  overflow-wrap: anywhere;
}

/* Print PDF: no interactive links (KDP strips them as non-printable markup
   and link annotation boxes often fail the margin check). */
a {
  color: inherit;
  text-decoration: none;
}

.about-author.backmatter h1,
.glossary.backmatter h1,
.index-section.backmatter h1 {
  break-after: avoid;
}
"""


_BODY_TEMPLATE = '''
:root {
  /* Page geometry — set by book_css(profile) */
  --page-w: __PAGE_W__;
  --page-h: __PAGE_H__;
  --m-top: __M_TOP__;
  --m-out: __M_OUT__;
  --m-bot: __M_BOT__;
  --m-in: __M_IN__;
  --ink: #0f172a;
  --muted: #475569;
  --accent: #0f766e;
  --accent-soft: #ccfbf1;
  --border: #cbd5e1;
  --code-bg: #f1f5f9;
  --warn: #b45309;
  --warn-bg: #fffbeb;
  --tip: #0369a1;
  --tip-bg: #f0f9ff;
  --note: #334155;
  --note-bg: #f8fafc;
  --danger: #b91c1c;
  --danger-bg: #fef2f2;
  --try: #166534;
  --try-bg: #f0fdf4;
  --interview: #6d28d9;
  --interview-bg: #f5f3ff;
}

html { font-size: 10pt; }
body {
  font-family: "Source Serif 4", "Iowan Old Style", Palatino, "Palatino Linotype", serif;
  color: var(--ink);
  line-height: 1.38;
  hyphens: auto;
}

h1, h2, h3, h4 {
  font-family: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  color: var(--ink);
  line-height: 1.22;
  hyphens: none;
}
/* Only keep chapter titles glued to the next line — not every h2/h3
   (avoid + large following block = empty pages in WeasyPrint). */
h1.chapter-heading {
  break-after: avoid;
  page-break-after: avoid;
}
h2 + .lab-banner,
h2 + .interview-banner,
h3 + .lab-banner {
  break-before: avoid;
  page-break-before: avoid;
}
h1 { font-size: 1.45rem; margin: 0 0 0.55rem; }
h2 { font-size: 1.15rem; margin: 0.95rem 0 0.4rem; }
h3 { font-size: 1.02rem; margin: 0.75rem 0 0.3rem; }
h4 { font-size: 0.95rem; margin: 0.6rem 0 0.25rem; }

p { margin: 0.4rem 0; }
ul, ol { margin: 0.4rem 0 0.55rem; padding-left: 1.25rem; }
li { margin: 0.15rem 0; }
a { color: var(--accent); text-decoration: none; }
p, li { orphans: 2; widows: 2; }

.course-title-mark { string-set: course-title content(); display: none; }
.chapter-title-mark { string-set: chapter-title content(); }

/* Front matter — keep compact */
.frontmatter { page: frontmatter; }
.cover {
  page: :first;
  position: relative;
  min-height: calc(var(--page-h) - var(--m-top) - var(--m-bot));
  overflow: hidden;
  color: #f8fafc;
  margin: calc(-1 * var(--m-top)) calc(-1 * var(--m-out)) 0 calc(-1 * var(--m-in));
  padding: 0;
  break-after: page;
  background: #0b1220;
}
.cover-fullbleed {
  /* Full trim page; negative margins cancel @page margins (recto/first) */
  box-sizing: border-box;
  width: var(--page-w);
  height: var(--page-h);
  margin: calc(-1 * var(--m-top)) calc(-1 * var(--m-out)) calc(-1 * var(--m-bot)) calc(-1 * var(--m-in));
  padding: 0;
  background: #0b1220;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.cover-fullbleed-img {
  /* Show the entire artwork — including author/footer — never crop */
  width: var(--page-w);
  height: var(--page-h);
  object-fit: contain;
  object-position: center center;
  display: block;
}
.cover-art {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}
.cover-overlay {
  position: relative;
  z-index: 1;
  min-height: calc(var(--page-h) - var(--m-top) - var(--m-bot));
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  text-align: center;
  padding: calc(var(--m-top) + 2mm) calc(var(--m-out) + 2mm) calc(var(--m-bot) + 2mm) calc(var(--m-in) + 2mm);
  background: linear-gradient(
    180deg,
    rgba(11, 18, 32, 0.72) 0%,
    rgba(11, 18, 32, 0.28) 42%,
    rgba(11, 18, 32, 0.78) 100%
  );
}
.cover-top {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.45rem;
}
.cover-logo {
  width: 14mm;
  height: 14mm;
  border-radius: 3.5mm;
  display: block;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
}
.cover .brand {
  letter-spacing: 0.22em;
  font-size: 0.78rem;
  font-family: "Source Sans 3", sans-serif;
  text-transform: uppercase;
  opacity: 0.95;
  margin: 0;
}
.cover h1 {
  color: #fff;
  font-size: 2.35rem;
  border: none;
  margin: 0.35rem 0;
  text-shadow: 0 2px 18px rgba(0, 0, 0, 0.35);
}
.cover .subtitle {
  font-size: 1.02rem;
  opacity: 0.95;
  margin: 0.5rem auto 0.9rem;
  max-width: 28rem;
  font-family: "Source Sans 3", sans-serif;
  font-weight: 400;
}
.cover-graphic-chips {
  display: flex;
  justify-content: center;
  gap: 0.45rem;
  flex-wrap: wrap;
  margin: 0.2rem 0 1rem;
  font-family: "Source Sans 3", sans-serif;
}
.cover-graphic-chips span {
  border: 1px solid rgba(94, 234, 212, 0.55);
  background: rgba(15, 118, 110, 0.28);
  color: #ecfeff;
  border-radius: 999px;
  padding: 0.22rem 0.7rem;
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.cover .meta {
  margin-top: auto;
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.9rem;
  opacity: 0.95;
}
.cover-photo {
  width: 30mm;
  height: 30mm;
  object-fit: cover;
  border-radius: 50%;
  border: 2.5px solid #5eead4;
  display: block;
  margin: 0 auto 0.75rem;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
}
.cover-author {
  font-size: 1.05rem;
  font-weight: 600;
  letter-spacing: 0.01em;
}
.cover .rule {
  width: 3.5rem;
  height: 2.5px;
  background: #5eead4;
  margin: 0.7rem auto;
  border: none;
}

.copyright-page {
  break-after: page;
  font-size: 0.88rem;
  color: var(--muted);
  padding-top: 4mm;
}
.copyright-page h1 {
  font-size: 1.1rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.3rem;
  color: var(--ink);
}
.copyright-page p { margin: 0.45rem 0; }

.about-author {
  break-after: page;
  font-size: 0.95rem;
}
.about-author h1 {
  font-size: 1.35rem;
  border-bottom: 2px solid var(--accent);
  padding-bottom: 0.25rem;
  margin-bottom: 0.85rem;
}
.author-card {
  display: flex;
  gap: 1.1rem;
  align-items: flex-start;
  margin: 0.4rem 0 0.9rem;
}
.author-photo {
  width: 32mm;
  height: 32mm;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid var(--accent);
  flex-shrink: 0;
}
.author-meta { flex: 1; min-width: 0; }
.author-name {
  font-family: "Source Serif 4", Georgia, serif;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 0.2rem;
}
.author-role {
  margin: 0 0 0.35rem;
  color: var(--accent);
  font-weight: 600;
  font-family: "Source Sans 3", sans-serif;
}
.author-headline {
  margin: 0 0 0.35rem;
  font-size: 0.86rem;
  color: var(--muted);
  font-family: "Source Sans 3", sans-serif;
  line-height: 1.35;
}
.author-location, .author-links {
  margin: 0.15rem 0;
  font-size: 0.88rem;
  font-family: "Source Sans 3", sans-serif;
}
.about-author p { margin: 0.55rem 0; }

.toc, .lof, .glossary, .index-section { break-before: page; }
.toc h1, .lof h1, .glossary h1, .index-section h1 {
  border-bottom: 2px solid var(--accent);
  padding-bottom: 0.25rem;
  margin-bottom: 0.6rem;
}
.toc-list, .lof-list, .index-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.toc-list li, .lof-list li {
  display: flex;
  align-items: baseline;
  gap: 0.3rem;
  margin: 0.12rem 0;
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.9rem;
}
.toc-list .mod {
  margin-top: 0.55rem;
  font-weight: 700;
  color: var(--accent);
  display: block;
}
.toc-list a, .lof-list a, .index-list a { color: var(--ink); flex: 0 1 auto; }
.toc-list .dots, .lof-list .dots {
  flex: 1 1 auto;
  border-bottom: 1px dotted #94a3b8;
  margin: 0 0.2rem;
  min-width: 0.8rem;
  height: 0.65em;
}
.toc-list .pg::after, .lof-list .pg::after, .index-list .pg::after {
  content: target-counter(attr(href), page);
  font-variant-numeric: tabular-nums;
  color: var(--muted);
}

/* Chapters — one break, no giant empty bands */
.chapter {
  break-before: page;
  padding-top: 0;
}
.chapter > h1.chapter-heading {
  font-size: 1.5rem;
  border-bottom: 2px solid var(--accent);
  padding-bottom: 0.3rem;
  margin: 0 0 0.55rem;
}
.chapter-kicker {
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 0 0 0.2rem;
}

/* Module label: compact strip, NOT a blank page */
.module-divider {
  break-before: avoid;
  margin: 0.4rem 0 0.7rem;
  padding: 0.35rem 0.6rem;
  background: var(--accent-soft);
  border-left: 3px solid var(--accent);
  border-radius: 4px;
  page-break-inside: avoid;
}
.module-divider span {
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

code, pre, .codehilite, .highlight {
  font-family: "IBM Plex Mono", "SFMono-Regular", Menlo, Consolas, monospace;
  font-size: 0.8em;
}
code {
  background: var(--code-bg);
  padding: 0.05em 0.25em;
  border-radius: 3px;
}
pre, .codehilite, .highlight {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 5px;
  padding: 0.5rem 0.65rem;
  overflow-x: auto;
  /* Allow tall listings to split — avoid leaves blank pages */
  break-inside: auto;
  page-break-inside: auto;
  line-height: 1.32;
  margin: 0.5rem 0 0.65rem;
}
.highlight pre, .codehilite pre {
  background: transparent;
  border: none;
  padding: 0;
  margin: 0;
}
.highlight .c, .highlight .ch, .highlight .cm, .highlight .c1 { color: #64748b; font-style: italic; }
.highlight .k, .highlight .kd, .highlight .kn { color: #0f766e; font-weight: 600; }
.highlight .s, .highlight .s1, .highlight .s2, .highlight .sa { color: #b45309; }
.highlight .nf, .highlight .nc { color: #0369a1; }
.highlight .mi, .highlight .mf { color: #7c3aed; }

/* Tables: prefer moving a whole short table to the next page rather than
   leaving a header + one broken row at the bottom (WeasyPrint orphans). */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 0.55rem 0 0.75rem;
  font-size: 0.88em;
  break-inside: avoid;
  page-break-inside: avoid;
}
thead {
  display: table-header-group;
  break-inside: avoid;
  page-break-inside: avoid;
}
tbody {
  break-inside: auto;
  page-break-inside: auto;
}
tr {
  break-inside: avoid;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid var(--border);
  padding: 0.28rem 0.4rem;
  vertical-align: top;
}
th { background: var(--accent-soft); font-family: "Source Sans 3", sans-serif; }

/* Keep "Troubleshooting" (etc.) glued to the table that follows */
h2 + table,
h3 + table,
h4 + table {
  break-before: avoid;
  page-break-before: avoid;
}

img, .figure {
  max-width: 100%;
  height: auto;
}
.figure {
  margin: 0.7rem 0 0.9rem;
  text-align: center;
  break-inside: avoid;
  page-break-inside: avoid;
  padding: 0.35rem 0.2rem 0.45rem;
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: 6px;
}
.figure img {
  max-width: 100%;
  max-height: 130mm;
  width: auto;
  height: auto;
  display: block;
  margin: 0 auto;
}
.figure figcaption {
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.78rem;
  color: var(--muted);
  margin-top: 0.35rem;
  padding: 0 0.4rem;
}

blockquote {
  border-left: 3px solid var(--accent);
  margin: 0.5rem 0;
  padding: 0.1rem 0 0.1rem 0.7rem;
  color: var(--muted);
}

.callout {
  border-radius: 5px;
  border: 1px solid var(--border);
  padding: 0.45rem 0.65rem;
  margin: 0.55rem 0;
  /* Short tip/warning boxes may avoid breaks; long ones must split */
  break-inside: auto;
  page-break-inside: auto;
  font-size: 0.92rem;
}
.callout .callout-title {
  font-family: "Source Sans 3", sans-serif;
  font-weight: 700;
  font-size: 0.78rem;
  letter-spacing: 0.02em;
  /* Keep title casing — uppercase made `code` look like raw backticks */
  text-transform: none;
  margin: 0 0 0.25rem;
  break-after: avoid;
  page-break-after: avoid;
}
.callout .callout-title code {
  font-size: 0.92em;
  font-weight: 650;
  text-transform: none;
}
.callout p:last-child { margin-bottom: 0; }
.callout-tip { background: var(--tip-bg); border-color: #7dd3fc; }
.callout-tip .callout-title { color: var(--tip); }
.callout-note { background: var(--note-bg); border-color: #94a3b8; }
.callout-note .callout-title { color: var(--note); }
.callout-warning { background: var(--warn-bg); border-color: #fcd34d; }
.callout-warning .callout-title { color: var(--warn); }
.callout-danger { background: var(--danger-bg); border-color: #fca5a5; }
.callout-danger .callout-title { color: var(--danger); }

/* Lab / interview: banners + breakable body (fixes empty "Hands-on Lab" pages) */
.lab-banner, .interview-banner {
  font-family: "Source Sans 3", sans-serif;
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin: 0.15rem 0 0.45rem;
  padding: 0.35rem 0.65rem;
  border-radius: 5px;
}
.lab-banner {
  color: var(--try);
  background: var(--try-bg);
  border: 1px solid #86efac;
  border-left: 3px solid var(--try);
}
.interview-banner {
  color: var(--interview);
  background: var(--interview-bg);
  border: 1px solid #c4b5fd;
  border-left: 3px solid var(--interview);
}
.callout-answer {
  background: #f8fafc;
  border-color: #94a3b8;
  border-left: 3px solid var(--accent);
  margin: 0.25rem 0 0.7rem;
}
.callout-answer .callout-title {
  color: var(--accent);
  text-transform: none;
  letter-spacing: 0.02em;
}

.lab-qr {
  display: flex;
  gap: 0.65rem;
  align-items: center;
  border: 1px dashed var(--accent);
  background: #f0fdfa;
  border-radius: 6px;
  padding: 0.4rem 0.55rem;
  margin: 0.35rem 0 0.7rem;
  page-break-inside: avoid;
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.8rem;
}
.lab-qr img { width: 16mm; height: 16mm; }
.lab-qr .lab-qr-text strong {
  color: var(--accent);
  display: block;
  margin-bottom: 0.1rem;
  font-size: 0.78rem;
}
.lab-qr a { word-break: break-all; font-size: 0.72rem; }

.backmatter-lead {
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.88rem;
  color: var(--muted);
  margin: 0 0 0.75rem;
}
.glossary dl {
  display: grid;
  grid-template-columns: 7.5rem 1fr;
  gap: 0.35rem 0.75rem;
  font-size: 0.86rem;
}
.glossary dt {
  font-family: "Source Sans 3", sans-serif;
  font-weight: 700;
  color: var(--accent);
  break-inside: avoid;
  page-break-inside: avoid;
}
.glossary dd {
  margin: 0;
  color: var(--ink);
  break-inside: avoid;
  page-break-inside: avoid;
}
.index-list {
  columns: 2;
  column-gap: 1.4rem;
  font-family: "Source Sans 3", sans-serif;
  font-size: 0.8rem;
  list-style: none;
  padding: 0;
  margin: 0;
}
.index-list li {
  break-inside: avoid;
  margin: 0.06rem 0;
  display: flex;
  gap: 0.2rem;
  align-items: baseline;
}
.index-list .index-letter {
  display: block;
  width: 100%;
  margin: 0.45rem 0 0.15rem;
  font-weight: 800;
  color: var(--accent);
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.1rem;
  break-after: avoid;
}
.index-list .term { flex: 0 1 auto; }
.index-list .dots {
  flex: 1 1 auto;
  border-bottom: 1px dotted #94a3b8;
  height: 0.65em;
  margin: 0 0.15rem;
}

@media screen {
  body { max-width: 50rem; margin: 0 auto; padding: 1rem; }
  .cover {
    margin: 0 0 1.25rem;
    border-radius: 8px;
    min-height: 28rem;
  }
  .cover-fullbleed {
    width: auto;
    height: auto;
    min-height: 36rem;
    margin: 0 0 1.25rem;
    border-radius: 8px;
  }
  .cover-fullbleed-img {
    width: 100%;
    height: auto;
    min-height: 36rem;
    border-radius: 8px;
    object-fit: contain;
  }
  .cover-overlay { min-height: 28rem; padding: 2rem 1.2rem; }
}
'''

def book_css(page_size: str = "a4") -> str:
    """Return full print stylesheet for the given page profile."""
    profile = get_page_profile(page_size)
    kdp = page_size.startswith("kdp")
    body = (
        _BODY_TEMPLATE.replace("__PAGE_W__", profile["width"])
        .replace("__PAGE_H__", profile["height"])
        .replace("__M_TOP__", profile["margin_top"])
        .replace("__M_OUT__", profile["margin_outside"])
        .replace("__M_BOT__", profile["margin_bottom"])
        .replace("__M_IN__", profile["margin_inside"])
    )
    css = _page_chrome(profile, kdp=kdp) + "\n" + body
    if kdp:
        css += "\n" + KDP_LAYOUT_CSS
    return css


# Back-compat default (A4 free download)
BOOK_CSS = book_css("a4")
