"""
Product Page Object Model
Handles product listing and individual product page functionality
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class ProductPage(BasePage):
    """Page Object for Product Page - Single Responsibility Principle"""
    
    # Search Results Page Locators
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".product-item")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-title a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".actual-price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".button-2.product-box-add-to-cart-button")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, ".no-result")
    
    # Individual Product Page Locators
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-name h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".price-value-22")
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".qty-input")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-button-22")
    ADD_TO_CART_BUTTON_GENERIC = (By.CSS_SELECTOR, ".button-1.add-to-cart-button")
    SUCCESS_NOTIFICATION = (By.CSS_SELECTOR, ".bar-notification.success")
    NOTIFICATION_CLOSE = (By.CSS_SELECTOR, ".close")
    SHOPPING_CART_LINK_NOTIFICATION = (By.XPATH, "//a[text()='shopping cart']")
    
    def __init__(self, driver):
        """Initialize ProductPage"""
        super().__init__(driver)
        logger.info("ProductPage initialized")
    
    def get_search_results_count(self) -> int:
        """
        Get number of products in search results
        
        Returns:
            Number of products found
        """
        try:
            products = self.find_elements(self.SEARCH_RESULTS)
            count = len(products)
            logger.info(f"Found {count} products in search results")
            return count
        except Exception as e:
            logger.error(f"Failed to get search results count: {e}")
            return 0
    
    def get_product_titles(self) -> list:
        """
        Get all product titles from search results
        
        Returns:
            List of product titles
        """
        try:
            title_elements = self.find_elements(self.PRODUCT_TITLES)
            titles = [elem.text for elem in title_elements if elem.text]
            logger.info(f"Retrieved {len(titles)} product titles")
            return titles
        except Exception as e:
            logger.error(f"Failed to get product titles: {e}")
            return []
    
    def click_product_by_index(self, index: int = 0) -> None:
        """
        Click on a product by index in search results
        
        Args:
            index: Index of product to click (0-based)
        """
        try:
            logger.info(f"Clicking product at index: {index}")
            product_titles = self.find_elements(self.PRODUCT_TITLES)
            
            if index < len(product_titles):
                product_titles[index].click()
                logger.info(f"Clicked product at index {index}")
            else:
                raise IndexError(f"Product index {index} out of range. Found {len(product_titles)} products")
        except Exception as e:
            logger.error(f"Failed to click product: {e}")
            self.capture_screenshot("product_click_failed")
            raise
    
    def click_product_by_name(self, product_name: str) -> None:
        """
        Click on a product by name in search results
        
        Args:
            product_name: Name of product to click
        """
        try:
            logger.info(f"Clicking product: {product_name}")
            product_locator = (By.LINK_TEXT, product_name)
            self.click(product_locator)
            logger.info(f"Clicked product: {product_name}")
        except Exception as e:
            logger.error(f"Failed to click product by name: {e}")
            self.capture_screenshot("product_by_name_click_failed")
            raise
    
    def add_to_cart_from_listing(self, index: int = 0) -> None:
        """
        Add product to cart directly from product listing
        
        Args:
            index: Index of product to add (0-based)
        """
        try:
            logger.info(f"Adding product to cart from listing at index: {index}")
            add_to_cart_buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
            
            if index < len(add_to_cart_buttons):
                add_to_cart_buttons[index].click()
                logger.info(f"Added product at index {index} to cart")
                
                # Wait for success notification
                if self.is_element_visible(self.SUCCESS_NOTIFICATION, timeout=5):
                    logger.info("Product added successfully - notification displayed")
            else:
                raise IndexError(f"Product index {index} out of range")
        except Exception as e:
            logger.error(f"Failed to add product to cart from listing: {e}")
            self.capture_screenshot("add_to_cart_listing_failed")
            raise
    
    def get_product_name_on_page(self) -> str:
        """
        Get product name from individual product page
        
        Returns:
            Product name
        """
        try:
            name = self.get_text(self.PRODUCT_NAME)
            logger.info(f"Product name: {name}")
            return name
        except Exception as e:
            logger.error(f"Failed to get product name: {e}")
            return ""
    
    def get_product_price_on_page(self) -> str:
        """
        Get product price from individual product page
        
        Returns:
            Product price
        """
        try:
            price = self.get_text(self.PRODUCT_PRICE)
            logger.info(f"Product price: {price}")
            return price
        except Exception as e:
            logger.error(f"Failed to get product price: {e}")
            return ""
    
    def set_quantity(self, quantity: int) -> None:
        """
        Set product quantity
        
        Args:
            quantity: Quantity to set
        """
        try:
            logger.info(f"Setting quantity to: {quantity}")
            self.send_keys(self.QUANTITY_INPUT, str(quantity))
            logger.info(f"Quantity set to {quantity}")
        except Exception as e:
            logger.warning(f"Failed to set quantity (element may not exist): {e}")
    
    def add_to_cart(self) -> bool:
        """
        Add product to cart from individual product page
        
        Returns:
            True if product added successfully, False otherwise
        """
        try:
            logger.info("Adding product to cart")
            
            # Try generic add to cart button
            if self.is_element_present(self.ADD_TO_CART_BUTTON_GENERIC, timeout=3):
                self.click(self.ADD_TO_CART_BUTTON_GENERIC)
            else:
                # Fallback to specific button ID
                self.click(self.ADD_TO_CART_BUTTON)
            
            # Wait for success notification
            if self.is_element_visible(self.SUCCESS_NOTIFICATION, timeout=10):
                logger.info("Product added to cart successfully")
                self.capture_screenshot("product_added_to_cart")
                return True
            else:
                logger.warning("Add to cart notification not displayed")
                return False
                
        except Exception as e:
            logger.error(f"Failed to add product to cart: {e}")
            self.capture_screenshot("add_to_cart_failed")
            raise
    
    def close_notification(self) -> None:
        """Close success notification bar"""
        try:
            if self.is_element_visible(self.NOTIFICATION_CLOSE, timeout=3):
                self.click(self.NOTIFICATION_CLOSE)
                logger.info("Closed notification bar")
        except Exception as e:
            logger.warning(f"Failed to close notification: {e}")
    
    def is_notification_displayed(self) -> bool:
        """
        Check if success notification is displayed
        
        Returns:
            True if notification visible, False otherwise
        """
        return self.is_element_visible(self.SUCCESS_NOTIFICATION, timeout=5)
    
    def navigate_to_cart_from_notification(self) -> None:
        """Navigate to shopping cart from notification bar"""
        try:
            logger.info("Navigating to cart from notification")
            self.click(self.SHOPPING_CART_LINK_NOTIFICATION)
            logger.info("Navigated to cart from notification")
        except Exception as e:
            logger.error(f"Failed to navigate to cart from notification: {e}")
            raise

