# Interview PDF intake

Drop DevOps interview question PDFs here (from the Google Drive collection).

This folder is **source material only** — not published on the site.

## Workflow

1. Download the Drive folder into this directory (keep original filenames).
2. Tell the agent: “Process `inbox/interview-pdfs/`”.
3. We will:
   - Extract questions and answers per PDF
   - Normalise and **deduplicate** against `docs/_curriculum/interview-question-registry.yaml`
   - Map each unique question to a category (Linux, Docker, Kubernetes, …)
   - Merge into `docs/interview/<topic>.md` (or a new topic page)
   - Update the registry so future imports do not repeat questions

## Category map (canonical)

| Category | Page | Notes |
|----------|------|--------|
| Linux | `docs/interview/linux.md` | published |
| Shell / Bash | `docs/interview/shell.md` | published |
| Networking | `docs/interview/networking.md` | published |
| Python | `docs/interview/python.md` | published |
| Git | `docs/interview/git.md` | published |
| Docker | `docs/interview/docker.md` | published |
| Kubernetes | `docs/interview/kubernetes.md` | published |
| AWS | `docs/interview/aws.md` | published |
| Terraform | `docs/interview/terraform.md` | published |
| CI/CD | `docs/interview/cicd.md` | published (GitLab-focused today) |
| GCP | `docs/interview/gcp.md` | create when content arrives |
| Ansible | `docs/interview/ansible.md` | create when content arrives |
| Helm | `docs/interview/helm.md` | create when content arrives |
| Jenkins | `docs/interview/jenkins.md` | create when content arrives |
| GitHub Actions | `docs/interview/github-actions.md` | create when content arrives |
| SRE / Observability | `docs/interview/sre.md` | create when content arrives |
| System Design | `docs/interview/system-design.md` | create when content arrives |
| Behavioral | `docs/interview/behavioral.md` | create when content arrives |

Cross-topic duplicates keep the **best answer** under the most specific category and get a cross-link where useful.
