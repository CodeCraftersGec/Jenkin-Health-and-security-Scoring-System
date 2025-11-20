from typing import Dict

DEFAULT_WEIGHTS = {
    "health": 0.6,
    "security": 0.4,
}

def overall_score(health_score: int, security_score: int, weights: Dict[str, float] = DEFAULT_WEIGHTS) -> float:
    h = max(0, min(100, health_score))
    s = max(0, min(100, security_score))
    return round(h * weights["health"] + s * weights["security"], 2)

def recommendations(health: Dict, sec: Dict) -> list[str]:
    recs: list[str] = []

    # Security
    if not sec["security"]["security_enabled"]:
        recs.append("Enable Jenkins security (Manage Jenkins → Configure Global Security).")
    if not sec["security"]["csrf_enabled"]:
        recs.append("Enable CSRF protection (crumb issuer).")
    if not sec["security"]["https_enabled"]:
        recs.append("Enable HTTPS/terminate TLS with a reverse proxy (Nginx/Apache).")
    if sec["security"]["plugins_outdated"] > 0:
        recs.append(f"Update {sec['security']['plugins_outdated']} outdated plugin(s).")
    if sec["security"]["anonymous_read"]:
        recs.append("Disable anonymous read access.")

    # Health
    h = health["host"]
    j = health["jenkins"]
    if h["host_cpu_percent"] > 85:
        recs.append("High CPU usage: consider tuning executors or moving heavy jobs to agents.")
    if h["host_mem_percent"] > 85:
        recs.append("High memory usage: increase RAM or reduce concurrent builds.")
    if h["host_disk_percent"] > 80:
        recs.append("Low disk space: prune workspaces, rotate artifacts, or expand storage.")
    if j["nodes_offline"] > 0:
        recs.append("Some nodes are offline: check agent connectivity.")
    if j["queue_length"] > 5:
        recs.append("Build queue is long: add executors/agents or schedule builds smarter.")
    if j["jobs_total"] > 0 and j["jobs_success_rate_percent"] < 80:
        recs.append("Low job success rate: review failing builds and flaky tests.")

    return recs
