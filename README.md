**Appointment API - Mutation & Unit Testing with Docker**

This project implements an Appointment Booking API using FastAPI, and supports both:

✅ Mutation Testing using MutPy

✅ HTML reporting for both

✅ Dockerized execution for reproducibility

🛠 Technologies Used

   - FastAPI – lightweight web framework for building APIs

   - Pytest – unit testing framework

   - MutPy – mutation testing tool for Python

   - Jinja2 – for HTML templating in mutation reports

   - junit2html – converts XML test results to HTML

   - Docker – containerizes test execution for reproducibility

📦 Project Structure

![image](https://github.com/user-attachments/assets/46bcde23-6783-4fe6-999b-676c2f0bc18a)


** Quick Start**

Prerequisites
Docker installed
🛠 1. Configure test mode
Set mutation to true or false in config.json:
{
  "mutation": true
}

🔄 2. Build the Docker Image

docker build -t mutation-test .

▶️ 3. Run the Tests

docker run --rm -v "${PWD}:/app" mutation-test

**Note: A batch file has been created in Appointments project with title 'run_tests' the to run the Build and Run the Docker Image. Just run this command to execute Building and running tests in Docker**

📁 4. View the HTML Reports

After the container runs:

✅ For Non Mutation Test run:

>> reports/report.html (converted from Pytest XML)

🧬 For Mutation Tests:

>> reports/mutation_report.html (parsed from raw output)

Test Results can be found in Appointments/reports folder

report.html               # Report for Non Mutation test run

mutation_report.html      # Report for Mutation test run


🛠 Troubleshooting

✅ Mutation report not found?

Check if this file exists:

reports/mutation_raw_output.txt

If it's missing, ensure:

You're calling test_runner.py (not mutpy directly)

start.py has:

from test_runner import main
main()

✅ Unit test report missing?

Check if this file exists:

reports/report.xml

If it's there but no HTML, re-run:

junit2html reports/report.xml reports/report.html

📊 Mutation Report Example

The mutation report shows:

   - Total mutants generated

   - Killed (tests caught them)

   - Survived (escaped mutants)

   - Incompetent / timeout cases

   - Final Mutation Score (%)

Example:

[*] Mutation score [1.23 s]: 42.8%
   - all: 28
   - killed: 12 (42.8%)
   - survived: 16 (57.2%)
   - incompetent: 0
   - timeout: 0

🧼 Clean Up

To remove volumes and containers:

> docker system prune -f

🧩 Uses of Extending This Setup in to other projects

>> This setup can be easily integrated into CI/CD pipelines using Docker, including platforms like GitHub Actions and Azure DevOps.

>> The generated reports can be exported as artifacts and visualized in dashboards using tools like Power BI or any platform that supports data import from structured files (e.g., XML, JSON, or CSV).

>> Mutation testing thresholds can be used to fail builds or act as gatekeepers in CI/CD pipelines.
