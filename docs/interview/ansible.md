---
title: "Ansible Interview Preparation"
description: "40 curated Ansible interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: ansible
tags:
  - interview
  - ansible
comments: false
---

{% raw %}
# Ansible Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is the workflow of Chef?**

??? success "Reveal answer"
    Connect chef workstation, chef server and chef node with each other. Create cookbook in chef
    workstation and write code in recipe w.r.t. the infrastructure to be created. Upload the entire cookbook
    to chef server and attach the cookbook's recipe to nodes run-list. Chef-client (automated) runs
    frequently towards chef server for new code, gets the code and applies it to the chef node —
    converting code into infrastructure. If no changes are there, chef-client won't take any action
    (Idempotency).

**2. What is the Attributes concept in Chef?**

??? success "Reveal answer"
    Sometimes we need host-specific details of each server (like IP Address, Hostname, etc.) for
    configuration files. This information varies from system to system. These host-specific details
    mentioned in configuration files are called 'Attributes'. Chef-client gathers these Attributes from the
    Ohai store and puts them in configuration files, using variables instead of hard coding.

**3. What is include_recipe in Chef?**

??? success "Reveal answer"
    By default, we can call one recipe at a time in one cookbook. To call multiple recipes from the same
    cookbook, we use include_recipe. We take the default recipe and mention all recipes to be called in
    order. When the default recipe is called, it automatically calls all other recipes inside it. Note: we can
    call recipes from the same cookbook only, not from different cookbooks.

**4. What is Ohai and how does it work?**

??? success "Reveal answer"
    Ohai is called a 'System Discovery Tool'. It stores system information and captures each and every
    minute detail of the system, updating it when new changes occur. Whenever chef-client converts code
    into infrastructure, the Ohai store is immediately updated. Before chef-client runs, it verifies in the
    Ohai store to know the current state of the server and acts accordingly.

**5. What is Dry run in playbook?**

??? success "Reveal answer"
    Dry run is used to test a playbook before executing it on nodes. Dry run doesn't actually execute the
    playbook, but shows output as if it were executed. By seeing the output, we can verify whether the
    playbook is written properly. It checks whether the playbook is formatted correctly and tests how it will
    behave without running the actual tasks.

**6. What is an Ansible Role, and how do you create it?**

??? success "Reveal answer"
    Start with a precise definition in the context of Ansible, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**7. what are the ansible modules you have used?**

??? success "Reveal answer"
    Start with a precise definition in the context of Ansible, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**8. What is the difference between import and include in Ansible?**

??? success "Reveal answer"
    Start with a precise definition in the context of Ansible, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**9. What is your hands-on experience with Ansible? Explain a real project where you used it?**

??? success "Reveal answer"
    Start with a precise definition in the context of Ansible, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**10. What is Task section in Ansible playbook?**

??? success "Reveal answer"
    This is the second most important section in playbook after the target section. In this section, we
    mention the list of all modules. We can mention any number of modules in one playbook. If there is
    only one task, we can use an arbitrary command with one module. For more than one module, we use
    the full playbook.

**11. What is Target section in Ansible playbook?**

??? success "Reveal answer"
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    In this section, we mention the group name which contains either IP addresses or Hostnames of
    nodes. When we execute the playbook, code is pushed to all nodes in the group mentioned in the
    Target section. We use the 'all' keyword to refer to all groups.

**12. What is Ansible Tower / AWX?**

??? success "Reveal answer"
    A web-based UI, REST API, and task engine for Ansible. Provides role-based access, job 
    scheduling, credential management, and real-time output. AWX is the open-source upstream of 
    Red Hat Ansible Tower.

**13. What is the register directive in Ansible?**

??? success "Reveal answer"
    Captures the output of a task into a variable for use in subsequent tasks. 
    - command: cat /etc/app/version 
     register: app_version 
    - debug: msg="Running version {{ app_version.stdout }}"

**14. What is the uri module in Ansible?**

??? success "Reveal answer"
    Makes HTTP requests from managed hosts. Used for health checks, API calls, webhook triggers. 
    - uri: 
     url: http://localhost:8080/health 
     status_code: 200 
     retries: 5 
     delay: 10

**15. What is a dynamic inventory in Ansible?**

??? success "Reveal answer"
    An inventory script or plugin that queries external sources (AWS, GCP, Azure, Terraform state) to 
    build the host list dynamically. AWS EC2 plugin: amazon.aws.aws_ec2.

## Scenarios and troubleshooting

**16. Write an Ansible playbook for a production-grade web server setup.**

??? success "Reveal answer"
    # playbook-webserver.yml
    - name: Configure Production Web Server
    hosts: web_servers
    become: true # Run tasks as sudo
    gather_facts: true # Collect system facts first
    vars:
    app_name: my-api
    app_user: appuser
    app_dir: /opt/{{ app_name }}
    nginx_config_dir: /etc/nginx/conf.d
    node_version: "18"
    pre_tasks:
    - name: Update apt cache
    apt:
    update_cache: yes
    cache_valid_time: 3600 # Only update if cache is older than 1 hour
    - name: Ensure required packages are installed
    apt:
    name:
    
    - git
    - curl
    - unzip
    - python3-pip
    - ufw
    state: present
    tasks:
    # ---- User Setup ----
    - name: Create application user
    user:
    name: "{{ app_user }}"
    system: true
    shell: /bin/false
    home: "{{ app_dir }}"
    create_home: true
    # ---- Node.js Installation ----
    - name: Add NodeSource apt repository
    shell: |
    curl -fsSL https://deb.nodesource.com/setup_{{ node_version }}.x |
    bash -
    args:
    creates: /etc/apt/sources.list.d/nodesource.list # Don't run if
    already exists
    - name: Install Node.js
    apt:
    name: nodejs
    state: present
    # ---- Application Deployment ----
    - name: Clone application repository
    git:
    repo:…

**17. Write a playbook to deploy an Nginx server and ensure the service is started and enabled on boot. How would you manage secrets in Ansible?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Ansible components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**18. What is max_fail_percentage in Ansible?**

??? success "Reveal answer"
    Sets the maximum percentage of failed hosts before aborting the entire play. Useful for rolling 
    deployments — stop if too many hosts fail.

## Practice questions

**19. How do you use Ansible Vault to manage secrets, and how does it integrate with a CI/CD pipeline?**

??? success "Reveal answer"
    Ansible Vault encrypts sensitive data (passwords, API keys, certificates) using AES256 encryption, 
    allowing you to safely commit encrypted secrets to version control. 
    # Create an encrypted variables file 
    ansible-vault create group_vars/production/vault.yml 
    # Opens editor — type your secrets: 
    # vault_db_password: "super-secret-db-password" 
    # vault_api_key: "sk-prod-abc123xyz" 
    # vault_ssl_certificate: | 
    # -----BEGIN CERTIFICATE----- 
    # ... 
    # Encrypt an existing file 
    
     
    ansible-vault encrypt group_vars/production/vars.yml 
    # View encrypted file (prompts for password) 
    ansible-vault view group_vars/production/vault.yml 
    # Edit encrypted file 
    ansible-vault edit group_vars/production/vault.yml 
    # Re-key (change the vault password) 
    ansible-vault rekey group_vars/production/vault.yml 
    # Encrypt a single string (useful for embedding in non-encrypted files) 
    ansible-vault encrypt_string 'super-secret-password' --name 'db_password' 
    # Output: 
    # db_password: !vault | 
    # $ANSIBLE_VAULT;1.1;AES256 
    # 38623665353561343... 
    CI/CD integration — storing vault password…

**20. What challenges have you faced with configuration management tools?**

??? success "Reveal answer"
    Complexity managing large-scale infrastructure and dependencies as playbooks or recipes grow, consistency across
    different environments with varying OS versions or package dependencies, scalability as infrastructure grows or
    changes, securely handling sensitive credentials within the tool, and integrating with existing systems already in the
    organization's ecosystem. Addressing these comes down to modular design, thorough testing, and careful planning
    rather than any single fix.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    5
    CLOUD COMPUTING: AWS

**21. What do you mean by Roles in Ansible?**

??? success "Reveal answer"
    Adding more and more functionality to playbooks makes them difficult to maintain in a single file. To
    address this, we organise playbooks into a directory structure called 'roles'. We create a separate file
    for each section and mention only the names of those sections in the main playbook. When the main
    playbook is called, it calls all section files in the specified order, keeping the main playbook small and
    manageable.

**22. How does Chef-client run automatically?**

??? success "Reveal answer"
    By default, chef-client runs manually. We use 'cron tool' (the default Linux scheduling tool) to
    automate it. In the crontab file, we give the chef-client command and set the timing as per
    requirement. Then chef-client runs automatically at frequent intervals. This is a one-time effort done
    during bootstrap.
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers

**23. if you have custom plugins that multiple roles depends on, how do you manage them in the context of Ansible Roles Management?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Ansible components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**24. How do you write an Ansible playbook, and what client requirements do you consider?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Ansible components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**25. If you have two different VMs,, how will you modify your playbook for diff requirement?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Ansible components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**26. In ansible if you need to execute something as root user how do you that?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Ansible components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**27. Where do we use conditionals in Playbooks?**

??? success "Reveal answer"
    Sometimes, nodes could be a mixture of different Linux OS flavors. Linux commands vary in different
    operating systems. We can't execute a common set of commands on all machines, nor separate
    commands on each node individually. Conditionals allow commands to be executed based on a
    certain condition we specify.

**28. What do you mean by Ad-Hoc commands in Ansible?**

??? success "Reveal answer"
    These are simple one-liner Linux commands used to meet temporary requirements without saving for
    later. We don't use Ansible modules here, so Idempotency will not work with Ad-Hoc commands. We
    use these for temporary purposes without playbooks, when no suitable YAML module is available.

**29. Why are we using loops concept in Ansible?**

??? success "Reveal answer"
    Sometimes we need to deal with multiple tasks — installing multiple packages, creating many users,
    creating many groups, etc. Mentioning a module for every task is complex. To address this, we use
    the loops concept in combination with variables.

**30. write a playbook to install apache in VM?**

??? success "Reveal answer"
    Outline the solution first, then give a minimal correct example (commands or config sketch).
    
    Call out the production hardening you would add next (pin versions, least privilege, secrets, health checks) and how you would validate the result.

**31. What does idempotent mean in Ansible?**

??? success "Reveal answer"
    Answer directly for Ansible: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**32. How does Ansible work?**

??? success "Reveal answer"
    Answer directly for Ansible: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**33. Describe the structure and advantage of using an Ansible role to manage a three-tier web application. what do you mean by three-tier web application?**

??? success "Reveal answer"
    Answer directly for Ansible: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**34. how to run anisble playbook and diff options?**

??? success "Reveal answer"
    Answer directly for Ansible: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**35. Why is PUT request called idempotency in nature. If I made another entry and name is same but location is differnet then what will db store.,?**

??? success "Reveal answer"
    Answer directly for Ansible: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**36. Ansible playbook times out on one host out of twenty. What do you check?**

??? success "Reveal answer"
    Answer directly for Ansible: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**37. How can you install a patch through ansible in more than 20 servers?**

??? success "Reveal answer"
    Answer directly for Ansible: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**38. Write a sample playbook by mentioning variables instead of hard coding?**

??? success "Reveal answer"
    --- # My First YAML playbook
    - hosts: demo
    user: ansible
    become: yes
    connection: ssh
    vars:
    pkgname: httpd
    tasks:
    - name: Install HTTPD server on centos 7
    action: yum name='{{pkgname}}' state=installed
    CI/CD & Jenkins

**39. How to deploy a web server using Chef?**

??? success "Reveal answer"
    package 'httpd' do
    action :install
    end
     
    file '/var/www/html/index.html' do
    content 'Hello Dear Students!!'
    action :create
    end
     
    service 'httpd' do
    action [ :enable, :start ]
    end

**40. Write a sample playbook to install any package?**

??? success "Reveal answer"
    --- # My First YAML playbook
    - hosts: demo
    user: ansible
    become: yes
    connection: ssh
    tasks:
    - name: Install HTTPD on centos 7
    action: yum name=httpd state=installed

## Related

- Course: [Ansible](../ansible/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
