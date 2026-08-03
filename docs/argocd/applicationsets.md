---
title: "ApplicationSets"
description: "Generate many Argo CD Applications from one ApplicationSet — git, list, cluster, matrix, merge, and pull request generators."
difficulty: advanced
estimated_time: "55–70 min"
technology: argocd
category: argocd
module: "Module 9 · ApplicationSets"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - argocd
  - gitops
  - kubernetes
prerequisites:
  - argocd/kustomize-with-argo-cd
  - argocd/helm-with-argo-cd
next:
  - argocd/multi-cluster-gitops
related:
  - kubernetes/gitops-and-cicd-with-kubernetes
labs: []
projects: []
interview: interview/argocd
certifications:
  - CKA
tags:
  - argocd
  - applicationset
  - gitops
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# ApplicationSets

## Overview

An **ApplicationSet** is a Kubernetes Custom Resource Definition (CRD) that generates one or more Argo CD **Application** resources from a template plus **generators**. Instead of copying Application YAML for every microservice or cluster, you declare rules: scan a Git repo for folders, list known clusters, combine dimensions with **matrix**, merge generator output, or react to **pull requests**.

The ApplicationSet controller ships with Argo CD (v2.3+). Platform teams use it for fleet onboarding — new folder in Git automatically gets an Application.

This is **Tutorial 9** in **Module 9 · ApplicationSets** of the REBASH Academy **Argo CD for Kubernetes GitOps** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Kustomize with Argo CD](kustomize-with-argo-cd.md)
- [Helm with Argo CD](helm-with-argo-cd.md)
- Argo CD with ApplicationSet controller enabled (default in current installs)
- `kubectl` and Python 3

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain ApplicationSet generators and template substitution
- [ ] Author an ApplicationSet with a **list** generator for fixed environments
- [ ] Describe **git**, **cluster**, **matrix**, **merge**, and **pull request** generators
- [ ] Validate ApplicationSet CRD YAML offline with Python
- [ ] Apply an ApplicationSet when the controller is present and verify generated Applications
- [ ] Avoid common template and ownership pitfalls in production

## Architecture

Generators produce parameters; the template renders Applications consumed by the Argo CD application controller.

![GitOps multi-app flow](../assets/excalidraw/git-gitops-flow.svg)

## Theory

### What it is

{% raw %}
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: example
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: dev
            cluster: in-cluster
  template:
    metadata:
      name: 'guestbook-{{env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/example/gitops.git
        path: 'overlays/{{env}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: 'guestbook-{{env}}'
```
{% endraw %}

**Generators** supply key-value pairs (and nested maps) referenced as Go template parameters in the template. Multiple generators can be chained with **matrix** (Cartesian product) or **merge** (combine lists with precedence rules).

| Generator | Purpose |
|-----------|---------|
| **list** | Static list of elements — envs, tenants, known apps |
| **git** | Discover directories or files in a repository |
| **cluster** | One Application per registered cluster secret |
| **matrix** | Combine two generators (e.g. cluster × git path) |
| **merge** | Merge generator results with override rules |
| **pullRequest** | Preview apps for open PRs (GitHub, GitLab, Bitbucket) |
| **scmProvider** | Scan org repos for matching files |

### Why it matters

Manual Application sprawl does not scale past a dozen services. ApplicationSets encode platform conventions once: naming, projects, sync policy, and allowed destinations. New services appear when Git folders appear — no ticket to platform for another YAML file.

### How it works

1. ApplicationSet controller watches ApplicationSet CRs.
2. For each generator result set, it renders the template into an Application name + spec.
3. Generated Applications are created/updated/deleted in the `argocd` namespace (by default).
4. Argo CD application controller syncs each Application as usual.
5. Owner references link generated Applications to the ApplicationSet for garbage collection.

**Go template** functions are available in fields (`path.basename`, `path.basenameNormalized`, etc.) — consult official docs for the full function library.

### Key concepts and comparisons

| Pattern | Use when |
|---------|----------|
| list generator | Small fixed set of envs or tenants |
| git directory generator | Monorepo with `apps/*/overlays/prod` layout |
| cluster generator | Same manifest to many registered clusters |
| matrix | Every service × every cluster |
| pullRequest generator | Ephemeral preview namespaces per PR |

### Common pitfalls

- **Template typos** produce invalid Application names (DNS-1123 violations). **Fix:** Use `path.basenameNormalized`; test with dry-run.
- **Deleting ApplicationSet deletes all child Apps** — including production if generator too broad. **Fix:** Use `syncPolicy.preserveResourcesOnDeletion` when appropriate; narrow generators.
- **PR generator without cleanup** leaves orphan namespaces. **Fix:** Configure requeue and TTL; automate namespace deletion on PR close.
- **Duplicate Application names** from matrix collisions. **Fix:** Include cluster and path in `metadata.name` template.
- **Controller not installed** — ApplicationSet CR never generates Apps. **Fix:** Verify `applicationset-controller` deployment in `argocd` namespace.

## Hands-on Lab

### Objective

Create an ApplicationSet with a **list** generator for dev and staging environments, validate CRD YAML with Python, apply when Argo CD is available, and confirm generated Applications.

### Prerequisites

- ApplicationSet CRD installed (bundled with Argo CD)
- Sample manifests under `~/rebash-argocd/module-09`
- Python 3 with PyYAML (or stdlib yaml if available)

### Lab environment

```bash title="Terminal"
mkdir -p ~/rebash-argocd/module-09/overlays/{dev,staging} \
  ~/rebash-argocd/module-09/appsets && cd ~/rebash-argocd/module-09
```

Namespaces: `rebash-argocd-m09-dev`, `rebash-argocd-m09-staging`.

### Real-world scenario

A platform team onboards internal tools using a list generator for known environments today. Next quarter they will switch the same template to a **git** directory generator when the monorepo grows beyond manual list maintenance.

### Step-by-step tasks

#### Task 1 – Minimal overlay stubs for generated Apps

Create `overlays/dev/kustomization.yaml`:

```yaml title="kustomization.yaml"
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: rebash-argocd-m09-dev
resources:
  - deployment.yaml
```

Create `overlays/dev/deployment.yaml`:

```yaml title="deployment.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: appset-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: appset-demo
  template:
    metadata:
      labels:
        app: appset-demo
    spec:
      containers:
        - name: web
          image: nginxinc/nginx-unprivileged:1.27-alpine
          ports:
            - containerPort: 8080
```

Create `overlays/staging/kustomization.yaml`:

```yaml title="kustomization.yaml"
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: rebash-argocd-m09-staging
resources:
  - deployment.yaml
```

Create `overlays/staging/deployment.yaml`:

```yaml title="deployment.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: appset-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: appset-demo
  template:
    metadata:
      labels:
        app: appset-demo
    spec:
      containers:
        - name: web
          image: nginxinc/nginx-unprivileged:1.27-alpine
          ports:
            - containerPort: 8080
```

Verify overlays build:

```bash title="Terminal"
cd ~/rebash-argocd/module-09
kubectl kustomize overlays/dev | grep 'replicas:' | tee dev-replicas-m09.txt
kubectl kustomize overlays/staging | grep 'replicas:' | tee staging-replicas-m09.txt
grep -q 'replicas: 1' dev-replicas-m09.txt
grep -q 'replicas: 2' staging-replicas-m09.txt
```

!!! example "Expected output"
    Dev overlay one replica; staging two replicas.


#### Task 2 – ApplicationSet with list generator

Create `appsets/applicationset-list.yaml`:

{% raw %}
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: rebash-appset-list
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
    - list:
        elements:
          - env: dev
            namespace: rebash-argocd-m09-dev
            replicas: "1"
          - env: staging
            namespace: rebash-argocd-m09-staging
            replicas: "2"
  template:
    metadata:
      name: rebash-demo-{{ .env }}
    spec:
      project: default
      source:
        repoURL: file:///tmp/rebash-argocd/module-09
        targetRevision: HEAD
        path: overlays/{{ .env }}
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{ .namespace }}"
      syncPolicy:
        automated:
          prune: false
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```
{% endraw %}

Create `appsets/applicationset-git-stub.yaml` (git generator pattern for documentation):

{% raw %}
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: rebash-appset-git-stub
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/argoproj/argocd-example-apps.git
        revision: HEAD
        directories:
          - path: kustomize-guestbook/*
  template:
    metadata:
      name: '{{path.basename}}-guestbook'
    spec:
      project: default
      source:
        repoURL: https://github.com/argoproj/argocd-example-apps.git
        targetRevision: HEAD
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: rebash-argocd-m09-{{path.basename}}
      syncPolicy:
        syncOptions:
          - CreateNamespace=true
```
{% endraw %}

#### Task 3 – Validate CRD YAML with Python

Create `scripts/validate_appset.py`:

```python title="validate_appset.py"
#!/usr/bin/env python3
"""Validate ApplicationSet YAML structure offline."""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

REQUIRED = ("apiVersion", "kind", "metadata", "spec")
GENERATORS = ("list", "git", "clusters", "matrix", "merge", "pullRequest")


def validate(path: Path) -> list[str]:
    errors = []
    doc = yaml.safe_load(path.read_text())
    for key in REQUIRED:
        if key not in doc:
            errors.append(f"{path}: missing {key}")
    if doc.get("kind") != "ApplicationSet":
        errors.append(f"{path}: kind must be ApplicationSet")
    gens = doc.get("spec", {}).get("generators", [])
    if not gens:
        errors.append(f"{path}: spec.generators empty")
    for i, g in enumerate(gens):
        if not any(k in g for k in GENERATORS):
            errors.append(f"{path}: generator[{i}] has no known generator key")
    if "template" not in doc.get("spec", {}):
        errors.append(f"{path}: missing spec.template")
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    files = list(root.glob("appsets/*.yaml"))
    all_errors = []
    for f in files:
        all_errors.extend(validate(f))
    if all_errors:
        print("\n".join(all_errors))
        return 1
    print(f"OK: validated {len(files)} ApplicationSet manifest(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Run validation:

```bash title="Terminal"
cd ~/rebash-argocd/module-09
mkdir -p scripts
chmod +x scripts/validate_appset.py
python3 scripts/validate_appset.py . | tee validate-m09.txt
grep -q 'OK: validated' validate-m09.txt
kubectl apply --dry-run=client -f appsets/applicationset-list.yaml 2>&1 | tee kubectl-dryrun-m09.txt
```

!!! example "Expected output"
    Python script reports OK; kubectl client dry-run accepts the list ApplicationSet.


#### Task 4 – Apply and verify generated Applications

Copy lab to `/tmp` for `file://` repo URL if needed, then apply:

```bash title="Terminal"
cd ~/rebash-argocd/module-09
cp -a ~/rebash-argocd/module-09 /tmp/rebash-argocd/ 2>/dev/null || true
kubectl apply -f appsets/applicationset-list.yaml | tee appset-apply-m09.txt
sleep 20
kubectl get applications -n argocd | grep rebash-demo | tee generated-apps-m09.txt
kubectl get application rebash-demo-dev -n argocd -o jsonpath='{.spec.destination.namespace}{"\n"}' | tee dest-dev-m09.txt
grep -q 'rebash-argocd-m09-dev' dest-dev-m09.txt
kubectl wait --for=jsonpath='{.status.sync.status}'=Synced \
  application/rebash-demo-dev -n argocd --timeout=300s | tee app-dev-sync-m09.txt
kubectl get deploy -n rebash-argocd-m09-dev | tee dev-deploy-m09.txt
grep -q appset-demo dev-deploy-m09.txt
echo "ApplicationSet apply OK" | tee appset-apply-ok-m09.txt
```

!!! example "Expected output"
    Applications `rebash-demo-dev` and `rebash-demo-staging` exist; dev Application syncs and Deployment runs in `rebash-argocd-m09-dev`.


### Validation steps

- [ ] List generator ApplicationSet validates with Python script
- [ ] Git generator stub documents directory discovery pattern
- [ ] Overlays for dev and staging build independently
- [ ] Generated Application names include environment suffix
- [ ] `goTemplate: true` with missingkey=error catches template typos early

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| No Applications generated | Controller disabled or CRD missing | Check `applicationset-controller` deployment |
| Invalid resource name | Template produces uppercase or dots | Use normalized template vars |
| File repo not allowed | Argo CD config blocks file:// | Add repo or use HTTPS Git remote |
| duplicate Application | Name collision in matrix | Include cluster and path in name template |
| preserveResourcesOnDeletion surprise | Apps deleted with ApplicationSet | Set preserve policy if Apps should survive |

### Challenge exercise

Author a **matrix** generator stub combining a two-element list (`dev`, `staging`) with a cluster list (`in-cluster` only) and validate the YAML with the Python script — do not apply unless you understand naming collisions.

### Learning outcomes

- Built list-generator ApplicationSet with environment parameters
- Documented git directory generator pattern for monorepo discovery
- Validated ApplicationSet CRDs offline before apply
- Verified generated Applications when controller is available

### Cleanup

```bash title="Terminal"
kubectl delete applicationset rebash-appset-list -n argocd --ignore-not-found
kubectl delete application rebash-demo-dev rebash-demo-staging -n argocd --ignore-not-found
kubectl delete namespace rebash-argocd-m09-dev rebash-argocd-m09-staging --ignore-not-found
```

## Validation

- [ ] Lab completed under `~/rebash-argocd/module-09/`
- [ ] You can name four generator types and their use cases
- [ ] You validated YAML before cluster apply
- [ ] You understand deletion behaviour for generated Applications

## Code Walkthrough

Production practice for **ApplicationSets** always combines:

1. Start with **list** or **git** generator before matrix complexity
2. Enable `goTemplate` and `missingkey=error` to fail fast on typos
3. CI validates ApplicationSet YAML and renders example Application names
4. Narrow git `directories` paths — avoid generating Apps for entire repo root
5. Document who owns the ApplicationSet CR versus team-owned overlay paths

## Security Considerations

- ApplicationSet in `argocd` namespace is highly privileged — restrict RBAC
- Pull request generators must not expose production credentials to preview apps
- Validate generated destination namespaces — prevent sync to kube-system
- Use Projects to cap allowed repos and clusters per ApplicationSet template
- Audit generator changes — broadening a git path can create unexpected Apps

## Common Mistakes

!!! warning "Over-broad git directory generator"
    `path: apps/*` picks up unfinished folders. **Fix:** Use `exclude` and require `config.yaml` marker files.

!!! warning "Same Application name from matrix"
    Second generator overwrites first. **Fix:** Template name includes `name-env-cluster` template.

!!! warning "Deleting ApplicationSet during incident"
    Removes all generated Applications and may prune workloads. **Fix:** Understand `preserveResourcesOnDeletion`; use maintenance windows.

## Best Practices

- One ApplicationSet per platform convention — not one mega-template for everything
- Migrate from list to git generator when folder count grows
- Integration test template rendering in CI with sample generator output
- Label generated Applications for cost and ownership tracking
- Keep template syncPolicy conservative for production generators

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| ApplicationSet Degraded | Invalid template or repo access | Describe ApplicationSet; check controller logs |
| Fewer Apps than expected | Generator filter excludes paths | Review `directories` exclude rules |
| PR Apps not created | Token or webhook misconfigured | Verify pullRequest generator credentials |
| Template literal braces in YAML | Go template escaping | Use quoted strings or document raw blocks |
| Child App OutOfSync | Overlay path wrong in template | Fix `path: overlays/<env>` parameter |

## Summary

ApplicationSets scale Argo CD Application management through generators and templates — list for fixed envs, git for monorepos, matrix for fleet-wide rollouts. Validate CRDs offline, apply with the controller, and verify generated Applications. Next: **multi-cluster GitOps** with cluster secrets and destinations.

## Interview Questions

**1. What problem do ApplicationSets solve?**

??? success "Reveal answer"
    They eliminate copy-paste Application YAML when many Applications share the same structure but differ by environment, cluster, or Git path. Generators produce parameters; the template renders Applications automatically — reducing platform toil and onboarding time for new services.

**2. Compare list and git generators.**

??? success "Reveal answer"
    List generator uses a static YAML array of elements — ideal for small known sets (dev, staging, prod). Git generator discovers paths or files in a repository — ideal for monorepos where new folders should automatically receive Applications. Git scales better; list is simpler to audit.

**3. What does a matrix generator do?**

??? success "Reveal answer"
    It creates the Cartesian product of two (or more) generators — for example every microservice path × every registered cluster. Powerful for fleet deploys but increases Application count quickly; template naming must avoid collisions.

**4. How do pull request generators fit GitOps workflows?**

??? success "Reveal answer"
    They create ephemeral Applications (and namespaces) when a PR is opened, deploying preview environments from the PR branch. When the PR closes, the generator removes the Application. Requires SCM tokens and careful resource limits so previews do not exhaust the cluster.

**5. What happens when you delete an ApplicationSet?**

??? success "Reveal answer"
    By default, generated Applications are deleted, which may trigger prune and remove workloads depending on sync policy and finalizers. `syncPolicy.preserveResourcesOnDeletion` on the ApplicationSet can keep Kubernetes resources when the ApplicationSet is removed — understand policy before deletion in production.

**6. Why enable `goTemplate: true` and `missingkey=error`?**

??? success "Reveal answer"
    Go templating provides functions like `path.basenameNormalized` and stricter parsing. `missingkey=error` fails template rendering when a parameter is misspelled instead of silently inserting empty strings — preventing invalid Application names or paths.

**7. (Senior) Design ApplicationSets for ten clusters and two hundred services.**

??? success "Reveal answer"
    Use git directory generator for service overlays with strict include/exclude rules; matrix with cluster generator only if every service truly deploys everywhere — otherwise split ApplicationSets by domain. Enforce Argo CD Projects per team, pin sync policy in template, CI-validate rendered Application names, and use progressive rollout (canary cluster in list first) before matrix expansion.

## Related Tutorials

- [Course overview](index.md)
- [Previous: Kustomize with Argo CD](kustomize-with-argo-cd.md)
- [Next: Multi-cluster GitOps](multi-cluster-gitops.md)

## References

- [ApplicationSet documentation](https://argo-cd.readthedocs.io/en/stable/user-guide/application-set/)
- [ApplicationSet generators](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators/)
- [ApplicationSet Go Template](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/GoTemplate/)
- [REBASH Academy Argo CD course](index.md)
