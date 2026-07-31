"""Topic-specific Hands-on Lab and Interview Question banks for Jenkins.

Lab bodies use a ``{lab_dir}`` placeholder substituted by ``lab_for``.
"""

from __future__ import annotations


LABS_JENKINS: dict[str, str] = {
    'introduction-to-jenkins-and-ci-cd': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** document CI/CD terms and sketch a controller–agent layout

### Step 1 – Primary exercise

```bash
cat > cicd-notes.md << 'EOF'
# Jenkins CI/CD notes
- CI: build and test every meaningful change
- CD: always releasable; gates decide when to ship
- Controller: schedules, stores JENKINS_HOME
- Agents: execute builds; prefer labels over built-in node
- LTS: production line; pin image tags in Compose
EOF
test -f cicd-notes.md && wc -l cicd-notes.md
```

### Step 2 – Validate your mental model checklist

```bash
grep -E 'Controller|Agents|LTS|CI:' cicd-notes.md
printf '%s\n' "controller=schedule" "agent=execute" "lts=production" > model.txt
cat model.txt
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'installing-jenkins-lts': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** bring up Jenkins LTS with Compose and prove JENKINS_HOME persists

### Step 1 – Primary exercise

```bash
cat > docker-compose.yml << 'EOF'
services:
  jenkins:
    image: jenkins/jenkins:lts
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
    restart: unless-stopped
volumes:
  jenkins_home:
EOF
docker compose up -d
sleep 5
docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Complete the setup wizard in the browser at `http://localhost:8080` (unlock → suggested plugins → admin user → Jenkins URL).

### Step 2 – Prove persistence

```bash
docker compose exec jenkins ls /var/jenkins_home | head
curl -sf -o /dev/null -w "%{http_code}\n" http://localhost:8080/login
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'using-jenkins-jobs-views-and-folders': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** create a folder, a Pipeline job stub, and a list view

### Step 1 – Primary exercise

```bash
# Document UI checklist while controller from module-02 runs
cat > ui-checklist.md << 'EOF'
# Using Jenkins checklist
- [ ] Dashboard loads
- [ ] New Item → Folder `rebash-labs`
- [ ] New Item → Pipeline `hello-pipeline` inside folder
- [ ] Build once; open Console Output
- [ ] Create List View including hello-pipeline
- [ ] Credentials link found under Manage Jenkins (do not store secrets yet)
EOF
# Optional: use jenkins-cli later; for now validate notes
grep -E 'Folder|Pipeline|Credentials' ui-checklist.md
test -f ui-checklist.md
```

### Step 2 – Capture job URL pattern

```bash
cat > url-pattern.txt << 'EOF'
Root job:   /job/hello-pipeline/
Folder job: /job/rebash-labs/job/hello-pipeline/
View:       /view/my-labs/
EOF
cat url-pattern.txt
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'pipeline-fundamentals-declarative': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** author and validate a Declarative Jenkinsfile locally

### Step 1 – Primary exercise

```bash
cat > Jenkinsfile << 'EOF'
pipeline {
  agent any
  options { timestamps() }
  stages {
    stage('Build') {
      steps {
        echo 'Compiling sample'
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
    always {
      echo 'Pipeline finished'
    }
  }
}
EOF
# Local structural checks (controller run optional if module-02 is up)
grep -E 'pipeline|agent|stages|post' Jenkinsfile
test "$(grep -c 'stage(' Jenkinsfile)" -ge 2
```

### Step 2 – Simulate stage commands locally

```bash
mkdir -p dist && echo ok > dist/status.txt
test -f dist/status.txt && grep -q ok dist/status.txt && echo 'local-stages-ok'
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'jenkinsfile-in-scm': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** create a Git repo with Jenkinsfile and validate SCM job settings file

### Step 1 – Primary exercise

```bash
git init -b main
cat > Jenkinsfile << 'EOF'
pipeline {
  agent any
  parameters {
    string(name: 'GREETING', defaultValue: 'hello', description: 'Message')
  }
  environment {
    APP_ENV = 'lab'
  }
  stages {
    stage('Checkout info') {
      steps {
        echo "Greeting=${params.GREETING} env=${env.APP_ENV}"
        sh 'git rev-parse --short HEAD || true'
      }
    }
    stage('Validate') {
      steps {
        sh 'test -f Jenkinsfile'
      }
    }
  }
}
EOF
git add Jenkinsfile && git -c user.email=lab@rebash.local -c user.name=Lab commit -m 'Add Jenkinsfile'
git log -1 --oneline
```

### Step 2 – Record Pipeline from SCM settings

```bash
cat > scm-job-settings.md << 'EOF'
# Pipeline from SCM
- SCM: Git
- Repository URL: (local path or remote)
- Script Path: Jenkinsfile
- Lightweight checkout: enable when definition-only is enough
EOF
grep 'Script Path' scm-job-settings.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'agents-nodes-and-executors': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** document a zero-executor controller policy and labelled agent Pipeline

### Step 1 – Primary exercise

```bash
cat > agent-policy.md << 'EOF'
# Agent policy (lab)
- Built-in node executors: 0 in production
- Required labels: linux, docker
- Pipeline snippet:
  agent { label 'linux' }
- Tools: prefer image-baked JDK/Maven over global auto-install when possible
EOF
cat > Jenkinsfile << 'EOF'
pipeline {
  agent { label 'linux' }
  stages {
    stage('Where am I') {
      steps {
        sh 'uname -a; pwd; echo "Run on labelled agent, not controller"'
      }
    }
  }
}
EOF
grep -E "label|executors|Built-in" agent-policy.md Jenkinsfile
```

### Step 2 – Validate label directive

```bash
grep -A1 'agent' Jenkinsfile
test -f agent-policy.md && echo 'policy-ok'
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'multibranch-pipelines-and-prs': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** simulate Multibranch discovery rules with a local repo layout

### Step 1 – Primary exercise

```bash
mkdir -p branches/main branches/feature-x
cp /dev/null branches/main/Jenkinsfile 2>/dev/null || true
cat > branches/main/Jenkinsfile << 'EOF'
pipeline { agent any; stages { stage('Main') { steps { echo 'main' } } } }
EOF
cat > branches/feature-x/Jenkinsfile << 'EOF'
pipeline { agent any; stages { stage('Feature') { steps { echo 'feature-x' } } } }
EOF
cat > multibranch-plan.md << 'EOF'
# Multibranch plan
- Branch source: Git
- Discover branches: all
- Discover PRs: origin only (lab)
- Orphaned item strategy: discard old items after 7 days
- Trigger: webhook preferred; scan fallback hourly
EOF
find branches -name Jenkinsfile | sort
grep -E 'Discover|Orphaned|webhook' multibranch-plan.md
```

### Step 2 – Validate both branch definitions

```bash
grep -R "stage(" branches/*/Jenkinsfile
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'docker-with-jenkins-pipeline': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Jenkinsfile with docker agent plus local Dockerfile build proof

### Step 1 – Primary exercise

```bash
cat > Dockerfile << 'EOF'
FROM python:3.12-alpine
WORKDIR /app
COPY app.py .
USER nobody
CMD ["python", "app.py"]
EOF
echo 'print("hello from jenkins docker lab")' > app.py
cat > Jenkinsfile << 'EOF'
pipeline {
  agent {
    docker {
      image 'python:3.12-alpine'
      args '-u root:root'
    }
  }
  stages {
    stage('Test') {
      steps {
        sh 'python -c "print(1+1)"'
      }
    }
    stage('Image build note') {
      steps {
        echo 'On a Docker-capable agent: docker build -t rebash/lab:${BUILD_NUMBER} .'
      }
    }
  }
}
EOF
docker build -t rebash/jenkins-lab:local .
docker run --rm rebash/jenkins-lab:local
grep -A3 'docker {' Jenkinsfile
```

### Step 2 – Credential hygiene note

```bash
cat > registry-notes.md << 'EOF'
# Registry
- Store username/password or token as Jenkins credentials
- Use withRegistry / withCredentials in Pipeline
- Tag with Git SHA; avoid latest for prod
EOF
grep credentials registry-notes.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'shared-libraries': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** scaffold a shared library vars/ step and a consuming Jenkinsfile

### Step 1 – Primary exercise

```bash
mkdir -p library/vars app
cat > library/vars/sayHello.groovy << 'EOF'
def call(String name = 'world') {
  echo "Hello, ${name}."
}
EOF
cat > app/Jenkinsfile << 'EOF'
@Library('rebash-lib@main') _
pipeline {
  agent any
  stages {
    stage('Greet') {
      steps {
        script { sayHello('rebash') }
      }
    }
  }
}
EOF
cat > library-notes.md << 'EOF'
# Register in Jenkins
- Name: rebash-lib
- Default version: main (pin tags in prod)
- Modern SCM: Git repo URL to library/
EOF
find library app -type f | sort
grep Library app/Jenkinsfile
```

### Step 2 – Sanity-check vars script

```bash
grep -E 'call|echo' library/vars/sayHello.groovy
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'managing-jenkins-plugins-tools-and-cli': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** script plugin inventory notes and CLI usage checklist

### Step 1 – Primary exercise

```bash
cat > manage-runbook.md << 'EOF'
# Managing Jenkins runbook
1. Snapshot / volume backup of JENKINS_HOME
2. List plugins (UI or CLI list-plugins)
3. Apply updates on TEST controller first
4. Safe restart in change window
5. Smoke: login, trigger known Pipeline, check agent
EOF
cat > cli-notes.md << 'EOF'
# Jenkins CLI
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth user:token help
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth user:token list-plugins | head
# Create API token under user configure — never commit it
EOF
grep -E 'Safe restart|list-plugins|Snapshot' manage-runbook.md cli-notes.md
```

### Step 2 – Tools block example

```bash
cat > tools-Jenkinsfile.snippet << 'EOF'
pipeline {
  agent { label 'linux' }
  tools { jdk 'jdk17' }
  stages { stage('V') { steps { sh 'java -version' } } }
}
EOF
grep jdk tools-Jenkinsfile.snippet
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'securing-jenkins': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** write a security checklist and unsafe-vs-safe Jenkinsfile snippets

### Step 1 – Primary exercise

```bash
cat > security-checklist.md << 'EOF'
# Jenkins security checklist
- [ ] No public signup
- [ ] Authz not "Anyone can do anything"
- [ ] CSRF protection enabled
- [ ] Built-in executors = 0
- [ ] Secrets only in Credentials store
- [ ] Admin via SSO/LDAP where possible
- [ ] Untrusted PRs without deploy credentials
EOF
cat > bad-vs-good.md << 'EOF'
Bad:  sh 'curl -u admin:password https://registry/...'
Good: withCredentials([...]) { sh 'echo $TOKEN | docker login ...' }
EOF
grep -E 'CSRF|Credentials|Anyone' security-checklist.md bad-vs-good.md
```

### Step 2 – Confirm checklist coverage

```bash
test "$(grep -c '\- \[ \]' security-checklist.md)" -ge 6 && echo 'checklist-ok'
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'testing-reports-and-quality-gates': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** generate JUnit XML and a Pipeline that publishes and gates

### Step 1 – Primary exercise

```bash
mkdir -p reports
cat > reports/TEST-sample.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="sample" tests="2" failures="0" errors="0" skipped="0">
  <testcase classname="demo.A" name="ok"/>
  <testcase classname="demo.B" name="also_ok"/>
</testsuite>
EOF
cat > Jenkinsfile << 'EOF'
pipeline {
  agent any
  stages {
    stage('Unit') {
      steps {
        sh 'mkdir -p reports && cp reports/TEST-sample.xml reports/ 2>/dev/null || true'
        sh 'test -f reports/TEST-sample.xml'
      }
    }
    stage('Quality gate') {
      steps {
        junit 'reports/TEST-*.xml'
      }
    }
    stage('Deploy') {
      when { expression { currentBuild.currentResult == 'SUCCESS' } }
      steps { echo 'Deploy would run only if tests passed' }
    }
  }
}
EOF
# Local proof without controller junit step:
xmllint --noout reports/TEST-sample.xml 2>/dev/null || python3 -c "import xml.etree.ElementTree as E; E.parse('reports/TEST-sample.xml'); print('junit-xml-ok')"
grep -E 'junit|Quality gate|Deploy' Jenkinsfile
```

### Step 2 – Parallel sketch

```bash
cat > parallel-snippet.txt << 'EOF'
parallel unit: { stage('Unit') { steps { sh 'echo unit' } } },
         lint: { stage('Lint') { steps { sh 'echo lint' } } }
EOF
grep parallel parallel-snippet.txt
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'kubernetes-agents-and-deploys': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** validate Pod template YAML and a deploy Pipeline stub (cluster optional)

### Step 1 – Primary exercise

```bash
cat > pod-template.yaml << 'EOF'
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-agent
  containers:
    - name: jnlp
      image: jenkins/inbound-agent:latest
    - name: kubectl
      image: bitnami/kubectl:latest
      command: ['cat']
      tty: true
EOF
cat > Jenkinsfile << 'EOF'
pipeline {
  agent {
    kubernetes {
      yamlFile 'pod-template.yaml'
    }
  }
  stages {
    stage('Build') {
      steps { sh 'echo build in pod' }
    }
    stage('Deploy') {
      steps {
        container('kubectl') {
          sh 'kubectl -n lab apply -f k8s/ || echo "cluster optional in lab"'
        }
      }
    }
  }
}
EOF
mkdir -p k8s
cat > k8s/deploy.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: demo }
spec:
  replicas: 1
  selector: { matchLabels: { app: demo } }
  template:
    metadata: { labels: { app: demo } }
    spec:
      containers:
        - name: demo
          image: hashicorp/http-echo:1.0
          args: ["-text=hello"]
EOF
# Validate YAML locally if kubectl available
kubectl apply --dry-run=client -f k8s/deploy.yaml 2>/dev/null || python3 -c "import yaml,sys; yaml.safe_load(open('pod-template.yaml')); yaml.safe_load(open('k8s/deploy.yaml')); print('yaml-ok')" 2>/dev/null || echo 'yaml-files-present'
test -f pod-template.yaml && test -f Jenkinsfile
```

### Step 2 – RBAC note

```bash
cat > rbac-notes.md << 'EOF'
# Least privilege
- Role: get/list/watch/create/update/patch on deployments, services in lab ns
- Avoid cluster-admin in Jenkins credentials
- Separate PR CI credentials from prod deploy
EOF
grep cluster-admin rbac-notes.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'terraform-pipelines-in-jenkins': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** Terraform plan-only Pipeline files with local backend for lab

### Step 1 – Primary exercise

```bash
cat > main.tf << 'EOF'
terraform {
  required_version = ">= 1.5.0"
}
resource "null_resource" "lab" {
  triggers = { always = timestamp() }
}
EOF
cat > Jenkinsfile << 'EOF'
pipeline {
  agent any
  parameters {
    booleanParam(name: 'DO_APPLY', defaultValue: false, description: 'Lab only')
  }
  stages {
    stage('Init') { steps { sh 'terraform init -input=false' } }
    stage('Validate') { steps { sh 'terraform validate' } }
    stage('Plan') {
      steps {
        sh 'terraform plan -input=false -out=tfplan'
        archiveArtifacts artifacts: 'tfplan', fingerprint: true
      }
    }
    stage('Apply') {
      when { expression { return params.DO_APPLY == true } }
      steps { sh 'terraform apply -input=false tfplan' }
    }
  }
}
EOF
terraform init -input=false
terraform validate
terraform plan -input=false -out=tfplan
test -f tfplan && echo 'plan-ok'
grep -E 'Plan|DO_APPLY|archiveArtifacts' Jenkinsfile
```

### Step 2 – Destroy discipline note

```bash
cat > destroy-policy.md << 'EOF'
# Destroy
- Never auto-destroy production
- Lab: explicit parameter + confirmation input
- Prefer terraform destroy in disposable workspaces only
EOF
grep production destroy-policy.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'jcasc-scaling-and-operations': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** author a minimal JCasC snippet and backup checklist

### Step 1 – Primary exercise

```bash
cat > jenkins.yaml << 'EOF'
jenkins:
  systemMessage: "REBASH Jenkins lab — managed with JCasC"
  numExecutors: 0
  remotingSecurity:
    enabled: true
unclassified:
  location:
    url: "http://localhost:8080/"
EOF
cat > ops-checklist.md << 'EOF'
# Ops checklist
- CASC_JENKINS_CONFIG points at jenkins.yaml
- numExecutors on controller: 0
- Daily volume snapshot + monthly restore drill
- Prometheus/metrics endpoint scraped (when enabled)
- Folder per team with scoped credentials
EOF
grep -E 'numExecutors|systemMessage' jenkins.yaml
grep -E 'snapshot|Folder|CASC' ops-checklist.md
```

### Step 2 – Validate YAML shape

```bash
python3 -c "import yaml; d=yaml.safe_load(open('jenkins.yaml')); assert d['jenkins']['numExecutors']==0; print('jcasc-ok')" 2>/dev/null || (grep -q 'numExecutors: 0' jenkins.yaml && echo 'jcasc-ok')
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
    'troubleshooting-and-upgrades': '''Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

**Focus:** triage a broken Jenkinsfile and draft an LTS upgrade runbook

### Step 1 – Primary exercise

```bash
cat > Jenkinsfile.broken << 'EOF'
pipeline {
  agent any
  stages {
    stage('Oops') {
      steps {
        sh 'exit 1'
      }
    }
  }
}
EOF
cat > Jenkinsfile.fixed << 'EOF'
pipeline {
  agent any
  stages {
    stage('Ok') {
      steps {
        sh 'echo healthy; exit 0'
      }
    }
  }
}
EOF
# Local triage simulation
bash -c 'sh -c "exit 1"' || echo "captured-failure-exit-$?"
diff -u Jenkinsfile.broken Jenkinsfile.fixed || true
cat > upgrade-runbook.md << 'EOF'
# LTS upgrade runbook
1. Read upgrade guide for target LTS
2. Snapshot volume / backup JENKINS_HOME
3. Upgrade TEST controller; run smoke Pipelines
4. Change window: upgrade PROD; safe restart
5. Smoke: login, agent, sample Multibranch, deploy dry-run
6. Rollback: restore snapshot if smoke fails
EOF
grep -E 'Snapshot|Rollback|TEST' upgrade-runbook.md
```

### Step 2 – Support bundle note

```bash
cat > support-notes.md << 'EOF'
# When asking for help
- Jenkins version (LTS)
- Plugin list excerpt
- Sanitised console log
- Whether still reproducible after replay
# Prefer support/admin monitors over pasting secrets
EOF
grep version support-notes.md
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-jenkins/ for later tutorials
```
''',
}


IQ_JENKINS: dict[str, str] = {
    'introduction-to-jenkins-and-ci-cd': '''1. What is the difference between Continuous Integration and Continuous Delivery?
2. What does the Jenkins controller store, and what should agents do instead?
3. Why prefer Jenkins LTS over weekly releases in production?
4. When would you choose Jenkins over a SaaS CI product?
5. What is an executor, and how does it relate to a node?

!!! tip "Sample answer — question 2"
    The controller holds `JENKINS_HOME` (jobs, plugins, credentials metadata, build history). Agents provide workspaces and toolchains so build code does not run on the control plane.

!!! tip "Sample answer — question 3"
    LTS is the supported production line with fewer breaking plugin churn cycles. Weeklies are for earlier features; validate them on a non-production controller.
''',
    'installing-jenkins-lts': '''1. What is `JENKINS_HOME` and why must it be persisted?
2. How do you unlock a fresh Jenkins controller?
3. Why pin `jenkins/jenkins:lts` instead of `latest`?
4. Which ports does a typical Docker Jenkins expose and why?
5. What does the setup wizard configure beyond plugins?

!!! tip "Sample answer — question 1"
    `JENKINS_HOME` holds jobs, plugins, credentials metadata, and build history. Without a volume or disk, every container recreate is a factory reset.

!!! tip "Sample answer — question 3"
    `latest` can jump major lines unexpectedly. LTS (or a specific LTS tag/digest) keeps upgrades intentional and testable.
''',
    'using-jenkins-jobs-views-and-folders': '''1. When would you still see Freestyle jobs in an enterprise?
2. How do folders help multi-team Jenkins controllers?
3. Where should credentials live instead of job shell steps?
4. What does build history give you during an incident?
5. What is the difference between a view and a folder?

!!! tip "Sample answer — question 2"
    Folders namespace jobs, can hold folder credentials and library config, and make authorization matrices manageable per team.

!!! tip "Sample answer — question 3"
    Use Manage Jenkins → Credentials (or folder credentials) and reference credential IDs from Pipeline steps such as `withCredentials`.
''',
    'pipeline-fundamentals-declarative': '''1. What are the required top-level sections of a Declarative Pipeline?
2. How does Declarative differ from Scripted Pipeline?
3. What is the purpose of the `post` block?
4. Why is Pipeline-as-code preferable to Freestyle for teams?
5. Where do you look up parameters for a Pipeline step?

!!! tip "Sample answer — question 1"
    At minimum: `pipeline { agent …; stages { … } }`. Most production files also use `options`, `environment`, and `post`.

!!! tip "Sample answer — question 5"
    Use the job’s Pipeline Syntax snippet generator and the online Pipeline Steps reference on jenkins.io.
''',
    'jenkinsfile-in-scm': '''1. Why store the Jenkinsfile in SCM instead of the job config?
2. What is Script Path in a Pipeline from SCM job?
3. How should secrets be handled in a Jenkinsfile?
4. What are parameters useful for?
5. How does a root Jenkinsfile help Multibranch later?

!!! tip "Sample answer — question 1"
    SCM storage makes Pipeline changes reviewable, branchable, and recoverable — the same as application code.

!!! tip "Sample answer — question 3"
    Store secret material in the Jenkins Credentials store; bind with `withCredentials` or dedicated steps; commit only credential IDs.
''',
    'agents-nodes-and-executors': '''1. Why set the built-in node’s executors to zero?
2. What is a label and how does a Pipeline select it?
3. How do executors affect throughput?
4. Inbound versus SSH agents — what differs?
5. When do global tool installations hurt more than they help?

!!! tip "Sample answer — question 1"
    So untrusted build steps cannot run on the controller host that holds `JENKINS_HOME` and credential material.

!!! tip "Sample answer — question 2"
    Labels are tags on nodes; `agent { label 'docker' }` schedules only matching agents.
''',
    'multibranch-pipelines-and-prs': '''1. What problem does Multibranch Pipeline solve?
2. What is branch indexing?
3. How should fork pull requests be treated for secrets?
4. When do you use an Organization Folder?
5. Webhook versus poll SCM — which do you prefer and why?

!!! tip "Sample answer — question 1"
    It automatically creates and maintains per-branch (and optionally per-PR) Pipeline jobs from Jenkinsfiles in SCM.

!!! tip "Sample answer — question 3"
    Treat fork PRs as untrusted: limited credentials, no deploy secrets, or disable fork discovery.
''',
    'docker-with-jenkins-pipeline': '''1. How does `agent { docker { … } }` differ from building an image in a stage?
2. What is the main risk of mounting the host Docker socket?
3. How should registry credentials be supplied to Pipeline?
4. Why pin image tags or digests?
5. When might you choose Kaniko or Buildah over docker CLI?

!!! tip "Sample answer — question 2"
    Socket access is effectively host-level Docker control — any Pipeline can start privileged containers or mount host paths.

!!! tip "Sample answer — question 3"
    Use the Credentials store and binding steps; never commit registry passwords in the Jenkinsfile.
''',
    'shared-libraries': '''1. What belongs in `vars/` versus `src/`?
2. How do you pin a shared library version?
3. Global versus folder library — when each?
4. Why is a shared library a trust boundary?
5. How do you test a library change safely?

!!! tip "Sample answer — question 2"
    Use `@Library('name@1.4.0') _` (tag) or a commit hash; avoid relying on mutable defaults for prod.

!!! tip "Sample answer — question 4"
    Library code runs inside Pipelines that may have credentials — treat library Git write access like prod code ownership.
''',
    'managing-jenkins-plugins-tools-and-cli': '''1. What is the difference between safe restart and reload configuration?
2. How do you roll out plugin updates safely?
3. What does the Pipeline `tools` directive expect to be configured?
4. How do you authenticate Jenkins CLI?
5. Why minimise installed plugins?

!!! tip "Sample answer — question 1"
    Reload re-reads certain config from disk without a full JVM bounce; safe restart drains executors then restarts Jenkins.

!!! tip "Sample answer — question 2"
    Backup, update on a test controller, read plugin changelogs, then change production in a window with smoke tests.
''',
    'securing-jenkins': '''1. Authentication versus authorisation in Jenkins?
2. Where should secrets live?
3. Why keep CSRF enabled?
4. How do you limit Multibranch PR access to credentials?
5. Which controller hardening steps would you verify first on an unknown instance?

!!! tip "Sample answer — question 2"
    In the Credentials store (global or folder), referenced by ID from Pipeline — never in Jenkinsfile plaintext.

!!! tip "Sample answer — question 5"
    Signup disabled, authz strategy, CSRF on, built-in executors, plugin currency, and whether the UI is exposed without TLS.
''',
    'testing-reports-and-quality-gates': '''1. What does the `junit` step give you beyond console output?
2. How do you stop a deploy when tests fail in Declarative Pipeline?
3. When is `parallel` appropriate?
4. Why publish HTML reports as artefacts?
5. What is a quality gate in a CI/CD Pipeline?

!!! tip "Sample answer — question 1"
    It records pass/fail trends, flaky visibility, and fails the build on test failures according to options.

!!! tip "Sample answer — question 5"
    A policy checkpoint — tests, coverage, or scans must pass before promotion/deploy stages run.
''',
    'kubernetes-agents-and-deploys': '''1. What advantage do ephemeral Kubernetes agents provide?
2. What is a Pod template in Jenkins?
3. How do you limit deploy permissions from Pipeline?
4. How do you roll back a bad Deployment?
5. Why separate CI and deploy credential sets?

!!! tip "Sample answer — question 1"
    Clean, scalable agents that match queue demand and avoid long-lived VM drift.

!!! tip "Sample answer — question 3"
    Namespace-scoped Roles, dedicated ServiceAccounts, and credentials only on trusted jobs.
''',
    'terraform-pipelines-in-jenkins': '''1. Why separate plan and apply stages?
2. What belongs in remote state configuration?
3. How do you prevent two applies at once?
4. How should cloud credentials be provided to Jenkins?
5. What is dangerous about auto-apply on every PR?

!!! tip "Sample answer — question 1"
    So humans (or policy) review the plan artefact before mutating infrastructure; apply uses the same binary plan.

!!! tip "Sample answer — question 3"
    Remote state locking (for example S3+DynamoDB, Terraform Cloud, or equivalent) serialises applies.
''',
    'jcasc-scaling-and-operations': '''1. What problem does JCasC solve?
2. What must a backup of Jenkins include?
3. Why set controller executors to zero in JCasC?
4. How do folders support multi-team governance?
5. What signals would you monitor on a Jenkins controller?

!!! tip "Sample answer — question 1"
    It versions and re-applies controller configuration so rebuilds and peer review replace click-ops drift.

!!! tip "Sample answer — question 2"
    At minimum `JENKINS_HOME` (config, jobs, plugins, credentials ciphertext) plus a tested restore path; agree retention for build artefacts.
''',
    'troubleshooting-and-upgrades': '''1. How do you triage a red Pipeline build?
2. When is Pipeline replay appropriate?
3. How do you isolate a bad plugin update?
4. What is your LTS upgrade checklist?
5. Agent offline — what do you check first?

!!! tip "Sample answer — question 2"
    Use replay to test a hypothesis quickly, then commit the real fix to SCM; control who has replay permission.

!!! tip "Sample answer — question 4"
    Read the upgrade guide, backup, upgrade test, smoke, production change window, smoke again, keep rollback snapshots.
''',
}


def supported_techs() -> set[str]:
    """Return technology keys supported by this bank module."""
    return {"jenkins"}


def lab_for(tech: str, slug: str, title: str, lab_dir: str) -> str | None:
    """Return a Hands-on Lab markdown body for ``tech``/``slug``, or None."""
    if tech != "jenkins":
        return None
    body = LABS_JENKINS.get(slug)
    if body is None:
        return None
    _ = title
    return body.replace("{lab_dir}", lab_dir)


def interview_for(tech: str, slug: str, title: str) -> str | None:
    """Return Interview Questions markdown body for ``tech``/``slug``, or None."""
    if tech != "jenkins":
        return None
    _ = title
    return IQ_JENKINS.get(slug)
