import base64
import hashlib
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

APP_KEY = "YOUR_APP_KEY_HERE"  # Insert App Key here
REDIRECT_URI = "http://localhost:8000/callback"


def generate_pkce():
    verifier = (
        base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8").rstrip("=")
    )
    challenge = (
        base64.urlsafe_b64encode(
            hashlib.sha256(verifier.encode("utf-8")).digest()
        )
        .decode("utf-8")
        .rstrip("=")
    )
    return verifier, challenge


code_verifier, code_challenge = generate_pkce()
auth_code = None


class CallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global auth_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                b"Authorization successful! TOKEN.txt has been updated."
            )


auth_url = (
    f"https://sim.logonvalidation.net/authorize?"
    f"response_type=code&client_id={APP_KEY}&"
    f"redirect_uri={urllib.parse.quote(REDIRECT_URI)}&"
    f"code_challenge={code_challenge}&code_challenge_method=S256"
)

print(f"\n1. Open this link in your browser:\n{auth_url}\n")

server = HTTPServer(("localhost", 8000), CallbackHandler)
server.handle_request()

# Exchange Code for Token
res = requests.post(
    "https://sim.logonvalidation.net/token",
    data={
        "grant_type": "authorization_code",
        "client_id": APP_KEY,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    },
)

tokens = res.json()
access_token = tokens.get("access_token")

if access_token:
    # Save automatically to TOKEN.txt
    with open("TOKEN.txt", "w") as f:
        f.write(access_token.strip())

    print("\n================ SUCCESS ================")
    print("Token automatically saved to TOKEN.txt!")
    print("=========================================\n")
else:
    print("\nFailed to retrieve token:", tokens)