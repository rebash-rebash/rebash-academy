---
title: "DevOps Fundamentals Interview Preparation"
description: "40 curated DevOps Fundamentals interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: devops
tags:
  - interview
  - devops
comments: false
---

{% raw %}
# DevOps Fundamentals Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. The server is extremely slow. How do you identify if the issue is CPU related and what is causing i?**

??? success "Reveal answer"
    + Check load average: uptime or w (run queue > CPU cores?) * Performance troubleshooting skills
    + Use top/htop to see high CPU processes. + Linux command knowledge
    - 9 + Use mpstat -P ALL 1 to check per-core usage. * Root cause isolation ability
    + Use pidstat -u 1 to monitor CPU per process. * Understanding of system behaviour
    -93 . ever dee reneiey processes: i loops, or high context switching. * Practical resolution approach
    + KillZunlimit or optimize the offending process.
    —> i
    : He i ?
    hy os = pean high ae eras leak? airline bia a;
    e free - vmstat 1 to understand memory usage. ea
    id + Use top/htop and sort by %MEM. F 3 . )
    + Use ps aux --sort--%mem to find memory hungry processes. . . : meee
    9 + Use smem -r or pmap <pid> to analyze memory usage. =_Understending of 0004
    + Check dmesg for OOM killer logs. * Root cause identification
    — ) + Restart/leak-fix the application or increase memory if required. * Correct remediation
    4 BD Tracie ta: Al oe gpa Pind aha Ab -eenendng. pane ‘
    and how do you free it safely? _ a
    PY ANS: + Run df -h to see full partitions. *…

## Scenarios and troubleshooting

**2. How would you handle scenarios where the payment succeeds but the order or shipping service fails?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**3. If a production instance is failing, what can be the possible causes?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**4. New image has been deployed in production but it fails immediately what steps would you take ?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**5. In Airflow, if a job fails, how do you debug it?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**6. Q4: now it is hosted and one of the services is leaking memory, how would you troubleshoot?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**7. How would you design an architecture for a 2 tier application?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**8. You are onboarding a new customer with 5 million+ users. How would you design the complete application architecture as a Solution Architect?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**9. If there is a sudden spike in traffic on the server, how will you troubleshoot it?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**10. If a rollback fails, how will you handle it?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**11. Q15. What is your approach to debug a CrashLoopBackOff?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**12. Are readiness probes failing?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**13. If clients reporting 504 Gateway Timeout errors. describe your approach to debugging the issue?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**14. How failover and failback happens in DRS?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**15. How do you ensure accountability and ownership in a DevOps team, especially during failures?,?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**16. I am getting the following error, how can I debug that and what does the error mean?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**17. If you're facing performance issues on a server, how do you troubleshoot?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**18. How would you redeploy this application with zero down time?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**19. You have a crashbackloop error. How would you fix this error?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**20. What happens if master node fails suddenly?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**21. How do you implement a retry mechanism for a failed API call?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**22. explain the production issue which you have faced?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**23. Failover happend in DB, so connection is switched from A to B, during this time interval, if user is writing some data, how to manage that ?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Devops, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**24. How would you restrict everything except two services?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**25. how would you implement optimistic locking a RESTful update endpoint to avoid lost updates?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**26. How would you secure the web app running in cloud from oswsap10 attacks,?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**27. How would you get application level metrics?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**28. How would you manage these microservices?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**29. How would you expose the application?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**30. How would you update the image and deploy them?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**31. If you have an on-prem application, how would you migrate and deploy it in a cloud-native environment?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**32. How would you structure disaster recovery for your applciation?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**33. How would you perform database migration for your database application?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**34. How would you provision karpenter. What all things are needed in configuration?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**35. What is CrashLoopBackOff, and how do you troubleshoot it?**

??? success "Reveal answer"
    Start with a precise definition in the context of Devops, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**36. What is your approach of doing a troubleshooting?**

??? success "Reveal answer"
    Start with a precise definition in the context of Devops, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

## Practice questions

**37. What challenges have you faced implementing DevOps in previous projects?**

??? success "Reveal answer"
    Cultural resistance is usually the biggest one -- dev and ops teams that are used to working in silos don't
    automatically start collaborating just because you introduce a pipeline. Tool integration is another, especially with
    legacy systems that weren't built with automation in mind; skill gaps on tools like Jenkins, Docker, or Kubernetes can
    slow early adoption; managing infrastructure through IaC requires a mindset shift for teams used to manual
    provisioning; and folding security checks into CI/CD, real DevSecOps, adds real complexity when deployments are
    frequent and compliance still needs to be satisfied.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    2
    GENERAL NETWORKING QUESTIONS FOR DEVOPS

**38. Design an architecture for the scenario: if I type www.application.com it should get resolved to the backend service?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**39. If U want to design a infra for high scalablity, how did u do that?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**40. Create system design for three tier architecture with secuirty and avalability in place?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Devops components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

## Related

- Hub: [Interview Preparation](index.md)
{% endraw %}
