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

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. What are the security protocols will be taken into consideration while designing three tier architecture?**

??? success "Reveal answer"
    **In short:** Secure each tier with identity, network segmentation, encryption, and least privilege.
    
    **Key points**
    - **Edge** — TLS, WAF, DDoS controls.
    - **App tier** — private subnets, IAM roles, secrets manager, patching.
    - **Data tier** — encryption at rest/in transit, tight security groups, backups.
    - Authn/authz (OIDC/OAuth), audit logs, and network ACLs between tiers.
    
    **Trap**
    - Public databases “temporarily” — temporary often becomes permanent.

**2. What is the difference between Trivy and other vulnerability scanners?**

??? success "Reveal answer"
    **In short:** Trivy is a versatile open-source scanner for images, filesystems, IaC, and SBOMs — not only containers.
    
    **Key points**
    - Scans CVEs in OS packages and app dependencies.
    - Also IaC misconfig (Terraform/K8s), secrets, and licence findings.
    - Easy CI integration; compares well to Grype/Snyk/Aqua on scope vs SaaS features.
    - Choose based on policy UI, language coverage, and org licensing needs.
    
    **Trap**
    - Claiming Trivy “replaces” SCA+SAST+DAST — it does not cover runtime DAST.

**3. What are NACLs,SecurityGroups,NAT Gateway?**

??? success "Reveal answer"
    **In short:** Security Groups are stateful instance firewalls; NACLs are stateless subnet firewalls; NAT Gateway enables private egress.
    
    **Key points**
    - **Security Group** — allow rules, stateful, attached to ENIs.
    - **NACL** — subnet-level, numbered allow/deny, ephemeral ports matter.
    - **NAT Gateway** — private subnets reach internet without public IPs.
    - Use SGs as primary control; NACLs as coarse guardrails.
    
    **Trap**
    - Forgetting ephemeral port allows on custom NACLs and mysteriously breaking return traffic.

**4. What are the best password security practices used by your organisation?**

??? success "Reveal answer"
    **In short:** Long unique passwords or passphrases, manager-stored, MFA everywhere, no reuse or sharing.
    
    **Key points**
    - Password managers (org-approved) beat human inventiveness.
    - MFA/WebAuthn for SSO and privileged access.
    - Rotation for shared/break-glass only; prefer SSO + short-lived tokens.
    - Block breached passwords; never put passwords in chat/Git.
    
    **Trap**
    - Monthly forced rotation without breach — drives sticky-note passwords.

**5. What are the vulnerability reports in your sonarqube?**

??? success "Reveal answer"
    **In short:** SonarQube security reports cover vulnerabilities and security hotspots from static analysis.
    
    **Key points**
    - Vulnerabilities: injection, weak crypto, XSS patterns, etc.
    - Hotspots: sensitive code needing human review.
    - Quality gates can fail on new security issues.
    - Complement with SCA and container scanning — Sonar is not the whole SBOM story.
    
    **Trap**
    - Closing hotspots as “Safe” without reading the rule.

**6. What are the security features in Nexus Repository Manager?**

??? success "Reveal answer"
    **In short:** Nexus hardens the supply chain with authz, content validation, cleanup, and optional IQ policy.
    
    **Key points**
    - RBAC/content selectors limit who can publish/consume.
    - Proxying + firewalling reduces direct internet dependency risk.
    - Cleanup and staging repos control what reaches prod.
    - Nexus IQ/Lifecycle adds CVE/licence policy enforcement.
    
    **Trap**
    - Anonymous upload enabled on hosted repos.

**7. What is SLSA (Supply-chain Levels for Software Artifacts)?**

??? success "Reveal answer"
    **In short:** SLSA is a framework of levels that harden how software is built and provenance is proven.
    
    **Key points**
    - Focuses on provenance, build integrity, and hermetic builds.
    - Higher levels require isolated, attested CI builds.
    - Consumers verify attestations before deploy.
    - Pairs with SBOM and signed artefacts (Sigstore/cosign).
    
    **Trap**
    - Saying “we do SLSA” because CI exists — without provenance attestations.

**8. What is software supply chain security?**

??? success "Reveal answer"
    **In short:** Supply-chain security protects source → build → dependency → distribute → deploy from tampering.
    
    **Key points**
    - Threats: poisoned deps, compromised CI, typosquatting, malicious images.
    - Controls: pin/lock deps, signed builds, SBOMs, image signing, least-privilege CI.
    - Verify provenance at deploy time.
    - Monitor advisories and rebuild when base images patch.
    
    **Trap**
    - Trusting `latest` tags from public registries in production.

**9. What is a Software Bill of Materials (SBOM)?**

??? success "Reveal answer"
    **In short:** An SBOM inventories the components and licences in your software — like an ingredients list.
    
    **Key points**
    - Formats: SPDX, CycloneDX.
    - Generated in CI for apps and container images.
    - Enables fast CVE impact analysis (“are we affected?”).
    - Store beside the artefact and verify at admission/deploy.
    
    **Try this**
    - `syft . -o cyclonedx-json`
    - `trivy image --format cyclonedx`
    
    **Trap**
    - Generating SBOMs you never query when the next Log4j-class CVE lands.

**10. What is GitLab's SAST (Static Application Security Testing)?**

??? success "Reveal answer"
    **In short:** GitLab SAST scans source in CI for vulnerable code patterns and reports findings on MRs.
    
    **Key points**
    - Uses language analyzers in CI jobs (Semgrep-based templates, etc.).
    - Findings appear as MR security widgets/reports.
    - Tune rules; fail pipelines on critical new issues.
    - Part of GitLab’s Secure stage alongside dependency and secret scanning.
    
    **Trap**
    - Leaving SAST `allow_failure: true` forever so MRs stay green.

**11. What is SAST (Static Application Security Testing)?**

??? success "Reveal answer"
    **In short:** SAST analyses source or bytecode without executing the app — finds insecure coding patterns early.
    
    **Key points**
    - Runs in IDE/CI; fast feedback on PRs.
    - Catches injection sinks, insecure APIs, secrets patterns (some tools).
    - False positives need triage — tune rulesets.
    - Complements SCA (deps) and DAST (running app).
    
    **Trap**
    - Expecting SAST alone to find authz bugs that need business context.

**12. What is secret scanning in GitHub/GitLab?**

??? success "Reveal answer"
    **In short:** Secret scanning detects tokens/keys committed to Git and blocks or alerts before abuse.
    
    **Key points**
    - GitHub secret scanning / push protection; GitLab secret detection.
    - Pre-commit hooks catch mistakes earlier.
    - On hit: revoke/rotate immediately, then purge history if needed.
    - Prefer OIDC and short-lived credentials over long-lived keys.
    
    **Trap**
    - Removing the secret in a later commit but leaving it in Git history.

**13. What is SCA (Software Composition Analysis)?**

??? success "Reveal answer"
    **In short:** SCA inventories third-party dependencies and flags known CVEs and licence risk.
    
    **Key points**
    - Reads lockfiles/SBOMs for libraries and versions.
    - Tools: Dependabot, Snyk, Trivy, OWASP Dependency-Check, GitLab Dependency Scanning.
    - Gate merges on critical CVEs with available fixes.
    - Keep lockfiles committed and rebuild regularly.
    
    **Trap**
    - Ignoring transitive dependencies — that’s where many CVEs hide.

**14. What is DAST (Dynamic Application Security Testing)?**

??? success "Reveal answer"
    **In short:** DAST probes a running application from the outside like an attacker.
    
    **Key points**
    - Crawls endpoints; tests injection, auth flaws, misconfig.
    - Needs a test environment and realistic auth setup.
    - Slower than SAST; finds runtime/config issues SAST misses.
    - Run on staging; never reckless against prod without approval.
    
    **Trap**
    - Pointing DAST at production and knocking over the site.

**15. What is GitHub's code scanning?**

??? success "Reveal answer"
    **In short:** GitHub code scanning runs CodeQL (or third-party SARIF) to find vulnerabilities in PRs and default branches.
    
    **Key points**
    - CodeQL analyses dataflow for classes of bugs.
    - Results in Security tab and PR annotations.
    - Enable default setup or advanced workflows; gate with required checks.
    - Combine with Dependabot and secret scanning.
    
    **Trap**
    - Turning it on but never assigning owners to open alerts.

**16. What is container image scanning?**

??? success "Reveal answer"
    **In short:** Image scanning inspects container layers for CVEs, secrets, and misconfigurations before deploy.
    
    **Key points**
    - Scan in CI after build; fail on critical/fixable CVEs.
    - Re-scan registries continuously — new CVEs appear after push.
    - Prefer minimal bases and digests; sign images.
    - Admission controllers can block unscanned/unsigned images.
    
    **Try this**
    - `trivy image myrepo/app:1.2.3`
    - `grype myrepo/app@sha256:...`
    
    **Trap**
    - Scanning once at build and never again for six months.

**17. What is Elasticsearch security (formerly X-Pack)?**

??? success "Reveal answer"
    **In short:** Elastic Stack security (formerly X-Pack features) adds authn/authz, TLS, and auditing to Elasticsearch/Kibana.
    
    **Key points**
    - Native users, SSO/JWT, API keys, and role-based access.
    - TLS between nodes and for HTTP clients.
    - Field/document level security in licensed tiers.
    - Audit logs for compliance investigations.
    
    **Trap**
    - Elasticsearch bound to `0.0.0.0` with no auth — ransomware favourite.

**18. What is a Zero Trust security model?**

??? success "Reveal answer"
    **In short:** Zero Trust means never trust by network location — authenticate and authorise every request.
    
    **Key points**
    - Verify explicitly; least privilege; assume breach.
    - Strong identity (SSO/MFA), device posture, short-lived access.
    - Micro-segmentation instead of flat “corp VPN = trusted”.
    - Continuous monitoring and policy engines (service mesh/IAM).
    
    **Trap**
    - VPN-only “Zero Trust” with flat access once connected.

**19. What is Shift-Left Security?**

??? success "Reveal answer"
    **In short:** Shift-left moves security testing earlier — design and PR time, not only pre-prod panic.
    
    **Key points**
    - Threat model in design; SAST/SCA/secrets in CI.
    - IDE plugins for developers; secure defaults in templates.
    - Still need runtime controls — shift-left is not shift-only.
    - Measure mean time from finding to fix on new code.
    
    **Trap**
    - Dumping 5000 legacy findings on day one with no new-code strategy.

## Practice questions

**20. What tools have you used to scan for vulnerabilities?**

??? success "Reveal answer"
    **In short:** I use a layered toolkit: SAST, SCA, secrets, image/IaC scanners, and occasional DAST.
    
    **Key points**
    - Code: Sonar/CodeQL/Semgrep.
    - Deps: Dependabot/Snyk/Trivy.
    - Images/IaC: Trivy/Checkov/tfsec.
    - Runtime: cloud CSPM and admission policies.
    
    **Trap**
    - Tool soup with overlapping alerts and no owner to fix them.

**21. How will you maintain your base image, vulnerability free?**

??? success "Reveal answer"
    **In short:** Pin minimal bases by digest, rebuild on CVE feeds, and block deploys on critical findings.
    
    **Key points**
    - Use slim/distroless bases; drop packages you don’t need.
    - Automate rebuilds when upstream patches land.
    - Scan continuously in the registry; sign approved images.
    - Separate build bases from runtime bases (multi-stage).
    
    **Trap**
    - Pinning an old digest forever “for stability” while CVEs pile up.

**22. How you ensure the best possible security for high availability architectures for 3 tier applications?**

??? success "Reveal answer"
    **In short:** HA must not weaken security — redundant components still need identity, encryption, and segmentation.
    
    **Key points**
    - Multi-AZ private app/data tiers; no public data plane.
    - Least-privilege IAM per instance/role; secrets not on disk.
    - WAF/Shield at edge; strict SG/NACL paths between tiers.
    - Backup/restore tested; break-glass accounts monitored.
    
    **Trap**
    - Opening `0.0.0.0/0` on databases “so failover health checks work”.

**23. Follow-up for Q23: If you are using GitHub Marketplace actions, which are third-party tools, how do you ensure security concerns regarding them?**

??? success "Reveal answer"
    **In short:** Pin third-party Actions to commit SHAs, least-privilege tokens, and review what they can access.
    
    **Key points**
    - Prefer `owner/action@<full-sha>` over moving tags.
    - Limit `permissions:`; don’t pass secrets to untrusted actions.
    - Prefer OIDC over handing cloud keys to Marketplace actions.
    - Review action source; host critical actions internally if needed.
    
    **Trap**
    - `uses: some-user/action@v1` when `v1` can move to malicious code.

**24. How will you check the vulnerability of your code?**

??? success "Reveal answer"
    **In short:** Scan in the PR with SAST/SCA/secrets, then review findings like defects before merge.
    
    **Key points**
    - CI jobs: Sonar/CodeQL + dependency scan + secret scan.
    - Developers fix or justify; security reviews criticals.
    - Track debt; don’t only rely on yearly pentests.
    - Container/IaC scans when those artefacts exist.
    
    **Trap**
    - “We’ll scan on the release branch” — bugs already merged by then.

**25. How have you implemented security in your project?**

??? success "Reveal answer"
    **In short:** Security was designed into identity, pipeline gates, secrets, and runtime controls — not bolted on late.
    
    **Key points**
    - SSO/MFA, least-privilege IAM/RBAC.
    - CI: SAST/SCA/secrets/image scan with failing gates.
    - Secrets in vault/OIDC; encrypted data stores.
    - Network policies, WAF, audit logs, and incident runbooks.
    
    **Trap**
    - A story with only “we used HTTPS” as the entire security programme.

**26. What if developer coming to you and saying that remove code quality from the pipeline as it is slow in scanning the code in this scenario what steps would you take?**

??? success "Reveal answer"
    **In short:** Don’t remove the gate — fix the speed: incremental analysis, caching, and new-code focus.
    
    **Key points**
    - Measure: where time is spent (checkout, tests, Sonar).
    - Use PR/new-code analysis; exclude generated code.
    - Parallelise jobs; cache dependencies/scanner.
    - Escalate: quality is a release requirement, not optional UX.
    
    **Trap**
    - Agreeing to delete the stage under release pressure without a written exception.

**27. How to insert Sonar scanner stage?**

??? success "Reveal answer"
    **In short:** Add a CI stage after tests/coverage that runs the Sonar scanner and waits for the quality gate.
    
    **Key points**
    - Generate coverage, then `sonar-scanner` / Maven `sonar:sonar`.
    - Pass host, token, project key, branch/PR properties.
    - Fail the pipeline on gate ERROR.
    - Publish the dashboard link in the job log.
    
    **Try this**
    - `mvn -B verify sonar:sonar`
    - `waitForQualityGate` (Jenkins)
    
    **Trap**
    - Putting Sonar before unit tests so coverage is always zero.

**28. In your project, what was the application language you scanned with SonarQube?**

??? success "Reveal answer"
    **In short:** Answer with the real languages you scanned — Sonar supports many; cite your project’s stack.
    
    **Key points**
    - Common: Java, JavaScript/TypeScript, Python, C#, Go, Kotlin.
    - Mention multi-module/monorepo setup if relevant.
    - Note quality profiles customised per language.
    - Honesty beats inventing exotic languages.
    
    **Trap**
    - Listing every Sonar language brochure-style when you only scanned Java.

**29. And how did you managed security for application level?**

??? success "Reveal answer"
    **In short:** Application security combined secure coding gates, dependency hygiene, and runtime protections.
    
    **Key points**
    - Authn/authz reviewed; secrets never in code.
    - SAST/SCA in CI; dependency updates automated.
    - Input validation, TLS, security headers, least privilege DB users.
    - Regular dependency bumps and incident-ready logging.
    
    **Trap**
    - WAF-only thinking while SQL injection lives in the app code.

**30. What top-level security risks from OWASP do you usually check for?**

??? success "Reveal answer"
    **In short:** I prioritise OWASP Top 10 classes that match our stack — injection, authn, XSS, misconfig, SSRF.
    
    **Key points**
    - Broken access control and injection remain perennial.
    - Cryptographic failures and security misconfiguration in cloud/K8s.
    - Vulnerable components (SCA) and SSRF for cloud metadata risk.
    - Map each risk to a concrete control in our pipeline/runtime.
    
    **Trap**
    - Memorising the Top 10 list without saying how you test for any item.

**31. How to enable RBAC to Service accounts?**

??? success "Reveal answer"
    **In short:** Create a ServiceAccount, bind Roles/ClusterRoles with least privilege, and mount the token only where needed.
    
    **Key points**
    - Kubernetes: `Role`/`ClusterRole` + `RoleBinding`/`ClusterRoleBinding`.
    - Disable automount on pods that don’t call the API.
    - Prefer projected short-lived tokens over legacy secrets.
    - Cloud: analogous IAM roles for service identities.
    
    **Try this**
    - `kubectl create sa app-sa -n prod`
    - `kubectl create rolebinding ... --serviceaccount=prod:app-sa`
    
    **Trap**
    - Binding `cluster-admin` to every app ServiceAccount “so it works”.

**32. Can Trivy scan local file systems and Git repositories?**

??? success "Reveal answer"
    **In short:** Yes — Trivy scans container images, local filesystems, Git repos, IaC, and SBOMs.
    
    **Key points**
    - `trivy fs` for directories; `trivy repo` for Git URLs.
    - `trivy image` for registries/local images.
    - `trivy config` for misconfigurations.
    - Use the mode that matches the artefact under review.
    
    **Trap**
    - Only scanning images while vulnerable IaC opens the cluster wide.

**33. How can you run a basic scan with Trivy?**

??? success "Reveal answer"
    **In short:** Install Trivy, then scan an image or filesystem and fail CI on severity thresholds.
    
    **Key points**
    - `trivy image python:3.12-slim` for a quick demo.
    - `trivy fs .` for project dependencies/config.
    - JSON/SARIF output for pipeline gates.
    - Cache DB in CI for speed; update vulnerability DB regularly.
    
    **Try this**
    - `trivy image --severity HIGH,CRITICAL nginx:1.27`
    - `trivy fs --scanners vuln,secret .`
    
    **Trap**
    - Ignoring exit codes so scans never fail the build.

**34. How do you implement DevSecOps in a pipeline?**

??? success "Reveal answer"
    **In short:** DevSecOps embeds security gates into every pipeline stage — prevent, detect, respond — with ownership.
    
    **Key points**
    - Prevent: templates, least privilege, signed commits, secret hygiene.
    - Detect: SAST/SCA/secrets/IaC/image scans failing PRs.
    - Protect runtime: policies, admission, WAF, monitoring.
    - Respond: revoke, patch, post-incident improvements in the same pipeline.
    
    **Trap**
    - A security stage that never fails the build — DevSecOps theatre.

## Related
- Hub: [Interview Preparation](index.md)
{% endraw %}
