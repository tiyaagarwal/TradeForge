from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from src.logger_config import log

def get_symbol_filters(client, symbol):
    """
    Fetches the price tick size and quantity step size Binance enforces for a symbol.
    Orders whose price or quantity is not a multiple of these are rejected (-1013).
    """
    info = client.get_symbol_info(symbol.upper())
    if info is None:
        raise ValueError(f"Unknown symbol: {symbol.upper()}")
    filters = {f['filterType']: f for f in info['filters']}
    return {
        'tick_size': filters['PRICE_FILTER']['tickSize'],
        'step_size': filters['LOT_SIZE']['stepSize'],
        'min_qty': filters['LOT_SIZE']['minQty'],
    }

def round_to_step(value, step, rounding=ROUND_DOWN):
    """
    Rounds value to a multiple of step and returns it as a plain decimal string
    (no exponent, no trailing zeros), e.g. round_to_step(0.123456, '0.00100000') -> '0.123'.
    """
    value = Decimal(str(value))
    step = Decimal(str(step))
    if step != 0:
        value = (value / step).to_integral_value(rounding=rounding) * step
    return format(value.normalize(), 'f')

def format_price(price, filters):
    """Rounds a price to the nearest valid tick."""
    formatted = round_to_step(price, filters['tick_size'], rounding=ROUND_HALF_UP)
    if Decimal(formatted) <= 0:
        raise ValueError(f"Price {price} is below the minimum tick size {filters['tick_size']}.")
    if Decimal(formatted) != Decimal(str(price)):
        log.warning(f"Price {price} adjusted to {formatted} (tick size {filters['tick_size']}).")
    return formatted

def format_quantity(quantity, filters):
    """Rounds a quantity down to a valid lot step, so we never trade more than asked."""
    formatted = round_to_step(quantity, filters['step_size'])
    if Decimal(formatted) < Decimal(filters['min_qty']) or Decimal(formatted) <= 0:
        raise ValueError(f"Quantity {quantity} is below the minimum order quantity {Decimal(filters['min_qty']).normalize():f}.")
    if Decimal(formatted) != Decimal(str(quantity)):
        log.warning(f"Quantity {quantity} adjusted to {formatted} (step size {filters['step_size']}).")
    return formatted
