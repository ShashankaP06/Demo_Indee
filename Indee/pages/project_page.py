from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import logger


class ProjectPage(BasePage):
    
    # Tab locators based on actual HTML structure
    DETAILS_TAB = (By.XPATH, "//a[@id='detailsSection' and @aria-label='Details'] | //a[@role='menuitem' and contains(text(), 'Details')]")
    VIDEOS_TAB = (By.XPATH, "//a[@role='menuitem' and contains(text(), 'Videos')] | //a[@aria-label='Videos']")
    VIDEO_CARD = (By.XPATH, "//button[contains(@aria-label, 'Play Video')] | //img[@class='video-thumbnail'] | //div[contains(@class, 'video-card')] | //div[@class='play-section']//button | (//button)[1]")
    INFO_BUTTON = (By.XPATH, "//button[@aria-label='Open Info Dialog']")
    PLAY_BUTTON_IN_MODAL = (By.XPATH, "//button[@aria-label='Continue Watching']")
    
    # Modal information locators
    EXPIRES_ON = (By.XPATH, "//*[contains(text(), 'Expires on') or contains(text(), 'Expires On')]")
    REMAINING_VIEWS = (By.XPATH, "//*[contains(text(), 'Remaining Views') or contains(text(), 'Remaining views')]")
    
    def click_details_tab(self):
        """Click Details tab with short timeout (fails fast if not found)"""
        logger.info("Clicking Details tab...")
        self.click(self.DETAILS_TAB, timeout=5)  # Short timeout for fast failure
        logger.info("✓ Details tab clicked")
    
    def click_videos_tab(self):
        """Click Videos tab with short timeout (fails fast if not found)"""
        logger.info("Clicking Videos tab...")
        self.click(self.VIDEOS_TAB, timeout=5)  # Short timeout for fast failure
        logger.info("✓ Videos tab clicked")
    
    def click_video(self):
        logger.info("Clicking video card to open modal...")
        import time
        time.sleep(2)  # Wait for videos to load
        
        # Try multiple strategies - INFO BUTTON FIRST!
        strategies = [
            ("Info button (i icon)", self.INFO_BUTTON),
            ("Play button with aria-label", (By.XPATH, "//button[@aria-label='Play Video']")),
            ("Video card by data attribute", (By.XPATH, "//div[@class='play-section']//button")),
            ("Video thumbnail image", (By.CSS_SELECTOR, "img.video-thumbnail")),
            ("First button in content", (By.XPATH, "(//button[contains(@aria-label, 'Play')])[1]")),
            ("Any play section button", (By.XPATH, "//div[contains(@class, 'play-section')]//button[1]")),
            ("First visible button", (By.XPATH, "(//button[@tabindex='0'])[1]")),
        ]
        
        for strategy_name, locator in strategies:
            try:
                logger.info(f"Trying strategy: {strategy_name}")
                self.click(locator, timeout=5)
                logger.info(f"✓ Video card clicked using: {strategy_name}")
                return
            except Exception as e:
                logger.warning(f"Strategy '{strategy_name}' failed: {str(e)[:100]}")
                continue
        
        # If all strategies fail, raise error
        raise Exception("Could not find video card with any strategy")
    
    def get_modal_info(self):
        """Get and log modal information (Expires On and Remaining Views)"""
        import time
        import re
        
        logger.info("Waiting 5 seconds for modal to fully load...")
        time.sleep(5)  # Wait 5 seconds for modal to fully load
        
        modal_info = {}
        
        # Get all text from the page
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            logger.info("Searching for modal information in page text...")
            
            # Debug: Print first 500 characters of page text to see what's available
            logger.info(f"Page text preview (first 500 chars): {page_text[:500]}")
            
            # Search for "Expires on:" or "Expires On:" pattern
            expires_match = re.search(r'Expires\s+[Oo]n:\s*(.+?)(?:\n|$)', page_text, re.IGNORECASE)
            if expires_match:
                modal_info['expires_on'] = expires_match.group(1).strip()
                logger.info(f"[EXPIRES ON] {modal_info['expires_on']}")
            else:
                logger.warning("Could not find 'Expires On' in page text")
                # Try alternative pattern
                expires_match2 = re.search(r'Expires[^:]*:\s*(.+?)(?:\n|$)', page_text, re.IGNORECASE)
                if expires_match2:
                    modal_info['expires_on'] = expires_match2.group(1).strip()
                    logger.info(f"[EXPIRES ON] (alt pattern) {modal_info['expires_on']}")
                else:
                    modal_info['expires_on'] = "Not found"
            
            # Search for "Remaining Views:" or "Remaining views:" pattern
            views_match = re.search(r'Remaining\s+[Vv]iews:\s*(.+?)(?:\n|$)', page_text, re.IGNORECASE)
            if views_match:
                modal_info['remaining_views'] = views_match.group(1).strip()
                logger.info(f"[REMAINING VIEWS] {modal_info['remaining_views']}")
            else:
                logger.warning("Could not find 'Remaining Views' in page text")
                # Try alternative pattern
                views_match2 = re.search(r'Remaining[^:]*:\s*(.+?)(?:\n|$)', page_text, re.IGNORECASE)
                if views_match2:
                    modal_info['remaining_views'] = views_match2.group(1).strip()
                    logger.info(f"[REMAINING VIEWS] (alt pattern) {modal_info['remaining_views']}")
                else:
                    modal_info['remaining_views'] = "Not found"
                
        except Exception as e:
            logger.error(f"Error extracting modal info: {e}")
            modal_info['expires_on'] = "Error"
            modal_info['remaining_views'] = "Error"
        
        return modal_info
    
    def click_play_in_modal(self):
        """Click the play button inside the modal to start video"""
        import time
        logger.info("Clicking play button in modal...")
        time.sleep(2)  # Wait for modal to be ready
        self.click(self.PLAY_BUTTON_IN_MODAL)
        logger.info("✓ Play button in modal clicked")
        time.sleep(3)  # Wait for video player to load
    
    def click_back(self):
        """Navigate back using browser back button (no dedicated back button in UI)"""
        logger.info("Navigating back using browser back button...")
        self.driver.back()
        logger.info("✓ Navigated back successfully")
        import time
        time.sleep(2)  # Wait for page to load after navigation

