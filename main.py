import requests
import re
import json

from proxmox_utils import *

isos = json.load(open('isos.json', 'r'))

def get_iso(url, regex):
    html = requests.get(url).text
    iso_file = re.findall(regex, html)
    if not iso_file:
        print(f"Failed to find ISO file at {url}")
        return None
    return url + iso_file[0]

for i in isos:
    regex = re.compile(i['regex'])
    i["complete_url"] = get_iso(i['url'], (i['regex']))
    if i["complete_url"]:
        print(f"{i['filename']} latest at: {i['complete_url']}")
    else:
        print(f"Failed to find {i['filename']}")
        isos.remove(i) # remove if can't find it

for i in isos:
    send_proxmox_iso_download_request(i['complete_url'], i['filename'])