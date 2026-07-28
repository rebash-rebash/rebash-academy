---
title: ConfigMaps and Secrets
description: Decouple configuration from container images using ConfigMaps and Secrets — inject as environment variables, command arguments, or mounted volumes.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
category: kubernetes
tags:
  - kubernetes
  - configmaps
  - secrets
  - configuration
  - twelve-factor
prerequisites:
  - Services and Cluster Networking
  - Deployments — Managing Replicated Pods
  - Pods — The Atomic Unit
comments: false
---

# ConfigMaps and Secrets

## Overview

Hardcoding configuration inside container images violates the [twelve-factor app](https://12factor.net/config) principle: **store config in the environment**. Kubernetes **ConfigMaps** hold non-sensitive configuration — feature flags, log levels, config file contents. **Secrets** hold sensitive data — passwords, API tokens, TLS certificates. Both decouple configuration from images so the same container runs in dev, staging, and production with different settings.

Platform engineers mount ConfigMaps as files, inject them as environment variables, or reference them in command arguments. Security teams integrate Secrets with external vaults (HashiCorp Vault, AWS Secrets Manager) via operators while keeping the Kubernetes API surface consistent.

This is **Tutorial 8** in **Module 3: Configuration & Storage** of the REBASH Academy Kubernetes series. Complete [Services and Cluster Networking](services-and-cluster-networking.md) and [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md) first.

## Prerequisites

- Completed [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md)
- Completed [Services and Cluster Networking](services-and-cluster-networking.md)
- Completed [Pods — The Atomic Unit](pods-the-atomic-unit.md) — volumes, env vars
- Familiarity with [Environment Variables and Shell Config](../linux/environment-variables-shell-config.md)
- A running Kubernetes cluster with kubectl configured

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create ConfigMaps from literals, files, and directories
- [ ] Create Secrets and understand base64 encoding vs encryption at rest
- [ ] Inject ConfigMaps and Secrets as environment variables
- [ ] Mount ConfigMaps and Secrets as volumes in Pods
- [ ] Update configuration and trigger Pod restarts when needed
- [ ] Apply security best practices for Secret management
- [ ] Know when to use ConfigMap vs Secret vs external secret stores

## Architecture Diagram

ConfigMaps and Secrets live in etcd (namespace-scoped). Pods consume them via env vars or volume mounts — the kubelet syncs mounted files.

```mermaid
flowchart TB
    subgraph Store["etcd — namespace scoped"]
        CM["ConfigMap app-config<br/>LOG_LEVEL=debug<br/>config.yaml"]
        SEC["Secret db-credentials<br/>username / password"]
    end

    subgraph Pod["Pod spec"]
        ENV["envFrom / valueFrom"]
        VOL["volumeMount<br/>/etc/config"]
    end

    subgraph Container["Container"]
        APP["Application reads<br/>env vars and files"]
    end

    CM --> ENV
    CM --> VOL
    SEC --> ENV
    SEC --> VOL
    ENV --> APP
    VOL --> APP```

## Theory

### ConfigMaps

ConfigMaps store key-value pairs or entire file contents as data. Maximum size is 1 MiB per ConfigMap — split large configs or use volumes backed by other storage for bigger files.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  LOG_LEVEL: "info"
  APP_MODE: "production"
  nginx.conf: |
    worker_processes auto;
    events { worker_connections 1024; }
    http {
      server { listen 80; location / { return 200 'ok'; } }
    }
```

Create imperatively:

```bash
kubectl create configmap app-config --from-literal=LOG_LEVEL=debug
kubectl create configmap nginx-config --from-file=nginx.conf
```

### Secrets

Secrets store sensitive data in `data` (base64-encoded) or `stringData` (plain text — encoded by the API server):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:
  username: appuser
  password: "s3cr3t-p@ss"
```

| Secret type | Use case |
|-------------|----------|
| **Opaque** | Generic user-defined data |
| **kubernetes.io/tls** | TLS cert and key pair |
| **kubernetes.io/dockerconfigjson** | Registry pull credentials |
| **kubernetes.io/service-account-token** | Legacy SA tokens (avoid manual creation) |

!!! warning "Base64 is not encryption"
    Secret values are base64-encoded for transport, not encrypted. Anyone with etcd access or `kubectl get secret -o yaml` permission can decode them. Enable **encryption at rest** and restrict RBAC.

### Injecting as Environment Variables

```yaml
spec:
  containers:
    - name: app
      image: myapp:1.0
      env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: LOG_LEVEL
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
      envFrom:
        - configMapRef:
            name: app-config
```

| Method | Behavior |
|--------|----------|
| `env.valueFrom.configMapKeyRef` | Single key as env var |
| `envFrom.configMapRef` | All keys as env vars |
| `env.valueFrom.secretKeyRef` | Single secret key as env var |

**Limitation:** Environment variables do not update after Pod start. ConfigMap/Secret changes require Pod restart to pick up new env values.

### Mounting as Volumes

Volume mounts **can** update on disk when the ConfigMap/Secret changes (kubelet sync interval ~60 seconds). Applications must watch files or support reload.

```yaml
spec:
  volumes:
    - name: config-vol
      configMap:
        name: app-config
        items:
          - key: nginx.conf
            path: nginx.conf
    - name: secret-vol
      secret:
        secretName: db-credentials
  containers:
    - name: app
      volumeMounts:
        - name: config-vol
          mountPath: /etc/config
          readOnly: true
        - name: secret-vol
          mountPath: /etc/secrets
          readOnly: true
```

Mounted Secrets appear as files named after keys (`/etc/secrets/password`). File permissions default to `0644` — use `defaultMode: 0400` for tighter permissions.

### Immutable ConfigMaps and Secrets

Mark resources immutable to prevent accidental updates and reduce kubelet watch load:

```yaml
metadata:
  name: app-config
immutable: true
```

Changes require creating a new ConfigMap/Secret and updating the Pod spec reference.

### Config vs Secret — When to Use Which

| Data type | Resource |
|-----------|----------|
| Log levels, feature flags, URLs | ConfigMap |
| Passwords, tokens, private keys | Secret |
| TLS certificates | Secret (type `kubernetes.io/tls`) |
| Large non-sensitive files | ConfigMap volume or PVC |
| Highly sensitive production secrets | External secret operator + Secret |

### External Secret Management

Production clusters often sync from:

- **HashiCorp Vault** via CSI driver or agents
- **AWS Secrets Manager / SSM** via External Secrets Operator
- **GCP Secret Manager** via External Secrets Operator

The Pod spec stays the same — only the Secret source changes.

## Hands-on Lab

### Step 1 – Create a ConfigMap

**Command:**

```bash
kubectl create namespace lab-config
kubectl create configmap web-config -n lab-config \
  --from-literal=LOG_LEVEL=debug \
  --from-literal=APP_ENV=lab
kubectl get configmap web-config -n lab-config -o yaml
```

**Explanation:** Literal keys become `data` entries. Inspect the YAML to see plain-text values in ConfigMaps.

### Step 2 – Create a Secret

**Command:**

```bash
kubectl create secret generic db-secret -n lab-config \
  --from-literal=username=appuser \
  --from-literal=password='lab-secret-123'
kubectl get secret db-secret -n lab-config -o yaml
echo "cGFzc3dvcmQ=" | base64 -d  # decode example if key visible
```

**Explanation:** Secrets store base64-encoded values in `data`. Prefer `stringData` in manifests for readability — the API encodes on write.

### Step 3 – Deploy with env var injection

**Command:**

Save as `web-with-config.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: lab-config
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:1.25-alpine
          env:
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: web-config
                  key: LOG_LEVEL
            - name: DB_USER
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: username
          command: ["/bin/sh", "-c"]
          args:
            - echo "LOG_LEVEL=$LOG_LEVEL DB_USER=$DB_USER"; nginx -g 'daemon off;'
```

```bash
kubectl apply -f web-with-config.yaml
kubectl logs -n lab-config -l app=web
```

**Expected output:**

```text
LOG_LEVEL=debug DB_USER=appuser
```

### Step 4 – Mount ConfigMap as a volume

**Command:**

Save as `web-config-volume.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-html
  namespace: lab-config
data:
  index.html: |
    <html><body><h1>ConfigMap Volume Lab</h1></body></html>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-vol
  namespace: lab-config
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web-vol
  template:
    metadata:
      labels:
        app: web-vol
    spec:
      volumes:
        - name: html
          configMap:
            name: nginx-html
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          volumeMounts:
            - name: html
              mountPath: /usr/share/nginx/html/index.html
              subPath: index.html
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: web-vol
  namespace: lab-config
spec:
  selector:
    app: web-vol
  ports:
    - port: 80
      targetPort: 80
```

```bash
kubectl apply -f web-config-volume.yaml
kubectl run curl-test --image=curlimages/curl:8.5.0 -n lab-config --restart=Never --rm -i -- \
  curl -s http://web-vol
```

**Expected output:**

```html
<html><body><h1>ConfigMap Volume Lab</h1></body></html>
```

### Step 5 – Update ConfigMap and observe behavior

**Command:**

```bash
kubectl patch configmap web-config -n lab-config -p '{"data":{"LOG_LEVEL":"trace"}}'
kubectl logs -n lab-config -l app=web --tail=1
kubectl rollout restart deployment/web -n lab-config
kubectl logs -n lab-config -l app=web --tail=1
```

**Explanation:** Env vars are set at Pod creation — patch alone does not update running Pods. Restart the Deployment to pick up changes.

### Step 6 – Create a TLS Secret

**Command:**

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt -subj "/CN=lab.local"
kubectl create secret tls web-tls -n lab-config --cert=tls.crt --key=tls.key
kubectl describe secret web-tls -n lab-config
rm -f tls.key tls.crt
```

**Explanation:** TLS Secrets store `tls.crt` and `tls.key`. Ingress controllers reference these for HTTPS termination.

### Step 7 – Clean up

**Command:**

```bash
kubectl delete namespace lab-config
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl create configmap` | Create ConfigMap | `kubectl create configmap cfg --from-literal=KEY=val` |
| `kubectl create secret generic` | Create Opaque Secret | `kubectl create secret generic sec --from-literal=PASS=x` |
| `kubectl create secret tls` | Create TLS Secret | `kubectl create secret tls tls --cert=c.crt --key=c.key` |
| `kubectl get configmap -o yaml` | Export ConfigMap | `kubectl get cm app-config -o yaml` |
| `kubectl rollout restart` | Restart Pods after config change | `kubectl rollout restart deployment/web` |

### Complete Deployment with ConfigMap volume and Secret env

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      volumes:
        - name: app-config
          configMap:
            name: api-config
      containers:
        - name: api
          image: myapi:2.0
          envFrom:
            - secretRef:
                name: api-secrets
          volumeMounts:
            - name: app-config
              mountPath: /etc/api/config.yaml
              subPath: config.yaml
              readOnly: true
```

## Common Mistakes

!!! warning "Storing secrets in ConfigMaps"
    ConfigMaps are not designed for sensitive data. Use Secrets (with encryption at rest and RBAC) or external vaults. Never commit Secrets to Git in plain text.

!!! warning "Expecting env vars to update live"
    Environment variables are injected at Pod start. Updating a ConfigMap does not change running container env — restart Pods or use volume mounts with app reload support.

!!! warning "Committing Secret manifests to Git"
    Even base64 is trivially decoded. Use Sealed Secrets, SOPS, or External Secrets Operator for GitOps workflows.

!!! warning "Oversized ConfigMaps"
    The 1 MiB limit applies per ConfigMap. Split large configs or use init containers to fetch configuration from object storage.

## Best Practices

!!! tip "Separate config by environment with namespaces"
    Use `dev`, `staging`, `prod` namespaces with identically named ConfigMaps containing environment-specific values.

!!! tip "Mark production ConfigMaps immutable"
    `immutable: true` prevents accidental kubectl edits and reduces control plane load on large clusters.

!!! tip "Use subPath carefully"
    subPath mounts do not receive ConfigMap updates. Use full directory mounts when hot-reload is required.

!!! tip "Restrict Secret access with RBAC"
    Grant `get/list` on Secrets only to service accounts that need them. Audit with [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md).

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `CreateContainerConfigError` | Missing ConfigMap/Secret reference | Verify resource exists in same namespace |
| Env var empty | Wrong key name | `kubectl get cm -o yaml`; match key exactly |
| Volume mount empty | Wrong key in `items` | Check ConfigMap keys vs volume `items.path` |
| Config change not reflected | Env injection (no hot reload) | `kubectl rollout restart deployment/...` |
| Secret decode in logs | Env vars visible in `/proc` | Prefer file mounts; use external secrets |
| Permission denied on secret file | defaultMode too restrictive | Set `defaultMode: 0440` appropriately |

## Summary

- **ConfigMaps** store non-sensitive configuration; **Secrets** store sensitive data
- Inject via **environment variables** (static after start) or **volume mounts** (can sync on update)
- Base64 encoding is **not encryption** — enable encryption at rest and strict RBAC
- **Immutable** ConfigMaps/Secrets prevent drift and reduce kubelet overhead
- Production teams integrate **External Secrets Operator** with cloud vaults
- Next: persist data beyond Pod lifecycle in [Persistent Volumes and Storage](persistent-volumes-and-storage.md)

## Interview Questions

1. What is the difference between a ConfigMap and a Secret?
2. How do you inject a ConfigMap into a Pod as an environment variable?
3. Why does updating a ConfigMap not automatically update env vars in a running Pod?
4. Is base64 encoding sufficient to protect Secrets?
5. What is the maximum size of a ConfigMap?
6. When would you mount a ConfigMap as a volume instead of using env vars?
7. What does `immutable: true` on a ConfigMap do?
8. How do TLS Secrets differ from Opaque Secrets?
9. Name two tools for managing Secrets in GitOps workflows.
10. What is `subPath` and how does it affect ConfigMap updates?

??? tip "Sample Answers (Questions 1, 3, and 4)"

    **Q1 — ConfigMap vs Secret:** ConfigMaps hold non-sensitive configuration like log levels and config files. Secrets hold sensitive data like passwords and TLS keys. Secrets are base64-encoded and intended for tighter RBAC and optional encryption at rest, but both are API objects stored in etcd.

    **Q3 — Env var updates:** The kubelet sets environment variables when the container starts. It does not re-inject env vars when the ConfigMap changes. Volume mounts can sync file content periodically, but env vars require Pod restart to pick up new values.

    **Q4 — Base64 security:** No. Base64 is encoding for transport, not encryption. Anyone with read access to the Secret can decode values instantly. Enable encryption at rest, restrict RBAC, and use external secret managers for production.

## Related Tutorials

- [Kubernetes – Category Overview](index.md)
- [Services and Cluster Networking](services-and-cluster-networking.md) *(previous)*
- [Persistent Volumes and Storage](persistent-volumes-and-storage.md) *(next)*
- [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md)
- [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md)
- [Volumes and Persistent Storage](../docker/volumes-and-persistent-storage.md)

## References

- [ConfigMaps documentation](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Secrets documentation](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Encrypting Secret Data at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)
- [External Secrets Operator](https://external-secrets.io/)
