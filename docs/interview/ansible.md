---
title: "Ansible Interview Preparation"
description: "31 curated Ansible interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: ansible
tags:
  - interview
  - ansible
comments: false
---

{% raw %}
# Ansible Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. What is Dry run in playbook?**

??? success "Reveal answer"
    **In short:** Dry run (`--check`) predicts changes without mutating hosts — pair it with `--diff` to see what would change.
    
    **Key points**
    - **Check mode** — modules that support it report *changed* vs *ok* without applying
    - **Not universal** — some modules lack check support; those may skip or lie
    - **Diff** — `--diff` shows file/template deltas you are about to ship
    - **CI habit** — run check on PRs; apply only from controlled AWX/Tower jobs
    
    **Try this**
    - `ansible-playbook site.yml --check --diff`
    - `ansible-playbook site.yml --limit web01 --check`
    
    **Trap**
    - Trusting check mode on custom modules that ignore it — false green, broken prod

**2. What is an Ansible Role, and how do you create it?**

??? success "Reveal answer"
    **In short:** A role is a reusable package of tasks, vars, handlers, and templates with a standard layout.
    
    **Key points**
    - **Layout** — `tasks/`, `handlers/`, `defaults/`, `vars/`, `templates/`, `files/`, `meta/`
    - **Create** — `ansible-galaxy role init nginx` (or Collection-aware workflows)
    - **Defaults vs vars** — defaults are overridable; vars are sticky
    - **Call it** — `roles:` or `include_role` / `import_role` from a play
    
    **Try this**
    - `ansible-galaxy role init webserver`
    - `tree roles/webserver`
    
    **Trap**
    - Hardcoding env-specific values in `vars/` — every consumer fights the role

**3. What are the ansible modules you have used?**

??? success "Reveal answer"
    **In short:** Name the modules you actually used in production — interviewers smell laundry lists.
    
    **Key points**
    - **Packages** — `apt` / `yum` / `dnf` / `package`
    - **Services** — `systemd` / `service`
    - **Files** — `copy`, `template`, `file`, `lineinfile`
    - **Cloud/API** — `amazon.aws.*`, `azure.azcollection.*`, `kubernetes.core.k8s` as used
    - **Ops** — `uri`, `command`/`shell` only when no module exists
    
    **Try this**
    - `ansible-doc apt | head`
    - `ansible-doc -l | rg systemd`
    
    **Trap**
    - Defaulting to `shell` for everything — non-idempotent and hard to audit

**4. What is the difference between import and include in Ansible?**

??? success "Reveal answer"
    **In short:** `import_*` is static (parsed at start); `include_*` is dynamic (at runtime) — loops and conditionals behave differently.
    
    **Key points**
    - **import_tasks / import_playbook / import_role** — expanded when the playbook loads
    - **include_tasks / include_role** — decided during execution; better with loops/`when`
    - **Tags** — imports inherit tags more predictably; includes need care
    - **Errors** — missing imported files fail early; includes fail when reached
    
    **Try this**
    - `ansible-playbook site.yml --list-tasks` — see static expansion
    
    **Trap**
    - Looping `import_tasks` expecting dynamic behaviour — it will not do what you think

**5. What is Task section in Ansible playbook?**

??? success "Reveal answer"
    **In short:** The `tasks:` section is the ordered list of modules Ansible runs on the selected hosts.
    
    **Key points**
    - **Unit of work** — each task has a name, module, and arguments
    - **Handlers** — notified by `notify:` after a real change
    - **Control** — `when`, loops, `block`/`rescue`/`always`, `ignore_errors`
    - **Idempotency** — prefer modules that converge rather than fire-and-forget scripts
    
    **Trap**
    - Untitled tasks — unreadable logs and painful failed-task triage

**6. What is Target section in Ansible playbook?**

??? success "Reveal answer"
    **In short:** Targets are the hosts/groups a play runs against — set with `hosts:` plus inventory and limits.
    
    **Key points**
    - **hosts:** — group, pattern (`web:&prod`), or `all`
    - **Inventory** — static INI/YAML or dynamic (cloud/CMDB)
    - **Limit** — `--limit` narrows blast radius without editing the playbook
    - **Connection** — `ansible_host`, `ansible_user`, `ansible_connection` per host
    
    **Try this**
    - `ansible-inventory --list`
    - `ansible-playbook site.yml --limit 'web:&eu'`
    
    **Trap**
    - `hosts: all` against a shared inventory in prod — classic blast-radius incident

**7. What is Ansible Tower / AWX?**

??? success "Reveal answer"
    **In short:** AWX (upstream) / Ansible Automation Platform (Tower lineage) add RBAC, schedules, credentials, and audit on top of Ansible.
    
    **Key points**
    - **Why** — central jobs, approvals, credential vaulting, logging for compliance
    - **Inventories & creds** — stored centrally; playbooks pull at runtime
    - **Surveys / workflows** — gated multi-playbook pipelines
    - **Execution environments** — containerised Ansible + collections for reproducibility
    
    **Trap**
    - Embedding secrets in job templates instead of credential objects — they leak in exports

**8. What is the register directive in Ansible?**

??? success "Reveal answer"
    **In short:** `register:` captures a task’s result into a variable for later `when`, debug, or loops.
    
    **Key points**
    - **Fields** — `.rc`, `.stdout`, `.stderr`, `.changed`, `.failed`
    - **Common pattern** — run a check, act only if needed
    - **failed_when / changed_when** — shape what 'failure' and 'changed' mean
    - **Keep it small** — huge stdout in registers bloats memory and logs
    
    **Try this**
    - `ansible localhost -m command -a 'uname -a' -vv` — inspect result shape
    
    **Trap**
    - Using `register` after `async` without `poll` — you get a job id, not the result

**9. What is the uri module in Ansible?**

??? success "Reveal answer"
    **In short:** `uri` is Ansible’s HTTP client module — health checks, webhooks, and API calls without leaving the playbook.
    
    **Key points**
    - **Methods** — GET/POST/PUT/DELETE with body, headers, status codes
    - **Auth** — basic, bearer tokens from Vault/creds (never hardcode)
    - **Validation** — `status_code`, `return_content`, JSON body asserts
    - **Idempotency** — design API calls carefully; POST is often not safe to repeat
    
    **Try this**
    - `ansible localhost -m uri -a 'url=https://example.com return_content=yes'`
    
    **Trap**
    - Printing full response bodies that contain tokens — secrets in job logs

**10. What is a dynamic inventory in Ansible?**

??? success "Reveal answer"
    **In short:** Dynamic inventory builds the host list at runtime from cloud APIs, CMDB, or scripts — no stale static files.
    
    **Key points**
    - **Sources** — AWS/Azure/GCP plugins, Kubernetes, custom scripts
    - **Groups** — from tags, labels, regions, or business metadata
    - **Refresh** — inventory reflects create/destroy without manual edits
    - **Cache** — short TTL cache to avoid API rate limits in CI
    
    **Try this**
    - `ansible-inventory -i aws_ec2.yml --graph`
    - `ansible-doc -t inventory amazon.aws.aws_ec2`
    
    **Trap**
    - Caching inventory forever — you target hosts that no longer exist (or miss new ones)

## Scenarios and troubleshooting

**11. Write an Ansible playbook for a production-grade web server setup.**

??? success "Reveal answer"
    **In short:** Production web setup = packages + hardened config + TLS + service + firewall, all idempotent via roles.
    
    **Key points**
    - **Baseline** — update cache, install nginx/httpd, create non-root deploy user
    - **Config as templates** — Jinja with variables per environment
    - **Handlers** — reload/restart only on real config change
    - **Security** — firewall ports, TLS certs from Vault/secrets, disable default sites
    - **Verify** — `uri` health check and `systemd` state asserts
    
    **Try this**
    - `ansible-playbook -i inv web.yml --tags nginx --check --diff`
    
    **Trap**
    - Restarting the service on every run — needless blips and flapping monitors

**12. Write a playbook to deploy an Nginx server and ensure the service is started and enabled on boot. How would you manage secrets in Ansible?**

??? success "Reveal answer"
    **In short:** Idempotent nginx role plus secrets via Ansible Vault (or external secret store) — never plaintext in Git.
    
    **Key points**
    - **Service** — `state=started`, `enabled=true` on `systemd`
    - **Config** — `template` + `notify: reload nginx`
    - **Secrets** — Vault-encrypted vars, or pull from HashiCorp Vault / cloud secret managers
    - **CI** — decrypt with a CI-injected Vault password / cloud IAM, not a committed key
    
    **Try this**
    - `ansible-vault encrypt group_vars/prod/vault.yml`
    - `ansible-playbook site.yml --ask-vault-pass`
    
    **Trap**
    - Committing `vault.yml` encrypted with a password stored in the same repo

**13. What is max_fail_percentage in Ansible?**

??? success "Reveal answer"
    **In short:** `max_fail_percentage` aborts the play early if too many hosts in a batch fail — protects rolling updates.
    
    **Key points**
    - **Meaning** — maximum allowed failure percentage before Ansible stops the play
    - **With serial** — combine with `serial:` for controlled rollouts
    - **any_errors_fatal** — stricter: one failure stops everything
    - **Use when** — large fleets where continuing after mass failure is pointless
    
    **Trap**
    - Setting it to 100% 'to be safe' — you just disabled the safety brake

## Practice questions

**14. How do you use Ansible Vault to manage secrets, and how does it integrate with a CI/CD pipeline?**

??? success "Reveal answer"
    **In short:** Vault encrypts sensitive vars at rest; CI unlocks them with a short-lived secret, never a Git-stored password.
    
    **Key points**
    - **Encrypt** — files or strings (`ansible-vault encrypt_string`)
    - **Runtime** — `--vault-password-file` or `ANSIBLE_VAULT_PASSWORD_FILE`
    - **CI/CD** — inject password from pipeline secret store; mask logs
    - **Better at scale** — look up secrets from HashiCorp Vault / cloud KMS at run time
    
    **Try this**
    - `ansible-vault view group_vars/prod/vault.yml`
    - `ansible-vault encrypt_string 's3cret' --name 'db_password'`
    
    **Trap**
    - Echoing decrypted vars in `debug:` tasks — they land in AWX/CI logs forever

**15. What challenges have you faced with configuration management tools?**

??? success "Reveal answer"
    **In short:** Real pain is drift, slow SSH fan-out, and playbooks that are not idempotent — not the YAML syntax.
    
    **Key points**
    - **Drift** — manual hotfixes fight the next apply
    - **Scale** — forks, persistent connections, and Execution Environments matter
    - **Windows / network gear** — different transports and modules
    - **Secrets & inventory** — stale inventories and leaked vault passwords
    
    **Trap**
    - Fixing prod with SSH then never updating the playbook — Ansible becomes fiction

**16. What do you mean by Roles in Ansible?**

??? success "Reveal answer"
    **In short:** Roles package reusable automation — the unit of sharing across playbooks and teams.
    
    **Key points**
    - **Structure** — standard directories so anyone can navigate
    - **Defaults** — safe, overridable knobs for consumers
    - **Dependencies** — `meta/main.yml` pulls other roles
    - **Collections** — modern distribution path on Galaxy/Automation Hub
    
    **Trap**
    - One mega-role that installs the universe — untestable and feared

**17. If you have custom plugins that multiple roles depends on, how do you manage them in the context of Ansible Roles Management?**

??? success "Reveal answer"
    **In short:** Ship custom plugins via a Collection (or a shared `plugins/` path on `ANSIBLE_ROLES_PATH`) so every role resolves them the same way.
    
    **Key points**
    - **Collections** — package plugins + roles + modules together
    - **plugin paths** — document `ansible.cfg` `collections_paths` / `roles_path`
    - **Version pin** — `requirements.yml` with Collection versions in CI
    - **Avoid** — copying plugin files into each role
    
    **Try this**
    - `ansible-galaxy collection install -r requirements.yml`
    
    **Trap**
    - Relying on a plugin that only exists on one engineer’s laptop

**18. How do you write an Ansible playbook, and what client requirements do you consider?**

??? success "Reveal answer"
    **In short:** Write plays against inventory + variables; gather OS, reachability, privilege, and change-window constraints first.
    
    **Key points**
    - **Client needs** — OS family, package manager, reboot policy, compliance
    - **Access** — SSH user, become method, jump hosts, network paths
    - **Idempotency** — declare desired state, not a shell script diary
    - **Safety** — `--check`, limits, serial batches, change tickets
    
    **Trap**
    - Assuming passwordless sudo everywhere — first prod run dies on become

**19. If you have two different VMs, how will you modify your playbook for diff requirement?**

??? success "Reveal answer"
    **In short:** One playbook, different vars/groups — not forked playbooks per VM.
    
    **Key points**
    - **Inventory groups** — `web_a` vs `web_b` with group_vars
    - **host_vars** — true one-off differences only
    - **when:** — branch tasks by `ansible_facts` or custom vars
    - **Prefer roles + defaults** — override per environment
    
    **Trap**
    - Copy-paste playbook_v2.yml for the second VM — permanent divergence

**20. In ansible if you need to execute something as root user how do you that?**

??? success "Reveal answer"
    **In short:** Use `become: true` (privilege escalation) — usually sudo — scoped to the play or task that needs root.
    
    **Key points**
    - **become / become_user** — escalate only where required
    - **become_method** — sudo, su, enable (network), etc.
    - **Least privilege** — don’t run the whole play as root if only one task needs it
    - **Inventory** — `ansible_become=true` per host when policy demands
    
    **Try this**
    - `ansible all -b -m ping`
    - `ansible-playbook site.yml --ask-become-pass`
    
    **Trap**
    - Hardcoding `sudo` inside `shell:` — skips Ansible’s become auditing and fails oddly

**21. Where do we use conditionals in Playbooks?**

??? success "Reveal answer"
    **In short:** Conditionals (`when:`) skip tasks based on facts, vars, or registered results — keep them readable.
    
    **Key points**
    - **Facts** — `ansible_os_family == 'Debian'`
    - **Registers** — act only if a check failed or a package is missing
    - **Blocks** — shared `when` on a group of tasks
    - **Clarity** — extract complex expressions into named vars
    
    **Trap**
    - Double negatives and nested Jinga in `when` — nobody can reason about the play

**22. What do you mean by Ad-Hoc commands in Ansible?**

??? success "Reveal answer"
    **In short:** Ad-hoc commands are one-shot module runs from the CLI — great for triage, not for lasting config.
    
    **Key points**
    - **Form** — `ansible <pattern> -m <module> -a '<args>'`
    - **Use for** — ping, quick package install, emergency restart
    - **Not for** — anything you need to reproduce next week → write a playbook
    - **Same engine** — still uses inventory, become, and forks
    
    **Try this**
    - `ansible web -m ping`
    - `ansible web -b -m systemd -a 'name=nginx state=restarted'`
    
    **Trap**
    - Fixing an outage only with ad-hoc and never capturing it — next on-call repeats the panic

**23. Why are we using loops concept in Ansible?**

??? success "Reveal answer"
    **In short:** Loops remove copy-paste — one task, many items (`loop:` / `with_items`).
    
    **Key points**
    - **Packages/users/files** — natural list processing
    - **loop_control** — label output for readable logs
    - **dict loops** — `dict2items` for maps of config
    - **Prefer modules that accept lists** when available (fewer tasks)
    
    **Trap**
    - Looping `shell` with `ignore_errors` — hides partial failure across 50 hosts

**24. Write a playbook to install apache in VM?**

??? success "Reveal answer"
    **In short:** Tiny idempotent play: install httpd/apache2 by OS family, then start and enable the service.
    
    **Key points**
    - **package module** — portable across apt/yum when possible
    - **systemd** — `state=started`, `enabled=true`
    - **handlers** — restart only if config templates change (when you add them)
    - **Validate** — curl localhost / check `systemctl is-active`
    
    **Try this**
    - `ansible-playbook apache.yml --check --diff`
    
    **Trap**
    - Using `command: apt-get install` — always reports changed, breaks check mode

**25. What does idempotent mean in Ansible?**

??? success "Reveal answer"
    **In short:** Idempotent means run it twice — second run makes zero changes if the system already matches desired state.
    
    **Key points**
    - **Modules** — declare end state (`package: state=present`), not steps
    - **changed** — only when something actually mutated
    - **Why it matters** — safe re-runs, CI check mode, calm rollouts
    - **Anti-pattern** — unguarded `shell` that always mutates
    
    **Try this**
    - `ansible-playbook site.yml` twice — second run should be all ok/green
    
    **Trap**
    - Claiming a playbook is idempotent while every task shows `changed=true`

**26. How does Ansible work?**

??? success "Reveal answer"
    **In short:** Control node pushes modules over SSH (or WinRM); agents are optional — push model, SSH + Python on Linux targets.
    
    **Key points**
    - **Inventory** — who to manage
    - **Playbook** — desired state as YAML
    - **Modules** — executed on targets (copied then run)
    - **Plugins** — connection, callback, inventory, lookup extend the engine
    
    **Trap**
    - Assuming a long-running agent like Puppet — Ansible is typically agentless push

**27. Describe the structure and advantage of using an Ansible role to manage a three-tier web application. what do you mean by three-tier web application?**

??? success "Reveal answer"
    **In short:** Three-tier = web + app + data; roles map cleanly to each tier so teams can reuse and test independently.
    
    **Key points**
    - **Tiers** — presentation (web), business logic (app), persistence (DB)
    - **Roles** — `roles/web`, `roles/app`, `roles/db` with clear interfaces
    - **Advantage** — swap nginx/apache or MySQL/Postgres without rewriting everything
    - **Inventory** — groups per tier; plays target each group
    
    **Trap**
    - One role that configures all three tiers — any change risks the database

**28. Ansible playbook times out on one host out of twenty. What do you check?**

??? success "Reveal answer"
    **In short:** One slow host is usually SSH, become, DNS, disk, or a stuck package lock — not 'Ansible is broken'.
    
    **Key points**
    - **Connectivity** — `ansible host -m ping -vvv`; check jump hosts and DNS
    - **Timeouts** — `timeout` / `ansible_ssh_timeout`; package manager waits
    - **Locks** — `apt`/`yum` lock held by unattended-upgrades
    - **Facts gathering** — huge facts on constrained VMs; try `gathering: smart`
    - **Serial noise** — confirm it’s not waiting on `serial:` batch mates
    
    **Try this**
    - `ansible badhost -m ping -vvv`
    - `ansible badhost -b -m shell -a 'ps aux | rg apt'`
    
    **Trap**
    - Raising global timeout to 60 minutes — you hide the real hang and burn the change window

**29. How can you install a patch through ansible in more than 20 servers?**

??? success "Reveal answer"
    **In short:** Patch with a rolling play: serial batches, health checks, and a package/update role — not a weekend of SSH.
    
    **Key points**
    - **serial / max_fail_percentage** — controlled blast radius
    - **Modules** — `apt: upgrade=dist` or vendor patch modules; reboot with `reboot` module
    - **Health gates** — uri/monitoring check before next batch
    - **Inventory** — target the 20+ via group pattern; exclude canaries if needed
    
    **Try this**
    - `ansible-playbook patch.yml --serial 20% --max-fail-percentage 10`
    
    **Trap**
    - Patching all 20 in one fork storm with forced reboot — correlated outage

**30. Write a sample playbook by mentioning variables instead of hard coding?**

??? success "Reveal answer"
    **In short:** Put values in `group_vars` / `host_vars` / role defaults — reference with `{{ var }}` in tasks and templates.
    
    **Key points**
    - **Precedence** — know extras > role vars > group_vars (simplified: don’t fight it)
    - **Vault** — encrypt sensitive vars
    - **Example** — `package: name={{ web_package }} state=present`
    - **Extra vars** — `-e` for rare overrides, not everyday config
    
    **Trap**
    - Mixing hardcoded names and vars for the same setting — silent inconsistency

**31. Write a sample playbook to install any package?**

??? success "Reveal answer"
    **In short:** One task, portable package module (or `apt`/`yum` when you must), then verify.
    
    **Key points**
    - **Task** — `ansible.builtin.package: name=httpd state=present` (or apache2 on Debian)
    - **Become** — package installs need privilege
    - **Idempotent** — second run is a no-op
    - **Better** — wrap in a role with OS-family vars for package names
    
    **Try this**
    - `ansible web -b -m package -a 'name=nginx state=present'`
    
    **Trap**
    - Hardcoding `apt-get` on a fleet that includes RHEL — half the run fails

## Related
- Course: [Ansible](../ansible/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
