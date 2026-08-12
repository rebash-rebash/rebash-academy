---
title: "Kubernetes Interview Preparation"
description: "60 curated Kubernetes interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
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

## Core concepts

**1. What is a Pod, Deployment, and Service in Kubernetes?**

??? success "Reveal answer"
    How do they relate to each other? 
    Answer: 
    
     
    These three objects are the foundation of almost every Kubernetes application. 
    Pod: The smallest deployable unit in Kubernetes. A Pod wraps one or more containers that share 
    network space and storage. Think of a Pod as a "logical host" for your containers. 
    # pod.yaml — a basic Pod definition 
    apiVersion: v1 
    kind: Pod 
    metadata: 
     name: my-app-pod 
     labels: 
     app: my-app 
     version: v1.0 
    spec: 
     containers: 
     - name: app 
     image: myregistry/my-app:1.0.0 
     ports: 
     - containerPort: 8080 
     resources: 
     requests: 
     memory: "128Mi" 
     cpu: "250m" 
     limits: 
     memory: "256Mi" 
     cpu: "500m" 
     readinessProbe: 
     httpGet: 
     path: /health 
     port: 8080 
     initialDelaySeconds: 10 
     periodSeconds: 5 
     livenessProbe: 
     httpGet: 
     path: /health 
     port: 8080 
     initialDelaySeconds: 30 
    
     
     periodSeconds: 10 
    In practice, you almost never create Pods directly. If a Pod crashes, it stays dead — there's 
    nothing to restart it. That's where Deployments come in. 
    Deployment: A Deployment manages a set of identical Pods (called a…

**2. What is a ConfigMap and Secret in Kubernetes?**

??? success "Reveal answer"
    How do you inject configuration into Pods? 
    Answer: 
    ConfigMap stores non-sensitive configuration data as key-value pairs. Secret stores sensitive 
    data (passwords, tokens, certificates) in base64-encoded form with additional access controls. 
    # configmap.yaml 
    apiVersion: v1 
    kind: ConfigMap 
    metadata: 
     name: app-config 
    
     
     namespace: production 
    data: 
     APP_ENV: "production" 
     LOG_LEVEL: "info" 
     MAX_CONNECTIONS: "100" 
     # Multi-line config files are also supported 
     app.properties: | 
     server.port=8080 
     server.timeout=30 
     feature.new_ui=true 
    # secret.yaml 
    apiVersion: v1 
    kind: Secret 
    metadata: 
     name: app-secrets 
     namespace: production 
    type: Opaque 
    # Values must be base64-encoded 
    # echo -n "mysupersecretpassword" | base64 
    data: 
     DB_PASSWORD: bXlzdXBlcnNlY3JldHBhc3N3b3Jk 
     API_KEY: c2VjcmV0YXBpa2V5MTIz 
    Injecting into a Pod — three methods: 
    Method 1: Environment variables 
    spec: 
     containers: 
     - name: app 
     image: my-app:1.0 
     env: 
     # From ConfigMap 
     - name: APP_ENV 
     valueFrom: 
     configMapKeyRef: 
     name: app-config 
    
     
     key: APP_ENV 
     # From…

**3. What is a Kubernetes Ingress, and how does it differ from a LoadBalancer Service?**

??? success "Reveal answer"
    Answer: 
    Understanding the difference between Services and Ingress is crucial for designing Kubernetes 
    networking correctly. 
    LoadBalancer Service: Creates an external cloud load balancer (like an AWS ALB or NLB) 
    for each Service. If you have 10 microservices, you get 10 load balancers — 10 bills. 
    Ingress: A single entry point (one load balancer) that routes HTTP/HTTPS traffic to different 
    Services based on host names and URL paths. One load balancer, many services. 
    Without Ingress: 
     api.myapp.com → ALB #1 → api-service 
     web.myapp.com → ALB #2 → web-service 
     admin.myapp.com → ALB #3 → admin-service 
     (3 load balancers = 3 bills) 
    With Ingress: 
     api.myapp.com ─┐ 
     web.myapp.com ─┤→ ALB #1 → Ingress Controller → routes to correct Service 
     admin.myapp.com ─┘ 
     (1 load balancer = 1 bill, + Ingress Controller overhead) 
    Complete NGINX Ingress example: 
    # ingress.yaml 
    apiVersion: networking.k8s.io/v1 
    kind: Ingress 
    metadata: 
     name: my-app-ingress 
     namespace: production 
     annotations: 
     kubernetes.io/ingress.class: "nginx" 
    …

**4. What is Argo CD, and how does it implement GitOps for Kubernetes deployments?**

??? success "Reveal answer"
    Answer: 
    Argo CD is a declarative GitOps continuous delivery tool for Kubernetes. The core idea 
    of GitOps is: Git is the single source of truth for both application code and infrastructure 
    configuration. Argo CD continuously watches a Git repository and ensures that the Kubernetes 
    cluster state matches what's defined in Git. 
    Git Repository Kubernetes Cluster 
    (desired state) Argo CD (actual state) 
    ───────────────── ←──────────── ───────────────── 
    deployment.yaml syncs Running pods 
    service.yaml Services 
    configmap.yaml ConfigMaps 
    If someone manually changes something in Kubernetes (a rogue kubectl apply), Argo CD 
    detects the drift and either alerts you or automatically reverts it. 
    Argo CD Application manifest: 
    # argocd-application.yaml 
    apiVersion: argoproj.io/v1alpha1 
    kind: Application 
    metadata: 
     name: my-api-production 
     namespace: argocd 
    spec: 
     project: default 
     source: 
     repoURL: https://github.com/myorg/k8s-manifests.git 
     targetRevision: main 
     path: services/my-api/production # Folder in the repo 
     destination: 
     server:…

**5. What is Vault by HashiCorp, and how does it integrate with Kubernetes for secrets management?**

??? success "Reveal answer"
    HashiCorp Vault is an enterprise-grade secrets management platform. Unlike Kubernetes 
    Secrets (which are base64-encoded and stored in etcd), Vault encrypts secrets with AES-256-
    GCM, provides fine-grained access control, maintains an audit log of every secret access, and can 
    generate short-lived, dynamic credentials. 
    Vault Agent Injector — the sidecar pattern: 
    
     
    Vault's Kubernetes integration works via a sidecar injector. When a Pod has specific annotations, 
    Vault automatically injects a sidecar container that: 
    1. Authenticates with Vault using the Pod's Kubernetes service account 
    2. Fetches the required secrets 
    3. Writes them to a shared volume as files or environment variables 
    4. Periodically renews leases for dynamic secrets 
    # deployment-with-vault.yaml 
    apiVersion: apps/v1 
    kind: Deployment 
    metadata: 
     name: my-api 
     namespace: production 
    spec: 
     template: 
     metadata: 
     annotations: 
     # Enable Vault Agent injection 
     vault.hashicorp.com/agent-inject: "true" 
     vault.hashicorp.com/role: "my-api-production" 
     # Inject database credentials as a file…

**6. Explain how you've set up a Kubernetes cluster.**

??? success "Reveal answer"
    For a managed setup I'd use a cloud provider's offering like EKS, GKE, or AKS, letting the provider handle the control
    plane. For a self-managed cluster, I'd use kubeadm init to set up the control plane node and kubeadm join to add
    worker nodes, install a CNI networking plugin like Calico or Weave immediately since pods can't communicate
    without one, then deploy applications as Deployments, Services, and ConfigMaps, and finally set up Prometheus and
    Grafana for cluster monitoring.

**7. What are some safe deployment strategies?**

??? success "Reveal answer"
    + Blue/Green: Two identical environments. Use for zero downtime releases. * Understanding of strategies |
    + Canary: Release to small % of users first. Use for risk reduction. * Trade-offs and use cases
    + Rolling Update: Gradual replacement of instances/pods. * Zero/low downtime mindset
    + Recreate: Stop old version before new one starts. Use for small apps. * Risk management |
    + Dark Launch / Feature Flags: Deploy hidden, enable for users gradually. * Business impact thinking
    G@)

**8. What are Kubernetes services, and how do they differ from Pods?**

??? success "Reveal answer"
    Pods are the smallest unit in Kubernetes, representing one or more tightly coupled containers sharing network and
    storage, and they're ephemeral -- they come and go as deployments roll out or nodes fail. A Service provides a
    stable IP address and DNS name for a set of Pods identified by a label selector, so traffic keeps reaching healthy
    Pods even as the underlying Pods themselves are replaced.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    1
    KUBERNETES

**9. What is Kubernetes, and how does it help in container orchestration?**

??? success "Reveal answer"
    Kubernetes automates the deployment, scaling, and management of containerized applications -- it handles
    automatic scaling based on traffic or resource usage, load balancing across containers, self-healing by restarting
    failed containers and killing unresponsive ones, automated rollouts and rollbacks with zero downtime, and resource
    allocation across the cluster.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**10. Explain the difference between a Deployment and a StatefulSet in Kubernetes.**

??? success "Reveal answer"
    A Deployment is for stateless applications and ensures the correct number of interchangeable Pods are running,
    scaling and recreating them freely. A StatefulSet is for stateful applications needing stable network identity and
    persistent storage per Pod, with ordered, predictable deployment and scaling -- useful for databases and other
    services where each replica has its own identity and data.

## Scenarios and troubleshooting

**11. How do you implement zero-downtime deployments on ECS Fargate with a production traffic cutover strategy?**

??? success "Reveal answer"
    Zero-downtime deployments on ECS Fargate require a combination of rolling updates, health 
    checks, and ALB target group management. The gold standard is Blue/Green deployment using 
    CodeDeploy with ECS, which provides atomic traffic shifting with instant rollback capability. 
    Architecture: 
    Internet → ALB (port 443) 
     [Listener Rules] 
    Blue TG (v1.0) Green TG (v1.1) 
    ECS Tasks (old) ECS Tasks (new) 
    CodeDeploy AppSpec for ECS Blue/Green: 
    # appspec.yaml 
    version: 0.0 
    Resources: 
     - TargetService: 
     Type: AWS::ECS::Service 
     Properties: 
     TaskDefinition: <TASK_DEFINITION> 
     LoadBalancerInfo: 
     ContainerName: "app" 
     ContainerPort: 8080 
     PlatformVersion: "LATEST" 
    Hooks: 
     - BeforeAllowTraffic: "LambdaFunctionToValidateBeforeTrafficShift" 
     - AfterAllowTraffic: "LambdaFunctionToValidateAfterTrafficShift" 
    Lambda validation hook: 
    import boto3 
    
     
    import json 
    def lambda_handler(event, context): 
     """ 
     Called by CodeDeploy before shifting traffic. 
     We run smoke tests against the new task version. 
     """ 
     codedeploy = boto3.client('codedeploy') 
     deployment_id =…

**12. How do you deploy the ELK stack on Kubernetes for production log aggregation?**

??? success "Reveal answer"
    In production Kubernetes environments, the modern approach is: Filebeat DaemonSet → 
    Logstash (or directly to Elasticsearch) → Elasticsearch Cluster → Kibana. 
    Filebeat DaemonSet — ships logs from all pods: 
    # filebeat-daemonset.yaml 
    apiVersion: apps/v1 
    kind: DaemonSet 
    metadata: 
     name: filebeat 
     namespace: logging 
    spec: 
     selector: 
     matchLabels: 
     app: filebeat 
     template: 
     metadata: 
    
     
     labels: 
     app: filebeat 
     spec: 
     serviceAccountName: filebeat 
     terminationGracePeriodSeconds: 30 
     containers: 
     - name: filebeat 
     image: docker.elastic.co/beats/filebeat:8.12.0 
     args: ["-c", "/etc/filebeat.yml", "-e"] 
     env: 
     - name: ELASTICSEARCH_HOST 
     value: "elasticsearch:9200" 
     - name: NODE_NAME 
     valueFrom: 
     fieldRef: 
     fieldPath: spec.nodeName 
     resources: 
     requests: 
     memory: "100Mi" 
     cpu: "100m" 
     limits: 
     memory: "200Mi" 
     cpu: "200m" 
     volumeMounts: 
     - name: config 
     mountPath: /etc/filebeat.yml 
     subPath: filebeat.yml 
     - name: varlog 
     mountPath: /var/log 
     readOnly: true 
     - name: varlibdockercontainers 
     mountPath: /var/lib/docker/containers 
    …

**13. Describe a real production incident where a misconfigured HPA caused cascading failure. How would you redesign autoscaling to avoid this?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**14. How would you design a Kubernetes cluster that must survive a full AZ failure without data loss, while running stateful workloads at scale?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**15. How do you rollback a failed deployment in production?**

??? success "Reveal answer"
    + Use automated rollback (Jenkins/Kubernetes/CodePipeline) if available. * Knowledge of rollback mechanisms
    + For Kubernetes: kubectl rollout undo deployment/<name> % Tool specific expertise
    + For ECS/ASG: Revert to previous task definition / launch template. * Minimizing downtime
    + For app servers: Restore previous artifact and restart services. * Verification after rollback
    + Verify rollback success with health checks and monitoring. * Customer impact awareness
    (3)

**16. right? So how it is basically getting deployed in cluster? I mean the deployment is basically failing just on the pod is currently in the error state. It is getting terminated. So how are you going to troubleshoot those such kind of Kubernetes issues?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**17. How do you approach the debug on the deployment failure?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**18. U handled any debug/troubleshoot for kubernetes?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**19. Tell me about a time you handled a failed deployment in production. How did you manage the team and stakeholders?,?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**20. How to troubleshoot if pod is failed in AKS, commands please?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**21. Logs are incomplete — how would you troubleshoot across AKS, Ingress, App, and Infra?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**22. When designing a microservices-oriented infrastructure, what technologies and components (like load balancer, service mesh, Kubernetes) would you bring in, and how would you design the estate?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**23. How would you design container images for ultra-fast cold starts in serverless or autoscaled Kubernetes environments?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**24. If your pod is in Pending state, then what are your troubleshoot steps?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**25. If you have a Kubernetes cluster with pods running, but when you hit the URL you get HTTP errors (403, 404, 503), what would be your troubleshooting steps?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**26. When kubernetes node fails what will happen?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**27. If you pod is not running, how do you troubleshoot it?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**28. If there a deployment failure what the next steps you perform ?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**29. I have an Ingress object that is not routing the traffic to the Kubernetes cluster. What are the reasons and how do you troubleshoot that?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**30. I have created a service object that is not mapped to a deployment. What could be the reason and how do you debug it?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**31. In Kubernetes, if a pod is in a pending state, how do you troubleshoot?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**32. Database connection from a pod is not working only for you. How will you troubleshoot?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**33. How will you investigate POD failure?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**34. How do you handle deployment failures?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**35. how did you troubleshoot the pod crashback loop?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**36. You have a Kubernetes cluster with 30 nodes. 29 nodes are Ready, but 1 node is NotReady. You have already checked kubectl logs, kubectl describe, and other basic commands. How will you troubleshoot the node further?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**37. Describe your approach to troubleshooting Kubernetes worker node issues beyond the basic kubectl commands?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**38. How do you debug intermittent pod restarts when liveness probes pass, readiness passes, but the pod is still killed by the node?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**39. In a multi-cloud environment, if you want to block a pod to go into a particular node, how would you do it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**40. How would you structure a multi-stage pipeline that builds, tests and deploys a containerized application to kubernetes using Github Actions?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**41. How would you implement feature toggles in Deployment pipelines?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**42. How would you decide on the type of environment required for deployment?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**43. If you are implementing HPA for statefulsets if new pod comes the pvc would be empty? How would it be able to serve the request?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**44. Kubernetes architecture in depth. Every component functioning. How would you join a new node to control plane?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**45. How would you implement security for Kubernetes(both on container side and the infra side using native Kubernetes solutions)?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**46. Pods in different namespaces can communicate. How would you block that communication? Where would you implement the NetworkPolicy?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**47. During a Canary deployment, how would you verify that the 10% deployment is healthy? What metrics would you monitor before proceeding to 100%?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**48. In Kubernetes, how would you configure your deployment to double CPU allocation once usage crosses 70%?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**49. How would you implement zero-trust networking inside Kubernetes without using a service mesh?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**50. How would you deploy a Kubernetes application using GitHub Actions and ArgoCD?**

??? success "Reveal answer"
    GitHub Actions handles the CI side -- linting manifests, running tests, building and pushing the image, then updating
    the Kubernetes manifests or Helm values in the Git repo ArgoCD watches. ArgoCD picks up that change and
    automatically syncs the cluster to match, so GitHub Actions never needs direct write access to the cluster itself.

**51. What are the common reasons for a Kubernetes node becoming NotReady, and how would you identify the root cause?**

??? success "Reveal answer"
    Start with a precise definition in the context of Kubernetes, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

## Practice questions

**52. How do you implement Horizontal Pod Autoscaling (HPA) in Kubernetes?**

??? success "Reveal answer"
    HPA automatically scales the number of Pods in a Deployment based on observed metrics. The 
    classic trigger is CPU utilization, but modern HPA supports custom metrics from Prometheus, 
    memory, or even external metrics (like queue depth in SQS). 
    Basic CPU-based HPA: 
    # hpa-cpu.yaml 
    apiVersion: autoscaling/v2 
    kind: HorizontalPodAutoscaler 
    metadata: 
     name: my-app-hpa 
     namespace: production 
    spec: 
     scaleTargetRef: 
     apiVersion: apps/v1 
     kind: Deployment 
     name: my-app 
     minReplicas: 3 
     maxReplicas: 20 
     metrics: 
     - type: Resource 
     resource: 
     name: cpu 
     target: 
     type: Utilization 
     averageUtilization: 70 # Scale when avg CPU > 70% 
     - type: Resource 
     resource: 
     name: memory 
     target: 
     type: Utilization 
     averageUtilization: 80 # Scale when avg memory > 80% 
    
     
     behaviour: 
     scaleUp: 
     stabilizationWindowSeconds: 30 # Wait 30s before scaling up again 
     policies: 
     - type: Pods 
     value: 4 # Add at most 4 pods at once 
     periodSeconds: 60 
     scaleDown: 
     stabilizationWindowSeconds: 300 # Wait 5min before scaling down 
     policies: 
     - type: Percent 
     value:…

**53. How do you implement cost optimization in a Kubernetes cluster?**

??? success "Reveal answer"
    Running Kubernetes in production can be expensive if not managed carefully. Here are the key 
    cost optimisation strategies with concrete implementations: 
    
     
    1. Cluster Autoscaler — right-size your node pool: 
    # cluster-autoscaler deployment on EKS 
    apiVersion: apps/v1 
    kind: Deployment 
    metadata: 
     name: cluster-autoscaler 
     namespace: kube-system 
    spec: 
     template: 
     spec: 
     containers: 
     - name: cluster-autoscaler 
     image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.28.0 
     command: 
     - ./cluster-autoscaler 
     - --v=4 
     - --stderrthreshold=info 
     - --cloud-provider=aws 
     - --skip-nodes-with-local-storage=false 
     - --expander=least-waste # Choose node type that wastes least 
    resources 
     - --node-group-auto-discovery=asg:tag=k8s.io/cluster-
    autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster 
     - --scale-down-delay-after-add=5m 
     - --scale-down-unneeded-time=10m # Remove idle nodes after 10 
    minutes 
     - --scale-down-utilization-threshold=0.5 # Node < 50% utilized = 
    candidate for removal 
    2. Spot/Preemptible instances for non-critical workloads: 
    # Use…

**54. How does Kubernetes handle storage?**

??? success "Reveal answer"
    PersistentVolumes represent actual durable storage resources in the cluster, PersistentVolumeClaims are requests
    from a Pod for storage matching certain criteria, and a StorageClass defines the type of storage -- SSD versus HDD,
    for instance -- enabling dynamic provisioning so a PV is created automatically to satisfy a PVC instead of needing to
    be pre-provisioned manually.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    2
    KUBERNETES ARCHITECTURE

**55. [ ] In Kubernetes, how do you manage application deployment, scaling, and rollback? Can you walk through a specific scenario?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**56. Design a multi-tenant Kubernetes platform where teams must not affect each other’s resource usage, network traffic, or upgrade cycles?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**57. Suppose a new deployment was implemented, suddenly all the PODs (new and old ones) crashed, what's the reason for this ?**

??? success "Reveal answer"
    New deployment exhausted the resource limit, so we need to use "limit" in our deployment.yaml file.
    
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Kubernetes components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**58. How does Kubernetes handle scaling?**

??? success "Reveal answer"
    Manual scaling with kubectl scale to directly adjust replica count; Horizontal Pod Autoscaler, which automatically
    scales replica count based on CPU/memory or custom metrics; and Vertical Pod Autoscaler, which adjusts a Pod's
    resource requests and limits based on observed consumption rather than the number of replicas.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    3
    INGRESS CONTROLLER

**59. How about the sticky session data if POD gets down?**

??? success "Reveal answer"
    Yes the session data will be lost,.
    
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Kubernetes, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**60. How do you handle subnetting in a Kubernetes environment?**

??? success "Reveal answer"
    Kubernetes needs CIDR ranges allocated for nodes, pods, and services, and getting that sizing right up front matters
    a lot because it's painful to change after the cluster is running -- I make sure the pod CIDR is large enough to support
    the cluster's eventual scale, since running out of pod IPs is a hard wall to hit later.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

## Related

- Course: [Kubernetes](../kubernetes/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
