"""MkDocs hook: inject analytics and environment-specific configuration."""

import os


def on_env(env, config, files):
    """Configure analytics from environment and disable when unset."""
    analytics_key = os.environ.get("GOOGLE_ANALYTICS_KEY", "").strip()
    plausible_domain = os.environ.get("PLAUSIBLE_DOMAIN", "").strip()

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
    else:
        config.extra.pop("analytics", None)
        config.extra.pop("consent", None)
