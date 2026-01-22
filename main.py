import time
from datetime import datetime
from core.browser import TradingBrowser
from logic.indicators import create_candle
from logic.strategy import analyze_signal
import config


def main():
    print("\n" + "=" * 40 + "\n   AUTOMATED TRADING SYSTEM\n" + "=" * 40)
    try:
        max_trades = int(input("Total trades for today?: "))
        max_losses = int(input("Stop Loss limit (max losses)?: "))
    except ValueError:
        print("[!] Error: Please enter valid integer numbers.")
        return

    bot = TradingBrowser()
    trades_completed = 0
    losses_detected = 0
    is_trading = False
    last_trade_time = 0

    try:
        bot.start()  # Changed from iniciar() to start()
        closed_candles = []
        current_ticks = []

        while True:
            # 1. LIMIT VERIFICATION
            if trades_completed >= max_trades:
                print("\n[FINISH] Daily trade limit reached.")
                break
            if losses_detected >= max_losses:
                print("\n[STOP LOSS] Max loss limit reached. Stopping bot.")
                break

            now = datetime.now()
            price = bot.get_current_price()
            asset = bot.get_current_asset()

            if price:
                current_ticks.append(price)
                # VISUAL MONITOR (STATUS BAR)
                if now.second % 5 == 0:
                    # Automatic result check after 70 seconds
                    if is_trading and (time.time() - last_trade_time) > 70:
                        result = bot.get_last_result()
                        if result == "LOSS":
                            losses_detected += 1
                            print("\n[RESULT] Last trade: LOSS ❌")
                        elif result == "WIN":
                            print("\n[RESULT] Last trade: WIN ✅")

                        # If result is no longer PENDING, release the lock
                        if result != "PENDING":
                            is_trading = False

                    status = f"Losses: {losses_detected}/{max_losses} | Trades: {trades_completed}/{max_trades}"
                    print(f"[{asset}] {price} | Candles: {len(closed_candles)} | {status}      ", end="\r")

            # 2. SIGNAL ANALYSIS
            if now.second == 0 and len(current_ticks) > 20:
                print(f"\n[{now.strftime('%H:%M')}] Analyzing market...")
                new_candle = create_candle(current_ticks)
                closed_candles.append(new_candle)
                current_ticks = []

                if len(closed_candles) >= config.MIN_CANDLE_HISTORY:
                    signal = analyze_signal(closed_candles, config.ZIGZAG_DEVIATION)

                    # Avoid duplicate orders in the same minute
                    if signal and (time.time() - last_trade_time) > 60:
                        if bot.execute_order(signal):
                            trades_completed += 1
                            is_trading = True
                            last_trade_time = time.time()
                            print("Order placed. Searching for next opportunity...")
                else:
                    print(f"Building history: {len(closed_candles)}/{config.MIN_CANDLE_HISTORY}")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nBot stopped manually by user.")
    finally:
        bot.close()


if __name__ == "__main__":
    main()