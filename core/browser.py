from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    TimeoutException
)
from webdriver_manager.chrome import ChromeDriverManager
import config
import time
import re
from datetime import datetime


class TradingBrowser:
    def __init__(self):
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
        except WebDriverException as e:
            print(f"[ERROR] Could not start Chrome: {e}")
            raise

    def start(self):
        """Starts the browser and waits for manual login/setup."""
        self.driver.get(config.URL)
        print("\n" + "=" * 55)
        print("🚀 LOGIN AND OPEN THE CLOSED DEALS PANEL (60s)")
        print("=" * 55)
        for i in range(60, 0, -1):
            print(f"Bot active in: {i}s...   ", end="\r")
            time.sleep(1)
        print("\n✅ Monitoring started.\n")

    def get_current_asset(self):
        """Extracts the asset name from the window title."""
        try:
            title = self.driver.title
            if "|" in title:
                return title.split("|")[0].strip()
            return "Asset"
        except (WebDriverException, AttributeError):
            return "Searching..."

    def get_current_price(self):
        """Gets the current price from the title or the visual element."""
        try:
            # First try to get price from browser title
            match = re.search(r"(\d+[.,]\d+)", self.driver.title)
            if match:
                return float(match.group(1).replace(',', '.'))

            # Fallback to CSS selector
            el = self.driver.find_element(By.CSS_SELECTOR, config.SELECTORS['price'])
            return float(re.sub(r'[^\d.]', '', el.text.replace(',', '.')))
        except (NoSuchElementException, ValueError, WebDriverException):
            return None

    def execute_order(self, direction):
        """Executes buy or sell and handles button timeout."""
        try:
            selector = config.SELECTORS['btn_up'] if direction == "UP" else config.SELECTORS['btn_down']
            button = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            button.click()
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ✅ {direction} ORDER PLACED")
            return True
        except (TimeoutException, WebDriverException, NoSuchElementException):
            print(f"\n[ERROR] The {direction} button is not available.")
            return False

    def get_last_result(self):
        """Reads the history to determine the result automatically."""
        try:
            # Looks for the last item in the closed deals history
            history_selector = config.SELECTORS.get('last_result', 'div[data-test="closed-deals-item"]')
            last_deal = self.driver.find_element(By.CSS_SELECTOR, history_selector)
            text = last_deal.text.lower()

            # If text indicates a loss (usually 0.00 or a minus sign)
            if "-" in text or "0.00" in text:
                return "LOSS"
            return "WIN"
        except (NoSuchElementException, WebDriverException):
            return "PENDING"

    def close(self):
        """Closes the browser safely."""
        try:
            if self.driver:
                self.driver.quit()
        except WebDriverException:
            pass