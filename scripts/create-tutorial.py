#!/usr/bin/env python3
"""Scaffold a new tutorial with standard structure and metadata."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"

VALID_CATEGORIES = [
    "getting-started", "linux", "networking", "git", "docker", "kubernetes",
    "terraform", "aws", "azure", "gcp", "gitlab", "python", "monitoring",
    "security", "devsecops", "ai", "architecture", "interview", "cheatsheets",
    "labs", "projects", "blog",
]

TEMPLATE = dedent("""\
    ---
    title: {title}
    description: {description}
    difficulty: {difficulty}
    estimated_time: "{estimated_time}"
    author: {author}
    category: {category}
    tags:
      - {category}
      - {tag}
    prerequisites:
      - TBD
    comments: false
    ---

    # {title}

    ## Overview

    {description}

    ## Prerequisites

    - Item 1
    - Item 2

    ## Learning Objectives

    By the end of this tutorial, you will be able to:

    - [ ] Objective 1
    - [ ] Objective 2
    - [ ] Objective 3

    ## Architecture Diagram

    ```mermaid
    flowchart LR
        A[Component A] --> B[Component B]
        B --> C[Component C]
    ```

    ## Theory

    Explain the core concepts here.

    ## Hands-on Lab

    ### Step 1 – Setup

    Describe the first step.

    ```bash
    # Example command
    echo "Hello REBASH Academy"
    ```

    ### Step 2 – Implementation

    Describe the second step.

    ## Commands

    | Command | Description |
    |---------|-------------|
    | `command` | What it does |

    ## Code

    ```python
    # Example Python code
    def main():
        print("REBASH Academy")

    if __name__ == "__main__":
        main()
    ```

    ## Common Mistakes

    !!! warning "Common Mistake"
        Describe a common mistake and how to avoid it.

    ## Best Practices

    !!! tip "Best Practice"
        Describe a production-ready recommendation.

    ## Troubleshooting

    | Issue | Cause | Solution |
    |-------|-------|----------|
    | Problem | Root cause | Fix |

    ## Summary

    - Key takeaway 1
    - Key takeaway 2

    ## Interview Questions

    1. Question one?
    2. Question two?

    ## Related Tutorials

    - [Related Tutorial](../getting-started/index.md)

    ## References

    - [Official Documentation](https://example.com)
    """)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new REBASH Academy tutorial")
    parser.add_argument("category", choices=VALID_CATEGORIES, help="Documentation category")
    parser.add_argument("title", help="Tutorial title")
    parser.add_argument("--description", default="", help="Short description")
    parser.add_argument("--difficulty", default="beginner", choices=["beginner", "intermediate", "advanced"])
    parser.add_argument("--time", default="30 min", dest="estimated_time", help="Estimated completion time")
    parser.add_argument("--author", default="Shaik Basha", help="Author name")
    args = parser.parse_args()

    description = args.description or f"Learn {args.title} with hands-on examples."
    slug = slugify(args.title)
    tag = slug.replace("-", " ")

    category_dir = DOCS_DIR / args.category
    if not category_dir.exists():
        print(f"Error: category directory '{args.category}' does not exist")
        return 1

    tutorial_path = category_dir / f"{slug}.md"
    if tutorial_path.exists():
        print(f"Error: {tutorial_path} already exists")
        return 1

    content = TEMPLATE.format(
        title=args.title,
        description=description,
        difficulty=args.difficulty,
        estimated_time=args.estimated_time,
        author=args.author,
        category=args.category,
        tag=tag,
    )

    tutorial_path.write_text(content, encoding="utf-8")
    print(f"Created: {tutorial_path.relative_to(ROOT)}")
    print(f"Add to navigation in mkdocs.yml under Tutorials > {args.category}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
