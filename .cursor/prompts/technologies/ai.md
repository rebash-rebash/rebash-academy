# Technology Definition

> **Syllabus frozen:** Follow [`docs/_curriculum/ai-for-devops-syllabus.md`](../../../docs/_curriculum/ai-for-devops-syllabus.md) (v1.0). Do not renumber or rename modules without a syllabus revision.
>
> **Content quality:** Follow `.cursor/prompts/CONTENT_QUALITY.md`, `tutorial-format-linux.md`, `create_lab.md`, and `create_interview_questions.md`. Labs: topic-specific, copy-paste executable, mock-first LLM. Prefer Codex until the user changes agents.

## Course

AI for DevOps Engineers

---

## Description

A production-focused AI for DevOps course for engineers who already use Linux, Shell, Python, and Git.

Teach Large Language Models (LLMs), prompts, Retrieval-Augmented Generation (RAG), Model Context Protocol (MCP), and agents as **engineering accelerators** with human oversight — never as silent production actors.

Learners finish able to build offline-first ops assistants: propose → validate → automate with gates.

---

## Target Roles

- AI for DevOps Engineer
- Automation Engineer
- MLOps Associate
- DevOps / Platform / Site Reliability Engineering (SRE) engineers adding AI tooling

---

## Difficulty

Intermediate (plain language; prerequisites carry foundations)

---

## Estimated Duration

8–10 weeks (course) · 10–14 weeks with Docker/Kubernetes on the learning path

---

## Prerequisites

- Linux
- Shell Scripting
- Python for DevOps
- Git
- Docker / Kubernetes recommended for context (labs use mocks in v1)

---

## Locked lab runtime

- Default: **mock LLM** under `~/rebash-ai/module-NN`
- Optional: OpenAI-compatible API when `OPENAI_API_KEY` is set
- Preferred local: **Ollama** (document; never require)
- Mutations behind dry-run / human approval
- Kubernetes: mock clients only in v1

---

## MCP Servers

Optional

- Context7
- GitHub
- Filesystem
- Kubernetes (concepts / mocks)

---

# Modules (frozen v1 — one tutorial each)

## Module 1 — Foundations

**File:** `ai-for-devops-foundations.md`  
**ID:** `ai/ai-for-devops-foundations`

- What AI for DevOps is and is not
- Human-in-the-loop risk model
- AI vs MLOps vs platform automation
- Threat notes for auto-remediation

**Lab proof:** Decision matrix + threat notes for a fake auto-remediate bot

---

## Module 2 — LLM & APIs

**File:** `llm-and-api-fundamentals.md`  
**ID:** `ai/llm-and-api-fundamentals`

- Tokens, chat completions, models
- Latency and cost basics
- OpenAI-compatible clients
- Mock vs live vs Ollama

**Lab proof:** CLI chat against mock client; optional live/Ollama

---

## Module 3 — Prompt Engineering

**File:** `prompt-engineering-for-ops.md`  
**ID:** `ai/prompt-engineering-for-ops`

- Structured prompts for logs and tickets
- Few-shot and JSON output
- Secret hygiene in prompts

**Lab proof:** Log-summariser CLI; prove secrets stay out of prompts

---

## Module 4 — Evaluation

**File:** `evaluation-and-reliability.md`  
**ID:** `ai/evaluation-and-reliability`

- Hallucinations and failure modes
- Golden tests for prompts
- Regression of prompt changes

**Lab proof:** Golden-file eval suite (10 incidents → expected labels)

---

## Module 5 — Embeddings

**File:** `embeddings-and-semantic-search.md`  
**ID:** `ai/embeddings-and-semantic-search`

- Embeddings for runbooks and tickets
- Semantic search concepts
- Local / fake vectors acceptable

**Lab proof:** Embed runbook snippets; top-k search

---

## Module 6 — Vector Stores

**File:** `vector-stores-for-ops.md`  
**ID:** `ai/vector-stores-for-ops`

- Simple stores (Chroma / FAISS / SQLite-class)
- Chunking for ops docs

**Lab proof:** Index runbooks; query “disk full” → relevant chunks

---

## Module 7 — RAG

**File:** `retrieval-augmented-generation-for-ops.md`  
**ID:** `ai/retrieval-augmented-generation-for-ops`

- Retrieve → prompt → answer
- Citations and grounding
- Break/fix missing sources

**Lab proof:** RAG CLI with source paths; break citation → fix

---

## Module 8 — Tool Calling

**File:** `tool-calling-and-function-apis.md`  
**ID:** `ai/tool-calling-and-function-apis`

- Model proposes tool; code executes
- Allowlists and deny lists
- Read-only vs mutating tools

**Lab proof:** Tools `read_log`, `list_pods` (mock); deny `delete_*`

---

## Module 9 — MCP

**File:** `mcp-for-devops.md`  
**ID:** `ai/mcp-for-devops`

- Model Context Protocol (MCP) idea
- Client/server roles
- Read-only ops context

**Lab proof:** Minimal MCP-style server exposing fake metrics; client lists tools

---

## Module 10 — Agents

**File:** `agents-for-ops-workflows.md`  
**ID:** `ai/agents-for-ops-workflows`

- Plan → act → observe
- Stop conditions
- No silent production mutations

**Lab proof:** Incident agent classifies → suggests checks → stops before mutate

---

## Module 11 — CI/CD

**File:** `ai-in-ci-cd.md`  
**ID:** `ai/ai-in-ci-cd`

- PR / diff summariser (advisory)
- Flaky-test explainer patterns
- Policy bot as advice only

**Lab proof:** Local or CI job summarises diff via mock LLM → artefact

---

## Module 12 — Observability

**File:** `observability-copilots.md`  
**ID:** `ai/observability-copilots`

- Alert enrichment
- Log/metric narrative
- On-call assist patterns

**Lab proof:** Enrich alert JSON → runbook link + checklist (mock LLM)

---

## Module 13 — Governance

**File:** `security-cost-and-governance.md`  
**ID:** `ai/security-cost-and-governance`

- Prompt injection
- Data exfiltration and keys
- Budgets and audit trails

**Lab proof:** Red-team prompt injection; prove block + audit log

---

## Module 14 — Production

**File:** `production-ai-for-devops.md`  
**ID:** `ai/production-ai-for-devops`

- Assistant architecture and SLOs
- Rollout and ownership
- Capstone glue

**Lab proof:** RAG + tool gate + audit under `~/rebash-ai/module-14` (capstone)

---

# Out of v1 (do not invent as required modules)

- Amazon Bedrock / Vertex AI / Azure OpenAI deep dives
- Fine-tuning
- Multi-agent orchestration platforms
- Live kind/EKS cluster labs

---

# Related

- Python Module 26: `python/ai-for-devops-openai-mcp-langchain` (taster)
- Learning path: `docs/learning-paths/ai-for-devops/`
- Rule: `.cursor/rules/40-technologies/48-ai-for-devops.mdc`
