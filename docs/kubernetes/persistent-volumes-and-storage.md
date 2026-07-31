---
title: "Persistent Volumes and Storage"
description: "Use Volumes, PVs, PVCs, StorageClasses, and CSI dynamic provisioning for stateful Kubernetes workloads."
difficulty: intermediate
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 7 · Storage"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - persistent-volumes
  - csi
prerequisites:
  - kubernetes/ingress-and-external-access
next:
  - kubernetes/configmaps-and-secrets
related:
  - kubernetes/workload-controllers-statefulset-daemonset-jobs
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
tags:
  - kubernetes
  - pvc
  - storageclass
  - csi
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Persistent Volumes and Storage

## Overview



Claim storage with a PVC against a StorageClass, mount it in a Pod, and explain PV vs PVC vs CSI.

**PVC** is the app’s request; **PV** is the provisioned volume; **StorageClass** selects a provisioner (CSI). Dynamic provisioning creates PVs automatically on most clouds and kind (local-path / rancher).

This is a core tutorial in **Module 7 · Storage** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Ingress and External Access](ingress-and-external-access.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Create PVC + Pod mount  
- [ ] List StorageClasses  
- [ ] Contrast access modes (RWO/RWX)  
- [ ] Outline CSI role



## Architecture



This topic’s control points and relationships are shown below.

![Storage architecture](../assets/excalidraw/k8s-storage-architecture.svg)



## Theory



### What it is

Kubernetes storage separates **what the app asks for** from **what the cluster provides**. A **PersistentVolumeClaim (PVC)** is the app’s request (size, access mode). A **PersistentVolume (PV)** is the actual volume. A **StorageClass** names a provisioner — usually a **CSI** (Container Storage Interface) driver — so PVs can be created dynamically. Ephemeral **Volumes** (emptyDir, config/secret mounts) die with the Pod; PVCs outlive Pods when configured to.

### Why it matters

Databases, queues, and ML artefacts need data that survives Pod restarts and reschedules. Cloud disks, NFS, and local path provisioners all plug in through the same PV/PVC model. Understanding access modes and reclaim policy prevents “volume already attached” and accidental data loss during delete.

### How it works (mental model)

1. Admin (or platform) installs CSI drivers and defines StorageClasses.
2. User creates a PVC referencing a StorageClass (or the default).
3. The provisioner creates a PV and binds it to the PVC.
4. A Pod mounts the PVC; kubelet attaches/mounts via CSI.
5. On Pod delete, the PVC/PV remain unless reclaim policy and delete workflows remove them.

**StatefulSets** often use `volumeClaimTemplates` so each ordinal gets its own PVC.

### Key concepts / comparisons

| Object | Role |
|--------|------|
| Volume (Pod field) | Mount into containers |
| PVC | Claim for durable storage |
| PV | Provisioned volume |
| StorageClass | Provisioner + parameters |
| CSI | Standard driver interface |

| Access mode | Meaning |
|-------------|---------|
| ReadWriteOnce (RWO) | One node writer (typical disks) |
| ReadOnlyMany (ROX) | Many nodes read-only |
| ReadWriteMany (RWX) | Many nodes read-write (NFS-like) |

### Common pitfalls

- Pending PVC because no default StorageClass or provisioner is broken.
- Scheduling Pods with RWO volumes onto different nodes after a move — attach conflicts.
- Deleting PVCs in production without backups; reclaim policy `Delete` destroys the backend.
- Using emptyDir for data you thought was persistent.
- Assuming every cluster has RWX — many cloud disks are RWO only.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-07 && cd ~/rebash-k8s/module-07
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



## Validation



- [ ] Lab commands run under `~/rebash-k8s/module-07/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Persistent Volumes and Storage** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.



## Security Considerations



- Treat credentials and tokens for kubernetes as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces



## Common Mistakes



!!! warning "Pending PVC because no default StorageClass or provisioner is broken."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Scheduling Pods with RWO volumes onto different nodes after a move — attach conflicts."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Persistent Volumes and Storage changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible



## Troubleshooting



| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |



## Summary



**Persistent Volumes and Storage** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What is the relationship between PersistentVolume, PersistentVolumeClaim, and StorageClass?
2. What does the Bound phase on a PVC mean?
3. What is the difference between ReadWriteOnce and ReadWriteMany?
4. What data-loss risks exist when deleting PVCs, and how do reclaim policies affect them?
5. Why are StatefulSets often paired with volumeClaimTemplates?

!!! tip "Sample answer — question 2"
    Bound means a PV has been allocated to the claim and is ready to mount. Until Bound, Pods needing the volume may stay Pending.

!!! tip "Sample answer — question 4"
    Deleting a PVC can delete underlying storage depending on reclaim policy (Delete vs Retain). Snapshot and backup strategies matter before destructive cleanup in production.



## Related Tutorials



- [Course overview](index.md)
- [ConfigMaps and Secrets](configmaps-and-secrets.md)



## References



- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
