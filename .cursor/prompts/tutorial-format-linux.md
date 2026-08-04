# Canonical tutorial format (all technologies)

**This is the de facto body structure for every tutorial under `docs/<technology>/`.**

Canonical examples: `docs/linux/*.md`, `docs/shell/*.md`.

Quality bar: `.cursor/rules/00-foundation/09-content-quality-standard.mdc`  
Index: `.cursor/prompts/CONTENT_QUALITY.md`

Do **not** use the short skeleton (`## Goal`, `{ .ra-facts }`, stop after `## Next`).

Prefer **Codex** for generation until the user changes agents.

---

## Audience progression

Layer content so students and professionals both gain value:

1. **Student entry** — plain definition, problem solved, smallest mental model  
2. **Practitioner bridge** — daily Cloud / DevOps / SRE / Platform work  
3. **Professional depth** — trade-offs, failure modes, security, evidence  
4. **Portfolio proof** — lab artefact the learner can discuss in interviews  

Use this progression *inside* sections as continuous prose — do **not** invent extra top-level headings, and do **not** label blocks “For beginners / practitioners / professionals”. Start simple, then deepen naturally.

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
- State beginner takeaway, practitioner skill, and production judgement.
- No separate `## Goal`. No `{ .ra-facts }` under the H1.

### Prerequisites

- Bullet list (knowledge and/or links).

### Learning Objectives

- Intro: `By the end of this tutorial, you will be able to:`
- 4–6 checkboxes (`- [ ] …`) that are measurable.

### Architecture

- One short intro sentence.
- One Excalidraw diagram: `![…](../assets/excalidraw/<name>.svg)`
- Never D2, Mermaid, or `assets/images/` for course diagrams.

### Theory

Preferred subsections (adapt names; keep depth):

1. `### What it is`
2. `### Why it matters`
3. `### How it works`
4. Topic headings **or** `### Key concepts and comparisons` (tables OK)
5. `### Common pitfalls`

Cover **every** concept from the technology prompt module for this tutorial.

Depth rule per concept:

- Beginner-safe explanation  
- Concrete command, config, or workflow example  
- Production judgement: when to use / avoid / what breaks  

Write at GeeksforGeeks clarity: define → show → compare → warn.

### Hands-on Lab

Title: `## Hands-on Lab`

Labs must be **production-grade interview preparation** — practical, production-oriented, and executable end-to-end.  
No markdown-only, note-taking, toy, or validate-only exercises. The learner **builds, breaks, fixes, and proves** a **real working system** for *this* topic (cloud sandbox, kind, LocalStack, or disposable VM as appropriate — not `null`/`local` stubs as the whole lab).

Required subsections (order fixed):

1. `### Objective` — one concrete outcome  
2. `### Prerequisites` — tools/accounts for *this* lab  
3. `### Lab environment` — `~/rebash-<technology>/labNN` (or `module-NN`) + runtime (Ubuntu VM, Docker, kind, local CLI)  
4. `### Real-world scenario` — 2–4 sentences of production context  
5. `### Step-by-step tasks` — `#### Task N – …` with create-file → code → run → **Expected output**  
6. `### Validation steps` — checkboxes proving the solution works  
7. `### Common errors and fixes` — table: Error | Cause | Fix  
8. `### Challenge exercise` — stretch **artefact** (script, unit, ACL, pipeline, rules) — not “write runbook.md”  
9. `### Learning outcomes` — bullets tied to tasks  
10. `### Cleanup` — remove disposable resources  

**Task shape (mandatory):**

````markdown
Create `main.tf`:

```hcl title="main.tf"
# file contents
```

``` {.bash .ra-terminal title="Terminal"}
terraform apply -auto-approve
```

!!! example "Expected output"
    Apply succeeds; resource exists.
````

- File fences: language + `title="filename"` (green file chrome)
- Command fences: `{.bash .ra-terminal title="Terminal"}` (dark terminal chrome without JS)  
- Command fences: `bash` + `title="Terminal"` (dark terminal chrome)  
- Success: `!!! example "Expected output"` — not only `**Expected output:**`  
- Review sample: `docs/labs/sample-code-block-conventions.md`  

Do **not** create files with `cat <<EOF`, `echo … > file`, or `printf` redirection. Those look ugly and hide the real file. Show the file in its own fence; use bash only to run and prove.

Rules:

- **2–4 tasks**, each tied to Theory for *this* slug and usable in interview storytelling  
- Short paste-safe bash for run/verify; prefer asserts (`test`, `grep -q`, exit codes) **after** real apply  
- Observable success on the **system** (Ready pod, cloud resource exists, service healthy, plan applied — not only “validate OK”)  
- Include at least one failure/drift/fix or production-shaped risk where the topic allows  
- Safe sandbox defaults + cleanup; no secrets; escape `${{` / `{%` / Go `{{` for mkdocs-macros  
- **Never** reuse a generic “host baseline + ip/ss” lab with only the title changed  
- **Never** ship simple / toy / simulate-forever labs as production interview prep  

**Good (users/sudo):** `useradd`, `usermod -aG`, create sudoers drop-in as a file fence + `visudo -c`, then `id` / `sudo -l` evidence.  
**Bad:** only `uname`/`df`/`ip` while the title says Users and sudo; or a wall of `cat > file <<EOF` heredocs; or Terraform that only `validate`s with `null_resource`.  

Full lab authoring rules: `.cursor/prompts/tutorials/create_lab.md`.

Apply/refresh generators only when they emit topic-specific labs:

```bash
python3 scripts/apply-production-labs.py --course <technology>
```

If the generator is still generic for a tech, **hand-write** the lab to this standard.

### Validation

Checkbox list:

- Lab path completed successfully  
- Can explain Theory in own words  
- Used modern tooling where applicable  
- Can describe one production failure mode for this topic  

### Code Walkthrough

5 short production habits for this topic (inspect → change → evidence → modern tools → least privilege).

### Security Considerations

5 bullets specific to the topic.

### Common Mistakes

2–4 `!!! warning` admonitions with **Fix:** guidance.

### Best Practices

5 actionable bullets.

### Troubleshooting

Markdown table: Symptom | Likely cause | Fix — real failures for this topic.

### Summary

2–3 sentences; point to next tutorial.

### Interview Questions

- **5–8 topic-specific** questions (concepts, debugging, security, trade-offs, production).  
- Difficulty ramp: ≥1 junior, ≥1 senior/production.  
- **Every question** is followed immediately by a **collapsible** answer (Material `pymdownx.details`):

```markdown
**1. Question text?**

??? success "Reveal answer"
    Answer paragraph(s). Explain *why*, not only *what*.
```

- Do **not** dump answers only at the end; do **not** use always-open `!!! tip` for the main answer.  
- Ban generic Cloud/platform boilerplate unrelated to this module.

### Related Tutorials

- Course index · next · optional prior/related  

### References

Official docs + course index.

---

## Frontmatter

Minimum:

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

Optional curriculum fields (`technology`, `module`, `learning_paths`, `skills`, `next`, `related`, `interview`, `certifications`, `labs`) may remain for tooling. **Body structure above is mandatory.**

---

## Anti-patterns

- `## Goal` as a top-level section  
- `{ .ra-facts }` under the title  
- Short skeleton stopping after `## Next`  
- Missing Architecture / Lab subsections / Interview sample answers  
- D2 or Mermaid diagrams  
- Note-taking Challenges  
- Templated labs that ignore the tutorial topic  

---

## Diagrams

```bash
python3 scripts/generate-excalidraw-svg.py
```

Assets: `docs/assets/excalidraw/` (`.svg` + `.excalidraw`).
