---
title: "Jenkins Interview Preparation"
description: "70 curated Jenkins interview prompts — model answers plus real interview questions collected across companies (deduplicated by topic)."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: jenkins
tags:
  - interview
  - jenkins
comments: false
---

{% raw %}
# Jenkins Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is User Administration in Jenkins?**

??? success "Reveal answer"
    In Jenkins, we can create users, groups and assign limited privileges to them for better control. Users
    access Jenkins as a user — we can't assign permissions directly to users. Instead we create 'Roles',
    assign permissions to those roles, and attach roles to users so users get the permissions assigned to
    
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    those roles.
    Q100.What is Global tool configuration in Jenkins?
    We install Java, Maven, Git and other tools in our server. By default Jenkins installs them
    automatically every time it needs them — which is not a good practice. Instead, we give the installed
    path of all these tools in Jenkins so it pulls them from the local machine instead of downloading every
    time. This way of giving paths of tools in Jenkins is called 'Global tool configuration'.
    Maven & Build Tools
    Q101.What is Build?
    Build means compiling the source code, assembling all class files and finally creating a deliverable.
    • Compile: Convert source code into machine-readable format
    • Assembly (Linking): Grouping all class files
    • Deliverable: .war,…

**2. What is Jenkins, and why is it used in DevOps?**

??? success "Reveal answer"
    Jenkins is an open-source automation server written in Java. Its primary job is to automate the 
    repetitive parts of software development — specifically building, testing, and deploying code. In 
    the context of DevOps, Jenkins sits at the heart of the CI/CD pipeline (Continuous Integration / 
    Continuous Delivery). 
    Here's how to think about it: Every time a developer pushes code to a repository like GitHub, 
    Jenkins can automatically: 
    1. Pull that code 
    2. Compile or build it 
    3. Run automated tests 
    4. Package it into a deployable artifact (like a Docker image or JAR file) 
    5. Deploy it to a staging or production environment 
    Why this matters: Before CI/CD tools like Jenkins, teams would "integrate" code once a week or 
    once a sprint. By then, hundreds of conflicting changes had piled up, causing what developers 
    call "integration hell." Jenkins solves this by integrating continuously — every commit, every day. 
    In an interview, say something like this: 
    
     
    "Jenkins is an automation server that enables Continuous Integration and Continuous Delivery. We 
    use it…

**3. What is a Jenkinsfile, and why should it be stored in version control?**

??? success "Reveal answer"
    A Jenkinsfile is a text file that contains the definition of a Jenkins pipeline. Instead of configuring 
    your pipeline through the Jenkins web UI (which is fragile, hard to audit, and doesn't survive 
    server crashes), you define your entire pipeline as code in a file called Jenkinsfile and commit it 
    to your repository. 
    Basic Jenkinsfile example (Declarative syntax): 
    pipeline { 
     agent any 
     environment { 
     APP_NAME = 'my-web-app' 
     DOCKER_IMAGE = "myregistry/${APP_NAME}:${BUILD_NUMBER}" 
     } 
     stages { 
     stage('Checkout') { 
     steps { 
     git branch: 'main', url: 'https://github.com/myorg/my-web-
    app.git' 
     } 
     } 
     stage('Build') { 
    
     
     steps { 
     sh 'mvn clean package -DskipTests' 
     } 
     } 
     stage('Test') { 
     steps { 
     sh 'mvn test' 
     } 
     post { 
     always { 
     junit 'target/surefire-reports/*.xml' 
     } 
     } 
     } 
     stage('Docker Build & Push') { 
     steps { 
     script { 
     docker.build(DOCKER_IMAGE) 
     docker.withRegistry('https://myregistry', 'docker-
    credentials') { 
     docker.image(DOCKER_IMAGE).push() 
     } 
     } 
     } 
     } 
     stage('Deploy to Staging') { 
     steps { 
     sh "kubectl set…

**4. Explain the difference between Declarative and Scripted pipelines in Jenkins.**

??? success "Reveal answer"
    Jenkins supports two syntaxes for writing pipelines, and understanding when to use each is a sign
    of real-world experience.
    Declarative Pipeline: Introduced in Jenkins 2.x, this is the recommended approach for most
    teams. It has a rigid, opinionated structure that enforces best practices and is easier to read.
    pipeline {
    agent any
    stages {
    stage('Build') {
    steps {
    sh 'make build'
    }
    }
    }
    }
    
    Key characteristics:
    •
    Must start with the pipeline block
    •
    Has predefined sections: agent, stages, steps, post
    •
    Built-in validation — Jenkins will tell you if the structure is wrong
    •
    Supports when conditions, parallel stages, input steps natively
    •
    Easier for beginners
    Scripted Pipeline: The older format, based on Apache Groovy. It gives you full programmatic
    control but at the cost of complexity.
    node {
    stage('Build') {
    sh 'make build'
    }
    stage('Test') {
    try {
    sh 'make test'
    } catch (e) {
    currentBuild.result = 'FAILURE'
    throw e
    }
    }
    }
    Key characteristics:
    •
    Starts with node block
    •
    Full Groovy programming — loops, conditionals, functions, classes
    •
    No structural validation —…

**5. What are Jenkins Agents/Nodes, and how do they work in a distributed build environment?**

??? success "Reveal answer"
    By default, Jenkins runs on a single server called the Master (now called the Controller in newer 
    Jenkins terminology). For small teams, this is fine. But in production environments, you almost 
    always need multiple agents for: 
    • 
    Running builds in parallel 
    • 
    Using different operating systems (Linux agent for building, Windows agent for .NET) 
    • 
    Isolating sensitive workloads 
    • 
    Scaling build capacity 
    How it works: 
    The Jenkins Controller manages the overall orchestration — it reads the Jenkinsfile, schedules 
    jobs, and records results. The actual build work happens on Agents (also called Nodes or 
    Workers). Agents connect to the controller via JNLP (Java Web Start) or SSH. 
    Jenkins Controller 
     |--- Agent 1 (Linux, 8 CPU) — runs Java builds 
    
     
     |--- Agent 2 (Linux, 16 CPU) — runs Docker builds 
     |--- Agent 3 (Windows) — runs .NET builds 
     |--- Agent 4 (macOS) — runs iOS builds 
    In your Jenkinsfile, you target specific agents using labels: 
    pipeline { 
     agent none // No global agent - each stage defines its own 
     stages { 
     stage('Build Java') { 
     agent {…

**6. When you deploy Jenkins with Helm, what is the folder structure?**

??? success "Reveal answer"
    A Helm chart typically includes:
    Chart.yaml
    values.yaml
    templates/
     deployment.yaml
     service.yaml
     ingress.yaml
     configmap.yaml
     pvc.yaml
    charts/
    README.md
     8. How much time will be taken for a Jenkins job 
    completion?
    ANSWER: Depends on pipeline stages, application build time, tests, and infra speed. 
    
    Typically ranges from 1 minute to 15+ minutes depending on the 
    complexity.
     9. Where do you deploy the microservices?
    ANSWER: Usually deployed in:
    •
    Kubernetes (EKS)
    •
    Docker containers
    •
    ECS
    •
    EC2
    •
    Fargate
     10. Who manages the infrastructure in your 
    organization?
    ANSWER: Infrastructure is usually managed by the DevOps Team using IaC tools 
    like Terraform, CloudFormation, and Ansible.
     11. Application deployed in EKS but not 
    accessible externally — how will you debug?
    Steps:

**7. Explain your Jenkins Pipeline Key Points : GA. thsights Mpaing Plate’: ) in your current project. OE eee |e As Se Answer : ' 6 ez | oe : | @ Maven Build Push Code Jenkins Maven Run In my current project, whenever developers ay Triggers Build Build Ths push code to the Git repository, Jenkins | © Selenium Automation automatically checks out the code, builds @ Allure Re ports L r the project using Maven, runs Selenium | Sy & | tests, generates Allure reports, sends © Email Notifications QO sac = email notifications, and deploys to the | @ Deployment to QA Allure Email Deploy to | QA environment if all tests pass. \ ages Nosifeatis Oh Sener SS EE". @ How do you run Selenium —_Key Points : QA_Insights Example Flow : tests in Jenkins?**

??? success "Reveal answer"
    a ——— Y Job Configuration ® > M > TestNG > Q > &)
    wer : A
    
    — en Chiomciett Git Maven TestNGxml Allure Email
    
    I configure the Jenkins job, pull the code Y Dependency Setup (Maven) | Checkout Clean Test Execution Report Team
    
    from Git, install dependencies using Y Execute TestNG Suite cnatiecsie aeasgoocneeastastsmstsae
    
    , Maven, execute the TestNG test suite, P- Coincabe Mura Rept | Artifacts Archived :
    generate Allure reports, archive the ; ? | N N N \
    artifacts for future reference, and SO facie Aasiiacks | (aa) |
    notify the team. ¥ Email Team \ HTML Screenshots Logs ZIP |
    r° | Report Archive ;

**8. What is Jenkins Workflow?**

??? success "Reveal answer"
    We attach Git, Maven, Selenium & Artifactory plugins to Jenkins. Once Developers put code in Git,
    Jenkins pulls that code and sends it to Maven for build. Once build is done, Jenkins pulls the built
    code and sends it to Selenium for testing. Once testing is done, Jenkins sends the code to Artifactory
    as required, and finally delivers the end product to the client (Continuous Delivery) or deploys directly
    into clients' machines.

**9. What is Jenkins Architecture?**

??? success "Reveal answer"
    Jenkins architecture is a Client-Server model. Wherever we install Jenkins, that server is called the
    Jenkins master. We can create slaves as well to distribute server load. Jenkins master randomly
    assigns tasks to slaves. If you want to restrict a job to run on a particular slave, we can do that. We
    can group slaves using 'Labels'.

**10. What are Jenkins agents?**

??? success "Reveal answer"
    How do they work?
    Agents, also called nodes or slaves, are machines configured to execute jobs on behalf of the Jenkins
    controller/master. The controller delegates work to agents, which can run on different platforms, distributing build
    load across multiple machines instead of everything running on the controller.

**11. What are the steps to secure Jenkins?**

??? success "Reveal answer"
    Enable Matrix-based or Role-based access control, run Jenkins behind a secure network with HTTPS, use SSH keys
    for secure communication, install security-relevant plugins like OWASP Dependency-Check, and keep Jenkins and
    all its plugins up to date to avoid known vulnerabilities.

**12. What are the different ways to trigger a build in Jenkins?**

??? success "Reveal answer"
    Manual trigger via "Build Now", triggering through source code changes via Git hooks, a cron schedule for periodic
    builds, webhooks or API calls, and triggering a build after another build completes.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**13. What is a Jenkins pipeline?**

??? success "Reveal answer"
    A Jenkins pipeline is a suite of plugins supporting implementing and integrating continuous delivery pipelines directly
    into Jenkins, letting me define complex build, test, and deployment workflows as code rather than manually
    configured job steps.

**14. What is Jenkins?**

??? success "Reveal answer"
    Why is it used?
    Jenkins is an open-source automation server used primarily for continuous integration and continuous delivery --
    automating build, test, and deployment so bugs are caught early, software quality improves, and delivery time
    shrinks.

**15. What is the difference between a freestyle project and a pipeline project in Jenkins?**

??? success "Reveal answer"
    A Freestyle Project is the basic Jenkins job type for simple tasks like running a shell script or a build step. A Pipeline
    Project defines complex job sequences, orchestrating multiple builds, tests, and deployments across environments
    as code.

**16. What is Blue Ocean in Jenkins?**

??? success "Reveal answer"
    Blue Ocean is a modern, more user-friendly Jenkins interface offering a simplified, visual view of CI/CD pipelines,
    making it easier to understand pipeline flow and troubleshoot failures than the classic Jenkins UI.

**17. What is a Jenkinsfile?**

??? success "Reveal answer"
    A Jenkinsfile is a text file defining a Jenkins pipeline, versioned alongside the code it builds, used to automate build,
    test, and deployment -- written as either a declarative or scripted pipeline.

**18. What is Jenkins Groovy sandbox?**

??? success "Reveal answer"
    A security mechanism that restricts the Groovy code in pipelines from executing dangerous 
    operations. Scripts needing privileged access must be approved by an administrator in "Script 
    Approval."

**19. What is Jenkins Configuration as Code (JCasC)?**

??? success "Reveal answer"
    A plugin that allows the entire Jenkins configuration (credentials, plugins, agents, job definitions) 
    to be defined in YAML and stored in version control. Enables reproducible Jenkins setups.

**20. What are the two types of Jenkins pipelines?**

??? success "Reveal answer"
    Declarative Pipeline, a newer, simpler syntax defined within a pipeline block, and Scripted Pipeline, written in full
    Groovy syntax for more flexibility at the cost of added complexity.

**21. What is the Jenkins Master/Agent architecture?**

??? success "Reveal answer"
    The Master (Controller) manages job scheduling, configuration, and results. Agents execute the 
    actual build steps. The controller should never run builds itself in production.

**22. What is the stash and unstash directive in Jenkins?**

??? success "Reveal answer"
    stash saves files from one stage; unstash retrieves them in another stage or on another agent. 
    Used to pass build artifacts between stages running on different agents.

## Scenarios and troubleshooting

**23. How can you handle failed builds in Jenkins?**

??? success "Reveal answer"
    Configure automatic retries a specified number of times after a failure, set up post-build actions like notifications or
    triggering other jobs on failure, and use conditional logic in pipelines -- like try-catch blocks -- to handle failures
    gracefully instead of letting the whole pipeline crash unhelpfully.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    2
    0
    LINUX FOR DEVOPS

**24. How can you monitor Jenkins logs and troubleshoot issues?**

??? success "Reveal answer"
    Jenkins logs are visible through the UI's "Manage Jenkins" → "System Log" section, individual job-specific logs are in
    each job's build history, and for deeper detail I check the actual server log files on the machine hosting Jenkins.

**25. How do you mark a build as unstable vs failed in Jenkins?**

??? success "Reveal answer"
    currentBuild.result = 'UNSTABLE' marks the build yellow (tests failed but build 
    succeeded). currentBuild.result = 'FAILURE' marks it red. Use error('message') to 
    immediately fail.

## Practice questions

**26. How do you manage secrets and credentials securely in Jenkins?**

??? success "Reveal answer"
    Hardcoding secrets in a Jenkinsfile is one of the most dangerous mistakes in DevOps. Jenkins 
    provides a built-in Credentials Store that encrypts secrets at rest and injects them into pipelines 
    without ever exposing them in logs. 
    Types of credentials Jenkins supports: 
    • 
    Username/Password 
    
     
    • 
    Secret Text (API keys, tokens) 
    • 
    SSH Private Key 
    • 
    Certificate 
    • 
    Docker Hub credentials 
    • 
    AWS access keys 
    Using credentials in a Declarative pipeline: 
    pipeline { 
     agent any 
     environment { 
     // Binds username/password to variables 
     DOCKER_CREDS = credentials('docker-hub-credentials') 
     // DOCKER_CREDS_USR = username 
     // DOCKER_CREDS_PSW = password (masked in logs) 
     } 
     stages { 
     stage('Docker Login') { 
     steps { 
     sh 'echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR 
    --password-stdin' 
     } 
     } 
     stage('Use AWS Credentials') { 
     steps { 
     withCredentials([ 
     string(credentialsId: 'aws-access-key', variable: 
    'AWS_ACCESS_KEY_ID'), 
     string(credentialsId: 'aws-secret-key', variable: 
    'AWS_SECRET_ACCESS_KEY') 
     ]) { 
     sh 'aws s3 ls' // AWS…

**27. How do you implement a Blue-Green deployment strategy using Jenkins?**

??? success "Reveal answer"
    Blue-Green deployment is a release strategy that eliminates downtime by maintaining two 
    identical production environments — "Blue" (current live) and "Green" (new version). Traffic is 
    switched from Blue to Green atomically. If Green has issues, you switch back instantly. 
    Here's a complete Jenkins pipeline implementing Blue-Green on Kubernetes: 
    pipeline { 
    
     
     agent any 
     environment { 
     APP_NAME = 'my-api' 
     DOCKER_IMAGE = "myregistry/${APP_NAME}:${BUILD_NUMBER}" 
     KUBE_NAMESPACE = 'production' 
     } 
     stages { 
     stage('Determine Active Environment') { 
     steps { 
     script { 
     // Check which colour is currently active via the service 
    selector 
     def activeColor = sh( 
     script: "kubectl get service ${APP_NAME} -n 
    ${KUBE_NAMESPACE} -o jsonpath='{.spec.selector.color}'", 
     returnStdout: true 
     ).trim() 
     env.ACTIVE_COLOR = activeColor 
     env.INACTIVE_COLOR = (activeColor == 'blue') ? 
    'green' : 'blue' 
     echo "Active: ${env.ACTIVE_COLOR}, Deploying to: 
    ${env.INACTIVE_COLOR}" 
     } 
     } 
     } 
     stage('Build & Push Docker Image') { 
     steps { 
     sh "docker build -t…

**28. How does GitLab CI/CD work, and how is it different from Jenkins?**

??? success "Reveal answer"
    Answer: 
    GitLab CI/CD is a built-in CI/CD platform tightly integrated with GitLab's repository, issue tracker, 
    and security features. Unlike Jenkins, which requires installation, plugin management, and 
    separate configuration, GitLab CI/CD is configured entirely through a .gitlab-ci.yml file in your 
    repository. 
    Basic .gitlab-ci.yml for a Python application: 
    # Define the stages in order 
    stages: 
     - validate 
     - test 
     - build 
     - deploy 
    # Variables available to all jobs 
    variables: 
     DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA 
     PYTHON_VERSION: "3.11" 
    # Default settings for all jobs 
    default: 
     image: python:3.11-slim 
     before_script: 
     - pip install -r requirements.txt 
    # Stage 1: Validate 
    lint: 
     stage: validate 
     script: 
     - pip install flake8 black 
     - flake8 src/ 
     - black --check src/ 
     rules: 
     - if: '$CI_PIPELINE_SOURCE == "merge_request_event"' 
    security-scan: 
     stage: validate 
     image: python:3.11-slim 
     script: 
    
     
     - pip install bandit 
     - bandit -r src/ -f json -o bandit-report.json 
     artifacts: 
     reports: 
     sast: bandit-report.json…

**29. Key terminology that we use in Jenkins?**

??? success "Reveal answer"
    • Integrate: Combine all code written by developers till some point of time
    • Build: Compile the code and make a small executable package
    • Test: Test in all environments whether the application is working properly
    • Archived: Stored in an artifactory so that in future we may use/deliver again
    • Deliver: Handing the product to Client
    • Deploy: Installing product in client's machines

**30. How to install Jenkins?**

??? success "Reveal answer"
    Ankit Dubey
    
    DevOps Interview Questions & Answers
    • Jenkins can be installed in any OS — we access it only through a web page so the OS doesn't
    matter
    • Choose Long Term Support (LTS) release for production environments; weekly release for testing
    • Java is a pre-requisite to install Jenkins
    • Need to install a web package since Jenkins is accessed through web page only

**31. What do you mean by workspace in Jenkins?**

??? success "Reveal answer"
    The workspace is the location on your computer where Jenkins places all files related to the Jenkins
    project. By default each project or job is assigned a workspace location containing Jenkins-specific
    project metadata, temporary files like logs, and any build artifacts. Jenkins web page acts like a
    window through which we are actually doing work in the workspace.

**32. How many types of configurations in Jenkins?**

??? success "Reveal answer"
    There are 3 types of configurations:
    • Global: Configuration changes applicable to whole Jenkins including jobs and nodes — highest
    priority
    • Job: Configurations applicable to only Jobs (also called projects or items in Jenkins)
    • Node: Configurations applicable to only nodes (also called Slaves — helpers to Jenkins master to
    distribute excessive load)

**33. Why only Jenkins?**

??? success "Reveal answer"
    • Has so many plugins — you can write your own or use community plugins
    • Jenkins is a framework, not just a tool — do whatever you want with plugins
    • Can attach slaves (nodes) to Jenkins master to distribute load
    • Jenkins also acts as a cron server replacement for repeated tasks
    • Can create Labels (groups of slaves) to restrict where projects run

**34. How do you integrate Nexus Repository Manager with Jenkins?**

??? success "Reveal answer"
    Install the Nexus Artifact Uploader plugin, configure Nexus repository settings within the Jenkins job, publish artifacts
    to Nexus via post-build actions after a successful build, and update build tools like Maven in Jenkins to resolve
    dependencies from the Nexus repository.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**35. What do you mean by Plugins in Jenkins?**

??? success "Reveal answer"
    • Nearly everything in Jenkins is a plugin — almost all functionality is provided by plugins
    • Plugins are small libraries that add new abilities to Jenkins and provide integration points to other
    tools
    • Jenkins ships with a small set of default plugins, some of which can be upgraded independently

**36. How do you configure SonarQube in Jenkins?**

??? success "Reveal answer"
    Install the SonarQube Scanner plugin, configure the SonarQube server connection under "Manage Jenkins" →
    "Configure System", add a SonarQube analysis stage to the pipeline using the sonar-scanner command or plugin,
    and configure the pipeline to check and act on the quality gate result.

**37. How does Jenkins achieve Continuous Integration?**

??? success "Reveal answer"
    Jenkins integrates with version control systems like Git, automatically triggering builds and tests whenever changes
    are committed -- running unit tests, static analysis, and deploying if everything passes, with notifications sent to the
    team about build status along the way.

**38. How does Jenkins handle parallel execution in pipelines?**

??? success "Reveal answer"
    The parallel directive lets multiple stages run simultaneously -- for example running unit tests and integration tests
    concurrently instead of sequentially -- which reduces overall build time when those stages don't depend on each
    other.

**39. How can you use Python in Jenkins pipelines?**

??? success "Reveal answer"
    I call Python scripts directly within a pipeline stage using the sh step -- for example sh 'python3 script.py' inside a
    stage block -- to automate testing, packaging, or deployment steps as part of the overall Jenkins pipeline.

**40. How do you parameterize a Jenkins job?**

??? success "Reveal answer"
    parameters { 
     string(name: 'DEPLOY_ENV', defaultValue: 'staging', description: 'Target 
    environment') 
     booleanParam(name: 'SKIP_TESTS', defaultValue: false) 
     choice(name: 'REGION', choices: ['us-east-1', 'ap-south-1']) 
    }

**41. How do you back up Jenkins?**

??? success "Reveal answer"
    Back up the $JENKINS_HOME directory — contains all jobs, configurations, and credentials. Use the 
    ThinBackup or Backup plugins to automate this. Critical 
    subdirectories: jobs/, credentials.xml, config.xml.

**42. How do you configure Jenkins for high availability?**

??? success "Reveal answer"
    Use Jenkins in Active/Standby mode with shared NFS storage for $JENKINS_HOME. Alternatively, 
    use CloudBees Jenkins with HA support or migrate to cloud-native alternatives like Tekton.

**43. How do you integrate SonarQube into Jenkins?**

??? success "Reveal answer"
    Install SonarQube Scanner plugin. Configure the SonarQube server in Manage Jenkins → 
    Configure System. Use withSonarQubeEnv('server-name') wrapper 
    and waitForQualityGate() step.

**44. How do you implement a Canary deployment in Jenkins?**

??? success "Reveal answer"
    Use the input step with metrics check between stages: deploy to 10% of servers, check error 
    rates via curl to monitoring API, if OK proceed with full rollout, otherwise rollback.

**45. How do you manage Jenkins credentials securely?**

??? success "Reveal answer"
    Use Jenkins Credentials Store (Manage Jenkins → Credentials). Reference in pipeline 
    via withCredentials([]) or credentials() binding. Never hardcode secrets in Jenkinsfile.

## Real interview prompts

Additional questions reported from real DevOps / SRE interviews. Company names are omitted — practise these out loud without notes.

- Describe your typical deployment flow and CI/CD workflow. What stages do you define in your Jenkins pipeline, and how do you ensure full quality checks during deployment?
- In a Jenkins pipeline, at which stage would you publish or push artifacts/images to Nexus or Artifactory—pre-build, build, or post-build? Why?
- How do you use Jenkins shared libraries? Explain their typical structure and how they are integrated into your Jenkinsfiles?
- Explain the CI/CD workflow you follow and the kind of pipeline you use. How do you define and invoke pipelines in Jenkins?
- What is the difference between Continuous Delivery and Continuous Deployment, and how do you implement them in Jenkins?
- What if I have 10 FE micro services and 10 BE micro services how do you design the cicd pipeline using jenkins?
- How does authentication happen in Jenkins pipeline to use aws with particular login, if you have 1 logout?
- What kind of applications do you deploy using Jenkins pipelines, and what deployment tools do you use?
- If the Jenkins pipeline runs but the build doesn’t happen, what possible issues could be causing it?
- How do you perform complete backup up of Jenkins including jobs/configurations/authentications,?
- Jenkins – If the controller (master) node goes down, how will you troubleshoot and restore it?
- How would you implement dynamic stages in a Jenkinsfile based on environment variables?
- How do you manage concurrent builds in Jenkins and ensure performance doesn’t degrade?
- Explain how you would set up a multi-branch Jenkins pipeline for a GitHub repository?
- Explain if a standalone Jenkins server setup will work, and what to consider?
- how do you copy the jobs from one jenkins worker node to another worker node?
- What are shared libraries in Jenkins, and how are they written and defined?
- Have you worked on Jenkins as your CI/CD tool, or used others like GitLab?
- How would trigger pipeline B in jenkins automatically after pipeline B?
- Which type of Jenkins File u r using? Can u pls Write a Jenkins File?
- How do you deploy python application on aws using jenkins pipeline?
- Your CI/CD pipeline has failed in jenkins. How do you investigate?
- Write Jenkins script to trigger simultaneous/ parallel execution?
- How do you store sensitive information like passwords in jenkins?
- Q17. If a Jenkins job starts but gets stuck, how do you debug?

## Related

- Course: [Jenkins](../jenkins/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
