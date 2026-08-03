# Course books (EPUB & PDF)

Professional books generated from `docs/<course>/.pages`.

## Features (always included)

| Feature | PDF | EPUB / HTML |
|---------|-----|-------------|
| Automatic cover page (with author photo) | ✓ | ✓ |
| Copyright page | ✓ | ✓ |
| About the author (LinkedIn-sourced bio + photo) | ✓ | ✓ |
| Table of contents (with page numbers in PDF) | ✓ | ✓ |
| List of figures | ✓ | ✓ |
| Syntax-highlighted code (Pygments) | ✓ | ✓ |
| Headers & footers | ✓ | screen CSS |
| Page numbers | ✓ (arabic; roman front matter) | n/a |
| Chapter numbering | ✓ | ✓ |
| Glossary | ✓ | ✓ |
| Index | ✓ (page refs in PDF) | ✓ |
| QR codes → live labs on rebash.in | ✓ | ✓ |
| “Try it yourself” lab/challenge boxes | ✓ | ✓ |
| Tips, notes, warnings, interview styling | ✓ | ✓ |

## Setup

```bash
source .venv/bin/activate
pip install -r requirements-books.txt

# macOS (WeasyPrint system libs)
brew install pango gdk-pixbuf libffi glib
```

## Build

```bash
python3 scripts/build_course_book.py --list-courses
python3 scripts/build_course_book.py linux
python3 scripts/build_course_book.py python --format epub
python3 scripts/build_course_book.py networking --author "Shaik Khadar Basha"

# Amazon KDP paperback (6" × 9" trim) — two PDFs
python3 scripts/build_course_book.py linux --kdp
```

Default author is **Shaik Khadar Basha**. Photo: `docs/assets/images/authors/shaik-khadar-basha.jpg`. Bio: `scripts/books/author.py`.

Designed covers (optional): put a full-bleed PNG at `docs/assets/images/covers/<course>.png` (e.g. `linux.png`). When present, it replaces the generated HTML/SVG cover.

### Amazon KDP (`--kdp`)

Follows [KDP paperback formatting](https://kdp.amazon.com/en_US/help/topic/GKX2T59EVGFSMKQK):

- **Trim:** 6″ × 9″ (15.24 × 22.86 cm), **no interior bleed** ([trim, bleed, margins](https://kdp.amazon.com/help/topic/GVBQ3CMEQW3W2VL6))
- **Margins:** 0.65″ outside; 0.7″ top/bottom; **0.75″ inside gutter** (above the 0.5″ minimum for 151–300 pages); mirrored on every named page
- **Print-safe PDF:** code wraps; link annotations stripped (avoids KDP “non-printable markup” / object-outside-margin flags)
- **Front matter:** half-title → title → copyright (verso) → contents ([front/body/back matter](https://kdp.amazon.com/en_US/help/topic/GDDYZG2C7RVF5N9J))
- **Body:** chapter 1 on a right-facing page; justified text; running heads (author / title)
- **Back matter:** about the author → glossary → index (each major section starts right-facing)
- **Even page count:** blank page appended when needed

| File | Use in KDP |
|------|------------|
| `<course>-kdp-6x9-interior.pdf` | **Manuscript** upload (no cover page) |
| `<course>-kdp-6x9.pdf` | Preview / complete book (includes cover page) — **not** the KDP wrap cover |

Upload the wraparound cover separately in KDP Cover Creator (or a full cover PDF). The interior manuscript must not include the front cover image.

## Output

`books/<course>/`

- `book.html` — canonical professional layout (A4 by default)
- `book.md` — assembled Markdown
- `<course>.epub` / `<course>.pdf` — A4 free download
- `<course>-kdp-6x9.pdf` / `<course>-kdp-6x9-interior.pdf` — when built with `--kdp`
- `assets/` — diagrams + per-chapter QR PNGs

Optional: add `docs/<course>/glossary.md` with `- **Term** — definition` lines to seed the glossary.

## Site downloads (free registration)

The live site page is [docs/books/index.md](../docs/books/index.md) (`/books/`).

1. Build the courses you want to offer.
2. Sync artefacts into the MkDocs site tree:

```bash
python3 scripts/sync_books_to_site.py
```

3. Configure lead capture in `mkdocs.yml` under `extra.books` — set **one** of:
   - `formspree_form_id` from [Formspree](https://formspree.io)
   - `web3forms_access_key` from [Web3Forms](https://web3forms.com)

Until one of those is set, the registration form cannot unlock downloads (by design).
