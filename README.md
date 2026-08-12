Here is a professional and well-structured `README.md` file for your GitHub repository. You can copy and paste this directly into your repo.

***

# 📈 Saxo Bank OpenAPI Data Downloader

A simple Python project to authenticate with the **Saxo Bank OpenAPI** (Simulation environment) using OAuth 2.0 PKCE, and download historical candlestick (OHLC) data directly into a CSV file.

## 🚀 Features
* **Automated OAuth 2.0 PKCE Flow:** Generates the code verifier/challenge and spins up a local server to catch the authorization callback automatically.
* **Token Management:** Securely saves the access token to a local `TOKEN.txt` file.
* **Data Fetching:** Easily fetch historical candles for various assets (Forex, Stocks, etc.).
* **Data Export:** Exports the fetched data into a clean CSV format using Pandas.

## 🛠 Prerequisites
* Python 3.6+
* A Saxo Bank OpenAPI Developer Account (If you don't have one, sign up at the [Saxo Developer Portal](https://www.developer.saxo/)).
* Required Python packages: `requests`, `pandas`

## ⚙️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Install dependencies:**
   ```bash
   pip install requests pandas
   ```

3. **Configure your Saxo App:**
   * Log into the Saxo Developer Portal and create an App.
   * Ensure your app's **Redirect URI** is set exactly to: `http://localhost:8000/callback`
   * Copy your **App Key** (Client ID).

4. **Update the Python script:**
   * Open `get_token.py`.
   * Replace `YOUR_APP_KEY_HERE` with your actual Saxo App Key.
   ```python
   APP_KEY = "YOUR_ACTUAL_APP_KEY_HERE"
   ```

## 📖 Usage

### Step 1: Get your Access Token
Run the token generation script:
```bash
python get_token.py
```
* The terminal will print an authorization URL. 
* **Open that link in your browser.**
* Log in with your Saxo credentials and approve the permissions.
* Once approved, your browser will show a success message, and the script will automatically save the token to a file named `TOKEN.txt` in the same folder.

### Step 2: Download Candle Data
Run the download script:
```bash
python download_candles.py
```
* The script will read the `TOKEN.txt` file, call the Saxo Chart API, print the last 5 candles to your console, and save the full dataset to `eurusd_candles.csv`.

## 🔧 Customization (Changing the Asset or Timeframe)

You can easily change what data you download by modifying the `params` dictionary inside `download_candles.py`:

```python
params = {
    "Uic": 21,            # 21 = EURUSD, 211 = Apple Stocks
    "AssetType": "FxSpot", # FxSpot, Stock, CfdOnStock, etc.
    "Horizon": 1440,      # 1440 = Daily candles, 1 = 1-minute candles
    "Count": 15,          # Number of candles to fetch
    "FieldGroups": "Data",
}
```
*Note: To find the `Uic` for other instruments, you can use the Saxo OpenAPI Instrument Search endpoint.*

## ⚠️ Important Notes
* This code currently targets the **Saxo Simulation environment** (`sim.logonvalidation.net` and `gateway.saxobank.com/sim/...`). To use it in a live trading environment, you will need to change the URLs to the live endpoints and use a Live App Key.
* Access tokens expire. If you get a `401 Unauthorized` error when running `download_candles.py`, simply run `get_token.py` again to generate a new token.
* **Never commit your `TOKEN.txt` or your actual App Key to GitHub.** (Consider adding `TOKEN.txt` to your `.gitignore` file).
