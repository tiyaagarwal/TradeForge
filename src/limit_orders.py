from binance.exceptions import BinanceAPIException
from src.client import get_binance_client
from src.filters import get_symbol_filters, format_price, format_quantity
from src.logger_config import log

def place_limit_order(symbol, side, quantity, price):
    """
    Places a limit order on the Binance Testnet.
    """
    try:
        client = get_binance_client()
        filters = get_symbol_filters(client, symbol)
        log.info(f"Attempting limit order: {side.upper()} {quantity} {symbol.upper()} @ {price}")

        order = client.create_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type='LIMIT',
            timeInForce='GTC',
            quantity=format_quantity(quantity, filters),
            price=format_price(price, filters)
        )

        log.info("SUCCESS: Limit order placed.")
        log.info(order)
        print("\n✅ Success! Limit order placed.")
        print(f"   - Symbol: {order['symbol']}")
        print(f"   - Order ID: {order['orderId']}")
        print(f"   - Status: {order['status']}")

    except BinanceAPIException as e:
        log.error(f"API ERROR: {e}")
        print(f"\n❌ API Error: {e.message}")
    except Exception as e:
        log.error(f"UNEXPECTED ERROR: {e}")
        print(f"\n❌ An unexpected error occurred: {e}")
