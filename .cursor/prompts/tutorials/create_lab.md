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

# Mandatory bar — production-grade interview preparation

**All labs** (in-tutorial and standalone) must be **production-grade interview preparation tasks**, not simple demos.

A stranger preparing for a Cloud / DevOps / Platform / SRE interview should finish the lab able to **explain what they built, how they proved it, and what they would do when it breaks** — the same class of work as a mid-level ticket on a real team.

| Must | Must not |
|------|----------|
| Build or change **real** systems (VMs, packages, units, containers, Kubernetes, cloud APIs, CI pipelines, remote state) | Toy `null_resource` / `local_file` / echo-only labs as the whole exercise |
| **Apply** and prove with operational CLIs | Pass only because `validate` / `fmt` / syntax-check succeeded |
| Include diagnose-and-fix (drift, failed unit, bad plan, auth, crashloop) | Happy-path click-through with no failure |
| Mandatory **cleanup** of durable/billable resources | Leave sandboxes dirty; skip destroy |
| Scenario reads like a production ticket / interview whiteboard | “Hello world” with no stakes |

Use cloud **sandbox** / free tier, **kind**, **LocalStack**, or a disposable Ubuntu VM as needed. Document accounts in Prerequisites. Prefer live apply over forever-simulate. Asserts support proof — they do not replace real work.

---

# Objective

Ship a complete lab that is:

1. **Interview / production real** — mirrors day-1 job work (onboarding a VM, hardening SSH, shipping a pipeline, remote state, fixing a failed unit)  
2. **Executable** — every command block pastes cleanly and runs on the stated environment  
3. **Validated on the system** — prove pods Ready, infra exists, service healthy — not only that config parsed  
4. **Safe** — disposable sandbox resources, cleanup, no secrets  

---

# Lab philosophy

- Solve a real engineering problem a hiring manager would recognise  
- Prefer investigation + evidence over “click Next”  
- Include failures learners actually hit in production and interviews  
- Teach operational thinking (inspect → change → verify → cleanup)  

**Avoid:** toy labs, simple validate-only paths, markdown note-taking (checklists / runbook diaries), **“Capture principles / stages / glossary” YAML or JSON as a task**, identical templates with only the title changed, and **ugly file creation via `echo` / `printf` / `cat <<EOF` heredocs**.

Principles, workflows, and glossaries belong in **Theory** and **Interview Questions** — never as Lab Task 1.

**Evidence instead of notes:** `tee *.txt` from real commands, asserts (`test`, `grep -q`), and real project files (`Jenkinsfile`, workflow YAML, compose, Terraform). Keep `.md` only for legitimate repo artefacts (short app `README.md`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/`).

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

Keep each task **straight and readable** — Microsoft Learn style:

1. `#### Task N – <verb phrase>`  
2. One-line why (production relevance)  
3. Tell the learner to **create the file** (path + name)  
4. Show the **file contents** in the correct language fence (`python`, `yaml`, `groovy`, `bash` for scripts, etc.) — not inside a shell heredoc  
5. Show the **run / verify** commands in a short `bash` fence  
6. `**Expected output:**` concrete success signal  

#### Canonical pattern (preferred)

Use Material fence titles: files get `title="filename"`, commands get `{.bash .ra-terminal title="Terminal"}` so dark terminal chrome works without JavaScript.  
Put success criteria in `!!! example "Expected output"` (not only bold prose).  
Always set a language tag. Optional: `linenums="1"` on long files (40+ lines).

Review sample: `docs/labs/sample-code-block-conventions.md`.

````markdown
#### Task 1 – Create and run a hello script

Create `hello.py` in the lab directory:

```python title="hello.py"
print("hello from rebash")
```

Run it:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-<tech>/labNN
python3 hello.py | tee hello-out.txt
grep -q 'hello from rebash' hello-out.txt
```

!!! example "Expected output"
    `hello-out.txt` contains `hello from rebash`.
````

#### Multi-file example

````markdown
#### Task 2 – Add Compose for Jenkins LTS

Create `compose.yaml`:

```yaml title="compose.yaml"
services:
  jenkins:
    image: jenkins/jenkins:lts-jdk17
    ports:
      - "8080:8080"
    volumes:
      - jenkins_home:/var/jenkins_home
volumes:
  jenkins_home:
```

Start and check:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-jenkins/module-02
docker compose up -d
docker compose ps | tee compose-ps.txt
```

!!! example "Expected output"
    `compose-ps.txt` shows the `jenkins` service running.
````

#### File-creation rules

| Do | Don't |
|----|-------|
| “Create `app.py`:” then a `python` fence | `cat > app.py << 'EOF'` … |
| “Create `ci.yml`:” then a `yaml` fence | `echo '…' > ci.yml` |
| Short `bash` blocks for **run / verify / cleanup** only | Giant bash blocks that both write files and run them |
| Learner copies content into the editor (or IDE) | Teaching file creation via shell redirection |

**Exception (rare):** tiny one-liners generated by a tool (`ssh-keygen`, `openssl`) — those stay as commands. Config/source/pipeline files always use the create-file + language-fence pattern.

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

- File bodies in language fences; run/verify in short `bash` fences  
- Quote paths; avoid interactive prompts (`-y` for apt when appropriate)  
- Idempotent where practical (`|| true` only when documented)  
- Escape MkDocs macros: `${{`, `{%`, Go `{{`  
- Pin image tags when pulling containers  
- Warn before destructive disk/firewall/sshd changes; keep a second SSH session for hardening labs  
- In scripts the learner creates, `set -euo pipefail` is fine — show the script as a `bash` file fence, then `chmod +x` + run  

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
- [ ] Files introduced as “Create `name.ext`:” + language fence (no `cat`/`echo` file writes)  
- [ ] Run/verify commands are short and separate  
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
