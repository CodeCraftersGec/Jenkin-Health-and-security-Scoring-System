import psutil
from typing import Dict, Any
from .jenkins_client import JenkinsClient

def _safe_percent(value: float | int, max_value: float | int) -> float:
    try:
        return round((float(value) / float(max_value)) * 100.0, 2)
    except Exception:
        return 0.0

def collect_host_health() -> Dict[str, Any]:
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk_root = psutil.disk_usage("/").percent

    return {
        "host_cpu_percent": cpu,
        "host_mem_percent": mem,
        "host_disk_percent": disk_root,
    }

def collect_jenkins_health(client: JenkinsClient) -> Dict[str, Any]:
    root = client.get_root()
    jobs_info = client.list_jobs_brief()

    total_jobs = len(jobs_info.get("jobs", []))
    success_jobs = len([j for j in jobs_info.get("jobs", []) if j.get("color") == "blue"])
    failed_jobs = len([j for j in jobs_info.get("jobs", []) if j.get("color") == "red"])
    unstable_jobs = len([j for j in jobs_info.get("jobs", []) if j.get("color") in ("yellow", "aborted")])

    success_rate = round((success_jobs / total_jobs) * 100, 2) if total_jobs else 0.0

    nodes = client.get_nodes()
    total_nodes = nodes.get("totalExecutors", 0)
    offline_nodes = 0
    for comp in nodes.get("computer", []):
        if comp.get("offline"):
            offline_nodes += 1

    queue = client.get_queue()
    queue_len = len(queue.get("items", []))

    return {
        "jenkins_mode": root.get("mode"),
        "jenkins_use_crums": root.get("useCrumbs", False),
        "jenkins_use_security": root.get("useSecurity", False),
        "jenkins_num_executors": root.get("numExecutors", 0),

        "jobs_total": total_jobs,
        "jobs_success": success_jobs,
        "jobs_failed": failed_jobs,
        "jobs_unstable": unstable_jobs,
        "jobs_success_rate_percent": success_rate,

        "nodes_total_executors": total_nodes,
        "nodes_offline": offline_nodes,

        "queue_length": queue_len,
    }

def build_health_score(host: Dict[str, Any], jenkins: Dict[str, Any]) -> int:
    score = 100

    # Host constraints
    if host["host_cpu_percent"] > 85: score -= 10
    elif host["host_cpu_percent"] > 70: score -= 5

    if host["host_mem_percent"] > 85: score -= 10
    elif host["host_mem_percent"] > 70: score -= 5

    if host["host_disk_percent"] > 90: score -= 10
    elif host["host_disk_percent"] > 80: score -= 5

    # Jenkins signals
    if jenkins["jenkins_mode"] != "NORMAL":
        score -= 10

    if jenkins["jobs_total"] > 0:
        if jenkins["jobs_success_rate_percent"] >= 90:
            score += 5
        elif jenkins["jobs_success_rate_percent"] < 60:
            score -= 10

    if jenkins["nodes_offline"] > 0:
        score -= min(15, 5 * jenkins["nodes_offline"])

    if jenkins["queue_length"] > 5:
        score -= 5
    if jenkins["queue_length"] > 15:
        score -= 10

    return max(0, min(100, score))

def get_health_metrics(client: JenkinsClient) -> Dict[str, Any]:
    host = collect_host_health()
    jenkins = collect_jenkins_health(client)
    score = build_health_score(host, jenkins)
    return {"host": host, "jenkins": jenkins, "health_score": score}
