"""GitLab, GitHub Actions, Git, Docker, and AWS lab + interview banks."""

from __future__ import annotations

from .formatters import bash, interview_body, lab_body


def supported_techs() -> set[str]:
    return {"gitlab", "github-actions", "git", "docker", "aws"}


def _iq(qs: list[str], t2: str, t4: str) -> str:
    return interview_body(qs, {2: t2, 4: t4})


def _raw(block: str) -> str:
    """Protect GitHub Actions expressions from mkdocs-macros."""
    return "{% raw %}\n" + block.strip() + "\n{% endraw %}\n"


# --- GitLab --------------------------------------------------------------------

def _gitlab_lab(slug: str, title: str, lab_dir: str) -> str:
    fundamentals = lab_body(
        lab_dir,
        "author a valid .gitlab-ci.yml and validate stages locally",
        [
            (
                "Pipeline skeleton",
                bash(
                    """mkdir -p src
echo 'print("ok")' > src/hello.py
cat > .gitlab-ci.yml << 'EOF'
stages: [lint, test]

lint:
  stage: lint
  image: python:3.12-alpine
  script:
    - python -m py_compile src/hello.py

test:
  stage: test
  image: python:3.12-alpine
  script:
    - python src/hello.py
EOF
python3 - <<'PY'
import yaml,sys
with open('.gitlab-ci.yml') as f:
    data=yaml.safe_load(f)
assert 'stages' in data and 'lint' in data
print('gitlab-ci.yml parsed OK; stages=', data['stages'])
PY
tee NOTES.txt << 'EOF'
Push to GitLab to run on a shared/runner. Use CI Lint in the UI for deeper validation.
EOF"""
                ),
            ),
        ],
        "# Keep the YAML; no cloud resources created",
    )

    syntax = lab_body(
        lab_dir,
        "practise rules, needs, and artefacts in .gitlab-ci.yml",
        [
            (
                "DAG-friendly pipeline",
                bash(
                    """cat > .gitlab-ci.yml << 'EOF'
stages: [build, test]

build:
  stage: build
  script:
    - mkdir -p dist && echo artefact > dist/app.txt
  artifacts:
    paths: [dist/]
    expire_in: 1 hour

test:
  stage: test
  needs: [build]
  script:
    - test -f dist/app.txt && cat dist/app.txt
EOF
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); print('OK')"
grep -n 'needs:\\|artifacts:' .gitlab-ci.yml"""
                ),
            ),
        ],
        "# File-only lab",
    )

    docker_ci = lab_body(
        lab_dir,
        "build a Dockerfile and a GitLab job that would build the image",
        [
            (
                "Dockerfile + CI job",
                bash(
                    """cat > Dockerfile << 'EOF'
FROM alpine:3.20
WORKDIR /app
COPY hello.txt .
CMD ["cat", "hello.txt"]
EOF
echo 'hello from gitlab ci' > hello.txt
docker build -t rebash-gitlab-lab:local .
docker run --rm rebash-gitlab-lab:local
cat > .gitlab-ci.yml << 'EOF'
build-image:
  image: docker:27
  services: [docker:27-dind]
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
EOF
echo 'CI job documented; local image build verified.'"""
                ),
            ),
        ],
        "docker rmi rebash-gitlab-lab:local 2>/dev/null || true",
    )

    vars_oidc = lab_body(
        lab_dir,
        "model CI variables and OIDC notes without storing secrets",
        [
            (
                "Variables map",
                bash(
                    """cat > .gitlab-ci.yml << 'EOF'
deploy:
  image: alpine:3.20
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://sts.amazonaws.com
  script:
    - echo "Exchange GITLAB_OIDC_TOKEN for cloud role — do not print the token"
    - test -n "$RUNTIME_ENV"
  variables:
    RUNTIME_ENV: lab
EOF
tee oidc-notes.txt << 'EOF'
Prefer OIDC/id_tokens over long-lived cloud keys in GitLab CI/CD variables.
Mask + protect secrets; scope to environments.
EOF
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); print('OK')"
cat oidc-notes.txt"""
                ),
            ),
        ],
        "# No secrets created",
    )

    runners = lab_body(
        lab_dir,
        "document runner/executor choices and a tags-based job",
        [
            (
                "Runner tags",
                bash(
                    """cat > .gitlab-ci.yml << 'EOF'
build:
  tags: [docker, linux]
  image: alpine:3.20
  script:
    - uname -a
    - echo "Job expects a runner with tags docker+linux"
EOF
tee runner-notes.txt << 'EOF'
Shell vs Docker vs Kubernetes executors trade isolation, speed, and ops cost.
Register runners with least privilege and ephemeral environments where possible.
EOF
cat runner-notes.txt"""
                ),
            ),
        ],
        "# File-only",
    )

    security = lab_body(
        lab_dir,
        "add a SAST/secret-scan shaped job and a local secret grep gate",
        [
            (
                "Security jobs",
                bash(
                    """echo 'password = "not-a-real-secret"' > bad.env.example
cat > .gitlab-ci.yml << 'EOF'
stages: [secure, test]
secret_hygiene:
  stage: secure
  image: alpine:3.20
  script:
    - !reference [.never_commit]
.never_commit:
  script:
    - echo "Use GitLab Secret Detection / SAST templates in real projects"

unit:
  stage: test
  image: alpine:3.20
  script: ["echo ok"]
EOF
# Local gate:
if grep -RniE 'api[_-]?key|secret|password\\s*=' --exclude='*.example' . 2>/dev/null | grep -v bad.env.example; then
  echo 'Found suspicious strings'
else
  echo 'Hygiene check passed for tracked lab files'
fi
ls -la"""
                ),
            ),
        ],
        "rm -f bad.env.example",
    )

    k8s = lab_body(
        lab_dir,
        "produce manifests + a GitLab deploy job outline for the agent",
        [
            (
                "Manifests and deploy job",
                bash(
                    """mkdir -p k8s
cat > k8s/deploy.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo
  namespace: rebash-lab
spec:
  replicas: 1
  selector:
    matchLabels: { app: demo }
  template:
    metadata:
      labels: { app: demo }
    spec:
      containers:
        - name: nginx
          image: nginx:1.27-alpine
EOF
cat > .gitlab-ci.yml << 'EOF'
deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl apply -f k8s/deploy.yaml
  environment:
    name: lab
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
EOF
kubectl apply --dry-run=client -f k8s/deploy.yaml | tee dryrun.txt || echo 'Install kubectl to dry-run; YAML written'"""
                ),
            ),
        ],
        "# No cluster changes required for dry-run-only",
    )

    tf_pipe = lab_body(
        lab_dir,
        "GitLab Terraform plan job with local Terraform validation",
        [
            (
                "Plan job + local terraform",
                bash(
                    """mkdir -p infra
cat > infra/main.tf << 'EOF'
terraform {
  required_providers {
    null = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
resource "null_resource" "x" {}
EOF
cat > .gitlab-ci.yml << 'EOF'
plan:
  image: hashicorp/terraform:1.7
  script:
    - cd infra
    - terraform init -input=false
    - terraform plan -input=false -out=tfplan
  artifacts:
    paths: [infra/tfplan]
EOF
cd infra && terraform init -backend=false && terraform validate && cd ..
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); print('CI OK')" """
                ),
            ),
        ],
        "rm -rf infra/.terraform",
    )

    artifacts = lab_body(
        lab_dir,
        "define artefacts/caches and simulate an artefact consumer locally",
        [
            (
                "Artefacts pipeline",
                bash(
                    """cat > .gitlab-ci.yml << 'EOF'
stages: [build, use]
build:
  stage: build
  script:
    - mkdir -p dist && echo v1 > dist/app.txt
  artifacts:
    paths: [dist/]
  cache:
    key: lib
    paths: [.cache/]
use:
  stage: use
  needs: [build]
  script:
    - cat dist/app.txt
EOF
mkdir -p dist .cache && echo v1 > dist/app.txt
cat dist/app.txt
python3 -c "import yaml; print(yaml.safe_load(open('.gitlab-ci.yml'))['build']['artifacts'])" """
                ),
            ),
        ],
        "rm -rf dist .cache",
    )

    testing = lab_body(
        lab_dir,
        "JUnit-style report job and a local pytest/compile gate",
        [
            (
                "Quality gate",
                bash(
                    """mkdir -p tests
echo 'def test_ok(): assert True' > tests/test_ok.py
cat > .gitlab-ci.yml << 'EOF'
test:
  image: python:3.12-alpine
  script:
    - pip install pytest
    - pytest --junitxml=report.xml
  artifacts:
    when: always
    reports:
      junit: report.xml
EOF
python3 -m pip install -q pytest && python3 -m pytest tests --junitxml=report.xml
head -n 20 report.xml
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); print('OK')" """
                ),
            ),
        ],
        "rm -f report.xml",
    )

    release = lab_body(
        lab_dir,
        "model release/version jobs with a changelog stub",
        [
            (
                "Release metadata",
                bash(
                    """echo '# Changelog\n\n## 0.1.0\n- Lab release' > CHANGELOG.md
cat > .gitlab-ci.yml << 'EOF'
release:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/release-cli:latest
  script:
    - echo "Create GitLab Release for $CI_COMMIT_TAG"
  rules:
    - if: $CI_COMMIT_TAG
EOF
cat CHANGELOG.md
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); print('OK')" """
                ),
            ),
        ],
        "# File-only",
    )

    production = lab_body(
        lab_dir,
        "environments, manual gates, and protected-branch style rules",
        [
            (
                "Prod gate pipeline",
                bash(
                    """cat > .gitlab-ci.yml << 'EOF'
stages: [deploy]
deploy_lab:
  stage: deploy
  script: ["echo deploy lab"]
  environment: lab
deploy_prod:
  stage: deploy
  script: ["echo deploy prod"]
  environment:
    name: production
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
EOF
python3 -c "import yaml; d=yaml.safe_load(open('.gitlab-ci.yml')); assert d['deploy_prod']['when']=='manual'; print('manual prod gate OK')" """
                ),
            ),
        ],
        "# File-only",
    )

    monitor = lab_body(
        lab_dir,
        "add a pipeline metrics/notes job and local timing evidence",
        [
            (
                "Observability notes",
                bash(
                    """cat > .gitlab-ci.yml << 'EOF'
observe:
  image: alpine:3.20
  script:
    - echo "Emit job duration/metrics to your observability backend"
    - date -u +%Y-%m-%dT%H:%M:%SZ | tee job-start.txt
EOF
date -u +%Y-%m-%dT%H:%M:%SZ | tee job-start.txt
tee monitor-notes.txt << 'EOF'
Track fail rates, queue time, and flaky jobs. Alert on sustained pipeline red rates.
EOF
cat monitor-notes.txt"""
                ),
            ),
        ],
        "# File-only",
    )

    enterprise = lab_body(
        lab_dir,
        "document group/project compliance controls for enterprise GitLab",
        [
            (
                "Enterprise checklist",
                bash(
                    """tee enterprise-checklist.txt << 'EOF'
- SSO/SAML + SCIM for identity
- Protected branches + required approvals
- Push rules / file denylist for secrets
- Separate runners for untrusted vs prod
- Audit events exported to SIEM
EOF
cat > .gitlab-ci.yml << 'EOF'
compliance_echo:
  script:
    - echo "Enterprise policies enforced outside YAML too"
EOF
cat enterprise-checklist.txt"""
                ),
            ),
        ],
        "# File-only",
    )

    projects = lab_body(
        lab_dir,
        "simulate MR-oriented pipeline rules",
        [
            (
                "MR rules",
                bash(
                    """cat > .gitlab-ci.yml << 'EOF'
test:
  script: ["echo unit tests"]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"
EOF
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); print('MR rules parsed')" """
                ),
            ),
        ],
        "# File-only",
    )

    multi = lab_body(
        lab_dir,
        "matrix-like parallel deploy stubs for two clouds",
        [
            (
                "Multi-cloud jobs",
                bash(
                    """cat > .gitlab-ci.yml << 'EOF'
.deploy:
  image: alpine:3.20
  script:
    - echo "Deploy to $CLOUD using OIDC — no static keys"

deploy_aws:
  extends: .deploy
  variables: { CLOUD: aws }
deploy_gcp:
  extends: .deploy
  variables: { CLOUD: gcp }
EOF
python3 -c "import yaml; d=yaml.safe_load(open('.gitlab-ci.yml')); print(sorted(k for k in d if k.startswith('deploy')))" """
                ),
            ),
        ],
        "# File-only",
    )

    design = lab_body(
        lab_dir,
        "includes and parent/child pipeline layout",
        [
            (
                "Includes",
                bash(
                    """mkdir -p ci
cat > ci/lint.yml << 'EOF'
lint:
  script: ["echo lint"]
EOF
cat > .gitlab-ci.yml << 'EOF'
include:
  - local: ci/lint.yml
stages: [lint, test]
test:
  stage: test
  script: ["echo test"]
EOF
python3 -c "import yaml; print(yaml.safe_load(open('.gitlab-ci.yml'))['include'])" """
                ),
            ),
        ],
        "# File-only",
    )

    troubleshoot = lab_body(
        lab_dir,
        "break YAML syntax and practise CI lint recovery",
        [
            (
                "Broken then fixed",
                bash(
                    """cat > .gitlab-ci.yml << 'EOF'
test
  script: ["echo broken"]
EOF
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))" 2>&1 | tee err.txt || true
cat > .gitlab-ci.yml << 'EOF'
test:
  script: ["echo fixed"]
EOF
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); print('fixed OK')" """
                ),
            ),
        ],
        "# File-only",
    )

    mapping = [
        ("pipeline-syntax", syntax),
        ("gitlab-ci-fundamentals", fundamentals),
        ("building-docker", docker_ci),
        ("variables-secrets", vars_oidc),
        ("oidc", vars_oidc),
        ("runners", runners),
        ("security", security),
        ("devsecops", security),
        ("kubernetes", k8s),
        ("terraform", tf_pipe),
        ("artifacts", artifacts),
        ("caches", artifacts),
        ("testing", testing),
        ("quality", testing),
        ("release", release),
        ("versioning", release),
        ("production", production),
        ("environments", production),
        ("monitoring", monitor),
        ("observability", monitor),
        ("enterprise", enterprise),
        ("projects-mrs", projects),
        ("multi-cloud", multi),
        ("pipeline-design", design),
        ("includes", design),
        ("troubleshoot", troubleshoot),
    ]
    for key, content in mapping:
        if key in slug:
            return content
    return fundamentals


def _gitlab_iq(slug: str, title: str) -> str:
    return _iq(
        [
            f"How does **{title}** show up in a real GitLab delivery workflow?",
            "A pipeline is stuck / red — what do you check first?",
            "How do `needs`, stages, and artefacts interact?",
            "How should secrets and cloud credentials be handled in GitLab CI?",
            "How would you keep merge-request pipelines fast but still safe?",
        ],
        "Open the failing job log, confirm runner tags/executor, then validate `.gitlab-ci.yml` with CI Lint. Check rules that skipped jobs and artefact dependencies.",
        "Prefer masked/protected variables and OIDC (`id_tokens`) over long-lived keys. Limit who can run protected-branch pipelines.",
    )


# --- GitHub Actions ------------------------------------------------------------

def _gha_lab(slug: str, title: str, lab_dir: str) -> str:
    basics = lab_body(
        lab_dir,
        "author a workflow with jobs/steps and validate YAML structure",
        [
            (
                "First workflow",
                _raw(
                    """```bash
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
name: ci
on:
  push:
  pull_request:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Compile check
        run: |
          echo ok > out.txt
          test -s out.txt
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml')); print('workflow OK')"
```"""
                ),
            ),
        ],
        "# File-only; push to GitHub to execute on hosted runners",
    )

    matrix = lab_body(
        lab_dir,
        "build a matrix workflow and reusable workflow stub",
        [
            (
                "Matrix + reusable",
                _raw(
                    """```bash
mkdir -p .github/workflows
cat > .github/workflows/matrix.yml << 'EOF'
name: matrix
on: workflow_dispatch
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - run: echo "python ${{ matrix.python }}"
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/matrix.yml')); print('matrix OK')"
```"""
                ),
            ),
        ],
        "# File-only",
    )

    docker = lab_body(
        lab_dir,
        "Dockerfile + Actions job that builds locally first",
        [
            (
                "Local build + workflow",
                _raw(
                    """```bash
cat > Dockerfile << 'EOF'
FROM alpine:3.20
COPY hi.txt /hi.txt
CMD ["cat","/hi.txt"]
EOF
echo hi > hi.txt
docker build -t rebash-gha-lab:local .
docker run --rm rebash-gha-lab:local
mkdir -p .github/workflows
cat > .github/workflows/docker.yml << 'EOF'
name: docker
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t demo:${{ github.sha }} .
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/docker.yml')); print('OK')"
```"""
                ),
            ),
        ],
        "docker rmi rebash-gha-lab:local 2>/dev/null || true",
    )

    oidc = lab_body(
        lab_dir,
        "OIDC permissions workflow without embedding cloud keys",
        [
            (
                "OIDC workflow",
                _raw(
                    """```bash
mkdir -p .github/workflows
cat > .github/workflows/oidc.yml << 'EOF'
name: oidc-deploy
on:
  workflow_dispatch:
permissions:
  id-token: write
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Configure cloud creds via OIDC
        run: echo "Use cloud-specific OIDC action; never echo secrets"
EOF
tee oidc-notes.txt << 'EOF'
permissions.id-token: write is required for OIDC. Bind GitHub subject claims to a least-privilege cloud role.
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/oidc.yml')); print('OK')"
cat oidc-notes.txt
```"""
                ),
            ),
        ],
        "# No cloud resources",
    )

    artifacts = lab_body(
        lab_dir,
        "upload/download artefacts and cache pattern in workflow YAML",
        [
            (
                "Artefacts workflow",
                _raw(
                    """```bash
mkdir -p .github/workflows dist
echo build > dist/app.txt
cat > .github/workflows/artifacts.yml << 'EOF'
name: artifacts
on: workflow_dispatch
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: mkdir -p dist && echo build > dist/app.txt
      - uses: actions/upload-artifact@v4
        with:
          name: app
          path: dist/
  use:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: app
          path: dist
      - run: cat dist/app.txt
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/artifacts.yml')); print('OK')"
```"""
                ),
            ),
        ],
        "rm -rf dist",
    )

    composite = lab_body(
        lab_dir,
        "write a composite action and call it from a workflow",
        [
            (
                "Composite action",
                _raw(
                    """```bash
mkdir -p .github/actions/hello .github/workflows
cat > .github/actions/hello/action.yml << 'EOF'
name: hello
description: composite hello
runs:
  using: composite
  steps:
    - run: echo "hello from composite"
      shell: bash
EOF
cat > .github/workflows/use-composite.yml << 'EOF'
name: use-composite
on: workflow_dispatch
jobs:
  call:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/hello
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/actions/hello/action.yml')); print('action OK')"
```"""
                ),
            ),
        ],
        "# File-only",
    )

    runners = lab_body(
        lab_dir,
        "contrast hosted vs self-hosted with labels in a workflow",
        [
            (
                "Runner labels",
                _raw(
                    """```bash
mkdir -p .github/workflows
cat > .github/workflows/runners.yml << 'EOF'
name: runners
on: workflow_dispatch
jobs:
  hosted:
    runs-on: ubuntu-latest
    steps:
      - run: uname -a
  # self_hosted:
  #   runs-on: [self-hosted, linux, x64]
  #   steps:
  #     - run: uname -a
EOF
tee runner-notes.txt << 'EOF'
Self-hosted runners need patching, isolation, and untrusted-PR hardening.
Prefer GitHub-hosted for open-source and simple CI; self-hosted for special hardware/network.
EOF
cat runner-notes.txt
```"""
                ),
            ),
        ],
        "# File-only",
    )

    security = lab_body(
        lab_dir,
        "pin actions and add a checkout-safe pull_request workflow",
        [
            (
                "Supply-chain hygiene",
                _raw(
                    """```bash
mkdir -p .github/workflows
cat > .github/workflows/secure.yml << 'EOF'
name: secure
on:
  pull_request:
permissions:
  contents: read
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Guard
        run: echo "Pin actions; least privileges; no secrets on fork PRs"
EOF
tee supply-chain.txt << 'EOF'
Pin actions by SHA for high assurance. Limit permissions: {}. Use environments for prod secrets.
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/secure.yml')); print('OK')"
```"""
                ),
            ),
        ],
        "# File-only",
    )

    terraform = lab_body(
        lab_dir,
        "Terraform plan workflow + local validate",
        [
            (
                "TF plan workflow",
                _raw(
                    """```bash
mkdir -p infra .github/workflows
cat > infra/main.tf << 'EOF'
terraform {
  required_providers {
    null = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
resource "null_resource" "x" {}
EOF
cat > .github/workflows/terraform.yml << 'EOF'
name: terraform
on: pull_request
jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: |
          cd infra
          terraform init -input=false
          terraform plan -input=false
EOF
cd infra && terraform init -backend=false && terraform validate && cd ..
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/terraform.yml')); print('OK')"
```"""
                ),
            ),
        ],
        "rm -rf infra/.terraform",
    )

    k8s = lab_body(
        lab_dir,
        "kubectl apply dry-run with a deploy workflow stub",
        [
            (
                "Manifest + workflow",
                _raw(
                    """```bash
mkdir -p k8s .github/workflows
cat > k8s/deploy.yaml << 'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: demo
  namespace: default
data:
  ok: "yes"
EOF
kubectl apply --dry-run=client -f k8s/deploy.yaml | tee dryrun.txt || true
cat > .github/workflows/k8s.yml << 'EOF'
name: k8s
on: workflow_dispatch
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: kubectl apply -f k8s/deploy.yaml
EOF
```"""
                ),
            ),
        ],
        "# No live cluster required for dry-run",
    )

    testing = lab_body(
        lab_dir,
        "test job with pytest locally and matching workflow",
        [
            (
                "Tests",
                _raw(
                    """```bash
mkdir -p tests .github/workflows
echo 'def test_ok(): assert 1==1' > tests/test_ok.py
python3 -m pip install -q pytest && python3 -m pytest tests
cat > .github/workflows/test.yml << 'EOF'
name: test
on: [push, pull_request]
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pytest && pytest
EOF
```"""
                ),
            ),
        ],
        "# File-only",
    )

    release = lab_body(
        lab_dir,
        "tag-driven release workflow stub",
        [
            (
                "Release workflow",
                _raw(
                    """```bash
mkdir -p .github/workflows
echo '0.1.0' > VERSION
cat > .github/workflows/release.yml << 'EOF'
name: release
on:
  push:
    tags: ["v*"]
jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - run: echo "Build and publish artefacts for ${{ github.ref_name }}"
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/release.yml')); print('OK')"
```"""
                ),
            ),
        ],
        "# File-only",
    )

    production = lab_body(
        lab_dir,
        "environment protection pattern in workflow YAML",
        [
            (
                "Environments",
                _raw(
                    """```bash
mkdir -p .github/workflows
cat > .github/workflows/prod.yml << 'EOF'
name: prod
on:
  workflow_dispatch:
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - run: echo "Requires environment approvals/secrets in GitHub settings"
EOF
tee env-notes.txt << 'EOF'
Use GitHub Environments for required reviewers, wait timers, and scoped secrets.
EOF
cat env-notes.txt
```"""
                ),
            ),
        ],
        "# File-only",
    )

    multi = lab_body(
        lab_dir,
        "parallel cloud deploy jobs with OIDC permissions",
        [
            (
                "Multi-cloud stub",
                _raw(
                    """```bash
mkdir -p .github/workflows
cat > .github/workflows/multi.yml << 'EOF'
name: multi
on: workflow_dispatch
permissions:
  id-token: write
  contents: read
jobs:
  aws:
    runs-on: ubuntu-latest
    steps:
      - run: echo "AWS OIDC deploy"
  azure:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Azure OIDC deploy"
EOF
python3 -c "import yaml; print(list(yaml.safe_load(open('.github/workflows/multi.yml'))['jobs']))"
```"""
                ),
            ),
        ],
        "# File-only",
    )

    cicd = lab_body(
        lab_dir,
        "end-to-end CI workflow: checkout, test, artefact",
        [
            (
                "CI path",
                _raw(
                    """```bash
mkdir -p .github/workflows src
echo 'print("ci")' > src/app.py
cat > .github/workflows/cicd.yml << 'EOF'
name: cicd
on: [push, pull_request]
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python src/app.py
EOF
python src/app.py
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/cicd.yml')); print('OK')"
```"""
                ),
            ),
        ],
        "# File-only",
    )

    troubleshoot = lab_body(
        lab_dir,
        "introduce a failing step locally and fix the workflow",
        [
            (
                "Fail then fix",
                _raw(
                    """```bash
mkdir -p .github/workflows
cat > .github/workflows/bad.yml << 'EOF'
name: bad
on: workflow_dispatch
jobs:
  j:
    runs-on: ubuntu-latest
    steps:
      - run: exit 1
EOF
# Local analogue of a failing step:
(false) 2>&1 | tee fail.txt || true
cat > .github/workflows/bad.yml << 'EOF'
name: bad
on: workflow_dispatch
jobs:
  j:
    runs-on: ubuntu-latest
    steps:
      - run: echo fixed && exit 0
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/bad.yml')); print('fixed')"
```"""
                ),
            ),
        ],
        "# File-only",
    )

    mapping = [
        ("workflow-syntax", matrix),
        ("matrix", matrix),
        ("reusable", matrix),
        ("basics", basics),
        ("workflows-jobs", basics),
        ("docker", docker),
        ("secrets", oidc),
        ("oidc", oidc),
        ("artifacts", artifacts),
        ("caching", artifacts),
        ("composite", composite),
        ("runners", runners),
        ("security", security),
        ("supply-chain", security),
        ("terraform", terraform),
        ("kubernetes", k8s),
        ("testing", testing),
        ("release", release),
        ("production", production),
        ("multi-cloud", multi),
        ("cicd-fundamentals", cicd),
        ("troubleshoot", troubleshoot),
    ]
    for key, content in mapping:
        if key in slug:
            return content
    return basics


def _gha_iq(slug: str, title: str) -> str:
    return _iq(
        [
            f"How does **{title}** fit into a GitHub Actions delivery model?",
            "A workflow fails only on `pull_request` — what differences do you inspect?",
            "Why pin Actions and limit `permissions`?",
            "How should production secrets and OIDC cloud access be designed?",
            "How do you keep workflows reusable without copy-paste sprawl?",
        ],
        "Compare event payloads, checkout ref for fork PRs, secrets availability, and required environments. Read the failing step log and re-run with debug logging if needed.",
        "Use `permissions` least privilege, environment protection for prod, and OIDC (`id-token: write`) instead of long-lived cloud keys.",
    )


# --- Git -----------------------------------------------------------------------

def _git_lab(slug: str, title: str, lab_dir: str) -> str:
    def repo_init_steps(extra: list[tuple[str, str]] | None = None) -> str:
        steps = [
            (
                "Init repository",
                bash(
                    """git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
echo '# lab' > README.md
git add README.md
git commit -m 'Initial commit'
git log --oneline"""
                ),
            ),
        ]
        if extra:
            steps.extend(extra)
        return lab_body(
            lab_dir,
            f"practise Git skills for: {title}",
            steps,
            "# Safe local repo under the lab directory; delete the folder when finished",
        )

    branching = repo_init_steps(
        [
            (
                "Branch and merge",
                bash(
                    """git switch -c feature/note
echo 'feature' > note.txt
git add note.txt
git commit -m 'Add note'
git switch main
git merge feature/note
git log --oneline --graph --all | tee log.txt"""
                ),
            ),
        ]
    )

    rebase = repo_init_steps(
        [
            (
                "Rebase practice",
                bash(
                    """git switch -c feature/rebase
echo a > a.txt && git add a.txt && git commit -m 'a'
git switch main
echo m > m.txt && git add m.txt && git commit -m 'm'
git switch feature/rebase
git rebase main
git log --oneline --graph --all | tee rebase.txt"""
                ),
            ),
        ]
    )

    undo = repo_init_steps(
        [
            (
                "Reset / stash / revert",
                bash(
                    """echo dirty > wip.txt
git stash push -m 'wip' -- wip.txt
git stash list
echo bad > bad.txt && git add bad.txt && git commit -m 'bad'
git revert --no-edit HEAD
git log --oneline | tee undo.txt"""
                ),
            ),
        ]
    )

    reflog = repo_init_steps(
        [
            (
                "Reflog recovery",
                bash(
                    """echo x > x.txt && git add x.txt && git commit -m 'x'
git reset --hard HEAD~1
git reflog | tee reflog.txt
git checkout -b recovered HEAD@{1}
git log --oneline | tee recovered.txt"""
                ),
            ),
        ]
    )

    bisect = repo_init_steps(
        [
            (
                "Bisect demo",
                bash(
                    """for i in 1 2 3 4 5; do echo $i > n.txt; git add n.txt; git commit -m "n$i"; done
echo 'broken' > n.txt; git add n.txt; git commit -m 'broken'
git bisect start
git bisect bad
git bisect good HEAD~5
git bisect run sh -c 'grep -q broken n.txt && exit 1 || exit 0' || true
git bisect reset
git log --oneline | head"""
                ),
            ),
        ]
    )

    hooks = repo_init_steps(
        [
            (
                "Client hook",
                bash(
                    """mkdir -p .git/hooks
cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
! grep -RniE 'AKIA[0-9A-Z]{16}' --exclude-dir=.git . || { echo 'Blocked potential AWS key'; exit 1; }
EOF
chmod +x .git/hooks/pre-commit
echo 'safe' > ok.txt && git add ok.txt && git commit -m 'hook ok'
echo 'Hook installed for this lab repo only.'"""
                ),
            ),
        ]
    )

    ignore = repo_init_steps(
        [
            (
                "gitignore",
                bash(
                    """cat > .gitignore << 'EOF'
*.env
__pycache__/
.DS_Store
EOF
echo SECRET=1 > local.env
git status --ignored | tee status.txt
git check-ignore -v local.env"""
                ),
            ),
        ]
    )

    objects = repo_init_steps(
        [
            (
                "Inspect objects",
                bash(
                    """echo 'payload' > blob.txt
git add blob.txt
git commit -m 'blob'
git rev-parse HEAD
git cat-file -t HEAD
git cat-file -p HEAD | tee commit-obj.txt
git rev-list --objects --all | head"""
                ),
            ),
        ]
    )

    remotes = repo_init_steps(
        [
            (
                "Remote simulation",
                bash(
                    """mkdir -p /tmp/rebash-git-remote.git
git init --bare /tmp/rebash-git-remote.git
git remote add origin /tmp/rebash-git-remote.git
git push -u origin main
git remote -v
git ls-remote origin"""
                ),
            ),
        ]
    )

    signing = repo_init_steps(
        [
            (
                "Signing readiness",
                bash(
                    """git config --get user.name
git config --get user.email
tee signing-notes.txt << 'EOF'
Production: enable commit signing (GPG/SSH) and require signed commits on protected branches.
Lab: confirm identity config is correct before enabling signing keys.
EOF
git log -1 --pretty=fuller | tee last.txt
cat signing-notes.txt"""
                ),
            ),
        ]
    )

    history = repo_init_steps(
        [
            (
                "History and diffs",
                bash(
                    """echo v1 > file.txt && git add file.txt && git commit -m 'v1'
echo v2 > file.txt && git commit -am 'v2'
git log --oneline --decorate | tee hist.txt
git show HEAD | tee show.txt
git diff HEAD~1 HEAD | tee diff.txt"""
                ),
            ),
        ]
    )

    conflicts = repo_init_steps(
        [
            (
                "Merge conflict",
                bash(
                    """echo base > conflict.txt
git add conflict.txt && git commit -m 'base'
git switch -c left
echo left > conflict.txt && git commit -am 'left'
git switch main
git switch -c right
echo right > conflict.txt && git commit -am 'right'
git switch main
git merge left
git merge right || true
tee conflict.txt << 'EOF'
resolved
EOF
git add conflict.txt
git commit -m 'resolve conflict'
git log --oneline --graph --all | tee merge.txt"""
                ),
            ),
        ]
    )

    basic = repo_init_steps(
        [
            (
                "Add commit cycle",
                bash(
                    """echo 'hello' > app.txt
git status
git add app.txt
git commit -m 'Add app.txt'
git status
git log -1 --stat"""
                ),
            ),
        ]
    )

    clone = lab_body(
        lab_dir,
        "create a bare remote and clone it",
        [
            (
                "Clone workflow",
                bash(
                    """git init -b main seed && cd seed
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
echo '# seed' > README.md
git add README.md && git commit -m 'seed'
cd ..
git clone --bare seed remote.git
git clone remote.git workspace
cd workspace && git log --oneline && pwd"""
                ),
            ),
        ],
        "rm -rf seed remote.git workspace",
    )

    install = lab_body(
        lab_dir,
        "verify Git install and set safe lab identity",
        [
            (
                "Config",
                bash(
                    """git --version | tee version.txt
git config --global --get user.name || true
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
git config --list --local | egrep 'user.|init.defaultBranch' | tee local-config.txt"""
                ),
            ),
        ],
        "# Local config only inside lab repo",
    )

    intro = basic

    pr = repo_init_steps(
        [
            (
                "Review-ready branch",
                bash(
                    """git switch -c pr/demo
echo 'change' > feature.txt
git add feature.txt
git commit -m 'feat: demo change'
git log main..HEAD --oneline
tee REVIEW.txt << 'EOF'
Open a pull/merge request with a clear summary, test plan, and small diff.
EOF
cat REVIEW.txt"""
                ),
            ),
        ]
    )

    gitops = repo_init_steps(
        [
            (
                "Desired-state folder",
                bash(
                    """mkdir -p desired/app
cat > desired/app/deploy.yaml << 'EOF'
apiVersion: v1
kind: ConfigMap
metadata: { name: demo }
data: { ok: "yes" }
EOF
git add desired && git commit -m 'Add desired state'
git ls-tree -r HEAD --name-only | tee tree.txt"""
                ),
            ),
        ]
    )

    iac = repo_init_steps(
        [
            (
                "IaC repo hygiene",
                bash(
                    """mkdir -p infra
echo 'resource "null_resource" "x" {}' > infra/main.tf
cat > .gitignore << 'EOF'
.terraform/
*.tfstate*
.terraform.lock.hcl
EOF
git add infra .gitignore
git commit -m 'Add infra scaffold'
git status --ignored | tee ignored.txt"""
                ),
            ),
        ]
    )

    cicd_git = repo_init_steps(
        [
            (
                "CI trigger layout",
                bash(
                    """mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
name: ci
on: [push, pull_request]
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - run: echo ok
EOF
git add .github && git commit -m 'Add CI workflow stub'
git log --oneline | tee commits.txt"""
                ),
            ),
        ]
    )

    submodules = repo_init_steps(
        [
            (
                "Subtree alternative demo",
                bash(
                    """mkdir -p vendor/lib
echo 'lib' > vendor/lib/README.md
git add vendor && git commit -m 'Vendor lib (subtree-style folder)'
tee submodule-notes.txt << 'EOF'
Submodules pin external Git SHAs; subtrees vendor history. Prefer package managers when possible.
EOF
cat submodule-notes.txt"""
                ),
            ),
        ]
    )

    production = repo_init_steps(
        [
            (
                "Protected-branch habits",
                bash(
                    """tee production-git.txt << 'EOF'
- trunk-based or short-lived branches
- required reviews + CI
- signed commits where mandated
- no force-push to main
EOF
git switch -c hotfix/typo
echo 'fix' >> README.md
git commit -am 'fix: typo'
git switch main
git merge hotfix/typo
cat production-git.txt"""
                ),
            ),
        ]
    )

    github_fund = repo_init_steps(
        [
            (
                "GitHub collaboration notes",
                bash(
                    """tee github-notes.txt << 'EOF'
Issues + PRs + Actions form the collaboration loop.
Protect default branch; use CODEOWNERS for critical paths.
EOF
mkdir -p .github
echo '* @platform-team' > .github/CODEOWNERS
git add .github github-notes.txt
git commit -m 'Add CODEOWNERS scaffold'
cat github-notes.txt"""
                ),
            ),
        ]
    )

    gha_devops = cicd_git

    advanced = repo_init_steps(
        [
            (
                "Cherry-pick + rebase combo",
                bash(
                    """git switch -c topic
echo t > t.txt && git add t.txt && git commit -m 'topic'
git switch main
echo m > m.txt && git add m.txt && git commit -m 'mainline'
git cherry-pick topic
git log --oneline --graph --all | tee advanced.txt"""
                ),
            ),
        ]
    )

    repo_mgmt = repo_init_steps(
        [
            (
                "Tag a release",
                bash(
                    """echo '1.0.0' > VERSION
git add VERSION && git commit -m 'Release 1.0.0'
git tag -a v1.0.0 -m 'v1.0.0'
git tag -l | tee tags.txt
git show v1.0.0 --no-patch | tee tag-show.txt"""
                ),
            ),
        ]
    )

    troubleshoot = repo_init_steps(
        [
            (
                "Diagnose divergence",
                bash(
                    """git switch -c other
echo o > o.txt && git add o.txt && git commit -m 'other'
git switch main
echo m2 > m2.txt && git add m2.txt && git commit -m 'm2'
git merge other || true
git status | tee status.txt
git log --oneline --graph --all | tee graph.txt"""
                ),
            ),
        ]
    )

    mapping = [
        ("branching", branching),
        ("rebase", rebase),
        ("undoing", undo),
        ("reset", undo),
        ("stash", undo),
        ("cherry-pick", reflog),
        ("reflog", reflog),
        ("bisect", bisect),
        ("hooks", hooks),
        ("gitignore", ignore),
        ("gitattributes", ignore),
        ("object-model", objects),
        ("remotes", remotes),
        ("signed", signing),
        ("security", signing),
        ("history", history),
        ("diffs", history),
        ("merging", conflicts),
        ("conflict", conflicts),
        ("basic-git-workflow", basic),
        ("add-commit", basic),
        ("creating-and-cloning", clone),
        ("installation", install),
        ("configuration", install),
        ("introduction", intro),
        ("pull-request", pr),
        ("code-review", pr),
        ("gitops", gitops),
        ("infrastructure-as-code", iac),
        ("git-for-infrastructure", iac),
        ("git-in-ci-cd", cicd_git),
        ("github-actions-for-devops", gha_devops),
        ("submodule", submodules),
        ("subtree", submodules),
        ("production-git", production),
        ("github-fundamentals", github_fund),
        ("advanced", advanced),
        ("repository-management", repo_mgmt),
        ("releases", repo_mgmt),
        ("troubleshoot", troubleshoot),
    ]
    for key, content in mapping:
        if key in slug:
            return content
    return basic


def _git_iq(slug: str, title: str) -> str:
    return _iq(
        [
            f"Explain **{title}** as you would in a senior engineer interview.",
            "You rebased a shared branch and teammates are blocked — what now?",
            "How do you recover a commit that seems lost?",
            "What Git security controls belong in a production org?",
            "How should Git history look for Infrastructure as Code (IaC) repos?",
        ],
        "Stop force-pushing; communicate; use `reflog` to recover; prefer revert on shared main. Reset/rebase only on private branches.",
        "Signed commits, protected branches, secret scanning, least-privilege tokens, and signed tags for releases.",
    )


# --- Docker --------------------------------------------------------------------

def _docker_lab(slug: str, title: str, lab_dir: str) -> str:
    cleanup_c = "docker rm -f rebash-lab rebash-lab2 2>/dev/null || true\ndocker network rm rebash-net 2>/dev/null || true\ndocker volume rm rebash-vol 2>/dev/null || true\ndocker rmi rebash-lab:local 2>/dev/null || true"

    first = lab_body(
        lab_dir,
        "run, inspect, curl, and remove a container",
        [
            (
                "Run nginx",
                bash(
                    """docker run -d --name rebash-lab -p 18080:80 nginx:alpine
docker ps --filter name=rebash-lab
curl -sI http://127.0.0.1:18080 | head -n 5 | tee headers.txt
docker logs rebash-lab 2>&1 | head -n 20"""
                ),
            ),
        ],
        cleanup_c,
    )

    images = lab_body(
        lab_dir,
        "pull, tag, inspect, and history an image",
        [
            (
                "Image workflow",
                bash(
                    """docker pull alpine:3.20
docker images alpine
docker tag alpine:3.20 rebash-lab:local
docker image inspect rebash-lab:local --format '{{ "{{" }}.Id{{ "}}" }} {{ "{{" }}.Os{{ "}}" }}/{{ "{{" }}.Architecture{{ "}}" }}'
docker history rebash-lab:local | head -n 15 | tee history.txt"""
                ),
            ),
        ],
        "docker rmi rebash-lab:local 2>/dev/null || true",
    )

    dockerfile = lab_body(
        lab_dir,
        "write a Dockerfile, build, run, and verify output",
        [
            (
                "Build and run",
                bash(
                    """cat > Dockerfile << 'EOF'
FROM alpine:3.20
WORKDIR /app
COPY message.txt .
CMD ["cat", "message.txt"]
EOF
echo 'hello from dockerfile' > message.txt
docker build -t rebash-lab:local .
docker run --rm rebash-lab:local | tee out.txt
test "$(cat out.txt)" = 'hello from dockerfile'"""
                ),
            ),
        ],
        "docker rmi rebash-lab:local 2>/dev/null || true",
    )

    multi = lab_body(
        lab_dir,
        "multi-stage build that keeps the final image small",
        [
            (
                "Multi-stage",
                bash(
                    """cat > Dockerfile << 'EOF'
FROM alpine:3.20 AS build
WORKDIR /src
RUN echo 'compiled-artefact' > app.txt
FROM alpine:3.20
COPY --from=build /src/app.txt /app.txt
CMD ["cat","/app.txt"]
EOF
docker build -t rebash-lab:local .
docker run --rm rebash-lab:local
docker image inspect rebash-lab:local --format '{{ "{{" }}.Size{{ "}}" }}' | tee size.txt"""
                ),
            ),
        ],
        "docker rmi rebash-lab:local 2>/dev/null || true",
    )

    compose = lab_body(
        lab_dir,
        "Compose file with network and healthcheck",
        [
            (
                "Compose up",
                bash(
                    """cat > compose.yaml << 'EOF'
services:
  web:
    image: nginx:alpine
    ports: ["18080:80"]
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1/"]
      interval: 5s
      timeout: 3s
      retries: 5
EOF
docker compose up -d
docker compose ps
curl -sI http://127.0.0.1:18080 | head -n 3
docker compose down"""
                ),
            ),
        ],
        "docker compose down -v 2>/dev/null || true",
    )

    network = lab_body(
        lab_dir,
        "user bridge network DNS between containers",
        [
            (
                "User-defined network",
                bash(
                    """docker network create rebash-net
docker run -d --name rebash-lab --network rebash-net nginx:alpine
docker run --rm --network rebash-net curlimages/curl:8.5.0 -sS -o /dev/null -w '%{http_code}\\n' http://rebash-lab/
docker network inspect rebash-net --format '{{ "{{" }}len .Containers{{ "}}" }} containers'"""
                ),
            ),
        ],
        cleanup_c,
    )

    volumes = lab_body(
        lab_dir,
        "persist data with a named volume",
        [
            (
                "Volume round-trip",
                bash(
                    """docker volume create rebash-vol
docker run --rm -v rebash-vol:/data alpine:3.20 sh -c 'echo persist > /data/note.txt'
docker run --rm -v rebash-vol:/data alpine:3.20 cat /data/note.txt | tee note.txt
docker volume inspect rebash-vol | tee vol.json"""
                ),
            ),
        ],
        "docker volume rm rebash-vol 2>/dev/null || true",
    )

    envsec = lab_body(
        lab_dir,
        "pass env files without baking secrets into the image",
        [
            (
                "Env file run",
                bash(
                    """cat > app.env << 'EOF'
APP_MODE=lab
EOF
docker run --rm --env-file app.env alpine:3.20 sh -c 'echo APP_MODE=$APP_MODE' | tee env-out.txt
tee secrets-notes.txt << 'EOF'
Never COPY .env with production secrets into images. Prefer runtime injection / orchestrator secrets.
EOF
cat secrets-notes.txt"""
                ),
            ),
        ],
        "rm -f app.env",
    )

    security = lab_body(
        lab_dir,
        "run as non-root and drop capabilities",
        [
            (
                "Hardened run",
                bash(
                    """docker run --rm --name rebash-lab --user 1000:1000 --read-only --cap-drop ALL alpine:3.20 id | tee id.txt
docker run --rm --security-opt=no-new-privileges:true alpine:3.20 true
tee docker-security.txt << 'EOF'
Prefer minimal base images, non-root, read-only rootfs, and scanning in CI.
EOF"""
                ),
            ),
        ],
        cleanup_c,
    )

    scan = lab_body(
        lab_dir,
        "build an image and produce a simple SBOM-ish inventory",
        [
            (
                "Inventory",
                bash(
                    """cat > Dockerfile << 'EOF'
FROM alpine:3.20
RUN apk add --no-cache curl
EOF
docker build -t rebash-lab:local .
docker run --rm rebash-lab:local sh -c 'apk info -v' | head -n 20 | tee pkgs.txt
echo 'In CI: run trivy/grype + attach SBOM (spdx/cyclonedx).' | tee scan-notes.txt"""
                ),
            ),
        ],
        "docker rmi rebash-lab:local 2>/dev/null || true",
    )

    logging = lab_body(
        lab_dir,
        "inspect container logs and docker events",
        [
            (
                "Logs",
                bash(
                    """docker run -d --name rebash-lab nginx:alpine
docker logs rebash-lab 2>&1 | head -n 20 | tee logs.txt
docker inspect rebash-lab --format '{{ "{{" }}.HostConfig.LogConfig.Type{{ "}}" }}'
docker events --since 1m --until 0s --filter container=rebash-lab | head || true"""
                ),
            ),
        ],
        cleanup_c,
    )

    limits = lab_body(
        lab_dir,
        "apply CPU/memory limits and observe docker stats",
        [
            (
                "Resource limits",
                bash(
                    """docker run -d --name rebash-lab --memory=64m --cpus=0.5 nginx:alpine
docker stats rebash-lab --no-stream | tee stats.txt
docker inspect rebash-lab --format 'mem={{ "{{" }}.HostConfig.Memory{{ "}}" }} cpus={{ "{{" }}.HostConfig.NanoCpus{{ "}}" }}'"""
                ),
            ),
        ],
        cleanup_c,
    )

    registry = lab_body(
        lab_dir,
        "tag images for a registry and document push auth hygiene",
        [
            (
                "Tag for registry",
                bash(
                    """docker pull alpine:3.20
docker tag alpine:3.20 localhost:5000/rebash/alpine:lab
docker images localhost:5000/rebash/alpine
tee registry-notes.txt << 'EOF'
Use credential helpers; prefer short-lived tokens; enable vulnerability scanning on the registry.
Do not docker login with tokens on shared lab machines without cleanup.
EOF
cat registry-notes.txt"""
                ),
            ),
        ],
        "docker rmi localhost:5000/rebash/alpine:lab 2>/dev/null || true",
    )

    install = lab_body(
        lab_dir,
        "verify Docker Engine install and permissions",
        [
            (
                "Doctor",
                bash(
                    """docker version | tee version.txt
docker info | egrep 'Server Version|Cgroup|Logging Driver|Swarm' | tee info.txt
docker run --rm hello-world | tee hello.txt"""
                ),
            ),
        ],
        "docker rmi hello-world 2>/dev/null || true",
    )

    intro = first

    arch = lab_body(
        lab_dir,
        "map client/daemon/images/containers with docker info",
        [
            (
                "Architecture signals",
                bash(
                    """docker version
docker info | tee info.txt
docker system df | tee df.txt
printf '%s\\n' 'CLI -> API -> dockerd -> containerd/runc + image graph driver' | tee model.txt"""
                ),
            ),
        ],
        "# Inspection only",
    )

    cicd = lab_body(
        lab_dir,
        "Dockerfile built in a CI-shaped script",
        [
            (
                "CI build script",
                bash(
                    """cat > Dockerfile << 'EOF'
FROM alpine:3.20
CMD ["echo","ci-ok"]
EOF
cat > ci-build.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
docker build -t rebash-lab:local .
docker run --rm rebash-lab:local
EOF
chmod +x ci-build.sh
./ci-build.sh | tee ci.txt"""
                ),
            ),
        ],
        "docker rmi rebash-lab:local 2>/dev/null || true",
    )

    swarm = lab_body(
        lab_dir,
        "inspect Swarm mode availability without leaving a manager up",
        [
            (
                "Swarm awareness",
                bash(
                    """docker info --format 'swarm={{ "{{" }}.Swarm.LocalNodeState{{ "}}" }}'
tee swarm-notes.txt << 'EOF'
Prefer Kubernetes for most new orchestration. If you init Swarm in a lab, leave with: docker swarm leave --force
EOF
cat swarm-notes.txt
docker run --rm alpine:3.20 echo 'orchestration-agnostic container still runs'"""
                ),
            ),
        ],
        "# Do not leave Swarm enabled on shared machines",
    )

    k8s_bridge = lab_body(
        lab_dir,
        "export a Compose-like app and note the Kubernetes mapping",
        [
            (
                "From Compose thinking to k8s",
                bash(
                    """cat > compose.yaml << 'EOF'
services:
  web:
    image: nginx:alpine
    ports: ["18080:80"]
EOF
docker compose config | tee compose-config.txt
tee map.txt << 'EOF'
Compose service -> Deployment+Service
Compose volume -> PVC
Compose env/files -> ConfigMap/Secret
EOF
docker compose up -d
curl -sI http://127.0.0.1:18080 | head -n 3
docker compose down"""
                ),
            ),
        ],
        "docker compose down -v 2>/dev/null || true",
    )

    production = lab_body(
        lab_dir,
        "production-minded image: non-root, healthcheck, pinned tag",
        [
            (
                "Prod-shaped Dockerfile",
                bash(
                    """cat > Dockerfile << 'EOF'
FROM nginx:1.27-alpine
RUN adduser -D -u 10001 appuser || true
HEALTHCHECK CMD wget -qO- http://127.0.0.1/ || exit 1
EOF
docker build -t rebash-lab:local .
docker run -d --name rebash-lab -p 18080:80 rebash-lab:local
sleep 2
curl -sI http://127.0.0.1:18080 | head -n 3
docker inspect rebash-lab --format '{{ "{{" }}json .State.Health{{ "}}" }}' | tee health.json || true"""
                ),
            ),
        ],
        cleanup_c,
    )

    troubleshoot = lab_body(
        lab_dir,
        "debug a failing container with logs and inspect",
        [
            (
                "Broken CMD",
                bash(
                    """docker run --name rebash-lab alpine:3.20 /bin/does-not-exist || true
docker ps -a --filter name=rebash-lab
docker logs rebash-lab 2>&1 | tee boom.log || true
docker inspect rebash-lab --format '{{ "{{" }}.State.Status{{ "}}" }} {{ "{{" }}.State.ExitCode{{ "}}" }} {{ "{{" }}.State.Error{{ "}}" }}'
docker rm rebash-lab
docker run --rm --name rebash-lab alpine:3.20 echo recovered"""
                ),
            ),
        ],
        cleanup_c,
    )

    capstone = production

    mapping = [
        ("running-your-first", first),
        ("working-with-docker-images", images),
        ("building-images", dockerfile),
        ("dockerfile-best", multi),
        ("multi-stage", multi),
        ("compose", compose),
        ("networking", network),
        ("volumes", volumes),
        ("persistent", volumes),
        ("environment-variables", envsec),
        ("secrets", envsec),
        ("security", security),
        ("scanning", scan),
        ("sbom", scan),
        ("logging", logging),
        ("monitoring", logging),
        ("performance", limits),
        ("resource-limits", limits),
        ("registries", registry),
        ("distribution", registry),
        ("installation", install),
        ("setup", install),
        ("introduction", intro),
        ("architecture", arch),
        ("ci-cd", cicd),
        ("swarm", swarm),
        ("from-docker-to-kubernetes", k8s_bridge),
        ("production", production),
        ("troubleshoot", troubleshoot),
        ("capstone", capstone),
    ]
    for key, content in mapping:
        if key in slug:
            return content
    return first


def _docker_iq(slug: str, title: str) -> str:
    return _iq(
        [
            f"What production problem does **{title}** address in container platforms?",
            "A container restarts continually — how do you triage?",
            "Why are mutable `latest` tags risky in production?",
            "Which container security controls do you insist on before prod?",
            "How do you keep images small and builds fast in CI?",
        ],
        "Check `docker ps -a`, logs, exit code, and `inspect` for OOM/restarts. Confirm command/entrypoint and volume permissions.",
        "Non-root, minimal base, no secrets in layers, scanning, read-only rootfs where possible, and least capabilities.",
    )


# --- AWS -----------------------------------------------------------------------

def _aws_lab(slug: str, title: str, lab_dir: str) -> str:
    warn = "!!! warning \"Cost and account safety\"\n    Prefer read-only `describe`/`get` calls. Create resources only in a sandbox account and destroy them in the cleanup step.\n"

    sts = lab_body(
        lab_dir,
        "verify identity with STS and record account/region facts",
        [
            (
                "Caller identity",
                bash(
                    """aws sts get-caller-identity | tee identity.json
aws configure get region || true
aws ec2 describe-regions --query 'Regions[].RegionName' --output text | tr '\\t' '\\n' | head -n 10 | tee regions.txt
tee safety.txt << 'EOF'
Use a sandbox account. Enable budgets/alerts. Never commit access keys.
EOF
cat safety.txt"""
                ),
            ),
        ],
        "# Read-only — revoke any temporary lab keys you exported",
    )

    # Prepend warning into lab by embedding in focus steps via NOTES - actually inject warn in returned string
    def with_warn(body: str) -> str:
        return warn + "\n" + body

    iam = lab_body(
        lab_dir,
        "inspect IAM identity and simulate policy evaluation read-only",
        [
            (
                "IAM inventory",
                bash(
                    """aws sts get-caller-identity | tee identity.json
aws iam get-user 2>/dev/null | tee user.json || echo 'Using a role session (normal for SSO)'
aws iam list-attached-user-policies --user-name "$(jq -r .Arn identity.json | awk -F/ '{print $NF}')" 2>/dev/null | tee policies.json || true
tee iam-notes.txt << 'EOF'
Prefer IAM Identity Center / roles over long-lived users. Least privilege + SCPs in Organizations.
EOF"""
                ),
            ),
        ],
        "# Read-only",
    )

    vpc = lab_body(
        lab_dir,
        "describe VPCs/subnets/route tables (read-only)",
        [
            (
                "Network inventory",
                bash(
                    """aws sts get-caller-identity >/dev/null
aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,Cidr:CidrBlock,IsDefault:IsDefault}' --output table | tee vpcs.txt
aws ec2 describe-subnets --query 'Subnets[].{Id:SubnetId,Vpc:VpcId,Cidr:CidrBlock,Az:AvailabilityZone}' --output table | head -n 40 | tee subnets.txt
aws ec2 describe-route-tables --query 'RouteTables[0].Routes' --output table 2>/dev/null | head | tee routes.txt || true"""
                ),
            ),
        ],
        "# Read-only",
    )

    compute = lab_body(
        lab_dir,
        "describe EC2/ASG/ELB inventory without launching instances",
        [
            (
                "Compute inventory",
                bash(
                    """aws ec2 describe-instances --query 'Reservations[].Instances[].{Id:InstanceId,Type:InstanceType,State:State.Name}' --output table | tee instances.txt
aws elbv2 describe-load-balancers --query 'LoadBalancers[].{Name:LoadBalancerName,Type:Type,DNS:DNSName}' --output table 2>/dev/null | tee elbs.txt || true
aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[].{Name:AutoScalingGroupName,Desired:DesiredCapacity}' --output table 2>/dev/null | tee asg.txt || true"""
                ),
            ),
        ],
        "# Read-only — do not leave lab instances running",
    )

    storage = lab_body(
        lab_dir,
        "list S3 buckets and inspect one bucket's encryption/public-access block",
        [
            (
                "S3 hygiene check",
                bash(
                    """aws s3api list-buckets --query 'Buckets[].Name' --output text | tr '\\t' '\\n' | head -n 20 | tee buckets.txt
BUCKET=$(head -n 1 buckets.txt)
if [ -n "$BUCKET" ]; then
  aws s3api get-public-access-block --bucket "$BUCKET" 2>/dev/null | tee pab.json || echo 'No PAB or no permission'
  aws s3api get-bucket-encryption --bucket "$BUCKET" 2>/dev/null | tee enc.json || echo 'No encryption config visible'
else
  echo 'No buckets visible — still record the commands.' | tee buckets.txt
fi"""
                ),
            ),
        ],
        "# Read-only",
    )

    containers = lab_body(
        lab_dir,
        "describe ECR/ECS/EKS read-only inventory",
        [
            (
                "Containers inventory",
                bash(
                    """aws ecr describe-repositories --query 'repositories[].repositoryName' --output text 2>/dev/null | tr '\\t' '\\n' | head | tee ecr.txt || true
aws ecs list-clusters --output text 2>/dev/null | tee ecs.txt || true
aws eks list-clusters --output text 2>/dev/null | tee eks.txt || true
tee containers-notes.txt << 'EOF'
Prefer private ECR, least-privilege task roles, and controlled cluster endpoint access.
EOF"""
                ),
            ),
        ],
        "# Read-only",
    )

    serverless = lab_body(
        lab_dir,
        "list Lambda functions and an API Gateway sketch (read-only)",
        [
            (
                "Serverless inventory",
                bash(
                    """aws lambda list-functions --query 'Functions[].{Name:FunctionName,Runtime:Runtime}' --output table 2>/dev/null | head -n 30 | tee lambda.txt || true
aws apigateway get-rest-apis --query 'items[].name' --output text 2>/dev/null | tee apis.txt || true
tee serverless-notes.txt << 'EOF'
Watch concurrency, timeouts, IAM roles, and cold starts. Use budgets for account-level spend.
EOF"""
                ),
            ),
        ],
        "# Read-only",
    )

    monitoring = lab_body(
        lab_dir,
        "list CloudWatch alarm names and recent metrics availability",
        [
            (
                "CloudWatch signals",
                bash(
                    """aws cloudwatch describe-alarms --query 'MetricAlarms[].{Name:AlarmName,State:StateValue}' --output table 2>/dev/null | head -n 40 | tee alarms.txt || true
aws logs describe-log-groups --query 'logGroups[].logGroupName' --output text 2>/dev/null | tr '\\t' '\\n' | head -n 20 | tee log-groups.txt || true
tee o11y-notes.txt << 'EOF'
Alarms need runbooks. Prefer metrics that track user symptoms (latency/errors) over only host CPU.
EOF"""
                ),
            ),
        ],
        "# Read-only",
    )

    security = lab_body(
        lab_dir,
        "read GuardDuty/Security Hub availability and IAM auth details",
        [
            (
                "Security services probe",
                bash(
                    """aws sts get-caller-identity | tee identity.json
aws guardduty list-detectors --output text 2>/dev/null | tee gd.txt || echo 'GuardDuty not enabled/visible'
aws securityhub describe-hub 2>/dev/null | tee sh.json || echo 'Security Hub not enabled/visible'
aws iam get-account-password-policy 2>/dev/null | tee pwd-policy.json || true"""
                ),
            ),
        ],
        "# Read-only",
    )

    cost = lab_body(
        lab_dir,
        "fetch cost-and-usage style signals if permitted (otherwise document)",
        [
            (
                "Cost awareness",
                bash(
                    """aws ce get-cost-and-usage \\
  --time-period Start=$(date -u -v-7d +%F 2>/dev/null || date -u -d '7 days ago' +%F),End=$(date -u +%F) \\
  --granularity DAILY --metrics UnblendedCost \\
  --query 'ResultsByTime[].{Date:TimePeriod.Start,Amount:Total.UnblendedCost.Amount}' \\
  --output table 2>/dev/null | tee cost.txt || echo 'Cost Explorer not permitted — enable budgets anyway' | tee cost.txt
tee finops.txt << 'EOF'
Tag owners, turn off idle NAT/ELB/EC2, use budgets + anomaly detection.
EOF"""
                ),
            ),
        ],
        "# Read-only",
    )

    iac = lab_body(
        lab_dir,
        "list CloudFormation stacks / document IaC entrypoints",
        [
            (
                "IaC inventory",
                bash(
                    """aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE \\
  --query 'StackSummaries[].StackName' --output text 2>/dev/null | tr '\\t' '\\n' | head -n 20 | tee stacks.txt || true
tee iac-notes.txt << 'EOF'
Prefer Terraform/CloudFormation/CDK with plan reviews. No click-ops on prod.
EOF
aws sts get-caller-identity | tee identity.json"""
                ),
            ),
        ],
        "# Read-only",
    )

    cicd_aws = lab_body(
        lab_dir,
        "list CodePipeline/CodeBuild if present; otherwise document OIDC deploy pattern",
        [
            (
                "CI/CD inventory",
                bash(
                    """aws codepipeline list-pipelines --query 'pipelines[].name' --output text 2>/dev/null | tr '\\t' '\\n' | head | tee pipelines.txt || true
aws codebuild list-projects --output text 2>/dev/null | tr '\\t' '\\n' | head | tee builds.txt || true
tee cicd-notes.txt << 'EOF'
GitHub Actions / GitLab OIDC to IAM roles beats static AKIA keys in CI.
EOF
cat cicd-notes.txt"""
                ),
            ),
        ],
        "# Read-only",
    )

    databases = lab_body(
        lab_dir,
        "describe RDS/DynamoDB inventory read-only",
        [
            (
                "Data stores",
                bash(
                    """aws rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,Engine:Engine,Class:DBInstanceClass}' --output table 2>/dev/null | tee rds.txt || true
aws dynamodb list-tables --output text 2>/dev/null | tr '\\t' '\\n' | head | tee dynamo.txt || true
tee db-notes.txt << 'EOF'
Backups, Multi-AZ, encryption, and least-privilege app roles are non-negotiable.
EOF"""
                ),
            ),
        ],
        "# Read-only",
    )

    landing = lab_body(
        lab_dir,
        "document Organizations / account-vending checklist with STS proof",
        [
            (
                "Landing zone checklist",
                bash(
                    """aws sts get-caller-identity | tee identity.json
aws organizations describe-organization 2>/dev/null | tee org.json || echo 'No org access from this identity'
tee landing-zone.txt << 'EOF'
- Mandatory accounts: security, log-archive, shared, workload OU structure
- SCPs for region/deny controls
- Central logging + GuardDuty/Security Hub
- No long-lived keys on humans
EOF
cat landing-zone.txt"""
                ),
            ),
        ],
        "# Read-only",
    )

    dr = lab_body(
        lab_dir,
        "inventory backup vaults / AMI snapshots signals read-only",
        [
            (
                "DR signals",
                bash(
                    """aws backup list-backup-vaults --query 'BackupVaultList[].BackupVaultName' --output text 2>/dev/null | tr '\\t' '\\n' | head | tee vaults.txt || true
aws ec2 describe-snapshots --owner-ids self --query 'Snapshots[:5].[SnapshotId,VolumeSize,StartTime]' --output table 2>/dev/null | tee snaps.txt || true
tee dr-notes.txt << 'EOF'
Define RTO/RPO per service. Test restore paths; backups that are never restored are fiction.
EOF"""
                ),
            ),
        ],
        "# Read-only",
    )

    fundamentals = sts

    troubleshoot = lab_body(
        lab_dir,
        "practise an AWS auth/network triage loop with read-only calls",
        [
            (
                "Triage loop",
                bash(
                    """aws sts get-caller-identity | tee identity.json
aws ec2 describe-vpcs --output table | tee vpcs.txt
aws ec2 describe-security-groups --query 'SecurityGroups[:5].{Id:GroupId,Name:GroupName,Vpc:VpcId}' --output table | tee sgs.txt
tee triage.txt << 'EOF'
Auth -> Region -> Network path (SG/NACL/route) -> Service quotas -> CloudTrail recent denials
EOF
cat triage.txt"""
                ),
            ),
        ],
        "# Read-only",
    )

    mapping = [
        ("fundamentals", fundamentals),
        ("global-infrastructure", fundamentals),
        ("iam", iam),
        ("organizations", iam),
        ("vpc", vpc),
        ("networking", vpc),
        ("compute", compute),
        ("ec2", compute),
        ("load-balancing", compute),
        ("storage", storage),
        ("s3", storage),
        ("containers", containers),
        ("ecs", containers),
        ("eks", containers),
        ("serverless", serverless),
        ("monitoring", monitoring),
        ("observability", monitoring),
        ("security-services", security),
        ("cost", cost),
        ("infrastructure-as-code", iac),
        ("cicd", cicd_aws),
        ("databases", databases),
        ("landing-zone", landing),
        ("reliability", dr),
        ("disaster", dr),
        ("troubleshoot", troubleshoot),
    ]
    body = fundamentals
    for key, content in mapping:
        if key in slug:
            body = content
            break
    return with_warn(body)


def _aws_iq(slug: str, title: str) -> str:
    return _iq(
        [
            f"How does **{title}** appear in a well-run AWS landing zone?",
            "Users report timeouts to a service — what is your AWS-oriented triage order?",
            "How do IAM roles and least privilege change your design for this topic?",
            "What cost or blast-radius controls should wrap experiments in this area?",
            "How would you prove correctness with read-only AWS APIs in an interview whiteboard?",
        ],
        "Confirm identity/region, then path: DNS, SG/NACL, routes, target health, and CloudWatch/CloudTrail signals before changing infrastructure.",
        "Sandbox accounts, budgets, tags, destroy-after-lab, and no long-lived keys in CI — use OIDC/roles.",
    )


def lab_for(tech: str, slug: str, title: str, lab_dir: str) -> str | None:
    if tech == "gitlab":
        return _gitlab_lab(slug, title, lab_dir)
    if tech == "github-actions":
        return _gha_lab(slug, title, lab_dir)
    if tech == "git":
        return _git_lab(slug, title, lab_dir)
    if tech == "docker":
        return _docker_lab(slug, title, lab_dir)
    if tech == "aws":
        return _aws_lab(slug, title, lab_dir)
    return None


def interview_for(tech: str, slug: str, title: str) -> str | None:
    if tech == "gitlab":
        return _gitlab_iq(slug, title)
    if tech == "github-actions":
        return _gha_iq(slug, title)
    if tech == "git":
        return _git_iq(slug, title)
    if tech == "docker":
        return _docker_iq(slug, title)
    if tech == "aws":
        return _aws_iq(slug, title)
    return None
