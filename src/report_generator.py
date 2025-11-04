import os


def generate_html_report():
metrics_path = 'reports/metrics.txt'
plot_path = 'reports/doge_plot.png'
output_html = 'reports/final_report.html'


with open(metrics_path) as f:
metrics = f.read()


html = f"""
<html>
<head><title>Dogecoin Forecast Report</title></head>
<body>
<h1>Dogecoin Price Prediction Report</h1>
<pre>{metrics}</pre>
<img src='{plot_path}' width='600'>
</body>
</html>
"""


with open(output_html, 'w') as f:
f.write(html)
print(f"HTML report generated at {output_html}")


if __name__ == "__main__":
generate_html_report()