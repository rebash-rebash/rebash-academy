---
title: "Cloud Automation — AWS, Azure, and GCP"
description: "Automate cloud inventory with boto3, Azure SDK, and Google Cloud client libraries — auth patterns, EC2/S3/IAM/Lambda sketches, and dry-run safe defaults."
difficulty: advanced
estimated_time: "60–75 min"
technology: python
category: python
module: "Module 15 · Cloud Automation"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - boto3
  - azure-sdk
  - gcp-sdk
  - cloud-automation
prerequisites:
  - python/rest-apis-requests-auth-and-resilience
next:
  - python/git-automation-github-and-gitlab
related:
  - networking/cloud-networking-vpc-and-subnets
  - labs/python-aws-ec2-inventory
  - labs/python-azure-resource-inventory
  - labs/python-gcp-inventory
labs:
  - labs/python-aws-ec2-inventory
  - labs/python-azure-resource-inventory
  - labs/python-gcp-inventory
projects:
  - projects/python-cloud-operations-toolkit
interview: interview/python
certifications:
  - AWS SAA
  - Azure AZ-104
  - Google ACE
tags:
  - python
  - boto3
  - aws
  - azure
  - gcp
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Cloud Automation — AWS, Azure, and GCP

## Overview

Sketch multi-cloud inventory automation with the right SDK auth model, practise a boto3-style EC2/S3 listing pattern (live or fixture), and keep mutating calls behind `--apply`.

Cloud SDKs are HTTP clients with pagination and IAM. This module teaches **patterns** — credentials, list APIs, least privilege — not every service API. Use Free Tier / read-only roles; fixtures are fine for CI.

Complete [REST APIs](rest-apis-requests-auth-and-resilience.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 15 · Cloud Automation** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [REST APIs — requests, Auth, and Resilience](rest-apis-requests-auth-and-resilience.md)
- Comfort with env-based secrets (Module 11)

### Recommended

- Optional: AWS/Azure/GCP account with **read-only** credentials  
- Without cloud access: use the fixture path in the lab

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Describe boto3 session/client/resource patterns  
- [ ] List EC2/S3 style inventory safely  
- [ ] Outline Azure DefaultAzureCredential + resource management  
- [ ] Outline GCP application default credentials + list calls  
- [ ] Prefer IAM roles over long-lived keys  
- [ ] Structure dry-run inventory CLIs for CI

## Architecture

This topic’s control points and relationships are shown below.

![Cloud automation](../assets/excalidraw/python-cloud-automation.svg)

## Theory

### What it is

Cloud Software Development Kits (SDKs) are official Python libraries that call provider APIs: **boto3** for Amazon Web Services (AWS), **azure-identity** / **azure-mgmt-*** for Microsoft Azure, and **google-cloud-*** clients for Google Cloud Platform (GCP). They handle signing, pagination helpers, and typed request shapes so you inventory Elastic Compute Cloud (EC2), blobs, and Identity and Access Management (IAM) without hand-rolling HTTP.

### Why it matters

Multi-cloud (or even single-cloud) operations need repeatable inventory, tagging audits, and safe change tools. Console click-paths do not scale; raw REST duplicates auth bugs. SDKs plus least-privilege roles on Continuous Integration (CI) runners are how platform teams prove “what exists” and gate mutations behind `--apply`. The same resilience ideas from the REST module — timeouts, pagination, fail-fast on 403 — apply here.

### How it works

On AWS, `boto3.Session(region_name=...)` builds clients (`ec2`, `s3`, …). Credential chain: environment variables, shared config, then instance/workload role — prefer **roles** over long-lived access keys. Always use paginators for list APIs. Azure uses `DefaultAzureCredential` (managed identity, `az login`, or service principal env vars) with management libraries scoped by subscription. GCP uses Application Default Credentials (`gcloud auth application-default login` or workload identity) with compute/storage clients. Pass region, subscription, or project as required CLI arguments — never hard-code production accounts.

```python
import boto3
session = boto3.Session(region_name="eu-west-1")
ec2 = session.client("ec2")
# paginator = ec2.get_paginator("describe_instances")
```

### Key concepts and comparisons

| Cloud | Auth pattern | Inventory examples |
|-------|--------------|--------------------|
| AWS | Roles / boto3 session | EC2, S3, Lambda, IAM (careful) |
| Azure | `DefaultAzureCredential` | Resource groups, VMs, storage |
| GCP | ADC / workload identity | Compute instances, GCS buckets |

| Rule | Practice |
|------|----------|
| Read-only first | `describe` / `list` / `get` |
| Paginate | Every list API |
| Mutate | `--apply` + confirmation |
| Secrets | Never commit access keys |

### Common pitfalls

- Hard-coding a single region and missing multi-region resources.  
- Using admin keys in CI “temporarily.”  
- Ignoring pagination and under-reporting inventory.  
- Mutating IAM or security groups without dry-run policy.  
- Confusing account/subscription/project IDs when credentials can see many.

## Hands-on Lab

**Focus:** practise the core workflow for Cloud Automation — AWS, Azure, and GCP

```bash
mkdir -p ~/rebash-python/module-15
cd ~/rebash-python/module-15

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'boto3==1.36.16'
# Optional later: azure-identity azure-mgmt-resource google-cloud-compute
```

### Step 1 – Fixture inventory (always works)

```bash
cd ~/rebash-python/module-15
source .venv/bin/activate

mkdir -p fixtures
cat > fixtures/ec2.json << 'EOF'
{
  "Reservations": [
    {
      "Instances": [
        {"InstanceId": "i-abc", "State": {"Name": "running"}, "Tags": [{"Key": "Name", "Value": "web-a"}]},
        {"InstanceId": "i-def", "State": {"Name": "stopped"}, "Tags": [{"Key": "Name", "Value": "web-b"}]}
      ]
    }
  ]
}
EOF

cat > ec2_inventory.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def from_fixture(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for res in data.get("Reservations", []):
        for inst in res.get("Instances", []):
            tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
            rows.append(
                {
                    "id": inst.get("InstanceId"),
                    "state": inst.get("State", {}).get("Name"),
                    "name": tags.get("Name", ""),
                }
            )
    return rows


def from_boto3(region: str) -> list[dict]:
    import boto3

    client = boto3.client("ec2", region_name=region)
    rows = []
    paginator = client.get_paginator("describe_instances")
    for page in paginator.paginate():
        for res in page.get("Reservations", []):
            for inst in res.get("Instances", []):
                tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
                rows.append(
                    {
                        "id": inst.get("InstanceId"),
                        "state": inst.get("State", {}).get("Name"),
                        "name": tags.get("Name", ""),
                    }
                )
    return rows


def main() -> int:
    p = argparse.ArgumentParser(description="EC2 inventory")
    p.add_argument("--region", default="eu-west-1")
    p.add_argument("--fixture", type=Path, help="use JSON fixture instead of AWS")
    args = p.parse_args()
    try:
        rows = from_fixture(args.fixture) if args.fixture else from_boto3(args.region)
    except Exception as exc:  # noqa: BLE001 — boundary for missing creds
        print(f"error: {exc}", file=sys.stderr)
        print("hint: pass --fixture fixtures/ec2.json for offline lab", file=sys.stderr)
        return 1
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python ec2_inventory.py --fixture fixtures/ec2.json
```

### Step 2 – Live AWS (optional)

```bash
# Only if credentials exist:
# python ec2_inventory.py --region eu-west-1
echo "Skip live call unless AWS creds are configured for read-only access"
```

### Step 3 – Multi-cloud mental model

Write `cloud-notes.md`:

```text
AWS: boto3 Session → client → paginator
Azure: DefaultAzureCredential → ResourceManagementClient
GCP: ADC → compute_v1.InstancesClient.list
Common: project/subscription/region flags, JSON stdout, secrets in env
```

### Step 4 – S3 list sketch (fixture-style)

```bash
python - <<'PY'
buckets = [{"Name": "logs-prod"}, {"Name": "tf-state-lab"}]
for b in buckets:
    print(b["Name"])
print("# live: boto3.client('s3').list_buckets()")
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-15/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Cloud Automation — AWS, Azure, and GCP** always combines:

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

!!! warning "Hard-coding a single region and missing multi-region resources.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using admin keys in CI “temporarily.”  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Cloud Automation — AWS, Azure, and GCP changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `NoCredentialsError` | Missing AWS creds | Use `--fixture` or configure role/env |
| AccessDenied | Over-scoped / under-scoped IAM | Least-privilege read policy |
| Wrong region | Default region empty | Pass `--region` explicitly |

## Summary

- SDKs = authenticated, paginated HTTP  
- Inventory first; mutate only with `--apply`  
- Fixtures keep CI green without cloud keys  
- Deep practise in AWS/Azure/GCP inventory labs

## Interview Questions

1. How does **Cloud Automation — AWS, Azure, and GCP** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Git Automation — GitHub and GitLab](git-automation-github-and-gitlab.md)  
- [AWS EC2 Inventory lab](../labs/python-aws-ec2-inventory.md)  
- [Azure Resource Inventory lab](../labs/python-azure-resource-inventory.md)  
- [GCP Inventory lab](../labs/python-gcp-inventory.md)

## References

- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)  
- [Azure Identity](https://learn.microsoft.com/python/api/overview/azure/identity-readme)  
- [GCP Python client](https://cloud.google.com/python/docs/reference)
