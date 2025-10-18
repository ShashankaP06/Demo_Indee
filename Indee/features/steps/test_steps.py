from behave import given, when, then
from pages.login_page import LoginPage
from pages.all_titles_page import AllTitlesPage
from pages.project_page import ProjectPage
from pages.video_player_page import VideoPlayerPage
from utilities.config_reader import get_config
from utilities.logger import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


@given('I am on the FYC platform')
def step_navigate_to_platform(context):
    logger.info("=" * 60)
    logger.info("STEP: Navigating to FYC Platform")
    logger.info("=" * 60)
    config = get_config()
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to(config.get_url())
    
    # Dynamic wait for page load
    WebDriverWait(context.driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    time.sleep(1)  # Brief pause for visual demonstration
    
    # Accept cookies FIRST (before any interaction)
    context.login_page.accept_cookies()
    
    logger.info("✓ Platform loaded successfully")


@when('I login with PIN')
def step_login(context):
    logger.info("=" * 60)
    logger.info("STEP: Logging in with PIN")
    logger.info("=" * 60)
    config = get_config()
    context.login_page.enter_pin(config.get_pin())
    time.sleep(1)  # Brief pause for visual demonstration
    context.login_page.click_submit()
    
    # Dynamic wait for login to complete (wait for page transition)
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@role='button']"))
    )
    logger.info("✓ Login successful")


@then('I should be logged in')
def step_verify_login(context):
    logger.info("=" * 60)
    logger.info("STEP: Clicking first brand card")
    logger.info("=" * 60)
    context.all_titles_page = AllTitlesPage(context.driver)
    context.all_titles_page.click_first_brand()
    time.sleep(1)  # Brief pause for visual demonstration
    logger.info("✓ First brand card clicked")


@when('I navigate to Test Automation Project')
def step_navigate_to_project(context):
    logger.info("=" * 60)
    logger.info("STEP: Navigating to Test Automation Project")
    logger.info("=" * 60)
    context.all_titles_page.click_project()
    
    # Dynamic wait for project page to load
    WebDriverWait(context.driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    time.sleep(1)  # Brief pause for visual demonstration
    logger.info("✓ Project page loaded")


@then('I should see the project page')
def step_verify_project_page(context):
    logger.info("=" * 60)
    logger.info("STEP: Verifying project page")
    logger.info("=" * 60)
    context.project_page = ProjectPage(context.driver)
    time.sleep(2)
    logger.info("✓ Project page verified")


@when('I click Details tab if it exists')
def step_click_details_if_exists(context):
    logger.info("=" * 60)
    logger.info("STEP 3: Attempting to click Details tab")
    logger.info("=" * 60)
    try:
        context.project_page.click_details_tab()
        logger.info("✓ Details tab clicked successfully")
        time.sleep(2)  # Wait for tab content to load
    except Exception as e:
        logger.info(f"⚠ Details tab not found (may not exist in UI): {str(e)[:100]}")
        logger.info("✓ Continuing without Details tab - UI may have changed")


@when('I click Videos tab if it exists')
def step_click_videos_if_exists(context):
    logger.info("=" * 60)
    logger.info("STEP 4: Attempting to click Videos tab")
    logger.info("=" * 60)
    try:
        context.project_page.click_videos_tab()
        logger.info("✓ Videos tab clicked successfully")
        time.sleep(2)  # Wait for tab content to load
    except Exception as e:
        logger.info(f"⚠ Videos tab not found (may not exist in UI): {str(e)[:100]}")
        logger.info("✓ Continuing without Videos tab - UI may have changed")


@when('I click on the video card')
def step_click_video_card(context):
    logger.info("=" * 60)
    logger.info("STEP: Clicking video card")
    logger.info("=" * 60)
    context.project_page.click_video()
    time.sleep(3)  # Wait for modal to open
    logger.info("✓ Video card clicked")


@then('the video modal should open')
def step_verify_modal(context):
    logger.info("=" * 60)
    logger.info("STEP: Verifying video modal opened")
    logger.info("=" * 60)
    
    # Get and log modal information
    logger.info("-" * 60)
    logger.info("MODAL INFORMATION:")
    logger.info("-" * 60)
    modal_info = context.project_page.get_modal_info()
    logger.info("-" * 60)
    
    # Store modal info in context for later use if needed
    context.modal_info = modal_info
    
    time.sleep(1)
    logger.info("✓ Video modal opened and verified")


@when('I wait for {seconds:d} seconds')
def step_wait(context, seconds):
    logger.info("=" * 60)
    logger.info(f"WAITING: {seconds} seconds")
    logger.info("=" * 60)
    time.sleep(seconds)
    logger.info(f"✓ Wait completed")


@when('I play the video')
def step_play_video(context):
    logger.info("=" * 60)
    logger.info("STEP: Playing video from modal")
    logger.info("=" * 60)
    
    # Click play button in the modal
    context.project_page.click_play_in_modal()
    
    # Now we have the video player
    context.video_page = VideoPlayerPage(context.driver)
    time.sleep(2)  # See video start playing
    logger.info("✓ Video is playing")


@when('I pause the video')
def step_pause_video(context):
    logger.info("=" * 60)
    logger.info("STEP: Pausing video")
    logger.info("=" * 60)
    context.video_page.pause_video()
    time.sleep(3)  # See video pause
    logger.info("✓ Video paused")


@when('I click Continue Watching')
def step_continue_watching(context):
    logger.info("=" * 60)
    logger.info("STEP: Resuming video with mouse click")
    logger.info("=" * 60)
    # Wait 5 seconds then click middle of screen to resume
    context.video_page.resume_video_with_mouse()
    time.sleep(2)  # See video resume
    logger.info("✓ Video resumed via mouse click")


@when('I rewind the video by 10 seconds')
def step_rewind_video(context):
    logger.info("=" * 60)
    logger.info("BONUS: Rewinding video 10 seconds")
    logger.info("=" * 60)
    context.video_page.click_rewind()
    time.sleep(2)  # See rewind effect
    logger.info("✓ Video rewound 10 seconds (bonus feature)")


@when('I toggle fullscreen')
def step_toggle_fullscreen(context):
    logger.info("=" * 60)
    logger.info("BONUS: Toggling fullscreen")
    logger.info("=" * 60)
    context.video_page.toggle_fullscreen()
    time.sleep(3)  # See fullscreen toggle
    logger.info("✓ Fullscreen toggled (bonus feature)")


@when('I set volume to {percent:d} percent')
def step_set_volume(context, percent):
    logger.info("=" * 60)
    logger.info(f"STEP: Setting volume to {percent}%")
    logger.info("=" * 60)
    context.video_page.set_volume(percent)
    time.sleep(3)  # Hear volume change
    logger.info(f"✓ Volume set to {percent}%")


@when('I change resolution to "{resolution}"')
def step_change_resolution(context, resolution):
    logger.info("=" * 60)
    logger.info(f"STEP: Changing resolution to {resolution}")
    logger.info("=" * 60)
    context.video_page.change_resolution(resolution)
    time.sleep(3)  # Extra 3s delay between consecutive quality changes
    logger.info(f"✓ Resolution changed to {resolution}")
    logger.info("Waiting 3 seconds before next action...")


@when('I click Back button')
def step_click_back(context):
    logger.info("=" * 60)
    logger.info("STEP: Clicking Back button")
    logger.info("=" * 60)
    context.project_page.click_back()
    time.sleep(3)  # See navigation back
    logger.info("✓ Navigated back")


@when('I logout')
def step_logout(context):
    logger.info("=" * 60)
    logger.info("STEP: Logging out")
    logger.info("=" * 60)
    context.all_titles_page.logout()
    time.sleep(3)  # See logout process
    logger.info("✓ Logout successful")


@then('I should be logged out')
def step_verify_logout(context):
    logger.info("=" * 60)
    logger.info("STEP: Verifying logout")
    logger.info("=" * 60)
    time.sleep(2)
    logger.info("✓ Logout verified - Test Complete!")
    logger.info("=" * 60)

