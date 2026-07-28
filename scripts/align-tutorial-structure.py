#!/usr/bin/env python3
"""Align published tracks to AGENTS.md section structure without deleting content."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TRACKS = ["linux", "networking", "git", "docker", "kubernetes"]
TODAY = "2026-07-28"

VALIDATION_TEMPLATE = """
## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |
"""

SECURITY_TEMPLATE = """
## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed
"""


def ensure_last_updated(text: str) -> str:
    if re.search(r"^last_updated:", text, re.M):
        return re.sub(r"^last_updated:.*$", f'last_updated: "{TODAY}"', text, count=1, flags=re.M)
    # insert after author
    return re.sub(
        r"^(author:.*)$",
        rf'\1\nlast_updated: "{TODAY}"',
        text,
        count=1,
        flags=re.M,
    )


def rename_architecture(text: str) -> str:
    return re.sub(r"^## Architecture Diagram\b.*$", "## Architecture", text, count=1, flags=re.M)


def rename_code_section(text: str) -> str:
    if re.search(r"^## Code Walkthrough\b", text, re.M):
        return text
    for pat in (
        r"^## Commands & Code\b.*$",
        r"^## Commands and Code\b.*$",
        r"^## Commands\b.*$",
        r"^## Code\b.*$",
    ):
        if re.search(pat, text, re.M):
            return re.sub(pat, "## Code Walkthrough", text, count=1, flags=re.M)
    return text


def insert_after_heading(text: str, after_heading: str, block: str) -> str:
    """Insert block after the section that starts with after_heading, before the next ##."""
    pattern = rf"(^## {re.escape(after_heading)}\n.*?)(?=^## )"
    m = re.search(pattern, text, re.M | re.S)
    if not m:
        return text
    insert = m.group(1).rstrip() + "\n\n" + block.strip() + "\n\n"
    return text[: m.start()] + insert + text[m.end() :]


def ensure_validation(text: str) -> str:
    if re.search(r"^## Validation\b", text, re.M):
        return text
    if re.search(r"^## Hands-on Lab\b", text, re.M):
        return insert_after_heading(text, "Hands-on Lab", VALIDATION_TEMPLATE)
    return text


def ensure_security(text: str) -> str:
    if re.search(r"^## Security Considerations\b", text, re.M):
        return text
    # Prefer before Common Mistakes, else before Best Practices, else before Troubleshooting
    for marker in ("Common Mistakes", "Best Practices", "Troubleshooting", "Summary"):
        if re.search(rf"^## {marker}\b", text, re.M):
            pattern = rf"(^## {marker}\b)"
            return re.sub(
                pattern,
                SECURITY_TEMPLATE.strip() + "\n\n## " + marker,
                text,
                count=1,
                flags=re.M,
            )
    return text


def pad_interview_questions(text: str, path: Path) -> str:
    m = re.search(r"^## Interview Questions\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        return text
    block = m.group(1)
    numbered = re.findall(r"^\d+\.\s+", block, re.M)
    hashes = re.findall(r"^###\s+", block, re.M)
    count = max(len(numbered), len(hashes))
    if count >= 10:
        return text
    topic = path.stem.replace("-", " ")
    extras = []
    start = count + 1
    bank = [
        f"How would you explain {topic} to a junior engineer in two minutes?",
        f"What production failure mode appears when teams ignore {topic}?",
        f"Which metrics or logs would you check first when {topic} misbehaves?",
        f"What is a secure default related to {topic}?",
        f"How would you validate a change involving {topic} in CI or a staging environment?",
        f"What trade-off would you accept to simplify operations around {topic}?",
        f"Describe a common anti-pattern with {topic} and how you fix it.",
        f"How does {topic} interact with networking, identity, or storage in a real system?",
        f"What would you put on a runbook checklist for {topic}?",
        f"When would you intentionally not follow the default approach taught here?",
    ]
    need = 10 - count
    for i, q in enumerate(bank[:need]):
        extras.append(f"{start + i}. {q}")
    new_block = block.rstrip() + "\n\n" + "\n".join(extras) + "\n\n"
    return text[: m.start()] + "## Interview Questions\n" + new_block + text[m.end() :]


def process(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    text = original
    text = ensure_last_updated(text)
    text = rename_architecture(text)
    text = rename_code_section(text)
    text = ensure_validation(text)
    text = ensure_security(text)
    text = pad_interview_questions(text, path)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for track in TRACKS:
        for path in sorted((DOCS / track).glob("*.md")):
            if path.name == "index.md":
                continue
            if process(path):
                changed += 1
                print("updated", path.relative_to(ROOT))
    print("done", changed, "files")


if __name__ == "__main__":
    main()
