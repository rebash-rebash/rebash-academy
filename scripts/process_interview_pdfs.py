#!/usr/bin/env python3
"""Extract, categorize, dedupe interview Q&A from inbox/interview-pdfs/."""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

import fitz
import yaml

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "inbox" / "interview-pdfs"
OUT_DIR = ROOT / "inbox" / "interview-extracted"
OCR_DIR = OUT_DIR / "ocr"
REGISTRY = ROOT / "docs" / "_curriculum" / "interview-question-registry.yaml"
INTERVIEW_DIR = ROOT / "docs" / "interview"

TOPIC_KEYWORDS: dict[str, tuple[str, ...]] = {
    "linux": (
        "linux",
        "systemd",
        "inode",
        "chmod",
        "selinux",
        "journalctl",
        "kernel",
        "lvm",
        "filesystem",
        "process",
        "nice ",
        "ulimit",
        "cron",
        "ssh ",
        "package manager",
        "yum",
        "apt ",
        "rhel",
        "ubuntu",
    ),
    "shell": (
        "shell",
        "bash",
        "script",
        "awk",
        "sed ",
        "grep",
        "pipe",
        "redirect",
        "shebang",
        "exit code",
    ),
    "networking": (
        "network",
        "dns",
        "tcp",
        "udp",
        "http",
        "https",
        "subnet",
        "cidr",
        "vlan",
        "firewall",
        "load balanc",
        "osi ",
        "routing",
        "nat ",
        "vpn",
        "ssl",
        "tls",
        "latency",
        "bandwidth",
        "port ",
        "socket",
        "coredns",
        "ingress",
    ),
    "python": ("python", "pip ", "virtualenv", "pytest", "django", "flask", "boto3"),
    "git": (
        "git ",
        "github",
        "gitlab",
        "merge",
        "rebase",
        "branch",
        "commit",
        "pull request",
        "source code management",
        "version control",
    ),
    "docker": (
        "docker",
        "container",
        "dockerfile",
        "image layer",
        "compose",
        "cgroup",
        "namespace",
        "registry",
        "volume",
    ),
    "kubernetes": (
        "kubernetes",
        "k8s",
        "pod ",
        "pods",
        "deployment",
        "service mesh",
        "kubelet",
        "etcd",
        "helm",
        "taint",
        "tolerat",
        "namespace",
        "configmap",
        "secret",
        "statefulset",
        "daemonset",
        "hpa",
        "ingress",
        "cni",
        "kubectl",
    ),
    "aws": (
        "aws",
        "ec2",
        "s3",
        "iam",
        "vpc",
        "lambda",
        "cloudformation",
        "eks",
        "rds",
        "route 53",
        "cloudwatch",
        "elb",
        "alb",
        "asg",
        "security group",
    ),
    "azure": (
        "azure",
        "aks",
        "entra",
        "active directory",
        "blob storage",
        "azure devops",
        "resource group",
    ),
    "gcp": ("gcp", "google cloud", "gke", "cloud run", "bigquery", "gcp "),
    "terraform": (
        "terraform",
        "iac",
        "infrastructure as code",
        "state file",
        "terraform import",
        "provider",
        "module",
        "opentofu",
    ),
    "ansible": ("ansible", "playbook", "inventory", "idempoten", "galaxy", "chef", "puppet"),
    "jenkins": ("jenkins", "pipeline as code", "jenkinsfile", "groovy", "agent ", "freestyle"),
    "github-actions": ("github actions", "workflow", "actions/", "gha"),
    "gitlab": ("gitlab ci", "gitlab-ci", ".gitlab-ci", "gitlab runner"),
    "argocd": ("argo", "gitops", "argocd"),
    "helm": ("helm", "chart.yaml", "values.yaml", "helm chart"),
    "cicd": (
        "ci/cd",
        "continuous integration",
        "continuous delivery",
        "continuous deployment",
        "pipeline",
        "blue green",
        "canary",
        "maven",
        "nexus",
        "sonarqube",
        "trivy",
        "selenium",
    ),
    "monitoring": (
        "prometheus",
        "grafana",
        "elk",
        "elasticsearch",
        "logstash",
        "kibana",
        "nagios",
        "monitoring",
        "logging",
        "alert",
        "observability",
        "opentelemetry",
        "jaeger",
    ),
    "security": (
        "security",
        "devsecops",
        "vulnerability",
        "rbac",
        "least privilege",
        "secret",
        "owasp",
        "scan",
        "compliance",
    ),
    "devops": (
        "devops",
        "agile",
        "sre",
        "sla",
        "slo",
        "error budget",
        "culture",
        "shift left",
    ),
}

# Prefer more specific topics when scores tie.
TOPIC_PRIORITY = [
    "argocd",
    "helm",
    "github-actions",
    "gitlab",
    "jenkins",
    "kubernetes",
    "docker",
    "terraform",
    "ansible",
    "aws",
    "azure",
    "gcp",
    "monitoring",
    "security",
    "python",
    "git",
    "networking",
    "shell",
    "linux",
    "cicd",
    "devops",
]

NOISE_Q = re.compile(
    r"(?i)^(page\s+\d+|prepared by|table of contents|section\s+\d+|module\s+\d+)",
)


def pdf_text(path: Path) -> str:
    doc = fitz.open(path)
    try:
        return "\n".join(page.get_text("text") for page in doc)
    finally:
        doc.close()


def clean_ws(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalize_question(q: str) -> str:
    q = q.lower().strip()
    q = re.sub(r"[^a-z0-9\s\?\-/]", " ", q)
    q = re.sub(r"\s+", " ", q).strip(" ?")
    # collapse near-duplicates like "what is docker" / "what is a docker"
    q = re.sub(r"\b(a|an|the)\b", "", q)
    q = re.sub(r"\b(how does it differ|how is it different|difference between)\b", "differ", q)
    q = re.sub(r"\b(virtual machine|vm)\b", "vm", q)
    q = re.sub(r"\s+", " ", q).strip()
    # Keep only first 12 significant tokens for near-dup matching
    tokens = [t for t in q.split() if t not in {"and", "or", "to", "of", "in", "on", "for", "with"}]
    return " ".join(tokens[:12])


def question_id(topic: str, question: str) -> str:
    digest = hashlib.sha1(normalize_question(question).encode()).hexdigest()[:10]
    slug = re.sub(r"[^a-z0-9]+", "-", normalize_question(question)[:48]).strip("-")
    return f"{topic}-{slug}-{digest}"


def classify(question: str, answer: str) -> str:
    q = question.lower()
    a = answer.lower()[:500]  # only lead of answer — avoids cross-topic drift
    # Hard overrides from the question stem
    hard = [
        ("kubernetes", ("kubernetes", "k8s", "kubectl", "kubelet", "etcd")),
        ("docker", ("docker", "dockerfile", "compose")),
        ("terraform", ("terraform",)),
        ("ansible", ("ansible", "playbook")),
        ("jenkins", ("jenkins", "jenkinsfile")),
        ("github-actions", ("github actions",)),
        ("argocd", ("argo cd", "argocd", "gitops")),
        ("helm", ("helm",)),
    ]
    for topic, keys in hard:
        if any(k in q for k in keys):
            return topic

    scores: dict[str, int] = {}
    for topic, keys in TOPIC_KEYWORDS.items():
        score = 0
        for key in keys:
            if key in q:
                score += 6 * q.count(key)
            if key in a:
                score += a.count(key)
        if score:
            scores[topic] = score
    if not scores:
        return "devops"
    best = max(scores.values())
    candidates = [t for t, s in scores.items() if s == best]
    for topic in TOPIC_PRIORITY:
        if topic in candidates:
            return topic
    return candidates[0]


def rewrite_answer(answer: str) -> str:
    """Light editorial pass toward REBASH voice (not a full rewrite)."""
    text = clean_ws(answer)
    text = re.sub(r"(?i)^ans(?:wer)?\s*:\s*", "", text)
    text = re.sub(r"(?m)^(Prepared by|Page \d+|CHAPTER\s+\d+.*|SECTION\s+\d+.*).*$", "", text)
    text = re.sub(r"(?i)\bCHAPTER\s+\d+[:\.]?[^\n]*", " ", text)
    text = re.sub(r"(?i)\bSECTION\s+\d+[:\.]?[^\n]*", " ", text)
    # Cut answer if a new chapter banner appears mid-body
    text = re.split(r"(?i)\bCHAPTER\s+\d+", text)[0].strip()
    # Drop ASCII art / table scaffolding that OCR-ish PDFs inject
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if re.fullmatch(r"[+\-|=\s]+", s):
            continue
        if s.count("|") >= 3 and len(s) < 80:
            continue
        lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    # Keep answers usable but trim extreme length
    if len(text) > 1100:
        text = text[:1080].rsplit(" ", 1)[0] + "…"
    # British spellings for common US forms in this corpus
    replacements = {
        " favor ": " favour ",
        " organize": " organise",
        " optimization": " optimisation",
        " optimized": " optimised",
        " behavior": " behaviour",
        " center": " centre",
        " color": " colour",
    }
    low = f" {text} "
    for a, b in replacements.items():
        low = low.replace(a, b)
        low = low.replace(a.title(), b.title())
    return low.strip()


def clean_question(question: str) -> str:
    q = clean_ws(question)
    q = re.sub(r"^\[(?:Beginner|Intermediate|Advanced|Expert)\]\s*", "", q, flags=re.I)
    q = re.sub(r"\s+", " ", q).strip()
    # Join broken stems like "writing one for a" + next line often in answer
    return q


def extract_qnum_dot(text: str) -> list[tuple[str, str]]:
    """Q1. question / answer blocks (Ankit + Docker PDF + Mastery)."""
    # Join Q1.\nWhat... into one line-friendly stream
    text = re.sub(r"(?m)^(Q\d+)\.\s*\n", r"\1. ", text)
    parts = re.split(r"(?m)^(Q\d+)\.\s+", text)
    items: list[tuple[str, str]] = []
    # parts: [preamble, num, body, num, body, ...]
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1].strip()
        if not body:
            continue
        # Question is first sentence/line; answer is rest
        m = re.match(r"(.+?\?)\s*(.*)", body, re.S)
        if m:
            q, a = m.group(1).strip(), m.group(2).strip()
        else:
            lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
            if not lines:
                continue
            # Multi-line stem without '?': take lines until Answer:/Ans: or long prose
            q_lines = []
            rest_idx = 0
            for idx, ln in enumerate(lines):
                if re.match(r"(?i)^(ans(?:wer)?\s*:|in my experience|yes[,.]|no[,.])", ln):
                    rest_idx = idx
                    break
                q_lines.append(ln)
                rest_idx = idx + 1
                # Stop if we already have a solid stem and next line looks like answer prose
                joined = " ".join(q_lines)
                if len(joined) > 140 and idx + 1 < len(lines) and len(lines[idx + 1]) > 80:
                    break
            if not q_lines:
                continue
            q = " ".join(q_lines)
            a = "\n".join(lines[rest_idx:])
            # Recover truncated stems: "for a" / "for an" often continue in answer first words
            if re.search(r"\bfor an?$", q, re.I) and a:
                first = a.splitlines()[0].strip()
                # pull short continuation phrase before Answer:
                cont = re.split(r"(?i)^(?:ans(?:wer)?\s*:)", first)[0].strip()
                if 3 < len(cont) < 80 and not cont.endswith("."):
                    q = f"{q} {cont}".strip()
                    a = "\n".join(a.splitlines()[1:]).strip() or a
        q = clean_question(q)
        a = re.sub(r"(?i)^ans(?:wer)?\s*:\s*", "", a).strip()
        if len(q) < 12 or len(a) < 40:
            continue
        if NOISE_Q.search(q):
            continue
        # Drop broken truncated questions
        if q.endswith((" for a", " for an", " for", " and", " the", " a", " an")):
            continue
        items.append((q, a))
    return items


def extract_qnum_space(text: str) -> list[tuple[str, str]]:
    """Q1 Question (Arvind 303 guide — Qn then question on same/next lines)."""
    text = re.sub(r"(?m)^(Q\d+)\s*\n", r"\1 ", text)
    parts = re.split(r"(?m)^(Q\d+)\s+", text)
    items: list[tuple[str, str]] = []
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1].strip()
        if not body:
            continue
        m = re.match(r"(.+?\?)\s*(.*)", body, re.S)
        if m:
            q, a = m.group(1).strip(), m.group(2).strip()
        else:
            lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
            if len(lines) < 2:
                continue
            q, a = lines[0], "\n".join(lines[1:])
        # Strip page footers
        a = re.sub(r"(?m)^Prepared by.*$", "", a)
        a = re.sub(r"(?m)^Page \d+.*$", "", a)
        a = clean_ws(a)
        if len(q) < 8 or len(a) < 25:
            continue
        if NOISE_Q.search(q):
            continue
        items.append((q, a))
    return items


def extract_numbered_answer(text: str) -> list[tuple[str, str]]:
    """1. Question\\nAnswer: ... (cheat sheet + top 100)."""
    text = re.sub(r"(?m)^(Answer|Ans)\s*:\s*", r"ANSWER: ", text)
    # Split on numbered questions that look like interview stems
    parts = re.split(
        r"(?m)^(\d+)\.\s+(?=(?:What|How|Why|When|Where|Which|Can|Do|Is|Are|Explain|Difference|Compare|Define|Describe|List|Name|If |Tell))",
        text,
    )
    items: list[tuple[str, str]] = []
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1].strip()
        m = re.match(r"(.+?\?)\s*(?:ANSWER:\s*)?(.*)", body, re.S)
        if not m:
            continue
        q, a = m.group(1).strip(), clean_ws(m.group(2))
        a = re.sub(r"(?i)^answer\s*:\s*", "", a)
        # Cut next section headers that leaked
        a = re.split(r"(?m)^\d+\.\s+[A-Z]", a)[0].strip()
        if len(q) < 8 or len(a) < 20:
            continue
        items.append((q, a))
    return items


PARSERS = {
    "1783358005276.pdf": extract_qnum_dot,
    "1784196457523.pdf": extract_numbered_answer,
    "1784431820463.pdf": extract_numbered_answer,
    "1785077379612.pdf": extract_qnum_space,
    "1786378433442.pdf": extract_qnum_dot,
    "1786456624707.pdf": extract_qnum_dot,
}


def extract_paren_num(text: str) -> list[tuple[str, str]]:
    """(1) What is ... —> answer (handwritten OCR)."""
    parts = re.split(r"(?m)^\(?\s*(\d{1,3})\s*\)\s+", text)
    items: list[tuple[str, str]] = []
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1].strip()
        m = re.match(r"(.+?\?)\s*(.*)", body, re.S)
        if not m:
            continue
        q, a = clean_question(m.group(1)), clean_ws(m.group(2))
        a = re.sub(r"^[\->—–\s]+", "", a)
        a = re.sub(r"(?m)^\(?\d{1,3}\)\s+.*", "", a)
        if len(q) < 12 or len(a) < 30:
            continue
        items.append((q, a))
    return items


def extract_q_ans_labels(text: str) -> list[tuple[str, str]]:
    """Q: ... ANS: ... (production scenario OCR)."""
    parts = re.split(r"(?m)(?:^|\s)[Qq]\s*:\s+", text)
    items: list[tuple[str, str]] = []
    for body in parts[1:]:
        m = re.match(
            r"(.+?)(?:\?|(?=\s*INTERVIEWER)|(?=\s*ANS\s*:)|(?=\s*Answer\s*:))",
            body,
            re.S | re.I,
        )
        if not m:
            continue
        q = clean_question(m.group(1))
        if not q.endswith("?"):
            q = q.rstrip(". ") + "?"
        rest = body[m.end() :]
        am = re.search(r"(?i)ANS(?:WER)?\s*:\s*(.*)", rest, re.S)
        if not am:
            continue
        a = am.group(1)
        a = re.split(r"(?m)(?:^|\s)[Qq]\s*:\s+", a)[0]
        a = re.sub(r"(?i)INTERVIEWER LOOKS FOR:.*", "", a)
        a = clean_ws(a)
        if len(q) < 20 or len(a) < 40:
            continue
        items.append((q, a))
    return items


def extract_numbered_answer_ocr(text: str) -> list[tuple[str, str]]:
    """1) What is Jenkins? Answer: ..."""
    parts = re.split(r"(?m)^\s*(\d{1,2})\)\s+", text)
    items: list[tuple[str, str]] = []
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1].strip()
        m = re.match(r"(.+?\?)\s*(.*)", body, re.S)
        if not m:
            continue
        q = clean_question(m.group(1))
        a = m.group(2)
        a = re.sub(r"(?i)^(answer|ans)\s*:?\s*", "", a.strip())
        a = re.split(r"(?m)^\s*\d{1,2}\)\s+", a)[0]
        a = clean_ws(a)
        if len(q) < 12 or len(a) < 40:
            continue
        items.append((q, a))
    return items


def extract_interview_answer_blocks(text: str) -> list[tuple[str, str]]:
    """Slide OCR: question lines then INTERVIEW ANSWER."""
    parts = re.split(r"(?i)INTERVIEW ANSWER", text)
    items: list[tuple[str, str]] = []
    for i in range(len(parts) - 1):
        before = parts[i]
        after = parts[i + 1]
        # last question-like sentence before ANSWER
        q_candidates = re.findall(
            r"(?:What|How|Why|Difference|Explain|When|Which)[^\n?]{8,160}\??",
            before,
            flags=re.I,
        )
        if not q_candidates:
            continue
        q = clean_question(q_candidates[-1])
        if not q.endswith("?"):
            q += "?"
        a = re.split(r"(?i)(?:SHEL|DEVOPS INTERVIEW|Slide\s+\d)", after)[0]
        a = clean_ws(a)
        if len(q) < 12 or len(a) < 40:
            continue
        items.append((q, a))
    return items


OCR_SOURCES = {
    "100 DevOps Engineer Interview Questions and Answers - Handwritten Notes.txt": extract_paren_num,
    "1784874876936.txt": extract_q_ans_labels,
    "1786289541473.txt": extract_numbered_answer_ocr,
    # 1786416024802.txt is a duplicate of 178628 — skipped
    "PptxGenJS Presentation.txt": extract_interview_answer_blocks,
}


def _ingest_pairs(source: str, pairs: list[tuple[str, str]], records: list[dict]) -> int:
    kept = 0
    for q, a in pairs:
        topic = classify(q, a)
        q = clean_question(q)
        a = rewrite_answer(a)
        if len(q) < 12 or len(a) < 40:
            continue
        if q.endswith((" for a", " for an", " for", " and", " the")):
            continue
        records.append(
            {
                "source": source,
                "topic": topic,
                "question": q,
                "answer": a,
                "norm": normalize_question(q),
            }
        )
        kept += 1
    return kept


def extract_all() -> list[dict]:
    records: list[dict] = []
    for pdf_name, parser in PARSERS.items():
        path = PDF_DIR / pdf_name
        if not path.is_file():
            print(f"skip missing {pdf_name}")
            continue
        text = clean_ws(pdf_text(path))
        if len(text) < 500:
            print(f"skip empty/scan {pdf_name}")
            continue
        pairs = parser(text)
        kept = _ingest_pairs(pdf_name, pairs, records)
        print(f"{pdf_name}: extracted {len(pairs)} kept {kept}")

    for ocr_name, parser in OCR_SOURCES.items():
        path = OCR_DIR / ocr_name
        if not path.is_file():
            print(f"skip missing OCR {ocr_name}")
            continue
        text = clean_ws(path.read_text(encoding="utf-8", errors="ignore"))
        pairs = parser(text)
        kept = _ingest_pairs(f"ocr:{ocr_name}", pairs, records)
        print(f"OCR {ocr_name}: extracted {len(pairs)} kept {kept}")
    return records


def dedupe(records: list[dict]) -> list[dict]:
    best: dict[str, dict] = {}
    for rec in records:
        key = rec["norm"]
        if not key or len(key) < 10:
            continue
        prev = best.get(key)
        if not prev or len(rec["answer"]) > len(prev["answer"]):
            best[key] = rec
    return list(best.values())


def md_escape_indent(text: str, spaces: int = 4) -> str:
    pad = " " * spaces
    lines = text.splitlines() or [""]
    return "\n".join(pad + (line if line else "") for line in lines)


TOPIC_META = {
    "linux": ("Linux", "linux", "material/linux", "../linux/index.md"),
    "shell": ("Shell", "shell", None, "../shell/index.md"),
    "networking": ("Networking", "networking", None, "../networking/index.md"),
    "python": ("Python", "python", None, "../python/index.md"),
    "git": ("Git", "git", None, "../git/index.md"),
    "docker": ("Docker", "docker", "docker.svg", "../docker/index.md"),
    "kubernetes": ("Kubernetes", "kubernetes", "kubernetes.svg", "../kubernetes/index.md"),
    "aws": ("AWS", "aws", "aws.svg", "../aws/index.md"),
    "azure": ("Azure", "azure", "azure.svg", None),
    "gcp": ("Google Cloud", "gcp", "google-cloud.svg", "../gcp/index.md"),
    "terraform": ("Terraform", "terraform", "terraform.svg", "../terraform/index.md"),
    "ansible": ("Ansible", "ansible", None, "../ansible/index.md"),
    "jenkins": ("Jenkins", "jenkins", None, "../jenkins/index.md"),
    "github-actions": ("GitHub Actions", "github-actions", None, "../github-actions/index.md"),
    "gitlab": ("GitLab CI/CD", "gitlab", "gitlab.svg", "../gitlab/index.md"),
    "argocd": ("Argo CD", "argocd", None, "../argocd/index.md"),
    "helm": ("Helm", "helm", None, "../helm/index.md"),
    "cicd": ("CI/CD", "cicd", None, None),
    "monitoring": ("Monitoring & Observability", "monitoring", None, None),
    "security": ("Security & DevSecOps", "security", None, None),
    "devops": ("DevOps Fundamentals", "devops", None, None),
}

# Cap published questions per topic to keep pages interview-useful (not encyclopedias).
TOPIC_CAPS = {
    "devops": 40,
    "linux": 50,
    "shell": 35,
    "networking": 45,
    "python": 35,
    "git": 40,
    "docker": 50,
    "kubernetes": 60,
    "aws": 50,
    "azure": 35,
    "gcp": 30,
    "terraform": 40,
    "ansible": 40,
    "jenkins": 45,
    "github-actions": 35,
    "gitlab": 30,
    "argocd": 30,
    "helm": 30,
    "cicd": 40,
    "monitoring": 40,
    "security": 40,
}


def score_record(rec: dict) -> int:
    """Prefer scenario/troubleshooting depth over one-liners."""
    q = rec["question"].lower()
    a = rec["answer"]
    score = min(len(a), 800)
    for token in ("how would", "troubleshoot", "production", "scenario", "fail", "debug", "design"):
        if token in q:
            score += 120
    if len(a) < 80:
        score -= 200
    return score


def render_topic_page(topic: str, records: list[dict]) -> str:
    title, tech, _brand, track = TOPIC_META[topic]
    records = sorted(records, key=score_record, reverse=True)
    cap = TOPIC_CAPS.get(topic, 40)
    records = records[:cap]
    today = "2026-08-12"
    desc = (
        f"{len(records)} curated interview questions and model answers for {title} — "
        "concepts, scenarios, troubleshooting, and production trade-offs."
    )
    related = []
    if track:
        related.append(f"- Course: [{title}]({track})")
    related.append("- Hub: [Interview Preparation](index.md)")

    # Group roughly
    concept, scenario, other = [], [], []
    for rec in records:
        ql = rec["question"].lower()
        if any(x in ql for x in ("how would", "troubleshoot", "debug", "fail", "incident", "production")):
            scenario.append(rec)
        elif any(x in ql for x in ("what is", "what are", "explain", "difference", "define")):
            concept.append(rec)
        else:
            other.append(rec)

    def section(name: str, items: list[dict], start: int) -> tuple[str, int]:
        if not items:
            return "", start
        lines = [f"## {name}", ""]
        n = start
        for rec in items:
            n += 1
            lines.append(f"**{n}. {rec['question']}**")
            lines.append("")
            lines.append('??? success "Reveal answer"')
            lines.append(md_escape_indent(rec["answer"]))
            lines.append("")
        return "\n".join(lines), n

    body_parts = []
    n = 0
    for heading, items in (
        ("Core concepts", concept),
        ("Scenarios and troubleshooting", scenario),
        ("Practice questions", other),
    ):
        chunk, n = section(heading, items, n)
        if chunk:
            body_parts.append(chunk)

    fm = f"""---
title: "{title} Interview Preparation"
description: "{desc}"
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "{today}"
category: interview
technology: {tech}
tags:
  - interview
  - {tech}
comments: false
---

"""
    # Wrap body in Jinja raw so Ansible/GitHub Actions examples with {{{{ }}}}
    # do not break mkdocs-macros.
    body = f"""{{% raw %}}
# {title} Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

{chr(10).join(body_parts)}
## Related

{chr(10).join(related)}
{{% endraw %}}
"""
    return fm + body


def write_registry(published: list[dict]) -> None:
    payload = {
        "version": 1,
        "updated": "2026-08-12",
        "topics": sorted(TOPIC_META.keys()),
        "question_count": len(published),
        "questions": [
            {
                "id": question_id(r["topic"], r["question"]),
                "topic": r["topic"],
                "question": r["question"],
                "aliases": [],
                "source": f"pdf:{r['source']}",
                "status": "published",
            }
            for r in sorted(published, key=lambda x: (x["topic"], x["norm"]))
        ],
    }
    REGISTRY.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw = extract_all()
    (OUT_DIR / "raw.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
    unique = dedupe(raw)
    (OUT_DIR / "unique.json").write_text(json.dumps(unique, indent=2), encoding="utf-8")
    print(f"raw={len(raw)} unique={len(unique)}")

    by_topic: dict[str, list[dict]] = defaultdict(list)
    for rec in unique:
        by_topic[rec["topic"]].append(rec)

    published_all: list[dict] = []
    counts = {}
    for topic, recs in sorted(by_topic.items()):
        if topic not in TOPIC_META:
            continue
        cap = TOPIC_CAPS.get(topic, 40)
        chosen = sorted(recs, key=score_record, reverse=True)[:cap]
        counts[topic] = (len(recs), len(chosen))
        page = render_topic_page(topic, chosen)
        out = INTERVIEW_DIR / f"{topic}.md"
        out.write_text(page, encoding="utf-8")
        published_all.extend(chosen)
        print(f"wrote {out.relative_to(ROOT)} unique={len(recs)} published={len(chosen)}")

    write_registry(published_all)
    summary = {
        "raw": len(raw),
        "unique": len(unique),
        "published": len(published_all),
        "by_topic": {k: {"unique": v[0], "published": v[1]} for k, v in counts.items()},
        "ocr_sources": sorted(OCR_SOURCES.keys()),
        "skipped_scans": sorted(
            p.name
            for p in PDF_DIR.glob("*.pdf")
            if p.name not in PARSERS
            and f"{p.stem}.txt" not in OCR_SOURCES
            and p.stem != "1786416024802"  # duplicate of 1786289541473
        ),
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
