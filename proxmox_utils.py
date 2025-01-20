import json
import requests
import os

# Because we don't use a valid SSL certificate, we need to disable warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_dotenv(filepath=".env"):
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Skip empty lines and comments

            key, value = line.split("=", 1)
            os.environ[key] = value

# load configs and env vars
load_dotenv()
proxmox_config = json.load(open('config.json', 'r'))

# Proxmox API base URL
api_base = f'https://{proxmox_config["host"]}:{proxmox_config["port"]}/api2/json'
print(f'Proxmox API base URL: {api_base}')

# Proxmox API token
PROXMOX_TOKEN_NAME = os.environ["PROXMOX_TOKEN_NAME"]
PROXMOX_TOKEN_VALUE = os.environ["PROXMOX_TOKEN_VALUE"]

def get_online_node():
    """Fetches the first online node."""
    headers = {
        "Authorization": f"PVEAPIToken={PROXMOX_TOKEN_NAME}={PROXMOX_TOKEN_VALUE}"
    }

    response = requests.get(f"{api_base}/nodes", headers=headers, verify=False)
    if response.status_code != 200:
        print("Failed to fetch nodes:", response.text)
        return None

    nodes = response.json().get("data", [])
    for node in nodes:
        if node.get("status") == "online":
            print(f"Found online node: {node['node']}")
            return node["node"]

    print("No online nodes found.")
    return None

def send_proxmox_iso_download_request(download_url, filename):
    print(f"Sending download request for {filename} from {download_url}")

    # find online node
    node = get_online_node()
    if not node:
        print("No online nodes found, aborting.")
        return
    print(f"Using node: {node}")

    download_endpoint = f'{api_base}/nodes/{node}/storage/{proxmox_config["storage"]}/download-url'

    # Prepare headers for token-based auth
    headers = {
        "Authorization": f"PVEAPIToken={PROXMOX_TOKEN_NAME}={PROXMOX_TOKEN_VALUE}"
    }

    # Prepare the JSON data to send
    payload = {
        "content": "iso",
        "filename": filename,
        "url": download_url,
    }

    response = requests.post(
        download_endpoint,
        headers=headers,
        json=payload,
        verify=False
    )

    try:
        print("Response:", response)
        print("Response JSON:", response.json())
    except Exception as e:
        print("Failed to parse JSON response:", response.text)
