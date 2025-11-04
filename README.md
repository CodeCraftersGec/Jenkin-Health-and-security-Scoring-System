# Dogecoin Price Forecasting with Jenkins CI/CD


### Overview
This project automates the Dogecoin price forecasting pipeline using Machine Learning and Jenkins CI/CD.


### Folder Structure
Refer to the project layout above.


### How to Run
1. Clone the repository.
2. Create a virtual environment and install dependencies:
```bash
pip install -r requirements.txt
```
3. Run each script manually or let Jenkins automate it using the provided Jenkinsfile.


### Jenkins Integration
- The Jenkinsfile automates all stages: data fetching, cleaning, model training, evaluation, and reporting.
- Security & Health scan stage simulates DevOps quality checks.


### Outputs
- `reports/doge_plot.png` → Visual forecast
- `reports/metrics.txt` → Model metrics
- `reports/final_report.html` → Combined HTML report