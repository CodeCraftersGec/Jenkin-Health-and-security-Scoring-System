from prettytable import PrettyTable
from .jenkins_client import JenkinsClient
from .health_module import get_health_metrics
from .security_module import get_security_metrics
from .scoring import overall_score, recommendations
from .report import to_csv, to_json

def run_once() -> None:
    client = JenkinsClient()

    health = get_health_metrics(client)
    sec = get_security_metrics(client)
    ov = overall_score(health["health_score"], sec["security_score"])

    # Table
    table = PrettyTable(["Category", "Metric", "Value"])
    # Health host
    for k, v in health["host"].items():
        table.add_row(["Host", k, v])
    # Health jenkins
    for k, v in health["jenkins"].items():
        table.add_row(["Jenkins", k, v])
    # Scores
    table.add_row(["Score", "Health", health["health_score"]])
    # Security
    for k, v in sec["security"].items():
        table.add_row(["Security", k, v])
    table.add_row(["Score", "Security", sec["security_score"]])
    table.add_row(["Score", "Overall", ov])

    print(table)

    # Recommendations
    recs = recommendations(health, sec)
    if recs:
        print("\nRecommendations:")
        for i, r in enumerate(recs, 1):
            print(f" {i}. {r}")
    else:
        print("\nNo recommendations. System looks good!")

    # Export artifacts
    bundle = {
        "health": health,
        "security": sec,
        "overall_score": ov,
        "recommendations": recs,
    }
    to_json("jenkins_report.json", bundle)
    to_csv("jenkins_report.csv", bundle)
    print("\nSaved: jenkins_report.json, jenkins_report.csv")

if __name__ == "__main__":
    run_once()
