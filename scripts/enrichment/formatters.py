"""Shared markdown formatters for lab and interview bodies."""

from __future__ import annotations


def lab_body(lab_dir: str, focus: str, steps: list[tuple[str, str]], cleanup: str) -> str:
    parts = [
        "Create a workspace for this tutorial.",
        "",
        "```bash",
        f"mkdir -p {lab_dir} && cd {lab_dir}",
        "```",
        "",
        f"**Focus:** {focus}",
        "",
    ]
    for i, (name, body) in enumerate(steps, start=1):
        parts.append(f"### Step {i} – {name}")
        parts.append("")
        parts.append(body.strip())
        parts.append("")
    parts.append("### Final step – Cleanup note")
    parts.append("")
    parts.append("```bash")
    parts.append(cleanup.strip())
    parts.append("```")
    return "\n".join(parts).rstrip() + "\n"


def bash(cmds: str) -> str:
    return f"```bash\n{cmds.strip()}\n```"


def yaml_block(content: str) -> str:
    return f"```yaml\n{content.strip()}\n```"


def interview_body(questions: list[str], tips: dict[int, str]) -> str:
    lines = [f"{i}. {q}" for i, q in enumerate(questions, start=1)]
    lines.append("")
    for num, text in sorted(tips.items()):
        lines.append(f'!!! tip "Sample answer — question {num}"')
        for para in text.strip().split("\n"):
            lines.append(f"    {para}" if para.strip() else "")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
