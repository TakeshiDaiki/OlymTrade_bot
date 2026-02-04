def create_candle(prices):
    """
    Converts a list of price ticks into a standard OHLC candle.
    """
    if not prices:
        return None
    return {
        "open": prices[0],
        "high": max(prices),
        "low": min(prices),
        "close": prices[-1]
    }


def calculate_zigzag(candles, deviation):
    """
    Identifies price reversal points based on a percentage deviation.
    """
    if len(candles) < 2:
        return []

    vertices = []
    # Using 'close' prices for the ZigZag line calculation
    prices = [v["close"] for v in candles]

    for i in range(1, len(prices)):
        # Calculate percentage change between current and previous price
        price_change = abs((prices[i] - prices[i - 1]) / prices[i - 1]) * 100

        if price_change >= deviation:
            vertices.append({
                "price": prices[i],
                "index": i
            })

    return vertices