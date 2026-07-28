---
title: Services and Cluster Networking
description: Expose Deployments with Kubernetes Services, understand ClusterIP routing, DNS, kube-proxy, and service types for internal and external traffic.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: kubernetes
tags:
  - kubernetes
  - services
  - networking
  - clusterip
  - dns
  - kube-proxy
prerequisites:
  - Deployments — Managing Replicated Pods
  - Pods — The Atomic Unit
  - Introduction to Networking
comments: false
---

# Services and Cluster Networking

## Overview

Pods are ephemeral — they are created, destroyed, rescheduled, and assigned new IP addresses constantly. Clients cannot rely on Pod IPs. **Services** provide a stable virtual IP and DNS name that load-balances traffic across healthy Pod endpoints. Every microservice in a Kubernetes cluster communicates through Services: frontend calls `http://api.default.svc.cluster.local`, databases expose `ClusterIP` endpoints, and external traffic enters through `NodePort`, `LoadBalancer`, or Ingress.

Understanding cluster networking is essential for debugging "connection refused" errors, designing multi-tier applications, and passing SRE interviews. This tutorial covers Service types, kube-proxy modes, CoreDNS, Endpoints, and the path a packet takes from one Pod to another.

This is **Tutorial 7** in **Module 3: Configuration & Storage** of the REBASH Academy Kubernetes series. Complete [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md) first. Networking fundamentals from [Introduction to Networking](../networking/introduction-to-networking.md) help with IP and port concepts.

## Prerequisites

- Completed [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md)
- Completed [Pods — The Atomic Unit](pods-the-atomic-unit.md) — container ports, labels
- Completed [Installing Kubernetes and kubectl](installing-kubernetes-and-kubectl.md)
- Familiarity with [TCP and UDP](../networking/tcp-and-udp-deep-dive.md) and [DNS Fundamentals](../networking/dns-fundamentals.md)
- A running cluster with a CNI plugin (default on minikube, kind, k3s)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain why Services exist and how they differ from Pod IPs
- [ ] Create ClusterIP, NodePort, and LoadBalancer Services
- [ ] Describe how label selectors connect Services to Pod endpoints
- [ ] Trace DNS resolution for Services via CoreDNS
- [ ] Understand kube-proxy iptables vs IPVS modes at a high level
- [ ] Debug Service connectivity with kubectl and in-cluster tools
- [ ] Choose the appropriate Service type for internal vs external access

## Architecture

A Service fronts a set of Pods selected by labels. kube-proxy programs rules on each node to route traffic to Pod endpoints.

```d2
direction: down

Client: "Calling Pod" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        C: "curl http://web.default.svc.cluster.local"
    }
    Control: "Control Plane" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        SVC: "Service web\nClusterIP 10.96.100.50:80"
        EP: "Endpoints\n10.244.1.5:8080\n10.244.2.3:8080\n10.244.3.7:8080"
    }
    Nodes: "Worker Nodes" {
      style: {
        fill: "#ffedd5"
        stroke: "#ea580c"
      }
        KP: "kube-proxy\niptables / IPVS"
        P1: "Pod web-aaa\n10.244.1.5:8080"
        P2: "Pod web-bbb\n10.244.2.3:8080"
        P3: "Pod web-ccc\n10.244.3.7:8080"
    }
    Client.C -> Control.SVC: "DNS lookup"
    Control.SVC -> Control.EP
    Client.C -> Nodes.KP
    Nodes.KP -> Nodes.P1
    Nodes.KP -> Nodes.P2
    Nodes.KP -> Nodes.P3
```

## Theory

### The Pod IP Problem

Every Pod receives a unique IP address from the CNI (Container Network Interface) plugin. When a Deployment rolls out or a node drains, Pod IPs change. Hardcoding Pod IPs in application config breaks immediately. Services solve this with:

- **Stable ClusterIP** — a virtual IP that persists for the Service lifetime
- **DNS name** — `<service>.<namespace>.svc.cluster.local`
- **Load balancing** — distribute connections across ready endpoints
- **Decoupling** — clients depend on Service name, not Pod lifecycle

### Service Types

| Type | Scope | Use case |
|------|-------|----------|
| **ClusterIP** | Internal only (default) | Microservice-to-microservice communication |
| **NodePort** | Exposes on every node IP at a static port (30000–32767) | Development, bare-metal external access |
| **LoadBalancer** | Provisions cloud LB pointing to NodePort | Production external access on cloud |
| **ExternalName** | CNAME DNS record to external hostname | Delegate to external SaaS/database |
| **Headless** (`clusterIP: None`) | DNS returns Pod IPs directly | StatefulSets, client-side discovery |

### Service Spec and Selectors

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web
  namespace: default
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
```

| Field | Meaning |
|-------|---------|
| `port` | Port the Service listens on (what clients connect to) |
| `targetPort` | Port on the Pod container (can be name or number) |
| `selector` | Must match Pod labels — Endpoints controller builds endpoint list |

!!! note "TargetPort vs containerPort"
    `containerPort` in the Pod spec is documentation for humans and some network policies. Service routing uses `targetPort`. They should match unless you intentionally map ports.

### Endpoints and EndpointSlices

The **Endpoints** controller watches Pods matching the Service selector and populates an Endpoints (or **EndpointSlice**) object with Pod IP:port pairs. If no Pods match, the Service exists but has zero endpoints — requests fail with connection errors.

```bash
kubectl get endpoints web
kubectl get endpointslices -l kubernetes.io/service-name=web
```

Only **Ready** Pods (passing readiness probe) receive traffic.

### Cluster DNS (CoreDNS)

Every Pod receives DNS config via `/etc/resolv.conf`:

```text
nameserver 10.96.0.10
search default.svc.cluster.local svc.cluster.local cluster.local
```

| Query | Resolves to |
|-------|-------------|
| `web` (same namespace) | ClusterIP of Service `web` |
| `web.default` | ClusterIP of Service `web` in `default` |
| `web.default.svc.cluster.local` | Fully qualified Service name |
| Headless Service | A records for each Pod IP |

CoreDNS runs as a Deployment in `kube-system`. If DNS fails cluster-wide, check CoreDNS Pods first.

### kube-proxy

**kube-proxy** runs on every node and implements Service virtual IPs. It watches Services and Endpoints, then programs:

- **iptables** (default on many clusters) — DNAT rules redirect Service IP traffic to Pod IPs
- **IPVS** — higher-performance load balancing for large clusters
- **userspace** (legacy) — rare in modern clusters

You rarely configure kube-proxy directly, but knowing it exists explains why Service IPs are not assigned to any single Pod.

### Pod-to-Pod Networking

The CNI plugin (Calico, Cilium, Flannel, etc.) assigns Pod CIDRs and routes traffic between nodes. Pod-to-Pod communication does not require a Service — but Services add stable naming and load balancing. Direct Pod IP access is appropriate for debugging only.

### NodePort and LoadBalancer

**NodePort** opens a port on every node's IP:

```yaml
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080
```

**LoadBalancer** builds on NodePort — cloud controllers (AWS, GCP, Azure) provision an external load balancer with a public IP that forwards to NodePort backends.

For HTTP routing by hostname and path, use **Ingress** — covered in [Ingress and External Access](ingress-and-external-access.md).

## Hands-on Lab

### Step 1 – Deploy an application with a ClusterIP Service

**Command:**

```bash
kubectl create namespace lab-services
kubectl create deployment api --image=nginx:1.25-alpine --replicas=3 -n lab-services
kubectl expose deployment api --port=80 --target-port=80 -n lab-services
kubectl get svc,pods,endpoints -n lab-services
```

**Explanation:** `kubectl expose` creates a ClusterIP Service with a selector matching the Deployment's Pod labels.

**Expected output:**

```text
NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/api   ClusterIP   10.96.142.33    <none>        80/TCP    10s

NAME              ENDPOINTS                                    AGE
endpoints/api     10.244.1.12:80,10.244.2.8:80,10.244.3.15:80   10s
```

### Step 2 – Test in-cluster DNS and connectivity

**Command:**

```bash
kubectl run curl-test --image=curlimages/curl:8.5.0 -n lab-services --restart=Never -- sleep 3600
kubectl wait --for=condition=Ready pod/curl-test -n lab-services --timeout=60s
kubectl exec -n lab-services curl-test -- curl -s -o /dev/null -w "%{http_code}\n" http://api
kubectl exec -n lab-services curl-test -- curl -s -o /dev/null -w "%{http_code}\n" http://api.lab-services.svc.cluster.local
```

**Explanation:** Short names resolve within the same namespace. Fully qualified domain names (FQDN) work across namespaces.

**Expected output:**

```text
200
200
```

### Step 3 – Observe endpoint changes during rollout

**Command:**

```bash
kubectl get endpoints api -n lab-services -w &
WATCH_PID=$!
kubectl set image deployment/api nginx=nginx:1.26-alpine -n lab-services
kubectl rollout status deployment/api -n lab-services
kill $WATCH_PID 2>/dev/null
kubectl get endpoints api -n lab-services
```

**Explanation:** During rollout, endpoints update as old Pods terminate and new Pods become Ready. Service ClusterIP stays constant.

### Step 4 – Create a NodePort Service

**Command:**

Save as `api-nodeport.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-nodeport
  namespace: lab-services
spec:
  type: NodePort
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30088
```

```bash
kubectl apply -f api-nodeport.yaml
kubectl get svc api-nodeport -n lab-services
# minikube: minikube service api-nodeport -n lab-services --url
```

**Explanation:** NodePort exposes the Service on every node at port 30088. Useful for local development without Ingress.

### Step 5 – Declarative Service manifest

**Command:**

Save as `api-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
  namespace: lab-services
  labels:
    app: api
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
    - name: http
      port: 80
      targetPort: 80
      protocol: TCP
  sessionAffinity: None
```

```bash
kubectl apply -f api-service.yaml
kubectl describe svc api -n lab-services
```

**Explanation:** Production Services belong in Git with explicit port names — required for some Ingress controllers and service mesh protocols.

### Step 6 – Debug a broken selector

**Command:**

```bash
kubectl patch svc api -n lab-services -p '{"spec":{"selector":{"app":"wrong-label"}}}'
kubectl get endpoints api -n lab-services
kubectl exec -n lab-services curl-test -- curl -s -o /dev/null -w "%{http_code}\n" --connect-timeout 3 http://api || echo "connection failed"
kubectl patch svc api -n lab-services -p '{"spec":{"selector":{"app":"api"}}}'
```

**Explanation:** Mismatched selectors produce empty endpoints — the most common Service debugging scenario.

### Step 7 – Clean up

**Command:**

```bash
kubectl delete namespace lab-services
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
| `kubectl expose` | Create Service from Deployment | `kubectl expose deployment api --port=80` |
| `kubectl get svc` | List Services | `kubectl get svc -n lab-services` |
| `kubectl get endpoints` | Show Pod IPs behind Service | `kubectl get endpoints api` |
| `kubectl describe svc` | Detailed Service info | `kubectl describe svc api` |
| `kubectl run` | Temporary Pod for testing | `kubectl run curl --image=curlimages/curl --rm -it -- curl http://api` |

### Multi-port Service example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: metrics-api
spec:
  selector:
    app: api
  ports:
    - name: http
      port: 80
      targetPort: 8080
    - name: metrics
      port: 9090
      targetPort: 9090
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Mismatching Service selector and Pod labels"
    If the Service selector does not match any Pod labels, Endpoints are empty and all requests fail. Verify with `kubectl get endpoints`.

!!! warning "Confusing port and targetPort"
    `port` is the Service front door; `targetPort` is the container port. Mapping `port: 80` → `targetPort: 8080` is valid — clients call port 80, traffic arrives at container port 8080.

!!! warning "Using NodePort in production without firewall rules"
    NodePort exposes a high port on every node. Without network policies and firewalls, you expose unintended attack surface. Prefer LoadBalancer or Ingress for production.

!!! warning "Expecting ExternalName to proxy traffic"
    ExternalName Services create a DNS CNAME only. They do not proxy TCP connections — the client resolves the external hostname and connects directly.

## Best Practices

!!! tip "Name ports explicitly"
    Use named ports (`name: http`) in both Pod and Service specs. Ingress controllers and HPAs reference port names reliably.

!!! tip "Use ClusterIP for internal communication"
    Default to ClusterIP. Add NodePort/LoadBalancer only when external access is required. HTTP routing belongs in Ingress.

!!! tip "Verify readiness before debugging Services"
    Not-ready Pods are excluded from Endpoints. Check `kubectl get pods` and readiness probe config before blaming the Service.

!!! tip "Document FQDN conventions"
    Cross-namespace calls require FQDN: `service.namespace.svc.cluster.local`. Short names only work within the same namespace.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused to Service | Empty endpoints, wrong targetPort | `kubectl get endpoints`; verify selector and port |
| DNS resolution fails | CoreDNS down, wrong namespace | `kubectl get pods -n kube-system -l k8s-app=kube-dns`; use FQDN |
| Works by IP, fails by name | DNS misconfiguration | Check Pod `/etc/resolv.conf`; test CoreDNS |
| Intermittent failures | Only some Pods ready | Check readiness probes and rollout status |
| NodePort unreachable | Firewall, wrong node IP | Verify security groups; use correct node external IP |
| LoadBalancer pending | No cloud controller | Expected on bare metal; use MetalLB or Ingress |

## Summary

- **Services** provide stable ClusterIP and DNS names for ephemeral Pod backends
- **Label selectors** link Services to Pods; the Endpoints controller maintains the backend list
- **ClusterIP** is the default for internal traffic; **NodePort** and **LoadBalancer** expose externally
- **CoreDNS** resolves Service names within the cluster
- **kube-proxy** implements Service load balancing on each node via iptables or IPVS
- Next: inject configuration with [ConfigMaps and Secrets](configmaps-and-secrets.md)

## Interview Questions

1. Why do Pods need Services instead of direct IP communication?
2. Explain the difference between `port` and `targetPort` in a Service spec.
3. What is a headless Service and when would you use one?
4. How does CoreDNS resolve `api.production.svc.cluster.local`?
5. What happens to Service endpoints during a rolling update?
6. Compare ClusterIP, NodePort, and LoadBalancer Service types.
7. What role does kube-proxy play in cluster networking?
8. How do readiness probes affect Service traffic routing?
9. What is an EndpointSlice and why did Kubernetes introduce it?
10. How would you debug a Pod that cannot reach a Service?

??? tip "Sample Answers (Questions 1, 3, and 6)"

    **Q1 — Why Services:** Pod IPs change whenever Pods restart, reschedule, or roll out. Services provide a stable virtual IP and DNS name that load-balances across current healthy Pod endpoints, decoupling clients from Pod lifecycle.

    **Q3 — Headless Service:** A headless Service has `clusterIP: None`. DNS returns A records pointing directly to Pod IPs instead of a single ClusterIP. Use with StatefulSets when clients need stable Pod identity or client-side load balancing.

    **Q6 — Service types:** ClusterIP is internal-only — reachable only inside the cluster. NodePort opens a static port (30000–32767) on every node. LoadBalancer provisions a cloud load balancer that forwards to NodePort backends, providing a public IP on supported platforms.

## Related Tutorials

- [Kubernetes – Category Overview](index.md)
- [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md) *(previous)*
- [ConfigMaps and Secrets](configmaps-and-secrets.md) *(next)*
- [Ingress and External Access](ingress-and-external-access.md)
- [DNS Fundamentals](../networking/dns-fundamentals.md)
- [Load Balancing Fundamentals](../networking/load-balancing-fundamentals.md)

## References

- [Kubernetes Services documentation](https://kubernetes.io/docs/concepts/services-networking/service/)
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [kube-proxy documentation](https://kubernetes.io/docs/reference/networking/virtual-ips/)
- [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/)
