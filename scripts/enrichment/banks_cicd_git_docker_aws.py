"""Topic-specific Hands-on Lab and Interview Question banks.

Covers: gitlab, github-actions, git, docker, aws.
Lab bodies use a ``{lab_dir}`` placeholder substituted by ``lab_for``.
"""

from __future__ import annotations


LABS_GITLAB: dict[str, str] = {
    'artifacts-caches-and-dependencies': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** configure cache keys and job artifacts with expire_in

### Step 1 – Build pipeline with cache + artifacts

```bash
mkdir -p src && echo 'print("build")' > src/main.py
cat > .gitlab-ci.yml << 'EOF'
stages: [deps, build, test]
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
deps:
  stage: deps
  image: python:3.12-alpine
  cache:
    key: {files: [requirements.txt]}
    paths: [.cache/pip]
  script:
    - echo pytest > requirements.txt
    - pip install -r requirements.txt
  artifacts:
    paths: [requirements.txt]
    expire_in: 1 day
build:
  stage: build
  image: python:3.12-alpine
  needs: [deps]
  script:
    - mkdir -p dist && cp -r src dist/ && echo "$CI_COMMIT_SHA" > dist/REVISION
  artifacts:
    paths: [dist/]
    expire_in: 3 days
test:
  stage: test
  image: python:3.12-alpine
  needs: [build]
  script: ["test -f dist/REVISION", "cat dist/REVISION"]
EOF
```

### Step 2 – Verify cache and artifact paths

```bash
grep -A8 'cache:' .gitlab-ci.yml
grep -A3 'artifacts:' .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'building-docker-images-in-ci': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Dockerfile plus Kaniko-style GitLab CI job; prove Dockerfile locally

### Step 1 – Create Dockerfile and CI build job

```bash
cat > Dockerfile << 'EOF'
FROM python:3.12-alpine AS runtime
WORKDIR /app
COPY app.py .
USER nobody
CMD ["python", "app.py"]
EOF
echo 'print("hello from gitlab docker lab")' > app.py
cat > .gitlab-ci.yml << 'EOF'
stages: [build]
build_image:
  stage: build
  image:
    name: gcr.io/kaniko-project/executor:v1.23.2-debug
    entrypoint: [""]
  script:
    - echo "Would push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
    - /kaniko/executor --context "$CI_PROJECT_DIR" --dockerfile "$CI_PROJECT_DIR/Dockerfile" --destination "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA" --no-push
  rules:
    - if: $CI_COMMIT_BRANCH
EOF
```

### Step 2 – Local Docker build proof

```bash
docker build -t rebash-gitlab-lab:local .
docker run --rm rebash-gitlab-lab:local
docker rmi rebash-gitlab-lab:local
grep -E 'kaniko|--no-push' .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
docker rmi rebash-gitlab-lab:local 2>/dev/null || true
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'enterprise-gitlab': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** sketch compliance controls: protected branches, required jobs, audit notes

### Step 1 – Enterprise guardrails + required pipeline

```bash
cat > enterprise-controls.md << 'EOF'
- Protected branches: main + release/*
- Required jobs: unit, secret_detection, deploy_production (manual)
- Runners: dedicated tags for prod
EOF
cat > .gitlab-ci.yml << 'EOF'
stages: [verify, compliance, deploy]
unit:
  stage: verify
  image: alpine:3.20
  script: ["echo unit"]
policy_check:
  stage: compliance
  image: alpine:3.20
  script: ["test -f enterprise-controls.md"]
deploy_production:
  stage: deploy
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  environment: {name: production}
  script: ["echo production change with approval trail"]
EOF
```

### Step 2 – Confirm control keywords

```bash
grep -E 'when: manual|environment:|policy_check' .gitlab-ci.yml
wc -l enterprise-controls.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'gitlab-ci-fundamentals': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** author a minimal .gitlab-ci.yml with stages and a real verify job

### Step 1 – Scaffold app and pipeline

```bash
cat > app.py << 'EOF'
def add(a, b):
    return a + b
if __name__ == "__main__":
    print(add(2, 3))
EOF
cat > .gitlab-ci.yml << 'EOF'
stages: [verify, package]
verify:
  stage: verify
  image: python:3.12-alpine
  script:
    - python -m pip install pytest
    - python -c "from app import add; assert add(2,3)==5"
package:
  stage: package
  image: alpine:3.20
  script:
    - tar czf app.tgz app.py
  artifacts:
    paths: [app.tgz]
    expire_in: 1 day
EOF
```

### Step 2 – Validate locally

```bash
python3 -c "from app import add; assert add(2,3)==5; print('ok')"
grep -E '^(stages:|verify:|package:)' .gitlab-ci.yml
wc -l .gitlab-ci.yml app.py
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'gitlab-projects-mrs-and-releases': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** model MR pipelines with merge request rules

### Step 1 – MR-centric workflow rules

```bash
echo '# Demo MR pipelines' > README.md
cat > .gitlab-ci.yml << 'EOF'
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH
stages: [verify]
mr_verify:
  stage: verify
  image: alpine:3.20
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  script: ["echo MR !$CI_MERGE_REQUEST_IID", "test -f README.md"]
branch_verify:
  stage: verify
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_BRANCH && $CI_PIPELINE_SOURCE != "merge_request_event"
  script: ["echo branch pipeline for $CI_COMMIT_BRANCH"]
EOF
```

### Step 2 – Validate workflow rules

```bash
grep -A6 'workflow:' .gitlab-ci.yml
grep 'merge_request_event' .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'gitlab-runners-and-executors': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** compare executor tags and pin a runner tag on a job

### Step 1 – Document executors and pin tags

```bash
cat > runner-notes.md << 'EOF'
# Runner executors
- shell: fast, weak isolation
- docker: clean images (common)
- kubernetes: elastic; needs RBAC
Prefer tags over untagged shared runners for production jobs
EOF
cat > .gitlab-ci.yml << 'EOF'
stages: [probe]
probe_docker:
  stage: probe
  image: alpine:3.20
  tags: [docker]
  script:
    - uname -a
    - echo "executor expected: docker"
probe_shell:
  stage: probe
  tags: [shell]
  rules: [{when: manual}]
  script: ["echo manual shell-tagged job"]
EOF
```

### Step 2 – Validate tags

```bash
grep -E 'tags:|image:' .gitlab-ci.yml
test -f runner-notes.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'kubernetes-deploys-and-gitlab-agent': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** GitLab Agent-style deploy job with kubectl dry-run manifests

### Step 1 – Manifests + agent deploy job

```bash
mkdir -p manifests
cat > manifests/deploy.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo
  namespace: rebash-lab
spec:
  replicas: 1
  selector: {matchLabels: {app: demo}}
  template:
    metadata: {labels: {app: demo}}
    spec:
      containers:
        - name: web
          image: nginx:alpine
          ports: [{containerPort: 80}]
EOF
cat > .gitlab-ci.yml << 'EOF'
stages: [validate, deploy]
validate:
  stage: validate
  image: bitnami/kubectl:latest
  script: ["kubectl apply --dry-run=client -f manifests/"]
deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  environment: {name: staging}
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  script:
    - echo "GitLab Agent injects kubectl context"
    - kubectl apply -f manifests/
EOF
```

### Step 2 – Client-side validate if kubectl exists

```bash
command -v kubectl >/dev/null && kubectl apply --dry-run=client -f manifests/ || echo "kubectl optional"
grep -E 'kubectl|environment:' .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'multi-cloud-deployments-with-gitlab': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** parameterise deploy jobs per cloud with OIDC-ready stubs (file-only)

### Step 1 – Multi-cloud job matrix

```bash
cat > .gitlab-ci.yml << 'EOF'
stages: [deploy]
.oidc_aws:
  id_tokens:
    GITLAB_OIDC_TOKEN: {aud: https://gitlab.com}
  variables: {CLOUD: aws}
.oidc_gcp:
  id_tokens:
    GITLAB_OIDC_TOKEN: {aud: https://gitlab.com}
  variables: {CLOUD: gcp}
deploy_aws:
  extends: .oidc_aws
  stage: deploy
  image: alpine:3.20
  rules:
    - if: $CLOUD_TARGET == "aws"
      when: manual
  script: ["echo Assume AWS role via OIDC — file-only", "echo cloud=$CLOUD"]
deploy_gcp:
  extends: .oidc_gcp
  stage: deploy
  image: alpine:3.20
  rules:
    - if: $CLOUD_TARGET == "gcp"
      when: manual
  script: ["echo Exchange OIDC for GCP WIF — file-only", "echo cloud=$CLOUD"]
EOF
```

### Step 2 – Confirm separate cloud jobs

```bash
grep -c 'id_tokens:' .gitlab-ci.yml
grep -E 'deploy_aws:|deploy_gcp:|CLOUD_TARGET' .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
# File-only — no cloud credentials
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'pipeline-design-dags-and-includes': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** split CI with include files and needs DAG edges

### Step 1 – Create includes and parent pipeline

```bash
mkdir -p ci
cat > ci/lint.yml << 'EOF'
lint:
  stage: lint
  image: alpine:3.20
  script: ["echo lint ok"]
EOF
cat > ci/test.yml << 'EOF'
unit:
  stage: test
  image: alpine:3.20
  needs: [lint]
  script: ["echo unit ok"]
EOF
cat > .gitlab-ci.yml << 'EOF'
stages: [lint, test, deploy]
include:
  - local: ci/lint.yml
  - local: ci/test.yml
deploy:
  stage: deploy
  image: alpine:3.20
  needs: [unit]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  script: ["echo deploy after DAG"]
EOF
```

### Step 2 – Verify includes and needs

```bash
test -f ci/lint.yml && test -f ci/test.yml
grep -E 'include:|needs:|local:' -n .gitlab-ci.yml ci/*.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'pipeline-monitoring-and-observability': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** emit pipeline metrics and observe duration

### Step 1 – Observability-friendly pipeline

```bash
cat > .gitlab-ci.yml << 'EOF'
stages: [build, observe]
build:
  stage: build
  image: alpine:3.20
  script:
    - START=$(date +%s); sleep 1; END=$(date +%s)
    - echo "job=build duration_s=$((END-START)) sha=$CI_COMMIT_SHA" | tee metrics.txt
  artifacts: {paths: [metrics.txt], expire_in: 1 week}
observe:
  stage: observe
  image: alpine:3.20
  needs: [build]
  script: ["test -f metrics.txt", "cat metrics.txt", "grep duration_s metrics.txt"]
EOF
```

### Step 2 – Local metrics dry-run

```bash
START=$(date +%s); sleep 1; END=$(date +%s)
echo "job=build duration_s=$((END-START)) sha=local" | tee metrics.txt
grep duration_s metrics.txt
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'pipeline-syntax-gitlab-ci-yml': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** exercise rules, needs, and parallel matrix syntax

### Step 1 – Write advanced syntax pipeline

```bash
cat > .gitlab-ci.yml << 'EOF'
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH
stages: [lint, test, build]
lint:
  stage: lint
  image: alpine:3.20
  script: ["echo linting $CI_COMMIT_SHA"]
unit:
  stage: test
  image: python:3.12-alpine
  parallel:
    matrix:
      - PYTHON: ["3.11", "3.12"]
  script: ["echo matrix python=$PYTHON"]
build:
  stage: build
  image: alpine:3.20
  needs: [lint, unit]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
  script: ["mkdir -p dist && echo ok > dist/marker.txt"]
  artifacts:
    paths: [dist/]
EOF
```

### Step 2 – Inspect keywords

```bash
grep -E '^(workflow:|parallel:|needs:|rules:)' -n .gitlab-ci.yml
grep -A3 'needs:' .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'production-pipelines-and-environments': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** model staging/production environments with manual production gate

### Step 1 – Environment-aware deploy jobs

```bash
cat > .gitlab-ci.yml << 'EOF'
stages: [build, deploy]
build:
  stage: build
  image: alpine:3.20
  script: ["mkdir -p dist && echo $CI_COMMIT_SHA > dist/REVISION"]
  artifacts: {paths: [dist/]}
deploy_staging:
  stage: deploy
  image: alpine:3.20
  environment: {name: staging, url: https://staging.example.invalid}
  script: ["test -f dist/REVISION", "echo deploy staging"]
deploy_production:
  stage: deploy
  image: alpine:3.20
  environment: {name: production, url: https://www.example.invalid}
  needs: [deploy_staging]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  script: ["echo production requires manual approval"]
EOF
```

### Step 2 – Confirm environment blocks

```bash
grep -A3 'environment:' .gitlab-ci.yml
grep -A2 'when: manual' .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'release-management-and-versioning': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** tag-driven release job with changelog artefact

### Step 1 – Release pipeline on tags

```bash
cat > CHANGELOG.md << 'EOF'
# Changelog
## Unreleased
- Lab release scaffolding
EOF
cat > .gitlab-ci.yml << 'EOF'
stages: [release]
release_notes:
  stage: release
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_TAG
  script:
    - echo "Releasing $CI_COMMIT_TAG"
    - mkdir -p dist && cp CHANGELOG.md dist/ && echo "$CI_COMMIT_TAG" > dist/VERSION
  artifacts: {paths: [dist/]}
  release:
    tag_name: $CI_COMMIT_TAG
    description: "Release $CI_COMMIT_TAG"
EOF
```

### Step 2 – Simulate tag metadata

```bash
echo "v0.1.0-lab" > VERSION.sim
grep -E 'CI_COMMIT_TAG|release:' .gitlab-ci.yml
test -f CHANGELOG.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'security-scanning-and-devsecops': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** SAST/secret-detection style jobs and a security gate

### Step 1 – Security scanning pipeline

```bash
echo 'PASSWORD_PLACEHOLDER = "replace-me"' > app.py
cat > .gitlab-ci.yml << 'EOF'
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
stages: [test, security, gate]
unit:
  stage: test
  image: alpine:3.20
  script: ["echo unit"]
secret_review:
  stage: security
  image: alpine:3.20
  script:
    - echo "Review Security tab reports"
    - test -f app.py
security_gate:
  stage: gate
  image: alpine:3.20
  needs: [secret_review]
  script: ["echo Fail when critical findings exceed policy"]
EOF
```

### Step 2 – Hunt for accidental secrets

```bash
grep -RInE '(AKIA[0-9A-Z]{16}|BEGIN (RSA |OPENSSH )?PRIVATE KEY)' . || echo "no obvious secrets"
grep -E 'Secret-Detection|SAST|security_gate' .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'terraform-pipelines-in-gitlab': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** plan/apply GitLab jobs with artefact plan (local backend)

### Step 1 – Minimal Terraform + CI jobs

```bash
cat > versions.tf << 'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
EOF
cat > main.tf << 'EOF'
resource "null_resource" "lab" {
  triggers = { note = "gitlab-terraform-lab" }
}
EOF
cat > .gitlab-ci.yml << 'EOF'
stages: [validate, plan, apply]
image: {name: hashicorp/terraform:1.9, entrypoint: [""]}
variables: {TF_IN_AUTOMATION: "true"}
validate:
  stage: validate
  script: ["terraform init -backend=false", "terraform validate"]
plan:
  stage: plan
  script: ["terraform init -backend=false", "terraform plan -out=plan.cache"]
  artifacts: {paths: [plan.cache], expire_in: 1 day}
apply:
  stage: apply
  needs: [plan]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  script: ["terraform init -backend=false", "terraform apply -auto-approve plan.cache"]
EOF
```

### Step 2 – Local validate/plan/destroy

```bash
if command -v terraform >/dev/null; then
  terraform init -backend=false && terraform validate
  terraform plan -out=plan.cache && terraform apply -auto-approve plan.cache
  terraform destroy -auto-approve
fi
grep -E 'plan.cache|when: manual' .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve 2>/dev/null || true
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'testing-reports-and-quality-gates': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** pytest JUnit reports and a quality gate job

### Step 1 – Tests + junit artifacts

```bash
cat > calc.py << 'EOF'
def mul(a, b):
    return a * b
EOF
cat > test_calc.py << 'EOF'
from calc import mul
def test_mul():
    assert mul(3, 4) == 12
EOF
cat > .gitlab-ci.yml << 'EOF'
stages: [test, gate]
unit:
  stage: test
  image: python:3.12-alpine
  script:
    - pip install pytest
    - pytest --junitxml=report.xml -q
  artifacts:
    when: always
    reports:
      junit: report.xml
    paths: [report.xml]
coverage_gate:
  stage: gate
  image: alpine:3.20
  needs: [unit]
  script:
    - test -f report.xml
    - grep -q testcase report.xml
EOF
```

### Step 2 – Run tests locally

```bash
python3 -c "from calc import mul; assert mul(3,4)==12; print('ok')"
echo '<?xml version="1.0"?><testsuite><testcase name="test_mul"/></testsuite>' > report.xml
grep -E 'junit:|reports:' .gitlab-ci.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'troubleshooting-gitlab-ci': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** reproduce a failing job locally and capture triage checklist

### Step 1 – Broken job + triage notes

```bash
cat > .gitlab-ci.yml << 'EOF'
stages: [broken, fixed]
broken_example:
  stage: broken
  image: alpine:3.20
  script: ["curl --version"]
  allow_failure: true
fixed_example:
  stage: fixed
  image: curlimages/curl:8.10.1
  script: ["curl --version"]
EOF
cat > triage.md << 'EOF'
1. First error in job log
2. Confirm image/tag and entrypoint
3. Check rules/needs
4. Verify variables on unprotected branches
5. CI_DEBUG_TRACE only in secure sandbox
EOF
```

### Step 2 – Simulate fix with Docker

```bash
docker run --rm alpine:3.20 sh -c 'command -v curl || echo curl-missing'
docker run --rm curlimages/curl:8.10.1 curl --version | head -n 1
test -f triage.md
```

### Final step – Cleanup note

```bash
docker rmi alpine:3.20 curlimages/curl:8.10.1 2>/dev/null || true
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
    'variables-secrets-and-oidc': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** separate non-secrets from masked vars; shape OIDC job (file-only validation)

### Step 1 – Author variables + id_tokens pipeline

```bash
cat > oidc-checklist.md << 'EOF'
- [ ] Non-secrets in YAML variables only
- [ ] Masked+protected secrets in CI/CD settings
- [ ] id_tokens with explicit aud
- [ ] Never echo tokens
EOF
cat > .gitlab-ci.yml << 'EOF'
stages: [verify, deploy]
variables:
  APP_ENV: "ci"
show_predefined:
  stage: verify
  image: alpine:3.20
  script:
    - echo "project=$CI_PROJECT_PATH ref=$CI_COMMIT_REF_NAME"
    - echo "APP_ENV=$APP_ENV"
oidc_ready_deploy:
  stage: deploy
  image: alpine:3.20
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://gitlab.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  script:
    - test -n "${GITLAB_OIDC_TOKEN:-}" && echo "OIDC token present (do not print)" || echo "Token only on GitLab runners"
    - echo "Exchange JWT via cloud STS — not long-lived keys"
EOF
```

### Step 2 – File-only validation

```bash
grep -A6 'id_tokens:' .gitlab-ci.yml
grep 'GITLAB_OIDC_TOKEN' .gitlab-ci.yml
test -f oidc-checklist.md
# No cloud API calls — structure only
```

### Final step – Cleanup note

```bash
# File-only OIDC lab — no cloud resources
# Keep ~/rebash-gitlab/ for later tutorials
```
''',
}

IQ_GITLAB: dict[str, str] = {
    'artifacts-caches-and-dependencies': '''1. What is the difference between cache and artifacts in GitLab CI?
2. A later job cannot find a file produced earlier — how do you diagnose it?
3. When should cache keys include a lockfile hash?
4. What security issue arises from caching world-writable directories?
5. How does expire_in help control storage cost?

!!! tip "Sample answer — question 2"
    Confirm the producer declared artifacts paths, the consumer needs/dependencies includes that job, and paths match. Cache is best-effort and must not be the only way to pass build outputs.

!!! tip "Sample answer — question 4"
    Treat caches as untrusted acceleration: pin keys, avoid storing secrets, and keep artifact retention short.
''',
    'building-docker-images-in-ci': '''1. Why is Docker-in-Docker often avoided in favour of Kaniko/Buildah?
2. How should image tags be chosen for traceability?
3. What does --no-push buy you while learning CI image builds?
4. How do you keep registry credentials out of the Dockerfile?
5. What base-image practices reduce supply-chain risk?

!!! tip "Sample answer — question 2"
    Check Dockerfile path/context, registry auth, and whether the executor may spawn builders. Confirm destination before enabling push.

!!! tip "Sample answer — question 4"
    Authenticate via CI variables or OIDC-linked tokens, never ENV passwords in the image. Prefer minimal bases and non-root users.
''',
    'enterprise-gitlab': '''1. Which GitLab controls map to separation of duties?
2. How do you evidence a production change for auditors?
3. What belongs in instance/group policy versus project config?
4. How should runner fleets be segmented in an enterprise?
5. What is a pragmatic approach to compliance-as-code in CI?

!!! tip "Sample answer — question 2"
    Start from the change record: MR, pipeline, approvals, environment deploy job, and artifact checksums.

!!! tip "Sample answer — question 4"
    Segment runners, enforce SSO, protect critical projects, and keep production secrets out of developer-controlled variables.
''',
    'gitlab-ci-fundamentals': '''1. What are stages versus jobs in GitLab CI, and why does order matter?
2. A pipeline is green in your mind but red on GitLab — what do you check first?
3. When would you split verify and package into separate stages?
4. How should secrets be handled in a first GitLab CI pipeline?
5. How do artifacts help downstream jobs without rebuilding everything?

!!! tip "Sample answer — question 2"
    Compare the job image and script with your laptop: missing packages, wrong shell, and different CI variables explain most first-pipeline failures. Open the failing job log at the first error line.

!!! tip "Sample answer — question 4"
    Keep non-secrets in YAML variables; put credentials in masked/protected CI variables or OIDC. Never commit tokens, and never echo secret values in job logs.
''',
    'gitlab-projects-mrs-and-releases': '''1. Why prefer merge request pipelines over duplicate branch pipelines?
2. What is detached merge request pipeline behaviour?
3. How do draft MRs change your required checks strategy?
4. Who should be allowed to merge to protected branches?
5. How do releases relate to tags and permissions?

!!! tip "Sample answer — question 2"
    Check workflow rules and whether both branch and MR pipelines fired. Confirm required status checks match jobs that run on merge_request_event.

!!! tip "Sample answer — question 4"
    Protected branches, CODEOWNERS, and required pipelines enforce review. Keep secret variables away from untrusted fork MRs.
''',
    'gitlab-runners-and-executors': '''1. Compare shell, Docker, and Kubernetes executors for isolation and cost.
2. Jobs stuck in pending — what runner factors do you verify first?
3. Why tag runners instead of relying on shared untagged runners?
4. What security risk does a privileged Docker runner introduce?
5. How do protected runners interact with protected branches/variables?

!!! tip "Sample answer — question 2"
    Check runner online status, matching tags, concurrent job limits, and whether the project may use that runner. Pending almost always means no eligible runner.

!!! tip "Sample answer — question 4"
    Privileged mode and Docker socket mounts can let jobs escape to the host. Prefer unprivileged executors and dedicated tags for production.
''',
    'kubernetes-deploys-and-gitlab-agent': '''1. What problem does the GitLab Agent solve versus storing kubeconfig in CI?
2. How do you validate manifests before a real apply?
3. Why scope agent access per environment/namespace?
4. What RBAC should a deploy job assume in-cluster?
5. How do you roll back a bad GitLab-driven deploy?

!!! tip "Sample answer — question 2"
    Start with kubectl dry-run/client validation and agent connectivity: wrong context, namespace, or missing RBAC explains most failures.

!!! tip "Sample answer — question 4"
    Prefer short-lived agent sessions and least-privilege ServiceAccounts per environment.
''',
    'multi-cloud-deployments-with-gitlab': '''1. How do you parameterise one pipeline for AWS and GCP deploys?
2. What OIDC claim conditions should differ per cloud role?
3. When is a matrix job better than separate deploy jobs?
4. How do you avoid cross-cloud credential mix-ups in logs?
5. What shared gates should every cloud deploy still pass?

!!! tip "Sample answer — question 2"
    Verify the job's cloud selector variables, matching OIDC trust, and that the correct provider CLI is in the image.

!!! tip "Sample answer — question 4"
    Isolate roles per cloud and environment; keep deploy jobs manual for production. File-only validation is enough until cloud trusts exist.
''',
    'pipeline-design-dags-and-includes': '''1. When do you choose include local versus project/remote includes?
2. A child job never runs after a refactor — what DAG mistakes are common?
3. How do hidden jobs help reuse?
4. What is the blast radius of a shared include owned by another team?
5. How do you version shared pipeline templates safely?

!!! tip "Sample answer — question 2"
    Trace needs edges and stage membership: a job can be skipped by rules or waiting on a renamed dependency. Confirm includes expanded as expected.

!!! tip "Sample answer — question 4"
    Pin shared templates to tags/SHAs and review changes like application code.
''',
    'pipeline-monitoring-and-observability': '''1. Which pipeline metrics matter for platform teams?
2. Job duration doubled overnight — where do you look first?
3. How can artifacts support auditability of CI behaviour?
4. What should you alert on versus only dashboard?
5. How do you keep observability from leaking secrets?

!!! tip "Sample answer — question 2"
    Compare recent commits to the job definition, runner load, and external dependency latency before changing timeouts blindly.

!!! tip "Sample answer — question 4"
    Redact tokens from exported logs/metrics and limit who can read job traces with secrets.
''',
    'pipeline-syntax-gitlab-ci-yml': '''1. What does needs change compared with stage-only ordering?
2. How do rules differ from only/except, and why prefer rules?
3. When is parallel matrix the right tool?
4. How can a malicious merge request abuse overly broad rules?
5. What is workflow rules for at the pipeline level?

!!! tip "Sample answer — question 2"
    Confirm whether the job was skipped by rules, blocked by needs on a failed dependency, or never created because workflow rules prevented the pipeline.

!!! tip "Sample answer — question 4"
    Prefer least-privilege rules: block pipelines from untrusted forks where secrets are available, keep production deploys manual on the default branch.
''',
    'production-pipelines-and-environments': '''1. How do GitLab environments help track deployments?
2. Why make production deploy when manual even if staging is automatic?
3. What should stop an automatic promote from staging to production?
4. How do protected environments reduce risk?
5. What evidence do you keep for a production change?

!!! tip "Sample answer — question 2"
    Check environment name/url, deployment job rules, and whether the commit is on the allowed branch. Read the job log and app health next.

!!! tip "Sample answer — question 4"
    Limit who can run production jobs, require approvals on protected environments, and inject production secrets only into those jobs.
''',
    'release-management-and-versioning': '''1. How do tag pipelines differ from branch pipelines?
2. What should a release job publish besides a version number?
3. Semantic versioning vs calendar versioning — when does each fit?
4. How do you prevent a rewritten tag from republishing artifacts?
5. Where do changelogs belong in the release process?

!!! tip "Sample answer — question 2"
    Confirm the pipeline ran on CI_COMMIT_TAG, artifacts uploaded, and the release object points at the intended commit SHA.

!!! tip "Sample answer — question 4"
    Protect release tags, sign artifacts when required, and keep provenance (commit SHA, pipeline ID). Do not reuse tags.
''',
    'security-scanning-and-devsecops': '''1. What is the difference between SAST and secret detection?
2. Security job is red on a dependency CVE — how do you respond in CI?
3. When is an allowlist acceptable for scanner findings?
4. How do you stop developers from disabling scanners on their branch?
5. What belongs in the pipeline versus a central security platform?

!!! tip "Sample answer — question 2"
    Triage by severity and exploitability: confirm the component is shipped, check for a fixed version, document temporary exceptions with expiry.

!!! tip "Sample answer — question 4"
    Keep scanners required on protected branches and never commit secrets to “fix” the detector.
''',
    'terraform-pipelines-in-gitlab': '''1. Why store terraform plan as an artifact before apply?
2. What does TF_IN_AUTOMATION change about Terraform CLI behaviour?
3. How do you keep state safe when plans run in CI?
4. Why is apply usually manual on the default branch?
5. How do you destroy lab infrastructure created in a pipeline experiment?

!!! tip "Sample answer — question 2"
    Confirm init backend config and that apply uses the exact plan artifact from the same pipeline. Drift and different variable sets between plan/apply are common.

!!! tip "Sample answer — question 4"
    Protect state with remote backends and restricted IAM/OIDC roles. Destroy experimental stacks in the same change window.
''',
    'testing-reports-and-quality-gates': '''1. How do JUnit report artifacts improve merge request feedback?
2. A quality gate flakes intermittently — what evidence do you gather?
3. Where should coverage thresholds live: CI job or shared policy?
4. Why keep allow_failure rare on security/unit gates?
5. How do you prevent skipped tests from counting as green?

!!! tip "Sample answer — question 2"
    Open the JUnit report and job log together: distinguish assertion failures from environment errors. Quarantine flakes with an owner rather than silently allow_failure.

!!! tip "Sample answer — question 4"
    Gates that protect production should fail closed. Ensure forks cannot skip required jobs while consuming protected variables.
''',
    'troubleshooting-gitlab-ci': '''1. Give a systematic order for debugging a red pipeline.
2. How do image entrypoints break scripts that work locally?
3. When is CI_DEBUG_TRACE appropriate — and when dangerous?
4. What runner vs project configuration mismatches look like?
5. How do you reproduce a CI failure on a laptop safely?

!!! tip "Sample answer — question 2"
    Read the first failing script line, confirm image/tag, then check rules/needs and variable availability.

!!! tip "Sample answer — question 4"
    Debug tracing can print secrets; use it only in isolated projects and rotate any credentials that may have been exposed.
''',
    'variables-secrets-and-oidc': '''1. Where should non-secret configuration live versus secret values?
2. OIDC job cannot assume a cloud role — what claims and settings do you verify?
3. What does masking actually guarantee in GitLab job logs?
4. Why prefer OIDC over long-lived cloud access keys in CI?
5. How do protected variables change merge request pipeline behaviour?

!!! tip "Sample answer — question 2"
    Verify id_tokens audience, the cloud identity provider trust policy (subject/ref/project), and that the job context may receive the token. Claim mismatches dominate.

!!! tip "Sample answer — question 4"
    OIDC issues short-lived credentials scoped by trust conditions, removing standing keys from GitLab variables. Never print the JWT.
''',
}

LABS_GHA: dict[str, str] = {
    'artifacts-and-caching': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** actions/cache patterns and upload/download-artifact across jobs

### Step 1 – Cache + artifact workflow

```bash
mkdir -p .github/workflows src
echo 'print(1)' > src/app.py
cat > .github/workflows/artifacts.yml << 'EOF'
name: Artifacts and caching
on: [push, workflow_dispatch]
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: |
          pip install pyyaml
          mkdir -p dist && cp src/app.py dist/
          echo "revision" > dist/REVISION
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
  verify:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: test -f dist/REVISION && cat dist/REVISION
EOF
```

### Step 2 – Confirm cache and artifact actions

```bash
grep -E 'upload-artifact|download-artifact|cache:' .github/workflows/artifacts.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'cicd-fundamentals-and-github-actions': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** first workflow with checkout, test, and artifact upload

### Step 1 – Scaffold app + workflow without expressions

```bash
mkdir -p .github/workflows src
cat > src/add.py << 'EOF'
def add(a, b):
    return a + b
EOF
cat > .github/workflows/ci.yml << 'EOF'
name: CI fundamentals
on: [push, pull_request, workflow_dispatch]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Test
        run: python -c "import sys; sys.path.insert(0,'src'); from add import add; assert add(1,2)==3"
      - name: Package
        run: tar czf app.tgz -C src add.py
      - uses: actions/upload-artifact@v4
        with:
          name: app-tgz
          path: app.tgz
EOF
```

### Step 2 – Validate workflow and run assertion locally

```bash
test -f .github/workflows/ci.yml
python3 -c "import sys; sys.path.insert(0,'src'); from add import add; assert add(1,2)==3; print('local-ok')"
grep -E 'upload-artifact|setup-python|permissions:' .github/workflows/ci.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'composite-actions-and-reusable-workflows': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** author a composite action and call it from a workflow

### Step 1 – Composite action + caller

```bash
mkdir -p .github/actions/hello .github/workflows
cat > .github/actions/hello/action.yml << 'EOF'
name: Hello composite
description: Greet and write an output file
inputs:
  name:
    required: true
runs:
  using: composite
  steps:
    - shell: bash
      run: |
        echo "Hello from composite"
        echo "ok" > "${GITHUB_WORKSPACE}/hello.out"
EOF
cat > .github/workflows/use-composite.yml << 'EOF'
name: Use composite
on: [workflow_dispatch, push]
permissions:
  contents: read
jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/hello
        with:
          name: rebash
      - run: test -f hello.out && cat hello.out
EOF

{% raw %}
```yaml
# Composite steps may use: echo "Hello ${{ inputs.name }}"
# Keep that expression inside {% raw %} when documenting on MkDocs pages.
```
{% endraw %}
```

### Step 2 – Validate composite action schema

```bash
grep -E 'using: composite|inputs:' .github/actions/hello/action.yml
grep 'uses: ./' .github/workflows/use-composite.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'docker-pipelines-with-github-actions': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Dockerfile plus build-push workflow (local build; push disabled)

### Step 1 – Dockerfile and workflow

```bash
mkdir -p .github/workflows
cat > Dockerfile << 'EOF'
FROM python:3.12-alpine
WORKDIR /app
COPY app.py .
USER nobody
CMD ["python", "app.py"]
EOF
echo 'print("gha docker lab")' > app.py

{% raw %}
```yaml
# .github/workflows/docker.yml
name: Docker pipelines
on: [push, workflow_dispatch]
permissions:
  contents: read
  packages: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: ghcr.io/example/demo:lab
          # production tags often use: ghcr.io/${{ github.repository }}/demo:${{ github.sha }}
```
{% endraw %}

cat > .github/workflows/docker.yml << 'EOF'
name: Docker pipelines
on: [push, workflow_dispatch]
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: ghcr.io/example/demo:lab
EOF
```

### Step 2 – Local docker build proof

```bash
docker build -t rebash-gha-lab:local .
docker run --rm rebash-gha-lab:local
docker rmi rebash-gha-lab:local
grep -E 'build-push-action|push: false' .github/workflows/docker.yml
```

### Final step – Cleanup note

```bash
docker rmi rebash-gha-lab:local 2>/dev/null || true
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'github-actions-basics-workflows-jobs-steps': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** map workflow → jobs → steps with needs between jobs

### Step 1 – Write multi-job workflow

```bash
mkdir -p .github/workflows
cat > .github/workflows/basics.yml << 'EOF'
name: Jobs and steps
on: [push, workflow_dispatch]
permissions:
  contents: read
jobs:
  prepare:
    runs-on: ubuntu-latest
    steps:
      - id: meta
        run: echo "stamp=$(date -u +%Y%m%dT%H%M%SZ)" >> "$GITHUB_OUTPUT"
  build:
    needs: prepare
    runs-on: ubuntu-latest
    steps:
      - run: mkdir -p out && echo ok > out/marker.txt
      - uses: actions/upload-artifact@v4
        with:
          name: marker
          path: out/marker.txt
EOF

{% raw %}
```yaml
# Example with outputs (expressions documented raw for mkdocs-macros)
# outputs:
#   stamp: ${{ steps.meta.outputs.stamp }}
# build job can read: ${{ needs.prepare.outputs.stamp }}
```
{% endraw %}
```

### Step 2 – Confirm needs and steps

```bash
grep -E 'needs:|steps:|upload-artifact' .github/workflows/basics.yml
test -f .github/workflows/basics.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'github-hosted-and-self-hosted-runners': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** contrast github-hosted labels with a self-hosted tagged job

### Step 1 – Hosted vs self-hosted definitions

```bash
mkdir -p .github/workflows notes
cat > notes/runners.md << 'EOF'
# Runner notes
- github-hosted: ubuntu-latest — patched by GitHub, ephemeral
- self-hosted: you patch OS, scale, isolate secrets
- Prefer labels like [self-hosted, linux, rebash]
EOF
cat > .github/workflows/runners.yml << 'EOF'
name: Runner shapes
on: [workflow_dispatch]
permissions:
  contents: read
jobs:
  hosted:
    runs-on: ubuntu-latest
    steps:
      - run: uname -a
  self_hosted_shape:
    runs-on: [self-hosted, linux, rebash]
    if: false
    steps:
      - run: echo "Enable when a labelled runner exists"
EOF
```

### Step 2 – Validate labels

```bash
grep -E 'ubuntu-latest|self-hosted' .github/workflows/runners.yml
test -f notes/runners.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'kubernetes-deployments-with-github-actions': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** kubectl dry-run deploy workflow with environment protection

### Step 1 – Manifests + deploy workflow

```bash
mkdir -p .github/workflows manifests
cat > manifests/deploy.yaml << 'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: demo
  namespace: rebash-lab
data:
  note: github-actions-k8s-lab
EOF
cat > .github/workflows/k8s.yml << 'EOF'
name: Kubernetes deploy shape
on: [workflow_dispatch]
permissions:
  contents: read
  id-token: write
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Client dry-run when kubectl exists
        run: |
          if command -v kubectl >/dev/null; then
            kubectl apply --dry-run=client -f manifests/
          else
            test -f manifests/deploy.yaml
          fi
  deploy_staging:
    needs: validate
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - run: echo "Wire cloud OIDC + kubectl apply for a real cluster"
EOF
```

### Step 2 – Validate manifests file

```bash
test -f manifests/deploy.yaml
grep -E 'environment: staging|dry-run' .github/workflows/k8s.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'multi-cloud-deployments-with-github-actions': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** OIDC-ready jobs for AWS and Azure shapes (file-only)

### Step 1 – Multi-cloud workflow

```bash
mkdir -p .github/workflows
cat > .github/workflows/multi-cloud.yml << 'EOF'
name: Multi-cloud deploy shapes
on: [workflow_dispatch]
permissions:
  contents: read
jobs:
  aws_oidc:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    environment: aws-staging
    steps:
      - run: echo "configure-aws-credentials when trust exists"
  azure_oidc:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    environment: azure-staging
    steps:
      - run: echo "azure/login with OIDC when federated credential exists"
EOF
```

### Step 2 – Confirm separate environments and id-token

```bash
grep -E 'id-token: write|aws-staging|azure-staging' .github/workflows/multi-cloud.yml
```

### Final step – Cleanup note

```bash
# File-only — no cloud calls
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'production-pipelines-and-environments': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** staging auto-deploy and production environment with concurrency gate

### Step 1 – Environment promotion workflow

```bash
mkdir -p .github/workflows
cat > .github/workflows/production.yml << 'EOF'
name: Production pipelines
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: prod-deploy
  cancel-in-progress: false
jobs:
  deploy_staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - run: echo "deploy staging"
  deploy_production:
    needs: deploy_staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - run: echo "production requires environment reviewers"
EOF
```

### Step 2 – Validate concurrency and environments

```bash
grep -E 'concurrency:|environment: production|needs: deploy_staging' .github/workflows/production.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'release-management-and-versioning': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** tag-driven release workflow publishing a changelog artifact

### Step 1 – Release workflow

```bash
mkdir -p .github/workflows
cat > CHANGELOG.md << 'EOF'
# Changelog
## Unreleased
- GHA release lab
EOF
cat > .github/workflows/release.yml << 'EOF'
name: Release
on:
  push:
    tags: ["v*"]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Package
        run: |
          mkdir -p dist
          cp CHANGELOG.md dist/
          echo "VERSION" > dist/VERSION
      - uses: actions/upload-artifact@v4
        with:
          name: release-dist
          path: dist/
EOF
```

### Step 2 – Check tag trigger and packaging

```bash
grep -E 'tags:|VERSION|CHANGELOG' .github/workflows/release.yml
test -f CHANGELOG.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'secrets-variables-and-oidc': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** separate vars/secrets and author an OIDC-ready job (file-only)

### Step 1 – Checklist + OIDC workflow

```bash
mkdir -p .github/workflows
cat > oidc-checklist.md << 'EOF'
- [ ] vars for non-secrets (DEMO_REGION)
- [ ] environment: staging for deploy secrets
- [ ] permissions: contents: read, id-token: write on OIDC jobs
- [ ] cloud trust on sub claim (repo + ref + environment)
- [ ] never echo secrets
EOF

{% raw %}
```yaml
# .github/workflows/secrets-and-oidc.yml
name: Secrets and OIDC
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  show-config:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Non-secret configuration
        env:
          DEMO_REGION: ${{ vars.DEMO_REGION }}
        run: |
          test -f oidc-checklist.md
          echo "DEMO_REGION=${DEMO_REGION:-unset}"
  staging-shape:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    permissions:
      contents: read
      id-token: write
    steps:
      - name: OIDC-ready placeholder
        run: echo "Add aws-actions/configure-aws-credentials when cloud trust exists"
```
{% endraw %}

# Persist a macros-safe copy without expressions for local tree checks:
cat > .github/workflows/secrets-and-oidc.yml << 'EOF'
name: Secrets and OIDC
on: [workflow_dispatch]
permissions:
  contents: read
jobs:
  show-config:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: test -f oidc-checklist.md
  staging-shape:
    runs-on: ubuntu-latest
    environment: staging
    permissions:
      contents: read
      id-token: write
    steps:
      - run: echo "OIDC-ready job has id-token: write"
EOF
```

### Step 2 – File-only validation

```bash
grep -E 'id-token: write|environment: staging' .github/workflows/secrets-and-oidc.yml
test -f oidc-checklist.md
```

### Final step – Cleanup note

```bash
# File-only OIDC lab — no cloud resources
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'security-scanning-and-supply-chain': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** secret hygiene job and supply-chain checklist

### Step 1 – Security workflow skeleton

```bash
mkdir -p .github/workflows
cat > SECURITY-CI.md << 'EOF'
- Enable secret scanning / push protection
- Pin actions to SHAs for high-assurance repos
- Least privilege permissions on workflows
- Review Dependabot PRs weekly
EOF
cat > .github/workflows/security.yml << 'EOF'
name: Security scanning
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
  security-events: write
jobs:
  secret_hygiene:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Basic secret grep
        run: |
          if grep -RInE '(AKIA[0-9A-Z]{16}|BEGIN (RSA |OPENSSH )?PRIVATE KEY)' .; then
            echo "Potential secret pattern found"; exit 1
          fi
          test -f SECURITY-CI.md
EOF
```

### Step 2 – Run local secret grep

```bash
grep -RInE '(AKIA[0-9A-Z]{16}|BEGIN (RSA |OPENSSH )?PRIVATE KEY)' . || echo "clean"
grep -E 'security-events|secret_hygiene' .github/workflows/security.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'terraform-pipelines-with-github-actions': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** plan/apply workflow with artifact plan and manual apply environment

### Step 1 – Terraform null provider + workflow

```bash
mkdir -p .github/workflows
cat > versions.tf << 'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
EOF
cat > main.tf << 'EOF'
resource "null_resource" "lab" {
  triggers = { note = "gha-tf-lab" }
}
EOF
cat > .github/workflows/terraform.yml << 'EOF'
name: Terraform
on: [push, workflow_dispatch]
permissions:
  contents: read
  id-token: write
jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init -backend=false
      - run: terraform plan -out=plan.cache
      - uses: actions/upload-artifact@v4
        with:
          name: plan
          path: plan.cache
  apply:
    needs: plan
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - uses: actions/download-artifact@v4
        with:
          name: plan
      - run: |
          terraform init -backend=false
          terraform apply -auto-approve plan.cache
EOF
```

### Step 2 – Local plan/destroy if terraform installed

```bash
if command -v terraform >/dev/null; then
  terraform init -backend=false
  terraform plan -out=plan.cache
  terraform apply -auto-approve plan.cache
  terraform destroy -auto-approve
fi
grep -E 'plan.cache|environment: production' .github/workflows/terraform.yml
```

### Final step – Cleanup note

```bash
terraform destroy -auto-approve 2>/dev/null || true
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'testing-in-github-actions': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** run pytest with JUnit and fail the job on test failure

### Step 1 – Test workflow with reporting

```bash
mkdir -p .github/workflows
cat > test_sample.py << 'EOF'
def test_truth():
    assert 2 + 2 == 4
EOF
cat > .github/workflows/test.yml << 'EOF'
name: Testing
on: [push, pull_request]
permissions:
  contents: read
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: |
          pip install pytest
          pytest --junitxml=junit.xml -q
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: junit
          path: junit.xml
EOF
```

### Step 2 – Local pytest + junit

```bash
python3 -m pytest --junitxml=junit.xml -q 2>/dev/null || python3 -c "assert 2+2==4"
test -f junit.xml || echo '<testsuite/>' > junit.xml
grep junit.xml .github/workflows/test.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'troubleshooting-github-actions': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** capture a failing step pattern and local reproduction

### Step 1 – Broken vs fixed workflow pair

```bash
mkdir -p .github/workflows
cat > triage.md << 'EOF'
1. Open the failed step log — first error
2. Confirm action version
3. Check permissions for GITHUB_TOKEN
4. Re-run failed jobs; debug logging only in private forks
5. Reproduce steps in a clean container
EOF
cat > .github/workflows/troubleshoot.yml << 'EOF'
name: Troubleshoot
on: [workflow_dispatch]
permissions:
  contents: read
jobs:
  broken_shape:
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - run: curl --fail https://example.invalid/missing
  fixed_shape:
    runs-on: ubuntu-latest
    steps:
      - run: curl --fail -I https://example.com | head -n 5
EOF
```

### Step 2 – Reproduce with Docker

```bash
docker run --rm curlimages/curl:8.10.1 curl --fail -I https://example.com | head -n 5
test -f triage.md
docker rmi curlimages/curl:8.10.1 2>/dev/null || true
```

### Final step – Cleanup note

```bash
docker rmi curlimages/curl:8.10.1 2>/dev/null || true
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
    'workflow-syntax-matrix-and-reusable': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** matrix workflow and reusable workflow caller/callee

### Step 1 – Create reusable + matrix workflows

```bash
mkdir -p .github/workflows
cat > .github/workflows/reusable-test.yml << 'EOF'
name: Reusable test
on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python --version
EOF
cat > .github/workflows/matrix.yml << 'EOF'
name: Matrix and reusable
on: [push, workflow_dispatch]
permissions:
  contents: read
jobs:
  matrix_probe:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python --version
  call_reusable:
    uses: ./.github/workflows/reusable-test.yml
    with:
      python-version: "3.12"
EOF

{% raw %}
```yaml
# When wiring matrix python version dynamically use:
# python-version: ${{ matrix.python }}
# inputs: ${{ inputs.python-version }}
# Wrap workflow files containing those expressions in {% raw %} on docs pages.
```
{% endraw %}
```

### Step 2 – Check matrix and workflow_call

```bash
grep -E 'matrix:|workflow_call:|uses: \./' -n .github/workflows/*.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later tutorials
```
''',
}

IQ_GHA: dict[str, str] = {
    'artifacts-and-caching': '''1. Cache vs artifact — which is authoritative for build outputs?
2. Cache restores but builds still slow — what else matters?
3. How do you pass files from job A to job B reliably?
4. What security caution applies to caches?
5. When should artifact retention be short?

!!! tip "Sample answer — question 2"
    Confirm upload/download names match and the producer job succeeded. Caches are best-effort acceleration, not a contract between jobs.

!!! tip "Sample answer — question 4"
    Do not cache secrets or writable shared directories across untrusted branches without careful keying.
''',
    'cicd-fundamentals-and-github-actions': '''1. What is the relationship between a workflow, a job, and a step?
2. A workflow is not starting on push — what do you verify first?
3. Why set top-level permissions even for simple CI?
4. How should secrets be referenced in GitHub Actions?
5. When do you choose workflow_dispatch over push triggers?

!!! tip "Sample answer — question 2"
    Check the on filters (branches/paths), whether Actions is enabled, and the Actions tab for skipped workflows. YAML indentation errors often prevent registration.

!!! tip "Sample answer — question 4"
    Default to read-only contents and open write permissions only where needed. Store secrets in GitHub Secrets/Environments and never print secret values.
''',
    'composite-actions-and-reusable-workflows': '''1. Composite action vs reusable workflow — when each?
2. How do inputs differ between the two?
3. Why can nested actions amplify supply-chain risk?
4. How do you test a composite action before publishing?
5. What metadata belongs in action.yml?

!!! tip "Sample answer — question 2"
    Confirm runs.using/workflow_call, input names, and relative uses paths. Most local composite failures are wrong working directory or missing shell on steps.

!!! tip "Sample answer — question 4"
    Pin dependencies inside shared actions and limit secrets passed into shared units.
''',
    'docker-pipelines-with-github-actions': '''1. Why keep push false until registry auth is ready?
2. How should image tags incorporate git SHA?
3. What permissions are needed to push to ghcr.io?
4. How does Buildx help multi-platform builds?
5. How do you avoid storing registry passwords in the Dockerfile?

!!! tip "Sample answer — question 2"
    Check Dockerfile context, Buildx setup, and whether push/tags match registry permissions.

!!! tip "Sample answer — question 4"
    Use OIDC or GITHUB_TOKEN/registry login actions; never bake credentials into layers.
''',
    'github-actions-basics-workflows-jobs-steps': '''1. How do needs and job outputs pass data between jobs?
2. Why might a step that works locally fail in Actions?
3. What is GITHUB_OUTPUT used for?
4. How can overly broad permissions write-all hurt you?
5. When should jobs be split versus one large job?

!!! tip "Sample answer — question 2"
    Confirm the upstream job published outputs, the downstream job declares needs, and expression syntax matches. Also check runner OS path differences.

!!! tip "Sample answer — question 4"
    Least-privilege tokens limit blast radius if a supply-chain step is compromised.
''',
    'github-hosted-and-self-hosted-runners': '''1. Pros and cons of github-hosted versus self-hosted runners?
2. Jobs queued forever on self-hosted — what do you check?
3. Why are labels important for runner pools?
4. What isolation risks do self-hosted runners have with public forks?
5. How do you patch and monitor self-hosted fleets?

!!! tip "Sample answer — question 2"
    Verify the runner is online, labels match runs-on, and the repository is allowed to use the runner group.

!!! tip "Sample answer — question 4"
    Never use self-hosted runners for untrusted public fork PRs without hard isolation.
''',
    'kubernetes-deployments-with-github-actions': '''1. How do you authenticate kubectl from GitHub Actions safely?
2. Why dry-run before apply in CI?
3. What role should a deploy job have in-cluster?
4. How do GitHub environments help Kubernetes promotions?
5. How do you roll back a bad deploy triggered by Actions?

!!! tip "Sample answer — question 2"
    Validate kubeconfig/OIDC exchange, namespace context, and client dry-run results before blaming the cluster.

!!! tip "Sample answer — question 4"
    Prefer short-lived credentials via OIDC, namespace-scoped Roles, and environment reviewers for production.
''',
    'multi-cloud-deployments-with-github-actions': '''1. How do you structure workflows for AWS and Azure without duplication?
2. What OIDC settings differ per cloud provider?
3. When are reusable workflows better than copy-paste jobs?
4. How do you prevent credential mix-ups across clouds?
5. Which checks should every cloud deploy share?

!!! tip "Sample answer — question 2"
    Verify environment names, id-token permissions, and the cloud-specific login action configuration.

!!! tip "Sample answer — question 4"
    Isolate roles per cloud/environment and keep production approvals separate.
''',
    'production-pipelines-and-environments': '''1. What protections do GitHub Environments provide?
2. Why use concurrency groups for production deploys?
3. How do you model staging then production promotion?
4. What evidence should a production deploy leave behind?
5. How do wait timers / reviewers change change management?

!!! tip "Sample answer — question 2"
    Check environment protection rules, required reviewers, and whether the job targeted the intended environment.

!!! tip "Sample answer — question 4"
    Store production secrets only on the production environment and require reviews.
''',
    'release-management-and-versioning': '''1. How do tag triggers differ from branch pushes?
2. What should a release artifact include for traceability?
3. Immutable tags — why do they matter?
4. How do you automate changelog generation safely?
5. Who should be allowed to publish releases?

!!! tip "Sample answer — question 2"
    Confirm the workflow ran on the tag ref, artifacts uploaded, and the release points at the expected commit.

!!! tip "Sample answer — question 4"
    Restrict contents write, protect release tags, and sign/attest artifacts when required.
''',
    'secrets-variables-and-oidc': '''1. Difference between vars and secrets?
2. OIDC cloud login fails — which trust settings do you inspect?
3. Why use environments for production secrets?
4. What does id-token write enable?
5. Why avoid pull_request_target with secrets?

!!! tip "Sample answer — question 2"
    Validate GitHub OIDC subject claims against the cloud IAM trust policy. Missing id-token write or wrong audience is frequent.

!!! tip "Sample answer — question 4"
    Prefer OIDC short-lived roles over long-lived cloud keys in repository secrets.
''',
    'security-scanning-and-supply-chain': '''1. Why pin third-party actions to commit SHAs?
2. What does dependency review add on pull requests?
3. How should teams handle a critical CVE in a base action/image?
4. What repository settings help prevent secret leaks?
5. How do workflow permissions reduce supply-chain impact?

!!! tip "Sample answer — question 2"
    Identify whether the finding is in direct dependencies, transitive packages, or the Action itself. Prefer patched versions and temporary exceptions with expiry.

!!! tip "Sample answer — question 4"
    Enable push protection/secret scanning and least-privilege permissions. Treat workflow YAML as production code.
''',
    'terraform-pipelines-with-github-actions': '''1. Why apply the exact plan artifact from the same workflow run?
2. What state backend considerations matter in CI?
3. When should apply require a GitHub environment approval?
4. How do you pass cloud credentials to Terraform in Actions?
5. How do you destroy experimental stacks created in labs?

!!! tip "Sample answer — question 2"
    Confirm init backend, matching variables between plan/apply, and that the plan artifact downloaded correctly.

!!! tip "Sample answer — question 4"
    Use OIDC-mapped least-privilege roles, protect state, and never commit tfstate. Destroy lab resources in the same session.
''',
    'testing-in-github-actions': '''1. How do you surface pytest failures clearly in PRs?
2. Flaky tests in CI only — what is your approach?
3. Why upload JUnit with if always?
4. How do path filters interact with required checks?
5. What belongs in unit versus integration jobs?

!!! tip "Sample answer — question 2"
    Read the pytest/JUnit output first, then compare dependency versions with local runs. Quarantine flakes with an owner.

!!! tip "Sample answer — question 4"
    Keep test jobs free of production secrets when possible; use ephemeral credentials for integration tests.
''',
    'troubleshooting-github-actions': '''1. Give a step-by-step triage for a red workflow.
2. When is Actions debug logging appropriate?
3. How do expression evaluation bugs show up?
4. What local tools help reproduce workflows?
5. How do you handle a compromised third-party action?

!!! tip "Sample answer — question 2"
    Open the failed step log first, confirm action versions and permissions, then re-run a single job after fixing.

!!! tip "Sample answer — question 4"
    Debug logs can leak secrets — enable briefly on private repos only and rotate credentials if exposure is possible.
''',
    'workflow-syntax-matrix-and-reusable': '''1. When is a build matrix the right tool?
2. How does workflow_call differ from workflow_run?
3. What does fail-fast false change in a matrix?
4. How do you version reusable workflows safely across repos?
5. What inputs/secrets patterns keep reusable workflows least-privileged?

!!! tip "Sample answer — question 2"
    Check matrix expansion in the UI, cancelled siblings from fail-fast, and whether the reusable workflow path/ref resolves.

!!! tip "Sample answer — question 4"
    Pin reusable workflows to tags/SHAs and pass only required secrets.
''',
}

LABS_GIT: dict[str, str] = {
    'advanced-git-workflows': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** practise worktrees and sparse checkout

### Step 1 – Worktree for a hotfix

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
mkdir -p services/a services/b
echo a > services/a/app.txt
echo b > services/b/app.txt
git add services && git commit -m "chore: monorepo baseline"
git worktree add ../hotfix-wt -b hotfix/log
cd ../hotfix-wt
echo fix >> services/a/app.txt
git add services/a/app.txt
git commit -m "fix: a logging"
cd -
git log --oneline hotfix/log -n 2
```

### Step 2 – Sparse checkout cone

```bash
git sparse-checkout init --cone
git sparse-checkout set services/a
ls services
git sparse-checkout disable
git worktree remove ../hotfix-wt 2>/dev/null || true
```

### Final step – Cleanup note

```bash
git worktree remove ../hotfix-wt 2>/dev/null || true
# Keep ~/rebash-git/ for later tutorials
```
''',
    'basic-git-workflow-add-commit-push': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** practise status → add → commit → log

### Step 1 – Edit, stage, commit

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo "service: api" > app.yaml
git add app.yaml
git commit -m "feat: add app.yaml skeleton"
echo "replicas: 2" >> app.yaml
git status
git diff
git add app.yaml
git commit -m "feat: set replicas to 2"
git log --oneline --decorate -n 5
```

### Step 2 – Partial staging awareness

```bash
echo "debug: true" >> app.yaml
echo "notes" > NOTES.txt
git add NOTES.txt
git status
git restore --staged NOTES.txt
git checkout -- app.yaml
git status
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'branching-fundamentals': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** create topic branches, switch, merge, delete

### Step 1 – Branch workflow

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo main > README.md
git add README.md && git commit -m "chore: main baseline"
git branch feature/login
git switch feature/login
echo "login" > login.txt
git add login.txt && git commit -m "feat: login stub"
git switch -
git branch -vv
git log --oneline --decorate --graph --all
```

### Step 2 – Merge feature to main

```bash
git merge feature/login -m "merge: feature/login"
git branch --merged
git branch -d feature/login
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'cherry-pick-and-reflog': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** cherry-pick a commit and recover via reflog

### Step 1 – Cherry-pick across branches

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo main > a.txt && git add a.txt && git commit -m "chore: main"
git switch -c feature/hotfix
echo fix > fix.txt && git add fix.txt && git commit -m "fix: critical hotfix"
HOTFIX=$(git rev-parse HEAD)
git switch -
git cherry-pick "$HOTFIX"
git log --oneline -n 5
```

### Step 2 – Recover with reflog after hard reset

```bash
echo oops > oops.txt && git add oops.txt && git commit -m "chore: oops"
OOPS=$(git rev-parse HEAD)
git reset --hard HEAD~1
git reflog -n 8
git cherry-pick "$OOPS"
git log --oneline -n 6
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'creating-and-cloning-repositories': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** create a bare remote and practise clone/fetch

### Step 1 – Bare remote + clone

```bash
mkdir -p remote work
git init --bare remote/app.git
git clone remote/app.git work/app
cd work/app
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo "v1" > VERSION
git add VERSION && git commit -m "chore: initial VERSION"
git push -u origin HEAD
```

### Step 2 – Second clone and pull

```bash
git clone remote/app.git work/app2
cd work/app2
git log --oneline -n 3
cat VERSION
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'git-bisect-and-debugging-history': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** use git bisect to find the commit that broke a script

### Step 1 – Create good→bad history

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
cat > check.sh << 'EOF'
#!/usr/bin/env bash
grep -q OK data.txt
EOF
chmod +x check.sh
echo OK > data.txt
git add check.sh data.txt && git commit -m "chore: good"
for i in 1 2 3 4; do echo "noise $i" >> noise.txt; git add noise.txt && git commit -m "chore: noise $i"; done
echo BAD > data.txt
git add data.txt && git commit -m "fix: accidentally break data"
for i in 5 6; do echo "noise $i" >> noise.txt; git add noise.txt && git commit -m "chore: noise $i"; done
```

### Step 2 – Bisect to the breaking commit

```bash
git bisect start
git bisect bad HEAD
git bisect good HEAD~7
git bisect run ./check.sh
git bisect reset
git log --oneline -n 12
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'git-for-infrastructure-as-code': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** structure an IaC-friendly repo with modules layout and ignore state

### Step 1 – IaC layout and ignores

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
mkdir -p modules/network envs/dev
cat > .gitignore << 'EOF'
.terraform/
*.tfstate
*.tfstate.*
crash.log
EOF
echo '# network module stub' > modules/network/main.tf
echo '# root module for dev' > envs/dev/main.tf
echo "local mock state — must not commit" > terraform.tfstate
git add .gitignore modules envs
git status
git check-ignore -v terraform.tfstate
git commit -m "chore: IaC layout with state ignored"
```

### Step 2 – Prove state is not tracked

```bash
git ls-files | grep -i tfstate && exit 1 || echo "state not tracked"
git ls-files
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'git-hooks-and-automation': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** install a pre-commit hook that blocks .env files

### Step 1 – Local hook

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
if git diff --cached --name-only | grep -E '(^|/)\.env$|\.pem$'; then
  echo "Refuse to commit secrets (.env/.pem)" >&2
  exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
echo ok > ok.txt
git add ok.txt && git commit -m "chore: ok file"
```

### Step 2 – Prove the hook blocks secrets

```bash
echo SECRET=1 > .env
git add .env
if git commit -m "bad"; then echo "hook failed to block"; exit 1; else echo "hook blocked secret commit"; fi
git reset HEAD .env
rm -f .env
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'git-in-ci-cd-and-devops': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** tag a release commit and export CI-friendly git metadata

### Step 1 – Commits + annotated tag

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo "1.0.0" > VERSION
git add VERSION && git commit -m "chore: version 1.0.0"
git tag -a v1.0.0 -m "release 1.0.0"
echo "1.0.1" > VERSION
git add VERSION && git commit -m "fix: patch 1.0.1"
git describe --tags --always
git show v1.0.0 --no-patch
```

### Step 2 – Export CI-friendly metadata

```bash
echo "GIT_SHA=$(git rev-parse HEAD)"
echo "GIT_DESCRIBE=$(git describe --tags --always)"
echo "GIT_TREE=$(git rev-parse 'HEAD^{tree}')"
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'git-installation-and-configuration': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** set useful local defaults and verify with git config --list

### Step 1 – Local config for this lab

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
git config core.editor "true"
git config pull.rebase false
git config --local --list | sort
```

### Step 2 – Compare identity and aliases

```bash
git config --get user.name
git config --get user.email
git config alias.st status
git st
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'git-submodules-and-subtrees': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** add a submodule from a local bare repo and update it

### Step 1 – Create dependency repo and add submodule

```bash
mkdir -p modules
git init --bare modules/lib.git
git clone modules/lib.git modules/lib-work
cd modules/lib-work
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo "lib-v1" > VERSION
git add VERSION && git commit -m "chore: lib v1"
git push origin HEAD
cd ../..
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
git submodule add ./modules/lib.git third_party/lib
git commit -m "chore: add lib submodule"
git submodule status
```

### Step 2 – Update submodule pointer

```bash
cd modules/lib-work
echo "lib-v2" > VERSION
git add VERSION && git commit -m "chore: lib v2"
git push origin HEAD
cd ../..
cd third_party/lib && git pull && cd ../..
git add third_party/lib
git commit -m "chore: bump lib submodule"
git submodule status
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'git-troubleshooting': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** recover from detached HEAD and run fsck/gc

### Step 1 – Detached HEAD recovery

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo 1 > f.txt && git add f.txt && git commit -m "chore: 1"
echo 2 > f.txt && git add f.txt && git commit -m "chore: 2"
git switch --detach HEAD~1
echo "detached work" > detached.txt
git add detached.txt && git commit -m "wip: detached"
git switch -c recover/detached
git switch main
git merge recover/detached -m "merge: recover detached work"
git log --oneline --graph -n 8
```

### Step 2 – Refresh index after messy state

```bash
git status
git fsck --no-full
git gc --quiet
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'github-actions-for-devops': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** add a minimal GitHub Actions workflow to a git repo

### Step 1 – Repo + workflow

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
name: CI
on: [push, pull_request]
permissions:
  contents: read
jobs:
  probe:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: test -f README.md
EOF
echo "# devops git lab" > README.md
git add .
git commit -m "ci: add minimal workflow"
git log --oneline -n 3
```

### Step 2 – Validate workflow present in git tree

```bash
git ls-files .github/workflows/ci.yml
grep -E 'checkout@v4|permissions:' .github/workflows/ci.yml
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'github-fundamentals': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** model a fork/PR workflow locally with two remotes

### Step 1 – Upstream + fork remotes

```bash
mkdir -p upstream.git fork.git
git init --bare upstream.git
git init --bare fork.git
git clone upstream.git product
cd product
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo "api" > README.md
git add README.md && git commit -m "chore: readme"
git push origin HEAD
git remote add fork ../fork.git
git push fork HEAD
git remote -v
```

### Step 2 – Feature branch ready for PR

```bash
cd product
git switch -c feature/docs
echo "more" >> README.md
git add README.md && git commit -m "docs: expand readme"
git push -u fork HEAD
git log --oneline --decorate -n 5
cat > pr-notes.md << 'EOF'
Open a Pull Request from fork/feature/docs into upstream/main
EOF
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'gitignore-and-gitattributes': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** write .gitignore / .gitattributes and prove ignored files stay out

### Step 1 – Ignore secrets and set attributes

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
cat > .gitignore << 'EOF'
.env
*.pem
__pycache__/
dist/
EOF
cat > .gitattributes << 'EOF'
*.sh text eol=lf
*.tf text eol=lf
EOF
echo "SECRET=do-not-commit" > .env
echo "print('x')" > app.py
git add .gitignore .gitattributes app.py
git status
git check-ignore -v .env
git commit -m "chore: ignore secrets and set attributes"
```

### Step 2 – Demonstrate force-add danger then undo

```bash
git add -f .env || true
git reset HEAD .env 2>/dev/null || true
rm -f .env
git status
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'gitops-fundamentals': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** env-repo style declarative manifests and image tag bump

### Step 1 – Env repo style commit

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
mkdir -p apps/demo overlays/prod
cat > apps/demo/deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo
spec:
  replicas: 1
  selector: {matchLabels: {app: demo}}
  template:
    metadata: {labels: {app: demo}}
    spec:
      containers:
        - name: demo
          image: ghcr.io/example/demo:1.0.0
EOF
cat > overlays/prod/kustomization.yaml << 'EOF'
resources:
  - ../../apps/demo
images:
  - name: ghcr.io/example/demo
    newTag: 1.0.0
EOF
git add apps overlays
git commit -m "gitops: add demo deployment at 1.0.0"
```

### Step 2 – Bump image tag as a GitOps change

```bash
sed -i.bak 's/1.0.0/1.0.1/g' overlays/prod/kustomization.yaml apps/demo/deployment.yaml
rm -f overlays/prod/kustomization.yaml.bak apps/demo/deployment.yaml.bak
git diff
git add apps overlays
git commit -m "gitops: bump demo to 1.0.1"
git log --oneline -n 3
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'introduction-to-git-and-version-control': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** initialise a repo and make your first commit

### Step 1 – Init and first commit

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
printf '# Git lab\n' > README.md
git add README.md
git status
git commit -m "docs: add README for git introduction lab"
git log --oneline -n 3
```

### Step 2 – Inspect working tree vs last commit

```bash
echo "note=$(date -u +%Y-%m-%d)" >> README.md
git status
git diff
git checkout -- README.md
git status
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'merging-and-merge-conflicts': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** create a real merge conflict and resolve it

### Step 1 – Divergent edits

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo "colour=blue" > config.env
git add config.env && git commit -m "chore: config"
git switch -c feature/a
echo "colour=azure" > config.env
git add config.env && git commit -m "feat: azure colour"
git switch -
git switch -c feature/b
echo "colour=navy" > config.env
git add config.env && git commit -m "feat: navy colour"
git switch -
git merge feature/a -m "merge: feature/a"
git merge feature/b || true
git status
```

### Step 2 – Resolve conflict

```bash
printf 'colour=navy\n' > config.env
git add config.env
git commit -m "merge: resolve colour conflict in favour of navy"
git log --oneline --graph --all -n 8
cat config.env
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'production-git-practices': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** encode protected-branch practices: CODEOWNERS + conventional commits

### Step 1 – Production practices files

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
mkdir -p .github
cat > .github/CODEOWNERS << 'EOF'
* @platform-team
/terraform/ @platform-team @sre-team
EOF
cat > CONTRIBUTING.md << 'EOF'
- Conventional commits: feat|fix|docs|chore
- No force-push to main
- PR required; CI green
EOF
git add .github CONTRIBUTING.md
git commit -m "docs: production git practices"
```

### Step 2 – Branch protection reminder commit

```bash
cat > protect-main.md << 'EOF'
Enable branch protection: require PR, status checks, disallow force push
EOF
git add protect-main.md && git commit -m "docs: branch protection reminder"
git log --oneline -n 3
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'pull-requests-and-code-review': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** prepare a small PR with conventional commits and review checklist

### Step 1 – Feature branch + review checklist

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo base > app.txt
git add app.txt && git commit -m "chore: base"
git switch -c feature/rate-limit
printf 'rate_limit: 100\n' > policy.yaml
git add policy.yaml
git commit -m "feat: add rate limit policy"
cat > REVIEW.md << 'EOF'
## PR checklist
- [ ] Title summarises intent
- [ ] Commits are reviewable units
- [ ] No secrets
- [ ] Rollback noted
EOF
git add REVIEW.md && git commit -m "docs: add PR checklist"
git log --oneline main..HEAD
```

### Step 2 – Show PR diff range

```bash
git diff main...HEAD
git status
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'rebasing-and-interactive-rebase': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** rebase a feature branch onto main and inspect reflog

### Step 1 – Create divergent history and rebase

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo base > app.txt
git add app.txt && git commit -m "chore: base"
git switch -c feature/x
echo feature >> app.txt
git add app.txt && git commit -m "feat: feature line"
git switch -
echo main >> app.txt
git add app.txt && git commit -m "fix: main line"
git switch feature/x
git rebase main
git log --oneline --graph --all -n 10
```

### Step 2 – Safety check with reflog

```bash
git reflog -n 10
git status
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'repository-management-and-releases': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** practise release branches, tags, and bundle archive

### Step 1 – Release branch and tag

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo "app" > README.md
git add README.md && git commit -m "chore: init"
git switch -c release/1.2
echo "1.2.0" > VERSION
git add VERSION && git commit -m "release: 1.2.0"
git tag -a v1.2.0 -m "1.2.0"
git switch -
git merge release/1.2 -m "merge: release 1.2"
git tag -l 'v*'
git branch -a
```

### Step 2 – Bundle for archive

```bash
git bundle create repo.bundle --all
git bundle verify repo.bundle
ls -lh repo.bundle
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'signed-commits-and-git-security': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** document SSH signing setup and inspect commit metadata

### Step 1 – Signing checklist + baseline commit

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
cat > signing-notes.md << 'EOF'
# Signed commits
- git config gpg.format ssh
- git config user.signingkey ~/.ssh/id_ed25519.pub
- git config commit.gpgsign true
- Verify with: git log --show-signature
EOF
echo "signed-lab" > README.md
git add README.md signing-notes.md
git commit -m "docs: signing notes (enable SSH signing when keys exist)"
git log -1 --format='%H %G? %s'
```

### Step 2 – Inspect commit headers

```bash
git cat-file -p HEAD | sed -n '1,12p'
test -f signing-notes.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'understanding-the-git-object-model': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** inspect blobs/trees/commits with cat-file and rev-parse

### Step 1 – Create objects and inspect

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo hello > hello.txt
git add hello.txt
git commit -m "chore: hello"
COMMIT=$(git rev-parse HEAD)
TREE=$(git rev-parse 'HEAD^{tree}')
echo "commit=$COMMIT"
echo "tree=$TREE"
git cat-file -t "$COMMIT"
git cat-file -p "$COMMIT"
git cat-file -p "$TREE"
```

### Step 2 – Blob content

```bash
BLOB=$(git rev-parse HEAD:hello.txt)
git cat-file -p "$BLOB"
git rev-list --objects --all | head
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'undoing-changes-reset-revert-stash': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** practise stash, restore, and revert

### Step 1 – Stash and restore

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo v1 > file.txt
git add file.txt && git commit -m "chore: v1"
echo dirty >> file.txt
git stash push -m "wip dirty"
git status
git stash list
git stash pop
git restore file.txt
git status
```

### Step 2 – Revert a commit

```bash
echo v2 > file.txt
git add file.txt && git commit -m "feat: v2"
git revert HEAD --no-edit
git log --oneline -n 5
cat file.txt
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'viewing-history-and-diffs': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** read history with log/diff/show

### Step 1 – Build history worth inspecting

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo a > file.txt && git add file.txt && git commit -m "chore: add file"
echo b >> file.txt && git add file.txt && git commit -m "feat: append b"
echo c >> file.txt && git add file.txt && git commit -m "feat: append c"
git log --oneline --graph -n 5
git show HEAD --stat
git diff HEAD~2 HEAD
```

### Step 2 – Search history

```bash
git log -S'b' --oneline
git log -p -n 1
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
    'working-with-remotes': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** add remotes, fetch, track branches, and prune

### Step 1 – Local bare remote simulation

```bash
mkdir -p origin.git workspace
git init --bare origin.git
git init workspace
cd workspace
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo r1 > README.md
git add README.md && git commit -m "chore: readme"
git remote add origin ../origin.git
git push -u origin HEAD
git remote -v
git fetch origin
git branch -vv
```

### Step 2 – Prune deleted remote branch

```bash
cd workspace
git push origin HEAD:refs/heads/temp
git push origin --delete temp
git fetch --prune
git branch -r
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```
''',
}

IQ_GIT: dict[str, str] = {
    'advanced-git-workflows': '''1. When do worktrees beat multiple clones?
2. What problems does sparse checkout solve?
3. Partial clone options for huge repos?
4. Risks of custom merge drivers?
5. How do you keep advanced workflows teachable for a team?

!!! tip "Sample answer — question 2"
    Check worktree list and sparse-checkout status when files appear missing.

!!! tip "Sample answer — question 4"
    Document team workflows; keep hooks and custom drivers reviewed like production automation.
''',
    'basic-git-workflow-add-commit-push': '''1. What does the staging area allow you to do?
2. You committed the wrong file — how do you fix it safely before push?
3. What makes a good commit message for IaC changes?
4. Why review git status before every commit?
5. When should you amend versus make a new commit?

!!! tip "Sample answer — question 2"
    If not pushed, restore --staged / soft reset can reshape the commit. If pushed and shared, prefer a follow-up commit.

!!! tip "Sample answer — question 4"
    Never amend commits that others have based work on. Keep secrets out with status/diff review.
''',
    'branching-fundamentals': '''1. What is a branch in Git's data model?
2. How do you list merged versus unmerged branches?
3. Feature branch naming conventions you recommend?
4. When is deleting a branch safe?
5. How do long-lived branches create risk?

!!! tip "Sample answer — question 2"
    Use git branch --merged/--no-merged and compare SHAs with main before deleting.

!!! tip "Sample answer — question 4"
    Protect main/release branches and require PRs.
''',
    'cherry-pick-and-reflog': '''1. When is cherry-pick better than merging a whole branch?
2. What does reflog record that git log does not?
3. Cherry-pick conflict handling?
4. How long is reflog kept by default roughly?
5. Dangers of cherry-picking the same fix twice?

!!! tip "Sample answer — question 2"
    Use git reflog to find the pre-change HEAD and cherry-pick or branch from that SHA.

!!! tip "Sample answer — question 4"
    Cherry-picking hotfixes into multiple release branches needs clear tracking to avoid duplicate fixes.
''',
    'creating-and-cloning-repositories': '''1. Difference between git init and git clone?
2. Clone succeeds but push is denied — what do you verify?
3. What is a bare repository used for?
4. How do you clone only a single branch for a large repo?
5. Why verify remote URL before first push?

!!! tip "Sample answer — question 2"
    Confirm remote permissions, SSH keys/auth, and that you are pushing to the intended URL (git remote -v).

!!! tip "Sample answer — question 4"
    Use least-privilege deploy keys. Never embed tokens in remote URLs that might be logged.
''',
    'git-bisect-and-debugging-history': '''1. How does bisect find a bad commit?
2. What makes a good automated bisect run script?
3. Limitations of bisect with flaky tests?
4. How do you mark skip commits?
5. What do you do after bisect names a commit?

!!! tip "Sample answer — question 2"
    Ensure you can script a deterministic good/bad test, then git bisect reset after collecting the SHA.

!!! tip "Sample answer — question 4"
    Do not bisect on production data stores. Keep repro scripts free of credentials.
''',
    'git-for-infrastructure-as-code': '''1. Which IaC files must never be committed?
2. How do you structure envs versus modules in Git?
3. Why are small commits valuable for terraform plan review?
4. How do CODEOWNERS help IaC paths?
5. What remote state considerations pair with Git workflows?

!!! tip "Sample answer — question 2"
    Confirm .gitignore excludes state and .terraform/, then review git status before commit.

!!! tip "Sample answer — question 4"
    Protect main, require plans in CI, and keep cloud credentials out of the repo.
''',
    'git-hooks-and-automation': '''1. Client-side versus server-side hooks?
2. Why aren't .git/hooks committed by default?
3. What should a pre-commit hook check in DevOps repos?
4. How do hooks fail closed without blocking emergencies?
5. Risks of downloading hook scripts from the internet?

!!! tip "Sample answer — question 2"
    Confirm the hook is executable and runs in the expected shell. Reproduce by running the hook script directly.

!!! tip "Sample answer — question 4"
    Do not bypass hooks on production repos without audit. Prefer managed frameworks pinned to reviewed versions.
''',
    'git-in-ci-cd-and-devops': '''1. Which git metadata should CI inject into artifacts?
2. Why prefer commit SHA tags over latest?
3. How do annotated tags support releases?
4. What breaks if CI checks out a shallow clone?
5. How do you trace a production binary back to git?

!!! tip "Sample answer — question 2"
    Print git rev-parse HEAD / git describe in the failing job and confirm checkout depth.

!!! tip "Sample answer — question 4"
    Sign releases when needed and keep provenance (SHA, pipeline ID).
''',
    'git-installation-and-configuration': '''1. Which Git config scopes exist (system/global/local)?
2. Commits show the wrong author — how do you fix it going forward?
3. Why set pull.rebase or merge explicitly?
4. What risks come from sharing a machine Git identity?
5. How do credential helpers interact with HTTPS remotes?

!!! tip "Sample answer — question 2"
    Check git config --show-origin user.name/user.email to see which scope wins.

!!! tip "Sample answer — question 4"
    Do not put PATs in plain config files. Prefer SSH keys or OS keychain-backed helpers.
''',
    'git-submodules-and-subtrees': '''1. Submodule versus subtree — operational differences?
2. Why do clones miss submodule content by default?
3. How do you bump a submodule pointer safely?
4. Common CI pitfalls with submodules?
5. When would you vendor instead?

!!! tip "Sample answer — question 2"
    Check .gitmodules, that git submodule update --init ran, and that the parent commit points at an existing submodule SHA.

!!! tip "Sample answer — question 4"
    Pin submodule URLs to trusted sources and review pointer bumps like dependency upgrades.
''',
    'git-troubleshooting': '''1. Detached HEAD — what happened and how do you keep work?
2. Index lock file errors — causes?
3. How do you approach possible object corruption?
4. Authentication loops with HTTPS remotes?
5. How do you recover a deleted branch?

!!! tip "Sample answer — question 2"
    Create a branch from the detached SHA immediately if you have commits to keep, then merge back.

!!! tip "Sample answer — question 4"
    Do not run experimental fsck repairs on the only copy of a production repo — clone/mirror first.
''',
    'github-actions-for-devops': '''1. How does a git push start CI on GitHub?
2. Why keep workflow YAML in the same repo as code?
3. What permissions should a basic CI workflow use?
4. How do required status checks relate to branch protection?
5. Where do you look when CI is green but deploy failed?

!!! tip "Sample answer — question 2"
    Open the Actions run for the commit SHA and confirm the workflow file path. Required checks must match actual job names.

!!! tip "Sample answer — question 4"
    Least-privilege permissions, pinned actions, and no secrets in forks.
''',
    'github-fundamentals': '''1. Fork versus branch in the same remote?
2. What does origin usually mean after clone?
3. How do GitHub permissions map to push/merge rights?
4. SSH versus HTTPS authentication trade-offs?
5. What is a good first repository hygiene checklist?

!!! tip "Sample answer — question 2"
    Verify remotes, default branch, and whether you have write access. SSO authorisation on SSH keys is a frequent enterprise gotcha.

!!! tip "Sample answer — question 4"
    Enable branch protection, 2FA, and secret scanning.
''',
    'gitignore-and-gitattributes': '''1. How do you ignore a file already tracked?
2. What is .gitattributes useful for in cross-platform teams?
3. Why ignore Terraform state?
4. How do you verify ignore rules?
5. Can ignore rules protect secrets by themselves?

!!! tip "Sample answer — question 2"
    Use git check-ignore -v and git status --ignored. Untrack with git rm --cached if needed.

!!! tip "Sample answer — question 4"
    Ignore rules are not security controls — use secret scanning and rotate if leaked.
''',
    'gitops-fundamentals': '''1. What does desired state in Git mean operationally?
2. App repo versus env repo patterns?
3. How do image tag bumps become deployments?
4. What happens if someone kubectl-edits live cluster state?
5. Security controls for who can merge to env repos?

!!! tip "Sample answer — question 2"
    Compare Git desired manifests to live cluster state and controller sync status. Drift often means manual changes or failed reconciles.

!!! tip "Sample answer — question 4"
    Protect env repos with strong reviews and least-privilege deploy identities for controllers.
''',
    'introduction-to-git-and-version-control': '''1. What problem does version control solve for infrastructure teams?
2. Working tree dirty unexpectedly — what commands do you run first?
3. Difference between distributed VCS and centralised VCS?
4. Why commit small, reviewable changes in DevOps repos?
5. What should never be committed even in a private repo?

!!! tip "Sample answer — question 2"
    Run git status and git diff to see whether changes are staged, unstaged, or untracked.

!!! tip "Sample answer — question 4"
    Exclude secrets, state files, and credentials with .gitignore and secret scanning.
''',
    'merging-and-merge-conflicts': '''1. Fast-forward versus merge commit — when each?
2. Walk through resolving a conflict responsibly.
3. Why might you abort a merge?
4. How do CODEOWNERS interact with contested files?
5. What merge strategies appear in DevOps repos?

!!! tip "Sample answer — question 2"
    Run git status to list unmerged paths, choose the correct result, git add, then commit. Do not mark conflicts resolved without understanding both sides.

!!! tip "Sample answer — question 4"
    Never bypass required reviews to force a conflicted production path.
''',
    'production-git-practices': '''1. List branch protection settings you enable on main.
2. How do you handle hotfixes under protected branches?
3. Why ban force-push on production branches?
4. What audit trail should a production change leave in git?
5. How do you onboard contractors with least privilege?

!!! tip "Sample answer — question 2"
    Confirm protection rules, required checks, and that the merge used the expected strategy.

!!! tip "Sample answer — question 4"
    Enforce SSO, 2FA, CODEOWNERS on sensitive paths, and short-lived access.
''',
    'pull-requests-and-code-review': '''1. What makes a high-quality PR for infrastructure?
2. How do you review Terraform/Kubernetes changes safely?
3. Draft PRs — when useful?
4. How should CODEOWNERS be used without bottlenecks?
5. What is rubber-stamp review risk?

!!! tip "Sample answer — question 2"
    Read the diff and risk areas first (IAM, network, data loss), then ask for tests/rollback notes. Block on secrets immediately.

!!! tip "Sample answer — question 4"
    Require reviews for sensitive paths and never approve changes you do not understand.
''',
    'rebasing-and-interactive-rebase': '''1. What does rebase rewrite, and when is that dangerous?
2. Golden rule of rebasing shared history?
3. Interactive rebase uses — squash/fixup/edit/reword?
4. How do you abort a painful rebase?
5. Rebase versus merge for feature branches?

!!! tip "Sample answer — question 2"
    If conflicts explode, git rebase --abort returns you to the pre-rebase state. Use reflog if you already completed a bad rebase.

!!! tip "Sample answer — question 4"
    Do not rebase commits already pushed to shared branches without team agreement.
''',
    'repository-management-and-releases': '''1. Release branch versus tagging on main?
2. How do you yank a bad release safely?
3. What belongs in a release checklist?
4. How do bundles/archives help disaster recovery?
5. Who should have permission to create release tags?

!!! tip "Sample answer — question 2"
    Verify tag points at the intended SHA (git show), artifacts match that SHA, and release notes are complete.

!!! tip "Sample answer — question 4"
    Protect tags, restrict releasers, and store checksums.
''',
    'signed-commits-and-git-security': '''1. Why sign commits/tags in an enterprise?
2. SSH signing versus GPG — trade-offs?
3. How do you verify signatures in git log?
4. What does commit signing not prove?
5. How do web-of-trust / key directories fit?

!!! tip "Sample answer — question 2"
    Check user.signingkey, gpg.format, and whether the public key is registered on the host.

!!! tip "Sample answer — question 4"
    Signing keys are high value — protect them and revoke promptly on loss. Signing does not replace code review.
''',
    'understanding-the-git-object-model': '''1. Explain blob, tree, commit, and tag objects.
2. How does a commit point to a tree?
3. What makes Git content-addressed?
4. How do you inspect an object with plumbing commands?
5. Why does rewriting history change commit hashes?

!!! tip "Sample answer — question 2"
    Use git rev-parse and git cat-file -p on HEAD and its tree to see the object graph.

!!! tip "Sample answer — question 4"
    Signed commits/tags bind identity to hashes. Rewriting published history breaks signatures.
''',
    'undoing-changes-reset-revert-stash': '''1. reset vs revert vs restore — when each?
2. You need to undo a commit already on main — safest option?
3. What does stash not include by default?
4. Hard reset risks?
5. How do you recover a commit after reset?

!!! tip "Sample answer — question 2"
    For published main history prefer git revert. Use reflog to find SHAs after a local reset.

!!! tip "Sample answer — question 4"
    Hard reset can delete uncommitted work. Coordinate before rewriting shared branches.
''',
    'viewing-history-and-diffs': '''1. When do you use git show versus git diff?
2. How do you find which commit introduced a string?
3. What does git log -p give you in an incident?
4. How do path filters help in monorepos?
5. Binary files break diffs — what options help?

!!! tip "Sample answer — question 2"
    Start with git log --oneline on the affected path, then git show on the suspicious commit. Use -S/-G to search history.

!!! tip "Sample answer — question 4"
    Avoid pasting sensitive diffs into tickets; redact secrets.
''',
    'working-with-remotes': '''1. What do fetch, pull, and push each do?
2. Upstream tracking branch — why set it?
3. How does fetch --prune help?
4. Multiple remotes — typical fork workflow?
5. Force-with-lease versus force push?

!!! tip "Sample answer — question 2"
    Inspect git remote -v and git status -sb. Auth failures and non-fast-forward rejects are common push blockers.

!!! tip "Sample answer — question 4"
    Prefer --force-with-lease over --force and avoid force-pushing protected branches.
''',
}

LABS_DOCKER: dict[str, str] = {
    'building-images-with-dockerfile': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** write a Dockerfile, build a tagged image, and run it

### Step 1 – Dockerfile build

```bash
cat > app.py << 'EOF'
print("hello from dockerfile lab")
EOF
cat > Dockerfile << 'EOF'
FROM python:3.12-alpine
WORKDIR /app
COPY app.py .
USER nobody
CMD ["python", "app.py"]
EOF
docker build -t rebash-df:lab .
docker run --rm rebash-df:lab
```

### Step 2 – Inspect image and cleanup

```bash
docker image inspect rebash-df:lab --format '{{ "{{" }}.Config.User{{ "}}" }}'
docker rmi rebash-df:lab
```

### Final step – Cleanup note

```bash
docker rmi rebash-df:lab 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'container-logging-and-monitoring': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** generate logs, fetch with docker logs, inspect logging driver

### Step 1 – Logging exercises

```bash
docker run -d --name rebash-log alpine:3.20 sh -c 'for i in 1 2 3 4 5; do echo "tick=$i"; sleep 0.2; done; sleep 30'
sleep 2
docker logs rebash-log
docker logs --since 1m rebash-log
docker inspect rebash-log --format '{{ "{{" }}.HostConfig.LogConfig.Type{{ "}}" }}'
```

### Step 2 – Cleanup

```bash
docker rm -f rebash-log
```

### Final step – Cleanup note

```bash
docker rm -f rebash-log 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'container-registries-and-distribution': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** tag for a registry path and practise save/load offline distribution

### Step 1 – Registry tagging patterns

```bash
docker pull alpine:3.20
docker tag alpine:3.20 ghcr.io/example/rebash-alpine:lab
docker image inspect ghcr.io/example/rebash-alpine:lab --format '{{ "{{" }}.RepoTags{{ "}}" }}'
docker save ghcr.io/example/rebash-alpine:lab -o image.tar
ls -lh image.tar
cat > registry-notes.md << 'EOF'
- Prefer digest pins for production
- Auth via credential helpers / OIDC in CI
EOF
```

### Step 2 – Cleanup

```bash
rm -f image.tar
docker rmi ghcr.io/example/rebash-alpine:lab
```

### Final step – Cleanup note

```bash
rm -f image.tar
docker rmi ghcr.io/example/rebash-alpine:lab 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'container-scanning-and-sbom': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** build an image and run a vulnerability scan when tools exist

### Step 1 – Build + scan attempt

```bash
cat > Dockerfile << 'EOF'
FROM alpine:3.20
RUN apk add --no-cache curl
USER nobody
CMD ["curl", "--version"]
EOF
docker build -t rebash-scan:lab .
if command -v trivy >/dev/null; then
  trivy image --severity HIGH,CRITICAL rebash-scan:lab || true
else
  echo "Install Trivy or Docker Scout for CVE scanning"
  docker image inspect rebash-scan:lab --format '{{ "{{" }}.Id{{ "}}" }}'
fi
echo "Generate SBOMs in CI and store as artefacts" > sbom-notes.md
```

### Step 2 – Cleanup image

```bash
docker rmi rebash-scan:lab
```

### Final step – Cleanup note

```bash
docker rmi rebash-scan:lab 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'docker-architecture-and-components': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** map client/daemon/images/containers with inspect output

### Step 1 – Explore architecture objects

```bash
docker pull nginx:alpine
docker create --name rebash-arch nginx:alpine
docker inspect rebash-arch --format 'image={{ "{{" }}.Image{{ "}}" }}'
docker image inspect nginx:alpine --format 'id={{ "{{" }}.Id{{ "}}" }}'
docker system df
```

### Step 2 – Cleanup create-only container

```bash
docker rm rebash-arch
docker ps -a --filter name=rebash-arch
```

### Final step – Cleanup note

```bash
docker rm -f rebash-arch 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'docker-capstone-and-next-steps': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** compose a small stack with volume, then full teardown

### Step 1 – Capstone stack

```bash
cat > compose.yaml << 'EOF'
services:
  web:
    image: nginx:alpine
    ports: ["18086:80"]
    volumes: ["rebash-cap:/usr/share/nginx/html:ro"]
volumes:
  rebash-cap:
EOF
docker volume create rebash-cap
docker run --rm -v rebash-cap:/data alpine:3.20 sh -c 'echo "<h1>capstone</h1>" > /data/index.html'
docker compose up -d
curl -s http://127.0.0.1:18086 | head -n 5
```

### Step 2 – Full teardown

```bash
docker compose down -v
docker volume rm rebash-cap 2>/dev/null || true
```

### Final step – Cleanup note

```bash
docker compose down -v 2>/dev/null || true
docker volume rm rebash-cap 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'docker-compose-fundamentals': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** run a two-service Compose stack and tear it down

### Step 1 – Compose file up

```bash
cat > compose.yaml << 'EOF'
services:
  web:
    image: nginx:alpine
    ports: ["18082:80"]
  redis:
    image: redis:7-alpine
EOF
docker compose up -d
docker compose ps
curl -sI http://127.0.0.1:18082 | head -n 5
docker compose exec redis redis-cli PING
```

### Step 2 – Down and remove

```bash
docker compose down -v
docker compose ps -a
```

### Final step – Cleanup note

```bash
docker compose down -v 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'docker-in-ci-cd-pipelines': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Dockerfile plus CI-shaped local build script tagged with git SHA

### Step 1 – Build script mimicking CI

```bash
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
cat > Dockerfile << 'EOF'
FROM alpine:3.20
COPY VERSION /VERSION
CMD ["cat", "/VERSION"]
EOF
echo "0.1.0" > VERSION
git add Dockerfile VERSION
git commit -m "chore: docker ci lab"
SHA=$(git rev-parse --short HEAD)
docker build -t rebash-ci:$SHA .
docker run --rm rebash-ci:$SHA
echo "built rebash-ci:$SHA" | tee build.out
```

### Step 2 – Cleanup tags

```bash
SHA=$(git rev-parse --short HEAD)
docker rmi rebash-ci:$SHA
```

### Final step – Cleanup note

```bash
docker rmi $(docker images -q rebash-ci) 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'docker-installation-and-setup': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** verify Docker Engine install and daemon connectivity

### Step 1 – Daemon and client checks

```bash
docker version
docker info --format '{{ "{{" }}.ServerVersion{{ "}}" }} {{ "{{" }}.Driver{{ "}}" }}'
docker pull alpine:3.20
docker run --rm alpine:3.20 uname -a
```

### Step 2 – Permission / context notes

```bash
docker context ls
id
cat > install-notes.md << 'EOF'
- Prefer Docker Engine from official docs for your OS
- docker group is root-equivalent — grant carefully
- Consider rootless mode when isolation requires it
EOF
```

### Final step – Cleanup note

```bash
docker rmi alpine:3.20 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'docker-networking-fundamentals': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** create a user-defined bridge network and connect two containers

### Step 1 – Network and DNS by name

```bash
docker network create rebash-net
docker run -d --name rebash-web --network rebash-net nginx:alpine
docker run --rm --network rebash-net curlimages/curl:8.10.1 curl -sI http://rebash-web/ | head -n 5
docker network inspect rebash-net --format '{{ "{{" }}json .Containers{{ "}}" }}' | head -c 400; echo
```

### Step 2 – Cleanup network resources

```bash
docker rm -f rebash-web
docker network rm rebash-net
```

### Final step – Cleanup note

```bash
docker rm -f rebash-web 2>/dev/null || true
docker network rm rebash-net 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'docker-performance-and-resource-limits': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** apply CPU/memory limits and observe with docker stats

### Step 1 – Constrained container

```bash
docker run -d --name rebash-lim --memory=64m --cpus=0.50 nginx:alpine
docker stats rebash-lim --no-stream
docker inspect rebash-lim --format 'mem={{ "{{" }}.HostConfig.Memory{{ "}}" }} nano_cpus={{ "{{" }}.HostConfig.NanoCpus{{ "}}" }}'
```

### Step 2 – Cleanup

```bash
docker rm -f rebash-lim
```

### Final step – Cleanup note

```bash
docker rm -f rebash-lim 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'docker-security-hardening': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** run as non-root, drop capabilities, read security options

### Step 1 – Hardening flags

```bash
docker run -d --name rebash-sec --user 101:101 --read-only --cap-drop ALL --cap-add NET_BIND_SERVICE nginx:alpine
docker exec rebash-sec id
docker inspect rebash-sec --format 'user={{ "{{" }}.Config.User{{ "}}" }} readonly={{ "{{" }}.HostConfig.ReadonlyRootfs{{ "}}" }}'
docker inspect rebash-sec --format '{{ "{{" }}json .HostConfig.CapDrop{{ "}}" }}'
```

### Step 2 – Cleanup

```bash
docker rm -f rebash-sec
```

### Final step – Cleanup note

```bash
docker rm -f rebash-sec 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'docker-swarm-orchestration-basics': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** initialise a local swarm, deploy a service, then leave swarm

### Step 1 – Swarm service lab

```bash
docker swarm init || docker info --format '{{ "{{" }}.Swarm.LocalNodeState{{ "}}" }}'
docker service create --name rebash-web --publish 18083:80 --replicas 2 nginx:alpine
docker service ls
docker service ps rebash-web
curl -sI http://127.0.0.1:18083 | head -n 5
```

### Step 2 – Remove service and leave swarm

```bash
docker service rm rebash-web
docker swarm leave --force || true
```

### Final step – Cleanup note

```bash
docker service rm rebash-web 2>/dev/null || true
docker swarm leave --force 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'dockerfile-best-practices-and-multi-stage-builds': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** build a multi-stage image and compare history

### Step 1 – Multi-stage Dockerfile

```bash
cat > hello.go << 'EOF'
package main
import "fmt"
func main() { fmt.Println("multi-stage ok") }
EOF
cat > Dockerfile << 'EOF'
FROM golang:1.22-alpine AS build
WORKDIR /src
COPY hello.go .
RUN go build -o /out/hello hello.go
FROM alpine:3.20
COPY --from=build /out/hello /usr/local/bin/hello
USER nobody
ENTRYPOINT ["/usr/local/bin/hello"]
EOF
docker build -t rebash-ms:lab .
docker run --rm rebash-ms:lab
docker images rebash-ms:lab
```

### Step 2 – Show layers / cleanup

```bash
docker history rebash-ms:lab | head -n 15
docker rmi rebash-ms:lab
```

### Final step – Cleanup note

```bash
docker rmi rebash-ms:lab 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'environment-variables-and-secrets': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** pass env files safely and avoid baking secrets into images

### Step 1 – Env file runtime inject

```bash
cat > app.env << 'EOF'
APP_MODE=lab
GREETING=hello
EOF
cat > Dockerfile << 'EOF'
FROM alpine:3.20
CMD ["sh", "-c", "echo mode=$APP_MODE greeting=$GREETING"]
EOF
docker build -t rebash-env:lab .
docker run --rm --env-file app.env rebash-env:lab
docker image inspect rebash-env:lab --format '{{ "{{" }}json .Config.Env{{ "}}" }}'
```

### Step 2 – Cleanup

```bash
rm -f app.env
docker rmi rebash-env:lab
```

### Final step – Cleanup note

```bash
rm -f app.env
docker rmi rebash-env:lab 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'from-docker-to-kubernetes': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** map a running container to Kubernetes YAML (dry-run if kubectl exists)

### Step 1 – Docker run vs Deployment YAML

```bash
docker run -d --name rebash-bridge -p 18084:80 nginx:alpine
cat > deploy.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: rebash-lab
spec:
  replicas: 1
  selector: {matchLabels: {app: web}}
  template:
    metadata: {labels: {app: web}}
    spec:
      containers:
        - name: web
          image: nginx:alpine
          ports: [{containerPort: 80}]
EOF
command -v kubectl >/dev/null && kubectl apply --dry-run=client -f deploy.yaml || true
curl -sI http://127.0.0.1:18084 | head -n 3
```

### Step 2 – Cleanup docker side

```bash
docker rm -f rebash-bridge
```

### Final step – Cleanup note

```bash
docker rm -f rebash-bridge 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'introduction-to-containers-and-docker': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** run a container, inspect it, and clean up completely

### Step 1 – Run and inspect

```bash
docker version
docker run -d --name rebash-intro -p 18080:80 nginx:alpine
docker ps --filter name=rebash-intro
curl -sI http://127.0.0.1:18080 | head -n 5
docker logs rebash-intro 2>&1 | head -n 20
docker inspect rebash-intro --format '{{ "{{" }}.State.Status{{ "}}" }} {{ "{{" }}.Config.Image{{ "}}" }}'
```

### Step 2 – Exec and cleanup

```bash
docker exec rebash-intro nginx -v
docker stop rebash-intro
docker rm rebash-intro
docker ps -a --filter name=rebash-intro
```

### Final step – Cleanup note

```bash
docker rm -f rebash-intro 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'production-docker-patterns': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** production-minded flags: restart policy, healthcheck

### Step 1 – Production-shaped run

```bash
cat > Dockerfile << 'EOF'
FROM nginx:alpine
HEALTHCHECK --interval=5s --timeout=2s --retries=3 CMD wget -qO- http://127.0.0.1/ || exit 1
EOF
docker build -t rebash-prod:lab .
docker run -d --name rebash-prod --restart=on-failure:3 -p 18085:80 rebash-prod:lab
sleep 6
docker inspect rebash-prod --format 'health={{ "{{" }}if .State.Health{{ "}}" }}{{ "{{" }}.State.Health.Status{{ "}}" }}{{ "{{" }}else{{ "}}" }}none{{ "{{" }}end{{ "}}" }}'
curl -sI http://127.0.0.1:18085 | head -n 3
```

### Step 2 – Cleanup

```bash
docker rm -f rebash-prod
docker rmi rebash-prod:lab
```

### Final step – Cleanup note

```bash
docker rm -f rebash-prod 2>/dev/null || true
docker rmi rebash-prod:lab 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'running-your-first-container': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** run, publish ports, view logs, and remove the container

### Step 1 – Foreground then detached

```bash
docker run --rm alpine:3.20 echo "hello from alpine"
docker run -d --name rebash-first -p 18081:80 nginx:alpine
curl -s http://127.0.0.1:18081 | head -n 3
docker logs rebash-first --tail 20
```

### Step 2 – Stop and remove

```bash
docker stop rebash-first
docker rm rebash-first
docker ps -a --filter name=rebash-first
```

### Final step – Cleanup note

```bash
docker rm -f rebash-first 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'troubleshooting-docker-containers': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** debug a failing container with logs, inspect, and a corrected run

### Step 1 – Broken then fixed

```bash
docker run -d --name rebash-bad alpine:3.20 sh -c 'echo boom; exit 1'
sleep 1
docker ps -a --filter name=rebash-bad
docker logs rebash-bad
docker inspect rebash-bad --format 'exit={{ "{{" }}.State.ExitCode{{ "}}" }}'
docker rm -f rebash-bad
docker run -d --name rebash-good alpine:3.20 sh -c 'echo ok; sleep 30'
docker logs rebash-good
```

### Step 2 – Cleanup

```bash
docker rm -f rebash-bad rebash-good
```

### Final step – Cleanup note

```bash
docker rm -f rebash-bad rebash-good 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'volumes-and-persistent-storage': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** persist data with a named volume across container recreate

### Step 1 – Write then recreate

```bash
docker volume create rebash-data
docker run --rm -v rebash-data:/data alpine:3.20 sh -c 'echo persisted > /data/note.txt'
docker run --rm -v rebash-data:/data alpine:3.20 cat /data/note.txt
docker volume inspect rebash-data --format '{{ "{{" }}.Mountpoint{{ "}}" }}'
```

### Step 2 – Remove volume

```bash
docker volume rm rebash-data
docker volume ls | grep rebash || echo "volume removed"
```

### Final step – Cleanup note

```bash
docker volume rm rebash-data 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
    'working-with-docker-images': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** pull, tag, save/load, and remove images

### Step 1 – Image operations

```bash
docker pull alpine:3.20
docker images alpine
docker tag alpine:3.20 rebash-alpine:lab
docker save rebash-alpine:lab -o rebash-alpine.tar
docker rmi rebash-alpine:lab
docker load -i rebash-alpine.tar
docker images rebash-alpine
```

### Step 2 – Cleanup local artifacts

```bash
rm -f rebash-alpine.tar
docker rmi rebash-alpine:lab
```

### Final step – Cleanup note

```bash
rm -f rebash-alpine.tar
docker rmi rebash-alpine:lab 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
''',
}

IQ_DOCKER: dict[str, str] = {
    'building-images-with-dockerfile': '''1. What do FROM/COPY/RUN/CMD/ENTRYPOINT each do?
2. Build context is huge — how do you shrink it?
3. Why avoid running as root in the final image?
4. Difference between CMD and ENTRYPOINT?
5. How do build args differ from runtime env?

!!! tip "Sample answer — question 2"
    Read the Dockerfile and docker history; rebuild with --progress=plain to see failing RUN lines.

!!! tip "Sample answer — question 4"
    Do not COPY secrets into layers. Use multi-stage builds and non-root users.
''',
    'container-logging-and-monitoring': '''1. Default Docker logging driver behaviour?
2. How do you avoid disk fill from container logs?
3. What should app logs include for operations?
4. Logs disappear after container rm — implications?
5. How does this change on Kubernetes?

!!! tip "Sample answer — question 2"
    Check logging driver in inspect, docker logs, and host disk usage.

!!! tip "Sample answer — question 4"
    Do not log secrets. Centralise logs with retention/access controls.
''',
    'container-registries-and-distribution': '''1. What is a content digest?
2. How do you authenticate to a private registry in CI?
3. Tag mutation risks?
4. Promotion patterns between registries?
5. How do mirrors/caches help enterprises?

!!! tip "Sample answer — question 2"
    Verify digests and repository permissions. Auth errors dominate first-push failures.

!!! tip "Sample answer — question 4"
    Use short-lived CI credentials/OIDC and immutable tags/digests for prod.
''',
    'container-scanning-and-sbom': '''1. What is an SBOM and why store it in CI?
2. How do you triage a CRITICAL CVE in a base image?
3. Scanner false positives — how do you handle them?
4. When should a pipeline fail on findings?
5. Difference between image scan and runtime detection?

!!! tip "Sample answer — question 2"
    Confirm the package is present in the final image and whether a fixed base exists.

!!! tip "Sample answer — question 4"
    Gate production on policy and keep SBOMs as artifacts for incident response.
''',
    'docker-architecture-and-components': '''1. Role of dockerd versus the CLI?
2. What storage driver concerns matter on Linux?
3. How do containerd/runc fit the stack?
4. Why does architecture knowledge help troubleshooting?
5. What is the difference between create and run?

!!! tip "Sample answer — question 2"
    Use docker info and inspect to see driver/runtime details.

!!! tip "Sample answer — question 4"
    Limit who can talk to the daemon socket.
''',
    'docker-capstone-and-next-steps': '''1. Which Docker skills are prerequisites for Kubernetes?
2. How would you demonstrate production readiness of an image?
3. What cleanup habits prevent lab debt?
4. When do you graduate from Compose to an orchestrator?
5. What personal lab project would you build next?

!!! tip "Sample answer — question 2"
    Re-run the capstone stack from a clean directory and confirm teardown leaves no containers/volumes.

!!! tip "Sample answer — question 4"
    Carry forward non-root images, scanning, and secret hygiene into Kubernetes/Helm/GitOps next steps.
''',
    'docker-compose-fundamentals': '''1. What problem does Compose solve locally?
2. How do you tear down including volumes?
3. Service DNS names in Compose?
4. Compose versus Swarm/Kubernetes for production?
5. How do you override config per environment?

!!! tip "Sample answer — question 2"
    Run docker compose ps and docker compose logs for the failing service.

!!! tip "Sample answer — question 4"
    Do not commit .env secrets.
''',
    'docker-in-ci-cd-pipelines': '''1. Why tag CI images with git SHA?
2. DinD versus Kaniko/Buildah trade-offs?
3. How do you cache layers safely in CI?
4. What should not be in CI build contexts?
5. How do you prove provenance of an image?

!!! tip "Sample answer — question 2"
    Check Dockerfile path/context, registry login, and whether the job ran on the expected commit SHA.

!!! tip "Sample answer — question 4"
    Never use long-lived registry passwords in clear logs. Prefer OIDC.
''',
    'docker-installation-and-setup': '''1. What does membership in the docker group imply on Linux?
2. Client works but daemon errors — where do you look?
3. Rootless Docker — when would you choose it?
4. How do you verify Engine versus Compose plugin install?
5. What is a Docker context used for?

!!! tip "Sample answer — question 2"
    Run docker version/docker info and inspect daemon logs. Permission denied on the socket usually means group/context issues.

!!! tip "Sample answer — question 4"
    Treat docker.sock access as root-equivalent.
''',
    'docker-networking-fundamentals': '''1. Bridge versus host versus none networks?
2. How do containers resolve each other by name?
3. Published ports versus container ports?
4. When do custom networks beat the default bridge?
5. How do you inspect connectivity failures?

!!! tip "Sample answer — question 2"
    Use docker network inspect and confirm both containers share the network.

!!! tip "Sample answer — question 4"
    Avoid host networking unless required; it weakens isolation.
''',
    'docker-performance-and-resource-limits': '''1. How do --memory and --cpus protect a host?
2. What does docker stats show you?
3. OOM kills — how do you confirm?
4. When do limits cause false failures?
5. How do cgroups relate to containers?

!!! tip "Sample answer — question 2"
    Use docker stats and inspect OOM fields / exit codes.

!!! tip "Sample answer — question 4"
    Set limits in shared environments so one container cannot starve neighbours.
''',
    'docker-security-hardening': '''1. List three hardening flags you use on docker run.
2. Why drop capabilities?
3. Read-only root filesystem — when it breaks apps?
4. Risks of privileged containers?
5. How do user namespaces help?

!!! tip "Sample answer — question 2"
    Inspect HostConfig for privileged, capabilities, and mounts.

!!! tip "Sample answer — question 4"
    Default deny: non-root, cap-drop ALL, no privileged, minimal mounts.
''',
    'docker-swarm-orchestration-basics': '''1. Swarm service versus standalone container?
2. How do you publish ports for a service?
3. When would you still choose Swarm vs Kubernetes?
4. How do you drain a node?
5. Secret handling differences in Swarm?

!!! tip "Sample answer — question 2"
    Inspect docker service ps for task failures and node availability.

!!! tip "Sample answer — question 4"
    Protect manager nodes and use Swarm secrets.
''',
    'dockerfile-best-practices-and-multi-stage-builds': '''1. How do multi-stage builds improve security and size?
2. What should the final stage contain?
3. Layer caching tips that actually help CI?
4. Why order Dockerfile instructions carefully?
5. When is distroless a good final base?

!!! tip "Sample answer — question 2"
    Compare image sizes and docker history before/after multi-stage.

!!! tip "Sample answer — question 4"
    Keep build tools out of production images and pin base digests.
''',
    'environment-variables-and-secrets': '''1. Why are ENV instructions in Dockerfiles risky for secrets?
2. Runtime --env-file versus build-time ARG?
3. How can secrets still leak via docker inspect?
4. Better secret patterns for Swarm/Kubernetes?
5. How do you rotate a secret used by containers?

!!! tip "Sample answer — question 2"
    Inspect the image config and container env to see whether a secret was baked in.

!!! tip "Sample answer — question 4"
    Use secret managers / orchestrator secret objects and short rotation intervals.
''',
    'from-docker-to-kubernetes': '''1. Map Docker run flags to Kubernetes fields.
2. Why isn't Compose a production orchestrator for most enterprises?
3. What stays the same when moving images to Kubernetes?
4. How do probes differ from Docker HEALTHCHECK?
5. What operational skills transfer directly?

!!! tip "Sample answer — question 2"
    Compare the working docker run/compose config to Deployment/Service YAML. Client dry-run catches API mistakes early.

!!! tip "Sample answer — question 4"
    Keep image supply-chain controls; move secrets to Kubernetes Secret/CSI providers.
''',
    'introduction-to-containers-and-docker': '''1. How does a container differ from a virtual machine?
2. Container exits immediately — what do you check first?
3. What is an image versus a container?
4. Why is cleanup (docker rm) part of every lab?
5. Where do containers fit in Cloud/DevOps workflows?

!!! tip "Sample answer — question 2"
    Check docker ps -a for exit code, then docker logs and the container command.

!!! tip "Sample answer — question 4"
    Prefer official images, avoid privileged mode, and never put secrets in image layers.
''',
    'production-docker-patterns': '''1. Restart policies you use in production?
2. Healthchecks — what should they verify?
3. Immutable infrastructure with containers means what?
4. How do you handle config changes safely?
5. Resource requests/limits mindset even on Docker hosts?

!!! tip "Sample answer — question 2"
    Inspect restart policy and health state, then application logs.

!!! tip "Sample answer — question 4"
    Non-root, minimal images, scanned bases, no secrets in images.
''',
    'running-your-first-container': '''1. What do -d, --name, and -p do?
2. Port publish fails — typical causes?
3. How do you get a shell in a running container?
4. Difference between stop and rm?
5. Why prefer --rm for ephemeral experiments?

!!! tip "Sample answer — question 2"
    Confirm the container is running, the published port mapping, and that nothing else bound the host port.

!!! tip "Sample answer — question 4"
    Do not publish administrative ports to 0.0.0.0 on untrusted networks.
''',
    'troubleshooting-docker-containers': '''1. Give a triage order for a failing container.
2. How do you copy files out for offline analysis?
3. When does docker diff help?
4. Name resolution fails inside a container — steps?
5. Disk full on Docker host — what do you reclaim first?

!!! tip "Sample answer — question 2"
    Status/exit code → logs → inspect config/mounts/networks → run an interactive replacement with the same flags.

!!! tip "Sample answer — question 4"
    Do not paste secret-bearing env dumps into tickets.
''',
    'volumes-and-persistent-storage': '''1. Named volume versus bind mount trade-offs?
2. What happens to a named volume on docker rm?
3. How do permissions problems show up with mounts?
4. Backup approach for volume data?
5. Security risks of bind-mounting docker.sock?

!!! tip "Sample answer — question 2"
    Confirm the mount in docker inspect and file paths inside the container.

!!! tip "Sample answer — question 4"
    Never mount docker.sock into untrusted containers.
''',
    'working-with-docker-images': '''1. What does an image tag represent?
2. How do save/load help air-gapped environments?
3. Why pin digests in production?
4. What does docker images not tell you about vulnerabilities?
5. How do you delete dangling images safely?

!!! tip "Sample answer — question 2"
    Verify tags with docker image inspect and confirm the digest you expect.

!!! tip "Sample answer — question 4"
    Only pull from trusted registries; scan before promoting.
''',
}

LABS_AWS: dict[str, str] = {
    'aws-fundamentals-and-global-infrastructure': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** verify identity and explore regions with describe APIs

### Step 1 – Caller identity and regions

```bash
aws sts get-caller-identity
aws configure get region || true
aws ec2 describe-regions --query 'Regions[].RegionName' --output text | tr '\t' '\n' | head
```

### Step 2 – Record lab notes (no create)

```bash
cat > notes.md << 'EOF'
- Region choice affects latency, services, and data residency
- AZ codes are account-mapped
- Prefer STS/OIDC over long-lived access keys
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'aws-security-services': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** read-only tour of CloudTrail/GuardDuty/Security Hub/Config

### Step 1 – Security services probe

```bash
aws sts get-caller-identity
aws cloudtrail describe-trails --query 'trailList[].{Name:Name,MultiRegion:IsMultiRegionTrail}' --output table 2>/dev/null || true
aws guardduty list-detectors --output table 2>/dev/null || echo "GuardDuty not enabled or no permission"
aws securityhub describe-hub 2>/dev/null || echo "Security Hub not enabled or no permission"
aws configservice describe-configuration-recorders --output table 2>/dev/null || true
```

### Step 2 – Control checklist

```bash
cat > security-controls.md << 'EOF'
- CloudTrail organisation trail + log file validation
- GuardDuty + Security Hub aggregation
- Config rules for required tags / public access blocks
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'cicd-on-aws': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** inventory CodePipeline/CodeBuild; OIDC trust checklist (file-only)

### Step 1 – CI/CD service inventory

```bash
aws sts get-caller-identity
aws codepipeline list-pipelines --query 'pipelines[].name' --output table 2>/dev/null || true
aws codebuild list-projects --output table 2>/dev/null || true
aws iam list-open-id-connect-providers --output table 2>/dev/null || true
```

### Step 2 – OIDC trust checklist

```bash
cat > oidc-aws-checklist.md << 'EOF'
- IdP: token.actions.githubusercontent.com or GitLab issuer
- Condition on sub: repo + ref + environment
- Role permissions least privilege for deploy
- No long-lived AKIA keys in CI variables
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'compute-ec2-asg-and-load-balancing': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** inventory EC2/ASG/ELB with describe APIs

### Step 1 – Describe compute landscape

```bash
aws sts get-caller-identity
aws ec2 describe-instances --query 'Reservations[].Instances[].{Id:InstanceId,State:State.Name,Type:InstanceType}' --output table
aws elbv2 describe-load-balancers --query 'LoadBalancers[].{Name:LoadBalancerName,Type:Type}' --output table 2>/dev/null || true
aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[].{Name:AutoScalingGroupName,Desired:DesiredCapacity}' --output table 2>/dev/null || true
```

### Step 2 – Optional create skipped by default

```bash
echo "Skipped create by default — describe-only is enough"
echo "If you launch an instance: aws ec2 terminate-instances --instance-ids <id>"
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'containers-ecs-eks-ecr': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** inspect ECR/ECS/EKS; optional ephemeral ECR repo create+delete

### Step 1 – Container services inventory

```bash
aws sts get-caller-identity
aws ecr describe-repositories --query 'repositories[].repositoryName' --output table 2>/dev/null || true
aws ecs list-clusters --output table 2>/dev/null || true
aws eks list-clusters --output table 2>/dev/null || true
```

### Step 2 – Optional ephemeral ECR repo

```bash
REPO="rebash-lab-$(date +%s)"
aws ecr create-repository --repository-name "$REPO" --tags Key=rebash,Value=lab
aws ecr describe-repositories --repository-names "$REPO" --query 'repositories[0].repositoryUri' --output text
aws ecr delete-repository --repository-name "$REPO" --force
echo "ECR repo deleted"
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'cost-optimisation-on-aws': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** hunt idle resources; Cost Explorer when permitted

### Step 1 – Cost and idle resource hunt

```bash
aws sts get-caller-identity
aws ce get-cost-and-usage --time-period Start=$(date -u -v-7d +%F 2>/dev/null || date -u -d '7 days ago' +%F),End=$(date -u +%F) --granularity DAILY --metrics UnblendedCost --query 'ResultsByTime[-3:].Total.UnblendedCost' --output table 2>/dev/null || echo "ce:GetCostAndUsage not permitted — continue with idle checks"
aws ec2 describe-addresses --query 'Addresses[?AssociationId==null].PublicIp' --output table
aws elbv2 describe-load-balancers --query 'LoadBalancers[].LoadBalancerName' --output table 2>/dev/null || true
```

### Step 2 – Tagging standard notes

```bash
cat > cost-tags.md << 'EOF'
Required tags: Owner, Project, Environment, Expiry
Hunt weekly: unattached EIPs, idle ALBs, old EBS, unused NAT
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'databases-on-aws': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** describe RDS/DynamoDB without creating paid databases

### Step 1 – Read-only database inventory

```bash
aws sts get-caller-identity
aws rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,Engine:Engine,MultiAZ:MultiAZ}' --output table
aws dynamodb list-tables --output table
```

### Step 2 – Design notes instead of creating RDS

```bash
cat > db-notes.md << 'EOF'
- Prefer Multi-AZ for HA; know backup windows
- Do not create RDS in labs without tagging + destroy alarm
- Secrets Manager / IAM auth over passwords in apps
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'iam-identity-access-and-organizations': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** inspect caller identity and IAM (read-only)

### Step 1 – Identity inventory

```bash
aws sts get-caller-identity
aws iam list-account-aliases --output text || true
aws iam get-user --output json 2>/dev/null | head -c 400 || echo "likely using a role — expected with SSO"
```

### Step 2 – Least-privilege checklist

```bash
cat > iam-checklist.md << 'EOF'
- Prefer roles + STS / OIDC over access keys
- SCPs for organisation guardrails
- MFA on humans; separate break-glass
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
# No IAM users/keys created
```
''',
    'infrastructure-as-code-on-aws': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** CloudFormation validate a tiny template; optional create/delete

### Step 1 – Template validate

```bash
aws sts get-caller-identity
cat > bucket.yaml << 'EOF'
AWSTemplateFormatVersion: '2010-09-09'
Description: rebash lab bucket
Resources:
  LabBucket:
    Type: AWS::S3::Bucket
    Properties:
      Tags:
        - Key: rebash
          Value: lab
Outputs:
  BucketName:
    Value: !Ref LabBucket
EOF
aws cloudformation validate-template --template-body file://bucket.yaml
```

### Step 2 – Optional create/delete stack skipped by default

```bash
echo "Validated template only by default"
echo "If created: aws cloudformation delete-stack --stack-name <name>"
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE --query 'StackSummaries[0:5].StackName' --output table
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'monitoring-and-observability-on-aws': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** list CloudWatch alarms/log groups (read-only)

### Step 1 – Observability inventory

```bash
aws sts get-caller-identity
aws cloudwatch describe-alarms --query 'MetricAlarms[0:10].{Name:AlarmName,State:StateValue}' --output table
aws logs describe-log-groups --limit 10 --query 'logGroups[].logGroupName' --output table
```

### Step 2 – Alarm design notes

```bash
cat > monitoring-notes.md << 'EOF'
Alert on symptoms customers feel; attach runbooks
Avoid paging on raw CPU without SLO context
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'production-aws-landing-zones': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** inspect Organisations layout when permitted; document OU intent

### Step 1 – Org read-only probe

```bash
aws sts get-caller-identity
aws organizations describe-organization 2>/dev/null || echo "No org access — use notes path"
aws organizations list-accounts --query 'Accounts[].{Id:Id,Name:Name}' --output table 2>/dev/null || true
```

### Step 2 – Landing zone sketch

```bash
cat > landing-zone.md << 'EOF'
OUs: Security, Infrastructure, Sandbox, Workloads
Security account: Log Archive, Audit
SCP: deny leave org, deny disable CloudTrail
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'reliability-and-disaster-recovery': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** map Multi-AZ resources and backup settings

### Step 1 – HA/DR signals

```bash
aws sts get-caller-identity
aws rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,MultiAZ:MultiAZ}' --output table
aws backup list-backup-vaults --query 'BackupVaultList[].BackupVaultName' --output table 2>/dev/null || true
aws ec2 describe-availability-zones --query 'AvailabilityZones[].ZoneName' --output text
```

### Step 2 – DR checklist file

```bash
cat > dr-checklist.md << 'EOF'
- Define RTO/RPO before choosing DR pattern
- Test restores — backups that never restore are fiction
- Multi-AZ ≠ Multi-Region
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'serverless-on-aws': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** list Lambda resources; optional tiny function only if role exists

### Step 1 – Serverless inventory

```bash
aws sts get-caller-identity
aws lambda list-functions --query 'Functions[].{Name:FunctionName,Runtime:Runtime}' --output table
aws apigatewayv2 get-apis --query 'Items[].{Name:Name,Id:ApiId}' --output table 2>/dev/null || true
```

### Step 2 – Optional hello Lambda (destroy after)

```bash
ROLE_ARN=$(aws iam get-role --role-name lab-lambda-basic --query Role.Arn --output text 2>/dev/null || true)
if [ -n "${ROLE_ARN:-}" ]; then
  cat > function.py << 'EOF'
def handler(event, context):
    return {"ok": True}
EOF
  zip -q function.zip function.py
  FN="rebash-lab-$(date +%s)"
  aws lambda create-function --function-name "$FN" --runtime python3.12 --role "$ROLE_ARN" --handler function.handler --zip-file fileb://function.zip
  aws lambda invoke --function-name "$FN" out.json && cat out.json && echo
  aws lambda delete-function --function-name "$FN"
  rm -f function.zip function.py out.json
else
  echo "No lab-lambda-basic role — describe-only path is fine"
fi
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'storage-s3-ebs-efs': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** create a uniquely named lab bucket, prove put/get, then delete everything

### Step 1 – S3 lab bucket lifecycle

```bash
aws sts get-caller-identity
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
BUCKET="rebash-lab-${ACCOUNT}-$(date +%s)"
echo "$BUCKET" > bucket-name.txt
REGION=$(aws configure get region || echo eu-west-1)
aws s3 mb "s3://${BUCKET}" --region "$REGION"
echo "hello rebash" > hello.txt
aws s3 cp hello.txt "s3://${BUCKET}/hello.txt"
aws s3 ls "s3://${BUCKET}/"
aws s3 cp "s3://${BUCKET}/hello.txt" hello-down.txt
cat hello-down.txt
```

### Step 2 – Destroy bucket contents and bucket

```bash
BUCKET=$(cat bucket-name.txt)
aws s3 rm "s3://${BUCKET}" --recursive
aws s3 rb "s3://${BUCKET}"
rm -f hello.txt hello-down.txt bucket-name.txt
aws ec2 describe-volumes --query 'Volumes[].{Id:VolumeId,Size:Size,State:State}' --output table | head
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'troubleshooting-aws': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** practise triage: identity → region → API error → CloudTrail

### Step 1 – Triage commands

```bash
aws sts get-caller-identity
echo "region=$(aws configure get region)"
aws ec2 describe-instances --max-items 1 >/tmp/aws-out.json 2>/tmp/aws-err.txt || true
head -n 20 /tmp/aws-err.txt || true
aws cloudtrail lookup-events --max-results 5 --query 'Events[].{Time:EventTime,Name:EventName}' --output table 2>/dev/null || echo "CloudTrail lookup not permitted"
```

### Step 2 – Incident notes template

```bash
cat > triage.md << 'EOF'
1. Who am I (STS ARN)? Which region?
2. Exact error code/message
3. Recent CloudTrail events for that API
4. Blast radius / rollback
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
    'vpc-networking-on-aws': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** describe existing VPCs/subnets/route tables (read-only)

### Step 1 – Network inventory

```bash
aws sts get-caller-identity
aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,Cidr:CidrBlock,Default:IsDefault}' --output table
aws ec2 describe-subnets --query 'Subnets[].{Id:SubnetId,Vpc:VpcId,Az:AvailabilityZone,Cidr:CidrBlock}' --output table
aws ec2 describe-route-tables --query 'RouteTables[0:3].{Id:RouteTableId,Vpc:VpcId}' --output table
```

### Step 2 – Design notes only

```bash
cat > vpc-design.md << 'EOF'
Public subnet: route to IGW
Private subnet: NAT is costly while idle — avoid in labs without destroy plan
Security groups: stateful allow-lists
EOF
```

### Final step – Cleanup note

```bash
# COST WARNING: prefer describe/list APIs. Destroy anything you create.
# Keep ~/rebash-aws/ for later tutorials
```
''',
}

IQ_AWS: dict[str, str] = {
    'aws-fundamentals-and-global-infrastructure': '''1. Region versus Availability Zone versus Local Zone?
2. How do you choose a region for a new workload?
3. What does sts get-caller-identity prove?
4. Why are AZ names account-specific?
5. How does global infrastructure affect DR design?

!!! tip "Sample answer — question 2"
    Confirm identity/region with STS and CLI config first — many “outages” are wrong account/region.

!!! tip "Sample answer — question 4"
    Prefer short-lived credentials (SSO/OIDC). Limit allowed regions via SCP where appropriate.
''',
    'aws-security-services': '''1. CloudTrail versus CloudWatch Logs versus Config?
2. What does GuardDuty detect at a high level?
3. Security Hub’s role in a multi-account org?
4. How do you respond to a public snapshot finding?
5. Why organisation trails matter?

!!! tip "Sample answer — question 2"
    Confirm the service is enabled in the account/region and that you are looking at the right aggregator account.

!!! tip "Sample answer — question 4"
    Centralise trails/findings and restrict who can disable logging.
''',
    'cicd-on-aws': '''1. CodePipeline versus GitHub Actions deploying to AWS?
2. Why OIDC to IAM roles beats AKIA keys in CI?
3. What should a deploy role be allowed to do?
4. How do you promote across accounts?
5. Artifact integrity between stages?

!!! tip "Sample answer — question 2"
    Check the pipeline stage error, the deploy role’s trust policy, and whether the commit SHA matches the artifact.

!!! tip "Sample answer — question 4"
    Scope roles per environment/account and forbid long-lived keys in CI.
''',
    'compute-ec2-asg-and-load-balancing': '''1. ASG desired/min/max — what do they mean?
2. ALB versus NLB versus CLB?
3. Instance unhealthy behind ALB — checks?
4. Implications of stopping versus terminating?
5. How do launch templates improve consistency?

!!! tip "Sample answer — question 2"
    Check instance state, status checks, and load balancer target health before resizing.

!!! tip "Sample answer — question 4"
    Use IMDSv2, least-privilege instance roles, and terminate lab instances promptly.
''',
    'containers-ecs-eks-ecr': '''1. ECR digest pins — why?
2. ECS versus EKS decision factors?
3. How do tasks/pods get AWS permissions?
4. ImagePullBackOff equivalent on ECS?
5. Control plane cost differences?

!!! tip "Sample answer — question 2"
    Verify repository permissions, image URI/digest, and task/execution roles.

!!! tip "Sample answer — question 4"
    Scan images, least-privilege task roles, and delete unused ECR images/repos in labs.
''',
    'cost-optimisation-on-aws': '''1. Top idle resources you hunt weekly?
2. What tags enable showback?
3. Savings Plans versus Reserved Instances — conceptual difference?
4. How do you attribute CI/CD costs?
5. NAT gateway cost control ideas?

!!! tip "Sample answer — question 2"
    Start with Cost Explorer by service, then inventory unattached EIPs, idle LBs, old volumes, and oversized idle EC2.

!!! tip "Sample answer — question 4"
    Enforce tagging, budget alarms, and destroy lab stacks with expiry tags.
''',
    'databases-on-aws': '''1. Multi-AZ RDS versus read replicas?
2. When is DynamoDB a better fit than RDS?
3. What does PITR give you?
4. How do you rotate database secrets?
5. Why is creating RDS in labs risky for cost?

!!! tip "Sample answer — question 2"
    Check instance/cluster status, subnet groups, and security group rules to the DB port.

!!! tip "Sample answer — question 4"
    Encrypt storage, restrict security groups, and delete lab databases the same day.
''',
    'iam-identity-access-and-organizations': '''1. User versus role versus group versus policy?
2. Access denied on a describe call — how do you diagnose?
3. Why are long-lived access keys discouraged?
4. What are SCPs for in AWS Organizations?
5. How does IAM Access Analyzer help?

!!! tip "Sample answer — question 2"
    Decode the ARN from STS, check applicable policies/SCPs, and confirm the action/resource in the error.

!!! tip "Sample answer — question 4"
    Use roles with MFA/SSO, least privilege, and rotate/delete unused keys immediately.
''',
    'infrastructure-as-code-on-aws': '''1. CloudFormation versus Terraform/CDK trade-offs?
2. Why validate templates before create-stack?
3. How do you recover from a ROLLBACK_COMPLETE stack?
4. Change sets — when required?
5. How do you keep credentials out of templates?

!!! tip "Sample answer — question 2"
    Read stack events for the first failing resource. Delete failed lab stacks so names can be reused.

!!! tip "Sample answer — question 4"
    Use roles for deployment and never hardcode secrets in templates.
''',
    'monitoring-and-observability-on-aws': '''1. Metric versus log versus trace?
2. What makes a good CloudWatch alarm?
3. How do you stop alarm fatigue?
4. Log retention versus cost?
5. How do runbooks link to alerts?

!!! tip "Sample answer — question 2"
    Check alarm state history, underlying metric, and related logs for the same time window.

!!! tip "Sample answer — question 4"
    Avoid putting secrets in logs; control who can read log groups.
''',
    'production-aws-landing-zones': '''1. What accounts belong in a security OU?
2. SCP examples that prevent foot-guns?
3. Log archive account purpose?
4. How do you onboard a new workload account?
5. Break-glass access patterns?

!!! tip "Sample answer — question 2"
    Verify org structure, SCP attachments, and that logging accounts actually receive trails/configs.

!!! tip "Sample answer — question 4"
    Separate duties across accounts and keep break-glass credentials offline with dual control.
''',
    'reliability-and-disaster-recovery': '''1. RTO versus RPO?
2. Multi-AZ versus Multi-Region?
3. Why test restores?
4. Pilot light versus warm standby?
5. How do backups interact with ransomware scenarios?

!!! tip "Sample answer — question 2"
    Clarify which failure mode you are designing for. Check Multi-AZ flags and last successful backup/restore test evidence.

!!! tip "Sample answer — question 4"
    Protect backup vaults and practise recovery — permissions included.
''',
    'serverless-on-aws': '''1. Lambda concurrency and timeout pitfalls?
2. API Gateway versus Lambda Function URLs?
3. How do you diagnose a failing Lambda?
4. Cold starts — mitigations?
5. IAM for Lambda least privilege patterns?

!!! tip "Sample answer — question 2"
    Read CloudWatch logs for the function and confirm the role can write logs and reach dependencies.

!!! tip "Sample answer — question 4"
    Least-privilege function roles and delete unused functions after labs.
''',
    'storage-s3-ebs-efs': '''1. S3 consistency model basics you rely on?
2. EBS versus EFS versus S3 for different workloads?
3. How do you prevent accidental public buckets?
4. What is versioning useful for?
5. Unattached EBS volumes — cost impact?

!!! tip "Sample answer — question 2"
    For access issues check bucket policy, Block Public Access, IAM, and the exact object key/region.

!!! tip "Sample answer — question 4"
    Block public access by default, encrypt where required, and delete lab buckets/objects when finished.
''',
    'troubleshooting-aws': '''1. Your standard AWS incident triage order?
2. How does CloudTrail help API failures?
3. Wrong region symptoms?
4. Throttling versus access denied — how to tell?
5. How do you capture evidence for a post-incident review?

!!! tip "Sample answer — question 2"
    STS identity → region → exact error → CloudTrail/event history → blast radius.

!!! tip "Sample answer — question 4"
    Limit who can disable logging during incidents; use temporary elevated roles with expiry.
''',
    'vpc-networking-on-aws': '''1. Public versus private subnet routing?
2. Security group versus NACL?
3. Why are NAT gateways a cost surprise?
4. How do you troubleshoot no route to host for EC2?
5. VPC endpoints — when do they help?

!!! tip "Sample answer — question 2"
    Trace route tables, subnet association, security groups, and NACLs in that order.

!!! tip "Sample answer — question 4"
    Avoid 0.0.0.0/0 SSH from the world. Prefer SSM Session Manager.
''',
}



def supported_techs() -> set[str]:
    """Return technology keys supported by this bank module."""
    return {"gitlab", "github-actions", "git", "docker", "aws"}


def lab_for(tech: str, slug: str, title: str, lab_dir: str) -> str | None:
    """Return a Hands-on Lab markdown body for ``tech``/``slug``, or None."""
    banks_map = {
        "gitlab": LABS_GITLAB,
        "github-actions": LABS_GHA,
        "git": LABS_GIT,
        "docker": LABS_DOCKER,
        "aws": LABS_AWS,
    }
    body = banks_map.get(tech, {}).get(slug)
    if body is None:
        return None
    _ = title  # reserved for future title-aware labs
    return body.replace("{lab_dir}", lab_dir)


def interview_for(tech: str, slug: str, title: str) -> str | None:
    """Return Interview Questions markdown body for ``tech``/``slug``, or None."""
    banks_map = {
        "gitlab": IQ_GITLAB,
        "github-actions": IQ_GHA,
        "git": IQ_GIT,
        "docker": IQ_DOCKER,
        "aws": IQ_AWS,
    }
    _ = title  # reserved for future title-aware questions
    return banks_map.get(tech, {}).get(slug)
