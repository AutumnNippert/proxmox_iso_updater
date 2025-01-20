# Proxmox Iso Updater
This is a small program to assist with managing frequently updated isos for Proxmox, like those of Arch Linux, Kali, and other rolling release operating systems.

It utilizes the [/nodes/{node}/storage/{storage}/download-url](https://pve.proxmox.com/pve-docs/api-viewer/index.html#/nodes/{node}/storage/{storage}/download-url) API call.

# Configuration files
## Config.json
This is where you can store the endpoint information of your proxmox
```
{
    "host": "proxmox.domain.tld",
    "port": 8006,
    "storage": "StoragePool:iso"
}
```

## isos.json
This is where you define your urls and regex strings to parse sources for your latest isos:
```
[
    {
        "filename": "arch-linux-latest.iso",
        "url": "https://mirrors.mit.edu/archlinux/iso/latest/",
        "regex": "archlinux-\\d{4}\\.\\d{2}\\.\\d{2}-x86_64\\.iso"
    },
    {
        "filename": "kali-linux-netinst-latest.iso",
        "url": "https://cdimage.kali.org/current/",
        "regex": "kali-linux-\\d{4}\\.\\d{1}-installer-netinst-amd64\\.iso"
    }
]
```

## .env
Here, you will identify your proxmox API key name and value
```
PROXMOX_TOKEN_NAME=<USER>@<REALM>!<TOKEN_ID>
PROXMOX_TOKEN_VALUE=<YOUR_KEY_VALUE>
```

# Proxmox Permissions
From the [docs](https://pve.proxmox.com/pve-docs/api-viewer/index.html#/nodes/{node}/storage/{storage}/download-url):
> Requires allocation access on the storage and as this allows one to probe the (local!) host network indirectly it also requires one of Sys.Modify on / (for backwards compatibility) or the newer Sys.AccessNetwork privilege on the node.
>
> `Check: ["and",["perm","/storage/{storage}",["Datastore.AllocateTemplate"]],["or",["perm","/",["Sys.Audit","Sys.Modify"]],["perm","/nodes/{node}",["Sys.AccessNetwork"]]]]`