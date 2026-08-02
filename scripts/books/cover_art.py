"""SVG cover artwork for REBASH Academy course books.

Palette matches book CSS tokens in styles.py:
  ink #0f172a, accent #0f766e, teal highlights #5eead4 / #99f6e4
"""

from __future__ import annotations

import html
import re


def cover_art_svg(course_title: str) -> str:
    """Return a full-bleed decorative SVG for the book cover (fallback when no PNG)."""
    title = html.escape(course_title)
    hero = re.sub(r"[^A-Za-z0-9 +&_-]+", "", course_title).strip().upper() or "COURSE"
    hero_word = hero.split()[0][:18]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1200" width="800" height="1200" role="img" aria-label="{title} cover art">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.25" y2="1">
      <stop offset="0%" stop-color="#0b1220"/>
      <stop offset="45%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#134e4a"/>
    </linearGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="#5eead4" stroke-opacity="0.10" stroke-width="1"/>
    </pattern>
  </defs>

  <rect width="800" height="1200" fill="url(#bg)"/>
  <rect width="800" height="1200" fill="url(#grid)"/>

  <!-- Series bar -->
  <rect x="0" y="0" width="800" height="48" fill="#0f766e"/>
  <text x="28" y="31" fill="#f8fafc" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="14" letter-spacing="2.5" font-weight="700">REBASH PRODUCTION ENGINEERING SERIES</text>
  <rect x="690" y="10" width="86" height="28" rx="4" fill="#14b8a6"/>
  <text x="733" y="30" text-anchor="middle" fill="#042f2e" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="12" font-weight="700">VOLUME 1</text>

  <!-- Hero title -->
  <text x="40" y="210" fill="#ffffff" font-family="Impact, Haettenschweiler, Arial Black, sans-serif" font-size="128" letter-spacing="4">{html.escape(hero_word)}</text>
  <text x="44" y="255" fill="#5eead4" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="28" font-weight="700" letter-spacing="6">COURSE BOOK</text>

  <text x="44" y="310" fill="#e2e8f0" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="20">From Beginner to Production Engineer</text>
  <text x="44" y="342" fill="#99f6e4" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="18" font-weight="600">Master Linux. Solve Real Problems.</text>

  <!-- Terminal card -->
  <g transform="translate(220, 390)">
    <rect x="0" y="0" width="360" height="240" rx="14" fill="#0f172a" stroke="#14b8a6" stroke-width="2"/>
    <rect x="0" y="0" width="360" height="36" rx="14" fill="#334155"/>
    <rect x="0" y="22" width="360" height="14" fill="#334155"/>
    <circle cx="24" cy="18" r="6" fill="#f87171"/>
    <circle cx="44" cy="18" r="6" fill="#fbbf24"/>
    <circle cx="64" cy="18" r="6" fill="#34d399"/>
    <text x="24" y="70" fill="#5eead4" font-family="IBM Plex Mono, Menlo, monospace" font-size="15">rebash@linux:~$</text>
    <text x="24" y="100" fill="#e2e8f0" font-family="IBM Plex Mono, Menlo, monospace" font-size="14">uname -a</text>
    <text x="24" y="128" fill="#94a3b8" font-family="IBM Plex Mono, Menlo, monospace" font-size="13">Linux rebash 6.8.0 x86_64</text>
    <text x="24" y="160" fill="#e2e8f0" font-family="IBM Plex Mono, Menlo, monospace" font-size="14">systemctl is-system-running</text>
    <text x="24" y="188" fill="#86efac" font-family="IBM Plex Mono, Menlo, monospace" font-size="14">running</text>
    <text x="24" y="220" fill="#5eead4" font-family="IBM Plex Mono, Menlo, monospace" font-size="15">rebash@linux:~$ ▍</text>
  </g>

  <!-- Feature chips -->
  <g font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="13" fill="#ecfeff">
    <rect x="40" y="680" width="200" height="36" rx="18" fill="#134e4a" stroke="#14b8a6"/>
    <text x="140" y="703" text-anchor="middle">Hands-on Labs</text>
    <rect x="260" y="680" width="220" height="36" rx="18" fill="#134e4a" stroke="#14b8a6"/>
    <text x="370" y="703" text-anchor="middle">Production Focused</text>
    <rect x="500" y="680" width="200" height="36" rx="18" fill="#134e4a" stroke="#14b8a6"/>
    <text x="600" y="703" text-anchor="middle">Interview Ready</text>
  </g>

  <!-- Stats -->
  <line x1="40" y1="760" x2="760" y2="760" stroke="#0f766e" stroke-width="2"/>
  <g fill="#fff" font-family="Source Sans 3, Helvetica, Arial, sans-serif" text-anchor="middle">
    <text x="130" y="800" font-size="16" font-weight="700">25 Chapters</text>
    <text x="320" y="800" font-size="16" font-weight="700">25 Labs</text>
    <text x="510" y="800" font-size="16" font-weight="700">Real Scenarios</text>
    <text x="690" y="800" font-size="16" font-weight="700">Interview Q&amp;A</text>
  </g>
  <line x1="40" y1="830" x2="760" y2="830" stroke="#0f766e" stroke-width="2"/>

  <!-- Author -->
  <text x="40" y="920" fill="#ffffff" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="32" font-weight="800">SHAIK KHADAR BASHA</text>
  <text x="40" y="955" fill="#5eead4" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="16">Cloud Architect · DevOps Trainer · Founder, REBASH Academy</text>
  <text x="40" y="985" fill="#cbd5e1" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="15">Helping engineers build production-ready skills</text>

  <rect x="0" y="1120" width="800" height="80" fill="#0b1220" fill-opacity="0.65"/>
  <text x="400" y="1168" text-anchor="middle" fill="#99f6e4" font-family="Source Sans 3, Helvetica, Arial, sans-serif" font-size="20" letter-spacing="5">REBASH ACADEMY  ·  rebash.in</text>
</svg>
"""
