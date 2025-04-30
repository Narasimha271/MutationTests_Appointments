**Appointment API - Mutation & Unit Testing with Docker**

This project implements an Appointment Booking API using FastAPI, and supports both:

✅ Mutation Testing using MutPy

✅ HTML reporting for both

✅ Dockerized execution for reproducibility

🛠 Technologies Used

   - FastAPI – lightweight web framework for building APIs
   - Pytest – unit testing framework
   - unittest – Python inbuilt unit testing framework
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


**🛠 Troubleshooting******

**✅ Mutation report not found?**

Check if this file exists:
   - reports/mutation_raw_output.txt

If it's missing, ensure:
   - You're calling test_runner.py (not mutpy directly)

make sure start.py has:
from test_runner import main
main()

**✅ Unit test report missing?**

Check if this file exists:
   - reports/report.xml

If it's there but no HTML, re-run:
   - junit2html reports/report.xml reports/report.html

**🧼 Clean Up**

To remove volumes and containers:
   - docker system prune -f

**🧩 Uses of Extending This Setup in to other projects**

>> This setup can be easily integrated into CI/CD pipelines using Docker, including platforms like GitHub Actions and Azure DevOps.

>> The generated reports can be exported as artifacts and visualized in dashboards using tools like Power BI or any platform that supports data import from structured files (e.g., XML, JSON, or CSV).

>> Mutation testing thresholds can be used to fail builds or act as gatekeepers in CI/CD pipelines.


**🔁 CI/CD Integration Tips**
1) Use a CI runner that supports Docker (Azure Pipelines, Jenkins and GitLab CI)

2) Build and run the container:
   - name: Build Docker image
     run: docker build -t mutation-test .

   - name: Run tests in container
     run: docker run --rm -v ${{ github.workspace }}:/app mutation-test
        
3) Collect reports/*.html as artifacts for review

**⚙️ Scaling Across Microservices (WIS-compatible)**
To scale this mutation testing framework across microservices in WIS:
1) Create a shared base Docker image with:
      - pytest, mutpy, jinja2, etc.
      - Your test_runner.py and generate_mutation_html.py
2) Copy the testing framework files into other microservices and ensure that the folder structure is consistent across all services. This consistency enables seamless integration of unit and mutation testing within each service, using the same Docker-based workflow and CI/CD steps.

![image](https://github.com/user-attachments/assets/4e2f0ee0-14d8-4e40-b252-2b4cb3c3afe8)

4) update the test_runner.py with all the test files to make them executable with Mutation testing
5) Use service-specific Dockerfiles that pull from the shared base image.
6) Define a reusable CI/CD template that:
      - Builds the image
      - Runs the test container
      - Publishes HTML reports as artifacts
  
Note: This mutation testing framework is designed to work with Pytest and uses MutPy as the mutation engine. Different mutation tools are available for different test frameworks — for example, mutmut can be used with unittest. If you're using a test framework other than Pytest, the mutation testing logic must be adapted accordingly to match its test discovery and execution model.   


