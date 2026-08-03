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



!!! warning "Cost and account safety"
    Use a sandbox account. Prefer read-only calls. Destroy anything you create before leaving the lab.

### Objective

Use read-only AWS APIs to inventory and verify aspects of **AWS Security Services — Keys, Secrets, and Detection** in a sandbox account.

### Prerequisites

- AWS CLI v2
- Credentials for a **sandbox** account (SSO or short-lived keys)

### Lab environment

Workspace: `~/rebash-aws/module-10`

Prefer `describe`/`list`/`get` APIs. Create resources only with an explicit destroy path.

```bash title="Terminal"
mkdir -p ~/rebash-aws/module-10 && cd ~/rebash-aws/module-10
```

### Real-world scenario

Security asks for evidence that **AWS Security Services — Keys, Secrets, and Detection** is configured correctly. You gather CLI proof without click-ops drift.

### Step-by-step tasks

#### Task 1 – Prove caller identity

Every AWS change starts by knowing which account/role you are.

```bash title="Terminal"
aws sts get-caller-identity | tee identity.json
aws configure get region || true
test -s identity.json
```

!!! example "Expected output"
    JSON includes Account, Arn, and UserId.


#### Task 2 – Collect topic signals

Inventory the service surface related to this module.

```bash title="Terminal"
aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,Cidr:CidrBlock}' --output table 2>/dev/null | tee vpcs.txt || true
aws iam get-account-summary 2>/dev/null | tee iam-summary.json || true
tee notes.txt << 'EOF'
Record which APIs apply to this topic and any NotAuthorized errors for follow-up.
EOF
cat notes.txt
```

!!! example "Expected output"
    Evidence files created even if some APIs are denied.


### Validation steps

- [ ] identity.json present
- [ ] No long-lived keys committed to the repo

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Unable to locate credentials | No profile/SSO | Run `aws sso login` or export sandbox keys |
| AccessDenied | Least privilege | Use a role that can read the service — or document the deny |
| UnauthorizedOperation | Wrong region/account | Check `AWS_REGION` and account id |

### Challenge exercise

Enable a cost budget alarm in the sandbox (or document the console clicks) and screenshot/CLI-describe it.

### Learning outcomes

- Authenticated safely
- Captured read-only evidence
- Avoided unmanaged spend

### Cleanup

```bash
# Revoke/lab-expire any temporary keys you exported
# Do not leave EC2/ELB/NAT running
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




1. CloudTrail versus CloudWatch Logs versus Config?
2. What does GuardDuty detect at a high level?
3. Security Hub’s role in a multi-account org?
4. How do you respond to a public snapshot finding?
5. Why organisation trails matter?

!!! tip "Sample answer — question 2"
    Confirm the service is enabled in the account/region and that you are looking at the right aggregator account.

!!! tip "Sample answer — question 4"
    Centralise trails/findings and restrict who can disable logging.

## Related Tutorials






- [Course overview](index.md)
- [Infrastructure as Code on AWS](infrastructure-as-code-on-aws.md)

## References






- [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)  
- [Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)  
- [Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)  
- [GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html) · [Inspector](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html)  
- [Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html) · [Macie](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)  
- [Shield](https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html) · [WAF](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html)
