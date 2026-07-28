# REBASH Academy

**Learn by Building.** A production-grade documentation platform for DevOps, Cloud, and Security engineers.

Built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), REBASH Academy provides hands-on tutorials, learning paths, labs, cheat sheets, and interview preparation guides.

## Features

- Structured learning paths (DevOps, AWS, Azure, GCP, DevSecOps, Platform, Cloud Architect)
- 20+ documentation categories with consistent tutorial structure
- D2 architecture diagrams, syntax highlighting, search, and dark/light themes
- GitHub Actions CI/CD with automatic deployment to GitHub Pages
- Tutorial scaffolding and validation scripts

## Quick Start

### Prerequisites

- Python 3.12+
- Git
- [D2](https://d2lang.com) (for architecture diagrams)

### Local Development

```bash
git clone https://github.com/rebash-rebash/rebash-academy.git
cd rebash-academy

# Install D2 (macOS / Linux)
curl -fsSL https://d2lang.com/install.sh | sh -s --

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Build

```bash
bash scripts/build.sh
```

Output is written to the `site/` directory.

## Project Structure

```
rebash-academy/
├── docs/                  # Documentation source (Markdown)
├── overrides/             # Material theme overrides (homepage)
├── hooks/                 # MkDocs hooks (analytics config)
├── scripts/               # Build, lint, validate, tutorial generator
├── mkdocs.yml             # MkDocs configuration
├── requirements.txt       # Python dependencies
└── .github/workflows/     # CI/CD pipelines
```

## Adding Tutorials

```bash
python3 scripts/create-tutorial.py kubernetes "Deploy with Helm" \
  --description "Package and deploy apps using Helm charts." \
  --difficulty intermediate \
  --time "60 min"
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/build.sh` | Build site with strict mode |
| `scripts/lint.sh` | Lint YAML and validate config |
| `scripts/validate.sh` | Check metadata and internal links |
| `scripts/deploy.sh` | Build and show deploy instructions |
| `scripts/create-tutorial.py` | Scaffold a new tutorial |

## Deployment

Documentation deploys automatically to GitHub Pages when changes are merged to `main`.

**Live site:** [https://academy.rebash.in](https://academy.rebash.in)

### Custom domain (academy.rebash.in)

DNS at your registrar:

| Type | Name | Value |
|------|------|-------|
| CNAME | `academy` | `rebash-rebash.github.io` |

After DNS propagates, GitHub Pages issues an HTTPS certificate automatically (can take up to 24 hours). Enable **Enforce HTTPS** under **Settings → Pages** once available.

Manual deployment:

```bash
mkdocs gh-deploy --force
```

### Analytics (Optional)

Set environment variables to enable analytics:

```bash
export GOOGLE_ANALYTICS_KEY="G-XXXXXXXXXX"
# or
export PLAUSIBLE_DOMAIN="academy.rebash.in"
```

## Documentation Categories

Getting Started · Linux · Networking · Git · Docker · Kubernetes · Terraform · AWS · Azure · GCP · GitLab CI/CD · Python · Monitoring · Security · DevSecOps · AI · Projects · Labs · Cheat Sheets · Interview Prep · Architecture · Blog

## Roadmap

See [docs/roadmap.md](docs/roadmap.md) for current progress and upcoming content.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

[MIT License](LICENSE) – Copyright (c) 2026 Shaik Basha

## Acknowledgements

- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) by Martin Donath
- [MkDocs](https://www.mkdocs.org/) by the MkDocs team
- The open-source DevOps and Cloud community
