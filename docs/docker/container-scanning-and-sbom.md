---
title: "Container Scanning and SBOM"
description: "Scan images with Trivy and Docker Scout, generate SBOMs, triage CVEs, and harden images in a DevOps pipeline gate."
difficulty: intermediate
estimated_time: "45–60 min"
technology: docker
category: docker
module: "Module 12 · Container Scanning"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - docker
  - trivy
  - sbom
prerequisites:
  - docker/docker-security-hardening
next:
  - docker/container-logging-and-monitoring
related:
  - docker/docker-in-ci-cd-pipelines
  - security/index
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - trivy
  - sbom
  - cve
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# Container Scanning and SBOM

## Overview







Scan an image for CVEs, produce a Software Bill of Materials (SBOM), and decide fix vs accept risk for a release gate.

**Trivy**, **Docker Scout**, and registry scanners find known vulnerabilities. An **SBOM** inventories packages for compliance and incident response. Scanning without a triage process becomes noise.

This is a core tutorial in **Module 12 · Container Scanning** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Docker Security Hardening](docker-security-hardening.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Run Trivy (or Scout) against a local image  
- [ ] Explain CRITICAL/HIGH triage  
- [ ] Generate an SBOM (Syft/Trivy)  
- [ ] List hardening moves that reduce findings

## Architecture







This topic’s control points and relationships are shown below.

![CI/CD pipeline with scan](../assets/excalidraw/docker-cicd-pipeline.svg)

## Theory







### What

**Vulnerability scanning** analyses image contents for known Common Vulnerabilities and Exposures (CVEs). A **Software Bill of Materials (SBOM)** lists packages and dependencies you shipped. Tools such as Trivy, Docker Scout, Syft, and Grype integrate into CI to gate or inform releases.

### Why

You cannot patch what you cannot see. Base OS packages and language libraries both introduce risk. SBOMs support incident response (“are we affected?”) and emerging compliance expectations. Failing CI on CRITICAL findings for production images is a common policy.

### How it works

Scanners index installed packages and match them to vulnerability databases. Results include severity, fixed versions, and sometimes misconfiguration checks (Dockerfile smells). Generate an SBOM at build time and store it with the artefact. Fix order is usually: upgrade base image → upgrade application dependencies → rebuild → accept residual risk with a ticket if needed. Do not ignore OS packages because “we only care about the app language”.

| Tool | Role |
|------|------|
| Trivy | OSS vuln + misconfig + SBOM |
| Docker Scout | Hub-integrated insights |
| Syft / Grype | SBOM + scan ecosystem |

### Key concepts

- **CVE noise** — triage by reachability and exploitability when possible  
- **Rebuild cadence** — periodic rebuilds pick up base patches  
- **Private base images** — control inheritance  
- **Sign + scan** — complementary supply-chain controls  


Wire scanners into both pull-request and main-branch pipelines so developers see findings early. Keep an allow-list process for accepted risks with expiry dates — permanent mute rules become invisible debt. After a major base-image upgrade, re-scan and redeploy even if application code did not change.

### Common pitfalls

- Scanning once at project start and never again  
- Suppressing all CVEs to keep CI green  
- Treating SBOM generation as paperwork without storing it  
- Scanning only the final stage while shipping a fat single-stage image

## Hands-on Lab

### Objective

Build a small lab image, attach a placeholder SBOM JSON, run Trivy when available (or a documented fallback), and validate output with a check script.

### Prerequisites

- Docker Engine or Docker Desktop
- `python3` for the check script
- Optional: [Trivy](https://trivy.dev/) installed (`trivy --version`)

### Lab environment

Workspace: `~/rebash-docker/module-12`

```bash title="Terminal"
mkdir -p ~/rebash-docker/module-12 && cd ~/rebash-docker/module-12
```

### Real-world scenario

Your pipeline must block merges when critical CVEs appear in base images. You build a tiny service image, record an SBOM stub for traceability, scan with Trivy (or a fallback that still produces `scan-results.txt`), and gate promotion with `check-scan.sh`.

### Step-by-step tasks

#### Task 1 – Build a scannable lab image

Create `Dockerfile`:

```dockerfile title="Dockerfile"
FROM alpine:3.20
RUN apk add --no-cache python3 py3-pip \
    && pip3 install --no-cache-dir flask==3.0.3
WORKDIR /app
COPY app.py .
USER nobody
EXPOSE 5000
CMD ["python3", "app.py"]
```

Create `app.py`:

```python title="app.py"
from flask import Flask
app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok", "service": "rebash-scan-lab"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Build and smoke-test:

```bash title="Terminal"
cd ~/rebash-docker/module-12
docker build -t rebash-scan-lab:1.0.0 .
docker run -d --name rebash-scan-18120 -p 18120:5000 rebash-scan-lab:1.0.0
sleep 2
curl -sS http://127.0.0.1:18120/health | tee health-scan.txt
grep -q '"status":"ok"' health-scan.txt
```

!!! example "Expected output"
    `health-scan.txt` contains JSON with `"status":"ok"`.


#### Task 2 – Add SBOM placeholder and scan

Create `sbom-placeholder.json`:

```json title="sbom-placeholder.json"
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "version": 1,
  "metadata": {
    "component": {
      "type": "container",
      "name": "rebash-scan-lab",
      "version": "1.0.0"
    }
  },
  "components": [
    {"type": "library", "name": "flask", "version": "3.0.3"},
    {"type": "library", "name": "alpine", "version": "3.20"}
  ]
}
```

Scan with Trivy if present; otherwise document packages via `docker inspect`:

{% raw %}
```bash title="Terminal"
cd ~/rebash-docker/module-12
if command -v trivy >/dev/null 2>&1; then
  trivy image --severity HIGH,CRITICAL --format table rebash-scan-lab:1.0.0 | tee scan-results.txt
else
  echo "Trivy not installed — fallback: inspect rootfs layers" | tee scan-results.txt
  docker inspect rebash-scan-lab:1.0.0 --format '{{ "{{" }}join .RootFS.Layers "\n"{{ "}}" }}' >> scan-results.txt
fi
test -s scan-results.txt
test -s sbom-placeholder.json
```
{% endraw %}

!!! example "Expected output"
    `scan-results.txt` is non-empty; `sbom-placeholder.json` validates as JSON.


#### Task 3 – Gate with check script

Create `check-scan.sh`:

```bash title="check-scan.sh"
#!/usr/bin/env bash
set -euo pipefail
RESULTS="${1:-scan-results.txt}"
SBOM="${2:-sbom-placeholder.json}"
test -s "$RESULTS"
python3 -c "import json; json.load(open('$SBOM'))"
if grep -qiE 'CRITICAL|HIGH' "$RESULTS" 2>/dev/null; then
  echo "Review required: HIGH/CRITICAL findings present"
  exit 2
fi
echo "Scan gate passed (or fallback documented)"
```

Run the gate:

```bash title="Terminal"
cd ~/rebash-docker/module-12
chmod +x check-scan.sh
./check-scan.sh scan-results.txt sbom-placeholder.json | tee gate-result.txt
test -s gate-result.txt
```

!!! example "Expected output"
    Script exits 0 or 2 with a message in `gate-result.txt`; SBOM JSON parses successfully.


### Validation steps

- [ ] Lab image builds and `/health` responds
- [ ] `sbom-placeholder.json` is valid CycloneDX-shaped JSON
- [ ] `scan-results.txt` exists from Trivy or documented fallback
- [ ] `check-scan.sh` validates both artefacts
- [ ] Cleanup removes container and image

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `trivy: command not found` | Trivy not installed | Use the fallback block in Task 2; install Trivy for full CVE output |
| Flask import error in container | Wrong Python path | Ensure `CMD ["python3", "app.py"]` and packages installed in Dockerfile |
| Gate exits 2 | Real CVEs in base image | Expected on some hosts — document findings; pin a smaller base if needed |
| Port 18120 in use | Previous lab | `docker rm -f rebash-scan-18120` |

### Challenge exercise

Export a real SBOM with `trivy image --format cyclonedx rebash-scan-lab:1.0.0 -o sbom-cyclonedx.json` and extend `check-scan.sh` to require that file when Trivy is available.

### Learning outcomes

- Built a minimal image suitable for vulnerability scanning
- Attached SBOM metadata for supply-chain traceability
- Ran Trivy or a honest fallback that still produces evidence
- Automated a scan gate with a shell check script

### Cleanup

```bash title="Terminal"
docker rm -f rebash-scan-18120 2>/dev/null || true
docker rmi rebash-scan-lab:1.0.0 2>/dev/null || true
rm -f ~/rebash-docker/module-12/*.txt
```

## Validation







- [ ] Lab commands run under `~/rebash-docker/module-12/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Container Scanning and SBOM** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations







- Treat credentials and tokens for docker as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes







!!! warning "Scanning once at project start and never again  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Suppressing all CVEs to keep CI green  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Container Scanning and SBOM changes as code and review them in pull requests
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







**Container Scanning and SBOM** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. What is an SBOM and why store it in CI?
2. How do you triage a CRITICAL CVE in a base image?
3. Scanner false positives — how do you handle them?
4. When should a pipeline fail on findings?
5. Difference between image scan and runtime detection?

!!! tip "Sample answer — question 2"
    Confirm the package is present in the final image and whether a fixed base exists.

!!! tip "Sample answer — question 4"
    Gate production on policy and keep SBOMs as artifacts for incident response.

## Related Tutorials







- [Course overview](index.md)
- [Container Logging and Monitoring](container-logging-and-monitoring.md)

## References







- [Trivy](https://trivy.dev/) · [Docker Scout](https://docs.docker.com/scout/)
