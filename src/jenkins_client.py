import requests
from typing import Any, Dict
from .config import JENKINS_URL, JENKINS_USER, JENKINS_TOKEN, VERIFY_TLS, REQUEST_TIMEOUT

class JenkinsClient:
    def __init__(self,
                 base_url: str = JENKINS_URL,
                 user: str = JENKINS_USER,
                 token: str = JENKINS_TOKEN,
                 verify_tls: bool = VERIFY_TLS) -> None:
        self.base_url = base_url.rstrip("/")
        self.auth = (user, token) if token else None
        self.verify_tls = verify_tls

    def _get(self, path: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = requests.get(url, auth=self.auth, verify=self.verify_tls, timeout=REQUEST_TIMEOUT, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_root(self) -> Dict[str, Any]:
        return self._get("/api/json")

    def get_plugins(self) -> Dict[str, Any]:
        # depth=1 yields plugin list with details (active, hasUpdate, etc.)
        return self._get("/pluginManager/api/json", params={"depth": 1})

    def get_nodes(self) -> Dict[str, Any]:
        return self._get("/computer/api/json", params={"depth": 1})

    def get_queue(self) -> Dict[str, Any]:
        return self._get("/queue/api/json")

    def get_crumb_issuer(self) -> Dict[str, Any]:
        # Present only if crumbs are enabled
        return self._get("/crumbIssuer/api/json")

    def get_job(self, job_name: str) -> Dict[str, Any]:
        return self._get(f"/job/{job_name}/api/json")

    def list_jobs_brief(self) -> Dict[str, Any]:
        # Only name and color to keep it light
        return self._get("/api/json", params={"tree": "jobs[name,color,url]"})
