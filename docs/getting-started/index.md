---
title: Overview
description: Start learning on REBASH Academy — tutorial structure, the eight ready tracks (including AWS and GitLab CI), and what to study first.
difficulty: beginner
estimated_time: "10 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: getting-started
tags:
  - getting-started
  - onboarding
comments: false
---

# Getting Started

Welcome to **REBASH Academy**. This page is your map: how tutorials work, what to learn first, and which tracks are ready today.

## How learning works here

Every tutorial follows a consistent structure so you can move between topics without relearning the format:

1. **Overview & prerequisites** — why it matters and what you need
2. **Learning objectives** — clear outcomes you can check off
3. **Architecture** — visual model of the system when it helps
4. **Theory** — concepts explained for real engineering work
5. **Hands-on lab** — step-by-step practice on your machine
6. **Code walkthrough, validation, best practices, security**
7. **Common mistakes, troubleshooting, interview questions**
8. **Summary, related tutorials, and official references**

Prefer a career-shaped roadmap? Open **[Learning Paths](../learning-paths/index.md)** and start with **DevOps Engineer**.

## What you need

| Requirement | Notes |
|-------------|--------|
| Laptop or VM | Linux preferred (Ubuntu 22.04+ / 24.04 works well) |
| Terminal comfort | Basic shell use is enough to begin |
| Curiosity | Break things in labs — that is the point |

**Add tools as you reach each track:**

| When you reach… | Typical tools |
|-----------------|---------------|
| [AWS](../aws/index.md) | Free Tier account, billing alarm, AWS CLI (LocalStack optional) |
| [CI/CD](../gitlab/index.md) | Free [GitLab.com](https://gitlab.com/) account; `gitlab-ci-local` optional for local lint |
| [Docker](../docker/index.md) | Docker Engine or Docker Desktop |
| [Kubernetes](../kubernetes/index.md) | `kubectl` plus minikube or kind |
| [Terraform](../terraform/index.md) | Terraform CLI 1.9+ |

!!! tip "CI/CD is GitLab-first"
    The CI/CD track under **Tutorials → GitLab CI/CD** (`/gitlab/`) teaches **GitLab CI** only. Jenkins and GitHub Actions are planned as later tracks — do not wait for them to start pipelines.

## Recommended first path

Follow this order: foundations → cloud → Git → **GitLab CI** → containers → orchestration → Infrastructure as Code.

<figure class="rebash-diagram rebash-tree-diagram" markdown="0">

<p class="rebash-tree-title">DevOps learning path</p>

<ul class="rebash-tree">
  <li>1 · Linux</li>
  <li>2 · Networking</li>
  <li>3 · AWS</li>
  <li>4 · Git</li>
  <li>5 · GitLab CI/CD</li>
  <li>6 · Docker</li>
  <li>7 · Kubernetes</li>
  <li>8 · Terraform</li>
</ul>
</figure>

### Start here today

| Step | Track | First tutorial | Status |
|------|--------|----------------|--------|
| 1 | [Linux](../linux/index.md) | [Introduction to Linux](../linux/introduction-to-linux.md) | Ready — 25 tutorials (incl. Advanced Servers) |
| 2 | [Networking](../networking/index.md) | [Introduction to Networking](../networking/introduction-to-networking.md) | Ready — 25 tutorials (incl. Production Network Ops) |
| 3 | [AWS](../aws/index.md) | [Introduction to AWS and Global Infrastructure](../aws/introduction-to-aws-and-global-infrastructure.md) | Ready — 20 tutorials |
| 4 | [Git](../git/index.md) | [Introduction to Git and Version Control](../git/introduction-to-git-and-version-control.md) | Ready — 20 tutorials |
| 5 | [GitLab CI/CD](../gitlab/index.md) | [Introduction to CI/CD and Delivery Models](../gitlab/introduction-to-cicd-and-delivery-models.md) | Ready — 20 tutorials (GitLab CI) |
| 6 | [Docker](../docker/index.md) | [Introduction to Containers and Docker](../docker/introduction-to-containers-and-docker.md) | Ready — 20 tutorials |
| 7 | [Kubernetes](../kubernetes/index.md) | [Introduction to Kubernetes and Orchestration](../kubernetes/introduction-to-kubernetes-and-orchestration.md) | Ready — 20 tutorials |
| 8 | [Terraform](../terraform/index.md) | [Introduction to Terraform and Infrastructure as Code](../terraform/introduction-to-terraform-and-iac.md) | Ready — 20 tutorials |

!!! tip "New to DevOps?"
    Begin with **[Introduction to Linux](../linux/introduction-to-linux.md)** — Linux is the golden foundation on REBASH Academy. Finish through Module 7 servers when you can; do not skip the labs.

## Practice alongside tutorials

| Resource | What it is |
|----------|------------|
| [Labs](../labs/index.md) | Scenario drills (Linux, Networking, AWS, Git, GitLab CI, Docker, Kubernetes, Terraform) |
| [Quizzes](../quizzes/index.md) | Self-mark assessments (incl. GitLab CI fundamentals) |
| [Cheat sheets](../cheatsheets/index.md) | Quick command and pattern reference |
| [Interview prep](../interview/index.md) | Theme maps per track |
| [Status API project](../projects/status-api-portfolio.md) | Portfolio build across Git → Docker → Kubernetes → Terraform |

## Study tips

- **One tutorial at a time** — finish the lab before jumping ahead
- **Type the commands** — copy-paste only after you understand the step
- **Keep notes** — short “what broke / what fixed it” notes beat passive bookmarks
- **Use interview questions** — treat them as a checkpoint, not optional fluff
- **Follow a path** — random topic hopping slows progress; use [Learning Paths](../learning-paths/index.md)
- **Destroy cloud resources** — AWS and paid runners create bills; clean up every session

## What is ready vs coming next

| Available now | Coming next |
|---------------|-------------|
| Linux, Networking, AWS, Git, **GitLab CI/CD**, Docker, Kubernetes, Terraform | Azure, GCP |
| [Labs](../labs/index.md) and [Quizzes](../quizzes/index.md) for the ready tracks | Jenkins and GitHub Actions tracks |
| Learning path, cheat sheets, interview guides | Monitoring, Security, DevSecOps |
| [Status API project](../projects/status-api-portfolio.md) | More portfolio projects |

See the full plan on the **[Roadmap](../roadmap.md)**.

## Learning objectives

After this page you should be able to:

- [ ] Explain how REBASH Academy tutorials are structured
- [ ] Choose a first track based on your experience
- [ ] Open the correct first tutorial and start the lab
- [ ] Find Learning Paths, Labs, and Quizzes when you want practice or a full career sequence
- [ ] Know that CI/CD today means the GitLab CI track under Tutorials

## Next steps

1. Open **[Introduction to Linux](../linux/introduction-to-linux.md)** *(recommended)*  
   or pick another ready track from the table above
2. Bookmark **[Learning Paths](../learning-paths/index.md)** for the full DevOps sequence
3. After Git, continue to **[GitLab CI/CD](../gitlab/index.md)** for pipelines
4. Read **[About](../about.md)** if you want standards and site background

Questions or feedback? Reach out on [LinkedIn](https://www.linkedin.com/in/shaikkhadarbasha/).
