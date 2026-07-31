# Technology Definition

## Course

Jenkins for Cloud & DevOps Engineers

---

## Description

A production-focused Jenkins course aligned with the official [Jenkins User Documentation](https://www.jenkins.io/doc/) (User Handbook, tutorials, and Pipeline references).

The course teaches Jenkins LTS from installation through Declarative Pipeline, agents, Docker, shared libraries, security, Kubernetes agents, Terraform pipelines, Jenkins Configuration as Code (JCasC), scaling, and production operations.

Learners finish able to design, operate, and troubleshoot Jenkins platforms used in Cloud and DevOps teams.

Blue Ocean is mentioned only as legacy UI — it is not the learning path.

---

## Target Roles

- DevOps Engineer
- Cloud Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Infrastructure Engineer

---

## Difficulty

Beginner → Advanced

---

## Estimated Duration

8–10 Weeks

---

## Prerequisites

- Git (required)
- Docker (required for labs)
- Kubernetes (before Module 13)
- Terraform (before Module 14)
- Basic Cloud knowledge

---

## MCP Servers

Primary

- Context7

Optional

- Kubernetes
- Terraform
- GitHub
- AWS
- Azure
- Google Cloud

---

## Official documentation map

| REBASH modules | jenkins.io |
|----------------|------------|
| 1–3 | Handbook overview, Installing, Using Jenkins, Guided Tour |
| 4–7 | Pipeline chapter, Multibranch tutorials |
| 8–9 | Pipeline + Docker, Shared libraries tutorial |
| 10–12 | Managing, Securing, testing/report tutorials |
| 13–16 | Scaling, System Administration, Troubleshooting, LTS upgrades + REBASH platform patterns |

Standing references: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/), [Pipeline Steps](https://www.jenkins.io/doc/pipeline/steps/).

---

# Modules

## Module 1 — Introduction to Jenkins and CI/CD

- What is Continuous Integration (CI) / Continuous Delivery (CD)?
- What is Jenkins?
- Controllers and agents
- Jenkins LTS vs weekly
- Ecosystem and plugins (overview)
- Guided Tour mental model

Tutorial: `introduction-to-jenkins-and-ci-cd.md`

---

## Module 2 — Installing Jenkins LTS

- Docker Compose install (lab default)
- Package / WAR awareness
- Initial setup wizard
- Suggested plugins
- Admin user and URL
- Home directory (`JENKINS_HOME`)

Tutorial: `installing-jenkins-lts.md`

---

## Module 3 — Using Jenkins: Jobs, Views, and Folders

- Dashboard
- Freestyle vs Pipeline (contrast only)
- Views and folders
- Build history
- Credentials entry points
- User basics

Tutorial: `using-jenkins-jobs-views-and-folders.md`

---

## Module 4 — Pipeline Fundamentals (Declarative)

- Pipeline concepts: Pipeline, node, stage, step
- Declarative vs Scripted
- `agent`, `stages`, `steps`, `post`
- Pipeline Syntax reference
- Why Pipeline-as-code

Tutorial: `pipeline-fundamentals-declarative.md`

---

## Module 5 — Jenkinsfile in SCM

- Jenkinsfile structure
- Parameters and environment
- Checkout from Git
- Multibranch readiness
- Reviewable pipeline changes
- Pipeline best practices

Tutorial: `jenkinsfile-in-scm.md`

---

## Module 6 — Agents, Nodes, and Executors

- Built-in node risk (do not build on controller)
- Static agents and labels
- Executors and workspaces
- Tool installations
- Agent connectivity basics

Tutorial: `agents-nodes-and-executors.md`

---

## Module 7 — Multibranch Pipelines and Pull Requests

- Multibranch Pipeline jobs
- Branch indexing
- Pull request builds
- Webhooks / SCM triggers
- Organization Folder awareness

Tutorial: `multibranch-pipelines-and-prs.md`

---

## Module 8 — Docker with Jenkins Pipeline

- `agent { docker { … } }`
- Dockerfile agent
- Image build and push patterns
- DinD vs sibling Docker socket (trade-offs)
- Registry credentials

Tutorial: `docker-with-jenkins-pipeline.md`

---

## Module 9 — Shared Libraries

- Global vs folder libraries
- `vars/` and `src/`
- Versioning (`@` version)
- Trust and sandbox
- Reusable steps for teams

Tutorial: `shared-libraries.md`

---

## Module 10 — Managing Jenkins: Plugins, Tools, and CLI

- Manage Jenkins screen
- Plugin Manager and updates
- Global tools
- Jenkins CLI
- Reload / safe restart

Tutorial: `managing-jenkins-plugins-tools-and-cli.md`

---

## Module 11 — Securing Jenkins

- Authentication and authorization
- Matrix / role strategies (overview)
- Credentials store
- CSRF and markup
- Isolate builds from the controller
- Credential hygiene in Multibranch

Tutorial: `securing-jenkins.md`

---

## Module 12 — Testing, Reports, and Quality Gates

- `junit` and test result trends
- HTML Publisher patterns
- Parallel stages
- Notifications
- Quality gates before deploy

Tutorial: `testing-reports-and-quality-gates.md`

---

## Module 13 — Kubernetes Agents and Deploys

- Kubernetes plugin / Pod templates
- Ephemeral agents
- kubectl / Helm from Pipeline
- Rollbacks
- Cluster access least privilege

Tutorial: `kubernetes-agents-and-deploys.md`

---

## Module 14 — Terraform Pipelines in Jenkins

- Init / validate / plan / apply
- Remote state awareness
- Credentials and OIDC-style patterns
- Plan artefacts and approvals
- Destroy discipline for labs

Tutorial: `terraform-pipelines-in-jenkins.md`

---

## Module 15 — JCasC, Scaling, and Operations

- Jenkins Configuration as Code (JCasC)
- Backup and restore of `JENKINS_HOME`
- Architecting for scale
- Metrics and logging hooks
- Multi-team folders and governance

Tutorial: `jcasc-scaling-and-operations.md`

---

## Module 16 — Troubleshooting and Upgrades

- Failed builds and agent issues
- Pipeline replay and console logs
- Plugin problems
- Performance symptoms
- LTS upgrade guides
- Safe restart and rollback

Tutorial: `troubleshooting-and-upgrades.md`

---

# Hands-on Labs

Default runtime: Jenkins LTS via Docker Compose under `~/rebash-jenkins/`.

- Bring up LTS and complete setup notes
- Create a Declarative Pipeline job
- Commit a Jenkinsfile and run from SCM (local Git)
- Label an agent / demonstrate controller isolation policy
- Multibranch or branch-indexed Pipeline stub
- Docker agent Pipeline
- Shared library skeleton
- Plugin list / CLI smoke
- Security checklist lab
- JUnit report Pipeline
- Kubernetes Pod template (kind) or dry-run manifests
- Terraform plan-only Pipeline
- JCasC snippet validation
- Broken Pipeline triage

---

# Projects

## Beginner

CI Pipeline for a Python application (Declarative Jenkinsfile)

---

## Intermediate

Enterprise Jenkins Shared Library

---

## Advanced

Cloud-Native Jenkins with Kubernetes agents

---

## Capstone

Production Jenkins Platform — JCasC, agents, Docker builds, Terraform plan gates, security, monitoring hooks, backup/restore drill

---

# Cheat Sheets

- Jenkins CLI
- Declarative Pipeline syntax
- Jenkinsfile patterns
- Shared libraries
- Credentials and security checklist
- Kubernetes agent snippets
- JCasC starters
- Troubleshooting commands

---

# Interview Preparation

- Controller vs agent architecture
- Why not build on the built-in node
- Declarative vs Scripted
- Multibranch and PR isolation
- Shared library trust model
- Credentials and CSRF
- JCasC and upgrade strategy
- Kubernetes ephemeral agents
- Production incident scenarios

---

# Diagrams

Excalidraw under `docs/assets/excalidraw/` (not D2):

- jenkins-architecture
- jenkins-pipeline-lifecycle
- jenkins-controller-agents
- jenkins-docker-pipeline
- jenkins-shared-library
- jenkins-security
- jenkins-kubernetes-agents
- jenkins-jcasc-ops

---

# Certifications

Light mapping where appropriate:

- CloudBees Certified Jenkins Engineer (CCJE)

---

# Capstone Outcome

After completing this course learners should be able to:

- Install and operate Jenkins LTS safely
- Author Declarative Jenkinsfiles in SCM
- Design agent topologies that protect the controller
- Reuse logic with shared libraries
- Secure credentials and authorization
- Integrate Docker, Kubernetes, and Terraform
- Manage configuration with JCasC
- Troubleshoot builds and plan LTS upgrades
