---
title: "Shell Interview Preparation"
description: "55 curated Shell interview prompts — model answers plus real interview questions collected across companies (deduplicated by topic)."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

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

**3. What is Configuration Management?**

??? success "Reveal answer"
    It is a method through which we automate admin tasks. Each and every minute detail of a system is
    called configuration details. If we do any change here, we are changing the configuration of the
    machine. System administrators used to manage configuration manually. DevOps engineers manage
    this configuration automatically using configuration management tools.

**4. What are YAML Pipelines, and how do they differ from Classic Pipelines?**

??? success "Reveal answer"
    YAML Pipelines are defined in a file checked into the source repo, giving version control and easier collaboration,
    while Classic Pipelines use a visual designer in the portal. YAML Pipelines are more flexible, reusable, and versioned
    alongside the application, which is why I default to them for anything beyond a quick proof of concept.

**5. What is a shell script?**

??? success "Reveal answer"
    Give an example of how you might use it in DevOps.
    A shell script automates a sequence of commands for a shell interpreter like Bash. I use them for things like
    deploying an application, applying server configuration changes, or scheduling routine backups -- anywhere a
    repeatable sequence of commands would otherwise be run manually.

**6. What is the use of the subprocess module in DevOps scripting?**

??? success "Reveal answer"
    subprocess lets a Python script spawn and manage other processes, capturing their output and return codes, which
    is useful for automating shell commands, deploying code, or wrapping CLI tools like Docker directly inside a Python
    automation script.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**7. What are the problems system admins used to face without configuration management tools?**

??? success "Reveal answer"
    • Managing users & groups is a big hectic thing (create, delete, edit...)
    • Dealing with packages (Installing, Upgrading & Uninstalling)
    • Taking backups on regular basis manually
    • Deploying all kinds of applications in servers
    • Configure services (Starting, stopping and restarting services)

**8. What is a Route Table and how is it used in DevOps?**

??? success "Reveal answer"
    A route table controls how traffic flows between subnets and out to gateways -- in AWS it's the actual mechanism
    that determines whether a subnet is public or private, based on whether its route table sends 0.0.0.0/0 traffic to an
    internet gateway or a NAT gateway.

**9. What is semgrep?**

??? success "Reveal answer"
    A static analysis tool for finding bugs and security issues using pattern-based rules. Faster and 
    more customizable than traditional SAST tools. Rules can be written in YAML without knowing 
    the language internals. 
     
     
    
     
    OBSERVABILITY & SRE (20 Questions)

**10. What is Tunneling and how is it used in DevOps?**

??? success "Reveal answer"
    Tunneling encapsulates one network protocol inside another to create a secure or otherwise unsupported path
    between networks -- SSH tunnels and VPNs are common examples I use for securely reaching cloud resources or
    bridging separate network environments.

**11. Explain the purpose of the grep command in Linux.**

??? success "Reveal answer"
    grep searches for specific patterns within files or command output, letting me extract exactly the relevant lines by
    matching regular expressions or plain strings -- it's one of the tools I reach for constantly when digging through logs.

**12. What is DynamoDB's partition key?**

??? success "Reveal answer"
    The primary attribute used to distribute data across partitions. Poor partition key choice (e.g., 
    using date/status with low cardinality) causes "hot partitions" — all traffic goes to one partition, 
    causing throttling.

**13. What is Logstash pipeline throughput tuning?**

??? success "Reveal answer"
    Key settings: pipeline.workers (parallel filter threads, set to CPU 
    count), pipeline.batch.size (events per batch, higher = more throughput, more 
    memory), pipeline.batch.delay (wait time for batch to fill).

**14. What is the difference between Declarative and Scripted pipelines?**

??? success "Reveal answer"
    Declarative has a rigid predefined structure (pipeline {} block), easier to read and validate. 
    Scripted uses Groovy's node {} block with full programming flexibility but no structural 
    validation.

**15. What is the purpose of post {} in a Declarative pipeline?**

??? success "Reveal answer"
    Defines actions to run after all stages complete, regardless of the result — e.g., send notifications, 
    clean workspace, archive artifacts. Supports always, success, failure, unstable.

**16. What is an Azure Pipeline YAML stage?**

??? success "Reveal answer"
    A major division of a pipeline, containing jobs. Stages run sequentially by default but can be 
    configured to run in parallel. Each stage can have its own approval requirements.

**17. What is a self-hosted runner group?**

??? success "Reveal answer"
    A collection of self-hosted runners assigned to specific organizations or repositories. Used for 
    access control — only certain repos can use certain runners.

**18. What are variables in Shell Scripting?**

??? success "Reveal answer"
    Variables store values for reuse.
    eee
    NAME="DevOps"
    echo $NAME
    @ Avoid spaces around = while assigning values.
    @ Intermediate
    e e e
    a6 im Explain if-else in

**19. What is the script {} block in Declarative pipelines?**

??? success "Reveal answer"
    Allows embedding Scripted pipeline Groovy code inside a Declarative pipeline for complex logic 
    like loops, conditionals, and dynamic stage creation.

**20. What is actions/github-script?**

??? success "Reveal answer"
    Runs JavaScript code with access to the GitHub API and workflow context. Used for commenting 
    on PRs, creating issues, and complex conditional logic.

**21. What is the difference between text and keyword field types?**

??? success "Reveal answer"
    text is analyzed (tokenized, lowercased) — used for full-text search. keyword is not analyzed — 
    used for exact matching, aggregations, and sorting.

**22. What is hashFiles() function?**

??? success "Reveal answer"
    Generates a hash of specified files — commonly used in cache keys. 
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}

## Scenarios and troubleshooting

**23. A pipeline failed in the build stage. How do you troubleshoot?**

??? success "Reveal answer"
    + Check build logs for compilation/test errors. * Debugging skills )
    + Verify code changes, dependencies, and build scripts. * Reproducibility approach
    + Reproduce the failure locally or in a container. % Knowledge of build tools
    + Check environment, cache, and artifact repository access. * Environment awareness
    + Fix the issue and re-run the pipeline with version control. * Efficient problem isolation
    © AQ: A pipeline failed in the deploy stage. What could be the causes and how do you fix it? 
    ANS: + Causes: Config issues, failed health checks, insufficient permissions, * Identifying possible causes
    bad artifacts, resource limits, network issues. * Cloud/K8s/Infra knowledge
    + Check deployment logs, events, and target environment health. * Security & permission awareness
    + Validate IAM roles, secrets, and cluster access. * Fast recovery mindset
    + Fix the root cause and redeploy or rollback. * Clear action plan |
    (G)

**24. Your CI pipeline is flaky — tests pass locally but fail in CI 30% of the time. What are the causes?**

??? success "Reveal answer"
    1. Tests depend on external services (network, time). 2) Parallel test interference (shared 
    database state). 3) Resource constraints (OOM in CI). 4) Timezone differences. 5) Non-
    deterministic test order. Fix: mock externals, isolate test databases, use --runInBand, set 
    timeouts.

**25. What is MTBF (Mean Time Between Failures)?**

??? success "Reveal answer"
    Average time between failures. Increased by improving reliability, adding redundancy, and 
    thorough testing.

## Practice questions

**26. Design a URL shortener like bit.ly. ; HIGH LEVEL ARCHITECTURE 7} . ah ‘i °?**

??? success "Reveal answer"
    « Write path: User -> API -> Generate short code -> Store mapping. let 4 caus gna)
    - 9 + Read path: Short URL ~» API =» Lecbup -» Redirect. Raicd iss, 8
    + Use base62 encoding for short IDs. Weegee, 2 = =. @B — =]
    -@ + Store in sealable DB (Cassandra / DynameD8). nee my tat Cig Pai 77
    + Cache hot mappings in Redis. 5 Rawicai eo .
    -@ + Track analytics (clicks, geo, device). coll] rine Bx. }
    -s @ a: design a system to handle 1004 DAV (Daily Active Uses) micas Grane saieaieammeane
    * Scalability thinking 5 = ag aoe
    hae “se. | 8-O-8-88
    + Auto-scaling (horizontal) based on metrics. pigehenereggis = ba | a
    + Asynchoneous processing for non-critical tasks. e Resili & foult tol
    OG mene? 
    -o ANS: . Real-time messaging with WebSocket / MOTT. # Real-time communication my . - @ -: i= + x
    -~ 9 + Presence service using in-memory store. a Raliebility & “ 6 —-—R ’
    + Delivery quarenates: ACKs & retrias. ;
    ; a ge no waa aie cad @ (s) all
    - eo + End-to-end encryption for security. aS ae Aaneer po sae tose aie
    0 FLOW
    Do dangn « vider srnaning platform 
    ANS: . Upload -» Transcode -»…

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

**29. How do you roll back a bad database migration?**

??? success "Reveal answer"
    1. If backward-compatible migration: redeploy old app code — it works with new schema. 
    2) If breaking change was applied: run the rollback script (Liquibase rollback, Flyway 
    undo). 3) Last resort: restore from pre-migration snapshot. Lesson: always test migrations 
    on a production-size staging copy first.

**30. How do you ensure the maintainability of Selenium test scripts?**

??? success "Reveal answer"
    The Page Object Model separates locators and page interactions from test logic, so a UI change only requires
    updating one page object. I also modularize tests into reusable methods, use consistent naming conventions, and
    keep everything in version control to track changes and collaborate.

**31. How is EIGRP used in DevOps?**

??? success "Reveal answer"
    EIGRP is a Cisco routing protocol I've mostly encountered in legacy, on-prem environments for managing internal
    routing efficiently -- it's less relevant in pure cloud-native setups but still shows up in hybrid infrastructure with a
    traditional networking footprint.

**32. How is Multicast used in DevOps?**

??? success "Reveal answer"
    Multicast efficiently delivers the same data to multiple receivers simultaneously without duplicating traffic for each
    one, which is useful in environments like Kubernetes clusters where certain real-time state updates need to reach
    many nodes at once.

**33. whatis the purpose of #!/bin/bash?**

??? success "Reveal answer"
    Known as the Shebang. It tells Linux which interpreter should execute the script.
    eee
    #! /bin/bash
    @ Without it, the script may run with a different, unintended

**34. whatare Exit Codes?**

??? success "Reveal answer"
    Exit codes indicate whether a command succeeded.
    QO Success
    +0 Error
    CHECK THE LAST EXIT CODE
    »_ echo $?
    @ Production Frequently Asked
    a e e o e
    lato 2? Why is

**35. What does 2>&1 mean in shell?**

??? success "Reveal answer"
    Redirects stderr (file descriptor 2) to wherever stdout (file descriptor 1) is currently pointing. Used 
    to capture both stdout and stderr together.

## Real interview prompts

Additional questions reported from real DevOps / SRE interviews. Company names are omitted — practise these out loud without notes.

- if you were required to run pre-task checks, main tasks and post-task validation for patch automation, how would you structure your RedHat Automation & Virtulization scripts?
- How to schedule pipeline, lets say i have validated the pipeline with some update and i want to schedule it to stage/main branch, how to do? (This also someone explain)?
- Do you use pipeline for three different env or one for all? Explain how?write a groovy script using any ci cd took for build, test and deploy stages?
- What is runs-on in a pipeline? Which type of runners are you using in your organization, and do you know how to configure self-hosted runners?
- Do you have experience with AWS DevOps services like CodeDeploy, CodeBuild, and CodePipeline? How would you set up a pipeline using them?
- [ ] What is a recent challenge you faced while implementing a DevOps practice or pipeline in your team or organization?
- Can you share an experience where your automation strategy failed or caused problems? What was your corrective action?,?
- What is the command or pipeline syntax used to refer the variable output of the previous stage in the current stage?
- Can you tell me the difference between single ampersand (&) and double ampersand (&&) in shell scripting?
- Write a script that renames all .txt files in a directory by appending the current date to the filename?
- Write a script to monitor a directory and automatically copy any new files to a remote server using SCP?
- Have you used any artifact repositories like Nexus or Artifactory, and where do you store dependencies?
- [ ] What is your approach to integrating automated testing in pipelines to ensure high code quality?
- Write a shell script that takes an integer N as input and prints numbers in a triangular pattern?
- Write a shell script that checks if a service is running, restarts it if not, and logs the event?
- You have a multi-cloud environment. How do you manage pipelines for all those cloud environments?
- How you will build single or minimal reusuable pipeline templates for 50 different applications?
- If the pipeline fails due to existing resources, how do you handle RIP (Remove, Import, Plan)?
- Write a shell script to find and delete all files in a directory that are older than 30 days?
- Which version of SonarQube have you used — Community, Developer, Enterprise, or SonarCloud?

## Related

- Course: [Shell](../shell/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
