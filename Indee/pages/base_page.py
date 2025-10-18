from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
    
    def find_element(self, locator, timeout=None):
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_element_located(locator))
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def click(self, locator, timeout=None):
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable(locator))
        else:
            element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def send_keys(self, locator, text, timeout=None):
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def wait_seconds(self, seconds):
        import time
        time.sleep(seconds)

