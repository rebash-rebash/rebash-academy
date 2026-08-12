---
title: "Security & DevSecOps Interview Preparation"
description: "49 curated Security & DevSecOps interview prompts — model answers plus real interview questions collected across companies (deduplicated by topic)."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is the difference between Trivy and other vulnerability scanners?**

??? success "Reveal answer"
    Trivy stands out for ease of use with minimal setup, comprehensive coverage of both OS packages and application
    dependencies in one tool, fast lightweight performance suited to CI/CD, and a frequently updated vulnerability
    database that keeps results current.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    3
    SELENIUM

**2. What is a Proxy Server?**

??? success "Reveal answer"
    A proxy server sits between a client and the internet, acting as an intermediary that can improve security by hiding
    the client's real address and improve performance through caching. I've used forward proxies for controlling
    outbound access from a private environment and reverse proxies in front of application servers.

**3. What is the OWASP Top 10?**

??? success "Reveal answer"
    The 10 most critical web application security risks: Broken Access Control, Cryptographic Failures, 
    Injection, Insecure Design, Security Misconfiguration, Vulnerable Components, Authentication 
    Failures, Integrity Failures, Security Logging Failures, SSRF.

**4. What is OWASP ZAP?**

??? success "Reveal answer"
    Zed Attack Proxy — a free, open-source DAST tool for finding security vulnerabilities in web 
    applications. Can be run in CI pipelines in headless mode. 
    docker run -t owasp/zap2docker-stable zap-baseline.py -t 
    https://staging.myapp.com

**5. What are the security features in Nexus Repository Manager?**

??? success "Reveal answer"
    User authentication support for LDAP and Crowd, role-based access control for who can access or modify
    repositories, SSL support for secure communication, and audit logs tracking user actions for security and compliance
    purposes.

**6. What is SLSA (Supply-chain Levels for Software Artifacts)?**

??? success "Reveal answer"
    A security framework with four levels of increasing supply chain security. Level 1: build process 
    documented. Level 2: version-controlled, auditable. Level 3: hardened build platform. Level 4: 
    two-party review of all changes.

**7. What is software supply chain security?**

??? success "Reveal answer"
    Securing the entire software delivery pipeline from source code to production. Covers: signed 
    commits, signed images, SBOM generation, dependency scanning, and SLSA (Supply-chain Levels 
    for Software Artifacts) compliance.

**8. What is JFrog Artifactory?**

??? success "Reveal answer"
    An enterprise-grade artifact management platform. Supports more formats than Nexus, stronger 
    HA capabilities, and deep integration with JFrog's security tools (Xray for vulnerability scanning).

**9. What is a Software Bill of Materials (SBOM)?**

??? success "Reveal answer"
    A formal list of all components, dependencies, and their versions in a software artifact. Generated 
    by tools like Syft, CycloneDX. Increasingly required for supply chain security compliance.

**10. What is GitLab's SAST (Static Application Security Testing)?**

??? success "Reveal answer"
    Built-in security scanning that analyzes source code for vulnerabilities. Enabled by including the 
    SAST template in .gitlab-ci.yml. Supports Python, Java, JavaScript, Go, Ruby, and more.

**11. What is a CVE?**

??? success "Reveal answer"
    Common Vulnerabilities and Exposures — a public database of known security vulnerabilities, 
    each with a unique ID (e.g., CVE-2021-44228 for Log4Shell) and severity score (CVSS).

**12. What is SAST (Static Application Security Testing)?**

??? success "Reveal answer"
    Analyzes source code without executing it. Tools: SonarQube, Semgrep, CodeQL, Bandit (Python), 
    Gosec (Go). Catches SQL injection, hardcoded secrets, insecure deserialization.

**13. What is secret scanning in GitHub/GitLab?**

??? success "Reveal answer"
    Automatically detects and alerts on accidentally committed secrets (API keys, passwords, tokens) 
    by scanning commits and repository content against known secret patterns.

**14. What is SCA (Software Composition Analysis)?**

??? success "Reveal answer"
    Identifies vulnerabilities in open-source dependencies. Tools: Snyk, OWASP Dependency Check, 
    Trivy --security-checks vuln. Critical for Log4Shell-type vulnerabilities.

**15. What is DAST (Dynamic Application Security Testing)?**

??? success "Reveal answer"
    Tests a running application by simulating attacks. Tools: OWASP ZAP, Burp Suite. Discovers 
    vulnerabilities that only appear at runtime (XSS, authentication issues).

**16. What is GitHub's code scanning?**

??? success "Reveal answer"
    Automated security analysis using CodeQL or third-party tools. Runs as part of CI and reports 
    vulnerabilities directly on PRs. Powered by GitHub Advanced Security.

**17. What is DevSecOps?**

??? success "Reveal answer"
    Integrating security practices into every phase of the DevOps lifecycle — "shift left" means 
    catching security issues during development, not after deployment.

**18. What is container image scanning?**

??? success "Reveal answer"
    Analyzing a Docker image for known security vulnerabilities in OS packages and application 
    dependencies. Tools: Trivy, Snyk, Clair, AWS ECR built-in scanning.

**19. What is Elasticsearch security (formerly X-Pack)?**

??? success "Reveal answer"
    Built-in security features: TLS encryption, user authentication, role-based access control, audit 
    logging, field-level security, and document-level security.

**20. What is trufflehog?**

??? success "Reveal answer"
    A secret detection tool that scans Git history deeply, including commit diffs, for sensitive data like 
    API keys, passwords, and private keys.

**21. What is Aqua Security?**

??? success "Reveal answer"
    An enterprise container security platform covering image scanning, runtime protection, secrets 
    management, and Kubernetes network policies.

**22. What is terrascan?**

??? success "Reveal answer"
    A static code analyzer for IaC (Terraform, CloudFormation, Kubernetes) that detects security 
    vulnerabilities and compliance violations.

**23. What is a Zero Trust security model?**

??? success "Reveal answer"
    o A model where no one is trusted by default, requiring strict identity verification.

**24. What is Policy-as-Code?**

??? success "Reveal answer"
    o Defining security and compliance policies in code (e.g., OPA, AWS SCPs).

**25. What is OWASP?**

??? success "Reveal answer"
    Open Web Application Security Project – provides security guidelines.

**26. What is a DAST tool?**

??? success "Reveal answer"
    o Dynamic Application Security Testing (e.g., OWASP ZAP, Burp Suite).

**27. What is Shift-Left Security?**

??? success "Reveal answer"
    Incorporating security early in the software development lifecycle.

**28. What is a SAST tool?**

??? success "Reveal answer"
    o Static Application Security Testing (e.g., SonarQube, Snyk).

## Scenarios and troubleshooting

**29. Your pipaine failed. sccurthy scan. How do. ge handle 18?**

??? success "Reveal answer"
    + Review sean report and understand the findings. # Security-first mindset
    -9 + Fix the issue in code, dependencies, or configuration. * Continuous improvement = = boat Line)
    + Re-run scans to validats. * Automation & quality gates i !
    9 + Document the fix and update security controls if needed. # Team collaborati o-@®
    + Educate the team and prevent similar issues. e penal BY
    ” Gi esas pacha stars eee ie pede 
    ANS: + Use a secrets manager (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault). + Knowledge of secret management tools
    + Never store secrets in code, images, or environment variables. * Best practices understanding lant ox
    i + Rotate secrets regularly. * Compliance & audit awareness - a = =
    - ] Gr Wu idatectad ural, scrivdy. ta your poouanen, eevirenmant: ~~ INCIDENT RESPONSE LIFECYCLE >)
    What is your response? 
    Creer
    ANS: + Detect: Alert triggered / anomaly noticed. # Incident response process N
    Ole oe INTERVIEWER LOOKS. FOR: - : 4
    -~o ANS: + Use IoC tools with security scanning (Checkov, tfeee, efn-nag). # DevSecOps mindset SECURITY AS CODE…

## Practice questions

**30. What tools have you used to scan for vulnerabilities?**

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

**31. How do you integrate security into the DevOps lifecycle (DevSecOps)?**

??? success "Reveal answer"
    During planning, security requirements and threat modeling are considered up front. During coding, secure coding
    practices and code analysis catch issues early. During build, automated static analysis runs in CI. During test,
    vulnerability scanning covers the application and infrastructure. At deploy, IaC scanners check for misconfigurations.
    And in operation, continuous monitoring and alerting catch anomalies, with automated incident detection closing the
    loop.
    KEY POINTS TO MENTION
    • Plan → code → build → test → deploy → operate → monitor, security embedded at every stage

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

## Real interview prompts

Additional questions reported from real DevOps / SRE interviews. Company names are omitted — practise these out loud without notes.

- What if developer coming to you and saying that remove code quality from the pipeline as it is slow in scanning the code in this scenario what steps would you take?
- Follow-up for Q23: If you are using GitHub Marketplace actions, which are third-party tools, how do you ensure security concerns regarding them?
- What are the security protocols will be taken into consideration while designing three tier architecture.,?
- how you ensure the best possible security for high availability architectures for 3 tier applications?
- In your project, what was the application language you scanned with SonarQube?
- What are the best password security practices used by your organisation?
- What top-level security risks from OWASP do you usually check for?
- How will you maintain your base image, vulnerability free?
- And how did you managed security for application level?
- What are the vulnerability reports in your sonarqube?
- How have you implemented security in your project?
- How will you check the vulnerability of your code?
- What are NACLs,SecurityGroups,NAT Gateway?
- How to enable RBAC to Service accounts?
- How to insert Sonar scanner stage?

## Related

- Hub: [Interview Preparation](index.md)
{% endraw %}
