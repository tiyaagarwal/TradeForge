import argparse
from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.stop_limit import place_stop_limit_order
from src.advanced.oco import place_oco_order
from src.advanced.twap import execute_twap_order # New import

def main():
    parser = argparse.ArgumentParser(description="TradeForge - a CLI-based Binance trading bot")
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    # --- Market ---
    parser_market = subparsers.add_parser('market', help='Place a market order')
    parser_market.add_argument('symbol', type=str)
    parser_market.add_argument('side', type=str, choices=['BUY', 'SELL'])
    parser_market.add_argument('quantity', type=float)

    # --- Limit ---
    parser_limit = subparsers.add_parser('limit', help='Place a limit order')
    parser_limit.add_argument('symbol', type=str)
    parser_limit.add_argument('side', type=str, choices=['BUY', 'SELL'])
    parser_limit.add_argument('quantity', type=float)
    parser_limit.add_argument('price', type=float)

    # --- Stop-Limit ---
    parser_stop = subparsers.add_parser('stoplimit', help='Place a stop-limit order')
    parser_stop.add_argument('symbol', type=str)
    parser_stop.add_argument('side', type=str, choices=['BUY', 'SELL'])
    parser_stop.add_argument('quantity', type=float)
    parser_stop.add_argument('price', type=float)
    parser_stop.add_argument('stop_price', type=float)

    # --- OCO ---
    parser_oco = subparsers.add_parser('oco', help='Place an OCO order (take-profit + stop-loss)')
    parser_oco.add_argument('symbol', type=str)
    parser_oco.add_argument('side', type=str, choices=['BUY', 'SELL'])
    parser_oco.add_argument('quantity', type=float)
    parser_oco.add_argument('price', type=float)
    parser_oco.add_argument('stop_price', type=float)
    parser_oco.add_argument('stop_limit_price', type=float)

    # --- NEW: TWAP (Time-Weighted Average Price) ---
    parser_twap = subparsers.add_parser('twap', help='Execute a TWAP order over time')
    parser_twap.add_argument('symbol', type=str)
    parser_twap.add_argument('side', type=str, choices=['BUY', 'SELL'])
    parser_twap.add_argument('total_quantity', type=float, help='The total quantity to trade')
    parser_twap.add_argument('duration_minutes', type=int, help='Total duration in minutes')

    args = parser.parse_args()

    # Call the correct function
    if args.command == 'market':
        place_market_order(args.symbol, args.side, args.quantity)
    elif args.command == 'limit':
        place_limit_order(args.symbol, args.side, args.quantity, args.price)
    elif args.command == 'stoplimit':
        place_stop_limit_order(args.symbol, args.side, args.quantity, args.price, args.stop_price)
    elif args.command == 'oco':
        place_oco_order(args.symbol, args.side, args.quantity, args.price, args.stop_price, args.stop_limit_price)
    elif args.command == 'twap':
        execute_twap_order(args.symbol, args.side, args.total_quantity, args.duration_minutes)

if __name__ == "__main__":
    main()
