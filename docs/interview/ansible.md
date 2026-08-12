---
title: "Ansible Interview Preparation"
description: "40 curated interview questions and model answers for Ansible — concepts, scenarios, troubleshooting, and production trade-offs."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

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

**2. What is Idempotency?**

??? success "Reveal answer"
    Idempotency is a unique feature in all configuration management tools. It ensures that changes
    should not re-apply repeatedly. Once chef-client converts code into Infrastructure, even if chef-client
    runs again, it will not take any action. Only if new changes are there in the code will chef-client take
    action. So running chef-client any number of times makes no difference if there are no changes.

**3. What is the Attributes concept in Chef?**

??? success "Reveal answer"
    Sometimes we need host-specific details of each server (like IP Address, Hostname, etc.) for
    configuration files. This information varies from system to system. These host-specific details
    mentioned in configuration files are called 'Attributes'. Chef-client gathers these Attributes from the
    Ohai store and puts them in configuration files, using variables instead of hard coding.

**4. What is include_recipe in Chef?**

??? success "Reveal answer"
    By default, we can call one recipe at a time in one cookbook. To call multiple recipes from the same
    cookbook, we use include_recipe. We take the default recipe and mention all recipes to be called in
    order. When the default recipe is called, it automatically calls all other recipes inside it. Note: we can
    call recipes from the same cookbook only, not from different cookbooks.

**5. What is Ohai and how does it work?**

??? success "Reveal answer"
    Ohai is called a 'System Discovery Tool'. It stores system information and captures each and every
    minute detail of the system, updating it when new changes occur. Whenever chef-client converts code
    into infrastructure, the Ohai store is immediately updated. Before chef-client runs, it verifies in the
    Ohai store to know the current state of the server and acts accordingly.

**6. What is Ansible vault?**

??? success "Reveal answer"
    Sometimes, we use sensitive information in playbooks like passwords and keys. Anyone can open
    these playbooks and read this sensitive information. By using Ansible vault, we encrypt playbooks so
    that only those who have the password can read the information. It is the way of protecting playbooks
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    by encrypting them.

**7. What is Dry run in playbook?**

??? success "Reveal answer"
    Dry run is used to test a playbook before executing it on nodes. Dry run doesn't actually execute the
    playbook, but shows output as if it were executed. By seeing the output, we can verify whether the
    playbook is written properly. It checks whether the playbook is formatted correctly and tests how it will
    behave without running the actual tasks.

**8. What is Playbook in Ansible?**

??? success "Reveal answer"
    A Playbook is a file where we write YAML script to create infrastructure in nodes. We use modules to
    create infrastructure. We create many sections in playbook and mention all modules in the task
    section. We can create any number of playbooks. Each playbook defines one scenario. All sections
    begin with '-' and attributes beneath it.

**9. What is wrapper cookbook?**

??? success "Reveal answer"
    Without downloading, we can call supermarket cookbooks during run time so we always get the latest
    updates automatically. We use our own cookbook to call the chef supermarket cookbook. This
    process of calling one cookbook by using another cookbook is called a wrapper cookbook. We
    especially use this concept to automate chef-client.

**10. What is Run-list in Chef?**

??? success "Reveal answer"
    Run-list is an ordered list of recipes that we are going to apply to nodes. We mention all recipes in the
    cookbook, upload to chef server, and attach recipes to the node's run-list in sequence order.
    Chef-client applies all recipes to nodes in the same order because sometimes order is important
    (especially for dependent recipes).

**11. What is Ansible?**

??? success "Reveal answer"
    Ansible is one of the Configuration Management Tools. It is a method through which we automate
    system admin tasks. Configuration refers to each and every minute detail of a system. All DevOps
    engineers manage this configuration automatically using tools like Ansible — that's why we call
    Ansible a configuration management tool.

**12. What is 'roles' in Chef?**

??? success "Reveal answer"
    Roles are custom run-lists. We create a role, upload it to chef server and assign it to nodes. If we have
    many nodes and need to add a cookbook to all their run-lists, we create a role and attach it to all
    nodes once. Next time, we just add the cookbook to the role — it automatically applies to all nodes
    assigned that role.

**13. What is Task section in Ansible playbook?**

??? success "Reveal answer"
    This is the second most important section in playbook after the target section. In this section, we
    mention the list of all modules. We can mention any number of modules in one playbook. If there is
    only one task, we can use an arbitrary command with one module. For more than one module, we use
    the full playbook.

**14. What is Target section in Ansible playbook?**

??? success "Reveal answer"
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    In this section, we mention the group name which contains either IP addresses or Hostnames of
    nodes. When we execute the playbook, code is pushed to all nodes in the group mentioned in the
    Target section. We use the 'all' keyword to refer to all groups.

**15. What is bootstrap?**

??? success "Reveal answer"
    Bootstrap is the process of adding a chef node to the chef server (bringing any machine into the chef
    environment). Three actions are performed automatically:
    • Node gets connected to chef server
    • Chef server installs chef package in the chef node
    • Cookbooks are applied to the chef node

**16. What is Ansible block?**

??? success "Reveal answer"
    Groups related tasks for error handling. Supports rescue (run on block failure) 
    and always (always run). 
    block: 
     - name: Deploy application 
     command: ./deploy.sh 
    rescue: 
     - name: Rollback 
     command: ./rollback.sh 
    always: 
     - name: Send notification 
     slack: msg="Deploy completed"

**17. What is there inside a cookbook?**

??? success "Reveal answer"
    • Chefignore: like .gitignore (to ignore files and folders)
    • Kitchen.yml: for testing of cookbook
    • Metadata.rb: name, author, version of cookbook
    • Readme.md: information about usage of cookbook
    • Recipe: file where you write code
    • Spec: for unit test
    • Test: for integration test

**18. What is Chef supermarket?**

??? success "Reveal answer"
    Chef supermarket is the place where we get custom cookbooks. We don't need to create cookbooks
    and write code from scratch every time. We can download custom cookbooks provided by the chef
    organization and community, and modify them as per our needs.

**19. What is serial in Ansible?**

??? success "Reveal answer"
    Controls how many hosts are processed at once in a play. serial: 1 processes hosts one at a 
    time — useful for rolling deployments with zero downtime. 
    - hosts: web_servers 
    
     
     serial: 25% # Update 25% of servers at a time

**20. What is Ansible facts?**

??? success "Reveal answer"
    System information automatically collected at playbook start: OS type, IP addresses, CPU count, 
    memory, disk partitions. Available as ansible_* variables. Disable with gather_facts: false for 
    faster runs.

**21. What is Ansible Tower / AWX?**

??? success "Reveal answer"
    A web-based UI, REST API, and task engine for Ansible. Provides role-based access, job 
    scheduling, credential management, and real-time output. AWX is the open-source upstream of 
    Red Hat Ansible Tower.

**22. What is an Ansible collection?**

??? success "Reveal answer"
    A distribution format for packaging roles, modules, plugins, and playbooks together. The modern 
    way to share Ansible content, replacing standalone roles. 
    ansible-galaxy collection install amazon.aws

## Scenarios and troubleshooting

**23. Write an Ansible playbook for a production-grade web server setup.**

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

**24. What is max_fail_percentage in Ansible?**

??? success "Reveal answer"
    Sets the maximum percentage of failed hosts before aborting the entire play. Useful for rolling 
    deployments — stop if too many hosts fail.

## Practice questions

**25. How do you use Ansible Vault to manage secrets, and how does it integrate with a CI/CD pipeline?**

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

**26. What challenges have you faced with configuration management tools?**

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

**27. How does Chef work?**

??? success "Reveal answer"
    We install chef package in workstation, server and nodes. We create a cookbook in workstation.
    Inside the cookbook, there is a default recipe where we write code in ruby script. After writing code in
    recipe, we upload the whole cookbook to chef server. Chef server acts as a central hub storing code.
    Then, we add the cookbook's recipe to the node's run-list. Chef-client runs frequently, comes to chef
    server, takes the code and applies it to the node. This is how code is converted into infrastructure.

**28. Components of Chef?**

??? success "Reveal answer"
    • Chef Workstation: Where you write the code
    • Chef Server: Where you upload the code
    • Chef Node: Where you apply the code
    • Knife: Tool to establish communication among workstation, server & node
    • Chef-client: Tool runs on every chef node to pull code from chef server
    • Ohai: Maintains current state information of chef node (System Discovery Tool)
    • Idempotency: Tracking the state of system resources to ensure changes don't re-apply repeatedly
    • Chef Supermarket: Where you get custom code

**29. What do you mean by Roles in Ansible?**

??? success "Reveal answer"
    Adding more and more functionality to playbooks makes them difficult to maintain in a single file. To
    address this, we organise playbooks into a directory structure called 'roles'. We create a separate file
    for each section and mention only the names of those sections in the main playbook. When the main
    playbook is called, it calls all section files in the specified order, keeping the main playbook small and
    manageable.

**30. Ansible components?**

??? success "Reveal answer"
    • Server: Place where we create playbooks and write code in YAML format
    • Node: Place where we apply code to create infrastructure (server pushes code to nodes)
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    • SSH: Agent through which Ansible server pushes code to nodes
    • Setup: Module in Ansible which gathers node information
    • Inventory file: File where we keep IP/DNS of nodes

**31. How many types of Chef server?**

??? success "Reveal answer"
    There are 3 ways to manage chef server:
    • Managed/Hosted Chef: Directly from Chef Company — everything managed by Chef, GUI, not
    free after free tier
    • Self-hosted GUI: Launch a server, install chef server package — free, GUI
    • Self-hosted CLI: Launch a server, install chef server package — free, Command Line Interface
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers

**32. How does Chef-client run automatically?**

??? success "Reveal answer"
    By default, chef-client runs manually. We use 'cron tool' (the default Linux scheduling tool) to
    automate it. In the crontab file, we give the chef-client command and set the timing as per
    requirement. Then chef-client runs automatically at frequent intervals. This is a one-time effort done
    during bootstrap.
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers

**33. How does Ansible work?**

??? success "Reveal answer"
    We give node IP addresses in the hosts file by creating groups in Ansible server (Ansible doesn't
    recognize individual IP addresses). We create a playbook and write YAML script. We mention the
    group name in the playbook and execute it. By default, the playbook is executed on all nodes under
    that group. This is how Ansible converts code into infrastructure.

**34. The architecture of Ansible?**

??? success "Reveal answer"
    We create an Ansible server by installing Ansible package in it. Python is a prerequisite. We don't
    need to install Ansible package in nodes because communication is established from server to node
    through 'ssh' client (available by default in all Linux machines). The server pushes code to nodes. So
    Ansible follows a pushing mechanism.

**35. Working process of Ansible?**

??? success "Reveal answer"
    We create a file called a playbook and inside it we write YAML script to create infrastructure. Once we
    execute this playbook, automatically code will be converted into Infrastructure (IAC — Infrastructure
    as Code). We have open source and enterprise editions of Ansible. The enterprise edition is called
    Ansible Tower.

**36. Where do we use conditionals in Playbooks?**

??? success "Reveal answer"
    Sometimes, nodes could be a mixture of different Linux OS flavors. Linux commands vary in different
    operating systems. We can't execute a common set of commands on all machines, nor separate
    commands on each node individually. Conditionals allow commands to be executed based on a
    certain condition we specify.

**37. Why should we go with Configuration Management Tools?**

??? success "Reveal answer"
    • Automate almost each and every admin task
    • Increase uptime and provide maximum user satisfaction
    • Improve the performance of systems
    • Ensure compliance
    • Prevent errors (tools don't make mistakes)
    • Reduce cost (Buy tool once and use 24/7)
    Chef
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers

**38. What do you mean by Ad-Hoc commands in Ansible?**

??? success "Reveal answer"
    These are simple one-liner Linux commands used to meet temporary requirements without saving for
    later. We don't use Ansible modules here, so Idempotency will not work with Ad-Hoc commands. We
    use these for temporary purposes without playbooks, when no suitable YAML module is available.

**39. Why are we using loops concept in Ansible?**

??? success "Reveal answer"
    Sometimes we need to deal with multiple tasks — installing multiple packages, creating many users,
    creating many groups, etc. Mentioning a module for every task is complex. To address this, we use
    the loops concept in combination with variables.

**40. Write a sample playbook by mentioning variables instead of hard coding?**

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

## Related

- Course: [Ansible](../ansible/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
