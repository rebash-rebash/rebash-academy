---
title: "Python Interview Preparation"
description: "21 curated Python interview prompts — model answers plus real interview questions collected across companies (deduplicated by topic)."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

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

**2. Can you explain how Python works with cloud services in DevOps?**

??? success "Reveal answer"
    Cloud SDKs like Boto3 for AWS let Python interact directly with services -- listing S3 buckets, managing EC2
    instances -- which is how I've automated infrastructure provisioning, deployment, and scaling tasks beyond what the
    CLI conveniently covers.

**3. What is Locust?**

??? success "Reveal answer"
    A Python-based load testing tool. Define user behaviour in Python, then simulate thousands of 
    concurrent users. Easy to write complex test scenarios.

## Scenarios and troubleshooting

**4. How would you manage environment variables in Python for a DevOps project?**

??? success "Reveal answer"
    The os module reads environment variables directly -- os.getenv("DATABASE_URL", "default_value") -- and for
    more structured or sensitive management I'd use something like python-dotenv locally or Docker secrets in
    containerized deployments.

## Practice questions

**5. How do you handle exceptions in Python scripts for DevOps automation?**

??? success "Reveal answer"
    try-except blocks around anything that can fail, catching specific exceptions like subprocess.CalledProcessError
    rather than a bare except, logging the actual error with useful context, and optionally triggering a retry mechanism for
    genuinely transient failures.

**6. How do you use Python to monitor server health in DevOps?**

??? success "Reveal answer"
    The psutil library gives direct access to CPU and memory usage -- psutil.cpu_percent() and psutil.virtual_memory() --
    which I can extend to push those metrics into Prometheus or Grafana for ongoing monitoring rather than just a
    one-off check.

## Real interview prompts

Additional questions reported from real DevOps / SRE interviews. Company names are omitted — practise these out loud without notes.

- How does Python's GIL affect multi-threaded web service performance and what alternatives exist to overcome it? what is Python's GIL affect multi-threaded web service?
- Write a Python function that takes a list of dictionaries representing job logs. The function should return a list of job IDs where the "status" is "FAILED"?
- What is the difference between set and list in python(Counter question of the above)?
- If a Python program is failing due to memory issues, what can be the cause?
- What is the difference between shallow copy and deep copy in Python?
- In Python, what are lists and tuples, and how do they differ?
- How to configure the Flask in Jenkin, tell me procedure ?
- Can you write code in Python? (Provided some samples)?
- Do you have any experience on python scripting?
- Create a python script for this requirement?
- write python program for reverse a string?
- What are Lists and Tuples in Python?
- What is search keyword in Python?
- what is list and tuple in python?
- What are decorators in Python?

## Related

- Course: [Python](../python/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
