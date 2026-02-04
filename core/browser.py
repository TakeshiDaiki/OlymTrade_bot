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
import re
from datetime import datetime


class TradingBrowser:
    def __init__(self):
        try:
            # Install driver and open Chrome immediately
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)

            # Load URL right away
            self.driver.get(config.URL)
        except WebDriverException as err_init:
            print(f"[ERROR] Could not start Chrome: {err_init}")
            raise

    def start(self):
        """Prints status. self is used here to avoid static method warning."""
        if self.driver:
            print("\n" + "=" * 55)
            print(">>> BROWSER READY: PLEASE LOG IN AND PREPARE ASSETS")
            print("=" * 55)

    def get_current_asset(self):
        try:
            title = self.driver.title
            if "|" in title:
                return title.split("|")[0].strip()
            return "Asset"
        except (WebDriverException, AttributeError):
            return "Searching..."

    def get_current_price(self):
        try:
            match = re.search(r"(\d+[.,]\d+)", self.driver.title)
            if match:
                return float(match.group(1).replace(',', '.'))

            el = self.driver.find_element(By.CSS_SELECTOR, config.SELECTORS['price'])
            return float(re.sub(r'[^\d.]', '', el.text.replace(',', '.')))
        except (NoSuchElementException, ValueError, WebDriverException):
            return None

    def execute_order(self, direction):
        try:
            sel_key = 'btn_up' if direction == "CALL" else 'btn_down'
            selector = config.SELECTORS[sel_key]

            button = self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            button.click()
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] [OK] {direction} ORDER PLACED")
            return True
        except (TimeoutException, WebDriverException, NoSuchElementException):
            print(f"\n[ERROR] The {direction} button is not available.")
            return False

    def close(self):
        try:
            if self.driver:
                self.driver.quit()
        except WebDriverException:
            pass