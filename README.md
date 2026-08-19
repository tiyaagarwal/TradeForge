

## Note on Stop-Limit Orders

The code for `stoplimit` is fully implemented in `src/advanced/stop_limit.py`.

However, the `testnet.binance.vision` (Spot Testnet) used for API key generation does not support the `STOP_LIMIT` order type. When run, it correctly connects to the API, but the server returns an `APIError(code=-1116): Invalid orderType`, which is captured in the `bot.log`. The code is correct, but the testnet has this limitation.# Binance CLI Trading Bot

This is a command-line interface (CLI) trading bot built for the Binance Testnet, as required for the Junior Python Developer application.

The bot supports market, limit, and stop-limit orders. All actions and errors are recorded in `bot.log`.

## Setup Instructions

1.  **Navigate to the project folder:**
    ```bash
    cd /path/to/your/binance_bot
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install required libraries:**
    ```bash
    pip install python-binance
    ```

4.  **Set API Keys:**
    You must set your API keys as environment variables in your terminal *before* running the bot.
    ```bash
    export BINANCE_API_KEY="your_api_key_here"
    export BINANCE_API_SECRET="your_secret_key_here"
    ```

## How to Run the Bot

All commands are run from the main project directory.

### Place a Market Order
Buys or sells immediately at the current market price.

**Usage:**
`python3 -m src.main market <SYMBOL> <SIDE> <QUANTITY>`

**Example:**
```bash
python3 -m src.main market BTCUSDT BUY 0.01
```
