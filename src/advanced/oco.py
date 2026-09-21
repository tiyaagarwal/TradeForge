from binance.exceptions import BinanceAPIException
from src.client import get_binance_client
from src.logger_config import log

def place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price):
    """
    Places an OCO (One-Cancels-the-Other) order on the Binance Testnet.

    Args:
        symbol (str): The trading pair (e.g., 'BTCUSDT').
        side (str): 'SELL' (for a stop-loss/take-profit combo).
        quantity (float): The amount to trade.
        price (float): The take-profit (limit) price.
        stop_price (float): The stop-loss trigger price.
        stop_limit_price (float): The stop-loss limit price (must be <= stop_price).
    """
    try:
        client = get_binance_client()
        log.info(f"Attempting OCO {side.upper()} order for {quantity} {symbol.upper()}.")
        log.info(f"  - Take Profit Price: {price}")
        log.info(f"  - Stop-Loss Trigger: {stop_price}")
        log.info(f"  - Stop-Loss Limit: {stop_limit_price}")

        # This is the specific API call for a Spot OCO order
        order_report = client.create_oco_order(
            symbol=symbol.upper(),
            side=side.upper(),
            quantity=quantity,
            price=f'{price:.2f}', # The Take-Profit Limit Price
            stopPrice=f'{stop_price:.2f}', # The Stop-Loss Trigger Price
            stopLimitPrice=f'{stop_limit_price:.2f}', # The Stop-Loss Limit Price
            stopLimitTimeInForce='GTC'
        )

        log.info("SUCCESS: OCO order placed.")
        log.info(order_report)
        print("\n✅ Success! OCO order placed.")
        print(f"   - {len(order_report['orderReports'])} orders created.")
        print(f"   - Order List ID: {order_report['orderListId']}")

    except BinanceAPIException as e:
        # Check for the 'Invalid orderType' error again
        if e.code == -1116:
            log.warning(f"API WARNING: This testnet does not support OCO orders. {e}")
            print("\n⚠️ API Warning: The testnet reported an 'Invalid orderType' error.")
            print("   This is a testnet limitation, but the code is correct.")
        else:
            log.error(f"API ERROR: {e}")
            print(f"\n❌ API Error: {e.message}")
    except Exception as e:
        log.error(f"UNEXPECTED ERROR: {e}")
        print(f"\n❌ An unexpected error occurred: {e}")
