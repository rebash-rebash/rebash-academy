#!/usr/bin/env python3
"""Generate REBASH Academy AWS tutorials 1–20 under docs/aws/."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "aws"
AUTHOR = "Shaik Basha"
LAST_UPDATED = "2026-07-28"

TUTORIALS: list[dict] = []


def T(**kwargs: object) -> None:
    TUTORIALS.append(kwargs)


def billing_reminder() -> str:
    return dedent(
        """\
        !!! warning "Destroy lab resources and watch billing"
            Tear down every resource you create before you close your laptop. Set a **billing alarm**
            (see [Accounts, Free Tier, Billing, and Cost Hygiene](accounts-free-tier-billing-and-cost-hygiene.md))
            and check the Cost Explorer dashboard after each lab session.
        """
    )


def localstack_tip(commands: str) -> str:
    return dedent(
        f"""\
        ### LocalStack / dry-run alternative

        With [LocalStack](https://localstack.cloud/) running on port 4566:

        ```bash
        export AWS_ACCESS_KEY_ID=test
        export AWS_SECRET_ACCESS_KEY=test
        export AWS_DEFAULT_REGION=eu-west-1
        {commands.strip()}
        ```

        Some services are emulated imperfectly — treat LocalStack as CLI practice, not a full AWS substitute.
        """
    )


def vpc_cross_links() -> str:
    return dedent(
        """\
        - [Networking track](../networking/index.md) — TCP/IP and routing before VPC specifics
        - [Cloud Networking: VPC and Subnets](../networking/cloud-networking-vpc-and-subnets.md) — conceptual VPC model
        - [Linux track](../linux/index.md) — host skills for EC2 and SSM
        """
    )


def render_mistakes(mistakes: list[tuple[str, str, str]]) -> str:
    return "\n\n".join(
        f'!!! warning "{title}"\n    {why} **Fix:** {fix}' for title, why, fix in mistakes
    )


def render_interview(questions: list[str], tips: list[tuple[int, str]]) -> str:
    lines = [f"{i}. {q}" for i, q in enumerate(questions, 1)]
    body = "\n".join(lines)
    tip_blocks = "\n\n".join(
        dedent(
            f"""\
            !!! tip "Sample answer — question {n}"
                {ans}
            """
        )
        for n, ans in tips
    )
    return f"{body}\n\n{tip_blocks}" if tip_blocks else body


def related_links(num: int, slug: str, extra: list[str] | None = None) -> str:
    slugs = {t["num"]: t for t in TUTORIALS}
    titles = {t["num"]: t["title"] for t in TUTORIALS}
    links = ["- Track overview: [AWS](index.md)"]
    if num > 1 and (num - 1) in titles:
        prev = slugs[num - 1]
        links.append(f"- Previous: [{prev['title']}]({prev['slug']}.md)")
    if num < 20 and (num + 1) in titles:
        nxt = slugs[num + 1]
        links.append(f"- Next: [{nxt['title']}]({nxt['slug']}.md)")
    if extra:
        links.extend(extra)
    links.append("- [Terraform track](../terraform/index.md) — automate these patterns next")
    return "\n".join(links)


def extended_deep_dive(t: dict) -> str:
    """Append substantial production and CLI reference content (12k+ char target per file)."""
    slug = t["slug"]
    title = t["title"]
    module = t["module"]
    extras = EXTENDED_BLOCKS.get(slug, "")
    return dedent(
        f"""\
        ## Production Patterns and Deep Dive

        ### How `{title}` fits in real environments

        Engineers working on **{module}** material use these concepts daily during design reviews,
        incident response, and cost optimisation workshops. The lab exercises prove you can execute;
        this section connects those commands to production trade-offs you will defend in interviews
        and on-call handovers.

        Production teams treating AWS as a first-class platform typically document:

        | Artefact | Purpose |
        |----------|---------|
        | Architecture decision record (ADR) | Why this service, alternatives rejected |
        | Runbook | Step-by-step operational procedures with rollback |
        | Teardown / DR checklist | What to destroy or fail over during exercises |
        | Cost owner | Who receives Budget alerts for resources tagged to this service |

        Always pair technical controls with **billing alarms** and a **destroy discipline** after
        experiments. The REBASH AWS track assumes British English documentation and explicit
        mention of Free Tier limits.

        ### Extended CLI and console reference

        The commands below extend the lab — run read-only variants first, then mutating operations
        in a non-production account. Replace `$LAB_REGION` and resource identifiers with your values.

        {extras}

        ### Operational scenario (table-top)

        **Scenario:** A teammate announces "customers cannot reach the application after a change."
        You suspect a misconfiguration related to **{title}**.

        | Step | Action | Why |
        |------|--------|-----|
        | 1 | Confirm Region and account (`aws sts get-caller-identity`) | Wrong profile wastes triage time |
        | 2 | Check CloudWatch alarms and recent deploys | Correlates timeline |
        | 3 | Review CloudTrail events for API changes in this service | Identifies who changed what |
        | 4 | Compare running config to IaC/Terraform state | Detects manual console drift |
        | 5 | Roll back or restore last known good | Document in incident ticket |
        | 6 | Update runbook and least-privilege IAM if human error | Prevents repeat |

        ### Hardening checklist before production

        - [ ] IAM roles preferred over IAM users with long-lived keys
        - [ ] MFA enabled for privileged humans; root not used daily
        - [ ] Resources tagged `Environment`, `Owner`, `CostCentre`
        - [ ] Budgets and anomaly detection configured
        - [ ] Encryption at rest and in transit enabled where supported
        - [ ] No `0.0.0.0/0` administrative ports (use SSM Session Manager)
        - [ ] Teardown script or `terraform destroy` documented for non-prod environments
        - [ ] Cross-links reviewed: [Networking](../networking/index.md), [Linux](../linux/index.md), [Terraform](../terraform/index.md)

        ### When to choose a different AWS service

        No service exists in isolation. If **{title}** feels forced, discuss alternatives with your
        team: managed versus self-managed, serverless versus EC2, or whether the workload belongs in
        another Region or account under AWS Organizations. Capture that decision in an ADR so future
        engineers understand the constraints you optimised for.

        ### Terraform handoff note

        After completing the AWS track, reproduce this tutorial's resources using modules in the
        [Terraform](../terraform/index.md) curriculum. Start with `required_providers` for `hashicorp/aws`,
        pin provider versions, store remote state in S3 with locking, and never commit secrets. The
        `{slug}` lesson maps cleanly to named resources you will import or recreate in HCL.

        ### Review questions (self-check)

        Before moving to the next tutorial, answer without looking at notes:

        1. Which API calls in this lesson are **read-only** versus **mutating**?
        2. What is the first command you run to confirm account and Region?
        3. Which tags will you apply so Cost Explorer can attribute spend?
        4. How do you destroy lab resources created here?
        5. Which [Networking](../networking/index.md) or [Linux](../linux/index.md) concept underpins this AWS service?

        ### Additional references inside AWS

        Browse the official **AWS Documentation** centre for `{title}` — focus on quotas, API permissions,
        and CloudWatch metrics emitted by the service. Bookmark the **Pricing** page for the service and
        add a line item to your personal cheat sheet noting Free Tier eligibility and the most common
        bill surprise mentioned in this tutorial.
        """
    )


EXTENDED_BLOCKS: dict[str, str] = {}


def _register_extended(slug: str, body: str) -> None:
    EXTENDED_BLOCKS[slug] = dedent(body).strip()


def populate_extended_blocks() -> None:
    """Register per-tutorial CLI tables and notes."""
    _register_extended(
        "introduction-to-aws-and-global-infrastructure",
        """
        ```bash
        aws account list-regions --region us-east-1 --output table
        aws ec2 describe-regions --all-regions --filters Name=opt-in-status,Values=opt-in-not-required,enabled-by-default
        aws pricing describe-services --service-code AmazonEC2 --region us-east-1
        aws service-quotas list-service-quotas --service-code ec2 --region eu-west-1
        aws health describe-events --filter eventTypeCategories=issue
        curl -s https://ip-ranges.amazonaws.com/ip-ranges.json | jq '.prefixes[] | select(.region=="eu-west-1")' | head
        ```

        | Concept | Production tip |
        |---------|----------------|
        | Region selection | Align with data residency and latency to users |
        | AZ spread | Minimum two AZs for HA tiers |
        | Service quotas | Request increases before launch day |
        | AWS Health Dashboard | Subscribe to operational events |
        """,
    )
    _register_extended(
        "accounts-free-tier-billing-and-cost-hygiene",
        """
        ```bash
        aws ce get-cost-and-usage --time-period Start=2026-07-01,End=2026-07-28 --granularity MONTHLY \\
          --metrics BlendedCost --group-by Type=DIMENSION,Key=SERVICE
        aws budgets describe-budgets --account-id $(aws sts get-caller-identity --query Account --output text)
        aws cloudwatch describe-alarms --alarm-names rebash-lab-monthly
        aws freetier get-free-tier-usage --region us-east-1
        aws account get-contact-information
        aws account get-alternate-contact --alternate-contact-type BILLING
        ```

        | Cost trap | Detection | Mitigation |
        |-----------|-----------|------------|
        | NAT Gateway | Cost Explorer `Amazon VPC` spike | SSM + endpoints in labs |
        | Idle ALB | ELB line item daily | Delete after lab |
        | Orphan EBS | `describe-volumes --filters Name=status,Values=available` | Weekly janitor script |
        | RDS storage | RDS snapshot/storage lines | Destroy instances; limit retention |
        """,
    )
    _register_extended(
        "iam-fundamentals",
        """
        ```bash
        aws iam generate-credential-report
        aws iam get-credential-report --query 'Content' --output text | base64 -d | column -t -s,
        aws iam list-roles --max-items 20
        aws iam get-role --role-name rebash-ec2-ssm-role
        aws iam simulate-custom-policy --policy-input-list file://policy.json \\
          --action-names ec2:DescribeInstances s3:ListAllMyBuckets --resource-arns '*'
        aws iam list-attached-role-policies --role-name rebash-ec2-ssm-role
        aws accessanalyzer list-analyzers
        ```

        Prefer **roles** with `sts:AssumeRole` for humans via SSO. Enforce **MFA** on root and admins.
        Never use root for daily CLI. Review the credential report monthly.
        """,
    )
    _register_extended(
        "aws-cli-credentials-and-profiles",
        """
        ```bash
        aws configure list-profiles
        aws configure get region --profile rebash-lab
        aws sts get-session-token --duration-seconds 3600 --profile rebash-lab
        aws sso login --profile rebash-sso && aws sts get-caller-identity --profile rebash-sso
        AWS_PAGER="" aws ec2 describe-instances --profile rebash-lab --query 'Reservations[].Instances[].InstanceId'
        aws history list | tail
        ```

        | Profile pattern | Example |
        |-----------------|---------|
        | Lab account | `rebash-lab` |
        | SSO admin | `rebash-sso` |
        | LocalStack | env vars + `--endpoint-url` |
        """,
    )
    _register_extended(
        "vpc-subnets-and-multi-az-design",
        """
        ```bash
        aws ec2 describe-vpcs --filters Name=tag:Environment,Values=lab
        aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC_ID --output table
        aws ec2 describe-route-tables --filters Name=vpc-id,Values=$VPC_ID
        aws ec2 describe-network-acls --filters Name=vpc-id,Values=$VPC_ID
        aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames
        aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-support
        ```

        Cross-read [Cloud Networking: VPC and Subnets](../networking/cloud-networking-vpc-and-subnets.md).
        """,
    )
    _register_extended(
        "internet-gateways-routes-and-egress",
        """
        ```bash
        aws ec2 describe-internet-gateways --filters Name=attachment.vpc-id,Values=$VPC_ID
        aws ec2 describe-route-tables --filters Name=vpc-id,Values=$VPC_ID --query 'RouteTables[].Routes'
        aws ec2 describe-nat-gateways --filter Name=vpc-id,Values=$VPC_ID
        aws ec2 describe-addresses --filters Name=domain,Values=vpc
        aws ssm describe-instance-information --filters Key=PingStatus,Values=Online
        ```

        **NAT Gateway COST warning:** destroy same session. Prefer public subnet + SSM for labs.
        """,
    )
    _register_extended(
        "security-groups-and-nacls",
        """
        ```bash
        aws ec2 describe-security-groups --filters Name=vpc-id,Values=$VPC_ID --output table
        aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 443 --source-group sg-alb
        aws ec2 describe-network-acls --filters Name=vpc-id,Values=$VPC_ID
        aws ec2 create-network-acl-entry --network-acl-id acl-xxx --ingress --rule-number 200 --protocol -1 \\
          --rule-action allow --cidr-block 0.0.0.0/0
        aws ec2 describe-security-group-rules --filters Name=group-id,Values=$WEB_SG
        ```
        """,
    )
    _register_extended(
        "vpc-endpoints-and-private-aws-access",
        """
        ```bash
        aws ec2 describe-vpc-endpoints --filters Name=vpc-id,Values=$VPC_ID
        aws ec2 create-vpc-endpoint --vpc-id $VPC_ID --service-name com.amazonaws.eu-west-1.s3 --route-table-ids $RTB_ID
        aws ec2 modify-vpc-endpoint --vpc-endpoint-id vpce-xxx --private-dns-enabled
        aws ec2 describe-prefix-lists --filters Name=prefix-list-name,Values=com.amazonaws.eu-west-1.s3
        ```
        """,
    )
    _register_extended(
        "ec2-fundamentals",
        """
        ```bash
        aws ec2 describe-instance-types --filters Name=free-tier-eligible,Values=true --query 'InstanceTypes[].InstanceType'
        aws ec2 run-instances --count 1 --instance-type t3.micro --metadata-options HttpTokens=required
        aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[].Instances[].State.Name'
        aws ec2 stop-instances --instance-ids $INSTANCE_ID
        aws ec2 terminate-instances --instance-ids $INSTANCE_ID
        aws ec2 describe-volumes --filters Name=attachment.instance-id,Values=$INSTANCE_ID
        ```
        """,
    )
    _register_extended(
        "user-data-imds-and-ssm-session-manager",
        """
        ```bash
        aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[].Instances[].MetadataOptions'
        TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
        curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/
        aws ssm start-session --target $INSTANCE_ID
        aws ssm describe-sessions --state History
        ```
        """,
    )
    _register_extended(
        "ebs-volumes-snapshots-and-encryption",
        """
        ```bash
        aws ec2 create-volume --availability-zone eu-west-1a --size 10 --volume-type gp3 --encrypted
        aws ec2 create-snapshot --volume-id vol-xxx --description "nightly backup"
        aws ec2 describe-snapshots --owner-ids self
        aws ec2 enable-ebs-encryption-by-default
        aws ec2 get-ebs-encryption-by-default
        aws dlm create-lifecycle-policy --execution-role-arn arn:aws:iam::ACCOUNT:role/DLMRole --policy-details file://dlm.json
        ```
        """,
    )
    _register_extended(
        "s3-fundamentals",
        """
        ```bash
        aws s3api list-buckets --query 'Buckets[].Name'
        aws s3api get-bucket-versioning --bucket $BUCKET
        aws s3api put-bucket-versioning --bucket $BUCKET --versioning-configuration Status=Enabled
        aws s3api get-bucket-encryption --bucket $BUCKET
        aws s3api put-object --bucket $BUCKET --key logs/2026/07/app.log --body ./app.log
        aws s3api list-objects-v2 --bucket $BUCKET --prefix logs/
        aws s3api get-bucket-lifecycle-configuration --bucket $BUCKET
        aws s3api delete-bucket --bucket $BUCKET  # after emptying — always teardown lab buckets
        ```

        Empty buckets with `aws s3 rm s3://$BUCKET --recursive` before deletion. Confirm **Block Public Access**
        remains enabled and verify **billing alarms** after any transfer-heavy experiment.
        """,
    )
    _register_extended(
        "s3-security-and-static-hosting",
        """
        ```bash
        aws s3api get-public-access-block --bucket $BUCKET
        aws s3api put-bucket-policy --bucket $BUCKET --policy file://policy-oac.json
        aws cloudfront create-distribution --distribution-config file://cf.json
        aws cloudfront create-invalidation --distribution-id E123 --paths "/*"
        aws s3api get-bucket-website --bucket $BUCKET
        ```
        """,
    )
    _register_extended(
        "elastic-load-balancing-alb-and-nlb",
        """
        ```bash
        aws elbv2 describe-load-balancers --names rebash-alb
        aws elbv2 describe-target-health --target-group-arn $TG_ARN
        aws elbv2 modify-target-group --target-group-arn $TG_ARN --health-check-interval-seconds 30
        aws elbv2 describe-rules --listener-arn $LISTENER_ARN
        aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN
        ```

        **ALB cost warning:** delete load balancer same session after validation.
        """,
    )
    _register_extended(
        "route-53-dns-and-health-checks",
        """
        ```bash
        aws route53 list-hosted-zones-by-name --dns-name lab.example
        aws route53 get-hosted-zone --id $ZONE_ID
        aws route53 list-resource-record-sets --hosted-zone-id $ZONE_ID
        aws route53 change-resource-record-sets --hosted-zone-id $ZONE_ID --change-batch file://upsert.json
        aws route53 list-health-checks
        dig +trace app.lab.example @8.8.8.8
        aws route53 delete-health-check --health-check-id $HC_ID
        ```

        Delete unused **health checks** during teardown — they incur small recurring charges. Confirm **billing alarms**
        after creating hosted zones in a real account.
        """,
    )
    _register_extended(
        "rds-fundamentals",
        """
        ```bash
        aws rds describe-db-instances --db-instance-identifier rebash-lab-db
        aws rds describe-db-subnet-groups --db-subnet-group-name rebash-db-subnets
        aws rds modify-db-instance --db-instance-identifier rebash-lab-db --backup-retention-period 7
        aws rds create-db-snapshot --db-instance-identifier rebash-lab-db --db-snapshot-identifier rebash-lab-snap
        aws rds delete-db-instance --db-instance-identifier rebash-lab-db --skip-final-snapshot
        ```

        **Destroy RDS ASAP** after lab validation.
        """,
    )
    _register_extended(
        "auto-scaling-groups-and-launch-templates",
        """
        ```bash
        aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names rebash-web-asg
        aws autoscaling describe-scaling-activities --auto-scaling-group-name rebash-web-asg
        aws autoscaling put-scaling-policy --auto-scaling-group-name rebash-web-asg \\
          --policy-name cpu-target --policy-type TargetTrackingScaling --target-tracking-configuration file://tt.json
        aws ec2 describe-launch-template-versions --launch-template-name rebash-web-lt
        aws autoscaling start-instance-refresh --auto-scaling-group-name rebash-web-asg
        ```
        """,
    )
    _register_extended(
        "cloudwatch-metrics-logs-and-alarms",
        """
        ```bash
        aws cloudwatch list-metrics --namespace AWS/EC2 --dimensions Name=InstanceId,Value=$INSTANCE_ID
        aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization \\
          --start-time 2026-07-28T00:00:00Z --end-time 2026-07-28T01:00:00Z --period 300 --statistics Average
        aws logs filter-log-events --log-group-name /rebash/lab/app --filter-pattern "ERROR"
        aws logs put-retention-policy --log-group-name /rebash/lab/app --retention-in-days 7
        aws cloudwatch describe-alarms --alarm-names rebash-high-cpu
        ```
        """,
    )
    _register_extended(
        "cloudtrail-config-and-account-guardrails",
        """
        ```bash
        aws cloudtrail describe-trails
        aws cloudtrail get-trail-status --name rebash-org-trail
        aws cloudtrail lookup-events --max-results 10
        aws configservice describe-configuration-recorders
        aws configservice describe-config-rules --config-rule-names s3-bucket-public-read-prohibited
        aws organizations describe-organization
        aws organizations list-policies --filter SERVICE_CONTROL_POLICY
        ```
        """,
    )
    _register_extended(
        "lambda-and-three-tier-capstone",
        """
        ```bash
        aws lambda list-functions --query 'Functions[].FunctionName'
        aws lambda get-function --function-name rebash-capstone-fn
        aws lambda update-function-code --function-name rebash-capstone-fn --zip-file fileb://function.zip
        aws apigatewayv2 create-api --name rebash-http --protocol-type HTTP
        aws lambda add-permission --function-name rebash-capstone-fn --statement-id apigw --action lambda:InvokeFunction \\
          --principal apigateway.amazonaws.com
        ```

        Continue with [Terraform production capstone](../terraform/production-patterns-and-capstone.md).
        """,
    )


def render(t: dict) -> str:
    num = t["num"]
    tags_yaml = "\n".join(f"  - {x}" for x in t["tags"])
    prereq_yaml = "\n".join(f"  - {x}" for x in t["prereq"])
    prereq_body = "\n".join(f"- {x}" for x in t["prereq"])
    objectives = "\n".join(f"- [ ] {x}" for x in t["objectives"])
    mistakes = render_mistakes(t["mistakes"])
    interview = render_interview(t["interview_q"], t.get("interview_tips", []))
    related = related_links(num, t["slug"], t.get("related_extra"))
    refs = "\n".join(f"{i}. [{n}]({u})" for i, (n, u) in enumerate(t["refs"], 1))
    desc = t["overview"].strip().splitlines()[0][:160]
    extra_warnings = t.get("extra_warnings", "")
    cross = t.get("cross_links_section", "")
    deep_dive = extended_deep_dive(t)

    return f"""---
title: {t['title']}
description: "{desc.replace('"', "'")}"
difficulty: {t['difficulty']}
estimated_time: "{t['minutes']}"
author: {AUTHOR}
last_updated: "{LAST_UPDATED}"
category: aws
tags:
{tags_yaml}
prerequisites:
{prereq_yaml}
comments: false
---

# {t['title']}

## Overview

{t['overview'].strip()}

This is **Tutorial {num}** in **{t['module']}** of the REBASH Academy AWS track.

{billing_reminder().strip()}

{extra_warnings.strip()}

## Prerequisites

{prereq_body}

## Learning Objectives

By the end of this tutorial, you will be able to:

{objectives}

## Architecture

![Architecture diagram for {t['title']}](../assets/images/{t['slug']}.svg)

{t.get('architecture_notes', '').strip()}

## Theory

{t['theory'].strip()}

## Hands-on Lab

{t['lab'].strip()}

## Validation

{t['validation'].strip()}

## Code Walkthrough

{t['walkthrough'].strip()}

## Security Considerations

{t['security'].strip()}

## Common Mistakes

{mistakes}

## Best Practices

{t['best_practices'].strip()}

## Troubleshooting

{t['troubleshooting'].strip()}

{deep_dive.strip()}

## Summary

{t['summary'].strip()}

## Interview Questions

{interview}

## Related Tutorials

{related}

{cross.strip()}

## References

{refs}
"""


def main() -> None:
    populate_extended_blocks()
    OUT.mkdir(parents=True, exist_ok=True)
    for t in TUTORIALS:
        path = OUT / f"{t['slug']}.md"
        path.write_text(render(t), encoding="utf-8")
        print(path.relative_to(ROOT))
    print(f"done — {len(TUTORIALS)} tutorials")


def load_tutorials() -> None:
    """Register all 20 AWS tutorials."""
    _load_module1()
    _load_module2()
    _load_module3()
    _load_module4()
    _load_module5()
    _load_module6()


def _load_module1() -> None:
    T(
        num=1,
        slug="introduction-to-aws-and-global-infrastructure",
        title="Introduction to AWS and Global Infrastructure",
        module="Module 1: Foundations",
        difficulty="beginner",
        minutes="35 min",
        tags=["aws", "regions", "availability-zones", "global-infrastructure", "foundations"],
        prereq=[
            "Completed the [Networking](../networking/index.md) fundamentals track (or equivalent TCP/IP awareness)",
            "Comfortable using a terminal on Linux, macOS, or WSL",
            "An email address if you plan to create a Free Tier account in a later tutorial",
        ],
        overview=dedent(
            """\
            Amazon Web Services (AWS) is the largest public cloud provider. Before you launch a single EC2
            instance, you need a mental map of **Regions**, **Availability Zones**, **Edge Locations**,
            and the **shared responsibility model** — otherwise every service name feels arbitrary.

            This tutorial explains how AWS organises infrastructure globally, how to choose a Region for
            labs, and how AWS partitions responsibility between you and the provider. You will explore
            the console and CLI read-only commands so you understand where resources live and why latency
            and compliance start with Region selection.
            """
        ),
        architecture_notes=dedent(
            """\
            | Layer | What it is | Lab relevance |
            |-------|------------|---------------|
            | **Region** | Geographic area (e.g. `eu-west-1`) | All resources are Regional unless stated |
            | **Availability Zone (AZ)** | Isolated data centre group within a Region | Multi-AZ designs for resilience |
            | **Local Zone / Wavelength** | Edge extensions | Low-latency special cases — skip in Module 1 |
            | **Edge location** | CloudFront / Route 53 caching | Covered in later edge tutorials |
            """
        ),
        objectives=[
            "Explain Regions, AZs, and why most resources are Regional",
            "Describe the AWS shared responsibility model in plain language",
            "List major global services (IAM, Route 53, CloudFront) versus Regional ones (EC2, VPC)",
            "Choose a sensible home Region for Free Tier labs",
            "Navigate the AWS Management Console and run read-only CLI discovery commands",
        ],
        theory=dedent(
            """\
            ### Regions and Availability Zones

            A **Region** is a named geographic area (`us-east-1`, `eu-west-1`, `ap-southeast-2`). Each
            Region contains multiple **Availability Zones** — physically separate data centres with
            independent power and networking, connected by low-latency links.

            | Concept | Analogy | Production note |
            |---------|---------|-----------------|
            | Region | Country or metro area | Data residency and latency |
            | AZ | Separate campus building | Spread tiers across ≥2 AZs |
            | Edge location | CDN cache near users | Static content, DNS caching |

            For REBASH Academy labs, pick **one Region** and stay there unless a tutorial says otherwise.
            `eu-west-1` (Ireland) and `us-east-1` (N. Virginia) are common choices; `us-east-1` often has
            the newest services first, whilst `eu-west-1` suits many European learners.

            ### Global vs Regional services

            | Scope | Examples | Implication |
            |-------|----------|-------------|
            | **Global** | IAM, Route 53 (hosted zones), CloudFront | Names are global; policies apply account-wide |
            | **Regional** | EC2, VPC, S3 buckets, RDS | ARNs include Region; failures can be Regional |
            | **AZ-scoped** | Subnets, EC2 instances | You choose AZ at launch |

            ### Shared responsibility model

            AWS secures **of** the cloud (hardware, hypervisor, physical facilities). You secure **in**
            the cloud (OS patches on EC2, IAM policies, encryption choices, security group rules).

            | AWS responsible | You responsible |
            |-----------------|-----------------|
            | Physical security | Guest OS and application patches |
            | Hypervisor | IAM users, roles, MFA |
            | Managed service patching (e.g. RDS engine) | Network configuration, open ports |
            | Global infrastructure resilience | Data classification and backup strategy |

            ### Account, Organisation, and landing zone (preview)

            An **AWS account** is a hard billing and security boundary. **AWS Organizations** lets you
            consolidate billing and apply **service control policies (SCPs)** across member accounts. You
            will create a single Free Tier account in the next tutorial; enterprise teams use multi-account
            strategies (separate accounts for prod/non-prod/logging).

            ### Console vs CLI vs Infrastructure as Code

            The console is excellent for discovery. The CLI scales for scripts and matches what
            [Terraform](../terraform/index.md) providers call under the hood. Production teams favour
            version-controlled IaC; the console remains useful for support and incident triage.
            """
        ),
        lab=dedent(
            """\
            ### Path A — AWS Free Tier (read-only discovery)

            Sign in to the [AWS Management Console](https://console.aws.amazon.com/). Note the Region
            selector (top-right). Switch to your chosen lab Region and leave it there for the whole track.

            ```bash
            aws --version
            aws configure list
            aws ec2 describe-regions --query 'Regions[].RegionName' --output table
            aws ec2 describe-availability-zones --region eu-west-1 --query 'AvailabilityZones[].ZoneName' --output table
            aws sts get-caller-identity
            ```

            **Expected:** Your account ID, user/role ARN, and a table of AZ names like `eu-west-1a`.

            Browse **Services → EC2 → Account attributes** and **VPC** to see default VPC presence (varies
            by account age). Do **not** launch billable resources yet.

            ### Path B — LocalStack (CLI shape only)

            """
        )
        + localstack_tip(
            """\
            aws --endpoint-url=http://localhost:4566 ec2 describe-regions --output table
            aws --endpoint-url=http://localhost:4566 sts get-caller-identity
            """
        )
        + dedent(
            """\
            ### Step — Document your lab Region

            Create `~/rebash-aws/region.txt`:

            ```bash
            mkdir -p ~/rebash-aws
            echo "LAB_REGION=eu-west-1" >> ~/rebash-aws/region.txt
            ```

            Use this Region in every subsequent tutorial unless instructed otherwise.
            """
        ),
        validation=dedent(
            """\
            | Check | Command / action | Pass criteria |
            |-------|------------------|---------------|
            | CLI installed | `aws --version` | Version 2.x shown |
            | Identity | `aws sts get-caller-identity` | Account, ARN returned |
            | Regions | `aws ec2 describe-regions` | Table of Region codes |
            | AZs | `aws ec2 describe-availability-zones --region $LAB_REGION` | ≥3 AZs listed |
            | Console | Region selector | Matches `$LAB_REGION` |
            """
        ),
        walkthrough=dedent(
            """\
            | Command / area | Purpose |
            |----------------|---------|
            | `aws ec2 describe-regions` | Lists opt-in and standard Regions |
            | `aws ec2 describe-availability-zones` | AZ names for VPC subnet planning |
            | `aws sts get-caller-identity` | Confirms which account and principal the CLI uses |
            | Console Region selector | Every Regional API call uses this default in the console |
            | Shared responsibility | Guides what you harden in later IAM and EC2 tutorials |
            """
        ),
        security=dedent(
            """\
            - Do not share root account credentials; enable MFA on root when you create an account
            - Use IAM users or roles for daily CLI access — covered in the next modules
            - Read-only discovery commands are safe; avoid creating resources until you understand billing
            - Record which Region stores data for compliance discussions with your organisation
            """
        ),
        mistakes=[
            ("Mixing Regions across tutorials", "Resources in `eu-west-1` cannot attach to a VPC in `us-east-1`.", "Pick one lab Region and export `AWS_DEFAULT_REGION`."),
            ("Assuming all services are global", "EC2 and VPC are Regional; ARNs include the Region.", "Check the service chapter in AWS documentation for scope."),
            ("Ignoring AZ labels", "`eu-west-1a` maps to different physical AZs per account.", "Use AZ IDs (`use1-az1`) in automation when absolute consistency matters."),
        ],
        best_practices=dedent(
            """\
            - Standardise a lab Region in team documentation
            - Design multi-AZ for production tiers; single-AZ is acceptable for short Free Tier labs
            - Prefer CLI or IaC once past discovery — reproducible and reviewable
            - Enable MFA on the root user and avoid daily root sign-in
            - Set billing alarms before launching EC2 or RDS (next tutorials)
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Likely cause | Fix |
            |-------|--------------|-----|
            | `Unable to locate credentials` | CLI not configured | Run `aws configure` or use SSO profile (Tutorial 4) |
            | Empty Region list | Wrong partition or endpoint | Use real AWS endpoints; check `AWS_DEFAULT_REGION` |
            | Access denied on describe | IAM policy missing read | Use an administrator lab user temporarily; tighten in Tutorial 3 |
            | Console shows different Region than CLI | Separate defaults | Align `AWS_DEFAULT_REGION` with console selector |
            """
        ),
        summary=dedent(
            """\
            - AWS organises compute and networking into **Regions** and **AZs**; most lab resources are Regional
            - **IAM** is global; **EC2/VPC** are Regional — always check scope
            - The **shared responsibility model** defines what AWS patches versus what you must harden
            - Choose one lab Region, verify identity with `sts get-caller-identity`, and enable billing alarms before billable labs
            """
        ),
        interview_q=[
            "What is the difference between an AWS Region and an Availability Zone?",
            "Which AWS services are global versus Regional? Give three examples of each.",
            "Explain the shared responsibility model for EC2 versus RDS.",
            "Why might two accounts see different physical mappings for `eu-west-1a`?",
            "How does Region choice affect latency and compliance?",
            "What is an AWS account boundary used for?",
            "When would you use more than one Region in production?",
            "How do you verify which account the CLI is using?",
            "Why is `us-east-1` special for some global services?",
            "What should you configure before launching billable resources in a new account?",
        ],
        interview_tips=[
            (
                1,
                "A Region is a geographic area containing multiple isolated AZs (separate data centres). "
                "AZs within a Region are connected with low-latency links; you spread resilient workloads "
                "across AZs, not across Regions unless you need disaster recovery or data residency in two areas.",
            ),
            (
                3,
                "For EC2, AWS secures the hardware and hypervisor; you patch the guest OS, configure "
                "security groups, and manage application secrets. For RDS, AWS manages more of the stack "
                "(engine patching options, storage infrastructure); you still control network access, IAM "
                "authentication, and encryption settings.",
            ),
        ],
        refs=[
            ("AWS Global Infrastructure", "https://docs.aws.amazon.com/general/latest/gr/rande.html"),
            ("Regions and Availability Zones", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html"),
            ("Shared Responsibility Model", "https://docs.aws.amazon.com/whitepapers/latest/aws-overview/shared-responsibility-model.html"),
            ("AWS CLI configure", "https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html"),
            ("AWS Free Tier", "https://aws.amazon.com/free/"),
        ],
    )

    T(
        num=2,
        slug="accounts-free-tier-billing-and-cost-hygiene",
        title="Accounts, Free Tier, Billing, and Cost Hygiene",
        module="Module 1: Foundations",
        difficulty="beginner",
        minutes="40 min",
        tags=["aws", "billing", "free-tier", "cost-management", "budgets"],
        prereq=[
            "Completed [Introduction to AWS and Global Infrastructure](introduction-to-aws-and-global-infrastructure.md)",
            "Email address and payment method for AWS account creation (Free Tier still requires a card)",
            "Access to root email inbox for verification",
        ],
        overview=dedent(
            """\
            Surprise cloud bills usually come from forgotten NAT Gateways, idle load balancers, or RDS instances
            left running overnight — not from malicious attacks. This tutorial walks through creating an
            account safely, enabling **MFA on root**, setting **billing alarms**, reading **Cost Explorer**,
            and understanding **Free Tier** limits.

            You will configure AWS Budgets, enable cost anomaly detection where available, and adopt a destroy
            discipline every lab session. Cost hygiene is a core production skill, not an finance afterthought.
            """
        ),
        objectives=[
            "Create or verify an AWS account with MFA enabled on the root user",
            "Enable IAM access to billing and create a monthly cost budget with email alerts",
            "Explain Free Tier categories and common billable traps (NAT, ALB, RDS)",
            "Use Cost Explorer and billing dashboards to find running resources",
            "Apply a lab teardown checklist before closing your session",
        ],
        theory=dedent(
            """\
            ### Account creation and root hygiene

            The **root user** owns the account and can do anything, including closing it. Production rule:
            **enable MFA on root**, store root credentials offline, and **never use root for daily work**.

            | Identity | Use for |
            |----------|---------|
            | Root | Account recovery, rare billing tasks only |
            | IAM admin user/role | Day-one setup, then delegate |
            | IAM role | EC2, Lambda, CI — no long-lived keys |

            ### Free Tier (high level)

            Free Tier offers limited usage for 12 months (account creation date) and some always-free services.
            Limits are **per service**, not a single pool of credits. Always check the official Free Tier page
            before launching:

            - **EC2** — limited hours of specific instance types per month
            - **S3** — limited storage and requests
            - **RDS** — limited db.t2/db.t3 hours in eligible Regions
            - **Not Free Tier** — NAT Gateway hourly + data processing, Application Load Balancer hours, many EIPs when unattached

            ### Cost allocation and tags

            Tags (`Environment=lab`, `Owner=rebash`) appear in Cost Explorer when activated. Tag every lab
            resource you create; untagged resources are hard to attribute during triage.

            ### Billing alarms vs Budgets vs Anomaly Detection

            | Tool | Purpose |
            |------|---------|
            | **Billing alarm (CloudWatch)** | Legacy metric on estimated charges |
            | **AWS Budgets** | Threshold alerts on cost or usage |
            | **Cost Anomaly Detection** | ML-assisted spikes |

            For labs, a **Budget** at `$5` or `$10` with email notification is a sensible default.

            ### Teardown discipline

            Before you stop for the day:

            1. Delete EC2 instances and volumes you do not need
            2. Remove NAT Gateways and Elastic IPs
            3. Delete RDS instances (skip snapshots in labs unless required)
            4. Empty and delete S3 buckets created for tests
            5. Confirm **Cost Explorer → Last 7 days** shows near-zero after cleanup
            """
        ),
        lab=dedent(
            """\
            ### Step 1 — Secure the root user

            1. Sign in as root → **IAM** → **Security credentials**
            2. Enable **MFA** on root (virtual authenticator app)
            3. Do **not** create access keys for root

            ### Step 2 — Enable IAM access to billing

            **Account** → **IAM user and role access to Billing information** → **Activate**.

            ### Step 3 — Create a billing budget (console)

            **Billing** → **Budgets** → **Create budget** → **Cost budget** → `$10` monthly → email alert at
            80% and 100%.

            CLI (after budget permissions exist):

            ```bash
            aws budgets create-budget \\
              --account-id $(aws sts get-caller-identity --query Account --output text) \\
              --budget file://budget.json \\
              --notifications-with-subscribers file://notifications.json
            ```

            Example `budget.json`:

            ```json
            {
              "BudgetName": "rebash-lab-monthly",
              "BudgetLimit": {"Amount": "10", "Unit": "USD"},
              "TimeUnit": "MONTHLY",
              "BudgetType": "COST"
            }
            ```

            ### Step 4 — Review Cost Explorer

            Open **Cost Explorer** → last 7 days → group by **Service**. Baseline should be near zero before
            compute labs.

            ### Step 5 — Lab teardown template

            Save `~/rebash-aws/teardown-checklist.md` with EC2, EIP, NAT, ALB, RDS, S3 sections — use it after
            every hands-on session.

            """
        )
        + localstack_tip(
            "# Billing APIs are not emulated — use the real account for this tutorial only.\n"
            "aws --endpoint-url=http://localhost:4566 sts get-caller-identity  # identity practice only"
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Root MFA | Console shows MFA enabled for root |
            | Budget | Budget visible with email subscriber |
            | IAM billing access | IAM user can open Billing dashboard |
            | Cost Explorer | Loads with zero or minimal spend pre-lab |
            | Teardown doc | Checklist saved locally |
            """
        ),
        walkthrough=dedent(
            """\
            | Item | Why it matters |
            |------|----------------|
            | Root MFA | Stops credential stuffing from owning your account |
            | Budget alerts | Early warning before a NAT weekend bill |
            | Cost Explorer grouping | Finds which service leaked spend |
            | Tags | Identifies lab vs personal experiments |
            | Teardown checklist | Habit beats memory after long labs |
            """
        ),
        security=dedent(
            """\
            - Never commit AWS access keys to Git
            - Root MFA is mandatory; prefer IAM roles over users where possible
            - Billing alerts go to a monitored inbox, not a throwaway address
            - Review **IAM Credential Report** monthly in production accounts
            """
        ),
        mistakes=[
            ("Leaving NAT Gateway running", "NAT charges hourly plus data processing.", "Use public subnet + SSM for labs; destroy NAT same session."),
            ("Unattached Elastic IPs", "AWS charges for idle public IPs.", "Release EIPs in teardown checklist."),
            ("Using root for CLI daily", "Maximum blast radius.", "Create IAM admin with MFA; use roles on compute."),
        ],
        best_practices=dedent(
            """\
            - Budget + anomaly detection on every account
            - Tag `Environment`, `Owner`, `Ticket` on all resources
            - Automate teardown with scripts or Terraform destroy
            - Review Free Tier page before each new service lab
            - Use **AWS Pricing Calculator** for architecture estimates
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | Cannot create budget | IAM billing access off | Activate in account settings |
            | Unexpected charge | NAT/ALB/RDS | Cost Explorer → service; delete resource |
            | Free Tier exceeded | Wrong instance class | Switch to eligible instance type or destroy |
            | No budget email | SNS spam or wrong address | Confirm subscriber email confirmed |
            """
        ),
        summary=dedent(
            """\
            - Secure root with MFA; do not use root daily
            - Configure **Budgets** and read **Cost Explorer** before billable labs
            - Free Tier is per-service with exceptions — NAT and ALB are common traps
            - Destroy resources and run the teardown checklist every session
            """
        ),
        interview_q=[
            "Why should MFA be enabled on the root user?",
            "Name three AWS services that are commonly not covered by Free Tier.",
            "What is the difference between a Budget and a billing alarm?",
            "How do tags help with cost allocation?",
            "What steps would you take if Cost Explorer shows a spike in EC2 spend?",
            "Why avoid long-lived IAM access keys on laptops?",
            "What is the shared billing benefit of AWS Organizations?",
            "How often should you review the IAM credential report?",
            "What should a lab teardown checklist include?",
            "When is it acceptable to leave an RDS instance running overnight?",
        ],
        interview_tips=[
            (
                1,
                "Root can change billing, close the account, and bypass most guardrails. MFA adds a second "
                "factor so stolen passwords alone cannot compromise the account. Daily work should use IAM "
                "roles with least privilege, not root.",
            ),
            (
                10,
                "In production, RDS may run continuously with backups and monitoring. In Free Tier **labs**, "
                "never — destroy RDS immediately after validation to avoid storage and instance charges; "
                "snapshots also cost money if retained.",
            ),
        ],
        refs=[
            ("AWS Billing and Cost Management", "https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html"),
            ("AWS Free Tier", "https://aws.amazon.com/free/"),
            ("AWS Budgets", "https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html"),
            ("IAM best practices", "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html"),
        ],
    )

    # Tutorials 3-5 continue in _load_module1 part 2
    _load_module1_part2()


def _load_module1_part2() -> None:
    T(
        num=3,
        slug="iam-fundamentals",
        title="IAM Fundamentals",
        module="Module 1: Foundations",
        difficulty="beginner",
        minutes="50 min",
        tags=["aws", "iam", "roles", "policies", "least-privilege", "mfa"],
        prereq=[
            "Completed [Accounts, Free Tier, Billing, and Cost Hygiene](accounts-free-tier-billing-and-cost-hygiene.md)",
            "Root MFA enabled; billing budget configured",
            "AWS CLI installed",
        ],
        overview=dedent(
            """\
            **Identity and Access Management (IAM)** is the control plane for who can call which AWS APIs.
            Every production incident involving public S3 buckets or crypto-mining EC2 instances traces back
            to IAM decisions — roles, policies, or missing MFA.

            You will create groups and users sparingly, attach **least-privilege policies**, create an **IAM role**
            for EC2, and enforce **MFA**. Prefer **roles** over long-lived access keys wherever possible.
            """
        ),
        objectives=[
            "Explain users, groups, roles, and policies with correct use cases",
            "Write and attach a least-privilege IAM policy using JSON",
            "Create an EC2 instance profile role and trust policy",
            "Enable MFA for an IAM user and test denied-without-MFA patterns",
            "Run `aws iam simulate-principal-policy` to validate permissions",
        ],
        theory=dedent(
            """\
            ### IAM building blocks

            | Entity | Purpose | Production preference |
            |--------|---------|------------------------|
            | **User** | Human or long-lived CLI | Avoid except break-glass admin |
            | **Group** | Bundle permissions for users | OK for small teams |
            | **Role** | Temporary credentials via STS | **Default for EC2, Lambda, CI** |
            | **Policy** | JSON allow/deny document | Least privilege, many small policies |

            IAM is **global** — policies apply account-wide regardless of Region.

            ### Policy structure

            ```json
            {
              "Version": "2012-10-17",
              "Statement": [{
                "Effect": "Allow",
                "Action": ["s3:ListBucket"],
                "Resource": "arn:aws:s3:::my-bucket",
                "Condition": {"Bool": {"aws:MultiFactorAuthPresent": "true"}}
              }]
            }
            ```

            - **Identity-based policies** attach to users, groups, roles
            - **Resource-based policies** attach to S3 buckets, KMS keys, etc.
            - **Permission boundaries** cap maximum permissions (advanced)

            ### Roles and trust policies

            A **role** has two parts: permissions policy (what it can do) and **trust policy** (who can
            assume it). EC2 assumes a role via an **instance profile**:

            ```json
            {
              "Version": "2012-10-17",
              "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole"
              }]
            }
            ```

            ### Least privilege workflow

            1. Start with AWS managed **ReadOnly** or job-function policies for discovery
            2. Narrow actions and resources based on CloudTrail `AccessDenied` logs
            3. Prefer **roles** + SSO in organisations; never embed keys in user-data

            ### MFA

            Require MFA for console users and sensitive API calls using `Condition` keys. Root MFA is
            mandatory; IAM user MFA strongly recommended for admins.
            """
        ),
        lab=dedent(
            """\
            ### Step 1 — Create lab group and user (console or CLI)

            ```bash
            aws iam create-group --group-name rebash-lab-admins
            aws iam attach-group-policy --group-name rebash-lab-admins \\
              --policy-arn arn:aws:iam::aws:policy/IAMUserChangePassword
            aws iam create-user --user-name rebash.lab
            aws iam add-user-to-group --user-name rebash.lab --group-name rebash-lab-admins
            ```

            Attach a custom least-privilege policy for EC2 read in one Region (create `ec2-read-lab.json` first).

            ### Step 2 — Enable MFA for the lab user

            Console: **IAM → Users → rebash.lab → Security credentials → Assign MFA device**.

            ### Step 3 — Create EC2 role + instance profile

            ```bash
            aws iam create-role --role-name rebash-ec2-ssm-role \\
              --assume-role-policy-document file://trust-ec2.json
            aws iam attach-role-policy --role-name rebash-ec2-ssm-role \\
              --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
            aws iam create-instance-profile --instance-profile-name rebash-ec2-ssm-profile
            aws iam add-role-to-instance-profile \\
              --instance-profile-name rebash-ec2-ssm-profile \\
              --role-name rebash-ec2-ssm-role
            ```

            ### Step 4 — Simulate policy

            ```bash
            aws iam simulate-principal-policy \\
              --policy-source-arn arn:aws:iam::ACCOUNT_ID:user/rebash.lab \\
              --action-names ec2:DescribeInstances s3:DeleteBucket
            ```

            ### Step 5 — Cleanup

            ```bash
            aws iam remove-role-from-instance-profile \\
              --instance-profile-name rebash-ec2-ssm-profile \\
              --role-name rebash-ec2-ssm-role
            aws iam delete-instance-profile --instance-profile-name rebash-ec2-ssm-profile
            aws iam detach-role-policy --role-name rebash-ec2-ssm-role \\
              --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
            aws iam delete-role --role-name rebash-ec2-ssm-role
            # delete user, group, custom policies when finished
            ```

            """
        )
        + localstack_tip(
            """\
            aws --endpoint-url=http://localhost:4566 iam create-user --user-name rebash.lab
            aws --endpoint-url=http://localhost:4566 iam list-users
            """
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | User MFA | Console shows MFA device assigned |
            | Role trust | `ec2.amazonaws.com` in trust policy |
            | SSM policy | `AmazonSSMManagedInstanceCore` attached to role |
            | Simulation | `DeleteBucket` simulated as denied for read-only user |
            | Cleanup | No orphan instance profiles or test users left |
            """
        ),
        walkthrough=dedent(
            """\
            | Component | Detail |
            |-----------|--------|
            | Trust policy | Defines **who** can assume the role (service principal for EC2) |
            | Permissions policy | Defines **what** API actions are allowed |
            | Instance profile | Container attaching a role to an EC2 instance at launch |
            | `simulate-principal-policy` | Tests policy without live API calls |
            | MFA condition | Adds `aws:MultiFactorAuthPresent` requirement for sensitive actions |
            """
        ),
        security=dedent(
            """\
            - Prefer **roles** over IAM users with access keys on laptops
            - Enable MFA on all privileged IAM users; never disable for convenience
            - Do not use `AdministratorAccess` for daily lab users once basics work
            - Rotate or delete unused access keys; check **Credential Report**
            - Use permission boundaries for third-party roles in production
            """
        ),
        mistakes=[
            ("Embedding access keys in user-data", "Keys appear in console and logs.", "Use instance profiles and roles."),
            ("One AdministratorAccess user for everyone", "No accountability; huge blast radius.", "Separate roles per job function with least privilege."),
            ("Skipping MFA on admin users", "Phished password owns the account.", "Require MFA via policy condition."),
        ],
        best_practices=dedent(
            """\
            - **Roles** for EC2, Lambda, GitHub Actions OIDC — not static keys
            - Name policies and roles clearly (`rebash-ec2-ssm-role`)
            - Use AWS SSO / IAM Identity Centre in multi-user organisations
            - Regularly audit with Access Analyzer and Credential Report
            - Break-glass admin only with MFA and logging
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | AccessDenied | Missing action in policy | Add action or use role with correct profile |
            | Cannot assume role | Trust policy wrong principal | Fix `Principal` service or ARN |
            | MFA still prompts on read | Sensitive action in policy | Split policies; use read-only role |
            | Instance profile not visible at launch | Propagation delay | Wait 10s after create; refresh console |
            """
        ),
        summary=dedent(
            """\
            - IAM controls API access globally — users, groups, roles, and JSON policies
            - **Prefer roles** with instance profiles for EC2; avoid long-lived keys
            - Apply **least privilege** and **MFA**; simulate policies before production
            - Destroy lab IAM artefacts you no longer need (users, test roles)
            """
        ),
        interview_q=[
            "What is the difference between an IAM user and an IAM role?",
            "Explain a trust policy versus a permissions policy.",
            "Why is IAM global while EC2 is Regional?",
            "How does an EC2 instance receive credentials from a role?",
            "What is least privilege and how do you iterate towards it?",
            "When would you use a permission boundary?",
            "How can you require MFA for deleting S3 buckets?",
            "What does `sts:AssumeRole` do?",
            "Why avoid AdministratorAccess for application roles?",
            "How do you audit unused IAM access keys?",
        ],
        interview_tips=[
            (
                1,
                "A user is a permanent identity with optional long-lived access keys — suited to humans "
                "with MFA. A role provides **temporary** credentials via STS when assumed by a service "
                "(EC2, Lambda) or federated user. Production compute should almost always use roles.",
            ),
            (
                4,
                "At launch, an instance profile attaches a role. The EC2 metadata service (IMDS) delivers "
                "short-lived credentials rotated automatically. No access keys are stored on disk in "
                "user-data — covered in Tutorial 10.",
            ),
        ],
        refs=[
            ("IAM User Guide", "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html"),
            ("IAM best practices", "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html"),
            ("IAM policy reference", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html"),
            ("Instance profiles", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html"),
        ],
    )

    T(
        num=4,
        slug="aws-cli-credentials-and-profiles",
        title="AWS CLI, Credentials, and Profiles",
        module="Module 1: Foundations",
        difficulty="beginner",
        minutes="40 min",
        tags=["aws", "cli", "credentials", "profiles", "sso"],
        prereq=[
            "Completed [IAM Fundamentals](iam-fundamentals.md)",
            "IAM lab user with programmatic access (or SSO configured)",
            "AWS CLI v2 installed",
        ],
        overview=dedent(
            """\
            The AWS CLI is how engineers script EC2, S3, and IAM changes in pipelines and during incidents.
            Misconfigured credentials — wrong profile, expired SSO token, keys in shell history — waste hours.

            This tutorial covers `aws configure`, **named profiles**, **SSO login**, environment variables,
            and safe patterns that mirror what Terraform and CI systems use. You will never paste secret keys
            into command lines.
            """
        ),
        objectives=[
            "Install and verify AWS CLI v2",
            "Configure named profiles in `~/.aws/credentials` and `~/.aws/config`",
            "Use `aws sso login` and `--profile` consistently",
            "Explain credential provider chain order",
            "Run mutating commands with explicit Region and profile flags",
        ],
        theory=dedent(
            """\
            ### CLI v2 vs v1

            AWS CLI v2 adds SSO, improved pagination, and unified installer. Verify with `aws --version`.

            ### Credential sources (chain order)

            1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`)
            2. SSO cached credentials (`aws sso login`)
            3. Named profiles in `~/.aws/credentials`
            4. Instance/container role (IMDS or ECS task role)

            Explicit `--profile lab` beats hoping the default is correct.

            ### Profiles in config

            `~/.aws/config`:

            ```ini
            [profile rebash-lab]
            region = eu-west-1
            output = json

            [profile rebash-sso]
            sso_start_url = https://my-org.awsapps.com/start
            sso_region = eu-west-1
            sso_account_id = 123456789012
            sso_role_name = AdministratorAccess
            region = eu-west-1
            ```

            ### Output and pagination

            - `--output table|json|text`
            - `--query` with JMESPath to filter
            - `--no-cli-pager` or `export AWS_PAGER=""` for scripts

            ### Safety flags

            Always pass `--region` and `--profile` in scripts. Use `set -euo pipefail` in Bash wrappers.
            """
        ),
        lab=dedent(
            """\
            ### Step 1 — Configure lab profile

            ```bash
            aws configure --profile rebash-lab
            # enter access key, secret, region eu-west-1, output json
            aws sts get-caller-identity --profile rebash-lab
            ```

            Prefer SSO in organisations:

            ```bash
            aws configure sso --profile rebash-sso
            aws sso login --profile rebash-sso
            aws sts get-caller-identity --profile rebash-sso
            ```

            ### Step 2 — Environment override (temporary)

            ```bash
            export AWS_PROFILE=rebash-lab
            export AWS_DEFAULT_REGION=eu-west-1
            aws ec2 describe-vpcs --max-items 5
            ```

            ### Step 3 — JMESPath query

            ```bash
            aws ec2 describe-vpcs \\
              --profile rebash-lab \\
              --query 'Vpcs[*].[VpcId,CidrBlock,IsDefault]' \\
              --output table
            ```

            ### Step 4 — Dry-run style read-only script

            ```bash
            cat > ~/rebash-aws/whoami.sh <<'EOF'
            #!/usr/bin/env bash
            set -euo pipefail
            PROFILE="${AWS_PROFILE:-rebash-lab}"
            aws sts get-caller-identity --profile "$PROFILE"
            aws configure list --profile "$PROFILE"
            EOF
            chmod +x ~/rebash-aws/whoami.sh
            ~/rebash-aws/whoami.sh
            ```

            """
        )
        + localstack_tip(
            """\
            export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=eu-west-1
            aws --endpoint-url=http://localhost:4566 sts get-caller-identity
            aws --endpoint-url=http://localhost:4566 s3 ls
            """
        ),
        validation=dedent(
            """\
            | Check | Command | Pass criteria |
            |-------|---------|---------------|
            | CLI version | `aws --version` | 2.x |
            | Profile | `aws sts get-caller-identity --profile rebash-lab` | Expected ARN |
            | Region | `aws configure get region --profile rebash-lab` | Your lab Region |
            | Script | `~/rebash-aws/whoami.sh` | Exit 0 |
            """
        ),
        walkthrough=dedent(
            """\
            | Setting | File | Notes |
            |---------|------|-------|
            | Access keys | `~/.aws/credentials` | chmod 600; never commit |
            | Region/output | `~/.aws/config` | `[profile name]` section |
            | SSO cache | `~/.aws/sso/cache/` | Refreshed via `aws sso login` |
            | `AWS_PROFILE` | Shell env | Overrides default profile |
            """
        ),
        security=dedent(
            """\
            - chmod 600 on credential files; use OS keychain where supported
            - Prefer SSO and roles over static keys on developer laptops
            - Never export secret keys in shell profile scripts
            - Rotate keys if leaked; use **CloudTrail** to detect misuse
            """
        ),
        mistakes=[
            ("Using default profile for prod and lab", "Wrong account deletes.", "Named profiles; prompt for account alias in scripts."),
            ("Secrets in shell history", "`export AWS_SECRET_ACCESS_KEY=` logged.", "Use profiles file or SSO; `HISTCONTROL=ignorespace` is not enough."),
            ("Forgotten SSO login", "Expired token errors.", "Wrap scripts with clear `aws sso login` message."),
        ],
        best_practices=dedent(
            """\
            - One profile per account/environment
            - Explicit `--region` in all automation
            - Use `AWS_PAGER=""` in CI logs
            - Document profile names in team README
            - Move to IAM Identity Centre SSO for teams
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | Unable to locate credentials | No profile/env | `aws configure` or SSO login |
            | Token expired | SSO session timeout | `aws sso login --profile X` |
            | Wrong region | Config mismatch | `--region` flag or fix config |
            | Partial JSON in pager | Default less pager | `AWS_PAGER=""` |
            """
        ),
        summary=dedent(
            """\
            - AWS CLI v2 with **named profiles** and optional **SSO** is the standard operator interface
            - Credential chain: env → SSO → files → instance role
            - Always specify profile and Region in scripts; protect credential files
            - LocalStack endpoint flag practices the same command shapes locally
            """
        ),
        interview_q=[
            "What is the AWS CLI credential provider chain order?",
            "How do named profiles differ between credentials and config files?",
            "Why prefer SSO over long-lived access keys?",
            "What does `--query` do?",
            "How would you prevent accidental changes in the wrong account?",
            "What is the purpose of `aws sts get-caller-identity`?",
            "How do instance roles provide credentials without a profile file?",
            "What environment variables override profile settings?",
            "Why set `AWS_PAGER` empty in CI?",
            "How would you rotate compromised access keys?",
        ],
        interview_tips=[
            (
                3,
                "SSO issues **temporary** credentials tied to corporate identity, centralised assignment, "
                "and MFA. Long-lived keys on laptops leak via git, backups, and malware. SSO reduces rotation "
                "pain and improves audit trails.",
            ),
            (
                5,
                "Use separate profiles per account, print `sts get-caller-identity` before destructive scripts, "
                "require explicit `--profile` flags, and in CI use OIDC roles scoped to one repository/environment.",
            ),
        ],
        refs=[
            ("AWS CLI User Guide", "https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html"),
            ("Configuring the CLI", "https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html"),
            ("SSO configuration", "https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html"),
            ("STS GetCallerIdentity", "https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html"),
        ],
    )


def _load_module2() -> None:
    vpc_extra = [
        vpc_cross_links().strip(),
    ]
    T(
        num=5,
        slug="vpc-subnets-and-multi-az-design",
        title="VPC, Subnets, and Multi-AZ Design",
        module="Module 2: VPC Networking",
        difficulty="intermediate",
        minutes="50 min",
        tags=["aws", "vpc", "subnets", "multi-az", "cidr"],
        prereq=[
            "Completed [AWS CLI, Credentials, and Profiles](aws-cli-credentials-and-profiles.md)",
            "Read [Cloud Networking: VPC and Subnets](../networking/cloud-networking-vpc-and-subnets.md)",
            "Understanding of CIDR and subnetting from [Networking](../networking/index.md)",
        ],
        related_extra=vpc_extra,
        cross_links_section=vpc_cross_links(),
        overview=dedent(
            """\
            A **Virtual Private Cloud (VPC)** is your isolated network in AWS. Subnets slice the VPC CIDR
            across **Availability Zones** so you can build tiers that survive single-AZ failure.

            You will design a small multi-AZ VPC with public and private subnets, associate route tables,
            and document why production apps spread across at least two AZs. This tutorial connects REBASH
            networking theory to AWS objects you will use in every later compute and data lab.
            """
        ),
        objectives=[
            "Plan VPC CIDR and subnet sizes without overlap",
            "Create public and private subnets in two AZs",
            "Associate route tables and explain default routes",
            "Tag VPC resources for cost and ownership",
            "Destroy the lab VPC cleanly to avoid NAT charges later",
        ],
        theory=dedent(
            """\
            ### VPC and subnet fundamentals

            | Object | Scope | Key field |
            |--------|-------|-----------|
            | VPC | Regional | `CidrBlock` e.g. `10.20.0.0/16` |
            | Subnet | Single AZ | `CidrBlock` subset of VPC |
            | Route table | Subnet association | Routes to IGW, NAT, local |
            | Internet Gateway | VPC attachment | Public ingress/egress |

            ### Public vs private subnet

            A **public** subnet has a route `0.0.0.0/0` → **Internet Gateway (IGW)** and instances with
            public IPs (or an Elastic IP). A **private** subnet has no direct IGW route; outbound internet
            uses NAT (Tutorial 6 — prefer SSM instead for labs).

            ### Multi-AZ design pattern

            ```
            AZ-a: public 10.20.1.0/24 | private 10.20.11.0/24
            AZ-b: public 10.20.2.0/24 | private 10.20.12.0/24
            ```

            Load balancers and RDS subnet groups span both AZs; EC2 Auto Scaling replaces failed AZ capacity.

            ### IP planning

            Reserve space for growth. `/16` VPC with `/24` subnets is a common lab pattern. Avoid overlapping
            with on-premises ranges you may VPN later.

            ### Default VPC

            Older accounts may still have a default VPC. Labs create a dedicated `rebash-lab-vpc` to practice
            explicit design — production rarely relies on defaults.
            """
        ),
        lab=dedent(
            """\
            Set variables:

            ```bash
            export AWS_PROFILE=rebash-lab
            export LAB_REGION=eu-west-1
            export VPC_CIDR=10.20.0.0/16
            ```

            ### Step 1 — Create VPC and subnets

            ```bash
            VPC_ID=$(aws ec2 create-vpc --cidr-block $VPC_CIDR --tag-specifications \\
              'ResourceType=vpc,Tags=[{Key=Name,Value=rebash-lab-vpc},{Key=Environment,Value=lab}]' \\
              --query Vpc.VpcId --output text --region $LAB_REGION)

            aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.20.1.0/24 \\
              --availability-zone ${LAB_REGION}a \\
              --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=rebash-public-a}]' \\
              --region $LAB_REGION

            aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.20.2.0/24 \\
              --availability-zone ${LAB_REGION}b \\
              --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=rebash-public-b}]' \\
              --region $LAB_REGION

            aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.20.11.0/24 \\
              --availability-zone ${LAB_REGION}a \\
              --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=rebash-private-a}]' \\
              --region $LAB_REGION

            aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.20.12.0/24 \\
              --availability-zone ${LAB_REGION}b \\
              --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=rebash-private-b}]' \\
              --region $LAB_REGION
            ```

            ### Step 2 — Verify

            ```bash
            aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC_ID \\
              --query 'Subnets[*].[SubnetId,CidrBlock,AvailabilityZone,Tags[?Key==`Name`].Value|[0]]' \\
              --output table --region $LAB_REGION
            ```

            ### Step 3 — Teardown (same session)

            ```bash
            # delete subnets, then vpc (after detaching IGW in later tutorials if added)
            aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC_ID --query 'Subnets[].SubnetId' \\
              --output text --region $LAB_REGION | xargs -n1 aws ec2 delete-subnet --subnet-id --region $LAB_REGION
            aws ec2 delete-vpc --vpc-id $VPC_ID --region $LAB_REGION
            ```

            """
        )
        + localstack_tip(
            """\
            aws --endpoint-url=http://localhost:4566 ec2 create-vpc --cidr-block 10.20.0.0/16
            aws --endpoint-url=http://localhost:4566 ec2 describe-vpcs --output table
            """
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | VPC | `rebash-lab-vpc` with `/16` CIDR |
            | Subnets | Four subnets across two AZs |
            | Tags | `Environment=lab` present |
            | Teardown | VPC deleted; no stray subnets |
            """
        ),
        walkthrough=dedent(
            """\
            | Resource | Walkthrough note |
            |----------|------------------|
            | `create-vpc` | Regional; CIDR cannot change after creation |
            | `create-subnet` | AZ is immutable; plan AZ spread upfront |
            | Tags | Required for Cost Explorer activation |
            | Teardown order | Dependents (instances, IGW) before VPC delete |
            """
        ),
        security=dedent(
            """\
            - Private subnets for application tiers; public only for load balancers or bastion-less patterns
            - Use Network ACLs and security groups (Tutorial 7) for defence in depth
            - Flow logs (optional) for audit — enable in production VPCs
            """
        ),
        mistakes=[
            ("Single AZ for production tiers", "AZ outage takes app offline.", "Spread subnets and ASG across ≥2 AZs."),
            ("Overlapping CIDR with office VPN", "Routing conflicts later.", "Document IPAM; use non-overlapping RFC1918 ranges."),
            ("Forgetting teardown", "Orphan subnets rarely bill alone but clutter quotas.", "Delete VPC at end of lab."),
        ],
        best_practices=dedent(
            """\
            - One VPC per environment or account in production
            - IPAM or spreadsheet for CIDR allocation
            - Enable DNS hostnames/support on VPC for internal names
            - Automate with Terraform modules after this track
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | `InvalidSubnet.Range` | CIDR outside VPC | Recalculate subnet bounds |
            | Cannot delete VPC | Dependencies remain | Delete IGW, subnets, endpoints first |
            | AZ name error | Region typo | Use `${REGION}a` pattern carefully |
            """
        ),
        summary=dedent(
            """\
            - VPCs isolate networks; subnets map to single AZs within a Region
            - Multi-AZ subnet layout is the foundation for resilient tiers
            - Tag and destroy lab VPCs; connect theory from the Networking track
            """
        ),
        interview_q=[
            "What is the difference between a VPC and a subnet?",
            "Why must a subnet exist in exactly one AZ?",
            "How do public and private subnets differ at the route table?",
            "What is the default VPC and why avoid it in production?",
            "How would you size a /16 VPC into application tiers?",
            "What happens if two VPCs peer with overlapping CIDRs?",
            "Why enable DNS hostnames on a VPC?",
            "How do tags support cost allocation?",
            "What is IPAM in large organisations?",
            "Which REBASH networking tutorial should you read before this one?",
        ],
        interview_tips=[
            (1, "A VPC is the Regional virtual network boundary with a CIDR block. Subnets are subdivisions of that CIDR tied to one AZ, where you place ENIs for EC2, RDS, and load balancers."),
            (3, "Public subnets route 0.0.0.0/0 to an Internet Gateway; instances can receive public IPs. Private subnets lack that route and rely on NAT or private-only access via endpoints."),
        ],
        refs=[
            ("Amazon VPC User Guide", "https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html"),
            ("VPCs and subnets", "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html"),
            ("Plan VPC IP addressing", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html"),
        ],
    )

    T(
        num=6,
        slug="internet-gateways-routes-and-egress",
        title="Internet Gateways, Routes, and Egress",
        module="Module 2: VPC Networking",
        difficulty="intermediate",
        minutes="45 min",
        tags=["aws", "igw", "routing", "nat", "egress"],
        prereq=[
            "Completed [VPC, Subnets, and Multi-AZ Design](vpc-subnets-and-multi-az-design.md)",
            "Billing budget configured",
        ],
        related_extra=vpc_extra,
        cross_links_section=vpc_cross_links(),
        extra_warnings=dedent(
            """\
            !!! danger "NAT Gateway cost warning"
                **NAT Gateway** bills hourly **and** per GB processed — it is **not** Free Tier friendly.
                For REBASH labs, prefer **public subnet EC2 with SSM Session Manager** (no inbound SSH)
                or **VPC endpoints** (Tutorial 8) instead of NAT. If you create NAT for learning, **destroy
                it in the same session**.
            """
        ),
        overview=dedent(
            """\
            Public internet reachability in AWS is explicit: an **Internet Gateway**, route table entries,
            and (for private subnets) **NAT** or alternatives. Misconfigured routes cause "works in public,
            broken in private" bugs.

            This tutorial attaches an IGW, configures routes, compares NAT egress costs, and demonstrates
            the **recommended lab pattern**: public subnet + **SSM** instead of NAT Gateway.
            """
        ),
        objectives=[
            "Attach and detach an Internet Gateway correctly",
            "Add `0.0.0.0/0` routes to public route tables",
            "Explain NAT Gateway egress and its cost model",
            "Implement lab egress via SSM without NAT",
            "Validate connectivity with ping/curl and teardown IGW",
        ],
        theory=dedent(
            """\
            ### Internet Gateway (IGW)

            Regional, horizontally scaled VPC component. One IGW per VPC for standard internet access.
            Public subnet route: `0.0.0.0/0` → `igw-xxxx`.

            ### NAT Gateway vs NAT instance vs alternatives

            | Option | Pros | Cons |
            |--------|------|------|
            | **NAT Gateway** | Managed, scalable | **Hourly + data charge — costly in labs** |
            | **NAT instance** | Cheaper (legacy) | You patch and scale it |
            | **Public + SSM** | No NAT for admin | Instance in public subnet; no SSH port |
            | **VPC endpoints** | Private access to AWS APIs | Not general internet |

            ### SSM Session Manager path

            EC2 in a **public subnet** with IGW route, **no SSH security group rule**, SSM agent, and
            instance profile `AmazonSSMManagedInstanceCore` gives shell access without bastion or NAT.

            ### Elastic IP charges

            Unattached EIPs and EIPs attached to stopped instances can incur charges. Release after labs.
            """
        ),
        lab=dedent(
            """\
            ### Step 1 — IGW and public route

            ```bash
            export LAB_REGION=eu-west-1
            # Assume VPC_ID and public subnet from Tutorial 5 or recreate minimal VPC

            IGW_ID=$(aws ec2 create-internet-gateway --region $LAB_REGION \\
              --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=rebash-igw}]' \\
              --query InternetGateway.InternetGatewayId --output text)

            aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID --region $LAB_REGION

            RTB_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --region $LAB_REGION \\
              --query RouteTable.RouteTableId --output text)

            aws ec2 create-route --route-table-id $RTB_ID --destination-cidr-block 0.0.0.0/0 \\
              --gateway-id $IGW_ID --region $LAB_REGION

            aws ec2 associate-route-table --route-table-id $RTB_ID --subnet-id $PUBLIC_SUBNET_ID --region $LAB_REGION
            ```

            ### Step 2 — Preferred lab pattern (SSM, no NAT)

            Launch Amazon Linux 2023 in the public subnet with the SSM instance profile from Tutorial 3.
            Security group: **no inbound** from 0.0.0.0/0; outbound HTTPS allowed.

            ```bash
            aws ssm start-session --target i-INSTANCE_ID --region $LAB_REGION
            ```

            ### Step 3 — Optional NAT demo (destroy immediately)

            ```bash
            # ONLY if you accept charges — delete within the hour
            # aws ec2 create-nat-gateway --subnet-id $PUBLIC_SUBNET_ID --allocation-id $EIP_ALLOC ...
            ```

            ### Step 4 — Teardown

            ```bash
            aws ec2 delete-route --route-table-id $RTB_ID --destination-cidr-block 0.0.0.0/0 --region $LAB_REGION
            aws ec2 detach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID --region $LAB_REGION
            aws ec2 delete-internet-gateway --internet-gateway-id $IGW_ID --region $LAB_REGION
            ```

            """
        )
        + localstack_tip(
            """\
            aws --endpoint-url=http://localhost:4566 ec2 create-internet-gateway
            aws --endpoint-url=http://localhost:4566 ec2 describe-internet-gateways
            """
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | IGW attached | `describe-internet-gateways` shows VPC |
            | Public route | `0.0.0.0/0` → igw in route table |
            | SSM session | Shell without SSH port open |
            | NAT | None left running (or deleted) |
            | Billing | Cost Explorer still near zero |
            """
        ),
        walkthrough=dedent(
            """\
            | Step | Detail |
            |------|--------|
            | Attach IGW | Required before public routing works |
            | Public route | Only subnets associated with this RTB become public |
            | SSM | Uses outbound HTTPS to AWS endpoints — no inbound SSH |
            | NAT GW | Place in **public** subnet; private RT points to NAT |
            """
        ),
        security=dedent(
            """\
            - Do not open SSH 0.0.0.0/0; use SSM with least-privilege instance role
            - NAT hides private IP sources but still exposes outbound attack surface — monitor egress
            - Release unused Elastic IPs promptly
            """
        ),
        mistakes=[
            ("NAT Gateway over weekend", "Tens of dollars for idle hours.", "Destroy same day; use SSM pattern in labs."),
            ("IGW on private subnet route only", "Confusion about direction.", "NAT goes in public subnet; private RT targets NAT."),
            ("SSH open to world", "Constant brute force.", "SSM Session Manager instead."),
        ],
        best_practices=dedent(
            """\
            - Prefer SSM and endpoints over NAT for admin and AWS API traffic
            - Use NAT Gateway in production private tiers when internet egress required
            - One NAT per AZ for HA in prod; single NAT for non-prod cost savings
            - Monitor NAT costs in Cost Explorer
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | No internet on public instance | Missing IGW route or `MapPublicIpOnLaunch` | Fix route table association |
            | SSM offline | No role or outbound block | Attach SSM policy; allow 443 outbound |
            | Cannot delete IGW | Still attached | Detach from VPC first |
            """
        ),
        summary=dedent(
            """\
            - IGW + public routes enable inbound/outbound internet for public subnets
            - **NAT Gateway is expensive** — avoid in Free Tier labs; prefer public + SSM
            - Destroy IGW, NAT, and EIPs after labs; confirm billing alarms
            """
        ),
        interview_q=[
            "What does an Internet Gateway do in a VPC?",
            "Why is NAT Gateway costly for labs?",
            "How can SSM replace a bastion host?",
            "Where must a NAT Gateway be placed?",
            "Difference between public IP and Elastic IP?",
            "What route makes a subnet public?",
            "When do you need NAT at all?",
            "How does outbound-only security group interact with IGW?",
            "What charges apply to unattached Elastic IPs?",
            "How would you give private subnets AWS API access without NAT?",
        ],
        interview_tips=[
            (2, "NAT Gateway has hourly availability charges plus per-GB data processing. A forgotten NAT over a weekend easily exceeds a student lab budget. SSM and VPC endpoints cover many lab/admin cases without general internet egress."),
            (3, "SSM Agent on EC2 calls AWS APIs outbound on 443. With an instance profile granting `ssm:StartSession`, operators get a shell in the console/CLI without opening SSH or running a bastion."),
        ],
        refs=[
            ("Internet gateways", "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html"),
            ("NAT gateways", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html"),
            ("SSM Session Manager", "https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html"),
        ],
    )

    # Tutorials 7-8 in _load_module2_part2
    _load_module2_part2()


def _load_module2_part2() -> None:
    vpc_extra = [vpc_cross_links().strip()]
    T(
        num=7,
        slug="security-groups-and-nacls",
        title="Security Groups and NACLs",
        module="Module 2: VPC Networking",
        difficulty="intermediate",
        minutes="45 min",
        tags=["aws", "security-groups", "nacl", "firewall"],
        prereq=["Completed [Internet Gateways, Routes, and Egress](internet-gateways-routes-and-egress.md)"],
        related_extra=vpc_extra,
        cross_links_section=vpc_cross_links(),
        overview=dedent(
            """\
            **Security groups** are stateful firewalls at the ENI level; **Network ACLs** are stateless
            filters at the subnet boundary. Production defence uses both plus least-privilege IAM.

            You will author restrictive security groups for a web tier, add NACL rules for subnet-level
            deny lists, and test allowed/denied flows — mirroring patterns from
            [Networking — Firewalls](../networking/firewalls-and-access-control.md).
            """
        ),
        objectives=[
            "Differentiate security groups (stateful) from NACLs (stateless)",
            "Create tiered security groups (web, app) with least privilege",
            "Add numbered NACL rules with explicit deny where needed",
            "Test connectivity with curl and expected failures",
            "Document rules for change control",
        ],
        theory=dedent(
            """\
            ### Security groups

            - **Stateful**: return traffic automatically allowed
            - **Allow rules only** — no deny rules
            - Attached to ENIs (EC2, ALB, RDS, etc.)
            - Reference other SGs as sources (preferred over CIDR sprawl)

            Example web tier inbound:

            | Type | Port | Source |
            |------|------|--------|
            | HTTPS | 443 | ALB security group |
            | (none) | 22 | **Do not open to 0.0.0.0/0** |

            ### Network ACLs

            - **Stateless**: must allow return traffic explicitly if you filter inbound/outbound separately
            - **Numbered rules** evaluated in order; first match wins
            - Subnet-level — affects all ENIs in subnet
            - Default NACL allows all; custom NACLs start deny-by-default

            ### When to use which

            | Control | Tool |
            |---------|------|
            | Instance-to-instance | Security group |
            | Subnet guardrail / deny IP block | NACL |
            | Admin access | SSM, not SG port 22 to world |
            """
        ),
        lab=dedent(
            """\
            ```bash
            export LAB_REGION=eu-west-1

            WEB_SG=$(aws ec2 create-security-group --group-name rebash-web-sg \\
              --description "Web tier HTTPS from ALB only" --vpc-id $VPC_ID \\
              --query GroupId --output text --region $LAB_REGION)

            ALB_SG=$(aws ec2 create-security-group --group-name rebash-alb-sg \\
              --description "ALB ingress 443" --vpc-id $VPC_ID \\
              --query GroupId --output text --region $LAB_REGION)

            aws ec2 authorize-security-group-ingress --group-id $ALB_SG --protocol tcp \\
              --port 443 --cidr 0.0.0.0/0 --region $LAB_REGION

            aws ec2 authorize-security-group-ingress --group-id $WEB_SG --protocol tcp \\
              --port 443 --source-group $ALB_SG --region $LAB_REGION

            aws ec2 authorize-security-group-egress --group-id $WEB_SG --protocol tcp \\
              --port 443 --cidr 0.0.0.0/0 --region $LAB_REGION
            ```

            Create custom NACL denying a test CIDR (lab only):

            ```bash
            NACL_ID=$(aws ec2 create-network-acl --vpc-id $VPC_ID --region $LAB_REGION \\
              --query NetworkAcl.NetworkAclId --output text)
            aws ec2 create-network-acl-entry --network-acl-id $NACL_ID --rule-number 100 \\
              --protocol -1 --rule-action deny --cidr-block 203.0.113.0/24 --ingress --region $LAB_REGION
            aws ec2 replace-network-acl-association --association-id $ASSOC_ID \\
              --network-acl-id $NACL_ID --region $LAB_REGION
            ```

            Teardown: delete security groups (after instances terminated), delete custom NACL associations.

            """
        )
        + localstack_tip(
            """\
            aws --endpoint-url=http://localhost:4566 ec2 create-security-group --group-name lab-sg --description test
            aws --endpoint-url=http://localhost:4566 ec2 describe-security-groups
            """
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Web SG | HTTPS only from ALB SG |
            | No SSH 0.0.0.0/0 | `describe-security-groups` confirms |
            | NACL deny | Test CIDR blocked at subnet edge |
            | Teardown | Custom SGs and NACL removed |
            """
        ),
        walkthrough=dedent(
            """\
            | Rule type | Behaviour |
            |-----------|-----------|
            | SG ingress referencing SG | Scales when IPs change behind ALB |
            | SG egress restrict | Limit lateral movement and data exfil |
            | NACL deny rule | Coarse block for known bad netblocks |
            | Rule numbering | Leave gaps (100, 200) for future inserts |
            """
        ),
        security=dedent(
            """\
            - Default deny inbound on app tiers; explicit allow only
            - Use SSM instead of SSH security group rules where possible
            - Log SG changes via AWS Config / CloudTrail (Tutorial 19)
            - Review NACL changes carefully — stateless mistakes break return traffic
            """
        ),
        mistakes=[
            ("SSH 0.0.0.0/0 on production SG", "Immediate brute-force noise.", "Remove; use SSM."),
            ("NACL without return rules", "Half-open connections fail.", "Allow ephemeral return ports or use SG only."),
            ("CIDR 0.0.0.0/0 on app SG ingress", "Bypasses ALB shield.", "Reference ALB SG only."),
        ],
        best_practices=dedent(
            """\
            - SG referencing SG beats hard-coded IPs
            - Separate SG per tier (web, app, db)
            - Automate rule documentation in change tickets
            - Periodic audit with VPC Reachability Analyzer
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | Timeout to app | SG missing ALB source | Add referencing rule |
            | Works once then fails | NACL stateless | Allow return traffic |
            | Cannot delete SG | Still attached | Terminate ENIs/instances first |
            """
        ),
        summary=dedent(
            """\
            - Security groups are stateful ENI firewalls; NACLs are stateless subnet filters
            - Layer controls: no SSH to world; ALB → web tier on 443 only
            - Test and tear down lab rules; align with Networking firewall tutorials
            """
        ),
        interview_q=[
            "Stateful vs stateless — SG or NACL?",
            "Can a security group contain a deny rule?",
            "Why reference an SG instead of CIDR for app tier?",
            "What happens to return traffic in a stateful SG?",
            "When would you use a NACL deny rule?",
            "Default NACL vs custom NACL behaviour?",
            "How do SGs apply to RDS?",
            "What ports does SSM require?",
            "How do you troubleshoot SG vs NACL issues?",
            "Relation to host firewalls on Linux?",
        ],
        interview_tips=[
            (1, "Security groups are stateful — response traffic is automatically allowed. NACLs are stateless — you must explicitly allow both directions if you filter, and rules are numbered with first match wins."),
            (3, "ALB IPs change with scaling. Referencing the ALB security group as source keeps rules stable and least-privilege without opening the app tier to the entire internet."),
        ],
        refs=[
            ("Security groups", "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html"),
            ("Network ACLs", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html"),
            ("Reachability Analyzer", "https://docs.aws.amazon.com/vpc/latest/reachability/what-is-reachability-analyzer.html"),
        ],
    )

    T(
        num=8,
        slug="vpc-endpoints-and-private-aws-access",
        title="VPC Endpoints and Private AWS Access",
        module="Module 2: VPC Networking",
        difficulty="intermediate",
        minutes="45 min",
        tags=["aws", "vpc-endpoints", "gateway", "interface", "private-link"],
        prereq=["Completed [Security Groups and NACLs](security-groups-and-nacls.md)"],
        related_extra=vpc_extra,
        cross_links_section=vpc_cross_links(),
        overview=dedent(
            """\
            Private subnets should reach S3, DynamoDB, and SSM without traversing the public internet or
            expensive NAT. **VPC endpoints** provide that path: **Gateway** endpoints for S3/DynamoDB and
            **Interface** endpoints (PrivateLink) for most other AWS APIs.

            You will add an S3 gateway endpoint and an SSM interface endpoint, update route tables or DNS,
            and verify private-only access patterns suitable for production tiers.
            """
        ),
        objectives=[
            "Compare Gateway vs Interface VPC endpoints",
            "Create an S3 Gateway endpoint and associate route tables",
            "Create an Interface endpoint for SSM or EC2 messages",
            "Explain DNS considerations for interface endpoints",
            "Remove endpoints during teardown (interface endpoints bill hourly)",
        ],
        theory=dedent(
            """\
            ### Gateway endpoints (S3, DynamoDB)

            - Free to use; no hourly charge
            - Added as a route in **route table** (`pl-xxx` prefix list target)
            - No security group on the endpoint itself

            ### Interface endpoints (PrivateLink)

            - ENI in your subnet with hourly + data charges (lower than NAT for AWS-only traffic)
            - Requires **private DNS** enablement for seamless API calls
            - Security group on endpoint ENI — allow 443 from clients

            ### SSM required endpoints (private subnet)

            For Session Manager without internet:

            - `com.amazonaws.region.ssm`
            - `com.amazonaws.region.ssmmessages`
            - `com.amazonaws.region.ec2messages`

            ### Cost note

            Interface endpoints have hourly cost but often **replace NAT GB charges** for AWS API traffic.
            Still **destroy lab endpoints** after validation.
            """
        ),
        lab=dedent(
            """\
            ```bash
            export LAB_REGION=eu-west-1

            aws ec2 create-vpc-endpoint --vpc-id $VPC_ID --service-name com.amazonaws.${LAB_REGION}.s3 \\
              --route-table-ids $PRIVATE_RTB_ID --region $LAB_REGION

            aws ec2 create-vpc-endpoint --vpc-id $VPC_ID \\
              --service-name com.amazonaws.${LAB_REGION}.ssm \\
              --vpc-endpoint-type Interface \\
              --subnet-ids $PRIVATE_SUBNET_ID \\
              --security-group-ids $ENDPOINT_SG \\
              --private-dns-enabled --region $LAB_REGION
            ```

            From private EC2 with SSM role (no public IP):

            ```bash
            aws s3 ls   # uses gateway route
            aws ssm describe-instance-information --region $LAB_REGION
            ```

            Teardown:

            ```bash
            aws ec2 delete-vpc-endpoints --vpc-endpoint-ids vpce-xxx --region $LAB_REGION
            ```

            """
        )
        + localstack_tip(
            """\
            aws --endpoint-url=http://localhost:4566 ec2 describe-vpc-endpoints
            aws --endpoint-url=http://localhost:4566 s3 mb s3://rebash-lab-bucket
            """
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | S3 endpoint | Route table entry to prefix list |
            | SSM endpoint | Interface ENI in private subnet |
            | Private EC2 | SSM session without public IP |
            | Teardown | No interface endpoints left billing |
            """
        ),
        walkthrough=dedent(
            """\
            | Endpoint type | Billing | Routing |
            |---------------|---------|---------|
            | Gateway S3 | No hourly | Route table entry |
            | Interface SSM | Hourly ENI | Private DNS resolves API name |
            | vs NAT | NAT charges internet GB | Endpoints only for AWS APIs |
            """
        ),
        security=dedent(
            """\
            - Restrict endpoint SG to client SGs only on 443
            - Use endpoint policies to limit S3 bucket access via endpoint
            - Prefer private access over public S3 URLs for internal data
            """
        ),
        mistakes=[
            ("Interface endpoint left running", "Hourly charges accumulate.", "Delete after lab."),
            ("Private DNS disabled", "SDK still resolves public IPs.", "Enable private DNS on interface endpoints."),
            ("Missing ssmmessages endpoint", "SSM sessions fail in private subnet.", "Create all three SSM-related endpoints."),
        ],
        best_practices=dedent(
            """\
            - Gateway endpoints for S3/DynamoDB in every production VPC
            - Interface endpoints for SSM, ECR, Secrets Manager in private tiers
            - Endpoint policies for exfiltration guardrails
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | S3 still public IP | Missing gateway route | Associate endpoint with RTB |
            | SSM timeout private | Missing endpoint or SG | Add endpoints; open 443 on endpoint SG |
            | DNS resolution fails | Private DNS off | Enable on interface endpoint |
            """
        ),
        summary=dedent(
            """\
            - Gateway endpoints route S3/DynamoDB privately; interface endpoints cover most AWS APIs
            - Enable SSM endpoints for private subnet admin without NAT
            - Destroy interface endpoints after labs; monitor billing
            """
        ),
        interview_q=[
            "Gateway vs Interface endpoint?",
            "Which services support Gateway endpoints?",
            "Why enable private DNS on interface endpoints?",
            "How do endpoint policies differ from IAM?",
            "SSM endpoints needed for private instances?",
            "Cost comparison NAT vs interface endpoint for S3 API traffic?",
            "Security group on interface endpoint purpose?",
            "Can endpoints replace all internet egress?",
            "What is AWS PrivateLink?",
            "How do you verify traffic uses the endpoint?",
        ],
        interview_tips=[
            (1, "Gateway endpoints are free route table targets for S3 and DynamoDB only. Interface endpoints place an ENI in your subnet with PrivateLink, usable for most AWS services, with hourly and data charges but no internet traversal."),
            (5, "Typically `ssm`, `ssmmessages`, and `ec2messages` interface endpoints in the same Region, plus an instance profile with SSM permissions and SG allowing HTTPS to the endpoint ENI."),
        ],
        refs=[
            ("VPC endpoints", "https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html"),
            ("Gateway endpoints", "https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html"),
            ("SSM VPC endpoints", "https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started-privatelink.html"),
        ],
    )


def _load_module3() -> None:
    T(
        num=9,
        slug="ec2-fundamentals",
        title="EC2 Fundamentals",
        module="Module 3: Compute",
        difficulty="intermediate",
        minutes="50 min",
        tags=["aws", "ec2", "ami", "instance-types", "compute"],
        prereq=[
            "Completed Module 2 VPC tutorials",
            "[Linux essentials](../linux/index.md) for SSH/SSM shell comfort",
        ],
        overview=dedent(
            """\
            **Elastic Compute Cloud (EC2)** provides virtual machines with configurable CPU, memory, networking,
            and AMI base images. Most AWS workloads still run on EC2 or containers on EC2-backed nodes.

            You will launch Amazon Linux 2023 in your lab VPC, choose instance type and EBS root volume,
            connect via **SSM Session Manager**, and terminate instances before leaving — with billing
            alarms confirmed.
            """
        ),
        objectives=[
            "Select AMI, instance type, and key-less SSM access pattern",
            "Launch EC2 in a tagged public subnet with instance profile",
            "Describe instance states and metadata categories",
            "Stop vs terminate cost implications",
            "Terminate instances and verify volume cleanup options",
        ],
        theory=dedent(
            """\
            ### Core concepts

            | Term | Meaning |
            |------|---------|
            | AMI | Boot image template |
            | Instance type | vCPU, RAM, network (e.g. `t3.micro`) |
            | EBS root volume | Persistent OS disk |
            | Instance store | Ephemeral local disks (specific families) |

            ### Purchase options (awareness)

            On-Demand (labs), Reserved, Savings Plans, Spot (interruptible). Free Tier often includes
            limited `t2/t3.micro` hours.

            ### Networking on launch

            - Subnet determines AZ
            - Security groups stateful firewall
            - Public IP only if subnet/route allow

            ### Connect patterns

            | Method | REBASH recommendation |
            |--------|-------------------------|
            | SSM Session Manager | **Yes** — no SSH port |
            | SSH with key pair | Learn but avoid 0.0.0.0/0 |
            | EC2 Instance Connect | Optional browser-based |
            """
        ),
        lab=dedent(
            """\
            ```bash
            export LAB_REGION=eu-west-1

            aws ec2 run-instances \\
              --image-id resolve_ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \\
              --instance-type t3.micro \\
              --subnet-id $PUBLIC_SUBNET_ID \\
              --security-group-ids $WEB_SG \\
              --iam-instance-profile Name=rebash-ec2-ssm-profile \\
              --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=rebash-web-01},{Key=Environment,Value=lab}]' \\
              --metadata-options HttpTokens=required,HttpEndpoint=enabled \\
              --region $LAB_REGION

            aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $LAB_REGION
            aws ssm start-session --target $INSTANCE_ID --region $LAB_REGION
            ```

            Inside instance:

            ```bash
            curl -s http://169.254.169.254/latest/meta-data/instance-id
            sudo dnf update -y
            ```

            Teardown:

            ```bash
            aws ec2 terminate-instances --instance-ids $INSTANCE_ID --region $LAB_REGION
            aws ec2 wait instance-terminated --instance-ids $INSTANCE_ID --region $LAB_REGION
            ```

            """
        )
        + localstack_tip(
            """\
            aws --endpoint-url=http://localhost:4566 ec2 run-instances --image-id ami-000001 --instance-type t3.micro
            aws --endpoint-url=http://localhost:4566 ec2 describe-instances
            """
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Instance running | `describe-instances` State=running |
            | SSM online | `PingStatus=Online` in Fleet Manager |
            | IMDSv2 | `HttpTokens=required` on launch |
            | Terminated | No running lab instances |
            | Billing | EC2 spend near zero post-teardown |
            """
        ),
        walkthrough=dedent(
            """\
            | Launch parameter | Why |
            |------------------|-----|
            | SSM path AMI query | Always latest Amazon Linux 2023 |
            | `t3.micro` | Free Tier eligible in many accounts |
            | Instance profile | Credentials for SSM without keys |
            | `HttpTokens=required` | IMDSv2 only — security best practice |
            """
        ),
        security=dedent(
            """\
            - Require IMDSv2 (`HttpTokens=required`)
            - No SSH from 0.0.0.0/0; use SSM
            - Patch AMIs regularly; use SSM Patch Manager in production
            - Instance role least privilege — not AdministratorAccess
            """
        ),
        mistakes=[
            ("Forgetting terminate", "EBS volumes may still bill.", "Terminate instances; delete unattached volumes."),
            ("IMDSv1 left enabled", "SSRF credential theft risk.", "Require IMDSv2 at launch."),
            ("Admin role on every instance", "Lateral movement.", "Scope role to SSM + app needs only."),
        ],
        best_practices=dedent(
            """\
            - Golden AMI or SSM parameter for latest Amazon Linux
            - Auto Recovery / ASG for production (Tutorial 17)
            - Detailed monitoring only when needed (cost)
            - Use Instance Metadata Service tags carefully
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | SSM offline | No profile or network | Attach SSM role; check SG egress |
            | Insufficient capacity | AZ capacity | Retry another AZ or type |
            | Cannot terminate | Termination protection | Disable protection flag |
            """
        ),
        summary=dedent(
            """\
            - EC2 launches AMIs as instances in subnets with SGs and roles
            - Use **SSM** and **IMDSv2**; terminate and verify billing after labs
            - Instance store vs EBS matters for data durability (next tutorial)
            """
        ),
        interview_q=[
            "Difference between stop and terminate?",
            "What is an AMI?",
            "How does SSM replace SSH?",
            "IMDSv1 vs IMDSv2?",
            "What does instance profile do at launch?",
            "When use Spot instances?",
            "How choose instance type?",
            "Public IP assignment rules?",
            "What bills after instance terminated?",
            "How resolve latest Amazon Linux AMI?",
        ],
        interview_tips=[
            (1, "Stop preserves EBS root volume and private IP (with caveats); you pay for EBS while stopped. Terminate ends billing for compute and, by default, deletes the root volume unless `DeleteOnTermination` is false."),
            (4, "IMDSv2 requires a session token via PUT before metadata GET, mitigating SSRF attacks that stole role credentials via IMDSv1."),
        ],
        refs=[
            ("Amazon EC2 User Guide", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html"),
            ("Connect via Session Manager", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/session-manager.html"),
            ("Instance metadata", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html"),
        ],
    )

    # Tutorials 10-11 in _load_module3_part2
    _load_module3_part2()


def _load_module3_part2() -> None:
    T(
        num=10,
        slug="user-data-imds-and-ssm-session-manager",
        title="User Data, IMDS, and SSM Session Manager",
        module="Module 3: Compute",
        difficulty="intermediate",
        minutes="55 min",
        tags=["aws", "user-data", "imds", "ssm", "cloud-init"],
        prereq=["Completed [EC2 Fundamentals](ec2-fundamentals.md)"],
        overview=dedent(
            """\
            **User data** bootstraps instances at first launch via cloud-init. The **Instance Metadata Service (IMDS)**
            exposes instance identity and role credentials — protect it with IMDSv2. **SSM Session Manager**
            delivers operator access without bastions or SSH keys.

            You will write user data to install a web server, fetch metadata safely, harden IMDS, and open
            an SSM session — the standard REBASH lab access pattern.
            """
        ),
        objectives=[
            "Write cloud-init user data to configure software at boot",
            "Retrieve metadata with IMDSv2 token workflow",
            "Require IMDSv2 on new instances",
            "Connect with SSM and run port forwarding demo",
            "Review user data logs for debugging",
        ],
        theory=dedent(
            """\
            ### User data lifecycle

            - Runs at **first boot** (and optionally every reboot if configured)
            - `#cloud-config` YAML or shell scripts
            - Logs: `/var/log/cloud-init.log` on Amazon Linux

            ### IMDS paths

            - `latest/meta-data/instance-id`
            - `latest/meta-data/placement/availability-zone`
            - `latest/meta-data/iam/security-credentials/ROLE_NAME`

            ### IMDSv2 token flow

            ```bash
            TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \\
              -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
            curl -H "X-aws-ec2-metadata-token: $TOKEN" \\
              http://169.254.169.254/latest/meta-data/instance-id
            ```

            ### SSM Session Manager

            Uses outbound HTTPS to SSM endpoints; supports port forwarding and logging to S3/CloudWatch.
            No inbound security group rules required for admin.
            """
        ),
        lab=dedent(
            """\
            Create `user-data.sh`:

            ```bash
            #!/bin/bash
            set -euxo pipefail
            dnf install -y httpd
            echo "rebash lab OK" > /var/www/html/index.html
            systemctl enable --now httpd
            ```

            Launch with user data (base64 handled by CLI file://):

            ```bash
            aws ec2 run-instances \\
              --image-id resolve_ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \\
              --instance-type t3.micro \\
              --subnet-id $PUBLIC_SUBNET_ID \\
              --security-group-ids $WEB_SG \\
              --iam-instance-profile Name=rebash-ec2-ssm-profile \\
              --user-data file://user-data.sh \\
              --metadata-options HttpTokens=required,HttpPutResponseHopLimit=1 \\
              --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=rebash-userdata-lab}]' \\
              --region $LAB_REGION
            ```

            SSM session and verify:

            ```bash
            aws ssm start-session --target $INSTANCE_ID --region $LAB_REGION
            sudo tail -50 /var/log/cloud-init.log
            curl localhost
            ```

            IMDSv2 from inside instance (see Theory). Teardown: terminate instance.

            """
        )
        + localstack_tip(
            "aws --endpoint-url=http://localhost:4566 ec2 run-instances --user-data file://user-data.sh ..."
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | User data | `index.html` serves rebash message |
            | cloud-init log | No fatal errors |
            | IMDSv2 | Token required for metadata |
            | SSM | Session opens without SSH |
            """
        ),
        walkthrough=dedent(
            """\
            | Mechanism | Detail |
            |-----------|--------|
            | `file://user-data.sh` | CLI encodes script at launch |
            | `HttpPutResponseHopLimit=1` | Blocks container SSRF to IMDS |
            | SSM agent | Preinstalled on Amazon Linux |
            | cloud-init | Idempotent modules; mind first-boot only defaults |
            """
        ),
        security=dedent(
            """\
            - Never embed IAM access keys in user data — use instance profiles
            - Require IMDSv2; hop limit 1 unless containers need metadata
            - Enable SSM session logging in production
            - User data is visible to anyone with `ec2:DescribeInstanceAttribute`
            """
        ),
        mistakes=[
            ("Secrets in user data", "Visible in console/API.", "Use Secrets Manager + role at runtime."),
            ("IMDSv1 enabled", "Credential theft via SSRF.", "HttpTokens=required on all launches."),
            ("Assuming user data re-runs on reboot", "Config drift.", "Use SSM Run Command or Ansible for changes."),
        ],
        best_practices=dedent(
            """\
            - Keep user data minimal — bootstrap only
            - Golden AMI for heavy software stacks
            - SSM as default admin path
            - Log shipping via CloudWatch agent (Tutorial 18)
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | User data not applied | Wrong shebang or MIME | Validate with cloud-init schema |
            | 401 on metadata | Missing IMDSv2 token | Use token PUT first |
            | SSM access denied | IAM or endpoint | Fix role policy; VPC endpoints |
            """
        ),
        summary=dedent(
            """\
            - User data bootstraps instances; keep secrets out of it
            - **IMDSv2** protects role credentials; **SSM** replaces SSH for access
            - Terminate lab instances; confirm billing alarms remain active
            """
        ),
        interview_q=[
            "When does user data execute?",
            "How fetch instance-id with IMDSv2?",
            "Why not put AWS keys in user data?",
            "SSM vs SSH trade-offs?",
            "What is hop limit on IMDS?",
            "Where debug failed user data?",
            "Can user data be changed after launch?",
            "How SSM port forwarding works?",
            "Role credentials rotation on instance?",
            "cloud-init vs SSM Run Command?",
        ],
        interview_tips=[
            (2, "PUT to `/latest/api/token` with TTL header returns a token; subsequent GETs to metadata paths must include `X-aws-ec2-metadata-token`. IMDSv1 allowed GET without token — deprecated."),
            (4, "SSM needs outbound 443 and an instance profile — no inbound SG rules, full audit logging possible, works for private subnets with endpoints. SSH requires key management and often opens port 22."),
        ],
        refs=[
            ("EC2 user data", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html"),
            ("Configure IMDS", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html"),
            ("Session Manager", "https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html"),
        ],
    )

    T(
        num=11,
        slug="ebs-volumes-snapshots-and-encryption",
        title="EBS Volumes, Snapshots, and Encryption",
        module="Module 3: Compute",
        difficulty="intermediate",
        minutes="45 min",
        tags=["aws", "ebs", "snapshots", "encryption", "storage"],
        prereq=["Completed [User Data, IMDS, and SSM Session Manager](user-data-imds-and-ssm-session-manager.md)"],
        overview=dedent(
            """\
            **Elastic Block Store (EBS)** provides durable block volumes for EC2. Snapshots back up volumes to S3;
            encryption protects data at rest with KMS keys.

            You will attach a secondary volume, create snapshots, restore to a new volume, enable encryption by
            default, and delete unattached volumes — a common source of silent billing.
            """
        ),
        objectives=[
            "Create and attach gp3 volumes in the same AZ",
            "Snapshot and restore volumes across AZs via snapshot copy",
            "Enable EBS encryption by default for the Region",
            "Identify `DeleteOnTermination` behaviour",
            "Delete snapshots and volumes during teardown",
        ],
        theory=dedent(
            """\
            ### Volume types (summary)

            | Type | Use case |
            |------|----------|
            | gp3 | General purpose default |
            | io2 | High IOPS databases |
            | st1/sc1 | Throughput/cold HDD (legacy patterns) |

            ### AZ affinity

            Volumes attach only in the same AZ as the instance. Snapshots are Regional; restored volumes can
            target any AZ in the Region.

            ### Encryption

            - Default encryption uses AWS managed KMS key `aws/ebs`
            - Snapshots inherit encryption; share encrypted snapshots via KMS key policy

            ### Billing traps

            - **Unattached gp3 volumes** bill monthly
            - **Snapshots** bill per GB-month
            - Orphan snapshots after quick instance terminate tests
            """
        ),
        lab=dedent(
            """\
            ```bash
            aws ec2 create-volume --availability-zone ${LAB_REGION}a --size 10 --volume-type gp3 \\
              --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=rebash-data}]' \\
              --region $LAB_REGION

            aws ec2 attach-volume --volume-id $VOL_ID --instance-id $INSTANCE_ID --device /dev/xvdf --region $LAB_REGION

            # on instance via SSM
            sudo mkfs -t xfs /dev/xvdf
            sudo mkdir /data && sudo mount /dev/xvdf /data
            echo lab > /data/test.txt

            aws ec2 create-snapshot --volume-id $VOL_ID --description "rebash lab snap" --region $LAB_REGION

            aws ec2 enable-ebs-encryption-by-default --region $LAB_REGION
            ```

            Teardown:

            ```bash
            aws ec2 terminate-instances --instance-ids $INSTANCE_ID --region $LAB_REGION
            aws ec2 delete-snapshot --snapshot-id $SNAP_ID --region $LAB_REGION
            aws ec2 delete-volume --volume-id $VOL_ID --region $LAB_REGION  # if detached
            ```

            """
        )
        + localstack_tip(
            "aws --endpoint-url=http://localhost:4566 ec2 create-volume --availability-zone eu-west-1a --size 10"
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Attach | Volume `in-use` same AZ |
            | Snapshot | `completed` state |
            | Encryption default | `get-ebs-encryption-by-default` true |
            | Cleanup | No volumes/snapshots remain |
            """
        ),
        walkthrough=dedent(
            """\
            | Operation | Note |
            |-----------|------|
            | `attach-volume` | Device name OS-specific |
            | Snapshot | Crash-consistent unless app quiesced |
            | Restore | New volume from snapshot in target AZ |
            | `DeleteOnTermination` | Root volume default true |
            """
        ),
        security=dedent(
            """\
            - Enable encryption by default in all Regions
            - Restrict snapshot sharing with KMS and IAM
            - Encrypt backups for compliance (GDPR, etc.)
            """
        ),
        mistakes=[
            ("Unattached volumes after lab", "Monthly gp3 charge.", "Delete volumes in teardown checklist."),
            ("Snapshot hoarding", "Storage cost creep.", "Lifecycle policy deletes old lab snaps."),
            ("Cross-AZ attach attempt", "API error.", "Snapshot-copy to target AZ first."),
        ],
        best_practices=dedent(
            """\
            - gp3 baseline; tune IOPS only when metrics prove need
            - Automate snapshots with Data Lifecycle Manager
            - Tag volumes with `Environment=lab`
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | Attach fails AZ | Volume AZ mismatch | Create volume in instance AZ |
            | Device busy | Already mounted | Unmount inside OS |
            | Encrypted share denied | KMS key policy | Update key policy for account |
            """
        ),
        summary=dedent(
            """\
            - EBS volumes are AZ-local block storage; snapshots enable backup and migration
            - Enable encryption by default; delete volumes and snapshots after labs
            - Watch billing for unattached volumes and old snapshots
            """
        ),
        interview_q=[
            "EBS vs instance store?",
            "Can you attach one volume to two instances?",
            "Snapshot consistency model?",
            "What happens to root volume on terminate?",
            "gp2 vs gp3?",
            "How encryption at rest works for EBS?",
            "Cross-Region snapshot copy use case?",
            "Billing for unattached volume?",
            "DeleteOnTermination flag purpose?",
            "DLM snapshot policy benefit?",
        ],
        interview_tips=[
            (1, "EBS is network-attached persistent block storage surviving stop/start. Instance store is local physical SSD with higher performance but data lost on stop/terminate — good for caches, not databases."),
            (8, "You pay for provisioned GB-month of gp3/io volumes whether attached or not — a classic post-lab leak if terminate leaves volumes behind."),
        ],
        refs=[
            ("Amazon EBS", "https://docs.aws.amazon.com/ebs/latest/userguide/how-ebs-works.html"),
            ("EBS snapshots", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-snapshots.html"),
            ("EBS encryption", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-encryption.html"),
        ],
    )


def _load_module4() -> None:
    T(
        num=12,
        slug="s3-fundamentals",
        title="S3 Fundamentals",
        module="Module 4: Storage",
        difficulty="beginner",
        minutes="45 min",
        tags=["aws", "s3", "object-storage", "buckets"],
        prereq=["Completed Module 3 Compute tutorials", "AWS CLI profile configured"],
        overview=dedent(
            """\
            **Amazon S3** is object storage for backups, artefacts, static sites, and data lakes. Buckets are
            global names; objects live in a Region. Understanding versioning, storage classes, and Block Public
            Access prevents headline-grabbing data leaks.

            You will create a bucket, upload objects, set lifecycle rules, and enable Block Public Access —
            then empty and delete the bucket in teardown.
            """
        ),
        objectives=[
            "Create a uniquely named bucket in your lab Region",
            "Upload, list, and download objects via CLI",
            "Explain storage classes at a high level",
            "Enable Block Public Access on the account and bucket",
            "Empty and delete buckets during teardown",
        ],
        theory=dedent(
            """\
            ### Bucket and object model

            - Bucket name globally unique across all AWS
            - Key = object path (`logs/2026/app.log`)
            - Strong read-after-write consistency for new objects

            ### Storage classes (awareness)

            | Class | Pattern |
            |-------|---------|
            | S3 Standard | Frequent access |
            | S3 Infrequent Access | Backups |
            | Glacier tiers | Archives |

            ### Block Public Access

            Account-level BPA prevents accidental public ACLs/policies — **enable before creating buckets**.

            ### Request and transfer billing

            PUT/LIST costs pennies at lab scale; egress to internet costs more — mind downloads in production.
            """
        ),
        lab=dedent(
            """\
            ```bash
            export LAB_REGION=eu-west-1
            BUCKET=rebash-lab-$(aws sts get-caller-identity --query Account --output text)-${LAB_REGION}

            aws s3api create-bucket --bucket $BUCKET --region $LAB_REGION \\
              --create-bucket-configuration LocationConstraint=$LAB_REGION

            aws s3api put-public-access-block --bucket $BUCKET \\
              --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

            echo "rebash s3 lab" > hello.txt
            aws s3 cp hello.txt s3://$BUCKET/hello.txt
            aws s3 ls s3://$BUCKET/
            aws s3 presign s3://$BUCKET/hello.txt --expires-in 300
            ```

            Teardown:

            ```bash
            aws s3 rm s3://$BUCKET --recursive
            aws s3api delete-bucket --bucket $BUCKET --region $LAB_REGION
            ```

            """
        )
        + localstack_tip(
            """\
            aws --endpoint-url=http://localhost:4566 s3 mb s3://rebash-local-bucket
            aws --endpoint-url=http://localhost:4566 s3 cp hello.txt s3://rebash-local-bucket/
            """
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Bucket | Created with BPA enabled |
            | Object | `hello.txt` listed |
            | Presigned URL | Downloads file before expiry |
            | Teardown | Bucket deleted (empty first) |
            """
        ),
        walkthrough=dedent(
            """\
            | API | Purpose |
            |-----|---------|
            | `create-bucket` | Region via LocationConstraint (not us-east-1) |
            | `put-public-access-block` | Defence against public exposure |
            | `cp` | High-level upload/download |
            | `presign` | Temporary HTTPS URL without public bucket |
            """
        ),
        security=dedent(
            """\
            - Block Public Access at account level
            - Bucket policies least privilege; no `Principal:*` without condition
            - Enable versioning for recovery; MFA delete for sensitive buckets
            - Encrypt with SSE-S3 or SSE-KMS default
            """
        ),
        mistakes=[
            ("Globally duplicate bucket name", "Create fails.", "Include account id in lab names."),
            ("Deleting non-empty bucket", "BucketNotEmpty error.", "Run `aws s3 rm --recursive` before delete-bucket."),
            ("Public read ACL on lab bucket", "Data leak.", "BPA + no public policies."),
        ],
        best_practices=dedent(
            """\
            - Standardise naming `{org}-{env}-{region}-{purpose}`
            - Lifecycle rules expire lab prefixes automatically
            - Access logging to dedicated audit bucket
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | BucketAlreadyExists | Name taken globally | Choose unique name |
            | AccessDenied | IAM policy | Add s3:PutObject for prefix |
            | Wrong Region | Endpoint mismatch | Pass `--region` consistently |
            """
        ),
        summary=dedent(
            """\
            - S3 stores objects in globally named Regional buckets
            - **Block Public Access** is mandatory hygiene
            - Empty and delete lab buckets; presigned URLs share without public ACLs
            """
        ),
        interview_q=[
            "S3 consistency model?",
            "Bucket naming rules?",
            "Block Public Access four settings?",
            "Storage class selection?",
            "Presigned URL use case?",
            "Versioning benefit?",
            "S3 vs EBS?",
            "Cross-Region replication purpose?",
            "Event notifications use case?",
            "How delete non-empty bucket?",
        ],
        interview_tips=[
            (3, "BlockPublicAcls and IgnorePublicAcls prevent public ACLs; BlockPublicPolicy and RestrictPublicBuckets prevent public bucket policies and cross-account public access — enable all four."),
            (7, "S3 is object storage accessed via HTTP API, unlimited scale, 11 nines durability. EBS is block storage attached to one EC2 instance in one AZ."),
        ],
        refs=[
            ("Amazon S3 User Guide", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"),
            ("Block Public Access", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html"),
            ("S3 storage classes", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html"),
        ],
    )

    T(
        num=13,
        slug="s3-security-and-static-hosting",
        title="S3 Security and Static Hosting",
        module="Module 4: Storage",
        difficulty="intermediate",
        minutes="50 min",
        tags=["aws", "s3", "static-website", "cloudfront", "security"],
        prereq=["Completed [S3 Fundamentals](s3-fundamentals.md)"],
        overview=dedent(
            """\
            Static websites on S3 plus CloudFront is a common pattern — but public buckets caused many breaches.
            This tutorial configures **encryption**, **bucket policies**, optional **static website hosting**,
            and CloudFront OAI/OAC patterns conceptually, keeping buckets private by default.

            You will enforce HTTPS-only access patterns and understand when static hosting is appropriate versus
            ALB-served dynamic apps.
            """
        ),
        objectives=[
            "Apply bucket policy allowing only CloudFront or specific principals",
            "Enable default encryption SSE-S3 or SSE-KMS",
            "Configure static website hosting safely in a lab bucket",
            "Explain OAC vs legacy OAI",
            "Tear down CloudFront distribution and bucket (distribution delete takes time)",
        ],
        theory=dedent(
            """\
            ### Secure static site pattern

            1. S3 bucket **private** (no public ACL)
            2. CloudFront distribution with **Origin Access Control (OAC)**
            3. Bucket policy allows `s3:GetObject` for CloudFront service principal only
            4. ACM certificate on CloudFront (cert in us-east-1 for CloudFront)

            ### Bucket policy example shape

            ```json
            {
              "Effect": "Allow",
              "Principal": {"Service": "cloudfront.amazonaws.com"},
              "Action": "s3:GetObject",
              "Resource": "arn:aws:s3:::bucket/*",
              "Condition": {"StringEquals": {"AWS:SourceArn": "arn:aws:cloudfront::ACCOUNT:distribution/ID"}}
            }
            ```

            ### Static website hosting endpoint

            `bucket.s3-website-REGION.amazonaws.com` — **avoid public internet exposure** without CloudFront
            and WAF in production.
            """
        ),
        lab=dedent(
            """\
            ```bash
            BUCKET=rebash-static-$(aws sts get-caller-identity --query Account --output text)

            aws s3api create-bucket --bucket $BUCKET --region $LAB_REGION \\
              --create-bucket-configuration LocationConstraint=$LAB_REGION

            aws s3api put-bucket-encryption --bucket $BUCKET \\
              --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

            aws s3 website s3://$BUCKET/ --index-document index.html --error-document error.html
            aws s3 cp index.html s3://$BUCKET/ --content-type text/html

            # Console: create CloudFront distribution with OAC (or document steps read-only)
            aws cloudfront list-distributions --query 'DistributionList.Items[*].Id' --output table
            ```

            Teardown: disable CloudFront distribution, wait deployed=false, delete distribution, empty bucket.

            """
        )
        + localstack_tip(
            "aws --endpoint-url=http://localhost:4566 s3api put-bucket-encryption --bucket rebash-local-bucket ..."
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Encryption | Default SSE enabled |
            | BPA | Still enabled |
            | Website config | Index document set |
            | No public policy | Policy denies anonymous GetObject |
            """
        ),
        walkthrough=dedent(
            """\
            | Control | Why |
            |---------|-----|
            | OAC | CloudFront reads private S3 without public bucket |
            | SSE | At-rest encryption compliance |
            | BPA | Blocks accidental public ACL |
            | WAF (prod) | Rate limit and geo block at edge |
            """
        ),
        security=dedent(
            """\
            - Never `Principal: *` on sensitive buckets without tight conditions
            - Use OAC + private bucket for static sites
            - Enable S3 access logging and CloudTrail data events for audit
            - MFA delete for production buckets with versioning
            """
        ),
        mistakes=[
            ("Public bucket for 'simple' static site", "Indexed by scanners.", "CloudFront + OAC + private bucket."),
            ("HTTP only website endpoint", "Credentials intercepted.", "Redirect HTTP→HTTPS at CloudFront."),
            ("Deleting bucket before CloudFront", "Distribution holds reference.", "Delete CloudFront first."),
        ],
        best_practices=dedent(
            """\
            - Infrastructure as Code for CloudFront + S3 modules
            - Invalidate CloudFront cache on deploy
            - Separate buckets per environment
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | 403 from CloudFront | OAC policy wrong | Fix SourceArn condition |
            | Website 404 | Missing index key | Upload index.html at root |
            | AccessDenied encryption | KMS key policy | Allow S3 service |
            """
        ),
        summary=dedent(
            """\
            - Static sites belong behind **CloudFront + OAC** with private S3
            - Default encryption and Block Public Access are non-negotiable
            - Tear down distributions and buckets to avoid storage and request charges
            """
        ),
        interview_q=[
            "OAC vs OAI?",
            "How serve private S3 via CloudFront?",
            "Why ACM cert in us-east-1 for CloudFront?",
            "Bucket policy vs IAM policy for S3?",
            "SSE-S3 vs SSE-KMS trade-off?",
            "Static website endpoint vs REST endpoint?",
            "How prevent hotlinking?",
            "S3 Object Lock use case?",
            "Versioning + delete marker behaviour?",
            "WAF at CloudFront benefit?",
        ],
        interview_tips=[
            (2, "Bucket remains private. CloudFront OAC gets an IAM condition-bound bucket policy allowing GetObject only from that distribution ARN. Viewers hit CloudFront HTTPS URL; S3 never exposed publicly."),
            (5, "SSE-S3 uses S3-managed keys (simple, no KMS API costs). SSE-KMS uses KMS CMK with audit trail and key policy control — better for regulated data, adds KMS API latency/cost."),
        ],
        refs=[
            ("Static website hosting", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html"),
            ("CloudFront OAC", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html"),
            ("S3 bucket policies", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html"),
        ],
    )


def _load_module5() -> None:
    T(
        num=14,
        slug="elastic-load-balancing-alb-and-nlb",
        title="Elastic Load Balancing — ALB and NLB",
        module="Module 5: Edge and Data",
        difficulty="intermediate",
        minutes="55 min",
        tags=["aws", "elb", "alb", "nlb", "load-balancer"],
        prereq=["Completed Module 4 Storage", "VPC with public subnets"],
        extra_warnings=dedent(
            """\
            !!! warning "Application Load Balancer cost"
                ALB bills hourly plus LCU usage — **not** Free Tier. Create for the lab, validate health checks,
                then **delete the load balancer the same session**. Prefer target group + curl tests on instances
                if you need to skip ALB cost entirely.
            """
        ),
        overview=dedent(
            """\
            **Elastic Load Balancing** distributes traffic across targets. **Application Load Balancers (ALB)**
            operate at Layer 7 with path-based routing; **Network Load Balancers (NLB)** handle TCP/UDP with
            extreme performance and static IPs.

            You will create an ALB, target group, health checks, and register EC2 instances — then delete the
            ALB to avoid ongoing charges.
            """
        ),
        objectives=[
            "Compare ALB vs NLB vs Classic ELB",
            "Create ALB in public subnets across two AZs",
            "Configure target group health checks on `/` HTTP 200",
            "Register EC2 targets and observe healthy state",
            "Delete load balancer and target group in teardown",
        ],
        theory=dedent(
            """\
            ### Load balancer types

            | Type | Layer | Use case |
            |------|-------|----------|
            | ALB | 7 HTTP/HTTPS/gRPC | Web apps, path routing |
            | NLB | 4 TCP/UDP/TLS | Low latency, static IP, gaming |
            | GLB | 3 Gateway | IP rewrites at VPC edge |

            ### ALB components

            - Listeners (443 → forward action)
            - Rules (host/path conditions)
            - Target groups (instances, IPs, Lambda)
            - Health checks (interval, threshold, matcher)

            ### Security

            ALB security group allows 443 from internet (or CloudFront prefix list). Instance SG allows
            traffic **only from ALB SG** on app port.

            ### Cost

            ALB hourly + LCU — destroy after lab. NLB similar model.
            """
        ),
        lab=dedent(
            """\
            ```bash
            TG_ARN=$(aws elbv2 create-target-group --name rebash-http-tg --protocol HTTP --port 80 \\
              --vpc-id $VPC_ID --health-check-path / --matcher HttpCode=200 \\
              --query TargetGroups[0].TargetGroupArn --output text --region $LAB_REGION)

            ALB_ARN=$(aws elbv2 create-load-balancer --name rebash-alb --type application \\
              --subnets $PUBLIC_SUBNET_A $PUBLIC_SUBNET_B \\
              --security-groups $ALB_SG \\
              --query LoadBalancers[0].LoadBalancerArn --output text --region $LAB_REGION)

            aws elbv2 create-listener --load-balancer-arn $ALB_ARN --protocol HTTP --port 80 \\
              --default-actions Type=forward,TargetGroupArn=$TG_ARN --region $LAB_REGION

            aws elbv2 register-targets --target-group-arn $TG_ARN \\
              --targets Id=$INSTANCE_ID --region $LAB_REGION

            aws elbv2 describe-target-health --target-group-arn $TG_ARN --region $LAB_REGION
            curl http://$ALB_DNS_NAME/
            ```

            Teardown:

            ```bash
            aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN --region $LAB_REGION
            aws elbv2 delete-target-group --target-group-arn $TG_ARN --region $LAB_REGION
            ```

            """
        )
        + localstack_tip(
            "aws --endpoint-url=http://localhost:4566 elbv2 describe-load-balancers"
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Target health | `healthy` state |
            | ALB DNS | Returns HTTP 200 body |
            | SG layering | Instance accepts only ALB SG |
            | Teardown | No load balancers remain |
            """
        ),
        walkthrough=dedent(
            """\
            | Component | Detail |
            |-----------|--------|
            | Health check | Unhealthy targets removed from rotation |
            | Cross-zone LB | ALB cross-zone enabled by default |
            | Idle timeout | Tune for long-lived connections |
            | Access logs | S3 bucket for ALB logs (prod) |
            """
        ),
        security=dedent(
            """\
            - TLS terminate at ALB with modern policy
            - Restrict instance SG to ALB source SG
            - Enable WAF on internet-facing ALB in production
            """
        ),
        mistakes=[
            ("ALB left over weekend", "Hourly charges.", "Delete in teardown checklist."),
            ("Health check wrong path", "All targets unhealthy.", "Match app endpoint returning 200."),
            ("Instance SG open to world", "Bypasses ALB shield.", "Allow only ALB SG."),
        ],
        best_practices=dedent(
            """\
            - HTTPS listeners with ACM certs
            - Connection draining on target deregistration
            - Use NLB for non-HTTP TCP services
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | Unhealthy targets | SG or wrong port | Open instance SG from ALB; check app port |
            | 502 Bad Gateway | App not listening | Start httpd on port 80 |
            | Slow delete ALB | Eni cleanup delay | Wait minutes; retry delete |
            """
        ),
        summary=dedent(
            """\
            - ALB routes HTTP/S to healthy targets; NLB for Layer 4
            - **Delete ALB after lab** — hourly charges apply
            - Layer security groups: internet → ALB → instances only
            """
        ),
        interview_q=[
            "ALB vs NLB?",
            "How health checks affect routing?",
            "Why two subnets for ALB?",
            "Target type instance vs IP?",
            "Connection draining purpose?",
            "ALB listener rules use case?",
            "Cross-zone load balancing?",
            "How stickiness works?",
            "ALB access logs location?",
            "Cost components of ALB?",
        ],
        interview_tips=[
            (1, "ALB understands HTTP — host/path routing, WAF integration, Lambda targets. NLB preserves source IP at TCP layer, handles millions of flows, supports static IPs — use for non-HTTP or extreme performance."),
            (10, "Hourly charge for each ALB plus LCU based on new connections, active connections, processed bytes, and rule evaluations — idle ALBs still cost hourly."),
        ],
        refs=[
            ("Elastic Load Balancing", "https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html"),
            ("Application Load Balancers", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html"),
            ("Target groups", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html"),
        ],
    )

    # Tutorials 15-17
    _load_module5_part2()


def _load_module5_part2() -> None:
    T(
        num=15,
        slug="route-53-dns-and-health-checks",
        title="Route 53 DNS and Health Checks",
        module="Module 5: Edge and Data",
        difficulty="intermediate",
        minutes="45 min",
        tags=["aws", "route53", "dns", "health-checks"],
        prereq=["Completed [Elastic Load Balancing — ALB and NLB](elastic-load-balancing-alb-and-nlb.md)"],
        overview=dedent(
            """\
            **Amazon Route 53** is AWS's DNS service — hosted zones, records, routing policies, and health checks
            that integrate with load balancers and failover architectures.

            You will create a public hosted zone (lab domain or subdomain), add A/alias records to an ALB,
            configure simple routing, and understand health check billing — destroy unused hosted zones after labs.
            """
        ),
        objectives=[
            "Create public hosted zone and interpret NS/SOA records",
            "Add alias A record to Application Load Balancer",
            "Compare routing policies: simple, weighted, failover",
            "Create HTTP health check against ALB endpoint",
            "Delete hosted zone records before zone deletion",
        ],
        theory=dedent(
            """\
            ### Record types

            | Type | Use |
            |------|-----|
            | A / AAAA | IPv4/IPv6 — often **Alias** to ALB/CloudFront |
            | CNAME | DNS name alias (not apex) |
            | NS / SOA | Zone delegation |

            ### Alias records

            Alias to AWS resources free of charge for queries to AWS targets; supports ALB, CloudFront, S3 website.

            ### Routing policies

            - **Simple** — one record, multiple values (RR)
            - **Weighted** — traffic split canary
            - **Failover** — primary/secondary with health check
            - **Latency / Geolocation** — user proximity

            ### Health checks

            Route 53 health checks bill per check — delete lab checks in teardown.
            """
        ),
        lab=dedent(
            """\
            ```bash
            ZONE_ID=$(aws route53 create-hosted-zone --name lab.rebash.example \\
              --caller-reference $(date +%s) --query HostedZone.Id --output text)

            cat > change-batch.json <<EOF
            {
              "Changes": [{
                "Action": "CREATE",
                "ResourceRecordSet": {
                  "Name": "app.lab.rebash.example",
                  "Type": "A",
                  "AliasTarget": {
                    "HostedZoneId": "$ALB_ZONE_ID",
                    "DNSName": "$ALB_DNS_NAME",
                    "EvaluateTargetHealth": true
                  }
                }
              }]
            }
            EOF

            aws route53 change-resource-record-sets --hosted-zone-id $ZONE_ID --change-batch file://change-batch.json

            aws route53 create-health-check --health-check-config \\
              IPAddress=8.8.8.8,Port=443,Type=HTTPS,ResourcePath=/,RequestInterval=30,FailureThreshold=3
            ```

            Teardown: delete records, health checks, hosted zone.

            """
        )
        + localstack_tip(
            "aws --endpoint-url=http://localhost:4566 route53 list-hosted-zones"
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Hosted zone | NS records returned |
            | Alias record | Points to ALB DNS name |
            | DNS resolution | `dig` returns ALB addresses (if delegated) |
            | Teardown | Health checks and zone removed |
            """
        ),
        walkthrough=dedent(
            """\
            | Item | Note |
            |------|------|
            | Caller reference | Idempotent zone creation token |
            | EvaluateTargetHealth | Alias considers target health |
            | TTL vs Alias | Alias uses AWS internal TTL |
            | Private zones | Associated with VPC — different tutorial path |
            """
        ),
        security=dedent(
            """\
            - DNSSEC signing for public zones when supported
            - Restrict Route 53 IAM changes — high blast radius
            - Monitor unexpected record changes via CloudTrail
            """
        ),
        mistakes=[
            ("Deleting zone with records", "HostedZoneNotEmpty.", "Delete all records except NS/SOA first."),
            ("CNAME at zone apex", "Invalid DNS.", "Use Alias A at apex."),
            ("Forgotten health checks", "Small monthly charge.", "Delete checks in teardown."),
        ],
        best_practices=dedent(
            """\
            - Infrastructure as Code for DNS (Terraform aws_route53_record)
            - Lower TTL before migrations; raise after stable
            - Failover health checks for DR patterns
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | NXDOMAIN | Zone not delegated | Update registrar NS |
            | Alias to wrong LB zone ID | ELB hosted zone IDs are per-Region | Use describe-load-balancers HostedZoneId |
            | Health check false negative | Wrong path/port | Match listener config |
            """
        ),
        summary=dedent(
            """\
            - Route 53 hosts DNS with alias integration to ALB and CloudFront
            - Choose routing policy to match failover and canary needs
            - Delete health checks and hosted zones after labs
            """
        ),
        interview_q=[
            "Alias vs CNAME at apex?",
            "Route 53 routing policies?",
            "How health checks tie to failover?",
            "Private hosted zone use case?",
            "DNS TTL trade-offs?",
            "Weighted routing canary?",
            "EvaluateTargetHealth meaning?",
            "Route 53 Resolver purpose?",
            "DNSSEC on Route 53?",
            "Billing for health checks?",
        ],
        interview_tips=[
            (1, "Route 53 Alias A records at zone apex can point to ALB/CloudFront/S3 — CNAME at apex is invalid per DNS RFC. Alias is AWS-specific extension with no charge for alias queries to AWS targets."),
            (3, "Failover routing uses primary/secondary record sets; health check on primary removes it from DNS answers when unhealthy, sending traffic to secondary."),
        ],
        refs=[
            ("Route 53 Developer Guide", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html"),
            ("Routing policies", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html"),
            ("Health checks", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html"),
        ],
    )

    T(
        num=16,
        slug="rds-fundamentals",
        title="RDS Fundamentals",
        module="Module 5: Edge and Data",
        difficulty="intermediate",
        minutes="50 min",
        tags=["aws", "rds", "mysql", "database", "multi-az"],
        prereq=["Completed VPC and security group tutorials"],
        extra_warnings=dedent(
            """\
            !!! danger "Destroy RDS immediately after the lab"
                RDS instances bill for compute and storage continuously. **Create, validate, snapshot optionally,
                then delete the instance in the same session.** Skip final snapshots in labs unless you need
                restore practice — snapshots also incur storage cost.
            """
        ),
        overview=dedent(
            """\
            **Amazon RDS** manages relational databases (PostgreSQL, MySQL, MariaDB, etc.) with automated backups,
            patching options, and Multi-AZ failover. It is powerful and **expensive for idle labs**.

            You will launch a small MySQL or PostgreSQL instance in private subnets, connect from EC2 via SSM,
            verify backups, and **delete the instance immediately** — with billing alarms confirmed.
            """
        ),
        objectives=[
            "Launch RDS in private subnets with security group referencing app tier",
            "Explain Multi-AZ vs Read Replica at high level",
            "Connect from EC2 using endpoint DNS name",
            "Review automated backup window and retention",
            "Delete RDS instance without unnecessary final snapshot retention",
        ],
        theory=dedent(
            """\
            ### RDS responsibilities

            AWS manages: hosting, storage replication (Multi-AZ), automated backups to S3, patching platform.
            You manage: schema, users, parameter groups, security groups, encryption keys.

            ### Deployment options

            | Option | HA | Read scaling |
            |--------|----|--------------|
            | Single-AZ | No | — |
            | Multi-AZ | Sync standby failover | No (standby not readable) |
            | Read replica | Async copy | Yes |

            ### Networking

            RDS lives in DB subnet group spanning AZs. SG allows app tier SG on DB port only.

            ### Cost warning

            db.t3.micro may have Free Tier hours — still **delete same day**. Storage and backup storage bill separately.
            """
        ),
        lab=dedent(
            """\
            ```bash
            aws rds create-db-subnet-group --db-subnet-group-name rebash-db-subnets \\
              --db-subnet-group-description "lab" \\
              --subnet-ids $PRIVATE_SUBNET_A $PRIVATE_SUBNET_B --region $LAB_REGION

            aws rds create-db-instance \\
              --db-instance-identifier rebash-lab-db \\
              --db-instance-class db.t3.micro \\
              --engine mysql \\
              --master-username admin \\
              --master-user-password 'ChangeMeLab123!' \\
              --allocated-storage 20 \\
              --vpc-security-group-ids $DB_SG \\
              --db-subnet-group-name rebash-db-subnets \\
              --backup-retention-period 1 \\
              --no-publicly-accessible \\
              --region $LAB_REGION

            aws rds wait db-instance-available --db-instance-identifier rebash-lab-db --region $LAB_REGION

            # From app EC2 via SSM:
            mysql -h $RDS_ENDPOINT -u admin -p
            ```

            Teardown (**same session**):

            ```bash
            aws rds delete-db-instance --db-instance-identifier rebash-lab-db \\
              --skip-final-snapshot --delete-automated-backups --region $LAB_REGION
            aws rds wait db-instance-deleted --db-instance-identifier rebash-lab-db --region $LAB_REGION
            ```

            """
        )
        + localstack_tip(
            "aws --endpoint-url=http://localhost:4566 rds create-db-instance --db-instance-identifier lab-db ..."
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Available | `describe-db-instances` Status=available |
            | Private | PubliclyAccessible=false |
            | Connect | SQL prompt from app EC2 |
            | Deleted | Instance gone; Cost Explorer quiet |
            """
        ),
        walkthrough=dedent(
            """\
            | Setting | Purpose |
            |---------|---------|
            | DB subnet group | AZ placement for ENIs |
            | `--no-publicly-accessible` | No internet route to database |
            | Backup retention | Point-in-time recovery window |
            | `--skip-final-snapshot` | Lab only — prod always snapshots |
            """
        ),
        security=dedent(
            """\
            - Never publicly accessible RDS
            - Encrypt at rest with KMS; TLS in transit
            - Rotate master password via Secrets Manager in production
            - Least-privilege DB users — not master for apps
            """
        ),
        mistakes=[
            ("RDS overnight", "Compute + storage bill.", "Delete same session."),
            ("Publicly accessible true", "Internet scanning.", "Always false; SG app tier only."),
            ("Master creds in app config", "Over-privileged apps.", "App-specific DB users + secrets store."),
        ],
        best_practices=dedent(
            """\
            - Multi-AZ for production OLTP
            - Parameter groups tuned with staging first
            - Performance Insights for slow queries
            - Aurora serverless v2 for variable workloads (awareness)
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | Cannot connect | SG wrong | Allow app SG on 3306/5432 |
            | Storage full | Autoscaling off | Enable storage autoscaling prod |
            | Slow delete | Final snapshot | Skip in lab; wait for delete |
            """
        ),
        summary=dedent(
            """\
            - RDS manages relational DB with backups and optional Multi-AZ
            - Keep databases in private subnets; **destroy immediately after labs**
            - Use security groups referencing app tier, not open CIDR
            """
        ),
        interview_q=[
            "Multi-AZ vs Read Replica?",
            "Who patches RDS engine?",
            "Why DB subnet group spans AZs?",
            "Publicly accessible flag risk?",
            "Backup vs snapshot?",
            "Encryption at rest options?",
            "Connection pooling at scale?",
            "Parameter group purpose?",
            "Failover time Multi-AZ?",
            "Cost if RDS left running?",
        ],
        interview_tips=[
            (1, "Multi-AZ maintains synchronous standby for automatic failover — not for read scaling. Read replicas are asynchronous copies for read traffic and DR, promoted manually or via automation."),
            (10, "You pay DB instance hours, storage GB-month, backup storage beyond free allocation, and I/O depending on engine — idle db.t3.micro still charges storage and instance hours outside Free Tier."),
        ],
        refs=[
            ("Amazon RDS User Guide", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html"),
            ("Creating DB instance", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html"),
            ("Multi-AZ", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html"),
        ],
    )

    T(
        num=17,
        slug="auto-scaling-groups-and-launch-templates",
        title="Auto Scaling Groups and Launch Templates",
        module="Module 5: Edge and Data",
        difficulty="intermediate",
        minutes="50 min",
        tags=["aws", "asg", "launch-template", "autoscaling"],
        prereq=["Completed [RDS Fundamentals](rds-fundamentals.md)", "ALB target group from Tutorial 14"],
        overview=dedent(
            """\
            **Auto Scaling Groups (ASG)** maintain desired capacity across AZs, replacing unhealthy instances and
            scaling on metrics. **Launch templates** define how each instance is built — AMI, type, SG, profile.

            You will create a launch template with SSM profile, attach an ASG to an ALB target group, trigger
            a scale event, and scale down to zero before teardown.
            """
        ),
        objectives=[
            "Create launch template with IMDSv2 and SSM instance profile",
            "Define ASG across two subnets/AZs",
            "Attach ASG to ALB target group for health",
            "Simulate scale out via desired capacity change",
            "Set desired capacity to 0 and delete ASG/template",
        ],
        theory=dedent(
            """\
            ### Launch template vs launch configuration

            Launch templates are the modern approach — versioning, mixed instances policy, T2/T3 unlimited.

            ### ASG integration

            - **ELB health checks** — replace instances failing ALB checks
            - **Scaling policies** — target tracking on CPU, request count
            - **Instance refresh** — rolling AMI updates

            ### Cooldowns and protection

            Scale-in protection on long-running jobs; lifecycle hooks for drain.

            ### Lab cost

            ASG with `t3.micro` still bills per instance-hour — scale to zero and delete ASG after lab.
            """
        ),
        lab=dedent(
            """\
            ```bash
            aws ec2 create-launch-template --launch-template-name rebash-web-lt \\
              --launch-template-data '{
                "ImageId": "resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64",
                "InstanceType": "t3.micro",
                "IamInstanceProfile": {"Name": "rebash-ec2-ssm-profile"},
                "SecurityGroupIds": ["'$WEB_SG'"],
                "MetadataOptions": {"HttpTokens": "required"},
                "UserData": "'$(base64 -w0 user-data.sh)'"
              }' --region $LAB_REGION

            aws autoscaling create-auto-scaling-group \\
              --auto-scaling-group-name rebash-web-asg \\
              --launch-template LaunchTemplateName=rebash-web-lt,Version='$Latest' \\
              --min-size 1 --max-size 3 --desired-capacity 2 \\
              --vpc-zone-identifier "$PUBLIC_SUBNET_A,$PUBLIC_SUBNET_B" \\
              --target-group-arns $TG_ARN \\
              --health-check-type ELB --health-check-grace-period 300 \\
              --region $LAB_REGION

            aws autoscaling set-desired-capacity --auto-scaling-group-name rebash-web-asg \\
              --desired-capacity 3 --region $LAB_REGION

            aws autoscaling update-auto-scaling-group --auto-scaling-group-name rebash-web-asg \\
              --min-size 0 --max-size 0 --desired-capacity 0 --region $LAB_REGION
            aws autoscaling delete-auto-scaling-group --auto-scaling-group-name rebash-web-asg \\
              --force-delete --region $LAB_REGION
            ```

            """
        )
        + localstack_tip(
            "aws --endpoint-url=http://localhost:4566 autoscaling describe-auto-scaling-groups"
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | ASG instances | Two healthy in target group |
            | Scale out | Desired 3 launches third instance |
            | Scale in | Desired 0 terminates instances |
            | Cleanup | ASG and launch template deleted |
            """
        ),
        walkthrough=dedent(
            """\
            | Setting | Detail |
            |---------|--------|
            | `health-check-type ELB` | ASG replaces targets failing ALB checks |
            | Grace period | Delay before health evaluation after launch |
            | Mixed instances | Spot + On-Demand in advanced configs |
            | Template version | `$Latest` vs pinned version for rollbacks |
            """
        ),
        security=dedent(
            """\
            - Launch template enforces IMDSv2 and SSM-only admin
            - Instance role least privilege per app
            - Validate user data does not contain secrets
            """
        ),
        mistakes=[
            ("ASG desired >0 overnight", "EC2 hours accumulate.", "Scale to zero; delete ASG."),
            ("EC2 health only with ALB", "App broken but instance healthy.", "Use ELB health check type."),
            ("No grace period", "Premature termination during boot.", "Set 300s grace for user data."),
        ],
        best_practices=dedent(
            """\
            - Target tracking scaling on CPU or ALB request count
            - Instance refresh for AMI patching
            - Spread across AZs matching ALB subnets
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | Instances cycle | Failed health checks | Fix user data; SG from ALB |
            | Launch fails | Bad AMI or quota | Check EC2 events; request limit increase |
            | ASG won't delete | Instances still running | Set desired 0; force-delete |
            """
        ),
        summary=dedent(
            """\
            - Launch templates version instance config; ASGs maintain capacity across AZs
            - Integrate with ALB health for realistic web tier patterns
            - Scale to zero and delete ASG after labs; monitor billing
            """
        ),
        interview_q=[
            "Launch template vs configuration?",
            "ELB vs EC2 health checks in ASG?",
            "What triggers scale out?",
            "Grace period purpose?",
            "Instance refresh use case?",
            "Mixed instances policy?",
            "Lifecycle hook use case?",
            "Minimum capacity 0 valid?",
            "AZ rebalance behaviour?",
            "How ASG picks subnet for instance?",
        ],
        interview_tips=[
            (2, "EC2 status checks only know hypervisor/network — app can be broken. ELB health checks hit the app path; ASG replaces instances that fail ALB target health — preferred for web tiers behind ALB."),
            (8, "Yes — desired capacity 0 terminates all instances but keeps ASG definition; useful to stop compute charges whilst retaining scaling config, or before delete."),
        ],
        refs=[
            ("Auto Scaling groups", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html"),
            ("Launch templates", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html"),
            ("ELB health checks", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-health-checks.html"),
        ],
    )


def _load_module6() -> None:
    T(
        num=18,
        slug="cloudwatch-metrics-logs-and-alarms",
        title="CloudWatch Metrics, Logs, and Alarms",
        module="Module 6: Ops and Capstone",
        difficulty="intermediate",
        minutes="45 min",
        tags=["aws", "cloudwatch", "metrics", "logs", "alarms"],
        prereq=["Completed Module 5 tutorials", "Running or recently terminated EC2 lab"],
        overview=dedent(
            """\
            **Amazon CloudWatch** collects metrics, logs, and alarms — the default observability layer for AWS.
            Without it, you fly blind during incidents.

            You will publish custom metrics, ship logs with the CloudWatch agent, create an alarm on CPU or
            billing metric, and wire an SNS email notification — then delete alarms and log groups in teardown.
            """
        ),
        objectives=[
            "Navigate EC2 and billing metrics namespaces",
            "Publish custom metric with `put-metric-data`",
            "Create log group and ingest sample logs",
            "Create alarm with SNS email action",
            "Delete alarms and log groups after lab",
        ],
        theory=dedent(
            """\
            ### Metrics

            - **AWS namespaces** — `AWS/EC2`, `AWS/RDS`, `AWS/Billing`
            - **Custom namespaces** — your app KPIs
            - Resolution: standard 1 min; high-resolution down to 1 sec (cost)

            ### Logs

            - **Log groups / streams** — retention configurable (cost control)
            - **CloudWatch agent** on EC2 for file metrics/logs
            - **Logs Insights** query language for triage

            ### Alarms

            States: OK, ALARM, INSUFFICIENT_DATA. Actions: SNS, Auto Scaling, EC2 recover.

            ### Billing alarm

            Legacy `AWS/Billing` metric in `us-east-1` — prefer **AWS Budgets** (Tutorial 2) plus anomaly detection.
            """
        ),
        lab=dedent(
            """\
            ```bash
            aws logs create-log-group --log-group-name /rebash/lab/app --region $LAB_REGION
            aws logs put-log-events --log-group-name /rebash/lab/app --log-stream-name web-01 \\
              --log-events timestamp=$(date +%s000),message="rebash lab log line"

            aws cloudwatch put-metric-data --namespace Rebash/Lab \\
              --metric-name ProcessedRequests --value 42 --unit Count --region $LAB_REGION

            aws sns create-topic --name rebash-alarms --region $LAB_REGION
            aws sns subscribe --topic-arn $SNS_ARN --protocol email --notification-endpoint you@example.com

            aws cloudwatch put-metric-alarm \\
              --alarm-name rebash-high-cpu \\
              --metric-name CPUUtilization --namespace AWS/EC2 \\
              --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold \\
              --evaluation-periods 2 --dimensions Name=InstanceId,Value=$INSTANCE_ID \\
              --alarm-actions $SNS_ARN --region $LAB_REGION
            ```

            Teardown: delete alarms, log group, SNS subscriptions.

            """
        )
        + localstack_tip(
            "aws --endpoint-url=http://localhost:4566 cloudwatch put-metric-data --namespace Lab --metric-name Test --value 1"
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Log event | Visible in log group |
            | Custom metric | Appears in console metrics |
            | SNS | Subscription pending confirm email |
            | Alarm | Shows configured threshold |
            """
        ),
        walkthrough=dedent(
            """\
            | Feature | Use |
            |---------|-----|
            | `put-metric-data` | Custom KPIs from scripts |
            | Agent | Disk/mem logs from EC2 |
            | Alarm actions | SNS for human notification |
            | Retention | Set log group retention to control cost |
            """
        ),
        security=dedent(
            """\
            - Restrict `cloudwatch:PutMetricData` to trusted roles
            - Encrypt log groups with KMS for sensitive apps
            - SNS topic policies least privilege
            """
        ),
        mistakes=[
            ("Infinite log retention", "Storage cost grows.", "Set 7–30 day retention in labs."),
            ("Alarm without SNS confirm", "Emails never arrive.", "Confirm subscription link."),
            ("Wrong Region for billing metric", "Alarm INSUFFICIENT_DATA.", "Billing metrics only in us-east-1."),
        ],
        best_practices=dedent(
            """\
            - Dashboards per service with golden signals
            - Logs Insights saved queries for incidents
            - Composite alarms reduce noise
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | INSUFFICIENT_DATA | Missing metric dimensions | Match instance ID exactly |
            | No logs | Agent not running | Install CloudWatch agent |
            | SNS no email | Unconfirmed subscription | Confirm via email link |
            """
        ),
        summary=dedent(
            """\
            - CloudWatch metrics, logs, and alarms form the AWS observability baseline
            - Pair with SNS for human alerts; use Budgets for cost
            - Set log retention and delete lab alarms after validation
            """
        ),
        interview_q=[
            "Standard vs high-resolution metrics?",
            "Logs Insights vs Athena on S3 logs?",
            "Alarm state INSUFFICIENT_DATA meaning?",
            "Where billing metric lives?",
            "CloudWatch agent vs embedded metric format?",
            "Composite alarm benefit?",
            "Metric dimensions purpose?",
            "Cross-account observability?",
            "Retention cost control?",
            "EventBridge vs CloudWatch alarms?",
        ],
        interview_tips=[
            (3, "Alarm lacks enough data points in evaluation periods — new metric, stopped instance, or wrong dimension. Not OK or ALARM — no action fires until data exists."),
            (4, "Estimated charges metric for billing alarms is published in us-east-1 regardless of resource Regions — a common exam trap."),
        ],
        refs=[
            ("Amazon CloudWatch User Guide", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html"),
            ("CloudWatch Logs", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html"),
            ("Using alarms", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html"),
        ],
    )

    T(
        num=19,
        slug="cloudtrail-config-and-account-guardrails",
        title="CloudTrail, Config, and Account Guardrails",
        module="Module 6: Ops and Capstone",
        difficulty="advanced",
        minutes="50 min",
        tags=["aws", "cloudtrail", "config", "guardrails", "audit"],
        prereq=["Completed [CloudWatch Metrics, Logs, and Alarms](cloudwatch-metrics-logs-and-alarms.md)"],
        overview=dedent(
            """\
            **AWS CloudTrail** records API activity for audit. **AWS Config** tracks resource configuration
            compliance over time. Together they provide guardrails and evidence for security and operations.

            You will enable a trail delivering to S3, run sample API calls, query events, enable Config recorder
            (awareness of cost), and review AWS **Control Tower** / **SCP** concepts for organisations.
            """
        ),
        objectives=[
            "Create multi-Region CloudTrail with S3 delivery and log file validation",
            "Look up events for IAM and EC2 API calls",
            "Enable AWS Config recorder and describe compliance (lab scope)",
            "Explain SCPs and AWS Organizations guardrails",
            "Delete lab trail and Config recorder to avoid storage charges",
        ],
        theory=dedent(
            """\
            ### CloudTrail

            - **Management events** — control plane (who created SG)
            - **Data events** — S3 object ops (optional, extra cost)
            - **Organization trail** — all accounts to central bucket

            ### AWS Config

            Records configuration snapshots and rules (`s3-bucket-public-read-prohibited`).
            Config items bill per recording — disable after lab.

            ### Guardrails hierarchy

            | Layer | Example |
            |-------|---------|
            | SCP | Deny `ec2:RunInstances` except approved types |
            | Config rule | Detect public SG |
            | CloudTrail | Prove who changed SG |
            | IAM policy | Least privilege daily access |

            ### Security Lake / CloudTrail Lake

            Advanced query stores — awareness for SOC teams.
            """
        ),
        lab=dedent(
            """\
            ```bash
            TRAIL_BUCKET=rebash-cloudtrail-$(aws sts get-caller-identity --query Account --output text)

            aws s3api create-bucket --bucket $TRAIL_BUCKET --region $LAB_REGION \\
              --create-bucket-configuration LocationConstraint=$LAB_REGION

            aws cloudtrail create-trail --name rebash-org-trail --s3-bucket-name $TRAIL_BUCKET \\
              --is-multi-region-trail --enable-log-file-validation --region $LAB_REGION

            aws cloudtrail start-logging --name rebash-org-trail --region $LAB_REGION

            aws iam list-users --region $LAB_REGION
            aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=ListUsers \\
              --max-results 5 --region $LAB_REGION

            aws configservice put-configuration-recorder --configuration-recorder name=default,roleARN=$CONFIG_ROLE_ARN
            aws configservice start-configuration-recorder --configuration-recorder-name default
            aws configservice describe-compliance-by-config-rule --config-rule-names s3-bucket-public-read-prohibited
            ```

            Teardown: stop logging, delete trail, empty bucket, stop Config recorder.

            """
        )
        + localstack_tip(
            "aws --endpoint-url=http://localhost:4566 cloudtrail describe-trails"
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Trail logging | `get-trail-status` IsLogging true |
            | Lookup events | ListUsers event found |
            | S3 delivery | Log objects appear in bucket |
            | Config | Recorder started (optional rule compliance) |
            """
        ),
        walkthrough=dedent(
            """\
            | Component | Detail |
            |-----------|--------|
            | Log file validation | Detect tampering of trail files |
            | Multi-Region | Captures activity in all Regions |
            | Config timeline | Who changed resource when |
            | SCP | Organisation-level deny/allow ceiling |
            """
        ),
        security=dedent(
            """\
            - Trail bucket policy allows CloudTrail service only
            - Encrypt trail bucket with SSE-KMS
            - Restrict `cloudtrail:StopLogging` to break-glass roles
            - Centralise logs to security account in organisations
            """
        ),
        mistakes=[
            ("Trail bucket public", "Audit log exposure.", "Block Public Access on trail bucket."),
            ("Config left recording", "Per-item charges.", "Stop recorder after lab."),
            ("No log validation", "Tampering undetected.", "Enable validation on trails."),
        ],
        best_practices=dedent(
            """\
            - Organization trail to immutable S3 with lifecycle to Glacier
            - Config conformance packs for CIS benchmarks
            - Integrate with Security Hub for findings aggregation
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | Trail not delivering | Bucket policy | Apply CloudTrail bucket policy template |
            | Lookup empty | Wrong Region/attribute | Use event time window; correct EventName |
            | Config failed | Missing service role | Create aws-config-role |
            """
        ),
        summary=dedent(
            """\
            - CloudTrail proves **who did what**; Config tracks **resource state**
            - Layer SCPs, Config rules, and IAM for defence in depth
            - Delete lab trails and stop Config to control storage costs
            """
        ),
        interview_q=[
            "Management vs data events in CloudTrail?",
            "Why multi-Region trail?",
            "Config vs CloudTrail?",
            "SCP vs IAM policy?",
            "Log file validation purpose?",
            "CloudTrail Lake benefit?",
            "How detect public S3 automatically?",
            "Organization trail advantage?",
            "Who can stop CloudTrail logging?",
            "Immutable audit storage pattern?",
        ],
        interview_tips=[
            (3, "CloudTrail is an event log of API calls — audit trail. Config is configuration snapshots over time with rules evaluating compliance — 'is this SG open now?' vs 'who opened it?' — complementary."),
            (4, "SCP is an organisation guardrail applied to accounts/OUs — maximum permissions ceiling even for admin IAM users in member accounts. IAM policies grant permissions within that ceiling."),
        ],
        refs=[
            ("AWS CloudTrail User Guide", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html"),
            ("AWS Config", "https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html"),
            ("Service control policies", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html"),
        ],
    )

    T(
        num=20,
        slug="lambda-and-three-tier-capstone",
        title="Lambda and Three-Tier Capstone",
        module="Module 6: Ops and Capstone",
        difficulty="advanced",
        minutes="60 min",
        tags=["aws", "lambda", "capstone", "three-tier", "terraform"],
        prereq=[
            "Completed tutorials 1–19 or equivalent AWS fundamentals",
            "Conceptual readiness for [Terraform](../terraform/index.md) automation",
        ],
        overview=dedent(
            """\
            Capstone time: sketch a **three-tier web application** on AWS — ALB web tier, optional Lambda for
            API events, RDS data tier, private subnets, SSM admin, CloudWatch observability, and IAM roles
            throughout. You will deploy a minimal Lambda behind API Gateway (or ALB Lambda target) and document
            the **Terraform handoff** — how this track maps to modules in the REBASH Terraform curriculum.

            Destroy **all** capstone resources and confirm billing alarms before celebrating completion.
            """
        ),
        objectives=[
            "Diagram three-tier flow: client → ALB → app (EC2/ASG) → RDS",
            "Create Lambda execution role with least privilege",
            "Deploy Python Lambda via CLI zip package (lab scale)",
            "Explain where Lambda fits versus EC2 for API workloads",
            "Produce Terraform module map for automating this architecture",
        ],
        theory=dedent(
            """\
            ### Three-tier on AWS (reference architecture)

            ```
            Internet → Route 53 → ALB (public subnets)
                              → EC2 ASG (private or public+SSM lab pattern)
                              → RDS (private subnets, SG from app tier)
            Sidecar: Lambda for async tasks, S3 for static assets, CloudWatch + CloudTrail for ops
            ```

            ### Lambda fundamentals

            - **Execution role** — trust `lambda.amazonaws.com`
            - **Package** — zip or container image
            - **Triggers** — API Gateway HTTP API, ALB, S3 events, EventBridge
            - **VPC** — optional ENIs for RDS access (cold start + NAT/endpoints trade-off)

            ### When Lambda vs EC2

            | Lambda | EC2/ASG |
            |--------|---------|
            | Spiky short requests | Long-lived connections |
            | Ops overhead minimal | Full OS control |
            | 15 min max timeout | Persistent workers |

            ### Terraform handoff

            | AWS track concept | Terraform resource (next steps) |
            |-------------------|----------------------------------|
            | VPC + subnets | `aws_vpc`, `aws_subnet` modules |
            | ALB + ASG | `aws_lb`, `aws_autoscaling_group` |
            | RDS | `aws_db_instance` in private subnets |
            | Lambda | `aws_lambda_function`, `aws_iam_role` |
            | Remote state | S3 + DynamoDB lock (Terraform Module 5+) |

            Proceed to [Introduction to Terraform and IaC](../terraform/introduction-to-terraform-and-iac.md).
            """
        ),
        lab=dedent(
            """\
            ### Part A — Lambda hello (CLI)

            `trust-lambda.json`:

            ```json
            {
              "Version": "2012-10-17",
              "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
              }]
            }
            ```

            ```bash
            aws iam create-role --role-name rebash-lambda-basic \\
              --assume-role-policy-document file://trust-lambda.json

            aws iam attach-role-policy --role-name rebash-lambda-basic \\
              --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

            cat > handler.py <<'EOF'
            import json
            def handler(event, context):
                return {"statusCode": 200, "body": json.dumps({"message": "rebash capstone ok"})}
            EOF
            zip function.zip handler.py

            aws lambda create-function --function-name rebash-capstone-fn \\
              --runtime python3.12 --role arn:aws:iam::ACCOUNT:role/rebash-lambda-basic \\
              --handler handler.handler --zip-file fileb://function.zip --region $LAB_REGION

            aws lambda invoke --function-name rebash-capstone-fn out.json --region $LAB_REGION
            cat out.json
            ```

            ### Part B — Architecture document

            Write `~/rebash-aws/capstone-architecture.md` listing:

            - VPC IDs/subnets from Module 2
            - ALB + ASG from Module 5
            - RDS endpoint (destroyed) pattern
            - Lambda role ARN
            - CloudWatch log group for Lambda `/aws/lambda/rebash-capstone-fn`
            - Terraform modules you would create next

            ### Part C — Full teardown

            ```bash
            aws lambda delete-function --function-name rebash-capstone-fn --region $LAB_REGION
            aws iam detach-role-policy --role-name rebash-lambda-basic \\
              --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
            aws iam delete-role --role-name rebash-lambda-basic
            # ASG, ALB, RDS, VPC — complete teardown checklist from Tutorial 2
            ```

            """
        )
        + localstack_tip(
            """\
            aws --endpoint-url=http://localhost:4566 lambda create-function --function-name lab-fn ...
            aws --endpoint-url=http://localhost:4566 lambda invoke --function-name lab-fn out.json
            """
        ),
        validation=dedent(
            """\
            | Check | Pass criteria |
            |-------|---------------|
            | Lambda invoke | HTTP 200 message in payload |
            | Architecture doc | All tiers documented |
            | IAM role | Basic execution only — no admin |
            | Teardown | Lambda, role, and prior module resources gone |
            | Billing | Budget alarm quiet |
            """
        ),
        walkthrough=dedent(
            """\
            | Piece | Capstone role |
            |-------|---------------|
            | ALB | Public entry, TLS termination |
            | ASG | Scalable stateless web tier |
            | RDS | Stateful data — private only |
            | Lambda | Event-driven/API functions without servers |
            | Terraform | Repeatable module stack in next track |
            """
        ),
        security=dedent(
            """\
            - Lambda role least privilege per function — not one shared admin role
            - API Gateway auth (JWT/IAM) before public Lambda URLs
            - RDS never public; secrets in Secrets Manager
            - CloudTrail enabled for capstone API changes
            """
        ),
        mistakes=[
            ("Lambda admin role", "Function code compromise = full account.", "Scope policy to logs + specific AWS APIs needed."),
            ("Public RDS for Lambda convenience", "Database scanned.", "Lambda in VPC with SG to RDS only."),
            ("Skipping final teardown", "ALB+NAT+RDS surprise bill.", "Run full checklist Tutorial 2."),
        ],
        best_practices=dedent(
            """\
            - IaC everything in Terraform modules after this capstone
            - Separate accounts for prod/non-prod via Organizations
            - Observability dashboards before go-live
            - Regular game days failing AZs and RDS failover
            """
        ),
        troubleshooting=dedent(
            """\
            | Issue | Cause | Fix |
            |-------|-------|-----|
            | Lambda timeout VPC | ENI setup | Increase timeout; check subnets/SG |
            | Invoke access denied | Role trust | Fix execution role trust policy |
            | 502 API GW | Bad proxy integration | Match handler response format |
            | Terraform handoff gaps | Manual resources | Import or recreate in HCL modules |
            """
        ),
        summary=dedent(
            """\
            - Three-tier AWS: Route 53 → ALB → compute → RDS with private networking and IAM roles
            - Lambda suits event/API workloads; EC2/ASG suits long-lived apps
            - **Destroy all capstone resources**; continue to **Terraform** to automate the stack
            """
        ),
        interview_q=[
            "Draw three-tier AWS architecture with AZs.",
            "Lambda execution role vs instance profile?",
            "Lambda in VPC pros/cons?",
            "How ALB targets Lambda?",
            "Where store DB credentials?",
            "Blue/green on ASG approach?",
            "CloudWatch for Lambda defaults?",
            "Terraform module boundaries for VPC vs app?",
            "SCP guarding prod account?",
            "Cost optimisations for lab vs prod?",
        ],
        interview_tips=[
            (1, "Public subnets: ALB only. Private subnets: app tier ASG and RDS Multi-AZ. Route 53 alias to ALB. SGs: ALB→app on 443/80, app→RDS on DB port. SSM for admin, no SSH. CloudWatch alarms on CPU/error rate."),
            (8, "Typical modules: `network` (VPC, subnets, endpoints), `compute` (ASG, launch template), `data` (RDS, subnet group), `edge` (ALB, Route53), `lambda` (function + IAM), composed by `envs/dev|prod` roots with remote state."),
        ],
        refs=[
            ("AWS Lambda Developer Guide", "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"),
            ("Lambda IAM roles", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html"),
            ("Three-tier architecture whitepaper", "https://docs.aws.amazon.com/whitepapers/latest/aws-overview/solutions.html"),
            ("Terraform AWS provider", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs"),
        ],
        related_extra=[
            "- Next track: [Introduction to Terraform and IaC](../terraform/introduction-to-terraform-and-iac.md)",
            "- [DevOps Engineer learning path](../learning-paths/devops-engineer.md)",
        ],
    )


if __name__ == "__main__":
    load_tutorials()
    main()
