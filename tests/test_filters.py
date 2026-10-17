from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from src.advanced.twap import split_quantity
from src.filters import format_price, format_quantity, get_symbol_filters, round_to_step

BTC_FILTERS = {'tick_size': '0.01000000', 'step_size': '0.00001000', 'min_qty': '0.00001000'}
DOGE_FILTERS = {'tick_size': '0.00001000', 'step_size': '1.00000000', 'min_qty': '1.00000000'}


def test_round_to_step_returns_plain_string():
    assert round_to_step(0.123456, '0.00100000') == '0.123'
    assert round_to_step(60000, '0.01000000') == '60000'
    assert round_to_step(0.00001234, '0.00000001') == '0.00001234'


def test_price_keeps_precision_of_low_priced_symbols():
    # The old f'{price:.2f}' sent '0.12' here (and '0.00' for sub-cent coins).
    assert format_price(0.12345, DOGE_FILTERS) == '0.12345'
    assert format_price(0.123456, DOGE_FILTERS) == '0.12346'


def test_price_rounds_to_nearest_tick():
    assert format_price(60000.126, BTC_FILTERS) == '60000.13'


def test_price_below_one_tick_is_rejected():
    with pytest.raises(ValueError):
        format_price(0.001, BTC_FILTERS)


def test_quantity_rounds_down_to_step():
    assert format_quantity(0.0123456, BTC_FILTERS) == '0.01234'
    assert format_quantity(10.9, DOGE_FILTERS) == '10'


def test_quantity_below_min_qty_is_rejected():
    with pytest.raises(ValueError):
        format_quantity(0.5, DOGE_FILTERS)


def test_get_symbol_filters_reads_exchange_info():
    client = MagicMock()
    client.get_symbol_info.return_value = {
        'filters': [
            {'filterType': 'PRICE_FILTER', 'tickSize': '0.01000000'},
            {'filterType': 'LOT_SIZE', 'stepSize': '0.00001000', 'minQty': '0.00001000'},
        ]
    }
    assert get_symbol_filters(client, 'btcusdt') == BTC_FILTERS
    client.get_symbol_info.assert_called_once_with('BTCUSDT')


def test_get_symbol_filters_unknown_symbol():
    client = MagicMock()
    client.get_symbol_info.return_value = None
    with pytest.raises(ValueError):
        get_symbol_filters(client, 'NOPEUSDT')


def test_twap_slices_are_step_aligned_and_sum_to_total():
    slices = split_quantity(0.00123, 10, BTC_FILTERS)
    assert len(slices) == 10
    assert slices[:9] == [Decimal('0.00012')] * 9
    assert slices[-1] == Decimal('0.00015')
    assert sum(slices) == Decimal('0.00123')
    step = Decimal(BTC_FILTERS['step_size'])
    assert all(s % step == 0 for s in slices)


@patch('src.limit_orders.get_binance_client')
def test_limit_order_sends_tick_aligned_price(get_client):
    from src.limit_orders import place_limit_order

    client = get_client.return_value
    client.get_symbol_info.return_value = {
        'filters': [
            {'filterType': 'PRICE_FILTER', 'tickSize': '0.00001000'},
            {'filterType': 'LOT_SIZE', 'stepSize': '1.00000000', 'minQty': '1.00000000'},
        ]
    }
    client.create_order.return_value = {'symbol': 'DOGEUSDT', 'orderId': 1, 'status': 'NEW'}

    place_limit_order('dogeusdt', 'buy', 100, 0.12345)

    kwargs = client.create_order.call_args.kwargs
    assert kwargs['price'] == '0.12345'
    assert kwargs['quantity'] == '100'
    assert kwargs['symbol'] == 'DOGEUSDT'
