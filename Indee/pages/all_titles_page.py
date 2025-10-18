from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import logger


class AllTitlesPage(BasePage):
    
    FIRST_BUTTON = (By.XPATH, "//button[@role='button']")
    PROJECT_CARD = (By.XPATH, "//*[contains(text(), 'Test Automation') or contains(text(), 'Test automation')]")
    # Logout button locator based on actual HTML structure (icon button with ID)
    LOGOUT_BUTTON = (By.ID, "signOutSideBar")
    
    def click_first_brand(self):
        logger.info("Clicking first brand button...")
        self.wait_seconds(2)
        try:
            self.click(self.FIRST_BUTTON)
            logger.info("✓ First brand button clicked")
        except:
            logger.warning("No first button found")
    
    def click_project(self):
        logger.info("Clicking Test Automation Project card...")
        self.wait_seconds(2)
        self.click(self.PROJECT_CARD)
        logger.info("✓ Project card clicked")
    
    def logout(self):
        logger.info("Clicking logout button...")
        self.click(self.LOGOUT_BUTTON)
        logger.info("✓ Logged out successfully")

