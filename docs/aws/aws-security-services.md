---
title: "AWS Security Services — Keys, Secrets, and Detection"
description: "Apply KMS, Secrets Manager, Parameter Store, GuardDuty, Inspector, Security Hub, Macie, Shield, and WAF for defence in depth on AWS."
difficulty: advanced
estimated_time: "55–70 min"
technology: aws
category: aws
module: "Module 10 · Security"
career_paths:
  - cloud-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - aws
  - kms
  - secrets-manager
  - guardduty
  - security-hub
  - waf
prerequisites:
  - aws/monitoring-and-observability-on-aws
  - aws/iam-identity-access-and-organizations
next:
  - aws/infrastructure-as-code-on-aws
related:
  - aws/iam-identity-access-and-organizations
  - aws/production-aws-landing-zones
  - security/index
labs: []
projects: []
interview: interview/aws
certifications:
  - AWS Solutions Architect Associate
  - AWS DevOps Engineer Professional
  - AWS Developer Associate
tags:
  - aws
  - security
  - kms
  - guardduty
  - waf
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# AWS Security Services — Keys, Secrets, and Detection

## Overview

Place AWS Key Management Service (KMS), Secrets Manager, Systems Manager Parameter Store, GuardDuty, Inspector, Security Hub, Macie, Shield, and AWS WAF into a coherent defence-in-depth model — and practise secret/parameter hygiene without leaving paid detectors unreviewed.

Identity (IAM) is necessary but not sufficient. **KMS** manages encryption keys. **Secrets Manager** and **Parameter Store** distribute secrets and configuration. **GuardDuty** detects threats from logs and findings. **Inspector** scans for software vulnerabilities. **Security Hub** aggregates findings and standards. **Macie** discovers sensitive data in S3. **Shield** protects against Distributed Denial of Service (DDoS); **AWS WAF** filters Layer 7 web exploits. Production platforms combine encryption, least privilege, continuous detection, and edge protection — with clear ownership for triage.

This is a core tutorial in **Module 10 · Security** of the REBASH Academy **AWS for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Monitoring and Observability on AWS](monitoring-and-observability-on-aws.md)
- Solid IAM (roles, policies, MFA, Organisations SCPs)
- CloudTrail enabled in the account you use for labs

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Choose KMS customer managed keys versus AWS managed keys and explain envelope encryption  
- [ ] Store and retrieve a secret in Secrets Manager and a `SecureString` in Parameter Store  
- [ ] Map GuardDuty, Inspector, Security Hub, and Macie to distinct detection jobs  
- [ ] Contrast Shield Standard versus Shield Advanced and place AWS WAF at Layer 7

## Architecture

This topic’s control points and relationships are shown below.

![AWS security services](../assets/excalidraw/aws-security.svg)

## Theory

### What it is

IAM alone is not defence in depth. **AWS KMS** manages encryption keys (key policy + IAM authorise use). **Secrets Manager** stores secrets with optional rotation. **Parameter Store `SecureString`** holds KMS-encrypted config. **GuardDuty** detects threats from CloudTrail, VPC Flow Logs, DNS, and related signals. **Inspector** finds CVEs on EC2, Lambda, and images. **Security Hub** aggregates findings and standards. **Macie** discovers sensitive data in S3. **Shield** mitigates DDoS (**Standard** included for eligible edges; **Advanced** adds specialised response). **AWS WAF** filters Layer 7 HTTP(S) on CloudFront, ALB, API Gateway, and AppSync.

| Layer | Services |
|-------|----------|
| Keys | KMS |
| Secrets / config | Secrets Manager, Parameter Store (`SecureString`) |
| Detect / posture | GuardDuty, Inspector, Security Hub, Macie |
| Edge / DDoS | Shield Standard / Advanced, WAF |

### Why it matters

Most incidents involve leaked credentials, missing encryption, unpatched software, or exposed data. DevSecOps fetches secrets at runtime via roles — never Git. Platform teams own a findings backlog people clear; Security Hub without owners is theatre. Stage WAF in **count** mode before block. Shared responsibility: you own keys, rotation, triage, and input validation.

### How it works

1. Use a **customer managed key** for key policies, rotation control, or cross-account access; otherwise AWS managed keys often suffice.
2. Rotating credentials → Secrets Manager; simple encrypted config → `SecureString`; grant only `GetSecretValue` / `GetParameter`.
3. Enable GuardDuty and Inspector where workloads run; aggregate in Security Hub.
4. Run Macie on buckets that may hold personal data.
5. Attach WAF managed rules to public HTTP; rely on Shield Standard unless Advanced is justified.
6. Keep CloudTrail on; prefer IAM roles/STS over static keys.

**Envelope encryption:** data key encrypts the payload; KMS wraps the data key (S3/EBS do this when KMS encryption is on).

### Concept deep dive

**KMS** keys are Region-scoped; every use is an authorised API call. Prefer aliases; schedule deletion only after inventory — losing the key loses ciphertext. **Secrets Manager** fits rotating DB passwords and cross-account retrieval; pay per secret — delete labs; fetch at runtime, not bake into env vars. **`SecureString`** fits encrypted config without full rotation; path hierarchies (`/app/prod/…`) aid IAM; advanced parameters cost more for size/policies.

**GuardDuty** is behavioural threat detection (compromise patterns, crypto-mining, reconnaissance) — not CVE scanning; use a delegated admin. **Inspector** is vulnerability management for EC2, Lambda, and ECR images — feed patch/rebuild pipelines. **Security Hub** aggregates standards (CIS, Foundational Best Practices); enable only what you remediate; EventBridge → tickets. **Macie** classifies sensitive data in S3 for compliance — complement, do not replace, bucket policy and encryption.

**Shield Standard** covers common volumetric/protocol attacks on eligible CloudFront, Route 53, and ELB resources at no extra charge. **Advanced** adds DDoS Response Team access, richer metrics, and attack-related cost protections — for critical public businesses, not every site. **WAF** applies IP sets, rate limits, and managed/custom rules at Layer 7; count → review → block; WAF is not a full volumetric DDoS substitute.

### Key concepts and comparisons

| Need | Prefer |
|------|--------|
| Rotating DB password | Secrets Manager |
| Non-secret config | Parameter Store String |
| Encrypted config / simple secret | `SecureString` |
| Key control / cross-account crypto | KMS customer managed key |
| Threat behaviour | GuardDuty |
| CVE scanning | Inspector |
| Standards backlog | Security Hub |
| Sensitive data in S3 | Macie |
| HTTP exploits | WAF |
| Critical public DDoS programme | Shield Advanced (else Standard) |

### Common pitfalls

- Scheduling KMS deletion without encrypted-resource inventory.
- Broad `kms:*` / `secretsmanager:*` on humans.
- Every Security Hub standard with no owners.
- Assuming Shield Advanced for every website.
- Blocking WAF rules that break health checks.
- Plaintext secrets in Lambda env vars.
- Confusing GuardDuty (behaviour), Inspector (CVEs), and Macie (data discovery).

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-aws/module-10 && cd ~/rebash-aws/module-10
```

**Focus:** hands-on practice for AWS Security Services — Keys, Secrets, and Detection

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: AWS Security Services — Keys, Secrets, and Detection"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

Create a **parameter or secret**, read it, delete it. Treat GuardDuty/Security Hub as **read/enable awareness**, not a permanent paid sprawl across unused regions.

```bash
mkdir -p ~/rebash-aws/module-10 && cd ~/rebash-aws/module-10
export LAB_REGION="${LAB_REGION:-eu-west-1}"

aws ssm put-parameter --name /rebash-lab/module-10/demo \
  --type SecureString --value "lab-only-not-a-real-secret" \
  --overwrite --region "$LAB_REGION"
aws ssm get-parameter --name /rebash-lab/module-10/demo \
  --with-decryption --region "$LAB_REGION" --query 'Parameter.Value' --output text

aws secretsmanager create-secret --name rebash-lab/module-10/demo \
  --secret-string '{"user":"lab","password":"ChangeMeLabOnly"}' \
  --region "$LAB_REGION"
aws secretsmanager get-secret-value --secret-id rebash-lab/module-10/demo \
  --region "$LAB_REGION" --query 'SecretString' --output text

aws guardduty list-detectors --region "$LAB_REGION" --output table || true
aws securityhub describe-hub --region "$LAB_REGION" 2>/dev/null || \
  echo "Security Hub not enabled (OK for sandbox review)."

cat > security-notes.md <<'EOF'
1. IAM least privilege + SCPs
2. KMS at rest
3. Secrets Manager / SSM — never Git
4. GuardDuty + Inspector → Security Hub
5. Macie on sensitive buckets
6. WAF + Shield on public HTTP
EOF

aws ssm delete-parameter --name /rebash-lab/module-10/demo --region "$LAB_REGION"
aws secretsmanager delete-secret --secret-id rebash-lab/module-10/demo \
  --force-delete-without-recovery --region "$LAB_REGION"
```

!!! warning "Cost hygiene"
    GuardDuty, Macie, Inspector, and Security Hub incur charges. Enable deliberately in regions you use; disable lab-only detectors when finished if your organisation allows. Secrets Manager charges per secret per month — delete lab secrets with `--force-delete-without-recovery` only in non-production.

### Final step – Cleanup note

```bash
# Keep ~/rebash-aws/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-aws/module-10/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **AWS Security Services — Keys, Secrets, and Detection** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for aws as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Scheduling KMS deletion without encrypted-resource inventory."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Broad `kms:*` / `secretsmanager:*` on humans."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode AWS Security Services — Keys, Secrets, and Detection changes as code and review them in pull requests
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

**AWS Security Services — Keys, Secrets, and Detection** is essential for Cloud and DevOps engineers working with aws. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **AWS Security Services — Keys, Secrets, and Detection** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Infrastructure as Code on AWS](infrastructure-as-code-on-aws.md)

## References

- [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)  
- [Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)  
- [Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)  
- [GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html) · [Inspector](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html)  
- [Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html) · [Macie](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)  
- [Shield](https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html) · [WAF](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html)
