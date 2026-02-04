from logic.indicators import calculate_zigzag
import config


def analyze_signal(candles, deviation):
    """
    Analyzes current market data to find high-probability reversal signals.
    """
    # Safety check: ensure we have enough history
    if len(candles) < config.MIN_CANDLE_HISTORY:
        return None

    vertices = calculate_zigzag(candles, deviation)
    if not vertices:
        return None

    # Get the last ZigZag pivot point (the level we expect a reversal from)
    last_pivot = vertices[-1]["price"]
    current_candle = candles[-1]

    # Calculate Candle Components
    body_size = abs(current_candle["open"] - current_candle["close"])
    upper_wick = current_candle["high"] - max(current_candle["open"], current_candle["close"])
    lower_wick = min(current_candle["open"], current_candle["close"]) - current_candle["low"]

    # Dynamic Tolerance based on Asset Price
    # Uses ZZ_TOLERANCE from config (e.g., 2.0)
    tolerance = last_pivot * (config.ZZ_TOLERANCE / 1000)

    # Check if price touched the reversal level
    hit_resistance = current_candle["high"] >= (last_pivot - tolerance)
    hit_support = current_candle["low"] <= (last_pivot + tolerance)

    # REJECTION LOGIC (The "Sniper" Filter)
    # Only enters if the wick is significantly larger than the body

    # 1. SELL SIGNAL (DOWN)
    if hit_resistance and upper_wick > (body_size * config.WICK_FACTOR):
        return "DOWN"

    # 2. BUY SIGNAL (UP)
    if hit_support and lower_wick > (body_size * config.WICK_FACTOR):
        return "UP"

    return None