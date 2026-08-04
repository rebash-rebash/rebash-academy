---
title: "Troubleshooting Ansible"
description: "Debug Ansible — YAML errors, SSH connectivity, variables, inventory mistakes, module failures, and verbosity with -vvv."
difficulty: intermediate
estimated_time: "45–60 min"
technology: ansible
category: ansible
module: "Module 17 · Troubleshooting"
learning_paths:
  - devops-engineer
  - platform-engineer
  - cloud-engineer
  - site-reliability-engineer
skills:
  - ansible
  - troubleshooting
prerequisites:
  - ansible/production-ansible-practices
next:
  - ansible/index
related:
  - ansible/ansible-collections-and-galaxy
  - linux/troubleshooting-linux-systems
labs: []
projects: []
interview: interview/ansible
certifications:
  - RHCE
tags:
  - ansible
  - troubleshooting
  - debugging
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# Troubleshooting Ansible

## Overview

Most Ansible failures are not mysterious — they cluster into a short list: invalid YAML, SSH or privilege escalation problems, wrong inventory host, undefined variables, or a module returning `failed`. A fixed triage order (`--syntax-check` → inventory ping → `-vvv` task output) saves hours during change windows.

This is **Tutorial 17** in **Module 17: Troubleshooting** of the REBASH Academy **Ansible for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers. Reference: [Ansible debugging guide](https://docs.ansible.com/ansible/latest/user_guide/playbooks_error_handling.html).

## Prerequisites

- [Production Ansible Practices](production-ansible-practices.md)
- Basic SSH troubleshooting on Linux

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Fix YAML and Jinja errors caught by `--syntax-check`
- [ ] Diagnose inventory mismatches and unreachable hosts
- [ ] Use `-vvv` verbosity to inspect module arguments and responses
- [ ] Repair a broken playbook and capture before/after evidence
- [ ] Document common failure modes in a triage table

## Architecture

Failures originate in playbook syntax, inventory resolution, transport (SSH), variable precedence, or module execution on the target.

![Linux troubleshooting flow](../assets/excalidraw/linux-troubleshooting.svg)

## Theory

### What it is

**Ansible troubleshooting** follows layers:

| Layer | Tools | Typical errors |
|-------|-------|----------------|
| Syntax | `ansible-playbook --syntax-check`, `ansible-lint` | Indentation, undefined Jinja |
| Inventory | `ansible-inventory --graph`, `--list` | Missing host, wrong group |
| Connectivity | `ansible -m ping`, `ssh -vvv` | Timeout, key, sudo |
| Variables | `ansible-playbook -e debug_var`, `-vvv` | Undefined, wrong precedence |
| Modules | `-vvv`, `register` + `debug` | Permission, idempotency, bad args |

### Why it matters

On-call engineers need a playbook-independent checklist. The same steps apply whether the failure is nginx config or a Kubernetes bootstrap role.

### How it works

Standard triage:

1. **Syntax-check** locally — no SSH required.
2. **Inventory graph** — confirm host is in expected group.
3. **Ping** — `ansible target -m ping -i inventories/prod`.
4. **Increase verbosity** — `-v` … `-vvvv` on failing play.
5. **Isolate** — `--tags` or `--start-at-task` to rerun one task.
6. **Validate vars** — `hostvars`, `group_vars`, Vault decrypt.

### Key concepts and comparisons

| Symptom | Often actually |
|---------|----------------|
| `UNREACHABLE!` | SSH/firewall/wrong `ansible_host` |
| `undefined variable` | Typo or missing `group_vars` |
| `Permission denied` | `become` / sudoers / remote user |
| `Module not found` | Collection not installed |
| Silent wrong behaviour | Cached facts or wrong inventory `-i` |

### Common pitfalls

- Editing production before syntax-check — **Fix:** always run `--syntax-check` first.
- Assuming `hosts: all` is safe — **Fix:** use limits (`--limit`) in prod.
- Ignoring `changed=false` but task failed — **Fix:** read `failed_when` / `ignore_errors` logic.

## Hands-on Lab

### Objective

Create a deliberately broken playbook that fails `--syntax-check`, fix it, demonstrate an inventory host miss, and capture before/after evidence logs.

### Prerequisites

- Ansible 2.18+
- No remote hosts required (localhost inventory)

### Lab environment

Workspace: `~/rebash-ansible/module-17`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-ansible/module-17/{inventories,playbooks} && cd ~/rebash-ansible/module-17
```

### Real-world scenario

A teammate pushed a hotfix playbook during an incident. CI was bypassed. You must reproduce the syntax failure, fix it, and prove an inventory typo would have caused a zero-host play before anyone ran against production.

### Step-by-step tasks

#### Task 1 – Create broken playbook and capture syntax failure

Create `inventories/lab/hosts.yml`:

```yaml title="hosts.yml"
all:
  hosts:
    localhost:
      ansible_connection: local
```

Create `playbooks/broken-site.yml` with an intentional YAML error (bad indent on `tasks`):

```yaml
---
- name: Broken site play
  hosts: localhost
  gather_facts: false
  tasks:
   - name: Broken indent task
      ansible.builtin.debug:
        msg: "this indent is invalid"
```

Run syntax-check and save failure evidence:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-ansible/module-17
ansible-playbook --syntax-check -i inventories/lab playbooks/broken-site.yml \
  > syntax-before.txt 2>&1 || true
grep -Ei 'error|yaml|while scanning' syntax-before.txt
```

!!! example "Expected output"
    Non-zero exit; log contains YAML/syntax error text.


#### Task 2 – Fix playbook and capture passing syntax-check

Create `playbooks/fixed-site.yml`:

```yaml title="fixed-site.yml"
---
- name: Fixed site play
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Valid debug task
      ansible.builtin.debug:
        msg: "syntax OK after fix"
```

Run syntax-check on fixed playbook:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-ansible/module-17
ansible-playbook --syntax-check -i inventories/lab playbooks/fixed-site.yml \
  | tee syntax-after.txt
grep -q 'playbook: playbooks/fixed-site.yml' syntax-after.txt
! grep -Ei 'error|fatal' syntax-after.txt
```

!!! example "Expected output"
    Syntax check passes; no error/fatal lines in output.


#### Task 3 – Demonstrate inventory host miss

Create `playbooks/needs-app-group.yml`:

```yaml title="needs-app-group.yml"
---
- name: Play targeting missing group
  hosts: app
  gather_facts: false
  tasks:
    - name: Should not run if inventory miss
      ansible.builtin.debug:
        msg: "app tier task"
```

Create `inventories/missing-app/hosts.yml` (no `app` group):

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
```

Run with verbosity and capture zero-host behaviour:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-ansible/module-17
ansible-playbook -i inventories/missing-app playbooks/needs-app-group.yml -vv \
  | tee inventory-miss.txt
grep -Ei 'skipping.*no hosts matched|empty|0 hosts' inventory-miss.txt
```

!!! example "Expected output"
    Play skips or reports no matching hosts for `app`.


Fix inventory — create `inventories/with-app/hosts.yml`:

```yaml title="hosts.yml"
all:
  children:
    app:
      hosts:
        localhost:
          ansible_connection: local
```

Re-run:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-ansible/module-17
ansible-playbook -i inventories/with-app playbooks/needs-app-group.yml \
  | tee inventory-hit.txt
grep -q 'app tier task' inventory-hit.txt
grep -q 'PLAY RECAP' inventory-hit.txt
```

!!! example "Expected output"
    Debug message appears; play completes.


#### Task 4 – Module failure demo with -vvv evidence

Create `playbooks/module-fail.yml`:

```yaml title="module-fail.yml"
---
- name: Module failure demo
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Run missing command
      ansible.builtin.command:
        cmd: /usr/bin/this-binary-does-not-exist-rebash
      register: cmd_out
      ignore_errors: true

    - name: Show failure details
      ansible.builtin.debug:
        var: cmd_out
```

Run with high verbosity:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-ansible/module-17
ansible-playbook -i inventories/lab playbooks/module-fail.yml -vvv \
  | tee module-fail-vvv.txt
grep -q 'rc' module-fail-vvv.txt
grep -q 'this-binary-does-not-exist-rebash' module-fail-vvv.txt
```

!!! example "Expected output"
    Verbose log shows command and non-zero return code in registered var.


#### Task 5 – Package before/after evidence tarball

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-ansible/module-17
tar -czf module-17-evidence.tgz \
  inventories/ playbooks/ \
  syntax-before.txt syntax-after.txt \
  inventory-miss.txt inventory-hit.txt module-fail-vvv.txt
ls -lh module-17-evidence.tgz | tee tarball.txt
test -s module-17-evidence.tgz
```

!!! example "Expected output"
    Tarball contains broken vs fixed syntax logs and inventory miss/hit proof.


### Validation steps

- [ ] Broken playbook fails `--syntax-check` with captured log
- [ ] Fixed playbook passes syntax-check
- [ ] Inventory without `app` group produces skip/no-host evidence
- [ ] Corrected inventory runs the task
- [ ] `-vvv` module failure log captured

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| YAML scanner error | Indentation under `tasks` | Align list items with two spaces consistently |
| `provided hosts list is empty` | Wrong group or limit | `ansible-inventory --graph`; fix group name |
| `sudo: a password is required` | Missing become password | `--ask-become-pass` or passwordless sudo |
| `couldn't resolve module` | Collection not installed | `ansible-galaxy collection install …` |
| Too much `-vvvv` noise | Log volume | Start `-v`, increase until module args visible |

### Challenge exercise

Add a `block`/`rescue` wrapper around the failing command task that writes a one-line incident note to `/tmp/ansible-rescue.log` on localhost when rescue triggers.

### Learning outcomes

- Repeatable syntax and inventory triage
- Verbosity skills for module-level failures
- Before/after artefacts suitable for post-incident review

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
rm -rf ~/rebash-ansible/module-17
```

## Validation

- [ ] All lab steps run under `~/rebash-ansible/module-17/`
- [ ] Before and after syntax logs differ as expected
- [ ] Inventory miss and hit demonstrated
- [ ] You can explain when to use `-vvv` vs `-vvvv`

## Code Walkthrough

The broken playbook uses misaligned `-` under `tasks` — YAML parsers fail before Ansible connects anywhere, which is why syntax-check is the first gate. The inventory miss play shows that a valid playbook can still change **zero** hosts if groups disagree — always graph inventory before production. The module failure play uses `ignore_errors: true` so the play continues while `-vvv` captures the exact command and return structure in `cmd_out`.

## Security Considerations

- Redact `-vvv` logs before sharing — they may include passwords passed as module args
- Do not disable host key checking permanently when debugging SSH — use jump hosts
- Avoid `--ask-vault-pass` on shared screens; use `--vault-password-file` with restrictive permissions
- Limit who can run verbose production plays; logs can expose internal topology
- Treat rescue blocks that mutate systems as audited changes

## Common Mistakes

!!! warning "Skipping syntax-check because 'it is just a one-line fix'"
    **Fix:** run `--syntax-check` every time; YAML errors are faster to fix locally.

!!! warning "Increasing verbosity without a hypothesis"
    **Fix:** know which layer failed (inventory vs SSH vs module) before `-vvvv`.

!!! warning "Using `--limit` with a typo in production"
    **Fix:** echo resolved hosts with `ansible-inventory --list --limit` before running.

## Best Practices

- Keep a team triage doc with command snippets (`syntax-check`, `ping`, inventory graph)
- Wire syntax-check into CI so broken YAML never merges
- Use `register` + `debug` with `verbosity: 2` for tricky tasks
- Snapshot failing `-vvv` output to the ticket system
- After fix, rerun with `--check` when modules support it

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `ERROR! Syntax Error` | YAML/Jinja | `--syntax-check`; fix indent; validate templates |
| `UNREACHABLE!` | SSH/network | Manual `ssh user@host`; check `ansible_host`, port, bastion |
| `Permission denied (publickey)` | Wrong key/user | `ansible_user`, `--private-key`, ssh-agent |
| `VARIABLE IS UNDEFINED` | Missing vars file | Trace precedence; `hostvars[inventory_hostname]` |
| Works locally, fails in AWX | Different inventory/credential | Compare template settings with CLI `-i` and `-e` |
| Hangs mid-play | Waiting for become password | `--ask-become-pass` or fix sudoers |

## Summary

Troubleshoot Ansible in layers: syntax, inventory, connectivity, variables, then modules. Capture before/after evidence when fixing incident playbooks. Verbosity `-vvv` is for understanding task execution — use it with a theory, not as a default.

## Interview Questions

**1. What is your first command when a playbook fails before running any task?**

??? success "Reveal answer"
    `ansible-playbook --syntax-check` (and `ansible-lint` in CI). YAML and Jinja errors fail locally without touching remote systems.

**2. How do you confirm a host is in the correct inventory group?**

??? success "Reveal answer"
    `ansible-inventory -i inventories/prod --graph` or `--host hostname` to inspect groups and vars resolved for that host.

**3. What does UNREACHABLE mean versus FAILED?**

??? success "Reveal answer"
    **UNREACHABLE** means Ansible could not connect (SSH/WinRM/network). **FAILED** means connection worked but the module/task returned failure — different fixes.

**4. When do you use -vvv?**

??? success "Reveal answer"
    When you need module arguments, connection details, and structured result JSON for a specific failing task — after syntax and inventory are ruled out.

**5. How can a playbook run but change nothing?**

??? success "Reveal answer"
    Wrong `-i`, empty group, `--limit` typo, or `--check` mode with tasks that skip changes. Always read `PLAY RECAP` and host counts.

**6. How do you debug undefined variables quickly?**

??? success "Reveal answer"
    Run with `-vvv`, use `ansible.builtin.debug: var=variable_name`, trace precedence (extra-vars > host_vars > group_vars > role defaults), confirm Vault files decrypt.

## Related Tutorials

- [Production Ansible Practices](production-ansible-practices.md)
- [Collections and Galaxy](ansible-collections-and-galaxy.md)
- [Ansible CI/CD Integration](ansible-ci-cd-integration.md)

## References

- [Ansible error handling](https://docs.ansible.com/ansible/latest/user_guide/playbooks_error_handling.html)
- [Ansible verbosity](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html#cmdoption-ansible-playbook-v)
- [Ansible inventory](https://docs.ansible.com/ansible/latest/inventory_guide/index.html)
- [ansible-lint](https://ansible.readthedocs.io/projects/lint/)
