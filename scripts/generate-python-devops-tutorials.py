#!/usr/bin/env python3
"""Generate REBASH Academy Python for DevOps Engineers tutorials 1–27 under docs/python/."""

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
        "python-fundamentals-install-venv-and-tooling",
        "Python Fundamentals — Install, venv, and Tooling",
        "Module 1: Python Fundamentals",
        "beginner",
        "50 min",
        "python-execution-flow",
        ["fundamentals", "venv", "uv", "poetry"],
        "What Python is for DevOps, how to install and version it, IDE setup, virtual environments, and package tools pip, uv, and Poetry.",
        "Cloud VMs, CI runners, and automation hosts need a reproducible Python. This tutorial builds the install and tooling baseline every later module assumes.",
        """### What is Python?

**Python** is a high-level, interpreted language with a large standard library and an ecosystem of SDKs for cloud, Kubernetes, Docker, and HTTP. For DevOps it is the layer that owns structured data (JSON/YAML), APIs, tests, and packaged CLIs — while Bash remains the launcher and glue.

Python is **not** a general “learn every language feature” course here. You will use it to automate infrastructure safely.

### Installing Python

On Linux prefer the distro package or a managed installer that gives **Python 3.12+**:

```bash
python3 --version
command -v python3
```

Cloud tip: pin the image Python or install via `deadsnakes` / `pyenv` only when the base image is too old. Never overwrite the system interpreter that package managers depend on.

### Python Versions

Use **3.12+** for this course. Check `sys.version_info` in scripts. Avoid writing for 2.x. When targeting fleet hosts, set `requires-python` in `pyproject.toml` so CI fails early on the wrong interpreter.

### Python Interpreter

The **interpreter** reads source (or bytecode) and executes it. `#!/usr/bin/env python3` resolves `python3` from `PATH`. Prefer `python3 -m pip` / `python3 -m venv` so you always target the intended binary.

### VS Code Setup

Install the official Python extension, select the workspace `.venv` interpreter, enable format-on-save (Ruff or Black), and open the lab folder as the workspace root so relative paths match CI.

### PyCharm Setup

Create a project pointing at the lab directory, configure a **Virtualenv** interpreter from `.venv`, and mark `src` as Sources Root when you adopt a package layout later.

### Virtual Environments

A **virtual environment** isolates project packages from the system site-packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Always activate (or call `.venv/bin/python`) before installing or running tools. Commit a lock/requirements file; do not commit `.venv`.

### pip

**pip** installs packages into the active environment. Prefer pins:

```bash
python -m pip install 'httpx==0.28.1'
python -m pip freeze > requirements.txt
```

Use `python -m pip` so you never hit a mismatched `pip` on `PATH`.

### uv

**uv** is a fast installer/resolver. Useful patterns:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Use uv when you want quick, reproducible installs in CI; keep the same pins as teammates.

### Poetry

**Poetry** manages `pyproject.toml`, virtualenvs, and lockfiles together. For ops CLIs that you publish internally, Poetry (or hatch/uv) is fine — pick one tool per repo and document it. This course defaults to `venv` + pinned `requirements.txt` unless a module says otherwise.
""",
        "install/fingerprint Python; create venv; compare pip vs uv install of a pinned package",
    ),
    (
        2,
        "python-basics-types-and-io",
        "Python Basics — Types and I/O",
        "Module 2: Python Basics",
        "beginner",
        "45 min",
        "python-basics-types",
        ["basics", "types", "io"],
        "Variables, data types, operators, strings, numbers, booleans, input/output, and type conversion for ops scripts.",
        "Ops scripts fail when types and I/O are sloppy. Master the basics before control flow and APIs.",
        """### Variables

Assign with `name = value`. Names are case-sensitive. Prefer `snake_case` for locals and functions; `UPPER_SNAKE` for module-level constants. Avoid single-letter names except short loop indices.

### Data Types

Common ops types: `str`, `int`, `float`, `bool`, `list`, `dict`, `tuple`, `None`. Use `type(x)` sparingly in debugging; prefer type hints on public functions.

### Operators

Arithmetic (`+ - * / // % **`), comparison (`== != < > <= >=`), logical (`and or not`), membership (`in`), identity (`is` / `is not` — use for `None`). Prefer `//` for integer division in counters.

### Strings

Strings are immutable. Prefer f-strings for logs: `f"host={host}"`. Methods: `strip`, `split`, `join`, `startswith`, `endswith`, `replace`. Never build shell commands by concatenating untrusted strings.

### Numbers

`int` for counts and exit codes; `float` for ratios. Beware float equality — compare with tolerances when parsing metrics. Exit codes stay integers 0–255.

### Booleans

`True` / `False`. Truthiness: empty `""`, `[]`, `{}`, `0`, and `None` are false. Prefer explicit checks for ops flags: `if dry_run is True`.

### Input

`input()` reads a line from stdin (interactive labs only). Production tools prefer CLI args (`sys.argv` / argparse) and environment variables — never block a cron job on `input()`.

### Output

`print(...)` writes to stdout. Diagnostics belong on stderr:

```python
print("RESULT ok")
print("progress...", file=sys.stderr)
```

Keep machine-readable results on stdout so pipes stay clean.

### Type Conversion

`int("42")`, `str(3)`, `bool(1)`, `float("1.5")`. Wrap conversions in `try`/`except ValueError` when parsing external text. Prefer `pathlib.Path` over raw strings for filesystem paths (Module 7).
""",
        "types and operators drills; stderr vs stdout; safe int conversion helper",
    ),
    (
        3,
        "control-flow-conditionals-and-loops",
        "Control Flow — Conditionals and Loops",
        "Module 3: Control Flow",
        "beginner",
        "45 min",
        "python-control-flow",
        ["control-flow", "match", "loops"],
        "Branch and iterate with if/elif/else, match, for, while, break, continue, and pass in ops automation.",
        "Health checks and CLI verbs are mostly control flow. Get branching and loops right before larger frameworks.",
        """### if

```python
if code != 0:
    print("failed", file=sys.stderr)
    raise SystemExit(code)
```

Use guard clauses early so the happy path stays left-aligned.

### elif

Chain mutually exclusive conditions with `elif`. Prefer dictionaries or `match` when the set of verbs grows.

### else

`else` covers the remaining case. On loops, `for`/`while`…`else` runs only if no `break` — rarely useful in ops scripts; prefer explicit flags.

### match

Python 3.10+ structural pattern matching suits CLI verbs and status enums:

```python
match verb:
    case "check" | "status":
        return check()
    case "apply":
        return apply(dry_run=False)
    case _:
        raise SystemExit(f"unknown verb: {verb}")
```

### for

Iterate collections and ranges: `for host in hosts:`, `for line in path.open():`. Prefer iterating files line-by-line over `read().splitlines()` for large logs.

### while

Use `while` for retries and poll loops with a clear exit:

```python
attempts = 0
while attempts < 3:
    if probe():
        break
    attempts += 1
```

Avoid infinite loops without a timeout.

### break

Exit the nearest loop immediately — useful when a host is healthy or a fatal error appears.

### continue

Skip to the next iteration — skip blank lines, comments, or dry-run-only hosts.

### pass

A no-op placeholder. Prefer real stubs that raise `NotImplementedError` in production code so unfinished paths fail loudly.
""",
        "classify log levels with if/match; retry loop with break/continue",
    ),
    (
        4,
        "functions-parameters-and-scope",
        "Functions — Parameters and Scope",
        "Module 4: Functions",
        "beginner",
        "45 min",
        "python-functions-scope",
        ["functions", "lambda", "scope"],
        "Define reusable ops helpers with parameters, returns, default/keyword/variable arguments, lambdas, and scope rules.",
        "Readable automation is small functions with clear contracts — inputs, side effects, and exit behaviour.",
        """### Functions

```python
def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)
```

Name functions as verbs. Keep side effects obvious; pure helpers are easier to test.

### Parameters

Positional parameters are required unless they have defaults. Annotate types on public APIs. Validate early and fail with stderr + non-zero exit.

### Return Values

Prefer returning data (`dict`, `Path`, `int` status) from library functions and reserve `SystemExit` for CLI entry points. Returning `None` implicitly is fine for mutators that only log.

### Default Arguments

Defaults are evaluated once at definition time — never use mutable defaults (`list`, `dict`). Use `None` and create inside:

```python
def collect(items: list[str] | None = None) -> list[str]:
    items = list(items or [])
    return items
```

### Keyword Arguments

Call with names for clarity: `run(cmd, dry_run=True, timeout=30)`. Force keyword-only with `*` in the signature when flags must not be positional.

### Variable Arguments

`*args` and `**kwargs` forward to lower layers — use sparingly and document. Prefer explicit parameters for ops flags teammates must discover.

### Lambda Functions

`lambda x: x["name"]` suits short `key=` / `sort` hooks. Prefer `def` for anything with branching or more than one expression.

### Scope

LEGB: Local → Enclosing → Global → Built-in. Avoid `global` in ops tools. Pass state as parameters or use a small class/dataclass (Module 9).
""",
        "die/classify helpers; keyword-only dry_run; demonstrate scope pitfalls",
    ),
    (
        5,
        "data-structures-comprehensions-and-generators",
        "Data Structures — Comprehensions and Generators",
        "Module 5: Data Structures",
        "beginner",
        "50 min",
        "python-data-structures",
        ["lists", "dicts", "generators"],
        "Lists, tuples, dictionaries, sets, comprehensions, iterators, and generators for inventory and log processing.",
        "Inventories, labels, and log streams are collections. Choose the right structure and stream large data with generators.",
        """### Lists

Ordered, mutable sequences: `hosts = ["web01", "web02"]`. Methods: `append`, `extend`, `sort`, `pop`. Use lists for ordered inventories and CLI argument lists for `subprocess`.

### Tuples

Immutable sequences — good for fixed records: `("web", 8080)`. Prefer tuples as dict keys when you need composite keys.

### Dictionaries

Key/value maps for JSON-like configs and inventories: `{"name": "api", "replicas": 2}`. Prefer `.get(key, default)` and validate required keys explicitly.

### Sets

Unordered unique membership: useful for comparing desired vs actual host sets (`desired - actual`).

### List Comprehensions

```python
failed = [h for h in hosts if h["status"] != "ok"]
```

Keep them readable; nest sparingly. Prefer generator expressions for large streams.

### Dictionary Comprehensions

```python
by_name = {h["name"]: h for h in hosts}
```

Ideal for indexing inventories after a cloud SDK call.

### Iterators

Objects supporting `__iter__` / `__next__`. Files, `range`, and dict views are iterators — they stream without loading everything into memory.

### Generators

Functions with `yield` produce values lazily — perfect for multi-gigabyte logs:

```python
def lines(path: Path):
    with path.open() as fh:
        for line in fh:
            yield line.rstrip("\\n")
```
""",
        "build inventory list/dict/set; stream a log with a generator",
    ),
    (
        6,
        "modules-packages-and-dependencies",
        "Modules, Packages, and Dependencies",
        "Module 6: Modules & Packages",
        "beginner",
        "45 min",
        "python-package-architecture",
        ["modules", "packages", "dependencies"],
        "Import mechanics, the standard library, custom modules, packages, and dependency management for ops tools.",
        "A single 800-line script becomes unreviewable. Split into packages and pin dependencies early.",
        """### import

```python
import json
from pathlib import Path
from mytool.lib.meta import fingerprint
```

Prefer absolute imports inside a package. Avoid `from module import *`.

### Standard Library

Reach for stdlib first: `pathlib`, `json`, `subprocess`, `logging`, `argparse`, `tempfile`, `dataclasses`, `concurrent.futures`. Add third-party libraries only when they clearly reduce risk or complexity.

### Custom Modules

A module is a `.py` file. Put shared helpers in `lib/` and keep `cli.py` thin. Use `if __name__ == "__main__":` only at entry points.

### Packages

A **package** is a directory with `__init__.py` (or a native namespace package). Layout that scales:

```text
tool/
  pyproject.toml
  src/tool/
    __init__.py
    cli.py
    lib/
  tests/
```

### Dependency Management

Pin versions in `requirements.txt` or a lockfile. Install only inside a venv. Separate runtime vs optional extras (`[dev]` for pytest). Never commit secrets; do commit the lock so CI and laptops match.
""",
        "create a tiny package with cli + lib; pin one dependency in requirements.txt",
    ),
    (
        7,
        "file-handling-pathlib-json-yaml-csv",
        "File Handling — pathlib, JSON, YAML, CSV",
        "Module 7: File Handling",
        "beginner",
        "55 min",
        "python-file-handling",
        ["pathlib", "json", "yaml", "csv"],
        "Read and write files safely with pathlib, CSV, JSON, YAML, XML, shutil, and temporary files.",
        "Configs and inventories live on disk. Parse them safely, validate keys, and write atomically.",
        """### Reading Files

Prefer `pathlib.Path`:

```python
text = Path("config.json").read_text(encoding="utf-8")
```

Always set encoding. For large logs, iterate lines instead of `read_text()`.

### Writing Files

Write to a temp file then `replace` for atomic updates. Set restrictive permissions on secret-bearing files (`0o600`).

### CSV

Use the `csv` module for inventory exports — do not split on commas by hand. Prefer DictReader/DictWriter with explicit fieldnames.

### JSON

`json.loads` / `json.dumps` / `json.load` / `json.dump`. Validate required keys after parse. Pretty-print with `indent=2` for human reports.

### YAML

Use **PyYAML** `safe_load` / `safe_dump` — never `yaml.load` without a Loader. Treat YAML as untrusted input from Git.

### XML

Prefer `xml.etree.ElementTree` for simple manifests; avoid `xml` packages that resolve external entities unsafely. Many ops tools should prefer JSON/YAML over XML.

### pathlib

`Path`, `/` join, `.resolve()`, `.exists()`, `.glob()`, `.write_text()`. Resolve then check a path stays under an allow-listed root before deletes.

### shutil

`shutil.copy2`, `move`, `rmtree`, `which`. Wrap destructive calls behind `--apply` / dry-run defaults.

### Temporary Files

`tempfile.TemporaryDirectory` and `NamedTemporaryFile` for scratch space — always clean up, preferably via context managers.
""",
        "JSON + YAML validators; CSV inventory round-trip; tempfile + atomic write",
    ),
    (
        8,
        "error-handling-and-exceptions",
        "Error Handling and Exceptions",
        "Module 8: Error Handling",
        "intermediate",
        "45 min",
        "python-error-handling",
        ["exceptions", "defensive"],
        "Exceptions, try/except/finally/raise, custom exceptions, and defensive programming for reliable automation.",
        "Silent `except Exception: pass` hides outages. Make failure modes visible and actionable.",
        """### Exceptions

Exceptions signal failure. Ops tools should catch **specific** types near the edge (I/O, HTTP, parse) and translate them into stderr messages + exit codes.

### try

Wrap only the statements that can fail for a known reason. Keep `try` blocks small.

### except

```python
try:
    data = json.loads(raw)
except json.JSONDecodeError as exc:
    print(f"invalid JSON: {exc}", file=sys.stderr)
    raise SystemExit(2) from exc
```

Never bare `except:`. Avoid catching `Exception` unless you re-raise or exit immediately after logging.

### finally

Runs for cleanup (close files, release locks) whether or not an error occurred. Prefer `with` context managers when possible.

### raise

Re-raise with `raise` or chain with `raise NewError(...) from exc` to preserve context. Raise early on invalid inputs (fail fast).

### Custom Exceptions

```python
class ConfigError(Exception):
    pass  # domain error for invalid or incomplete configuration
```

Use custom types for domain failures teammates can catch selectively.

### Defensive Programming

Validate inputs, set timeouts, default to dry-run for mutations, check return codes, and assume networks lie. Prefer explicit preconditions over hoping callers behave.
""",
        "parse JSON with specific except; custom ConfigError; finally/cleanup demo",
    ),
    (
        9,
        "oop-classes-and-dataclasses",
        "OOP — Classes and Dataclasses",
        "Module 9: Object-Oriented Programming",
        "intermediate",
        "50 min",
        "python-oop-dataclasses",
        ["oop", "dataclasses"],
        "Classes, objects, methods, constructors, inheritance, encapsulation, polymorphism, and dataclasses for ops models.",
        "Inventories and clients benefit from small typed models — not deep inheritance trees.",
        """### Classes

A **class** defines a blueprint. Prefer composition over deep hierarchies for automation clients.

### Objects

An **object** is an instance. Keep instances immutable when they represent snapshots (inventory rows).

### Methods

Instance methods take `self`. Use `@staticmethod` / `@classmethod` sparingly. Keep methods short and side-effect explicit.

### Constructors

`__init__` validates and stores state. Fail in `__init__` if required config is missing rather than failing later in obscure methods.

### Inheritance

Share behaviour carefully (`BaseClient` → `GitHubClient`). Prefer protocols/duck typing when a single method is shared.

### Encapsulation

Prefix internal helpers with `_`. Do not expose raw tokens as public attributes — store and redact.

### Polymorphism

Call the same method name across client types (`inventory()`, `health()`). Useful for multi-cloud inventory CLIs.

### Dataclasses

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Host:
    name: str
    env: str
    healthy: bool
```

Prefer dataclasses for structured records you serialise to JSON.
""",
        "Host dataclass; small Client class with dry_run; JSON serialise hosts",
    ),
    (
        10,
        "logging-and-debugging",
        "Logging and Debugging",
        "Module 10: Logging & Debugging",
        "intermediate",
        "45 min",
        "python-logging-debug",
        ["logging", "pdb", "debug"],
        "logging module, log levels, structured logging, pdb, tracebacks, and practical debugging techniques.",
        "CI and cron have no interactive terminal. Logs and disciplined debugging replace print archaeology.",
        """### logging

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("rebash")
```

Prefer the logging module over ad-hoc prints for libraries; CLIs may still print RESULT lines to stdout.

### Log Levels

DEBUG, INFO, WARNING, ERROR, CRITICAL. Default INFO in production; DEBUG behind a `--verbose` flag.

### Structured Logging

Emit key=value or JSON fields: `host=web01 status=down`. Makes Loki/ELK queries possible. Never log secrets or tokens.

### pdb

`python -m pdb script.py` or `breakpoint()` for interactive sessions. Do not leave breakpoints in CI code.

### Tracebacks

Unhandled exceptions print tracebacks to stderr — good. Catch-and-swallow hides them. Use `logging.exception(...)` inside handlers.

### Debugging Techniques

Reproduce with a minimal env, binary-search inputs, add temporary DEBUG logs, run under `pytest -vv`, compare working/failing configs, and capture `repr()` of parsed data.
""",
        "configure logging levels; provoke a traceback; use breakpoint only locally",
    ),
    (
        11,
        "configuration-management-and-secrets",
        "Configuration Management and Secrets",
        "Module 11: Configuration Management",
        "intermediate",
        "50 min",
        "python-config-secrets",
        ["config", "dotenv", "secrets"],
        "Environment variables, dotenv, YAML/JSON/TOML configs, and secret handling for automation.",
        "Config belongs in files and env; secrets belong in a secret store — never in Git.",
        """### Environment Variables

Read with `os.environ.get("API_URL")` or `os.environ["REQUIRED"]` (raises KeyError). Document required vars in README. Prefer explicit fail on missing secrets.

### dotenv

`python-dotenv` loads `.env` for local labs. Add `.env` to `.gitignore`. Never commit credentials. In CI, inject secrets as masked variables instead.

### YAML

Human-friendly service configs — parse with `safe_load`, validate schema keys, reject unknown dangerous fields.

### JSON

Machine-friendly configs and API fixtures. Same validation rules as Module 7.

### TOML

`tomllib` (3.11+) reads `pyproject.toml` and tool configs. Good for packaging metadata and static tool settings.

### Configuration Files

Layering: defaults < file < env < CLI flags. Document precedence. Fail if conflicting sources disagree on critical safety flags.

### Secret Handling

Load secrets at runtime, keep them in memory briefly, never log them, never write them to world-readable files, rotate tokens, and prefer cloud secret managers in production.
""",
        "layered config (JSON + env); .env gitignore pattern; redact secrets in logs",
    ),
    (
        12,
        "cli-applications-argparse-click-typer",
        "CLI Applications — argparse, Click, and Typer",
        "Module 12: CLI Applications",
        "intermediate",
        "55 min",
        "python-cli-apps",
        ["argparse", "click", "typer", "rich"],
        "Build operator-friendly CLIs with argparse, Click, Typer, Rich, progress bars, and interactive patterns.",
        "Ops tools are CLIs first. Clear flags, dry-run defaults, and readable output beat clever frameworks.",
        """### argparse

Stdlib CLI parser — zero dependencies. Use subparsers for verbs (`check`, `apply`). Default mutating actions to dry-run / require `--apply`.

### Click

Decorator-based CLIs with nice help text and option types. Common in older ops tools. Still excellent for nested command groups.

### Typer

Built on Click with type-hint driven options — modern default for new internal CLIs. Generates help from annotations.

### Rich

Pretty tables, panels, and colour for human terminals. Detect non-TTY (CI) and fall back to plain text.

### Progress Bars

Use Rich/tqdm for long inventories — disable or simplify when stdout is piped. Never mix progress paint with machine-readable JSON on the same stream.

### Interactive CLI Applications

Prompts are fine for human installers; disable them in CI with flags/`CI=true`. Never require interactive confirmation for scheduled jobs — use explicit `--apply`.
""",
        "argparse subcommands with --apply; optional Typer/Rich table if installed",
    ),
    (
        13,
        "linux-automation-subprocess-and-psutil",
        "Linux Automation — subprocess and psutil",
        "Module 13: Linux Automation",
        "intermediate",
        "55 min",
        "python-linux-automation",
        ["subprocess", "psutil", "linux"],
        "Drive Linux safely with subprocess, os, pathlib, shutil, signal, psutil, process management, and permissions — never shell=True on the happy path.",
        "Python should call system tools with argument lists, timeouts, and captured stderr — not by building shell strings.",
        """### subprocess

```python
subprocess.run(["systemctl", "is-active", "nginx"], check=False, capture_output=True, text=True, timeout=30)
```

Pass a **list** of args. Set `timeout`. Inspect `returncode`, `stdout`, `stderr`.

### os

Environment, getuid, and low-level helpers. Prefer `pathlib` for paths. Use `os.environ` copies carefully when spawning children.

### pathlib

Resolve and validate paths before mutating. Combine with subprocess for tools that need path arguments.

### shutil

Copy/move/which — wrap deletes behind dry-run. `shutil.which("kubectl")` before assuming binaries exist.

### signal

Handle SIGTERM/SIGINT for graceful shutdown of long pollers. Register handlers that set a stop flag rather than ignoring signals.

### psutil

Cross-platform process and host metrics (CPU, memory, connections). Ideal for Linux health checkers when available; degrade gracefully if missing.

### Process Management

List, inspect, and — carefully — terminate processes. Prefer signalling your own children. Never kill by fuzzy name match in production without allow-lists.

### File Permissions

Inspect with `Path.stat().st_mode`; set with `chmod`. Secret files should be `0o600`. Refuse to run if a private key is group/world-readable.

**CRITICAL:** never use `shell=True` on the happy path. If you must for a legacy one-liner, pass a constant string and never interpolate untrusted input.
""",
        "Linux health checker with subprocess list args + optional psutil; prove no shell=True",
    ),
    (
        14,
        "rest-apis-requests-auth-and-resilience",
        "REST APIs — requests, Auth, and Resilience",
        "Module 14: REST APIs",
        "intermediate",
        "55 min",
        "python-rest-api-flow",
        ["requests", "httpx", "auth", "apis"],
        "Call HTTP APIs with requests (and httpx), covering methods, auth, OAuth, tokens, pagination, rate limits, and errors.",
        "Most DevOps glue is HTTP. Timeouts, auth hygiene, and pagination decide whether automation is production-ready.",
        """### requests

Popular sync HTTP client. Always set `timeout=`. Prefer sessions for connection pooling.

Also know **httpx** — modern alternative with sync/async APIs and explicit timeouts; many new tools choose httpx. Patterns below apply to both.

### HTTP Methods

GET for reads, POST/PUT/PATCH for writes, DELETE for removals. Use GET for health checks and inventory; require dry-run before destructive methods.

### Authentication

Basic, bearer tokens, and header API keys. Load secrets from env. Never hard-code credentials in source.

### OAuth

OAuth 2.0 client-credentials or device flows for cloud APIs. Store refresh tokens securely; rotate on revoke.

### Tokens

Short-lived tokens beat long-lived PATs when possible. Scope tokens to least privilege (read-only inventory vs write).

### Pagination

Follow `Link` headers or `next` cursors until exhausted. Cap pages in labs. Persist progress for huge inventories.

### Rate Limiting

Honour `Retry-After` and 429 responses with exponential backoff and jitter. Centralise retry helpers (Module 24).

### Error Handling

Treat non-2xx as failures unless documented. Log status codes and response IDs — not bodies that may contain secrets.
""",
        "fixture-based API monitor with requests/httpx timeouts, pagination stub, 429 handling",
    ),
    (
        15,
        "cloud-automation-aws-azure-gcp",
        "Cloud Automation — AWS, Azure, and GCP",
        "Module 15: Cloud Automation",
        "intermediate",
        "60 min",
        "python-cloud-automation",
        ["aws", "azure", "gcp", "boto3"],
        "Automate AWS (boto3 EC2/S3/IAM/Lambda), Azure SDK auth/resources, and GCP storage/compute — with dry-run and fixtures when credentials are absent.",
        "Multi-cloud inventory is a classic Python job. Labs must work offline with fixtures so CI never needs live keys.",
        """### boto3

AWS SDK for Python. Use sessions/profiles, never embed access keys in code.

### EC2

Describe instances, tags, and states for inventory. Start/stop only behind `--apply`.

### S3

List buckets/objects; upload artefacts carefully with server-side encryption settings required by policy.

### IAM

Read-only inventory of roles/policies in labs. Privilege changes need human change control.

### Lambda

Invoke or list functions for ops audits. Avoid deploying from ad-hoc laptops — use CI.

### Azure SDK

Use `azure-identity` (`DefaultAzureCredential`) and resource management clients. Same dry-run discipline.

### Authentication (Azure)

Prefer managed identity in cloud; service principals in CI with short-lived secrets.

### Resource Management (Azure)

List resource groups and resources for inventory tools; mutate only with explicit apply flags.

### Google Cloud SDK

Client libraries for GCP services. Application Default Credentials (ADC) in cloud; fixtures in CI.

### Storage (GCP)

Inventory buckets/objects; enforce uniform bucket-level access expectations in checks.

### Compute Engine

List VMs/instances and labels for inventory parity with EC2/Azure VM views.

When credentials are missing, load JSON fixtures and print `mode=fixture` so pipelines stay green.
""",
        "multi-cloud inventory CLI with fixtures + dry-run; no live cloud required",
    ),
    (
        16,
        "git-automation-github-and-gitlab",
        "Git Automation — GitHub and GitLab",
        "Module 16: Git Automation",
        "intermediate",
        "55 min",
        "python-git-automation",
        ["gitpython", "github", "gitlab"],
        "Automate Git with GitPython plus GitHub/GitLab APIs for repos, pull requests, and webhooks.",
        "Repository hygiene and PR automation are high-leverage DevOps Python tasks — always use tokens with least privilege.",
        """### GitPython

Programmatic Git operations (clone, status, commit) when you must. Prefer the `git` CLI via subprocess for simple cases; use GitPython for structured inspection.

### GitHub API

REST/GraphQL via `requests`/`httpx` or PyGithub. List repos, branch protection, and workflow runs. Fixture responses in CI.

### GitLab API

Similar patterns with personal/project access tokens. Normalise fields so one auditor can target either forge.

### Repository Automation

Clone mirrors, enforce README/LICENSE presence, check default branch names, and report drift.

### Pull Requests

Open/list PRs, require reviews, label risk. Never auto-merge from untrusted events without checks.

### Webhooks

Validate signatures, reject replayed events, and keep handlers idempotent. Process asynchronously when work is heavy.
""",
        "GitHub repository auditor against recorded JSON fixtures; optional live dry-run",
    ),
    (
        17,
        "docker-sdk-automation",
        "Docker SDK Automation",
        "Module 17: Docker Automation",
        "intermediate",
        "55 min",
        "python-docker-sdk-workflow",
        ["docker", "sdk", "containers"],
        "Automate Docker with the Python SDK — containers, images, networks, volumes, and registry workflows.",
        "Cleanup and inventory tools prevent disk fill on build agents — default to report-only.",
        """### Docker SDK

`docker` PyPI package talks to the local Docker Engine API. Check the daemon is reachable before work.

### Containers

List/filter containers; stop/remove only with `--apply`. Label lab containers so cleanup is scoped.

### Images

List dangling images; prune behind apply flags. Prefer digest pins in production deploy tools.

### Networks

Inspect custom networks and stale attachments. Avoid deleting networks still in use.

### Volumes

Unused volumes waste disk — report first, delete only when policy allows.

### Registry Automation

Login, push/pull, and tag promotion. Store registry credentials in env/secret stores — never in scripts.
""",
        "Docker cleanup tool: report dangling images/containers; --apply optional",
    ),
    (
        18,
        "kubernetes-python-client-automation",
        "Kubernetes Python Client Automation",
        "Module 18: Kubernetes Automation",
        "intermediate",
        "60 min",
        "python-k8s-client-architecture",
        ["kubernetes", "client", "k8s"],
        "Automate Kubernetes with kubernetes-python-client across Pods, Deployments, Services, ConfigMaps, Secrets, Jobs, and Namespaces.",
        "In-cluster and kubeconfig clients power health and validation tools — never print Secret values.",
        """### kubernetes-python-client

Official client. Load config via `load_kube_config` or `load_incluster_config`. Use fixtures when no cluster is available.

### Pods

List phases, restarts, and not-ready conditions for health reports.

### Deployments

Check desired vs available replicas; validate strategy and labels.

### Services

Verify selectors match Pod labels — a common outage class.

### ConfigMaps

Inventory keys (not necessarily values) for drift detection.

### Secrets

List names/keys only. Never dump values to logs or CI artefacts.

### Jobs

Detect failed Jobs and surface backoff limits for batch ops.

### Namespaces

Scope all queries; refuse cluster-wide destructive actions without explicit flags.
""",
        "Kubernetes health checker using fixtures (or live read-only if kubeconfig present)",
    ),
    (
        19,
        "infrastructure-automation-terraform",
        "Infrastructure Automation — Terraform",
        "Module 19: Infrastructure Automation",
        "intermediate",
        "55 min",
        "python-terraform-automation",
        ["terraform", "cdktf", "iac"],
        "Wrap the Terraform CLI and understand cdktf, validation, plan automation, and state inspection from Python.",
        "Python orchestrates `terraform` safely — it should not reinvent providers. Always plan before apply.",
        """### Terraform CLI

Call `terraform` via subprocess with argument lists: `version`, `init`, `validate`, `plan`, `show`. Pin plugin caches in CI.

### cdktf Overview

**CDK for Terraform (cdktf)** lets you define infra in Python and synthesise Terraform JSON. Use it when teams already live in Python; otherwise HCL remains fine. This course focuses on CLI wrapping first.

### Terraform Validation

`terraform validate` and `fmt -check` in CI wrappers. Fail the pipeline on errors.

### Plan Automation

`terraform plan -out=tfplan` then parse `terraform show -json tfplan` for policy checks. Default to plan-only; apply needs explicit approval.

### State Inspection

`terraform state list` / `show` for audits. Never commit state containing secrets; use remote backends.
""",
        "Terraform wrapper: validate + plan dry-run against a tiny fixture module",
    ),
    (
        20,
        "ssh-automation-paramiko-and-fabric",
        "SSH Automation — Paramiko and Fabric",
        "Module 20: SSH Automation",
        "intermediate",
        "50 min",
        "python-ssh-paramiko",
        ["paramiko", "fabric", "ssh"],
        "Remote execution with Paramiko, Fabric, SCP, SSH keys, and safe remote command patterns.",
        "Bastions and fleets still need SSH automation — key hygiene and timeouts matter as much as the API.",
        """### Paramiko

SSH client library for Python. Prefer key-based auth, set connection timeouts, and reject unknown hosts unless you manage a known_hosts policy deliberately.

### Fabric

Higher-level remote execution built on Paramiko — convenient for multi-host runbooks. Keep commands allow-listed.

### SCP

Copy files with Paramiko SFTP/SCP helpers. Validate remote paths; do not overwrite blindly.

### SSH Keys

Load from agent or files with correct permissions (`0o600`). Never embed private keys in repos.

### Remote Execution

Run remote commands with explicit argv-style strings you control. Capture exit codes. Prefer idempotent remote scripts. Default to a dry-run that only prints intended hosts/commands.
""",
        "Paramiko/Fabric dry-run runner that prints planned remote commands; mock transport if no SSH host",
    ),
    (
        21,
        "concurrency-threads-asyncio-and-futures",
        "Concurrency — Threads, asyncio, and Futures",
        "Module 21: Concurrency",
        "advanced",
        "55 min",
        "python-concurrency",
        ["asyncio", "threads", "futures"],
        "Scale I/O-bound ops with threads, multiprocessing, asyncio, concurrent.futures, and queues.",
        "Inventory fan-out is I/O-bound. Pick the simplest concurrency model that meets the SLA — and bound it.",
        """### Threads

Good for I/O waits (HTTP, SSH). Use `concurrent.futures.ThreadPoolExecutor` with a max worker cap. Mind GIL for CPU-heavy work.

### Multiprocessing

Separate processes for CPU-bound parsing. Higher overhead; serialise carefully.

### asyncio

Async I/O with `async`/`await` and httpx AsyncClient. Ideal for many concurrent API calls in one process. Do not mix blocking SDK calls inside the event loop without executors.

### concurrent.futures

Unified interface for thread/process pools — preferred over raw `threading` for ops tools.

### Queues

`queue.Queue` / `asyncio.Queue` to bound work and decouple producers/consumers. Always set timeouts on `get`/`put`.
""",
        "fan-out HTTP health checks with ThreadPoolExecutor or asyncio; bound workers",
    ),
    (
        22,
        "testing-with-pytest",
        "Testing with pytest",
        "Module 22: Testing",
        "intermediate",
        "55 min",
        "python-pytest-testing",
        ["pytest", "unittest", "mocking"],
        "unittest and pytest, fixtures, mocking, coverage, and integration testing for automation tools.",
        "Untested cleanup tools are outages waiting to happen. Fixture the network and assert dry-run behaviour.",
        """### unittest

Stdlib xUnit style — fine for legacy. New code should prefer pytest.

### pytest

Concise asserts, fixtures, parametrisation, and plugins. Run with `pytest -q` in CI.

### Fixtures

Share temp dirs, sample configs, and fake API responses. Prefer function-scoped fixtures unless expensive setup needs module scope.

### Mocking

`unittest.mock` / `pytest-mock` to stub subprocess, HTTP, and cloud SDKs. Assert call args (especially that `shell=False`).

### Coverage

`pytest --cov` to find untested failure paths. Aim for meaningful coverage of parsers and mutators — not 100% vanity.

### Integration Testing

Optional live tests marked `@pytest.mark.integration` and skipped without credentials. Default CI runs unit/fixture tests only.
""",
        "pytest for a parser + mocked subprocess; coverage on the failure path",
    ),
    (
        23,
        "packaging-pyproject-and-wheels",
        "Packaging — pyproject.toml and Wheels",
        "Module 23: Packaging",
        "intermediate",
        "50 min",
        "python-packaging-wheels",
        ["pyproject", "wheels", "packaging"],
        "Package ops tools with pyproject.toml, wheels, publishing, versioning, and dependency management.",
        "A tool teammates can `pip install` beats a wiki of copy-pasted scripts.",
        """### pyproject.toml

Declare build system, project metadata, scripts/entry points, and optional deps. Single source of truth for modern packaging.

### Wheels

Built distributions (`*.whl`) install fast and reproducibly. Build with `python -m build`.

### Publishing Packages

Publish to a private index (or PyPI) from CI using trusted publishing / tokens. Tag releases from CI, not laptops.

### Versioning

SemVer for APIs; calendar or SemVer for internal CLIs. Single-source version in package metadata.

### Dependency Management

Pin ranges thoughtfully (`>=x,<y`) for libraries; pin exact versions for applications/lockfiles. Separate `[project.optional-dependencies]` for dev/test.
""",
        "minimal pyproject.toml + console script entry; build wheel if build installed",
    ),
    (
        24,
        "production-engineering-patterns",
        "Production Engineering Patterns",
        "Module 24: Production Engineering",
        "advanced",
        "55 min",
        "python-automation-pipeline",
        ["retry", "metrics", "observability"],
        "Retries, exponential backoff, metrics, logging, health checks, performance, memory profiling, and observability.",
        "Production automation expects failure. Encode retry, metrics, and health so operators can trust the tool.",
        """### Retry Logic

Retry transient failures (timeouts, 429, 503) only. Do not retry permanent 4xx validation errors blindly.

### Exponential Backoff

Sleep `base * 2**attempt` with jitter. Cap attempts and total time.

### Metrics

Emit counters/histograms (Prometheus client or statsd) for run duration, failures, and items processed.

### Logging

Correlate with `run_id` fields. Keep INFO lean; use DEBUG for payloads without secrets.

### Health Checks

`/healthz` style functions or CLI `health` verbs that verify deps (disk, API reachability) without side effects.

### Performance

Profile before rewriting. Prefer streaming and bounded concurrency over premature micro-optimisations.

### Memory Profiling

Watch RSS on large inventories; use generators and paginate. `tracemalloc` for leaks in long-running services.

### Observability

Combine logs + metrics + traces where the platform supports OpenTelemetry. Propagate correlation IDs across HTTP calls.
""",
        "retry with backoff helper; health check verb; simple counter metrics to stderr",
    ),
    (
        25,
        "security-for-devops-python",
        "Security for DevOps Python",
        "Module 25: Security",
        "advanced",
        "55 min",
        "python-security-devops",
        ["security", "secrets", "supply-chain"],
        "Secret management, encryption, hashing, secure coding, input validation, dependency scanning, and supply chain security.",
        "Automation runs with powerful credentials. Secure coding and supply-chain hygiene are mandatory.",
        """### Secret Management

Load from env/secret managers; never commit; rotate; scope least privilege; redact logs.

### Encryption

Use TLS for networks. For data at rest, prefer platform KMS. Do not invent crypto — use `cryptography` library primitives correctly.

### Hashing

Prefer `hashlib` for integrity checksums (SHA-256). For passwords, use purpose-built KDFs (bcrypt/argon2) — not raw SHA.

### Secure Coding

No `shell=True`, no `eval`, no `pickle` of untrusted data, no YAML `load` without SafeLoader, path traversal checks before writes/deletes.

### Input Validation

Allow-list hosts, namespaces, and path prefixes. Reject surprising characters in CLI args used for filesystem or shell-adjacent operations.

### Dependency Scanning

Run `pip-audit` / OSV scanners in CI. Fail on known critical CVEs for runtime deps.

### Supply Chain Security

Pin digests where possible, verify signatures when available, prefer trusted indexes, and review new dependencies like production code.
""",
        "secrets scanner for accidental tokens in files; pip-audit if available",
    ),
    (
        26,
        "ai-for-devops-openai-mcp-langchain",
        "AI for DevOps — OpenAI, MCP, and LangChain",
        "Module 26: AI for DevOps",
        "advanced",
        "50 min",
        "python-ai-devops",
        ["openai", "mcp", "langchain", "ai"],
        "OpenAI SDK, MCP clients, LangChain basics, AI-assisted automation, and ops agents — with mocked/offline examples only.",
        "AI can draft runbooks and summarise incidents — but labs must never require real API keys.",
        """### OpenAI SDK

Official client for chat/completions. In this course, call a **mock client** that returns fixture text so CI stays offline.

### MCP Clients

**Model Context Protocol (MCP)** connects assistants to tools (Kubernetes, Terraform, docs). Understand client/server roles; practise with stub tool lists.

### LangChain Basics

Chains/agents that call tools. Use only for well-bounded ops assistants with human approval on mutating tools.

### AI-assisted Automation

Summarise logs, propose kubectl/terraform commands, and draft PRs — always show the plan and require `--apply` / human confirm for side effects.

### AI Agents for Operations

Agents that can call inventory tools are useful; agents that can delete namespaces need strict allow-lists, dry-run defaults, and audit logs. Prefer recommendation over autonomous mutation.
""",
        "mock LLM client summarising a fixture log; no real API keys",
    ),
    (
        27,
        "troubleshooting-python-automation",
        "Troubleshooting Python Automation",
        "Module 27: Troubleshooting",
        "advanced",
        "50 min",
        "python-plugin-architecture",
        ["troubleshooting", "debugging", "production"],
        "Diagnose dependency issues, venv problems, API failures, memory leaks, performance issues, and production debugging — framed with a plugin architecture overview.",
        "When automation fails at 03:00, a checklist beats guesswork. This module closes the loop with systematic debugging and a reusable plugin shape for your toolkit.",
        """### Dependency Issues

`ModuleNotFoundError`, version conflicts, and wrong interpreters. Fix: recreate venv, install from lockfile, fingerprint `sys.executable` in CI logs.

### Virtual Environment Problems

Forgot to activate, nested venvs, or system pip. Always invoke `.venv/bin/python -m pytest`.

### API Failures

Timeouts, 401/403, pagination bugs, and rate limits. Log status + request id; reproduce with fixtures; verify token scopes.

### Memory Leaks

Long-running listeners holding lists of responses. Use generators, clear caches, and `tracemalloc` snapshots.

### Performance Issues

Serial HTTP to thousands of hosts, huge `read_text()`, unbounded thread pools. Bound concurrency and stream data.

### Production Debugging

Capture versions, config provenance (without secrets), recent deploys, and a failing input sample. Prefer feature flags and dry-run to bisect.

### Plugin architecture (framework overview)

A durable ops toolkit uses a small core CLI plus plugins (inventory, k8s, terraform) discovered via entry points — isolating failures to one plugin without breaking the suite.
""",
        "broken-venv checklist; reproduce API failure from fixture; document plugin layout",
    ),
]

assert len(SPEC) == 27, len(SPEC)

OBSOLETE = [
    "introduction-to-python-for-devops.md",
    "syntax-essentials-types-control-flow-functions.md",
    "modules-imports-and-project-layout.md",
    "virtual-environments-and-dependency-pinning.md",
    "errors-exceptions-and-logging-for-ops.md",
    "filesystem-automation-with-pathlib.md",
    "json-and-yaml-for-infrastructure-config.md",
    "regular-expressions-for-log-and-text-ops.md",
    "environment-variables-dotenv-and-secrets-hygiene.md",
    "configuration-management-patterns.md",
    "subprocess-calling-cli-tools-safely.md",
    "building-clis-with-argparse.md",
    "modern-clis-with-typer-or-click.md",
    "rest-apis-with-httpx-and-requests.md",
    "authentication-patterns-for-automation.md",
    "ssh-automation-with-paramiko.md",
    "github-api-automation.md",
    "docker-sdk-images-containers-cleanup.md",
    "kubernetes-python-client-health-checks.md",
    "automating-terraform-workflows.md",
    "python-in-ci-cd-pipelines.md",
    "async-basics-for-io-bound-ops-tools.md",
    "testing-automation-with-pytest.md",
    "packaging-with-pyproject-uv-and-poetry.md",
    "production-patterns-for-devops-python.md",
    "capstone-prep-framework-skeleton.md",
]

STYLE = (
    "*: { style: { border-radius: 14; font-size: 14; bold: true; "
    "shadow: true; stroke-width: 2 } }\n"
    "direction: right\n"
)


def _flow(
    a: str,
    b: str,
    c: str,
    d: str,
    ca: str = "#dbeafe",
    cb: str = "#dcfce7",
    cc: str = "#ffedd5",
    cd: str = "#fce7f3",
    sa: str = "#2563eb",
    sb: str = "#16a34a",
    sc: str = "#ea580c",
    sd: str = "#db2777",
) -> str:
    return dedent(
        f"""\
        {STYLE}A: "{a}" {{ style.fill: "{ca}"; style.stroke: "{sa}" }}
        B: "{b}" {{ style.fill: "{cb}"; style.stroke: "{sb}" }}
        C: "{c}" {{ style.fill: "{cc}"; style.stroke: "{sc}" }}
        D: "{d}" {{ style.fill: "{cd}"; style.stroke: "{sd}" }}
        A -> B -> C -> D
        """
    )


DIAGRAMS: dict[str, str] = {
    "python-execution-flow": _flow(
        "Source .py", "Interpreter", "Bytecode / run", "Exit + stderr"
    ),
    "python-virtual-environment": _flow(
        "python3 -m venv", ".venv isolate", "pip / uv pins", "Ops tool runs"
    ),
    "python-basics-types": _flow(
        "Variables", "Types + operators", "I/O streams", "Conversions"
    ),
    "python-control-flow": _flow(
        "Preconditions", "if / match", "for / while", "break continue"
    ),
    "python-functions-scope": _flow(
        "Call site", "Parameters", "Local scope", "Return / exit"
    ),
    "python-data-structures": _flow(
        "Collections", "Comprehensions", "Iterators", "Generators"
    ),
    "python-package-architecture": _flow(
        "cli entry", "lib modules", "pyproject pins", "tests"
    ),
    "python-file-handling": _flow(
        "pathlib Path", "JSON YAML CSV", "Validate", "Atomic write"
    ),
    "python-error-handling": _flow(
        "Operation", "try / except", "Custom errors", "Exit code"
    ),
    "python-oop-dataclasses": _flow(
        "Class / dataclass", "Instances", "Methods", "JSON models"
    ),
    "python-logging-debug": _flow(
        "Events", "Log levels", "Structured fields", "pdb / traceback"
    ),
    "python-config-secrets": _flow(
        "ENV / files", "Layer merge", "Secret load", "Redacted use"
    ),
    "python-cli-apps": _flow(
        "argv / flags", "argparse Click Typer", "Rich output", "Exit status"
    ),
    "python-linux-automation": _flow(
        "Python tool", "subprocess list", "psutil / fs", "Host state"
    ),
    "python-rest-api-flow": _flow(
        "Client + timeout", "Auth token", "Paginate / retry", "Parsed result"
    ),
    "python-cloud-automation": _flow(
        "Fixtures / creds", "AWS Azure GCP", "Inventory", "Dry-run report"
    ),
    "python-git-automation": _flow(
        "Token + API", "Repos / PRs", "Policy checks", "Webhook verify"
    ),
    "python-docker-sdk-workflow": _flow(
        "Docker SDK", "List resources", "Report orphans", "Apply cleanup"
    ),
    "python-k8s-client-architecture": _flow(
        "kubeconfig / in-cluster", "API client", "Pods Deployments", "Health report"
    ),
    "python-terraform-automation": _flow(
        "Wrapper CLI", "validate / plan", "JSON plan", "Apply gated"
    ),
    "python-ssh-paramiko": _flow(
        "SSH keys", "Paramiko / Fabric", "Remote exec", "SCP result"
    ),
    "python-concurrency": _flow(
        "Work queue", "Threads / asyncio", "Bounded pool", "Aggregated results"
    ),
    "python-pytest-testing": _flow(
        "Fixtures", "pytest cases", "Mocks", "Coverage CI"
    ),
    "python-packaging-wheels": _flow(
        "pyproject.toml", "build wheel", "Publish index", "pip install"
    ),
    "python-automation-pipeline": _flow(
        "Trigger CI / cron", "Retry + metrics", "Health checks", "Observability"
    ),
    "python-security-devops": _flow(
        "Validate input", "Secret hygiene", "Dependency scan", "Supply chain"
    ),
    "python-ai-devops": _flow(
        "Ops event", "Mock LLM / MCP", "Proposed actions", "Human --apply"
    ),
    "python-plugin-architecture": _flow(
        "Core CLI", "Plugin entry points", "Cloud / K8s / TF", "Shared logging"
    ),
}

LAB_EXTRA: dict[int, str] = {
    1: dedent(
        """\
        ### Step 2 – venv and tooling fingerprint

        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        python -m pip install --upgrade pip
        python -m pip install 'packaging==24.2'
        python - <<'PY'
        import platform, sys
        print(f"executable={sys.executable}")
        print(f"version={platform.python_version()}")
        print(f"prefix={sys.prefix}")
        PY
        command -v uv >/dev/null && uv --version || echo 'uv optional'
        command -v poetry >/dev/null && poetry --version || echo 'poetry optional'
        deactivate || true
        ```
        """
    ),
    2: dedent(
        """\
        ### Step 2 – Types and I/O

        ```bash
        cat > basics.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        import sys

        def to_int(raw: str) -> int:
            try:
                return int(raw.strip())
            except ValueError as exc:
                print(f"invalid int: {raw!r}", file=sys.stderr)
                raise SystemExit(2) from exc

        def main(argv: list[str]) -> int:
            if len(argv) < 2:
                print(f"usage: {argv[0]} N", file=sys.stderr)
                return 2
            n = to_int(argv[1])
            print(f"RESULT n={n} doubled={n * 2}")
            print("ok", file=sys.stderr)
            return 0

        if __name__ == "__main__":
            raise SystemExit(main(sys.argv))
        EOF
        python3 basics.py 21
        python3 basics.py nope || echo "exit=$?"
        ```
        """
    ),
    3: dedent(
        """\
        ### Step 2 – Control flow

        ```bash
        cat > flow.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        import sys

        def classify(level: str) -> str:
            match level.upper():
                case "INFO" | "DEBUG":
                    return "low"
                case "WARN" | "WARNING":
                    return "medium"
                case "ERROR" | "CRITICAL":
                    return "high"
                case _:
                    raise ValueError(level)

        def main(argv: list[str]) -> int:
            for raw in argv[1:]:
                if not raw.strip():
                    continue
                try:
                    print(f"{raw}->{classify(raw)}")
                except ValueError:
                    print(f"skip:{raw}", file=sys.stderr)
                    continue
            return 0

        if __name__ == "__main__":
            raise SystemExit(main(sys.argv))
        EOF
        python3 flow.py INFO WARN nope ERROR
        ```
        """
    ),
    4: dedent(
        """\
        ### Step 2 – Functions

        ```bash
        cat > funcs.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        import sys

        def die(msg: str, code: int = 1) -> None:
            print(msg, file=sys.stderr)
            raise SystemExit(code)

        def run(*, dry_run: bool = True, hosts: list[str] | None = None) -> int:
            hosts = list(hosts or [])
            for h in hosts:
                action = "WOULD_CHECK" if dry_run else "CHECK"
                print(f"{action} {h}")
            return 0

        def main(argv: list[str]) -> int:
            if len(argv) < 2:
                die(f"usage: {argv[0]} host [host...]", 2)
            apply = "--apply" in argv
            hosts = [a for a in argv[1:] if a != "--apply"]
            return run(dry_run=not apply, hosts=hosts)

        if __name__ == "__main__":
            raise SystemExit(main(sys.argv))
        EOF
        python3 funcs.py web01 web02
        python3 funcs.py web01 --apply
        ```
        """
    ),
    5: dedent(
        """\
        ### Step 2 – Structures and generators

        ```bash
        cat > inventory.json << 'EOF'
        [{"name":"web","env":"prod"},{"name":"db","env":"prod"},{"name":"bastion","env":"ops"}]
        EOF
        printf 'a\\nb\\na\\n' > sample.log
        cat > structs.py << 'EOF'
        #!/usr/bin/env python3
        import json
        from pathlib import Path

        def lines(path: Path):
            with path.open() as fh:
                for line in fh:
                    yield line.rstrip("\\n")

        hosts = json.loads(Path("inventory.json").read_text())
        by_env = {h["name"]: h["env"] for h in hosts}
        envs = {h["env"] for h in hosts}
        print(by_env)
        print(sorted(envs))
        print(list(lines(Path("sample.log"))))
        EOF
        python3 structs.py
        ```
        """
    ),
    6: dedent(
        """\
        ### Step 2 – Package layout

        ```bash
        mkdir -p demo_tool/lib
        printf '%s\\n' '' > demo_tool/__init__.py
        printf '%s\\n' '' > demo_tool/lib/__init__.py
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
        echo 'PyYAML==6.0.2' > requirements.txt
        PYTHONPATH=. python3 -m demo_tool.cli
        ```
        """
    ),
    7: dedent(
        """\
        ### Step 2 – JSON/YAML validators

        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        python -m pip install -q 'PyYAML==6.0.2'
        cat > good.json << 'EOF'
        {"service":"api","replicas":2}
        EOF
        cat > good.yaml << 'EOF'
        service: api
        replicas: 2
        EOF
        cat > validate.py << 'EOF'
        #!/usr/bin/env python3
        import csv, json, sys, tempfile
        from pathlib import Path
        import yaml

        def need(d: dict, keys: list[str]) -> None:
            missing = [k for k in keys if k not in d]
            if missing:
                raise SystemExit(f"missing keys: {missing}")

        need(json.loads(Path("good.json").read_text()), ["service", "replicas"])
        need(yaml.safe_load(Path("good.yaml").read_text()), ["service", "replicas"])
        with Path("inv.csv").open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["name", "env"])
            w.writeheader()
            w.writerow({"name": "web", "env": "prod"})
        td = tempfile.TemporaryDirectory()
        p = Path(td.name) / "out.json"
        p.write_text(json.dumps({"ok": True}) + "\\n")
        print(p.read_text().strip())
        td.cleanup()
        print("RESULT ok")
        EOF
        python validate.py
        deactivate || true
        ```
        """
    ),
    8: dedent(
        """\
        ### Step 2 – Exceptions

        ```bash
        cat > errors.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        import json, sys
        from pathlib import Path

        class ConfigError(Exception):
            pass

        def load_config(path: Path) -> dict:
            try:
                data = json.loads(path.read_text())
            except FileNotFoundError as exc:
                raise ConfigError(f"missing {path}") from exc
            except json.JSONDecodeError as exc:
                raise ConfigError(f"invalid JSON in {path}") from exc
            if "service" not in data:
                raise ConfigError("service required")
            return data

        def main() -> int:
            Path("bad.json").write_text("{")
            try:
                load_config(Path("bad.json"))
            except ConfigError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 2
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 errors.py || echo "exit=$?"
        ```
        """
    ),
    9: dedent(
        """\
        ### Step 2 – Dataclass inventory

        ```bash
        cat > oop.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        from dataclasses import asdict, dataclass
        import json

        @dataclass(frozen=True)
        class Host:
            name: str
            env: str
            healthy: bool

        class Inventory:
            def __init__(self, dry_run: bool = True) -> None:
                self.dry_run = dry_run
                self._hosts: list[Host] = []

            def add(self, host: Host) -> None:
                self._hosts.append(host)

            def report(self) -> list[dict]:
                return [asdict(h) for h in self._hosts]

        inv = Inventory()
        inv.add(Host("web01", "prod", True))
        print(json.dumps(inv.report(), indent=2))
        EOF
        python3 oop.py
        ```
        """
    ),
    10: dedent(
        """\
        ### Step 2 – Logging

        ```bash
        cat > logdemo.py << 'EOF'
        #!/usr/bin/env python3
        import logging, sys

        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s", stream=sys.stderr)
        log = logging.getLogger("rebash")
        log.info("host=%s status=%s", "web01", "ok")
        try:
            raise RuntimeError("boom")
        except RuntimeError:
            log.exception("probe failed")
        print("RESULT ok")
        EOF
        python3 logdemo.py
        ```
        """
    ),
    11: dedent(
        """\
        ### Step 2 – Config and secrets hygiene

        ```bash
        cat > config.json << 'EOF'
        {"api_url":"https://example.invalid","timeout":5}
        EOF
        cat > .env << 'EOF'
        API_TOKEN=lab-secret-do-not-commit
        EOF
        echo '.env' > .gitignore
        cat > cfg.py << 'EOF'
        #!/usr/bin/env python3
        import json, os, sys
        from pathlib import Path

        def redact(value: str) -> str:
            if len(value) <= 4:
                return "***"
            return value[:2] + "***" + value[-2:]

        cfg = json.loads(Path("config.json").read_text())
        token = os.environ.get("API_TOKEN", "")
        # simulate dotenv without dependency:
        for line in Path(".env").read_text().splitlines():
            if line.startswith("API_TOKEN="):
                token = line.split("=", 1)[1]
        print(f"api_url={cfg['api_url']}")
        print(f"token={redact(token)}", file=sys.stderr)
        print("RESULT ok")
        EOF
        python3 cfg.py
        ```
        """
    ),
    12: dedent(
        """\
        ### Step 2 – argparse CLI

        ```bash
        cat > cli.py << 'EOF'
        #!/usr/bin/env python3
        import argparse

        def main() -> int:
            p = argparse.ArgumentParser(prog="ops")
            sub = p.add_subparsers(dest="cmd", required=True)
            c = sub.add_parser("check")
            c.add_argument("host")
            a = sub.add_parser("apply")
            a.add_argument("host")
            a.add_argument("--apply", action="store_true")
            args = p.parse_args()
            if args.cmd == "check":
                print(f"CHECK {args.host}")
                return 0
            if not args.apply:
                print(f"WOULD_APPLY {args.host}")
                return 0
            print(f"APPLY {args.host}")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 cli.py check web01
        python3 cli.py apply web01
        python3 cli.py apply web01 --apply
        ```
        """
    ),
    13: dedent(
        """\
        ### Step 2 – Linux health checker

        ```bash
        cat > health.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        import shutil, subprocess, sys
        from pathlib import Path

        def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
            return subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=30)

        def main() -> int:
            df = run(["df", "-h", "."])
            print(df.stdout.splitlines()[0] if df.stdout else "df failed")
            which_python = shutil.which("python3")
            print(f"python3={which_python}")
            mode = Path(__file__).stat().st_mode & 0o777
            print(f"mode={oct(mode)}")
            try:
                import psutil  # optional
                print(f"cpu_percent={psutil.cpu_percent(interval=0.1)}")
            except ImportError:
                print("psutil optional — skipped", file=sys.stderr)
            # Explicit: never shell=True
            print("RESULT ok")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 health.py
        ```
        """
    ),
    14: dedent(
        """\
        ### Step 2 – Fixture API monitor

        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        python -m pip install -q 'requests==2.32.3'
        cat > fixture.json << 'EOF'
        {"items":[{"id":1,"ok":true},{"id":2,"ok":false}],"next":null}
        EOF
        cat > monitor.py << 'EOF'
        #!/usr/bin/env python3
        import json, time
        from pathlib import Path

        def fetch_pages(path: Path):
            data = json.loads(path.read_text())
            yield data
            # pagination stub: stop when next is null
            while data.get("next"):
                time.sleep(0.01)
                data = json.loads(Path(data["next"]).read_text())
                yield data

        failed = []
        for page in fetch_pages(Path("fixture.json")):
            for item in page["items"]:
                if not item["ok"]:
                    failed.append(item["id"])
        print(f"RESULT failed={failed}")
        EOF
        python monitor.py
        deactivate || true
        ```
        """
    ),
    15: dedent(
        """\
        ### Step 2 – Multi-cloud inventory fixtures

        ```bash
        mkdir -p fixtures
        cat > fixtures/aws.json << 'EOF'
        {"provider":"aws","instances":[{"id":"i-1","name":"web"}]}
        EOF
        cat > fixtures/azure.json << 'EOF'
        {"provider":"azure","instances":[{"id":"vm-1","name":"api"}]}
        EOF
        cat > fixtures/gcp.json << 'EOF'
        {"provider":"gcp","instances":[{"id":"gce-1","name":"worker"}]}
        EOF
        cat > inventory.py << 'EOF'
        #!/usr/bin/env python3
        import json, os
        from pathlib import Path

        def load(provider: str) -> dict:
            if os.environ.get(f"{provider.upper()}_CREDENTIALS"):
                mode = "live"
            else:
                mode = "fixture"
            data = json.loads(Path(f"fixtures/{provider}.json").read_text())
            data["mode"] = mode
            return data

        for p in ("aws", "azure", "gcp"):
            print(load(p))
        print("RESULT ok")
        EOF
        python3 inventory.py
        ```
        """
    ),
    16: dedent(
        """\
        ### Step 2 – GitHub repo auditor (fixtures)

        ```bash
        cat > repos.json << 'EOF'
        [{"name":"app","default_branch":"main","has_license":true},{"name":"legacy","default_branch":"master","has_license":false}]
        EOF
        cat > auditor.py << 'EOF'
        #!/usr/bin/env python3
        import json
        from pathlib import Path

        repos = json.loads(Path("repos.json").read_text())
        findings = []
        for r in repos:
            if r["default_branch"] != "main":
                findings.append(f"{r['name']}: default_branch={r['default_branch']}")
            if not r["has_license"]:
                findings.append(f"{r['name']}: missing license")
        print("FINDINGS")
        print("\\n".join(findings) or "none")
        print("RESULT ok")
        EOF
        python3 auditor.py
        ```
        """
    ),
    17: dedent(
        """\
        ### Step 2 – Docker cleanup report

        ```bash
        cat > docker_clean.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        import argparse, json

        FIXTURE = {
            "containers": [{"id": "c1", "status": "exited", "names": ["lab_old"]}],
            "images": [{"id": "img1", "dangling": True}],
        }

        def main() -> int:
            p = argparse.ArgumentParser()
            p.add_argument("--apply", action="store_true")
            args = p.parse_args()
            for c in FIXTURE["containers"]:
                verb = "REMOVE" if args.apply else "WOULD_REMOVE"
                print(f"{verb} container {c['id']} {c['names']}")
            for i in FIXTURE["images"]:
                if i["dangling"]:
                    verb = "REMOVE" if args.apply else "WOULD_REMOVE"
                    print(f"{verb} image {i['id']}")
            print("RESULT ok")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 docker_clean.py
        python3 docker_clean.py --apply
        ```
        """
    ),
    18: dedent(
        """\
        ### Step 2 – Kubernetes health fixtures

        ```bash
        cat > pods.json << 'EOF'
        {"items":[{"metadata":{"name":"web-0","namespace":"demo"},"status":{"phase":"Running","containerStatuses":[{"ready":true,"restartCount":0}]}},{"metadata":{"name":"web-1","namespace":"demo"},"status":{"phase":"Running","containerStatuses":[{"ready":false,"restartCount":3}]}}]}
        EOF
        cat > k8s_health.py << 'EOF'
        #!/usr/bin/env python3
        import json
        from pathlib import Path

        data = json.loads(Path("pods.json").read_text())
        bad = []
        for pod in data["items"]:
            name = pod["metadata"]["name"]
            cs = pod["status"]["containerStatuses"][0]
            if not cs["ready"] or cs["restartCount"] > 2:
                bad.append(name)
        print(f"unhealthy={bad}")
        print("RESULT ok")
        EOF
        python3 k8s_health.py
        ```
        """
    ),
    19: dedent(
        """\
        ### Step 2 – Terraform wrapper (dry-run)

        ```bash
        mkdir -p tf
        cat > tf/main.tf << 'EOF'
        terraform {
          required_version = ">= 1.5.0"
        }
        EOF
        cat > tfwrap.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        import shutil, subprocess, sys
        from pathlib import Path

        def run(args: list[str]) -> int:
            print("+", " ".join(args), file=sys.stderr)
            if not shutil.which("terraform"):
                print("terraform not installed — fixture mode", file=sys.stderr)
                print("RESULT validate=skipped plan=skipped")
                return 0
            cp = subprocess.run(args, cwd="tf", text=True)
            return cp.returncode

        def main() -> int:
            code = run(["terraform", "version"])
            if code != 0:
                return code
            # init may be needed; keep lab non-destructive
            run(["terraform", "init", "-backend=false", "-input=false"])
            code = run(["terraform", "validate"])
            print("RESULT ok" if code == 0 else "RESULT fail")
            return code

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 tfwrap.py
        ```
        """
    ),
    20: dedent(
        """\
        ### Step 2 – SSH dry-run planner

        ```bash
        cat > hosts.txt << 'EOF'
        web01.example
        db01.example
        EOF
        cat > ssh_plan.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        import argparse
        from pathlib import Path

        def main() -> int:
            p = argparse.ArgumentParser()
            p.add_argument("--apply", action="store_true")
            p.add_argument("--cmd", default="uname -a")
            args = p.parse_args()
            hosts = [h.strip() for h in Path("hosts.txt").read_text().splitlines() if h.strip()]
            for host in hosts:
                verb = "SSH" if args.apply else "WOULD_SSH"
                print(f"{verb} {host} -- {args.cmd}")
            print("RESULT ok")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 ssh_plan.py
        ```
        """
    ),
    21: dedent(
        """\
        ### Step 2 – Concurrent probes

        ```bash
        cat > concurrent.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import time

        def probe(name: str) -> str:
            time.sleep(0.05)
            return f"{name}=ok"

        def main() -> int:
            hosts = [f"h{i}" for i in range(8)]
            with ThreadPoolExecutor(max_workers=4) as pool:
                futs = {pool.submit(probe, h): h for h in hosts}
                for fut in as_completed(futs):
                    print(fut.result())
            print("RESULT ok")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        python3 concurrent.py
        ```
        """
    ),
    22: dedent(
        """\
        ### Step 2 – pytest

        ```bash
        python3 -m venv .venv && source .venv/bin/activate
        python -m pip install -q 'pytest==8.3.4'
        cat > parse.py << 'EOF'
        def parse_kv(line: str) -> dict[str, str]:
            out = {}
            for part in line.split():
                if "=" in part:
                    k, v = part.split("=", 1)
                    out[k] = v
            return out
        EOF
        cat > test_parse.py << 'EOF'
        from parse import parse_kv

        def test_parse_kv():
            assert parse_kv("host=web status=ok") == {"host": "web", "status": "ok"}

        def test_empty():
            assert parse_kv("") == {}
        EOF
        pytest -q
        deactivate || true
        ```
        """
    ),
    23: dedent(
        """\
        ### Step 2 – Minimal packaging

        ```bash
        mkdir -p src/rebash_lab
        cat > src/rebash_lab/__init__.py << 'EOF'
        __version__ = "0.1.0"
        EOF
        cat > src/rebash_lab/__main__.py << 'EOF'
        def main() -> int:
            print("rebash-lab 0.1.0")
            return 0

        if __name__ == "__main__":
            raise SystemExit(main())
        EOF
        cat > pyproject.toml << 'EOF'
        [project]
        name = "rebash-lab"
        version = "0.1.0"
        description = "Lab package"
        requires-python = ">=3.11"
        [project.scripts]
        rebash-lab = "rebash_lab.__main__:main"
        [build-system]
        requires = ["setuptools>=68"]
        build-backend = "setuptools.build_meta"
        [tool.setuptools.packages.find]
        where = ["src"]
        EOF
        PYTHONPATH=src python3 -m rebash_lab
        python3 -m pip install -q build >/dev/null 2>&1 && python3 -m build || echo 'build optional'
        ```
        """
    ),
    24: dedent(
        """\
        ### Step 2 – Retry and health

        ```bash
        cat > prodpat.py << 'EOF'
        #!/usr/bin/env python3
        from __future__ import annotations
        import random, time, sys

        def retry(fn, *, attempts: int = 4, base: float = 0.01):
            last = None
            for i in range(attempts):
                try:
                    return fn()
                except Exception as exc:  # noqa: BLE001 — lab demo
                    last = exc
                    sleep = base * (2**i) + random.random() * base
                    print(f"retry={i+1} sleep={sleep:.3f}", file=sys.stderr)
                    time.sleep(sleep)
            raise last  # type: ignore[misc]

        def flaky() -> str:
            if random.random() < 0.6:
                raise TimeoutError("transient")
            return "ok"

        def health() -> int:
            print("health=ok")
            return 0

        print(retry(flaky))
        raise SystemExit(health())
        EOF
        python3 prodpat.py
        ```
        """
    ),
    25: dedent(
        """\
        ### Step 2 – Secrets scanner

        ```bash
        mkdir -p sample
        printf 'token = "ghp_EXAMPLESECRETVALUE1234567890"\\n' > sample/bad.py
        printf 'print("hello")\\n' > sample/good.py
        cat > scan.py << 'EOF'
        #!/usr/bin/env python3
        import re
        from pathlib import Path

        PAT = re.compile(r"ghp_[A-Za-z0-9]{20,}")
        findings = []
        for path in Path("sample").rglob("*.py"):
            text = path.read_text()
            if PAT.search(text):
                findings.append(str(path))
        print("findings=", findings)
        print("RESULT ok" if findings else "RESULT clean")
        raise SystemExit(0 if findings else 0)
        EOF
        python3 scan.py
        command -v pip-audit >/dev/null && pip-audit || echo 'pip-audit optional'
        ```
        """
    ),
    26: dedent(
        """\
        ### Step 2 – Mock LLM summary

        ```bash
        cat > incident.log << 'EOF'
        ERROR nginx upstream timed out
        WARN disk 85 percent
        INFO deploy finished
        EOF
        cat > ai_ops.py << 'EOF'
        #!/usr/bin/env python3
        from pathlib import Path

        class MockLLM:
            def summarise(self, text: str) -> str:
                errors = [ln for ln in text.splitlines() if "ERROR" in ln]
                return f"errors={len(errors)}; first={errors[0] if errors else 'none'}"

        log = Path("incident.log").read_text()
        plan = MockLLM().summarise(log)
        print(f"SUMMARY {plan}")
        print("WOULD_NOTIFY slack --apply required for send")
        print("RESULT ok")
        EOF
        python3 ai_ops.py
        ```
        """
    ),
    27: dedent(
        """\
        ### Step 2 – Troubleshoot checklist + plugin sketch

        ```bash
        cat > checklist.md << 'EOF'
        - [ ] Same sys.executable / venv
        - [ ] Lockfile installed
        - [ ] Timeouts on HTTP
        - [ ] Fixture mode without cloud creds
        - [ ] Dry-run default for mutators
        EOF
        mkdir -p plugins
        cat > plugins/inventory.py << 'EOF'
        name = "inventory"

        def run() -> str:
            return "inventory-plugin-ok"
        EOF
        cat > core.py << 'EOF'
        #!/usr/bin/env python3
        from pathlib import Path
        import importlib.util

        def load_plugins():
            for path in Path("plugins").glob("*.py"):
                spec = importlib.util.spec_from_file_location(path.stem, path)
                mod = importlib.util.module_from_spec(spec)
                assert spec.loader
                spec.loader.exec_module(mod)
                yield getattr(mod, "name", path.stem), mod.run()

        for name, result in load_plugins():
            print(f"plugin={name} result={result}")
        print("RESULT ok")
        EOF
        python3 core.py
        ```
        """
    ),
}


def related(num: int) -> str:
    links = ["- [Python for DevOps Engineers – Category Overview](index.md)"]
    if num > 1:
        prev = SPEC[num - 2]
        links.append(f"- [{prev[2]}]({prev[1]}.md) *(previous)*")
    if num < len(SPEC):
        nxt = SPEC[num]
        links.append(f"- [{nxt[2]}]({nxt[1]}.md) *(next)*")
    links.append("- [Shell Scripting for DevOps Engineers](../shell/index.md)")
    links.append("- [Learning Paths](../learning-paths/index.md)")
    return "\n".join(links)


def lab_block(num: int, slug: str, focus: str) -> str:
    """Build Hands-on Lab markdown without accidental leading indentation."""
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
    prev_title = SPEC[num - 2][2] if num > 1 else "Linux Fundamentals and Shell Scripting"
    prereq = [
        prev_title if num > 1 else "Linux Fundamentals and basic Shell Scripting",
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

This is **Tutorial {num}** in **{module}** of the REBASH Academy **Python for DevOps Engineers** series — written for DevOps engineers, SREs, platform engineers, and cloud engineers who automate infrastructure with production-quality Python.

## Prerequisites

{pr}

## Learning Objectives

By the end of this tutorial, you will be able to:

{obj}

## Architecture

Ops Python sits between operators/CI and platforms (files, APIs, CLIs, and cloud control planes). This topic’s control points are shown below.

![Architecture diagram for {title}](../assets/images/{diagram}.svg)

## Theory

{theory.strip()}

## Hands-on Lab

{lab_block(num, slug, lab_focus).rstrip()}

## Validation

- [ ] Lab commands run under `~/rebash-python/lab{num:02d}/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] Dry-run / fixture behaviour is clear for any mutating or cloud action
- [ ] You can relate this topic to a real DevOps or platform task

## Code Walkthrough

Production Python for **{title}** always combines:

1. A clear entry point (`main()` + `if __name__ == "__main__"`)
2. A project virtual environment and pinned dependencies when third-party libs are used
3. Explicit error handling and logging (no silent `except Exception: pass`)
4. Safe I/O: `pathlib`, timeouts on HTTP, `subprocess.run([...])` without `shell=True`
5. Documented exit codes and dry-run defaults for mutating actions

Keep modules short enough to review in a single merge request. Prefer stdlib first; add httpx/requests, Typer, pytest, and platform SDKs when the job needs them.

## Security Considerations

- Treat all external input (args, files, env, API payloads) as untrusted until validated
- Never log secrets or `Authorization` headers; prefer masked CI variables and secret stores
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
- Fixture / mock paths for GitHub, Docker, Kubernetes, Terraform, and cloud SDKs in CI
- Pair every new tool with at least one failing-path test you actually run

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `ModuleNotFoundError` in CI | Missing venv / pins | Recreate venv; install from lock/requirements |
| Works locally, fails in pipeline | Different Python or env | Pin `requires-python`; fingerprint env in the job |
| Hang on HTTP call | No timeout | Set `timeout=` on requests/httpx clients |
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
- [requests documentation](https://requests.readthedocs.io/)
- [httpx documentation](https://www.python-httpx.org/)
- Track index: [Python for DevOps Engineers](index.md)
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


def delete_obsolete() -> list[str]:
    keep = {f"{sp[1]}.md" for sp in SPEC} | {"index.md"}
    deleted: list[str] = []
    for name in OBSOLETE:
        if name in keep:
            continue
        path = OUT / name
        if path.exists():
            path.unlink()
            deleted.append(name)
            print(f"deleted {path.relative_to(ROOT)}")
    # Also remove any other tutorial md not in keep (except index)
    for path in sorted(OUT.glob("*.md")):
        if path.name in keep:
            continue
        path.unlink()
        if path.name not in deleted:
            deleted.append(path.name)
            print(f"deleted {path.relative_to(ROOT)}")
    return deleted


def assert_no_hash_brace(text: str, label: str) -> None:
    """mkdocs-macros breaks on '{#' sequences in page content."""
    if "{#" in text:
        raise AssertionError(f"forbidden '{{#' found in {label}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assert len(SPEC) == 27, len(SPEC)
    required = {
        "python-execution-flow",
        "python-virtual-environment",
        "python-package-architecture",
        "python-rest-api-flow",
        "python-docker-sdk-workflow",
        "python-k8s-client-architecture",
        "python-automation-pipeline",
        "python-plugin-architecture",
    }
    missing = required - set(DIAGRAMS)
    assert not missing, missing
    md_count = 0
    for sp in SPEC:
        diagram = sp[6]
        assert diagram in DIAGRAMS, diagram
        body = render(sp)
        assert_no_hash_brace(body, sp[1])
        path = OUT / f"{sp[1]}.md"
        path.write_text(body, encoding="utf-8")
        md_count += 1
        print(f"wrote {path.relative_to(ROOT)}")
    print(f"done: {md_count} tutorials")
    d2_count, svg_count, errors = write_diagrams()
    print(f"diagrams: d2={d2_count} svg={svg_count}")
    deleted = delete_obsolete()
    print(f"deleted_obsolete: {len(deleted)}")
    for e in errors:
        print(f"ERROR: {e}")
    print(
        f"SUMMARY md={md_count} d2={d2_count} svg={svg_count} "
        f"deleted={len(deleted)} errors={len(errors)}"
    )


if __name__ == "__main__":
    main()
