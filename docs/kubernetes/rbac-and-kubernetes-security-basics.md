---
title: RBAC and Kubernetes Security Basics
description: Control who can do what in your cluster with Roles, ClusterRoles, RoleBindings, ServiceAccounts, and security contexts for production-grade access management.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: kubernetes
tags:
  - kubernetes
  - rbac
  - security
  - serviceaccount
  - authorization
  - least-privilege
prerequisites:
  - Complete [Health Checks, Probes, and Self-Healing](health-checks-probes-and-self-healing.md)
  - Familiarity with namespaces from [Namespaces and Resource Management](namespaces-and-resource-management.md)
  - Cluster admin access for RBAC lab exercises (minikube/kind enable RBAC by default)
comments: false
---

# RBAC and Kubernetes Security Basics

## Overview

Every kubectl command and every in-cluster API call is **authenticated** (who are you?) and **authorized** (are you allowed?). **Role-Based Access Control (RBAC)** is Kubernetes' primary authorization model: administrators define **Roles** (permissions) and **RoleBindings** (who gets them). Without RBAC, any compromised ServiceAccount token or overly broad kubeconfig grants cluster-wide damage potential.

Platform engineers use RBAC to enforce **least privilege** — developers deploy to their namespace but cannot read Secrets in production; CI pipelines apply manifests but cannot delete nodes; observability agents list Pods but cannot exec into them. This tutorial builds that mental model and hands-on skill set.

This is **Tutorial 13** in **Module 5: Security & Tooling** of the REBASH Academy Kubernetes series. Complete [Health Checks, Probes, and Self-Healing](health-checks-probes-and-self-healing.md) first.

## Prerequisites

- Completed [Health Checks, Probes, and Self-Healing](health-checks-probes-and-self-healing.md)
- Understanding of namespaces and Deployments
- Cluster where you can create Roles and RoleBindings (minikube, kind, or cloud cluster with admin access)
- Basic familiarity with verbs: get, list, create, update, delete, patch, watch
- Optional: `openssl` or `kubectl create token` for token-based auth testing

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the Kubernetes authentication and authorization flow for API requests
- [ ] Create Roles and ClusterRoles with granular rules on resources and verbs
- [ ] Bind Roles to users, groups, and ServiceAccounts via RoleBindings and ClusterRoleBindings
- [ ] Scope developer access to specific namespaces using RBAC
- [ ] Configure Pod ServiceAccounts and understand default token behaviour
- [ ] Apply security contexts for non-root containers and read-only filesystems
- [ ] Audit RBAC with `kubectl auth can-i` and avoid overly permissive bindings

## Architecture

RBAC sits in the authorization path after authentication. Bindings connect subjects (users, groups, ServiceAccounts) to roles.

```d2
direction: down

REQ: "API Request"
    AUTHN: "Authentication\ncert / token / OIDC"
    AUTHZ: "Authorization\nRBAC webhook"
    ADM: "Admission Controllers"
    ETCD: etcd
    REQ -> AUTHN
    AUTHN -> AUTHZ: identity
    AUTHZ -> ADM: allowed
    ADM -> ETCD
    RBAC: "RBAC Objects" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        ROLE: "Role / ClusterRole\nrules: verbs + resources"
        BIND: "RoleBinding / ClusterRoleBinding"
        SA: ServiceAccount
        ROLE -> BIND
        SA -> BIND
    }
    RBAC: RBAC
    AUTHZ -> RBAC
```

## Theory

### Authentication vs Authorization

| Stage | Question | Mechanisms |
|-------|----------|------------|
| **Authentication** | Who is making this request? | Client certs, bearer tokens, OIDC (Google, Azure AD, Okta), webhook |
| **Authorization** | Is this identity allowed? | RBAC (default), ABAC (legacy), webhook, Node authorizer |
| **Admission** | Is the request valid/safe? | PodSecurity, ResourceQuota, mutating/validating webhooks |

Human operators typically authenticate via `kubectl` with OIDC or cloud IAM. **Pods** authenticate as **ServiceAccounts** — each namespace has a `default` ServiceAccount unless specified otherwise.

### RBAC Core Objects

| Object | Scope | Purpose |
|--------|-------|---------|
| **Role** | Namespace | Permissions within one namespace |
| **ClusterRole** | Cluster-wide | Permissions across all namespaces or cluster resources |
| **RoleBinding** | Namespace | Grants Role (or ClusterRole) to subjects in namespace |
| **ClusterRoleBinding** | Cluster | Grants ClusterRole cluster-wide |

**Rules** use API groups, resources, verbs, and optional resource names:

```yaml
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "create", "update", "patch"]
```

### Common Verbs and Resources

| Verb | Effect |
|------|--------|
| `get`, `list`, `watch` | Read access |
| `create` | Create new objects |
| `update`, `patch` | Modify existing objects |
| `delete` | Remove objects |
| `*` | All verbs (avoid in production roles) |

Cluster-scoped resources (`nodes`, `persistentvolumes`, `clusterroles`) require **ClusterRole** — Roles cannot grant them.

### Built-in ClusterRoles

Kubernetes ships aggregate and system roles:

| ClusterRole | Purpose |
|-------------|---------|
| `view` | Read-only access to most namespaced resources |
| `edit` | Read/write namespaced resources (no Roles or Secrets read) |
| `admin` | Full namespace admin including Roles |
| `cluster-admin` | Unrestricted cluster access — platform team only |

Bind `edit` or custom roles to developers instead of `cluster-admin`.

### ServiceAccounts

Every Pod runs with a ServiceAccount (default: `default` in its namespace). The legacy auto-mounted token allowed any compromised container to call the API. Modern clusters (1.24+) use **bound service account tokens** with audience and expiration.

```yaml
spec:
  serviceAccountName: payments-api
  automountServiceAccountToken: false  # disable if app doesn't need API access
```

Create dedicated ServiceAccounts per application; grant minimal RBAC via RoleBinding.

### Least-Privilege Patterns

| Persona | Typical permissions |
|---------|---------------------|
| Developer (dev ns) | create/get/list/update Deployments, Pods, ConfigMaps |
| Developer (prod ns) | get/list/watch only; deploy via CI |
| CI/CD pipeline | apply manifests in target namespace; no delete on cluster resources |
| Monitoring agent | get/list/watch Pods, nodes, metrics |
| Backup tool | get/list/watch PVs, PVCs, Secrets (scoped) |

Use **RoleBinding** to a namespace Role for tenant isolation. Reserve **ClusterRoleBinding** for platform components.

### Security Contexts

RBAC controls API access; **security contexts** harden container runtime:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
```

Pod-level and container-level contexts combine. Enforce via Pod Security Standards (restricted baseline) in production namespaces.

### Aggregated ClusterRoles

The `view`, `edit`, and `admin` roles use **aggregation** — custom roles labeled `rbac.authorization.k8s.io/aggregate-to-edit: "true"` merge into built-in roles. Platform teams extend defaults without editing system objects.

## Hands-on Lab

### Step 1 – Verify RBAC is enabled and inspect defaults

**Command:**

```bash
kubectl create namespace rbac-lab
kubectl auth can-i create deployments --namespace=rbac-lab
kubectl auth can-i delete nodes
kubectl get clusterrole view -o yaml | head -30
kubectl get clusterrolebinding cluster-admin -o yaml | grep -A5 subjects
```

**Explanation:** `can-i` checks current user's permissions. `view` ClusterRole defines read-only rules aggregated across API groups.

**Expected output:**

```text
yes
no
kind: ClusterRole
metadata:
  name: view
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
```

### Step 2 – Create a developer Role

**Command:**

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: rbac-lab
  name: developer
rules:
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "create", "update"]
EOF

kubectl describe role developer -n rbac-lab
```

**Explanation:** This Role allows deployment management and log access but not Secret read or Role modification — typical developer scope.

**Expected output:**

```text
Name:         developer
Labels:       <none>
PolicyRule:
  Resources          Non-Resource URLs  Resource Names  Verbs
  ---------          -----------------  --------------  -----
  configmaps         []                 []              [get list create update]
  pods/log           []                 []              [get list watch]
  ...
```

### Step 3 – Create ServiceAccount and RoleBinding

**Command:**

```bash
kubectl create serviceaccount dev-sa -n rbac-lab

cat <<'EOF' | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-sa-binding
  namespace: rbac-lab
subjects:
  - kind: ServiceAccount
    name: dev-sa
    namespace: rbac-lab
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io/v1
EOF

kubectl get rolebinding -n rbac-lab
```

**Explanation:** RoleBinding links `dev-sa` to the `developer` Role. Pods using this ServiceAccount inherit these permissions when calling the API.

**Expected output:**

```text
NAME             ROLE              AGE
dev-sa-binding   Role/developer    5s
```

### Step 4 – Test permissions as ServiceAccount

**Command:**

```bash
kubectl auth can-i create deployments \
  --as=system:serviceaccount:rbac-lab:dev-sa \
  -n rbac-lab

kubectl auth can-i delete secrets \
  --as=system:serviceaccount:rbac-lab:dev-sa \
  -n rbac-lab

kubectl auth can-i create deployments \
  --as=system:serviceaccount:rbac-lab:dev-sa \
  -n default
```

**Explanation:** ServiceAccount identity format is `system:serviceaccount:<namespace>:<name>`. Permissions do not cross namespaces unless ClusterRoleBinding grants them.

**Expected output:**

```text
yes
no
no
```

### Step 5 – Deploy Pod with ServiceAccount and security context

**Command:**

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-web
  namespace: rbac-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: secure-web
  template:
    metadata:
      labels:
        app: secure-web
    spec:
      serviceAccountName: dev-sa
      automountServiceAccountToken: true
      securityContext:
        runAsNonRoot: true
        runAsUser: 101
        fsGroup: 101
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          volumeMounts:
            - name: cache
              mountPath: /var/cache/nginx
            - name: run
              mountPath: /var/run
      volumes:
        - name: cache
          emptyDir: {}
        - name: run
          emptyDir: {}
EOF

kubectl get pods -n rbac-lab -l app=secure-web
kubectl exec -n rbac-lab deploy/secure-web -- id
```

**Explanation:** nginx runs as UID 101 with read-only root filesystem — writable paths use emptyDir volumes. Combined with minimal RBAC, compromise impact is reduced.

**Expected output:**

```text
uid=101(nginx) gid=101(nginx) groups=101(nginx)
```

### Step 6 – Create read-only ClusterRole for observability

**Command:**

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log", "namespaces"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: rbac-lab
subjects:
  - kind: ServiceAccount
    name: dev-sa
    namespace: rbac-lab
roleRef:
  kind: ClusterRole
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io/v1
EOF

kubectl auth can-i list pods --all-namespaces \
  --as=system:serviceaccount:rbac-lab:dev-sa
```

**Explanation:** A ClusterRole can be bound with a namespaced RoleBinding — permissions apply only in `rbac-lab` despite ClusterRole scope.

**Expected output:**

```text
no
```

### Step 7 – Audit and clean up

**Command:**

```bash
kubectl auth can-i list pods \
  --as=system:serviceaccount:rbac-lab:dev-sa \
  -n rbac-lab
kubectl get role,rolebinding,sa -n rbac-lab
kubectl delete namespace rbac-lab --wait=false
```

**Explanation:** Regular RBAC audits (`can-i`, reviewing bindings) catch permission creep after incidents or onboarding changes.

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl auth can-i` | Check permission | `kubectl auth can-i delete pods -n prod` |
| `kubectl auth can-i --list` | List all permissions | `kubectl auth can-i --list -n dev` |
| `kubectl create role` | Imperative role creation | `kubectl create role pod-reader --verb=get,list --resource=pods` |
| `kubectl create rolebinding` | Bind role to subject | `kubectl create rolebinding ... --role=... --serviceaccount=...` |
| `kubectl get clusterrolebindings` | List cluster-wide bindings | `kubectl get clusterrolebindings` |

### CI/CD deploy Role (namespace-scoped)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: cicd-deployer
  namespace: production
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["services", "configmaps"]
    verbs: ["get", "list", "create", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: github-actions-deploy
  namespace: production
subjects:
  - kind: User
    name: github-actions-prod
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: cicd-deployer
  apiGroup: rbac.authorization.k8s.io
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Granting cluster-admin to developers"
    Full cluster access bypasses namespace isolation. Use namespace-scoped Roles; escalate through break-glass procedures only.

!!! warning "Using default ServiceAccount for all Pods"
    Every Pod in a namespace shares the same default identity. Create per-app ServiceAccounts with minimal bindings.

!!! warning "Wildcard verbs or resources in Roles"
    `verbs: ["*"]` on `resources: ["*"]` is equivalent to admin. Enumerate only required permissions.

!!! warning "Forgetting cross-namespace Secret access"
    ClusterRoleBindings to `view` or custom roles may expose Secrets. Kubernetes hides Secret content from `view` — verify custom roles do not grant `secrets` get/list unnecessarily.

## Best Practices

!!! tip "Use RBAC for humans and machines separately"
    OIDC groups for engineers; dedicated ServiceAccounts for CI, operators, and agents — each with distinct Roles.

!!! tip "Automate RBAC in Git"
    Store Roles and RoleBindings in version control. Review permission changes like application code.

!!! tip "Disable automount when not needed"
    Set `automountServiceAccountToken: false` for workloads that never call the Kubernetes API — reduces token exfiltration risk.

!!! tip "Combine RBAC with Pod Security Standards"
    RBAC prevents unauthorized API changes; Pod Security restricts privileged containers at admission — defense in depth.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Forbidden` on kubectl | Missing Role or RoleBinding | `kubectl auth can-i --list`; add binding |
| Pod cannot access API | SA lacks permissions | Check RoleBinding; verify SA name in Pod spec |
| Works as admin, fails as SA | Binding wrong namespace/subject | Verify subject name and namespace match |
| Token not mounted | automount disabled or projected token | Check Pod spec; use projected volume if needed |
| Permission denied cross-namespace | Role is namespace-scoped | Use ClusterRole + RoleBinding or separate Role per ns |
| Security context prevents start | runAsUser conflicts with image | Check image USER; adjust UID or use compatible image |

## Summary

- Kubernetes **authentication** identifies callers; **RBAC authorization** grants or denies API actions
- **Roles** and **ClusterRoles** define permissions; **RoleBindings** and **ClusterRoleBindings** assign them to users, groups, and ServiceAccounts
- **Least privilege** means namespace-scoped roles for developers, dedicated ServiceAccounts per workload, and no unnecessary `cluster-admin`
- **Security contexts** enforce non-root execution, dropped capabilities, and read-only filesystems at runtime
- Audit with `kubectl auth can-i` and treat RBAC manifests as version-controlled infrastructure
- RBAC is necessary but not sufficient — pair with Pod Security, network policies, and secrets management

## Interview Questions

1. What is the difference between a Role and a ClusterRole?
2. Explain how RoleBinding connects subjects to permissions.
3. How does a Pod authenticate to the Kubernetes API?
4. What changed about ServiceAccount tokens in Kubernetes 1.24+?
5. Why should developers not receive cluster-admin in production clusters?
6. What is the difference between the built-in `view`, `edit`, and `admin` ClusterRoles?
7. How do you test whether a ServiceAccount can perform a specific action?
8. What is a security context, and name three fields that improve container security?
9. Can a ClusterRole be bound to permissions in a single namespace? How?
10. What is the difference between RBAC authorization and admission control?

??? tip "Sample Answers (Questions 1, 3, and 9)"

    **Q1 — Role vs ClusterRole:** A Role defines permissions within a single namespace — it can only grant access to namespaced resources in that namespace. A ClusterRole is cluster-scoped: it can grant access to cluster resources (nodes, PVs, ClusterRoles) and can also grant access to namespaced resources across all namespaces. Use Roles for tenant isolation; ClusterRoles for platform components or when binding cluster-wide read access.

    **Q3 — Pod API authentication:** Pods run as a ServiceAccount (explicit or `default`). When `automountServiceAccountToken` is true, the kubelet mounts a JWT token the Pod can present to the API server. The API server authenticates the token as `system:serviceaccount:<ns>:<name>`, then RBAC checks whether that identity has permission for the requested verb and resource.

    **Q9 — ClusterRole in one namespace:** Yes. Create a ClusterRole with desired rules, then create a RoleBinding (not ClusterRoleBinding) in the target namespace. Reference the ClusterRole in `roleRef`. The subject receives only the permissions defined in the ClusterRole, scoped to the RoleBinding's namespace.

## Related Tutorials

- [Kubernetes – Category Overview](index.md)
- [Health Checks, Probes, and Self-Healing](health-checks-probes-and-self-healing.md) *(previous — Module 4)*
- [Troubleshooting Kubernetes Workloads](troubleshooting-kubernetes-workloads.md) *(next in Module 5)*
- [Namespaces and Resource Management](namespaces-and-resource-management.md)
- [Networking – Reverse Proxy and Ingress](../networking/reverse-proxy-and-ingress-basics.md)
- Cheat sheet: [Kubernetes Cheat Sheet](../cheatsheets/kubernetes.md)
- Interview prep: [Kubernetes Interview Prep](../interview/kubernetes.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- [Controlling Access to the Kubernetes API](https://kubernetes.io/docs/concepts/security/controlling-access/)
- [Authorization Overview](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)
