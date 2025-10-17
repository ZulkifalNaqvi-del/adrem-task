"""
Cart Page Object Model
Handles shopping cart functionality
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class CartPage(BasePage):
    """Page Object for Shopping Cart Page - Single Responsibility Principle"""
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item-row")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-name")
    UNIT_PRICES = (By.CSS_SELECTOR, ".product-unit-price")
    QUANTITIES = (By.CSS_SELECTOR, ".qty-input")
    SUBTOTALS = (By.CSS_SELECTOR, ".product-subtotal")
    REMOVE_CHECKBOXES = (By.CSS_SELECTOR, ".remove-from-cart input[type='checkbox']")
    UPDATE_CART_BUTTON = (By.CSS_SELECTOR, ".button-2.update-cart-button")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, ".button-2.continue-shopping-button")
    
    # Cart Totals
    CART_TOTAL = (By.CSS_SELECTOR, ".cart-total-right .value-summary strong")
    ORDER_TOTAL = (By.CSS_SELECTOR, ".order-total .cart-total-right strong")
    
    # Checkout
    TERMS_OF_SERVICE_CHECKBOX = (By.ID, "termsofservice")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    
    # Empty Cart
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".order-summary-content")
    
    def __init__(self, driver):
        """Initialize CartPage"""
        super().__init__(driver)
        logger.info("CartPage initialized")
    
    def get_cart_items_count(self) -> int:
        """
        Get number of items in cart
        
        Returns:
            Number of items in cart
        """
        try:
            items = self.find_elements(self.CART_ITEMS)
            count = len(items)
            logger.info(f"Cart contains {count} items")
            return count
        except Exception as e:
            logger.error(f"Failed to get cart items count: {e}")
            return 0
    
    def get_product_names(self) -> list:
        """
        Get all product names in cart
        
        Returns:
            List of product names
        """
        try:
            name_elements = self.find_elements(self.PRODUCT_NAMES)
            names = [elem.text.strip() for elem in name_elements if elem.text]
            logger.info(f"Products in cart: {names}")
            return names
        except Exception as e:
            logger.error(f"Failed to get product names: {e}")
            return []
    
    def get_product_prices(self) -> list:
        """
        Get all product unit prices in cart
        
        Returns:
            List of prices as strings
        """
        try:
            price_elements = self.find_elements(self.UNIT_PRICES)
            prices = [elem.text.strip() for elem in price_elements if elem.text]
            logger.info(f"Product prices: {prices}")
            return prices
        except Exception as e:
            logger.error(f"Failed to get product prices: {e}")
            return []
    
    def get_product_quantities(self) -> list:
        """
        Get quantities of all products in cart
        
        Returns:
            List of quantities
        """
        try:
            qty_elements = self.find_elements(self.QUANTITIES)
            quantities = [elem.get_attribute('value') for elem in qty_elements]
            logger.info(f"Product quantities: {quantities}")
            return quantities
        except Exception as e:
            logger.error(f"Failed to get product quantities: {e}")
            return []
    
    def update_quantity(self, product_index: int, quantity: int) -> None:
        """
        Update quantity for a specific product
        
        Args:
            product_index: Index of product (0-based)
            quantity: New quantity
        """
        try:
            logger.info(f"Updating quantity for product {product_index} to {quantity}")
            qty_elements = self.find_elements(self.QUANTITIES)
            
            if product_index < len(qty_elements):
                qty_input = qty_elements[product_index]
                qty_input.clear()
                qty_input.send_keys(str(quantity))
                logger.info(f"Set quantity to {quantity}")
            else:
                raise IndexError(f"Product index {product_index} out of range")
                
        except Exception as e:
            logger.error(f"Failed to update quantity: {e}")
            raise
    
    def click_update_cart(self) -> None:
        """Click Update Shopping Cart button"""
        try:
            logger.info("Clicking Update Cart button")
            self.click(self.UPDATE_CART_BUTTON)
            logger.info("Cart updated")
        except Exception as e:
            logger.error(f"Failed to update cart: {e}")
            raise
    
    def remove_product(self, product_index: int) -> None:
        """
        Remove a product from cart
        
        Args:
            product_index: Index of product to remove (0-based)
        """
        try:
            logger.info(f"Removing product at index {product_index}")
            remove_checkboxes = self.find_elements(self.REMOVE_CHECKBOXES)
            
            if product_index < len(remove_checkboxes):
                remove_checkboxes[product_index].click()
                self.click_update_cart()
                logger.info(f"Removed product at index {product_index}")
            else:
                raise IndexError(f"Product index {product_index} out of range")
                
        except Exception as e:
            logger.error(f"Failed to remove product: {e}")
            self.capture_screenshot("remove_product_failed")
            raise
    
    def get_cart_total(self) -> str:
        """
        Get cart total amount
        
        Returns:
            Cart total as string
        """
        try:
            # Wait a bit for cart to load
            import time
            time.sleep(2)
            
            # Try multiple locators for cart total
            total_locators = [
                (By.CSS_SELECTOR, ".order-total .cart-total-right strong"),
                (By.CSS_SELECTOR, ".order-total strong"),
                (By.XPATH, "//div[@class='order-total']//strong"),
                (By.XPATH, "//*[contains(@class, 'order-total')]//strong"),
                (By.CSS_SELECTOR, ".cart-total strong"),
                (By.XPATH, "//span[@class='order-total']//strong"),
            ]
            
            total = ""
            for locator in total_locators:
                try:
                    if self.is_element_present(locator, timeout=2):
                        total = self.get_text(locator)
                        if total:
                            break
                except:
                    continue
            
            # If still no total, try getting any total from the page
            if not total:
                try:
                    all_strongs = self.driver.find_elements(By.TAG_NAME, "strong")
                    for strong in all_strongs:
                        text = strong.text.strip()
                        if text and '$' in text and text[0].isdigit() or text.startswith('$'):
                            total = text
                            logger.info(f"Found total using fallback method: {total}")
                            break
                except:
                    pass
            
            if total:
                logger.info(f"Cart total: {total}")
            else:
                logger.warning("Could not find cart total, but continuing...")
                total = "Total not displayed"
            
            return total
        except Exception as e:
            logger.error(f"Failed to get cart total: {e}")
            return "Total retrieval failed"
    
    def is_cart_empty(self) -> bool:
        """
        Check if cart is empty
        
        Returns:
            True if cart is empty, False otherwise
        """
        try:
            is_empty = self.is_element_visible(self.EMPTY_CART_MESSAGE, timeout=5)
            logger.info(f"Cart empty status: {is_empty}")
            return is_empty
        except Exception as e:
            logger.error(f"Failed to check if cart is empty: {e}")
            return False
    
    def accept_terms_of_service(self) -> None:
        """Check the Terms of Service checkbox"""
        try:
            logger.info("Accepting Terms of Service")
            self.click(self.TERMS_OF_SERVICE_CHECKBOX)
            logger.info("Terms of Service accepted")
        except Exception as e:
            logger.error(f"Failed to accept terms of service: {e}")
            self.capture_screenshot("terms_acceptance_failed")
            raise
    
    def click_checkout(self) -> None:
        """Click Checkout button"""
        try:
            logger.info("Clicking Checkout button")
            self.click(self.CHECKOUT_BUTTON)
            logger.info("Navigated to checkout")
        except Exception as e:
            logger.error(f"Failed to click checkout: {e}")
            self.capture_screenshot("checkout_click_failed")
            raise
    
    def proceed_to_checkout(self) -> None:
        """
        Complete flow to proceed to checkout
        Accepts terms and clicks checkout button
        """
        try:
            logger.info("Proceeding to checkout")
            self.accept_terms_of_service()
            self.click_checkout()
            logger.info("Successfully proceeded to checkout")
        except Exception as e:
            logger.error(f"Failed to proceed to checkout: {e}")
            self.capture_screenshot("proceed_to_checkout_failed")
            raise
    
    def continue_shopping(self) -> None:
        """Click Continue Shopping button"""
        try:
            logger.info("Continuing shopping")
            self.click(self.CONTINUE_SHOPPING_BUTTON)
            logger.info("Returned to shopping")
        except Exception as e:
            logger.error(f"Failed to continue shopping: {e}")
            raise
    
    def validate_cart_contents(self, expected_item_count: int) -> bool:
        """
        Validate cart contents
        
        Args:
            expected_item_count: Expected number of items
            
        Returns:
            True if validation passes, False otherwise
        """
        try:
            actual_count = self.get_cart_items_count()
            
            if actual_count == expected_item_count:
                logger.info(f"Cart validation passed: {actual_count} items")
                return True
            else:
                logger.error(f"Cart validation failed. Expected: {expected_item_count}, Actual: {actual_count}")
                return False
                
        except Exception as e:
            logger.error(f"Cart validation error: {e}")
            return False

