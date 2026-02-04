import time
import sys
from datetime import datetime
from core.browser import TradingBrowser
from logic.indicators import create_candle
from logic.strategy import analyze_signal
import config


def main(max_trades=10, max_losses=3):
    print("\n" + "=" * 40)
    print(f"   AUTOMATED TRADING SYSTEM - SNIPER")
    print(f"   LIMITS: {max_trades} Trades | {max_losses} Losses")
    print("=" * 40 + "\n")

    bot = TradingBrowser()
    trades_completed = 0
    losses_detected = 0
    is_trading = False
    last_trade_time = 0

    try:
        bot.start()
        closed_candles = []
        current_ticks = []

        while True:
            # 1. VERIFICACIÓN DE LÍMITES
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

                # MONITOR VISUAL (Cada 5 segundos)
                if now.second % 5 == 0:
                    # Chequeo automático de resultado después de 70 segundos
                    if is_trading and (time.time() - last_trade_time) > 70:
                        result = bot.get_last_result()
                        if result == "LOSS":
                            losses_detected += 1
                            print("\n[RESULT] Last trade: LOSS [X]")
                        elif result == "WIN":
                            print("\n[RESULT] Last trade: WIN [OK]")

                        if result != "PENDING":
                            is_trading = False

                    status = f"Losses: {losses_detected}/{max_losses} | Trades: {trades_completed}/{max_trades}"
                    # Nota: Quitamos el \r (carro de retorno) para que se vea bien en la consola de la App
                    print(f"[{asset}] {price} | Candles: {len(closed_candles)} | {status}")

            # 2. ANÁLISIS DE SEÑALES
            if now.second == 0 and len(current_ticks) > 20:
                print(f"[{now.strftime('%H:%M')}] Analyzing market...")
                new_candle = create_candle(current_ticks)
                closed_candles.append(new_candle)
                current_ticks = []

                if len(closed_candles) >= config.MIN_CANDLE_HISTORY:
                    signal = analyze_signal(closed_candles, config.ZIGZAG_DEVIATION)

                    if signal and (time.time() - last_trade_time) > 60:
                        if bot.execute_order(signal):
                            trades_completed += 1
                            is_trading = True
                            last_trade_time = time.time()
                            print(f"[{now.strftime('%H:%M')}] Order {signal} placed successfully!")
                else:
                    print(f"Building history: {len(closed_candles)}/{config.MIN_CANDLE_HISTORY}")

            time.sleep(0.5)

    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
    finally:
        bot.close()
        print("Driver closed. Session finished.")


if __name__ == "__main__":
    # Esta parte detecta si la GUI envió argumentos
    # Ejemplo: python main.py 15 5
    if len(sys.argv) > 2:
        try:
            arg_trades = int(sys.argv[1])
            arg_losses = int(sys.argv[2])
            main(max_trades=arg_trades, max_losses=arg_losses)
        except ValueError:
            print("[!] Invalid arguments from GUI. Using defaults.")
            main()
    else:
        # Si lo corres manual, aún puedes usar los inputs o defaults
        main()