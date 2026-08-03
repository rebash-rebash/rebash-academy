---
title: FAQ
description: "Frequently asked questions about the Argo CD course."
technology_id: argocd
hide:
  - toc
author: Shaik Basha
category: argocd
tags:
  - argocd
last_updated: "2026-08-03"
---

# Argo CD — FAQ

## Who is this course for?

Engineers who need production **GitOps** skills with [Argo CD](https://github.com/argoproj/argo-cd) for Cloud, DevOps, Platform, and SRE work.

## What cluster do I need?

A local **kind** or **minikube** cluster is enough for most labs. Multi-cluster modules use templates and in-cluster destinations so you do not need a second cloud account.

## Should I pin the install version?

Yes for production. Labs may use the `stable` manifest for convenience; pin a release tag from [GitHub Releases](https://github.com/argoproj/argo-cd/releases) in real environments.

``` {.bash .ra-terminal title="Terminal"}
kubectl create namespace argocd
kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## Can I use the official example apps?

Yes. Several labs reference [argocd-example-apps](https://github.com/argoproj/argocd-example-apps) (for example guestbook). Prefer declarative Application YAML in the course labs.

## When should I use ApplicationSets?

Use ApplicationSets when one generator should create many Applications (environments, clusters, or teams). Start with a **list** or **git** generator before matrix/PR generators.

## How do Helm templates work in MkDocs?

Helm and Go template markers can confuse MkDocs macros. Tutorial fences that contain those markers are wrapped in raw Jinja blocks. Committed chart files in your repo use normal Helm syntax with no wrapping.


## Why do some labs use `file:///tmp/rebash-argocd/...`?

Local Application examples use a `file://` repository URL. After you create files under `~/rebash-argocd/module-NN`, mirror them for Argo CD:

``` {.bash .ra-terminal title="Terminal"}
mkdir -p /tmp/rebash-argocd
rsync -a --delete ~/rebash-argocd/module-NN/ /tmp/rebash-argocd/module-NN/
```

Prefer a real Git remote (or [argocd-example-apps](https://github.com/argoproj/argocd-example-apps)) for anything beyond a laptop lab.

## Where is the source of truth for Argo CD behaviour?

The upstream project and docs:

- https://github.com/argoproj/argo-cd  
- https://argo-cd.readthedocs.io/en/stable/
