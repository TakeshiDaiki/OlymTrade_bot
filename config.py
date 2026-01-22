# ==========================
# PLATFORM
# ==========================
URL = "https://olympterade.com/platform"

# ==========================
# CONTEXT
# ==========================
MIN_CANDLE_HISTORY = 8  # Recommended to keep between 8-10

# ==========================
# ZIGZAG SETTINGS
# ==========================
ZIGZAG_DEVIATION = 4.0

# ==========================
# PRECISION (CONSERVATIVE STRATEGY)
# ==========================
ZZ_TOLERANCE = 2.0
WICK_FACTOR = 0.35       # Higher = more demanding rejection filter

# ==========================
# RISK CONTROL
# ==========================
COOLDOWN_SECONDS = 65
REANALYSIS_CANDLES = 7

# ==========================
# SELECTORS (OLYMP TRADE)
# ==========================
SELECTORS = {
    "btn_up": 'button[data-test="deal-button-up"]',
    "btn_down": 'button[data-test="deal-button-down"]',
    "price": 'span[class*="price"]',
    "last_result": 'div[data-test="closed-deals-item"]' # For automatic result detection
}