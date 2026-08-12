import os
import sys
import pandas as pd
import requests


# 1. Read access token from TOKEN.txt
def load_token():
    token_file = "TOKEN.txt"
    if not os.path.exists(token_file):
        print(
            f"Error: '{token_file}' not found! Run get_token.py first to generate it."
        )
        sys.exit(1)

    with open(token_file, "r") as f:
        token = f.read().strip()

    if not token:
        print(f"Error: '{token_file}' is empty!")
        sys.exit(1)

    return token


ACCESS_TOKEN = load_token()

# 2. Setup Parameters & Call API
url = "https://gateway.saxobank.com/sim/openapi/chart/v3/charts"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Change parameters as needed (e.g., Uic: 21 for EURUSD, 211 for Apple)
params = {
    "Uic": 21,
    "AssetType": "FxSpot",
    "Horizon": 1440,  # 1440 = Daily candles, 1 = 1-min intraday
    "Count": 15,
    "FieldGroups": "Data",
}

print("Fetching candles from Saxo Bank using TOKEN.txt...")
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json().get("Data", [])
    if data:
        df = pd.DataFrame(data)

        print("\nSUCCESS! Here are your candles:")
        print(df.tail(5))

        df.to_csv("eurusd_candles.csv", index=False)
        print("\nSaved to 'eurusd_candles.csv'!")
    else:
        print("No data returned.")
else:
    print(f"Error {response.status_code}: {response.text}")