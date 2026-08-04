---
title: Overview
description: "AI for DevOps Engineers — complete 14-module course: LLMs, RAG, tools, MCP, agents, CI/CD, observability, and governed production assistants."
difficulty: intermediate
estimated_time: "8–10 weeks"
author: Shaik Basha
last_updated: "2026-08-04"
category: ai
technology: ai
tags:
  - ai
  - devops
  - automation
  - course
comments: false
---

# AI for DevOps Engineers

**Duration:** 8–10 weeks · **Difficulty:** Intermediate · **Syllabus:** frozen v1.0 · **Status:** complete
{ .ra-facts }

Use Large Language Models (LLMs) as assistants for DevOps work: propose → validate → automate with gates. Suitable if you already use Linux, Shell, Python, and Git.

!!! tip "How to use this course"
    Work modules in order. Labs use mock LLMs, hashing embeddings, and allowlisted tools under `~/rebash-ai/module-NN`. A paid API is never required.

---

## Learning roadmap

1. **Foundations** — what AI for DevOps is / isn’t; risk model  
2. **Prompting for ops** — logs, tickets, runbooks; evaluation  
3. **Knowledge for ops** — embeddings, vector stores, Retrieval-Augmented Generation (RAG)  
4. **Tools & agents** — function calling, Model Context Protocol (MCP), safe loops  
5. **Pipeline & platform** — CI assistants, observability copilots  
6. **Operate & govern** — security, cost, production patterns  

### Prerequisites

- [Linux](../linux/index.md) · [Shell](../shell/index.md) · [Python](../python/index.md) · [Git](../git/index.md)

---

## Modules

| Module | Tutorial | Lab proof |
|-------:|----------|-----------|
| 1 | [AI for DevOps Foundations](ai-for-devops-foundations.md) | Policy gate + threat notes |
| 2 | [LLM and API Fundamentals](llm-and-api-fundamentals.md) | Mock-first chat CLI |
| 3 | [Prompt Engineering for Ops](prompt-engineering-for-ops.md) | Log summariser + redaction |
| 4 | [Evaluation and Reliability](evaluation-and-reliability.md) | 10-incident golden eval |
| 5 | [Embeddings and Semantic Search](embeddings-and-semantic-search.md) | Top-k runbook search |
| 6 | [Vector Stores for Ops](vector-stores-for-ops.md) | SQLite index + disk-full query |
| 7 | [Retrieval-Augmented Generation for Ops](retrieval-augmented-generation-for-ops.md) | RAG + citation break/fix |
| 8 | [Tool Calling and Function APIs](tool-calling-and-function-apis.md) | Allowlist; deny `delete_*` |
| 9 | [Model Context Protocol (MCP) for DevOps](mcp-for-devops.md) | List/call fake metrics tools |
| 10 | [Agents for Ops Workflows](agents-for-ops-workflows.md) | Stop before mutate |
| 11 | [AI in CI/CD](ai-in-ci-cd.md) | Advisory diff summary artefact |
| 12 | [Observability Copilots](observability-copilots.md) | Alert → runbook checklist |
| 13 | [Security, Cost, and Governance](security-cost-and-governance.md) | Injection block + audit |
| 14 | [Production AI for DevOps](production-ai-for-devops.md) | Capstone: RAG + gate + approve |

---

## Capstone

[Production AI for DevOps](production-ai-for-devops.md) — offline ops assistant with citations, allowlisted tools, audit trail, and `--approve` before dry-run mutate.

## Start here

1. [AI for DevOps Foundations](ai-for-devops-foundations.md)

## Related

- [AI for DevOps Engineer learning path](../learning-paths/ai-for-devops/index.md)
- [Python — OpenAI, MCP, and LangChain](../python/ai-for-devops-openai-mcp-langchain.md)
