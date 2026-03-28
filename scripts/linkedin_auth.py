#!/usr/bin/env python3
"""
LinkedIn OAuth flow - gets an access token and saves it to .env
Run once to authenticate, then use the token in other scripts.
"""

import os
import sys
import urllib.parse
import urllib.request
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

DOTENV = Path(__file__).parent.parent / ".env"

def load_env():
    env = {}
    if DOTENV.exists():
        for line in DOTENV.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

def save_env(updates: dict):
    env = load_env()
    env.update(updates)
    lines = [f"{k}={v}" for k, v in env.items()]
    DOTENV.write_text("\n".join(lines) + "\n")

AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
PROFILE_URL = "https://api.linkedin.com/v2/userinfo"
REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = "openid profile w_member_social"

auth_code = None

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h2>Authenticated! You can close this tab.</h2>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h2>Error: no code returned.</h2>")

    def log_message(self, format, *args):
        pass  # suppress request logs

def main():
    env = load_env()
    client_id = env.get("LINKEDIN_CLIENT_ID")
    client_secret = env.get("LINKEDIN_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("ERROR: LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET must be set in .env")
        sys.exit(1)

    # Build auth URL
    params = urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    })
    url = f"{AUTH_URL}?{params}"

    print("Opening LinkedIn auth page in your browser...")
    print(f"If it doesn't open, visit:\n  {url}\n")
    webbrowser.open(url)

    # Wait for callback
    server = HTTPServer(("localhost", 8000), CallbackHandler)
    print("Waiting for LinkedIn callback on http://localhost:8000/callback ...")
    server.handle_request()

    if not auth_code:
        print("ERROR: no auth code received")
        sys.exit(1)

    print("Got auth code, exchanging for access token...")

    # Exchange code for token
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()

    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(req) as resp:
        token_data = json.loads(resp.read())

    access_token = token_data.get("access_token")
    if not access_token:
        print(f"ERROR: {token_data}")
        sys.exit(1)

    print("Got access token. Fetching your profile URN...")

    # Get person URN
    req2 = urllib.request.Request(PROFILE_URL)
    req2.add_header("Authorization", f"Bearer {access_token}")
    with urllib.request.urlopen(req2) as resp:
        profile = json.loads(resp.read())

    person_urn = profile.get("sub")  # OpenID Connect subject = LinkedIn URN
    name = profile.get("name", "unknown")

    print(f"Authenticated as: {name}")
    print(f"Person URN: {person_urn}")

    save_env({
        "LINKEDIN_ACCESS_TOKEN": access_token,
        "LINKEDIN_PERSON_URN": person_urn,
    })

    print(f"\nSaved to .env")
    print("You're ready to post to LinkedIn.")

if __name__ == "__main__":
    main()
