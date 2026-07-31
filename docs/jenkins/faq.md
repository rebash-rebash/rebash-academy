---
title: FAQ
description: "Frequently asked questions about the Jenkins for Cloud & DevOps Engineers course."
technology_id: jenkins
hide:
  - toc
author: Shaik Basha
category: jenkins
tags:
  - jenkins
---

# Jenkins — FAQ

## Who is this course for?

DevOps, Cloud, Platform, Site Reliability Engineering (SRE), DevSecOps, and infrastructure engineers who need production Jenkins Long-Term Support (LTS) skills — from first install to Pipeline, agents, security, and operations.

## Do I need prior experience?

Complete [Git](../git/index.md) and [Docker](../docker/index.md) first. Modules 1–3 assume beginner Continuous Integration (CI) knowledge. [Kubernetes](../kubernetes/index.md) and [Terraform](../terraform/index.md) are required from Modules 13–14 onward.

## Should I use Jenkins LTS or weekly?

Use **LTS** for production and for this course. Weekly releases expose newer features earlier with more churn. The [LTS download line](https://www.jenkins.io/download/lts/) and User Handbook install guides are the authoritative sources.

## Declarative or Scripted Pipeline?

Learn **Declarative Pipeline** first (`pipeline { … }`). Scripted Pipeline remains useful for advanced cases; the official [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/) documents both. This course centres Declarative.

## Why not build on the built-in node?

The controller holds configuration and credentials metadata. Running untrusted build steps there expands blast radius. Prefer labelled agents (static, Docker, or Kubernetes) as described in the [Using Jenkins](https://www.jenkins.io/doc/book/using/) and scaling guidance on jenkins.io.

## How do labs work?

Labs use `~/rebash-jenkins/module-NN`. Early modules bring up Jenkins LTS with Docker Compose; later modules validate Jenkinsfiles and manifests when a full cluster is optional.

## Do diagrams use D2 or Mermaid?

No. This course uses **Excalidraw** SVGs under `docs/assets/excalidraw/`.

## Where is the official documentation?

Start at the [Jenkins User Documentation](https://www.jenkins.io/doc/) — Handbook chapters for installing, using, Pipeline, managing, securing, scaling, and system administration.
