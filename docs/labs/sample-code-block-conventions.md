---
title: "Sample — Code block conventions"
description: "Review sample for lab code UX: filename titles, file vs terminal fences, expected-output admonitions, and optional line numbers."
difficulty: beginner
estimated_time: "15–20 min"
author: Shaik Basha
last_updated: "2026-08-03"
category: labs
tags:
  - sample
  - conventions
  - labs
comments: false
---

# Sample — Code block conventions

!!! tip "Approved convention"
    This page is the **canonical sample** for lab code blocks. **Terminal** chrome (dark panel) versus **file** chrome (green filename bar) is the site-wide standard. Hard-refresh if styles look stale.

## What to look for

| Convention | How it appears |
|------------|----------------|
| File to create | Light panel + green filename bar (`title="main.tf"`) |
| Commands to run | Dark terminal chrome (`title="Terminal"`) — not the same as file blocks |
| Expected output | `!!! example "Expected output"` admonition |
| Long files | Optional `linenums="1"` (shown once below) |
| Always tagged | No bare fences |

---

## Hands-on Lab

### Objective

Apply a tiny **Docker** Terraform stack and prove the container with CLI evidence — using the new code-block conventions.

### Prerequisites

- Terraform CLI ≥ 1.5
- Docker Engine running

### Lab environment

```bash title="Terminal"
mkdir -p ~/rebash-labs/sample-code-blocks && cd ~/rebash-labs/sample-code-blocks
```

Runtime: local Docker Engine + `kreuzwerker/docker` provider.

### Real-world scenario

A platform engineer is onboarding a disposable lab pattern: create config as files (not heredocs), run a short terminal session, and prove success with a clear expected-output panel — the same shape learners should see in production interview prep labs.

### Step-by-step tasks

#### Task 1 – Author provider and network

Create the provider pin and a bridge network.

```hcl title="versions.tf"
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}
```

```hcl title="main.tf"
resource "docker_network" "lab" {
  name   = "rebash-sample-net"
  driver = "bridge"
}

resource "docker_image" "nginx" {
  name         = "nginx:1.25-alpine"
  keep_locally = true
}

resource "docker_container" "web" {
  name  = "rebash-sample-web"
  image = docker_image.nginx.image_id

  networks_advanced {
    name = docker_network.lab.name
  }

  ports {
    internal = 80
    external = 18080
  }

  labels {
    label = "rebash.sample"
    value = "code-blocks"
  }
}

output "container_name" {
  value = docker_container.web.name
}
```

Initialise and apply:

{% raw %}
```bash title="Terminal"
cd ~/rebash-labs/sample-code-blocks
terraform init
terraform apply -auto-approve
docker ps --filter name=rebash-sample-web --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | tee docker-ps.txt
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18080/ | tee http-code.txt
grep -q rebash-sample-web docker-ps.txt
grep -q 200 http-code.txt
```
{% endraw %}

!!! example "Expected output"
    - `terraform apply` creates the network and `rebash-sample-web`
    - `docker-ps.txt` lists `rebash-sample-web` as Up
    - `http-code.txt` contains `200`

#### Task 2 – Prove labels (interview-style evidence)

Inspect the container label set by Terraform:

{% raw %}
```bash title="Terminal"
cd ~/rebash-labs/sample-code-blocks
docker inspect -f '{{index .Config.Labels "rebash.sample"}}' rebash-sample-web | tee label.txt
grep -q code-blocks label.txt
terraform output -raw container_name | tee output-name.txt
grep -q rebash-sample-web output-name.txt
```
{% endraw %}

!!! example "Expected output"
    - `label.txt` is `code-blocks`
    - `output-name.txt` is `rebash-sample-web`

#### Task 3 – Optional: long file with line numbers

Use line numbers only when a file is long enough that reviewers discuss specific lines (example shape — do not require this file for the lab):

```yaml title="compose.example.yaml" linenums="1"
# Example only — illustrates linenums on longer artefacts
services:
  web:
    image: nginx:1.25-alpine
    ports:
      - "18080:80"
    labels:
      rebash.sample: code-blocks
  # …
  # (truncated in real labs; linenums help when walking line 12 in review)
```

### Validation steps

- [ ] `docker ps` shows `rebash-sample-web`
- [ ] HTTP check returns `200`
- [ ] Label and Terraform output match
- [ ] Filename titles appear above file fences; Terminal title appears on command fences
- [ ] Expected output uses green/example admonitions, not plain bold text alone

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Cannot connect to Docker | Daemon not running | Start Docker Desktop / `dockerd` |
| Port 18080 in use | Another local service | Change `external` port in `main.tf` and re-apply |
| Provider not found | Skipped init | Run `terraform init` again |

### Challenge exercise

Add an output `network_name` and prove it with `terraform output` plus `docker network ls`.

### Learning outcomes

- File fences carry `title="filename"` so copy targets are obvious
- Terminal fences stay short and labelled
- Success criteria sit in an **Expected output** admonition
- Lab still does real apply / proof / cleanup

### Cleanup

```bash title="Terminal"
cd ~/rebash-labs/sample-code-blocks
terraform destroy -auto-approve
rm -f docker-ps.txt http-code.txt label.txt output-name.txt
```

!!! example "Expected output"
    Terraform reports destroy complete; `docker ps -a --filter name=rebash-sample-web` is empty.

---

## Authoring cheat sheet (for reviewers)

````markdown
Create `main.tf`:

```hcl title="main.tf"
resource "docker_network" "lab" {
  name = "rebash-sample-net"
}
```

```bash title="Terminal"
terraform apply -auto-approve
```

!!! example "Expected output"
    Apply succeeds; resource exists.
````

**Do not** use `**Expected output:**` as the only success signal once this convention is approved.  
**Do not** put multi-line files inside `cat <<EOF` heredocs.
