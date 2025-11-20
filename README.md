
# Jenkins Health & Security Scoring

This project collects **health** and **security** metrics from a Jenkins instance,  
calculates an **overall score**, prints a CLI report, and exposes a modern **web dashboard** using Flask.

---

## Features

- 🖥 **CLI report**
  - Host metrics (CPU, memory, disk usage)
  - Jenkins metrics (jobs, executors, queue, etc.)
  - Health / Security / Overall scores
  - Text recommendations
  - Exports to `jenkins_report.json` and `jenkins_report.csv`

- 🌐 **Web dashboard (Flask)**
  - Animated cards for Health, Security, and Overall scores
  - Host health table with progress bars
  - Jenkins health table with live metrics
  - Security configuration table (HTTPS, CSRF, plugins, etc.)
  - Recommendations section driven by real data

- 🔌 **Pluggable Jenkins client**
  - All data is fetched via `JenkinsClient` inside `src/jenkins_client.py`
  - You can point it to any Jenkins instance by setting URL/credentials

---

## Project Structure (important files)

```text
.
├── src/
│   ├── main.py              # CLI entrypoint
│   ├── app.py               # Flask web app
│   ├── jenkins_client.py    # Jenkins API wrapper (configure this)
│   ├── health_module.py     # host + Jenkins health metrics
│   ├── security_module.py   # security-related metrics
│   ├── scoring.py           # score calculation + recommendations()
│   ├── report.py            # JSON / CSV export helpers
│   └── templates/
│       └── dashboard.html   # UI for the Flask dashboard
├── requirements.txt
└── README.md
```

Your layout may be slightly different, but the key pieces are:

- `src/main.py` – prints the table + saves reports.
- `src/app.py` – runs the dashboard.
- `templates/dashboard.html` – the UI using the metrics.

---

## Requirements

- Python **3.8+** (3.10+ recommended)
- A Jenkins instance accessible from where this script runs
- Virtualenv (optional but recommended)

Python dependencies (example):

```text
Flask
prettytable
requests
psutil
```

(plus anything else your modules use; keep them in `requirements.txt`.)

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate      # Linux/macOS
# or .venv\Scripts\activate  # Windows PowerShell

pip install -r requirements.txt
```

---

## 1. Configure Jenkins Connection

Open `src/jenkins_client.py` and configure it for your Jenkins:

```python
class JenkinsClient:
    def __init__(self):
        self.base_url = "http://your-jenkins:8080"
        self.user = "your-username"
        self.token = "your-api-token"
        # self.session = ...
```

Typically you’ll use:

- **Jenkins URL** (e.g. `http://localhost:8080` or `https://jenkins.example.com`)
- **Username + API token** (recommended instead of password)

Make sure the user has permissions to:

- Read system info
- Read jobs
- Read plugins
- Access `/api/json` endpoints

---

## 2. Running the CLI Report

The CLI entry point is `src.main`. From the project root:

```bash
source .venv/bin/activate
python3 -m src.main
```

Example output:

```text
+----------+---------------------------+--------+
| Category |           Metric          | Value  |
+----------+---------------------------+--------+
|   Host   |      host_cpu_percent     |  40.7  |
|   Host   |      host_mem_percent     |  51.7  |
|   Host   |     host_disk_percent     |  26.8  |
| Jenkins  |        jenkins_mode       | NORMAL |
| Jenkins  |     jenkins_use_crums     |  True  |
| Jenkins  |    jenkins_use_security   |  True  |
| Jenkins  |   jenkins_num_executors   |   2    |
| Jenkins  |         jobs_total        |   3    |
| Jenkins  |        jobs_success       |   3    |
| Jenkins  |        jobs_failed        |   0    |
| Jenkins  |       jobs_unstable       |   0    |
| Jenkins  | jobs_success_rate_percent | 100.0  |
| Jenkins  |   nodes_total_executors   |   2    |
| Jenkins  |       nodes_offline       |   0    |
| Jenkins  |        queue_length       |   0    |
|  Score   |           Health          |  100   |
| Security |       https_enabled       | False  |
| Security |        csrf_enabled       |  True  |
| Security |      security_enabled     |  True  |
| Security |       plugins_total       |  100   |
| Security |      plugins_outdated     |   7    |
| Security |      plugins_inactive     |   0    |
| Security |       plugins_pinned      |   0    |
| Security |       anonymous_read      | False  |
|  Score   |          Security         |   59   |
|  Score   |          Overall          |  83.6  |
+----------+---------------------------+--------+

Recommendations:
 1. Enable HTTPS/terminate TLS with a reverse proxy (Nginx/Apache).
 2. Update 7 outdated plugin(s).

Saved: jenkins_report.json, jenkins_report.csv
```

Artifacts generated in the project root:

- `jenkins_report.json` – full data bundle: health, security, scores, recommendations.
- `jenkins_report.csv` – flattened CSV for quick analysis or import.

---

## 3. Running the Web Dashboard (Flask)

The web dashboard lives in `src/app.py`.

### Start the server

From the project root:

```bash
source .venv/bin/activate
python3 -m src.app
```

By default it will start on:

```text
http://0.0.0.0:5000/
```

Open that URL in your browser.

---

## 4. What the Dashboard Shows

The dashboard uses `get_health_metrics`, `get_security_metrics`, `overall_score`, and `recommendations` – the same code as the CLI.

### Score Cards

- **Health Score** – from `health["health_score"]`
- **Security Score** – from `sec["security_score"]`
- **Overall Score** – from `overall_score(health_score, security_score)`

Each score is rendered as:

- Big number (animated)
- Circular progress ring, filled based on percentage

### Host Health Table

Backed by `health["host"]`, typically:

- `host_cpu_percent`
- `host_mem_percent`
- `host_disk_percent`

Each value is rendered as a progress bar (with animated width).

### Jenkins Health Table

From `health["jenkins"]`, including:

- `jenkins_mode`
- `jobs_total`
- `jobs_success_rate_percent`
- `jobs_failed`
- `jobs_unstable`
- `nodes_total_executors`
- `nodes_offline`
- `queue_length`
- etc.

### Security Table

From `sec["security"]`, including:

- `https_enabled`
- `csrf_enabled`
- `security_enabled`
- `anonymous_read`
- `plugins_total`
- `plugins_outdated`
- `plugins_inactive`
- `plugins_pinned`

Values are color-coded:

- ✅ **green** for good (e.g. HTTPS enabled)
- ⚠️ **orange** for warnings (e.g. some outdated plugins)
- ❌ **red** for bad (e.g. HTTPS disabled, anonymous read enabled)

### Recommendations Section

From `recommendations(health, sec)`:

- If there are recommendations, a bulleted list is shown.
- Example:
  - Enable HTTPS / terminate TLS with a reverse proxy.
  - Update 7 outdated plugin(s).
- If no issues, shows: `No recommendations. System looks good!`

---

## 5. How the Data Flows

1. **JenkinsClient** talks to Jenkins and fetches raw data (system info, jobs, plugins, etc.).
2. **health_module.get_health_metrics(client)**:
   - Builds `health["host"]` and `health["jenkins"]`.
   - Computes `health["health_score"]`.
3. **security_module.get_security_metrics(client)**:
   - Builds `security["security"]`.
   - Computes `security["security_score"]`.
4. **scoring.overall_score(health_score, security_score)**:
   - Combines to a final overall score (e.g. 60% health + 40% security).
5. **scoring.recommendations(health, sec)**:
   - Looks at metrics and produces human-readable suggestions.
6. **report.to_json / report.to_csv**:
   - Export the metrics and scores.

Both `src.main` (CLI) and `src.app` (Flask) use the same logic, ensuring consistency.

---

## 6. Customization

### Change score weights

Open `src/scoring.py` and adjust how the overall score is calculated:

```python
def overall_score(health_score: float, security_score: float) -> float:
    return health_score * 0.6 + security_score * 0.4
```

Change the `0.6` / `0.4` as needed.

### Add more metrics

- Add logic in `health_module.py` or `security_module.py`.
- Return them in the `health["host"]`, `health["jenkins"]`, or `security["security"]` dictionaries.
- Update `dashboard.html` to show new rows.

### Run behind Nginx/Apache

To put this behind a reverse proxy or enable HTTPS, you can:

- Run Flask via `gunicorn` or `uwsgi`.
- Configure Nginx/Apache to:
  - Terminate TLS
  - Reverse proxy to the Flask app (e.g. `127.0.0.1:5000`)

This will also help you address the “Enable HTTPS” recommendation for your Jenkins URL itself.

---

## 7. Troubleshooting

### 1. I see demo data instead of real data

Make sure:

- You replaced the old static `dashboard.html` with the template that uses Jinja variables (`{{ ... }}`).
- `app.py` is importing and calling:
  - `get_health_metrics`
  - `get_security_metrics`
  - `overall_score`
  - `recommendations`
- You restart the Flask server after any change.

### 2. Flask cannot import modules

Check that you’re running from the **project root**:

```bash
python3 -m src.app
```

And that `src` has an `__init__.py` (so it’s a Python package).

### 3. Jenkins authentication errors

- Verify Jenkins URL is correct.
- Check username and API token.
- Try hitting Jenkins’ API manually with `curl` to confirm.

---

## 8. License

MIT

---

## 9. Credits

Developed as a Jenkins health & security scoring tool with:

- Python
- Flask
- PrettyTable
- Jenkins REST API
