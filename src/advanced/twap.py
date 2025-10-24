import time
from src.logger_config import log
from src.market_orders import place_market_order

def execute_twap_order(symbol, side, total_quantity, duration_minutes):
    """
    Executes a TWAP (Time-Weighted Average Price) order by splitting it 
    into 10 smaller market orders placed over a set duration.
    """
    try:
        num_slices = 10  # We'll split the order into 10 smaller pieces
        quantity_per_slice = round(total_quantity / num_slices, 6)

        if quantity_per_slice == 0:
            log.error("TWAP Error: Total quantity is too small to be split.")
            print("\n❌ Error: Total quantity is too small for a 10-slice TWAP.")
            return

        # Calculate the time to wait between each order
        total_duration_seconds = duration_minutes * 60
        sleep_time_seconds = round(total_duration_seconds / num_slices)

        if sleep_time_seconds < 1:
            sleep_time_seconds = 1  # Ensure at least 1 second between orders

        log.info(f"--- Initiating TWAP {side.upper()} Order ---")
        log.info(f"  Total Quantity: {total_quantity} {symbol.upper()}")
        log.info(f"  Duration: {duration_minutes} minutes")
        log.info(f"  Slices: {num_slices} x {quantity_per_slice} {symbol.upper()}")
        log.info(f"  Interval: {sleep_time_seconds} seconds per order")
        print(f"\n--- Executing TWAP {side.upper()} Order ---")
        print(f"Total: {total_quantity} {symbol.upper()} over {duration_minutes} min.")
        print(f"Placing 1 order of {quantity_per_slice} every {sleep_time_seconds}s...")

        for i in range(num_slices):
            log.info(f"TWAP Slice {i+1}/{num_slices}: Placing order...")
            print(f"\nPlacing TWAP slice {i+1}/{num_slices}...")

            # We re-use our existing, proven market order function!
            place_market_order(symbol, side, quantity_per_slice)

            if i < num_slices - 1:
                log.info(f"TWAP: Sleeping for {sleep_time_seconds} seconds...")
                time.sleep(sleep_time_seconds)

        log.info("--- TWAP Order Completed ---")
        print("\n✅ --- TWAP Execution Finished ---")

    except Exception as e:
        log.error(f"TWAP UNEXPECTED ERROR: {e}")
        print(f"\n❌ An unexpected error occurred during TWAP execution: {e}")
