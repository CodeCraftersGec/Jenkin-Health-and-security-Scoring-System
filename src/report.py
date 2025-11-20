import csv
import json
from typing import Dict, Any

def to_csv(path: str, data: Dict[str, Any]) -> None:
    # Flatten a bit
    rows = []
    for k, v in data.items():
        if isinstance(v, dict):
            for kk, vv in v.items():
                rows.append((f"{k}.{kk}", vv))
        else:
            rows.append((k, v))
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerows(rows)

def to_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
