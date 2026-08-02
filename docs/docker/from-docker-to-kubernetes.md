---
title: From Docker to Kubernetes
description: Map Docker concepts to Kubernetes — containers to pods, docker run to Deployments, Compose to manifests, and services to kube Service objects.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: docker
tags:
  - docker
  - kubernetes
  - migration
  - pods
  - deployments
prerequisites:
  - Docker Swarm Orchestration Basics
  - Docker Compose Fundamentals
  - Production Docker Patterns
comments: false
---


# From Docker to Kubernetes

## Overview







If you understand Docker, you already know half of Kubernetes. Containers become **Pods**, `docker run` flags become **Pod specs**, Compose services become **Deployments** and **Services**, and Swarm overlay networks become **ClusterIP** routing. This tutorial builds a explicit concept map so you can read Kubernetes manifests confidently and migrate workloads incrementally.

This is **Tutorial 19** in **Module 6: Production & Beyond** of the REBASH Academy Docker track.

## Prerequisites







- [Docker Swarm Orchestration Basics](docker-swarm-orchestration-basics.md)
- [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- [Production Docker Patterns](production-docker-patterns.md)
- [Docker Networking Fundamentals](docker-networking-fundamentals.md)
- Optional: local cluster via [minikube](https://minikube.sigs.k8s.io/) or [kind](https://kind.sigs.k8s.io/)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Map Docker primitives to Kubernetes API objects
- [ ] Explain Pods, Deployments, Services, and Namespaces in Docker terms
- [ ] Translate a Compose file into equivalent Kubernetes manifests
- [ ] Understand how health checks, env vars, volumes, and secrets differ in K8s
- [ ] Plan an incremental migration path from Docker Compose to Kubernetes
- [ ] Know when to continue with the [Kubernetes track](../kubernetes/index.md)

## Architecture







![Production container platform](../assets/excalidraw/docker-production-platform.svg)

## Theory







### The big picture

| Docker mental model | Kubernetes equivalent |
|---------------------|----------------------|
| Container | Container inside a **Pod** |
| `docker run` | `kubectl run` or Pod manifest (prefer Deployment) |
| Image | Same OCI image — pulled from same registries |
| `docker compose` service | **Deployment** + **Service** (+ **Ingress**) |
| Bridge network | Pod network (CNI plugin) |
| `--publish 8080:80` | Service `type: NodePort/LoadBalancer` + Ingress |
| Named volume | **PersistentVolumeClaim** |
| Bind mount | `hostPath` or ConfigMap/Secret volume |
| Env file / `-e` | ConfigMap, Secret, or env in manifest |
| HEALTHCHECK | `livenessProbe`, `readinessProbe`, `startupProbe` |
| `--restart unless-stopped` | Deployment `restartPolicy: Always` |
| Swarm service | Deployment + Service |
| Swarm secret | Secret object |
| Swarm stack | Helm chart or Kustomize overlay |

Kubernetes adds a **control plane** that continuously reconciles desired state — similar to Swarm managers, but richer and ecosystem-backed.

### Pod — the atomic unit

A **Pod** is the smallest deployable unit in Kubernetes. Usually one Pod runs one primary container (sometimes sidecars share the network namespace).

Docker equivalent:

```bash
docker run -d --name api --network backend -e DB_HOST=db myapi:1.2.0
```

Kubernetes Pod (simplified):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: api
  labels:
    app: api
spec:
  containers:
    - name: api
      image: myapi:1.2.0
      env:
        - name: DB_HOST
          value: db
      ports:
        - containerPort: 3000
  restartPolicy: Always
```

!!! note "Do not deploy bare Pods in production"
    Pods are ephemeral. Use a **Deployment** (or StatefulSet for stable identity) to manage Pod lifecycle.

### Deployment — desired replica count and rollouts

A **Deployment** owns ReplicaSets and Pods. It provides scaling and rolling updates — the closest match to a Swarm **replicated service** or a Compose service with `deploy.replicas`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: registry.example.com/myapi:1.2.0
          ports:
            - containerPort: 3000
          resources:
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            periodSeconds: 5
```

| Deployment field | Docker/Swarm analog |
|------------------|---------------------|
| `replicas: 3` | `--replicas 3` / scale 3 |
| `strategy.rollingUpdate` | `docker service update --update-parallelism` |
| `resources.limits` | `--memory`, `--cpus` |
| Probes | HEALTHCHECK with separate liveness/readiness |

### Service — stable network identity

Pods get new IPs on restart. A **Service** provides a stable ClusterIP and DNS name (`api.default.svc.cluster.local`) that load-balances to healthy Pod endpoints.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
```

| Service type | Docker analog |
|--------------|---------------|
| **ClusterIP** | Internal overlay DNS (default) |
| **NodePort** | `--publish` on every node IP |
| **LoadBalancer** | Cloud LB in front of NodePort |
| **Ingress** | nginx/Traefik routing rules (no direct Docker equivalent) |

### Namespace — logical isolation

**Namespaces** partition objects (`dev`, `staging`, `prod`). Docker has no direct match — closest is separate Compose project names or Swarm stack names.

```bash
kubectl create namespace staging
kubectl get pods -n staging
```

### ConfigMap and Secret

| Docker | Kubernetes |
|--------|------------|
| `-e KEY=val` | env from ConfigMap/Secret |
| `--env-file` | ConfigMap keys |
| Swarm secret file | Secret volume mount |
| Bind mount config | ConfigMap volume |

### Volumes

| Docker | Kubernetes |
|--------|------------|
| Named volume | PersistentVolumeClaim |
| Bind mount | hostPath (avoid in prod), ConfigMap, emptyDir |
| tmpfs | emptyDir with medium: Memory |

```yaml
volumes:
  - name: data
    persistentVolumeClaim:
      claimName: postgres-pvc
containers:
  - name: db
    volumeMounts:
      - name: data
        mountPath: /var/lib/postgresql/data
```

### Health checks — three probes

Kubernetes improves on Docker's single HEALTHCHECK:

| Probe | Maps to | Failure action |
|-------|---------|----------------|
| **startupProbe** | Extended boot grace | Kill container if boot never succeeds |
| **livenessProbe** | Liveness HEALTHCHECK | Restart container |
| **readinessProbe** | Readiness check | Remove from Service endpoints |

See [Production Docker Patterns](production-docker-patterns.md) for probe design principles.


### Translate intent, not flags

A naïve Compose-to-Kubernetes conversion that copies `privileged`, host mounts, and published ports will recreate the same risks at larger blast radius. Map services to Deployments, ports to Services/Ingress, env files to ConfigMaps/Secrets, and healthchecks to probes — then apply Pod Security and NetworkPolicies. Keep image digests identical across the migration so you debug orchestration differences, not application drift.


### Practice mindset

As you work through this tutorial, narrate *why* each control or command exists — not only *how* to type it. Production incidents are rarely solved by memorising flags; they are solved by connecting symptoms to the architecture (daemon vs kubelet, image vs running container, Service vs Endpoints, volume vs writable layer). After the lab, write three bullet notes in your own words: what you verified, what would break in production if skipped, and what you would monitor next.


### Connecting the lab to production reviews

When a teammate asks “is this ready?”, answer with evidence from this tutorial’s controls: image provenance, privilege level, network exposure, health signals, and teardown/rollback. Copy-pasting a working lab snippet into production without those answers is how quiet misconfigurations become incidents. Prefer small, reviewable changes — one Dockerfile improvement, one RBAC binding, one probe — over large untested stacks.

### Observability while you learn

Get into the habit of watching state while commands run: `docker events` / `kubectl get events`, resource usage, and logs in a second pane. Many failures are timing issues (probes, readiness, volume attach) that disappear if you only look at the final steady state. Capturing a short timeline of what you saw will also make your Troubleshooting section notes far more valuable later.


### Checklist before you leave the lab

1. Resources created in this tutorial are deleted or clearly labelled for retention.
2. No secrets, kubeconfigs, or registry passwords were written into Git.
3. You can explain the Architecture diagram without reading the caption.
4. Validation pass criteria in this page are satisfied on your machine.
5. You noted one question to revisit in the next tutorial of the series.

### Common production failure modes this topic prevents

Misconfiguration here usually shows up as intermittent outages rather than clean errors: restart loops without log shipping, services that listen but never become Ready, volumes that work on one node only, or credentials that leak into image history. Use the Hands-on Lab as a rehearsal for the failure mode — break something on purpose, watch the signal, then apply the fix documented in Troubleshooting.

## Hands-on Lab



### Objective

Build or run a real Docker solution for **From Docker to Kubernetes** and prove it with inspect/logs/HTTP.

### Prerequisites

- Docker Engine or Docker Desktop
- Permission to run containers

### Lab environment

Workspace: `~/rebash-docker/from-docker-to-kubernetes`

Local Docker daemon. Clean up containers/images after the lab.

```bash
mkdir -p ~/rebash-docker/from-docker-to-kubernetes && cd ~/rebash-docker/from-docker-to-kubernetes
```

### Real-world scenario

You are validating **From Docker to Kubernetes** before it lands in CI. The change must be reproducible with copy-paste commands and leave no orphan containers.

### Step-by-step tasks

#### Task 1 – Run and inspect a container

Start from a known image, publish a port, and verify HTTP.

```bash
docker run -d --name rebash-lab -p 18080:80 nginx:alpine
docker ps --filter name=rebash-lab
curl -sI http://127.0.0.1:18080 | head -n 5 | tee headers.txt
docker logs rebash-lab 2>&1 | head -n 10 | tee logs.txt
```

**Expected output:** Container Up; HTTP 200 in headers.txt.

#### Task 2 – Inspect runtime config

Use inspect for status — production debugging rarely starts with guesswork.

```bash
docker inspect rebash-lab --format '{{ "{{" }}.State.Status{{ "}}" }} {{ "{{" }}.Config.Image{{ "}}" }}' | tee inspect.txt
test -s inspect.txt
```

**Expected output:** inspect.txt shows `running` and the nginx image.

### Validation steps

- [ ] Container or image behaves as Expected output describes
- [ ] Ports respond or command output matches
- [ ] Cleanup removes lab resources

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| port is already allocated | Previous lab left a container | `docker rm -f` the old name or change port |
| permission denied | User not in docker group | Use rootless Docker or fix group membership |
| manifest unknown | Bad tag | Pin a real tag such as `nginx:alpine` |

### Challenge exercise

Add a non-root USER (or Compose healthcheck) and prove it with inspect.

### Learning outcomes

- Executed a real Docker workflow
- Captured evidence files
- Removed disposable resources

### Cleanup

```bash
docker rm -f rebash-lab 2>/dev/null || true
docker rmi rebash-lab:local 2>/dev/null || true
docker compose down -v 2>/dev/null || true
```

## Validation







Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Mapping | You produced Deployment/Service YAML equivalent to the Compose services |
| Probes | Healthcheck mapped to a probe (or documented deliberate difference) |
| Config/secret | Env/volume concerns mapped to ConfigMap/Secret/Volume patterns |
| Review | You listed at least two security differences Compose→Kubernetes |

## Code Walkthrough







### kubectl ↔ docker cheat sheet

| Operation | Docker | Kubernetes |
|-----------|--------|------------|
| List running | `docker ps` | `kubectl get pods` |
| Logs | `docker logs CONTAINER` | `kubectl logs POD` |
| Exec shell | `docker exec -it C sh` | `kubectl exec -it POD -- sh` |
| Inspect | `docker inspect C` | `kubectl describe pod POD` |
| Remove | `docker rm -f C` | `kubectl delete pod POD` |
| Scale | `docker service scale` | `kubectl scale deployment D --replicas=5` |
| Update image | `docker service update --image` | `kubectl set image deployment/D c=img:tag` |
| Rollout status | service ps | `kubectl rollout status deployment/D` |
| Rollback | service rollback | `kubectl rollout undo deployment/D` |

Ingress replaces manual nginx routing in Compose stacks — see the [Kubernetes track](../kubernetes/index.md).

## Security Considerations







- Do not translate Compose `privileged: true` or host mounts into Kubernetes without a security review
- Map Compose secrets to Kubernetes Secrets or an external secret store — not plain ConfigMaps
- Replace host port publishes with Services/Ingress and network policies
- Keep image digests stable across the migration so you are not debugging two variables at once
- Apply Pod Security standards early; “it worked in Compose” is not a security model
- Limit kubeconfig privileges used during migration labs to a dedicated namespace

## Common Mistakes







!!! warning "Running one Pod per deployment without probes"
    Silent failures stay in load rotation. Port Docker HEALTHCHECK to liveness and readiness probes.

!!! warning "Using latest tag in manifests"
    Same anti-pattern as Docker — pin SHA or semver; use imagePullPolicy: IfNotPresent thoughtfully.

!!! warning "Lift-and-shift stateful containers as Deployments"
    Postgres in a Deployment loses data on reschedule. Use StatefulSet + PVC + backup.

!!! warning "Assuming kubectl apply from laptop is production CD"
    Use CI/CD or GitOps — same lesson as [Docker in CI/CD Pipelines](docker-in-ci-cd-pipelines.md).

!!! warning "Ignoring resource requests"
    Without requests, scheduler overcommits nodes — worse than missing Docker `--memory` limits.

## Best Practices







!!! tip "Migrate stateless services first"
    API, workers, frontends — then tackle databases with proper operators.

!!! tip "Keep images unchanged"
    Kubernetes runs the same OCI images you built for Docker — reuse CI pipelines.

!!! tip "Use Helm or Kustomize for environments"
    Like Compose overrides — base chart + staging/prod values.

!!! tip "Learn one local cluster tool"
    kind or minikube plus kubectl beats Docker Desktop alone for K8s-specific learning.

!!! tip "Continue on the Kubernetes track"
    This tutorial maps concepts — [Kubernetes](../kubernetes/index.md) tutorials go deep on operations.

## Troubleshooting







| Issue | Cause | Solution |
|-------|-------|----------|
| ImagePullBackOff | Private registry auth | imagePullSecrets |
| CrashLoopBackOff | App exits on boot | kubectl logs; fix config |
| Pod pending | Insufficient resources | Check requests; add nodes |
| Service no traffic | Selector mismatch | Labels on Pod template must match Service selector |
| Probe failures | Wrong port/path | Align with HEALTHCHECK from Docker image |
| PVC pending | No storage class | Define StorageClass or use hostPath in lab only |

## Summary







- **Pods** wrap containers; **Deployments** manage replica count and rollouts (like Swarm services)
- **Services** provide stable DNS and load balancing (like overlay service names + VIP)
- **ConfigMaps/Secrets**, **PVCs**, and **probes** map directly from Compose and Dockerfile patterns
- Migration is incremental: same images, new orchestration API, stronger production primitives
- Continue learning on the [Kubernetes track](../kubernetes/index.md)
- Finish the Docker series with [Docker Capstone and Next Steps](docker-capstone-and-next-steps.md)

## Interview Questions




1. Map Docker run flags to Kubernetes fields.
2. Why isn't Compose a production orchestrator for most enterprises?
3. What stays the same when moving images to Kubernetes?
4. How do probes differ from Docker HEALTHCHECK?
5. What operational skills transfer directly?

!!! tip "Sample answer — question 2"
    Compare the working docker run/compose config to Deployment/Service YAML. Client dry-run catches API mistakes early.

!!! tip "Sample answer — question 4"
    Keep image supply-chain controls; move secrets to Kubernetes Secret/CSI providers.

## Related Tutorials







- [Docker Swarm Orchestration Basics](docker-swarm-orchestration-basics.md) *(previous)*
- [Docker Capstone and Next Steps](docker-capstone-and-next-steps.md) *(next)*
- [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- [Production Docker Patterns](production-docker-patterns.md)
- [Kubernetes – Category Overview](../kubernetes/index.md)
- [Docker – Category Overview](index.md)
- Cheat sheet: [Docker Cheat Sheet](../cheatsheets/docker.md)
- Interview prep: [Docker Interview Prep](../interview/docker.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References







- [Kubernetes – Concepts](https://kubernetes.io/docs/concepts/)
- [Kubernetes – Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Kubernetes – Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes – Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Kompose – User guide](https://kompose.io/user-guide/)
- [CNCF – Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) *(advanced)*
