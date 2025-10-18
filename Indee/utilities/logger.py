import logging
import sys
from datetime import datetime

# Initialize colorama for Windows compatibility
try:
    from colorama import Fore, Back, Style
    USE_COLORAMA = True
except ImportError:
    # Fallback if colorama not installed
    class Fore:
        GREEN = ''
        YELLOW = ''
        RED = ''
        CYAN = ''
        MAGENTA = ''
    
    class Style:
        RESET_ALL = ''
    
    USE_COLORAMA = False


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output (Windows compatible with colorama)"""
    
    # Use colorama colors (works on Windows after just_fix_windows_console())
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA,
    }
    
    def format(self, record):
        # Add color to level name and message
        levelname = record.levelname
        if levelname in self.COLORS:
            color = self.COLORS[levelname]
            # Color the level name
            record.levelname = f"{color}{levelname}{Style.RESET_ALL}"
            # Color the message as well for better visibility
            record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


def setup_logger(name='AutomationFramework'):
    """Setup and return a configured logger"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with custom formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Format: [TIME] [LEVEL] Message
    formatter = ColoredFormatter(
        fmt='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Create a global logger instance
logger = setup_logger()

