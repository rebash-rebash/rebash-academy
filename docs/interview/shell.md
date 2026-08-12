---
title: "Shell Interview Preparation"
description: "35 curated Shell interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: shell
tags:
  - interview
  - shell
comments: false
---

{% raw %}
# Shell Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What are artifacts, and how do you manage them in a pipeline?**

??? success "Reveal answer"
    Artifacts are the actual build outputs -- JAR/WAR files, Docker images, zip packages, binaries. I manage them by
    storing them in a repository like Nexus, Artifactory, or Docker Hub, versioning and tagging each one based on the
    release or build number for traceability and rollback, and applying retention policies so old, unused artifacts don't
    accumulate indefinitely.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**2. What are Sticky Sessions and how are they used in DevOps?**

??? success "Reveal answer"
    Sticky sessions configure a load balancer to consistently route a given user's requests to the same backend
    instance, which matters for stateful applications that store session data locally rather than in a shared external store.
    I generally prefer designing stateless services that don't need sticky sessions at all, since they scale and fail over
    more cleanly.

**3. [ ] What is a recent challenge you faced while implementing a DevOps practice or pipeline in your team or organization?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Shell components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**4. What are YAML Pipelines, and how do they differ from Classic Pipelines?**

??? success "Reveal answer"
    YAML Pipelines are defined in a file checked into the source repo, giving version control and easier collaboration,
    while Classic Pipelines use a visual designer in the portal. YAML Pipelines are more flexible, reusable, and versioned
    alongside the application, which is why I default to them for anything beyond a quick proof of concept.

**5. What is the difference between Declarative and Scripted pipelines?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**6. Can you tell me the difference between single ampersand (&) and double ampersand (&&) in shell scripting?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**7. What is the purpose of agent, post-conditions and environment blocks in pipeline?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**8. What are the tools you have used for CI/CD pipeline?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**9. What is the controller used to manage the self managed worker nodes?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**10. What is runs-on in a pipeline? Which type of runners are you using in your organization, and do you know how to configure self-hosted runners?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**11. What are webhooks, and have you used them anywhere?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**12. Difference between build artificats and pipeline artifacts and which one is better?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**13. What is the command or pipeline syntax used to refer the variable output of the previous stage in the current stage?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**14. What are some main differences between scripted and declarative pipeline?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**15. What is the purpose of a webhook, and how is it used in a CI/CD pipeline?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**16. what are the best practices can be used to keep the systems highly available?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**17. What is the difference between Find and sed ?**

??? success "Reveal answer"
    Start with a precise definition in the context of Shell, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**18. What is the use of the subprocess module in DevOps scripting?**

??? success "Reveal answer"
    subprocess lets a Python script spawn and manage other processes, capturing their output and return codes, which
    is useful for automating shell commands, deploying code, or wrapping CLI tools like Docker directly inside a Python
    automation script.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**19. What is a Route Table and how is it used in DevOps?**

??? success "Reveal answer"
    A route table controls how traffic flows between subnets and out to gateways -- in AWS it's the actual mechanism
    that determines whether a subnet is public or private, based on whether its route table sends 0.0.0.0/0 traffic to an
    internet gateway or a NAT gateway.

## Scenarios and troubleshooting

**20. Pipeline fails only on Tuesdays, no code changes — how do you debug?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Shell, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**21. Can you share an experience where your automation strategy failed or caused problems? What was your corrective action?,?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Shell, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**22. Write a script to capture the failures?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Shell, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**23. If the pipeline fails due to existing resources, how do you handle RIP (Remove, Import, Plan)?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Shell, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**24. if you were required to run pre-task checks, main tasks and post-task validation for patch automation, how would you structure your RedHat Automation & Virtulization scripts?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Shell components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**25. Do you have experience with AWS DevOps services like CodeDeploy, CodeBuild, and CodePipeline? How would you set up a pipeline using them?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Shell components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**26. Your CI pipeline is flaky — tests pass locally but fail in CI 30% of the time. What are the causes?**

??? success "Reveal answer"
    1. Tests depend on external services (network, time). 2) Parallel test interference (shared 
    database state). 3) Resource constraints (OOM in CI). 4) Timezone differences. 5) Non-
    deterministic test order. Fix: mock externals, isolate test databases, use --runInBand, set 
    timeouts.

## Practice questions

**27. What tools have you used for CI/CD, and why did you choose them?**

??? success "Reveal answer"
    Jenkins for its flexibility and huge plugin ecosystem across almost any tech stack; GitHub Actions for smaller projects
    or where deep GitHub integration matters; GitLab CI when the codebase is already hosted on GitLab, for the
    seamless built-in integration; ArgoCD specifically for GitOps-based delivery into Kubernetes; Docker for consistent
    packaging across environments; and Terraform for automating the infrastructure the pipeline deploys into.

**28. How do you migrate a monolith application to microservices with zero downtime?**

??? success "Reveal answer"
    FINAL SECTION: SCENARIO-BASED &
    
     
    Use the Strangler Fig pattern: 1) Put a proxy/API gateway in front of the monolith. 2) Extract one 
    service at a time — start with the least coupled. 3) Route traffic for the extracted feature to the 
    new service via the proxy. 4) Verify with feature flags. 5) Repeat until monolith is empty. Never do 
    a big-bang rewrite.

**29. Q21. How do you handle multi-environment pipelines?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Shell components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**30. Q5. How do you create auto scaling policies based on memory & disk usage?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Shell components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**31. How do you trigger a pipeline if:?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Shell components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**32. You have a multi-cloud environment. How do you manage pipelines for all those cloud environments?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Shell components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**33. How do you roll back a bad database migration?**

??? success "Reveal answer"
    1. If backward-compatible migration: redeploy old app code — it works with new schema. 
    2) If breaking change was applied: run the rollback script (Liquibase rollback, Flyway 
    undo). 3) Last resort: restore from pre-migration snapshot. Lesson: always test migrations 
    on a production-size staging copy first.

**34. How do you ensure the maintainability of Selenium test scripts?**

??? success "Reveal answer"
    The Page Object Model separates locators and page interactions from test logic, so a UI change only requires
    updating one page object. I also modularize tests into reusable methods, use consistent naming conventions, and
    keep everything in version control to track changes and collaborate.

**35. How is EIGRP used in DevOps?**

??? success "Reveal answer"
    EIGRP is a Cisco routing protocol I've mostly encountered in legacy, on-prem environments for managing internal
    routing efficiently -- it's less relevant in pure cloud-native setups but still shows up in hybrid infrastructure with a
    traditional networking footprint.

## Related

- Course: [Shell](../shell/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
