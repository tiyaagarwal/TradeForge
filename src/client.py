import os
from binance import Client

def get_binance_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        raise ValueError("Error: API keys must be set as environment variables.")
    client = Client(api_key, api_secret, testnet=True)
    client.API_URL = "https://testnet.binance.vision/api"
    print("Successfully connected to Binance Testnet.")
    return client

