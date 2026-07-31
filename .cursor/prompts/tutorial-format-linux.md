# Tutorial content format (Linux de facto)

**Canonical reference:** `docs/linux/*.md` and `docs/shell/*.md`.

Every technology tutorial under `docs/<technology>/` MUST follow this body structure.
Do **not** use the shorter Helm-style skeleton (`## Goal`, `{ .ra-facts }`, `## Environment setup`, stop after `## Next`).

---

## Required section order

```markdown
# <Title>

## Overview
## Prerequisites
## Learning Objectives
## Architecture
## Theory
## Hands-on Lab
## Validation
## Code Walkthrough
## Security Considerations
## Common Mistakes
## Best Practices
## Troubleshooting
## Summary
## Interview Questions
## Related Tutorials
## References
```

---

## Section rules

### Overview

- 2–4 short paragraphs: why the topic matters in Cloud/DevOps.
- Include: `This is **Tutorial N** in **Module M: …** of the REBASH Academy **<Course Name>** series — written for …`
- No separate `## Goal` section (fold the outcome into Overview).
- No `{ .ra-facts }` line under the H1.

### Prerequisites

- Bullet list (plain language and/or links).

### Learning Objectives

- Intro line: `By the end of this tutorial, you will be able to:`
- 4–6 checkbox objectives (`- [ ] …`).

### Architecture

- One short intro sentence.
- One Excalidraw diagram only: `![…](../assets/excalidraw/<name>.svg)`
- Never D2/Mermaid/`assets/images/`.

### Theory

Preferred subsections (adapt names to the topic, keep depth):

1. `### What it is`
2. `### Why it matters` (Cloud / DevOps / SRE context)
3. `### How it works`
4. Topic-specific concept headings **or** `### Key concepts and comparisons` (tables OK)
5. `### Common pitfalls`

Cover **every** concept from the technology prompt module. British English. Production focus.

### Hands-on Lab

- Title casing: `## Hands-on Lab` (not “lab”).
- Workspace: `~/rebash-<technology>/labNN` (zero-padded) **or** `module-NN` consistently within a course — prefer `labNN` to match Linux/Shell.
- Line: `**Focus:** …` (what the learner will practise)
- **2–3 real steps** with **topic-relevant** titles: `### Step 1 – …`, `### Step 2 – …`, `### Final step – Cleanup note`
- Each step needs runnable commands tied to Theory and an **observable success** (file created, pod Ready, plan shows change, curl 200, pipeline YAML validates).
- Cleanup must remove disposable resources (containers, namespaces, Terraform state) — not re-run a no-op script.
- Safe defaults: local/`null`/kind where possible; AWS read-only / sandbox warnings; no committed secrets.
- **Never** use a placeholder “Skeleton” step that only echoes the tutorial name — every step must teach the module skill.
- Use `set -euo pipefail` in shell labs where appropriate.
- Escape `${{` / `{#` for mkdocs-macros (`{% raw %}`).
- Quality bar examples: `docs/linux/ssh-and-remote-access.md`. Enrich priority tracks with `python3 scripts/enrich-labs-and-interviews.py --course <technology>`.

### Validation

Checkbox list (not a one-line paragraph):

- Lab path ran successfully
- Can explain Theory in own words
- Used modern tooling where applicable
- Can describe one production failure mode

### Code Walkthrough

5 short production habits for this topic (inspect → change → evidence → modern tools → least privilege).

### Security Considerations

5 bullets specific to the topic.

### Common Mistakes

2–4 `!!! warning` admonitions with **Fix:** guidance.

### Best Practices

5 bullets.

### Troubleshooting

Markdown table: Symptom | Likely cause | Fix

### Summary

2–3 sentences; point to next tutorial.

### Interview Questions

- **5 topic-specific questions** (concepts, debugging, security, trade-offs, production) — not the generic “How does X show up…” boilerplate.
- **1–2 sample answers** in `!!! tip "Sample answer — question N"` blocks tied to this module.
- British English; expand acronyms on first use in answers when needed.
- Prefer banks from `scripts/enrich-labs-and-interviews.py` over aligner stubs.

### Related Tutorials

- Course index
- Next tutorial
- Optional prior / related path

### References

Official docs + course index link.

---

## Frontmatter

Minimum (Linux/Shell style):

```yaml
---
title: "…"
description: "…"
difficulty: beginner|intermediate|advanced|expert
estimated_time: "45 min"
author: Shaik Basha
last_updated: "YYYY-MM-DD"
category: <technology>
tags: […]
prerequisites: […]
comments: false
---
```

Optional curriculum fields (`technology`, `module`, `career_paths`, `skills`, `next`, `related`, `interview`, `certifications`) may remain for site tooling, but **body structure above is mandatory**.

---

## Anti-patterns (do not use)

- `## Goal` as a top-level section
- `{ .ra-facts }` under the title
- Stopping after `## Next` / short Validation paragraph only
- Missing Architecture / Code Walkthrough / Security / Common Mistakes / Best Practices / Troubleshooting / Summary / Interview / Related
- D2 or Mermaid diagrams

---

## Diagrams

```bash
python3 scripts/generate-excalidraw-svg.py
```

Excalidraw SVGs live under `docs/assets/excalidraw/`.
