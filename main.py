"""Macros for REBASH Academy (mkdocs-macros)."""

import os
import re

import material

ICON_ROOT = os.path.join(os.path.dirname(material.__file__), "templates", ".icons")

# Technology id -> (label, icon, brand colour). Icons come from the bundled
# Material / Simple Icons sets so roadmaps always use real brand logos.
TECH = {
    "linux": ("Linux", "material/linux", "#333333"),
    "shell": ("Shell Scripting", "material/console", "#4eaa25"),
    "python": ("Python for DevOps", "material/language-python", "#3776ab"),
    "networking": ("Networking", "material/lan", "#607d8b"),
    "git": ("Git", "material/git", "#f05032"),
    "docker": ("Docker", "material/docker", "#2496ed"),
    "kubernetes": ("Kubernetes", "material/kubernetes", "#326ce5"),
    "helm": ("Helm", "simple/helm", "#0f1689"),
    "gitlab": ("GitLab CI/CD", "material/gitlab", "#fc6d26"),
    "github-actions": ("GitHub Actions", "simple/githubactions", "#2088ff"),
    "jenkins": ("Jenkins", "simple/jenkins", "#d24939"),
    "argocd": ("Argo CD", "simple/argo", "#ef7b4d"),
    "terraform": ("Terraform", "simple/terraform", "#7b42bc"),
    "ansible": ("Ansible", "simple/ansible", "#ee0000"),
    "aws": ("AWS", "material/aws", "#ff9900"),
    "azure": ("Azure", "material/microsoft-azure", "#0078d4"),
    "gcp": ("Google Cloud", "material/google-cloud", "#4285f4"),
    "prometheus": ("Prometheus", "simple/prometheus", "#e6522c"),
    "grafana": ("Grafana", "simple/grafana", "#f46800"),
    "loki": ("Loki", "material/text-search", "#f46800"),
    "tempo": ("Tempo", "material/chart-timeline-variant", "#f46800"),
    "opentelemetry": ("OpenTelemetry", "simple/opentelemetry", "#f5a800"),
    "devsecops": ("DevSecOps", "material/shield-lock", "#6a1b9a"),
    "security": ("Security", "material/security", "#c62828"),
    "platform-engineering": ("Platform Engineering", "material/layers-triple", "#3949ab"),
    "sre": ("Site Reliability Engineering", "material/speedometer", "#00acc1"),
    "architecture": ("Cloud Architecture", "material/sitemap", "#455a64"),
    "ai": ("AI for DevOps", "material/robot", "#7c4dff"),
    "monitoring": ("Monitoring", "material/chart-line", "#43a047"),
}


def _icon_svg(name: str) -> str:
    path = os.path.join(ICON_ROOT, *name.split("/")) + ".svg"
    with open(path, encoding="utf-8") as handle:
        svg = handle.read().strip()
    return re.sub(r"<svg ", '<svg aria-hidden="true" ', svg, count=1)


def define_env(env):
    @env.macro
    def roadmap(steps, prefix="../../"):
        """Render a serpentine technology roadmap (prefix = relative path to docs root)."""
        items = []
        for step in steps:
            label, icon, colour = TECH[step]
            items.append(
                "<li>"
                f'<a class="ra-roadmap__node" href="{prefix}{step}/">'
                f'<span class="rebash-roadmap__card ra-roadmap__circle" style="color:{colour}">'
                f"{_icon_svg(icon)}</span>"
                f'<span class="ra-roadmap__label">{label}</span>'
                "</a>"
                "</li>"
            )
        return (
            '<div class="ra-roadmap">'
            '<div class="rebash-roadmap__canvas">'
            '<svg class="rebash-roadmap__path" viewBox="0 0 100 100" '
            'preserveAspectRatio="none" aria-hidden="true">'
            '<path class="rebash-roadmap__stroke" d=""></path>'
            '<path class="rebash-roadmap__dash" d=""></path>'
            "</svg>"
            f'<ol class="rebash-roadmap__stops ra-roadmap__steps">{"".join(items)}</ol>'
            "</div>"
            "</div>"
        )

    @env.macro
    def course_flow(stages):
        """Render a course-flow stepper. stages = [[badge, [topic, ...]], ...]."""
        rows = []
        for badge, topics in stages:
            chips = '<span class="ra-flow__arrow" aria-hidden="true">›</span>'.join(
                f'<span class="ra-flow__chip">{topic}</span>' for topic in topics
            )
            rows.append(
                '<li class="ra-flow__stage">'
                f'<span class="ra-flow__badge">{badge}</span>'
                f'<span class="ra-flow__chips">{chips}</span>'
                "</li>"
            )
        return (
            '<div class="ra-flow" markdown="0">'
            f'<ol class="ra-flow__stages">{"".join(rows)}</ol>'
            "</div>"
        )
