#!/usr/bin/env python3
"""Generate REBASH Academy Python for DevOps tutorials 1–26 under docs/python/."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "python"
D2_DIR = ROOT / "docs" / "assets" / "d2"
IMG_DIR = ROOT / "docs" / "assets" / "images"
AUTHOR = "Shaik Basha"
DATE = "2026-07-29"

# (num, slug, title, module, difficulty, minutes, diagram, tag_extra, desc, overview, theory, lab_focus)
SPEC: list[tuple] = [
    (
        1,
        "introduction-to-python-for-devops",
        "Introduction to Python for DevOps",
        "Module 1: Foundations for Ops",
        "beginner",
        "35 min",
        "python-intro-devops",
        ["devops", "ops"],
        "Why Python complements Bash for DevOps — structured data, APIs, tests, and packaged CLIs.",
        "Shell launches; Python owns structured data, HTTP clients, and testable automation. This tutorial sets that split.",
        """### Bash versus Python for ops

| Job | Prefer |
|-----|--------|
| Glue one-liners, pipes, cron wrappers | Bash |
| JSON/YAML transforms, APIs, SDKs | Python |
| Packaged CLIs with tests | Python |
| Bootstrap on a minimal image | Bash first |

Python is not a replacement for the shell — it is the next layer when data and failure modes get structured.

### Ops script contract (Python)

1. Documented inputs (CLI args / environment)
2. Explicit side effects (dry-run when mutating)
3. Logging to stderr; machine-readable summaries when needed
4. Non-zero exit on failure (`sys.exit`)
""",
        "fingerprint Python/venv; write a tiny `hello_ops.py` that prints host metadata",
    ),
    (
        2,
        "syntax-essentials-types-control-flow-functions",
        "Syntax Essentials — Types, Control Flow, Functions",
        "Module 1: Foundations for Ops",
        "beginner",
        "50 min",
        "python-syntax-ops",
        ["syntax", "functions"],
        "Enough Python syntax for readable ops automation — types, control flow, and small functions.",
        "Ops scripts need clear branching and pure helpers, not academic Python. Build the minimum fluent surface.",
        """### Types you actually use

`str`, `int`, `bool`, `list`, `dict`, `tuple`, `Path` (later), and `None`. Prefer type hints on public functions.

### Control flow

`if` / `elif` / `else`, `for` over iterables, `while` sparingly, `match` (3.10+) for CLI verbs when helpful.

### Functions for ops

```python
def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)
```

Keep functions small: validate → transform → side effect.
""",
        "type hints; guard clauses; small helpers; match or if for verbs",
    ),
    (
        3,
        "modules-imports-and-project-layout",
        "Modules, Imports, and Project Layout",
        "Module 1: Foundations for Ops",
        "beginner",
        "40 min",
        "python-modules-layout",
        ["modules", "imports"],
        "Structure automation as packages — imports, __main__, and a layout teammates can extend.",
        "A single 800-line script becomes unreviewable. Split into `cli`, `lib`, and fixtures early.",
        """### Layout that scales

```text
tool/
  pyproject.toml
  src/tool/
    __init__.py
    cli.py
    lib/
      logging.py
  tests/
```

### Imports

Prefer absolute imports inside the package. Use `python -m tool.cli` during development. Avoid mutating `sys.path` in production code.

### `__main__`

```python
if __name__ == "__main__":
    raise SystemExit(main())
```
""",
        "create package layout; import a helper; run as module",
    ),
    (
        4,
        "virtual-environments-and-dependency-pinning",
        "Virtual Environments and Dependency Pinning",
        "Module 1: Foundations for Ops",
        "beginner",
        "40 min",
        "python-venv-deps",
        ["venv", "pip", "uv"],
        "Isolate projects with venv and pin dependencies for reproducible ops tooling.",
        "System Python and floating versions break CI overnight. Pin what you ship.",
        """### venv

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Pinning

- `requirements.txt` with `==` pins for simple tools
- Prefer `uv lock` or Poetry lockfiles for apps you maintain
- Never rely on globally installed packages for automation

### Hygiene

Commit lockfiles; document Python version (`requires-python`); keep `.venv` out of git.
""",
        "create venv; pin a package; freeze requirements; verify isolation",
    ),
    (
        5,
        "errors-exceptions-and-logging-for-ops",
        "Errors, Exceptions, and Logging for Ops",
        "Module 1: Foundations for Ops",
        "intermediate",
        "45 min",
        "python-errors-logging",
        ["exceptions", "logging"],
        "Catch the right exceptions, log for operators, and map failures to exit codes.",
        "Silent `except Exception` is how automation lies. Logging and exit taxonomy make failures audible.",
        """### Exceptions

Catch specific errors (`FileNotFoundError`, `json.JSONDecodeError`). Re-raise unexpected faults. Use `raise SystemExit(code)` for CLI contracts.

### logging

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stderr,
)
```

Never log secrets. Prefer structured messages: `host=%s action=%s`.

### Exit taxonomy

Document small integers: `2` usage, `3` missing dependency, `4` runtime failure.
""",
        "configure logging; catch JSON errors; map to exit codes",
    ),
    (
        6,
        "filesystem-automation-with-pathlib",
        "Filesystem Automation with pathlib",
        "Module 2: Data, Files, and Configuration",
        "beginner",
        "45 min",
        "python-pathlib",
        ["pathlib", "files"],
        "Automate files and directories with pathlib — safer joins, globs, and path validation.",
        "String concatenation for paths fails on spaces and platforms. pathlib is the default for ops file work.",
        """### Core API

```python
from pathlib import Path
root = Path.home() / "rebash-python"
root.mkdir(parents=True, exist_ok=True)
for p in root.glob("**/*.log"):
    print(p.resolve())
```

### Safety

- Resolve and check prefixes before destructive deletes
- Prefer `Path.write_text` / `read_text` with explicit encoding=`utf-8`
- Use `iterdir` / `glob` instead of parsing `ls` output
""",
        "mkdir tree; write/read files; glob logs; refuse paths outside workspace",
    ),
    (
        7,
        "json-and-yaml-for-infrastructure-config",
        "JSON and YAML for Infrastructure Config",
        "Module 2: Data, Files, and Configuration",
        "intermediate",
        "50 min",
        "python-json-yaml",
        ["json", "yaml", "config"],
        "Parse and emit JSON/YAML for infrastructure configs with validation and clear errors.",
        "Infra is data. Treat configs as typed documents, not opaque strings.",
        """### JSON (stdlib)

```python
import json
data = json.loads(path.read_text(encoding="utf-8"))
path.write_text(json.dumps(data, indent=2) + "\\n", encoding="utf-8")
```

### YAML

Use **PyYAML** (`yaml.safe_load`) or `ruamel.yaml` for round-trips. Never `yaml.load` without a SafeLoader.

### Validation

Check required keys early; fail with field names on stderr.
""",
        "round-trip JSON; safe_load YAML; validate required keys",
    ),
    (
        8,
        "regular-expressions-for-log-and-text-ops",
        "Regular Expressions for Log and Text Ops",
        "Module 2: Data, Files, and Configuration",
        "intermediate",
        "45 min",
        "python-regex-logs",
        ["regex", "logs"],
        "Extract fields from logs and text with the re module — compile once, fail clearly.",
        "Log grepping grows into parsers. Use named groups and tests, not one-off regex soup.",
        """### Patterns

```python
import re
LINE = re.compile(
    r"^(?P<level>INFO|WARN|ERROR)\\s+(?P<msg>.+)$"
)
m = LINE.match(line)
if m:
    print(m.group("level"), m.group("msg"))
```

Prefer `re.finditer` for multi-match. Avoid catastrophic backtracking on untrusted input — bound input size.
""",
        "compile a log pattern; count ERROR lines; emit summary JSON",
    ),
    (
        9,
        "environment-variables-dotenv-and-secrets-hygiene",
        "Environment Variables, dotenv, and Secrets Hygiene",
        "Module 2: Data, Files, and Configuration",
        "intermediate",
        "40 min",
        "python-env-secrets",
        ["secrets", "dotenv", "env"],
        "Load configuration from the environment safely — dotenv for local labs, never commit secrets.",
        "Tokens in git history outlive the engineer who committed them. Design for env-based secrets from day one.",
        """### Patterns

```python
import os
token = os.environ.get("API_TOKEN")
if not token:
    raise SystemExit("API_TOKEN required")
```

- Local labs: `.env` (mode `600`) loaded via `python-dotenv` — gitignore it
- CI: masked variables / secret stores
- Never print secrets; redact in logs

Prefer short-lived tokens with least privilege.
""",
        "require env var; dotenv local file; refuse logging the secret",
    ),
    (
        10,
        "configuration-management-patterns",
        "Configuration Management Patterns",
        "Module 2: Data, Files, and Configuration",
        "intermediate",
        "45 min",
        "python-config-patterns",
        ["config", "tomllib"],
        "Layer defaults, files, and environment into a single config object for ops tools.",
        "Scattered `os.environ` calls hide behaviour. Centralise config with clear precedence.",
        """### Precedence (typical)

1. Built-in defaults
2. Config file (`toml` / YAML / JSON)
3. Environment variables
4. CLI flags (highest)

### tomllib (3.11+)

```python
import tomllib
with path.open("rb") as f:
    cfg = tomllib.load(f)
```

Document the merge order in `--help` and the README.
""",
        "defaults + TOML + env override; print effective config (no secrets)",
    ),
    (
        11,
        "subprocess-calling-cli-tools-safely",
        "subprocess — Calling CLI Tools Safely",
        "Module 3: System and Network Automation",
        "intermediate",
        "50 min",
        "python-subprocess",
        ["subprocess", "cli"],
        "Call OS tools with subprocess.run list arguments — never shell=True on the happy path.",
        "Python wrapping kubectl/terraform/aws is normal. Injection via shell=True is not.",
        """### Safe pattern

```python
import subprocess
r = subprocess.run(
    ["git", "status", "--porcelain"],
    check=False,
    capture_output=True,
    text=True,
)
```

- Pass **list** args, not a string
- Set `check=True` when failure must abort
- Capture and log stderr; map `returncode` to exit taxonomy
- Avoid `shell=True` unless you fully control the string (almost never)
""",
        "run git/hostname with list args; handle non-zero; refuse shell=True demo note",
    ),
    (
        12,
        "building-clis-with-argparse",
        "Building CLIs with argparse",
        "Module 3: System and Network Automation",
        "intermediate",
        "50 min",
        "python-argparse",
        ["argparse", "cli"],
        "Build reliable operator CLIs with argparse — subcommands, --dry-run, and exit codes.",
        "A clear CLI is the UI for automation. argparse is stdlib and enough for many tools.",
        """### Skeleton

```python
import argparse
p = argparse.ArgumentParser(prog="inventory")
p.add_argument("--dry-run", action="store_true")
sub = p.add_subparsers(dest="cmd", required=True)
sub.add_parser("list")
```

Always provide `--help`, default dry-run for destructive verbs, and validate paths early.
""",
        "argparse with --verbose and subcommands; dry-run flag",
    ),
    (
        13,
        "modern-clis-with-typer-or-click",
        "Modern CLIs with Typer or Click",
        "Module 3: System and Network Automation",
        "intermediate",
        "45 min",
        "python-typer-click",
        ["typer", "click"],
        "Graduate to Typer or Click for typed options, nested commands, and richer operator UX.",
        "When argparse grows painful, Typer/Click keep CLIs readable — still with dry-run and logging.",
        """### Typer sketch

```python
import typer
app = typer.Typer(no_args_is_help=True)

@app.command()
def ping(host: str, dry_run: bool = False) -> None:
    if dry_run:
        typer.echo(f"would ping {host}")
        raise typer.Exit(0)
```

Teach argparse first (stdlib), then Typer for packaged tools. Click remains common in older repos.
""",
        "minimal Typer app (or Click); --dry-run command; show --help",
    ),
    (
        14,
        "rest-apis-with-httpx-and-requests",
        "REST APIs with httpx (and requests)",
        "Module 3: System and Network Automation",
        "intermediate",
        "55 min",
        "python-http-apis",
        ["httpx", "requests", "http"],
        "Call REST APIs with httpx — timeouts, status checks, and requests familiarity for legacy code.",
        "Ops tools live on HTTP. Prefer httpx for new code; understand requests for brownfield.",
        """### httpx

```python
import httpx
with httpx.Client(timeout=10.0) as client:
    r = client.get("https://httpbin.org/get")
    r.raise_for_status()
    data = r.json()
```

Always set timeouts. Prefer `raise_for_status()`. Retry idempotent GETs carefully; never retry blind POSTs.

### requests

Same ideas: `timeout=`, `raise_for_status()`, session reuse.
""",
        "httpx GET with timeout; print selected JSON fields; handle HTTP error",
    ),
    (
        15,
        "authentication-patterns-for-automation",
        "Authentication Patterns for Automation",
        "Module 3: System and Network Automation",
        "intermediate",
        "45 min",
        "python-api-auth",
        ["auth", "tokens", "oauth"],
        "Authenticate automation safely — bearer tokens, basic auth, and header hygiene.",
        "Broken auth either leaks credentials or bricks pipelines. Standardise how tools load tokens.",
        """### Patterns

| Pattern | Use |
|---------|-----|
| Bearer token header | Most REST APIs |
| Basic auth | Legacy endpoints |
| mTLS / client certs | High-security internal APIs |

```python
headers = {"Authorization": f"Bearer {token}"}
```

Load tokens from env; never hard-code; never log `Authorization`. Prefer fine-grained, short-lived credentials.
""",
        "build auth headers from env; redact in debug logs; fail closed if missing",
    ),
    (
        16,
        "ssh-automation-with-paramiko",
        "SSH Automation with Paramiko",
        "Module 3: System and Network Automation",
        "intermediate",
        "55 min",
        "python-paramiko-ssh",
        ["paramiko", "ssh"],
        "Automate remote commands with Paramiko — keys, timeouts, and careful command construction.",
        "SSH from Python is powerful and dangerous. Prefer keys, known_hosts discipline, and no shell metacharacters.",
        """### Sketch

```python
import paramiko
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.RejectPolicy())
```

For labs without a remote host, mock the exec interface or use fixtures. Prefer key auth over passwords. Avoid interpolating untrusted strings into remote shells.
""",
        "dry-run / fixture SSH runner; document key auth; refuse password in code",
    ),
    (
        17,
        "github-api-automation",
        "GitHub API Automation",
        "Module 4: Platform Automation",
        "intermediate",
        "55 min",
        "python-github-api",
        ["github", "api"],
        "Report on repositories via the GitHub REST API with httpx — token optional via fixtures.",
        "Inventory and compliance reports often start with GitHub. Use fine-grained tokens or recorded fixtures.",
        """### Approach

- Authenticate with `GITHUB_TOKEN` when available
- Otherwise load a recorded JSON fixture for offline/CI labs
- Paginate carefully; respect rate limits
- Prefer dry-run / report-only tools first

Document both live and fixture paths in the lab README.
""",
        "list repos via fixture or live API; emit markdown summary; no token required for fixture path",
    ),
    (
        18,
        "docker-sdk-images-containers-cleanup",
        "Docker SDK — Images, Containers, Cleanup",
        "Module 4: Platform Automation",
        "intermediate",
        "55 min",
        "python-docker-sdk",
        ["docker", "sdk"],
        "Inspect and clean Docker resources with the Docker SDK — dry-run by default.",
        "Prune scripts without dry-run delete production state. Always list first.",
        """### Safety

```python
# dry_run=True by default
for c in client.containers.list(all=True, filters={...}):
    print(c.name)
```

- Default to dry-run
- Label lab resources; only delete labelled/dangling targets you own
- If Docker is unavailable, use fixture inventories

Never run unbounded `prune` in shared environments.
""",
        "list containers via SDK or fixture; dry-run dangling cleanup report",
    ),
    (
        19,
        "kubernetes-python-client-health-checks",
        "Kubernetes Python Client — Read and Health Checks",
        "Module 4: Platform Automation",
        "advanced",
        "60 min",
        "python-k8s-client",
        ["kubernetes", "health"],
        "Read cluster health with the official Kubernetes Python client — report-only first.",
        "Write access from automation needs RBAC scrutiny. Start with list/get health reports.",
        """### Patterns

- Load kubeconfig or in-cluster config
- List pods/deployments; check Ready conditions
- Prefer namespaced, least-privilege ServiceAccounts
- Fixture/mock client when kind/minikube is unavailable

Document dry-run and fixture modes for CI.
""",
        "health report from fixture or live cluster; print non-ready pods",
    ),
    (
        20,
        "automating-terraform-workflows",
        "Automating Terraform Workflows",
        "Module 4: Platform Automation",
        "advanced",
        "55 min",
        "python-terraform-wrap",
        ["terraform", "iac"],
        "Wrap terraform fmt/validate/plan with subprocess — parse plan JSON for summaries.",
        "Python should orchestrate Terraform, not reimplement it. Capture plan JSON and report.",
        """### Wrapper flow

1. `terraform fmt -check`
2. `terraform validate`
3. `terraform plan -out=tfplan` then `terraform show -json`

Use list-form `subprocess.run`. Default to plan/report; require an explicit flag for apply. Fixture plan JSON when Terraform is not installed.
""",
        "parse fixture plan JSON or run fmt/validate; print resource change summary",
    ),
    (
        21,
        "python-in-ci-cd-pipelines",
        "Python in CI/CD Pipelines",
        "Module 4: Platform Automation",
        "intermediate",
        "50 min",
        "python-cicd",
        ["cicd", "gitlab", "pytest"],
        "Run lint and pytest for Python automation in GitLab CI or GitHub Actions.",
        "CI is where pinning and venv discipline pay off. Keep jobs fail-fast and secret-safe.",
        """### Job shape

```yaml
test:
  image: python:3.12-slim
  script:
    - python -m venv .venv
    - . .venv/bin/activate
    - pip install -r requirements.txt
    - pytest -q
```

Mask secrets; cache venvs carefully; prefer repo scripts over huge inline YAML.
""",
        "write pytest stub + CI YAML sketch; run tests locally in venv",
    ),
    (
        22,
        "async-basics-for-io-bound-ops-tools",
        "Async Basics for I/O-bound Ops Tools",
        "Module 5: Production Engineering",
        "advanced",
        "50 min",
        "python-async-ops",
        ["asyncio", "async", "httpx"],
        "Use asyncio and httpx AsyncClient for concurrent I/O-bound ops checks — not CPU-bound work.",
        "Fan-out health checks benefit from async. CPU parsing usually does not.",
        """### When async helps

Many independent HTTP/SSH waits — yes. Tight CPU loops — no (use processes).

```python
async with httpx.AsyncClient(timeout=10.0) as client:
    await client.get(url)
```

Keep concurrency bounded (`asyncio.Semaphore`). Prefer sync code until measurement says otherwise.
""",
        "async gather of fixture URLs or local sleeps; bound concurrency",
    ),
    (
        23,
        "testing-automation-with-pytest",
        "Testing Automation with pytest",
        "Module 5: Production Engineering",
        "intermediate",
        "55 min",
        "python-pytest",
        ["pytest", "testing"],
        "Test ops automation with pytest — fixtures, tmp paths, and no live cloud in CI.",
        "Untested prune scripts are incidents waiting to happen. Fixture the dangerous edges.",
        """### Habits

```python
def test_parse_log(tmp_path: Path) -> None:
    p = tmp_path / "a.log"
    p.write_text("ERROR disk\\n", encoding="utf-8")
    assert count_errors(p) == 1
```

- Prefer tmp_path over real home directories
- Mock subprocess/HTTP at boundaries
- Assert exit codes for CLI entry points
""",
        "write pytest for a pure helper; use tmp_path; run pytest -q",
    ),
    (
        24,
        "packaging-with-pyproject-uv-and-poetry",
        "Packaging with pyproject.toml, uv, and Poetry",
        "Module 5: Production Engineering",
        "intermediate",
        "50 min",
        "python-packaging-uv",
        ["packaging", "uv", "poetry"],
        "Package DevOps CLIs with pyproject.toml — installable entry points via uv or Poetry.",
        "Editable installs and console scripts make tools shareable. Lock dependencies.",
        """### pyproject essentials

```toml
[project]
name = "ops-tool"
requires-python = ">=3.12"
dependencies = ["httpx>=0.27"]

[project.scripts]
ops-tool = "ops_tool.cli:app"
```

Teach **uv** (`uv sync`, `uv lock`) and Poetry as alternatives. Prefer reproducible locks in CI.
""",
        "minimal pyproject + console script; pip install -e . or uv sync",
    ),
    (
        25,
        "production-patterns-for-devops-python",
        "Production Patterns for DevOps Python",
        "Module 5: Production Engineering",
        "advanced",
        "55 min",
        "python-prod-patterns",
        ["production", "dry-run", "idempotency"],
        "Ship production-grade patterns — dry-run, idempotency, retries, and blast-radius limits.",
        "Patterns beat cleverness. Standardise how every mutating tool behaves under failure.",
        """### Checklist

1. Dry-run default for destructive actions
2. Idempotent retries where safe
3. Timeouts on all I/O
4. Structured logging without secrets
5. Explicit exit taxonomy
6. Least privilege documentation

Prefer small composable commands over monolith scripts.
""",
        "implement dry-run + idempotent marker file; logging; exit codes",
    ),
    (
        26,
        "capstone-prep-framework-skeleton",
        "Capstone Prep — Framework Skeleton",
        "Module 5: Production Engineering",
        "advanced",
        "45 min",
        "python-framework-skeleton",
        ["capstone", "framework"],
        "Assemble a small DevOps automation framework skeleton ready for the course capstone.",
        "Pull the track together: package layout, shared logging/config, dry-run commands, and tests.",
        """### Target layout

```text
framework/
  pyproject.toml
  src/rebash_ops/
    cli.py
    lib/{logging,config,http}.py
  tests/
  .gitlab-ci.yml.example
```

Commands stubbed: `logs analyse`, `k8s health`, `tf plan-summary`, `docker dangling` — all dry-run by default.
""",
        "create skeleton package; one working dry-run command; pytest smoke",
    ),
]

assert len(SPEC) == 26, len(SPEC)


def related(num: int) -> str:
    titles = {sp[0]: sp[2] for sp in SPEC}
    slugs = {sp[0]: sp[1] for sp in SPEC}
    links = ["- Track overview: [Python for DevOps](index.md)"]
    if num > 1:
        links.append(f"- Previous: [{titles[num - 1]}]({slugs[num - 1]}.md)")
    if num < len(SPEC):
        links.append(f"- Next: [{titles[num + 1]}]({slugs[num + 1]}.md)")
    links.append("- Prerequisite: [Shell Scripting](../shell/index.md)")
    links.append(
        "- Course path: [Python for DevOps Engineers](../learning-paths/python-for-devops.md)"
    )
    return "\n".join(links)


LAB_EXTRA: dict[int, str] = {
    1: dedent(
        """\
        ### Step 2 – Ops hello script

        ```bash
        cat > hello_ops.py << 'EOF'
        #!/usr/bin/env python3
        import os
        import platform
        import socket
        import sys

        def main() -> int:
            print(f"host={socket.gethostname()}")
            print(f"user={os.environ.get('USER', 'unknown')}")
            print(f"python={platform.python_version()}")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        chmod +x hello_ops.py
        ./hello_ops.py
        ```
        """
    ),
    2: dedent(
        """\
        ### Step 2 – Functions and guard clauses

        ```bash
        cat > syntax_ops.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        import sys

        def die(msg: str, code: int = 2) -> None:
            print(msg, file=sys.stderr)
            raise SystemExit(code)

        def classify(level: str) -> str:
            level = level.upper()
            if level not in {"INFO", "WARN", "ERROR"}:
                die(f"unknown level: {level}")
            return level

        def main(argv: list[str]) -> int:
            if len(argv) < 2:
                die(f"usage: {argv[0]} LEVEL")
            print(f"level={classify(argv[1])}")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main(sys.argv))
        EOF
        python3 syntax_ops.py INFO
        python3 syntax_ops.py nope || echo "exit=$?"
        ```
        """
    ),
    3: dedent(
        """\
        ### Step 2 – Package layout

        ```bash
        mkdir -p demo_tool/lib
        cat > demo_tool/__init__.py << 'EOF'
        __version__ = "0.1.0"
        EOF
        cat > demo_tool/lib/__init__.py << 'EOF'
        EOF
        cat > demo_tool/lib/meta.py << 'EOF'
        def fingerprint() -> str:
            return "demo_tool-ok"
        EOF
        cat > demo_tool/cli.py << 'EOF'
        from demo_tool.lib.meta import fingerprint

        def main() -> int:
            print(fingerprint())
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        PYTHONPATH=. python3 -m demo_tool.cli
        ```
        """
    ),
    4: dedent(
        """\
        ### Step 2 – venv and pins

        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        python -m pip install --upgrade pip
        python -m pip install 'httpx==0.28.1'
        python -m pip freeze > requirements.txt
        grep -E '^httpx==' requirements.txt
        python -c "import httpx; print(httpx.__version__)"
        deactivate
        ```
        """
    ),
    5: dedent(
        """\
        ### Step 2 – logging and exit codes

        ```bash
        cat > log_ops.py << 'EOF'
        #!/usr/bin/env python3
        import json
        import logging
        import sys
        from pathlib import Path

        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s %(message)s",
            stream=sys.stderr,
        )
        log = logging.getLogger("ops")

        def main(argv: list[str]) -> int:
            if len(argv) < 2:
                log.error("usage: log_ops.py FILE.json")
                return 2
            path = Path(argv[1])
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except FileNotFoundError:
                log.error("missing file path=%s", path)
                return 3
            except json.JSONDecodeError as exc:
                log.error("invalid json path=%s err=%s", path, exc)
                return 4
            log.info("keys=%s", sorted(data))
            print(json.dumps({"ok": True, "n": len(data)}))
            return 0

        if __name__ == "__main__":
            raise SystemExit(main(sys.argv))
        EOF
        echo '{"a":1}' > ok.json
        echo 'not-json' > bad.json
        python3 log_ops.py ok.json
        python3 log_ops.py bad.json || echo "exit=$?"
        ```
        """
    ),
    6: dedent(
        """\
        ### Step 2 – pathlib workspace

        ```bash
        cat > path_ops.py << 'EOF'
        #!/usr/bin/env python3
        from pathlib import Path
        import sys

        def main() -> int:
            root = Path.cwd().resolve()
            data = root / "data"
            data.mkdir(parents=True, exist_ok=True)
            sample = data / "app.log"
            sample.write_text("INFO start\\nERROR disk\\n", encoding="utf-8")
            for p in data.glob("*.log"):
                print(f"file={p.name} bytes={p.stat().st_size}")
            target = (data / ".." / "data" / "app.log").resolve()
            if not str(target).startswith(str(root)):
                print("refuse path outside workspace", file=sys.stderr)
                return 2
            print(f"safe={target.relative_to(root)}")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 path_ops.py
        ```
        """
    ),
    7: dedent(
        """\
        ### Step 2 – JSON and YAML

        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        pip install -q 'PyYAML==6.0.2'
        cat > config_ops.py << 'EOF'
        #!/usr/bin/env python3
        import json
        import sys
        from pathlib import Path
        import yaml

        REQUIRED = {"service", "replicas"}

        def load_yaml(path: Path) -> dict:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("root must be a mapping")
            missing = REQUIRED - data.keys()
            if missing:
                raise ValueError(f"missing keys: {sorted(missing)}")
            return data

        def main() -> int:
            yml = Path("svc.yaml")
            yml.write_text("service: api\\nreplicas: 2\\n", encoding="utf-8")
            data = load_yaml(yml)
            out = Path("svc.json")
            out.write_text(json.dumps(data, indent=2) + "\\n", encoding="utf-8")
            print(out.read_text(encoding="utf-8"), end="")
            return 0

        if __name__ == "__main__":
            try:
                raise SystemExit(main())
            except Exception as exc:
                print(exc, file=sys.stderr)
                raise SystemExit(4)
        EOF
        python3 config_ops.py
        ```
        """
    ),
    8: dedent(
        """\
        ### Step 2 – log regex summary

        ```bash
        cat > regex_ops.py << 'EOF'
        #!/usr/bin/env python3
        import json
        import re
        from pathlib import Path

        LINE = re.compile(r"^(?P<level>INFO|WARN|ERROR)\\s+(?P<msg>.+)$")

        def summarise(path: Path) -> dict:
            counts = {"INFO": 0, "WARN": 0, "ERROR": 0}
            for raw in path.read_text(encoding="utf-8").splitlines():
                m = LINE.match(raw)
                if m:
                    counts[m.group("level")] += 1
            return counts

        def main() -> int:
            log = Path("app.log")
            log.write_text("INFO ok\\nERROR disk\\nERROR mem\\nINFO done\\n", encoding="utf-8")
            print(json.dumps(summarise(log), indent=2))
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 regex_ops.py
        ```
        """
    ),
    9: dedent(
        """\
        ### Step 2 – secrets hygiene

        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        pip install -q 'python-dotenv==1.1.0'
        cat > .env << 'EOF'
        API_TOKEN=lab-secret-do-not-commit
        EOF
        chmod 600 .env
        cat > secrets_ops.py << 'EOF'
        #!/usr/bin/env python3
        import logging
        import os
        import sys
        from dotenv import load_dotenv

        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
        log = logging.getLogger("ops")

        def main() -> int:
            load_dotenv()
            token = os.environ.get("API_TOKEN")
            if not token:
                log.error("API_TOKEN required")
                return 2
            log.debug("token_loaded=yes redacted=%s", "*" * 8)
            print("auth=ready")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 secrets_ops.py
        echo ".env" >> .gitignore
        ```
        """
    ),
    10: dedent(
        """\
        ### Step 2 – layered config

        ```bash
        cat > defaults.toml << 'EOF'
        [app]
        region = "eu-west-1"
        verbose = false
        EOF
        cat > config_layer.py << 'EOF'
        #!/usr/bin/env python3
        import os
        import tomllib
        from pathlib import Path

        def load() -> dict:
            with Path("defaults.toml").open("rb") as f:
                cfg = tomllib.load(f)["app"]
            if region := os.environ.get("APP_REGION"):
                cfg["region"] = region
            if os.environ.get("APP_VERBOSE", "").lower() in {"1", "true"}:
                cfg["verbose"] = True
            return cfg

        if __name__ == "__main__":
            print(load())
        EOF
        APP_REGION=us-east-1 python3 config_layer.py
        ```
        """
    ),
    11: dedent(
        """\
        ### Step 2 – safe subprocess

        ```bash
        cat > subproc_ops.py << 'EOF'
        #!/usr/bin/env python3
        import subprocess
        import sys

        def run_cmd(argv: list[str]) -> int:
            # Never shell=True on the happy path
            r = subprocess.run(argv, check=False, capture_output=True, text=True)
            if r.returncode != 0:
                print(r.stderr.strip() or "command failed", file=sys.stderr)
                return 4
            print(r.stdout.strip())
            return 0

        def main() -> int:
            code = run_cmd(["uname", "-s"])
            if code:
                return code
            return run_cmd(["git", "--version"])

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 subproc_ops.py
        ```
        """
    ),
    12: dedent(
        """\
        ### Step 2 – argparse CLI

        ```bash
        cat > argparse_ops.py << 'EOF'
        #!/usr/bin/env python3
        import argparse
        import sys

        def main(argv: list[str] | None = None) -> int:
            p = argparse.ArgumentParser(prog="inventory")
            p.add_argument("-v", "--verbose", action="store_true")
            p.add_argument("--dry-run", action="store_true", default=True)
            p.add_argument("--apply", action="store_true", help="disable dry-run")
            sub = p.add_subparsers(dest="cmd", required=True)
            sub.add_parser("list", help="list resources")
            sub.add_parser("delete", help="delete resources")
            args = p.parse_args(argv)
            dry_run = not args.apply
            if args.verbose:
                print(f"cmd={args.cmd} dry_run={dry_run}", file=sys.stderr)
            if args.cmd == "delete" and not dry_run:
                print("DELETE applied")
            else:
                print(f"would {args.cmd}")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 argparse_ops.py list -v
        python3 argparse_ops.py delete
        python3 argparse_ops.py delete --apply
        ```
        """
    ),
    13: dedent(
        """\
        ### Step 2 – Typer CLI

        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        pip install -q 'typer==0.16.0'
        cat > typer_ops.py << 'EOF'
        #!/usr/bin/env python3
        import typer

        app = typer.Typer(no_args_is_help=True, add_completion=False)

        @app.command()
        def ping(host: str, dry_run: bool = True) -> None:
            if dry_run:
                typer.echo(f"would ping {host}")
                raise typer.Exit(0)
            typer.echo(f"ping {host}")

        if __name__ == "__main__":
            app()
        EOF
        python3 typer_ops.py --help
        python3 typer_ops.py ping example.com
        python3 typer_ops.py ping example.com --no-dry-run
        ```
        """
    ),
    14: dedent(
        """\
        ### Step 2 – httpx GET

        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        pip install -q 'httpx==0.28.1'
        cat > http_ops.py << 'EOF'
        #!/usr/bin/env python3
        import sys
        import httpx

        def main() -> int:
            url = "https://httpbin.org/get"
            try:
                with httpx.Client(timeout=10.0) as client:
                    r = client.get(url)
                    r.raise_for_status()
            except httpx.HTTPError as exc:
                print(f"http error: {exc}", file=sys.stderr)
                return 4
            data = r.json()
            print(f"url={data.get('url')}")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 http_ops.py
        ```
        """
    ),
    15: dedent(
        """\
        ### Step 2 – auth headers

        ```bash
        cat > auth_ops.py << 'EOF'
        #!/usr/bin/env python3
        import logging
        import os
        import sys

        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
        log = logging.getLogger("ops")

        def auth_headers() -> dict[str, str]:
            token = os.environ.get("API_TOKEN")
            if not token:
                raise SystemExit("API_TOKEN required")
            return {"Authorization": f"Bearer {token}"}

        def main() -> int:
            headers = auth_headers()
            log.debug("headers_keys=%s authorization=REDACTED", sorted(headers))
            print("authorization=present")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        API_TOKEN=lab-token python3 auth_ops.py
        python3 auth_ops.py || echo "exit=$?"
        ```
        """
    ),
    16: dedent(
        """\
        ### Step 2 – SSH fixture runner (no remote required)

        ```bash
        cat > ssh_ops.py << 'EOF'
        #!/usr/bin/env python3
        # Fixture SSH runner - swap for Paramiko when a lab host exists.
        from __future__ import annotations
        import json
        from pathlib import Path

        class FixtureSSH:
            def exec_command(self, command: str) -> tuple[str, str, int]:
                # Never interpolate untrusted input into a remote shell
                if command != "uname -s":
                    return "", f"unsupported: {command}", 2
                return "Linux\\n", "", 0

        def main() -> int:
            client = FixtureSSH()
            out, err, code = client.exec_command("uname -s")
            result = {"stdout": out.strip(), "stderr": err.strip(), "code": code}
            Path("ssh-result.json").write_text(json.dumps(result, indent=2) + "\\n")
            print(result)
            return code

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 ssh_ops.py
        ```
        """
    ),
    17: dedent(
        """\
        ### Step 2 – GitHub reporter with fixture fallback

        ```bash
        mkdir -p fixtures
        cat > fixtures/repos.json << 'EOF'
        [{"name": "rebash-academy", "private": false, "open_issues": 3},
         {"name": "lab-private", "private": true, "open_issues": 0}]
        EOF
        cat > github_ops.py << 'EOF'
        #!/usr/bin/env python3
        import json
        import os
        import sys
        from pathlib import Path

        def load_repos() -> list[dict]:
            token = os.environ.get("GITHUB_TOKEN")
            if not token:
                return json.loads(Path("fixtures/repos.json").read_text(encoding="utf-8"))
            # Live path sketch (requires network + token):
            # import httpx
            # with httpx.Client(headers={"Authorization": f"Bearer {token}"}, timeout=20) as c:
            #     r = c.get("https://api.github.com/user/repos")
            #     r.raise_for_status()
            #     return r.json()
            print("live API path documented; using fixture unless you enable it", file=sys.stderr)
            return json.loads(Path("fixtures/repos.json").read_text(encoding="utf-8"))

        def main() -> int:
            repos = load_repos()
            print("# GitHub repo report")
            for repo in repos:
                vis = "private" if repo["private"] else "public"
                print(f"- {repo['name']} ({vis}) issues={repo['open_issues']}")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 github_ops.py
        ```
        """
    ),
    18: dedent(
        """\
        ### Step 2 – Docker cleanup dry-run (fixture if no Docker)

        ```bash
        mkdir -p fixtures
        cat > fixtures/containers.json << 'EOF'
        [{"name": "lab-nginx", "status": "exited", "labels": {"rebash.lab": "true"}},
         {"name": "prod-db", "status": "running", "labels": {}}]
        EOF
        cat > docker_ops.py << 'EOF'
        #!/usr/bin/env python3
        import json
        import sys
        from pathlib import Path

        def list_containers() -> list[dict]:
            try:
                import docker  # type: ignore
                client = docker.from_env()
                return [
                    {
                        "name": c.name,
                        "status": c.status,
                        "labels": c.labels or {},
                    }
                    for c in client.containers.list(all=True)
                ]
            except Exception:
                print("docker unavailable — using fixtures", file=sys.stderr)
                return json.loads(Path("fixtures/containers.json").read_text(encoding="utf-8"))

        def main(dry_run: bool = True) -> int:
            victims = [
                c for c in list_containers()
                if c.get("labels", {}).get("rebash.lab") == "true" and c["status"] == "exited"
            ]
            for c in victims:
                action = "would remove" if dry_run else "removing"
                print(f"{action} {c['name']}")
            if not victims:
                print("nothing to clean")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main(dry_run=True))
        EOF
        python3 docker_ops.py
        ```
        """
    ),
    19: dedent(
        """\
        ### Step 2 – Kubernetes health from fixture

        ```bash
        mkdir -p fixtures
        cat > fixtures/pods.json << 'EOF'
        [{"name": "api-1", "namespace": "demo", "ready": true},
         {"name": "api-2", "namespace": "demo", "ready": false}]
        EOF
        cat > k8s_ops.py << 'EOF'
        #!/usr/bin/env python3
        import json
        import sys
        from pathlib import Path

        def load_pods() -> list[dict]:
            try:
                from kubernetes import client, config  # type: ignore
                config.load_kube_config()
                v1 = client.CoreV1Api()
                pods = v1.list_namespaced_pod("demo").items
                out = []
                for p in pods:
                    ready = all(
                        (c.ready or False) for c in (p.status.container_statuses or [])
                    )
                    out.append({"name": p.metadata.name, "namespace": "demo", "ready": ready})
                return out
            except Exception:
                print("cluster unavailable — using fixtures", file=sys.stderr)
                return json.loads(Path("fixtures/pods.json").read_text(encoding="utf-8"))

        def main() -> int:
            bad = [p for p in load_pods() if not p["ready"]]
            for p in bad:
                print(f"NOT_READY ns={p['namespace']} pod={p['name']}")
            print(f"RESULT non_ready={len(bad)}")
            return 1 if bad else 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 k8s_ops.py || echo "exit=$?"
        ```
        """
    ),
    20: dedent(
        """\
        ### Step 2 – Terraform plan summary (fixture)

        ```bash
        mkdir -p fixtures
        cat > fixtures/plan.json << 'EOF'
        {"resource_changes": [
          {"address": "local_file.a", "change": {"actions": ["create"]}},
          {"address": "local_file.b", "change": {"actions": ["update"]}},
          {"address": "local_file.c", "change": {"actions": ["no-op"]}}
        ]}
        EOF
        cat > tf_ops.py << 'EOF'
        #!/usr/bin/env python3
        import json
        import shutil
        import subprocess
        import sys
        from collections import Counter
        from pathlib import Path

        def load_plan() -> dict:
            if shutil.which("terraform"):
                # Live path: terraform show -json tfplan
                print("terraform found — lab still uses fixture for safety", file=sys.stderr)
            return json.loads(Path("fixtures/plan.json").read_text(encoding="utf-8"))

        def main() -> int:
            plan = load_plan()
            counts: Counter[str] = Counter()
            for rc in plan.get("resource_changes", []):
                for action in rc["change"]["actions"]:
                    counts[action] += 1
            print(dict(counts))
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 tf_ops.py
        ```
        """
    ),
    21: dedent(
        """\
        ### Step 2 – pytest + CI sketch

        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        pip install -q pytest
        mkdir -p src tests
        cat > src/util.py << 'EOF'
        def add(a: int, b: int) -> int:
            return a + b
        EOF
        cat > tests/test_util.py << 'EOF'
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
        from util import add

        def test_add() -> None:
            assert add(2, 3) == 5
        EOF
        cat > .gitlab-ci.yml.example << 'EOF'
        test:
          image: python:3.12-slim
          script:
            - python -m venv .venv
            - . .venv/bin/activate
            - pip install pytest
            - pytest -q
        EOF
        PYTHONPATH=src pytest -q
        ```
        """
    ),
    22: dedent(
        """\
        ### Step 2 – bounded async gather

        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        pip install -q 'httpx==0.28.1'
        cat > async_ops.py << 'EOF'
        #!/usr/bin/env python3
        import asyncio
        import time

        async def check(name: str, sem: asyncio.Semaphore) -> str:
            async with sem:
                await asyncio.sleep(0.05)
                return f"{name}=ok"

        async def main() -> int:
            sem = asyncio.Semaphore(3)
            names = [f"target-{i}" for i in range(6)]
            t0 = time.perf_counter()
            results = await asyncio.gather(*(check(n, sem) for n in names))
            print(results)
            print(f"elapsed={time.perf_counter() - t0:.2f}s")
            return 0

        if __name__ == "__main__":
            raise SystemExit(asyncio.run(main()))
        EOF
        python3 async_ops.py
        ```
        """
    ),
    23: dedent(
        """\
        ### Step 2 – pytest with tmp_path

        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        pip install -q pytest
        cat > parse_log.py << 'EOF'
        from pathlib import Path

        def count_errors(path: Path) -> int:
            return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("ERROR"))
        EOF
        cat > test_parse_log.py << 'EOF'
        from pathlib import Path
        from parse_log import count_errors

        def test_count_errors(tmp_path: Path) -> None:
            p = tmp_path / "a.log"
            p.write_text("INFO ok\\nERROR disk\\nERROR mem\\n", encoding="utf-8")
            assert count_errors(p) == 2
        EOF
        pytest -q
        ```
        """
    ),
    24: dedent(
        """\
        ### Step 2 – pyproject console script

        ```bash
        mkdir -p src/ops_tool
        cat > pyproject.toml << 'EOF'
        [build-system]
        requires = ["setuptools>=68"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "ops-tool"
        version = "0.1.0"
        requires-python = ">=3.12"
        dependencies = []

        [project.scripts]
        ops-tool = "ops_tool.cli:main"

        [tool.setuptools.packages.find]
        where = ["src"]
        EOF
        cat > src/ops_tool/__init__.py << 'EOF'
        __version__ = "0.1.0"
        EOF
        cat > src/ops_tool/cli.py << 'EOF'
        def main() -> None:
            print("ops-tool ready")

        if __name__ == "__main__":
            main()
        EOF
        python3 -m venv .venv && source .venv/bin/activate
        pip install -q -e .
        ops-tool
        ```
        """
    ),
    25: dedent(
        """\
        ### Step 2 – dry-run and idempotency

        ```bash
        cat > prod_ops.py << 'EOF'
        #!/usr/bin/env python3
        import argparse
        import logging
        import sys
        from pathlib import Path

        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stderr)
        log = logging.getLogger("ops")

        def ensure_marker(path: Path, dry_run: bool) -> int:
            if path.exists():
                log.info("idempotent skip path=%s", path)
                print("RESULT status=ok changed=0")
                return 0
            if dry_run:
                log.info("dry-run would create path=%s", path)
                print("RESULT status=ok changed=0 dry_run=1")
                return 0
            path.write_text("done\\n", encoding="utf-8")
            print("RESULT status=ok changed=1")
            return 0

        def main() -> int:
            p = argparse.ArgumentParser()
            p.add_argument("--apply", action="store_true")
            args = p.parse_args()
            return ensure_marker(Path("state.marker"), dry_run=not args.apply)

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 prod_ops.py
        python3 prod_ops.py --apply
        python3 prod_ops.py --apply
        ```
        """
    ),
    26: dedent(
        """\
        ### Step 2 – framework skeleton

        ```bash
        mkdir -p src/rebash_ops/lib tests
        cat > pyproject.toml << 'EOF'
        [build-system]
        requires = ["setuptools>=68"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "rebash-ops"
        version = "0.1.0"
        requires-python = ">=3.12"
        dependencies = []

        [project.scripts]
        rebash-ops = "rebash_ops.cli:main"

        [tool.setuptools.packages.find]
        where = ["src"]
        EOF
        cat > src/rebash_ops/__init__.py << 'EOF'
        __version__ = "0.1.0"
        EOF
        cat > src/rebash_ops/lib/logging.py << 'EOF'
        import logging
        import sys

        def setup() -> logging.Logger:
            logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stderr)
            return logging.getLogger("rebash_ops")
        EOF
        cat > src/rebash_ops/cli.py << 'EOF'
        import argparse
        from rebash_ops.lib.logging import setup

        def main() -> None:
            log = setup()
            p = argparse.ArgumentParser(prog="rebash-ops")
            sub = p.add_subparsers(dest="cmd", required=True)
            d = sub.add_parser("docker")
            d.add_argument("action", choices=["dangling"])
            d.add_argument("--apply", action="store_true")
            args = p.parse_args()
            dry_run = not args.apply
            log.info("cmd=%s action=%s dry_run=%s", args.cmd, args.action, dry_run)
            print(f"would report dangling images" if dry_run else "applying")

        if __name__ == "__main__":
            main()
        EOF
        cat > tests/test_smoke.py << 'EOF'
        def test_version() -> None:
            from rebash_ops import __version__
            assert __version__
        EOF
        python3 -m venv .venv && source .venv/bin/activate
        pip install -q -e .
        pip install -q pytest
        rebash-ops docker dangling
        PYTHONPATH=src pytest -q
        ```
        """
    ),
}


DIAGRAMS: dict[str, str] = {
    "python-intro-devops": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Human: "Human / CI" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Py: "Python tool" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Data: "APIs / files" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Out: "Exit + logs" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Human -> Py -> Data -> Out
        """
    ),
    "python-syntax-ops": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Input: "Args / data" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Fn: "Functions" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Flow: "if / for / match" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Result: "Return / exit" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Input -> Fn -> Flow -> Result
        """
    ),
    "python-modules-layout": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        CLI: "cli.py" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Lib: "lib/*" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Tests: "tests/" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Pkg: "pyproject" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        CLI -> Lib
        Tests -> Lib
        Pkg -> CLI
        """
    ),
    "python-venv-deps": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Py: "Python 3.12+" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Venv: ".venv" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Pins: "lock / requirements" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Tool: "ops tool" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Py -> Venv -> Pins -> Tool
        """
    ),
    "python-errors-logging": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Call: "Operation" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Exc: "Exceptions" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Log: "stderr logs" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Exit: "Exit code" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Call -> Exc -> Log -> Exit
        """
    ),
    "python-pathlib": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Root: "Workspace Path" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Glob: "glob / iterdir" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Safe: "resolve + prefix" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        IO: "read / write" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Root -> Glob -> Safe -> IO
        """
    ),
    "python-json-yaml": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        File: "JSON / YAML" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Parse: "safe_load / loads" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Val: "required keys" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Out: "dict / report" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        File -> Parse -> Val -> Out
        """
    ),
    "python-regex-logs": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Log: "Log lines" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Re: "compiled re" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Groups: "named groups" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Sum: "summary JSON" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Log -> Re -> Groups -> Sum
        """
    ),
    "python-env-secrets": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Env: "ENV / .env" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Load: "os.environ" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Redact: "no secret logs" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        API: "authenticated call" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Env -> Load -> Redact -> API
        """
    ),
    "python-config-patterns": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Def: "defaults" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        File: "TOML / YAML" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Env: "environment" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        CLI: "CLI flags" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Def -> File -> Env -> CLI
        """
    ),
    "python-subprocess": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Py: "Python" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Run: "subprocess.run\\nlist argv" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Tool: "git / terraform" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        RC: "returncode" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Py -> Run -> Tool -> RC
        """
    ),
    "python-argparse": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Argv: "sys.argv" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        AP: "argparse" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Sub: "subcommands" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Act: "dry-run / apply" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Argv -> AP -> Sub -> Act
        """
    ),
    "python-typer-click": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        User: "Operator" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Typer: "Typer / Click" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Cmd: "typed commands" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Out: "UX + exit" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        User -> Typer -> Cmd -> Out
        """
    ),
    "python-http-apis": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Client: "httpx Client" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        HTTP: "GET / POST" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        API: "REST API" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        JSON: "JSON body" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Client -> HTTP -> API -> JSON
        """
    ),
    "python-api-auth": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Secret: "ENV token" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Hdr: "Authorization" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        API: "protected API" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Log: "redacted logs" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Secret -> Hdr -> API
        Hdr -> Log
        """
    ),
    "python-paramiko-ssh": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Py: "Paramiko" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Key: "SSH key" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Host: "remote host" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Cmd: "exec result" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Py -> Key -> Host -> Cmd
        """
    ),
    "python-github-api": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Tok: "GITHUB_TOKEN\\nor fixture" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Httpx: "httpx" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        GH: "GitHub API" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Rpt: "Markdown report" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Tok -> Httpx -> GH -> Rpt
        """
    ),
    "python-docker-sdk": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        SDK: "Docker SDK" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        List: "list + filter" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Dry: "dry-run default" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Clean: "labelled cleanup" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        SDK -> List -> Dry -> Clean
        """
    ),
    "python-k8s-client": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Kube: "kubeconfig" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Client: "K8s client" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Read: "list pods" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Health: "ready report" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Kube -> Client -> Read -> Health
        """
    ),
    "python-terraform-wrap": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Wrap: "Python wrapper" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        TF: "terraform CLI" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Plan: "plan JSON" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Sum: "change summary" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Wrap -> TF -> Plan -> Sum
        """
    ),
    "python-cicd": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Push: "git push" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        CI: "CI job" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Test: "pytest / lint" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Gate: "pass / fail" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Push -> CI -> Test -> Gate
        """
    ),
    "python-async-ops": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Tasks: "I/O tasks" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Sem: "Semaphore" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Async: "asyncio.gather" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Res: "results" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Tasks -> Sem -> Async -> Res
        """
    ),
    "python-pytest": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Code: "ops code" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Fix: "fixtures" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        PyT: "pytest" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        CI: "CI green" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Code -> Fix -> PyT -> CI
        """
    ),
    "python-packaging-uv": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Toml: "pyproject.toml" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Uv: "uv / Poetry" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Lock: "lockfile" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Entry: "console script" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Toml -> Uv -> Lock -> Entry
        """
    ),
    "python-prod-patterns": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        Dry: "dry-run" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Idem: "idempotent" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Log: "structured logs" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Blast: "blast radius" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        Dry -> Idem -> Log -> Blast
        """
    ),
    "python-framework-skeleton": dedent(
        """\
        *: { style: { border-radius: 14; font-size: 14; bold: true; shadow: true; stroke-width: 2 } }
        direction: right
        CLI: "rebash-ops CLI" { style.fill: "#dbeafe"; style.stroke: "#2563eb" }
        Lib: "shared lib" { style.fill: "#dcfce7"; style.stroke: "#16a34a" }
        Cmds: "plugins / cmds" { style.fill: "#ffedd5"; style.stroke: "#ea580c" }
        Test: "pytest + CI" { style.fill: "#fce7f3"; style.stroke: "#db2777" }
        CLI -> Lib -> Cmds -> Test
        """
    ),
}


def lab_block(num: int, slug: str, focus: str) -> str:
    """Build Hands-on Lab markdown without accidental leading indentation."""
    # Do NOT wrap the whole lab in an indented dedent() f-string while
    # interpolating already-dedented LAB_EXTRA — that leaves body lines indented.
    extra = LAB_EXTRA.get(num, "").rstrip()
    parts = [
        "Create a workspace for this tutorial.",
        "",
        "```bash",
        f"mkdir -p ~/rebash-python/lab{num:02d} && cd ~/rebash-python/lab{num:02d}",
        "```",
        "",
        f"**Focus:** {focus}",
        "",
        "### Step 1 – Skeleton",
        "",
        "```bash",
        "cat > lab.py << 'EOF'",
        "#!/usr/bin/env python3",
        f'print("lab{num:02d} {slug}")',
        "EOF",
        "chmod +x lab.py",
        "python3 lab.py",
        "```",
    ]
    if extra:
        parts.extend(["", extra])
    parts.extend(
        [
            "",
            "### Final step – Cleanup note",
            "",
            "```bash",
            "python3 lab.py",
            "# keep ~/rebash-python for later labs",
            "```",
        ]
    )
    return "\n".join(parts)


def render(sp: tuple) -> str:
    (
        num,
        slug,
        title,
        module,
        difficulty,
        minutes,
        diagram,
        tag_extra,
        desc,
        overview,
        theory,
        lab_focus,
    ) = sp
    tags = ["python", *tag_extra]
    tag_yaml = "\n".join(f"  - {t}" for t in tags)
    prev_title = SPEC[num - 2][2] if num > 1 else "Shell Scripting foundations"
    prereq = [
        prev_title if num > 1 else "Linux essentials and Shell Scripting Module 1–2 recommended",
        "Python 3.12+ on Linux (WSL2/VM/cloud)",
    ]
    objectives = [
        f"Apply the core ideas of “{title}” in real ops automation",
        "Use a project venv and avoid relying on system site-packages",
        "Produce clear stderr diagnostics and meaningful exit codes",
        "Prefer safe patterns (pathlib, subprocess list args, dry-run)",
        "Relate this topic to day-to-day DevOps and platform work",
    ]
    obj = "\n".join(f"- [ ] {o}" for o in objectives)
    pr = "\n".join(f"- {p}" for p in prereq)
    pr_yaml = "\n".join(f"  - {p}" for p in prereq)

    return f"""---
title: "{title}"
description: "{desc}"
difficulty: {difficulty}
estimated_time: "{minutes}"
author: {AUTHOR}
last_updated: "{DATE}"
category: python
tags:
{tag_yaml}
prerequisites:
{pr_yaml}
comments: false
---

# {title}

## Overview

{overview}

This is **Tutorial {num}** in **{module}** of the REBASH Academy Python for DevOps series — written for Linux administrators and DevOps engineers who automate infrastructure with production-quality Python.

## Prerequisites

{pr}

## Learning Objectives

By the end of this tutorial, you will be able to:

{obj}

## Architecture

Ops Python sits between operators/CI and platforms (files, APIs, CLIs). This topic’s control points are shown below.

![Architecture diagram for {title}](../assets/images/{diagram}.svg)

## Theory

{theory.strip()}

## Hands-on Lab

{lab_block(num, slug, lab_focus).rstrip()}

## Validation

- [ ] Lab code runs in a dedicated workspace under `~/rebash-python/`
- [ ] Failure path exits non-zero and prints diagnostics to stderr
- [ ] You can explain dry-run / fixture behaviour where relevant
- [ ] You can explain this topic to a teammate without opening notes

## Code Walkthrough

Production Python for **{title}** always combines:

1. A clear entry point (`main()` + `if __name__ == "__main__"`)
2. A project virtual environment and pinned dependencies when third-party libs are used
3. Explicit error handling and logging (no silent `except Exception: pass`)
4. Safe I/O: `pathlib`, timeouts on HTTP, `subprocess.run([...])` without `shell=True`
5. Documented exit codes and dry-run defaults for mutating actions

Keep modules short enough to review in a single merge request. Prefer stdlib first; add httpx, Typer, pytest, and platform SDKs when the job needs them.

## Security Considerations

- Treat all external input (args, files, env, API payloads) as untrusted until validated
- Never log secrets or `Authorization` headers; prefer masked CI variables
- Prefer least privilege tokens and read-only / dry-run modes by default
- Avoid `shell=True`, unvalidated path deletes, and committing `.env` files
- Pin dependencies; review transitive packages for automation that runs in CI

## Common Mistakes

!!! warning "Using system Python without a venv"
    Global packages drift between laptops and CI. **Fix:** `python3 -m venv .venv` per project and pin dependencies.

!!! warning "Calling subprocess with shell=True"
    Untrusted strings become remote code execution. **Fix:** pass a list of arguments; never build a shell string for the happy path.

!!! warning "Mutating without dry-run"
    Cleanup and apply tools destroy shared environments. **Fix:** default to dry-run; require `--apply` for side effects.

## Best Practices

- One purpose per command; share helpers in a small library package
- Log to stderr; reserve stdout for data or RESULT lines
- Idempotent behaviour where schedulers and CI may retry
- Fixture / mock paths for GitHub, Docker, Kubernetes, and Terraform in CI
- Pair every new tool with at least one failing-path test you actually run

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `ModuleNotFoundError` in CI | Missing venv / pins | Recreate venv; install from lock/requirements |
| Works locally, fails in pipeline | Different Python or env | Pin `requires-python`; fingerprint env in the job |
| Hang on HTTP call | No timeout | Set `timeout=` on httpx/requests clients |
| Secrets in logs | Debug printing headers | Redact; never log tokens |
| Accidental prune/delete | No dry-run default | Default dry-run; label lab resources |

## Summary

**{title}** is a core skill for DevOps engineers automating real hosts, APIs, and pipelines with Python. Practise the lab until the failure path and dry-run path are as familiar as the happy path, then continue the track.

## Interview Questions

1. When would you choose Python over Bash for this kind of ops task?
2. What failure mode appears if you skip a venv, pinning, or dry-run here?
3. How would you test this behaviour in CI without live cloud credentials?
4. Where could secrets leak in a naive implementation of this topic?
5. What exit code contract would you document for teammates?

!!! tip "Sample answer — question 2"
    Floating dependencies and missing dry-run defaults create “works on my machine” automation that either breaks overnight or mutates shared infrastructure unexpectedly. Pin versions and default to report-only.

## Related Tutorials

{related(num)}

## References

- [Python 3 documentation](https://docs.python.org/3/)
- [httpx documentation](https://www.python-httpx.org/)
- Track index: [Python for DevOps](index.md)
"""


def write_diagrams() -> tuple[int, int, list[str]]:
    """Write D2 sources and render SVGs when d2 is available."""
    D2_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    d2_count = 0
    svg_count = 0
    errors: list[str] = []
    d2_bin = shutil.which("d2")
    for name, source in DIAGRAMS.items():
        d2_path = D2_DIR / f"{name}.d2"
        d2_path.write_text(source.lstrip("\n"), encoding="utf-8")
        d2_count += 1
        print(f"wrote {d2_path.relative_to(ROOT)}")
        svg_path = IMG_DIR / f"{name}.svg"
        if not d2_bin:
            errors.append(f"d2 not found; skipped SVG for {name}")
            continue
        try:
            subprocess.run(
                [
                    d2_bin,
                    "--theme",
                    "3",
                    "--layout",
                    "dagre",
                    "--pad",
                    "48",
                    str(d2_path),
                    str(svg_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            svg_count += 1
            print(f"wrote {svg_path.relative_to(ROOT)}")
        except subprocess.CalledProcessError as exc:
            err = (exc.stderr or exc.stdout or str(exc)).strip()
            errors.append(f"d2 failed for {name}: {err}")
    return d2_count, svg_count, errors


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assert len(SPEC) == 26, len(SPEC)
    assert len(DIAGRAMS) == 26, len(DIAGRAMS)
    for sp in SPEC:
        diagram = sp[6]
        assert diagram in DIAGRAMS, diagram
        path = OUT / f"{sp[1]}.md"
        path.write_text(render(sp), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    print(f"done: {len(SPEC)} tutorials")
    d2_count, svg_count, errors = write_diagrams()
    print(f"diagrams: d2={d2_count} svg={svg_count}")
    for e in errors:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
