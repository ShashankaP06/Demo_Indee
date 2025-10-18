# Initialize colorama for Windows ANSI color support
try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
except:
    pass

from utilities.driver_factory import DriverFactory
from utilities.logger import logger


def before_scenario(context, scenario):
    """Setup before each scenario"""
    logger.info("\n" + "=" * 60)
    logger.info("Starting Chrome Browser...")
    logger.info("=" * 60)
    context.driver = DriverFactory.create_driver()


def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    logger.info("\n" + "=" * 60)
    logger.info("Closing browser...")
    logger.info("=" * 60)
    try:
        context.driver.quit()
    except:
        pass

