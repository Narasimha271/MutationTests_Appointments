import os
from jinja2 import Template

# Load raw output
with open("reports/mutation_raw_output.txt") as f:
    output = f.read()

# Extract mutation summary from raw output
summary = {"total": 0, "killed": 0, "survived": 0, "incompetent": 0, "timeout": 0}
for line in output.splitlines():
    if "Mutation score" in line:
        parts = line.strip().split(":")[-1].strip().split("%")[0]
        summary["score"] = round(float(parts), 2)
    elif "all:" in line:
        tokens = line.strip().split()
        summary["total"] = int(tokens[1])
        summary["killed"] = int(tokens[3])
        summary["survived"] = int(tokens[5])
        summary["incompetent"] = int(tokens[7])
        summary["timeout"] = int(tokens[9])

# Default score if not found
if "score" not in summary:
    summary["score"] = 0.0

# HTML template
html_template = """
<html>
<head><title>Mutation Report</title></head>
<body>
    <h1>Mutation Test Report</h1>
    <ul>
        <li><strong>Total Mutants:</strong> {{ total }}</li>
        <li><strong>Killed:</strong> {{ killed }}</li>
        <li><strong>Survived:</strong> {{ survived }}</li>
        <li><strong>Incompetent:</strong> {{ incompetent }}</li>
        <li><strong>Timeout:</strong> {{ timeout }}</li>
        <li><strong>Mutation Score:</strong> {{ score }}%</li>
    </ul>
    <h3>Raw Output</h3>
    <pre>{{ raw }}</pre>
</body>
</html>
"""

html = Template(html_template).render(**summary, raw=output)

# Save HTML file
os.makedirs("reports", exist_ok=True)
with open("reports/mutation_report.html", "w") as f:
    f.write(html)

print("[✔] Mutation HTML report created at reports/mutation_report.html")
