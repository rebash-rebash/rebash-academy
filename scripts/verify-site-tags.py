#!/usr/bin/env python3
"""Fail if built site pages are missing Analytics / AdSense tags."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# Canonical IDs (must match mkdocs.yml / ads.txt)
GA_ID = "G-2N59X0856S"
ADSENSE_CLIENT = "ca-pub-8933118209357814"
ADS_TXT_LINE = "google.com, pub-8933118209357814, DIRECT, f08c47fec0942fa0"


def main() -> int:
    if not SITE.is_dir():
        print("ERROR: site/ missing — run mkdocs build first", file=sys.stderr)
        return 1

    ads_txt = SITE / "ads.txt"
    if not ads_txt.is_file():
        print("ERROR: site/ads.txt missing", file=sys.stderr)
        return 1
    if ADS_TXT_LINE not in ads_txt.read_text(encoding="utf-8"):
        print("ERROR: site/ads.txt missing required publisher line", file=sys.stderr)
        return 1

    pages = list(SITE.rglob("index.html"))
    extras = [p for p in (SITE / "404.html",) if p.is_file()]
    targets = pages + extras
    if not targets:
        print("ERROR: no HTML pages in site/", file=sys.stderr)
        return 1

    missing_ga: list[str] = []
    missing_ads: list[str] = []
    missing_meta: list[str] = []

    for path in targets:
        html = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path.relative_to(SITE))
        if GA_ID not in html or "googletagmanager.com/gtag" not in html:
            missing_ga.append(rel)
        if ADSENSE_CLIENT not in html or "adsbygoogle.js" not in html:
            missing_ads.append(rel)
        if "google-adsense-account" not in html:
            missing_meta.append(rel)

    errors = False
    if missing_ga:
        errors = True
        print(f"ERROR: {len(missing_ga)} page(s) missing Google Analytics {GA_ID}")
        print("  e.g.", ", ".join(missing_ga[:5]))
    if missing_ads:
        errors = True
        print(f"ERROR: {len(missing_ads)} page(s) missing AdSense {ADSENSE_CLIENT}")
        print("  e.g.", ", ".join(missing_ads[:5]))
    if missing_meta:
        errors = True
        print(f"ERROR: {len(missing_meta)} page(s) missing google-adsense-account meta")
        print("  e.g.", ", ".join(missing_meta[:5]))

    if errors:
        return 1

    print(
        f"OK: {len(targets)} HTML page(s) include Analytics ({GA_ID}), "
        f"AdSense ({ADSENSE_CLIENT}), meta tag; ads.txt present"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
