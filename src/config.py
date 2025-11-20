import os
from dotenv import load_dotenv

load_dotenv()

def as_bool(v: str | None, default: bool = False) -> bool:
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "y", "on")

JENKINS_URL = os.getenv("JENKINS_URL", "http://localhost:8080").rstrip("/")
JENKINS_USER = os.getenv("JENKINS_USER", "admin")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN", "")
VERIFY_TLS = as_bool(os.getenv("VERIFY_TLS"), False)

REQUEST_TIMEOUT = 10  # seconds
