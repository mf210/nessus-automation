# Use the official Python image from Docker Hub
FROM python:3.12-slim


# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libc-dev \
#     libffi-dev \
#     libssl-dev \
#     && rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Copy Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pip install pipenv && pipenv install --system

# Copy the Python script into the container
COPY lunch-scan-export-report.py ./

# Run the script when the container starts
CMD ["python", "lunch-scan-export-report.py"]