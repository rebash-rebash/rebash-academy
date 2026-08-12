---
title: "Python Interview Preparation"
description: "20 curated Python interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: python
tags:
  - interview
  - python
comments: false
---

{% raw %}
# Python Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is Python's role in DevOps?**

??? success "Reveal answer"
    Python's simplicity and rich ecosystem make it useful for automating infrastructure as code alongside tools like
    Terraform and Ansible, scripting steps in CI/CD pipelines, and building monitoring and logging integrations with tools
    like Prometheus or Grafana APIs where the built-in tooling doesn't cover a specific need.

**2. What are Lists and Tuples in Python?**

??? success "Reveal answer"
    Start with a precise definition in the context of Python, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**3. What is search keyword in Python?**

??? success "Reveal answer"
    Start with a precise definition in the context of Python, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**4. What is the difference between shallow copy and deep copy in Python?**

??? success "Reveal answer"
    Start with a precise definition in the context of Python, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**5. what is list and tuple in python?**

??? success "Reveal answer"
    Start with a precise definition in the context of Python, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**6. What are decorators in Python?**

??? success "Reveal answer"
    Start with a precise definition in the context of Python, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**7. What is the difference between set and list in python(Counter question of the above)?**

??? success "Reveal answer"
    Start with a precise definition in the context of Python, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**8. Can you explain how Python works with cloud services in DevOps?**

??? success "Reveal answer"
    Cloud SDKs like Boto3 for AWS let Python interact directly with services -- listing S3 buckets, managing EC2
    instances -- which is how I've automated infrastructure provisioning, deployment, and scaling tasks beyond what the
    CLI conveniently covers.

**9. How does Python's GIL affect multi-threaded web service performance and what alternatives exist to overcome it? what is Python's GIL affect multi-threaded web service?**

??? success "Reveal answer"
    Answer directly for Python: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**10. In Python, what are lists and tuples, and how do they differ?**

??? success "Reveal answer"
    Answer directly for Python: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

## Scenarios and troubleshooting

**11. If a Python program is failing due to memory issues, what can be the cause?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Python, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**12. Write a Python function that takes a list of dictionaries representing job logs. The function should return a list of job IDs where the "status" is "FAILED"?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Python, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**13. How would you manage environment variables in Python for a DevOps project?**

??? success "Reveal answer"
    The os module reads environment variables directly -- os.getenv("DATABASE_URL", "default_value") -- and for
    more structured or sensitive management I'd use something like python-dotenv locally or Docker secrets in
    containerized deployments.

## Practice questions

**14. How do you handle exceptions in Python scripts for DevOps automation?**

??? success "Reveal answer"
    try-except blocks around anything that can fail, catching specific exceptions like subprocess.CalledProcessError
    rather than a bare except, logging the actual error with useful context, and optionally triggering a retry mechanism for
    genuinely transient failures.

**15. How do you use Python to monitor server health in DevOps?**

??? success "Reveal answer"
    The psutil library gives direct access to CPU and memory usage -- psutil.cpu_percent() and psutil.virtual_memory() --
    which I can extend to push those metrics into Prometheus or Grafana for ongoing monitoring rather than just a
    one-off check.

**16. write python program for reverse a string?**

??? success "Reveal answer"
    Outline the solution first, then give a minimal correct example (commands or config sketch).
    
    Call out the production hardening you would add next (pin versions, least privilege, secrets, health checks) and how you would validate the result.

**17. Can you write code in Python? (Provided some samples)?**

??? success "Reveal answer"
    Outline the solution first, then give a minimal correct example (commands or config sketch).
    
    Call out the production hardening you would add next (pin versions, least privilege, secrets, health checks) and how you would validate the result.

**18. Create a python script for this requirement?**

??? success "Reveal answer"
    Outline the solution first, then give a minimal correct example (commands or config sketch).
    
    Call out the production hardening you would add next (pin versions, least privilege, secrets, health checks) and how you would validate the result.

**19. Do you have any experience on python scripting?**

??? success "Reveal answer"
    Answer directly for Python: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**20. How to configure the Flask in Jenkin, tell me procedure ?**

??? success "Reveal answer"
    Answer directly for Python: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

## Related

- Course: [Python](../python/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
