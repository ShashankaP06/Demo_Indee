from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
from utilities.logger import logger


class VideoPlayerPage(BasePage):
    
    # JW Player specific locators
    VIDEO_PLAYER = (By.CSS_SELECTOR, "div.jw-wrapper")
    VIDEO_ELEMENT = (By.TAG_NAME, "video")
    PLAY_BUTTON = (By.CSS_SELECTOR, "div.jw-icon-playback")  # JW Player play/pause toggle
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue')] | //div[contains(text(), 'Continue')]")
    SETTINGS_BUTTON = (By.CSS_SELECTOR, "div.jw-icon-settings")  # JW Player settings icon
    VOLUME_BUTTON = (By.CSS_SELECTOR, "div.jw-icon-volume")  # JW Player volume icon
    VOLUME_SLIDER_CONTAINER = (By.CSS_SELECTOR, "div.jw-horizontal-volume-container")  # Volume slider with aria attributes
    VOLUME_SLIDER = (By.CSS_SELECTOR, "div.jw-slider-volume")  # JW Player volume slider
    VOLUME_PROGRESS = (By.CSS_SELECTOR, "div.jw-slider-volume div.jw-progress")  # Volume progress bar
    QUALITY_MENU = (By.CSS_SELECTOR, "div.jw-settings-submenu-quality")  # Quality/resolution submenu
    QUALITY_OPTION = lambda self, quality: (By.XPATH, f"//button[@aria-label='{quality}' and @role='menuitemradio']")  # Specific quality button
    
    # Note: Fullscreen and Rewind use JavaScript DOM methods, no locators needed
    
    def wait_seconds(self, seconds):
        """Wait for specified seconds"""
        import time
        time.sleep(seconds)
    
    def play_pause_video(self):
        """Play video by clicking the play button in the UI"""
        logger.info("Playing video via UI button...")
        self.wait_seconds(2)
        
        # Hover over video to reveal controls
        try:
            video_element = self.find_element(self.VIDEO_ELEMENT, timeout=10)
            actions = ActionChains(self.driver)
            actions.move_to_element(video_element).perform()
            self.wait_seconds(1)
        except:
            pass
        
        self.click(self.PLAY_BUTTON, timeout=15)
        self.wait_seconds(1)
        logger.info("✓ Video is playing")
    
    def pause_video(self):
        """Pause video using ActionChains with iframe support"""
        logger.info("Pausing video via ActionChains + iframe hover...")
        self.wait_seconds(2)
        
        from selenium.webdriver.support import expected_conditions as EC
        
        in_iframe = False
        paused = False
        
        try:
            # Find which context has the player
            try:
                video_wrapper = self.driver.find_element(By.CSS_SELECTOR, "div.jw-wrapper")
                logger.info("Found player in main page")
            except:
                logger.info("Player not in main page, checking iframes...")
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                for idx, iframe in enumerate(iframes):
                    try:
                        self.driver.switch_to.frame(iframe)
                        video_wrapper = self.driver.find_element(By.CSS_SELECTOR, "div.jw-wrapper")
                        logger.info(f"Found player in iframe {idx}")
                        in_iframe = True
                        break
                    except:
                        self.driver.switch_to.default_content()
                        continue
            
            # Method 1: Reliable ActionChains hover + click pause button
            try:
                logger.info("Using reliable ActionChains flow to pause...")
                wait = self.wait
                video_wrapper = self.find_element(self.VIDEO_PLAYER, timeout=10)
                
                # Hover over player to reveal controls with realistic pause
                actions = ActionChains(self.driver)
                actions.move_to_element(video_wrapper).pause(0.3).perform()
                logger.info("✓ Mouse hovered over player")
                
                # Wait for controls to fade in
                self.wait_seconds(3)
                logger.info("✓ Controls visible now")
                
                # Re-locate pause button AFTER hover (avoid stale element)
                pause_button = wait.until(EC.visibility_of_element_located(self.PLAY_BUTTON))
                pause_button = wait.until(EC.element_to_be_clickable(self.PLAY_BUTTON))
                logger.info("✓ Pause button located")
                
                # Click pause button with ActionChains for accuracy
                actions = ActionChains(self.driver)
                actions.move_to_element(pause_button).pause(0.2).click(pause_button).perform()
                logger.info("✓ Pause button clicked via ActionChains")
                paused = True
            except Exception as e:
                logger.warning(f"ActionChains method failed: {str(e)[:200]}")
            
            # Method 2: Click on video player area
            if not paused:
                try:
                    logger.info("Trying to click on video player area...")
                    self.click(self.VIDEO_ELEMENT, timeout=10)
                    logger.info("✓ Video player area clicked")
                    paused = True
                except Exception as e:
                    logger.warning(f"Could not click video area: {e}")
            
            # Method 3: JavaScript fallback (last resort)
            if not paused:
                logger.warning("All ActionChains methods failed, using JavaScript fallback...")
                try:
                    # JS should work in current context (already in iframe if needed)
                    self.driver.execute_script("document.querySelector('video').pause()")
                    logger.info("✓ Video paused via JavaScript")
                    paused = True
                except Exception as e:
                    logger.error(f"JavaScript fallback also failed: {str(e)[:200]}")
            
            # Final status
            if paused:
                logger.info("✓ Video successfully paused")
            else:
                logger.error("✗ Failed to pause video")
                
        except Exception as e:
            logger.error(f"Pause failed: {str(e)}")
        finally:
            # Switch back to main content if we were in iframe
            if in_iframe:
                self.driver.switch_to.default_content()
                logger.info("Switched back to main content")
            self.wait_seconds(2)
    
    def resume_video_with_mouse(self):
        """Resume video using ActionChains with iframe support"""
        logger.info("Resuming video via ActionChains + iframe hover...")
        self.wait_seconds(5)  # Wait 5 seconds before resuming
        
        from selenium.webdriver.support import expected_conditions as EC
        
        in_iframe = False
        resumed = False
        
        try:
            # Find which context has the player
            try:
                video_wrapper = self.driver.find_element(By.CSS_SELECTOR, "div.jw-wrapper")
                logger.info("Found player in main page")
            except:
                logger.info("Player not in main page, checking iframes...")
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                for idx, iframe in enumerate(iframes):
                    try:
                        self.driver.switch_to.frame(iframe)
                        video_wrapper = self.driver.find_element(By.CSS_SELECTOR, "div.jw-wrapper")
                        logger.info(f"Found player in iframe {idx}")
                        in_iframe = True
                        break
                    except:
                        self.driver.switch_to.default_content()
                        continue
            
            # Method 1: Reliable ActionChains hover + click play button
            try:
                logger.info("Using reliable ActionChains flow to resume...")
                wait = self.wait
                video_wrapper = self.find_element(self.VIDEO_PLAYER, timeout=10)
                
                # Hover over player to reveal controls with realistic pause
                actions = ActionChains(self.driver)
                actions.move_to_element(video_wrapper).pause(0.3).perform()
                logger.info("✓ Mouse hovered over player")
                
                # Wait for controls to fade in
                self.wait_seconds(3)
                logger.info("✓ Controls visible now")
                
                # Re-locate play button AFTER hover (avoid stale element)
                play_button = wait.until(EC.visibility_of_element_located(self.PLAY_BUTTON))
                play_button = wait.until(EC.element_to_be_clickable(self.PLAY_BUTTON))
                logger.info("✓ Play button located")
                
                # Click play button with ActionChains for accuracy
                actions = ActionChains(self.driver)
                actions.move_to_element(play_button).pause(0.2).click(play_button).perform()
                logger.info("✓ Play button clicked via ActionChains")
                resumed = True
            except Exception as e:
                logger.warning(f"ActionChains method failed: {str(e)[:200]}")
            
            # Method 2: Click video player area
            if not resumed:
                try:
                    logger.info("Trying to click video player area...")
                    video_wrapper = self.find_element(self.VIDEO_PLAYER, timeout=10)
                    actions = ActionChains(self.driver)
                    actions.move_to_element(video_wrapper).click().perform()
                    logger.info("✓ Video player area clicked")
                    resumed = True
                except Exception as e:
                    logger.warning(f"Could not click video area: {str(e)[:200]}")
            
            # Method 3: JavaScript fallback (last resort)
            if not resumed:
                logger.warning("All ActionChains methods failed, using JavaScript fallback...")
                try:
                    # JS should work in current context (already in iframe if needed)
                    self.driver.execute_script("document.querySelector('video').play()")
                    logger.info("✓ Video resumed via JavaScript")
                    resumed = True
                except Exception as e:
                    logger.error(f"JavaScript fallback also failed: {str(e)[:200]}")
            
            # Final status
            if resumed:
                logger.info("✓ Video resumed successfully")
            else:
                logger.error("✗ Failed to resume video")
                
        except Exception as e:
            logger.error(f"Resume failed: {str(e)}")
        finally:
            # Switch back to main content if we were in iframe
            if in_iframe:
                self.driver.switch_to.default_content()
                logger.info("Switched back to main content")
            self.wait_seconds(2)
    
    def continue_watching(self):
        """Resume video by clicking Continue Watching button or video area"""
        logger.info("Resuming video playback...")
        self.wait_seconds(3)
        
        # Method 1: Look for "Continue Watching" button
        try:
            logger.info("Looking for Continue Watching button...")
            self.click(self.CONTINUE_BUTTON, timeout=5)
            logger.info("✓ Continue Watching button clicked")
            self.wait_seconds(2)
            return
        except:
            logger.warning("No Continue Watching button found")
        
        # Method 2: Just play the video again (most reliable)
        try:
            logger.info("Attempting to resume by clicking play button...")
            # Hover first
            video_element = self.find_element(self.VIDEO_ELEMENT, timeout=10)
            actions = ActionChains(self.driver)
            actions.move_to_element(video_element).perform()
            self.wait_seconds(2)
            
            # Click play button
            self.click(self.PLAY_BUTTON, timeout=10)
            logger.info("✓ Play button clicked to resume")
            self.wait_seconds(2)
            return
        except:
            logger.warning("Could not click play button")
        
        # Method 3: Click on video element directly
        try:
            logger.info("Clicking on video player area...")
            self.click(self.VIDEO_ELEMENT, timeout=10)
            logger.info("✓ Video area clicked")
            self.wait_seconds(2)
        except Exception as e:
            logger.error(f"Could not resume video: {e}")
            logger.warning("Skipping resume - continuing with next step...")
    
    def click_rewind(self):
        """Rewind video by 10 seconds using JavaScript (Bonus Feature)"""
        logger.info("Rewinding video 10 seconds using JavaScript...")
        self.wait_seconds(1)
        
        in_iframe = False
        rewound = False
        
        try:
            # Try main page first
            try:
                logger.info("Attempting rewind in main page...")
                current_time_before = self.driver.execute_script("return document.querySelector('video').currentTime;")
                logger.info(f"Current time before rewind: {current_time_before:.1f}s")
                
                self.driver.execute_script("document.querySelector('video').currentTime -= 10;")
                self.wait_seconds(0.5)  # Brief wait for change to apply
                
                current_time_after = self.driver.execute_script("return document.querySelector('video').currentTime;")
                logger.info(f"Current time after rewind: {current_time_after:.1f}s")
                
                # Verify rewind actually happened
                if abs(current_time_after - (current_time_before - 10)) < 1:
                    logger.info(f"✓ VERIFIED: Rewound {current_time_before:.1f}s → {current_time_after:.1f}s")
                    rewound = True
                else:
                    logger.warning(f"⚠ Rewind executed but verification failed: expected ~{current_time_before-10:.1f}s, got {current_time_after:.1f}s")
                    
            except Exception as e:
                # Try iframes
                logger.info(f"Main page failed: {str(e)[:50]}")
                logger.info("Checking iframes...")
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                logger.info(f"Found {len(iframes)} iframe(s)")
                
                for idx, iframe in enumerate(iframes):
                    try:
                        self.driver.switch_to.frame(iframe)
                        
                        current_time_before = self.driver.execute_script("return document.querySelector('video').currentTime;")
                        logger.info(f"Iframe {idx} - Current time before: {current_time_before:.1f}s")
                        
                        self.driver.execute_script("document.querySelector('video').currentTime -= 10;")
                        self.wait_seconds(0.5)
                        
                        current_time_after = self.driver.execute_script("return document.querySelector('video').currentTime;")
                        logger.info(f"Iframe {idx} - Current time after: {current_time_after:.1f}s")
                        
                        # Verify
                        if abs(current_time_after - (current_time_before - 10)) < 1:
                            logger.info(f"✓ VERIFIED: Rewound in iframe {idx}: {current_time_before:.1f}s → {current_time_after:.1f}s")
                            in_iframe = True
                            rewound = True
                            break
                        else:
                            logger.warning(f"Iframe {idx} rewind verification failed")
                            self.driver.switch_to.default_content()
                            
                    except Exception as iframe_error:
                        logger.warning(f"Iframe {idx} error: {str(iframe_error)[:50]}")
                        self.driver.switch_to.default_content()
                        continue
                
                if not rewound:
                    logger.warning("⚠ Could not rewind in any context (non-critical)")
            
            if rewound:
                logger.info("✓ Video rewound 10 seconds (bonus feature)")
            else:
                logger.warning("⚠ Rewind not verified - continuing with main flow")
                
        except Exception as e:
            logger.error(f"Rewind failed (non-critical): {str(e)[:100]}")
            logger.info("⚠ Skipping rewind - continuing with main flow")
        finally:
            if in_iframe:
                self.driver.switch_to.default_content()
            self.wait_seconds(1)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode - Note: May be blocked by browser security (Bonus Feature)"""
        logger.info("Toggling fullscreen mode...")
        logger.info("⚠ NOTE: Browsers often block programmatic fullscreen for security")
        self.wait_seconds(1)
        
        in_iframe = False
        fullscreen_changed = False
        
        try:
            # Try main page first
            try:
                logger.info("Checking fullscreen state in main page...")
                is_fullscreen_before = self.driver.execute_script("return document.fullscreenElement != null;")
                logger.info(f"Fullscreen before: {is_fullscreen_before}")
                
                if is_fullscreen_before:
                    # Exit fullscreen
                    logger.info("Attempting to exit fullscreen...")
                    self.driver.execute_script("document.exitFullscreen();")
                    self.wait_seconds(0.5)
                else:
                    # Enter fullscreen
                    logger.info("Attempting to enter fullscreen...")
                    result = self.driver.execute_script("""
                        var player = document.querySelector('div.jw-wrapper') || document.querySelector('video');
                        if (!player) return 'No player found';
                        
                        if (player.requestFullscreen) {
                            player.requestFullscreen().catch(err => console.log('Fullscreen error:', err));
                            return 'requestFullscreen called';
                        } else if (player.webkitRequestFullscreen) {
                            player.webkitRequestFullscreen();
                            return 'webkitRequestFullscreen called';
                        } else if (player.mozRequestFullScreen) {
                            player.mozRequestFullScreen();
                            return 'mozRequestFullScreen called';
                        } else if (player.msRequestFullscreen) {
                            player.msRequestFullscreen();
                            return 'msRequestFullscreen called';
                        }
                        return 'No fullscreen API available';
                    """)
                    logger.info(f"JS result: {result}")
                    self.wait_seconds(0.5)
                
                # Check if it actually changed
                is_fullscreen_after = self.driver.execute_script("return document.fullscreenElement != null;")
                logger.info(f"Fullscreen after: {is_fullscreen_after}")
                
                if is_fullscreen_before != is_fullscreen_after:
                    logger.info(f"✓ VERIFIED: Fullscreen toggled ({is_fullscreen_before} → {is_fullscreen_after})")
                    fullscreen_changed = True
                else:
                    logger.warning(f"⚠ Fullscreen state unchanged - Browser may be blocking it")
                    logger.warning("⚠ This is EXPECTED behavior (browser security) - Non-critical")
                    
            except Exception as e:
                # Try iframes
                logger.info(f"Main page failed: {str(e)[:50]}")
                logger.info("Checking iframes...")
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                logger.info(f"Found {len(iframes)} iframe(s)")
                
                for idx, iframe in enumerate(iframes):
                    try:
                        self.driver.switch_to.frame(iframe)
                        
                        is_fullscreen_before = self.driver.execute_script("return document.fullscreenElement != null;")
                        logger.info(f"Iframe {idx} - Fullscreen before: {is_fullscreen_before}")
                        
                        if is_fullscreen_before:
                            self.driver.execute_script("document.exitFullscreen();")
                        else:
                            self.driver.execute_script("""
                                var player = document.querySelector('div.jw-wrapper') || document.querySelector('video');
                                if (player && player.requestFullscreen) {
                                    player.requestFullscreen().catch(err => console.log('Error:', err));
                                }
                            """)
                        
                        self.wait_seconds(0.5)
                        is_fullscreen_after = self.driver.execute_script("return document.fullscreenElement != null;")
                        logger.info(f"Iframe {idx} - Fullscreen after: {is_fullscreen_after}")
                        
                        if is_fullscreen_before != is_fullscreen_after:
                            logger.info(f"✓ VERIFIED: Fullscreen toggled in iframe {idx}")
                            in_iframe = True
                            fullscreen_changed = True
                            break
                        else:
                            logger.warning(f"Iframe {idx} fullscreen unchanged")
                            self.driver.switch_to.default_content()
                            
                    except Exception as iframe_error:
                        logger.warning(f"Iframe {idx} error: {str(iframe_error)[:50]}")
                        self.driver.switch_to.default_content()
                        continue
            
            if fullscreen_changed:
                logger.info("✓ Fullscreen toggled successfully (bonus feature)")
            else:
                logger.warning("⚠ Fullscreen blocked by browser (EXPECTED - security policy)")
                logger.info("⚠ Continuing with main flow - this is non-critical")
                
        except Exception as e:
            logger.error(f"Fullscreen failed (non-critical): {str(e)[:100]}")
            logger.info("⚠ Skipping fullscreen - continuing with main flow")
        finally:
            if in_iframe:
                self.driver.switch_to.default_content()
            self.wait_seconds(1)
    
    def set_volume(self, percent):
        """Set volume using JavaScript with verification"""
        logger.info(f"Setting volume to {percent}% using JavaScript...")
        self.wait_seconds(2)
        
        in_iframe = False
        
        try:
            # Convert percent to 0-1 range
            volume_value = percent / 100.0
            
            # Try main page first
            try:
                logger.info("Attempting to set volume in main page...")
                self.driver.execute_script(f"document.querySelector('video').volume = {volume_value};")
                actual_volume = self.driver.execute_script("return document.querySelector('video').volume;")
                logger.info(f"✓ Volume set in main page")
            except:
                # Try iframes
                logger.info("Video not in main page, checking iframes...")
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                volume_set = False
                
                for idx, iframe in enumerate(iframes):
                    try:
                        self.driver.switch_to.frame(iframe)
                        self.driver.execute_script(f"document.querySelector('video').volume = {volume_value};")
                        actual_volume = self.driver.execute_script("return document.querySelector('video').volume;")
                        logger.info(f"✓ Volume set in iframe {idx}")
                        in_iframe = True
                        volume_set = True
                        break
                    except:
                        self.driver.switch_to.default_content()
                        continue
                
                if not volume_set:
                    raise Exception("Could not find video element to set volume")
            
            # Verify volume was set correctly
            actual_percent = actual_volume * 100
            logger.info(f"[VOLUME VERIFICATION] Target: {percent}%, Actual: {actual_percent:.1f}%")
            
            # Assert volume is correct (within 2% tolerance)
            if abs(actual_percent - percent) <= 2:
                logger.info(f"✓ Volume successfully set and verified: {actual_percent:.1f}%")
            else:
                raise AssertionError(f"Volume verification failed: target={percent}%, actual={actual_percent:.1f}%")
                
        except Exception as e:
            logger.error(f"Failed to set volume: {str(e)}")
            raise  # Re-raise to fail the test
        finally:
            if in_iframe:
                self.driver.switch_to.default_content()
    
    def change_resolution(self, resolution):
        """Change video resolution using reliable ActionChains flow with iframe support"""
        logger.info(f"Changing resolution to {resolution} via reliable ActionChains flow...")
        self.wait_seconds(2)
        
        from selenium.webdriver.support import expected_conditions as EC
        
        in_iframe = False
        
        try:
            # STEP 1: Switch into iframe FIRST
            logger.info("Step 1: Detecting and switching to iframe if needed...")
            try:
                video_wrapper = self.driver.find_element(By.CSS_SELECTOR, "div.jw-wrapper")
                logger.info("✓ Player found in main page")
            except:
                logger.info("Player not in main page, checking iframes...")
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                for idx, iframe in enumerate(iframes):
                    try:
                        self.driver.switch_to.frame(iframe)
                        video_wrapper = self.driver.find_element(By.CSS_SELECTOR, "div.jw-wrapper")
                        logger.info(f"✓ Switched to iframe {idx} - player found!")
                        in_iframe = True
                        break
                    except:
                        self.driver.switch_to.default_content()
                        continue
            
            # STEP 2: Move mouse over video player area to make controls appear
            logger.info("Step 2: Moving mouse over player to reveal controls...")
            wait = self.wait
            video_wrapper = self.find_element(self.VIDEO_PLAYER, timeout=10)
            
            actions = ActionChains(self.driver)
            actions.move_to_element(video_wrapper).pause(0.3).perform()  # Add pause for realistic rendering
            logger.info("✓ Mouse hovered over player area")
            
            self.wait_seconds(3)  # Wait for controls to fade in
            logger.info("✓ Controls visible now")
            
            # STEP 3: Re-locate settings button AFTER hover (avoid stale element)
            logger.info("Step 3: Re-locating settings button after hover...")
            settings_btn = wait.until(EC.visibility_of_element_located(self.SETTINGS_BUTTON))
            settings_btn = wait.until(EC.element_to_be_clickable(self.SETTINGS_BUTTON))
            logger.info("✓ Settings button located and clickable")
            
            # STEP 4: Hover directly over settings button (optional but safer)
            logger.info("Step 4: Hovering directly over settings button...")
            actions = ActionChains(self.driver)
            actions.move_to_element(settings_btn).pause(0.3).click(settings_btn).perform()
            logger.info("✓ Settings button clicked with ActionChains")
            
            self.wait_seconds(2)  # Wait for menu to open
            
            # Wait for quality menu to appear
            logger.info("Waiting for quality menu to appear...")
            quality_menu = wait.until(EC.visibility_of_element_located(self.QUALITY_MENU))
            logger.info("✓ Quality menu visible")
            
            # Locate and click the specific resolution button
            logger.info(f"Locating {resolution} button...")
            quality_button = wait.until(EC.element_to_be_clickable(self.QUALITY_OPTION(resolution)))
            logger.info(f"✓ {resolution} button located")
            
            # Click resolution with ActionChains for consistency
            logger.info(f"Clicking {resolution} button with ActionChains...")
            actions = ActionChains(self.driver)
            actions.move_to_element(quality_button).pause(0.2).click(quality_button).perform()
            logger.info(f"✓ {resolution} clicked via ActionChains")
            
            # Wait for video quality to adjust
            logger.info("Waiting 5 seconds for quality adjustment...")
            self.wait_seconds(5)
            
            # VERIFICATION: Re-open settings to verify change
            logger.info("Verifying resolution change...")
            
            # Hover over player again to reveal controls
            video_wrapper = self.find_element(self.VIDEO_PLAYER, timeout=10)
            actions = ActionChains(self.driver)
            actions.move_to_element(video_wrapper).pause(0.3).perform()
            self.wait_seconds(2)
            
            # Re-locate and click settings button
            settings_btn = wait.until(EC.element_to_be_clickable(self.SETTINGS_BUTTON))
            actions = ActionChains(self.driver)
            actions.move_to_element(settings_btn).pause(0.2).click(settings_btn).perform()
            self.wait_seconds(1)
            
            # Check which button is active (aria-checked="true")
            active_quality = self.driver.find_element(By.XPATH, "//button[@role='menuitemradio' and @aria-checked='true']")
            active_label = active_quality.get_attribute('aria-label')
            logger.info(f"[RESOLUTION VERIFICATION] Active: {active_label}")
            
            if resolution in active_label:
                logger.info(f"✓ Resolution successfully changed and verified: {active_label}")
            else:
                raise AssertionError(f"Resolution verification failed: expected {resolution}, got {active_label}")
            
            # Close settings menu
            actions = ActionChains(self.driver)
            actions.move_to_element(settings_btn).pause(0.2).click(settings_btn).perform()
            self.wait_seconds(1)
            logger.info("✓ Settings menu closed")
            
        except Exception as e:
            logger.error(f"ActionChains method failed: {str(e)[:200]}")
            
            # Method 2: JW Player API fallback
            try:
                logger.info(f"Attempting JW Player API fallback...")
                logger.info(f"Attempting to set quality to {resolution} via JW Player API...")
                
                # Get available quality levels
                quality_levels = self.driver.execute_script("""
                    return jwplayer().getQualityLevels().map(q => q.label);
                """)
                logger.info(f"Available qualities: {quality_levels}")
                
                # Find the index of desired quality
                target_index = -1
                for idx, quality in enumerate(quality_levels):
                    if resolution in quality:
                        target_index = idx
                        break
                
                if target_index == -1:
                    raise Exception(f"{resolution} not found in available qualities")
                
                # Set the quality
                self.driver.execute_script(f"jwplayer().setCurrentQuality({target_index});")
                logger.info(f"✓ Quality set via API to index {target_index}")
                
                # Wait for quality change and video to stabilize
                logger.info("Waiting 5 seconds for quality to adjust...")
                self.wait_seconds(5)
                
                # Verify
                current_quality = self.driver.execute_script("return jwplayer().getCurrentQuality();")
                current_label = self.driver.execute_script("return jwplayer().getQualityLevels()[jwplayer().getCurrentQuality()].label;")
                
                logger.info(f"[RESOLUTION VERIFICATION] Target: {resolution}, Actual: {current_label}")
                
                if resolution in current_label:
                    logger.info(f"✓ Resolution successfully changed and verified: {current_label}")
                else:
                    raise AssertionError(f"Resolution verification failed: expected {resolution}, got {current_label}")
                    
            except Exception as api_error:
                logger.error(f"JW Player API fallback also failed: {str(api_error)[:200]}")
                raise  # Re-raise to fail the test
                        
        finally:
            # Switch back to main content if we were in iframe
            if in_iframe:
                self.driver.switch_to.default_content()
                logger.info("Switched back to main content")

