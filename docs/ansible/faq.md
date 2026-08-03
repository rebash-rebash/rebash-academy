---
title: FAQ
description: "Frequently asked questions about the Ansible course."
technology_id: ansible
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-03"
category: ansible
tags:
  - ansible
---

# Ansible — FAQ

## Who is this course for?

Engineers who need production-ready **Ansible** skills for cloud, DevOps, platform, and SRE work — from first playbooks through AWX/AAP and CI pipelines.

## ansible-core vs ansible — which should I install?

Install **ansible-core** when you want the minimal engine and explicitly add collections via `ansible-galaxy`. Install the **`ansible` PyPI package** (community distribution) when you want a bundled set of collections for a quicker start. Labs assume **ansible-core 2.18+** unless noted. See [Ansible packaging](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).

```bash
pip install 'ansible-core>=2.18,<2.19'
ansible --version
```

## Do I need remote servers for labs?

Most early modules use **localhost** (`ansible_connection: local`) so you can complete labs on a practice VM or laptop without cloud spend. Modules that target SSH hosts clearly state when a second VM is helpful. Kubernetes modules can validate offline with `--dry-run=client` when no cluster is available.

## What Vault password policy should I use in labs?

Use a **dedicated lab password** — never reuse production Vault passwords. For local practice:

```bash
ansible-vault create group_vars/lab/vault.yml
ansible-playbook site.yml --ask-vault-pass
```

In CI, inject `ANSIBLE_VAULT_PASSWORD` from your platform’s secret store; do not commit `.vault_pass` files. Rotate lab passwords if you share screen recordings or tarball evidence publicly.

## Where do Ansible Galaxy and collections fit?

**Ansible Galaxy** hosts roles and collections. Declare dependencies in `collections/requirements.yml` and install with:

```bash
ansible-galaxy collection install -r collections/requirements.yml
```

Prefer **collections** (for example `kubernetes.core`) over copying legacy role code. Pin versions for reproducible CI and Execution Environments.

## AWX vs Ansible Automation Platform — which is this course about?

Both share the same object model (projects, inventories, job templates, credentials). **AWX** is the upstream open-source controller — ideal for labs and self-managed platforms. **Ansible Automation Platform (AAP)** is Red Hat’s supported enterprise product. Module 15 teaches concepts with offline topology stubs; a full AWX install is optional and resource-heavy. Docs: [AWX](https://ansible.readthedocs.io/projects/awx/en/latest/) · [Red Hat AAP](https://www.redhat.com/en/technologies/management/ansible).

## How do Jinja2 and GitHub Actions expressions work in MkDocs tutorials?

Ansible playbooks and GitHub workflow files contain Jinja double-brace expressions and Actions dollar-brace-brace expressions that confuse MkDocs macros. Tutorial **documentation** wraps those fences in raw Jinja blocks so the site builds. Files you create on disk for labs use normal syntax without MkDocs wrapping.

## Where are the tutorials?

Tutorials live inside each **module** in the sidebar — open [Course overview](index.md) or follow the [Learning roadmap](roadmap.md).

## How do labs and projects fit in?

Complete module tutorials first, then use **Labs**, **Quizzes**, and **Projects** for extra practice and portfolio work.

## What is the source of truth for Ansible behaviour?

Official documentation:

- https://docs.ansible.com/
- https://galaxy.ansible.com/
