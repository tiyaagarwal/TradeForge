import sys
from unittest.mock import patch

import pytest

from src import main as cli


def run(*argv):
    with patch.object(sys, 'argv', ['tradeforge', *argv]):
        cli.main()


@pytest.mark.parametrize('qty', ['0', '-1', 'nan', 'inf'])
def test_rejects_non_positive_or_non_finite_quantity(qty):
    with pytest.raises(SystemExit):
        run('market', 'BTCUSDT', 'BUY', qty)


@patch('src.main.place_market_order')
def test_side_is_case_insensitive(place):
    run('market', 'BTCUSDT', 'buy', '0.01')
    place.assert_called_once_with('BTCUSDT', 'BUY', 0.01)
