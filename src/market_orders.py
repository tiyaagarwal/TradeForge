from binance.exceptions import BinanceAPIException
from src.client import get_binance_client
from src.logger_config import log

def place_market_order(symbol, side, quantity):
    """
    Places a market order on the Binance Testnet.
    """
    try:
        client = get_binance_client()
        log.info(f"Attempting market order: {side.upper()} {quantity} {symbol.upper()}")

        order = client.create_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type='MARKET',
            quantity=quantity
        )

        log.info("SUCCESS: Market order placed.")
        log.info(order)
        print("\n✅ Success! Market order placed.")
        print(f"   - Symbol: {order['symbol']}")
        print(f"   - Order ID: {order['orderId']}")
        print(f"   - Status: {order['status']}")

    except BinanceAPIException as e:
        log.error(f"API ERROR: {e}")
        print(f"\n❌ API Error: {e.message}")
    except Exception as e:
        log.error(f"UNEXPECTED ERROR: {e}")
        print(f"\n❌ An unexpected error occurred: {e}")
