---
title: "Project — Python Log Analysis Tool"
description: "Beginner project: package a log analysis CLI with pathlib, regex, JSON output, argparse, and pytest."
difficulty: beginner
estimated_time: "4–6 hours"
category: projects
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - projects
  - python
  - beginner
  - logging
  - cli
comments: false
---

# Project — Python Log Analysis Tool

Beginner portfolio build for [Python for DevOps](../python/index.md) — turn the log analyser lab into a packaged, tested CLI.

## Project Overview

**Goal:** Ship an installable console script that analyses application logs and writes a summary report.

**Deliverable for your portfolio:**

- Packaged CLI (`loganalyse` or similar) via `pyproject.toml`
- `pathlib` + regex aggregation
- JSON (and optional text) output
- `pytest` for parsers and exit codes
- README with sample logs and usage

**Estimated cost:** £0.

## Goals

- [ ] Console script entry point
- [ ] `--input` / `--output` / `--min-level` flags
- [ ] Stable JSON schema documented in README
- [ ] Unit tests for regex and aggregation
- [ ] Clear exit codes (`0` ok, `2` usage/input)

## Stack

| Piece | Choice |
|-------|--------|
| Packaging | pyproject.toml |
| CLI | argparse or Typer |
| Test | pytest |

## Prerequisites

- Labs: [Python Log Analyser](../labs/python-log-analyser.md)
- Tutorials: [Python Fundamentals](../python/python-fundamentals-install-venv-and-tooling.md), [File Handling](../python/file-handling-pathlib-json-yaml-csv.md), [Testing with pytest](../python/testing-with-pytest.md)

## Milestones

### Milestone 1 — Lab → package

Move lab script into `src/loganalyse/`, add `pyproject.toml` with `[project.scripts]`.

### Milestone 2 — CLI polish

Help text, validation, stderr errors, `--format json|text`.

### Milestone 3 — Tests and sample data

`tests/fixtures/*.log`, pytest coverage of counts and missing-input exit code.

### Milestone 4 — README

Architecture note, example invocation, link to next intermediate project.

## Success criteria

- `pip install -e .` then `loganalyse --help` works
- Tests pass offline
- Sample run matches documented expected JSON

## Related

- Lab: [Python Log Analyser](../labs/python-log-analyser.md)
- Next: [Infrastructure Inventory CLI](python-infra-inventory-cli.md)
- Cheat sheet: [Python](../cheatsheets/python.md)
