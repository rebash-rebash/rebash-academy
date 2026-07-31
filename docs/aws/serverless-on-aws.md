---
title: "Serverless on AWS — Lambda, APIs, and Eventing"
description: "Design event-driven serverless architectures with Lambda, API Gateway, EventBridge, SNS, SQS, and Step Functions — with cost-aware labs for Cloud DevOps."
difficulty: intermediate
estimated_time: "50–65 min"
technology: aws
category: aws
module: "Module 8 · Serverless"
career_paths:
  - cloud-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - aws
  - lambda
  - api-gateway
  - eventbridge
  - sns
  - sqs
  - step-functions
prerequisites:
  - aws/containers-ecs-eks-ecr
  - aws/iam-identity-access-and-organizations
next:
  - aws/monitoring-and-observability-on-aws
related:
  - aws/compute-ec2-asg-and-load-balancing
  - python/index
labs: []
projects: []
interview: interview/aws
certifications:
  - AWS Developer Associate
  - AWS Solutions Architect Associate
  - AWS DevOps Engineer Professional
tags:
  - aws
  - serverless
  - lambda
  - eventbridge
  - sqs
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Serverless on AWS — Lambda, APIs, and Eventing

## Overview

Assemble a small event-driven design using AWS Lambda, Amazon API Gateway, Amazon EventBridge, Amazon Simple Notification Service (SNS), Amazon Simple Queue Service (SQS), and AWS Step Functions — and tear it down so idle resources do not linger.

**Serverless** on AWS means you deploy code or workflows and pay primarily for invocations, duration, and messages — not for always-on virtual machines. **Lambda** runs functions. **API Gateway** exposes HTTP/WebSocket APIs. **EventBridge** routes events from AWS services and custom buses. **SNS** fans out notifications; **SQS** buffers work for consumers. **Step Functions** orchestrate multi-step workflows with retries and branching. Together they form the backbone of many Cloud DevOps automation and product backends.

This is a core tutorial in **Module 8 · Serverless** of the REBASH Academy **AWS for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Containers on AWS](containers-ecs-eks-ecr.md) (when to choose serverless vs containers)
- IAM roles and least-privilege policies
- AWS CLI configured; optional Python or Node.js for a tiny handler

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Place Lambda behind API Gateway (sync) or an event source (async)  
- [ ] Choose SNS fan-out vs SQS buffering vs EventBridge routing  
- [ ] Outline Step Functions orchestration for a multi-step job  
- [ ] Apply timeouts, concurrency, DLQs, and teardown for cost hygiene

## Architecture

This topic’s control points and relationships are shown below.

![Serverless architecture](../assets/excalidraw/aws-serverless.svg)

## Theory

### What it is

**Serverless** on AWS means you deploy code or workflows and pay primarily for invocations, duration, and messages — not for always-on virtual machines. **AWS Lambda** runs functions. **Amazon API Gateway** exposes HTTP/WebSocket APIs. **Amazon EventBridge** routes events from AWS services and custom buses. **Amazon Simple Notification Service (SNS)** fans out notifications; **Amazon Simple Queue Service (SQS)** buffers work for consumers. **AWS Step Functions** orchestrates multi-step workflows with retries and branching.

### Why it matters

Serverless fits bursty automation — webhooks, scheduled jobs, fan-out pipelines — without patching servers. You still own IAM execution roles, packaging, cold starts, dead-letter queues (DLQs), and cost. Long synchronous work behind API Gateway hits hard timeouts. Choosing SNS vs SQS vs EventBridge — and when Step Functions should own orchestration instead of nested Lambda calls — is a staple Cloud/DevOps design question.

### How it works

1. Package code; create Lambda with an **execution role** for logs and downstream APIs.  
2. **Sync HTTP:** API Gateway → Lambda; deploy a stage; caller waits.  
3. **Async events:** EventBridge/SNS/SQS → Lambda; attach a **DLQ** for poison messages.  
4. **Multi-step:** Step Functions with retry/backoff; start via API or events.  
5. **Operate:** avoid provisioned concurrency unless SLOs need it; watch errors/throttles; delete lab stacks.

Design for **at-least-once** delivery — make handlers idempotent.

### Concept deep dive

- **Lambda** — Managed function compute. Upload a handler; memory also scales CPU. Set timeout, concurrency, and env vars; use VPC only when you must reach private resources (adds cold-start/ENI cost). Prefer short, single-purpose functions.
- **API Gateway** — HTTP/WebSocket front door to Lambda (and other integrations), with throttling, authorisers, and stages. Integration timeout is ~**29 seconds** — accept long work and process asynchronously.
- **EventBridge** — Event bus with content-based rules (or schedules) delivering to Lambda, SQS, Step Functions, and many AWS services. Prefer when many producers/consumers need routing without hard-wiring each pair.
- **SNS** — Pub/sub for **fan-out**: one publish, many subscriptions (Lambda, SQS, email, HTTPS). Prefer when several systems react to one notification; use SNS → SQS when each consumer needs its own buffer.
- **SQS** — Durable queues that **decouple** producers from consumers. Standard maximises throughput; FIFO preserves order within limits. Lambda can poll SQS. Prefer for buffering, back-pressure, and visibility-timeout retries.
- **Step Functions** — **Orchestration** via Amazon States Language: sequence, choice, parallel/map, wait, retries/catchers. Prefer for multi-step workflows instead of fragile nested Lambda calls. Standard for durable jobs; Express for high-volume short flows.
- **Sync vs async** — **Synchronous:** caller waits (API Gateway → Lambda); errors return immediately. **Asynchronous:** event accepted and processed later (EventBridge/SNS/SQS → Lambda). Async needs DLQs, idempotency, and observability.
- **Fan-out** — One event, many consumers (SNS with multiple subscriptions, or EventBridge rules to several targets). Do not use one Lambda to notify everyone sequentially.
- **Orchestration** — Coordinating steps with state, retries, and branching. Step Functions own orchestration; Lambda owns units of work.

### Key concepts and comparisons

| Pattern | Prefer |
|---------|--------|
| Request/response API | API Gateway → Lambda (sync) |
| Many subscribers | SNS fan-out (± SQS per consumer) |
| Buffered workers | SQS → Lambda (async) |
| SaaS/AWS event routing | EventBridge |
| Long business workflow | Step Functions (orchestration) |
| Work longer than ~29s from HTTP | Accept + async (SQS/Step Functions) |

Keep secrets in Secrets Manager or Systems Manager Parameter Store, not plaintext environment variables for sensitive values.

### Common pitfalls

- Assuming serverless is free — traffic and provisioned concurrency still bill  
- Swallowing errors and returning 200 — retries and DLQs never engage  
- Using SNS when you need a buffer (SQS), or SQS when you need heterogeneous fan-out (SNS/EventBridge)  
- Nested Lambda “orchestration” instead of Step Functions  
- Large payloads in events — store in S3 and pass references  
- Leaving rules, APIs, queues, and log groups after labs

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-aws/module-08 && cd ~/rebash-aws/module-08
```

**Focus:** hands-on practice for Serverless on AWS — Lambda, APIs, and Eventing

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Serverless on AWS — Lambda, APIs, and Eventing"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

Create a **minimal** function and tear it down the same session. Prefer zip upload over containers for labs.

```bash
mkdir -p ~/rebash-aws/module-08 && cd ~/rebash-aws/module-08
export LAB_REGION="${LAB_REGION:-eu-west-1}"

cat > handler.py <<'EOF'
def handler(event, context):
    return {"statusCode": 200, "body": '{"ok": true}'}
EOF
zip -q function.zip handler.py

# Role needs lambda.amazonaws.com trust + AWSLambdaBasicExecutionRole
ROLE_ARN=$(aws iam get-role --role-name rebash-lab-lambda-role \
  --query 'Role.Arn' --output text)

aws lambda create-function --function-name rebash-lab-hello \
  --runtime python3.12 --role "$ROLE_ARN" --handler handler.handler \
  --zip-file fileb://function.zip --timeout 10 --memory-size 128 \
  --region "$LAB_REGION"

aws lambda invoke --function-name rebash-lab-hello --payload '{}' \
  --cli-binary-format raw-in-base64-out --region "$LAB_REGION" out.json && cat out.json

cat > eventing-notes.md <<'EOF'
API Gateway → Lambda (sync)
EventBridge schedule → Lambda (cron)
SNS → SQS → Lambda (buffer)
Step Functions → Lambda (orchestration)
EOF

aws lambda delete-function --function-name rebash-lab-hello --region "$LAB_REGION"
rm -f function.zip out.json
```

!!! warning "Cost hygiene"
    Delete functions, APIs, rules, topics, and queues after validation. Avoid provisioned concurrency in labs. Large Step Functions Express vs Standard choice affects pricing — start with Standard and short executions.

### Final step – Cleanup note

```bash
# Keep ~/rebash-aws/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-aws/module-08/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Serverless on AWS — Lambda, APIs, and Eventing** always combines:

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

!!! warning "Assuming serverless is free — traffic and provisioned concurrency still bill  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Swallowing errors and returning 200 — retries and DLQs never engage  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Serverless on AWS — Lambda, APIs, and Eventing changes as code and review them in pull requests
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

**Serverless on AWS — Lambda, APIs, and Eventing** is essential for Cloud and DevOps engineers working with aws. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Serverless on AWS — Lambda, APIs, and Eventing** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Monitoring and Observability on AWS](monitoring-and-observability-on-aws.md)

## References

- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)  
- [Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)  
- [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)  
- [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) · [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)  
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
