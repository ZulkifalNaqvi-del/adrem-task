"""
Screenshot Handler utility module
Manages screenshot capture for test failures and important steps
"""
import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class ScreenshotHandler:
    """Utility class to handle screenshot capture"""
    
    def __init__(self, driver: WebDriver, screenshot_dir: str = None):
        """
        Initialize ScreenshotHandler
        
        Args:
            driver: Selenium WebDriver instance
            screenshot_dir: Directory to save screenshots (default: screenshots/)
        """
        self.driver = driver
        
        if screenshot_dir is None:
            self.screenshot_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'screenshots'
            )
        else:
            self.screenshot_dir = screenshot_dir
        
        # Create screenshots directory if it doesn't exist
        os.makedirs(self.screenshot_dir, exist_ok=True)
        logger.debug(f"Screenshot directory: {self.screenshot_dir}")
    
    def capture_screenshot(self, name: str = None) -> str:
        """
        Capture screenshot and save to file
        
        Args:
            name: Name for the screenshot file. If None, uses timestamp
            
        Returns:
            Path to the saved screenshot file
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            
            if name:
                # Sanitize the name to remove invalid characters
                name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name)
                filename = f"{name}_{timestamp}.png"
            else:
                filename = f"screenshot_{timestamp}.png"
            
            filepath = os.path.join(self.screenshot_dir, filename)
            
            # Capture screenshot
            self.driver.save_screenshot(filepath)
            logger.info(f"Screenshot captured: {filename}")
            
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return None
    
    def capture_failure_screenshot(self, test_name: str) -> str:
        """
        Capture screenshot for test failure
        
        Args:
            test_name: Name of the failed test
            
        Returns:
            Path to the saved screenshot file
        """
        return self.capture_screenshot(f"FAIL_{test_name}")
    
    def capture_success_screenshot(self, test_name: str) -> str:
        """
        Capture screenshot for successful test step
        
        Args:
            test_name: Name of the test
            
        Returns:
            Path to the saved screenshot file
        """
        return self.capture_screenshot(f"SUCCESS_{test_name}")
    
    @staticmethod
    def cleanup_old_screenshots(directory: str, days_old: int = 7) -> None:
        """
        Clean up screenshots older than specified days
        
        Args:
            directory: Directory containing screenshots
            days_old: Remove screenshots older than this many days
        """
        try:
            current_time = datetime.now()
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if (current_time - file_modified).days > days_old:
                        os.remove(filepath)
                        logger.info(f"Removed old screenshot: {filename}")
        except Exception as e:
            logger.warning(f"Error cleaning up old screenshots: {e}")

