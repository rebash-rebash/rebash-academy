"""Topic-specific Hands-on Lab and Interview Question banks.

Covers Kubernetes, Terraform, and Helm tutorial slugs for REBASH Academy enrichment.
Lab bodies use a ``{lab_dir}`` placeholder substituted by ``lab_for``.
"""

from __future__ import annotations

LABS_K8S: dict[str, str] = {
    'configmaps-and-secrets': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Inject configuration and secrets into Pods without baking them into images

### Step 1 – Create ConfigMap and Secret

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab create configmap app-config --from-literal=APP_ENV=lab --from-literal=LOG_LEVEL=info
kubectl -n rebash-lab create secret generic app-secret --from-literal=DB_PASSWORD='s3cret-lab'
kubectl -n rebash-lab get configmap,secret
```

### Step 2 – Mount them into a Pod and verify

```bash
cat > pod-config.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: cfg-demo
  namespace: rebash-lab
spec:
  containers:
  - name: demo
    image: busybox:1.36
    command: ["sh", "-c", "env | grep -E 'APP_|DB_|LOG_'; sleep 3600"]
    envFrom:
    - configMapRef:
        name: app-config
    - secretRef:
        name: app-secret
EOF
kubectl apply -f pod-config.yaml
kubectl -n rebash-lab wait --for=condition=Ready pod/cfg-demo --timeout=60s
kubectl -n rebash-lab exec cfg-demo -- sh -c 'env | grep -E "APP_|DB_|LOG_"'
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'deployments-managing-replicated-pods': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Roll out and scale a Deployment safely

### Step 1 – Create a Deployment and Service

```bash
kubectl create namespace rebash-lab
cat > deploy.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: rebash-lab
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
  namespace: rebash-lab
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
EOF
kubectl apply -f deploy.yaml
kubectl -n rebash-lab rollout status deploy/web
```

### Step 2 – Scale and perform a rolling update

```bash
kubectl -n rebash-lab scale deploy/web --replicas=3
kubectl -n rebash-lab set image deploy/web nginx=nginx:1.27
kubectl -n rebash-lab rollout status deploy/web
kubectl -n rebash-lab rollout history deploy/web
kubectl -n rebash-lab get pods -l app=web -o wide
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'gitops-and-cicd-with-kubernetes': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Treat cluster desired state as versioned manifests with a dry-run apply loop

### Step 1 – Initialise a GitOps-style manifest repo layout

```bash
kubectl create namespace rebash-lab
mkdir -p apps/demo overlays/lab
cat > apps/demo/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gitops-demo
  namespace: rebash-lab
  labels:
    app: gitops-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gitops-demo
  template:
    metadata:
      labels:
app: gitops-demo
    spec:
      containers:
      - name: nginx
image: nginx:1.27-alpine
EOF
cat > overlays/lab/kustomization.yaml <<'EOF'
resources:
  - ../../apps/demo/deployment.yaml
images:
  - name: nginx
    newTag: 1.27-alpine
EOF
git init -b main
git add apps overlays
git -c user.email=lab@rebash.local -c user.name=Lab commit -m "Add GitOps demo manifests"
```

### Step 2 – Apply from Git and verify drift detection habit

```bash
kubectl apply -k overlays/lab
kubectl -n rebash-lab rollout status deploy/gitops-demo
kubectl -n rebash-lab get deploy gitops-demo -o yaml | grep -A2 'image:'
# Simulate a CI check: render and diff without mutating the live cluster
kubectl diff -k overlays/lab || true
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'health-checks-probes-and-self-healing': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Configure liveness and readiness probes so Kubernetes restarts and unready Pods correctly

### Step 1 – Deploy an app with probes

```bash
kubectl create namespace rebash-lab
cat > probes.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: probe-demo
  namespace: rebash-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: probe-demo
  template:
    metadata:
      labels:
app: probe-demo
    spec:
      containers:
      - name: nginx
image: nginx:1.27-alpine
ports:
- containerPort: 80
readinessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 2
  periodSeconds: 5
livenessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 10
  periodSeconds: 10
EOF
kubectl apply -f probes.yaml
kubectl -n rebash-lab rollout status deploy/probe-demo
```

### Step 2 – Observe Ready condition and describe probe status

```bash
kubectl -n rebash-lab get pods -l app=probe-demo
kubectl -n rebash-lab describe pod -l app=probe-demo | sed -n '/Conditions:/,/Volumes:/p'
kubectl -n rebash-lab get pod -l app=probe-demo -o jsonpath='{.items[0].status.containerStatuses[0].ready}{"\n"}'
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'helm-package-management': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Install and inspect a Helm chart into a dedicated namespace (Helm from the Kubernetes track)

### Step 1 – Create a chart and template it

```bash
kubectl create namespace rebash-lab
helm create chart-demo
helm lint chart-demo
helm template chart-demo ./chart-demo -n rebash-lab --set replicaCount=1 | head -n 40
```

### Step 2 – Install, upgrade, and list the release

```bash
helm upgrade --install demo ./chart-demo -n rebash-lab --set replicaCount=2
helm -n rebash-lab list
kubectl -n rebash-lab get deploy,svc
helm -n rebash-lab get values demo
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-lab --ignore-not-found || true
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'ingress-and-external-access': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Expose HTTP traffic through an Ingress resource (controller optional)

### Step 1 – Deploy a backend and Ingress object

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab create deployment web --image=nginx:1.27-alpine
kubectl -n rebash-lab expose deployment web --port=80
cat > ingress.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
  namespace: rebash-lab
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: web.rebash.local
    http:
      paths:
      - path: /
pathType: Prefix
backend:
  service:
    name: web
    port:
      number: 80
EOF
kubectl apply -f ingress.yaml
```

### Step 2 – Validate Ingress wiring

```bash
kubectl -n rebash-lab get ingress web -o wide
kubectl -n rebash-lab describe ingress web
# If an Ingress controller is installed, ADDRESS will populate; otherwise the object still validates routing intent
kubectl -n rebash-lab get svc web endpoints
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'installing-kubernetes-and-kubectl': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Verify kubectl connectivity and cluster prerequisites

### Step 1 – Check client and cluster versions

```bash
kubectl version --client
kubectl config current-context
kubectl cluster-info
kubectl get nodes -o wide
```

### Step 2 – Create a smoke-test namespace and Pod

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab run smoke --image=busybox:1.36 --restart=Never --command -- echo 'cluster-ok'
kubectl -n rebash-lab wait --for=jsonpath='{.status.phase}'=Succeeded pod/smoke --timeout=60s || kubectl -n rebash-lab get pod smoke -o yaml
kubectl -n rebash-lab logs smoke
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'introduction-to-kubernetes-and-orchestration': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Run your first workload and contrast it with a single container process

### Step 1 – Create a namespace and run a Pod

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab run hello --image=nginx:1.27-alpine --port=80
kubectl -n rebash-lab wait --for=condition=Ready pod/hello --timeout=60s
kubectl -n rebash-lab get pods -o wide
```

### Step 2 – Inspect orchestration metadata

```bash
kubectl -n rebash-lab describe pod hello | head -n 40
kubectl -n rebash-lab get pod hello -o jsonpath='{.status.podIP}{"\n"}{.spec.nodeName}{"\n"}'
kubectl -n rebash-lab delete pod hello
# Note: a bare Pod is not recreated — Deployments restore desired replicas
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'kubectl-essentials-and-workflows': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Practise everyday kubectl workflows: get, describe, logs, exec, apply

### Step 1 – Apply a manifest and explore resources

```bash
kubectl create namespace rebash-lab
cat > app.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: tools
  namespace: rebash-lab
  labels:
    app: tools
spec:
  containers:
  - name: tools
    image: busybox:1.36
    command: ["sleep", "3600"]
EOF
kubectl apply -f app.yaml
kubectl -n rebash-lab get pods -l app=tools -o wide
kubectl -n rebash-lab describe pod tools | head -n 30
```

### Step 2 – Logs, exec, and output formats

```bash
kubectl -n rebash-lab exec tools -- uname -a
kubectl -n rebash-lab get pod tools -o yaml | head -n 20
kubectl -n rebash-lab get pod tools -o jsonpath='{.status.phase}{"\n"}'
kubectl api-resources | head -n 15
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'kubernetes-architecture-and-components': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Map control plane and node components from a live cluster

### Step 1 – Inspect nodes and system Pods

```bash
kubectl create namespace rebash-lab
kubectl get nodes -o custom-columns=NAME:.metadata.name,ROLES:.metadata.labels.node-role\.kubernetes\.io/control-plane,VERSION:.status.nodeInfo.kubeletVersion
kubectl get pods -n kube-system -o wide
kubectl get --raw /readyz?verbose | head -n 20 || true
```

### Step 2 – Identify API server and scheduling signals

```bash
kubectl cluster-info
kubectl get componentstatuses 2>/dev/null || kubectl get --raw /livez | head -c 200; echo
kubectl explain pod.spec.nodeName
kubectl -n rebash-lab run arch-probe --image=busybox:1.36 --restart=Never --command -- sleep 30
kubectl -n rebash-lab get pod arch-probe -o jsonpath='Node={.spec.nodeName} Phase={.status.phase}{"\n"}'
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'kubernetes-autoscaling': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Configure Horizontal Pod Autoscaler metrics wiring (metrics-server dependent)

### Step 1 – Deploy a CPU-requesting workload

```bash
kubectl create namespace rebash-lab
cat > hpa-app.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hpa-demo
  namespace: rebash-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hpa-demo
  template:
    metadata:
      labels:
app: hpa-demo
    spec:
      containers:
      - name: php-apache
image: registry.k8s.io/hpa-example
ports:
- containerPort: 80
resources:
  requests:
    cpu: 100m
    memory: 64Mi
EOF
kubectl apply -f hpa-app.yaml
kubectl -n rebash-lab expose deploy/hpa-demo --port=80
```

### Step 2 – Create an HPA and inspect status

```bash
kubectl -n rebash-lab autoscale deployment hpa-demo --cpu-percent=50 --min=1 --max=3
kubectl -n rebash-lab get hpa
kubectl -n rebash-lab describe hpa hpa-demo | head -n 40
# Without metrics-server, TARGETS may show <unknown>; install metrics-server for live CPU ratios
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'kubernetes-capstone-and-next-steps': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Assemble a miniature production-shaped stack: Deploy, Service, probes, and resources

### Step 1 – Apply a multi-resource application bundle

```bash
kubectl create namespace rebash-lab
cat > capstone.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shop
  namespace: rebash-lab
spec:
  replicas: 2
  selector:
    matchLabels:
      app: shop
  template:
    metadata:
      labels:
app: shop
    spec:
      containers:
      - name: web
image: nginx:1.27-alpine
ports:
- containerPort: 80
resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    memory: 128Mi
readinessProbe:
  httpGet:
    path: /
    port: 80
---
apiVersion: v1
kind: Service
metadata:
  name: shop
  namespace: rebash-lab
spec:
  selector:
    app: shop
  ports:
  - port: 80
EOF
kubectl apply -f capstone.yaml
kubectl -n rebash-lab rollout status deploy/shop
```

### Step 2 – Validate and document readiness for next learning

```bash
kubectl -n rebash-lab get deploy,svc,pods -o wide
kubectl -n rebash-lab get endpoints shop
cat > NOTES.md <<'EOF'
Capstone checklist: replicas ready, Service endpoints populated, probes green.
Next: GitOps, HPA, network policies, and managed Kubernetes offerings.
EOF
cat NOTES.md
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'kubernetes-networking-deep-dive': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Trace ClusterIP Service DNS and Pod-to-Pod connectivity

### Step 1 – Create two Pods and a Service

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab run server --image=nginx:1.27-alpine --port=80 --labels=app=server
kubectl -n rebash-lab expose pod server --port=80 --name=server
kubectl -n rebash-lab run client --image=busybox:1.36 --restart=Never --command -- sleep 3600
kubectl -n rebash-lab wait --for=condition=Ready pod/server pod/client --timeout=90s
```

### Step 2 – Resolve DNS and curl across the Service

```bash
kubectl -n rebash-lab get svc server -o wide
kubectl -n rebash-lab exec client -- nslookup server.rebash-lab.svc.cluster.local
kubectl -n rebash-lab exec client -- wget -qO- http://server.rebash-lab.svc.cluster.local/ | head -n 5
kubectl -n rebash-lab get endpoints server -o yaml | head -n 30
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'kubernetes-objects-labels-and-namespaces': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Organise objects with namespaces, labels, and selectors

### Step 1 – Create labelled resources

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab run api --image=nginx:1.27-alpine --labels=tier=frontend,env=lab
kubectl -n rebash-lab run worker --image=busybox:1.36 --labels=tier=backend,env=lab --command -- sleep 3600
kubectl -n rebash-lab label pod api owner=rebash --overwrite
kubectl -n rebash-lab get pods --show-labels
```

### Step 2 – Query with selectors and namespace scope

```bash
kubectl -n rebash-lab get pods -l tier=frontend
kubectl -n rebash-lab get pods -l 'env in (lab),tier!=frontend'
kubectl get ns rebash-lab -o yaml | head -n 20
kubectl -n rebash-lab get all
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'kubernetes-production-operations': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Practise operational hygiene: rollouts, events, and resource snapshots

### Step 1 – Deploy and capture operational baseline

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab create deployment ops --image=nginx:1.27-alpine --replicas=2
kubectl -n rebash-lab rollout status deploy/ops
kubectl -n rebash-lab get events --sort-by=.lastTimestamp | tail -n 15
```

### Step 2 – Perform a controlled change and inspect history

```bash
kubectl -n rebash-lab set resources deploy/ops -c=nginx --requests=cpu=50m,memory=64Mi
kubectl -n rebash-lab rollout status deploy/ops
kubectl -n rebash-lab rollout history deploy/ops
kubectl -n rebash-lab get deploy ops -o jsonpath='{.spec.template.spec.containers[0].resources}{"\n"}'
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'kubernetes-scheduling': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Influence placement with nodeSelector and observe the scheduler

### Step 1 – Inspect node labels and schedule a constrained Pod

```bash
kubectl create namespace rebash-lab
kubectl get nodes --show-labels | head -n 5
NODE=$(kubectl get nodes -o jsonpath='{.items[0].metadata.name}')
kubectl label node "$NODE" lab-role=demo --overwrite
cat > scheduled.yaml <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: pinned
  namespace: rebash-lab
spec:
  nodeSelector:
    lab-role: demo
  containers:
  - name: pause
    image: registry.k8s.io/pause:3.10
EOF
kubectl apply -f scheduled.yaml
kubectl -n rebash-lab wait --for=condition=Ready pod/pinned --timeout=60s
```

### Step 2 – Confirm placement and clean node label later

```bash
kubectl -n rebash-lab get pod pinned -o wide
kubectl -n rebash-lab describe pod pinned | sed -n '/Node-Selectors:/,/Tolerations:/p'
NODE=$(kubectl get nodes -l lab-role=demo -o jsonpath='{.items[0].metadata.name}')
echo "Scheduled on: $NODE"
```

### Final step – Cleanup note

```bash
NODE=$(kubectl get nodes -l lab-role=demo -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)
if [ -n "$NODE" ]; then kubectl label node "$NODE" lab-role-; fi
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'kubernetes-security-hardening': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Apply a Pod Security Context and non-root container settings

### Step 1 – Deploy a hardened Pod

```bash
kubectl create namespace rebash-lab
cat > hardened.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: hardened
  namespace: rebash-lab
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: busybox:1.36
    command: ["sh", "-c", "id; sleep 3600"]
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
drop: ["ALL"]
EOF
kubectl apply -f hardened.yaml
kubectl -n rebash-lab wait --for=condition=Ready pod/hardened --timeout=60s
```

### Step 2 – Verify identity and security fields

```bash
kubectl -n rebash-lab exec hardened -- id
kubectl -n rebash-lab get pod hardened -o jsonpath='{.spec.securityContext}{"\n"}'
kubectl -n rebash-lab get pod hardened -o jsonpath='{.spec.containers[0].securityContext}{"\n"}'
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'managed-kubernetes-eks-aks-gke': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Compare local cluster context with managed-Kubernetes operational checks (no paid cloud required)

### Step 1 – Document cluster identity and node pool shape

```bash
kubectl create namespace rebash-lab
kubectl config view --minify -o yaml | head -n 40
kubectl get nodes -o custom-columns=NAME:.metadata.name,INSTANCE:.metadata.labels.node\.kubernetes\.io/instance-type,ZONE:.metadata.labels.topology\.kubernetes\.io/zone
kubectl get ns kube-system -o jsonpath='{.metadata.annotations}{"\n"}' || true
```

### Step 2 – Run a portability smoke test as you would after attaching a managed cluster

```bash
kubectl -n rebash-lab run managed-smoke --image=busybox:1.36 --restart=Never --command -- echo ok-from-cluster
kubectl -n rebash-lab wait --for=jsonpath='{.status.phase}'=Succeeded pod/managed-smoke --timeout=60s
kubectl -n rebash-lab logs managed-smoke
cat > MANAGED_NOTES.md <<'EOF'
EKS/AKS/GKE differences to revisit: IAM mapping, CNI, load balancers, add-ons, upgrades.
This lab only validates kubectl access patterns that stay the same across providers.
EOF
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'monitoring-and-logging-in-kubernetes': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Collect Pod logs and basic resource signals for observability practice

### Step 1 – Generate log output from a Deployment

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab create deployment logger --image=busybox:1.36 --replicas=1 -- sleep 3600
kubectl -n rebash-lab wait --for=condition=Available deploy/logger --timeout=60s
POD=$(kubectl -n rebash-lab get pod -l app=logger -o jsonpath='{.items[0].metadata.name}')
kubectl -n rebash-lab exec "$POD" -- sh -c 'echo "$(date -Iseconds) lab-event" >> /tmp/app.log; cat /tmp/app.log'
# Container stdout is the usual log path — write a short message:
kubectl -n rebash-lab delete pod "$POD" --force --grace-period=0 2>/dev/null || true
kubectl -n rebash-lab set command deploy/logger -- sh -c 'while true; do echo "$(date -Iseconds) heartbeat"; sleep 5; done'
kubectl -n rebash-lab rollout status deploy/logger
```

### Step 2 – Tail logs and check metrics endpoints if present

```bash
kubectl -n rebash-lab logs deploy/logger --tail=20
kubectl top pods -n rebash-lab 2>/dev/null || echo "metrics-server not installed; logs still available via kubectl logs"
kubectl -n rebash-lab get events --field-selector involvedObject.kind=Pod --sort-by=.lastTimestamp | tail -n 10
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'namespaces-and-resource-management': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Isolate workloads and set namespace-level resource budgets

### Step 1 – Create namespace with ResourceQuota and LimitRange

```bash
kubectl create namespace rebash-lab
cat > budget.yaml <<'EOF'
apiVersion: v1
kind: ResourceQuota
metadata:
  name: lab-quota
  namespace: rebash-lab
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 1Gi
    pods: "10"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: lab-limits
  namespace: rebash-lab
spec:
  limits:
  - type: Container
    default:
      cpu: 100m
      memory: 128Mi
    defaultRequest:
      cpu: 50m
      memory: 64Mi
EOF
kubectl apply -f budget.yaml
kubectl -n rebash-lab describe resourcequota lab-quota
```

### Step 2 – Schedule a Pod and observe quota usage

```bash
kubectl -n rebash-lab run quota-pod --image=nginx:1.27-alpine
kubectl -n rebash-lab get pod quota-pod -o jsonpath='{.spec.containers[0].resources}{"\n"}'
kubectl -n rebash-lab describe resourcequota lab-quota
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'persistent-volumes-and-storage': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Claim storage with a PersistentVolumeClaim using the default StorageClass

### Step 1 – Create a PVC and mount it

```bash
kubectl create namespace rebash-lab
kubectl get storageclass
cat > pvc.yaml <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
  namespace: rebash-lab
spec:
  accessModes: ["ReadWriteOnce"]
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: writer
  namespace: rebash-lab
spec:
  containers:
  - name: app
    image: busybox:1.36
    command: ["sh", "-c", "echo hello-storage > /data/msg.txt; sleep 3600"]
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data
EOF
kubectl apply -f pvc.yaml
```

### Step 2 – Wait for Bound and read the file

```bash
kubectl -n rebash-lab get pvc data -w &
WPID=$!; sleep 8; kill $WPID 2>/dev/null || true
kubectl -n rebash-lab get pvc,pv
kubectl -n rebash-lab wait --for=condition=Ready pod/writer --timeout=120s || kubectl -n rebash-lab describe pod writer
kubectl -n rebash-lab exec writer -- cat /data/msg.txt
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'platform-engineering-on-kubernetes': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Package a golden-path Deployment template teams can reuse

### Step 1 – Create a reusable base manifest set

```bash
kubectl create namespace rebash-lab
mkdir -p platform/base
cat > platform/base/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: TEAM_APP
  namespace: rebash-lab
  labels:
    platform.rebash.ai/tier: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: TEAM_APP
  template:
    metadata:
      labels:
app: TEAM_APP
    spec:
      containers:
      - name: app
image: nginx:1.27-alpine
resources:
  requests:
    cpu: 50m
    memory: 64Mi
EOF
sed 's/TEAM_APP/payments/g' platform/base/deployment.yaml > payments.yaml
kubectl apply -f payments.yaml
kubectl -n rebash-lab rollout status deploy/payments
```

### Step 2 – Validate platform labels and self-service checklist

```bash
kubectl -n rebash-lab get deploy payments --show-labels
kubectl -n rebash-lab get deploy payments -o jsonpath='{.spec.template.spec.containers[0].resources}{"\n"}'
cat > platform/CHECKLIST.md <<'EOF'
Golden path: namespace, requests/limits, labels, probes, non-root (next iteration).
EOF
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'pods-the-atomic-unit': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Understand Pod lifecycle, multi-container patterns, and IP identity

### Step 1 – Create a multi-container Pod sharing a volume

```bash
kubectl create namespace rebash-lab
cat > pod.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: atomic
  namespace: rebash-lab
spec:
  containers:
  - name: writer
    image: busybox:1.36
    command: ["sh", "-c", "echo from-writer > /shared/note; sleep 3600"]
    volumeMounts:
    - name: shared
      mountPath: /shared
  - name: reader
    image: busybox:1.36
    command: ["sh", "-c", "sleep 2; cat /shared/note; sleep 3600"]
    volumeMounts:
    - name: shared
      mountPath: /shared
  volumes:
  - name: shared
    emptyDir: {}
EOF
kubectl apply -f pod.yaml
kubectl -n rebash-lab wait --for=condition=Ready pod/atomic --timeout=60s
```

### Step 2 – Inspect shared network and volume

```bash
kubectl -n rebash-lab logs atomic -c reader
kubectl -n rebash-lab get pod atomic -o jsonpath='PodIP={.status.podIP}{"\n"}'
kubectl -n rebash-lab exec atomic -c writer -- ls -l /shared
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'production-kubernetes-excellence': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Apply production defaults: requests, probes, and disruption-aware replica count

### Step 1 – Deploy with production-minded fields

```bash
kubectl create namespace rebash-lab
cat > prod.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prod-web
  namespace: rebash-lab
spec:
  replicas: 3
  selector:
    matchLabels:
      app: prod-web
  template:
    metadata:
      labels:
app: prod-web
    spec:
      containers:
      - name: nginx
image: nginx:1.27-alpine
ports:
- containerPort: 80
resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    memory: 128Mi
readinessProbe:
  httpGet: {path: /, port: 80}
  periodSeconds: 5
livenessProbe:
  httpGet: {path: /, port: 80}
  periodSeconds: 10
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: prod-web
  namespace: rebash-lab
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: prod-web
EOF
kubectl apply -f prod.yaml
kubectl -n rebash-lab rollout status deploy/prod-web
```

### Step 2 – Validate excellence checklist

```bash
kubectl -n rebash-lab get deploy,pdb
kubectl -n rebash-lab get pods -l app=prod-web -o wide
kubectl -n rebash-lab describe pdb prod-web | head -n 25
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'production-patterns-hpa-pdb-and-affinity': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Combine PDB and pod anti-affinity for resilient scheduling

### Step 1 – Deploy with anti-affinity and PDB

```bash
kubectl create namespace rebash-lab
cat > patterns.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resilient
  namespace: rebash-lab
spec:
  replicas: 2
  selector:
    matchLabels:
      app: resilient
  template:
    metadata:
      labels:
app: resilient
    spec:
      affinity:
podAntiAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
  - weight: 100
    podAffinityTerm:
      labelSelector:
matchLabels:
  app: resilient
      topologyKey: kubernetes.io/hostname
      containers:
      - name: nginx
image: nginx:1.27-alpine
resources:
  requests:
    cpu: 50m
    memory: 64Mi
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: resilient
  namespace: rebash-lab
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: resilient
EOF
kubectl apply -f patterns.yaml
kubectl -n rebash-lab rollout status deploy/resilient
```

### Step 2 – Inspect placement and disruption budget

```bash
kubectl -n rebash-lab get pods -l app=resilient -o wide
kubectl -n rebash-lab get pdb resilient -o yaml | head -n 30
kubectl -n rebash-lab describe deploy resilient | sed -n '/Affinity:/,/Containers:/p'
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'rbac-and-kubernetes-security-basics': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Grant least-privilege access with Role and RoleBinding

### Step 1 – Create a ServiceAccount and Role

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab create serviceaccount app-sa
cat > rbac.yaml <<'EOF'
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: rebash-lab
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-sa-pod-reader
  namespace: rebash-lab
subjects:
- kind: ServiceAccount
  name: app-sa
  namespace: rebash-lab
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-reader
EOF
kubectl apply -f rbac.yaml
```

### Step 2 – Verify authorisation with kubectl auth can-i

```bash
kubectl -n rebash-lab auth can-i list pods --as=system:serviceaccount:rebash-lab:app-sa
kubectl -n rebash-lab auth can-i delete pods --as=system:serviceaccount:rebash-lab:app-sa
kubectl -n rebash-lab get role,rolebinding
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'resource-quotas-and-limit-ranges': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Enforce hard quotas and default container limits

### Step 1 – Apply quota objects

```bash
kubectl create namespace rebash-lab
cat > limits.yaml <<'EOF'
apiVersion: v1
kind: LimitRange
metadata:
  name: defaults
  namespace: rebash-lab
spec:
  limits:
  - type: Container
    max:
      memory: 256Mi
    default:
      memory: 128Mi
    defaultRequest:
      memory: 64Mi
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: hard
  namespace: rebash-lab
spec:
  hard:
    requests.memory: 512Mi
    limits.memory: 1Gi
    pods: "5"
EOF
kubectl apply -f limits.yaml
```

### Step 2 – Admit a Pod and attempt an oversize request

```bash
kubectl -n rebash-lab run ok --image=nginx:1.27-alpine
kubectl -n rebash-lab get pod ok -o jsonpath='{.spec.containers[0].resources}{"\n"}'
kubectl -n rebash-lab run too-big --image=nginx:1.27-alpine --overrides='{"spec":{"containers":[{"name":"too-big","image":"nginx:1.27-alpine","resources":{"limits":{"memory":"512Mi"}}}]}}' 2>&1 || true
kubectl -n rebash-lab describe resourcequota hard
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'services-and-cluster-networking': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Expose Pods via ClusterIP and exercise Service selectors

### Step 1 – Create Deployment and Service

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab create deployment svc-demo --image=nginx:1.27-alpine --replicas=2
kubectl -n rebash-lab expose deployment svc-demo --port=80 --target-port=80 --name=svc-demo
kubectl -n rebash-lab get svc svc-demo -o wide
kubectl -n rebash-lab get endpoints svc-demo
```

### Step 2 – Test Service DNS from another Pod

```bash
kubectl -n rebash-lab run curl --image=busybox:1.36 --restart=Never --command -- sleep 3600
kubectl -n rebash-lab wait --for=condition=Ready pod/curl --timeout=60s
kubectl -n rebash-lab exec curl -- wget -qO- http://svc-demo/ | head -n 3
kubectl -n rebash-lab describe svc svc-demo | sed -n '/Selector:/,/Session Affinity:/p'
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'troubleshooting-kubernetes-workloads': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Diagnose a failing Pod using describe, logs, and events

### Step 1 – Create a broken Pod on purpose

```bash
kubectl create namespace rebash-lab
cat > broken.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: broken
  namespace: rebash-lab
spec:
  containers:
  - name: app
    image: nginx:1.27-alpine
    command: ["/bin/false"]
EOF
kubectl apply -f broken.yaml
sleep 5
kubectl -n rebash-lab get pod broken
```

### Step 2 – Trace the failure and fix it

```bash
kubectl -n rebash-lab describe pod broken | sed -n '/Events:/,$p'
kubectl -n rebash-lab logs broken || true
kubectl -n rebash-lab delete pod broken
kubectl -n rebash-lab run fixed --image=nginx:1.27-alpine
kubectl -n rebash-lab wait --for=condition=Ready pod/fixed --timeout=60s
kubectl -n rebash-lab get pod fixed
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'workload-controllers-statefulset-daemonset-jobs': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Run Job, DaemonSet, and StatefulSet controller patterns

### Step 1 – Create a Job and DaemonSet

```bash
kubectl create namespace rebash-lab
cat > controllers.yaml <<'EOF'
apiVersion: batch/v1
kind: Job
metadata:
  name: hello-job
  namespace: rebash-lab
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: hello
image: busybox:1.36
command: ["echo", "job-complete"]
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-agent
  namespace: rebash-lab
spec:
  selector:
    matchLabels:
      app: node-agent
  template:
    metadata:
      labels:
app: node-agent
    spec:
      containers:
      - name: pause
image: registry.k8s.io/pause:3.10
EOF
kubectl apply -f controllers.yaml
kubectl -n rebash-lab wait --for=condition=Complete job/hello-job --timeout=60s
```

### Step 2 – Add a simple StatefulSet and compare identities

```bash
kubectl -n rebash-lab logs job/hello-job
kubectl -n rebash-lab get ds node-agent -o wide
cat > sts.yaml <<'EOF'
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: store
  namespace: rebash-lab
spec:
  serviceName: store
  replicas: 2
  selector:
    matchLabels:
      app: store
  template:
    metadata:
      labels:
app: store
    spec:
      containers:
      - name: nginx
image: nginx:1.27-alpine
EOF
kubectl apply -f sts.yaml
kubectl -n rebash-lab get pods -l app=store -o wide
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
}

IQ_K8S: dict[str, str] = {
    'configmaps-and-secrets': '''1. What is the difference between a ConfigMap and a Secret in Kubernetes?
2. How can applications consume ConfigMap and Secret data at runtime?
3. What happens to running Pods when you update a ConfigMap that is mounted as a volume?
4. Why should Secrets not be treated as strong encryption at rest by default, and what controls improve their security?
5. When would you prefer environment variables versus volume mounts for configuration?

!!! tip "Sample answer — question 2"
    Applications can inject keys as environment variables, mount them as files via volumes, or use the Kubernetes API. Environment variables suit simple scalars; volume mounts suit files and live updates for many volume-mounted ConfigMaps.

!!! tip "Sample answer — question 4"
    etcd may store Secrets only base64-encoded unless encryption at rest is enabled. Improve security with encryption providers, least-privilege RBAC, external secret managers, short-lived credentials, and avoiding logging Secret values.
''',
    'deployments-managing-replicated-pods': '''1. What problem does a Deployment solve compared with creating Pods directly?
2. How does a rolling update differ from a recreate strategy?
3. What does `kubectl rollout undo` do, and when would you use it?
4. How do readiness probes interact with a Deployment rollout, and what risk appears if they are missing?
5. Explain the relationship between Deployment, ReplicaSet, and Pod.

!!! tip "Sample answer — question 2"
    A rolling update gradually replaces Pods with a new ReplicaSet while keeping capacity available. A recreate strategy terminates old Pods first, causing downtime but avoiding mixed versions.

!!! tip "Sample answer — question 4"
    Without readiness probes, new Pods may receive traffic before they can serve it, causing errors during rollouts. Probes gate Endpoints so only ready Pods join the Service.
''',
    'gitops-and-cicd-with-kubernetes': '''1. What is GitOps in the context of Kubernetes delivery?
2. Why is the Git repository treated as the source of truth rather than imperative kubectl changes?
3. What is the difference between push-based CI deploy jobs and pull-based GitOps agents?
4. What security trade-offs exist when CI pipelines hold kubeconfig credentials versus a cluster-side reconciler?
5. How do you detect and remediate configuration drift?

!!! tip "Sample answer — question 2"
    Git records the desired state, enabling review, audit, and rollback through normal version control. Imperative cluster edits are easy to lose and hard to reproduce across environments.

!!! tip "Sample answer — question 4"
    CI push models concentrate powerful credentials in the pipeline. Pull-based controllers keep credentials in-cluster with narrower RBAC, reducing blast radius if the CI system is compromised, at the cost of another in-cluster component to operate.
''',
    'health-checks-probes-and-self-healing': '''1. What is the difference between liveness, readiness, and startup probes?
2. What does Kubernetes do when a liveness probe fails repeatedly?
3. When should you use a startup probe instead of a long initialDelaySeconds on liveness?
4. How can aggressive probes harm availability, and how do you tune them safely?
5. Why is a readiness probe essential for Services during rollouts?

!!! tip "Sample answer — question 2"
    Repeated liveness failures cause the kubelet to restart the container. This recovers stuck processes but cannot fix application bugs that crash-loop immediately.

!!! tip "Sample answer — question 4"
    Probes that are too frequent or too strict can kill healthy Pods under load or remove them from Service prematurely. Tune thresholds with realistic timeouts, failure thresholds, and separate readiness from liveness semantics.
''',
    'helm-package-management': '''1. What is a Helm chart, and what problem does it solve?
2. What is the difference between `helm install` and `helm upgrade --install`?
3. Where does Helm store release metadata in modern Helm 3?
4. What risks come from installing charts with default values in production?
5. How do values files help manage environment differences?

!!! tip "Sample answer — question 2"
    `helm upgrade --install` creates the release if missing or upgrades it if present, which is convenient for CI idempotency. Plain `helm install` fails if the release already exists.

!!! tip "Sample answer — question 4"
    Default values often enable broad permissions, public images, or weak resource settings. Production needs reviewed values, pinned versions, least privilege, and secret handling outside plain values where possible.
''',
    'ingress-and-external-access': '''1. What does an Ingress resource declare, and what still needs to exist for traffic to flow?
2. How does Ingress differ from a Service of type LoadBalancer?
3. What is pathType Prefix versus Exact?
4. What security controls should sit in front of Ingress-exposed applications?
5. Why might an Ingress show no ADDRESS even though the object is valid?

!!! tip "Sample answer — question 2"
    Ingress describes HTTP routing rules. A controller must implement them, and backends must be Ready Service Endpoints. Without a controller, the object alone does not open traffic.

!!! tip "Sample answer — question 4"
    Exposing HTTP needs TLS, authentication where appropriate, WAF or rate limiting, network policies, and careful host/path design so internal apps are not accidentally public.
''',
    'installing-kubernetes-and-kubectl': '''1. What components must be reachable for kubectl to manage a cluster?
2. What does kubeconfig contain, and why should it be protected?
3. How do you verify that your client can authenticate to the API server?
4. What are the risks of using an admin kubeconfig on a shared workstation?
5. Name two common local cluster options for learning Kubernetes.

!!! tip "Sample answer — question 2"
    Run `kubectl cluster-info` or `kubectl get nodes`. Success shows credentials and network path to the API server work. Failures usually indicate wrong context, expired tokens, or network blocks.

!!! tip "Sample answer — question 4"
    Admin kubeconfigs grant cluster-wide power. On shared machines they risk credential theft and accidental destructive commands. Prefer short-lived credentials, least privilege, and separate contexts per environment.
''',
    'introduction-to-kubernetes-and-orchestration': '''1. What problem does container orchestration solve beyond running a single container?
2. What is a Pod, and why is it the smallest deployable unit?
3. How does desired state reconciliation differ from imperative scripting?
4. What operational risks appear if you only run containers with Docker on one host in production?
5. Name three capabilities Kubernetes provides out of the box for applications.

!!! tip "Sample answer — question 2"
    A Pod is one or more containers sharing network and storage namespaces. Kubernetes schedules and restarts Pods as units, so the Pod—not the container—is the atomic deployable object.

!!! tip "Sample answer — question 4"
    A single host lacks automated rescheduling, rolling updates, and cluster-wide service discovery. Failures of that host take everything down, and scaling is manual and error-prone.
''',
    'kubectl-essentials-and-workflows': '''1. What is the difference between imperative kubectl run and declarative kubectl apply?
2. When should you use `kubectl describe` versus `kubectl logs`?
3. How do labels and selectors help day-to-day operations?
4. Why is applying manifests from version control safer than one-off imperative edits?
5. What does `--dry-run=client` help you validate?

!!! tip "Sample answer — question 2"
    describe shows object state, events, and configuration; logs show container stdout/stderr. Use describe for scheduling and probe issues, logs for application errors.

!!! tip "Sample answer — question 4"
    Git-backed manifests give review, history, and repeatable environments. Imperative edits drift from documented intent and are hard to audit after incidents.
''',
    'kubernetes-architecture-and-components': '''1. What are the main control plane components of Kubernetes?
2. What is the role of kubelet versus kube-proxy on a node?
3. Where does etcd fit, and why is its health critical?
4. How does a highly available control plane change failure domains compared with a single API server?
5. What is the scheduler responsible for?

!!! tip "Sample answer — question 2"
    kubelet ensures Pod specs assigned to the node are running and reports status. kube-proxy programmes Service networking rules (or relies on equivalent dataplane) so ClusterIP traffic reaches Pods.

!!! tip "Sample answer — question 4"
    Multiple API server and etcd members reduce single points of failure, but you must still plan for quorum, load balancing, and zone-aware placement so correlated failures do not take the whole control plane down.
''',
    'kubernetes-autoscaling': '''1. What does the Horizontal Pod Autoscaler adjust?
2. Why do resource requests matter for CPU-based HPA?
3. What is the difference between HPA and Cluster Autoscaler?
4. What risks arise from autoscaling without PodDisruptionBudgets and readiness probes?
5. When would you choose custom metrics over CPU utilisation?

!!! tip "Sample answer — question 2"
    HPA scales Pod replica counts from metrics. Requests define the baseline for utilisation percentages; without requests, CPU targets are unreliable or unavailable.

!!! tip "Sample answer — question 4"
    Rapid scale-down can terminate Pods mid-request if PDBs and readiness are weak. Scale-up can overwhelm dependencies. Pair HPA with sensible limits, PDBs, and dependency capacity planning.
''',
    'kubernetes-capstone-and-next-steps': '''1. Which Kubernetes primitives form a minimal production-ready web service?
2. How would you decide the next skills to learn after core workloads?
3. What evidence shows a Deployment is healthy beyond Pods being Running?
4. What security baseline would you require before calling a cluster production-ready?
5. How do managed Kubernetes services change what you operate versus what the vendor operates?

!!! tip "Sample answer — question 2"
    Ready replicas, passing probes, populated Endpoints, and recent events without CrashLoopBackOff are stronger signals than phase Running alone.

!!! tip "Sample answer — question 4"
    Production readiness needs RBAC least privilege, network policy, secret hygiene, resource requests, observability, backup/upgrade plans, and restricted privileged workloads—not only green Deployments.
''',
    'kubernetes-networking-deep-dive': '''1. How does Pod networking typically work regarding IP addresses?
2. How does CoreDNS resolve a Service name inside a cluster?
3. What is the difference between ClusterIP, NodePort, and LoadBalancer?
4. How can NetworkPolicy restrict east-west traffic, and what must the CNI support?
5. What symptoms suggest a CNI or kube-proxy problem rather than an application bug?

!!! tip "Sample answer — question 2"
    Services get a stable DNS name like `name.namespace.svc.cluster.local` that resolves to the ClusterIP. kube-dns/CoreDNS answers these queries for in-cluster clients.

!!! tip "Sample answer — question 4"
    NetworkPolicy only enforces if the CNI implements it. Policies default-deny unused paths, allow needed namespaces/pods/ports, and should be tested so you do not lock out DNS or probes accidentally.
''',
    'kubernetes-objects-labels-and-namespaces': '''1. What is a Kubernetes namespace used for?
2. How do labels differ from annotations?
3. How do selectors use labels to group Pods for Services and Deployments?
4. What security benefit do namespaces provide, and what do they not isolate by themselves?
5. Give an example of a useful label taxonomy for multi-team clusters.

!!! tip "Sample answer — question 2"
    Labels are identifying metadata for selection; annotations hold non-identifying tool or descriptive data. Controllers and Services select on labels, not annotations.

!!! tip "Sample answer — question 4"
    Namespaces scope names and RBAC subjects, but they do not provide network or node isolation alone. Combine with NetworkPolicy, quotas, and Pod security controls for stronger tenancy.
''',
    'kubernetes-production-operations': '''1. What operational signals do you check first when a Deployment misbehaves?
2. How do you perform a safe configuration change in production?
3. What is the value of recording rollout history?
4. How do you balance change velocity with change safety in a shared cluster?
5. Which cluster upgrades are typically your responsibility on a managed service?

!!! tip "Sample answer — question 2"
    Prefer declarative apply, staged environments, rollouts with probes, and quick rollback via rollout undo. Avoid unreviewed imperative edits on live production objects.

!!! tip "Sample answer — question 4"
    Use progressive delivery, RBAC separation, quotas, PDBs, and change windows for risky work. Automate checks so velocity does not skip validation.
''',
    'kubernetes-scheduling': '''1. What inputs does the kube-scheduler consider when placing a Pod?
2. What is the difference between nodeSelector and node affinity?
3. When would you use taints and tolerations?
4. How can poor affinity rules reduce utilisation or availability?
5. What does Pending with FailedScheduling usually indicate?

!!! tip "Sample answer — question 2"
    nodeSelector is a simple required label match. Node affinity supports required/preferred rules and richer operators, giving more expressive placement control.

!!! tip "Sample answer — question 4"
    Overly strict anti-affinity or scarce node labels can leave Pods Pending or pack unevenly. Preferred rules soften constraints; required rules must match capacity planning.
''',
    'kubernetes-security-hardening': '''1. What does a Pod securityContext control?
2. Why drop Linux capabilities and disable privilege escalation?
3. What is the purpose of readOnlyRootFilesystem?
4. How do admission policies complement runtime securityContext settings?
5. What is a practical hardening checklist for a typical web Deployment?

!!! tip "Sample answer — question 2"
    Dropping capabilities and setting allowPrivilegeEscalation false reduce the blast radius if a process is compromised, preventing easy root or capability grabs inside the container.

!!! tip "Sample answer — question 4"
    Admission policies enforce organisational baselines so individual manifests cannot opt into privileged mode. Runtime settings protect each Pod; admission makes the standard mandatory.
''',
    'managed-kubernetes-eks-aks-gke': '''1. What responsibilities typically remain with you on a managed Kubernetes service?
2. How does cloud IAM integration differ across EKS, AKS, and GKE at a high level?
3. Why pin node image/version upgrade strategies even when the control plane is managed?
4. What vendor lock-in trade-offs appear when using cloud-specific Ingress or identity add-ons?
5. How do you validate portability of an application across managed offerings?

!!! tip "Sample answer — question 2"
    You still own workloads, RBAC inside the cluster, networking design, upgrades of node pools, add-ons you install, and cost. The vendor usually operates the control plane API servers and etcd.

!!! tip "Sample answer — question 4"
    Cloud-native LB annotations and IAM roles simplify ops but couple manifests to one provider. Prefer portable core APIs where possible, and isolate provider-specific resources behind modules.
''',
    'monitoring-and-logging-in-kubernetes': '''1. Where do container logs go by default on a node?
2. How does `kubectl logs` retrieve application output?
3. What cluster components are needed for `kubectl top` to work?
4. What privacy and security concerns apply to centralised log pipelines?
5. How would you alert on CrashLoopBackOff versus high latency?

!!! tip "Sample answer — question 2"
    kubectl logs reads the container runtime log stream for a Pod/container via the API server and kubelet. It shows stdout/stderr, not arbitrary files inside the filesystem unless you exec.

!!! tip "Sample answer — question 4"
    Logs may contain secrets, personal data, or tokens. Scrub sensitive fields, encrypt in transit and at rest, restrict access, and set retention aligned with compliance.
''',
    'namespaces-and-resource-management': '''1. How do ResourceQuota and LimitRange differ?
2. What happens when a new Pod would exceed a ResourceQuota?
3. Why set default requests via LimitRange?
4. How can quotas be abused or misconfigured to cause denial of service for a team?
5. When would you use multiple namespaces per team versus one shared namespace?

!!! tip "Sample answer — question 2"
    Admission rejects Pods that would break the quota. Teams see create failures until they free capacity or request a quota increase.

!!! tip "Sample answer — question 4"
    Quotas that are too tight block legitimate work; quotas that are too loose allow noisy neighbours. Review usage, set fair shares, and separate critical platforms into their own namespaces.
''',
    'persistent-volumes-and-storage': '''1. What is the relationship between PersistentVolume, PersistentVolumeClaim, and StorageClass?
2. What does the Bound phase on a PVC mean?
3. What is the difference between ReadWriteOnce and ReadWriteMany?
4. What data-loss risks exist when deleting PVCs, and how do reclaim policies affect them?
5. Why are StatefulSets often paired with volumeClaimTemplates?

!!! tip "Sample answer — question 2"
    Bound means a PV has been allocated to the claim and is ready to mount. Until Bound, Pods needing the volume may stay Pending.

!!! tip "Sample answer — question 4"
    Deleting a PVC can delete underlying storage depending on reclaim policy (Delete vs Retain). Snapshot and backup strategies matter before destructive cleanup in production.
''',
    'platform-engineering-on-kubernetes': '''1. What is a golden path in platform engineering?
2. How do templates or Helm charts reduce cognitive load for product teams?
3. What should a platform expose as self-service versus keep as a ticket?
4. How do you prevent golden paths from becoming unchangeable constraints?
5. Which Kubernetes APIs commonly underpin an internal developer platform?

!!! tip "Sample answer — question 2"
    Golden paths encode defaults for Deployments, networking, observability, and security so teams ship without reinventing cluster details.

!!! tip "Sample answer — question 4"
    Offer escape hatches, versioned templates, and feedback loops. Rigid platforms that block legitimate needs drive shadow IT; measure adoption and iterate with users.
''',
    'pods-the-atomic-unit': '''1. Why can containers in a Pod share localhost and volumes?
2. When should you use multiple containers in one Pod versus separate Pods?
3. What happens to a Pod IP when the Pod is recreated?
4. What security implication follows from containers sharing a network namespace?
5. What is an init container used for?

!!! tip "Sample answer — question 2"
    Sidecars suit tightly coupled helpers (proxy, log shipper) that must share lifecycle and network. Independent scaling or failure domains belong in separate Pods behind Services.

!!! tip "Sample answer — question 4"
    Shared network namespaces mean any container can bind ports and talk over localhost; a compromised sidecar can reach the app. Keep images minimal and apply strict securityContext settings.
''',
    'production-kubernetes-excellence': '''1. List five controls you expect on a production Deployment.
2. How do PodDisruptionBudgets protect availability during node drains?
3. Why are resource requests required for reliable scheduling and HPA?
4. What trade-off exists between many small clusters and one large multi-tenant cluster?
5. How do you validate excellence continuously after the first go-live?

!!! tip "Sample answer — question 2"
    PDBs limit voluntary disruptions so drains and upgrades cannot take too many Pods down at once, preserving minAvailable or maxUnavailable guarantees.

!!! tip "Sample answer — question 4"
    Multi-tenant clusters improve density but need stronger isolation and governance. Many clusters improve blast-radius isolation at higher operational and cost overhead.
''',
    'production-patterns-hpa-pdb-and-affinity': '''1. How do HPA and PDB interact during scale-down and node drains?
2. What is preferred versus required pod anti-affinity?
3. When is topology spread constraints a better fit than anti-affinity?
4. What failure mode appears if minAvailable is higher than current Ready replicas?
5. How would you place replicas across zones for a critical Service?

!!! tip "Sample answer — question 2"
    Preferred anti-affinity soft-scores placement; required rules block scheduling if unsatisfied. Preferred is safer when node count is small.

!!! tip "Sample answer — question 4"
    If minAvailable exceeds Ready Pods, voluntary disruptions are blocked and drains can stall. Keep PDB aligned with actual replica counts and readiness.
''',
    'rbac-and-kubernetes-security-basics': '''1. What are Role, ClusterRole, RoleBinding, and ClusterRoleBinding?
2. How do you test whether a ServiceAccount can list Pods in a namespace?
3. Why prefer RoleBinding in a single namespace over ClusterRoleBinding?
4. What is the danger of binding users to cluster-admin for convenience?
5. How should applications authenticate to the API from inside a Pod?

!!! tip "Sample answer — question 2"
    Use `kubectl auth can-i` with `--as=system:serviceaccount:ns:name` to evaluate RBAC without guessing. It reflects the authorisation rules currently applied.

!!! tip "Sample answer — question 4"
    cluster-admin bypasses least privilege and turns any credential leak into full cluster compromise. Scope Roles narrowly and use Just-In-Time elevation where possible.
''',
    'resource-quotas-and-limit-ranges': '''1. What fields commonly appear under ResourceQuota hard limits?
2. How does LimitRange set defaults differently from forcing every manifest to declare resources?
3. Can a LimitRange max block a Pod that a quota would otherwise allow?
4. How do memory limits interact with OOMKilled behaviour?
5. What governance process should surround quota changes?

!!! tip "Sample answer — question 2"
    LimitRange can inject default request/limit values at admission, reducing boilerplate while still enforcing maxima. Teams can override within allowed bounds.

!!! tip "Sample answer — question 4"
    Exceeding a memory limit triggers OOMKill of the container. Set limits from observed usage plus headroom; too low causes restarts, too high wastes node capacity.
''',
    'services-and-cluster-networking': '''1. What does a ClusterIP Service provide to clients?
2. How do Service selectors relate to Pod labels?
3. What are Endpoints or EndpointSlices used for?
4. What happens if no Pods match a Service selector?
5. When would you use a headless Service?

!!! tip "Sample answer — question 2"
    Selectors must match Pod labels for Endpoints to populate. Mismatched labels are a common reason Services exist but receive no backends.

!!! tip "Sample answer — question 4"
    With no matching Ready Pods, the Service still has a ClusterIP but no backends, so connections fail. Check selectors, readiness, and EndpointSlices when debugging.
''',
    'troubleshooting-kubernetes-workloads': '''1. What is a sensible first triage order for a failing Pod?
2. How do you distinguish ImagePullBackOff from CrashLoopBackOff?
3. Which kubectl commands help most during an incident?
4. How can excessive logging or exec debugging create security risk during outages?
5. What cluster-level checks do you add if many Pods fail at once?

!!! tip "Sample answer — question 2"
    ImagePullBackOff means the image cannot be fetched; CrashLoopBackOff means the container starts then exits. describe events and logs separate registry issues from application failures.

!!! tip "Sample answer — question 4"
    Incident shells and dumped env may expose secrets. Prefer controlled debug containers, redacted logs, and audited break-glass access rather than unrestricted exec everywhere.
''',
    'workload-controllers-statefulset-daemonset-jobs': '''1. When should you choose StatefulSet over Deployment?
2. What guarantees does a DaemonSet provide?
3. How does a Job differ from a Deployment?
4. What risk exists if a Job without backoff limits keeps failing?
5. Why do StatefulSets often need an associated headless Service?

!!! tip "Sample answer — question 2"
    DaemonSets run a Pod on each matching node—ideal for agents and CNI helpers. They are not for horizontally scaled user apps that should float across nodes.

!!! tip "Sample answer — question 4"
    Failing Jobs can consume cluster capacity with retries. Set backoffLimit, activeDeadlineSeconds, and alerts so broken batch work cannot starve other workloads.
''',
}

LABS_TF: dict[str, str] = {
    'data-sources-and-existing-infrastructure': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Read existing data with data sources alongside managed resources

### Step 1 – Create a file then read it back via data source

```bash
echo 'existing-seed' > seed.txt
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
data "local_file" "seed" {
  filename = "${path.module}/seed.txt"
}
resource "local_file" "copy" {
  filename = "${path.module}/copy.txt"
  content  = "copied:${data.local_file.seed.content}"
}
output "seed_content" {
  value = data.local_file.seed.content
}
EOF
terraform init
```

### Step 2 – Apply and confirm data was read, not created by Terraform

```bash
terraform apply -auto-approve
terraform output seed_content
cat copy.txt
terraform state list
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'format-validate-and-terraform-test': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Run fmt, validate, and a simple terraform test

### Step 1 – Create configuration and a test file

```bash
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
variable "prefix" {
  type = string
}
resource "local_file" "out" {
  filename = "${path.module}/${var.prefix}.txt"
  content  = var.prefix
}
EOF
mkdir -p tests
cat > tests/basic.tftest.hcl <<'EOF'
run "applies_with_prefix" {
  command = apply
  variables {
    prefix = "ok"
  }
  assert {
    condition     = local_file.out.content == "ok"
    error_message = "content should match prefix"
  }
}
EOF
terraform init
terraform fmt
terraform validate
```

### Step 2 – Execute terraform test and a normal apply

```bash
terraform test
terraform apply -auto-approve -var=prefix=lab
cat lab.txt
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'functions-templates-and-dynamic-blocks': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Use functions, templatestring/templatefile patterns, and dynamic blocks

### Step 1 – Build dynamic content

```bash
cat > greeting.tftpl <<'EOF'
Hello, ${name}!
EOF
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
variable "names" {
  type    = list(string)
  default = ["alpha", "beta"]
}
resource "local_file" "greetings" {
  for_each = toset(var.names)
  filename = "${path.module}/hi-${each.key}.txt"
  content  = templatefile("${path.module}/greeting.tftpl", { name = each.key })
}
locals {
  upper_names = [for n in var.names : upper(n)]
}
output "upper_names" { value = local.upper_names }
EOF
terraform init
```

### Step 2 – Apply and verify rendered files

```bash
terraform apply -auto-approve
cat hi-alpha.txt hi-beta.txt
terraform output
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'hcl-fundamentals-blocks-arguments-and-expressions': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Practise HCL blocks, arguments, and simple expressions

### Step 1 – Author blocks with expressions

```bash
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}

locals {
  project = "rebash"
  env     = "lab"
  name    = "${local.project}-${local.env}"
}

resource "local_file" "readme" {
  filename = "${path.module}/${local.name}.txt"
  content  = join("\n", ["name=${local.name}", "env=${local.env}"])
}
EOF
terraform init
terraform validate
```

### Step 2 – Apply and read interpolated output

```bash
terraform apply -auto-approve
cat rebash-lab.txt
terraform console <<<'local.name'
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'installing-terraform-and-the-cli-workflow': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Practise the core CLI workflow: init, validate, plan, apply, destroy

### Step 1 – Initialise and validate

```bash
cat > main.tf <<'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "null_resource" "lab" {
  triggers = {
    note = "rebash-lab"
  }
}

resource "local_file" "marker" {
  content  = "managed-by-terraform\n"
  filename = "${path.module}/marker.txt"
}
EOF
terraform version
terraform init
terraform validate
terraform fmt -check || terraform fmt
```

### Step 2 – Plan, apply, then prove destroy works

```bash
terraform plan -out=tfplan
terraform apply tfplan
ls -la marker.txt
terraform destroy -auto-approve
test ! -f marker.txt && echo "destroyed OK"
# Recreate for the cleanup step below
terraform apply -auto-approve
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'introduction-to-terraform-and-iac': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Apply your first Terraform configuration with local and null providers

### Step 1 – Write a minimal configuration

```bash
cat > main.tf <<'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "null_resource" "lab" {
  triggers = {
    note = "rebash-lab"
  }
}

resource "local_file" "marker" {
  content  = "managed-by-terraform\n"
  filename = "${path.module}/marker.txt"
}
EOF
terraform init
terraform plan
```

### Step 2 – Apply and inspect state

```bash
terraform apply -auto-approve
terraform state list
cat marker.txt
terraform show | head -n 40
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'kubernetes-infrastructure-with-terraform': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Represent Kubernetes-oriented objects as local files (no live cluster provider required)

### Step 1 – Generate namespace and deployment manifests from Terraform

```bash
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
variable "namespace" {
  type    = string
  default = "rebash-lab"
}
resource "local_file" "namespace" {
  filename = "${path.module}/manifests/namespace.yaml"
  content  = <<-EOT
    apiVersion: v1
    kind: Namespace
    metadata:
      name: ${var.namespace}
  EOT
}
resource "local_file" "deploy" {
  filename = "${path.module}/manifests/deploy.yaml"
  content  = <<-EOT
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: demo
      namespace: ${var.namespace}
    spec:
      replicas: 1
      selector:
matchLabels:
  app: demo
      template:
metadata:
  labels:
    app: demo
spec:
  containers:
  - name: nginx
    image: nginx:1.27-alpine
  EOT
}
EOF
mkdir -p manifests
terraform init
```

### Step 2 – Apply and optionally dry-run with kubectl if available

```bash
terraform apply -auto-approve
ls -la manifests/
head -n 20 manifests/deploy.yaml
if command -v kubectl >/dev/null; then kubectl apply --dry-run=client -f manifests/; else echo "kubectl optional for dry-run"; fi
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'modules-creating-reusable-infrastructure': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Build and call a local module

### Step 1 – Author a module and root module

```bash
mkdir -p modules/label
cat > modules/label/main.tf <<'EOF'
variable "name" { type = string }
resource "local_file" "out" {
  filename = "${path.root}/${var.name}.label"
  content  = "module-built:${var.name}\n"
}
output "path" { value = local_file.out.filename }
EOF
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
module "app" {
  source = "./modules/label"
  name   = "checkout"
}
output "label_path" { value = module.app.path }
EOF
terraform init
```

### Step 2 – Apply and inspect module address in state

```bash
terraform apply -auto-approve
terraform state list
cat checkout.label
terraform output
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'multi-cloud-terraform': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Simulate multi-cloud composition with two provider aliases (local/null only)

### Step 1 – Declare two logical stacks in one root

```bash
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
    null  = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
resource "local_file" "aws_like" {
  filename = "${path.module}/stack-a.txt"
  content  = "stack=a cloud=simulated-aws\n"
}
resource "local_file" "gcp_like" {
  filename = "${path.module}/stack-b.txt"
  content  = "stack=b cloud=simulated-gcp\n"
}
resource "null_resource" "cross_cut" {
  depends_on = [local_file.aws_like, local_file.gcp_like]
  triggers = {
    a = local_file.aws_like.content
    b = local_file.gcp_like.content
  }
}
EOF
terraform init
```

### Step 2 – Apply and discuss real multi-cloud coupling

```bash
terraform apply -auto-approve
cat stack-a.txt stack-b.txt
terraform state list
echo "Real multi-cloud: separate states per account/provider often reduce blast radius"
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'production-terraform-patterns': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Apply production habits: pinning, naming, tagging outputs, and safe plan review

### Step 1 – Create a structured configuration

```bash
cat > versions.tf <<'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
    null  = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
EOF
cat > main.tf <<'EOF'
locals {
  tags = {
    project = "rebash"
    env     = "lab"
    managed = "terraform"
  }
}
resource "null_resource" "guard" {
  triggers = local.tags
}
resource "local_file" "inventory" {
  filename = "${path.module}/inventory.json"
  content  = jsonencode(local.tags)
}
output "tags" { value = local.tags }
EOF
terraform init
terraform validate
```

### Step 2 – Plan with refresh and apply

```bash
terraform plan -input=false
terraform apply -auto-approve
cat inventory.json
terraform output -json
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'providers-and-the-terraform-plugin-model': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Pin providers and inspect the plugin lock file

### Step 1 – Declare required_providers and initialise

```bash
cat > main.tf <<'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}
provider "null" {}
resource "null_resource" "plugin_demo" {}
EOF
terraform init
ls -la .terraform.lock.hcl .terraform/providers | head -n 20
```

### Step 2 – Show provider versions and apply

```bash
terraform providers
terraform version
terraform apply -auto-approve
grep -A3 'provider "registry.terraform.io/hashicorp/null"' .terraform.lock.hcl || head -n 40 .terraform.lock.hcl
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'registry-modules-and-composition': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Compose multiple local modules as you would Registry modules

### Step 1 – Create two small modules and compose them

```bash
mkdir -p modules/network modules/app
cat > modules/network/main.tf <<'EOF'
resource "local_file" "net" {
  filename = "${path.root}/network.txt"
  content  = "cidr=10.0.0.0/16\n"
}
output "net_file" { value = local_file.net.filename }
EOF
cat > modules/app/main.tf <<'EOF'
variable "network_file" { type = string }
resource "local_file" "app" {
  filename = "${path.root}/app.txt"
  content  = "uses:${var.network_file}\n"
}
EOF
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
module "network" { source = "./modules/network" }
module "app" {
  source        = "./modules/app"
  network_file  = module.network.net_file
}
EOF
terraform init
```

### Step 2 – Apply composition and verify wiring

```bash
terraform apply -auto-approve
cat network.txt app.txt
terraform state list
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'remote-state-and-backends': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Configure a local backend path to practise backend blocks (no cloud account)

### Step 1 – Move state into an explicit local backend directory

```bash
mkdir -p state-backend
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
  backend "local" {
    path = "state-backend/terraform.tfstate"
  }
}
resource "local_file" "marker" {
  content  = "remote-style-local-backend\n"
  filename = "${path.module}/marker.txt"
}
EOF
terraform init
terraform apply -auto-approve
```

### Step 2 – Verify state location and discuss locking

```bash
ls -la state-backend/terraform.tfstate
terraform state list
echo "S3/Azure/GCS backends add shared storage + locking; this lab only relocates local state"
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'resources-dependencies-and-meta-arguments': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Explore implicit dependencies, count, and depends_on

### Step 1 – Create chained resources

```bash
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
    null  = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
resource "local_file" "base" {
  filename = "${path.module}/base.txt"
  content  = "base\n"
}
resource "local_file" "child" {
  count    = 2
  filename = "${path.module}/child-${count.index}.txt"
  content  = "depends on ${local_file.base.filename}\n"
}
resource "null_resource" "after" {
  depends_on = [local_file.child]
  triggers   = { stamp = timestamp() }
}
EOF
terraform init
```

### Step 2 – Apply and inspect graph order

```bash
terraform apply -auto-approve
terraform state list
ls -1 child-*.txt base.txt
terraform graph | head -n 30
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'terraform-cloud-and-hcp-terraform': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Model remote-run concepts locally without requiring HCP Terraform login

### Step 1 – Document run stages with a local dry-run script

```bash
cat > main.tf <<'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "null_resource" "lab" {
  triggers = {
    note = "rebash-lab"
  }
}

resource "local_file" "marker" {
  content  = "managed-by-terraform\n"
  filename = "${path.module}/marker.txt"
}
EOF
terraform init
cat > simulate-remote-run.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "1) queue plan"
terraform plan -out=tfplan
echo "2) policy checks (placeholder)"
echo "3) apply after approval"
terraform apply tfplan
EOF
chmod +x simulate-remote-run.sh
```

### Step 2 – Execute the simulated remote run

```bash
./simulate-remote-run.sh
terraform state list
echo "HCP Terraform adds remote execution, state, and policy — this lab mirrors the stages"
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'terraform-in-ci-cd-pipelines': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Simulate a CI plan artefact workflow locally

### Step 1 – Produce a saved plan like CI would

```bash
cat > main.tf <<'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "null_resource" "lab" {
  triggers = {
    note = "rebash-lab"
  }
}

resource "local_file" "marker" {
  content  = "managed-by-terraform\n"
  filename = "${path.module}/marker.txt"
}
EOF
terraform init
terraform fmt -check || terraform fmt
terraform validate
terraform plan -input=false -out=tfplan
terraform show -no-color tfplan | head -n 40
```

### Step 2 – Apply the exact plan file (CI apply job pattern)

```bash
terraform apply -input=false tfplan
terraform state list
echo "In real CI: OIDC to cloud, remote state, plan on PR, apply on main"
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'terraform-security-and-secrets': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Keep secrets out of state-friendly patterns using sensitive variables

### Step 1 – Mark sensitive inputs and avoid writing them to local files casually

```bash
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
variable "api_token" {
  type      = string
  sensitive = true
}
resource "local_file" "safe_marker" {
  filename = "${path.module}/safe.txt"
  content  = "token-configured=${var.api_token != ""}\n"
}
output "token_set" {
  value     = var.api_token != ""
  sensitive = true
}
EOF
terraform init
```

### Step 2 – Apply with an env-based variable and inspect redaction

```bash
export TF_VAR_api_token='lab-not-a-real-secret'
terraform apply -auto-approve
terraform output
cat safe.txt
echo "Note: sensitive values can still appear in state — protect state files"
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'terraform-state-fundamentals': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Inspect and safely query Terraform state

### Step 1 – Apply resources and explore state subcommands

```bash
cat > main.tf <<'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "null_resource" "lab" {
  triggers = {
    note = "rebash-lab"
  }
}

resource "local_file" "marker" {
  content  = "managed-by-terraform\n"
  filename = "${path.module}/marker.txt"
}
EOF
terraform init
terraform apply -auto-approve
terraform state list
terraform state show local_file.marker | head -n 30
```

### Step 2 – Pull state and understand remote implications

```bash
terraform state pull | head -n 40
ls -la terraform.tfstate*
echo "Local state is a file — remote backends store this centrally with locking"
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'terraform-workflow-init-plan-apply': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Walk the init → plan → apply loop with a saved plan file

### Step 1 – Initialise and create a plan artefact

```bash
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
    null  = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
resource "null_resource" "workflow" {
  triggers = { step = "plan-apply" }
}
resource "local_file" "note" {
  filename = "${path.module}/workflow.txt"
  content  = "init-plan-apply\n"
}
EOF
terraform init
terraform plan -out=tfplan
terraform show -no-color tfplan | head -n 30
```

### Step 2 – Apply the saved plan and confirm state

```bash
terraform apply tfplan
cat workflow.txt
terraform state list
terraform plan -detailed-exitcode || test $? -eq 0
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'troubleshooting-terraform': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Reproduce and diagnose a common apply failure, then fix it

### Step 1 – Create a configuration with a deliberate error

```bash
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
resource "local_file" "broken" {
  filename = "${path.module}/out.txt"
  content  = local.missing
}
EOF
terraform init
terraform validate 2>&1 || true
```

### Step 2 – Fix, apply, and use diagnostics habitually

```bash
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
locals {
  message = "fixed"
}
resource "local_file" "broken" {
  filename = "${path.module}/out.txt"
  content  = local.message
}
EOF
terraform validate
TF_LOG=INFO terraform apply -auto-approve 2>&1 | tail -n 20
cat out.txt
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'variables-locals-and-outputs': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Wire input variables, locals, and outputs cleanly

### Step 1 – Define variables and outputs

```bash
cat > variables.tf <<'EOF'
variable "app_name" {
  type    = string
  default = "demo"
}
variable "tags" {
  type    = map(string)
  default = { team = "platform" }
}
EOF
cat > main.tf <<'EOF'
terraform {
  required_providers {
    local = { source = "hashicorp/local", version = "~> 2.5" }
  }
}
locals {
  label = "${var.app_name}-lab"
}
resource "local_file" "config" {
  filename = "${path.module}/config.json"
  content  = jsonencode({ name = local.label, tags = var.tags })
}
output "config_path" {
  value = local_file.config.filename
}
output "label" {
  value = local.label
}
EOF
cat > terraform.tfvars <<'EOF'
app_name = "payments"
tags = { team = "platform", env = "lab" }
EOF
terraform init
```

### Step 2 – Apply and read outputs

```bash
terraform apply -auto-approve
terraform output
cat config.json
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'workspaces-and-environment-strategies': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Use workspaces to separate lab environments in one configuration

### Step 1 – Apply in default workspace then create another

```bash
cat > main.tf <<'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "null_resource" "lab" {
  triggers = {
    note = "rebash-lab"
  }
}

resource "local_file" "marker" {
  content  = "managed-by-terraform\n"
  filename = "${path.module}/marker.txt"
}
EOF
terraform init
terraform apply -auto-approve
terraform workspace list
terraform workspace new staging
```

### Step 2 – Apply in staging and contrast state

```bash
terraform apply -auto-approve
terraform workspace show
terraform state list
terraform workspace select default
terraform state list
echo "Workspaces isolate state keys; prefer separate directories/accounts for strong prod isolation"
```

### Final step – Cleanup note

```bash
terraform workspace select staging 2>/dev/null || true
terraform destroy -auto-approve || true
terraform workspace select default
terraform destroy -auto-approve
terraform workspace delete staging 2>/dev/null || true
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
}

IQ_TF: dict[str, str] = {
    'data-sources-and-existing-infrastructure': '''1. What is a data source used for?
2. How does a data source differ from a managed resource?
3. When is it better to import existing infrastructure than only read it with data sources?
4. What failures occur if a data source cannot find the object?
5. Can data source results end up in state?

!!! tip "Sample answer — question 2"
    Data sources read existing objects; resources create and manage lifecycle. Data sources fail the plan/apply if lookups miss, while resources propose creation.

!!! tip "Sample answer — question 4"
    Use import or bring resources under management when Terraform must create/update/delete them. Data sources alone will not reconcile drift on those objects.
''',
    'format-validate-and-terraform-test': '''1. What does `terraform fmt` guarantee?
2. How does `terraform test` differ from only running plan in CI?
3. What belongs in a minimal module test?
4. Why should format and validate gate merges?
5. What cannot validate catch that plan still might reveal?

!!! tip "Sample answer — question 2"
    `terraform test` can apply assertions against real or mocked runs, catching behavioural regressions beyond syntax. Plan alone may miss output/contract mistakes.

!!! tip "Sample answer — question 4"
    fmt/validate stop noise and basic errors early. Skipping them slows reviews and lets broken modules reach later, costlier pipeline stages.
''',
    'functions-templates-and-dynamic-blocks': '''1. What is `templatefile` useful for?
2. How does `for_each` differ from `dynamic` blocks?
3. When should you prefer explicit resources over dynamic blocks?
4. What readability trade-offs do nested functions create in reviews?
5. Give an example of a safe use of `tonumber` or `try`.

!!! tip "Sample answer — question 2"
    `for_each` creates multiple resource instances; `dynamic` generates nested blocks inside one resource. Use dynamic for repeated nested arguments like ingress rules.

!!! tip "Sample answer — question 4"
    Heavy nesting hides intent. Prefer locals with names, smaller templates, and tests so security-relevant values stay reviewable.
''',
    'hcl-fundamentals-blocks-arguments-and-expressions': '''1. What is the difference between an argument and a nested block in HCL?
2. How do string interpolation and the `join` function help build values?
3. What are locals used for?
4. Why avoid overly clever expressions that hide important business logic?
5. What does `path.module` refer to?

!!! tip "Sample answer — question 2"
    Interpolation and functions build strings and collections from parts. Prefer readable expressions and locals so outputs stay clear in reviews.

!!! tip "Sample answer — question 4"
    Dense one-liners make reviews and incidents harder. Extract locals, name things clearly, and keep security-sensitive logic obvious.
''',
    'installing-terraform-and-the-cli-workflow': '''1. What does `terraform init` download and create?
2. Why separate plan and apply in team workflows?
3. What does `terraform validate` check versus `terraform plan`?
4. Why must destroy be treated as carefully as apply in shared environments?
5. What files should normally be committed versus ignored?

!!! tip "Sample answer — question 2"
    Plan shows the proposed changeset without mutating (unless using certain targets). Applying a saved plan ensures CI applies exactly what was reviewed, reducing surprise drift between plan and apply.

!!! tip "Sample answer — question 4"
    Destroy removes managed resources and can delete data. In shared environments it needs the same approvals, state locking awareness, and backups as any production change.
''',
    'introduction-to-terraform-and-iac': '''1. What problem does Infrastructure as Code solve compared with ClickOps?
2. What does Terraform’s desired-state model mean in practice?
3. What is the role of providers in Terraform?
4. What risks remain even when infrastructure is coded?
5. How does Terraform differ conceptually from a pure configuration management tool?

!!! tip "Sample answer — question 2"
    You declare the end state; Terraform plans creates/updates/deletes to converge. Re-running apply should move reality toward the configuration rather than blindly re-running imperative scripts.

!!! tip "Sample answer — question 4"
    IaC can still destroy production if plans are unreviewed, state is corrupt, or credentials are overly broad. Code review, policy checks, and least-privilege credentials remain essential.
''',
    'kubernetes-infrastructure-with-terraform': '''1. How can Terraform manage Kubernetes objects?
2. What is the trade-off between the Kubernetes provider and rendering manifests for GitOps?
3. Why is cluster bootstrap often split from workload delivery?
4. What credential risks exist when Terraform talks directly to the API server?
5. How do you avoid Terraform fighting a GitOps controller?

!!! tip "Sample answer — question 2"
    Terraform-applied cluster objects can drift from GitOps reconcilers if both manage the same resources. Pick one controller per object or clearly separate layers (cluster vs apps).

!!! tip "Sample answer — question 4"
    Kubeconfig or cloud tokens in CI are powerful. Scope RBAC, prefer short-lived auth, and keep cluster-admin usage rare.
''',
    'modules-creating-reusable-infrastructure': '''1. What problem do modules solve?
2. How do module inputs and outputs define a contract?
3. What should you avoid putting inside a general-purpose module?
4. How can a poorly versioned module create blast radius across many stacks?
5. What is the difference between a root module and a child module?

!!! tip "Sample answer — question 2"
    Variables declare required inputs; outputs expose selected results. A clear contract lets callers compose modules without reading every resource inside.

!!! tip "Sample answer — question 4"
    One module change can alter hundreds of workspaces. Version modules, changelog breaking changes, and roll out upgrades gradually with plans reviewed per environment.
''',
    'multi-cloud-terraform': '''1. What does multi-cloud Terraform usually mean in practice?
2. Why might separate states per cloud be safer than one mega root module?
3. How do you keep interfaces consistent across clouds?
4. What operational complexity grows with multi-cloud estates?
5. When is multi-cloud the wrong goal?

!!! tip "Sample answer — question 2"
    Separate states isolate credentials, locking, and failure domains. A mega root couples unrelated outages and lengthens plans.

!!! tip "Sample answer — question 4"
    Identity, networking, and observability differ per cloud; tooling sprawl rises. Pursue multi-cloud for clear requirements, not fashion.
''',
    'production-terraform-patterns': '''1. Which version pinning practices belong in production roots?
2. How do you structure repositories for many environments?
3. What review checklist items matter on every production plan?
4. How do you limit blast radius of a mistaken apply?
5. Why keep modules thin at the edge and shared modules versioned?

!!! tip "Sample answer — question 2"
    Check destroys, replacements, security group openings, and IAM changes carefully. Small unexpected deletes are common incident sources.

!!! tip "Sample answer — question 4"
    Separate states, guardrails on who can apply prod, prevent_destroy on critical data stores, and canary environments reduce blast radius.
''',
    'providers-and-the-terraform-plugin-model': '''1. What does a Terraform provider plugin do?
2. Why pin provider versions with required_providers and the lock file?
3. What is the difference between provider source address and local name?
4. How can overly loose version constraints cause production incidents?
5. What happens during `terraform init` regarding plugins?

!!! tip "Sample answer — question 2"
    Pinning and committing `.terraform.lock.hcl` keeps plans reproducible across machines and CI. Without pins, new plugin releases can change behaviour unexpectedly.

!!! tip "Sample answer — question 4"
    Floating to the newest provider may introduce breaking resource schemas or behavioural changes during routine plans. Constrain versions and test upgrades deliberately.
''',
    'registry-modules-and-composition': '''1. What is the Terraform Registry used for?
2. Why pin module versions from the Registry?
3. How does composition of small modules differ from one giant module?
4. What supply-chain risks exist when consuming third-party modules?
5. How do you evaluate whether a Registry module is trustworthy?

!!! tip "Sample answer — question 2"
    Composition keeps networking, compute, and app layers separable and testable. Giant modules become hard to change and review.

!!! tip "Sample answer — question 4"
    Third-party modules can run unexpected resources or exfiltrate data via provisioners. Prefer verified sources, pinned versions, code review, and least-privilege credentials.
''',
    'remote-state-and-backends': '''1. What problems do remote backends solve?
2. What is state locking and why does it matter?
3. How does partial apply failure interact with remote state?
4. What security controls belong on a remote state bucket?
5. When might you split state across multiple backends/workspaces?

!!! tip "Sample answer — question 2"
    Locking prevents two applies from corrupting state or racing changes. Without locks, concurrent runs can overwrite each other’s state snapshots.

!!! tip "Sample answer — question 4"
    Encrypt the bucket, block public access, limit IAM to CI roles, enable versioning, and audit access. State is as sensitive as production config.
''',
    'resources-dependencies-and-meta-arguments': '''1. How does Terraform infer dependencies between resources?
2. When do you need explicit `depends_on`?
3. What is the difference between `count` and `for_each`?
4. What operational risk does `count` index shifting introduce?
5. What does `lifecycle { prevent_destroy = true }` protect against?

!!! tip "Sample answer — question 2"
    Implicit dependencies come from references. `depends_on` is for hidden ordering (for example, API readiness) that references cannot express.

!!! tip "Sample answer — question 4"
    Removing an element from a `count` list can force replacement of later indexes. `for_each` with stable keys usually produces safer updates.
''',
    'terraform-cloud-and-hcp-terraform': '''1. What capabilities does HCP Terraform add beyond open-source CLI alone?
2. What is a remote run versus local run?
3. How do policy-as-code checks fit into a remote run?
4. What organisational trade-offs exist when centralising runs in HCP Terraform?
5. How should VCS-driven workflows map to workspaces?

!!! tip "Sample answer — question 2"
    Remote runs execute plan/apply on managed workers with central state and optional policy gates. Local runs use your machine’s credentials and plugins.

!!! tip "Sample answer — question 4"
    Centralisation improves governance but creates platform dependency and needs clear workspace permissions so teams cannot apply each other’s prod stacks.
''',
    'terraform-in-ci-cd-pipelines': '''1. What is a typical PR plan / merge apply pipeline shape?
2. Why apply a saved plan file rather than re-planning on apply?
3. How does OIDC improve cloud authentication from CI?
4. What blast-radius controls belong in Terraform pipelines?
5. How do you prevent unreviewed applies to production?

!!! tip "Sample answer — question 2"
    Re-planning at apply time can pick up drift or new provider behaviour that reviewers never saw. Applying the exact plan artefact preserves intent.

!!! tip "Sample answer — question 4"
    Use environment protections, required reviews, remote state locking, least-privilege roles, and separate prod pipelines with manual approval gates.
''',
    'terraform-security-and-secrets': '''1. How does the sensitive flag on variables help?
2. Why can secrets still appear in state despite sensitive outputs?
3. What is a better pattern than hard-coding cloud keys in provider blocks?
4. How should you handle secret rotation with Terraform-managed resources?
5. What policies reduce accidental secret leakage in plans?

!!! tip "Sample answer — question 2"
    Sensitive flags redact CLI UI output but do not encrypt values in state. Protect backends and minimise secret material stored as resource attributes.

!!! tip "Sample answer — question 4"
    Prefer short-lived credentials via OIDC/IAM roles over static keys in env files. Static keys in CI variables still need rotation and scoped permissions.
''',
    'terraform-state-fundamentals': '''1. What information does Terraform state store?
2. Why is state required for Terraform to update infrastructure safely?
3. What is state drift?
4. Why must state files be treated as sensitive?
5. What does `terraform state mv` help with?

!!! tip "Sample answer — question 2"
    State maps configuration addresses to real remote object IDs and attributes so plans know what already exists. Without state, Terraform may try to recreate everything.

!!! tip "Sample answer — question 4"
    State can contain secrets and resource identifiers. Encrypt remote state, restrict IAM, enable locking, and never commit state with secrets to public Git.
''',
    'terraform-workflow-init-plan-apply': '''1. What is the purpose of each stage: init, plan, and apply?
2. Why save a plan with `-out` before applying?
3. What does a subsequent plan with no changes tell you?
4. What can go wrong if someone applies while another engineer plans against stale state?
5. How should interactive approval differ between laptops and CI?

!!! tip "Sample answer — question 2"
    A saved plan freezes the changeset reviewers approved. Applying that file avoids a newer unexpected plan. It is the usual pattern for CI apply jobs.

!!! tip "Sample answer — question 4"
    Without locking, two operators can race and corrupt state or apply conflicting changes. Remote backends with locking serialise applies and reduce this risk.
''',
    'troubleshooting-terraform': '''1. What are common causes of provider authentication errors?
2. How do you interpret a resource that must be replaced?
3. What does state inconsistency look like after a partial failure?
4. How can TF_LOG help, and what must you avoid when sharing logs?
5. When is `terraform refresh` / plan with refresh useful versus dangerous?

!!! tip "Sample answer — question 2"
    Replacement means Terraform cannot update in place—often from force-new arguments. Expect delete/create and plan for downtime or recreation side effects.

!!! tip "Sample answer — question 4"
    Debug logs may include secrets and tokens. Redact before sharing, and prefer targeted provider logs over dumping full environment variables.
''',
    'variables-locals-and-outputs': '''1. How do input variables differ from locals?
2. When should an output be marked sensitive?
3. What precedence do tfvars and environment variables follow at a high level?
4. Why can putting secrets in terraform.tfvars committed to Git be dangerous?
5. How do typed variables improve module interfaces?

!!! tip "Sample answer — question 2"
    Outputs marked sensitive are redacted in CLI output but may still exist in state. Use them for credentials you must expose to callers carefully, and protect state storage.

!!! tip "Sample answer — question 4"
    Committed tfvars often leak passwords and keys through Git history. Prefer secret managers, CI-injected TF_VAR_ values, and never commit real secrets.
''',
    'workspaces-and-environment-strategies': '''1. What does a Terraform workspace change about state?
2. When are workspaces a good fit versus separate directories or accounts?
3. How can workspace-based prod/staging separation fail as a hard tenancy boundary?
4. What naming strategy helps avoid applying the wrong workspace?
5. How do workspaces interact with remote backends?

!!! tip "Sample answer — question 2"
    Workspaces select different state keys for the same configuration. They are convenient for similar environments but easy to mis-select.

!!! tip "Sample answer — question 4"
    Because code is shared, a variable mistake can affect prod if you select the wrong workspace. Stronger isolation uses separate states, accounts, and pipelines.
''',
}

LABS_HELM: dict[str, str] = {
    'helm-architecture-and-components': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Map chart layout to rendered Kubernetes objects

### Step 1 – Inspect chart structure and render

```bash
kubectl create namespace rebash-helm
helm create arch-demo
find arch-demo -type f | sort
helm template demo ./arch-demo -n rebash-helm --debug 2>&1 | head -n 50
```

### Step 2 – Install and inspect release secret metadata (Helm 3)

```bash
helm upgrade --install demo ./arch-demo -n rebash-helm
kubectl -n rebash-helm get secrets -l owner=helm
helm -n rebash-helm get manifest demo | head -n 40
helm -n rebash-helm status demo
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-helm --ignore-not-found || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'helm-chart-dependencies': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Declare a chart dependency and build charts/ with helm dependency

### Step 1 – Create a parent chart with a file:// dependency

```bash
kubectl create namespace rebash-helm
helm create child
helm create parent
cat > parent/Chart.yaml <<'EOF'
apiVersion: v2
name: parent
description: parent with local dependency
type: application
version: 0.1.0
appVersion: "1.0.0"
dependencies:
  - name: child
    version: 0.1.0
    repository: "file://../child"
EOF
helm dependency update parent
ls -la parent/charts
```

### Step 2 – Lint and install the parent release

```bash
helm lint parent
helm upgrade --install demo ./parent -n rebash-helm
helm -n rebash-helm list
kubectl -n rebash-helm get deploy
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-helm --ignore-not-found || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'helm-gitops-integration': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Render Helm to plain YAML for a GitOps-friendly commit layout

### Step 1 – Template a chart into a manifests directory

```bash
kubectl create namespace rebash-helm
helm create gitops-demo
mkdir -p gitops/lab
helm template demo ./gitops-demo -n rebash-helm --set replicaCount=2 > gitops/lab/all.yaml
head -n 40 gitops/lab/all.yaml
git init -b main
git add gitops
git -c user.email=lab@rebash.local -c user.name=Lab commit -m "Render Helm manifests for GitOps"
```

### Step 2 – Apply rendered manifests and compare with a Helm release approach

```bash
kubectl apply -f gitops/lab/all.yaml
kubectl -n rebash-helm get deploy
echo "GitOps tools often render Helm in CI or use helm-controller — avoid double-managing the same objects"
# Optional: same chart via Helm for comparison
helm upgrade --install demo ./gitops-demo -n rebash-helm --set replicaCount=2 || true
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-helm --ignore-not-found || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'helm-releases-and-lifecycle': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Practise install, upgrade, history, rollback, and uninstall

### Step 1 – Install and upgrade a release

```bash
kubectl create namespace rebash-helm
helm create life-demo
helm upgrade --install demo ./life-demo -n rebash-helm --set replicaCount=1
helm upgrade demo ./life-demo -n rebash-helm --set replicaCount=2
helm -n rebash-helm history demo
```

### Step 2 – Rollback and confirm revision

```bash
helm -n rebash-helm rollback demo 1
helm -n rebash-helm history demo
helm -n rebash-helm status demo
kubectl -n rebash-helm get deploy -o wide
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-helm --ignore-not-found || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'helm-security': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Review rendered RBAC/service account settings before install

### Step 1 – Render and audit privileged-looking defaults

```bash
kubectl create namespace rebash-helm
helm create secure-demo
helm template demo ./secure-demo -n rebash-helm \
  --set serviceAccount.create=true \
  --set podSecurityContext.runAsNonRoot=true \
  --set podSecurityContext.runAsUser=1000 | tee rendered.yaml | head -n 60
grep -nE 'ServiceAccount|runAsNonRoot|allowPrivilegeEscalation|ClusterRole' rendered.yaml || true
```

### Step 2 – Install hardened values and verify objects

```bash
cat > secure-values.yaml <<'EOF'
serviceAccount:
  create: true
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
EOF
helm upgrade --install demo ./secure-demo -n rebash-helm -f secure-values.yaml
kubectl -n rebash-helm get sa,deploy
kubectl -n rebash-helm get deploy -o jsonpath='{.items[0].spec.template.spec.securityContext}{"\n"}'
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-helm --ignore-not-found || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'helm-templates-and-go-templating': 'Create a workspace for this tutorial.\n\n```bash\nmkdir -p {lab_dir} && cd {lab_dir}\n```\n\n**Focus:** Edit templates safely and render with helm template\n\n### Step 1 – Customise a ConfigMap template\n\n```bash\nkubectl create namespace rebash-helm\nhelm create tmpl-demo\npython3 - <<\'PY\'\nfrom pathlib import Path\nPath(\'tmpl-demo/templates/configmap.yaml\').write_text(\'\'\'apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: {{ include "tmpl-demo.fullname" . }}-config\n  labels:\n    {{- include "tmpl-demo.labels" . | nindent 4 }}\ndata:\n  APP_ENV: {{ .Values.env | default "lab" | quote }}\n\'\'\')\nprint(Path(\'tmpl-demo/templates/configmap.yaml\').read_text())\nPY\n```\n\n### Step 2 – Lint, template, and install\n\n```bash\nhelm lint tmpl-demo\nhelm template demo ./tmpl-demo -n rebash-helm --set env=lab | grep -A5 \'kind: ConfigMap\'\nhelm upgrade --install demo ./tmpl-demo -n rebash-helm --set env=lab\nkubectl -n rebash-helm get configmap\n```\n\n### Final step – Cleanup note\n\n```bash\nhelm uninstall demo -n rebash-helm --ignore-not-found || true\nkubectl delete namespace rebash-helm --ignore-not-found\n# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished\n```\n',
    'helm-testing-and-validation': 'Create a workspace for this tutorial.\n\n```bash\nmkdir -p {lab_dir} && cd {lab_dir}\n```\n\n**Focus:** Validate charts with lint, template, and helm test hooks\n\n### Step 1 – Add a simple test Pod hook\n\n```bash\nkubectl create namespace rebash-helm\nhelm create test-demo\nmkdir -p test-demo/templates/tests\npython3 - <<\'PY\'\nfrom pathlib import Path\nPath(\'test-demo/templates/tests/test-connection.yaml\').write_text(\'\'\'apiVersion: v1\nkind: Pod\nmetadata:\n  name: "{{ include "test-demo.fullname" . }}-test-connection"\n  labels:\n    {{- include "test-demo.labels" . | nindent 4 }}\n  annotations:\n    "helm.sh/hook": test\nspec:\n  containers:\n  - name: wget\n    image: busybox:1.36\n    command: [\'wget\']\n    args: [\'{{ include "test-demo.fullname" . }}:{{ .Values.service.port }}\']\n  restartPolicy: Never\n\'\'\')\nPY\nhelm lint test-demo\nhelm template demo ./test-demo -n rebash-helm >/dev/null\n```\n\n### Step 2 – Install and run helm test\n\n```bash\nhelm upgrade --install demo ./test-demo -n rebash-helm\nkubectl -n rebash-helm rollout status deploy -l app.kubernetes.io/instance=demo --timeout=90s || kubectl -n rebash-helm get deploy\nhelm -n rebash-helm test demo --logs || true\n```\n\n### Final step – Cleanup note\n\n```bash\nhelm uninstall demo -n rebash-helm --ignore-not-found || true\nkubectl delete namespace rebash-helm --ignore-not-found\n# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished\n```\n',
    'helm-values-and-overrides': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Override chart values via flags and values files

### Step 1 – Create a chart and environment values file

```bash
kubectl create namespace rebash-helm
helm create values-demo
cat > lab-values.yaml <<'EOF'
replicaCount: 2
service:
  type: ClusterIP
EOF
helm template demo ./values-demo -n rebash-helm -f lab-values.yaml | grep -A2 'replicas:'
```

### Step 2 – Install with layered overrides

```bash
helm upgrade --install demo ./values-demo -n rebash-helm -f lab-values.yaml --set image.tag=1.27-alpine
helm -n rebash-helm get values demo
kubectl -n rebash-helm get deploy demo-values-demo -o jsonpath='{.spec.replicas}{"\n"}' 2>/dev/null || kubectl -n rebash-helm get deploy -o wide
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-helm --ignore-not-found || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'installing-helm-and-repositories': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Verify Helm client and practise repository add/update/search

### Step 1 – Check Helm and add a repository

```bash
helm version
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo bitnami/nginx --versions | head -n 5
```

### Step 2 – Pull a chart locally and inspect without installing from remote blindly

```bash
helm pull bitnami/nginx --version $(helm search repo bitnami/nginx --versions -o json | python3 -c 'import sys,json; print(json.load(sys.stdin)[0]["version"])') --untar
ls -la nginx
helm template inspect-nginx ./nginx -n rebash-helm | head -n 30
kubectl create namespace rebash-helm
helm lint ./nginx
```

### Final step – Cleanup note

```bash
rm -rf nginx nginx-*.tgz 2>/dev/null || true
helm repo remove bitnami 2>/dev/null || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'introduction-to-helm': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Create a chart and install it into namespace rebash-helm

### Step 1 – Scaffold and lint a chart

```bash
kubectl create namespace rebash-helm
helm create hello-helm
helm lint hello-helm
helm template demo ./hello-helm -n rebash-helm | head -n 40
```

### Step 2 – Install and verify the release

```bash
helm upgrade --install demo ./hello-helm -n rebash-helm
helm -n rebash-helm list
kubectl -n rebash-helm get deploy,svc
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-helm --ignore-not-found || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'production-helm-practices': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Pin versions, use values files, and verify before upgrade

### Step 1 – Prepare production-style install inputs

```bash
kubectl create namespace rebash-helm
helm create prod-demo
# Pin chart version in Chart.yaml (already 0.1.0) and freeze image tag via values
cat > prod-values.yaml <<'EOF'
replicaCount: 2
image:
  tag: "1.27-alpine"
resources:
  requests:
    cpu: 50m
    memory: 64Mi
EOF
helm lint prod-demo
helm template demo ./prod-demo -n rebash-helm -f prod-values.yaml > /tmp/prod-render.yaml
grep -E 'replicas:|image:|cpu:' /tmp/prod-render.yaml | head -n 20
```

### Step 2 – Upgrade with atomic flag and check history

```bash
helm upgrade --install demo ./prod-demo -n rebash-helm -f prod-values.yaml --atomic --timeout 2m
helm -n rebash-helm history demo
kubectl -n rebash-helm get deploy -o wide
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-helm --ignore-not-found || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'troubleshooting-helm': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Diagnose a failed release using status, hooks, and kubectl

### Step 1 – Install a chart then break an upgrade on purpose

```bash
kubectl create namespace rebash-helm
helm create trouble
helm upgrade --install demo ./trouble -n rebash-helm
# Force a bad image tag to provoke ImagePullBackOff
helm upgrade demo ./trouble -n rebash-helm --set image.repository=nginx --set image.tag=not-a-real-tag-xyz --wait --timeout 45s || true
helm -n rebash-helm status demo || true
```

### Step 2 – Collect evidence and roll back

```bash
kubectl -n rebash-helm get pods
kubectl -n rebash-helm describe pod -l app.kubernetes.io/instance=demo | sed -n '/Events:/,$p' | head -n 30
helm -n rebash-helm history demo
helm -n rebash-helm rollback demo 1
kubectl -n rebash-helm rollout status deploy -l app.kubernetes.io/instance=demo --timeout=90s || true
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-helm --ignore-not-found || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
    'working-with-helm-charts': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Create, package, and install a local chart

### Step 1 – Build and package

```bash
kubectl create namespace rebash-helm
helm create work-chart
helm lint work-chart
helm package work-chart
ls -la work-chart-*.tgz
```

### Step 2 – Install from the package and show values

```bash
helm upgrade --install demo ./work-chart-*.tgz -n rebash-helm
helm -n rebash-helm get values demo --all | head -n 40
kubectl -n rebash-helm get all
```

### Final step – Cleanup note

```bash
helm uninstall demo -n rebash-helm --ignore-not-found || true
kubectl delete namespace rebash-helm --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```
''',
}

IQ_HELM: dict[str, str] = {
    'helm-architecture-and-components': '''1. What are the main directories inside a chart?
2. Where does Helm 3 store release metadata?
3. What role do helpers (_helpers.tpl) play?
4. Why was Tiller removed, and what security benefit followed?
5. How does the chart version relate to appVersion?

!!! tip "Sample answer — question 2"
    Release metadata lives in the cluster namespace as Secrets labelled for Helm, not in a central Tiller. That design keeps RBAC scoped to the namespace where you install.

!!! tip "Sample answer — question 4"
    Removing Tiller eliminated a powerful in-cluster shared server. Helm 3 uses your kubeconfig credentials directly, so RBAC of the caller matters.
''',
    'helm-chart-dependencies': '''1. What does the dependencies field in Chart.yaml declare?
2. What do `helm dependency update` and the charts/ directory contain?
3. How do you override subchart values from a parent?
4. What versioning risks exist when depending on floating subchart versions?
5. When should a dependency be optional with a condition/tags?

!!! tip "Sample answer — question 2"
    `helm dependency update` downloads/packaged charts into charts/ based on Chart.yaml. Parents then render subcharts as part of the release.

!!! tip "Sample answer — question 4"
    Floating versions can pull breaking subchart changes unexpectedly. Pin versions and test upgrades of parent and children together.
''',
    'helm-gitops-integration': '''1. How can Helm fit a GitOps workflow?
2. What is the risk of managing the same object with both Helm and kubectl/GitOps?
3. Why render charts to YAML in CI for some platforms?
4. How do you handle secrets when Helm is used with GitOps?
5. What drift symptoms appear when two controllers fight?

!!! tip "Sample answer — question 2"
    Double management causes thrashing updates and confusing rollbacks. Choose Helm releases or rendered manifests in Git as the single writer for each object.

!!! tip "Sample answer — question 4"
    Secrets should not live in plain values committed to Git. Use sealed secrets, external operators, or SOPS so GitOps can sync without exposing credentials.
''',
    'helm-releases-and-lifecycle': '''1. What does a release revision represent?
2. When would you `helm rollback` versus fix-forward with another upgrade?
3. What does `helm uninstall` remove, and what might remain?
4. How can hooks complicate upgrades and rollbacks?
5. Why is `--atomic` useful on production upgrades?

!!! tip "Sample answer — question 2"
    Rollback restores a previous revision’s manifest set. Fix-forward is better when rollback would reintroduce a known bug or when data migrations only go one way.

!!! tip "Sample answer — question 4"
    Hooks can create Jobs that are not fully reverted by rollback, leaving incomplete migrations. Design hooks carefully and document manual cleanup steps.
''',
    'helm-security': '''1. What chart features should you audit before install?
2. How do ServiceAccounts and RBAC in charts expand cluster rights?
3. Why pin image digests or immutable tags in production values?
4. What is chart provenance, and when does it help?
5. How should secrets be supplied to Helm releases?

!!! tip "Sample answer — question 2"
    Charts may create ClusterRoles, privileged pods, or hostPath mounts. Rendering and reviewing these objects prevents accidental cluster-admin paths.

!!! tip "Sample answer — question 4"
    Mutable tags like latest can change under you. Pin versions/digests so rollbacks and audits know exactly what ran, reducing supply-chain surprise.
''',
    'helm-templates-and-go-templating': '''1. What engine does Helm use for templates?
2. Why use `include` with helpers instead of duplicating labels?
3. How do `required` and `default` functions improve chart safety?
4. What dangers exist with `| safe` / unescaped HTML-like injection into manifests?
5. How do you debug a failing template render?

!!! tip "Sample answer — question 2"
    Helpers keep names and labels consistent across templates, which Services and selectors rely on. Duplication invites subtle mismatches that break traffic.

!!! tip "Sample answer — question 4"
    Careless sprig usage or piping untrusted values into YAML can break structure or inject unexpected fields. Validate inputs, quote carefully, and render in CI before apply.
''',
    'helm-testing-and-validation': '''1. What does `helm lint` check?
2. How do Helm test hooks differ from unit-testing templates?
3. Why run `helm template` in CI before allowing merges?
4. What security benefit comes from validating rendered manifests against policies?
5. When can `helm test` pass while production still fails?

!!! tip "Sample answer — question 2"
    template in CI catches render errors and lets policy engines scan YAML without touching a cluster. It is a cheap gate before install.

!!! tip "Sample answer — question 4"
    Policy checks (for example Pod Security) catch privileged defaults that lint may miss. Preventing those charts from shipping reduces cluster compromise risk.
''',
    'helm-values-and-overrides': '''1. In what order do default values, values files, and --set flags combine?
2. When should you prefer values files over long --set chains?
3. How do you see the values a release is currently using?
4. What security issue appears when secrets are placed in values files?
5. How do you manage values across staging and production?

!!! tip "Sample answer — question 2"
    Later sources override earlier ones: chart defaults, then -f files in order, then --set. Knowing precedence prevents surprise configuration.

!!! tip "Sample answer — question 4"
    Values files in Git often leak credentials. Keep secrets in sealed/external secret systems and reference them; treat values repos as sensitive if they contain any secrets.
''',
    'installing-helm-and-repositories': '''1. What does `helm repo add` store on your machine?
2. Why run `helm repo update` before installing?
3. What is the difference between searching a repo and pulling a chart?
4. How can a compromised chart repository harm you?
5. When should you vendor charts instead of installing straight from the internet?

!!! tip "Sample answer — question 2"
    Repositories are indexes of chart locations. update refreshes local cache so you see current chart versions rather than stale index data.

!!! tip "Sample answer — question 4"
    A malicious repo can serve charts that escalate privileges. Prefer HTTPS repos you trust, pin versions, verify provenance when available, and review rendered YAML.
''',
    'introduction-to-helm': '''1. What problem does Helm solve for Kubernetes packaging?
2. What is a release in Helm 3?
3. How do charts differ from raw manifests?
4. What risks come from installing untrusted charts?
5. What is the difference between `helm template` and `helm install`?

!!! tip "Sample answer — question 2"
    A release is a named instance of a chart running in a cluster (with revision history). Helm tracks it via release metadata stored as Secrets (or ConfigMaps) in the namespace.

!!! tip "Sample answer — question 4"
    Untrusted charts can create privileged workloads, ClusterRoles, or exfiltrate secrets. Always render and review, pin versions, and install into least-privilege namespaces.
''',
    'production-helm-practices': '''1. Which Helm flags help safer production upgrades?
2. How should chart and image versions be pinned?
3. What belongs in a release checklist before upgrading prod?
4. How do you limit blast radius of a bad chart upgrade?
5. Why keep values structured per environment rather than one mega file?

!!! tip "Sample answer — question 2"
    `--atomic`, timeouts, and staged environments help upgrades fail cleanly. Pin chart version and image tags, review `helm diff`/`template` output, and ensure PDBs exist for the app.

!!! tip "Sample answer — question 4"
    Use canary namespaces, smaller replica changes, and fast rollback. Separate prod pipelines with approvals so a bad values edit cannot silently ship.
''',
    'troubleshooting-helm': '''1. What commands start Helm release triage?
2. How do you distinguish a template failure from a Kubernetes runtime failure?
3. What does a pending-install/pending-upgrade state often indicate?
4. How can resources with `helm.sh/resource-policy: keep` surprise you during uninstall?
5. When should you use `helm rollback` during an incident?

!!! tip "Sample answer — question 2"
    Template failures happen at render time; runtime failures show after objects apply (ImagePullBackOff, CrashLoop). Use `helm status`, history, and kubectl describe/logs together.

!!! tip "Sample answer — question 4"
    Resources marked to keep remain after uninstall and can block reinstalls or leave credentials behind. Know which objects persist and delete them deliberately when appropriate.
''',
    'working-with-helm-charts': '''1. What does `helm package` produce?
2. How do you inspect default values before installing?
3. What is the purpose of Chart.yaml versus values.yaml?
4. Why lint charts before sharing them with other teams?
5. How do semantic versions on charts help consumers?

!!! tip "Sample answer — question 2"
    `helm show values` or reading values.yaml reveals defaults. Always review before production installs so replica counts, images, and service types are intentional.

!!! tip "Sample answer — question 4"
    Lint catches template and metadata mistakes early. Sharing broken charts wastes cluster time and can leave failed releases that need cleanup.
''',
}


def supported_techs() -> set[str]:
    """Return technology keys supported by this bank module."""
    return {"kubernetes", "terraform", "helm"}


def lab_for(tech: str, slug: str, title: str, lab_dir: str) -> str | None:
    """Return a Hands-on Lab markdown body for ``tech``/``slug``, or None."""
    banks_map = {
        "kubernetes": LABS_K8S,
        "terraform": LABS_TF,
        "helm": LABS_HELM,
    }
    body = banks_map.get(tech, {}).get(slug)
    if body is None:
        return None
    _ = title  # reserved for future title-aware labs
    return body.replace("{lab_dir}", lab_dir)


def interview_for(tech: str, slug: str, title: str) -> str | None:
    """Return Interview Questions markdown body for ``tech``/``slug``, or None."""
    banks_map = {
        "kubernetes": IQ_K8S,
        "terraform": IQ_TF,
        "helm": IQ_HELM,
    }
    _ = title  # reserved for future title-aware questions
    return banks_map.get(tech, {}).get(slug)
