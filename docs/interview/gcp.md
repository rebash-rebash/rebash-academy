---
title: "Google Cloud Interview Preparation"
description: "3 curated Google Cloud interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: gcp
tags:
  - interview
  - gcp
comments: false
robots: noindex, follow
search:
  exclude: true
---

{% raw %}
# Google Cloud Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

<div class="ra-interview-qa" markdown="1">

## Practice questions

**1. How can you restrict public access to load balancers either standalone or gke?**

??? success "Reveal answer"
    **In short:** Keep backends private and gate who can hit the frontend — Cloud Armor / IAP for external, Internal LB for private-only.
    
    **Key points**
    
    - **Standalone** — prefer Internal HTTP(S) or Internal TCP/UDP LB when traffic must stay in the VPC
    - **External ALB** — attach Cloud Armor (allowlists, geo, rate limits); require Identity-Aware Proxy (IAP) for admin UIs
    - **GKE** — annotate Service with `networking.gke.io/load-balancer-type: "Internal"`, or use Gateway/Ingress with an internal Application LB
    - **Source ranges** — set `loadBalancerSourceRanges` / firewall rules; never rely on obscurity of a public IP
    
    **Try this**
    
    - `gcloud compute forwarding-rules list --format='table(name,IPAddress,loadBalancingScheme)'`
    - `kubectl get svc -A -o wide` — confirm INTERNAL vs EXTERNAL
    
    **Trap**
    
    - External LB + open `0.0.0.0/0` with no Armor/IAP — looks secure until a scanner finds it

**2. How can you can you migrate one node pool vms to another node pool in gcp?**

??? success "Reveal answer"
    **In short:** Create the new node pool first, then cordon/drain the old pool so Pods reschedule — never delete VMs out from under workloads.
    
    **Key points**
    
    - **Create target pool** — desired machine type, disk, labels, taints, and Kubernetes version
    - **Cordon** — stop new scheduling on old nodes (`kubectl cordon`)
    - **Drain in batches** — honour Pod Disruption Budgets (PDBs); watch Deployments/StatefulSets move
    - **Validate** — Ready nodes, selectors/taints match, Cluster Autoscaler still healthy
    - **Delete old pool** — only after zero user Pods remain on it
    
    **Try this**
    
    - `gcloud container node-pools create NEW_POOL --cluster=CLUSTER --zone=ZONE --num-nodes=3`
    - `kubectl get nodes -L cloud.google.com/gke-nodepool`
    - `kubectl drain NODE --ignore-daemonsets --delete-emptydir-data`
    
    **Trap**
    
    - Deleting the old pool before drain completes — orphaned volumes and PDB deadlocks

**3. How can you reduce gcp storage buckets costs?**

??? success "Reveal answer"
    **In short:** Cost drops when you match storage class to access patterns and stop paying for chatty requests and egress.
    
    **Key points**
    
    - **Visibility first** — Billing reports + Storage insights by bucket, class, and ops
    - **Lifecycle / Autoclass** — age cold objects into Nearline, Coldline, or Archive
    - **Cut request noise** — cache listings, avoid per-object List storms in CI
    - **Egress** — keep compute near data; use CDN for hot public reads
    - **Versioning hygiene** — lifecycle noncurrent versions and incomplete multipart uploads
    
    **Try this**
    
    - `gcloud storage buckets describe gs://BUCKET --format=json | jq '.lifecycle_config,.autoclass'`
    - Billing export to BigQuery — group by `storage.googleapis.com` SKUs before/after
    
    **Trap**
    
    - Moving hot data to Archive to 'save money' — early-delete and retrieval fees erase the win

## Related
- Course: [Google Cloud](../gcp/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
