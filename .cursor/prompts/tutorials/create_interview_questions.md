# REBASH Academy — Create Interview Questions

Prefer **Codex** until the user explicitly changes the agent.

Read first:

- `.cursor/rules/00-foundation/09-content-quality-standard.mdc`  
- `.cursor/prompts/CONTENT_QUALITY.md`  

---

# Step 1 — Detect technologies

Identify technologies. Verify facts with MCP / official docs. No deprecated trivia.

---

## Role

You are a Principal Engineer and hiring interviewer for Cloud, DevOps, Platform, SRE, Security, Kubernetes, and Linux roles.

Create material that reflects **real interviews** — judgement and explanation, not flashcard trivia.

---

# Objectives

Help candidates:

- Explain concepts clearly  
- Debug with a method  
- Defend design trade-offs  
- Handle production scenarios  
- Show senior signal without arrogance  

---

# Two outputs

## A) In-tutorial `## Interview Questions`

- **5–8** questions tied to **this tutorial’s Theory and Lab**  
- Difficulty ramp (junior → senior)  
- **Every question** followed by a collapsible answer:

```markdown
**1. Question text?**

??? success "Reveal answer"
    Answer with *why* (signals interviewers listen for).
```

- Do not put answers only at the bottom; do not use always-open `!!! tip` for the main answer.

## B) Standalone interview guide (`docs/interview/<topic>.md`)

Full guide structure below.

---

# Standalone guide structure

```yaml
---
title: "…"
description: "…"
difficulty: beginner|intermediate|advanced|expert
author: Shaik Basha
last_updated: "YYYY-MM-DD"
category: interview
technology: <technology>
tags: […]
comments: false
---
```

```markdown
# <Topic> Interview Guide

## Role overview
## Skills expected
## How interviewers evaluate answers
## Core concept questions
## Scenario / production questions
## Troubleshooting questions
## Hands-on / whiteboard tasks
## Architecture / trade-off questions
## Behavioural (role-relevant)
## Model answers (selected)
## Follow-up questions interviewers ask
## Red flags and strong signals
## Practice plan
## References
```

---

# Question design rules

| Type | Purpose | Example stem |
|------|---------|--------------|
| Concept | Precise definition + mental model | “What is … and what problem does it solve?” |
| Compare | Trade-offs | “When would you choose A over B?” |
| Debug | Methodical triage | “Service is down — what do you check first and why?” |
| Security | Least privilege / failure | “How do you harden … without locking yourself out?” |
| Production | Operations evidence | “What would you capture for the incident ticket?” |
| Design | Constraints | “Design … for multi-AZ with rollback” |

**Avoid:** acronym expansion quizzes, version-number trivia, “list 10 commands” with no judgement.

---

# Answer quality (model answers)

Each model answer should:

1. Open with a direct definition or decision  
2. Give a short concrete example  
3. Note a trade-off or failure mode  
4. Close with how you’d verify in production  

Use British English; expand acronyms on first use.

Length: 120–220 words for mid-level; shorter for junior; deeper for senior prompts.

---

# Follow-ups

For every major question, list 1–2 follow-ups interviewers use to test depth, e.g.:

- “What breaks if that assumption is wrong?”  
- “How would you prove it with commands?”  
- “How does this change under Kubernetes / multi-account / regulated env?”  

---

# Strong signals vs red flags

Document briefly:

**Strong:** structured triage, least privilege, evidence-first, rollback thinking  
**Weak:** memorised flags without meaning, `chmod 777`, “restart until fixed”, ignoring blast radius  

---

# In-tutorial format (copy pattern)

```markdown
## Interview Questions

**1. …?**

??? success "Reveal answer"
    …

**2. …?**

??? success "Reveal answer"
    …
```

---

# Quality checklist

- [ ] Questions match the page topic (not generic Cloud filler)  
- [ ] Mix of concept / scenario / troubleshooting  
- [ ] Junior and senior coverage  
- [ ] Every question has a collapsible `??? success "Reveal answer"` that explains *why*  
- [ ] Follow-ups present (standalone)  
- [ ] No invented product behaviour  
- [ ] British English  

---

# Final requirement

A candidate who studied only REBASH materials for this topic should be able to answer at interview depth — not just recognise buzzwords.
