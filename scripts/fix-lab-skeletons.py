#!/usr/bin/env python3
"""Remove placeholder Hands-on Lab skeletons and promote real exercises.

Also synthesises topic-relevant labs when only the echo skeleton existed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

SKEL_BLOCK = re.compile(
    r"### Step 1 – Skeleton\n\n"
    r"```bash\n"
    r"cat > lab\.sh << 'EOF'\n"
    r"#!/usr/bin/env bash\n"
    r"(?:set -euo pipefail\n)?"
    r"echo \"[^\"]+\"\n"
    r"EOF\n"
    r"chmod \+x lab\.sh\n"
    r"\./lab\.sh\n"
    r"```\n*",
    re.M,
)

FINAL_LABSH = re.compile(
    r"### Final step – Cleanup note\n\n"
    r"```bash\n"
    r"(?:# Keep[^\n]*\n)?"
    r"(?:# keep[^\n]*\n)?"
    r"\./lab\.sh(?: \|\| true)?\n"
    r"(?:# keep[^\n]*\n)?"
    r"```",
    re.M,
)

STEP_HEAD = re.compile(r"^### Step (\d+) – (.+)$", re.M)


def tech_from_path(path: Path) -> str:
    parts = path.relative_to(DOCS).parts
    return parts[0] if parts else "lab"


def slug_lab_dir(path: Path, tech: str, body: str) -> str:
    m = re.search(r"mkdir -p (~/rebash-[^\s&]+)", body)
    if m:
        return m.group(1)
    # derive from filename
    stem = path.stem.replace("_", "-")
    return f"~/rebash-{tech}/{stem}"


def synthesise_lab(tech: str, title: str, lab_dir: str, theory_hints: str) -> str:
    """Topic-shaped starter labs when Step 2 was empty/weak."""
    t = title.lower()
    hints = (theory_hints or "").lower()

    common_setup = f"mkdir -p {lab_dir} && cd {lab_dir}"

    if tech == "docker":
        return f"""Create a workspace for this tutorial.

```bash
{common_setup}
```

**Focus:** run and inspect containers relevant to {title}

### Step 1 – Run and inspect

```bash
docker run -d --name rebash-lab -p 18080:80 nginx:alpine
docker ps --filter name=rebash-lab
curl -sI http://127.0.0.1:18080 | head -n 5
docker logs rebash-lab 2>&1 | head -n 20
docker inspect rebash-lab --format '{{{{.State.Status}}}}'
```

### Step 2 – Change and verify

```bash
docker exec rebash-lab nginx -v
docker stop rebash-lab
docker rm rebash-lab
docker ps -a --filter name=rebash-lab
```

### Final step – Cleanup note

```bash
docker rm -f rebash-lab 2>/dev/null || true
# Keep ~/rebash-docker/ for later tutorials
```
"""

    if tech == "kubernetes":
        return f"""Create a workspace for this tutorial.

```bash
{common_setup}
```

**Focus:** apply and inspect Kubernetes objects for {title}

### Step 1 – Create a disposable namespace and pod

```bash
kubectl create namespace rebash-lab --dry-run=client -o yaml | tee ns.yaml
kubectl apply -f ns.yaml
kubectl -n rebash-lab run web --image=nginx:alpine --port=80 --restart=Never
kubectl -n rebash-lab get pods -o wide
kubectl -n rebash-lab describe pod web | sed -n '1,40p'
```

### Step 2 – Exercise the topic safely

```bash
kubectl -n rebash-lab get all
kubectl -n rebash-lab logs web --tail=20 || true
kubectl -n rebash-lab delete pod web --wait=false
kubectl delete namespace rebash-lab --wait=false
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Keep ~/rebash-kubernetes/ for later tutorials
```
"""

    if tech == "helm":
        return f"""Create a workspace for this tutorial.

```bash
{common_setup}
```

**Focus:** chart workflow for {title}

### Step 1 – Scaffold and lint a chart

```bash
helm create demo-app
helm lint demo-app
helm template demo-app ./demo-app --debug | sed -n '1,80p'
```

### Step 2 – Install to a lab namespace (local cluster)

```bash
kubectl create namespace rebash-helm --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install demo-app ./demo-app -n rebash-helm --wait --timeout 2m
helm -n rebash-helm list
helm -n rebash-helm get values demo-app
helm -n rebash-helm uninstall demo-app
kubectl delete namespace rebash-helm --ignore-not-found
```

### Final step – Cleanup note

```bash
helm -n rebash-helm uninstall demo-app 2>/dev/null || true
kubectl delete namespace rebash-helm --ignore-not-found
# Keep ~/rebash-helm/ for later tutorials
```
"""

    if tech == "terraform":
        return f"""Create a workspace for this tutorial.

```bash
{common_setup}
```

**Focus:** local Terraform workflow for {title} (no cloud spend)

### Step 1 – Minimal configuration

```bash
cat > main.tf << 'EOF'
terraform {{
  required_version = ">= 1.5.0"
}}

resource "null_resource" "lab" {{
  triggers = {{
    topic = "{title.replace('"', '')}"
  }}
  provisioner "local-exec" {{
    command = "echo lab-ok"
  }}
}}
EOF
terraform init
terraform validate
terraform plan -out=tfplan
```

### Step 2 – Apply, inspect state, destroy

```bash
terraform apply -auto-approve tfplan
terraform state list
terraform show | sed -n '1,40p'
terraform destroy -auto-approve
```

### Final step – Cleanup note

```bash
rm -f tfplan
# Keep ~/rebash-terraform/ for later tutorials; never leave remote state unlocked
```
"""

    if tech in {"gitlab", "github-actions"}:
        runner = "gitlab-ci" if tech == "gitlab" else "github-actions"
        file_name = ".gitlab-ci.yml" if tech == "gitlab" else ".github/workflows/lab.yml"
        if tech == "gitlab":
            pipeline = """cat > .gitlab-ci.yml << 'EOF'
stages: [validate]
validate:
  stage: validate
  image: alpine:3.20
  script:
    - echo "pipeline ok"
    - uname -a
EOF
"""
        else:
            pipeline = """mkdir -p .github/workflows
cat > .github/workflows/lab.yml << 'EOF'
name: lab
on: workflow_dispatch
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "workflow ok"
EOF
"""
        return f"""Create a workspace for this tutorial.

```bash
{common_setup}
git init -q
```

**Focus:** author and validate CI config for {title}

### Step 1 – Write a minimal pipeline

```bash
{pipeline}ls -la
sed -n '1,80p' {file_name}
```

### Step 2 – Static checks before push

```bash
# Syntax / structure sanity (no runner required)
test -s {file_name}
grep -E 'script:|runs-on:|steps:' {file_name}
# When a runner is available, push a branch and confirm the job is green
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-{runner}/ for later tutorials; delete remote test branches when finished
```
"""

    if tech == "aws":
        return f"""Create a workspace for this tutorial.

```bash
{common_setup}
```

**Focus:** read-only AWS CLI checks for {title} (no create unless you intend to pay)

### Step 1 – Identity and region hygiene

```bash
aws sts get-caller-identity
aws configure get region || true
echo "Use a sandbox account. Prefer --dry-run / read-only APIs first."
```

### Step 2 – Topic inspection

```bash
# Adapt to the service in this tutorial — examples:
aws ec2 describe-regions --query 'Regions[].RegionName' --output text | tr '\\t' '\\n' | head
aws s3api list-buckets --query 'Buckets[].Name' --output table 2>/dev/null | head || true
# Document which API maps to the Theory section for: {title}
```

### Final step – Cleanup note

```bash
# Destroy anything you created; leave IAM/roles tagged and time-boxed
# Keep ~/rebash-aws/ notes for later tutorials
```
"""

    if tech == "git":
        return f"""Create a workspace for this tutorial.

```bash
{common_setup}
git init -q
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
```

**Focus:** Git mechanics for {title}

### Step 1 – Seed a tiny repo

```bash
echo '# lab' > README.md
git add README.md
git commit -m 'chore: seed lab'
git status
git log --oneline
```

### Step 2 – Practise the topic

```bash
git switch -c feature/lab
echo 'change' >> README.md
git add README.md
git commit -m 'docs: lab change'
git log --oneline --decorate --graph
git switch -
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials; do not force-push shared remotes from labs
```
"""

    if tech in {"shell", "linux"}:
        safe_title = title.replace("'", "").replace('"', "")
        return f"""Create a workspace for this tutorial.

```bash
{common_setup}
```

**Focus:** practise {title} with inspect → change → verify

### Step 1 – Inspect current state

```bash
pwd
whoami
uname -a
echo "PATH=$PATH"
ls -la
```

### Step 2 – Hands-on for this topic

```bash
cat > practise.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "topic: {safe_title}"
date -u +"utc=%Y-%m-%dT%H:%M:%SZ"
EOF
chmod +x practise.sh
./practise.sh | tee practise.out
test -s practise.out
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-{tech}/ for later tutorials
```
"""

    # generic fallback using theory keywords
    safe = title.replace('"', "")
    return f"""Create a workspace for this tutorial.

```bash
{common_setup}
```

**Focus:** hands-on practice for {title}

### Step 1 – Capture baseline evidence

```bash
date -u +"started=%Y-%m-%dT%H:%M:%SZ" | tee lab-notes.txt
pwd | tee -a lab-notes.txt
echo "Topic: {safe}" | tee -a lab-notes.txt
```

### Step 2 – Core exercise

```bash
# Re-run the commands from the Theory section here until you can explain each output.
# Prefer dry-run / validate / plan modes before any apply or destroy.
test -s lab-notes.txt
```

### Final step – Cleanup note

```bash
# Keep {lab_dir.rsplit('/', 1)[0]}/ for later tutorials; destroy cloud resources you created
```
"""


def renumber_steps(lab: str) -> str:
    idx = 1

    def repl(m: re.Match[str]) -> str:
        nonlocal idx
        name = m.group(2).strip()
        # drop leftover "Skeleton" names
        if name.lower() == "skeleton":
            name = "Core exercise"
        out = f"### Step {idx} – {name}"
        idx += 1
        return out

    # Only renumber ### Step N – ... (not Final step)
    return STEP_HEAD.sub(repl, lab)


def fix_final_cleanup(lab: str, tech: str) -> str:
    replacement = (
        "### Final step – Cleanup note\n\n"
        "```bash\n"
        f"# Keep ~/rebash-{tech}/ for later tutorials; destroy disposable cloud resources from this lab\n"
        "```"
    )
    lab2, n = FINAL_LABSH.subn(replacement, lab)
    if n:
        return lab2
    # Also fix finals that only run ./lab.sh with bash -x
    lab2 = re.sub(
        r"### Final step[^\n]*\n\n```bash\n(?:bash -x \./lab\.sh[^\n]*\n)?(?:\./lab\.sh[^\n]*\n)?(?:# keep[^\n]*\n)?```",
        replacement,
        lab,
        count=1,
        flags=re.M,
    )
    return lab2


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "### Step 1 – Skeleton" not in text and "./lab.sh" not in text:
        return False

    m = re.search(r"(## Hands-on Lab\n)(.*?)(\n## )", text, re.S)
    if not m:
        return False

    prefix, lab, suffix_head = m.group(1), m.group(2), m.group(3)
    tech = tech_from_path(path)
    title_m = re.search(r'(?m)^title:\s*["\']?(.+?)["\']?\s*$', text)
    title = title_m.group(1) if title_m else path.stem
    lab_dir = slug_lab_dir(path, tech, lab)

    original = lab
    lab = SKEL_BLOCK.sub("", lab)
    lab = fix_final_cleanup(lab, tech)

    # If no remaining Step headings with real code, synthesise
    remaining_steps = re.findall(
        r"### Step \d+ – ([^\n]+)\n\n```bash\n(.*?)```", lab, re.S
    )
    real = [
        (n, b)
        for n, b in remaining_steps
        if "echo \"lab" not in b
        and 'echo "lab:' not in b
        and len(b.strip()) > 40
    ]

    if not real:
        theory_m = re.search(r"## Theory\n(.*?)(\n## |\Z)", text, re.S)
        theory = theory_m.group(1) if theory_m else ""
        lab = synthesise_lab(tech, title, lab_dir, theory)
    else:
        lab = renumber_steps(lab)
        # Ensure focus line exists
        if "**Focus:**" not in lab:
            lab = f"**Focus:** hands-on practice for {title}\n\n" + lab.lstrip()

    if lab == original:
        return False

    new_text = text[: m.start(2)] + lab + text[m.end(2) :]
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    skip_roots = {"_curriculum", "includes", "assets"}
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS)
        if rel.parts and rel.parts[0] in skip_roots:
            continue
        try:
            if process_file(path):
                changed += 1
                print(f"fixed: {rel}")
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR {path}: {exc}", file=sys.stderr)
            return 1
    print(f"Updated {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
