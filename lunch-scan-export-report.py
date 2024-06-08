import os
import sys
import mimetypes
from time import sleep
from http import HTTPStatus
from datetime import datetime

import requests



# Nessus API configuration
NESSUS_URL = os.getenv("NESSUS_URL")
ACCESS_KEY = os.getenv("NESSUS_ACCESS_KEY")
SECRET_KEY = os.getenv("NESSUS_SECRET_KEY")
SCAN_NAME = os.getenv("NESSUS_SCAN_NAME")
HEADERS = {"X-ApiKeys": f"accessKey={ACCESS_KEY};secretKey={SECRET_KEY}"}

# Confluence
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USER = os.getenv("CONFLUENCE_USER")
CONFLUENCE_PASSWORD = os.getenv("CONFLUENCE_PASSWORD")
CONFLUENCE_PAGE_ID = os.getenv("CONFLUENCE_PAGE_ID")
CONFLUENCE_ATTACHMENT_URL = f"{CONFLUENCE_URL}/rest/api/content/{CONFLUENCE_PAGE_ID}/child/attachment/"



# get scan ID by name
def get_scan_id_by_name():
    url = f"{NESSUS_URL}/scans"
    response = requests.get(url, headers=HEADERS, verify=False)
    scans = response.json()["scans"]

    for scan in scans:
        if scan["name"] == SCAN_NAME:
            return scan["id"]

    return None

# launch a scan by ID
def launch_scan_by_id(scan_id):
    url = f"{NESSUS_URL}/scans/{scan_id}/launch"
    response = requests.post(url, headers=HEADERS, verify=False)
    if response.status_code == 200:

        print("Lunch scan by id: status code",response.status_code)
        return response.json()
    else:
        print(f"Error: Scan lunch failed!, {response.json()}")
        sys.exit(1)

def is_scan_complete(scan_id):
    status = 'running'
    url = f"{NESSUS_URL}/scans/{scan_id}"
    while True:
        response = requests.get(url, headers=HEADERS, verify=False)
        status = response.json()['info']['status']
        print(f"Scan status: {status}...")
        if status == "completed":
            return True
        sleep(10)

# export scan report
def export_scan_report(scan_id, format="nessus"):
    url = f"{NESSUS_URL}/scans/{scan_id}/export?limit=2500"
    data = {"format": format, "template_id": 606}
    response = requests.post(url, headers=HEADERS, json=data, verify=False)
    print(response.json())
    return response.json()

# Check the file status of an exported scan
def is_exported_file_ready(scan_id, file_id):
    url = f"{NESSUS_URL}/scans/{scan_id}/export/{file_id}/status"
    response = requests.get(url, headers=HEADERS, verify=False)
    print(response.json())
    if response.status_code == HTTPStatus.OK and response.json()["status"] == "ready":
        return True

# download the exported report
def download_report(token, scan_id, file_id, file_name):
    url = f"{NESSUS_URL}/scans/{scan_id}/export/{file_id}/download"
    response = requests.get(url, headers=HEADERS, verify=False)
    with open(file_name, "wb") as f:
        f.write(response.content)


def upload_file_confluence(file_name):
    headers = {'X-Atlassian-Token': 'no-check'} #no content-type here!
    
    # determine content-type
    content_type, encoding = mimetypes.guess_type(file_name)
    if content_type is None:
        content_type = 'multipart/form-data'

    # provide content-type explicitly
    files = {'file': (file_name, open(file_name, 'rb'), content_type)}

    auth = (CONFLUENCE_USER, CONFLUENCE_PASSWORD)
    r = requests.post(CONFLUENCE_ATTACHMENT_URL, headers=headers, files=files, auth=auth)
    r.raise_for_status()


# Main script
def main():
    # Get scan ID by name
    scan_id = get_scan_id_by_name()
    print("scan_id", scan_id)

    if scan_id:
        # Launch the selected scan
        launch_scan_by_id(scan_id)
        print(f"Scan '{SCAN_NAME}' launched successfully. Scan ID: {scan_id}")
        is_scan_complete(scan_id)
        # Export scan report in PDF format
        export_result = export_scan_report(scan_id, format="html")

        if "file" in export_result:
            file_id = export_result["file"]
            # check if the file is ready, if not wait
            while True:
                if is_exported_file_ready(scan_id, file_id):
                    break
                sleep(3)

            print("file_id", file_id)
            file_name = f"{SCAN_NAME}_report-{datetime.now()}.html"

            # Download the exported report
            download_report(scan_id, file_id, file_name)
            print(f"Report downloaded successfully: {file_name}")
            upload_file_confluence(file_name)
            print("Report Uploaded to the confluence.")

        else:
            print("Failed to export scan report.")
    else:
        print(f"Scan with name '{SCAN_NAME}' not found.")

if __name__ == "__main__":
    main()
