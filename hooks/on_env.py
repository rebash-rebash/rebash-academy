"""MkDocs hook: inject analytics and environment-specific configuration."""

import os


def on_env(env, config, files):
    """Disable analytics when no tracking ID is configured."""
    analytics_key = os.environ.get("GOOGLE_ANALYTICS_KEY", "").strip()
    plausible_domain = os.environ.get("PLAUSIBLE_DOMAIN", "").strip()

    if not analytics_key and not plausible_domain:
        config.extra.pop("analytics", None)
        config.extra.pop("consent", None)
    elif plausible_domain and not analytics_key:
        config.extra["analytics"] = {
            "provider": "plausible",
            "domain": plausible_domain,
        }
