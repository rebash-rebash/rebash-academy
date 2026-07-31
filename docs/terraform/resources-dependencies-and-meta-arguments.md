---
title: "Resources, Dependencies, and Meta-Arguments"
description: "Model Terraform resources, implicit and explicit dependencies, and meta-arguments — count, for_each, lifecycle, and depends_on."
difficulty: intermediate
estimated_time: "45–60 min"
technology: terraform
category: terraform
module: "Module 6 · Resources"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - resources
  - dependencies
prerequisites:
  - terraform/providers-and-the-terraform-plugin-model
next:
  - terraform/variables-locals-and-outputs
related:
  - terraform/terraform-state-fundamentals
  - terraform/functions-templates-and-dynamic-blocks
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - resources
  - meta-arguments
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Resources, Dependencies, and Meta-Arguments

## Overview



Declare managed resources, understand the dependency graph, and use `count`, `for_each`, `lifecycle`, and `depends_on` correctly.

A **resource** is something Terraform creates and updates through a provider. Addresses look like `local_file.readme`. Terraform builds a **graph** from references between resources; **meta-arguments** change how many instances exist and how replace/destroy behaves.

This is a core tutorial in **Module 6 · Resources** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Providers and the Terraform Plugin Model](providers-and-the-terraform-plugin-model.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Write a resource block and read its address in state  
- [ ] Explain implicit vs explicit (`depends_on`) dependencies  
- [ ] Choose `for_each` over `count` for named instances  
- [ ] Apply a `lifecycle` rule intentionally



## Architecture



This topic’s control points and relationships are shown below.

![Terraform resources](../assets/excalidraw/terraform-resources.svg)



## Theory



### What it is

```hcl
resource "local_file" "readme" {
  filename = "${path.module}/README.txt"
  content  = "managed by Terraform\n"
}
```

Terraform tracks this as `local_file.readme` in state. When another resource references `local_file.readme.filename`, Terraform gains an **implicit dependency** and creates the file first. Use **`depends_on`** only when there is a real ordering need that references cannot express (for example, an API side effect with no attribute link).

**Meta-arguments** (available on most resources):

| Meta-argument | Purpose |
|---------------|---------|
| `count` | Create N copies; instances are `resource.name[0]` |
| `for_each` | Create one instance per map/set key; `resource.name["key"]` |
| `depends_on` | Explicit edges in the graph |
| `lifecycle` | `create_before_destroy`, `prevent_destroy`, `ignore_changes`, … |
| `provider` | Select a non-default provider alias |

### Why it matters

Wrong dependencies cause apply-time races (subnet before VPC, DNS before load balancer). Prefer **implicit** links via attribute references — they document intent. Prefer **`for_each`** with stable keys (environment names, availability zones) so removing one item does not reshuffle indexes the way `count` often does. Lifecycle rules protect production databases from accidental destroy — and can also hide drift if you overuse `ignore_changes`.

### How it works

1. Terraform evaluates expressions and builds a directed graph of resources.
2. Walk order respects dependencies; independent resources may create in parallel.
3. `count` / `for_each` expand one block into multiple instances in state.
4. On update, providers may **update in place** or **force replace** (destroy + create) depending on the attribute.
5. `lifecycle` tweaks replace/destroy behaviour for that resource.

`for_each = toset(["dev", "stage"])` expands to `local_file.env["dev"]` and `local_file.env["stage"]` — stable keys beat `count` indexes when membership changes.

### Key concepts and comparisons

| Pattern | Prefer when |
|---------|-------------|
| Implicit reference | Attribute of A is needed by B |
| `depends_on` | Ordering without a referenceable attribute |
| `count` | Simple N identical copies; indexes OK |
| `for_each` | Named, stable instance keys |
| `create_before_destroy` | Zero-downtime-style replace |
| `prevent_destroy` | Block accidental destroy plans |
| `ignore_changes` | Skip listed attributes (use sparingly) |

### Common pitfalls

- Using `count` with a list that reorders — instance indexes shift and force replacements.
- Sprinkling `depends_on` everywhere instead of wiring attributes.
- Setting `ignore_changes = all` to “fix” drift — you stop managing the resource.
- Assuming `prevent_destroy` blocks `terraform destroy` of the whole root without care — it blocks plans that would destroy that resource; design env teardown deliberately.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-06 && cd ~/rebash-terraform/module-06
```

**Focus:** Explore implicit dependencies, count, and depends_on

### Step 1 – Create chained resources

```bash
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
    null  = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
resource "local_file" "base" {
  filename = "${path.module}/base.txt"
  content  = "base
"
}
resource "local_file" "child" {
  count    = 2
  filename = "${path.module}/child-${count.index}.txt"
  content  = "depends on ${local_file.base.filename}
"
}
resource "null_resource" "after" {
  depends_on = [local_file.child]
  triggers   = { stamp = timestamp() }
}
EOF
terraform init
```

### Step 2 – Apply and inspect graph order

```bash
terraform apply -auto-approve
terraform state list
ls -1 child-*.txt base.txt
terraform graph | head -n 30
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-terraform/module-06/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Resources, Dependencies, and Meta-Arguments** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.



## Security Considerations



- Treat credentials and tokens for terraform as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces



## Common Mistakes



!!! warning "Using `count` with a list that reorders — instance indexes shift and force replacements."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Sprinkling `depends_on` everywhere instead of wiring attributes."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Resources, Dependencies, and Meta-Arguments changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible



## Troubleshooting



| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |



## Summary



**Resources, Dependencies, and Meta-Arguments** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. How does Terraform infer dependencies between resources?
2. When do you need explicit `depends_on`?
3. What is the difference between `count` and `for_each`?
4. What operational risk does `count` index shifting introduce?
5. What does `lifecycle { prevent_destroy = true }` protect against?

!!! tip "Sample answer — question 2"
    Implicit dependencies come from references. `depends_on` is for hidden ordering (for example, API readiness) that references cannot express.

!!! tip "Sample answer — question 4"
    Removing an element from a `count` list can force replacement of later indexes. `for_each` with stable keys usually produces safer updates.



## Related Tutorials



- [Course overview](index.md)
- [Variables, Locals, and Outputs](variables-locals-and-outputs.md)



## References



- [Resources](https://developer.hashicorp.com/terraform/language/resources)  
- [Meta-arguments](https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on)
