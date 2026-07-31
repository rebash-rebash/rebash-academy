---
title: "AI for DevOps — OpenAI, MCP, and LangChain"
description: "Use AI assistively in DevOps — OpenAI SDK patterns, MCP clients, LangChain basics, and human-approved automation agents with strong guardrails."
difficulty: advanced
estimated_time: "45–60 min"
technology: python
category: python
module: "Module 26 · AI for DevOps"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - openai
  - mcp
  - langchain
  - ai-ops
prerequisites:
  - python/security-for-devops-python
next:
  - python/troubleshooting-python-automation
related:
  - python/cli-applications-argparse-click-typer
  - python/production-engineering-patterns
labs: []
projects: []
interview: interview/python
certifications: []
tags:
  - python
  - ai
  - openai
  - mcp
  - langchain
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# AI for DevOps — OpenAI, MCP, and LangChain

## Overview

Use LLMs as **assistants** for ops work — summarise logs, draft runbooks, call tools via MCP — with human approval before any mutating action.

AI does not replace kubectl, Terraform, or judgment. It speeds reading and drafting. **Never** let a model hold long-lived cloud keys or auto-apply infrastructure without a human gate.

Complete [Security](security-for-devops-python.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 26 · AI for DevOps** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [REST APIs](rest-apis-requests-auth-and-resilience.md)
- [Configuration and Secrets](configuration-management-and-secrets.md)

### Recommended

- Optional API key for a provider; otherwise use the offline stub lab

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Call a chat API pattern with timeouts and secrets from env  
- [ ] Explain MCP (Model Context Protocol) clients at a high level  
- [ ] Sketch a LangChain-style tool-calling flow  
- [ ] List guardrails for AI-assisted automation  
- [ ] Design human-in-the-loop approval for destructive tools

## Architecture

This topic’s control points and relationships are shown below.

![AI for DevOps](../assets/excalidraw/python-ai-devops.svg)

## Theory

### What it is

AI-assisted DevOps tooling uses large language model (LLM) APIs and orchestration libraries to **summarise, draft, classify, and call tools** — while humans and policy still own mutations. In Python you typically see OpenAI-compatible SDKs, **Model Context Protocol (MCP)** clients that discover scoped tools, and frameworks such as **LangChain** for prompts, chains, and agents. Offline stubs remain first-class for labs and CI without keys.

### Why it matters

On-call noise is mostly text: logs, alerts, pull request diffs. Models compress that text and propose next steps. Without guardrails they also invent shell commands, leak secrets into prompts you log, or call write APIs. Treating AI as a **read-mostly assistant with allow-listed tools** is how platform teams gain speed without creating a new breach class.

### How it works

Load API keys from the environment (never commit them). Call chat/completions with timeouts and retry on 429 — same resilience as any HTTP client. Azure OpenAI and other providers differ mainly by base URL and auth. An MCP **client** connects to servers that expose tools/resources (docs, read-only cluster APIs, tickets). LangChain (or similar) wires prompt templates to those tools. Agents may choose tools; your code must still validate outputs before executing anything. Bound max tokens and log model name plus latency for cost control.

```python
# Conceptual — key from env, never committed
# from openai import OpenAI
# client = OpenAI()  # uses OPENAI_API_KEY
# client.chat.completions.create(...)
```

### Key concepts and comparisons

| Pattern | Example |
|---------|---------|
| Summarise | Compress incident logs |
| Draft | PR description / runbook |
| Classify | Severity from alert text |
| Tool use | Read-only `kubectl get` via MCP |

| Layer | Responsibility |
|-------|----------------|
| Model | Propose text / tool calls |
| Allow-list | Which tools exist |
| Human / policy | Approve writes |
| Validator | Schema-check before exec |

### Common pitfalls

- Pasting secrets, tokens, or full `.env` files into prompts.  
- Letting the model run arbitrary shell from its reply.  
- No timeout/cost cap → runaway bills or hung jobs.  
- Logging full prompts that contain customer data.  
- Skipping an offline stub so CI cannot run without a vendor key.

## Hands-on Lab

**Focus:** practise the core workflow for AI for DevOps — OpenAI, MCP, and LangChain

```bash
mkdir -p ~/rebash-python/module-26
cd ~/rebash-python/module-26

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
# Optional live SDK:
# python -m pip install 'openai==1.59.6'
```

### Step 1 – Offline “assistant” stub

```bash
cd ~/rebash-python/module-26
source .venv/bin/activate

cat > ai_assist.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def summarise_log(text: str) -> str:
    errors = [ln for ln in text.splitlines() if "ERROR" in ln]
    return json.dumps({
        "line_count": len(text.splitlines()),
        "error_count": len(errors),
        "sample_errors": errors[:5],
        "model": os.environ.get("AI_MODEL", "offline-stub"),
    }, indent=2)


def main() -> int:
    p = argparse.ArgumentParser(description="AI-assisted log summary (stub or live)")
    p.add_argument("logfile", type=Path)
    p.add_argument("--live", action="store_true", help="call real provider (needs key)")
    args = p.parse_args()
    text = args.logfile.read_text(encoding="utf-8", errors="ignore")
    if args.live:
        if not os.environ.get("OPENAI_API_KEY"):
            print("error: OPENAI_API_KEY required for --live", file=sys.stderr)
            return 2
        print("error: live path left to operator — wire OpenAI SDK with timeout", file=sys.stderr)
        return 1
    print(summarise_log(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

printf '%s\n' 'INFO start' 'ERROR timeout db' 'INFO ok' 'ERROR 502 upstream' > sample.log
python ai_assist.py sample.log
```

### Step 2 – Approval gate sketch

```bash
cat > approve.py << 'EOF'
#!/usr/bin/env python3
proposed = {"tool": "kubectl_delete", "args": {"resource": "pod/web-a"}}
print("PROPOSED", proposed)
answer = "n"  # in real CLI: input("Approve? [y/N] ")
if answer.lower() != "y":
    raise SystemExit("rejected")
print("would execute")
EOF

python approve.py || true
```

### Step 3 – MCP mental model notes

Write `mcp-notes.md`: server exposes `list_pods` (read); client must not expose `delete_namespace` without approval + RBAC.

## Validation

- [ ] Lab commands run under `~/rebash-python/module-26/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **AI for DevOps — OpenAI, MCP, and LangChain** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for python as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Pasting secrets, tokens, or full `.env` files into prompts.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Letting the model run arbitrary shell from its reply.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode AI for DevOps — OpenAI, MCP, and LangChain changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| High cost | Huge prompts / loops | Truncate logs; cap tokens |
| Hallucinated kubectl | Model invents flags | Never exec raw model text; use structured tools |
| Data leak | Prompt logs contain secrets | Redact before send/log |

## Summary

- AI assists; humans approve mutations  
- MCP/LangChain = tool orchestration, not magic  
- Offline stubs keep the course runnable without keys  
- Security module rules still apply

## Interview Questions

1. How does **AI for DevOps — OpenAI, MCP, and LangChain** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Troubleshooting Python Automation](troubleshooting-python-automation.md)

## References

- [OpenAI API docs](https://platform.openai.com/docs)  
- [Model Context Protocol](https://modelcontextprotocol.io/)  
- [LangChain](https://python.langchain.com/)
