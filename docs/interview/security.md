---
title: "Security & DevSecOps Interview Preparation"
description: "34 curated Security & DevSecOps interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: security
tags:
  - interview
  - security
comments: false
---

{% raw %}
# Security & DevSecOps Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What are the security protocols will be taken into consideration while designing three tier architecture.,?**

??? success "Reveal answer"
    Start with a precise definition in the context of Security, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**2. What is the difference between Trivy and other vulnerability scanners?**

??? success "Reveal answer"
    Trivy stands out for ease of use with minimal setup, comprehensive coverage of both OS packages and application
    dependencies in one tool, fast lightweight performance suited to CI/CD, and a frequently updated vulnerability
    database that keeps results current.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    3
    SELENIUM

**3. What are NACLs,SecurityGroups,NAT Gateway?**

??? success "Reveal answer"
    Start with a precise definition in the context of Security, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**4. What are the best password security practices used by your organisation?**

??? success "Reveal answer"
    Start with a precise definition in the context of Security, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**5. What are the vulnerability reports in your sonarqube?**

??? success "Reveal answer"
    Start with a precise definition in the context of Security, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**6. What are the security features in Nexus Repository Manager?**

??? success "Reveal answer"
    User authentication support for LDAP and Crowd, role-based access control for who can access or modify
    repositories, SSL support for secure communication, and audit logs tracking user actions for security and compliance
    purposes.

**7. What is SLSA (Supply-chain Levels for Software Artifacts)?**

??? success "Reveal answer"
    A security framework with four levels of increasing supply chain security. Level 1: build process 
    documented. Level 2: version-controlled, auditable. Level 3: hardened build platform. Level 4: 
    two-party review of all changes.

**8. What is software supply chain security?**

??? success "Reveal answer"
    Securing the entire software delivery pipeline from source code to production. Covers: signed 
    commits, signed images, SBOM generation, dependency scanning, and SLSA (Supply-chain Levels 
    for Software Artifacts) compliance.

**9. What is a Software Bill of Materials (SBOM)?**

??? success "Reveal answer"
    A formal list of all components, dependencies, and their versions in a software artifact. Generated 
    by tools like Syft, CycloneDX. Increasingly required for supply chain security compliance.

**10. What is GitLab's SAST (Static Application Security Testing)?**

??? success "Reveal answer"
    Built-in security scanning that analyzes source code for vulnerabilities. Enabled by including the 
    SAST template in .gitlab-ci.yml. Supports Python, Java, JavaScript, Go, Ruby, and more.

**11. What is SAST (Static Application Security Testing)?**

??? success "Reveal answer"
    Analyzes source code without executing it. Tools: SonarQube, Semgrep, CodeQL, Bandit (Python), 
    Gosec (Go). Catches SQL injection, hardcoded secrets, insecure deserialization.

**12. What is secret scanning in GitHub/GitLab?**

??? success "Reveal answer"
    Automatically detects and alerts on accidentally committed secrets (API keys, passwords, tokens) 
    by scanning commits and repository content against known secret patterns.

**13. What is SCA (Software Composition Analysis)?**

??? success "Reveal answer"
    Identifies vulnerabilities in open-source dependencies. Tools: Snyk, OWASP Dependency Check, 
    Trivy --security-checks vuln. Critical for Log4Shell-type vulnerabilities.

**14. What is DAST (Dynamic Application Security Testing)?**

??? success "Reveal answer"
    Tests a running application by simulating attacks. Tools: OWASP ZAP, Burp Suite. Discovers 
    vulnerabilities that only appear at runtime (XSS, authentication issues).

**15. What is GitHub's code scanning?**

??? success "Reveal answer"
    Automated security analysis using CodeQL or third-party tools. Runs as part of CI and reports 
    vulnerabilities directly on PRs. Powered by GitHub Advanced Security.

**16. What is container image scanning?**

??? success "Reveal answer"
    Analyzing a Docker image for known security vulnerabilities in OS packages and application 
    dependencies. Tools: Trivy, Snyk, Clair, AWS ECR built-in scanning.

**17. What is Elasticsearch security (formerly X-Pack)?**

??? success "Reveal answer"
    Built-in security features: TLS encryption, user authentication, role-based access control, audit 
    logging, field-level security, and document-level security.

**18. What is a Zero Trust security model?**

??? success "Reveal answer"
    o A model where no one is trusted by default, requiring strict identity verification.

**19. What is Shift-Left Security?**

??? success "Reveal answer"
    Incorporating security early in the software development lifecycle.

## Practice questions

**20. What tools have you used to scan for vulnerabilities?**

??? success "Reveal answer"
    OWASP Dependency-Check for known vulnerabilities in third-party libraries against the NVD database, SonarQube
    for static code analysis catching code smells, vulnerabilities, and bugs, Trivy for scanning container images,
    filesystems, and Git repositories, Aqua Security or Clair for container image scanning, Snyk for open-source library
    and Docker image vulnerabilities integrated directly into CI/CD, Checkmarx for SAST on source code, and checkov
    or terrascan specifically for scanning Terraform IaC for misconfigurations. Wiring all of these into the pipeline is what
    actually gives a genuine shift-left security posture, catching issues from code through deployment.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    9
    JENKINS

**21. How will you maintain your base image, vulnerability free?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Security components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**22. how you ensure the best possible security for high availability architectures for 3 tier applications?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Security components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**23. Follow-up for Q23: If you are using GitHub Marketplace actions, which are third-party tools, how do you ensure security concerns regarding them?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Security components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**24. How will you check the vulnerability of your code?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Security components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**25. How have you implemented security in your project?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Security components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**26. What if developer coming to you and saying that remove code quality from the pipeline as it is slow in scanning the code in this scenario what steps would you take?**

??? success "Reveal answer"
    Answer directly for Security: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**27. How to insert Sonar scanner stage?**

??? success "Reveal answer"
    Answer directly for Security: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**28. In your project, what was the application language you scanned with SonarQube?**

??? success "Reveal answer"
    Answer directly for Security: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**29. And how did you managed security for application level?**

??? success "Reveal answer"
    Answer directly for Security: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**30. What top-level security risks from OWASP do you usually check for?**

??? success "Reveal answer"
    Answer directly for Security: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**31. How to enable RBAC to Service accounts?**

??? success "Reveal answer"
    Answer directly for Security: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**32. Can Trivy scan local file systems and Git repositories?**

??? success "Reveal answer"
    Yes -- trivy fs scans a local directory, and trivy repo scans a Git repository directly, both against the same
    vulnerability database used for image scans.

**33. How can you run a basic scan with Trivy?**

??? success "Reveal answer"
    trivy image scans a Docker image -- for example, trivy image nginx:latest scans the latest official nginx image for
    known vulnerabilities.

**34. How do you implement DevSecOps in a pipeline?**

??? success "Reveal answer"
    o Integrate security scanning tools (SAST, DAST) into CI/CD.

## Related

- Hub: [Interview Preparation](index.md)
{% endraw %}
