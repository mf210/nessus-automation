# Nessus Automation

![GitHub last commit](https://img.shields.io/github/last-commit/mf210/nessus-automation)

## Overview

This Python script automates Nessus scans, report exports, and downloads using the Nessus API. Leverage this script to integrate Nessus into your security workflow and simplify vulnerability assessments.

## Prerequisites

Before using the script, ensure you have the following:

- Docker: Run Nessus in a Docker container using the following command:

  ```bash
  docker pull tenable/nessus:latest-ubuntu
  docker container run --name nessus -p 8834:8834 -d tenable/nessus:latest-ubuntu
  ```
- Nessus API Keys: Store your username, password, Nessus API access and secret keys in a .env file.

- Pipenv: Install dependencies using Pipenv:
  ```bash
  pipenv install
  ```
## Usage
- Clone the repository to your local machine:
  ```bash
  git clone https://github.com/mf210/nessus-automation.git
  cd nessus-automation-script
  ```
- Create and configure your .env file with Nessus API keys.
- Run the script using Pipenv:
  ```bash
  pipenv run python export-scan-report.py
  ```

## Configuration
Modify the NESSUS_URL, ACCESS_KEY, SECRET_KEY, and other parameters in the script according to your Nessus server setup.

## Contributing
Contributions and feedback are welcome! If you have ideas for improvements, new features, or bug fixes, feel free to open an issue or submit a pull request.
