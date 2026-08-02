"""Print/EPUB stylesheet for professional course books (compact layout)."""

BOOK_CSS = r"""
/* ===== Page chrome (WeasyPrint / print) ===== */
@page {
  size: A4;
  margin: 14mm 12mm 16mm 12mm;

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
}

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

:root {
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
  min-height: 260mm;
  overflow: hidden;
  color: #f8fafc;
  margin: -14mm -12mm 0;
  padding: 0;
  break-after: page;
  background: #0b1220;
}
.cover-fullbleed {
  /* Full A4 page; negative margins cancel @page margins */
  box-sizing: border-box;
  width: 210mm;
  height: 297mm;
  margin: -14mm -12mm -16mm -12mm;
  padding: 0;
  background: #0b1220;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.cover-fullbleed-img {
  /* Show the entire artwork — including author/footer — never crop */
  width: 210mm;
  height: 297mm;
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
  min-height: 260mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  text-align: center;
  padding: 16mm 14mm 18mm;
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
"""
