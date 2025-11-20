from typing import Dict, Any
from .jenkins_client import JenkinsClient

def collect_security(client: JenkinsClient) -> Dict[str, Any]:
    root = client.get_root()

    https_enabled = client.base_url.lower().startswith("https")
    csrf_enabled = bool(root.get("useCrumbs", False))
    security_enabled = bool(root.get("useSecurity", False))

    # Plugins
    plugins_raw = client.get_plugins()
    plugins = plugins_raw.get("plugins", [])
    outdated = [p for p in plugins if p.get("hasUpdate")]
    inactive = [p for p in plugins if not p.get("active")]
    pinned = [p for p in plugins if p.get("pinned")]

    # Anonymous read?
    # Heuristic: if security is disabled, anonymous can read. If enabled,
    # you can also test permissions via an unauthenticated call, but we’ll keep it simple.
    anonymous_read = not security_enabled

    return {
        "https_enabled": https_enabled,
        "csrf_enabled": csrf_enabled,
        "security_enabled": security_enabled,
        "plugins_total": len(plugins),
        "plugins_outdated": len(outdated),
        "plugins_inactive": len(inactive),
        "plugins_pinned": len(pinned),
        "anonymous_read": anonymous_read,
    }

def build_security_score(sec: Dict[str, Any]) -> int:
    score = 100

    if not sec["https_enabled"]:
        score -= 20
    if not sec["csrf_enabled"]:
        score -= 15
    if not sec["security_enabled"]:
        score -= 30
    if sec["anonymous_read"]:
        score -= 10

    # Outdated plugins penalty (capped)
    score -= min(25, sec["plugins_outdated"] * 3)
    # Inactive plugins penalty (mild)
    score -= min(10, sec["plugins_inactive"])

    return max(0, min(100, score))

def get_security_metrics(client: JenkinsClient) -> Dict[str, Any]:
    sec = collect_security(client)
    score = build_security_score(sec)
    return {"security": sec, "security_score": score}
