---
title: Persistent Volumes and Storage
description: Provision durable storage with PersistentVolumes, PersistentVolumeClaims, and StorageClasses — understand access modes, reclaim policies, and dynamic provisioning.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: kubernetes
tags:
  - kubernetes
  - persistent-volumes
  - pvc
  - storage
  - stateful
prerequisites:
  - ConfigMaps and Secrets
  - Deployments — Managing Replicated Pods
  - Pods — The Atomic Unit
comments: false
---

# Persistent Volumes and Storage

## Overview

Containers are ephemeral — when a Pod dies, its local filesystem dies with it. Stateful workloads — databases, message queues, file uploads, CI caches — need **durable storage** that survives Pod restarts and rescheduling. Kubernetes separates storage **provisioning** from **consumption** through **PersistentVolumes (PV)**, **PersistentVolumeClaims (PVC)**, and **StorageClasses**.

A developer requests "10 GiB of fast SSD" with a PVC. The cluster's **dynamic provisioner** creates a PV backed by cloud disk (EBS, GCE PD, Azure Disk) or local storage. When the Pod mounts the PVC, data persists across container crashes, node failures, and rolling updates — as long as reclaim policy and backup strategy are correct.

This is **Tutorial 9** in **Module 3: Configuration & Storage** of the REBASH Academy Kubernetes series. Complete [ConfigMaps and Secrets](configmaps-and-secrets.md) first. Docker volume concepts from [Volumes and Persistent Storage](../docker/volumes-and-persistent-storage.md) transfer directly.

## Prerequisites

- Completed [ConfigMaps and Secrets](configmaps-and-secrets.md)
- Completed [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md)
- Completed [Pods — The Atomic Unit](pods-the-atomic-unit.md) — volumes, volumeMounts
- Completed [Installing Kubernetes and kubectl](installing-kubernetes-and-kubectl.md)
- A cluster with a default StorageClass (minikube and kind provide one)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the PV / PVC / StorageClass relationship
- [ ] Request storage dynamically with PersistentVolumeClaims
- [ ] Mount PVCs in Deployments and understand limitations for replicas
- [ ] Describe access modes: RWO, ROX, RWX
- [ ] Configure reclaim policies: Retain, Delete, Recycle
- [ ] Expand PVCs and handle storage class parameters
- [ ] Know when to use StatefulSets instead of Deployments for stateful apps

## Architecture Diagram

Administrators define StorageClasses; developers create PVCs; the provisioner binds PVs; Pods consume PVCs as volumes.

```d2
direction: right

Admin: "Cluster Admin" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        SC: "StorageClass\nfast-ssd"
    }
    Dev: Developer {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        PVC: "PVC data-vol\n10Gi RWO"
    }
    System: "Control Plane" {
      style: {
        fill: "#ffedd5"
        stroke: "#ea580c"
      }
        PROV: "Dynamic Provisioner\nEBS / hostPath / NFS"
        PV: "PersistentVolume\n10Gi Bound"
    }
    Workload: Pod {
      style: {
        fill: "#f3e8ff"
        stroke: "#9333ea"
      }
        MNT: "volumeMount\n/var/lib/data"
    }
    Admin.SC -> System.PROV
    Dev.PVC -> System.PROV
    System.PROV -> System.PV
    Dev.PVC -> System.PV
    Dev.PVC -> Workload.MNT
```

## Theory

### Why Separate PV and PVC?

Kubernetes decouples **how storage is provided** (admin concern) from **how much storage an app needs** (developer concern):

| Object | Owner | Purpose |
|--------|-------|---------|
| **StorageClass** | Admin | Define provisioner, parameters, reclaim policy default |
| **PersistentVolume (PV)** | Cluster | Actual storage resource (NFS export, cloud disk) |
| **PersistentVolumeClaim (PVC)** | Developer | Request for storage capacity and access mode |
| **Volume (in Pod spec)** | Developer | Mount a PVC into a container |

### Access Modes

| Mode | Abbreviation | Meaning |
|------|--------------|---------|
| ReadWriteOnce | RWO | Single node read-write |
| ReadOnlyMany | ROX | Many nodes read-only |
| ReadWriteMany | RWX | Many nodes read-write |
| ReadWriteOncePod | RWOP | Single Pod read-write (K8s 1.22+) |

Most cloud block storage (EBS, GCE PD) supports **RWO** only. Shared filesystems (NFS, EFS, Azure Files) support **RWX** for multiple Pods.

### Reclaim Policies

When a PVC is deleted, the bound PV's fate depends on reclaim policy:

| Policy | Behavior |
|--------|----------|
| **Delete** | PV and underlying storage asset deleted (default for dynamic provisioning) |
| **Retain** | PV released but data preserved — manual cleanup required |
| **Recycle** | Deprecated — scrub data and make available (use Delete or Retain) |

!!! warning "Delete policy and production data"
    Dynamic StorageClasses often default to `reclaimPolicy: Delete`. Deleting a PVC can permanently destroy database files. Use `Retain` for production databases or implement backup/restore before PVC deletion.

### Dynamic vs Static Provisioning

**Dynamic (recommended):** PVC specifies `storageClassName`; provisioner creates PV automatically.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

**Static:** Admin pre-creates PVs; PVC binds to matching available PV by size, access mode, and storage class.

### Mounting in Pods

```yaml
spec:
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: data-pvc
  containers:
    - name: app
      volumeMounts:
        - name: data
          mountPath: /var/lib/data
```

### Deployments vs StatefulSets with Storage

| Pattern | Storage behavior |
|---------|------------------|
| **Deployment + single PVC** | Only one Pod can mount RWO volume — other replicas fail or stay pending |
| **Deployment + RWX PVC** | Multiple Pods share one volume — requires shared filesystem |
| **StatefulSet + volumeClaimTemplates** | Each Pod gets its own PVC — correct pattern for replicated stateful apps |

For databases, prefer **StatefulSets** with `volumeClaimTemplates` — covered in advanced tutorials. This lab uses single-replica Deployments for clarity.

### StorageClass Example

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

| Parameter | Purpose |
|-----------|---------|
| `allowVolumeExpansion` | Enable PVC resize |
| `volumeBindingMode: WaitForFirstConsumer` | Delay binding until Pod scheduled — better topology awareness |

### EmptyDir vs PVC

| Volume type | Lifetime | Use case |
|-------------|----------|----------|
| **emptyDir** | Pod lifetime | Scratch space, caching, sidecar handoff |
| **hostPath** | Node filesystem | Node-level data (avoid in multi-tenant prod) |
| **PVC** | Independent of Pod | Databases, uploads, durable app state |

## Hands-on Lab

### Step 1 – Inspect available StorageClasses

**Command:**

```bash
kubectl get storageclass
kubectl describe storageclass $(kubectl get sc -o jsonpath='{.items[0].metadata.name}')
```

**Explanation:** Most local clusters ship with a default StorageClass. Cloud clusters offer multiple tiers (standard, SSD, premium).

**Expected output:**

```text
NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE
standard (default)   k8s.io/minikube-hostpath Delete         Immediate
```

### Step 2 – Create a PVC

**Command:**

```bash
kubectl create namespace lab-storage
```

Save as `data-pvc.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
  namespace: lab-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: standard
```

```bash
kubectl apply -f data-pvc.yaml
kubectl get pvc,pv -n lab-storage
```

**Explanation:** Dynamic provisioning creates a PV and binds it to the PVC automatically.

**Expected output:**

```text
NAME       STATUS   VOLUME                                     CAPACITY   ACCESS MODES
data-pvc   Bound    pvc-a1b2c3d4-e5f6-7890-abcd-ef1234567890   1Gi        RWO
```

### Step 3 – Deploy an app with persistent storage

**Command:**

Save as `web-with-pvc.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: lab-storage
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
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: data-pvc
      containers:
        - name: nginx
          image: nginx:1.25-alpine
          volumeMounts:
            - name: data
              mountPath: /usr/share/nginx/html
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: web
  namespace: lab-storage
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
```

```bash
kubectl apply -f web-with-pvc.yaml
kubectl exec -n lab-storage deploy/web -- sh -c 'echo "<h1>Persistent Data</h1>" > /usr/share/nginx/html/index.html'
kubectl run curl-test --image=curlimages/curl:8.5.0 -n lab-storage --restart=Never --rm -i -- curl -s http://web
```

**Expected output:**

```html
<h1>Persistent Data</h1>
```

### Step 4 – Verify data survives Pod restart

**Command:**

```bash
kubectl delete pod -n lab-storage -l app=web
kubectl wait --for=condition=Ready pod -n lab-storage -l app=web --timeout=60s
kubectl run curl-test2 --image=curlimages/curl:8.5.0 -n lab-storage --restart=Never --rm -i -- curl -s http://web
```

**Explanation:** The new Pod remounts the same PVC. Data written to the volume persists across Pod deletion.

### Step 5 – Demonstrate RWO limitation with replicas

**Command:**

```bash
kubectl scale deployment web --replicas=2 -n lab-storage
sleep 10
kubectl get pods -n lab-storage -o wide
```

**Explanation:** With RWO storage, only one Pod can mount the volume. Additional replicas stay `Pending` or fail with Multi-Attach errors. Scale back:

```bash
kubectl scale deployment web --replicas=1 -n lab-storage
```

### Step 6 – Static PV lab (optional)

**Command:**

Save as `static-pv.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: static-pv
spec:
  capacity:
    storage: 512Mi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /tmp/k8s-static-pv
    type: DirectoryOrCreate
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: static-pvc
  namespace: lab-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 512Mi
  storageClassName: manual
```

```bash
kubectl apply -f static-pv.yaml
kubectl get pv static-pv
kubectl get pvc static-pvc -n lab-storage
```

**Explanation:** Static provisioning pre-creates PVs. Useful for NFS exports or pre-provisioned cloud disks.

### Step 7 – Clean up

**Command:**

```bash
kubectl delete namespace lab-storage
# Retain-policy PVs require manual cleanup:
kubectl get pv | grep Released
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl get pvc` | List claims | `kubectl get pvc -n lab-storage` |
| `kubectl get pv` | List volumes | `kubectl get pv` |
| `kubectl describe pvc` | Debug binding issues | `kubectl describe pvc data-pvc` |
| `kubectl get sc` | List StorageClasses | `kubectl get storageclass` |
| `kubectl patch pvc` | Expand volume (if allowed) | `kubectl patch pvc data-pvc -p '{"spec":{"resources":{"requests":{"storage":"2Gi"}}}}'` |

### StatefulSet volumeClaimTemplates pattern

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:16
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 20Gi
        storageClassName: fast-ssd
```

Each Pod (`postgres-0`, `postgres-1`, ...) receives a dedicated PVC (`data-postgres-0`, ...).

## Common Mistakes

!!! warning "Multiple Deployment replicas with RWO PVC"
    ReadWriteOnce volumes attach to one node. Scaling a Deployment beyond one replica with a single RWO PVC causes Pending Pods or mount failures. Use StatefulSets or RWX storage.

!!! warning "Deleting PVCs with Delete reclaim policy"
    Dynamic volumes with `reclaimPolicy: Delete` destroy underlying cloud disks when the PVC is deleted. Backup before deletion in production.

!!! warning "Using hostPath in production"
    hostPath binds to a specific node's filesystem. Pods rescheduled to other nodes lose access. Acceptable for minikube labs only.

!!! warning "Running databases without backups"
    PVCs are not backups. Disk failure, accidental deletion, or cluster loss destroys data. Implement Velero, cloud snapshots, or native DB backup tools.

## Best Practices

!!! tip "Use WaitForFirstConsumer for zone-aware clusters"
    Delays volume provisioning until Pod scheduling — ensures cloud disks are created in the same availability zone as the Pod.

!!! tip "Set Retain for production databases"
    Configure StorageClass or PV reclaim policy to Retain. Delete PVCs only after confirming data is backed up or migrated.

!!! tip "Enable allowVolumeExpansion"
    Storage growth is common. Enable expansion on StorageClass and monitor disk usage with Prometheus.

!!! tip "Use StatefulSets for replicated stateful workloads"
    volumeClaimTemplates provide stable, per-Pod storage — the correct pattern for Kafka, PostgreSQL, Elasticsearch.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| PVC stuck Pending | No StorageClass, no matching PV | Check `kubectl describe pvc`; verify StorageClass exists |
| Pod Pending — volume | Multi-Attach error, zone mismatch | RWO already mounted elsewhere; use WaitForFirstConsumer |
| Data lost after PVC delete | reclaimPolicy: Delete | Restore from backup; use Retain for prod |
| Permission denied on mount | fsGroup / securityContext | Set `securityContext.fsGroup` in Pod spec |
| Cannot expand PVC | StorageClass lacks allowVolumeExpansion | Enable on StorageClass; some providers need offline resize |

## Summary

- **PVCs** request storage; **PVs** provide it; **StorageClasses** enable dynamic provisioning
- **RWO** suits single-Pod workloads; **RWX** requires shared filesystems for multi-Pod access
- **Reclaim policies** control whether data survives PVC deletion
- **Deployments + single RWO PVC** support only one replica — use **StatefulSets** for stateful clusters
- **emptyDir** is ephemeral; **PVCs** persist beyond Pod lifecycle
- Next: expose applications externally with [Ingress and External Access](ingress-and-external-access.md)

## Interview Questions

1. What is the relationship between PV, PVC, and StorageClass?
2. Explain ReadWriteOnce vs ReadWriteMany access modes.
3. What happens when you delete a PVC with reclaimPolicy Delete?
4. Why can't a Deployment with three replicas share one RWO PVC?
5. What is dynamic provisioning?
6. When would you use a StatefulSet instead of a Deployment for storage?
7. What is volumeBindingMode WaitForFirstConsumer?
8. How does Kubernetes storage differ from Docker named volumes?
9. What is the difference between emptyDir and a PVC?
10. How do you expand a PersistentVolumeClaim?

??? tip "Sample Answers (Questions 1, 4, and 6)"

    **Q1 — PV/PVC/StorageClass:** A StorageClass defines how storage is dynamically provisioned (provisioner, parameters, reclaim policy). A PVC is a developer's request for storage capacity and access mode. A PV is the actual storage resource. Dynamic provisioning automatically creates a PV when a PVC is created with a StorageClass.

    **Q4 — RWO limitation:** ReadWriteOnce volumes can be mounted read-write by only one node at a time. Multiple Pods on different nodes cannot attach the same RWO volume simultaneously. Scaling a Deployment to three replicas would leave extra Pods pending or failing with Multi-Attach errors.

    **Q6 — StatefulSet:** StatefulSets provide stable Pod identity and `volumeClaimTemplates` that create a dedicated PVC per Pod replica. This is the correct pattern for databases and clustered stateful apps where each instance needs its own durable storage.

## Related Tutorials

- [Kubernetes – Category Overview](index.md)
- [ConfigMaps and Secrets](configmaps-and-secrets.md) *(previous)*
- [Ingress and External Access](ingress-and-external-access.md) *(next)*
- [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md)
- [Volumes and Persistent Storage](../docker/volumes-and-persistent-storage.md)
- [Production Patterns — HPA, PDB, and Affinity](production-patterns-hpa-pdb-and-affinity.md)

## References

- [Persistent Volumes documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- [Configure a Pod to Use a PVC](https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/)
- [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
