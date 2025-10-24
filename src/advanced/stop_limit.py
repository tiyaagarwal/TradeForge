from binance.exceptions import BinanceAPIException
from src.client import get_binance_client
from src.logger_config import log

def place_stop_limit_order(symbol, side, quantity, price, stop_price):
    """
    Places a stop-limit order on the Binance Testnet.
    """
    try:
        client = get_binance_client()
        log.info(f"Attempting stop-limit: {side.upper()} {quantity} {symbol.upper()}")
        log.info(f"Stop Price: {stop_price}, Limit Price: {price}")

        order = client.create_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type='STOP_LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=f'{price:.2f}', # The limit price
            stopPrice=f'{stop_price:.2f}' # The trigger price
        )

        log.info("SUCCESS: Stop-limit order placed.")
        log.info(order)
        print("\n✅ Success! Stop-limit order placed.")
        print(f"   - Order ID: {order['orderId']}")
        print(f"   - Status: {order['status']}")

    except BinanceAPIException as e:
        log.error(f"API ERROR: {e}")
        print(f"\n❌ API Error: {e.message}")
    except Exception as e:
        log.error(f"UNEXPECTED ERROR: {e}")
        print(f"\n❌ An unexpected error occurred: {e}")
