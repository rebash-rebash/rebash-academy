# Contributing to REBASH Academy

Thank you for contributing to REBASH Academy! This guide covers how to set up your environment,
add tutorials, and submit changes.

## Getting Started

### Prerequisites

- Python 3.12 or later
- Git

### Local Setup

```bash
git clone https://github.com/rebash-rebash/rebash-academy.git
cd rebash-academy

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to preview the site.

### Course books (EPUB / PDF)

Professional books include cover, copyright, TOC, list of figures, syntax highlighting,
headers/footers/page numbers, glossary, index, QR codes to live labs, and styled callouts.

```bash
pip install -r requirements-books.txt
# macOS: brew install pango gdk-pixbuf libffi glib
python3 scripts/build_course_book.py --list-courses
python3 scripts/build_course_book.py linux
python3 scripts/build_course_book.py python --format epub
```

Outputs land in `books/<course>/`. See [books/README.md](books/README.md).

## Adding a Tutorial

Use the tutorial generator to scaffold a new page with the standard structure:

```bash
python3 scripts/create-tutorial.py docker "Build a Multi-Stage Dockerfile" \
  --description "Create optimized production Docker images." \
  --difficulty intermediate \
  --time "45 min"
```

Then add the new page to the category's `.pages` file (the create script does this automatically for Linux and other categories with `.pages`).

Navigation is managed via `.pages` files — not `mkdocs.yml`:

| File | Purpose |
|------|---------|
| `docs/.pages` | Top-level nav (Home, Tutorials, About, …) |
| `docs/linux/.pages` | Linux section title, icon, and tutorial order |
| `docs/<category>/.pages` | Per-category sidebar entries |

Sidebar sections are **collapsible**: click the section label or arrow to expand/collapse topics (e.g. Linux → 20 tutorials).

### Tutorial Structure

Every tutorial must include:

1. Overview
2. Prerequisites
3. Learning Objectives
4. Architecture Diagram (D2)
5. Theory
6. Hands-on Lab
7. Commands & Code
8. Common Mistakes
9. Best Practices
10. Troubleshooting
11. Summary
12. Interview Questions
13. Related Tutorials
14. References

### Required Metadata

Each page needs YAML front matter:

```yaml
---
title: Tutorial Title
description: Short description for SEO
difficulty: beginner | intermediate | advanced
estimated_time: "30 min"
author: Your Name
category: docker
tags:
  - docker
  - containers
prerequisites:
  - Basic Linux knowledge
comments: false
---
```

## Validation

Before submitting a pull request, run:

```bash
bash scripts/build.sh      # Build with strict mode
bash scripts/lint.sh       # Lint YAML and Markdown
bash scripts/validate.sh   # Check metadata and links
```

## Pull Request Process

1. Fork the repository and create a feature branch
2. Make your changes following the documentation standards
3. Run validation scripts locally
4. Submit a pull request with a clear description
5. Ensure CI checks pass

## Code of Conduct

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Git hooks (required for contributors)

This repo blocks all `Co-authored-by:` trailers. After cloning, run:

```bash
bash scripts/install-git-hooks.sh
```

Also disable **Cursor → Settings → Agents → Attribution** so the IDE stops injecting co-authors.

To clean existing history:

```bash
bash scripts/strip-coauthor-trailers.sh
git push --force-with-lease origin main
```

## Questions?

Open a [GitHub Issue](https://github.com/rebash-rebash/rebash-academy/issues) or start a discussion.
