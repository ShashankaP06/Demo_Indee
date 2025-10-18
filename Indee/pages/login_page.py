from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import logger


class LoginPage(BasePage):
    
    PIN_INPUT = (By.XPATH, "//input[@type='text' or @type='password']")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' or contains(text(), 'Submit') or contains(text(), 'Sign In')]")
    COOKIE_ACCEPT = (By.XPATH, "//button[contains(text(), 'Accept All') or contains(text(), 'Accept all')]")
    
    def navigate_to(self, url):
        self.driver.get(url)
    
    def enter_pin(self, pin):
        logger.info("Entering PIN...")
        self.send_keys(self.PIN_INPUT, pin)
        logger.info("✓ PIN entered")
    
    def click_submit(self):
        logger.info("Clicking submit button...")
        self.click(self.SUBMIT_BUTTON)
        logger.info("✓ Submit clicked")
    
    def accept_cookies(self):
        try:
            logger.info("Looking for cookie popup...")
            import time
            time.sleep(2)
            self.click(self.COOKIE_ACCEPT, timeout=5)
            logger.info("✓ Cookie consent accepted")
        except:
            logger.info("No cookie popup found")

