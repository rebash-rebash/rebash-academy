---
title: Ingress and External Access
description: Route HTTP/HTTPS traffic into the cluster with Ingress resources, TLS termination, path-based routing, and Ingress controllers for production external access.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: kubernetes
tags:
  - kubernetes
  - ingress
  - tls
  - external-access
  - nginx
  - load-balancing
prerequisites:
  - Persistent Volumes and Storage
  - Services and Cluster Networking
  - Deployments — Managing Replicated Pods
comments: false
---

# Ingress and External Access

## Overview

ClusterIP Services reach only internal workloads. **NodePort** and **LoadBalancer** expose individual Services — but each public Service needs its own IP or port, and L7 routing (hostname, path, TLS) belongs at the edge, not in every Service definition. **Ingress** defines HTTP/HTTPS routing rules; an **Ingress controller** (nginx, Traefik, HAProxy, AWS ALB) implements those rules and terminates TLS at the cluster boundary.

When a user visits `https://api.example.com/v1/users`, the Ingress controller matches the host and path, forwards to the correct backend Service, and returns the response — hiding internal Pod topology. This is the Kubernetes equivalent of the reverse proxy patterns from [Reverse Proxy and Ingress Basics](../networking/reverse-proxy-and-ingress-basics.md).

This is **Tutorial 10** in **Module 4: Networking & Operations** of the REBASH Academy Kubernetes series. Complete [Persistent Volumes and Storage](persistent-volumes-and-storage.md) and [Services and Cluster Networking](services-and-cluster-networking.md) first.

## Prerequisites

- Completed [Services and Cluster Networking](services-and-cluster-networking.md) — ClusterIP, NodePort, DNS
- Completed [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md)
- Completed [Persistent Volumes and Storage](persistent-volumes-and-storage.md)
- Completed [ConfigMaps and Secrets](configmaps-and-secrets.md) — TLS Secrets
- Familiarity with [HTTP, HTTPS, and the Application Layer](../networking/http-https-and-application-layer.md)
- A cluster with an Ingress controller (minikube: `minikube addons enable ingress`)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the difference between Ingress, Ingress controller, and Service
- [ ] Install and verify an Ingress controller (nginx)
- [ ] Create Ingress rules for hostname and path-based routing
- [ ] Terminate TLS with Kubernetes TLS Secrets
- [ ] Compare Ingress vs LoadBalancer vs Gateway API
- [ ] Debug common Ingress failures (404, 502, certificate errors)
- [ ] Apply production patterns: annotations, rate limiting, and multiple backends

## Architecture

External clients hit the Ingress controller LoadBalancer. The controller reads Ingress rules and proxies to internal ClusterIP Services.

```d2
direction: down

Internet: Internet {
        USER: "Client\nhttps://shop.example.com"
    }
    Edge: "Ingress Controller — nginx / Traefik" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        IC: "LoadBalancer IP\nTLS termination"
        RULES: "Ingress rules\nhost + path routing"
    }
    Cluster: "Cluster Internal" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        SVC1: "Service web\nClusterIP :80"
        SVC2: "Service api\nClusterIP :8080"
        P1: "Pods web"
        P2: "Pods api"
    }
    Internet.USER -> Edge.IC
    Edge.IC -> Edge.RULES
    Edge.RULES -> Cluster.SVC1: "/"
    Edge.RULES -> Cluster.SVC2: "/api"
    Cluster.SVC1 -> Cluster.P1
    Cluster.SVC2 -> Cluster.P2
```

## Theory

### Ingress vs Service vs Ingress Controller

| Component | Role |
|-----------|------|
| **Service (ClusterIP)** | Stable internal IP for Pod load balancing |
| **Ingress** | Declarative HTTP routing rules (API object) |
| **Ingress controller** | Pod(s) that watch Ingress resources and configure a reverse proxy |

Ingress is useless without a controller. Unlike Services (built into Kubernetes), Ingress requires installing nginx-ingress, Traefik, or a cloud-specific controller.

### Ingress Resource Structure

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - shop.example.com
      secretName: shop-tls
  rules:
    - host: shop.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 8080
```

| Field | Purpose |
|-------|---------|
| `ingressClassName` | Selects which controller handles this Ingress |
| `rules.host` | Virtual host matching (HTTP Host header) |
| `paths.pathType` | `Prefix`, `Exact`, or `ImplementationSpecific` |
| `tls.secretName` | Reference to TLS Secret for HTTPS |
| `annotations` | Controller-specific behaviour (rewrites, timeouts, certs) |

### Path Types

| pathType | Matching behaviour |
|----------|-------------------|
| **Prefix** | Matches URL path prefix (`/api` matches `/api/users`) |
| **Exact** | Exact path match only |
| **ImplementationSpecific** | Delegated to controller — avoid unless required |

### TLS Termination

TLS Secrets store certificate and key:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: shop-tls
type: kubernetes.io/tls
data:
  tls.crt: <base64-cert>
  tls.key: <base64-key>
```

Production clusters use **cert-manager** to automate Let's Encrypt certificates — covered in advanced tutorials.

The Ingress controller terminates HTTPS and typically forwards plain HTTP to backend Services on the cluster network (trusted internal path).

### External Access Patterns

| Pattern | When to use |
|---------|-------------|
| **Ingress** | HTTP/HTTPS apps, multiple services on one IP, path/host routing |
| **LoadBalancer Service** | TCP/UDP non-HTTP, single service, cloud LB integration |
| **NodePort** | Development, bare metal without Ingress |
| **Gateway API** | Next-gen replacement for Ingress — advanced traffic management |

### Common Ingress Controller Annotations (nginx)

```yaml
annotations:
  nginx.ingress.kubernetes.io/ssl-redirect: "true"
  nginx.ingress.kubernetes.io/proxy-body-size: "10m"
  nginx.ingress.kubernetes.io/rate-limit: "100"
  cert-manager.io/cluster-issuer: "letsencrypt-prod"
```

Annotations are controller-specific — nginx annotations do not work on Traefik without equivalents.

### Default Backend

Ingress can define a `defaultBackend` for requests matching no rules — typically a custom 404 page Service.

## Hands-on Lab

### Step 1 – Enable Ingress controller (minikube)

**Command:**

```bash
minikube addons enable ingress
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
kubectl get pods -n ingress-nginx
```

**Explanation:** kind and k3s have different install paths. minikube bundles the nginx Ingress controller as an addon.

For kind, install via official manifest:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

### Step 2 – Deploy two backend Services

**Command:**

```bash
kubectl create namespace lab-ingress
kubectl create deployment web --image=nginx:1.25-alpine -n lab-ingress
kubectl create deployment api --image=hashicorp/http-echo -n lab-ingress \
  -- --text="API response" --listen=:8080
kubectl expose deployment web --port=80 --target-port=80 -n lab-ingress
kubectl expose deployment api --port=8080 --target-port=8080 -n lab-ingress
```

**Explanation:** Two Deployments with ClusterIP Services simulate a frontend and API backend.

### Step 3 – Create a basic Ingress

**Command:**

Save as `web-ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: demo-ingress
  namespace: lab-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: demo.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 8080
```

```bash
kubectl apply -f web-ingress.yaml
kubectl get ingress -n lab-ingress
kubectl describe ingress demo-ingress -n lab-ingress
```

**Expected output:**

```text
NAME           CLASS   HOSTS        ADDRESS        PORTS   AGE
demo-ingress   nginx   demo.local   192.168.49.2   80      30s
```

### Step 4 – Test routing

**Command:**

```bash
# minikube — get controller IP
MINIKUBE_IP=$(minikube ip)
curl -s -H "Host: demo.local" http://$MINIKUBE_IP/ | head -5
curl -s -H "Host: demo.local" http://$MINIKUBE_IP/api
```

**Explanation:** The Host header selects the Ingress rule. Path `/` routes to nginx; `/api` routes to http-echo.

**Expected output:**

```text
<!DOCTYPE html>
<html>
...
API response
```

### Step 5 – Add TLS termination

**Command:**

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt -subj "/CN=demo.local"
kubectl create secret tls demo-tls -n lab-ingress --cert=tls.crt --key=tls.key
```

Update Ingress:

```yaml
spec:
  tls:
    - hosts:
        - demo.local
      secretName: demo-tls
  rules:
    - host: demo.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port:
                  number: 80
```

```bash
kubectl apply -f web-ingress.yaml
curl -sk -H "Host: demo.local" https://$MINIKUBE_IP/ | head -3
rm -f tls.key tls.crt
```

**Explanation:** The Ingress controller presents the TLS certificate for HTTPS connections.

### Step 6 – Debug a misconfigured backend

**Command:**

```bash
kubectl patch ingress demo-ingress -n lab-ingress --type=json \
  -p='[{"op":"replace","path":"/spec/rules/0/http/paths/1/backend/service/name","value":"nonexistent"}]'
curl -s -o /dev/null -w "%{http_code}\n" -H "Host: demo.local" http://$MINIKUBE_IP/api
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller --tail=10
kubectl patch ingress demo-ingress -n lab-ingress --type=json \
  -p='[{"op":"replace","path":"/spec/rules/0/http/paths/1/backend/service/name","value":"api"}]'
```

**Explanation:** Wrong Service names produce 502/503 errors. Controller logs reveal upstream resolution failures.

### Step 7 – Clean up

**Command:**

```bash
kubectl delete namespace lab-ingress
```

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
| `kubectl get ingress` | List Ingress resources | `kubectl get ingress -A` |
| `kubectl describe ingress` | Show rules, address, events | `kubectl describe ingress demo-ingress` |
| `minikube addons enable ingress` | Enable nginx controller | minikube only |
| `curl -H "Host: ..."` | Test Ingress routing | `curl -H "Host: demo.local" http://$IP/` |

### Multi-host Ingress with TLS

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: production-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "25m"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
        - api.example.com
      secretName: example-com-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 80
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 8080
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Creating Ingress without a controller"
    Ingress rules are inert without an Ingress controller deployment. Verify controller Pods run in `ingress-nginx` or equivalent namespace.

!!! warning "Wrong ingressClassName"
    Multiple controllers may coexist. `ingressClassName` must match the installed controller class — mismatches leave Ingress unprocessed.

!!! warning "Backend port mismatch"
    Ingress references Service **port** (not targetPort). If Service maps `port: 80` → `targetPort: 8080`, Ingress must use `port.number: 80`.

!!! warning "Forgetting DNS or Host header"
    Ingress routes by Host header. Without DNS pointing to the controller IP, local testing requires `curl -H "Host: ..."` or `/etc/hosts` entries.

## Best Practices

!!! tip "One Ingress controller per cluster edge"
    Standardize on nginx or Traefik. Document supported annotations for your platform team.

!!! tip "Automate TLS with cert-manager"
    Manual certificate rotation does not scale. cert-manager integrates with Let's Encrypt and cloud CAs.

!!! tip "Use NetworkPolicies with Ingress"
    Restrict backend Services to accept traffic only from the Ingress controller namespace.

!!! tip "Monitor Ingress controller health"
    The controller is a single edge failure point. Run multiple replicas and alert on 5xx rate spikes.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 404 Not Found | No matching Ingress rule | Check host, path, pathType; verify `kubectl describe ingress` |
| 502 Bad Gateway | Backend Service has no endpoints | `kubectl get endpoints`; fix selector or probes |
| 503 Service Unavailable | Backend Pods not ready | Check readiness probes and Pod status |
| Certificate error | Wrong/missing TLS Secret | Verify Secret in same namespace; CN/SAN matches host |
| Ingress ADDRESS empty | Controller not ready | Wait for controller Pod; check cloud LB provisioning |
| Redirect loop | ssl-redirect misconfiguration | Check TLS termination and backend protocol annotations |

## Summary

- **Ingress** defines L7 HTTP routing rules; **Ingress controllers** implement them
- Route by **hostname** and **path** to different backend Services on one external IP
- **TLS Secrets** enable HTTPS termination at the cluster edge
- **Ingress** is preferred over per-Service LoadBalancers for HTTP applications
- **Gateway API** is the evolving successor for advanced traffic management
- Next: isolate environments with [Namespaces and Resource Management](namespaces-and-resource-management.md)

## Interview Questions

1. What is the difference between an Ingress and an Ingress controller?
2. Why is Ingress preferred over LoadBalancer for multiple HTTP services?
3. Explain pathType Prefix vs Exact.
4. How does TLS termination work with Ingress?
5. What happens if an Ingress references a Service with no endpoints?
6. What is ingressClassName used for?
7. Compare Ingress with the Gateway API.
8. How do you test Ingress locally without DNS?
9. What annotations are common on nginx Ingress controllers?
10. How does Ingress relate to a reverse proxy like nginx on a VM?

??? tip "Sample Answers (Questions 1, 2, and 5)"

    **Q1 — Ingress vs controller:** An Ingress is a Kubernetes API object declaring HTTP routing rules (hosts, paths, TLS). An Ingress controller is a separate deployment (e.g., nginx-ingress) that watches Ingress resources and configures a reverse proxy to implement those rules. Without a controller, Ingress objects have no effect.

    **Q2 — Ingress vs LoadBalancer:** Each LoadBalancer Service typically provisions a separate cloud load balancer with its own cost and IP. Ingress consolidates many HTTP services behind one entry point, routing by hostname and path — reducing cost and centralizing TLS termination and routing policy.

    **Q5 — No endpoints:** The Ingress controller cannot reach healthy backends. Clients receive 502 Bad Gateway or 503 Service Unavailable. Fix by ensuring Pod labels match Service selectors and readiness probes pass.

## Related Tutorials

- [Kubernetes – Category Overview](index.md)
- [Persistent Volumes and Storage](persistent-volumes-and-storage.md) *(previous in Module 3)*
- [Services and Cluster Networking](services-and-cluster-networking.md)
- [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md)
- [Pods — The Atomic Unit](pods-the-atomic-unit.md)
- [Namespaces and Resource Management](namespaces-and-resource-management.md) *(next in Module 4)*
- [Reverse Proxy and Ingress Basics](../networking/reverse-proxy-and-ingress-basics.md)
- [Load Balancing Fundamentals](../networking/load-balancing-fundamentals.md)

## References

- [Ingress documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [cert-manager documentation](https://cert-manager.io/docs/)
- [Gateway API](https://gateway-api.sigs.k8s.io/)
- [REBASH Academy – Networking Overview](../networking/index.md)
