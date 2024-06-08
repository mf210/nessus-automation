import os
import sys
import requests



# Nessus API configuration
NESSUS_URL = "https://nessus.xxxxxxxxx.com"
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
SCAN_NAME = "test"

# get scan ID by name
def get_scan_id_by_name(scan_name):
    url = f"{NESSUS_URL}/scans"
    headers = {"X-ApiKeys": f"accessKey={ACCESS_KEY};secretKey={SECRET_KEY}"}
    response = requests.get(url, headers=headers, verify=False)
    scans = response.json()["scans"]
    
    for scan in scans:
        if scan["name"] == scan_name:
            return scan["id"]
    
    return None

# launch a scan by ID
def launch_scan_by_id(scan_id):
    url = f"{NESSUS_URL}/scans/{scan_id}/launch"
    headers = {"X-ApiKeys": f"accessKey={ACCESS_KEY};secretKey={SECRET_KEY}"}
    response = requests.post(url, headers=headers, verify=False)
    if response.status_code == 200:

        print("Lunch scan by id: status code",response.status_code)
        return response.json()
    else:
        print(f"Error: Scan lunch failed!, {response.json()}")
        sys.exit(1)


def main():
    scan_id = get_scan_id_by_name(SCAN_NAME)
    if scan_id:
        # Launch the selected scan
        result = launch_scan_by_id(scan_id)
        # print(result)
        print(f"Scan '{SCAN_NAME}' launched successfully. Scan ID: {scan_id}")
    else:
        print(f"Scan with name '{SCAN_NAME}' not found.")


if __name__ == "__main__":
    main()
