# ==========================
# PLATFORM
# ==========================
# Corregido: olympterade -> olympmetrade
URL = "https://olymptrade.com/platform"

# ==========================
# CONTEXT
# ==========================
MIN_CANDLE_HISTORY = 8  # Recomendado entre 8-10 para el ZigZag

# ==========================
# ZIGZAG SETTINGS
# ==========================
ZIGZAG_DEVIATION = 4.0

# ==========================
# PRECISION (CONSERVATIVE STRATEGY)
# ==========================
ZZ_TOLERANCE = 2.0
WICK_FACTOR = 0.35       # 0.35 = Filtro de mecha exigente (Sniper)

# ==========================
# RISK CONTROL
# ==========================
COOLDOWN_SECONDS = 65
REANALYSIS_CANDLES = 7

# ==========================
# SELECTORS (OLYMP TRADE 2026)
# ==========================
SELECTORS = {
    "btn_up": 'button[data-test="deal-button-up"]',
    "btn_down": 'button[data-test="deal-button-down"]',
    # Selector de precio actualizado para mayor estabilidad
    "price": 'div[data-test="current-price"]',
    "last_result": 'div[data-test="closed-deals-item"]'
}