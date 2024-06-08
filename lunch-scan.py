import os
import sys
import requests



# Nessus API configuration
NESSUS_URL = "https://127.0.0.1:8834"
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
SCAN_NAME = "test"

# get Nessus API token
def get_nessus_token():
    url = f"{NESSUS_URL}/session"
    data = {"username": "xxxxx", "password": "xxxxxxxx"}
    response = requests.post(url, json=data, verify=False)
    # print(response.json())
    token = response.json()["token"]
    return token

# get scan ID by name
def get_scan_id_by_name(token, scan_name):
    url = f"{NESSUS_URL}/scans"
    headers = {"X-Cookie": f"token={token}"}
    response = requests.get(url, headers=headers, verify=False)
    scans = response.json()["scans"]
    
    for scan in scans:
        if scan["name"] == scan_name:
            return scan["id"]
    
    return None

# launch a scan by ID
def launch_scan_by_id(token, scan_id):
    url = f"{NESSUS_URL}/scans/{scan_id}/launch"
    headers = {"X-Cookie": f"token={token}"}
    response = requests.post(url, headers=headers, verify=False)
    if response.status_code == 200:

        print("Lunch scan by id: status code",response.status_code)
        return response.json()
    else:
        print(f"Error: Scan lunch failed!, {response.json()}")
        sys.exit(1)

# Main script
def main():
    # Get Nessus API token
    token = get_nessus_token()
    # print(token)

    if token:
        # Get scan ID by name
        scan_id = get_scan_id_by_name(token, SCAN_NAME)

        if scan_id:
            # Launch the selected scan
            result = launch_scan_by_id(token, scan_id)
            # print(result)
            print(f"Scan '{SCAN_NAME}' launched successfully. Scan ID: {scan_id}")
        else:
            print(f"Scan with name '{SCAN_NAME}' not found.")
    else:
        print("Failed to obtain Nessus API token.")

if __name__ == "__main__":
    main()
