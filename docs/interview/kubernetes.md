---
title: "Kubernetes Interview Preparation"
description: "59 curated Kubernetes interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: kubernetes
tags:
  - interview
  - kubernetes
comments: false
---

{% raw %}
# Kubernetes Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. What is a Pod, Deployment, and Service in Kubernetes?**

??? success "Reveal answer"
    **In short:** A Pod is the smallest deployable unit; a Deployment manages replicas and rollouts; a Service gives stable networking to Pods.
    
    **Key points**
    - Pods share network/storage and schedule together on one node—rarely created naked in production.
    - Deployments own ReplicaSets for declarative rollouts and rollbacks.
    - Services select Pods by labels and provide ClusterIP/DNS load balancing.
    - Day-to-day: deploy apps with Deployments, expose with Services (and Ingress for HTTP).
    
    **Try this**
    - `kubectl get pods,deploy,svc -o wide`
    - `kubectl rollout status deploy/<name>`
    
    **Trap**
    - Exposing a Pod IP directly ignores churn when the Pod is rescheduled.

**2. What is a ConfigMap and Secret in Kubernetes?**

??? success "Reveal answer"
    **In short:** ConfigMaps hold non-sensitive config; Secrets hold sensitive material—both inject as env or files into Pods.
    
    **Key points**
    - ConfigMaps: feature flags, config files, non-secret env.
    - Secrets are base64 in the API by default—not strong encryption at rest unless configured.
    - Prefer file mounts over env for secrets to reduce accidental leakage in process listings.
    - Externalise real secret storage with Sealed Secrets, SOPS, External Secrets, or Vault.
    
    **Try this**
    - `kubectl create configmap app-config --from-literal=LOG_LEVEL=info`
    - `kubectl get secret`
    
    **Trap**
    - Committing live Secret YAML to Git is a classic breach path.

**3. What is a Kubernetes Ingress, and how does it differ from a LoadBalancer Service?**

??? success "Reveal answer"
    **In short:** Ingress routes HTTP/HTTPS by host and path; a LoadBalancer Service asks the cloud for an L4 (usually) load balancer per Service.
    
    **Key points**
    - Ingress needs a controller (NGINX, cloud LB controller, Traefik, Gateway API).
    - One Ingress can multiplex many Services on shared VIP/TLS.
    - LoadBalancer is simpler for TCP/UDP or single-service exposure.
    - Troubleshoot controller logs, Ingress events, and backend EndpointSlices.
    
    **Try this**
    - `kubectl describe ingress <name>`
    - `kubectl get svc,ingress`
    
    **Trap**
    - Annotation dialects differ by controller—copying YAML between clusters often breaks TLS or paths.

**4. What is Argo CD, and how does it implement GitOps for Kubernetes deployments?**

??? success "Reveal answer"
    **In short:** Argo CD continuously reconciles Kubernetes live state to desired manifests in Git (GitOps).
    
    **Key points**
    - Desired state lives in Git as YAML, Helm, or Kustomize.
    - Detects drift and syncs manually or automatically.
    - RBAC, SSO, and project isolation matter for multi-team use.
    - Rollbacks are Git reverts (or sync to a prior revision), not ad-hoc kubectl edits.
    
    **Try this**
    - `kubectl get application -n argocd`
    - `argocd app get <app>`
    
    **Trap**
    - Clicking sync while someone force-pushes main can deploy unintended commits—pin revisions in prod apps.

**5. What is Vault by HashiCorp, and how does it integrate with Kubernetes for secrets management?**

??? success "Reveal answer"
    **In short:** Vault centralises secrets and dynamic credentials; on Kubernetes, inject short-lived secrets instead of stuffing etcd.
    
    **Key points**
    - Common patterns: Agent Injector, Secrets Store CSI, or External Secrets Operator.
    - Apps read from a memory volume or env populated at runtime.
    - Kubernetes auth binds ServiceAccount identities to Vault roles.
    - Enable audit devices and rotate anything long-lived.
    
    **Try this**
    - `kubectl get pods -n vault`
    - `vault status`
    
    **Trap**
    - Copying Vault secrets into Kubernetes Secret objects long-term recreates the problem Vault solved.

**6. Explain how you've set up a Kubernetes cluster.**

??? success "Reveal answer"
    **In short:** I create clusters as Infrastructure as Code—managed control plane, multi-AZ nodes, then baseline add-ons.
    
    **Key points**
    - Prefer EKS/AKS/GKE via Terraform for control plane, networking, and node pools.
    - Add CNI, metrics-server, ingress, autoscaler, and GitOps early.
    - Separate system and workload node pools; private API when required.
    - For labs only: kubeadm init/join with explicit networking and certificates plan.
    
    **Try this**
    - `kubectl get nodes -o wide`
    - `kubectl get pods -A`
    
    **Trap**
    - Hand-built “pet” control planes without backups or IaC become unrecoverable snowflakes.

**7. What are some safe deployment strategies?**

??? success "Reveal answer"
    **In short:** Prefer rolling updates with readiness, plus blue/green or canary when you need safer cutovers gated on metrics.
    
    **Key points**
    - RollingUpdate + readiness keeps traffic on healthy Pods.
    - Blue/green switches at Service/Ingress once green is healthy.
    - Canary/progressive delivery (Argo Rollouts/Flagger) shifts a small percentage first.
    - Always plan backward-compatible migrations and automated rollback criteria.
    
    **Try this**
    - `kubectl rollout status deploy/<name>`
    - `kubectl get rs`
    
    **Trap**
    - Recreate strategy for user-facing APIs causes downtime unless explicitly accepted.

**8. What are Kubernetes services, and how do they differ from Pods?**

??? success "Reveal answer"
    **In short:** Pods are mortal workloads with changing IPs; Services provide stable virtual IPs/DNS across Ready endpoints.
    
    **Key points**
    - Label selectors bind Services to Pods.
    - Empty Endpoints mean labels/selectors or readiness failed—not “DNS is down” first.
    - ClusterIP is internal; NodePort/LoadBalancer/Ingress expose externally.
    - Clients should target Service DNS, never Pod IPs.
    
    **Try this**
    - `kubectl get svc,endpointslice`
    - `kubectl get pods --show-labels`
    
    **Trap**
    - A Service with mismatched labels silently load-balances to nothing.

**9. What is Kubernetes, and how does it help in container orchestration?**

??? success "Reveal answer"
    **In short:** Kubernetes is an open-source orchestrator that schedules containers, heals failures, scales, and rolls out desired state.
    
    **Key points**
    - You declare desired state; controllers reconcile toward it via the API server.
    - Replaces SSH snowflake hosts with declarative workloads.
    - Provides Service discovery, config injection, and rolling updates as primitives.
    - You still own app design, networking policy, and day-2 operations.
    
    **Try this**
    - `kubectl api-resources | head`
    - `kubectl get --raw='/readyz?verbose'`
    
    **Trap**
    - Calling Kubernetes “just Docker on many machines” undersells scheduling, desired-state, and extensibility.

**10. Explain the difference between a Deployment and a StatefulSet in Kubernetes.**

??? success "Reveal answer"
    **In short:** Deployments suit stateless interchangeable replicas; StatefulSets add stable identity, ordered ops, and per-ordinal PVCs.
    
    **Key points**
    - Deployments: RollingUpdate, no sticky pod names required.
    - StatefulSets: pod-0..N identity, volumeClaimTemplates, ordered scale/deploy.
    - Use StatefulSets for clustered datastores that need stable network IDs.
    - New ordinals get empty PVCs unless the app replicates data itself.
    
    **Try this**
    - `kubectl get sts,pvc,pods`
    
    **Trap**
    - HPA on a StatefulSet does not clone data into new PVCs—empty disks surprise people.

## Scenarios and troubleshooting

**11. How do you implement zero-downtime deployments on ECS Fargate with a production traffic cutover strategy?**

??? success "Reveal answer"
    **In short:** On ECS Fargate, use CodeDeploy blue/green with an ALB: healthy green targets, weighted shift, then drain blue.
    
    **Key points**
    - New task definition registers to a green target group first.
    - Require passing target health checks before shifting traffic.
    - Set deregistration delay for in-flight requests; keep migrations backward-compatible.
    - Rollback redirects traffic to blue; secrets from Secrets Manager/SSM, not baked images.
    
    **Try this**
    - `aws ecs describe-services --cluster <c> --services <s>`
    
    **Trap**
    - Cutting 100% traffic before green is healthy creates an instant outage with a fancy name.

**12. How do you deploy the ELK stack on Kubernetes for production log aggregation?**

??? success "Reveal answer"
    **In short:** Ship logs with a node agent DaemonSet into OpenSearch/Elasticsearch+Kibana—or prefer managed OpenSearch/Loki to cut toil.
    
    **Key points**
    - Apps log to stdout; Fluent Bit/Fluentd collect and forward.
    - Pin resources; isolate data nodes; set ILM/retention; enable TLS/RBAC.
    - Watch disk pressure and agent gaps when logs look “incomplete”.
    - Avoid kubectl exec as your primary logging strategy.
    
    **Try this**
    - `kubectl get ds -A | grep -i fluent`
    - `kubectl logs -n <ns> <pod>`
    
    **Trap**
    - Self-managing huge Elasticsearch clusters without retention policies is how logging becomes the outage.

**13. Describe a real production incident where a misconfigured HPA caused cascading failure. How would you redesign autoscaling to avoid this?**

??? success "Reveal answer"
    **In short:** A bad HPA can stampede replicas on noisy CPU, crush dependencies, exhaust IPs/nodes, and amplify latency into a cascade.
    
    **Key points**
    - Scale on saturation signals (RPS capacity, concurrency, queue depth), not GC blips alone.
    - Set sensible min/max, stabilisation windows, and rate limits on scale-up/down.
    - Protect dependencies with bulkheads, timeouts, and connection pools.
    - Use PDBs so scale-down and drains do not breach availability.
    
    **Try this**
    - `kubectl get hpa`
    - `kubectl describe hpa <name>`
    
    **Trap**
    - maxReplicas set to “something huge” without cluster capacity planning recreates the incident.

**14. How would you design a Kubernetes cluster that must survive a full AZ failure without data loss, while running stateful workloads at scale?**

??? success "Reveal answer"
    **In short:** Survive AZ loss with regional multi-AZ control plane/nodes, topology spread, and storage/data replication that tolerates zone failure.
    
    **Key points**
    - Spread replicas with topology spread / anti-affinity across zones.
    - Prefer storage that replicates across AZs or DB quorum that can lose one zone.
    - Watch RWO volume zone affinity—failover may need attach in another zone.
    - Test zone loss drills; do not assume regional API equals durable app data.
    
    **Try this**
    - `kubectl get pods -o wide`
    - `kubectl get pv,pvc`
    
    **Trap**
    - Single-AZ node groups with “replicas: 3” still die together when that AZ fails.

**15. How do you rollback a failed deployment in production?**

??? success "Reveal answer"
    **In short:** Roll back by reverting to a known-good revision—kubectl rollout undo, Helm rollback, or GitOps sync to prior commit/digest.
    
    **Key points**
    - Confirm Ready replicas and golden signals after rollback.
    - Prefer previous image digest over rebuilding under pressure.
    - Database migrations must be backward-compatible or you need a forward fix.
    - Capture timeline and change ID for the incident review.
    
    **Try this**
    - `kubectl rollout undo deploy/<name>`
    - `kubectl rollout history deploy/<name>`
    - `helm rollback <release> <revision>`
    
    **Trap**
    - Rolling back the app while leaving a breaking schema migration in place keeps the outage alive.

**16. How do you approach the debug on the deployment failure?**

??? success "Reveal answer"
    **In short:** Define the failure, check rollout status, then inspect new Pods with describe/logs before changing more than one variable.
    
    **Key points**
    - Stuck rollout vs Ready-but-bad-traffic need different paths.
    - Validate image digest, probes, resources, config/secrets, RBAC, webhooks.
    - Compare to last healthy ReplicaSet/revision.
    - Decide quickly: fix-forward vs rollback based on blast radius and evidence.
    
    **Try this**
    - `kubectl rollout status deploy/<name>`
    - `kubectl describe pod <pod>`
    - `kubectl logs <pod> --previous`
    
    **Trap**
    - Deleting random Pods without reading events often destroys evidence.

**17. U handled any debug/troubleshoot for kubernetes?**

??? success "Reveal answer"
    **In short:** Yes—most Kubernetes debug work is Pod/node lifecycle, networking, and rollout failures using describe, logs, and events.
    
    **Key points**
    - Start with kubectl get/describe/events before changing manifests.
    - Separate app bugs from cluster issues (NotReady nodes, CNI, DNS).
    - Use previous logs for CrashLoopBackOff.
    - Close the loop with a prevention change (probe, resources, PDB, alert).
    
    **Try this**
    - `kubectl get events --sort-by=.lastTimestamp`
    - `kubectl top pods`
    
    **Trap**
    - Jumping straight to restarting the whole node for one bad Pod is a junior reflex.

**18. Tell me about a time you handled a failed deployment in production. How did you manage the team and stakeholders?**

??? success "Reveal answer"
    **In short:** I stabilise first (rollback or disable traffic), communicate impact and ETA, then fix with a single owner and a clear go/no-go.
    
    **Key points**
    - Mitigate user impact before deep root-cause theatre.
    - Give stakeholders factual status: impact, next update time, owner.
    - Keep a tight change window—one hypothesis at a time.
    - Run a blameless review with action items (tests, progressive delivery, alerts).
    
    **Try this**
    - `kubectl rollout undo deploy/<name>`
    - `kubectl get pods -w`
    
    **Trap**
    - Silent Slack threads without an incident channel leave leaders inventing their own narrative.

**19. How to troubleshoot if pod is failed in AKS, commands please?**

??? success "Reveal answer"
    **In short:** On AKS, treat a failed Pod like any Kubernetes Pod—namespace events, describe, logs—then check Azure node/CNI/pull identity if cluster-level.
    
    **Key points**
    - kubectl describe pod and kubectl logs (--previous) first.
    - Check image pull (ACR auth/identity), probes, and resource quotas.
    - Node NotReady: kubectl describe node plus Azure activity/VMSS health.
    - Confirm subnet IP exhaustion and CNI plugin status on AKS.
    
    **Try this**
    - `kubectl describe pod <pod> -n <ns>`
    - `kubectl logs <pod> -n <ns> --previous`
    - `kubectl get nodes -o wide`
    
    **Trap**
    - Azure Portal graphs without Pod events usually miss ImagePullBackOff and probe failures.

**20. Logs are incomplete — how would you troubleshoot across AKS, Ingress, App, and Infra?**

??? success "Reveal answer"
    **In short:** Incomplete logs mean collection gaps—verify app stdout, node agents, Ingress access logs, and time ranges before blaming “AKS lost logs”.
    
    **Key points**
    - Confirm the Pod logged to stdout and was not OOM-killed mid-request.
    - Check Fluent Bit/OMS agent DaemonSet health and disk pressure.
    - Compare Ingress/controller logs with app logs for the same request ID.
    - Align UTC time windows and retention/ILM settings.
    
    **Try this**
    - `kubectl logs -n <ns> <pod> --since=1h`
    - `kubectl get ds -A`
    
    **Trap**
    - Searching only the wrong index/time zone creates false “missing log” incidents.

**21. When designing a microservices-oriented infrastructure, what technologies and components (like load balancer, service mesh, Kubernetes) would you bring in, and how would you design the estate?**

??? success "Reveal answer"
    **In short:** For microservices, use Kubernetes for scheduling, an Ingress/Gateway for north-south, and add a mesh only when east-west policy and observability demand it.
    
    **Key points**
    - Baseline: Deployments, Services, Ingress/Gateway, HPA, observability, GitOps.
    - Load balancers at the edge; NetworkPolicies for namespace isolation.
    - Service mesh (Istio/Linkerd) when you need mTLS, traffic shaping, and rich telemetry at scale.
    - Externalise data stores; standardise platform golden paths for teams.
    
    **Try this**
    - `kubectl get gateway,ingress,svc -A`
    
    **Trap**
    - Bolting on a mesh before you have basics (probes, SLOs, CI) multiplies operational load.

**22. How would you design container images for ultra-fast cold starts in serverless or autoscaled Kubernetes environments?**

??? success "Reveal answer"
    **In short:** Fast cold starts need tiny images, minimal startup work, and readiness that becomes true quickly.
    
    **Key points**
    - Distroless/static binaries; multi-stage; avoid huge JVM defaults without tuning.
    - Lazy-load non-critical deps; cache wisely; skip unnecessary migrations at boot.
    - Set resources so the scheduler places Pods quickly; use startup probes for slow boots.
    - Prefer ready-first over “perfect warm” for scale-from-zero paths.
    
    **Try this**
    - `docker history <image>`
    - `kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].ready}'`
    
    **Trap**
    - Giant images plus eager classloading make autoscaling amplify latency under load spikes.

**23. If your pod is in Pending state, then what are your troubleshoot steps?**

??? success "Reveal answer"
    **In short:** Pending means the scheduler has not placed the Pod—check events for resources, taints, PVC, or quota blockers.
    
    **Key points**
    - kubectl describe pod Events is the source of truth.
    - Common causes: insufficient CPU/memory, taints/tolerations, node selectors/affinity.
    - Unbound PVCs and missing StorageClass also keep Pods Pending.
    - ResourceQuota/LimitRange can deny the Pod silently until you read events.
    
    **Try this**
    - `kubectl describe pod <pod>`
    - `kubectl get pvc,nodes`
    
    **Trap**
    - Deleting and recreating a Pending Pod without reading events often loops forever.

**24. If you have a Kubernetes cluster with pods running, but when you hit the URL you get HTTP errors (403, 404, 503), what would be your troubleshooting steps?**

??? success "Reveal answer"
    **In short:** HTTP 403/404/503 with healthy-looking Pods usually means Ingress/Service/path or readiness—not “Kubernetes is down”.
    
    **Key points**
    - 403: auth/WAF/Ingress annotation or NetworkPolicy deny.
    - 404: wrong host/path rewrite or Service backend mapping.
    - 503: no Ready endpoints, probe failures, or upstream overload.
    - Trace curl from outside → Ingress → Service → Pod, checking EndpointSlices.
    
    **Try this**
    - `kubectl get ingress,svc,endpointslice`
    - `kubectl describe ingress <name>`
    - `kubectl get pods -l <selector>`
    
    **Trap**
    - Fixing the Deployment image when Ingress path rules are wrong wastes the incident clock.

**25. When kubernetes node fails what will happen?**

??? success "Reveal answer"
    **In short:** When a node fails, the control plane marks it NotReady and eventually reschedules Pods that can run elsewhere—subject to PVCs and DaemonSets.
    
    **Key points**
    - Pods on the dead node become Unreachable/Unknown then get replaced if controllers exist.
    - DaemonSets cannot reschedule that node’s copy until the node returns.
    - RWO volumes may stay attached to the failed node until timeout/detach.
    - PDBs and replicas determine user-visible impact.
    
    **Try this**
    - `kubectl get nodes`
    - `kubectl get pods -A -o wide --field-selector spec.nodeName=<node>`
    
    **Trap**
    - Assuming StatefulSet Pods instantly appear elsewhere ignores volume attach delays.

**26. If you pod is not running, how do you troubleshoot it?**

??? success "Reveal answer"
    **In short:** If a Pod is not running, classify the phase (Pending, CrashLoop, ImagePull, etc.) and follow describe/logs for that class.
    
    **Key points**
    - Pending → scheduling/PVC/quota.
    - ImagePullBackOff → registry auth/tag/digest.
    - CrashLoopBackOff → app exit; use logs --previous.
    - Running but not Ready → readiness probes/dependencies.
    
    **Try this**
    - `kubectl get pod <pod> -o yaml`
    - `kubectl describe pod <pod>`
    - `kubectl logs <pod> --previous`
    
    **Trap**
    - One generic “restart the Pod” step without phase classification hides the real fault.

**27. If there a deployment failure what the next steps you perform?**

??? success "Reveal answer"
    **In short:** On deployment failure: stop the bleed (rollback if needed), gather evidence, fix one cause, then re-roll with validation.
    
    **Key points**
    - Check rollout status and Pod events first.
    - Rollback if user impact is high and the prior revision is trusted.
    - Fix probes, image, config, or resources based on evidence.
    - Verify Ready replicas and synthetic checks before calling success.
    
    **Try this**
    - `kubectl rollout status deploy/<name>`
    - `kubectl rollout undo deploy/<name>`
    
    **Trap**
    - Pushing “just one more hotfix” without undo criteria extends the outage.

**28. I have an Ingress object that is not routing the traffic to the Kubernetes cluster. What are the reasons and how do you troubleshoot that?**

??? success "Reveal answer"
    **In short:** Ingress not routing is usually controller, class, DNS, TLS, Service selector, or path mismatch—not a mystery kube-proxy bug first.
    
    **Key points**
    - Confirm an IngressClass/controller is running and watching the object.
    - Check host/DNS and TLS secret validity.
    - Verify backend Service has Ready endpoints.
    - Compare path/prefix rules and annotations for your controller.
    
    **Try this**
    - `kubectl describe ingress <name>`
    - `kubectl logs -n <ingress-ns> deploy/<controller>`
    - `kubectl get endpointslice`
    
    **Trap**
    - Creating Ingress YAML without installing a controller leaves Address empty forever.

**29. I have created a service object that is not mapped to a deployment. What could be the reason and how do you debug it?**

??? success "Reveal answer"
    **In short:** A Service “not mapped” to a Deployment almost always means label selector mismatch—or the Pods are never Ready.
    
    **Key points**
    - Compare Service selector to Pod labels exactly.
    - Wrong namespace is a frequent miss.
    - Empty EndpointSlices confirm nothing is selected/Ready.
    - Deployments do not auto-wire Services—you must align labels.
    
    **Try this**
    - `kubectl get svc <svc> -o yaml`
    - `kubectl get pods --show-labels`
    - `kubectl get endpointslice -l kubernetes.io/service-name=<svc>`
    
    **Trap**
    - Renaming a label in the Deployment template without updating the Service selector silently blackholes traffic.

**30. In Kubernetes, if a pod is in a pending state, how do you troubleshoot?**

??? success "Reveal answer"
    **In short:** Pending troubleshooting is event-driven: resources, affinity/taints, PVCs, and quotas—same as any Pending Pod investigation.
    
    **Key points**
    - Read describe Events top to bottom.
    - kubectl describe node for pressure/taints if FailedScheduling mentions them.
    - Check PVC binding and StorageClass provisioner errors.
    - Confirm the cluster has schedulable capacity in the target zone/pool.
    
    **Try this**
    - `kubectl describe pod <pod>`
    - `kubectl get events --field-selector involvedObject.name=<pod>`
    
    **Trap**
    - Raising replicas while Pending usually multiplies Pending Pods, not capacity.

**31. Database connection from a pod is not working only for you. How will you troubleshoot?**

??? success "Reveal answer"
    **In short:** If only your Pod cannot reach the database, compare network path, credentials, and DNS with a working Pod in the same namespace.
    
    **Key points**
    - Exec and test DNS (db hostname) plus TCP connect to DB port.
    - Check NetworkPolicies and cloud security groups/NACLs for your Pod IP/namespace.
    - Verify Secret/config values and DB allowlists.
    - Confirm you are not on a different namespace/VPC path than teammates.
    
    **Try this**
    - `kubectl exec -it <pod> -- nslookup <db-host>`
    - `kubectl exec -it <pod> -- nc -vz <db-host> 5432`
    
    **Trap**
    - Rotating a DB password in one Secret while your Deployment still mounts an old key looks like “random network failure”.

**32. How will you investigate POD failure?**

??? success "Reveal answer"
    **In short:** Investigate Pod failure by phase, last termination reason, logs, and node health—then fix the specific cause.
    
    **Key points**
    - kubectl describe for Events and Last State (OOMKilled, Error, Completed).
    - logs / logs --previous for crash loops.
    - Check probes, resources, and image digest drift.
    - If many Pods fail together, suspect node, CNI, or bad shared config rollout.
    
    **Try this**
    - `kubectl describe pod <pod>`
    - `kubectl logs <pod> --previous`
    - `kubectl get pod <pod> -o jsonpath='{.status.containerStatuses}'`
    
    **Trap**
    - Ignoring OOMKilled and only “adding retries” guarantees the next memory spike.

**33. How do you handle deployment failures?**

??? success "Reveal answer"
    **In short:** Handle deployment failures with mitigate → diagnose → fix/rollback → verify → prevent.
    
    **Key points**
    - Mitigate: undo rollout or pause progressive delivery.
    - Diagnose with rollout history, Pod events, and metrics.
    - Ship a forward fix only when rollback is unsafe (migrations).
    - Add a gate (smoke test, canary metric) so the same break cannot ship silently.
    
    **Try this**
    - `kubectl rollout history deploy/<name>`
    - `kubectl rollout undo deploy/<name>`
    
    **Trap**
    - Leaving a failed Deployment at 50% unavailable without PDB awareness can violate SLOs during node drains.

**34. How did you troubleshoot the pod crashback loop?**

??? success "Reveal answer"
    **In short:** CrashLoopBackOff means the container starts then exits—read --previous logs and Last State, not only the current empty log stream.
    
    **Key points**
    - Exit code and OOMKilled tell you crash vs kill.
    - Common causes: bad config, missing migrations, failing startup command, probe mis-set as liveness too early.
    - Fix config/image or adjust startup/liveness probes.
    - Confirm stable Ready after a controlled rollout.
    
    **Try this**
    - `kubectl logs <pod> --previous`
    - `kubectl describe pod <pod>`
    
    **Trap**
    - Lengthening liveness failure thresholds forever hides a process that never actually becomes healthy.

**35. You have a Kubernetes cluster with 30 nodes. 29 nodes are Ready, but 1 node is NotReady. You have already checked kubectl logs, kubectl describe, and other basic commands. How will you troubleshoot the node further?**

??? success "Reveal answer"
    **In short:** After basic kubectl, dig into node OS/runtime: kubelet logs, container runtime, disk/memory pressure, and cloud instance health.
    
    **Key points**
    - systemctl status kubelet; journalctl -u kubelet on the node (or SSM/serial console).
    - Check disk full on /var/lib/containerd or /var/log.
    - crictl/ps for runtime hung pulls; CNI IP exhaustion.
    - Cloud side: VM NotReady, failed node upgrade, or network interface issues.
    
    **Try this**
    - `kubectl describe node <node>`
    - `journalctl -u kubelet -n 200 --no-pager`
    - `df -h`
    
    **Trap**
    - Cordon/drain the last healthy capacity before you understand why the node died.

**36. Describe your approach to troubleshooting Kubernetes worker node issues beyond the basic kubectl commands?**

??? success "Reveal answer"
    **In short:** Beyond kubectl, use node SSH/SSM, kubelet/runtime logs, CNI checks, and provider APIs to find NotReady root causes.
    
    **Key points**
    - Classify: kubelet down, runtime down, network NotReady, disk pressure, PID pressure.
    - Inspect CNI pods and routes; verify clock skew for certs.
    - Correlate with autoscaler replacements and spot interruptions.
    - Automate node problem detector alerts so this is not tribal knowledge.
    
    **Try this**
    - `kubectl get node <node> -o yaml`
    - `crictl info`
    
    **Trap**
    - Rebooting nodes as step one destroys forensic evidence and can thrash the autoscaler.

**37. How do you debug intermittent pod restarts when liveness probes pass, readiness passes, but the pod is still killed by the node?**

??? success "Reveal answer"
    **In short:** If probes pass but the Pod still dies, suspect node OOM/eviction, disk pressure, preemption, or external kill—not the liveness handler.
    
    **Key points**
    - Check kubectl describe for Reason=Evicted/OOMKilled and node conditions.
    - kubectl get events on the node; dmesg/OOM killer on the host.
    - Priority/preemption and spot reclaim can kill healthy Pods.
    - Confirm cgroup memory vs process RSS; adjust requests/limits honestly.
    
    **Try this**
    - `kubectl describe pod <pod>`
    - `kubectl get events --field-selector involvedObject.kind=Node`
    
    **Trap**
    - Raising liveness delay does nothing when the kubelet is evicting for disk pressure.

**38. In a multi-cloud environment, if you want to block a pod to go into a particular node, how would you do it?**

??? success "Reveal answer"
    **In short:** Block scheduling onto a node with taints, node selectors/affinity rules, or both—do not rely on hope.
    
    **Key points**
    - Taint the node and omit tolerations on the Pod.
    - nodeSelector / required nodeAffinity to exclude labels (cloud/zone/instance).
    - For runtime blocks, NetworkPolicy cannot stop scheduling—only traffic.
    - In multi-cloud, label nodes by provider and affinity away.
    
    **Try this**
    - `kubectl taint nodes <node> dedicated=teamA:NoSchedule`
    - `kubectl explain pod.spec.affinity`
    
    **Trap**
    - A PreferNoSchedule taint is a soft preference—Pods may still land there under pressure.

**39. How would you structure a multi-stage pipeline that builds, tests and deploys a containerized application to kubernetes using Github Actions?**

??? success "Reveal answer"
    **In short:** Structure GitHub Actions as build → test → scan → push digest → deploy via GitOps or a controlled kubectl/Helm job with environments.
    
    **Key points**
    - Build and unit/integration test on PR; scan image before push.
    - Push digest to registry; write the digest into a GitOps repo or deploy job.
    - Use environment protection rules for staging/production.
    - Prefer Argo CD sync over long-lived kubecredentials in Actions when possible.
    
    **Try this**
    - `# gh workflow run / actions logs`
    - `kubectl get application -n argocd`
    
    **Trap**
    - Storing a cluster-admin kubeconfig in GitHub secrets invites lasting compromise.

**40. How would you implement feature toggles in Deployment pipelines?**

??? success "Reveal answer"
    **In short:** Feature toggles separate deploy from release—ship dark, enable for cohorts, and kill-switch without rolling back binaries.
    
    **Key points**
    - Store flags in ConfigMap/remote flag service; keep defaults safe.
    - Deploy code with flag off; validate; flip for percentage of users.
    - Avoid using flags as permanent config spaghetti—retire them.
    - Combine with canary metrics for progressive delivery.
    
    **Try this**
    - `kubectl rollout restart deploy/<name>`
    
    **Trap**
    - Baking flags into image tags forces rebuilds for every experiment.

**41. How would you decide on the type of environment required for deployment?**

??? success "Reveal answer"
    **In short:** Choose environments by risk and parity needs: ephemeral PR previews, shared integration, staging that mirrors prod, and locked production.
    
    **Key points**
    - More prod-like as you get closer to release (data, networking, IAM).
    - Ephemeral envs for PR validation cut cost and contention.
    - Staging should match prod topology enough to catch Ingress/IAM issues.
    - Production needs change control, observability, and backup/restore proof.
    
    **Trap**
    - A “staging” that shares the production database is not a safe environment—it is a dual-write incident waiting to happen.

**42. If you are implementing HPA for statefulsets if new pod comes the pvc would be empty? How would it be able to serve the request?**

??? success "Reveal answer"
    **In short:** New StatefulSet Pods get empty PVCs—HPA does not copy data; the application must join the cluster and replicate/rebuild state.
    
    **Key points**
    - volumeClaimTemplates create a fresh claim per ordinal.
    - Design the datastore for membership changes (replication, rebalance).
    - Often prefer vertical scaling or operator-managed scaling for stateful systems.
    - Warm pools/restore-from-snapshot patterns exist but are app-specific.
    
    **Try this**
    - `kubectl get pvc -l app=<name>`
    - `kubectl get sts <name> -o yaml`
    
    **Trap**
    - Scaling a single-primary database StatefulSet with HPA is how you create empty replicas that cannot serve reads/writes.

**43. Kubernetes architecture in depth. Every component functioning. How would you join a new node to control plane?**

??? success "Reveal answer"
    **In short:** Control plane (API server, etcd, scheduler, controller-manager) plus kubelet/kube-proxy/runtime on nodes; join nodes with bootstrap credentials against the API.
    
    **Key points**
    - API server is the front door; etcd stores cluster state.
    - Scheduler places Pods; controllers reconcile desired objects.
    - Workers run kubelet + container runtime + CNI.
    - Join: kubeadm join or managed node pools that bootstrap automatically.
    
    **Try this**
    - `kubectl get componentstatuses 2>/dev/null || true`
    - `kubectl get nodes`
    - `kubeadm token create --print-join-command`
    
    **Trap**
    - Joining nodes with mismatched Kubernetes/CNI versions creates flapping Ready state.

**44. How would you implement security for Kubernetes(both on container side and the infra side using native Kubernetes solutions)?**

??? success "Reveal answer"
    **In short:** Secure Kubernetes with least privilege RBAC, admission controls, NetworkPolicies, and hardened images/nodes—defence in depth.
    
    **Key points**
    - Container side: non-root, read-only rootfs, drop caps, scan images, no privileged by default.
    - Cluster side: RBAC, PSS/PSA or PodSecurity, OPA/Gatekeeper/Kyverno, secrets encryption.
    - NetworkPolicies default-deny where practical; private nodes/API.
    - Node OS patching, minimal SSH, and audited cloud IAM to the API.
    
    **Try this**
    - `kubectl auth can-i --list`
    - `kubectl get networkpolicy -A`
    
    **Trap**
    - Cluster-admin bindings for every pipeline identity make “RBAC exists” meaningless.

**45. Pods in different namespaces can communicate. How would you block that communication? Where would you implement the NetworkPolicy?**

??? success "Reveal answer"
    **In short:** Block cross-namespace traffic with NetworkPolicies selecting pods/namespaces—usually default-deny ingress in each namespace, then allow explicit peers.
    
    **Key points**
    - NetworkPolicy is enforced by the CNI (Calico/Cilium/etc.)—it must support policy.
    - Implement in the namespaces that host the workloads (and sometimes host NS for agents).
    - Use namespaceSelector/podSelector; remember DNS allow rules.
    - Test with a deny-all then open only what the app needs.
    
    **Try this**
    - `kubectl apply -f networkpolicy.yaml`
    - `kubectl get networkpolicy -n <ns>`
    
    **Trap**
    - Applying NetworkPolicy while the CNI does not enforce it gives a false sense of isolation.

**46. During a Canary deployment, how would you verify that the 10% deployment is healthy? What metrics would you monitor before proceeding to 100%?**

??? success "Reveal answer"
    **In short:** Judge a 10% canary on golden signals and error budget—not only “Pods Ready”.
    
    **Key points**
    - Watch latency (p95/p99), error rate, saturation, and key business KPIs.
    - Compare canary vs baseline with the same traffic shape.
    - Gate promotion on automated thresholds; keep a fast abort.
    - Include synthetic probes hitting canary-only routes when possible.
    
    **Try this**
    - `kubectl get pods -l role=canary`
    - `kubectl rollout status deploy/<name>`
    
    **Trap**
    - Promoting on CPU alone misses user-visible 500s that never raise CPU.

**47. In Kubernetes, how would you configure your deployment to double CPU allocation once usage crosses 70%?**

??? success "Reveal answer"
    **In short:** You cannot make a Deployment “double CPU at 70%” by itself—use HPA (and optionally VPA) on metrics, or adjust resources via a controlled rollout.
    
    **Key points**
    - HPA scales replica count from CPU/custom metrics—not instantaneous CPU doubling inside one container.
    - Set requests/limits; HPA targets average utilisation (e.g. 70%).
    - VPA can recommend/resize resource requests over time (with care).
    - For sudden doubling, change resources in the template and roll out.
    
    **Try this**
    - `kubectl get hpa`
    - `kubectl autoscale deploy <name> --cpu-percent=70 --min=2 --max=10`
    
    **Trap**
    - Setting limits without requests (or absurd ratios) makes HPA and bin-packing unpredictable.

**48. How would you implement zero-trust networking inside Kubernetes without using a service mesh?**

??? success "Reveal answer"
    **In short:** Without a mesh, pursue zero-trust with default-deny NetworkPolicies, mTLS at the app or sidecars you control, identity via ServiceAccount, and strict ingress.
    
    **Key points**
    - Default-deny ingress/egress; allow only declared flows.
    - ServiceAccount + projected tokens; no long-lived secrets in Pods.
    - App-level TLS or protocol proxies; deny plaintext where possible.
    - Admission policies block privileged/hostNetwork pods.
    
    **Try this**
    - `kubectl get networkpolicy -A`
    - `kubectl get sa,rolebinding -A`
    
    **Trap**
    - Calling flat cluster networking “zero-trust” because you have TLS at the edge only is incomplete.

**49. How would you deploy a Kubernetes application using GitHub Actions and ArgoCD?**

??? success "Reveal answer"
    **In short:** GitHub Actions builds/pushes the image; Argo CD deploys by reconciling a Git repo that references the new digest.
    
    **Key points**
    - Actions: test, build, scan, push digest; update manifest/values in GitOps repo.
    - Argo CD Application points at that repo/path and syncs to the cluster.
    - Use PR to prod GitOps path or progressive sync policies.
    - Avoid kubectl apply from Actions against prod when GitOps is the source of truth.
    
    **Try this**
    - `argocd app sync <app>`
    - `kubectl get application -n argocd`
    
    **Trap**
    - Updating only the cluster while leaving Git stale guarantees Argo CD will revert or drift-fight you.

**50. What are the common reasons for a Kubernetes node becoming NotReady, and how would you identify the root cause?**

??? success "Reveal answer"
    **In short:** NotReady usually means kubelet/runtime/network/disk pressure or cloud instance failure—describe the node, then inspect kubelet and OS.
    
    **Key points**
    - Conditions: MemoryPressure, DiskPressure, NetworkUnavailable, PIDPressure.
    - Kubelet crash, container runtime hang, or CNI failure are frequent.
    - Spot interruption, failed upgrade, or full disk on /var/lib/*.
    - Correlate with node Events and provider health status.
    
    **Try this**
    - `kubectl describe node <node>`
    - `kubectl get node <node> -o jsonpath='{.status.conditions}'`
    
    **Trap**
    - Deleting the node object before capturing logs removes the evidence trail.

## Practice questions

**51. How do you implement Horizontal Pod Autoscaling (HPA) in Kubernetes?**

??? success "Reveal answer"
    **In short:** HPA scales workload replicas from resource or custom metrics via the metrics pipeline (metrics-server or adapter).
    
    **Key points**
    - Define min/max replicas and target CPU/memory or custom metrics.
    - Requires resource requests for CPU/memory targets.
    - Tune behaviour (stabilisation windows) to avoid flapping.
    - Validate with load tests and watch that dependencies can take the scale.
    
    **Try this**
    - `kubectl get hpa -A`
    - `kubectl describe hpa <name>`
    
    **Trap**
    - HPA without requests set yields “unknown” metrics and no scaling.

**52. How do you implement cost optimization in a Kubernetes cluster?**

??? success "Reveal answer"
    **In short:** Cut Kubernetes cost by right-sizing requests, bin-packing, autoscaling nodes/Pods, and deleting idle environments.
    
    **Key points**
    - Set realistic requests/limits; use VPA recommendations carefully.
    - Cluster Autoscaler / node auto-provisioning for elastic capacity.
    - Spot/preemptible for fault-tolerant workloads; turn down non-prod nights.
    - Watch orphaned LoadBalancers, unattached disks, and unused images in registries.
    
    **Try this**
    - `kubectl top pods -A`
    - `kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes`
    
    **Trap**
    - Setting tiny requests to “save money” causes noisy-neighbour throttling and bigger outages than the bill.

**53. How does Kubernetes handle storage?**

??? success "Reveal answer"
    **In short:** Kubernetes storage binds Pods to PersistentVolumes via PVCs, provisioned dynamically by StorageClasses (CSI drivers).
    
    **Key points**
    - PVC requests size/access mode; StorageClass selects provisioner/parameters.
    - RWO vs RWX matters for multi-Pod attach.
    - StatefulSets use volumeClaimTemplates for per-Pod disks.
    - Backup/restore and zone affinity are operational concerns beyond the PVC YAML.
    
    **Try this**
    - `kubectl get sc,pvc,pv`
    - `kubectl describe pvc <name>`
    
    **Trap**
    - Deleting a PVC with reclaim policy Delete can destroy production data in one command.

**54. In Kubernetes, how do you manage application deployment, scaling, and rollback? Can you walk through a specific scenario?**

??? success "Reveal answer"
    **In short:** Deploy with Deployments/Helm/GitOps, scale with replicas/HPA, and roll back via revision history when a release misbehaves.
    
    **Key points**
    - Scenario: ship digest v2 → Ready spike in 5xx → kubectl rollout undo to v1.
    - Scale: HPA reacts to CPU/RPS; verify EndpointSlices keep up.
    - GitOps: revert commit and sync for an auditable rollback.
    - Always validate with smoke tests and golden signals after changes.
    
    **Try this**
    - `kubectl set image deploy/<name> app=<image>@sha256:<digest>`
    - `kubectl rollout undo deploy/<name>`
    
    **Trap**
    - Scaling replicas during a bad config rollout multiplies failure faster than it restores capacity.

**55. Design a multi-tenant Kubernetes platform where teams must not affect each other’s resource usage, network traffic, or upgrade cycles?**

??? success "Reveal answer"
    **In short:** Multi-tenant platforms isolate with namespaces + hard quotas, NetworkPolicies, separate node pools/clusters per trust tier, and controlled upgrade waves.
    
    **Key points**
    - ResourceQuota/LimitRange per team namespace; priority classes.
    - NetworkPolicies and optional service mesh mTLS between tenants.
    - Separate node pools or clusters for noisy/untrusted workloads.
    - GitOps projects and RBAC so teams cannot edit each other’s apps or upgrade channels.
    
    **Try this**
    - `kubectl get resourcequota -A`
    - `kubectl get networkpolicy -A`
    
    **Trap**
    - Soft multi-tenancy with only namespaces and cluster-admin per team is not isolation.

**56. Suppose a new deployment was implemented, suddenly all the PODs (new and old ones) crashed, what's the reason for this?**

??? success "Reveal answer"
    **In short:** When new and old Pods all crash after a deploy, suspect a shared dependency: bad ConfigMap/Secret, broken mesh/policy, bad node taint wave, or incompatible cluster-wide change.
    
    **Key points**
    - Shared config mounted by both revisions can poison rolling updates.
    - Webhook/CNI/DNS outages affect every Pod start.
    - Image registry outage causes mass ImagePullBackOff—not app logic.
    - Compare the change diff: config, policy, and platform add-ons—not only the app image.
    
    **Try this**
    - `kubectl get events -A --sort-by=.lastTimestamp | tail -n 50`
    - `kubectl get pods -A | grep -v Running`
    
    **Trap**
    - Assuming “only the new ReplicaSet is bad” delays rollback when a shared Secret rotation broke everyone.

**57. How does Kubernetes handle scaling?**

??? success "Reveal answer"
    **In short:** Kubernetes scales Pods (manual replicas or HPA/KEDA) and nodes (Cluster Autoscaler/node pools); the two must work together.
    
    **Key points**
    - Horizontal Pod scaling adds replicas; vertical adjusts resources.
    - Node autoscaling adds capacity when Pods are unschedulable.
    - Custom metrics and event-driven scalers (KEDA) fit queues/jobs.
    - Always watch dependency capacity when apps scale out.
    
    **Try this**
    - `kubectl get hpa,deploy`
    - `kubectl describe nodes | grep -A5 Allocated`
    
    **Trap**
    - Pod autoscaling without node autoscaling leaves Pending replicas during peaks.

**58. How about the sticky session data if POD gets down?**

??? success "Reveal answer"
    **In short:** Sticky sessions pin clients to a Pod—when that Pod dies, in-memory session data dies unless you externalise it.
    
    **Key points**
    - Prefer external session stores (Redis/DB) for HA.
    - Service sessionAffinity ClientIP is best-effort and breaks on Pod replacement.
    - Ingress cookie stickiness has the same failure mode on Pod death.
    - Design apps as stateless at the Pod layer for rolling updates.
    
    **Try this**
    - `kubectl explain svc.spec.sessionAffinity`
    
    **Trap**
    - Relying on sticky sessions as your persistence layer guarantees user logouts during every deploy.

**59. How do you handle subnetting in a Kubernetes environment?**

??? success "Reveal answer"
    **In short:** Plan cluster subnets for nodes, Pods, and Services with enough IP headroom—CNI mode (overlay vs VPC-native) drives the design.
    
    **Key points**
    - Size Pod CIDRs for peak Pod density; avoid secondary IP exhaustion.
    - Separate ranges for Services (ClusterIP) and Pods per platform docs.
    - VPC-native CNIs need subnet capacity across AZs.
    - Reserve space for future node pools and dual-stack if required.
    
    **Try this**
    - `kubectl get nodes -o custom-columns=NAME:.metadata.name,PODCIDR:.spec.podCIDR`
    - `kubectl cluster-info dump | head`
    
    **Trap**
    - Undersized subnets show up as Pending Pods with failed IP allocation—often mistaken for CPU shortage.

## Related
- Course: [Kubernetes](../kubernetes/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
