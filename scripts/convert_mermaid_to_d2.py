#!/usr/bin/env python3
"""Convert ```mermaid fences in docs/ to ```d2 (flowchart, sequence, state)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MERMAID_FENCE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
D2_FENCE = re.compile(r"```d2\s*\n(.*?)```", re.DOTALL)

DIR_MAP = {
    "TB": "down",
    "TD": "down",
    "BT": "up",
    "LR": "right",
    "RL": "left",
}

STYLE_FILL = re.compile(
    r"^\s*style\s+([A-Za-z0-9_]+)\s+.*?\bfill:\s*(#[0-9A-Fa-f]{3,8})",
    re.IGNORECASE,
)
STYLE_STROKE = re.compile(
    r"^\s*style\s+([A-Za-z0-9_]+)\s+.*?\bstroke:\s*(#[0-9A-Fa-f]{3,8})",
    re.IGNORECASE,
)

# Node id + optional shape on the same token. Also [*] for state diagrams.
ENDPOINT = re.compile(
    r"(?:\[\*\])|"
    r"(?:"
    r"([A-Za-z][A-Za-z0-9_]*)"
    r"(?:"
    r"\[\[([^\]]*)\]\]|"
    r"\[\(([^)]*)\)\]|"
    r"\[([^\]]*)\]|"
    r"\{\{([^}]*)\}\}|"
    r"\{([^}]*)\}|"
    r"\(\(([^)]*)\)\)|"
    r"\(([^)]*)\)|"
    r">([^]]*)\]|"
    r"\[/([^/]*)/\]|"
    r"\[\\([^\\]*)\\\]"
    r")?"
    r")"
)

ARROW = re.compile(r"(<-->|-->|-\.->|---|==>|->>|-->>|->)")

SUBGRAPH_START = re.compile(
    r"^(\s*)subgraph\s+([A-Za-z][A-Za-z0-9_]*)(?:\[([^\]]*)\]|\s+(.+))?\s*$"
)
SUBGRAPH_END = re.compile(r"^(\s*)end\s*$")

PARTICIPANT = re.compile(
    r"^\s*participant\s+([A-Za-z][A-Za-z0-9_]*)(?:\s+as\s+(.+))?\s*$"
)
SEQ_MSG = re.compile(
    r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*(-->>|->>|->)\s*([A-Za-z][A-Za-z0-9_]*)\s*:\s*(.+)\s*$"
)

STATE_TRANS = re.compile(
    r"^\s*(\[\*\]|[A-Za-z][A-Za-z0-9_]*)\s*-->\s*(\[\*\]|[A-Za-z][A-Za-z0-9_]*)"
    r"(?:\s*:\s*(.+))?\s*$"
)


def _label(text: str | None) -> str:
    if text is None:
        return ""
    text = text.strip().strip('"').strip("'")
    text = text.replace("<br/>", "\\n").replace("<br>", "\\n").replace("<br />", "\\n")
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return text


def _quote(text: str) -> str:
    if not text:
        return '""'
    if re.search(r'[:#{"\'\\/\n]', text) or " " in text or text[0].isdigit():
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


def _shape_from_groups(groups: tuple) -> tuple[str | None, str | None]:
    """groups after id: stadium, cyl, box, hex, rhombus, circle, round, asym, para, trap."""
    stadium, cyl, box, hexagon, rhombus, circle, round_, asym, para, trap = groups
    if stadium is not None:
        return _label(stadium), "oval"
    if cyl is not None:
        return _label(cyl), "cylinder"
    if box is not None:
        return _label(box), None
    if hexagon is not None:
        return _label(hexagon), "hexagon"
    if rhombus is not None:
        return _label(rhombus), "diamond"
    if circle is not None:
        return _label(circle), "circle"
    if round_ is not None:
        return _label(round_), "oval"
    if asym is not None:
        return _label(asym), None
    if para is not None:
        return _label(para), "parallelogram"
    if trap is not None:
        return _label(trap), "parallelogram"
    return None, None


def _emit_node_lines(
    body: list[str],
    indent: str,
    nid: str,
    label: str | None,
    shape: str | None,
    defined: set[str],
) -> None:
    if nid in defined or nid == "[*]":
        return
    defined.add(nid)
    text = label if label is not None else nid
    if shape:
        body.append(f"{indent}{nid}: {_quote(text)} {{")
        body.append(f"{indent}  shape: {shape}")
        body.append(f"{indent}}}")
    else:
        body.append(f"{indent}{nid}: {_quote(text)}")


def _parse_endpoint(token: str) -> tuple[str, str | None, str | None]:
    token = token.strip()
    if token == "[*]":
        return "start_end", "start/end", "circle"
    m = ENDPOINT.fullmatch(token)
    if not m or m.group(1) is None:
        return token, None, None
    nid = m.group(1)
    label, shape = _shape_from_groups(m.groups()[1:])
    return nid, label, shape


def _split_edge_chain(line: str) -> list[tuple[str, str, str | None, str]] | None:
    """Parse chained edges into hops of (left, arrow, label, right)."""
    s = line.strip()
    if not ARROW.search(s):
        return None

    hops: list[tuple[str, str, str | None, str]] = []
    pos = 0
    while True:
        em = ENDPOINT.match(s, pos)
        if not em:
            return None
        left = em.group(0)
        pos = em.end()
        while pos < len(s) and s[pos].isspace():
            pos += 1
        if pos >= len(s):
            break
        am = ARROW.match(s, pos)
        if not am:
            return None if not hops else hops
        arrow = am.group(1)
        pos = am.end()
        while pos < len(s) and s[pos].isspace():
            pos += 1
        label = None
        if pos < len(s) and s[pos] == "|":
            end = s.find("|", pos + 1)
            if end < 0:
                return None
            label = s[pos + 1 : end]
            pos = end + 1
            while pos < len(s) and s[pos].isspace():
                pos += 1
        em2 = ENDPOINT.match(s, pos)
        if not em2:
            return None
        right = em2.group(0)
        hops.append((left, arrow, label, right))
        # Continue chain from the right endpoint if another arrow follows.
        nxt = em2.end()
        while nxt < len(s) and s[nxt].isspace():
            nxt += 1
        if nxt < len(s) and ARROW.match(s, nxt):
            pos = em2.start()
            continue
        break
    return hops or None


def convert_flowchart(src: str) -> str:
    lines = src.strip().splitlines()
    if not lines:
        return ""

    direction = "down"
    first = lines[0].strip()
    m = re.match(r"^(?:flowchart|graph)\s+(TB|TD|BT|LR|RL)\b", first, re.I)
    if m:
        direction = DIR_MAP[m.group(1).upper()]
        lines = lines[1:]
    elif re.match(r"^(?:flowchart|graph)\b", first, re.I):
        lines = lines[1:]

    fills: dict[str, str] = {}
    strokes: dict[str, str] = {}
    body: list[str] = []
    stack: list[str] = []
    node_owner: dict[str, str | None] = {}
    defined: set[str] = set()

    def owner_path(node: str) -> str:
        own = node_owner.get(node)
        return f"{own}.{node}" if own else node

    def register(nid: str) -> None:
        if nid == "start_end":
            return
        if stack:
            node_owner.setdefault(nid, ".".join(stack))
        else:
            node_owner.setdefault(nid, None)

    def ensure_node(indent: str, token: str) -> str:
        nid, label, shape = _parse_endpoint(token)
        register(nid)
        _emit_node_lines(body, indent, nid, label, shape, defined)
        if stack:
            return nid
        return owner_path(nid)

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        i += 1

        if not stripped or stripped.startswith("%%"):
            continue

        fm = STYLE_FILL.match(stripped)
        sm = STYLE_STROKE.match(stripped)
        if fm or sm or stripped.startswith("style "):
            if fm:
                fills[fm.group(1)] = fm.group(2)
            if sm:
                strokes[sm.group(1)] = sm.group(2)
            continue
        if stripped.startswith(("classDef", "class ", "linkStyle", "click ")):
            continue

        sg = SUBGRAPH_START.match(line)
        if sg:
            indent, sid, bracket_label, space_label = sg.groups()
            label = _label(bracket_label if bracket_label is not None else space_label) or sid
            stack.append(sid)
            body.append(f"{indent}{sid}: {_quote(label)} {{")
            continue

        if SUBGRAPH_END.match(line) and stack:
            indent = re.match(r"^(\s*)", line).group(1)
            stack.pop()
            body.append(f"{indent}}}")
            continue

        indent = re.match(r"^(\s*)", line).group(1)

        # Standalone node definition (no arrows)
        if not ARROW.search(stripped):
            em = ENDPOINT.fullmatch(stripped)
            if em:
                ensure_node(indent, stripped)
                continue
            body.append(f"# UNPARSED: {stripped}")
            continue

        hops = _split_edge_chain(stripped)
        if not hops:
            body.append(f"# UNPARSED: {stripped}")
            continue

        for left_tok, arrow, elabel, right_tok in hops:
            # Define nodes at current indent level (inside container if any)
            left_id, left_label, left_shape = _parse_endpoint(left_tok)
            right_id, right_label, right_shape = _parse_endpoint(right_tok)
            register(left_id)
            register(right_id)
            _emit_node_lines(body, indent, left_id, left_label, left_shape, defined)
            _emit_node_lines(body, indent, right_id, right_label, right_shape, defined)

            if stack:
                left, right = left_id, right_id
            else:
                left, right = owner_path(left_id), owner_path(right_id)

            if arrow in ("<-->",):
                conn = f"{left} <-> {right}"
            elif arrow in ("-.->",):
                conn = f"{left} -> {right}"
                # D2 stroke dash via connection attribute
                if elabel:
                    body.append(f"{indent}{conn}: {_quote(_label(elabel))} {{")
                    body.append(f"{indent}  style.stroke-dash: 3")
                    body.append(f"{indent}}}")
                else:
                    body.append(f"{indent}{conn}: {{")
                    body.append(f"{indent}  style.stroke-dash: 3")
                    body.append(f"{indent}}}")
                continue
            else:
                conn = f"{left} -> {right}"

            if elabel:
                conn += f": {_quote(_label(elabel))}"
            body.append(f"{indent}{conn}")

    text = "\n".join(body)

    def inject_style(cid: str, block: str) -> str:
        fill = fills.get(cid)
        stroke = strokes.get(cid)
        if not fill and not stroke:
            return block
        style_lines = ["  style: {"]
        if fill:
            style_lines.append(f'    fill: "{fill}"')
        if stroke:
            style_lines.append(f'    stroke: "{stroke}"')
        style_lines.append("  }")
        pattern = re.compile(rf"^(\s*{re.escape(cid)}: .*\{{\n)", re.MULTILINE)

        def add_style(m: re.Match[str]) -> str:
            base_indent = re.match(r"^(\s*)", m.group(1)).group(1)
            styled = "\n".join(
                f"{base_indent}{line}" if line else line for line in style_lines
            )
            return m.group(1) + styled + "\n"

        return pattern.sub(add_style, block, count=1)

    for cid in fills.keys() | strokes.keys():
        text = inject_style(cid, text)

    return f"direction: {direction}\n\n{text.strip()}\n"


def convert_sequence(src: str) -> str:
    lines = src.strip().splitlines()
    if lines and lines[0].strip().lower().startswith("sequencediagram"):
        lines = lines[1:]

    out = ["shape: sequence_diagram", ""]
    seen: set[str] = set()

    for raw in lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("%%"):
            continue
        low = stripped.lower()
        if low.startswith(("alt ", "opt ", "loop ", "par ", "critical ", "break ")):
            out.append(f"# {stripped}")
            continue
        if low == "else" or low.startswith("else "):
            out.append(f"# {stripped}")
            continue
        if low == "end":
            continue
        if low.startswith("note "):
            out.append(f"# {stripped}")
            continue

        pm = PARTICIPANT.match(stripped)
        if pm:
            pid, alias = pm.groups()
            label = _label(alias) if alias else pid
            if pid not in seen:
                out.append(f"{pid}: {_quote(label)}")
                seen.add(pid)
            continue

        sm = SEQ_MSG.match(stripped)
        if sm:
            a, _arrow, b, msg = sm.groups()
            for pid in (a, b):
                if pid not in seen:
                    out.append(f"{pid}: {pid}")
                    seen.add(pid)
            out.append(f"{a} -> {b}: {_quote(_label(msg))}")
            continue

        out.append(f"# UNPARSED: {stripped}")

    return "\n".join(out).rstrip() + "\n"


def convert_state(src: str) -> str:
    lines = src.strip().splitlines()
    if lines and lines[0].strip().lower().startswith("statediagram"):
        lines = lines[1:]

    out = ["direction: right", ""]
    defined: set[str] = set()

    for raw in lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("%%"):
            continue
        if stripped.startswith(("state ", "[", "]")) and "-->" not in stripped:
            # nested state blocks — flatten comments
            if stripped in ("[*]",) or stripped.startswith("state "):
                out.append(f"# {stripped}")
            continue

        tm = STATE_TRANS.match(stripped)
        if not tm:
            out.append(f"# UNPARSED: {stripped}")
            continue
        a, b, label = tm.groups()
        left = "start" if a == "[*]" else a
        right = "end" if b == "[*]" else b
        for nid, lab in ((left, left), (right, right)):
            if nid not in defined:
                if nid == "start":
                    out.append('start: "" {')
                    out.append("  shape: circle")
                    out.append("}")
                elif nid == "end":
                    out.append('end: "" {')
                    out.append("  shape: circle")
                    out.append("}")
                else:
                    out.append(f"{nid}: {_quote(nid)}")
                defined.add(nid)
        if label:
            out.append(f"{left} -> {right}: {_quote(_label(label))}")
        else:
            out.append(f"{left} -> {right}")

    return "\n".join(out).rstrip() + "\n"


def convert(src: str) -> str:
    head = src.strip().splitlines()[0].strip().lower() if src.strip() else ""
    if head.startswith("sequencediagram"):
        return convert_sequence(src)
    if head.startswith("statediagram"):
        return convert_state(src)
    return convert_flowchart(src)


def replace_mermaid_in_text(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return f"```d2\n{convert(m.group(1))}```"

    return MERMAID_FENCE.sub(repl, text), count


def reconvert_from_git(path: Path) -> int:
    """Replace working-tree D2 fences using Mermaid sources from HEAD."""
    rel = path.relative_to(ROOT)
    result = subprocess.run(
        ["git", "show", f"HEAD:{rel.as_posix()}"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        check=False,
    )
    if result.returncode != 0:
        return 0
    head_text = result.stdout
    mermaids = MERMAID_FENCE.findall(head_text)
    if not mermaids:
        return 0

    work = path.read_text(encoding="utf-8")
    d2_blocks = list(D2_FENCE.finditer(work))
    # Prefer 1:1 replacement by order when counts match; else rewrite whole file from HEAD.
    if len(d2_blocks) == len(mermaids):
        out: list[str] = []
        last = 0
        for match, src in zip(d2_blocks, mermaids):
            out.append(work[last : match.start()])
            out.append(f"```d2\n{convert(src)}```")
            last = match.end()
        out.append(work[last:])
        path.write_text("".join(out), encoding="utf-8")
        return len(mermaids)

    converted, count = replace_mermaid_in_text(head_text)
    path.write_text(converted, encoding="utf-8")
    return count


def replace_in_file(path: Path, dry_run: bool = False) -> int:
    text = path.read_text(encoding="utf-8")
    new_text, count = replace_mermaid_in_text(text)
    if count and not dry_run and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--from-git",
        action="store_true",
        help="Reconvert using Mermaid fences from HEAD (fixes broken D2)",
    )
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()

    paths = [p.resolve() for p in args.paths] if args.paths else sorted(DOCS.rglob("*.md"))
    total = 0
    for path in paths:
        if not path.is_file():
            continue
        if args.from_git:
            n = reconvert_from_git(path)
        else:
            n = replace_in_file(path, dry_run=args.dry_run)
        if n:
            try:
                rel = path.relative_to(ROOT)
            except ValueError:
                rel = path
            print(f"{rel}: {n} diagram(s)")
            total += n
    print(f"Converted {total} diagram(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
