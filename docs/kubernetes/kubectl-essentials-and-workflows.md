---
title: kubectl Essentials and Workflows
description: Master kubectl declarative and imperative workflows — get, describe, apply, diff, contexts, namespaces, output formats, and production-safe daily operations.
difficulty: beginner
estimated_time: "35 min"
author: Shaik Basha
category: kubernetes
tags:
  - kubernetes
  - kubectl
  - cli
  - workflows
  - declarative
prerequisites:
  - Installing Kubernetes and kubectl
  - Kubernetes Architecture and Components
  - Basic YAML familiarity
comments: false
---

# kubectl Essentials and Workflows

## Overview

**kubectl** is how engineers interact with Kubernetes every day — inspect Pods, apply manifests, stream logs, exec into containers, and roll out changes. Fluent kubectl separates beginners from production-ready operators. This tutorial covers the commands and **workflows** you will use repeatedly: declarative `apply`, imperative debugging, output formatting, context switching, and dry-run patterns.

This is **Tutorial 4** in **Module 2: Workloads** of the REBASH Academy Kubernetes series. Ensure your local cluster from [Installing Kubernetes and kubectl](installing-kubernetes-and-kubectl.md) is running.

## Prerequisites

- [Installing Kubernetes and kubectl](installing-kubernetes-and-kubectl.md) — working cluster and kubectl
- [Kubernetes Architecture and Components](kubernetes-architecture-and-components.md)
- [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md) — docker/kubectl cheat sheet baseline
- Basic [Git](../git/index.md) workflow — manifests belong in version control
- Familiarity with YAML syntax (indentation, lists, key-value pairs)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Use kubectl to inspect cluster resources with get, describe, and logs
- [ ] Apply declarative manifests with kubectl apply and manage changes safely
- [ ] Format kubectl output as YAML, JSON, and custom columns
- [ ] Switch contexts and namespaces efficiently
- [ ] Generate manifests with --dry-run=client and create resources imperatively for learning
- [ ] Follow production-safe workflows: Git-first, diff before apply, avoid manual prod edits
- [ ] Map common Docker commands to kubectl equivalents

## Architecture Diagram

kubectl is a client — it never runs containers directly. Every command becomes an HTTPS request to the API server.

```d2
direction: right

USER: "Engineer / CI"
    KUBECTL: kubectl
    KCFG: "kubeconfig\ncontext + credentials"
    API: kube-apiserver
    OBJ: "API Objects\nPod / Deployment / Service"
    ETCD: etcd
    USER -> KUBECTL
    KUBECTL -> KCFG
    KCFG -> API
    API -> OBJ
    OBJ -> ETCD
```

## Theory

### Declarative vs Imperative

| Approach | Example | Production use |
|----------|---------|----------------|
| **Declarative** | `kubectl apply -f deployment.yaml` | Primary — GitOps, CI/CD, repeatable |
| **Imperative** | `kubectl run nginx --image=nginx` | Quick experiments, debugging |
| **Imperative + dry-run** | `kubectl create deployment ... --dry-run=client -o yaml` | Generate YAML templates |

Kubernetes controllers reconcile **declared state**. Production changes flow: edit YAML in Git → CI validates → `kubectl apply` or GitOps operator syncs.

### Resource Specification: Name, Namespace, Labels

Every object has:

| Field | Purpose |
|-------|---------|
| `apiVersion` | API group and version (`v1`, `apps/v1`) |
| `kind` | Object type (`Pod`, `Deployment`, `Service`) |
| `metadata.name` | Unique name within namespace |
| `metadata.namespace` | Logical partition (default: `default`) |
| `metadata.labels` | Key-value selectors for Services and controllers |

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

### Namespaces

| Namespace | Typical contents |
|-----------|------------------|
| `default` | Your lab workloads |
| `kube-system` | CoreDNS, kube-proxy, CNI |
| `kube-public` | Public cluster info |
| `kube-node-lease` | Node heartbeats |

Create isolated environments: `kubectl create namespace dev`

### Output Formats

| Flag | Use case |
|------|----------|
| `-o wide` | Extra columns (IP, node) |
| `-o yaml` | Full manifest — backup, inspect |
| `-o json` | Scripting with jq |
| `-o name` | Resource/name only — piping to delete |
| `-o jsonpath='{.items[*].metadata.name}'` | Extract specific fields |
| `--show-labels` | Display labels column |

### Essential Command Categories

#### Inspection

```bash
kubectl get pods
kubectl describe pod POD_NAME
kubectl logs POD_NAME [-c CONTAINER] [-f]
kubectl exec -it POD_NAME -- /bin/sh
kubectl top pods   # requires metrics-server
```

#### Modification

```bash
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
kubectl scale deployment NAME --replicas=3
kubectl set image deployment/NAME container=image:tag
kubectl rollout status deployment/NAME
kubectl rollout undo deployment/NAME
```

#### Cluster meta

```bash
kubectl cluster-info
kubectl api-resources
kubectl explain pod.spec.containers
```

### Docker to kubectl Mapping

| Docker | kubectl |
|--------|---------|
| `docker ps` | `kubectl get pods` |
| `docker logs` | `kubectl logs` |
| `docker exec -it` | `kubectl exec -it` |
| `docker inspect` | `kubectl describe` |
| `docker rm -f` | `kubectl delete pod` |
| `docker run` | `kubectl run` / `apply -f` (prefer apply) |

See the full cheat sheet in [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md).

### Production Workflow Pattern

```d2
direction: right

EDIT: "Edit YAML locally"
    DIFF: "kubectl diff -f ."
    APPLY: "kubectl apply -f ."
    VERIFY: "kubectl rollout status"
    GIT: "git commit + push"
    EDIT -> DIFF
    DIFF -> APPLY
    APPLY -> VERIFY
    VERIFY -> GIT
```

Never `kubectl edit` in production without capturing changes back to Git.

### Shell Productivity

| Technique | Example |
|-----------|---------|
| Alias | `alias k=kubectl` |
| Completion | `source <(kubectl completion bash)` |
| Default namespace | `kubectl config set-context --current --namespace=dev` |
| Watch | `kubectl get pods -w` |

## Hands-on Lab

Ensure your cluster is running: `kubectl get nodes`

### Step 1 – Verify context and explore namespaces

**Command:**

```bash
kubectl config current-context
kubectl get namespaces
kubectl get all -n default
```

**Explanation:** Confirm you are on your local lab cluster, not a production context. `kubectl get all` shows common namespaced resources.

**Expected output:**

```text
minikube   (or kind-rebash-lab)
NAME              STATUS   AGE
default           Active   1d
kube-system       Active   1d
...
```

### Step 2 – Create resources declaratively

**Command:**

```bash
mkdir -p ~/k8s-lab/module2
cat <<'EOF' > ~/k8s-lab/module2/web-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  labels:
    app: web
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.27-alpine
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
EOF
kubectl apply -f ~/k8s-lab/module2/web-deployment.yaml
```

**Explanation:** One file, multiple documents separated by `---`. Deployment owns Pods; Service selects them by label `app: web`.

**Expected output:**

```text
deployment.apps/web created
service/web created
```

### Step 3 – Inspect with get, describe, and labels

**Command:**

```bash
kubectl get deployments,pods,svc -l app=web
kubectl get pods -l app=web -o wide
kubectl describe deployment web | tail -20
```

**Explanation:** `-l` filters by label. `describe` shows Events — essential for debugging scheduling and rollout issues.

**Expected output:**

```text
NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/web    2/2     2            2           30s
NAME                       READY   STATUS    RESTARTS   AGE
web-xxxxxxxx-xxxxx         1/1     Running   0          30s
```

### Step 4 – Logs, exec, and port-forward

**Command:**

```bash
POD=$(kubectl get pod -l app=web -o jsonpath='{.items[0].metadata.name}')
kubectl logs "$POD" --tail=5
kubectl exec "$POD" -- nginx -v
kubectl port-forward svc/web 8888:80 &
sleep 2
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8888
kill %1 2>/dev/null || true
```

**Explanation:** Mirrors `docker logs`, `docker exec`, and publishing ports — but Service-backed port-forward is preferred over NodePort for local debugging.

**Expected output:**

```text
HTTP 200
nginx version: nginx/1.27.x
```

### Step 5 – Imperative commands and dry-run YAML generation

**Command:**

```bash
kubectl create deployment debug-demo --image=busybox:1.36 --dry-run=client -o yaml | head -25
kubectl run temp-shell --image=busybox:1.36 --restart=Never --command -- sleep 3600
kubectl get pod temp-shell
kubectl delete pod temp-shell --wait=false
```

**Explanation:** `--dry-run=client -o yaml` prints manifest without sending to API — use to bootstrap YAML files. `kubectl run` creates a bare Pod (Tutorial 5 covers Pods in depth).

### Step 6 – Scale, update image, and rollout

**Command:**

```bash
kubectl scale deployment web --replicas=3
kubectl get pods -l app=web
kubectl set image deployment/web nginx=nginx:1.27-alpine --record=false
kubectl rollout status deployment/web
kubectl rollout history deployment/web
```

**Explanation:** Scaling updates ReplicaSet desired count. Image changes trigger rolling update — old Pods terminate as new ones become Ready.

**Expected output:**

```text
deployment "web" successfully rolled out
```

### Step 7 – Diff, apply update, and clean up

**Command:**

```bash
# Patch replicas in YAML
sed 's/replicas: 2/replicas: 2/' ~/k8s-lab/module2/web-deployment.yaml > /tmp/web-check.yaml
kubectl diff -f /tmp/web-check.yaml || true
kubectl delete -f ~/k8s-lab/module2/web-deployment.yaml
kubectl get all -l app=web
```

**Explanation:** `kubectl diff` previews changes before apply — use in CI. Clean up lab resources when finished.

**Expected output:**

```text
deployment.apps "web" deleted
service "web" deleted
No resources found in default namespace.
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl get` | List resources | `kubectl get pods -A` |
| `kubectl describe` | Detailed state + events | `kubectl describe pod NAME` |
| `kubectl apply -f` | Declarative create/update | `kubectl apply -f dir/` |
| `kubectl delete -f` | Delete from manifest | `kubectl delete -f app.yaml` |
| `kubectl logs -f` | Stream container logs | `kubectl logs -f POD -c CONTAINER` |
| `kubectl exec -it` | Interactive shell | `kubectl exec -it POD -- sh` |
| `kubectl port-forward` | Local tunnel to Pod/Service | `kubectl port-forward svc/S 8080:80` |
| `kubectl diff -f` | Preview apply changes | `kubectl diff -f manifest.yaml` |
| `kubectl rollout` | Manage deployment history | `kubectl rollout undo deploy/web` |
| `kubectl explain` | OpenAPI field documentation | `kubectl explain pod.spec` |

### ~/.bashrc kubectl helpers

```bash
# Add to shell profile
alias k=kubectl
complete -o default -F __start_kubectl k 2>/dev/null || true

kctx() { kubectl config use-context "$1"; }
kns()  { kubectl config set-context --current --namespace="$1"; }
kgp()  { kubectl get pods "$@"; }
```

Reload: `source ~/.bashrc`

## Common Mistakes

!!! warning "Using kubectl run for production workloads"
    Bare Pods from `kubectl run` are not self-healing. Use Deployments (Tutorial 6+) for anything beyond quick tests.

!!! warning "Applying manifests without reviewing diff"
    Unexpected field changes cause outages. Run `kubectl diff -f` or rely on CI validation before apply.

!!! warning "Forgetting -n namespace flag"
    Commands default to current context namespace. Always verify namespace when working in multi-tenant clusters.

!!! warning "Deleting resources with kubectl delete pod on Deployment-owned Pods"
    Deployment recreates deleted Pods. Scale down or delete the Deployment instead.

!!! warning "Editing live objects without Git sync"
    `kubectl edit` changes cluster state but not your repo — drift accumulates. Export changes back to YAML and commit.

## Best Practices

!!! tip "Treat kubectl apply + Git as source of truth"
    Same principle as Dockerfiles in Git — cluster state should trace to a commit SHA via CI or GitOps.

!!! tip "Use labels consistently"
    `app`, `version`, `component` labels enable clean selectors for Services and monitoring.

!!! tip "Prefer describe and events over guessing"
    When something fails, `kubectl describe` before Stack Overflow — Events pinpoint the failing component.

!!! tip "Set default namespace per context for dev"
    `kubectl config set-context --current --namespace=dev` reduces repetitive `-n dev` flags.

!!! tip "Learn kubectl explain early"
    `kubectl explain deployment.spec.strategy` documents fields inline — faster than context-switching to browser docs.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Unable to connect to the server` | Cluster down or wrong context | `kubectl cluster-info`; restart minikube/kind |
| `error: the namespace from the provided object does not match` | Namespace in file vs `-n` flag | Align namespace in YAML and CLI |
| `Forbidden` | RBAC denies action | Check `kubectl auth can-i create pods` |
| Empty `kubectl get pods` | Wrong namespace | `kubectl get pods -A` |
| `kubectl diff` not supported | Server-side diff needs SSA | Use client dry-run or upgrade kubectl |
| Logs empty | Container not started yet | Wait; check `kubectl describe pod` |
| exec fails | Container lacks shell | Use `busybox` debug image or distroless-aware debug tools |

## Summary

- **kubectl** sends requests to the API server using **kubeconfig** contexts — verify context before every session
- **Declarative** `apply -f` is the production workflow; imperative commands help exploration and YAML generation via `--dry-run=client -o yaml`
- Master **get**, **describe**, **logs**, **exec**, and **port-forward** for daily debugging — direct analogs to Docker commands
- Use **labels**, **namespaces**, and **output formats** (`-o yaml`, `-o wide`, jsonpath) for efficient operations
- **rollout**, **scale**, and **set image** manage Deployment lifecycle; always follow with `rollout status`
- Next: [Pods — The Atomic Unit](pods-the-atomic-unit.md)

## Interview Questions

1. What is the difference between kubectl create and kubectl apply?
2. How do you stream logs from a specific container in a Pod?
3. What does kubectl describe show that kubectl get does not?
4. Explain declarative vs imperative kubectl usage in production.
5. How do you switch namespaces without changing context?
6. Map `docker ps`, `docker logs`, and `docker exec` to kubectl.
7. What is kubectl diff used for?
8. How do you generate a Deployment YAML without creating it?
9. Why should you avoid kubectl edit in production without Git sync?
10. What does `kubectl rollout undo` do?

??? tip "Sample Answers (Questions 1, 4, and 6)"

    **Q1 — create vs apply:** `kubectl create` fails if the object exists — it is one-time imperative creation. `kubectl apply` is declarative and idempotent: it creates the object if missing, or patches existing fields to match the manifest (server-side apply in modern kubectl). Production uses apply because repeated application converges state safely.

    **Q4 — Declarative vs imperative:** Declarative workflows store manifests in Git and run `kubectl apply` (or GitOps) so the cluster matches version-controlled desired state. Imperative commands (`run`, `expose`, `scale`) are fine for local experiments but do not leave an audit trail unless captured in YAML. Production requires declarative apply with CI validation and rollbacks via Git revert.

    **Q6 — Docker mapping:** `docker ps` → `kubectl get pods`; `docker logs CONTAINER` → `kubectl logs POD`; `docker exec -it CONTAINER sh` → `kubectl exec -it POD -- sh`. Kubernetes adds namespace, label selectors, and controllers — you rarely manage bare Pods in production.

## Related Tutorials

- [Installing Kubernetes and kubectl](installing-kubernetes-and-kubectl.md) *(previous — Module 1)*
- [Pods — The Atomic Unit](pods-the-atomic-unit.md) *(next)*
- [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md)
- [Kubernetes Architecture and Components](kubernetes-architecture-and-components.md)
- [Kubernetes – Category Overview](index.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Managing Objects — Declarative](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/)
- [kubectl diff](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#diff)
- [Configure Shell Completion](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_completion/)
- [Server-Side Apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/)
