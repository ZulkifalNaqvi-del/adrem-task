"""
Base Page Module
Implements common functionality for all page objects (DRY Principle)
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementNotInteractableException,
    StaleElementReferenceException
)
from typing import List, Tuple
from utils.logger import Logger
from utils.screenshot_handler import ScreenshotHandler

logger = Logger.get_logger(__name__)


class BasePage:
    """
    Base page class with common methods for all page objects
    Implements DRY principle and Fail Fast principle
    """
    
    def __init__(self, driver: WebDriver, timeout: int = 20):
        """
        Initialize BasePage
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for explicit waits
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.screenshot_handler = ScreenshotHandler(driver)
        logger.debug(f"Initialized {self.__class__.__name__}")
    
    def find_element(self, locator: Tuple[By, str]) -> WebElement:
        """
        Find single element with explicit wait (Fail Fast)
        
        Args:
            locator: Tuple of (By, locator_string)
            
        Returns:
            WebElement if found
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"Found element: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found within {self.timeout}s: {locator}")
            self.screenshot_handler.capture_screenshot(f"element_not_found_{locator[1]}")
            raise
    
    def find_elements(self, locator: Tuple[By, str]) -> List[WebElement]:
        """
        Find multiple elements with explicit wait
        
        Args:
            locator: Tuple of (By, locator_string)
            
        Returns:
            List of WebElements
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found within {self.timeout}s: {locator}")
            return []
    
    def click(self, locator: Tuple[By, str]) -> None:
        """
        Click on element with wait for clickable state
        
        Args:
            locator: Tuple of (By, locator_string)
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.info(f"Clicked element: {locator}")
        except (TimeoutException, ElementNotInteractableException) as e:
            logger.error(f"Failed to click element: {locator}. Error: {e}")
            self.screenshot_handler.capture_screenshot(f"click_failed_{locator[1]}")
            raise
    
    def send_keys(self, locator: Tuple[By, str], text: str, clear_first: bool = True) -> None:
        """
        Send keys to element
        
        Args:
            locator: Tuple of (By, locator_string)
            text: Text to send
            clear_first: Clear field before sending keys (default: True)
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"Sent keys to element: {locator}")
        except (TimeoutException, ElementNotInteractableException) as e:
            logger.error(f"Failed to send keys to element: {locator}. Error: {e}")
            self.screenshot_handler.capture_screenshot(f"sendkeys_failed_{locator[1]}")
            raise
    
    def get_text(self, locator: Tuple[By, str]) -> str:
        """
        Get text from element
        
        Args:
            locator: Tuple of (By, locator_string)
            
        Returns:
            Text content of element
        """
        try:
            element = self.find_element(locator)
            text = element.text
            logger.debug(f"Got text from element: {locator} -> '{text}'")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element: {locator}. Error: {e}")
            raise
    
    def get_attribute(self, locator: Tuple[By, str], attribute: str) -> str:
        """
        Get attribute value from element
        
        Args:
            locator: Tuple of (By, locator_string)
            attribute: Attribute name
            
        Returns:
            Attribute value
        """
        try:
            element = self.find_element(locator)
            value = element.get_attribute(attribute)
            logger.debug(f"Got attribute '{attribute}' from element: {locator} -> '{value}'")
            return value
        except Exception as e:
            logger.error(f"Failed to get attribute from element: {locator}. Error: {e}")
            raise
    
    def is_element_visible(self, locator: Tuple[By, str], timeout: int = None) -> bool:
        """
        Check if element is visible
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Custom timeout (uses default if None)
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            logger.debug(f"Element is not visible: {locator}")
            return False
    
    def is_element_present(self, locator: Tuple[By, str], timeout: int = None) -> bool:
        """
        Check if element is present in DOM
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Custom timeout (uses default if None)
            
        Returns:
            True if element is present, False otherwise
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"Element is present: {locator}")
            return True
        except TimeoutException:
            logger.debug(f"Element is not present: {locator}")
            return False
    
    def wait_for_element_to_disappear(self, locator: Tuple[By, str], timeout: int = None) -> bool:
        """
        Wait for element to disappear from DOM
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Custom timeout (uses default if None)
            
        Returns:
            True if element disappeared, False otherwise
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.invisibility_of_element_located(locator))
            logger.debug(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            logger.debug(f"Element still visible: {locator}")
            return False
    
    def select_dropdown_by_text(self, locator: Tuple[By, str], text: str) -> None:
        """
        Select dropdown option by visible text
        
        Args:
            locator: Tuple of (By, locator_string)
            text: Visible text to select
        """
        try:
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_visible_text(text)
            logger.info(f"Selected dropdown option: {text}")
        except Exception as e:
            logger.error(f"Failed to select dropdown option: {locator}. Error: {e}")
            self.screenshot_handler.capture_screenshot(f"dropdown_failed_{locator[1]}")
            raise
    
    def select_dropdown_by_value(self, locator: Tuple[By, str], value: str) -> None:
        """
        Select dropdown option by value attribute
        
        Args:
            locator: Tuple of (By, locator_string)
            value: Value attribute to select
        """
        try:
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_value(value)
            logger.info(f"Selected dropdown value: {value}")
        except Exception as e:
            logger.error(f"Failed to select dropdown value: {locator}. Error: {e}")
            raise
    
    def scroll_to_element(self, locator: Tuple[By, str]) -> None:
        """
        Scroll element into view
        
        Args:
            locator: Tuple of (By, locator_string)
        """
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            logger.debug(f"Scrolled to element: {locator}")
        except Exception as e:
            logger.error(f"Failed to scroll to element: {locator}. Error: {e}")
            raise
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        url = self.driver.current_url
        logger.debug(f"Current URL: {url}")
        return url
    
    def get_page_title(self) -> str:
        """Get current page title"""
        title = self.driver.title
        logger.debug(f"Page title: {title}")
        return title
    
    def refresh_page(self) -> None:
        """Refresh current page"""
        self.driver.refresh()
        logger.info("Page refreshed")
    
    def navigate_back(self) -> None:
        """Navigate back in browser history"""
        self.driver.back()
        logger.info("Navigated back")
    
    def switch_to_alert(self):
        """
        Switch to alert
        
        Returns:
            Alert object
        """
        try:
            alert = self.wait.until(EC.alert_is_present())
            logger.info("Switched to alert")
            return alert
        except TimeoutException:
            logger.error("Alert not present")
            raise
    
    def accept_alert(self) -> None:
        """Accept alert"""
        try:
            alert = self.switch_to_alert()
            alert.accept()
            logger.info("Alert accepted")
        except Exception as e:
            logger.error(f"Failed to accept alert. Error: {e}")
            raise
    
    def dismiss_alert(self) -> None:
        """Dismiss alert"""
        try:
            alert = self.switch_to_alert()
            alert.dismiss()
            logger.info("Alert dismissed")
        except Exception as e:
            logger.error(f"Failed to dismiss alert. Error: {e}")
            raise
    
    def capture_screenshot(self, name: str = None) -> str:
        """
        Capture screenshot
        
        Args:
            name: Screenshot name
            
        Returns:
            Path to screenshot file
        """
        return self.screenshot_handler.capture_screenshot(name)

