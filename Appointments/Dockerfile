
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from your project into the container
COPY . .

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run your mutation test script
CMD ["sh", "-c", "python start.py | tee test_report.txt"]


