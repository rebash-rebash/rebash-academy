---
title: AI for DevOps — Frozen syllabus
description: Canonical frozen syllabus for the AI for DevOps course (v1). Do not renumber or rename without an explicit syllabus change.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
  - ai
  - syllabus
last_updated: "2026-08-04"
status: frozen
version: "1.0"
---

# AI for DevOps — Frozen syllabus (v1.0)

**Frozen:** 2026-08-04  
**Status:** Syllabus locked. Implement tutorials against this document. Do not add, remove, rename, or reorder modules without an explicit syllabus revision (bump `version`).

Canonical generation prompt: [`.cursor/prompts/technologies/ai.md`](../../.cursor/prompts/technologies/ai.md)  
Course URL prefix: `docs/ai/`  
Career path: `ai-for-devops`

---

## Locked product decisions

| Decision | Freeze |
|----------|--------|
| Module count | **14** modules · **14** tutorials (one tutorial per module) |
| Difficulty | Intermediate (plain teaching voice; prereqs carry foundations) |
| Duration | 8–10 weeks course · 10–14 weeks with Docker/Kubernetes on the career path |
| LLM runtime | **Mock-first.** Optional OpenAI-compatible API if `OPENAI_API_KEY` is set. **Ollama** documented as preferred local path. Paid API never required. |
| Kubernetes in v1 | **Mock** cluster / fake API clients only (no kind required) |
| Course nav | Overview (roadmap on page) + Module 1–14 only. No Labs / Quizzes / Projects / Capstone / Cheatsheets / Interview / Certifications / FAQ / Roadmap sidebar hubs |
| Related depth (out of v1) | Cloud AI (Bedrock / Vertex / Azure OpenAI), fine-tuning, multi-agent handoffs — deferred |
| Python Module 26 | Remains a Python taster; after AI course ships, cross-link “Go deeper → AI for DevOps”. Do not delete M26 in v1 |
| Capstone (in Module 14 lab) | Offline-first ops assistant: RAG + allowlisted tools + audit + human gate |
| Standalone project / capstone IDs | `ai-ops-assistant` · `ai-assisted-platform-ops` (backlog; not course nav) |
| Lab root | `~/rebash-ai/module-NN` |
| Philosophy | AI proposes; humans and code dispose. No blind production mutations |

---

## Positioning

**Title:** AI for DevOps Engineers  
**Promise:** Use Large Language Models (LLMs) as assistants for DevOps — propose → validate → automate with gates.  
**Not in scope:** Deep ML theory, model training from scratch, “ChatGPT tips” without engineering guardrails.

### Prerequisites

| Required | Nice to have |
|----------|----------------|
| Linux | Docker |
| Shell | Kubernetes (context for later modules; labs stay mock) |
| Python (APIs, CLIs, secrets) | Cloud familiarity |
| Git | Python Module 26 |

### Target roles

AI for DevOps Engineer · Automation Engineer · MLOps Associate · DevOps / Platform / SRE adding AI tooling

---

## Learning roadmap (course Overview)

1. **Foundations** — what AI for DevOps is / isn’t; risk model  
2. **Prompting for ops** — logs, tickets, runbooks; evaluation  
3. **Knowledge for ops** — embeddings, vector stores, Retrieval-Augmented Generation (RAG)  
4. **Tools & agents** — function calling, Model Context Protocol (MCP), safe loops  
5. **Pipeline & platform** — CI assistants, observability copilots  
6. **Operate & govern** — security, cost, production patterns  

---

## Frozen module map

| # | Module title | Tutorial ID | Tutorial title | Lab proof |
|---|--------------|-------------|----------------|-----------|
| 1 | Foundations | `ai/ai-for-devops-foundations` | AI for DevOps Foundations | Decision matrix + threat notes for a fake auto-remediate bot |
| 2 | LLM & APIs | `ai/llm-and-api-fundamentals` | LLM and API Fundamentals | CLI chat against mock client; optional live/Ollama |
| 3 | Prompt Engineering | `ai/prompt-engineering-for-ops` | Prompt Engineering for Ops | Log-summariser CLI; no secret leakage |
| 4 | Evaluation | `ai/evaluation-and-reliability` | Evaluation and Reliability | Golden-file eval: 10 incidents → expected labels |
| 5 | Embeddings | `ai/embeddings-and-semantic-search` | Embeddings and Semantic Search | Embed local runbook snippets; top-k search |
| 6 | Vector Stores | `ai/vector-stores-for-ops` | Vector Stores for Ops | Index runbooks; query “disk full” → chunks |
| 7 | RAG | `ai/retrieval-augmented-generation-for-ops` | Retrieval-Augmented Generation for Ops | RAG CLI with citations; break/fix citation |
| 8 | Tool Calling | `ai/tool-calling-and-function-apis` | Tool Calling and Function APIs | Allowlist tools; deny `delete_*` |
| 9 | MCP | `ai/mcp-for-devops` | Model Context Protocol (MCP) for DevOps | Minimal MCP-style server + client tool list |
| 10 | Agents | `ai/agents-for-ops-workflows` | Agents for Ops Workflows | Classify → suggest checks → stop before mutate |
| 11 | CI/CD | `ai/ai-in-ci-cd` | AI in CI/CD | Local/CI job summarises diff via mock LLM → artefact |
| 12 | Observability | `ai/observability-copilots` | Observability Copilots | Enrich alert JSON → runbook link + checklist |
| 13 | Governance | `ai/security-cost-and-governance` | Security, Cost, and Governance | Prompt-injection red team; block + audit log |
| 14 | Production | `ai/production-ai-for-devops` | Production AI for DevOps | Capstone glue: RAG + tool gate + audit |

---

## Tutorial chain (prerequisites)

```
1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14
```

Each tutorial’s `prerequisites` frontmatter points at the previous tutorial ID (Module 1 has Linux/Python/Git as soft prereqs in prose).

---

## Interview outcomes (end of course)

Learners should defend:

- Why AI must not hold long-lived production credentials  
- RAG vs fine-tuning for runbooks  
- How prompt changes are evaluated (golden tests)  
- MCP / tool-calling trust boundaries  
- Cost controls and prompt-injection defences  

---

## Delivery conventions

- Topic-first Overview openings (no audience stamp on every page)  
- Teaching pattern: problem → analogy → term → tiny example → interview one-liner → depth → real lab  
- Labs: create → prove → break/fix where useful → cleanup  
- Terminal fences: `{.bash .ra-terminal title="Terminal"}`  
- Interview: question outside `??? success "Reveal answer"`  
- British English; explain acronyms on first use  
- Escape template syntax for mkdocs-macros (`{% raw %}`) when needed  

---

## Implementation phases (post-freeze)

| Phase | Modules | Outcome |
|-------|---------|---------|
| A | Skeleton: `index.md`, `.pages` when files exist, backlog sync | Structure ready |
| B | 1–4 | Prompt + eval core |
| C | 5–7 | Working RAG lab |
| D | 8–10 | Safe tool/agent loop |
| E | 11–14 | CI + gov + production + capstone |
| F | Career path, Python M26 cross-links, catalogs | Mark course ready |

**Phase B (Modules 1–4):** published 2026-08-04.

**Phase C (Modules 5–7):** published 2026-08-04.

**Phase D (Modules 8–10):** published 2026-08-04.

**Phase E (Modules 11–14):** published 2026-08-04.

**Course status:** complete (v1.0 syllabus fully published).

---

## Out of syllabus (explicit non-goals for v1)

- Training or fine-tuning production models  
- Full MLOps / feature-store platforms  
- Requiring paid cloud AI accounts  
- Requiring a live Kubernetes cluster  
- Course-sidebar hub pages (labs/quiz/faq/roadmap as separate nav items)  

---

## Change control

To revise this syllabus: update this file, bump `version`, update `curriculum.yaml`, `tutorial_backlog.md`, `.cursor/prompts/technologies/ai.md`, and `docs/ai/index.md` in the same change.
