"""
Home Page Object Model
Handles homepage and product search functionality
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class HomePage(BasePage):
    """Page Object for Home Page - Single Responsibility Principle"""
    
    # Locators
    SEARCH_BOX = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".button-1.search-box-button")
    LOGO = (By.CSS_SELECTOR, ".header-logo")
    
    # Product Categories
    BOOKS_LINK = (By.XPATH, "//a[contains(@href, '/books')][@class='']")
    COMPUTERS_LINK = (By.XPATH, "//a[contains(@href, '/computers')][@class='']")
    ELECTRONICS_LINK = (By.XPATH, "//a[contains(@href, '/electronics')][@class='']")
    
    # Featured Products
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, ".product-item")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-title a")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".button-2.product-box-add-to-cart-button")
    
    # Cart
    SHOPPING_CART_LINK = (By.LINK_TEXT, "Shopping cart")
    CART_QTY = (By.CSS_SELECTOR, ".cart-qty")
    
    def __init__(self, driver):
        """Initialize HomePage"""
        super().__init__(driver)
        logger.info("HomePage initialized")
    
    def search_product(self, product_name: str) -> None:
        """
        Search for a product
        
        Args:
            product_name: Name of product to search
        """
        try:
            logger.info(f"Searching for product: {product_name}")
            self.send_keys(self.SEARCH_BOX, product_name)
            self.click(self.SEARCH_BUTTON)
            logger.info(f"Search initiated for: {product_name}")
        except Exception as e:
            logger.error(f"Failed to search product: {e}")
            self.capture_screenshot("product_search_failed")
            raise
    
    def navigate_to_category(self, category: str) -> None:
        """
        Navigate to product category
        
        Args:
            category: Category name (books, computers, electronics)
        """
        try:
            logger.info(f"Navigating to category: {category}")
            category_lower = category.lower()
            
            if category_lower == "books":
                self.click(self.BOOKS_LINK)
            elif category_lower == "computers":
                self.click(self.COMPUTERS_LINK)
            elif category_lower == "electronics":
                self.click(self.ELECTRONICS_LINK)
            else:
                raise ValueError(f"Unknown category: {category}")
            
            logger.info(f"Navigated to {category} category")
        except Exception as e:
            logger.error(f"Failed to navigate to category: {e}")
            self.capture_screenshot("category_navigation_failed")
            raise
    
    def get_featured_products_count(self) -> int:
        """
        Get count of featured products on homepage
        
        Returns:
            Number of featured products
        """
        try:
            products = self.find_elements(self.FEATURED_PRODUCTS)
            count = len(products)
            logger.info(f"Found {count} featured products")
            return count
        except Exception as e:
            logger.error(f"Failed to get featured products count: {e}")
            return 0
    
    def get_product_titles(self) -> list:
        """
        Get all product titles on the page
        
        Returns:
            List of product titles
        """
        try:
            title_elements = self.find_elements(self.PRODUCT_TITLES)
            titles = [elem.text for elem in title_elements if elem.text]
            logger.info(f"Found {len(titles)} product titles")
            return titles
        except Exception as e:
            logger.error(f"Failed to get product titles: {e}")
            return []
    
    def navigate_to_shopping_cart(self) -> None:
        """Navigate to shopping cart"""
        try:
            logger.info("Navigating to shopping cart")
            self.click(self.SHOPPING_CART_LINK)
            logger.info("Successfully navigated to shopping cart")
        except Exception as e:
            logger.error(f"Failed to navigate to shopping cart: {e}")
            self.capture_screenshot("cart_navigation_failed")
            raise
    
    def get_cart_quantity(self) -> str:
        """
        Get current cart quantity
        
        Returns:
            Cart quantity as string
        """
        try:
            qty = self.get_text(self.CART_QTY)
            logger.info(f"Current cart quantity: {qty}")
            return qty
        except Exception as e:
            logger.warning(f"Failed to get cart quantity: {e}")
            return "0"
    
    def click_logo(self) -> None:
        """Click on site logo to return to homepage"""
        try:
            logger.info("Clicking logo to return to homepage")
            self.click(self.LOGO)
            logger.info("Returned to homepage")
        except Exception as e:
            logger.error(f"Failed to click logo: {e}")
            raise

