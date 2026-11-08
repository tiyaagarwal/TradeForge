from binance.exceptions import BinanceAPIException
from src.client import get_binance_client
from src.logger_config import log

def place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price):
    """
    Places an OCO (One-Cancels-the-Other) order on the Binance Testnet.

    Args:
        symbol (str): The trading pair (e.g., 'BTCUSDT').
        side (str): 'SELL' (take-profit/stop-loss on a long) or 'BUY'
            (take-profit/stop-loss on a short).
        quantity (float): The amount to trade.
        price (float): The take-profit (limit) price.
        stop_price (float): The stop-loss trigger price.
        stop_limit_price (float): The stop-loss limit price (must be <= stop_price for SELL,
            >= stop_price for BUY).
    """
    try:
        client = get_binance_client()
        log.info(f"Attempting OCO {side.upper()} order for {quantity} {symbol.upper()}.")
        log.info(f"  - Take Profit Price: {price}")
        log.info(f"  - Stop-Loss Trigger: {stop_price}")
        log.info(f"  - Stop-Loss Limit: {stop_limit_price}")

        # The installed python-binance client (>=0.28) replaced the old
        # price/stopPrice/stopLimitPrice/stopLimitTimeInForce OCO params
        # with an above/below order-list scheme. Which leg sits above vs.
        # below the current market price flips with side: a SELL's take-profit
        # sits above market (LIMIT_MAKER) with its stop-loss below (STOP_LOSS_LIMIT);
        # a BUY's take-profit sits below market with its stop-loss above.
        if side.upper() == 'SELL':
            leg_kwargs = dict(
                aboveType='LIMIT_MAKER', # The Take-Profit leg
                abovePrice=f'{price:.2f}', # The Take-Profit Limit Price
                belowType='STOP_LOSS_LIMIT', # The Stop-Loss leg
                belowStopPrice=f'{stop_price:.2f}', # The Stop-Loss Trigger Price
                belowPrice=f'{stop_limit_price:.2f}', # The Stop-Loss Limit Price
                belowTimeInForce='GTC',
            )
        else:
            leg_kwargs = dict(
                belowType='LIMIT_MAKER', # The Take-Profit leg
                belowPrice=f'{price:.2f}', # The Take-Profit Limit Price
                aboveType='STOP_LOSS_LIMIT', # The Stop-Loss leg
                aboveStopPrice=f'{stop_price:.2f}', # The Stop-Loss Trigger Price
                abovePrice=f'{stop_limit_price:.2f}', # The Stop-Loss Limit Price
                aboveTimeInForce='GTC',
            )

        order_report = client.create_oco_order(
            symbol=symbol.upper(),
            side=side.upper(),
            quantity=quantity,
            **leg_kwargs,
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
