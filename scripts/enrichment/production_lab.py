"""Production Hands-on Lab bodies: executable, scenario-driven, end-to-end."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    explanation: str
    commands: str
    expected: str


@dataclass
class LabSpec:
    objective: str
    prerequisites: list[str]
    environment: str
    scenario: str
    tasks: list[Task]
    validation: list[str]
    errors: list[tuple[str, str, str]]
    challenge: str
    outcomes: list[str]
    cleanup: str
    warning: str = ""


def render(spec: LabSpec, lab_dir: str) -> str:
    lines: list[str] = []
    if spec.warning:
        lines += [spec.warning.rstrip(), ""]
    lines += [
        "### Objective",
        "",
        spec.objective.strip(),
        "",
        "### Prerequisites",
        "",
    ]
    for p in spec.prerequisites:
        lines.append(f"- {p}")
    lines += [
        "",
        "### Lab environment",
        "",
        f"Workspace: `{lab_dir}`",
        "",
        spec.environment.strip(),
        "",
        "```bash",
        f"mkdir -p {lab_dir} && cd {lab_dir}",
        "```",
        "",
        "### Real-world scenario",
        "",
        spec.scenario.strip(),
        "",
        "### Step-by-step tasks",
        "",
    ]
    for i, task in enumerate(spec.tasks, start=1):
        lines += [
            f"#### Task {i} – {task.name}",
            "",
            task.explanation.strip(),
            "",
            "```bash",
            task.commands.strip(),
            "```",
            "",
            f"**Expected output:** {task.expected.strip()}",
            "",
        ]
    lines += ["### Validation steps", ""]
    for v in spec.validation:
        lines.append(f"- [ ] {v}")
    lines += [
        "",
        "### Common errors and fixes",
        "",
        "| Error | Cause | Fix |",
        "|-------|-------|-----|",
    ]
    for err, cause, fix in spec.errors:
        lines.append(f"| {err} | {cause} | {fix} |")
    lines += [
        "",
        "### Challenge exercise",
        "",
        spec.challenge.strip(),
        "",
        "### Learning outcomes",
        "",
    ]
    for o in spec.outcomes:
        lines.append(f"- {o}")
    lines += [
        "",
        "### Cleanup",
        "",
        "```bash",
        spec.cleanup.strip(),
        "```",
        "",
    ]
    return "\n".join(lines)


def _slug_hit(slug: str, *keys: str) -> bool:
    return any(k in slug for k in keys)


def build_lab(tech: str, slug: str, title: str, lab_dir: str, headings: list[str] | None = None) -> str:
    builders = {
        "kubernetes": _k8s,
        "terraform": _tf,
        "helm": _helm,
        "docker": _docker,
        "git": _git,
        "gitlab": _gitlab,
        "github-actions": _gha,
        "aws": _aws,
        "jenkins": _jenkins,
        "linux": _linux,
        "shell": _shell,
        "python": _python,
        "networking": _networking,
    }
    fn = builders.get(tech, _generic)
    return render(fn(slug, title, lab_dir, headings or []), lab_dir)


# --- Kubernetes ----------------------------------------------------------------

def _k8s(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    ns = "rebash-lab"
    base_prereq = [
        "kubectl configured against a lab cluster (kind/minikube preferred)",
        "Cluster-admin or namespace-create rights in the lab cluster",
        f"Writable workspace at `{lab_dir}`",
    ]
    cleanup = f"kubectl delete namespace {ns} --ignore-not-found\n# Keep ~/rebash-kubernetes/ for later tutorials"

    if _slug_hit(slug, "pod"):
        tasks = [
            Task(
                "Declare and apply a Pod",
                "Create an isolated namespace and apply a Pod manifest so the scheduler places a container.",
                f"""kubectl create namespace {ns} --dry-run=client -o yaml | kubectl apply -f -
cat > pod.yaml << 'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: web
  namespace: {ns}
  labels:
    app: web
spec:
  containers:
    - name: nginx
      image: nginx:1.27-alpine
      ports:
        - containerPort: 80
EOF
kubectl apply -f pod.yaml
kubectl wait --for=condition=Ready pod/web -n {ns} --timeout=120s
kubectl get pod web -n {ns} -o wide""",
                "Pod `web` shows Ready 1/1 and a node name.",
            ),
            Task(
                "Inspect Events and prove the app answers",
                "Use describe/Events/logs — the same triage path used in production incidents.",
                f"""kubectl describe pod web -n {ns} | tee describe.txt
kubectl get events -n {ns} --sort-by=.lastTimestamp | tail -n 20
kubectl exec -n {ns} web -- wget -qO- http://127.0.0.1/ | head -n 5""",
                "HTML from nginx appears; describe.txt contains Events without ImagePullBackOff.",
            ),
            Task(
                "Capture evidence for handover",
                "Save a short status snapshot you would attach to a ticket.",
                f"""kubectl get pod,events -n {ns} -o wide | tee evidence.txt
test -s evidence.txt""",
                "evidence.txt is non-empty and lists the Pod.",
            ),
        ]
    elif _slug_hit(slug, "deployment", "replicated"):
        tasks = [
            Task(
                "Create a Deployment",
                "Controllers own Pods — practise Deployment create and rollout status.",
                f"""kubectl create namespace {ns} --dry-run=client -o yaml | kubectl apply -f -
kubectl create deployment demo --image=nginx:1.27-alpine -n {ns} --replicas=2
kubectl rollout status deployment/demo -n {ns}
kubectl get deploy,rs,pods -n {ns} -o wide""",
                "Deployment available; two Pods Running.",
            ),
            Task(
                "Scale and verify ReplicaSets",
                "Scale is a production change — confirm the new ReplicaSet owns Pods.",
                f"""kubectl scale deployment/demo -n {ns} --replicas=3
kubectl get rs,pods -n {ns} -l app=demo
kubectl rollout history deployment/demo -n {ns}""",
                "Three Pods Ready; rollout history shows revisions.",
            ),
        ]
    elif _slug_hit(slug, "service", "cluster-networking"):
        tasks = [
            Task(
                "Expose a Deployment with a Service",
                "Services give a stable virtual IP and DNS name while Pods churn.",
                f"""kubectl create namespace {ns} --dry-run=client -o yaml | kubectl apply -f -
kubectl create deployment web --image=nginx:1.27-alpine -n {ns}
kubectl expose deployment web -n {ns} --port=80 --target-port=80 --name=web
kubectl get svc,endpoints -n {ns}""",
                "Service `web` has Endpoints populated.",
            ),
            Task(
                "Prove ClusterIP reachability",
                "Test from inside the cluster the way apps discover each other.",
                f"""kubectl run curl --rm -it --restart=Never -n {ns} --image=curlimages/curl:8.5.0 -- \\
  curl -sS -o /dev/null -w '%{{http_code}}\\n' http://web
kubectl describe svc web -n {ns} | tee svc.txt""",
                "HTTP status `200` printed; svc.txt shows selector and Endpoints.",
            ),
        ]
    elif _slug_hit(slug, "rbac", "security"):
        tasks = [
            Task(
                "Create ServiceAccount, Role, RoleBinding",
                "Least privilege starts with namespaced RBAC objects.",
                f"""kubectl create namespace {ns} --dry-run=client -o yaml | kubectl apply -f -
kubectl create serviceaccount viewer -n {ns}
cat > rbac.yaml << EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: {ns}
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: viewer-pods
  namespace: {ns}
subjects:
  - kind: ServiceAccount
    name: viewer
    namespace: {ns}
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
EOF
kubectl apply -f rbac.yaml""",
                "Role and RoleBinding created without error.",
            ),
            Task(
                "Prove allow and deny with auth can-i",
                "Never guess permissions — ask the API.",
                f"""kubectl auth can-i list pods -n {ns} --as=system:serviceaccount:{ns}:viewer
kubectl auth can-i delete pods -n {ns} --as=system:serviceaccount:{ns}:viewer || true""",
                "`yes` for list; `no` (or non-zero) for delete.",
            ),
        ]
    else:
        hint = headings[0] if headings else title
        tasks = [
            Task(
                "Apply a topic workload",
                f"Create a namespace and a small Deployment to practise **{hint}** against a live API.",
                f"""kubectl create namespace {ns} --dry-run=client -o yaml | kubectl apply -f -
kubectl create deployment topic --image=nginx:1.27-alpine -n {ns}
kubectl rollout status deployment/topic -n {ns}
kubectl get all -n {ns}""",
                "Deployment Ready; Pods listed under the namespace.",
            ),
            Task(
                "Inspect and gather evidence",
                "Production changes always leave an audit trail of describe/Events.",
                f"""kubectl describe deploy topic -n {ns} | tee describe.txt
kubectl get events -n {ns} --sort-by=.lastTimestamp | tail -n 15 | tee events.txt""",
                "describe.txt and events.txt capture healthy Objects/Events.",
            ),
        ]

    return LabSpec(
        objective=f"Build and verify a working Kubernetes solution for **{title}** that you can inspect, prove, and tear down safely.",
        prerequisites=base_prereq,
        environment="Local kind/minikube or a dedicated sandbox cluster. Never target a shared production API server.",
        scenario=f"Your platform team is rolling out **{title}** for a new microservice. You must apply the change in an isolated namespace, prove it works with kubectl, and leave evidence for the on-call handover.",
        tasks=tasks,
        validation=[
            f"Namespace `{ns}` contains the expected Ready objects",
            "You can explain each Task command from the Theory section",
            "Cleanup deletes the namespace without leftover workloads",
        ],
        errors=[
            ("ImagePullBackOff", "Wrong tag or registry auth", "Fix image reference; check pull secrets"),
            ("Pending Pod", "Scheduling / quota / PVC", "`kubectl describe pod` and read Events"),
            ("Empty Endpoints", "Selector or readiness mismatch", "Compare Service selector to Pod labels and Ready"),
        ],
        challenge="Add a readinessProbe and a ResourceQuota to the namespace, then show that over-quota creates are rejected.",
        outcomes=[
            f"Applied a real cluster change for {title}",
            "Used describe/Events for verification",
            "Destroyed lab resources cleanly",
        ],
        cleanup=cleanup,
    )


# --- Terraform -----------------------------------------------------------------

def _tf(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    destroy = "terraform destroy -auto-approve\nrm -rf .terraform tfplan 2>/dev/null || true"
    tasks = [
        Task(
            "Author and initialise configuration",
            "Use local/null providers so the lab never bills a cloud account.",
            """cat > versions.tf << 'EOF'
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = { source = "hashicorp/null", version = "~> 3.2" }
  }
}
EOF
cat > main.tf << 'EOF'
resource "null_resource" "lab" {
  triggers = { topic = "rebash-lab" }
  provisioner "local-exec" {
    command = "echo applied > applied.txt"
  }
}
output "note" { value = null_resource.lab.triggers.topic }
EOF
terraform init
terraform validate""",
            "`Terraform has been successfully initialized` and validate succeeds.",
        ),
        Task(
            "Plan, apply, and prove outputs",
            "Treat the plan as the change ticket — review before apply.",
            """terraform plan -out=tfplan
terraform show -no-color tfplan | tee plan.txt
terraform apply tfplan
terraform output
test -f applied.txt && cat applied.txt""",
            "plan.txt shows create; `applied` written; output prints the note.",
        ),
    ]
    if _slug_hit(slug, "variable", "workspace", "module", "state"):
        tasks.append(
            Task(
                "Inspect state safely",
                "State is the source of truth — list and show without hand-editing.",
                """terraform state list | tee state-list.txt
terraform state show null_resource.lab | tee state-show.txt""",
                "state-list.txt contains `null_resource.lab`.",
            )
        )
    return LabSpec(
        objective=f"Run a complete Terraform workflow (init → plan → apply → prove → destroy) for **{title}** without paid cloud resources.",
        prerequisites=["Terraform CLI ≥ 1.5", "Network access to download the null provider once"],
        environment="Local Terraform only (`null`/`local` providers). No AWS/GCP/Azure credentials required.",
        scenario=f"You are automating **{title}** for a platform repo. Reviewers expect a clean plan artefact, applied evidence, and a destroy path before merge.",
        tasks=tasks,
        validation=[
            "terraform validate passes",
            "Plan was saved and reviewed before apply",
            "Destroy completes with empty state (or resources removed)",
        ],
        errors=[
            ("Provider not found", "Missing init / network", "Run `terraform init` again"),
            ("State locked", "Concurrent apply", "Wait or coordinate; never force-unlock casually"),
            ("Unexpected destroy in plan", "Drift or wrong workspace", "Read plan line-by-line before apply"),
        ],
        challenge="Add an input variable with a validation block and fail the plan with an illegal value, then fix it.",
        outcomes=["Completed a reviewable plan/apply cycle", "Proved outputs/files exist", "Destroyed lab state"],
        cleanup=destroy,
    )


# --- Helm ----------------------------------------------------------------------

def _helm(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    hns = "rebash-helm"
    cleanup = f"helm uninstall labchart -n {hns} 2>/dev/null || true\nkubectl delete namespace {hns} --ignore-not-found"
    return LabSpec(
        objective=f"Create, lint, render, install, and uninstall a Helm chart demonstrating **{title}**.",
        prerequisites=["helm CLI", "kubectl + lab cluster", "Ability to create namespaces"],
        environment=f"Helm 3 against kind/minikube; release namespace `{hns}`.",
        scenario=f"A team wants **{title}** packaged as a chart so GitOps can promote the same artefact across environments.",
        tasks=[
            Task(
                "Create and lint a chart",
                "Scaffold a chart and fail the build on lint errors before install.",
                """helm version
helm create labchart
helm lint ./labchart | tee lint.txt
helm template labchart ./labchart | egrep '^kind:' | sort | uniq -c | tee kinds.txt""",
                "lint reports no failures; kinds.txt lists Deployment/Service/etc.",
            ),
            Task(
                "Install with values override",
                "Prove values change rendered replicas, then install with wait.",
                f"""kubectl create namespace {hns} --dry-run=client -o yaml | kubectl apply -f -
cat > myvalues.yaml << 'EOF'
replicaCount: 2
EOF
helm template labchart ./labchart -f myvalues.yaml | egrep 'replicas:' | head
helm upgrade --install labchart ./labchart -n {hns} -f myvalues.yaml --wait --timeout 2m
helm list -n {hns}
kubectl get deploy -n {hns}""",
                "Release deployed; Deployment shows 2 replicas (or Ready pods).",
            ),
        ],
        validation=["helm lint clean", "Release listed in namespace", "Uninstall removes the release"],
        errors=[
            ("PENDING_INSTALL", "Image pull / probes", "`helm status` + `kubectl describe`"),
            ("lint failed", "Template YAML break", "Fix templates; re-run helm lint"),
            ("context deadline", "Slow cluster", "Increase --timeout or fix readiness"),
        ],
        challenge="Add a ConfigMap template driven by values and prove it with `helm get manifest`.",
        outcomes=["Packaged Kubernetes YAML as a chart", "Overrode values safely", "Cleaned up the release"],
        cleanup=cleanup,
    )


# --- Docker --------------------------------------------------------------------

def _docker(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    cleanup = "docker rm -f rebash-lab 2>/dev/null || true\ndocker rmi rebash-lab:local 2>/dev/null || true\ndocker compose down -v 2>/dev/null || true"
    if _slug_hit(slug, "compose"):
        tasks = [
            Task(
                "Write Compose file and start stack",
                "Compose is how many teams run multi-container apps locally and in CI.",
                """cat > compose.yaml << 'EOF'
services:
  web:
    image: nginx:alpine
    ports: ["18080:80"]
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1/"]
      interval: 5s
      retries: 5
EOF
docker compose up -d
docker compose ps
curl -sI http://127.0.0.1:18080 | head -n 5 | tee headers.txt""",
                "Service healthy/running; headers show HTTP/1.1 200.",
            ),
            Task(
                "Inspect and stop cleanly",
                "Always tear down Compose projects so ports and networks do not leak.",
                """docker compose logs --tail=20 web | tee compose.log
docker compose down
test ! -z "$(cat headers.txt)" """,
                "Logs captured; containers removed after down.",
            ),
        ]
    elif _slug_hit(slug, "dockerfile", "building", "multi-stage"):
        tasks = [
            Task(
                "Author Dockerfile and build",
                "Images are the deployment unit — build a tagged local image.",
                """cat > Dockerfile << 'EOF'
FROM alpine:3.20 AS build
WORKDIR /src
RUN echo 'artefact' > app.txt
FROM alpine:3.20
COPY --from=build /src/app.txt /app.txt
CMD ["cat", "/app.txt"]
EOF
docker build -t rebash-lab:local .
docker image ls rebash-lab:local""",
                "Image `rebash-lab:local` listed with a recent CREATED time.",
            ),
            Task(
                "Run and verify output",
                "Prove the runtime image does what the Dockerfile claims.",
                """docker run --rm --name rebash-lab rebash-lab:local | tee out.txt
test "$(cat out.txt)" = 'artefact'""",
                "out.txt contains exactly `artefact`.",
            ),
        ]
    else:
        tasks = [
            Task(
                "Run and inspect a container",
                "Start from a known image, publish a port, and verify HTTP.",
                """docker run -d --name rebash-lab -p 18080:80 nginx:alpine
docker ps --filter name=rebash-lab
curl -sI http://127.0.0.1:18080 | head -n 5 | tee headers.txt
docker logs rebash-lab 2>&1 | head -n 10 | tee logs.txt""",
                "Container Up; HTTP 200 in headers.txt.",
            ),
            Task(
                "Inspect runtime config",
                "Use inspect for status — production debugging rarely starts with guesswork.",
                """docker inspect rebash-lab --format '{{ "{{" }}.State.Status{{ "}}" }} {{ "{{" }}.Config.Image{{ "}}" }}' | tee inspect.txt
test -s inspect.txt""",
                "inspect.txt shows `running` and the nginx image.",
            ),
        ]
    return LabSpec(
        objective=f"Build or run a real Docker solution for **{title}** and prove it with inspect/logs/HTTP.",
        prerequisites=["Docker Engine or Docker Desktop", "Permission to run containers"],
        environment="Local Docker daemon. Clean up containers/images after the lab.",
        scenario=f"You are validating **{title}** before it lands in CI. The change must be reproducible with copy-paste commands and leave no orphan containers.",
        tasks=tasks,
        validation=["Container or image behaves as Expected output describes", "Ports respond or command output matches", "Cleanup removes lab resources"],
        errors=[
            ("port is already allocated", "Previous lab left a container", "`docker rm -f` the old name or change port"),
            ("permission denied", "User not in docker group", "Use rootless Docker or fix group membership"),
            ("manifest unknown", "Bad tag", "Pin a real tag such as `nginx:alpine`"),
        ],
        challenge="Add a non-root USER (or Compose healthcheck) and prove it with inspect.",
        outcomes=["Executed a real Docker workflow", "Captured evidence files", "Removed disposable resources"],
        cleanup=cleanup,
    )


# --- Git -----------------------------------------------------------------------

def _git(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    tasks = [
        Task(
            "Initialise a repository and first commit",
            "Every production change starts as a commit with clear identity config.",
            """git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
echo '# lab' > README.md
git add README.md
git commit -m 'Initial commit'
git log --oneline | tee log.txt""",
            "log.txt shows the initial commit on `main`.",
        ),
    ]
    if _slug_hit(slug, "branch", "merge", "rebase", "conflict"):
        tasks.append(
            Task(
                "Branch, change, and integrate",
                "Practise the integration path your team uses in pull requests.",
                """git switch -c feature/lab
echo feature > note.txt
git add note.txt && git commit -m 'Add note'
git switch main
git merge feature/lab
git log --oneline --graph --all | tee graph.txt""",
                "graph.txt shows the merge/commit topology.",
            )
        )
    else:
        tasks.append(
            Task(
                "Inspect status and diff discipline",
                "Clean working trees prevent accidental commits of secrets.",
                """echo 'work' > work.txt
git status
git add work.txt
git commit -m 'Add work.txt'
git show --stat HEAD | tee show.txt""",
                "show.txt lists work.txt in the commit.",
            )
        )
    return LabSpec(
        objective=f"Complete a real Git workflow for **{title}** with commits you can inspect and recover.",
        prerequisites=["Git 2.x installed"],
        environment="Local Git repository only (no required remote).",
        scenario=f"A delivery team is standardising **{title}**. You prototype the workflow in a throwaway repo and capture log evidence for the playbook.",
        tasks=tasks,
        validation=["Repository has at least two commits or a merge as designed", "log/graph evidence files exist"],
        errors=[
            ("Author identity unknown", "Missing user.name/email", "Set local `git config user.*` as in Task 1"),
            ("merge conflict", "Overlapping edits", "Edit file, `git add`, complete merge"),
            ("detached HEAD", "Checked out a raw SHA", "`git switch -c` a branch before committing"),
        ],
        challenge="Use `git reflog` to recover a commit after a hard reset on a private branch.",
        outcomes=["Performed real Git operations", "Left auditable history", "Understood recovery basics"],
        cleanup="# Safe local repo — delete the lab directory when finished:\n# rm -rf \"$(pwd)\"",
    )


# --- GitLab / GHA --------------------------------------------------------------

def _gitlab(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    return LabSpec(
        objective=f"Author a valid `.gitlab-ci.yml` that models **{title}** and validate it locally before pushing.",
        prerequisites=["Python 3 with PyYAML (`pip install pyyaml`)", "Optional: GitLab project to run the pipeline"],
        environment="File-first lab. Push to GitLab only when you want a runner to execute jobs.",
        scenario=f"Your squad is encoding **{title}** as CI. Reviewers reject YAML that does not parse or that skips artefacts/needs incorrectly.",
        tasks=[
            Task(
                "Write pipeline YAML",
                "Stages and jobs must be explicit so MR pipelines are predictable.",
                """mkdir -p src && echo 'print("ok")' > src/app.py
cat > .gitlab-ci.yml << 'EOF'
stages: [lint, test]
lint:
  stage: lint
  image: python:3.12-alpine
  script:
    - python -m py_compile src/app.py
test:
  stage: test
  image: python:3.12-alpine
  needs: [lint]
  script:
    - python src/app.py
EOF
python3 -c "import yaml; d=yaml.safe_load(open('.gitlab-ci.yml')); assert d['stages']==['lint','test']; print('OK', list(d))" """,
                "Prints `OK` and job names; no YAML exception.",
            ),
            Task(
                "Simulate the scripts locally",
                "Prove the job script works before burning runner minutes.",
                """python3 -m py_compile src/app.py
python3 src/app.py | tee out.txt
test "$(cat out.txt)" = 'ok'""",
                "Compile succeeds; out.txt is `ok`.",
            ),
        ],
        validation=["`.gitlab-ci.yml` parses", "Local script path matches job intent"],
        errors=[
            ("yaml.scanner.ScannerError", "Indentation", "Use 2-space indent; re-validate with PyYAML"),
            ("job stuck pending", "No runner / tags", "Check runner tags match job tags"),
            ("needs not found", "Typo in job name", "Align `needs` with actual job keys"),
        ],
        challenge="Add an `artifacts:` path from lint to test and document expire_in.",
        outcomes=["Produced reviewable GitLab CI YAML", "Validated structure and scripts locally"],
        cleanup="# File-only lab — keep YAML for the next tutorial",
    )


def _gha(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    return LabSpec(
        objective=f"Author a GitHub Actions workflow that implements **{title}** and validate YAML structure locally.",
        prerequisites=["Python 3 with PyYAML", "Optional: GitHub repo to run the workflow"],
        environment="Workflows under `.github/workflows/`. In docs, wrap GitHub Actions expressions in Jinja raw blocks so MkDocs macros do not parse them; use heredocs in the lab.",
        scenario=f"Platform engineering wants **{title}** as a reusable workflow pattern. You prototype YAML that passes review and runs on `ubuntu-latest`.",
        tasks=[
            Task(
                "Create workflow file",
                "Jobs and steps must be explicit; pin mainstream actions.",
                """mkdir -p .github/workflows
cat > .github/workflows/lab.yml << 'EOF'
name: lab
on:
  workflow_dispatch:
  push:
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Prove workspace
        run: |
          mkdir -p out
          echo ok > out/marker.txt
          test -s out/marker.txt
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/lab.yml')); print('workflow OK')" """,
                "`workflow OK` printed; file exists under `.github/workflows/`.",
            ),
            Task(
                "Dry-run the shell steps locally",
                "The `run:` block should work in a normal shell before CI.",
                """mkdir -p out && echo ok > out/marker.txt
test -s out/marker.txt && cat out/marker.txt""",
                "Prints `ok`.",
            ),
        ],
        validation=["Workflow YAML parses", "Local run steps succeed"],
        errors=[
            ("Invalid workflow file", "YAML/indent", "Validate with PyYAML / actionlint"),
            ("Action not found", "Bad uses ref", "Pin `actions/checkout@v4`"),
            ("Permission denied", "Missing permissions/OIDC", "Set least-privilege `permissions:`"),
        ],
        challenge="Add a second job with `needs: build` that uploads `out/` as an artefact (YAML only is fine offline).",
        outcomes=["Created a real workflow file", "Validated structure before push"],
        cleanup="# Keep workflow stubs under ~/rebash-github-actions/",
    )


# --- AWS -----------------------------------------------------------------------

def _aws(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    return LabSpec(
        objective=f"Use read-only AWS APIs to inventory and verify aspects of **{title}** in a sandbox account.",
        prerequisites=["AWS CLI v2", "Credentials for a **sandbox** account (SSO or short-lived keys)"],
        environment="Prefer `describe`/`list`/`get` APIs. Create resources only with an explicit destroy path.",
        scenario=f"Security asks for evidence that **{title}** is configured correctly. You gather CLI proof without click-ops drift.",
        warning='!!! warning "Cost and account safety"\n    Use a sandbox account. Prefer read-only calls. Destroy anything you create before leaving the lab.\n',
        tasks=[
            Task(
                "Prove caller identity",
                "Every AWS change starts by knowing which account/role you are.",
                """aws sts get-caller-identity | tee identity.json
aws configure get region || true
test -s identity.json""",
                "JSON includes Account, Arn, and UserId.",
            ),
            Task(
                "Collect topic signals",
                "Inventory the service surface related to this module.",
                """aws ec2 describe-vpcs --query 'Vpcs[].{Id:VpcId,Cidr:CidrBlock}' --output table 2>/dev/null | tee vpcs.txt || true
aws iam get-account-summary 2>/dev/null | tee iam-summary.json || true
tee notes.txt << 'EOF'
Record which APIs apply to this topic and any NotAuthorized errors for follow-up.
EOF
cat notes.txt""",
                "Evidence files created even if some APIs are denied.",
            ),
        ],
        validation=["identity.json present", "No long-lived keys committed to the repo"],
        errors=[
            ("Unable to locate credentials", "No profile/SSO", "Run `aws sso login` or export sandbox keys"),
            ("AccessDenied", "Least privilege", "Use a role that can read the service — or document the deny"),
            ("UnauthorizedOperation", "Wrong region/account", "Check `AWS_REGION` and account id"),
        ],
        challenge="Enable a cost budget alarm in the sandbox (or document the console clicks) and screenshot/CLI-describe it.",
        outcomes=["Authenticated safely", "Captured read-only evidence", "Avoided unmanaged spend"],
        cleanup="# Revoke/lab-expire any temporary keys you exported\n# Do not leave EC2/ELB/NAT running",
    )


# --- Jenkins -------------------------------------------------------------------

def _jenkins(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    if _slug_hit(slug, "install"):
        tasks = [
            Task(
                "Start Jenkins LTS with Docker Compose",
                "Controllers should be reproducible — Compose pins the LTS image.",
                """cat > compose.yaml << 'EOF'
services:
  jenkins:
    image: jenkins/jenkins:lts-jdk17
    ports: ["8080:8080", "50000:50000"]
    volumes: ["jenkins_home:/var/jenkins_home"]
volumes:
  jenkins_home:
EOF
docker compose up -d
docker compose ps
docker compose logs --tail=30 jenkins | tee boot.log""",
                "Service running; logs show Jenkins starting.",
            ),
            Task(
                "Read initial admin password from the container",
                "The setup wizard requires the one-time password from JENKINS_HOME.",
                """sleep 15
docker compose exec -T jenkins bash -lc 'test -f /var/jenkins_home/secrets/initialAdminPassword && cat /var/jenkins_home/secrets/initialAdminPassword' | tee initialAdminPassword.txt || \\
  docker compose logs jenkins | tee boot2.log
ls -l initialAdminPassword.txt boot.log 2>/dev/null || true""",
                "Password file present (or logs show Jenkins still warming up — retry once).",
            ),
        ]
        cleanup = "docker compose down -v"
    elif _slug_hit(slug, "pipeline", "jenkinsfile"):
        tasks = [
            Task(
                "Author a Declarative Jenkinsfile",
                "Pipeline-as-code is the production default — Declarative first.",
                """cat > Jenkinsfile << 'EOF'
pipeline {
  agent any
  options { timestamps() }
  stages {
    stage('Build') {
      steps {
        sh 'mkdir -p dist && echo ok > dist/status.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'test -f dist/status.txt && grep -q ok dist/status.txt'
      }
    }
  }
  post {
    always { archiveArtifacts artifacts: 'dist/**', allowEmptyArchive: true }
  }
}
EOF
test -f Jenkinsfile && grep -n 'pipeline\\|stages\\|post' Jenkinsfile""",
                "Jenkinsfile contains pipeline/stages/post blocks.",
            ),
            Task(
                "Validate structure locally",
                "Run the shell steps the Pipeline will execute so failures are cheap.",
                """mkdir -p dist && echo ok > dist/status.txt
test -f dist/status.txt && grep -q ok dist/status.txt
tar -cf evidence.tar Jenkinsfile dist
ls -l evidence.tar""",
                "Shell checks pass; evidence.tar created for the job upload story.",
            ),
        ]
        cleanup = "rm -f evidence.tar\n# Keep Jenkinsfile for SCM modules"
    else:
        tasks = [
            Task(
                "Capture controller/agent mental model files",
                "Document how this topic shows up on a real controller.",
                f"""tee scenario.md << 'EOF'
Topic: {title}
- Controller owns config and orchestration
- Agents execute untrusted build steps
- Prefer Jenkinsfile in SCM over click-ops jobs
EOF
cat scenario.md
mkdir -p jobs && echo 'pipelineJob stub' > jobs/README.txt""",
                "scenario.md and jobs/README.txt exist.",
            ),
            Task(
                "Write a minimal Declarative stub",
                "Even management topics should leave a Pipeline artefact.",
                """cat > Jenkinsfile << 'EOF'
pipeline {
  agent any
  stages { stage('OK') { steps { echo 'lab' } } }
}
EOF
grep -n agent Jenkinsfile""",
                "Jenkinsfile present with an agent directive.",
            ),
        ]
        cleanup = "# Keep lab notes under ~/rebash-jenkins/"
    return LabSpec(
        objective=f"Configure a real Jenkins-facing artefact for **{title}** (Compose controller and/or Jenkinsfile) you can run or import.",
        prerequisites=["Docker Engine for controller labs", "Text editor / shell"],
        environment="Local Docker Compose Jenkins LTS where a live UI is needed; file-only Jenkinsfile labs otherwise.",
        scenario=f"Your organisation is standardising **{title}**. You prototype on a lab controller, keep everything as files, and avoid building on the built-in node in production designs.",
        tasks=tasks,
        validation=["Artefacts from tasks exist", "No secrets committed", "Compose stack stopped if started"],
        errors=[
            ("port 8080 in use", "Another Jenkins/lab", "Change host port or stop the other container"),
            ("permission denied on volume", "Podman/rootless path", "Fix volume ownership or use named volumes"),
            ("agent any hangs", "No executors", "Attach an agent or enable a lab executor carefully"),
        ],
        challenge="Disable builds on the built-in node in your notes and document the agent label you would require instead.",
        outcomes=["Produced runnable Jenkins artefacts", "Practised safe lab controller hygiene"],
        cleanup=cleanup,
    )


# --- Linux / Shell / Python / Networking ---------------------------------------

def _linux(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    tasks = [
        Task(
            "Gather host baseline",
            "Production Linux work starts with facts: kernel, OS, disk, memory.",
            """uname -a | tee uname.txt
cat /etc/os-release | tee os-release.txt
df -h | tee df.txt
free -h | tee free.txt 2>/dev/null || vm_stat | tee free.txt""",
            "Baseline files created with real host data.",
        ),
        Task(
            "Topic drill with modern tools",
            f"Exercise commands relevant to **{title}** (prefer `ip`/`ss`/`systemctl`/`journalctl` when applicable).",
            """ip -br a 2>/dev/null | tee ip.txt || ifconfig | tee ip.txt
ss -lntu 2>/dev/null | head -n 20 | tee ss.txt || netstat -lntu 2>/dev/null | head | tee ss.txt || true
systemctl is-system-running 2>/dev/null | tee systemd-state.txt || echo 'no systemd' | tee systemd-state.txt""",
            "ip/ss/systemd evidence files exist (or honest fallbacks).",
        ),
    ]
    return LabSpec(
        objective=f"Perform real host operations for **{title}** and capture command evidence.",
        prerequisites=["Linux or macOS with a POSIX shell", "sudo only if a task requires it"],
        environment="Local machine or lab VM. Prefer non-destructive inspection unless the tutorial requires a change.",
        scenario=f"You are onboarding a Cloud VM. **{title}** is failing health checks — gather facts before changing production.",
        tasks=tasks,
        validation=["Evidence files under the lab directory", "You can interpret each output"],
        errors=[
            ("command not found", "Minimal image", "Install util-linux/iproute2 or use the documented fallback"),
            ("Permission denied", "Needs root", "Re-run the specific command with sudo if appropriate"),
        ],
        challenge="Write a one-page runbook snippet (`runbook.md`) listing the first five commands you would run at 03:00.",
        outcomes=["Collected real host telemetry", "Practised modern Linux tooling"],
        cleanup="# Keep ~/rebash-linux/ evidence for later modules",
    )


def _shell(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    return LabSpec(
        objective=f"Write and run a real shell script that demonstrates **{title}** with `set -euo pipefail`.",
        prerequisites=["bash", "chmod"],
        environment="Local bash. Scripts must be executable and idempotent where practical.",
        scenario=f"A CI job needs a reliable script for **{title}**. Fragile scripts without `set -euo pipefail` have caused outages.",
        tasks=[
            Task(
                "Write the script",
                "Production scripts fail fast and log clearly.",
                f"""cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
TOPIC="{title}"
mkdir -p out
echo "topic=$TOPIC" | tee out/meta.txt
date -u +%Y-%m-%dT%H:%M:%SZ | tee out/timestamp.txt
test -s out/meta.txt
EOF
chmod +x lab.sh
./lab.sh
cat out/meta.txt""",
                "Script exits 0; out/meta.txt contains the topic line.",
            ),
            Task(
                "Prove failure handling",
                "A broken command must fail the script — that is the point of `set -e`.",
                """cat > fail.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
false
echo should-not-print
EOF
chmod +x fail.sh
./fail.sh >fail.out 2>&1 || echo "failed_as_expected=$!" | tee fail.out
grep -q should-not-print fail.out && exit 1 || true
grep -q failed_as_expected fail.out""",
                "fail.out records failure; `should-not-print` is absent.",
            ),
        ],
        validation=["lab.sh succeeds", "fail.sh demonstrates set -e behaviour"],
        errors=[
            ("unbound variable", "`set -u` + missing var", "Initialise variables or use defaults"),
            ("Permission denied", "Not executable", "`chmod +x`"),
        ],
        challenge="Add argument parsing (`$1`) with a usage message when missing.",
        outcomes=["Shipped an executable script", "Verified fail-fast behaviour"],
        cleanup="rm -f fail.sh fail.out\n# Keep lab.sh/out for review",
    )


def _python(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    return LabSpec(
        objective=f"Implement a small Python program that exercises **{title}** with tests or assertions.",
        prerequisites=["Python 3.10+"],
        environment="Local virtualenv optional; stdlib preferred for labs.",
        scenario=f"A service stub needs **{title}** implemented with a regression check before CI turns red.",
        tasks=[
            Task(
                "Implement module and run it",
                "Keep the example tiny but real — importable and runnable.",
                f"""cat > app.py << 'EOF'
\"\"\"Lab module for: {title}\"\"\"

def answer() -> str:
    return "ok"

if __name__ == "__main__":
    print(answer())
EOF
python3 app.py | tee out.txt
test "$(cat out.txt)" = 'ok'""",
                "Prints `ok`.",
            ),
            Task(
                "Add a failing-fast test",
                "Automate the check you would run in CI.",
                """cat > test_app.py << 'EOF'
from app import answer

def test_answer():
    assert answer() == "ok"
EOF
python3 -m pip install -q pytest
python3 -m pytest -q | tee pytest.txt""",
                "pytest reports passed tests.",
            ),
        ],
        validation=["app.py runs", "pytest passes"],
        errors=[
            ("ModuleNotFoundError", "Wrong cwd", "Run from the lab directory"),
            ("pytest not found", "Missing install", "`python3 -m pip install pytest`"),
        ],
        challenge="Add type hints and run `python3 -m compileall`.",
        outcomes=["Built runnable Python", "Automated verification"],
        cleanup="# Keep app/tests; remove .pytest_cache if desired",
    )


def _networking(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    return LabSpec(
        objective=f"Capture real network evidence for **{title}** using modern CLI tools.",
        prerequisites=["iproute2/`ip`/`ss` preferred", "Optional: dig/curl"],
        environment="Local host networking. Prefer inspection over changing firewall rules.",
        scenario=f"Users report timeouts related to **{title}**. You collect path/DNS/socket evidence before changing security groups.",
        tasks=[
            Task(
                "Interface and route inventory",
                "Know the data path before blaming the application.",
                """ip -br a | tee addrs.txt 2>/dev/null || ifconfig | tee addrs.txt
ip route | tee routes.txt 2>/dev/null || netstat -rn | tee routes.txt
ss -lntu | head -n 30 | tee listeners.txt 2>/dev/null || true""",
                "addrs/routes/listeners evidence files populated.",
            ),
            Task(
                "DNS and HTTP probe",
                "Separate DNS failure from TCP/HTTP failure.",
                """getent hosts example.com | tee dns.txt || dig example.com +short | tee dns.txt
curl -sI https://example.com | head -n 8 | tee http.txt || true
test -s dns.txt""",
                "dns.txt has an address; http.txt shows headers if network allows.",
            ),
        ],
        validation=["Evidence files exist", "You can explain address vs route vs listener"],
        errors=[
            ("Network unreachable", "No default route / VPN", "Check `ip route` and interface state"),
            ("NXDOMAIN", "DNS misconfig", "Check resolver in `/etc/resolv.conf` or platform DNS"),
        ],
        challenge="Traceroute/MTR to a known host and attach the output to `path.txt`.",
        outcomes=["Collected network forensics", "Separated DNS from transport symptoms"],
        cleanup="# Inspection-only — keep evidence files",
    )


def _generic(slug: str, title: str, lab_dir: str, headings: list[str]) -> LabSpec:
    hint = headings[0] if headings else title
    return LabSpec(
        objective=f"Produce a working, verifiable artefact that demonstrates **{title}**.",
        prerequisites=["Shell access", "Tools listed in the tutorial Prerequisites"],
        environment=f"Workspace `{lab_dir}`. Prefer local/sandbox tooling.",
        scenario=f"You must operationalise **{hint}** for a delivery team with evidence, not slides.",
        tasks=[
            Task(
                "Create the working artefact",
                "Encode the topic as files/commands the team can rerun.",
                f"""tee README-LAB.md << 'EOF'
# {title}
Implement the Theory workflow here with real commands.
EOF
date -u +%Y-%m-%dT%H:%M:%SZ | tee started.txt
# Topic commands belong here — prefer tools from the tutorial Theory section.
ls -la | tee listing.txt""",
                "started.txt and listing.txt exist.",
            ),
            Task(
                "Prove success with an assertion",
                "Every lab needs a binary pass/fail check.",
                """test -s started.txt && test -s listing.txt
echo PASS | tee result.txt""",
                "`PASS` written to result.txt.",
            ),
        ],
        validation=["result.txt is PASS", "Artefacts committed only if non-secret"],
        errors=[("command not found", "Missing toolchain", "Install prerequisites from the tutorial")],
        challenge="Automate the validation steps in a small `validate.sh` with `set -euo pipefail`.",
        outcomes=["Created runnable lab artefacts", "Verified with an assertion"],
        cleanup="# Remove disposable resources created for this topic",
    )
