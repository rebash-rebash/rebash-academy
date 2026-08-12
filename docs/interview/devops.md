---
title: "DevOps Fundamentals Interview Preparation"
description: "65 curated DevOps Fundamentals interview prompts — model answers plus real interview questions collected across companies (deduplicated by topic)."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. Can you explain the differences between Agile and DevOps?**

??? success "Reveal answer"
    Agile is focused on the development process itself -- breaking work into sprints and delivering working software
    iteratively, with feedback coming mainly from stakeholders after each sprint. DevOps extends that same iterative
    philosophy across the entire lifecycle, including deployment and operations, requiring collaboration between dev,
    ops, and QA, and leaning heavily on automation for build, test, and deployment rather than the more manual testing
    Agile alone implies. DevOps also closes the feedback loop continuously from production itself -- performance
    monitoring, real user behaviour -- not just from a sprint review.
    KEY POINTS TO MENTION
    • Agile: iterative development, sprint-based, stakeholder feedback
    • DevOps: full lifecycle, dev+ops+QA collaboration, heavy automation, continuous production feedback

**2. The server is extremely slow. How do you identify if the issue is CPU related and what is causing i?**

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

**3. What is the DevOps lifecycle ?**

??? success "Reveal answer"
    ! > Plan, code, build, test, release, deploy, operate, monitor, Sareea !
    P and improve. P4 [ Pepey ) Operate) Moritr) Improve» :
    4 (4) What is Continuous Integration ? , tthe ;
    =O Se Commi Build & Test
    ° > Continuous Integration automatically builds and tests code (SS by
    4 whenever developers commit changes aN ated Y °
    : (6) What is Continuous Delivery ? i
    ; SEE Ye AVON UUOUS, LEUIY 9
    : > Continuous Delivery keeps software ready for production (Ee :
    ° deployment through automated build, test, and release processes. £0} e
    What is Continuous Deployment ? <
    > Continuous Deployment automatically releases every re
    validated change to production. ‘2 Wyn,

**4. What are the key principles of DevOps?**

??? success "Reveal answer"
    Automation of testing, integration, and deployment to speed delivery and cut errors; close collaboration between
    development, QA, and operations; CI/CD so every change is automatically tested and deployed; continuous
    monitoring and feedback so issues surface early; infrastructure as code for consistent, versioned environments; and
    a culture of continuous improvement built on retrospectives and experimentation.
    KEY POINTS TO MENTION
    • Automation
    • Collaboration
    • CI/CD
    • Monitoring & Feedback
    • Infrastructure as Code
    • Culture of improvement
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**5. What is virtualization?**

??? success "Reveal answer"
    Logically dividing a big machine into multiple virtual machines so that each virtual machine acts as a
    new server and we can deploy any kind of applications in it. For this, we install virtualization software
    on top of base OS. This software divides base machine resources into logical components. In simple
    terms, logically dividing one machine into multiple machines is called virtualization.
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers

**6. What is DevOps, and why is it important?**

??? success "Reveal answer"
    DevOps is a set of practices that bridges development and operations by automating and integrating the processes
    between them, so collaboration improves and software ships faster without sacrificing reliability. It matters because it
    shortens development cycles, improves release efficiency through CI/CD and monitoring, and builds a culture where
    teams own quality end to end instead of throwing code over a wall.

**7. What is Handler section?**

??? success "Reveal answer"
    Some tasks with dependencies should not be mentioned in the tasks section — they go in the handler
    section. For example, installing a package is one task and starting the service is another, but starting
    the service depends on the package being installed first. The package task goes in the task section;
    the service task goes in the handler section so it runs only after the package is installed.

**8. What is a Packet Sniffer and its role in DevOps?**

??? success "Reveal answer"
    A packet sniffer like Wireshark or tcpdump captures and inspects raw network traffic, which I've used to troubleshoot
    connectivity issues, debug microservice communication, or figure out exactly where a pipeline-related network call is
    failing when higher-level logs aren't giving enough detail.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**9. What is Packet Filtering in DevOps?**

??? success "Reveal answer"
    Packet filtering inspects individual packets against a rule set and allows or blocks them accordingly -- it's the
    fundamental mechanism behind both traditional firewalls and cloud security groups, enforcing which traffic is allowed
    to reach an application.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**10. What is the role of a Hub in DevOps?**

??? success "Reveal answer"
    A hub is a basic networking device that broadcasts everything it receives to all connected ports -- I've only really
    seen these in small test environments or legacy office networks, since switches are strictly better for anything beyond
    the simplest setup.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**11. What is the role of the Controller Manager?**

??? success "Reveal answer"
    The Controller Manager runs a set of controllers that continuously monitor cluster state and reconcile it toward the
    desired state -- the Node Controller watches node health, the Replication Controller ensures the right number of Pod
    replicas are running, the Job Controller manages job completion, and so on.

**12. What is the systemctl command, and why is it important for a DevOps engineer?**

??? success "Reveal answer"
    systemctl controls systemd, the service manager on modern Linux distributions -- starting, stopping, restarting
    services, checking status, and managing boot targets. It's essential for managing critical infrastructure components
    like web servers and databases running as systemd services.

**13. What is an Access Control List (ACL) in DevOps?**

??? success "Reveal answer"
    An ACL restricts access to specific resources based on rules, and I commonly define these as part of
    infrastructure-as-code configurations -- like a Network ACL in a VPC -- to enforce secure access at the subnet level
    as code rather than a manually managed console setting.

**14. What is a Service Level Agreement (SLA) in DevOps?**

??? success "Reveal answer"
    An SLA defines the uptime and performance commitments made to customers, often with contractual consequences
    if breached. As a DevOps engineer I monitor the underlying metrics closely enough to know before the SLA is at risk,
    not just after it's already been breached.

**15. What is a database migration rollback strategy?**

??? success "Reveal answer"
    Write backward-compatible migrations so both old and new code versions can run against the 
    same schema simultaneously. Use feature flags to control which code path runs. Never drop 
    columns in the same release that removes the code using them.

**16. What is a Point-to-Point Connection in DevOps?**

??? success "Reveal answer"
    A point-to-point connection is a direct link between two networks, commonly used in hybrid environments to securely
    connect on-prem infrastructure to a cloud VPC -- AWS Direct Connect is a real example of exactly this kind of
    dedicated link.

**17. What is a DHCP Scope and how does it help DevOps?**

??? success "Reveal answer"
    A DHCP scope is the range of IP addresses a DHCP server can automatically assign, which simplifies IP
    management in on-prem or private cloud environments by automating address allocation instead of manually
    tracking which IPs are in use.

**18. What is dorny/paths-filter action?**

??? success "Reveal answer"
    A popular community action that detects which paths changed, enabling conditional job 
    execution in monorepos. 
    - uses: dorny/paths-filter@v3 
     id: changes 
     with: 
     filters: | 
     api: 
     - 'services/api/**' 
     web: 
     - 'services/web/**'

**19. What are the key DevOps tools?**

??? success "Reveal answer"
    o CI/CD: Jenkins, GitLab CI, GitHub Actions 
    o Containerization: Docker, Podman 
    o Orchestration: Kubernetes, OpenShift 
    o Monitoring: Prometheus, Grafana 
    o Configuration Management: Ansible, Puppet, Chef 
    o Version Control: Git

**20. What is include_tasks vs import_tasks?**

??? success "Reveal answer"
    import_tasks: static inclusion — tasks are loaded at parse time. Tags and conditions apply to 
    individual tasks. include_tasks: dynamic inclusion — evaluated at runtime. Allows conditionally 
    including different task files.

**21. What is an error budget?**

??? success "Reveal answer"
    The allowed amount of unreliability in a service. Error Budget = 1 - SLO. If SLO = 99.9%, error 
    budget = 0.1% = 43.8 minutes/month of allowed downtime. When the error budget is exhausted, 
    new feature deployments pause.

**22. What is database sharding?**

??? success "Reveal answer"
    Horizontally partitioning data across multiple database instances. Each shard contains a subset of 
    data (e.g., users 1-1M on shard 1, 1M-2M on shard 2). Enables horizontal scaling beyond single-
    node limits.

## Scenarios and troubleshooting

**23. High latenc google.com) from ii D «a Gateway knowledge = ih lta otaen seta the : Cn OS was 3 ae ae troubleshoot?**

??? success "Reveal answer"
    bacnante its ot A Ree et snes) * havi ie ree tools
    =) + Hlantfy the APE & sevice hitting the APL. igation shills
    —@ Toplerert ex ee series Quotas ee 
    3 Seles a ap alc ace « Keededge of AS ti :
    {.. wey _Use caching / batchi if needed. * Best practi we penis
    = Q le TAKEAWAY: batching to reduce API calls. PL a for handling limits
    pre: Peameection We nave aes ae “Cc tion & resilience mi
    3 VES ees ae eo
    : Loe Proaeti a
    Ohne Tate Fie right order, and right mindset | | = ae ae a
    eis eevee dy mer ever | | Gal Q 5 a % (REMEMBER);
    - ——— ) { Monitor G : a
    sate a ee
    a ee @ | VERIQTA,
    2 Verify |
    Prevent G3] @verigta_
    
    oy VERIQTA Z ;
    | 5 | NcrepennG TS) oem TOPICS COVERED:
    | bs INFRASTRUCTU ¥ v Terraform failures
    ee RE AS CODE = |vmrm=
    : < Dri i
    9 Real interview questions. Real production scenarios : ine
    : | % tion changes
    3 @

**24. What steps do you take after the incident is resolved?**

??? success "Reveal answer"
    * Conduct a postmortem / root cause analysis. * Continuous improvement
    | + Identify what went wrong and why. * Ownership & accountability
    | + Document lessons learned. + Preventive thinking
    + Implement preventive actions to avoid recurrence. * Good documentation habits
    + Share postmortem with the team and stakeholders. * Team learning mindsst
    | @

**25. What is the strategy.fail-fast option?**

??? success "Reveal answer"
    When true (default), cancels all in-progress matrix jobs if any job fails. Set to false to let all 
    matrix jobs complete regardless.

**26. How would you find all files modified in the last 7 days in a directory?**

??? success "Reveal answer"
    find /path/to/directory -mtime -7 uses the -mtime option to filter by modification time within the last 7 days.

## Practice questions

**27. How e rs ~-cpus s / a er exec a — : aE?**

??? success "Reveal answer"
    do » quer or ~~ | jesiei it <id mg 2 : ;
    : = : : > top. f « C li ene:
    ° ‘ en ren period/ s / bad | 5 : 3 :
    | ; Z : = a --cpu- querie: IN efficiency layers
    Minimi -root vale: r se ing: quota: ‘i = :
    - . ad-onl image ae x = ae : 4
    + K iy files (USE! es :
    | = ie i = rype) Resour: ess shooting
    tos w Ait He (Dock possible. — 5 * poe
    2 ANS: ers rs can and pee gaat Ait = :
    | : : : a rola Vault, Al : INTER’ & ale zo,
    : ferif twork bleshoot? ¢ on ly. — | 2 :
    ah sah ewes ta thie 2 : : |
    B 3 es . ps a host bu ). av ty best pr FOR:
    ; 3 ees Hi hind macvian, Eibcaen ie fe, ae ility actices
    —. ss tivit - . : tainers. 7 |
    ke TA ‘y ee Benes / ean — oe 3 :
    rs ; curl, pi mn ees Mle :
    oo ways are light ping, ne a =
    —_ Autor bserv. tweig! ie ; - 7 oo
    B sainunis e, isolat i fs)
    mists: Mon te, claws a ,
    onitor, secure : :
    shihbdiss axa ati be ant : = i 3
    ure, and keep i RikiGn = jC as ints =
    ~<e ; : | = * venga
    : ‘3 Dock
    | | ab aes a ‘
    ; ; nd 6 abi “
    & Moni small. Ri mune: | }
    = Aut tor aise ~~ | : : :
    __ Automate “ ;
    A VE
    ; RIQ
    2 TA
    @verigta.
    
    ~~ hae VERIQTA, en nag
    Instagram:…

**28. What challenges have you faced implementing DevOps in previous projects?**

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

**29. How does Zero Trust Architecture relate to DevOps?**

??? success "Reveal answer"
    Zero Trust assumes nobody, inside or outside the network, is trusted by default -- every request has to prove its
    identity and authorization on its own merits. I implement this in DevOps through things like mutual TLS between
    services and scoped IAM roles per workload, rather than relying on network location as an implicit trust boundary.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    3
    SUBNET-RELATED QUESTIONS

**30. How does ARP Poisoning affect DevOps?**

??? success "Reveal answer"
    ARP poisoning is an attack where a malicious actor sends forged ARP messages to associate their MAC address
    with another device's IP, letting them intercept traffic. It's a network security risk that DevOps teams need to defend
    against with proper network segmentation and monitoring, particularly in shared or less-trusted network segments.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**31. What do you mean by Upstream and Downstream projects?**

??? success "Reveal answer"
    These are linked projects — ways to connect jobs with each other.
    Upstream jobs: First job triggers the second job after its build is over. First job is active.
    Downstream jobs: Second job waits till the first job finishes its build. As and when the first job finishes,
    the second job is triggered automatically. Second job is active.
    We can use either type to link multiple jobs.

**32. How does a DMZ (Demilitarized Zone) apply in DevOps?**

??? success "Reveal answer"
    A DMZ isolates public-facing services in their own network segment, acting as a buffer between the internet and
    internal, more sensitive networks. I've used this pattern for production environments where the public-facing load
    balancer or API gateway sits in the DMZ while backend services stay fully isolated from direct internet exposure.

**33. What role do Network Switches play in DevOps?**

??? success "Reveal answer"
    Switches manage local traffic within a private network or data centre, forwarding frames based on MAC address --
    essential for efficient on-premise service communication in hybrid DevOps environments where not everything has
    moved to the cloud.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**34. How does Mesh Topology benefit DevOps?**

??? success "Reveal answer"
    A mesh topology, where nodes connect to multiple other nodes rather than a single central point, gives redundancy
    and failover -- which is exactly the resilience model behind Kubernetes cluster networking and service mesh
    architectures like Istio, where losing one path doesn't isolate a service.

**35. How does Split-Horizon work in DevOps?**

??? success "Reveal answer"
    Split-horizon DNS resolves the same domain name differently depending on whether the query comes from inside or
    outside the network, which I've used to let internal services reach each other via internal IPs while external users are
    routed through a public-facing endpoint for the same hostname.

**36. How does Open Shortest Path First (OSPF) contribute to DevOps?**

??? success "Reveal answer"
    OSPF is a dynamic routing protocol that lets routers automatically adjust routing tables in response to network
    changes, giving fault tolerance and efficient path selection -- important for DevOps teams managing resilient internal
    network routing in hybrid or on-prem-heavy environments.

**37. How are Broadcast Domains relevant to DevOps?**

??? success "Reveal answer"
    A broadcast domain is the set of devices that receive broadcast traffic from each other, and keeping these
    appropriately scoped in network design minimizes unnecessary traffic and avoids performance issues that come
    from an overly large flat network.

**38. How is Quality of Service (QoS) utilized in DevOps?**

??? success "Reveal answer"
    QoS prioritizes certain types of network traffic over others, which matters when I need to make sure a
    latency-sensitive or resource-intensive service gets sufficient bandwidth even when the network is under contention
    from less critical traffic.

**39. Benefits of CI?**

??? success "Reveal answer"
    • Detects bugs as soon as possible so that bugs can be rectified fast
    • Complete automation — no need for manual intervention
    • Can intervene manually whenever needed — better control
    • Can establish a complete and continuous work flow

**40. How to write ruby code to create file, directory?**

??? success "Reveal answer"
    file '/myfile' do
    content 'This is my second file'
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    action :create
    owner 'root'
    group 'root'
    end
     
    directory '/mydir' do
    action :create
    owner 'root'
    group 'root'
    end

## Real interview prompts

Additional questions reported from real DevOps / SRE interviews. Company names are omitted — practise these out loud without notes.

- When you deploy from CI, you build a package and then need a platform to deploy the application. How do you build that platform, and if it requires human intervention, how do you eliminate that dependency?
- How and from where to clone repo, is there any local repo you are using and then transferring from local to remote or how? (Honestly I didn’t get this Q, if anyone has real time exposure pls explain)?
- In a multi-account environment, if the resources are residing in one account and the users are in different accounts, how will you configure so that the user can access the resources?
- If you have a monolith application and need to convert it to microservices, what prerequisites would you ask from the development and tech teams before starting the work?
- If your lead or team member is not technically strong or doesn’t behave well, how do you handle the situation and continue working as a team member?
- You are onboarding a new customer with 5 million+ users. How would you design the complete application architecture as a Solution Architect?
- Failover happend in DB, so connection is switched from A to B, during this time interval, if user is writing some data, how to manage that ?
- How the auto scaling works, how things work in the back-end, from worker nodes to master nodes. Communication track behind that?
- Tell me about a successful DevOps transformation project you were part of. What was your role, and how did you drive change?
- How would the service account know which role to assume. What all things you would need to configure in the service account?
- How do you mitigate the risk of misscommunication when there are multi-lingual stakeholders involved in email threads?
- Design an architecture for the scenario: if I type www.application.com it should get resolved to the backend service?
- 10 developers are checking in code in GIT, I want to remove the code checkin done by developer 10, how to do that ?
- I have 3 nodes (small, medium, and large), and I want only data load to go to the large node. How can I do that?
- In your project, what was your domain name? How are you establishing connection between domain name and service?
- You also mentioned about basically to reduce the MTTR so can you explain me what automation that you have done?
- Describe how you handled a rollback situation during a major release. What went wrong, and what did you learn?,?
- Describe a time when you had to work under tight deadlines. How did you manage team workload and expectations?,?
- How do you ensure smooth collaboration between development and operations teams in a high-pressure situation?,?
- Question : What is your knowledge of production system sizing, provisioning, setup, maintenance, and closure?
- Describe a scenario where you had to introduce a new DevOps tool or practice. How did you get team buy-in?,?
- Have you deployed both applications and infrastructure? What kind of tech stack have you mainly worked on?
- Q1. Explain the infrastructure and application setup of your last project. How is the application hosted?
- Tell me about a conflict you faced within your DevOps or cross-functional team. How did you resolve it?,?
- If you have an on-prem application, how would you migrate and deploy it in a cloud-native environment?

## Related

- Hub: [Interview Preparation](index.md)
{% endraw %}
