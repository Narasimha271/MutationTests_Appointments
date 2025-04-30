import sys
sys.argv[0] = "test_runner.py"  # 💣 overwrite inherited CLI context

import json
import subprocess

def load_config():
    with open('config.json') as f:
        return json.load(f)

def run_mutation_tests():
    import subprocess
    import os
    from jinja2 import Template

    os.makedirs("reports", exist_ok=True)
    print("[*] Running mutation tests and capturing output...")

    # Run MutPy and capture output
    result = subprocess.run(
        [
            "mut.py",
            "--target", "Services.main",
            "--unit-test", "Test.appointments_test",
            "--runner", "unittest"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    output = result.stdout
    with open("reports/mutation_raw_output.txt", "w") as f:
        f.write(output)
        print("[✔] mutation_raw_output.txt has been written.")

    # Extract summary from output
    summary = {"total": 0, "killed": 0, "survived": 0, "incompetent": 0, "timeout": 0}
    for line in output.splitlines():
        if "Mutation score" in line:
            parts = line.strip().split(":")[-1].strip().split("%")[0]
            summary["score"] = round(float(parts), 2)
        elif "- all:" in line:
            summary["total"] = int(line.strip().split(":")[1].strip())
        elif "- killed:" in line:
            summary["killed"] = int(line.strip().split(":")[1].strip().split()[0])
        elif "- survived:" in line:
            summary["survived"] = int(line.strip().split(":")[1].strip().split()[0])
        elif "- incompetent:" in line:
            summary["incompetent"] = int(line.strip().split(":")[1].strip().split()[0])
        elif "- timeout:" in line:
            summary["timeout"] = int(line.strip().split(":")[1].strip().split()[0])


    # Fallback score if not found
    if "score" not in summary:
        summary["score"] = 0.0

    # Render HTML
    template = """
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
        <h3>Raw Output:</h3>
        <pre>{{ raw }}</pre>
    </body>
    </html>
    """

    html = Template(template).render(**summary, raw=output)
    with open("reports/mutation_report.html", "w") as f:
        f.write(html)

    print("[✔] Mutation HTML report created at reports/mutation_report.html")


def run_normal_tests():
    import subprocess
    import os

    os.makedirs("reports", exist_ok=True)

    print("[*] Running normal tests and generating report.xml...")

    # Run pytest and generate XML report
    result = subprocess.run([
        "pytest",
        "--junitxml=reports/report.xml"
    ])

    if os.path.exists("reports/report.xml"):
        subprocess.run([
            "junit2html",
            "reports/report.xml",
            "reports/report.html"
        ])
        print("[*] HTML report generated: reports/report.html")
    else:
        print("[!] report.xml was not found.")

    if result.returncode != 0:
        print("[!] Tests failed.")
        exit(result.returncode)

def main():
    config = load_config()
    if config.get("mutation", False):
        print("[*] Running mutation tests...")
        run_mutation_tests()
    else:
        print("[*] Running normal tests...")
        run_normal_tests()
