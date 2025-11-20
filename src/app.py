from flask import Flask, render_template
from .jenkins_client import JenkinsClient
from .health_module import get_health_metrics
from .security_module import get_security_metrics
from .scoring import overall_score, recommendations

app = Flask(__name__)


def _class_for_percent(value: float) -> str:
    """
    Helper to map percentage values into CSS classes: ok / warn / bad.
    Tune thresholds as you like.
    """
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "ok"

    if v >= 80:
        return "ok"
    elif v >= 50:
        return "warn"
    else:
        return "bad"


@app.route("/")
def dashboard():
    client = JenkinsClient()

    # Get same real data as in main.run_once()
    health = get_health_metrics(client)
    sec = get_security_metrics(client)
    ov = overall_score(health["health_score"], sec["security_score"])
    recs = recommendations(health, sec)

    # Precompute some convenience values for UI
    host = health["host"]
    jenkins = health["jenkins"]
    security = sec["security"]

    # For progress rings (circle circumference for r=26)
    circumference = 2 * 3.14159 * 26

    # Map scores (0–100) → dashoffset (lower = more filled)
    def dash_offset(score: float) -> float:
        score = max(0, min(100, float(score)))
        return circumference * (1 - score / 100.0)

    health_score = health["health_score"]
    security_score = sec["security_score"]
    overall = ov

    context = {
        "health": health,
        "security": sec,
        "overall": ov,
        "recs": recs,
        "host": host,
        "jenkins_metrics": jenkins,
        "security_metrics": security,
        "circumference": circumference,
        "health_dashoffset": dash_offset(health_score),
        "security_dashoffset": dash_offset(security_score),
        "overall_dashoffset": dash_offset(overall),
        "_class_for_percent": _class_for_percent,
    }

    return render_template("dashboard.html", **context)


if __name__ == "__main__":
    # For local demo/dev
    app.run(host="0.0.0.0", port=5000, debug=True)
