---
title: "Kubernetes Interview Preparation"
description: "60 curated interview questions and model answers for Kubernetes — concepts, scenarios, troubleshooting, and production trade-offs."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. Explain the Kubernetes architecture — what are the main components?**

??? success "Reveal answer"
    Kubernetes follows a control plane + worker node architecture. Think of the control plane as 
    the brain (it makes decisions) and worker nodes as the muscles (they run the actual workloads). 
    Control Plane Components: 
    ┌─────────────────────────────────────────────────────────────────┐ 
    │ CONTROL PLANE │ 
    │ │ 
    │ ┌────────────┐ ┌────────────┐ ┌───────────────────────────┐ │ 
    │ │ API Server │ │ Scheduler │ │ Controller Manager │ │ 
    │ │(kube- │ │(kube- │ │(ReplicaSet, Deployment, │ │ 
    │ │ apiserver) │ │ scheduler) │ │ Job controllers) │ │ 
    │ └────────────┘ └────────────┘ └───────────────────────────┘ │ 
    │ ┌────────────────────────────────────────────────────────────┐ │ 
    │ │ etcd (cluster state) │ │ 
    │ └────────────────────────────────────────────────────────────┘ │ 
    └─────────────────────────────────────────────────────────────────┘ 
     │ 
     ┌────────────────┼────────────────┐ 
     │ │ │ 
    
     
     ┌─────────▼──────┐ ┌───────▼──────┐ ┌──────▼───────┐ 
     │ WORKER NODE 1 │ │ WORKER NODE 2│ │ WORKER NODE 3│ 
     │ │ │ │ │ │ 
     │ ┌──────────┐ │ │ ┌──────────┐ │ │ ┌──────────┐ │ 
     │ │…

**2. What is a Pod, Deployment, and Service in Kubernetes?**

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

**3. What is a ConfigMap and Secret in Kubernetes?**

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

**4. Explain Kubernetes resource requests and limits. What happens when a container exceeds its limits?**

??? success "Reveal answer"
    Answer: 
    Resource management in Kubernetes is one of the most practically important topics — get it 
    wrong and your cluster either wastes money (over-provisioned) or crashes workloads (under-
    provisioned). 
    Requests vs Limits: 
    • 
    Request: The amount of CPU/memory Kubernetes guarantees for the container. The 
    Scheduler uses this to decide which node to place the Pod on 
    • 
    Limit: The maximum amount of CPU/memory the container can use. If it exceeds this, it 
    gets throttled (CPU) or killed (memory) 
    resources: 
     requests: 
     memory: "256Mi" # Guaranteed 256MB RAM 
     cpu: "250m" # Guaranteed 0.25 CPU cores (250 millicores) 
     limits: 
     memory: "512Mi" # Never use more than 512MB RAM 
     cpu: "1000m" # Never use more than 1 CPU core 
    What happens when limits are exceeded: 
    Resource 
    Behavior when limit exceeded 
    CPU 
    Container is throttled (slowed down) — not killed 
    Memory 
    Container is OOMKilled (killed by the OS) and restarted 
    # Checking OOMKilled events 
    kubectl describe pod my-app-abc123 
    # Look for: 
    # Last State: Terminated 
    # Reason: OOMKilled 
    # Exit Code: 137…

**5. What is a Kubernetes Ingress, and how does it differ from a LoadBalancer Service?**

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

**6. What is Argo CD, and how does it implement GitOps for Kubernetes deployments?**

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

**7. What is Vault by HashiCorp, and how does it integrate with Kubernetes for secrets management?**

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

**8. Explain how you've set up a Kubernetes cluster.**

??? success "Reveal answer"
    For a managed setup I'd use a cloud provider's offering like EKS, GKE, or AKS, letting the provider handle the control
    plane. For a self-managed cluster, I'd use kubeadm init to set up the control plane node and kubeadm join to add
    worker nodes, install a CNI networking plugin like Calico or Weave immediately since pods can't communicate
    without one, then deploy applications as Deployments, Services, and ConfigMaps, and finally set up Prometheus and
    Grafana for cluster monitoring.

**9. What are some safe deployment strategies?**

??? success "Reveal answer"
    + Blue/Green: Two identical environments. Use for zero downtime releases. * Understanding of strategies |
    + Canary: Release to small % of users first. Use for risk reduction. * Trade-offs and use cases
    + Rolling Update: Gradual replacement of instances/pods. * Zero/low downtime mindset
    + Recreate: Stop old version before new one starts. Use for small apps. * Risk management |
    + Dark Launch / Feature Flags: Deploy hidden, enable for users gradually. * Business impact thinking
    G@)

**10. What are Kubernetes services, and how do they differ from Pods?**

??? success "Reveal answer"
    Pods are the smallest unit in Kubernetes, representing one or more tightly coupled containers sharing network and
    storage, and they're ephemeral -- they come and go as deployments roll out or nodes fail. A Service provides a
    stable IP address and DNS name for a set of Pods identified by a label selector, so traffic keeps reaching healthy
    Pods even as the underlying Pods themselves are replaced.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    1
    KUBERNETES

**11. What is Kubernetes, and how does it help in container orchestration?**

??? success "Reveal answer"
    Kubernetes automates the deployment, scaling, and management of containerized applications -- it handles
    automatic scaling based on traffic or resource usage, load balancing across containers, self-healing by restarting
    failed containers and killing unresponsive ones, automated rollouts and rollbacks with zero downtime, and resource
    allocation across the cluster.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**12. Explain the difference between a Deployment and a StatefulSet in Kubernetes.**

??? success "Reveal answer"
    A Deployment is for stateless applications and ensures the correct number of interchangeable Pods are running,
    scaling and recreating them freely. A StatefulSet is for stateful applications needing stable network identity and
    persistent storage per Pod, with ordered, predictable deployment and scaling -- useful for databases and other
    services where each replica has its own identity and data.

**13. What is the difference between High Availability and Disaster Recovery?**

??? success "Reveal answer"
    + High Availability (HA): Keep the “ running during component. failures. (sc avtvanry Disaster | (Usa HAF enoponenl fillies
    = Local to a region (¢.g., Multi-AZ). > Secret Recover ‘eimai
    ad + Disaster Recovery (DR): Recover the system after a major outage. ee et co cee aaa A) v4 8 for agen disaster
    -s Tncctres ‘maltigle: royiens: Goals Stag up Goal: Recover 5} [EZ] ue Both for fall resence

**14. What are the main components of Kubernetes architecture?**

??? success "Reveal answer"
    The Control Plane manages the overall cluster -- API Server, etcd, Scheduler, and Controller Manager -- and Worker
    Nodes run the actual containerized applications through the Kubelet, Kube-proxy, and container runtime.
    KEY POINTS TO MENTION
    • Control Plane: API Server, etcd, Scheduler, Controller Manager
    • Worker Nodes: Kubelet, Kube-proxy, container runtime

**15. What is etcd and why is it important in Kubernetes?**

??? success "Reveal answer"
    etcd is the distributed key-value store holding all cluster state -- Pods, Secrets, ConfigMaps, Services, everything. It's
    the actual source of truth for cluster configuration, and it ensures data consistency and high availability across control
    plane nodes, which is why losing etcd quorum is one of the most serious things that can happen to a cluster.

**16. What is the CAP theorem?**

??? success "Reveal answer"
    A distributed system can only guarantee two of three: Consistency (all nodes see the same 
    data), Availability (every request gets a response), Partition tolerance (system works despite 
    network failures). In practice, partition tolerance is required, so systems choose CP (Zookeeper, 
    etcd) or AP (Cassandra, DynamoDB).

**17. What are Taints and Tolerations?**

??? success "Reveal answer"
    Taints repel Pods from nodes unless the Pod has a matching Toleration. Used to dedicate nodes 
    for specific workloads (GPU nodes, spot-only nodes). 
    # Node taint: 
    kubectl taint nodes gpu-node-1 gpu=true:NoSchedule 
    # Pod toleration: 
    tolerations: 
     - key: "gpu" 
     value: "true" 
     effect: "NoSchedule"

**18. What is a Kubelet, and what role does it play?**

??? success "Reveal answer"
    The Kubelet is the agent running on every worker node, making sure the containers described in Pod specs are
    actually running correctly, communicating with the control plane to receive instructions and report node/pod status,
    and interacting with the container runtime to manage container lifecycle.

**19. What is Kubernetes and why is it used?**

??? success "Reveal answer"
    Kubernetes is an open-source container orchestration platform that automates deploying, scaling, and managing
    containerized applications across a cluster of servers, letting distributed applications run efficiently without manual,
    error-prone intervention for every scaling or failover event.

**20. What is the role of the Kubernetes API Server?**

??? success "Reveal answer"
    The API Server is the front-end to the entire control plane, exposing the Kubernetes API. It processes every REST
    request -- kubectl commands or otherwise -- updates the cluster's state accordingly, and manages communication
    between internal control plane components and external users.

**21. What is Kubernetes Priority Classes?**

??? success "Reveal answer"
    Assigns priority to Pods for scheduling and eviction. High-priority Pods preempt lower-priority 
    Pods if the cluster is resource-constrained. 
    apiVersion: scheduling.k8s.io/v1 
    kind: PriorityClass 
    value: 1000000 
    globalDefault: false 
    
     
    description: "Critical production workloads"

**22. What is a pod in Kubernetes?**

??? success "Reveal answer"
    A Pod is the smallest and simplest Kubernetes object -- a group of one or more containers sharing storage and
    network resources and the same execution context, typically running a single instance of an application.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**23. Can you explain the GitOps workflow in Kubernetes using ArgoCD and GitHub Actions?**

??? success "Reveal answer"
    Developers push code or manifest changes to Git, a GitHub Actions workflow validates those changes and updates
    the Kubernetes manifests accordingly, and ArgoCD continuously monitors the repository, automatically syncing the
    live cluster to match the desired state declared in Git.

**24. Can you explain how to set up an Ingress Controller in a Kubernetes cluster?**

??? success "Reveal answer"
    Choose a controller like NGINX, deploy it via a Helm chart or manifest into the cluster, then define Ingress resources
    specifying host and path rules pointing at backend Services, and finally update DNS to point at the Ingress
    Controller's external IP or load balancer endpoint.

**25. What is the significance of a Service in Kubernetes?**

??? success "Reveal answer"
    A Service defines a logical set of Pods and a policy to access them, providing a stable IP address and DNS name
    even as the underlying Pods are dynamically created or destroyed -- exposing an app either internally via ClusterIP
    or externally via a LoadBalancer-type Service.

**26. What are Namespaces in Kubernetes?**

??? success "Reveal answer"
    Namespaces divide cluster resources between multiple users or teams, organizing objects, separating resources for
    different environments or teams, and letting resource limits and access controls be applied at the namespace level
    rather than only cluster-wide.

**27. What is an Ingress Controller in Kubernetes?**

??? success "Reveal answer"
    An Ingress Controller is a specialized load balancer for the cluster that interprets Ingress resources and routes
    external HTTP/S traffic to the right services based on host and path rules -- NGINX, Traefik, and HAProxy are
    common ones I've worked with.

**28. What is iptables vs ipvs in Kubernetes?**

??? success "Reveal answer"
    Both are kube-proxy modes for implementing Service load balancing. iptables (default): 
    sequential rule matching, slower at scale. ipvs (kernel-level): hash table lookups, O(1) 
    performance, better for clusters with thousands of services.

**29. What is a TopologySpreadConstraint?**

??? success "Reveal answer"
    Distributes Pods evenly across nodes, zones, or regions. 
    
     
    topologySpreadConstraints: 
     - maxSkew: 1 
     topologyKey: topology.kubernetes.io/zone 
     whenUnsatisfiable: DoNotSchedule 
     labelSelector: 
     matchLabels: 
     app: my-api

**30. What is the function of the Cloud Controller Manager?**

??? success "Reveal answer"
    It manages cloud-provider-specific logic -- provisioning load balancers, managing node instances, handling
    persistent storage integration -- keeping that vendor-specific logic decoupled from the core Kubernetes components.

**31. What is a service mesh?**

??? success "Reveal answer"
    An infrastructure layer managing service-to-service communication. Provides: automatic mTLS, 
    traffic splitting, retries, circuit breaking, distributed tracing, and traffic metrics — all without 
    application code changes.

**32. What is a Kubernetes NetworkPolicy?**

??? success "Reveal answer"
    Controls traffic flow between Pods. Without NetworkPolicy, all Pods can communicate freely. 
    With NetworkPolicy, you can restrict ingress/egress traffic based on Pod selectors, namespace 
    selectors, and IP blocks.

**33. What are Pods in Kubernetes?**

??? success "Reveal answer"
    A Pod is the smallest deployable object in Kubernetes, representing a single instance of a running process that can
    contain one or more tightly coupled containers sharing the same network namespace and storage.

## Scenarios and troubleshooting

**34. How do you implement zero-downtime deployments on ECS Fargate with a production traffic cutover strategy?**

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

**35. How do you deploy the ELK stack on Kubernetes for production log aggregation?**

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

**36. How do you handle rollbacks in the case of a failed deployment?**

??? success "Reveal answer"
    With blue-green or canary deployments, rollback is just redirecting traffic back to the previous version without
    downtime. Since artifacts are versioned, I can also redeploy the last known-good version directly from the artifact
    repository. Automated health checks post-deployment can trigger this rollback automatically, and for
    infrastructure-level failures, Terraform lets me revert to a previous infrastructure state as well.
    KEY POINTS TO MENTION
    • Canary/Blue-Green: redirect traffic back
    • Versioned artifacts enable redeploying last known-good build
    • Automated health-check-triggered rollback
    • Terraform for infrastructure-level reverts
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    0
    CONTAINERIZATION: DOCKER & KUBERNETES

**37. How do you handle datebase migrations in production?**

??? success "Reveal answer"
    + Use backward compatible migrations. * DB migration strategies
    + Apply migrations in steps (expand — migrate + contract). *® Risk mitigation
    + Test on staging with real-like data. * Data integrity focus
    + Use feature flags to avoid breaking changes. * Experience with real systems
    + Monitor performance during and after migration. * Attention to detail
    re KEY TAKEAWAY: | Golden Rule: VERIQTA
    9 Successful deployments are not about pushing code, | “Automate everything you can,
    they are about delivering value safely and reliably. ; but always monitor what matters.” Cy] @verigta_
    
    a@ (me VERIQTA. (TOPICS covereD, |
    3, = KUBERNETES PRODUCTION FAILURES - 7S"
    =» Real interview questions. Real production scenarios. L* Networking issues
    @

**38. How do you rollback a failed deployment in production?**

??? success "Reveal answer"
    + Use automated rollback (Jenkins/Kubernetes/CodePipeline) if available. * Knowledge of rollback mechanisms
    + For Kubernetes: kubectl rollout undo deployment/<name> % Tool specific expertise
    + For ECS/ASG: Revert to previous task definition / launch template. * Minimizing downtime
    + For app servers: Restore previous artifact and restart services. * Verification after rollback
    + Verify rollback success with health checks and monitoring. * Customer impact awareness
    (3)

**39. Service is running, but pods cannot communicate with each other. How do you troubleshoot?**

??? success "Reveal answer"
    « Check if pods are in the same namespace and service discovery works. * Kubernetes networking model
    =) + Test DNS: nslookup <service-name> or dig <service-name> * DNS & service discovery
    + Check NetworkPolicies blocking traffic. * NetworkPolicy awareness |
    + Verify CNI plugin and pod IP connectivity. * CNI understanding
    + Check if correct ports and selectors are configured. * End-to-end. connectivity thinking ’
    e ©

**40. Pods are in CrashLoopBackOff status. How do you troubleshoot and fix it?**

??? success "Reveal answer"
    © Check pod description: kubectl describe pod <pod-name> 
    —3 + Check logs: kubectl logs <pod-name> --previous * Systematic oer
    . Identify exit code, error message, and failed command. = cae —
    . Nesity cont env variables, secrets, vores: and pease thine : nae Veuta a
    . > + Fix the issue and redeploy. Add readiness/liveness probes if missing. &. Proactive Eivncedaat
    @

**41. How would you deploy a Kubernetes application using GitHub Actions and ArgoCD?**

??? success "Reveal answer"
    GitHub Actions handles the CI side -- linting manifests, running tests, building and pushing the image, then updating
    the Kubernetes manifests or Helm values in the Git repo ArgoCD watches. ArgoCD picks up that change and
    automatically syncs the cluster to match, so GitHub Actions never needs direct write access to the cluster itself.

**42. A pod is in CrashLoopBackOff. How do you debug it?**

??? success "Reveal answer"
    kubectl describe pod <name> # Check events and last state reason 
    kubectl logs <pod> --previous # Logs from the crashed container 
    kubectl logs <pod> -c <container> # Specific container logs 
    # Common causes: missing env vars, DB connection failure, OOMKill, bad CMD

**43. What is kubectl debug?**

??? success "Reveal answer"
    Creates an ephemeral debug container attached to a running Pod — useful for debugging 
    minimal containers that don't have shell or debugging tools. 
    kubectl debug -it my-pod --image=busybox --target=app

## Practice questions

**44. How do you implement Horizontal Pod Autoscaling (HPA) in Kubernetes?**

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

**45. How do you implement cost optimization in a Kubernetes cluster?**

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

**46. A node in the cluster is NotReady. How do you investigate?**

??? success "Reveal answer"
    «+ Check node status: kubectl get nodes 
    = > + Describe node: kubectl describe node <node-name> * Node lifecycle understanding
    + Check kubelet: journalctl -u kubelet -f * Kubelet & system-level debugging
    + Check node resource pressure (CPU/Memory/Disk/PID). * Resource pressure awareness
    + Verify network connectivity & CNI status. * CNI/network troubleshooting
    -9 + Drain the node if needed and fix the root cause. * Safe remediation approach
    © A: Pods are pending and not getting scheduled. Whet could be the reason end how do you fix iti?
    ANS: + Check events: kubectl get events --sort-by=.metadata.creationTimestramp 2 Khedalng "at sears |
    a | + Check node resources and quotas. Events analysis :
    . Verify node selectors, taints/tolerations, offinity/anti-affinity rules. * Resource & quota awareness
    + Check required PVCs, storage classes, limits, and namespaces. * Taints/tolerations & affinity
    + Fix constraints or scale the cluster / adjust configs. * Problem isolation skills
    Ss @)

**47. How do you design a system that can scale to millions of users?**

??? success "Reveal answer"
    + Use horizontal scaling (add more instances/containers). 1 Horizontal vs vertical sealing 4 _. hutto Sealing Group :
    +. + Auto Sealing Groups / Kubernetes HPA. Si Auslalig soaps | @-B-@- GBEB-)
    : + Use caching (Redis, ElastiCache, CDN). # Caching strategies <M _ “ete :
    =) + Database scaling: read replicas, sharding if needed. Database scaling bnouledge | 4
    Cahe
    -~ 5S 6-s28
    : " ness continuity?
    — ) (6)

**48. A new deployment was successful, but users are now facing errors. | How do you proceed?**

??? success "Reveal answer"
    ° Check application logs for exceptions and error patterns. * Fast but safe decision making
    x + Compare metrics (error rate, latency, throughput) with previous version. * Rollback strategy knowledge
    + Validate config, environment variables, feature flags, secrets. * Dependency awareness
    * Check dependencies (DB connections, cache, queues, external services). | . Balancing speed vs stability
    | + Rollback if needed to restore service quickly, then investigate. * Learn then fix approach
    OQ)

**49. How does Kubernetes handle storage?**

??? success "Reveal answer"
    PersistentVolumes represent actual durable storage resources in the cluster, PersistentVolumeClaims are requests
    from a Pod for storage matching certain criteria, and a StorageClass defines the type of storage -- SSD versus HDD,
    for instance -- enabling dynamic provisioning so a PV is created automatically to satisfy a PVC instead of needing to
    be pre-provisioned manually.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    2
    KUBERNETES ARCHITECTURE

**50. How do you ensure a deployment is zero-downtime?**

??? success "Reveal answer"
    + Use strategies like Blue/Green, Canary, or Rolling Update. * Zero downtime techniques
    + Ensure health checks, readiness/liveness probes are configured. * Health check & monitoring awareness
    + Use load balancers to route traffic during deployment. * Database change strategy
    + Maintain backward compatibility for DB schema changes. ® Risk mitigation |
    + Test in staging with production-like data before release. * Production best practices
    @

**51. How does Kubernetes handle scaling?**

??? success "Reveal answer"
    Manual scaling with kubectl scale to directly adjust replica count; Horizontal Pod Autoscaler, which automatically
    scales replica count based on CPU/memory or custom metrics; and Vertical Pod Autoscaler, which adjusts a Pod's
    resource requests and limits based on observed consumption rather than the number of replicas.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    3
    INGRESS CONTROLLER

**52. How do you handle subnetting in a Kubernetes environment?**

??? success "Reveal answer"
    Kubernetes needs CIDR ranges allocated for nodes, pods, and services, and getting that sizing right up front matters
    a lot because it's painful to change after the cluster is running -- I make sure the pod CIDR is large enough to support
    the cluster's eventual scale, since running out of pod IPs is a hard wall to hit later.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**53. Pod restarts intermittently with OOMKilled. How do you fix?**

??? success "Reveal answer"
    + Check pod logs and describe for OOMKilled reason. * Resource management knowledge
    + Check memory usage: kubectl top pod <pod-name> * Observability usage
    + Increase resources (requests/limits) approprately. * Right-sizing mindsst
    : > + Optimize application memory usage. * Monitoring & alerting
    + Add alerts for memory threshold breaches. as . * Root cause vs symptom focus s |
    ©

**54. How do you manage secrets for Kubernetes deployments in GitOps using GitHub Actions and ArgoCD?**

??? success "Reveal answer"
    GitHub Actions secrets handle anything the CI workflow itself needs, while in the cluster I use Sealed Secrets or
    HashiCorp Vault, or native Kubernetes Secret management, so actual secret values are never committed as
    plaintext into the Git repository ArgoCD is watching.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    6
    GITLAB

**55. How do you expose a Kubernetes application to external traffic?**

??? success "Reveal answer"
    A Service of type LoadBalancer provisions a cloud load balancer for the app; Ingress provides HTTP/HTTPS routing
    with support for features like SSL termination and host/path-based rules; and NodePort exposes the app on a static
    port on every node, which I mostly use for quick testing rather than production.

**56. How does Kubernetes networking work?**

??? success "Reveal answer"
    Kubernetes uses a flat network model where every Pod gets its own unique IP, and Pods can communicate across
    nodes without NAT. CNI plugins like Calico, Flannel, or Weave implement that connectivity, and kube-proxy on each
    node manages Service networking, routing traffic to the correct backing Pods.

**57. How do you use Python to interact with a Kubernetes cluster?**

??? success "Reveal answer"
    The official kubernetes Python client lets me load the kubeconfig and call the API directly -- listing pods in a
    namespace with v1.list_namespaced_pod(), for example -- which is also how I've built custom automation like scripts
    that find and report every pod stuck in a bad state across a cluster.

**58. Your Kubernetes cluster nodes are running at 90% memory. What do you do?**

??? success "Reveal answer"
    Immediate: 1) kubectl top pods --sort-by=memory — find memory hogs. 2) Check for 
    OOMKilled pods. 3) Scale up node group. Long-term: 4) Set proper resource requests/limits. 5) 
    Run VPA to get recommendations. 6) Enable Cluster Autoscaler. 7) Optimize application memory 
    usage.

**59. How does Kubernetes achieve high availability?**

??? success "Reveal answer"
    Multiple control plane nodes so losing one doesn't take down cluster management, a clustered, highly available etcd
    for consistent state and failover, and Pod replication across multiple worker nodes so a single node failure doesn't
    take a service down entirely.

**60. What does the Kubernetes Scheduler do?**

??? success "Reveal answer"
    The Scheduler assigns Pods to nodes, factoring in resource availability, node conditions, affinity/anti-affinity rules,
    and other constraints, aiming to distribute Pods efficiently across the cluster rather than overloading any single node.

## Related

- Course: [Kubernetes](../kubernetes/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
