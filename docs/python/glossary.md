# Python for DevOps glossary

Curated terms for the REBASH Python course book.

- **argparse** — Standard-library module for parsing command-line arguments.
- **asyncio** — Standard-library framework for concurrent I/O with `async`/`await`.
- **Click** — Popular library for building CLI applications with decorators.
- **comprehension** — Compact expression that builds a list, set, or dict from an iterable.
- **dataclass** — Class decorator that generates boilerplate for data-holding objects.
- **dependency** — External package your project needs (declared in `pyproject.toml` or requirements).
- **exception** — Error object raised and optionally caught with `try` / `except`.
- **Fabric** — High-level SSH automation library built on Paramiko patterns.
- **generator** — Function that yields values lazily with `yield` instead of returning a full list.
- **GIL** — Global Interpreter Lock; CPython limit on parallel bytecode execution in threads.
- **JSON** — JavaScript Object Notation; common data interchange format.
- **logging** — Standard-library facility for structured application messages and levels.
- **module** — A single `.py` file importable as a namespace.
- **package** — Directory of modules (often with `__init__.py`) or a distributable project.
- **Paramiko** — Python SSHv2 library for remote command and file automation.
- **pathlib** — Object-oriented filesystem paths in the standard library.
- **pip** — Package installer for Python.
- **pytest** — Widely used test framework for Python.
- **pyproject.toml** — Modern project metadata and build/tool configuration file.
- **requests** — Popular HTTP client library for calling REST APIs.
- **SDK** — Software Development Kit; vendor libraries (for example AWS, Docker, Kubernetes).
- **secret** — Credential or token that must not be committed; load from env or a vault.
- **subprocess** — Standard-library module for running external commands.
- **type hint** — Optional annotation of expected types (`def f(x: int) -> str`).
- **Typer** — CLI framework built on type hints (powered by Click).
- **venv** — Virtual environment; isolated Python interpreter and site-packages.
- **virtualenv** — Tooling concept for isolated environments (often created with `python -m venv`).
- **wheel** — Built package format (`.whl`) for installing Python projects quickly.
- **YAML** — Human-friendly configuration format common in Kubernetes and CI.
