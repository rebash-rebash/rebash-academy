"""MkDocs hook: inject analytics and environment-specific configuration."""

import os


def on_env(env, config, files):
    """Configure analytics from environment, falling back to mkdocs.yml."""
    analytics_key = os.environ.get("GOOGLE_ANALYTICS_KEY", "").strip()
    plausible_domain = os.environ.get("PLAUSIBLE_DOMAIN", "").strip()
    existing = config.extra.get("analytics") or {}
    existing_property = str(existing.get("property") or "").strip()

    if analytics_key:
        config.extra["analytics"] = {
            "provider": "google",
            "property": analytics_key,
        }
    elif plausible_domain:
        config.extra["analytics"] = {
            "provider": "plausible",
            "domain": plausible_domain,
        }
    elif existing.get("provider") == "google" and existing_property:
        # Keep Measurement ID from mkdocs.yml (public by design).
        pass
    else:
        config.extra.pop("analytics", None)
        config.extra.pop("consent", None)
