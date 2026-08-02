# REBASH Academy — Create Hands-on Lab

Prefer **Codex** until the user explicitly changes the agent.

Read first:

- `.cursor/rules/00-foundation/09-content-quality-standard.mdc`  
- `.cursor/prompts/CONTENT_QUALITY.md`  
- For in-tutorial labs: `.cursor/prompts/tutorial-format-linux.md` → Hands-on Lab  

---

# Step 1 — Detect technologies

Identify technologies. Load relevant MCP servers. Verify commands against official docs.

Never invent flags or APIs.

---

## Role

You design labs like AWS Skill Builder / Microsoft Learn / Linux Foundation — **exercises, not essays**.

A lab is where the learner **applies** concepts by building, configuring, breaking, and fixing real systems.

---

# Objective

Ship a complete lab that is:

1. **Real-world** — mirrors production work (onboarding a VM, hardening SSH, shipping a pipeline, fixing a failed unit)  
2. **Executable** — every command block pastes cleanly and runs on the stated environment  
3. **Validated** — learner can prove success without guessing  
4. **Safe** — disposable resources, cleanup, no secrets  

---

# Lab philosophy

- Solve a real engineering problem  
- Prefer investigation + evidence over “click Next”  
- Include failures learners actually hit  
- Teach operational thinking (inspect → change → verify → cleanup)  

**Avoid:** toy `echo hello` labs, markdown note-taking, identical templates with only the title changed.

---

# Audience

Junior → mid DevOps, Cloud, Platform, SRE, Linux, Kubernetes administrators.

---

# Two lab types

## A) In-tutorial Hands-on Lab

Embedded under `## Hands-on Lab` in a tutorial. Must use the subsection list below. Keep 2–4 tasks; deepen in a standalone lab if needed.

## B) Standalone lab page

Under `docs/labs/`. Longer scenario, multiple tasks, still fully executable. Link from matching tutorials via frontmatter `labs:`.

---

# Required structure (both types)

```markdown
### Objective
### Prerequisites
### Lab environment
### Real-world scenario
### Step-by-step tasks
### Validation steps
### Common errors and fixes
### Challenge exercise
### Learning outcomes
### Cleanup
```

Standalone pages may wrap these under `# Lab — …` with Overview + Architecture first; keep the lab core identical.

---

# Section rules

### Objective

One sentence: what working result exists at the end (e.g. “Create a least-privilege app user, sudoers drop-in, and prove access with `id` and `sudo -l`.”).

### Prerequisites

Tools, OS, privileges, prior tutorials. Be honest (e.g. “Ubuntu 24.04 VM with sudo; not WSL-only for firewalld”).

### Lab environment

```bash
mkdir -p ~/rebash-<tech>/labNN && cd ~/rebash-<tech>/labNN
```

State runtime: local Ubuntu VM, Docker Engine, kind cluster, cloud sandbox, etc.

### Real-world scenario

2–4 sentences: who you are, what is broken or required, what “done” means for the business.

### Step-by-step tasks

For each task:

1. `#### Task N – <verb phrase>`  
2. One-line why (production relevance)  
3. Fenced `bash` (or language) block — **complete, paste-safe**  
4. `**Expected output:**` concrete success signal  

Use heredocs for files. Prefer:

```bash
set -euo pipefail
# …
test -f evidence.txt
grep -q 'expected' evidence.txt
```

### Validation steps

Checkboxes the learner ticks after proving the system works.

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| … | … | … |

### Challenge exercise

Stretch goal that produces another **artefact** (second user, timer unit, fail2ban jail stub, pipeline job). No “write a markdown essay”.

### Learning outcomes

3–5 bullets tied to completed tasks.

### Cleanup

Commands to remove users, units, containers, namespaces, state. Never “re-run the lab” as cleanup.

---

# Copy-paste safety rules

- Quote paths; avoid interactive prompts (`-y` for apt when appropriate)  
- Idempotent where practical (`|| true` only when documented)  
- Escape MkDocs macros: `${{`, `{%`, Go `{{`  
- Pin image tags when pulling containers  
- Warn before destructive disk/firewall/sshd changes; keep a second SSH session for hardening labs  

---

# Topic fidelity examples

| Topic | Minimum lab proof |
|-------|-------------------|
| Users / sudo | `useradd`, group, sudoers.d, `id`, `sudo -l` |
| Permissions / ACL | `chmod`/`chown`/`setfacl`, `namei -l` / `getfacl` |
| systemd | unit file, enable --now, `journalctl -u` evidence |
| SSH hardening | key auth, `sshd -t`, config drop-in, firewall allow |
| Text processing | sample log + grep/sed/awk pipeline + assert |
| Packages | install, verify version, hold/pin or remove |
| cron / timers | job runs; `list-timers` or cron log evidence |
| Docker | build/run, health, inspect (macros-safe format) |
| Kubernetes | namespace + workload Ready + evidence `tee` |
| Terraform | init/plan (null/local), show planned change |
| CI (GHA/GitLab) | YAML validates locally; job script runs offline |

---

# Quality checklist

- [ ] Scenario is production-flavoured  
- [ ] Commands run copy-paste on stated OS  
- [ ] Each task has Expected output  
- [ ] Validation proves the outcome  
- [ ] Errors table is realistic  
- [ ] Challenge is a working stretch, not notes  
- [ ] Cleanup is real  
- [ ] No secrets; macros escaped  
- [ ] Lab matches the tutorial/lab title topic  

---

# Final requirement

A learner with the prerequisites and a clean environment can finish without improvising missing commands.
