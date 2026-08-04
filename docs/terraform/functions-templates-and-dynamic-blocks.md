---
title: "Functions, Templates, and Dynamic Blocks"
description: "Use Terraform built-in functions, templatefile, for expressions, conditionals, and dynamic blocks to generate flexible infrastructure configuration."
difficulty: intermediate
estimated_time: "65–75 min"
technology: terraform
category: terraform
module: "Module 10 · Expressions & Functions"
learning_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - hcl
  - templatefile
prerequisites:
  - terraform/registry-modules-and-composition
  - terraform/hcl-fundamentals-blocks-arguments-and-expressions
next:
  - terraform/data-sources-and-existing-infrastructure
related:
  - terraform/resources-dependencies-and-meta-arguments
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - functions
  - templatefile
  - dynamic-blocks
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# Functions, Templates, and Dynamic Blocks

## Overview

Infrastructure requirements rarely fit a static block of HCL. **Functions** transform data; **`templatefile`** renders config from templates; **`for` expressions** build lists and maps; **conditionals** choose values; **dynamic blocks** repeat nested blocks without copy-paste.

This tutorial covers **built-in functions**, **`templatefile`**, **conditional expressions**, **`for` expressions**, and **dynamic blocks** — the expression toolkit for production modules. The lab under `~/rebash-terraform/module-10` applies a **Docker** stack with templated env files, merged labels, and dynamic mount blocks — real containers you prove with `docker inspect`.

This is **Tutorial 12** in **Module 10: Expressions & Functions** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series.

## Prerequisites

- [Registry Modules and Composition](registry-modules-and-composition.md)
- [HCL Fundamentals](hcl-fundamentals-blocks-arguments-and-expressions.md)
- Terraform CLI ≥ 1.5

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Use string, collection, and encoding functions (`join`, `merge`, `jsonencode`, `try`)
- [ ] Render files with `templatefile` and pass variables into templates
- [ ] Build maps and lists with `for` expressions and conditional (`? :`) logic
- [ ] Author `dynamic` blocks driven by `for_each`
- [ ] Choose between static blocks, `for_each` on resources, and dynamic blocks

## Architecture

Input variables and locals feed function pipelines; templates render artefacts; dynamic blocks expand nested configuration from collections.

![Terraform expressions and functions](../assets/excalidraw/terraform-expressions.svg)

## Theory

### What it is

**Functions** — HCL calls like `upper("dev")`, `merge(local.base_tags, var.extra_tags)`, `try(var.optional, "default")`.

**templatefile** — renders a template file with `${variable}` placeholders:

```hcl
locals {
  rendered = templatefile("${path.module}/templates/app.env.tftpl", {
    service_name = var.service_name
    port         = var.port
  })
}
```

**Conditional expressions:**

```hcl
instance_count = var.environment == "prod" ? 3 : 1
```

**For expressions:**

```hcl
# List comprehension
enabled_services = [for s in var.services : s.name if s.enabled]

# Map comprehension
name_by_id = { for s in var.services : s.id => s.name }
```

**Dynamic blocks** — generate repeated nested blocks:

```hcl
dynamic "ingress" {
  for_each = var.ingress_rules
  content {
    from_port   = ingress.value.port
    to_port     = ingress.value.port
    protocol    = "tcp"
    cidr_blocks = ingress.value.cidrs
  }
}
```

The iterator label defaults to the block type name (`ingress` here); use **`iterator`** to rename.

### Why it matters

Functions keep modules DRY — one tag map merged everywhere. Templates separate **config file shape** from Terraform logic — the same pattern as Ansible Jinja2, but evaluated at plan time. Dynamic blocks model **variable-length nested rules** (security group rules, load balancer listeners) without generating invalid zero-block resources.

### How it works

1. Terraform evaluates expressions during **plan** (pure functions — no side effects).
2. `templatefile` reads disk at plan time; changing template triggers plan diff.
3. `for` expressions produce typed collections matching context.
4. `dynamic` blocks expand to zero-or-more nested blocks before provider schema validation.
5. Provider APIs define which nested blocks support `dynamic`.

| Need | Tool |
|------|------|
| Repeat whole resource | `count` or `for_each` on resource |
| Repeat nested block | `dynamic` block |
| Transform list → map | `for` expression with `{ for ... }` |
| Optional attribute | `try()` or conditional |

### Key concepts and comparisons

| Approach | Prefer when |
|----------|-------------|
| `for_each` on resource | Each instance is a full resource with own lifecycle |
| `dynamic` block | Variable nested rules inside one resource |
| `templatefile` | Rendered config files (systemd, env files, cloud-init) |
| Inline heredoc in HCL | Tiny one-line snippets only |

### Common pitfalls

- **`templatefile` path wrong** — relative to module; use `path.module`.
- **Dynamic block iterator typo** — reference `ingress.value` not `for_each.value`.
- **Empty dynamic for_each** — valid — zero blocks; ensure provider accepts empty.
- **Sensitive values in templates** — may land in state via rendered file resource.
- **Over-nesting functions** — extract to `locals` for readability.

## Hands-on Lab

### Objective

Render a service env file with **`templatefile`**, build tag maps with **`merge`** and **`for` expressions**, apply a **Docker** container with dynamic mount blocks, and prove labels and mounts with `docker inspect` under `~/rebash-terraform/module-10`.

### Prerequisites

- Terraform CLI ≥ 1.5
- Docker Engine running (`docker info` succeeds)
- Completed Module 9 labs

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-terraform/module-10/{templates,config} && cd ~/rebash-terraform/module-10
```

Runtime: local Docker Engine.

### Real-world scenario

Platform engineering generates per-service **environment files** from a template, merges standard and team tags onto containers, and mounts variable-length config volumes with **dynamic blocks** — the same expression patterns used in AWS security-group modules and Azure NSG rules before apply.

### Step-by-step tasks

#### Task 1 – templatefile, merge/for expressions, and Docker container

Create `templates/service.env.tftpl`:

```text title="service.env.tftpl"
SERVICE_NAME=${service_name}
ENVIRONMENT=${environment}
PORT=${port}
OWNER=${owner}
```

Create `versions.tf`:

```hcl title="versions.tf"
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}
```

Create `providers.tf`:

```hcl title="providers.tf"
provider "docker" {}
```

Create `variables.tf`:

```hcl title="variables.tf"
variable "service_name" {
  type    = string
  default = "billing"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "port" {
  type    = number
  default = 8080
}

variable "owner" {
  type    = string
  default = "platform-team"
}

variable "extra_tags" {
  type    = map(string)
  default = { cost_centre = "CC-100" }
}

variable "config_mounts" {
  type = list(object({
    source = string
    target = string
  }))
  default = [
    { source = "config/app.conf", target = "/etc/app/app.conf" },
    { source = "config/logging.conf", target = "/etc/app/logging.conf" },
  ]
}
```

Create `locals.tf`:

```hcl title="locals.tf"
locals {
  base_tags = {
    managed_by  = "terraform"
    environment = var.environment
  }

  merged_tags = merge(local.base_tags, var.extra_tags, {
    service = var.service_name
  })

  rendered_env = templatefile("${path.module}/templates/service.env.tftpl", {
    service_name = var.service_name
    environment  = var.environment
    port         = var.port
    owner        = var.owner
  })

  tag_lines = [for k, v in local.merged_tags : "${k}=${v}"]
}
```

Create `config/app.conf`:

```text title="app.conf"
log_level=info
```

Create `config/logging.conf`:

```text title="logging.conf"
format=json
```

Create `main.tf`:

```hcl title="main.tf"
resource "local_file" "service_env" {
  filename = "${path.module}/rendered/service.env"
  content  = local.rendered_env
}

resource "docker_image" "service" {
  name         = "nginx:1.27-alpine"
  keep_locally = true
}

resource "docker_container" "service" {
  name  = "${var.service_name}-${var.environment}"
  image = docker_image.service.image_id

  labels = local.merged_tags

  dynamic "mounts" {
    for_each = var.config_mounts
    content {
      type   = "bind"
      source = abspath("${path.module}/${mounts.value.source}")
      target = mounts.value.target
      read_only = true
    }
  }

  ports {
    internal = 80
    external = 0
  }
}
```

Create `outputs.tf`:

```hcl title="outputs.tf"
output "tag_lines" {
  value = local.tag_lines
}

output "container_name" {
  value = docker_container.service.name
}

output "mount_count" {
  value = length(var.config_mounts)
}
```

Run:

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-terraform/module-10
terraform init
terraform apply -auto-approve
test -f rendered/service.env
grep -q 'SERVICE_NAME=billing' rendered/service.env
docker inspect billing-dev --format '{{json .Config.Labels}}' | tee container-labels.json
grep -q 'cost_centre' container-labels.json
docker inspect billing-dev --format '{{len .Mounts}}' | tee mount-count.txt
test "$(cat mount-count.txt)" -ge 2
echo "task1 OK" | tee task1-ok.txt
```
{% endraw %}

!!! example "Expected output"
    Container running with merged labels and two bind mounts.


#### Task 2 – Conditional and for expression overrides

Create `terraform.tfvars`:

```hcl title="terraform.tfvars"
environment  = "prod"
port         = 443
extra_tags   = { cost_centre = "CC-200", tier = "critical" }
```

Create `locals_override.tf`:

```hcl title="locals_override.tf"
locals {
  replica_hint = var.environment == "prod" ? "multi-az" : "single-instance"
  critical_keys = [for k, v in local.merged_tags : k if v == "critical"]
}
```

Append to `outputs.tf`:

```hcl
output "replica_hint" {
  value = local.replica_hint
}

output "critical_keys" {
  value = local.critical_keys
}
```

Run:

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-terraform/module-10
terraform apply -auto-approve
terraform output -raw replica_hint | tee replica-hint.txt
test "$(cat replica-hint.txt)" = "multi-az"
docker ps --filter "name=billing-prod" --format '{{.Names}}' | tee prod-container.txt
grep -q 'billing-prod' prod-container.txt
terraform output -json critical_keys | grep -q tier
echo "task2 OK" | tee task2-ok.txt
```
{% endraw %}

!!! example "Expected output"
    `replica_hint` is `multi-az`; new `billing-prod` container is running.


#### Task 3 – Extend dynamic mounts and prove plan diff

Add a third mount to `variables.tf` default list in `config_mounts`:

```hcl
  default = [
    { source = "config/app.conf", target = "/etc/app/app.conf" },
    { source = "config/logging.conf", target = "/etc/app/logging.conf" },
    { source = "config/metrics.conf", target = "/etc/app/metrics.conf" },
  ]
```

Create `config/metrics.conf`:

```text title="metrics.conf"
scrape_interval=30s
```

Run:

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-terraform/module-10
terraform plan -no-color | tee plan-third-mount.txt
grep -q 'metrics.conf' plan-third-mount.txt
terraform apply -auto-approve
docker inspect billing-prod --format '{{len .Mounts}}' | tee mount-count-after.txt
test "$(cat mount-count-after.txt)" -ge 3
echo "task3 OK" | tee task3-ok.txt
```
{% endraw %}

!!! example "Expected output"
    Plan shows mount update; container has three bind mounts.


#### Task 4 – Expressions evidence script

Create `expressions-evidence.sh`:

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
#!/usr/bin/env bash
set -euo pipefail
cd ~/rebash-terraform/module-10
terraform validate
test -f rendered/service.env
terraform output -raw replica_hint | grep -q 'multi-az'
grep -q 'dynamic "mounts"' main.tf
docker inspect billing-prod --format '{{.State.Running}}' | grep -q true
echo "expressions-evidence PASS" | tee expressions-evidence-pass.txt
```
{% endraw %}

Run:

``` {.bash .ra-terminal title="Terminal"}
chmod +x ~/rebash-terraform/module-10/expressions-evidence.sh
~/rebash-terraform/module-10/expressions-evidence.sh
```

!!! example "Expected output"
    `expressions-evidence-pass.txt` contains `expressions-evidence PASS`.


### Validation steps

- [ ] templatefile rendered env file on disk
- [ ] merge and for expressions drive container labels
- [ ] Conditional chose prod replica hint
- [ ] Dynamic mount blocks applied three bind mounts
- [ ] Evidence script passes with running container

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| templatefile: no file | Wrong path | Prefix with `${path.module}/` |
| Invalid reference in dynamic | Wrong iterator | Use `mounts.value.source` |
| Function type error | merge non-maps | Ensure all args are maps |
| Mount path not found | Config file missing | Create files under `config/` before apply |
| Container name conflict | Old container from prior run | `terraform destroy` then re-apply |

### Challenge exercise

Add `{ source = "config/secrets.conf", target = "/etc/app/secrets.conf" }` only when `var.environment == "prod"` using a conditional in locals, re-apply, and count prod-only mounts:

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-terraform/module-10
# Extend locals with prod_config_mounts using conditional ? :
terraform apply -auto-approve
docker inspect billing-prod --format '{{range .Mounts}}{{.Destination}} {{end}}' | tee mount-paths.txt
grep -q 'secrets.conf' mount-paths.txt
echo "conditional mount challenge OK"
```
{% endraw %}

!!! example "Expected output"
    Prod container includes the secrets mount path.


### Learning outcomes

- templatefile rendering pipeline feeding real resources
- merge/for/conditional expression fluency on Docker labels
- dynamic block structure for variable-length mounts
- Operational proof with `docker inspect` after apply

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-terraform/module-10
terraform destroy -auto-approve
rm -rf rendered config task*-ok.txt replica-hint.txt prod-container.txt \
  container-labels.json mount-count.txt mount-count-after.txt plan-third-mount.txt \
  expressions-evidence-pass.txt mount-paths.txt
rm -rf .terraform .terraform.lock.hcl terraform.tfstate terraform.tfstate.backup
```

## Validation

- [ ] Completed module-10 expressions lab
- [ ] Can write a for expression map comprehension
- [ ] Understand dynamic vs for_each on resources
- [ ] Know templatefile uses ${} placeholders

## Code Walkthrough

1. **Templates in `templates/`** — keep rendering separate from logic.
2. **merge for tags** — base org tags + team overrides.
3. **locals for readability** — break complex function chains.
4. **dynamic for nested rules** — one NSG resource, N rules.
5. **validate before cloud apply** — catch HCL errors early in CI.

## Security Considerations

- Rendered templates may contain secrets — mark sensitive and restrict file permissions.
- `file()` and `templatefile()` read disk at plan — no path traversal from user input.
- Dynamic rules can accidentally open `0.0.0.0/0` — validate CIDR inputs.
- Do not log rendered templates at DEBUG in CI if they include credentials.
- Review `try()` fallbacks — silent defaults can weaken security settings.

## Common Mistakes

!!! warning "Using templatefile for tiny strings"
    One-line content does not need a template file.  
    **Fix:** Inline string or heredoc in HCL for simple cases.

!!! warning "dynamic block with wrong iterator name"
    Referencing `for_each.value` instead of iterator label fails.  
    **Fix:** Default iterator is block name; or set `iterator = alias`.

!!! warning "count vs for_each confusion on resources"
    Dynamic blocks solve nested repetition, not whole resources.  
    **Fix:** `for_each` on resource for separate instances; dynamic for nested blocks.

## Best Practices

- Coalesce tag maps in one `locals` block — single source of truth.
- Unit-test expressions with `terraform console` during development.
- Keep template variables explicit — document keys in module README.
- Prefer `for_each` maps with stable keys over `count` indexes.
- Run `terraform validate` in CI on every module directory.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Template unchanged in plan | Variable did not change | Template only updates when vars change |
| Empty dynamic block | for_each empty list | Expected — verify input collection |
| Type mismatch in for | Wrong object shape | Add explicit `type =` on variable |
| validate OK but plan fails | Provider auth at plan | Expected for cloud; lab stops at validate |
| md5 forces replace | Trigger on file hash | Intentional for demo; use carefully in prod |

## Summary

Functions and expressions make Terraform modules flexible and concise. You rendered templates, merged tags, used conditionals and `for` expressions, and validated dynamic security rules. Next, [Data Sources and Existing Infrastructure](data-sources-and-existing-infrastructure.md) reads reality without managing it.

## Interview Questions

**1. What is the difference between templatefile and the file function?**

??? success "Reveal answer"
    **`file()`** reads a file literally into a string — no variable substitution. **`templatefile()`** reads a template and substitutes **`${name}`** placeholders using the map argument. Use `templatefile` for config generation; `file` for static payloads.

**2. When do you use a dynamic block instead of for_each on a resource?**

??? success "Reveal answer"
    **`dynamic`** repeats **nested blocks inside one resource** (ingress rules, routes). **`for_each` on a resource** creates **multiple separate resources**. Choose dynamic when the provider schema expects repeated nested blocks under one parent.

**3. Write a for expression that filters a list.**

??? success "Reveal answer"
    `[for s in var.services : s.name if s.enabled]` — builds a list of names where `enabled` is true. Map form: `{ for s in var.services : s.id => s.name if s.enabled }`.

**4. What does try() do and when is it risky?**

??? success "Reveal answer"
    **`try(expr, default)`** returns the first successful expression — useful for optional attributes or provider differences. **Risky** when defaults hide misconfiguration — prefer explicit variables over silent insecure defaults.

**5. How do dynamic block iterators work?**

??? success "Reveal answer"
    `for_each` on the dynamic block sets the collection; inside `content`, the iterator (default block name like `ingress`) exposes **`.key`** and **`.value`**. Rename with **`iterator = alias`** and reference `alias.value`.

**6. Are Terraform functions allowed to have side effects?**

??? success "Reveal answer"
    **No** — functions are pure and evaluated at plan time. They cannot call APIs or mutate infrastructure. Side effects happen only through **resources** during apply.

**7. Why use merge for tags?**

??? success "Reveal answer"
    **`merge(map1, map2, ...)`** combines maps; later keys override earlier. Standard pattern: org mandatory tags + environment tags + resource-specific tags in one **`locals.merged_tags`** used across resources.

**8. templatefile changed but plan shows no diff — why?**

??? success "Reveal answer"
    The **rendered result** might be unchanged if variables feeding the template did not change — or the resource using rendered content lacks update trigger. Ensure the resource references the template output and check whether provider updates file in place.

## Related Tutorials

- [Terraform course index](index.md)
- **Previous:** [Registry Modules and Composition](registry-modules-and-composition.md)
- **Next:** [Data Sources and Existing Infrastructure](data-sources-and-existing-infrastructure.md)
- [HCL Fundamentals](hcl-fundamentals-blocks-arguments-and-expressions.md)

## References

- [Functions](https://developer.hashicorp.com/terraform/language/functions)
- [templatefile](https://developer.hashicorp.com/terraform/language/functions/templatefile)
- [For expressions](https://developer.hashicorp.com/terraform/language/expressions/for)
- [Dynamic blocks](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)
- [Conditional expressions](https://developer.hashicorp.com/terraform/language/expressions/conditionals)
