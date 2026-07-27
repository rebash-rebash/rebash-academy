#!/usr/bin/env python3
"""Validate YAML files, including MkDocs-specific tags like !ENV."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml


class MkDocsYamlLoader(yaml.SafeLoader):
    """Accept MkDocs/Material YAML tags used in mkdocs.yml."""


def _construct_mkdocs_tag(loader: MkDocsYamlLoader, node: yaml.Node) -> str:
    if isinstance(node, yaml.ScalarNode):
        return str(loader.construct_scalar(node))
    return str(loader.construct_sequence(node))


MkDocsYamlLoader.add_constructor("!ENV", _construct_mkdocs_tag)
MkDocsYamlLoader.add_constructor(
    tag="tag:yaml.org,2002:python/name:material.extensions.emoji.to_svg",
    constructor=_construct_mkdocs_tag,
)
MkDocsYamlLoader.add_constructor(
    tag="tag:yaml.org,2002:python/name:material.extensions.emoji.twemoji",
    constructor=_construct_mkdocs_tag,
)
MkDocsYamlLoader.add_constructor(
    tag="tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format",
    constructor=_construct_mkdocs_tag,
)


def validate(path: Path) -> None:
    yaml.load(path.read_text(), Loader=MkDocsYamlLoader)
    print(f"  OK: {path}")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    paths = [root / "mkdocs.yml", *sorted((root / ".github/workflows").glob("*.yml"))]
    errors = 0
    for path in paths:
        if not path.exists():
            continue
        try:
            validate(path)
        except yaml.YAMLError as exc:
            print(f"  FAIL: {path}: {exc}", file=sys.stderr)
            errors += 1
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
