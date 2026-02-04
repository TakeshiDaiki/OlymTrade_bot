import time
import sys
import os
from datetime import datetime

# Path configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import config
from core.browser import TradingBrowser
from logic.indicators import create_candle
from logic.strategy import analyze_signal


def main(max_trades=10, max_losses=3):
    """Main trading engine loop"""
    sys.stdout.reconfigure(encoding='utf-8')

    # 1. IMMEDIATE BROWSER INITIALIZATION
    print(">>> OPENING CHROME... PLEASE WAIT", flush=True)
    try:
        bot = TradingBrowser()
        bot.start()
    except Exception as err_bot:
        print(f"\n[CRITICAL ERROR] Failed to launch browser: {err_bot}", flush=True)
        return

    # 2. SYSTEM COUNTDOWN - FORCED OVERWRITE FORMAT
    print("\n>>> SYSTEM INITIALIZING: PLEASE LOG IN", flush=True)
    for i in range(120, 0, -1):
        # We use a unique prefix @@ to tell the GUI: "DELETE LAST LINE BEFORE PRINTING THIS"
        sys.stdout.write(f"@@Initializing in: {i}s... Please login and set the asset.\n")
        sys.stdout.flush()
        time.sleep(1)

    print("\n[OK] Monitoring started.\n", flush=True)

    trades_completed = 0
    losses_detected = 0
    is_trading = False
    entry_price = 0.0
    expiry_time = 0.0
    current_side = None

    try:
        closed_candles = []
        current_ticks = []

        while True:
            if trades_completed >= max_trades or losses_detected >= max_losses:
                print("\n[FINISH] Limits reached.", flush=True)
                break

            now = datetime.now()
            price = bot.get_current_price()
            asset = bot.get_current_asset()

            if price:
                current_ticks.append(price)
                status = f"L: {losses_detected}/{max_losses} | T: {trades_completed}/{max_trades}"

                # RESULT DETECTION
                if is_trading and time.time() >= expiry_time:
                    exit_price = price
                    if exit_price == entry_price:
                        res_msg = "TIE"
                    elif current_side == "CALL":
                        res_msg = "WIN" if exit_price > entry_price else "LOSS"
                    else:
                        res_msg = "WIN" if exit_price < entry_price else "LOSS"

                    if res_msg == "LOSS": losses_detected += 1
                    print(f"\n[RESULT] {current_side} @ {entry_price} -> {exit_price} | {res_msg}\n", flush=True)
                    is_trading = False

                # CANDLE LOGIC
                if now.second == 0 and len(current_ticks) > 5:
                    # FIXED LINE when candle closes
                    print(f"[{now.strftime('%H:%M')}] {asset}: {price} | Candle Closed | {status}", flush=True)

                    new_candle = create_candle(current_ticks)
                    closed_candles.append(new_candle)
                    current_ticks = []

                    if len(closed_candles) >= config.MIN_CANDLE_HISTORY:
                        signal = analyze_signal(closed_candles, config.ZIGZAG_DEVIATION)
                        if signal and not is_trading:
                            if bot.execute_order(signal):
                                trades_completed += 1
                                is_trading = True
                                entry_price = price
                                current_side = signal
                                expiry_time = time.time() + 60
                                print(f"[{now.strftime('%H:%M')}] {signal} ORDER PLACED AT {entry_price}", flush=True)
                else:
                    # LIVE UPDATE - We use @@ to tell GUI to overwrite
                    sys.stdout.write(f"@@[{now.strftime('%H:%M:%S')}] {asset}: {price} | Live... | {status}\n")
                    sys.stdout.flush()

            time.sleep(0.5)

    except Exception as err_loop:
        print(f"\n[ERROR] System Failure: {err_loop}", flush=True)
    finally:
        bot.close()